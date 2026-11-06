#!/usr/bin/env python3
"""
fetch_iati_funding.py
=====================
Extract international development assistance and EdTech funding from the IATI Datastore
(International Aid Transparency Initiative).

Pulls commitments, disbursements, and expenditures for education (DAC 111-114),
ICT/communications (DAC 220), and EdTech-keyword projects across focus countries.
Supports both the IATI Datastore Solr API and offline CSV / JSON exports.

Outputs:
  - iati_funding_by_year.csv: Annual aggregated funding by country, year, sector group, tx_type, currency.
  - iati_transactions.csv: Normalized disaggregated transaction rows with attributed values.
  - iati_audit.json: Metadata, field mappings, coverage, currency tallies, and audit summary.
"""
from __future__ import annotations

import argparse
import ast
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

__version__ = "1.0.0"
log = logging.getLogger("iati")


class IatiError(Exception):
    """A problem the user must fix (missing key, bad query, bad input)."""


AFRICA_ISO_MAP = {
    "AGO": "AO", "BDI": "BI", "BEN": "BJ", "BFA": "BF", "BWA": "BW", "CAF": "CF",
    "CIV": "CI", "CMR": "CM", "COD": "CD", "COG": "CG", "COM": "KM", "CPV": "CV",
    "DJI": "DJ", "DZA": "DZ", "EGY": "EG", "ERI": "ER", "ETH": "ET", "GAB": "GA",
    "GHA": "GH", "GIN": "GN", "GMB": "GM", "GNB": "GW", "GNQ": "GQ", "KEN": "KE",
    "LBR": "LR", "LBY": "LY", "LSO": "LS", "MAR": "MA", "MDG": "MG", "MLI": "ML",
    "MOZ": "MZ", "MRT": "MR", "MUS": "MU", "MWI": "MW", "NAM": "NA", "NER": "NE",
    "NGA": "NG", "RWA": "RW", "SDN": "SD", "SEN": "SN", "SLE": "SL", "SOM": "SO",
    "SSD": "SS", "STP": "ST", "SWZ": "SZ", "SYC": "SC", "TCD": "TD", "TGO": "TG",
    "TUN": "TN", "TZA": "TZ", "UGA": "UG", "ZAF": "ZA", "ZMB": "ZM", "ZWE": "ZW",
}

ALL_SSA_ISO3 = [
    "AGO", "BDI", "BEN", "BFA", "BWA", "CAF", "CIV", "CMR", "COD", "COG",
    "COM", "CPV", "ERI", "ETH", "GAB", "GHA", "GIN", "GMB", "GNB", "GNQ",
    "KEN", "LBR", "LSO", "MDG", "MLI", "MOZ", "MRT", "MUS", "MWI", "NAM",
    "NER", "NGA", "RWA", "SDN", "SEN", "SLE", "SOM", "SSD", "STP", "SWZ",
    "SYC", "TCD", "TGO", "TZA", "UGA", "ZAF", "ZMB", "ZWE",
]

