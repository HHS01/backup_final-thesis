#!/usr/bin/env python3
"""
UNESCO 6-Pillars EdTech Data Pipeline: Sub-Saharan Africa & MENA
================================================================
A production-grade, reusable extraction and synthesis pipeline for mapping
the educational technology landscape across all 48 Sub-Saharan African (SSA)
and 21 Middle East & North Africa (MENA) nations (69 countries total).

Key Features:
  - Deterministic on-disk caching (SHA-256): Zero redundant network requests.
  - Robust handling of multi-country and list-type API responses.
  - Uses modern, active World Bank WDI and Statistical Performance Indicators (SPI).
  - Pulls active World Bank financing for digital learning/ICT without type errors.
  - Produces both long-format timeseries and latest wide-format profile matrices.

Usage:
  python3 fetch_6pillars_pipeline.py --all
  python3 fetch_6pillars_pipeline.py --pillar 2 --region ssa
  python3 fetch_6pillars_pipeline.py --pillar 3 --region mena
  python3 fetch_6pillars_pipeline.py --all --refresh  # Force fresh download
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# -----------------------------------------------------------------------------
# Configuration: Target Geographies (69 Economies)
# -----------------------------------------------------------------------------

SSA_48 = [
    "AGO", "BEN", "BWA", "BFA", "BDI", "CPV", "CMR", "CAF", "TCD", "COM",
    "COD", "COG", "CIV", "GNQ", "ERI", "SWZ", "ETH", "GAB", "GMB", "GHA",
    "GIN", "GNB", "KEN", "LSO", "LBR", "MDG", "MWI", "MLI", "MRT", "MUS",
    "MOZ", "NAM", "NER", "NGA", "RWA", "STP", "SEN", "SYC", "SLE", "SOM",
    "ZAF", "SSD", "SDN", "TZA", "TGO", "UGA", "ZMB", "ZWE"
]

MENA_21 = [
    "DZA", "BHR", "DJI", "EGY", "IRN", "IRQ", "ISR", "JOR", "KWT", "LBN",
    "LBY", "MLT", "MAR", "OMN", "PSE", "QAT", "SAU", "SYR", "TUN", "ARE", "YEM"
]

COUNTRY_REGIONS = {iso: "SSA" for iso in SSA_48}
COUNTRY_REGIONS.update({iso: "MENA" for iso in MENA_21})

# -----------------------------------------------------------------------------
# UNESCO 6-Pillars Indicator Mapping (Updated with Active Modern Indicators)
# -----------------------------------------------------------------------------

PILLAR_INDICATORS = {
    1: {
        "name": "Coordination and Leadership",
        "indicators": {
            "SE.XPD.TOTL.GD.ZS": "Gov expenditure on education (% of GDP)",
            "SE.XPD.TOTL.GB.ZS": "Gov expenditure on education (% of total gov budget)",
            "IQ.SPI.OVRL": "Statistical performance & governance index (SPI 0-100)",
        }
    },
    2: {
        "name": "Connectivity and Infrastructure",
        "indicators": {
            "EG.ELC.ACCS.ZS": "Access to electricity (% of population)",
            "EG.ELC.ACCS.RU.ZS": "Access to electricity, rural (% of rural population)",
            "EG.ELC.ACCS.UR.ZS": "Access to electricity, urban (% of urban population)",
            "IT.NET.USER.ZS": "Individuals using the Internet (% of population)",
            "IT.CEL.SETS.P2": "Mobile cellular subscriptions (per 100 people)",
            "IT.NET.BBND.P2": "Fixed broadband subscriptions (per 100 people)",
        }
    },
    3: {
        "name": "Cost and Sustainability",
        "indicators": {
            "NY.GDP.PCAP.CD": "GDP per capita (current US$)",
            "NY.GDP.PCAP.PP.CD": "GDP per capita, PPP (current international $)",
            "SE.XPD.PRIM.PC.ZS": "Gov expenditure per primary student (% of GDP per capita)",
            "SE.XPD.SECO.PC.ZS": "Gov expenditure per secondary student (% of GDP per capita)",
        }
    },
    4: {
        "name": "Capacity and Culture",
        "indicators": {
            "SE.PRM.TCAQ.ZS": "Trained teachers in primary education (% of total)",
            "SE.SEC.TCAQ.ZS": "Trained teachers in secondary education (% of total)",
            "SE.PRM.ENRL.TC.ZS": "Pupil-teacher ratio, primary",
            "SE.SEC.ENRL.TC.ZS": "Pupil-teacher ratio, secondary",
            "SE.ADT.LITR.ZS": "Adult literacy rate (% 15+)",
        }
    },
    5: {
        "name": "Content and Solutions",
        "indicators": {
            "con30e.s": "Accessed online info to learn/educate (% internet users 15+)",
            "IT.NET.SECR.P6": "Secure Internet servers (per 1 million people) - Digital hosting & platforms",
            "TM.VAL.ICTG.ZS.UN": "ICT goods imports (% of total goods imports) - Tech hardware inflows",
        }
    },
    6: {
        "name": "Data and Evidence",
        "indicators": {
            "IQ.SPI.OVRL": "SPI: Overall statistical performance score (scale 0-100)",
            "IQ.SPI.PIL1": "SPI: Data use score (scale 0-100)",
            "IQ.SPI.PIL5": "SPI: Data infrastructure & standards score (scale 0-100)",
        }
    }
}

PROJECT_QUERIES = [
    "digital learning", "education technology", "e-learning",
    "distance education", "teacher ICT", "digital skills"
]

USER_AGENT = "EdTech-6Pillars-Research/1.0 (academic research; Master ICT4D UniTO)"

# -----------------------------------------------------------------------------
# Caching HTTP Client
# -----------------------------------------------------------------------------

class CachedClient:
    """HTTP client with SHA-256 caching and retry logic."""
    def __init__(self, cache_dir: Path, refresh: bool = False):
        self.cache_dir = cache_dir
        self.refresh = refresh
        self.session = requests.Session()
        retry = Retry(total=4, backoff_factor=1.2, status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.headers["User-Agent"] = USER_AGENT

    def get_json(self, url: str, params: Optional[Dict[str, Any]] = None, source: str = "general") -> Any:
        params = params or {}
        cache_key = hashlib.sha256(f"{url}?{sorted(params.items())}".encode("utf-8")).hexdigest()
        cache_path = self.cache_dir / "raw" / source / f"{cache_key}.json"

        if not self.refresh and cache_path.exists():
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass  # Corrupt cache; re-fetch

        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        manifest_path = self.cache_dir / "manifest.jsonl"
        with open(manifest_path, "a", encoding="utf-8") as f:
            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": source,
                "url": resp.url,
                "bytes": len(resp.content),
                "cache_file": str(cache_path.relative_to(self.cache_dir))
            }
            f.write(json.dumps(log_entry) + "\n")

        time.sleep(0.12)
        return data

# -----------------------------------------------------------------------------
# Data Extractors
# -----------------------------------------------------------------------------

def fetch_indicator_series(
    client: CachedClient,
    indicator_code: str,
    indicator_name: str,
    pillar_num: int,
    pillar_name: str,
    countries: List[str],
    start_year: int,
    end_year: int,
    chunk_size: int = 24
) -> List[Dict[str, Any]]:
    """Fetches full timeseries for an indicator across country chunks."""
    records = []
    wb_base = "https://api.worldbank.org/v2"

    for i in range(0, len(countries), chunk_size):
        chunk = countries[i:i + chunk_size]
        country_str = ";".join(chunk)
        page = 1
        
        while True:
            url = f"{wb_base}/country/{country_str}/indicator/{indicator_code}"
            params = {
                "format": "json",
                "date": f"{start_year}:{end_year}",
                "per_page": 1000,
                "page": page
            }
            try:
                data = client.get_json(url, params=params, source="worldbank")
            except Exception as e:
                print(f"    [WARN] Failed fetch for {indicator_code} (chunk {i//chunk_size}): {e}")
                break

            if not isinstance(data, list) or len(data) < 2 or not data[1]:
                break

            meta = data[0]
            entries = data[1]

            for row in entries:
                val = row.get("value")
                if val is not None:
                    iso = row.get("countryiso3code") or row["country"]["id"]
                    if not iso:
                        iso = row["country"]["id"]
                    records.append({
                        "iso3": iso,
                        "country": row["country"]["value"],
                        "region": COUNTRY_REGIONS.get(iso, "Other"),
                        "pillar_number": pillar_num,
                        "pillar_name": pillar_name,
                        "indicator_code": indicator_code,
                        "indicator_name": indicator_name,
                        "year": int(row["date"]),
                        "value": float(val),
                        "source": "World Bank / UNESCO-UIS Mirror"
                    })

            total_pages = int(meta.get("pages", 1) or 1)
            if page >= total_pages:
                break
            page += 1

    return records


def fetch_world_bank_projects(
    client: CachedClient,
    target_countries: List[str],
    max_records: int = 200
) -> pd.DataFrame:
    """Pulls digital education, distance learning, and ICT projects safely handling list fields."""
    print("  Querying World Bank Projects API for Digital Education Financing...")
    wb_projects_url = "https://search.worldbank.org/api/v2/projects"
    seen_ids = set()
    project_rows = []

    target_set = set(target_countries)

    for q in PROJECT_QUERIES:
        params = {
            "format": "json",
            "qterm": q,
            "rows": 100,
            "os": 0
        }
        try:
            data = client.get_json(wb_projects_url, params=params, source="wb_projects")
            projects = data.get("projects", {})
            for pid, p in projects.items():
                if pid in seen_ids:
                    continue
                seen_ids.add(pid)

                # Safely normalize country code (may be list, str, or None)
                ccode_raw = p.get("countrycode")
                if isinstance(ccode_raw, list):
                    ccodes = [str(c).upper() for c in ccode_raw if c]
                elif isinstance(ccode_raw, str):
                    ccodes = [ccode_raw.upper()]
                else:
                    ccodes = []

                # Safely normalize country name
                cname = p.get("countryshortname")
                if isinstance(cname, list):
                    cname = ", ".join(str(c) for c in cname)
                elif not isinstance(cname, str):
                    cname = str(cname or "")

                # Safely normalize region
                region_raw = p.get("regionname", "")
                if isinstance(region_raw, list):
                    region_str = ", ".join(str(r) for r in region_raw)
                else:
                    region_str = str(region_raw or "")

                # Check match against target countries or regional tags
                is_target = any(c in target_set for c in ccodes) or any(
                    r in region_str for r in [
                        "Africa", "Middle East", "Eastern and Southern Africa",
                        "Western and Central Africa"
                    ]
                )

                if is_target:
                    comm_amt = p.get("totalcommamt") or p.get("totalamt") or 0
                    try:
                        comm_amt = float(str(comm_amt).replace(",", ""))
                    except ValueError:
                        comm_amt = 0.0

                    sector_obj = p.get("sector1")
                    sector_name = sector_obj.get("Name") if isinstance(sector_obj, dict) else str(sector_obj or "")

                    project_rows.append({
                        "project_id": pid,
                        "project_name": p.get("project_name"),
                        "country": cname,
                        "country_code": ccodes[0] if ccodes else "",
                        "region": region_str,
                        "status": p.get("projectstatusdisplay") or p.get("status"),
                        "approval_date": p.get("boardapprovaldate"),
                        "closing_date": p.get("closingdate"),
                        "commitment_usd": comm_amt,
                        "sector": sector_name,
                        "matched_query": q,
                        "url": p.get("url")
                    })
        except Exception as e:
            print(f"    [WARN] Failed projects query '{q}': {e}")

    df_projects = pd.DataFrame(project_rows)
    return df_projects

# -----------------------------------------------------------------------------
# Aggregators and Synthesis
# -----------------------------------------------------------------------------

def build_latest_wide_profile(df_long: pd.DataFrame) -> pd.DataFrame:
    """Takes the timeseries long table and builds a wide matrix of latest available data."""
    if df_long.empty:
        return pd.DataFrame()

    latest = df_long.sort_values("year").groupby(["iso3", "indicator_code"]).last().reset_index()

    wide_vals = latest.pivot(index="iso3", columns="indicator_code", values="value")
    wide_years = latest.pivot(index="iso3", columns="indicator_code", values="year").add_suffix("_year")

    meta = latest[["iso3", "country", "region"]].drop_duplicates("iso3").set_index("iso3")

    combined = meta.join(wide_vals).join(wide_years).reset_index()
    return combined


def build_regional_summary(df_wide: pd.DataFrame, df_long: pd.DataFrame) -> pd.DataFrame:
    """Calculates SSA vs. MENA comparison statistics and data coverage rates."""
    if df_wide.empty:
        return pd.DataFrame()

    summary_rows = []
    val_cols = [c for c in df_wide.columns if c not in ["iso3", "country", "region"] and not c.endswith("_year")]

    for col in val_cols:
        matching_meta = df_long[df_long["indicator_code"] == col]
        ind_desc = matching_meta["indicator_name"].iloc[0] if not matching_meta.empty else col

        for reg in ["SSA", "MENA"]:
            sub = df_wide[df_wide["region"] == reg][col].dropna()
            total_countries = 48 if reg == "SSA" else 21
            reporting_count = len(sub)
            coverage_pct = round((reporting_count / total_countries) * 100, 1)

            summary_rows.append({
                "region": reg,
                "indicator_code": col,
                "indicator_name": ind_desc,
                "reporting_countries": reporting_count,
                "total_countries": total_countries,
                "coverage_pct": coverage_pct,
                "mean": round(sub.mean(), 2) if not sub.empty else None,
                "median": round(sub.median(), 2) if not sub.empty else None,
                "min": round(sub.min(), 2) if not sub.empty else None,
                "max": round(sub.max(), 2) if not sub.empty else None,
            })

    return pd.DataFrame(summary_rows)

# -----------------------------------------------------------------------------
# Main Execution Pipeline
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="UNESCO 6-Pillars EdTech Data Pipeline for SSA & MENA",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--pillar", type=int, choices=[1, 2, 3, 4, 5, 6], help="Extract a single specific pillar")
    parser.add_argument("--all", action="store_true", help="Extract all 6 pillars and projects data")
    parser.add_argument("--region", choices=["all", "ssa", "mena"], default="all", help="Target regional scope")
    parser.add_argument("--refresh", action="store_true", help="Bypass cache and force fresh downloads")
    parser.add_argument("--start-year", type=int, default=2015, help="Start year for timeseries (default: 2015)")
    parser.add_argument("--end-year", type=int, default=2024, help="End year for timeseries (default: 2024)")
    parser.add_argument("--out-dir", default="data", help="Output directory path (default: 'data')")

    args = parser.parse_args()

    if not args.all and args.pillar is None:
        print("\n[!] Please specify either --all or --pillar [1-6]. Use --help for full options.\n")
        sys.exit(1)

    out_dir = Path(args.out_dir)
    raw_dir = out_dir / "raw"
    proc_dir = out_dir / "processed"
    proc_dir.mkdir(parents=True, exist_ok=True)

    client = CachedClient(cache_dir=out_dir, refresh=args.refresh)

    if args.region == "ssa":
        countries = SSA_48
    elif args.region == "mena":
        countries = MENA_21
    else:
        countries = SSA_48 + MENA_21

    print("=" * 75)
    print(" UNESCO 6-PILLARS EDTECH PIPELINE: SUB-SAHARAN AFRICA & MENA")
    print(f" Scope: {len(countries)} Countries | Years: {args.start_year}-{args.end_year} | Cache: {raw_dir}")
    print("=" * 75)

    pillars_to_run = [args.pillar] if args.pillar else [1, 2, 3, 4, 5, 6]
    all_series_records = []

    for p_num in pillars_to_run:
        p_cfg = PILLAR_INDICATORS[p_num]
        p_name = p_cfg["name"]
        print(f"\n[Pillar {p_num}: {p_name}]")

        for ind_code, ind_desc in p_cfg["indicators"].items():
            print(f"  Fetching: {ind_code} -> {ind_desc[:45]}...")
            records = fetch_indicator_series(
                client=client,
                indicator_code=ind_code,
                indicator_name=ind_desc,
                pillar_num=p_num,
                pillar_name=p_name,
                countries=countries,
                start_year=args.start_year,
                end_year=args.end_year
            )
            print(f"    -> {len(records)} data points retrieved.")
            all_series_records.extend(records)

    df_long = pd.DataFrame(all_series_records)
    if not df_long.empty:
        timeseries_file = proc_dir / "indicators_timeseries.csv"
        df_long.to_csv(timeseries_file, index=False)
        print(f"\n[✓] Saved Long Timeseries: {timeseries_file} ({len(df_long)} rows)")

        df_wide = build_latest_wide_profile(df_long)
        wide_file = proc_dir / "latest_country_profiles_6pillars.csv"
        df_wide.to_csv(wide_file, index=False)
        print(f"[✓] Saved Latest Wide Profile: {wide_file} ({len(df_wide)} countries)")

        df_summary = build_regional_summary(df_wide, df_long)
        summary_file = proc_dir / "pillar_regional_benchmarks.csv"
        df_summary.to_csv(summary_file, index=False)
        print(f"[✓] Saved Regional Benchmarks (SSA vs MENA): {summary_file}")
    else:
        print("\n[!] No indicator data was retrieved.")

    if args.all or args.pillar == 3:
        print("\n[Pillar 3 Project Financing]")
        df_projects = fetch_world_bank_projects(client, countries)
        if not df_projects.empty:
            proj_file = proc_dir / "wb_digital_education_projects.csv"
            df_projects.to_csv(proj_file, index=False)
            print(f"[✓] Saved World Bank Projects: {proj_file} ({len(df_projects)} projects)")

    print("\n" + "=" * 75)
    print(" Pipeline execution complete! All tidy data stored in data/processed/")
    print("=" * 75)


if __name__ == "__main__":
    main()
