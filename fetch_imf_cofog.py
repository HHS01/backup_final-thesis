#!/usr/bin/env python3
"""
fetch_imf_cofog.py
==================
Government spending BY FUNCTION (IMF GFS "COFOG") for your focus countries: education (COFOG 09),
communication (04.6), transport (04.5) and, where the data allow, each as a share of total spending.
Defaults to the MOST RECENT years; history is a flag away.

    # 1) most reliable: download a CSV from the IMF data portal (https://data.imf.org, dataset
    #    "Government Finance Statistics: Expenditure by Function of Government"), then:
    python fetch_imf_cofog.py --input cofog_download.csv --out data/imf
    python fetch_imf_cofog.py --input cofog_download.csv --years 10
    python fetch_imf_cofog.py --input cofog_download.csv --since 2000 --until 2015
    python fetch_imf_cofog.py --input cofog_download.csv --all-years
    python fetch_imf_cofog.py --input cofog_download.csv --list-functions   # see the codes the file uses

    # 2) best-effort API call (unverified host/params; preview first):
    python fetch_imf_cofog.py --api --dry-run
    python fetch_imf_cofog.py --api --out data/imf

Default countries: Kenya, Rwanda, Tanzania, Mauritius, Ghana, Nigeria, Zambia (--countries to change).

Outputs (in --out): imf_cofog_long.csv, imf_cofog_shares.csv, imf_cofog_coverage.csv, imf_cofog_audit.json

VERIFIED: the IMF serves data through a new SDMX 3.0 REST API at data.imf.org (the old JSON service is
being retired); dataflows have ids such as GFS_COFOG under agency IMF.STA; queries take a dot-separated key
or named filters; an SDMX-CSV representation exists; an API key is optional for open data.
NOT VERIFIED: the API host path, the filter parameter names, and the COFOG dimension/column names and
codes. Hence: columns are detected by name, function codes by pattern (--education-pattern etc. to
override, --list-functions to inspect), and every choice is written to the audit file.

CAVEATS
  * Coverage of sub-Saharan Africa in GFS COFOG is patchy and lags 9-12+ months; the coverage file shows
    exactly which country-years exist. A missing year is missing, not zero.
  * Level of government differs (central vs general) between countries; a 'sector' column is kept so you
    can compare like with like. Shares are computed only within identical country/year/sector/unit.
  * COFOG measures spending by purpose, not by programme: EdTech or connectivity budgets are not
    separable here; 04.6 "Communication" is the closest connectivity proxy.
"""
from __future__ import annotations

import argparse
import io
import json
import logging
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

__version__ = "1.0.0"
log = logging.getLogger("imf")


class ImfError(Exception):
    """A problem the user must fix (bad input, no columns found, API failure)."""


COUNTRY_NAMES = {
    "AGO": ["Angola"], "BDI": ["Burundi"], "BEN": ["Benin"], "BFA": ["Burkina Faso"],
    "BWA": ["Botswana"], "CAF": ["Central African Republic"], "CIV": ["Cote d'Ivoire", "Ivory Coast"],
    "CMR": ["Cameroon"], "COD": ["Congo, Dem. Rep.", "Democratic Republic of the Congo"],
    "COG": ["Congo, Rep.", "Republic of the Congo"], "COM": ["Comoros"], "CPV": ["Cabo Verde", "Cape Verde"],
    "DJI": ["Djibouti"], "DZA": ["Algeria"], "EGY": ["Egypt"], "ERI": ["Eritrea"], "ETH": ["Ethiopia"],
    "GAB": ["Gabon"], "GHA": ["Ghana"], "GIN": ["Guinea"], "GMB": ["Gambia"], "GNB": ["Guinea-Bissau"],
    "GNQ": ["Equatorial Guinea"], "KEN": ["Kenya"], "LBR": ["Liberia"], "LBY": ["Libya"],
    "LSO": ["Lesotho"], "MAR": ["Morocco"], "MDG": ["Madagascar"], "MLI": ["Mali"], "MOZ": ["Mozambique"],
    "MRT": ["Mauritania"], "MUS": ["Mauritius"], "MWI": ["Malawi"], "NAM": ["Namibia"], "NER": ["Niger"],
    "NGA": ["Nigeria"], "RWA": ["Rwanda"], "SDN": ["Sudan"], "SEN": ["Senegal"], "SLE": ["Sierra Leone"],
    "SOM": ["Somalia"], "SSD": ["South Sudan"], "STP": ["Sao Tome and Principe"], "SWZ": ["Eswatini", "Swaziland"],
    "SYC": ["Seychelles"], "TCD": ["Chad"], "TGO": ["Togo"], "TUN": ["Tunisia"],
    "TZA": ["Tanzania", "United Republic of Tanzania"], "UGA": ["Uganda"], "ZAF": ["South Africa"],
    "ZMB": ["Zambia"], "ZWE": ["Zimbabwe"]
}