COUNTRY_CODE_MAP = {
    "KEN": "KE", "KE": "KE", "KENYA": "KE",
    "RWA": "RW", "RW": "RW", "RWANDA": "RW",
    "TZA": "TZ", "TZ": "TZ", "TANZANIA": "TZ",
    "MUS": "MU", "MU": "MU", "MAURITIUS": "MU",
    "GHA": "GH", "GH": "GH", "GHANA": "GH",
    "NGA": "NG", "NG": "NG", "NIGERIA": "NG",
    "ZMB": "ZM", "ZM": "ZM", "ZAMBIA": "ZM",
    "UGA": "UG", "UG": "UG", "UGANDA": "UG",
    "ETH": "ET", "ET": "ET", "ETHIOPIA": "ET",
    "MWI": "MW", "MW": "MW", "MALAWI": "MW",
    "SEN": "SN", "SN": "SN", "SENEGAL": "SN",
    "ZAF": "ZA", "ZA": "ZA", "SOUTH AFRICA": "ZA",
    "BWA": "BW", "BW": "BW", "BOTSWANA": "BW",
    "NAM": "NA", "NA": "NA", "NAMIBIA": "NA",
    "MOZ": "MZ", "MZ": "MZ", "MOZAMBIQUE": "MZ",
    "ZWE": "ZW", "ZW": "ZW", "ZIMBABWE": "ZW",
    "SLE": "SL", "SL": "SL", "SIERRA LEONE": "SL",
    "BEN": "BJ", "BJ": "BJ", "BENIN": "BJ",
    "BFA": "BF", "BF": "BF", "BURKINA FASO": "BF",
    "MLI": "ML", "ML": "ML", "MALI": "ML",
    "NER": "NE", "NE": "NE", "NIGER": "NE",
    "CIV": "CI", "CI": "CI", "COTE D'IVOIRE": "CI", "IVORY COAST": "CI",
}
for _iso3, _iso2 in AFRICA_ISO_MAP.items():
    COUNTRY_CODE_MAP[_iso3] = _iso2
    COUNTRY_CODE_MAP[_iso2] = _iso2

DEFAULT_COUNTRIES = ["KEN", "RWA", "TZA", "MUS", "GHA", "NGA", "ZMB"]

TX_TYPE_MAP = {
    "1": "incoming_funds",
    "2": "commitment",
    "3": "disbursement",
    "4": "expenditure",
    "5": "interest_repayment",
    "6": "loan_repayment",
    "7": "reimbursement",
    "8": "purchase_of_equity",
    "9": "sale_of_equity",
    "10": "credit_guarantee",
    "11": "incoming_commitment",
    "12": "outgoing_commitment",
}

FIELD_CANDIDATES = {
    "country": ["recipient_country_code", "recipient_country", "country_code"],
    "sector_code": ["sector_code", "sector"],
    "sector_percentage": ["sector_percentage", "sector_pct", "percentage"],
    "sector_vocab": ["sector_vocabulary", "sector_vocab", "vocabulary"],
    "tx_value": ["transaction_value", "value", "tx_value"],
    "tx_currency": ["transaction_value_currency", "transaction_currency", "currency", "value_currency"],
    "tx_type": ["transaction_transaction_type_code", "transaction_type_code", "transaction_type", "type"],
    "tx_date": ["transaction_transaction_date_iso_date", "transaction_date_iso_date", "transaction_date", "date"],
    "title": ["title_narrative", "title", "title_narrative_text"],
    "desc": ["description_narrative", "description", "description_narrative_text"],
    "reporting_org": ["reporting_org_ref", "reporting_org_narrative", "reporting_org"],
    "iati_id": ["iati_identifier", "iati_id", "identifier", "id"],
}

EDTECH_REGEX = re.compile(
    r"\b(edtech|digital learning|e-learning|elearning|remote learning|distance learning|"
    r"smart classroom|tablets?|educational technology|computer assisted learning|ict in education)\b",
    re.I
)


# --------------------------------------------------------------------------
# Helpers: window & data structures
# --------------------------------------------------------------------------
def resolve_window(years: int, since: int | None, until: int | None, all_years: bool,
                   now_year: int | None = None) -> tuple[int | None, int | None, str]:
    now_year = now_year or datetime.now().year
    if all_years:
        return None, None, "all available years"
    if since is not None or until is not None:
        return since, until, f"{since or 'earliest'}-{until or 'latest'}"
    if years < 1:
        raise IatiError("--years must be at least 1")
    return now_year - years + 1, now_year, f"last {years} years ({now_year - years + 1}-{now_year})"


def as_list(v: Any) -> list:
    if v is None:
        return []
    if isinstance(v, float) and np.isnan(v):
        return []
    if isinstance(v, list):
        return list(v)
    if isinstance(v, (int, float)):
        return [v]
    s = str(v).strip()
    if not s or s.lower() == "nan":
        return []
    if s.startswith("[") and s.endswith("]"):
        try:
            parsed = ast.literal_eval(s)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass
    if ";" in s:
        return [p.strip() for p in s.split(";") if p.strip()]
    return [s]


