#!/usr/bin/env python3
"""
extract_afrobarometer_education.py
==================================
Country-agnostic extraction of education indicators from an Afrobarometer
respondent-level dataset (Round 8, 9, 10 ... as .sav or .csv).

Usage
-----
    python extract_afrobarometer_education.py \\
        --input afrobarometer_release-dataset_ken_r9_en_2023-03-01.sav \\
        --country KEN \\
        --output afrobarometer_KEN_r9.json

Indicators (all on a 0-100 scale, each reported for national / urban / rural)
---------------------------------------------------------------------------
1. education_priority_problem
       % of respondents naming education among their (up to) three most
       important national problems, plus % naming it as the FIRST problem.
       Denominator: all respondents in the country sample.
2. school_deficits
       % reporting problems with local public schools (textbooks/materials,
       teaching quality, teacher absenteeism, overcrowding, toilets/sanitation)
       plus an "any problem" composite. Denominator: respondents giving a valid
       answer (don't know / refused / "no experience" are excluded).
3. satisfaction_education_delivery
       % saying the government handles "addressing educational needs"
       fairly/very WELL vs fairly/very BADLY. Denominator: respondents who
       gave a well-or-badly answer.

Design: variables are found by LABEL, not by hard-coded code
-------------------------------------------------------------
Question numbers and answer codes change between rounds (the "Education"
answer is code 9 in Round 2 merged data but 14 in Round 9 country files; the
"most important problems" items are Q45PT1-3 in Round 9). So the script:
  * locates variables by keywords in variable labels,
  * resolves answer meaning from VALUE LABELS (so it works for any code),
  * never guesses an answer code. For label-less CSVs, supply --education-code.
Every variable used, its label, and the answers counted as "problem" are
written to the JSON so each number can be audited against the codebook.

Important caveats
-----------------
* The school-problem items ("absent teachers", "lack of textbooks" ...) were
  asked in early rounds (e.g. Round 2.5/3, Q73 series). They may NOT exist in
  Rounds 8-10. If none is found the indicator is reported as "not_found"
  instead of being fabricated.
* Estimates use the within-country weight (e.g. 'withinwt') when present.
* CSV files carry no value labels unless the export wrote label text; use the
  .sav file where possible.

Requires: Python 3.9+, pandas, numpy; pyreadstat for .sav files.
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
from typing import Any

import numpy as np
import pandas as pd

__version__ = "1.0.0"
log = logging.getLogger("afrobarometer")


class ExtractionError(Exception):
    """Raised for problems the user must fix (bad input, unknown country...)."""


# --------------------------------------------------------------------------
# Country matching (ISO3 -> names as they appear in COUNTRY value labels)
# --------------------------------------------------------------------------
def _norm_country(text: Any) -> str:
    t = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z0-9]+", " ", t).strip()
    return re.sub(r"^(the |republic of |kingdom of )+", "", t)


_ISO3_NAMES: dict[str, list[str]] = {
    "DZA": ["Algeria"], "AGO": ["Angola"], "BEN": ["Benin"], "BWA": ["Botswana"],
    "BFA": ["Burkina Faso"], "BDI": ["Burundi"], "CPV": ["Cabo Verde", "Cape Verde"],
    "CMR": ["Cameroon"], "TCD": ["Chad"], "COM": ["Comoros"],
    "COG": ["Congo-Brazzaville", "Congo Brazzaville", "Congo"],
    "COD": ["Congo-Kinshasa", "DR Congo", "Democratic Republic of the Congo", "DRC"],
    "CIV": ["Cote d'Ivoire", "Ivory Coast"], "EGY": ["Egypt"],
    "SWZ": ["Eswatini", "Swaziland"], "ETH": ["Ethiopia"], "GAB": ["Gabon"],
    "GMB": ["Gambia", "The Gambia"], "GHA": ["Ghana"], "GIN": ["Guinea"],
    "GNB": ["Guinea-Bissau"], "KEN": ["Kenya"], "LSO": ["Lesotho"], "LBR": ["Liberia"],
    "MDG": ["Madagascar"], "MWI": ["Malawi"], "MLI": ["Mali"], "MRT": ["Mauritania"],
    "MUS": ["Mauritius"], "MAR": ["Morocco"], "MOZ": ["Mozambique"], "NAM": ["Namibia"],
    "NER": ["Niger"], "NGA": ["Nigeria"], "RWA": ["Rwanda"],
    "STP": ["Sao Tome and Principe", "Sao Tome & Principe"], "SEN": ["Senegal"],
    "SYC": ["Seychelles"], "SLE": ["Sierra Leone"], "ZAF": ["South Africa"],
    "SDN": ["Sudan"], "TZA": ["Tanzania"], "TGO": ["Togo"], "TUN": ["Tunisia"],
    "UGA": ["Uganda"], "ZMB": ["Zambia"], "ZWE": ["Zimbabwe"],
}
COUNTRY_ALIASES: dict[str, set[str]] = {
    iso: {_norm_country(n) for n in names} for iso, names in _ISO3_NAMES.items()
}

# --------------------------------------------------------------------------
# Keyword configuration (edit here if a future round changes wording)
# --------------------------------------------------------------------------
COUNTRY_COLUMNS = ("country", "countryname", "country_name", "cntry")
URBRUR_COLUMNS = ("urbrur", "urban_rural", "urbanrural")
WEIGHT_COLUMNS = ("withinwt_ea", "withinwt_hh", "withinwt", "within_wt", "wgt", "weight", "wt")

MIP_LABEL = re.compile(r"most important problems?|important problems? facing|most urgent problems?")
MIP_ORDINAL = re.compile(r"\b(1st|2nd|3rd|first|second|third)\b")
SATISFACTION_LABEL = re.compile(r"educational needs")
WELL = re.compile(r"\b(fairly|very) well\b")
BADLY = re.compile(r"\b(fairly|very) badly\b")

SCHOOL_ISSUES = {
    "textbooks_materials": re.compile(r"textbook|text book|\bbooks\b|learning material|teaching material|supplies"),
    "teaching_quality": re.compile(r"teaching quality|quality of (teaching|education)|poor(ly)? (teaching|taught)|unqualified|poorly (trained|qualified)"),
    "teacher_absenteeism": re.compile(r"absent|absentee"),
    "overcrowded_classrooms": re.compile(r"overcrowd|crowded|class size|too many (students|pupils)"),
    "toilets_sanitation": re.compile(r"toilet|latrine|sanitation|washroom"),
}
# Answer-label classification for problem-frequency/yes-no items.
EXCLUDE_ANS = re.compile(r"don.?t know|refused|missing|not applicable|\bn/?a\b|no (contact|experience|children|answer|response)|"
                         r"haven.?t (heard|had)|did not|not asked|other")
NEGATIVE_ANS = re.compile(r"^(never|no|none|not at all|not a problem|no problem)\b")
POSITIVE_ANS = re.compile(r"^(yes|once or twice|a few times|several times|many times|rarely|sometimes|"
                          r"occasionally|often|always|frequently|a lot)\b")


# --------------------------------------------------------------------------
# Survey container
# --------------------------------------------------------------------------
def _norm(text: Any) -> str:
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return ""
    t = unicodedata.normalize("NFKC", str(text)).lower()
    t = t.replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"\s+", " ", t).strip()


@dataclass
class Survey:
    df: pd.DataFrame
    var_labels: dict[str, str] = field(default_factory=dict)
    val_labels: dict[str, dict[float, str]] = field(default_factory=dict)
    path: Path = Path(".")

    def __post_init__(self) -> None:
        self._lower = {c.lower(): c for c in self.df.columns}

    def col(self, *names: str) -> str | None:
        """Case-insensitive column lookup; first hit wins."""
        for n in names:
            if n.lower() in self._lower:
                return self._lower[n.lower()]
        return None

    def label(self, col: str) -> str:
        return _norm(self.var_labels.get(col, ""))

    def decode(self, col: str, df: pd.DataFrame | None = None) -> pd.Series | None:
        """Return normalised answer-label text per row (NaN if missing/unlabelled).
        None means the column has neither value labels nor text values."""
        df = self.df if df is None else df
        s = df[col]
        if col in self.val_labels:
            mp = {float(k): _norm(v) for k, v in self.val_labels[col].items()}
            return s.map(lambda v: mp.get(float(v)) if pd.notna(v) else None).astype(object)
        if s.dtype == object or pd.api.types.is_string_dtype(s):
            return s.map(lambda v: _norm(v) if pd.notna(v) else None).astype(object)
        return None


def load_survey(path: Path) -> Survey:
    """Load a .sav (via pyreadstat) or .csv file, keeping variable/value labels."""
    if not path.exists():
        raise ExtractionError(f"Input file not found: {path}")
    suffix = path.suffix.lower()
    if suffix in (".sav", ".zsav"):
        try:
            import pyreadstat
        except ImportError as e:  # pragma: no cover
            raise ExtractionError("Reading .sav files needs pyreadstat: pip install pyreadstat") from e
        try:
            df, meta = pyreadstat.read_sav(str(path), apply_value_formats=False)
        except Exception as e:
            raise ExtractionError(f"Could not read SPSS file {path.name}: {e}") from e
        var_labels = {c: (l or "") for c, l in zip(meta.column_names, meta.column_labels)}
        val_labels = {}
        for c, mapping in (meta.variable_value_labels or {}).items():
            try:
                val_labels[c] = {float(k): str(v) for k, v in mapping.items()}
            except (TypeError, ValueError):
                continue
        return Survey(df, var_labels, val_labels, path)
    if suffix == ".csv":
        last: Exception | None = None
        for enc in ("utf-8", "utf-8-sig", "latin-1"):
            try:
                return Survey(pd.read_csv(path, low_memory=False, encoding=enc), path=path)
            except UnicodeDecodeError as e:
                last = e
            except Exception as e:
                raise ExtractionError(f"Could not parse CSV {path.name}: {e}") from e
        raise ExtractionError(f"Could not decode CSV {path.name}: {last}")
    raise ExtractionError(f"Unsupported file type '{suffix}'. Use .sav or .csv")


# --------------------------------------------------------------------------
# Context: country filter, weights, urban/rural, round
# --------------------------------------------------------------------------
@dataclass
class Ctx:
    sv: Survey
    df: pd.DataFrame            # country subset
    w: np.ndarray               # weights aligned to df rows
    seg: np.ndarray | None      # 'urban' / 'rural' / other / nan, aligned to df rows
    warnings: list[str]
    assumptions: list[str]


def filter_country(sv: Survey, iso3: str, country_col: str | None, country_value: str | None,
                   warnings: list[str]) -> tuple[pd.DataFrame, str | None, str | None]:
    """Return (subset, country_column_used, label_matched)."""
    col = sv.col(country_col) if country_col else sv.col(*COUNTRY_COLUMNS)
    if country_col and col is None:
        raise ExtractionError(f"--country-column '{country_col}' not found in the file.")
    if col is None:
        warnings.append("No country column found; assuming the whole file is the requested country.")
        return sv.df, None, None
    raw = sv.df[col]
    if country_value is not None:
        mask = raw.astype(str).str.strip() == str(country_value).strip()
        label = str(country_value)
    else:
        labels = sv.decode(col)
        if labels is None:
            codes = sorted(raw.dropna().unique().tolist())[:60]
            raise ExtractionError(f"Column '{col}' holds numeric codes with no labels, so '{iso3}' cannot be "
                                  f"resolved. Pass --country-value with the code (values: {codes}).")
        aliases = COUNTRY_ALIASES.get(iso3)
        if not aliases:
            raise ExtractionError(f"Unknown ISO3 code '{iso3}'. Use --country-value to select by raw value.")
        norm = labels.map(lambda v: _norm_country(v) if v else "")
        mask = norm.isin(aliases)
        if not mask.any():
            avail = sorted({v for v in labels.dropna().unique()})[:60]
            raise ExtractionError(f"No respondents matched country '{iso3}' in column '{col}'. "
                                  f"Labels present: {avail}")
        first = raw[mask].iloc[0]  # original (un-normalised) label as stored in the file
        label = sv.val_labels.get(col, {}).get(float(first), str(first)) if pd.notna(first) and \
            not isinstance(first, str) else str(first)
    if not mask.any():
        raise ExtractionError(f"--country-value '{country_value}' matched no rows in column '{col}'.")
    return sv.df[mask.to_numpy()].reset_index(drop=True), col, label


def pick_weights(sv: Survey, df: pd.DataFrame, override: str | None, unweighted: bool,
                 warnings: list[str]) -> tuple[np.ndarray, str | None]:
    n = len(df)
    if unweighted:
        return np.ones(n), None
    col = sv.col(override) if override else sv.col(*WEIGHT_COLUMNS)
    if override and col is None:
        raise ExtractionError(f"--weight-col '{override}' not found in the file.")
    if col is None:
        warnings.append("No weight column found; estimates are unweighted.")
        return np.ones(n), None
    w = pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
    bad = ~np.isfinite(w) | (w < 0)
    if bad.all():
        warnings.append(f"Weight column '{col}' has no usable values; estimates are unweighted.")
        return np.ones(n), None
    if bad.any():
        warnings.append(f"{int(bad.sum())} respondents had missing/invalid '{col}' and get weight 0.")
        w = np.where(bad, 0.0, w)
    return w, col


def find_urban_rural(sv: Survey, df: pd.DataFrame, warnings: list[str],
                     assumptions: list[str]) -> tuple[np.ndarray | None, str | None]:
    col = sv.col(*URBRUR_COLUMNS)
    if col is None:
        for c, lab in sv.var_labels.items():
            if re.search(r"urban(\s+or|/)\s*rural|rural(\s+or|/)\s*urban", _norm(lab)):
                col = c
                break
    if col is None:
        warnings.append("No urban/rural variable found; urban/rural splits are null.")
        return None, None
    labels = sv.decode(col, df)
    if labels is None:  # numeric, unlabelled
        assumptions.append(f"'{col}' has no value labels; assumed 1=urban, 2=rural.")
        codes = pd.to_numeric(df[col], errors="coerce")
        return np.where(codes == 1, "urban", np.where(codes == 2, "rural", "")).astype(object), col

    def cls(v):
        if not v:
            return ""
        if v.startswith("rural"):
            return "rural"
        if v.startswith("peri"):
            return "peri-urban"
        if v.startswith("urban"):
            return "urban"
        return ""
    return labels.map(cls).to_numpy(dtype=object), col


def detect_round(sv: Survey, df: pd.DataFrame, override: str | None) -> str:
    if override:
        return str(override)
    col = sv.col("round", "survey_round")
    if col is not None:
        vals = pd.to_numeric(df[col], errors="coerce").dropna()
        if len(vals):
            return str(int(vals.mode().iloc[0]))
    m = re.search(r"(?<![a-z0-9])r(?:ound)?[ _-]?(\d{1,2})(?![0-9])", sv.path.name.lower())
    return m.group(1) if m else "unknown"


# --------------------------------------------------------------------------
# Aggregation
# --------------------------------------------------------------------------
def _wp(flag: np.ndarray, valid: np.ndarray, w: np.ndarray) -> dict:
    """Weighted % of `flag` among `valid` rows. n is the unweighted valid count."""
    valid = np.asarray(valid, dtype=bool)
    n = int(valid.sum())
    if n == 0:
        return {"pct": None, "n": 0}
    wv = w[valid]
    tot = float(wv.sum())
    if tot <= 0:
        return {"pct": None, "n": n}
    return {"pct": round(100.0 * float((wv * flag[valid]).sum()) / tot, 2), "n": n}


def segments(ctx: Ctx, flag: np.ndarray, valid: np.ndarray) -> dict:
    """national / urban / rural estimates for one flag."""
    flag = np.asarray(flag, dtype=float)
    out: dict[str, Any] = {"national": _wp(flag, valid, ctx.w)}
    for name in ("urban", "rural"):
        out[name] = None if ctx.seg is None else _wp(flag, np.asarray(valid, bool) & (ctx.seg == name), ctx.w)
    return out


def _skipped(status: str, note: str) -> dict:
    return {"status": status, "note": note}


# --------------------------------------------------------------------------
# Indicator 1: education as a priority problem
# --------------------------------------------------------------------------
def find_mip_columns(sv: Survey, explicit: list[str] | None, warnings: list[str]) -> list[str]:
    if explicit:
        missing = [c for c in explicit if sv.col(c) is None]
        if missing:
            raise ExtractionError(f"--mip-columns not found: {missing}")
        return [sv.col(c) for c in explicit]
    groups: dict[str, list[str]] = {}
    for c in sv.df.columns:
        lab = sv.label(c)
        if MIP_LABEL.search(lab) and MIP_ORDINAL.search(lab):
            stem = re.sub(r"^q\d+\w*[.:]?\s*", "", lab)  # drop a leading question id such as 'q45pt1.'
            groups.setdefault(MIP_ORDINAL.sub("#", stem), []).append(c)
    if not groups and not sv.var_labels:  # CSV: fall back to the Qnn PT1-3 naming pattern
        for c in sv.df.columns:
            m = re.fullmatch(r"(q\d+)pt[1-3]", c.lower())
            if m:
                groups.setdefault(m.group(1), []).append(c)
        if groups:
            warnings.append("No variable labels (CSV): most-important-problems columns found by name pattern only.")
    if not groups:
        return []
    if len(groups) > 1:
        warnings.append(f"Several 'most important problems' groups found ({len(groups)}); using the one "
                        f"mentioning 'country' or the largest. Override with --mip-columns.")
    best = max(groups.values(), key=lambda g: (any("country" in sv.label(c) for c in g), len(g)))
    return sorted(best, key=lambda c: c.lower())


def ind_education_priority(ctx: Ctx, mip_cols: list[str] | None, edu_codes: list[float] | None) -> dict:
    cols = find_mip_columns(ctx.sv, mip_cols, ctx.warnings)
    if not cols:
        return _skipped("not_found", "No 'most important problems' columns found (looked for labels like "
                        "'Most important problems - 1st response'). Use --mip-columns.")
    n = len(ctx.df)
    flags, used = [], []
    for c in cols:
        lab = ctx.sv.decode(c, ctx.df)
        if lab is not None:
            vl = ctx.sv.val_labels.get(c)
            if vl is not None and not any("educat" in _norm(v) for v in vl.values()):
                return _skipped("unresolved", f"{c} has no 'Education' answer category in its value labels.")
            f = lab.fillna("").str.contains("educat").to_numpy()
            how = "value label contains 'Education'"
        elif edu_codes:
            f = pd.to_numeric(ctx.df[c], errors="coerce").isin(edu_codes).to_numpy()
            how = f"numeric code in {edu_codes} (from --education-code)"
        else:
            return _skipped("unresolved", f"{c} is numeric without value labels, so the 'Education' code cannot "
                            "be identified. The code differs between rounds - pass --education-code from the codebook.")
        flags.append(f)
        used.append({"variable": c, "label": ctx.sv.var_labels.get(c, ""), "education_identified_by": how})
    any_flag = np.logical_or.reduce(flags)
    return {"status": "ok",
            "definition": "Share of respondents naming education in any of their top-3 national problems; "
                          "'first_mention' is education as the 1st problem only.",
            "denominator": "all respondents in the country sample",
            "variables_used": used,
            "any_top3_mention": segments(ctx, any_flag, np.ones(n, bool)),
            "first_mention": segments(ctx, flags[0], np.ones(n, bool))}


# --------------------------------------------------------------------------
# Indicator 2: school facility & quality deficits
# --------------------------------------------------------------------------
def _classify_answers(labels: pd.Series) -> tuple[dict[str, str], list[str]]:
    """Classify the answer labels actually present as pos/neg/excl; list unknown ones."""
    mapping, unknown = {}, []
    for lab in sorted({v for v in labels.dropna().unique() if v}):
        if EXCLUDE_ANS.search(lab):
            mapping[lab] = "excl"
        elif NEGATIVE_ANS.match(lab):
            mapping[lab] = "neg"
        elif POSITIVE_ANS.match(lab):
            mapping[lab] = "pos"
        else:
            unknown.append(lab)
    return mapping, unknown


def ind_school_deficits(ctx: Ctx) -> dict:
    items: dict[str, list] = {}
    skipped_vars: list[dict] = []
    per_var: list[tuple[np.ndarray, np.ndarray]] = []
    if not ctx.sv.var_labels:
        return _skipped("not_found", "CSV without variable labels: school-problem items cannot be located by "
                        "keyword. Use the .sav file.")
    for c in ctx.sv.df.columns:
        lab = ctx.sv.label(c)
        if "school" not in lab:
            continue
        issue = next((k for k, rx in SCHOOL_ISSUES.items() if rx.search(lab)), None)
        if issue is None:
            continue
        ans = ctx.sv.decode(c, ctx.df)
        if ans is None:
            skipped_vars.append({"variable": c, "reason": "no value labels"})
            continue
        mapping, unknown = _classify_answers(ans)
        if unknown:
            skipped_vars.append({"variable": c, "reason": f"unrecognised answer labels: {unknown}"})
            continue
        cls = ans.map(lambda v: mapping.get(v, "excl") if v else "excl").to_numpy()
        pos, valid = cls == "pos", (cls == "pos") | (cls == "neg")
        if not valid.any():
            skipped_vars.append({"variable": c, "reason": "no valid answers in this country sample"})
            continue
        per_var.append((pos, valid))
        items.setdefault(issue, []).append({
            "variable": c, "label": ctx.sv.var_labels.get(c, ""),
            "answers_counted_as_problem": sorted(k for k, v in mapping.items() if v == "pos"),
            "answers_counted_as_no_problem": sorted(k for k, v in mapping.items() if v == "neg"),
            "answers_excluded": sorted(k for k, v in mapping.items() if v == "excl"),
            "pct_reporting_problem": segments(ctx, pos, valid)})
    if not per_var:
        note = ("No school-problem items found by keyword (searched variable labels for 'school' plus: "
                "textbooks, teaching quality, absent teachers, overcrowded, toilets). These items were asked in "
                "early Afrobarometer rounds but may not exist in this round's questionnaire.")
        res = _skipped("not_found", note)
        res["skipped_candidates"] = skipped_vars
        return res
    any_pos = np.logical_or.reduce([p for p, _ in per_var])
    any_valid = np.logical_or.reduce([v for _, v in per_var])
    return {"status": "ok",
            "definition": "% reporting the problem at least once with local public schools; "
                          "no-experience / don't know / refused excluded from the denominator.",
            "items": items,
            "any_problem": {"definition": "at least one problem reported among items answered",
                            "pct_reporting_problem": segments(ctx, any_pos, any_valid)},
            "skipped_candidates": skipped_vars}


# --------------------------------------------------------------------------
# Indicator 3: satisfaction with education delivery
# --------------------------------------------------------------------------
def ind_satisfaction(ctx: Ctx, sat_col: str | None = None) -> dict:
    if sat_col:
        if ctx.sv.col(sat_col) is None:
            raise ExtractionError(f"--satisfaction-column '{sat_col}' not found in the file.")
        cands = [ctx.sv.col(sat_col)]
    else:
        cands = [c for c in ctx.sv.df.columns if SATISFACTION_LABEL.search(ctx.sv.label(c))]
    if not cands:
        return _skipped("not_found", "No variable labelled 'addressing educational needs' found (R9: Q46H). "
                        "For CSVs without variable labels pass --satisfaction-column.")
    col = cands[0]
    if len(cands) > 1:
        ctx.warnings.append(f"Several satisfaction candidates {cands}; using {col}.")
    ans = ctx.sv.decode(col, ctx.df)
    if ans is not None:
        well = ans.fillna("").map(lambda v: bool(WELL.search(v))).to_numpy()
        badly = ans.fillna("").map(lambda v: bool(BADLY.search(v))).to_numpy()
        how = "answer labels 'fairly/very well' vs 'fairly/very badly'"
    else:
        ctx.assumptions.append(f"'{col}' has no value labels; assumed 1-2=badly, 3-4=well (Afrobarometer scale).")
        codes = pd.to_numeric(ctx.df[col], errors="coerce")
        well, badly = codes.isin([3, 4]).to_numpy(), codes.isin([1, 2]).to_numpy()
        how = "assumed numeric scale 1-2 badly / 3-4 well"
    valid = well | badly
    return {"status": "ok", "variable": col, "label": ctx.sv.var_labels.get(col, ""),
            "classification": how,
            "definition": "Government handling 'addressing educational needs'. Denominator excludes "
                          "don't know / haven't heard enough / refused.",
            "pct_well": segments(ctx, well, valid),
            "pct_badly": segments(ctx, badly, valid)}


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------
def extract(input_path: Path, iso3: str, *, country_col: str | None = None,
            country_value: str | None = None, weight_col: str | None = None,
            unweighted: bool = False, round_override: str | None = None,
            mip_cols: list[str] | None = None, edu_codes: list[float] | None = None,
            sat_col: str | None = None) -> dict:
    warnings: list[str] = []
    assumptions: list[str] = []
    sv = load_survey(input_path)
    sub, ccol, clabel = filter_country(sv, iso3, country_col, country_value, warnings)
    w, wcol = pick_weights(sv, sub, weight_col, unweighted, warnings)
    seg, ucol = find_urban_rural(sv, sub, warnings, assumptions)
    ctx = Ctx(sv, sub, w, seg, warnings, assumptions)

    indicators: dict[str, dict] = {}
    for name, fn in (("education_priority_problem", lambda: ind_education_priority(ctx, mip_cols, edu_codes)),
                     ("school_deficits", lambda: ind_school_deficits(ctx)),
                     ("satisfaction_education_delivery", lambda: ind_satisfaction(ctx, sat_col))):
        try:
            indicators[name] = fn()
        except ExtractionError:
            raise
        except Exception as e:  # keep the other indicators alive
            log.exception("indicator %s failed", name)
            indicators[name] = {"status": "error", "note": f"{type(e).__name__}: {e}"}

    return {
        "metadata": {
            "country_iso3": iso3,
            "country_label_in_file": clabel,
            "country_column": ccol,
            "round": detect_round(sv, sub, round_override),
            "sample_size_n": int(len(sub)),
            "n_urban": None if seg is None else int((seg == "urban").sum()),
            "n_rural": None if seg is None else int((seg == "rural").sum()),
            "urban_rural_variable": ucol,
            "weight_variable": wcol,
            "weighted": wcol is not None,
            "scale": "percentages on a 0-100 scale; 'n' is the unweighted valid base",
            "source_file": input_path.name,
            "extraction_timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "script_version": __version__,
            "assumptions": assumptions,
            "warnings": warnings,
        },
        "indicators": indicators,
    }


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Extract education indicators from an Afrobarometer survey file.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--input", required=True, type=Path, help="Afrobarometer .sav or .csv file")
    ap.add_argument("--country", required=True, help="ISO3 code, e.g. KEN, NGA, GHA, TZA")
    ap.add_argument("--output", required=True, type=Path, help="output JSON path")
    g = ap.add_argument_group("optional overrides")
    g.add_argument("--round", dest="round_override", help="survey round if it cannot be inferred")
    g.add_argument("--country-column", help="name of the country column")
    g.add_argument("--country-value", help="raw value to select (for label-less numeric country codes)")
    g.add_argument("--weight-col", help="weight variable (default: withinwt if present)")
    g.add_argument("--unweighted", action="store_true", help="ignore weights")
    g.add_argument("--mip-columns", nargs="+", help="most-important-problem columns, e.g. Q45PT1 Q45PT2 Q45PT3")
    g.add_argument("--satisfaction-column", help="column for 'addressing educational needs' (e.g. Q46H), "
                   "needed for CSVs without variable labels")
    g.add_argument("--education-code", nargs="+", type=float,
                   help="numeric 'Education' answer code(s); required only for label-less CSVs")
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
        result = extract(a.input, iso3, country_col=a.country_column, country_value=a.country_value,
                         weight_col=a.weight_col, unweighted=a.unweighted, round_override=a.round_override,
                         mip_cols=a.mip_columns, edu_codes=a.education_code,
                         sat_col=a.satisfaction_column)
    except ExtractionError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    try:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError as e:
        print(f"error: could not write {a.output}: {e}", file=sys.stderr)
        return 2
    ok = [k for k, v in result["indicators"].items() if v.get("status") == "ok"]
    for k, v in result["indicators"].items():
        if v.get("status") != "ok":
            print(f"  - {k}: {v['status']} - {v.get('note', '')}", file=sys.stderr)
    print(f"Wrote {a.output}  (N={result['metadata']['sample_size_n']}, round={result['metadata']['round']}, "
          f"indicators ok: {len(ok)}/3)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