ALL_SSA_ISO3 = [
    "AGO", "BDI", "BEN", "BFA", "BWA", "CAF", "CIV", "CMR", "COD", "COG",
    "COM", "CPV", "ERI", "ETH", "GAB", "GHA", "GIN", "GMB", "GNB", "GNQ",
    "KEN", "LBR", "LSO", "MDG", "MLI", "MOZ", "MRT", "MUS", "MWI", "NAM",
    "NER", "NGA", "RWA", "SDN", "SEN", "SLE", "SOM", "SSD", "STP", "SWZ",
    "SYC", "TCD", "TGO", "TZA", "UGA", "ZAF", "ZMB", "ZWE",
]

DEFAULT_COUNTRIES = ["KEN", "RWA", "TZA", "MUS", "GHA", "NGA", "ZMB"]


def rx(p: str) -> re.Pattern:
    return re.compile(p, re.I)


# Patterns applied to the function code (and any label-like text). COFOG 1999: 09 Education,
# 04.5 Transport, 04.6 Communication; the total is whatever "total expenditure" row the file has.
FUNCTION_PATTERNS = {
    "education": r"^(gf)?0?9(\.?\d{1,2})?(_[a-z0-9]+)?$|education",
    "communication": r"^(gf)?0?46(\.?\d)?0?(_[a-z0-9]+)?$|^0?4\.6(\.\d)?$|communicat",
    "transport": r"^(gf)?0?45(\.?\d)?0?(_[a-z0-9]+)?$|^0?4\.5(\.\d)?$|transport",
    "total": r"^(gf|total|tot|_t|_z|gf00|00|totout)(_[a-z0-9]+)?$|total expenditure|^total$|total government expenditure|totout",
}
# Top-level (aggregate) codes: sub-functions such as GF0901 are INSIDE GF09, so never sum across levels.
TOP_LEVEL = {
    "education": r"^(gf)?0?9(_[a-z0-9]+)?$",
    "communication": r"^(gf)?0?460?(_[a-z0-9]+)?$|^0?4\.6$",
    "transport": r"^(gf)?0?450?(_[a-z0-9]+)?$|^0?4\.5$",
    "total": r".*"
}
# Column-name detection (SDMX-CSV dimension ids are unverified; labels differ by download type).
COLUMN_PATTERNS = {
    "country": r"^(country|ref_?area|economy|geo|iso3?|reporter|area)(_?(code|id|name|label))?$|country",
    "function": r"^(indicator|cofog)$|cofog|function|expense_?class|indicator|classification",
    "time": r"^(time_?period|time|period|year)$|time_?period",
    "value": r"^obs_?value$|^value$|obs.?val",
    "unit": r"^(type_of_transformation|unit_measure|unit)$|unit|measure|transformation|scale",
    "sector": r"^sector$|sector|government_?level|level_?of_?government|institutional",
    "label": r"label|description|desc|name",
}


# --------------------------------------------------------------------------
# Window + country helpers
# --------------------------------------------------------------------------
def resolve_window(years: int, since: int | None, until: int | None, all_years: bool,
                   now_year: int | None = None) -> tuple[int | None, int | None, str]:
    now_year = now_year or datetime.now().year
    if all_years:
        return None, None, "all available years"
    if since is not None or until is not None:
        return since, until, f"{since or 'earliest'}-{until or 'latest'}"
    if years < 1:
        raise ImfError("--years must be at least 1")
    return now_year - years + 1, now_year, f"last {years} years ({now_year - years + 1}-{now_year})"


def _norm(s: Any) -> str:
    t = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def country_matcher(iso3: list[str]):
    bad = [c for c in iso3 if c not in COUNTRY_NAMES]
    if bad:
        raise ImfError(f"Unknown ISO3 code(s) {bad}. Known: {sorted(COUNTRY_NAMES)}")
    alias = {}
    for c in iso3:
        alias[c.lower()] = c
        for n in COUNTRY_NAMES[c]:
            alias[_norm(n)] = c
    return lambda v: alias.get(_norm(v))