def normalize_country(code: str) -> str:
    key = str(code).strip().upper()
    if key in COUNTRY_CODE_MAP:
        return COUNTRY_CODE_MAP[key]
    raise IatiError(f"Unknown country code '{code}'. Supported: {sorted(set(COUNTRY_CODE_MAP.keys()))}")


# --------------------------------------------------------------------------
# Solr Query Builder
# --------------------------------------------------------------------------
def build_query(countries: list[str], lo: int | None, hi: int | None, include_edtech: bool,
                field_map: dict[str, str]) -> str:
    parts = []
    c_field = field_map.get("country", FIELD_CANDIDATES["country"][0])
    parts.append(f"{c_field}:({' OR '.join(countries)})")

    s_field = field_map.get("sector_code", FIELD_CANDIDATES["sector_code"][0])
    sector_expr = f"{s_field}:(111* OR 112* OR 113* OR 114* OR 220*)"

    if include_edtech:
        t_field = field_map.get("title", FIELD_CANDIDATES["title"][0])
        d_field = field_map.get("desc", FIELD_CANDIDATES["desc"][0])
        parts.append(f"({sector_expr} OR {t_field}:*edtech* OR {d_field}:*edtech*)")
    else:
        parts.append(sector_expr)

    d_field = field_map.get("tx_date", FIELD_CANDIDATES["tx_date"][0])
    if lo is not None and hi is not None:
        parts.append(f"{d_field}:[{lo}-01-01T00:00:00Z TO {hi}-12-31T23:59:59Z]")
    elif lo is not None:
        parts.append(f"{d_field}:[{lo}-01-01T00:00:00Z TO *]")
    elif hi is not None:
        parts.append(f"{d_field}:[* TO {hi}-12-31T23:59:59Z]")

    return " AND ".join(parts)


# --------------------------------------------------------------------------
# Sector classification & attribution
# --------------------------------------------------------------------------
def classify_dac_sector(code: str) -> str | None:
    c = str(code).strip()
    if c.startswith(("111", "112", "113", "114")):
        return "education"
    if c.startswith("220"):
        return "ict_communications"
    return None


def sector_attribution(codes: list, percentages: list, vocabularies: list) -> dict[str, tuple[float, bool]]:
    c_list = [str(c).strip() for c in (codes or []) if str(c).strip()]
    v_list = [str(v).strip() for v in (vocabularies or [])]
    p_list = []
    for p in (percentages or []):
        try:
            p_list.append(float(p))
        except (ValueError, TypeError):
            p_list.append(0.0)

    can_align = len(c_list) > 0 and len(p_list) == len(c_list) and sum(p_list) > 0

    if can_align:
        matched: dict[str, float] = {}
        for idx, code in enumerate(c_list):
            voc = v_list[idx] if idx < len(v_list) else "1"
            if voc in ("1", "DAC-5", "", "None", "nan"):
                grp = classify_dac_sector(code)
                if grp:
                    pct = p_list[idx]
                    share = pct / 100.0 if pct > 1.0 else pct
                    matched[grp] = matched.get(grp, 0.0) + share
        return {grp: (round(val, 4), True) for grp, val in matched.items()}
    else:
        found = []
        for idx, code in enumerate(c_list):
            voc = v_list[idx] if idx < len(v_list) else "1"
            if voc in ("1", "DAC-5", "", "None", "nan"):
                grp = classify_dac_sector(code)
                if grp and grp not in found:
                    found.append(grp)
        if not found:
            return {}
        default_share = 1.0 / len(found)
        return {grp: (default_share, False) for grp in found}


# --------------------------------------------------------------------------
# Normalization, Filtering, and Aggregation
# --------------------------------------------------------------------------
def parse_year(v: Any) -> int | None:
    if v is None:
        return None
    m = re.search(r"(\d{4})", str(v))
    return int(m.group(1)) if m else None


