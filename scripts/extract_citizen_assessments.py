#!/usr/bin/env python3
"""
extract_citizen_assessments.py
==============================
Country-agnostic extraction of foundational-learning and household indicators
from Citizen-Led Assessment (CLA) data: Uwezo (Kenya, Tanzania, Uganda), PAL
Network ICAN/ICAR, ASER-style files, as child/household microdata OR district
summary tables.

Usage
-----
    python extract_citizen_assessments.py --input uwezo_2015.csv --country KEN \
        --output uwezo_KEN_latest.json

Inputs: .csv, .xlsx/.xls (needs openpyxl/xlrd), and also .dta/.sav (needs
pyreadstat), because Uwezo household data is distributed as Stata files and
those carry the variable/value labels this script relies on.

Indicators (0-100 scale; every estimate carries its valid N)
------------------------------------------------------------
 foundational_literacy   % of children in Grades 3-5 reading a Grade 2 story
                         (national / urban / rural / male / female)
 foundational_numeracy   % of children in Grades 3-5 at "subtraction" level or
                         above (subtraction, multiplication or division)
 out_of_school_children  % of children aged 6-16 not enrolled
 household_technology    % of households with a radio, a television and a
                         mobile phone (national / urban / rural)

How columns are found (and why)
-------------------------------
Real files differ a lot. Uwezo-style files use readable names (read_level);
PAL ICAN/ICAR 2025 microdata uses codes (ch02 = child's age, hh07k = owns a
television) that only make sense through their LABELS. So every column is
scored on its name AND its label (labels come from .dta/.sav metadata, or from
a --codebook CSV/Excel with columns such as "variable","label"). Noisy lookalikes
are excluded on purpose, e.g. "read or tell stories to the child", "is it a
smartphone?", "minimum proficiency level (MPL)" scores, combined "addition /
subtraction" items. When several columns tie, the script reports "ambiguous"
with the candidates instead of guessing; pick one with --col KEY=NAME.

Honest limits
-------------
* Variable names/labels in real Uwezo and PAL files could not be inspected
  here; matching is tested on synthetic fixtures modelled on published
  descriptions. Always read data_audit.column_mappings in the output.
* Grade-2 pass rules: reading = "story" level or above; numeracy = subtraction
  level or above. Uwezo's top math benchmark is division in Kenya/Uganda but
  multiplication in Tanzania, hence "or above". Override with --pass-values.
* "Working" radio/TV/phone: reported only if the data record working status;
  otherwise the audit says the measure is ownership.
* District-summary mode cannot verify that percentages already refer to
  Grades 3-5 or ages 6-16; it records that as an assumption.

Requires Python 3.9+, pandas, numpy. Optional: openpyxl (xlsx), pyreadstat.
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd

__version__ = "1.0.0"
log = logging.getLogger("cla")


class ExtractionError(Exception):
    """A problem the user must fix (bad input, unknown country, bad override)."""


class Unresolved(Exception):
    """A matched column whose values cannot be interpreted safely."""


def rx(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.I)


# --------------------------------------------------------------------------
# Text helpers
# --------------------------------------------------------------------------
def words(name: Any) -> str:
    """Column name -> lowercase words: 'HHWeightProvided' -> 'hh weight provided'."""
    t = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", str(name))
    t = re.sub(r"[^A-Za-z0-9/%]+", " ", t).lower()
    return re.sub(r"\s+", " ", t).strip()


def norm_label(text: Any) -> str:
    if text is None or (np.isscalar(text) and pd.isna(text)):
        return ""
    t = unicodedata.normalize("NFKC", str(text)).lower().replace("\u2019", "'")
    return re.sub(r"\s+", " ", t).strip()


def _s(v: Any) -> str:
    """Normalise one cell to a comparable lowercase key ('' for missing)."""
    if v is None or (np.isscalar(v) and pd.isna(v)):
        return ""
    if isinstance(v, (bool, np.bool_)):
        return "true" if v else "false"
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    if isinstance(v, (float, np.floating)):
        return str(int(v)) if float(v).is_integer() else str(float(v))
    return norm_label(v)


# --------------------------------------------------------------------------
# Country matching
# --------------------------------------------------------------------------
def _norm_country(text: Any) -> str:
    t = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z0-9]+", " ", t).strip()
    return re.sub(r"^(the |republic of |united republic of |kingdom of )+", "", t)


_ISO3_NAMES = {
    "KEN": ["Kenya"], "TZA": ["Tanzania", "United Republic of Tanzania"], "UGA": ["Uganda"],
    "SEN": ["Senegal"], "MLI": ["Mali"], "NGA": ["Nigeria"], "ETH": ["Ethiopia"], "GHA": ["Ghana"],
    "ZMB": ["Zambia"], "ZWE": ["Zimbabwe"], "MWI": ["Malawi"], "MOZ": ["Mozambique"], "RWA": ["Rwanda"],
    "BDI": ["Burundi"], "SSD": ["South Sudan"], "SDN": ["Sudan"], "SOM": ["Somalia"], "BEN": ["Benin"],
    "BFA": ["Burkina Faso"], "CIV": ["Cote d'Ivoire", "Ivory Coast"], "CMR": ["Cameroon"],
    "COD": ["DR Congo", "Democratic Republic of the Congo", "Congo-Kinshasa"], "NER": ["Niger"],
    "TGO": ["Togo"], "LBR": ["Liberia"], "SLE": ["Sierra Leone"], "GMB": ["Gambia", "The Gambia"],
    "ZAF": ["South Africa"], "BWA": ["Botswana"], "NAM": ["Namibia"], "LSO": ["Lesotho"],
    "MDG": ["Madagascar"], "IND": ["India"], "PAK": ["Pakistan"], "BGD": ["Bangladesh"], "NPL": ["Nepal"],
    "MEX": ["Mexico"], "COL": ["Colombia"],
}
COUNTRY_ALIASES = {k: {_norm_country(n) for n in v} | {k.lower()} for k, v in _ISO3_NAMES.items()}

# --------------------------------------------------------------------------
# Column specifications: patterns scored against column NAME and LABEL
# --------------------------------------------------------------------------
_NOISE = (r"someone|anyone|household member|parent|library|brought|homework|tuition|coaching|\bhelp|"
          r"\btell|mother|father|caregiver|head of|teacher|school fee|reason")
_WORKING = rx(r"work|function")

SPECS: dict[str, dict[str, Any]] = {
    "read": dict(
        include=[(rx(r"read\w*.*story|story.*read"), 5), (rx(r"\bstory\b"), 3),
                 (rx(r"\bread(ing)?\b|literacy"), 2)],
        exclude=rx(r"\bmpl\b|proficien|\birt\b|score|ability|std ?err|standard error|fluen|per minute|wcpm|"
                   r"language of|home lang|assessment lang|material|book|" + _NOISE)),
    "math": dict(
        include=[(rx(r"subtract"), 5), (rx(r"divi(sion|de)"), 5),
                 (rx(r"\b(math|maths|mathematics|numeracy|arithmetic)\b"), 2)],
        exclude=rx(r"addition ?/ ?subtraction|add ?/ ?sub|multiplication ?/ ?division|word problem|\bmpl\b|"
                   r"proficien|\birt\b|score|ability|std ?err|standard error|" + _NOISE)),
    "enrolled": dict(
        include=[(rx(r"enrol"), 5), (rx(r"in school|attend\w* school|currently attend|school status|"
                                         r"school attendance"), 3)],
        exclude=rx(r"\b(grade|class|std|standard|form)\b.*enrol|enrol.*\b(grade|class|std|standard|form)\b|"
                   r"reason|date|\byear\b|\btype\b|private|public|government|name of|fee")),
    "age": dict(
        include=[(rx(r"^age$|\bage\b"), 3), (rx(r"child'?s? age|age of (the )?child|age in years"), 3)],
        exclude=rx(r"age at|start|marri|group|band|categor|adult|parent|head|mother|father|caregiver|"
                   r"respondent|teacher|enrol|first|last|dropout")),
    "grade": dict(
        include=[(rx(r"\b(grade|class|std|standard)\b"), 3),
                 (rx(r"current (grade|class)|(grade|class|std|standard) (attend\w*|enrol\w*|current\w*)"), 2)],
        exclude=rx(r"read|story|math|numer|subtract|divi|level of|test|assess|task|pass|complet|highest|repeat|"
                   r"teacher|size|room|mother|father|parent|head|household|\bhh\b|school type|status|reason|"
                   r"language|\bmpl\b|score")),
    "radio": dict(
        require=rx(r"\bradio\b"), include=[(rx(r"\bradio\b"), 5), (_WORKING, 3)],
        exclude=rx(r"listen|programme|program|station|how often|frequen|hour|wave|content|learn|lesson")),
    "tv": dict(
        require=rx(r"\btv\b|television"), include=[(rx(r"\btv\b|television"), 5), (_WORKING, 3)],
        exclude=rx(r"watch|programme|program|channel|how often|frequen|hour|lesson|dstv|decoder|subscription")),
    "phone": dict(
        require=rx(r"\bmobile\b|\bcell\w*|\bphone\b"),
        include=[(rx(r"mobile phone|cell ?phone|\bphone\b|\bmobile\b|\bcell\b"), 5), (_WORKING, 3)],
        exclude=rx(r"smart|landline|land line|airtime|credit|money|internet|data|\buse|number|network|charge|"
                   r"electric|\bcall|sms|\bapp\b|owner name|\bwho\b")),
    "oos": dict(  # summary files: a direct out-of-school percentage
        include=[(rx(r"out.?of.?school|oosc|not (in school|enrol\w*)|drop ?out"), 5)], exclude=None),
    "urbrur": dict(
        include=[(rx(r"urban|rural|residence|locality|settlement|\barea\b|location|urbrur|geo ?type"), 3)],
        exclude=rx(r"district|region|county|province|village|school|parish|ward|\bname\b|\bid\b")),
    "sex": dict(
        include=[(rx(r"\b(sex|gender)\b"), 4), (rx(r"\b(male|female|boy|girl)s?\b"), 2)],
        exclude=rx(r"head|parent|mother|father|caregiver|respondent|teacher|spouse")),
    "hhid": dict(
        include=[(rx(r"\b(hh|household)\b.*\b(id|identifier|no|number|code|num)\b|\bhhid\b|\bhh ?id\b"), 5)],
        exclude=rx(r"head|member|size|income|child|village|school|enumer|interview|count")),
    "year": dict(
        include=[(rx(r"^(survey |assessment |data |fieldwork )?year$|\byear\b"), 3)],
        exclude=rx(r"birth|born|enrol|since|school year|grade|age|start|dropout|complet")),
    "country": dict(
        include=[(rx(r"^country( name)?$|\bcountry\b"), 3)],
        exclude=rx(r"birth|origin|residen|code of|region|district")),
}

SEG_UR = rx(r"urban|rural")
SEG_SEX = rx(r"^(m|f|male|female|boys?|girls?|man|woman|men|women)\b")


def _val_urbrur(s: pd.Series) -> bool:
    k = s.map(_s)
    k = k[k != ""]
    return len(k) > 0 and float((k.str.contains(SEG_UR) | k.isin(["u", "r"])).mean()) >= 0.8


def _val_sex(s: pd.Series) -> bool:
    k = s.map(_s)
    k = k[k != ""]
    return len(k) > 0 and float(k.str.contains(SEG_SEX).mean()) >= 0.8


def _val_year(s: pd.Series) -> bool:
    v = pd.to_numeric(s, errors="coerce").dropna()
    return len(v) > 0 and bool(((v >= 1990) & (v <= 2100) & (v == v.round())).mean() >= 0.95)


VALIDATORS: dict[str, Callable[[pd.Series], bool]] = {"urbrur": _val_urbrur, "sex": _val_sex, "year": _val_year}

# --------------------------------------------------------------------------
# Value interpretation
# --------------------------------------------------------------------------
INVALID_RX = rx(r"^(|nan|na|n/a|dk|dnk|d/k|refused|refuse|missing|unknown|not applicable|not asked|not tested|"
                r"not assessed|absent|don'?t know|do not know|no response|no answer)$")
WORKING_NEG = rx(r"not working|non.?working|broken|not functional|non.?functional|doesn'?t work|faulty")
POS_RX = rx(r"^(yes|y|true|t|correct|can|able|has|have|own\w*|working|functional|enrolled|attend\w*|currently\b(?!.*\bnot\b)|"
            r"in school|present)\b")
NEG_RX = rx(r"^(no|n|false|f|incorrect|wrong|cannot|can'?t|unable|not|never|none|dropped?|drop.?out|out of school)\b")
ENROL_POS = rx(r"pre.?primary|\becd\b|nursery|kindergarten|\bprimary\b|\bsecondary\b|\bschool\b")
ENROL_NEG = rx(r"dropped|drop.?out|never|not enrol|not in school|out of school|not attending|no longer")
READ_PASS = rx(r"story|comprehension|\bfluent\b")
READ_FAIL = rx(r"nothing|none|non.?reader|can'?t read|letter|alphabet|\bword|syllable|paragraph|sentence|beginner|"
               r"cannot|unable|\bno\b|not able")
MATH_PASS = rx(r"subtract|multipl|divi(sion|de)")
MATH_FAIL = rx(r"nothing|none|count|recogni|addition|\badd\b|cannot|can'?t|unable|\bno\b|not able|number")
MATH_COMBINED = rx(r"addition ?/ ?subtraction|add ?/ ?sub")
INVALID_NUMERIC_CODES = {"-1", "-9", "-99", "-999", "-888", "-777", "8", "9", "88", "98", "99", "888", "998",
                         "999", "9999"}


@dataclass
class Coded:
    flag: np.ndarray                      # 1.0 positive, 0.0 negative, NaN invalid/unknown
    kind: str                             # binary | ladder | custom
    mapping: dict[str, list[str]]
    unrecognised: dict[str, int]
    note: str = ""


def _vcounts(series: pd.Series) -> tuple[pd.Series, pd.Series]:
    keys = series.map(_s)
    return keys, keys[keys != ""].value_counts()


def looks_binary(series: pd.Series) -> bool:
    _, uniq = _vcounts(series)
    if uniq.empty:
        return False
    if all(re.fullmatch(r"-?\d+(\.\d+)?", k) for k in uniq.index):
        core = sum(int(c) for k, c in uniq.items() if k in ("0", "1", "2"))
        return core / uniq.sum() >= 0.95
    return all(INVALID_RX.match(k) or POS_RX.match(k) or NEG_RX.match(k) or WORKING_NEG.search(k)
               for k in uniq.index)


def _finish(keys: pd.Series, cls: dict[str, str], kind: str, note: str = "") -> Coded:
    mapping = {t: sorted(k for k, v in cls.items() if v == t) for t in ("pos", "neg", "invalid")}
    uniq = keys[keys != ""].value_counts()
    unknown = {k: int(uniq[k]) for k, v in cls.items() if v == "unknown"}
    valid_rows = int(uniq.sum())
    if not mapping["pos"]:
        raise Unresolved(f"no value was recognised as positive; values seen: {sorted(uniq.index)[:25]}")
    if valid_rows and sum(unknown.values()) / valid_rows > 0.10:
        raise Unresolved(f"{sum(unknown.values())}/{valid_rows} values not understood: {sorted(unknown)[:25]}")
    flag = keys.map(lambda k: 1.0 if cls.get(k) == "pos" else 0.0 if cls.get(k) == "neg" else np.nan).to_numpy(float)
    return Coded(flag, kind, mapping, unknown, note)


def code_binary(series: pd.Series, *, working: bool = False, pos_extra: re.Pattern | None = None,
                neg_extra: re.Pattern | None = None) -> Coded:
    keys, uniq = _vcounts(series)
    cls: dict[str, str] = {}
    note = ""
    if uniq.size and all(re.fullmatch(r"-?\d+(\.\d+)?", k) for k in uniq.index):
        core = {k for k in uniq.index if k in ("0", "1", "2")}
        if "0" in core and "2" in core:
            raise Unresolved("numeric column mixes 0, 1 and 2; cannot tell which means yes")
        if core == {"1", "2"}:
            pos, neg, note = "1", "2", "assumed 1=yes, 2=no (common survey convention)"
        else:
            pos, neg = "1", "0"
        for k in uniq.index:
            cls[k] = "pos" if k == pos else "neg" if k == neg else "invalid"
    else:
        for k in uniq.index:
            if INVALID_RX.match(k):
                cls[k] = "invalid"
            elif working and WORKING_NEG.search(k):
                cls[k] = "neg"
            elif (neg_extra and neg_extra.search(k)) or NEG_RX.match(k):
                cls[k] = "neg"
            elif (pos_extra and pos_extra.search(k)) or POS_RX.match(k):
                cls[k] = "pos"
            else:
                cls[k] = "unknown"
    return _finish(keys, cls, "binary", note)


def code_ladder(series: pd.Series, pass_rx: re.Pattern, fail_rx: re.Pattern,
                combined_rx: re.Pattern | None = None) -> Coded:
    keys, uniq = _vcounts(series)
    cls: dict[str, str] = {}
    for k in uniq.index:
        if INVALID_RX.match(k):
            cls[k] = "invalid"
        elif combined_rx and combined_rx.search(k):
            cls[k] = "unknown"
        elif pass_rx.search(k):
            cls[k] = "pos"
        elif fail_rx.search(k):
            cls[k] = "neg"
        else:
            cls[k] = "unknown"
    try:
        return _finish(keys, cls, "ladder")
    except Unresolved as e:
        raise Unresolved(f"{e}. If the levels are numeric codes, pass --pass-values KEY=<codes>.") from None


def code_custom(series: pd.Series, pass_vals: list[str], invalid_vals: list[str]) -> Coded:
    keys, uniq = _vcounts(series)
    pv, iv = {_s(v) for v in pass_vals}, {_s(v) for v in invalid_vals}
    cls = {k: ("invalid" if (k in iv or INVALID_RX.match(k)) else "pos" if k in pv else "neg") for k in uniq.index}
    note = "user-defined: listed pass values count as positive, every other non-missing value as negative"
    return _finish(keys, cls, "custom", note)


def parse_grade(v: Any) -> float:
    if v is None or (np.isscalar(v) and pd.isna(v)):
        return np.nan
    if isinstance(v, (int, float, np.integer, np.floating)):
        return float(v) if float(v).is_integer() else np.nan
    s = _s(v)
    if re.search(r"\b(pre|ecd|ece|nursery|kinder\w*|baby|middle|top|reception|form|secondary|adult|madrasa)\b|"
                 r"not in school|out of school|never|drop|none|nothing", s):
        return np.nan
    m = re.search(r"(?<!\d)(\d{1,2})(?!\d)", s)
    return float(m.group(1)) if m else np.nan


def parse_number(series: pd.Series) -> np.ndarray:
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce").to_numpy(float)
    ext = series.astype("object").map(lambda v: "" if v is None else str(v)).str.extract(r"(\d+(?:\.\d+)?)")[0]
    return pd.to_numeric(ext, errors="coerce").to_numpy(float)


# --------------------------------------------------------------------------
# Reading files
# --------------------------------------------------------------------------
@dataclass
class Frame:
    df: pd.DataFrame
    labels: dict[str, str]
    path: Path
    sheet: str | None = None
    notes: list[str] = field(default_factory=list)


def read_codebook(path: Path) -> dict[str, str]:
    if not path.exists():
        raise ExtractionError(f"Codebook not found: {path}")
    try:
        cb = pd.read_csv(path) if path.suffix.lower() == ".csv" else pd.read_excel(path)
    except Exception as e:
        raise ExtractionError(f"Could not read codebook {path.name}: {e}") from e
    low = {c.lower(): c for c in cb.columns}
    ncol = next((low[k] for k in ("variable", "var", "name", "variable_name", "varname", "column", "field") if k in low),
                cb.columns[0])
    lcol = next((low[k] for k in ("label", "description", "question", "variable_label", "text", "question_text")
                 if k in low), cb.columns[1] if len(cb.columns) > 1 else None)
    if lcol is None:
        raise ExtractionError("Codebook needs a variable-name column and a label column.")
    return {str(n): norm_label(l) for n, l in zip(cb[ncol], cb[lcol]) if pd.notna(n)}


def read_table(path: Path, sheet: str | None, codebook: Path | None) -> Frame:
    if not path.exists():
        raise ExtractionError(f"Input file not found: {path}")
    suffix, labels, notes, used_sheet = path.suffix.lower(), {}, [], None
    try:
        if suffix == ".csv":
            for enc in ("utf-8", "utf-8-sig", "latin-1"):
                try:
                    df = pd.read_csv(path, low_memory=False, encoding=enc)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ExtractionError(f"Could not decode {path.name}")
        elif suffix in (".xlsx", ".xlsm", ".xls"):
            xl = pd.ExcelFile(path)
            if sheet is None:
                sheet = xl.sheet_names[0]
                if len(xl.sheet_names) > 1:
                    notes.append(f"Workbook has sheets {xl.sheet_names}; using the first ('{sheet}'). Use --sheet.")
            elif sheet not in xl.sheet_names:
                raise ExtractionError(f"Sheet '{sheet}' not found. Sheets: {xl.sheet_names}")
            df, used_sheet = xl.parse(sheet), sheet
        elif suffix in (".dta", ".sav", ".zsav"):
            try:
                import pyreadstat
            except ImportError as e:
                raise ExtractionError("Reading .dta/.sav needs pyreadstat: pip install pyreadstat") from e
            reader = pyreadstat.read_dta if suffix == ".dta" else pyreadstat.read_sav
            df, meta = reader(str(path), apply_value_formats=True)
            labels = {c: norm_label(l) for c, l in zip(meta.column_names, meta.column_labels) if l}
        else:
            raise ExtractionError(f"Unsupported file type '{suffix}'. Use .csv, .xlsx, .xls, .dta or .sav")
    except ExtractionError:
        raise
    except ImportError as e:
        raise ExtractionError(f"Missing dependency to read {suffix}: {e}") from e
    except Exception as e:
        raise ExtractionError(f"Could not read {path.name}: {e}") from e
    if codebook:
        cb = read_codebook(codebook)
        labels.update({c: l for c, l in cb.items() if c in df.columns})
        notes.append(f"Labels for {sum(c in cb for c in df.columns)} columns taken from codebook {codebook.name}.")
    elif not labels:
        notes.append("No variable labels available (plain CSV/Excel): matching uses column names only. "
                     "For coded names such as 'hh07k', supply --codebook.")
    return Frame(df, labels, path, used_sheet, notes)


# --------------------------------------------------------------------------
# Aggregation
# --------------------------------------------------------------------------
def _wp(flag: np.ndarray, valid: np.ndarray, w: np.ndarray) -> dict:
    valid = np.asarray(valid, bool)
    n = int(valid.sum())
    if n == 0:
        return {"pct": None, "n": 0}
    tot = float(w[valid].sum())
    if tot <= 0:
        return {"pct": None, "n": n}
    return {"pct": round(100.0 * float((w[valid] * flag[valid]).sum()) / tot, 2), "n": n}


@dataclass
class Resolved:
    cols: list[str]
    status: str                       # ok | not_found | ambiguous
    method: str = ""
    alts: list[str] = field(default_factory=list)


@dataclass
class Options:
    country_value: str | None = None
    year: int | None = None
    mode: str = "auto"
    col_overrides: dict[str, list[str]] = field(default_factory=dict)
    pass_values: dict[str, list[str]] = field(default_factory=dict)
    invalid_values: dict[str, list[str]] = field(default_factory=dict)
    weight_col: str | None = None
    hh_weight_col: str | None = None
    unweighted: bool = False
    grade_min: int = 3
    grade_max: int = 5
    age_min: int = 6
    age_max: int = 16


class Extractor:
    def __init__(self, fr: Frame, iso3: str, opts: Options):
        self.fr, self.iso3, self.o = fr, iso3, opts
        self.df = fr.df.copy()
        self.labels = fr.labels
        self.warnings: list[str] = list(fr.notes)
        self.assumptions: list[str] = []
        self.mappings: dict[str, dict] = {}
        self.values: dict[str, dict] = {}
        self._res: dict[str, Resolved] = {}
        self._arr_cache: dict[str, np.ndarray | None] = {}
        self._w_cache: dict[str, tuple[np.ndarray, str | None]] = {}
        self.rows_read = len(self.df)
        self.country_label: str | None = None
        self.years_in_file: list[int] = []
        self.data_year: int | None = None
        self.year_source = "unknown"

    # ---- column resolution ------------------------------------------------
    def _lookup(self, name: str) -> str | None:
        low = {c.lower(): c for c in self.df.columns}
        return low.get(str(name).lower())

    def _hay(self, col: str) -> tuple[str, str]:
        return words(col), self.labels.get(col, "")

    def find(self, key: str) -> list[tuple[str, float]]:
        spec, out = SPECS[key], []
        validate = VALIDATORS.get(key)
        for c in self.df.columns:
            nm, lb = self._hay(c)
            if spec.get("exclude") and (spec["exclude"].search(nm) or (lb and spec["exclude"].search(lb))):
                continue
            if spec.get("require") and not (spec["require"].search(nm) or (lb and spec["require"].search(lb))):
                continue
            score = 0.0
            for pat, w in spec["include"]:
                score += w * bool(pat.search(nm)) + w * bool(lb and pat.search(lb))
            if score > 0 and (validate is None or validate(self.df[c])):
                out.append((c, score))
        return sorted(out, key=lambda t: -t[1])

    @staticmethod
    def _choose(cands: list[tuple[str, float]]) -> tuple[str | None, str, list[str]]:
        if not cands:
            return None, "not_found", []
        if len(cands) == 1 or cands[0][1] > cands[1][1]:
            return cands[0][0], "ok", [c for c, _ in cands[1:4]]
        return None, "ambiguous", [c for c, s in cands if s == cands[0][1]]

    def resolve(self, key: str) -> Resolved:
        if key in self._res:
            return self._res[key]
        ov = self.o.col_overrides.get(key)
        if ov:
            cols = []
            for name in ov:
                c = self._lookup(name)
                if c is None:
                    raise ExtractionError(f"--col {key}={name}: column not found in the file.")
                cols.append(c)
            r = Resolved(cols, "ok", "user override (--col)")
        elif key == "math":
            r = self._choose_math()
        else:
            c, status, alts = self._choose(self.find(key))
            r = Resolved([c] if c else [], status, "fuzzy match on name and label", alts)
        self._res[key] = r
        self.mappings[key] = {"columns": r.cols, "labels": [self.labels.get(c, "") for c in r.cols],
                              "status": r.status, "method": r.method, "alternatives": r.alts}
        return r

    def _choose_math(self) -> Resolved:
        cands = self.find("math")
        strong = [(c, s) for c, s in cands if s >= 5]
        if len(strong) == 1:
            return Resolved([strong[0][0]], "ok", "fuzzy match on name and label",
                            [c for c, _ in cands if c != strong[0][0]][:3])
        if len(strong) == 2:
            hays = [" ".join(self._hay(c)) for c, _ in strong]
            if any("subtract" in h for h in hays) and any(re.search(r"divi", h) for h in hays) and \
                    not all("subtract" in h for h in hays):
                return Resolved([c for c, _ in strong], "ok", "fuzzy match: subtraction + division columns (either)")
        if len(strong) > 2 or len(strong) == 2:
            return Resolved([], "ambiguous", "fuzzy match", [c for c, _ in strong])
        c, status, alts = self._choose(cands)
        return Resolved([c] if c else [], status, "fuzzy match on name and label", alts)

    # ---- country / year / mode --------------------------------------------
    def apply_country_filter(self) -> None:
        r = self.resolve("country")
        if r.status != "ok":
            self.warnings.append("No country column found; assuming the whole file is the requested country.")
            return
        col = r.cols[0]
        keys = self.df[col].map(_s)
        if self.o.country_value is not None:
            mask = keys == _s(self.o.country_value)
        else:
            aliases = COUNTRY_ALIASES.get(self.iso3, {self.iso3.lower()})
            mask = self.df[col].map(lambda v: _norm_country(v) in aliases or _s(v) == self.iso3.lower())
        mask = mask.to_numpy(bool)
        if not mask.any():
            avail = sorted({str(v) for v in self.df[col].dropna().unique()})[:40]
            raise ExtractionError(f"No rows matched country '{self.iso3}' in column '{col}'. Values present: "
                                  f"{avail}. Use --country-value to select by raw value.")
        self.country_label = str(self.df.loc[mask, col].iloc[0])
        self.df = self.df[mask].reset_index(drop=True)

    def apply_year(self) -> None:
        r = self.resolve("year")
        if r.status == "ok":
            col = r.cols[0]
            yrs = pd.to_numeric(self.df[col], errors="coerce")
            self.years_in_file = sorted({int(y) for y in yrs.dropna().unique()})
            if self.o.year is not None:
                if self.o.year not in self.years_in_file:
                    raise ExtractionError(f"--year {self.o.year} not in file; years present: {self.years_in_file}")
                target, self.year_source = self.o.year, "--year"
            else:
                target, self.year_source = max(self.years_in_file), f"latest of column '{col}'"
                if len(self.years_in_file) > 1:
                    self.warnings.append(f"Several survey years present {self.years_in_file}; using the latest "
                                         f"({target}). Use --year to choose.")
            self.df = self.df[(yrs == target).to_numpy(bool)].reset_index(drop=True)
            self.data_year = int(target)
            return
        if self.o.year is not None:
            self.data_year, self.year_source = self.o.year, "--year (no year column to filter on)"
            return
        m = re.findall(r"(?<!\d)((?:19|20)\d{2})(?!\d)", self.fr.path.name)
        if m:
            self.data_year, self.year_source = int(m[-1]), "file name"
        else:
            self.warnings.append("Data year could not be determined; use --year.")

    def detect_mode(self) -> str:
        if self.o.mode != "auto":
            return self.o.mode
        for key in ("read", "math", "radio", "tv", "phone", "enrolled"):
            for c, _ in self.find(key)[:3]:
                if self._percent_like(c):
                    return "summary"
        return "micro"

    def _percent_like(self, col: str) -> bool:
        s = self.df[col]
        if not pd.api.types.is_numeric_dtype(s):
            return False
        v = s.dropna().to_numpy(float)
        if len(v) == 0 or v.min() < 0 or v.max() > 100:
            return False
        named = bool(re.search(r"pct|percent|rate|proportion|share|%", words(col) + " " + self.labels.get(col, "")))
        if named:
            return True
        return len(np.unique(v)) >= 3 and bool((v != np.round(v)).any())

    # ---- weights & segments ----------------------------------------------
    def weight(self, kind: str) -> tuple[np.ndarray, str | None]:
        if kind in self._w_cache:
            return self._w_cache[kind]
        n = len(self.df)
        if self.o.unweighted:
            out: tuple[np.ndarray, str | None] = (np.ones(n), None)
        else:
            out = self._pick_weight(kind)
        self._w_cache[kind] = out
        self.mappings[f"weight_{kind}"] = {"columns": [out[1]] if out[1] else [], "unweighted": out[1] is None}
        return out

    def _pick_weight(self, kind: str) -> tuple[np.ndarray, str | None]:
        n = len(self.df)
        explicit = self.o.hh_weight_col if kind == "hh" and self.o.hh_weight_col else self.o.weight_col
        if explicit:
            c = self._lookup(explicit)
            if c is None:
                raise ExtractionError(f"Weight column '{explicit}' not found.")
            return self._numeric_weight(c)
        hh, child, generic = [], [], []
        for c in self.df.columns:
            nm, lb = self._hay(c)
            hay = nm + " " + lb
            if not re.search(r"\bweights?\b|\bwt\b|\bwgt\b", hay) or re.search(r"body|height|\bkg\b|birth|mass", hay):
                continue
            if not pd.api.types.is_numeric_dtype(self.df[c]):
                continue
            (hh if re.search(r"\bhh\b|household", hay) else child if re.search(r"child|pupil|student|learner", hay)
             else generic).append(c)
        order = (hh + generic) if kind == "hh" else (child + generic + hh)
        if kind == "child" and not (child or generic) and hh:
            self.warnings.append("Only a household weight exists; child estimates use it (each child inherits its "
                                 "household's weight).")
        if not order:
            self.warnings.append(f"No {'household' if kind == 'hh' else 'child'} weight column found; "
                                 "estimates for that unit are unweighted.")
            return np.ones(n), None
        return self._numeric_weight(order[0])

    def _numeric_weight(self, col: str) -> tuple[np.ndarray, str]:
        w = pd.to_numeric(self.df[col], errors="coerce").to_numpy(float)
        bad = ~np.isfinite(w) | (w < 0)
        if bad.all():
            raise ExtractionError(f"Weight column '{col}' has no usable values.")
        if bad.any():
            self.warnings.append(f"{int(bad.sum())} rows have missing/invalid '{col}' and get weight 0.")
            w = np.where(bad, 0.0, w)
        return w, col

    def seg(self, kind: str) -> np.ndarray | None:
        """'urban'/'rural' or 'male'/'female' per row ('' if other); None if unavailable."""
        if kind in self._arr_cache:
            return self._arr_cache[kind]
        key = "urbrur" if kind == "ur" else "sex"
        r = self.resolve(key)
        arr: np.ndarray | None = None
        if r.status != "ok":
            self.warnings.append(f"No usable {'urban/rural' if kind == 'ur' else 'sex'} column "
                                 f"({r.status}); those splits are null.")
        else:
            keys = self.df[r.cols[0]].map(_s)
            numeric = keys[keys != ""].str.fullmatch(r"\d+").all()
            if numeric:
                if "user override" in r.method:
                    a, b = ("urban", "rural") if kind == "ur" else ("male", "female")
                    self.assumptions.append(f"'{r.cols[0]}' is numeric; assumed 1={a}, 2={b}.")
                    arr = keys.map({"1": a, "2": b}).fillna("").to_numpy(object)
                else:
                    self.warnings.append(f"Column '{r.cols[0]}' has unlabelled numeric codes; use "
                                         f"--col {key}={r.cols[0]} to assume 1/2 coding. Splits are null.")
            elif kind == "ur":
                arr = keys.map(lambda k: "urban" if (k.startswith("urban") or k == "u") else
                               "rural" if (k.startswith("rural") or k == "r") else "").to_numpy(object)
            else:
                arr = keys.map(lambda k: "female" if re.match(r"^(f|female|girls?|woman|women)\b", k) else
                               "male" if re.match(r"^(m|male|boys?|man|men)\b", k) else "").to_numpy(object)
        self._arr_cache[kind] = arr
        return arr

    def estimates(self, pos: np.ndarray, valid: np.ndarray, w: np.ndarray, sex: bool = True) -> dict:
        pos = np.asarray(pos, float)
        valid = np.asarray(valid, bool)
        out: dict[str, Any] = {"national": _wp(pos, valid, w)}
        groups = [("ur", ("urban", "rural"))] + ([("sex", ("male", "female"))] if sex else [])
        for kind, names in groups:
            arr = self.seg(kind)
            for nm in names:
                out[nm] = None if arr is None else _wp(pos, valid & (arr == nm), w)
        return out

    # ---- coding a resolved column (or columns) ------------------------------
    def coded(self, key: str, cols: list[str], *, working: bool = False, pos_extra=None, neg_extra=None,
              pass_rx=None, fail_rx=None, combined_rx=None) -> tuple[np.ndarray, np.ndarray, list[dict]]:
        """Return (positive, valid, per-column audit). Multiple columns are OR-combined."""
        flags, audit = [], []
        for c in cols:
            s = self.df[c]
            if key in self.o.pass_values:
                cd = code_custom(s, self.o.pass_values[key], self.o.invalid_values.get(key, []))
            elif looks_binary(s):
                cd = code_binary(s, working=working, pos_extra=pos_extra, neg_extra=neg_extra)
            elif pass_rx is not None:
                cd = code_ladder(s, pass_rx, fail_rx, combined_rx)
            else:
                raise Unresolved(f"values of '{c}' are not yes/no; pass --pass-values {key}=<values>")
            flags.append(cd.flag)
            audit.append({"column": c, "label": self.labels.get(c, ""), "interpretation": cd.kind,
                          "positive_values": cd.mapping["pos"], "negative_values": cd.mapping["neg"],
                          "invalid_values": cd.mapping["invalid"], "unrecognised_values": cd.unrecognised,
                          "note": cd.note})
            if cd.note:
                self.assumptions.append(f"{key}/{c}: {cd.note}")
        stack = np.vstack(flags)
        valid = ~np.isnan(stack).all(axis=0)
        pos = np.where(np.isnan(stack), -1, stack).max(axis=0) == 1
        self.values[key] = {"columns": audit, "combined_by": "any positive" if len(cols) > 1 else None}
        return pos, valid, audit

    # ---- indicators (micro) -------------------------------------------------
    def _need(self, key: str) -> Resolved:
        r = self.resolve(key)
        return r

    def _skip(self, key: str, r: Resolved, what: str) -> dict:
        if r.status == "ambiguous":
            return {"status": "ambiguous", "note": f"Several equally good columns for {what}: {r.alts}. "
                    f"Choose with --col {key}=NAME (several names allowed: any positive counts)."}
        return {"status": "not_found", "note": f"No column found for {what}. Use --col {key}=NAME "
                f"(and --codebook if names are coded)."}

    def _grade_mask(self) -> tuple[np.ndarray | None, dict | None]:
        r = self._need("grade")
        if r.status != "ok":
            return None, self._skip("grade", r, "grade/class (needed to select Grades "
                                    f"{self.o.grade_min}-{self.o.grade_max})")
        g = self.df[r.cols[0]].map(parse_grade).to_numpy(float)
        return (g >= self.o.grade_min) & (g <= self.o.grade_max), None

    def _learning(self, key: str, what: str, definition: str, pass_rx, fail_rx, combined=None) -> dict:
        r = self._need(key)
        if r.status != "ok":
            return self._skip(key, r, what)
        gm, err = self._grade_mask()
        if err:
            return err
        pos, valid, audit = self.coded(key, r.cols, pass_rx=pass_rx, fail_rx=fail_rx, combined_rx=combined)
        elig = gm
        w, wcol = self.weight("child")
        return {"status": "ok", "definition": definition,
                "population": f"children in Grades {self.o.grade_min}-{self.o.grade_max} with a valid result",
                "eligible_n": int(elig.sum()), "variables": audit, "weight_variable": wcol,
                "estimates": self.estimates(pos, valid & elig, w)}

    def ind_literacy(self) -> dict:
        return self._learning("read", "reading level / story",
                              "% of children who can read a Grade 2 level story (story level or above)",
                              READ_PASS, READ_FAIL)

    def ind_numeracy(self) -> dict:
        return self._learning("math", "subtraction/division (math level)",
                              "% of children who can solve a Grade 2 subtraction or division problem "
                              "(subtraction level or above)", MATH_PASS, MATH_FAIL, MATH_COMBINED)

    def ind_oos(self) -> dict:
        r = self._need("enrolled")
        if r.status != "ok":
            return self._skip("enrolled", r, "school enrolment status")
        pos, valid, audit = self.coded("enrolled", r.cols, pos_extra=ENROL_POS, neg_extra=ENROL_NEG)
        ra = self._need("age")
        if ra.status == "ok":
            age = parse_number(self.df[ra.cols[0]])
            elig = (age >= self.o.age_min) & (age <= self.o.age_max)
            age_note = f"ages {self.o.age_min}-{self.o.age_max}"
        else:
            elig = np.ones(len(self.df), bool)
            age_note = "ALL children (no age column found, so the 6-16 filter could not be applied)"
            self.warnings.append("No age column: out-of-school % is not restricted to ages "
                                 f"{self.o.age_min}-{self.o.age_max}.")
        w, wcol = self.weight("child")
        oos = ~pos
        return {"status": "ok", "definition": "% of children not enrolled in school (= 100 - % enrolled)",
                "population": f"{age_note} with a valid enrolment status", "eligible_n": int(elig.sum()),
                "variables": audit, "age_variable": ra.cols[0] if ra.status == "ok" else None,
                "weight_variable": wcol, "estimates": self.estimates(oos, valid & elig, w)}

    def ind_household_tech(self) -> dict:
        r_id = self._need("hhid")
        n = len(self.df)
        keep = np.ones(n, bool)
        if r_id.status == "ok":
            ids = self.df[r_id.cols[0]]
            keep = ~(ids.duplicated(keep="first") & ids.notna()).to_numpy(bool)
            unit = f"households (one row kept per '{r_id.cols[0]}')"
        else:
            unit = "file rows (no household id found: if rows are children, households are weighted by number " \
                   "of children)"
            if any(self._need(k).status == "ok" for k in ("grade", "age", "read")):
                self.warnings.append("No household id found in a child-level file: household indicators are "
                                     "child-weighted. Use --col hhid=NAME.")
        w, wcol = self.weight("hh")
        out: dict[str, Any] = {}
        for key, name in (("radio", "radio"), ("tv", "television"), ("phone", "mobile_phone")):
            r = self._need(key)
            if r.status != "ok":
                out[name] = self._skip(key, r, name)
                continue
            try:
                working = any(re.search(r"work|function", " ".join(self._hay(c))) for c in r.cols)
                pos, valid, audit = self.coded(key, r.cols, working=working)
            except Unresolved as e:
                out[name] = {"status": "unresolved", "note": str(e)}
                continue
            out[name] = {"status": "ok", "variables": audit,
                         "measures": "working device" if working else
                         "ownership (the data do not record whether it works)",
                         "estimates": self.estimates(pos, valid & keep, w, sex=False)}
        oks = [v for v in out.values() if v.get("status") == "ok"]
        return {"status": "ok" if len(oks) == 3 else "partial" if oks else "not_found",
                "definition": "% of households with a radio / television / mobile phone",
                "unit_of_analysis": unit, "weight_variable": wcol, **out}

    # ---- summary mode -------------------------------------------------------
    def _seg_tokens(self, col: str) -> tuple[str | None, str | None]:
        tk = set(words(col).split())
        res = "urban" if "urban" in tk else "rural" if "rural" in tk else None
        sx = "male" if tk & {"male", "boy", "boys", "men"} else "female" if tk & {"female", "girl", "girls", "women"} else None
        return res, sx

    def _pct_series(self, col: str) -> pd.Series | None:
        s = pd.to_numeric(self.df[col], errors="coerce")
        if s.notna().sum() == 0:
            return None
        mx = float(s.max())
        if mx <= 1.0:
            self.assumptions.append(f"'{col}' values are 0-1; multiplied by 100.")
            return s * 100
        return s if mx <= 100 else None

    def _summary_weights(self) -> tuple[np.ndarray, str | None, bool]:
        n = len(self.df)
        if self.o.unweighted:
            return np.ones(n), None, False
        if self.o.weight_col:
            c = self._lookup(self.o.weight_col)
            if c is None:
                raise ExtractionError(f"Weight column '{self.o.weight_col}' not found.")
            return pd.to_numeric(self.df[c], errors="coerce").fillna(0).to_numpy(float), c, False
        best = None
        for c in self.df.columns:
            nm, lb = self._hay(c)
            hay = nm + " " + lb
            if re.search(r"pct|percent|rate|share|%", hay) or not pd.api.types.is_numeric_dtype(self.df[c]):
                continue
            if re.search(r"\bn\b|\bcount\b|sample|children|assessed|tested|respondents|households|pupils|students|"
                         r"\bweights?\b|\bwt\b", hay):
                best = c
                break
        if best is None:
            self.warnings.append("No sample-size/weight column in the summary table: units are averaged with equal "
                                 "weight and N is unavailable.")
            return np.ones(n), None, False
        w = pd.to_numeric(self.df[best], errors="coerce").fillna(0).to_numpy(float)
        is_count = not re.search(r"\bweights?\b|\bwt\b", words(best))
        return w, best, is_count

    def _agg(self, vals: pd.Series, mask: np.ndarray, w: np.ndarray, is_count: bool) -> dict | None:
        v = vals.to_numpy(float)
        ok = mask & np.isfinite(v)
        if not ok.any():
            return None
        tot = float(w[ok].sum())
        pct = float((v[ok] * w[ok]).sum() / tot) if tot > 0 else float(v[ok].mean())
        return {"pct": round(pct, 2), "n": int(round(tot)) if (is_count and tot > 0) else None,
                "n_units": int(ok.sum())}

    def _summary_indicator(self, keys: list[str], complement_keys: list[str], sex: bool) -> dict:
        w, wcol, is_count = self._summary_weights()
        cands: list[tuple[str, float, bool]] = []
        for k in keys:
            cands += [(c, s, False) for c, s in self.find(k) if self._percent_like(c)]
        for k in complement_keys:
            cands += [(c, s, True) for c, s in self.find(k) if self._percent_like(c)]
        if not cands:
            return {"status": "not_found", "note": "No percentage column found. Use --col KEY=NAME."}
        plain = [(c, s, comp) for c, s, comp in cands if self._seg_tokens(c) == (None, None)]
        if not plain:
            return {"status": "not_found", "note": "Only segment-specific percentage columns were found."}
        plain.sort(key=lambda t: -t[1])
        if len(plain) > 1 and plain[0][1] == plain[1][1]:
            return {"status": "ambiguous", "note": f"Equally good percentage columns: {[c for c, _, _ in plain[:4]]}. "
                    "Choose with --col."}
        col, _, comp = plain[0]
        ser = self._pct_series(col)
        if ser is None:
            return {"status": "unresolved", "note": f"'{col}' values exceed 100; not a percentage."}
        ser = 100 - ser if comp else ser
        n_all = np.ones(len(self.df), bool)
        est = {"national": self._agg(ser, n_all, w, is_count)}
        wide = {self._seg_tokens(c): c for c, _, cp in cands if self._seg_tokens(c) != (None, None) and cp == comp}
        for nm in ("urban", "rural") + (("male", "female") if sex else ()):
            wcol_name = next((c for (res, sx), c in wide.items() if nm in (res, sx) and
                              (res is None or sx is None)), None)
            if wcol_name:
                s2 = self._pct_series(wcol_name)
                est[nm] = None if s2 is None else self._agg(100 - s2 if comp else s2, n_all, w, is_count)
                continue
            arr = self.seg("ur" if nm in ("urban", "rural") else "sex")
            est[nm] = None if arr is None else self._agg(ser, arr == nm, w, is_count)
        return {"status": "ok", "variable": col, "label": self.labels.get(col, ""),
                "derived_as": "100 - enrolment %" if comp else "as given", "weight_variable": wcol,
                "estimates": est}

    def run_summary(self) -> dict[str, dict]:
        self.assumptions.append("Summary mode: percentages are assumed to already refer to the target populations "
                                f"(Grades {self.o.grade_min}-{self.o.grade_max}; ages {self.o.age_min}-"
                                f"{self.o.age_max}); this cannot be verified from the table.")
        hh = {}
        for key, name in (("radio", "radio"), ("tv", "television"), ("phone", "mobile_phone")):
            hh[name] = self._summary_indicator([key], [], sex=False)
        oks = [v for v in hh.values() if v.get("status") == "ok"]
        return {
            "foundational_literacy": self._summary_indicator(["read"], [], sex=True),
            "foundational_numeracy": self._summary_indicator(["math"], [], sex=True),
            "out_of_school_children": self._summary_indicator(["oos"], ["enrolled"], sex=True),
            "household_technology": {"status": "ok" if len(oks) == 3 else "partial" if oks else "not_found", **hh},
        }

    # ---- driver ----------------------------------------------------------------
    def run(self) -> dict:
        self.apply_country_filter()
        self.apply_year()
        mode = self.detect_mode()
        rows_used = len(self.df)
        if mode == "summary":
            inds = self.run_summary()
        else:
            inds = {}
            for name, fn in (("foundational_literacy", self.ind_literacy), ("foundational_numeracy", self.ind_numeracy),
                             ("out_of_school_children", self.ind_oos), ("household_technology", self.ind_household_tech)):
                try:
                    inds[name] = fn()
                except Unresolved as e:
                    inds[name] = {"status": "unresolved", "note": str(e)}
                except ExtractionError:
                    raise
                except Exception as e:  # keep other indicators alive
                    log.exception("indicator %s failed", name)
                    inds[name] = {"status": "error", "note": f"{type(e).__name__}: {e}"}
        return {
            "metadata": {
                "country_iso3": self.iso3, "country_label_in_file": self.country_label,
                "data_year": self.data_year, "data_year_source": self.year_source,
                "years_in_file": self.years_in_file, "mode": mode,
                "scale": "percentages on a 0-100 scale; 'n' is the unweighted valid base (summary mode: summed "
                         "sample sizes, if a count column exists)",
                "source_file": self.fr.path.name, "sheet": self.fr.sheet, "rows_read": self.rows_read,
                "rows_used": rows_used, "extraction_timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "script_version": __version__},
            "indicators": inds,
            "data_audit": {
                "column_mappings": self.mappings, "value_interpretation": self.values,
                "filters": {"grades": [self.o.grade_min, self.o.grade_max], "ages": [self.o.age_min, self.o.age_max],
                            "country_value": self.o.country_value, "year": self.data_year},
                "assumptions": self.assumptions, "warnings": self.warnings},
        }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _kv(items: list[str] | None, flag: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for it in items or []:
        if "=" not in it:
            raise ExtractionError(f"{flag} expects KEY=VALUE[,VALUE...], got '{it}'")
        k, v = it.split("=", 1)
        out[k.strip().lower()] = [x.strip() for x in v.split(",") if x.strip()]
    return out


VALID_KEYS = sorted(set(SPECS) | {"weight"})


def extract(path: Path, iso3: str, opts: Options, *, sheet: str | None = None, codebook: Path | None = None) -> dict:
    bad = [k for k in {**opts.col_overrides, **opts.pass_values, **opts.invalid_values} if k not in SPECS]
    if bad:
        raise ExtractionError(f"Unknown KEY(s) {bad}. Valid keys: {sorted(SPECS)}")
    return Extractor(read_table(path, sheet, codebook), iso3, opts).run()


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Extract foundational-learning and household indicators from "
                                             "Citizen-Led Assessment data (Uwezo, PAL Network ICAN, ASER-style).",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--input", required=True, type=Path, help=".csv/.xlsx/.xls/.dta/.sav file")
    ap.add_argument("--country", required=True, help="ISO3 code, e.g. KEN, TZA, UGA")
    ap.add_argument("--output", required=True, type=Path, help="output JSON path, e.g. uwezo_KEN_latest.json")
    g = ap.add_argument_group("optional")
    g.add_argument("--year", type=int, help="survey year (default: latest year in the file)")
    g.add_argument("--sheet", help="Excel sheet name (default: first)")
    g.add_argument("--codebook", type=Path, help="CSV/Excel with 'variable' and 'label' columns")
    g.add_argument("--mode", choices=["auto", "micro", "summary"], default="auto",
                   help="micro = child/household rows; summary = district percentage table")
    g.add_argument("--col", action="append", metavar="KEY=NAME[,NAME]",
                   help=f"force a column; keys: {', '.join(sorted(SPECS))}. Several names = any positive counts")
    g.add_argument("--pass-values", action="append", metavar="KEY=V1,V2",
                   help="values meaning pass/yes for KEY (needed for numeric-coded levels)")
    g.add_argument("--invalid-values", action="append", metavar="KEY=V1,V2", help="values to treat as missing")
    g.add_argument("--country-value", help="raw value in the country column (instead of ISO3 matching)")
    g.add_argument("--weight-col", help="weight column (child level)")
    g.add_argument("--hh-weight-col", help="household weight column")
    g.add_argument("--unweighted", action="store_true")
    g.add_argument("--grade-min", type=int, default=3)
    g.add_argument("--grade-max", type=int, default=5)
    g.add_argument("--age-min", type=int, default=6)
    g.add_argument("--age-max", type=int, default=16)
    ap.add_argument("-v", "--verbose", action="store_true")
    return ap


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.WARNING, format="%(levelname)s: %(message)s")
    iso3 = a.country.strip().upper()
    if not re.fullmatch(r"[A-Z]{3}", iso3):
        print(f"error: --country must be a 3-letter ISO code, got '{a.country}'", file=sys.stderr)
        return 2
    try:
        opts = Options(country_value=a.country_value, year=a.year, mode=a.mode,
                       col_overrides=_kv(a.col, "--col"), pass_values=_kv(a.pass_values, "--pass-values"),
                       invalid_values=_kv(a.invalid_values, "--invalid-values"), weight_col=a.weight_col,
                       hh_weight_col=a.hh_weight_col, unweighted=a.unweighted, grade_min=a.grade_min,
                       grade_max=a.grade_max, age_min=a.age_min, age_max=a.age_max)
        if "country_column" in a.__dict__:
            pass
        result = extract(a.input, iso3, opts, sheet=a.sheet, codebook=a.codebook)
    except ExtractionError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    try:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError as e:
        print(f"error: could not write {a.output}: {e}", file=sys.stderr)
        return 2
    ok = [k for k, v in result["indicators"].items() if v.get("status") in ("ok", "partial")]
    for k, v in result["indicators"].items():
        if v.get("status") not in ("ok", "partial"):
            print(f"  - {k}: {v.get('status')} - {v.get('note', '')}", file=sys.stderr)
    m = result["metadata"]
    print(f"Wrote {a.output}  (mode={m['mode']}, year={m['data_year']}, rows used={m['rows_used']}, "
          f"indicators ok: {len(ok)}/4)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