# --------------------------------------------------------------------------
# Column detection and function classification
# --------------------------------------------------------------------------
def detect_columns(df: pd.DataFrame, overrides: dict[str, str]) -> dict[str, str | None]:
    low = {c.lower(): c for c in df.columns}
    out: dict[str, str | None] = {}
    for key, pat in COLUMN_PATTERNS.items():
        if key in overrides:
            if overrides[key].lower() not in low:
                raise ImfError(f"--col {key}={overrides[key]}: no such column. Columns: {list(df.columns)}")
            out[key] = low[overrides[key].lower()]
            continue
        hits = [c for c in df.columns if re.search(pat, c, re.I)]
        if key == "value":
            hits = [c for c in hits if pd.api.types.is_numeric_dtype(df[c]) or pd.to_numeric(df[c], errors="coerce").notna().mean() > .8]
        if key == "label":   # label-like text columns that are not the country/unit columns
            hits = [c for c in hits if not re.search(r"country|unit|sector|time|obs|ref_?area", c, re.I)]
        out[key] = hits[0] if hits else None
    return out


def classify_functions(texts: pd.Series, patterns: dict[str, str]) -> pd.Series:
    rxs = {k: rx(v) for k, v in patterns.items()}

    def one(t: Any) -> str | None:
        s = str(t).strip()
        for g in ("total", "education", "communication", "transport"):   # total first: avoids 'total education'
            if rxs[g].search(s):
                return g
        return None
    return texts.map(one)


def parse_year(v: Any) -> float:
    m = re.match(r"\s*(\d{4})", str(v))
    return float(m.group(1)) if m else np.nan


# --------------------------------------------------------------------------
# Core processing
# --------------------------------------------------------------------------
def process(df: pd.DataFrame, iso3: list[str], lo: int | None, hi: int | None, overrides: dict[str, str],
            patterns: dict[str, str]) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    cols = detect_columns(df, overrides)
    missing = [k for k in ("country", "function", "time", "value") if cols[k] is None]
    if missing:
        raise ImfError(f"Could not find columns for {missing}. Columns present: {list(df.columns)}. "
                       "Use --col country=NAME function=NAME time=NAME value=NAME.")
    match = country_matcher(iso3)
    d = df.copy()
    d["_iso3"] = d[cols["country"]].map(match)
    d = d[d["_iso3"].notna()]
    if d.empty:
        seen = sorted({str(v) for v in df[cols["country"]].dropna().unique()})[:30]
        raise ImfError(f"No rows for countries {iso3} in column '{cols['country']}'. Values include: {seen}")
    d["_year"] = d[cols["time"]].map(parse_year)
    d["_value"] = pd.to_numeric(d[cols["value"]], errors="coerce")
    d = d.dropna(subset=["_year", "_value"])
    fn_text = d[cols["function"]].astype(str)
    if cols["label"] and cols["label"] != cols["function"]:
        fn_text = fn_text + " " + d[cols["label"]].astype(str)
    d["_group"] = classify_functions(d[cols["function"]].astype(str), patterns)
    by_label = classify_functions(fn_text, patterns)
    d["_group"] = d["_group"].where(d["_group"].notna(), by_label)
    d = d[d["_group"].notna()].copy()
    d["_year"] = d["_year"].astype(int)
    code_group = classify_functions(d[cols["function"]].astype(str), patterns)
    d["_level"] = [("label-matched" if pd.isna(cg) else "aggregate" if re.match(TOP_LEVEL[g], str(c).strip(), re.I)
                    else "sub-function") for cg, g, c in zip(code_group, d["_group"], d[cols["function"]])]
    # coverage is computed BEFORE the window filter so gaps and lags are visible
    cov_rows = []
    for c in iso3:
        sub = d[d["_iso3"] == c]
        cov_rows.append({"country": c, "years_any": int(sub["_year"].nunique()),
                         "first_year": int(sub["_year"].min()) if len(sub) else None,
                         "latest_year": int(sub["_year"].max()) if len(sub) else None,
                         **{f"has_{g}": bool((sub["_group"] == g).any()) for g in ("education", "communication", "transport", "total")}})
    cov = pd.DataFrame(cov_rows)
    if lo is not None:
        d = d[d["_year"] >= lo]
    if hi is not None:
        d = d[d["_year"] <= hi]
    key_cols = [c for c in (cols["sector"], cols["unit"]) if c]
    long = d.rename(columns={"_iso3": "country_iso3", "_year": "year", "_value": "value", "_group": "group",
                             "_level": "level"})
    keep = ["country_iso3", "year", "group", "level", cols["function"], "value"] + key_cols
    long = long[list(dict.fromkeys(keep))].sort_values(["country_iso3", "group", "year"], ascending=[True, True, False])
    # shares: function value / total expenditure, only within identical country, year, sector, unit
    keys = ["country_iso3", "year"] + key_cols
    tot = long[long["group"] == "total"].drop_duplicates(keys)[keys + ["value"]].rename(columns={"value": "total_value"})
    fun = long[long["group"].isin(["education", "communication", "transport"])]
    shares = fun.merge(tot, on=keys, how="left")
    shares["share_of_total_pct"] = (shares["value"] / shares["total_value"] * 100).round(2)
    audit = {"columns_detected": cols, "countries_requested": iso3,
             "countries_found": sorted(set(long["country_iso3"])) if len(long) else [],
             "rows_long": int(len(long)), "share_rows": int(shares["share_of_total_pct"].notna().sum()),
             "distinct_units": sorted({str(u) for u in long[cols["unit"]].unique()})[:20] if cols["unit"] else [],
             "distinct_sectors": sorted({str(u) for u in long[cols["sector"]].unique()})[:20] if cols["sector"] else [],
             "latest_year_by_country": {r.country: r.latest_year for r in cov.itertuples() if r.latest_year}}
    return long, shares, {"audit": audit, "coverage": cov}