def normalise(docs: list[dict], field_overrides: dict[str, str] | None = None) -> tuple[pd.DataFrame, dict[str, str], dict]:
    overrides = field_overrides or {}
    if not docs:
        return pd.DataFrame(), {}, {}

    first = docs[0]
    first_keys_low = {k.lower(): k for k in first.keys()}

    # Resolve field mapping
    fm: dict[str, str] = {}
    for key, candidates in FIELD_CANDIDATES.items():
        if key in overrides:
            ov = overrides[key]
            if ov not in first and ov.lower() not in first_keys_low:
                raise IatiError(f"--field {key}={ov}: column not found. Available: {list(first.keys())}")
            fm[key] = ov if ov in first else first_keys_low[ov.lower()]
            continue
        matched = None
        for cand in candidates:
            if cand in first:
                matched = cand
                break
            if cand.lower() in first_keys_low:
                matched = first_keys_low[cand.lower()]
                break
        if matched:
            fm[key] = matched

    # Validate essential fields
    for req in ("tx_value", "country", "tx_date"):
        if req not in fm:
            raise IatiError(f"Missing required field for '{req}'. Use --field {req}=NAME to specify. "
                            f"Available fields: {list(first.keys())}")

    rows = []
    currencies_seen = set()
    latest_year_by_country: dict[str, int] = {}

    for doc in docs:
        # Date & Year
        raw_date = as_list(doc.get(fm.get("tx_date", "")))
        year = parse_year(raw_date[0]) if raw_date else None
        if year is None:
            continue

        # Country
        raw_country = as_list(doc.get(fm.get("country", "")))
        if not raw_country:
            continue
        try:
            iso2 = normalize_country(raw_country[0])
        except IatiError:
            continue

        # Value
        raw_val = as_list(doc.get(fm.get("tx_value", "")))
        if not raw_val:
            continue
        try:
            val = float(raw_val[0])
        except (ValueError, TypeError):
            continue

        # Currency
        curr_field = fm.get("tx_currency")
        raw_curr = as_list(doc.get(curr_field, "")) if curr_field else []
        curr = str(raw_curr[0]).upper() if raw_curr else "USD"
        currencies_seen.add(curr)

        # Transaction type
        type_field = fm.get("tx_type")
        raw_type = as_list(doc.get(type_field, "")) if type_field else []
        t_code = str(raw_type[0]).strip() if raw_type else "3"
        tx_type = TX_TYPE_MAP.get(t_code, t_code.lower())

        # Identifiers & Narrative
        id_field = fm.get("iati_id")
        iati_id = str(as_list(doc.get(id_field, ""))[0]) if id_field and doc.get(id_field) else ""
        t_field = fm.get("title")
        title_list = as_list(doc.get(t_field, "")) if t_field else []
        title_str = " ".join(map(str, title_list))
        d_field = fm.get("desc")
        desc_list = as_list(doc.get(d_field, "")) if d_field else []
        desc_str = " ".join(map(str, desc_list))
        combined_text = f"{title_str} {desc_str}"

        # Sector codes, percentages, and vocabularies
        sec_field = fm.get("sector_code")
        pct_field = fm.get("sector_percentage")
        voc_field = fm.get("sector_vocab")

        sec_codes = as_list(doc.get(sec_field, "")) if sec_field else []
        sec_pcts = as_list(doc.get(pct_field, "")) if pct_field else []
        sec_vocs = as_list(doc.get(voc_field, "")) if voc_field else []

        attribution = sector_attribution(sec_codes, sec_pcts, sec_vocs)

        if not attribution:
            # Fallback to EdTech keyword search in narrative text
            if EDTECH_REGEX.search(combined_text):
                attribution = {"edtech_keyword": (1.0, True)}

        if not attribution:
            continue

        # Update latest year per country
        if iso2 not in latest_year_by_country or year > latest_year_by_country[iso2]:
            latest_year_by_country[iso2] = year

        for grp, (share, share_known) in attribution.items():
            rows.append({
                "iati_id": iati_id,
                "country_iso2": iso2,
                "year": year,
                "group": grp,
                "tx_type": tx_type,
                "currency": curr,
                "value": val,
                "share": share,
                "value_attributed": round(val * share, 2),
                "sector_share_known": share_known,
                "title": title_str,
            })

    df_tx = pd.DataFrame(rows)
    audit_meta = {
        "currencies_seen": sorted(currencies_seen),
        "latest_year_with_data": latest_year_by_country,
    }
    return df_tx, fm, audit_meta


def filter_window(df: pd.DataFrame, lo: int | None, hi: int | None, countries: list[str]) -> pd.DataFrame:
    if df.empty:
        return df
    iso2_targets = {normalize_country(c) for c in countries}
    out = df[df["country_iso2"].isin(iso2_targets)].copy()
    if lo is not None:
        out = out[out["year"] >= lo]
    if hi is not None:
        out = out[out["year"] <= hi]
    return out


def funding_by_year(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["country_iso2", "year", "group", "tx_type", "currency", "value"])
    keys = ["country_iso2", "year", "group", "tx_type", "currency"]
    agg = df.groupby(keys, as_index=False)["value_attributed"].sum()
    agg = agg.rename(columns={"value_attributed": "value"})
    agg["value"] = agg["value"].round(2)
    return agg.sort_values(["country_iso2", "year", "group", "tx_type"], ascending=[True, False, True, True])


# --------------------------------------------------------------------------
# IatiClient: Solr API connection
# --------------------------------------------------------------------------
class IatiClient:
    def __init__(self, session=None, base_url: str = "https://api.iatistandard.org/datastore",
                 api_key: str | None = None, key_header: str = "Ocp-Apim-Subscription-Key"):
        import requests
        self.session = session or requests.Session()
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.key_header = key_header

    def select(self, endpoint: str, q: str, rows: int = 1000, max_rows: int | None = None,
               sleep: float = 0.2) -> tuple[list[dict], int]:
        clean_ep = endpoint.strip("/")
        url = f"{self.base_url}/{clean_ep}/select"
        headers = {}
        if self.api_key:
            headers[self.key_header] = self.api_key

        docs: list[dict] = []
        start = 0
        total = 0

        while True:
            fetch_rows = rows
            if max_rows is not None:
                remaining = max_rows - len(docs)
                if remaining <= 0:
                    break
                fetch_rows = min(rows, remaining)

            params = {"q": q, "wt": "json", "rows": fetch_rows, "start": start}
            r = self.session.get(url, params=params, headers=headers)
            if r.status_code == 401:
                raise IatiError("IATI API returned 401 Unauthorized: Get an API key at developer.iatistandard.org "
                                "and set IATI_API_KEY environment variable.")
            if r.status_code == 400:
                raise IatiError(f"IATI API returned 400 Bad Request: Check --q query syntax ({url}?{params}).")
            if r.status_code == 404:
                raise IatiError(f"IATI API returned 404 Not Found: Check --base-url ({url}).")
            if r.status_code >= 400:
                r.raise_for_status()

            data = r.json()
            resp = data.get("response", {})
            total = resp.get("numFound", 0)
            batch = resp.get("docs", [])
            if not batch:
                break
            docs.extend(batch)

            if max_rows is not None and len(docs) >= max_rows:
                docs = docs[:max_rows]
                break

            start += len(batch)
            if start >= total:
                break

            if sleep > 0:
                time.sleep(sleep)

        return docs, total