def list_functions(df: pd.DataFrame, overrides: dict[str, str]) -> pd.DataFrame:
    cols = detect_columns(df, overrides)
    if cols["function"] is None:
        raise ImfError(f"No function column found. Columns: {list(df.columns)}")
    cc = [cols["function"]] + ([cols["label"]] if cols["label"] and cols["label"] != cols["function"] else [])
    return df[cc].drop_duplicates().sort_values(cc[0]).reset_index(drop=True)


# --------------------------------------------------------------------------
# API (best effort, unverified host/params)
# --------------------------------------------------------------------------
DEFAULT_BASE = "https://api.imf.org/external/sdmx/3.0"


def build_api_request(base: str, flow: str, agency: str, iso3: list[str], lo: int | None, hi: int | None,
                      country_dim: str, time_dim: str) -> tuple[str, dict]:
    key_str = f"{'+'.join(iso3)}.*.*.*.*.*"
    url = f"{base.rstrip('/')}/data/dataflow/{agency}/{flow}/11.0.0/{key_str}"
    params = {}
    if lo is not None:
        params["startPeriod"] = str(lo)
    if hi is not None:
        params["endPeriod"] = str(hi)
    return url, params


def fetch_api(a, iso3: list[str], lo: int | None, hi: int | None) -> pd.DataFrame:
    import requests
    url, params = build_api_request(a.base_url, a.flow, a.agency, iso3, lo, hi, a.country_dim, a.time_dim)
    headers = {"Accept": a.accept, "User-Agent": "imf-cofog-fetcher/1.0 (research)"}
    key = os.environ.get(a.key_env, "")
    if key:
        headers[a.key_header] = key
    r = requests.get(url, params=params, headers=headers, timeout=180)
    if r.status_code in (401, 403):
        raise ImfError(f"IMF API returned {r.status_code}: set {a.key_env} (request a key on data.imf.org) or use --input.")
    if r.status_code in (400, 404):
        raise ImfError(f"IMF API returned {r.status_code}: the host path or filter names probably differ from the "
                       f"defaults ({r.url}). Check data.imf.org's API docs, adjust --base-url/--country-dim/--time-dim, "
                       f"or download a CSV and use --input. Response: {r.text[:200]}")
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text), low_memory=False)