# --------------------------------------------------------------------------
# CLI Runner
# --------------------------------------------------------------------------
def run(a) -> dict:
    if getattr(a, "all_ssa", False):
        a.countries = list(ALL_SSA_ISO3)

    lo, hi, label = resolve_window(a.years, a.since, a.until, a.all_years)
    iso2_countries = [normalize_country(c) for c in a.countries]

    overrides = {}
    for item in a.field or []:
        k, _, v = item.partition("=")
        if k not in FIELD_CANDIDATES or not v:
            raise IatiError(f"--field expects KEY=NAME with KEY in {sorted(FIELD_CANDIDATES)}")
        overrides[k] = v

    field_map = {k: overrides.get(k, FIELD_CANDIDATES[k][0]) for k in FIELD_CANDIDATES}
    q = a.q or build_query(iso2_countries, lo, hi, not a.no_edtech, field_map)

    audit: dict[str, Any] = {
        "script_version": __version__,
        "window": label,
        "query": q,
        "countries_requested": a.countries,
        "countries_iso2": iso2_countries,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    if a.dry_run:
        url = f"{a.base_url.rstrip('/')}/{a.endpoint.strip('/')}/select"
        print(f"Window: {label}\nGET {url}\nquery: {q}\nHeader: {a.key_header}")
        return audit

    out = Path(a.out)
    docs: list[dict] = []

    # Check local cache first if no input file is specified and not forced refresh
    cached_tx_path = out / "iati_transactions.csv"
    if not a.input and not getattr(a, "force_refresh", False) and cached_tx_path.is_file():
        try:
            cached_df = pd.read_csv(cached_tx_path, low_memory=False)
            cached_iso2 = set(cached_df["country_iso2"].dropna().unique())
            missing_iso2 = [c for c in iso2_countries if c not in cached_iso2]
            if not missing_iso2:
                # Full cache hit!
                tx_filtered = filter_window(cached_df, lo, hi, iso2_countries)
                fy = funding_by_year(tx_filtered)
                out.mkdir(parents=True, exist_ok=True)
                fy.to_csv(out / "iati_funding_by_year.csv", index=False)
                audit["source"] = f"cached {cached_tx_path.name}"
                audit["rows_transactions"] = int(len(tx_filtered))
                audit["rows_funding_by_year"] = int(len(fy))
                (out / "iati_audit.json").write_text(json.dumps(audit, indent=2, default=str), encoding="utf-8")
                print(f"Loaded {len(tx_filtered)} transactions from cache ({cached_tx_path}) for {iso2_countries} (use --force-refresh to bypass).")
                return audit
            else:
                # Incremental fetch for missing countries only
                key = os.environ.get(a.key_env, "")
                if not key:
                    raise IatiError(f"API key missing to fetch newly requested countries {missing_iso2}. "
                                    f"Set {a.key_env} or provide an offline download with --input.")
                q_missing = build_query(missing_iso2, lo, hi, not a.no_edtech, field_map)
                client = IatiClient(base_url=a.base_url, api_key=key, key_header=a.key_header)
                new_docs, total = client.select(a.endpoint, q_missing, rows=a.rows, max_rows=a.max_rows)
                new_tx, detected_fm, extra_audit = normalise(new_docs, overrides)
                combined_tx = pd.concat([cached_df, new_tx], ignore_index=True)
                tx_all = combined_tx.drop_duplicates(subset=["iati_id", "country_iso2", "year", "group", "tx_type", "currency"])
                tx_filtered = filter_window(tx_all, lo, hi, iso2_countries)
                fy = funding_by_year(tx_filtered)
                out.mkdir(parents=True, exist_ok=True)
                fy.to_csv(out / "iati_funding_by_year.csv", index=False)
                tx_all.to_csv(out / "iati_transactions.csv", index=False)
                audit["source"] = f"merged API + cached {cached_tx_path.name}"
                audit["rows_transactions"] = int(len(tx_filtered))
                audit["rows_funding_by_year"] = int(len(fy))
                audit["field_mapping"] = detected_fm
                audit.update(extra_audit)
                (out / "iati_audit.json").write_text(json.dumps(audit, indent=2, default=str), encoding="utf-8")
                print(f"Fetched {len(new_tx)} new transactions for {missing_iso2} and merged into cache ({len(tx_all)} total).")
                return audit
        except Exception as e:
            if not isinstance(e, IatiError):
                log.warning(f"Failed to read cache {cached_tx_path}: {e}; falling back to standard fetch.")

    if a.input:
        p = Path(a.input)
        if not p.exists():
            raise IatiError(f"Input file not found: {p}")
        try:
            if p.suffix.lower() == ".csv":
                df_raw = pd.read_csv(p, low_memory=False)
                docs = df_raw.to_dict(orient="records")
            else:
                data = json.loads(p.read_text(encoding="utf-8"))
                docs = data.get("response", {}).get("docs", data) if isinstance(data, dict) else data
        except Exception as e:
            raise IatiError(f"Could not read {p.name}: {e}") from e
        audit["source"] = f"file {p.name}"
    else:
        key = os.environ.get(a.key_env, "")
        if not key:
            raise IatiError(f"API key missing. Set {a.key_env} or provide an offline download with --input.")
        client = IatiClient(base_url=a.base_url, api_key=key, key_header=a.key_header)
        docs, total = client.select(a.endpoint, q, rows=a.rows, max_rows=a.max_rows)
        audit["source"] = f"API {a.base_url}"
        audit["total_found_api"] = total

    audit["raw_records_count"] = len(docs)
    tx_all, detected_fm, extra_audit = normalise(docs, overrides)
    audit["field_mapping"] = detected_fm
    audit.update(extra_audit)

    tx_filtered = filter_window(tx_all, lo, hi, iso2_countries)
    fy = funding_by_year(tx_filtered)

    out.mkdir(parents=True, exist_ok=True)
    fy.to_csv(out / "iati_funding_by_year.csv", index=False)
    tx_filtered.to_csv(out / "iati_transactions.csv", index=False)

    audit["rows_transactions"] = int(len(tx_filtered))
    audit["rows_funding_by_year"] = int(len(fy))
    (out / "iati_audit.json").write_text(json.dumps(audit, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {out}/  ({len(fy)} aggregate rows; {len(tx_filtered)} transactions; window: {label})")
    return audit


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--countries", nargs="+", default=DEFAULT_COUNTRIES, help="Country ISO3 or ISO2 codes")
    ap.add_argument("--all-ssa", action="store_true", help="Fetch/process all 48 Sub-Saharan African economies")
    ap.add_argument("--years", type=int, default=5, help="most recent N calendar years (default 5)")
    ap.add_argument("--since", type=int, help="start year")
    ap.add_argument("--until", type=int, help="end year")
    ap.add_argument("--all-years", action="store_true", help="full history")
    ap.add_argument("--out", default="data/iati", help="output directory")
    ap.add_argument("--input", help="CSV or JSON file downloaded from IATI")
    ap.add_argument("--force-refresh", action="store_true", help="Bypass local cache and re-fetch from API")
    ap.add_argument("--dry-run", action="store_true", help="print request and exit")
    ap.add_argument("--field", action="append", metavar="KEY=NAME", help=f"force a column override; keys: {', '.join(FIELD_CANDIDATES)}")
    ap.add_argument("--base-url", default="https://api.iatistandard.org/datastore")
    ap.add_argument("--endpoint", default="transaction")
    ap.add_argument("--key-env", default="IATI_API_KEY")
    ap.add_argument("--key-header", default="Ocp-Apim-Subscription-Key")
    ap.add_argument("--q", help="custom Solr query")
    ap.add_argument("--no-edtech", action="store_true", help="exclude edtech keyword search")
    ap.add_argument("--rows", type=int, default=1000, help="Solr pagination rows per page")
    ap.add_argument("--max-rows", type=int, help="max total rows to fetch")
    ap.add_argument("-v", "--verbose", action="store_true")
    return ap


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.WARNING, format="%(levelname)s: %(message)s")
    try:
        run(a)
    except IatiError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