# --------------------------------------------------------------------------
def run(a) -> dict:
    if getattr(a, "all_ssa", False):
        a.countries = list(ALL_SSA_ISO3)
    out = Path(a.out)
    lo, hi, label = resolve_window(a.years, a.since, a.until, a.all_years)
    iso3 = [c.upper() for c in a.countries]
    country_matcher(iso3)   # validate early
    overrides = {}
    for item in a.col or []:
        k, _, v = item.partition("=")
        if k not in COLUMN_PATTERNS or not v:
            raise ImfError(f"--col expects KEY=NAME with KEY in {sorted(COLUMN_PATTERNS)}")
        overrides[k] = v
    patterns = dict(FUNCTION_PATTERNS)
    for g in ("education", "communication", "transport", "total"):
        v = getattr(a, f"{g}_pattern", None)
        if v:
            patterns[g] = v
    audit: dict[str, Any] = {"script_version": __version__, "window": label,
                             "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    if a.dry_run:
        url, params = build_api_request(a.base_url, a.flow, a.agency, iso3, lo, hi, a.country_dim, a.time_dim)
        print(f"Window: {label}\nGET {url}\nparams: {json.dumps(params)}\nAccept: {a.accept}")
        return audit

    # Check cache if not explicitly running an input file or forced refresh
    cached_shares_path = out / "imf_cofog_shares.csv"
    if not a.input and not getattr(a, "force_refresh", False) and cached_shares_path.is_file():
        try:
            cached_shares = pd.read_csv(cached_shares_path, low_memory=False)
            cached_iso3 = set(cached_shares["country_iso3"].dropna().unique())
            if set(iso3).issubset(cached_iso3) or not a.api:
                audit["source"] = f"cached {cached_shares_path.name}"
                audit["rows_read"] = int(len(cached_shares))
                print(f"Using cached IMF COFOG data from {out} for {iso3} (use --force-refresh or --input to reload).")
                return audit
        except Exception as e:
            log.warning(f"Could not read cache {cached_shares_path}: {e}")

    if a.input:
        p = Path(a.input)
        if not p.exists():
            raise ImfError(f"Input file not found: {p}")
        try:
            df = pd.read_csv(p, low_memory=False) if p.suffix.lower() == ".csv" else pd.read_excel(p)
        except Exception as e:
            raise ImfError(f"Could not read {p.name}: {e}") from e
        audit["source"] = f"file {p.name}"
    elif a.api:
        df = fetch_api(a, iso3, lo, hi)
        audit["source"] = f"API {a.base_url}"
    else:
        raise ImfError("Choose a source: --input FILE (recommended) or --api.")
    audit["rows_read"] = int(len(df))
    if a.list_functions:
        print(list_functions(df, overrides).to_string(index=False))
        return audit
    long, shares, extra = process(df, iso3, lo, hi, overrides, patterns)
    audit.update(extra["audit"])
    out.mkdir(parents=True, exist_ok=True)
    long.to_csv(out / "imf_cofog_long.csv", index=False)
    shares.to_csv(out / "imf_cofog_shares.csv", index=False)
    extra["coverage"].to_csv(out / "imf_cofog_coverage.csv", index=False)
    audit["caveats"] = ["do not sum across 'level' values: sub-functions sit inside their aggregate",
                        "coverage patchy and lagged for SSA", "central vs general government differs by country",
                        "missing year means no data, not zero", "COFOG is by purpose, not by programme"]
    if len(long) == 0:
        audit["warning"] = f"No rows left in window {label}; see imf_cofog_coverage.csv for the years that exist."
        print(f"  warning: {audit['warning']}")
    (out / "imf_cofog_audit.json").write_text(json.dumps(audit, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {out}/  ({len(long)} rows; {audit['share_rows']} with shares; window: {label})")
    return audit


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--countries", nargs="+", default=DEFAULT_COUNTRIES, help="ISO3 codes")
    ap.add_argument("--all-ssa", action="store_true", help="Process all 48 Sub-Saharan African economies")
    ap.add_argument("--years", type=int, default=5, help="most recent N calendar years (default 5)")
    ap.add_argument("--since", type=int)
    ap.add_argument("--until", type=int)
    ap.add_argument("--all-years", action="store_true", help="full history")
    ap.add_argument("--out", default="data/imf")
    ap.add_argument("--input", help="CSV/Excel downloaded from data.imf.org")
    ap.add_argument("--api", action="store_true", help="best-effort API call (unverified defaults)")
    ap.add_argument("--force-refresh", action="store_true", help="Bypass local cache and re-process")
    ap.add_argument("--dry-run", action="store_true", help="print the API request and exit")
    ap.add_argument("--list-functions", action="store_true", help="list the function codes found in the file and exit")
    ap.add_argument("--col", action="append", metavar="KEY=NAME", help=f"force a column; keys: {', '.join(COLUMN_PATTERNS)}")
    for g in ("education", "communication", "transport", "total"):
        ap.add_argument(f"--{g}-pattern", help=f"regex for the {g} function code (default: {FUNCTION_PATTERNS[g]})")
    ap.add_argument("--base-url", default=DEFAULT_BASE, help="UNVERIFIED default")
    ap.add_argument("--flow", default="GFS_COFOG")
    ap.add_argument("--agency", default="IMF.STA")
    ap.add_argument("--country-dim", default="COUNTRY", help="UNVERIFIED dimension id")
    ap.add_argument("--time-dim", default="TIME_PERIOD")
    ap.add_argument("--accept", default="application/vnd.sdmx.data+csv; version=2.0.0")
    ap.add_argument("--key-env", default="IMF_API_KEY")
    ap.add_argument("--key-header", default="Ocp-Apim-Subscription-Key", help="UNVERIFIED default")
    ap.add_argument("-v", "--verbose", action="store_true")
    return ap


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.WARNING, format="%(levelname)s: %(message)s")
    try:
        run(a)
    except ImfError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
