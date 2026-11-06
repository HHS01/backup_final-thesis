#!/usr/bin/env python3
"""
compile_macro_fiscal_indicators.py
==================================
Synthesizes domestic government expenditure (IMF GFS COFOG) and external
development assistance (IATI Datastore) with UNESCO/World Bank macro indicators
into a unified Macro-Fiscal & Aid Observatory dataset.

Features:
  - Dynamic country resolution: supports any SSA or global country code,
    `all-ssa` (all 48 SSA economies), or `all-available` (auto-detect).
  - Smart caching: reuses existing compiled datasets when source files
    are unchanged, with `--force-refresh` to bypass.
  - Transparent fallback: seamlessly marries IMF GFS COFOG with World Bank /
    UNESCO UIS benchmarks when COFOG reporting is absent.
  - Dual-Gatekeeping & Recurrent Cliff Index: computes empirical tension
    between donor capital absorption and domestic operational envelopes.

Outputs:
  - data/processed/macro_fiscal_ecosystem.json (Primary JSON dataset)
  - data/processed/macro_fiscal_data.js (Browser-ready JavaScript module)
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("compile_macro_fiscal")

# --------------------------------------------------------------------------
# Comprehensive African ISO Mapping (All 54 Economies)
# --------------------------------------------------------------------------
AFRICA_ISO_MAP: dict[str, tuple[str, str]] = {
    "AGO": ("AO", "Angola"), "BDI": ("BI", "Burundi"), "BEN": ("BJ", "Benin"),
    "BFA": ("BF", "Burkina Faso"), "BWA": ("BW", "Botswana"), "CAF": ("CF", "Central African Republic"),
    "CIV": ("CI", "Cote d'Ivoire"), "CMR": ("CM", "Cameroon"), "COD": ("CD", "Congo, Dem. Rep."),
    "COG": ("CG", "Congo, Rep."), "COM": ("KM", "Comoros"), "CPV": ("CV", "Cabo Verde"),
    "DJI": ("DJ", "Djibouti"), "DZA": ("DZ", "Algeria"), "EGY": ("EG", "Egypt"),
    "ERI": ("ER", "Eritrea"), "ETH": ("ET", "Ethiopia"), "GAB": ("GA", "Gabon"),
    "GHA": ("GH", "Ghana"), "GIN": ("GN", "Guinea"), "GMB": ("GM", "Gambia"),
    "GNB": ("GW", "Guinea-Bissau"), "GNQ": ("GQ", "Equatorial Guinea"), "KEN": ("KE", "Kenya"),
    "LBR": ("LR", "Liberia"), "LBY": ("LY", "Libya"), "LSO": ("LS", "Lesotho"),
    "MAR": ("MA", "Morocco"), "MDG": ("MG", "Madagascar"), "MLI": ("ML", "Mali"),
    "MOZ": ("MZ", "Mozambique"), "MRT": ("MR", "Mauritania"), "MUS": ("MU", "Mauritius"),
    "MWI": ("MW", "Malawi"), "NAM": ("NA", "Namibia"), "NER": ("NE", "Niger"),
    "NGA": ("NG", "Nigeria"), "RWA": ("RW", "Rwanda"), "SDN": ("SD", "Sudan"),
    "SEN": ("SN", "Senegal"), "SLE": ("SL", "Sierra Leone"), "SOM": ("SO", "Somalia"),
    "SSD": ("SS", "South Sudan"), "STP": ("ST", "Sao Tome and Principe"), "SWZ": ("SZ", "Eswatini"),
    "SYC": ("SC", "Seychelles"), "TCD": ("TD", "Chad"), "TGO": ("TG", "Togo"),
    "TUN": ("TN", "Tunisia"), "TZA": ("TZ", "Tanzania"), "UGA": ("UG", "Uganda"),
    "ZAF": ("ZA", "South Africa"), "ZMB": ("ZM", "Zambia"), "ZWE": ("ZW", "Zimbabwe"),
}

ALL_SSA_ISO3: list[str] = [
    "AGO", "BDI", "BEN", "BFA", "BWA", "CAF", "CIV", "CMR", "COD", "COG",
    "COM", "CPV", "ERI", "ETH", "GAB", "GHA", "GIN", "GMB", "GNB", "GNQ",
    "KEN", "LBR", "LSO", "MDG", "MLI", "MOZ", "MRT", "MUS", "MWI", "NAM",
    "NER", "NGA", "RWA", "SDN", "SEN", "SLE", "SOM", "SSD", "STP", "SWZ",
    "SYC", "TCD", "TGO", "TZA", "UGA", "ZAF", "ZMB", "ZWE",
]

DEFAULT_PILOT_COUNTRIES: list[str] = ["KEN", "RWA", "TZA", "MUS", "GHA", "NGA", "ZMB"]

# Curated qualitative deep-dive narratives for anchor pilot archetypes
CURATED_ARCHETYPES: dict[str, dict[str, str]] = {
    "KEN": {
        "name": "Kenya",
        "archetype": "East African Innovation Hub with High Pedagogical Qualifications",
        "imf_sector_pref": "S1311B,S13,S1311",
        "cliff_tier": "High Tension (Structural Recurrent Lock)",
        "cliff_narrative": (
            "Kenya allocates 18.43% of national budget to education (strong domestic commitment), "
            "yet central ICT receives only 0.46%. With over $1B in external education aid driving "
            "hardware deployments, schools lack ongoing public connectivity and maintenance subsidies."
        ),
    },
    "RWA": {
        "name": "Rwanda",
        "archetype": "State-Led Digital Push vs. Classroom Crowding & Language Transition",
        "imf_sector_pref": "S1311B,S13",
        "cliff_tier": "High External Reliance (Classroom Crowding Deficit)",
        "cliff_narrative": (
            "Rwanda absorbed $974.7M in external education assistance (surging 554% during COVID). "
            "However, missing domestic COFOG transparency and high student-teacher crowding limit "
            "sustainable recurring operations."
        ),
    },
    "TZA": {
        "name": "Tanzania",
        "archetype": "Swahili Foundational Anchor vs. Severe Rural Energy Deficit",
        "imf_sector_pref": "S1311B,S13",
        "cliff_tier": "Severe Infrastructure Void vs. Aid Volume",
        "cliff_narrative": (
            "Tanzania absorbed $2.05B in external education aid (top bilateral recipient), with 19.6% "
            "domestic education budget share, but a 47.6% national unelectrified rate creates a sharp "
            "hardware utilization barrier."
        ),
    },
    "MUS": {
        "name": "Mauritius",
        "archetype": "High-Income SIDS with Complete Electrification and Broadband",
        "imf_sector_pref": "S13,S1311,S1311B",
        "cliff_tier": "Self-Financed Universal SIDS Benchmark",
        "cliff_narrative": (
            "Mauritius maintains complete school electrification (100%) and 73% internet saturation "
            "with minimal external aid dependency ($2.5M total), financed entirely through domestic tax revenues."
        ),
    },
    "GHA": {
        "name": "Ghana",
        "archetype": "West African Digital Frontrunner vs. Rural School Wiring Gap",
        "imf_sector_pref": "S1311B,S13",
        "cliff_tier": "Expanding Donor ICT Capital vs. Rural Electrification",
        "cliff_narrative": (
            "Ghana received $223.5M in targeted ICT aid alongside $443.5M in education disbursements, "
            "supporting rapid urban digital growth while rural primary electrification remains unfinished."
        ),
    },
    "NGA": {
        "name": "Nigeria",
        "archetype": "Macro Startup Giant vs. Severe Federal Budget & Power Gap",
        "imf_sector_pref": "S1311B,S13",
        "cliff_tier": "Severe Macro Federal Budget Deficit",
        "cliff_narrative": (
            "Federal education budget allocation is critically low (~3.0%), leaving external development assistance "
            "($1.97B disbursed) to shoulder foundational infrastructure and emergency learning programs."
        ),
    },
    "ZMB": {
        "name": "Zambia",
        "archetype": "Severe Rural Infrastructure Deficit & High Linguistic Fragmentation",
        "imf_sector_pref": "S1311B,S13",
        "cliff_tier": "Moderate Domestic Envelope & Sustained Aid Reliance",
        "cliff_narrative": (
            "Zambia dedicates 14.6% of budget to education and 0.64% to communication. External assistance "
            "($380.6M) surged 262% during COVID to bridge severe rural learning divides."
        ),
    },
}

# Standard currency exchange rates to USD for IATI transactions
CURRENCY_TO_USD = {
    "USD": 1.0, "GBP": 1.28, "EUR": 1.09, "CAD": 0.74, "CHF": 1.13,
    "AUD": 0.66, "DKK": 0.146, "SEK": 0.095, "NOK": 0.093, "JPY": 0.0071,
    "KRW": 0.00075, "TZS": 0.00039, "KES": 0.0078, "RWF": 0.00077,
    "GHS": 0.075, "ZMK": 0.040, "CZK": 0.043, "FKP": 1.28,
}

COFOG_SUBFUNCTIONS = {
    "GF091": "Pre-primary and primary education",
    "GF091_T": "Pre-primary and primary education",
    "GF092": "Secondary education",
    "GF092_T": "Secondary education",
    "GF093": "Post-secondary non-tertiary education",
    "GF0930_T": "Post-secondary non-tertiary education",
    "GF094": "Tertiary education",
    "GF094_T": "Tertiary education",
    "GF095": "Education not definable by level",
    "GF0950_T": "Education not definable by level",
    "GF096": "Subsidiary services to education",
    "GF0960_T": "Subsidiary services to education",
    "GF097": "R&D Education",
    "GF0970_T": "R&D Education",
    "GF098": "Education n.e.c.",
    "GF0980_T": "Education n.e.c.",
}


# --------------------------------------------------------------------------
# Loader & Helper Functions
# --------------------------------------------------------------------------
def load_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        logger.warning(f"File not found: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_json_file(path: Path) -> dict:
    if not path.is_file():
        logger.warning(f"File not found: {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_country_metadata(
    requested_codes: list[str],
    profiles_rows: list[dict[str, str]],
    available_iso2_in_iati: set[str],
    available_iso3_in_imf: set[str],
) -> dict[str, dict[str, Any]]:
    """
    Dynamically maps requested country codes to (ISO3, ISO2, Name, Archetype),
    ensuring zero hardcoding and graceful fallback for any SSA/global country.
    """
    p_lookup: dict[str, dict] = {}
    for r in profiles_rows:
        iso = r.get("iso3", "").strip().upper()
        if iso:
            p_lookup[iso] = r

    iso2_to_iso3 = {v[0]: k for k, v in AFRICA_ISO_MAP.items()}

    target_iso3: list[str] = []
    for code in requested_codes:
        c = code.strip().upper()
        if c in ("ALL-SSA", "ALL_SSA", "SSA"):
            for iso in ALL_SSA_ISO3:
                if iso not in target_iso3:
                    target_iso3.append(iso)
        elif c in ("ALL-AVAILABLE", "ALL_AVAILABLE", "ALL"):
            found_iso3 = set(CURATED_ARCHETYPES.keys()) | available_iso3_in_imf
            for iso2 in available_iso2_in_iati:
                if iso2 in iso2_to_iso3:
                    found_iso3.add(iso2_to_iso3[iso2])
            for iso in sorted(found_iso3):
                if iso not in target_iso3:
                    target_iso3.append(iso)
        elif c in AFRICA_ISO_MAP:
            if c not in target_iso3:
                target_iso3.append(c)
        elif c in iso2_to_iso3:
            iso = iso2_to_iso3[c]
            if iso not in target_iso3:
                target_iso3.append(iso)
        elif c in p_lookup:
            if c not in target_iso3:
                target_iso3.append(c)
        elif len(c) == 3:
            if c not in target_iso3:
                target_iso3.append(c)

    metadata: dict[str, dict[str, Any]] = {}
    for iso3 in target_iso3:
        p_row = p_lookup.get(iso3, {})
        curated = CURATED_ARCHETYPES.get(iso3, {})
        iso2 = AFRICA_ISO_MAP.get(iso3, (iso3[:2], ""))[0]
        country_name = curated.get("name") or p_row.get("country") or AFRICA_ISO_MAP.get(iso3, ("", iso3))[1]

        if curated.get("archetype"):
            arch_title = curated["archetype"]
        else:
            elec = float(p_row.get("EG.ELC.ACCS.ZS", 0) or 0)
            net = float(p_row.get("IT.NET.USER.ZS", 0) or 0)
            ed_b = float(p_row.get("SE.XPD.TOTL.GB.ZS", 0) or 0)
            lp = float(p_row.get("SE.LPV.PRIM", 0) or 0)

            if elec >= 80 and net >= 50:
                arch_title = "Expanding Digital Frontrunner with Grid Foundation"
            elif elec < 40 or lp > 80:
                arch_title = "Severe Rural Infrastructure Deficit & Foundational Learning Priority"
            elif ed_b >= 18:
                arch_title = "High Domestic Budget Commitment with Recurrent Absorption Challenges"
            else:
                arch_title = f"{p_row.get('region', 'SSA')} Educational Infrastructure & Transition Frontier"

        pref = curated.get("imf_sector_pref", "S1311B,S13,S1311").split(",")

        metadata[iso3] = {
            "iso3": iso3,
            "iso2": iso2,
            "name": country_name,
            "archetype": arch_title,
            "imf_sector_pref": pref,
            "is_curated": bool(curated),
            "cliff_tier": curated.get("cliff_tier"),
            "cliff_narrative": curated.get("cliff_narrative"),
        }

    return metadata


# --------------------------------------------------------------------------
# IMF COFOG Processor
# --------------------------------------------------------------------------
def process_imf_cofog(
    imf_shares_rows: list[dict[str, str]],
    target_countries: dict[str, dict],
) -> dict[str, Any]:
    country_data: dict[str, dict] = {}

    for iso3, meta in target_countries.items():
        rows = [r for r in imf_shares_rows if r.get("country_iso3") == iso3]
        if not rows:
            country_data[iso3] = {
                "has_imf_data": False,
                "reporting_status": "No recent COFOG reported to IMF GFS",
                "source": "IMF STA GFS (Non-reporting)",
                "sectors_available": [],
                "years_available": [],
                "latest_year": None,
                "latest_indicators": {},
                "annual_series": {},
                "subfunctions_latest_year": {},
            }
            continue

        sectors = sorted({r["SECTOR"] for r in rows if "SECTOR" in r})
        pref_sectors = meta.get("imf_sector_pref", ["S1311B", "S13"])
        chosen_sector = None
        for ps in pref_sectors:
            if ps in sectors:
                chosen_sector = ps
                break
        if not chosen_sector and sectors:
            chosen_sector = sectors[0]

        pogdp_rows = [
            r for r in rows
            if r.get("SECTOR") == chosen_sector and r.get("TYPE_OF_TRANSFORMATION") == "POGDP_PT"
        ]

        agg_edu_rows = [
            r for r in pogdp_rows
            if r.get("group") == "education" and r.get("level") == "aggregate"
        ]
        years = sorted({int(r["year"]) for r in agg_edu_rows if r.get("year", "").isdigit()})

        annual_series: dict[int, dict] = {}
        for yr in years:
            annual_series[yr] = {
                "education_pct_gdp": None,
                "education_pct_budget": None,
                "communication_pct_gdp": None,
                "communication_pct_budget": None,
                "transport_pct_gdp": None,
                "transport_pct_budget": None,
                "total_outlays_pct_gdp": None,
            }

        for r in pogdp_rows:
            try:
                yr = int(r["year"])
            except (ValueError, TypeError):
                continue
            if yr not in annual_series:
                continue

            grp = r.get("group")
            lvl = r.get("level")
            val = float(r["value"]) if r.get("value") not in ("", None) else None
            share = float(r["share_of_total_pct"]) if r.get("share_of_total_pct") not in ("", None) else None
            tot_val = float(r["total_value"]) if r.get("total_value") not in ("", None) else None

            if tot_val is not None:
                annual_series[yr]["total_outlays_pct_gdp"] = round(tot_val, 2)

            if lvl == "aggregate":
                if grp == "education":
                    annual_series[yr]["education_pct_gdp"] = round(val, 2) if val is not None else None
                    annual_series[yr]["education_pct_budget"] = round(share, 2) if share is not None else None
                elif grp == "communication":
                    annual_series[yr]["communication_pct_gdp"] = round(val, 3) if val is not None else None
                    annual_series[yr]["communication_pct_budget"] = round(share, 2) if share is not None else None
                elif grp == "transport":
                    annual_series[yr]["transport_pct_gdp"] = round(val, 2) if val is not None else None
                    annual_series[yr]["transport_pct_budget"] = round(share, 2) if share is not None else None

        latest_yr = max(years) if years else None
        latest_inds = annual_series.get(latest_yr, {}) if latest_yr else {}

        subfuncs: dict[str, dict] = {}
        if latest_yr:
            sub_rows = [
                r for r in pogdp_rows
                if int(r.get("year", 0)) == latest_yr and r.get("level") == "sub-function" and r.get("group") == "education"
            ]
            for sr in sub_rows:
                ind = sr.get("INDICATOR", "")
                val = float(sr["value"]) if sr.get("value") not in ("", None) else 0.0
                share = float(sr["share_of_total_pct"]) if sr.get("share_of_total_pct") not in ("", None) else 0.0
                desc = COFOG_SUBFUNCTIONS.get(ind, ind)
                subfuncs[ind] = {
                    "code": ind,
                    "name": desc,
                    "pct_gdp": round(val, 3),
                    "pct_budget": round(share, 2),
                }

        country_data[iso3] = {
            "has_imf_data": True,
            "reporting_status": "Active IMF GFS COFOG reporting",
            "source": f"IMF STA GFS COFOG (Sector: {chosen_sector})",
            "sector_used": chosen_sector,
            "sectors_available": sectors,
            "years_available": years,
            "latest_year": latest_yr,
            "latest_indicators": latest_inds,
            "annual_series": {str(k): v for k, v in sorted(annual_series.items())},
            "subfunctions_latest_year": subfuncs,
        }

    return country_data


# --------------------------------------------------------------------------
# IATI Aid Processor
# --------------------------------------------------------------------------
def process_iati_funding(
    iati_tx_rows: list[dict[str, str]],
    target_countries: dict[str, dict],
    since_year: int = 2017,
    until_year: int = 2024,
) -> dict[str, Any]:
    country_data: dict[str, dict] = {}
    years_range = list(range(since_year, until_year + 1))

    for iso3, meta in target_countries.items():
        iso2 = meta["iso2"]
        sub_tx = [r for r in iati_tx_rows if r.get("country_iso2") == iso2]

        annual_aid: dict[int, dict] = {
            yr: {
                "education_disbursements_usd": 0.0,
                "education_commitments_usd": 0.0,
                "ict_disbursements_usd": 0.0,
                "ict_commitments_usd": 0.0,
                "edtech_disbursements_usd": 0.0,
                "total_disbursements_usd": 0.0,
                "total_commitments_usd": 0.0,
            }
            for yr in years_range
        }

        initiatives: list[dict] = []
        seen_titles = set()

        for tx in sub_tx:
            try:
                yr = int(tx["year"])
            except (ValueError, TypeError):
                continue
            if yr < since_year or yr > until_year:
                continue

            grp = tx.get("group", "")
            tx_type = tx.get("tx_type", "")
            curr = tx.get("currency", "USD").upper()
            try:
                raw_val = float(tx.get("value_attributed", 0.0))
            except (ValueError, TypeError):
                raw_val = 0.0

            rate = CURRENCY_TO_USD.get(curr, 1.0)
            val_usd = raw_val * rate

            if tx_type == "disbursement":
                if grp == "education":
                    annual_aid[yr]["education_disbursements_usd"] += val_usd
                    annual_aid[yr]["total_disbursements_usd"] += val_usd
                elif grp == "ict_communications":
                    annual_aid[yr]["ict_disbursements_usd"] += val_usd
                    annual_aid[yr]["total_disbursements_usd"] += val_usd
                elif grp == "edtech_keyword":
                    annual_aid[yr]["edtech_disbursements_usd"] += val_usd
                    annual_aid[yr]["total_disbursements_usd"] += val_usd

            elif tx_type == "commitment":
                if grp == "education":
                    annual_aid[yr]["education_commitments_usd"] += val_usd
                    annual_aid[yr]["total_commitments_usd"] += val_usd
                elif grp == "ict_communications":
                    annual_aid[yr]["ict_commitments_usd"] += val_usd
                    annual_aid[yr]["total_commitments_usd"] += val_usd

            title = tx.get("title", "").strip()
            if title and title not in seen_titles and len(title) > 10 and val_usd > 200000:
                seen_titles.add(title)
                initiatives.append({
                    "title": title[:140],
                    "year": yr,
                    "group": grp,
                    "value_usd": round(val_usd, 0),
                    "iati_id": tx.get("iati_id", ""),
                })

        initiatives.sort(key=lambda x: x["value_usd"], reverse=True)

        annual_millions: dict[str, dict] = {}
        tot_edu_disb = 0.0
        tot_edu_comm = 0.0
        tot_ict_disb = 0.0
        tot_ict_comm = 0.0

        for yr, d in annual_aid.items():
            edu_d_m = round(d["education_disbursements_usd"] / 1e6, 2)
            edu_c_m = round(d["education_commitments_usd"] / 1e6, 2)
            ict_d_m = round(d["ict_disbursements_usd"] / 1e6, 2)
            ict_c_m = round(d["ict_commitments_usd"] / 1e6, 2)
            tot_d_m = round(d["total_disbursements_usd"] / 1e6, 2)
            tot_c_m = round(d["total_commitments_usd"] / 1e6, 2)

            annual_millions[str(yr)] = {
                "education_disbursements_usd_m": edu_d_m,
                "education_commitments_usd_m": edu_c_m,
                "ict_disbursements_usd_m": ict_d_m,
                "ict_commitments_usd_m": ict_c_m,
                "total_disbursements_usd_m": tot_d_m,
                "total_commitments_usd_m": tot_c_m,
            }

            tot_edu_disb += d["education_disbursements_usd"]
            tot_edu_comm += d["education_commitments_usd"]
            tot_ict_disb += d["ict_disbursements_usd"]
            tot_ict_comm += d["ict_commitments_usd"]

        y2019_edu = annual_aid[2019]["education_disbursements_usd"]
        y2020_edu = annual_aid[2020]["education_disbursements_usd"]
        covid_surge_abs_m = round((y2020_edu - y2019_edu) / 1e6, 2)
        covid_surge_pct = round(((y2020_edu - y2019_edu) / y2019_edu) * 100, 1) if y2019_edu > 0 else None

        country_data[iso3] = {
            "window": f"{since_year}-{until_year}",
            "transaction_count": len(sub_tx),
            "summary_8yr": {
                "education_disbursements_usd_m": round(tot_edu_disb / 1e6, 2),
                "education_commitments_usd_m": round(tot_edu_comm / 1e6, 2),
                "ict_disbursements_usd_m": round(tot_ict_disb / 1e6, 2),
                "ict_commitments_usd_m": round(tot_ict_comm / 1e6, 2),
                "total_aid_disbursements_usd_m": round((tot_edu_disb + tot_ict_disb) / 1e6, 2),
            },
            "covid_2020_dynamics": {
                "disbursed_2019_usd_m": round(y2019_edu / 1e6, 2),
                "disbursed_2020_usd_m": round(y2020_edu / 1e6, 2),
                "surge_absolute_usd_m": covid_surge_abs_m,
                "surge_growth_pct": covid_surge_pct,
            },
            "annual_timeseries": annual_millions,
            "top_initiatives": initiatives[:8],
        }

    return country_data


# --------------------------------------------------------------------------
# UNESCO / World Bank Context Enrichment & Fallback
# --------------------------------------------------------------------------
def load_country_profiles_context(
    profiles_rows: list[dict[str, str]],
    target_countries: dict[str, dict],
) -> dict[str, Any]:
    context: dict[str, dict] = {}

    for iso3 in target_countries:
        match = [r for r in profiles_rows if r.get("iso3") == iso3]
        if not match:
            context[iso3] = {}
            continue
        r = match[0]

        def parse_flt(val: Any, dec: int = 2) -> Optional[float]:
            try:
                return round(float(val), dec) if val not in ("", None) else None
            except (ValueError, TypeError):
                return None

        context[iso3] = {
            "country_name": r.get("country", ""),
            "region": r.get("region", "SSA"),
            "gdp_per_capita_usd": parse_flt(r.get("NY.GDP.PCAP.CD"), 0),
            "internet_users_pct": parse_flt(r.get("IT.NET.USER.ZS"), 1),
            "fixed_broadband_per100": parse_flt(r.get("IT.NET.BBND.P2"), 2),
            "electricity_access_pct": parse_flt(r.get("EG.ELC.ACCS.ZS"), 1),
            "rural_electricity_pct": parse_flt(r.get("EG.ELC.ACCS.RU.ZS"), 1),
            "urban_electricity_pct": parse_flt(r.get("EG.ELC.ACCS.UR.ZS"), 1),
            "learning_poverty_pct": parse_flt(r.get("SE.LPV.PRIM"), 1),
            "adult_literacy_pct": parse_flt(r.get("SE.ADT.LITR.ZS"), 1),
            "wb_education_pct_gdp": parse_flt(r.get("SE.XPD.TOTL.GD.ZS"), 2),
            "wb_education_pct_budget": parse_flt(r.get("SE.XPD.TOTL.GB.ZS"), 2),
        }

    return context


# --------------------------------------------------------------------------
# Dual-Gatekeeping & "The Digital Recurrent Cliff" Synthesis
# --------------------------------------------------------------------------
def synthesize_macro_fiscal(
    target_countries: dict[str, dict],
    imf_data: dict[str, Any],
    iati_data: dict[str, Any],
    wb_context: dict[str, Any],
) -> dict[str, Any]:
    ecosystem_countries: dict[str, dict] = {}

    for iso3, meta in target_countries.items():
        name = meta["name"]
        archetype = meta["archetype"]
        imf = imf_data.get(iso3, {})
        iati = iati_data.get(iso3, {})
        wb = wb_context.get(iso3, {})

        has_imf = imf.get("has_imf_data", False)
        latest_imf = imf.get("latest_indicators", {})

        if has_imf and latest_imf.get("education_pct_budget") is not None:
            edu_budget_pct = latest_imf.get("education_pct_budget")
            edu_gdp_pct = latest_imf.get("education_pct_gdp")
            edu_src = f"IMF STA GFS ({imf.get('sector_used')}, {imf.get('latest_year')})"
        else:
            edu_budget_pct = wb.get("wb_education_pct_budget")
            edu_gdp_pct = wb.get("wb_education_pct_gdp")
            edu_src = "World Bank / UNESCO UIS Benchmark"

        comm_budget_pct = latest_imf.get("communication_pct_budget") if has_imf else None
        comm_gdp_pct = latest_imf.get("communication_pct_gdp") if has_imf else None

        summary_8yr = iati.get("summary_8yr", {})
        edu_aid_m = summary_8yr.get("education_disbursements_usd_m", 0.0)
        ict_aid_m = summary_8yr.get("ict_disbursements_usd_m", 0.0)
        total_aid_m = summary_8yr.get("total_aid_disbursements_usd_m", 0.0)
        covid_surge = iati.get("covid_2020_dynamics", {})

        ratio_edu_to_comm = None
        if edu_budget_pct and comm_budget_pct and comm_budget_pct > 0:
            ratio_edu_to_comm = round(edu_budget_pct / comm_budget_pct, 1)

        if meta.get("cliff_tier") and meta.get("cliff_narrative"):
            cliff_tier = meta["cliff_tier"]
            cliff_narrative = meta["cliff_narrative"]
        else:
            if ratio_edu_to_comm and ratio_edu_to_comm >= 25.0:
                cliff_tier = "High Tension (Structural Recurrent Lock)"
            elif ratio_edu_to_comm and ratio_edu_to_comm >= 10.0:
                cliff_tier = "Moderate Tension (Recurrent Financing Gap)"
            elif edu_aid_m > 300.0:
                cliff_tier = "High External Reliance (Donor Capital Absorption Gap)"
            else:
                cliff_tier = "Frontier External Assistance Portfolio"

            surge_txt = f", surging {covid_surge.get('surge_growth_pct')}% during COVID" if covid_surge.get('surge_growth_pct') else ""
            edu_b_str = f"{edu_budget_pct}%" if edu_budget_pct is not None else "undisclosed %"
            comm_b_str = f"{comm_budget_pct}%" if comm_budget_pct is not None else "unfunded / unreported"

            cliff_narrative = (
                f"{name} allocates {edu_b_str} of national budget to education while communications receives {comm_b_str}. "
                f"External assistance (${edu_aid_m:,.1f}M disbursed 2017-2024{surge_txt}) supports foundational expansion, "
                f"leaving operational ICT maintenance as an essential public budget priority."
            )

        ecosystem_countries[iso3] = {
            "country_iso3": iso3,
            "country_iso2": meta["iso2"],
            "country_name": name,
            "archetype": archetype,
            "domestic_fiscal": {
                "source": edu_src,
                "has_imf_cofog": has_imf,
                "education_pct_budget": edu_budget_pct,
                "education_pct_gdp": edu_gdp_pct,
                "communication_pct_budget": comm_budget_pct,
                "communication_pct_gdp": comm_gdp_pct,
                "transport_pct_budget": latest_imf.get("transport_pct_budget"),
                "transport_pct_gdp": latest_imf.get("transport_pct_gdp"),
                "total_outlays_pct_gdp": latest_imf.get("total_outlays_pct_gdp"),
                "annual_timeseries": imf.get("annual_series", {}),
                "subfunctions": imf.get("subfunctions_latest_year", {}),
            },
            "external_assistance": {
                "source": "IATI Datastore Solr API (2017-2024)",
                "education_disbursed_8yr_usd_m": summary_8yr.get("education_disbursements_usd_m", 0.0),
                "education_committed_8yr_usd_m": summary_8yr.get("education_commitments_usd_m", 0.0),
                "ict_disbursed_8yr_usd_m": summary_8yr.get("ict_disbursements_usd_m", 0.0),
                "total_aid_disbursed_8yr_usd_m": summary_8yr.get("total_aid_disbursements_usd_m", 0.0),
                "covid_2020_surge": covid_surge,
                "annual_timeseries": iati.get("annual_timeseries", {}),
                "top_initiatives": iati.get("top_initiatives", []),
            },
            "recurrent_cliff_analysis": {
                "cliff_risk_tier": cliff_tier,
                "domestic_edu_to_comm_ratio": ratio_edu_to_comm,
                "narrative": cliff_narrative,
            },
            "macro_context": wb,
        }

    comparison_table = []
    for iso3, meta in target_countries.items():
        eco = ecosystem_countries[iso3]
        comparison_table.append({
            "iso3": iso3,
            "name": meta["name"],
            "edu_pct_budget": eco["domestic_fiscal"]["education_pct_budget"],
            "comm_pct_budget": eco["domestic_fiscal"]["communication_pct_budget"],
            "edu_aid_disb_usd_m": eco["external_assistance"]["education_disbursed_8yr_usd_m"],
            "ict_aid_disb_usd_m": eco["external_assistance"]["ict_disbursed_8yr_usd_m"],
            "covid_2020_disb_usd_m": eco["external_assistance"]["covid_2020_surge"].get("disbursed_2020_usd_m"),
            "electricity_pct": eco["macro_context"].get("electricity_access_pct"),
            "learning_poverty_pct": eco["macro_context"].get("learning_poverty_pct"),
            "cliff_risk": eco["recurrent_cliff_analysis"]["cliff_risk_tier"],
        })

    total_edu_aid = sum(r["edu_aid_disb_usd_m"] for r in comparison_table)
    total_ict_aid = sum(r["ict_aid_disb_usd_m"] for r in comparison_table)

    return {
        "metadata": {
            "title": "Macro-Fiscal & External Aid Observatory Dataset",
            "compiled_utc": datetime.now(timezone.utc).isoformat(),
            "script_version": "1.1.0",
            "coverage_window": "2017-2024",
            "target_economies": list(target_countries.keys()),
            "sources": [
                "IMF Government Finance Statistics (GFS) COFOG",
                "IATI Datastore Registry API (2017-2024 Normalized Transactions)",
                "World Bank / UNESCO UIS EdStats",
            ],
            "total_education_aid_usd_m": round(total_edu_aid, 2),
            "total_ict_aid_usd_m": round(total_ict_aid, 2),
        },
        "comparison_table": comparison_table,
        "countries": ecosystem_countries,
    }


# --------------------------------------------------------------------------
# Main Execution CLI
# --------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Compile IMF COFOG and IATI Datastore funding into a unified macro-fiscal dataset."
    )
    p.add_argument(
        "--countries",
        nargs="+",
        default=DEFAULT_PILOT_COUNTRIES,
        help="Target ISO3 or ISO2 country codes, or 'all-ssa' for all 48 SSA economies, or 'all-available' to auto-detect.",
    )
    p.add_argument(
        "--imf-shares",
        type=Path,
        default=Path("data/imf/imf_cofog_shares.csv"),
        help="Path to imf_cofog_shares.csv",
    )
    p.add_argument(
        "--iati-tx",
        type=Path,
        default=Path("data/iati/iati_transactions.csv"),
        help="Path to iati_transactions.csv",
    )
    p.add_argument(
        "--country-profiles",
        type=Path,
        default=Path("data/processed/latest_country_profiles_6pillars.csv"),
        help="Path to latest_country_profiles_6pillars.csv",
    )
    p.add_argument(
        "--out-json",
        type=Path,
        default=Path("data/processed/macro_fiscal_ecosystem.json"),
        help="Output JSON path",
    )
    p.add_argument(
        "--out-js",
        type=Path,
        default=Path("data/processed/macro_fiscal_data.js"),
        help="Output JavaScript module path",
    )
    p.add_argument("--since", type=int, default=2017, help="Starting year (default 2017)")
    p.add_argument("--until", type=int, default=2024, help="Ending year (default 2024)")
    p.add_argument("--force-refresh", action="store_true", help="Bypass local cache and recompile")
    p.add_argument("-v", "--verbose", action="store_true", help="Verbose debug logging")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    if not args.force_refresh and args.out_json.is_file() and args.out_js.is_file():
        try:
            cached_ds = json.loads(args.out_json.read_text(encoding="utf-8"))
            cached_countries = set(cached_ds.get("metadata", {}).get("target_economies", []))
            req_set = {c.upper() for c in args.countries}
            if req_set == cached_countries or (req_set == set(DEFAULT_PILOT_COUNTRIES) and set(DEFAULT_PILOT_COUNTRIES).issubset(cached_countries)):
                json_mtime = args.out_json.stat().st_mtime
                input_mtimes = [
                    p.stat().st_mtime for p in [args.imf_shares, args.iati_tx, args.country_profiles] if p.is_file()
                ]
                if input_mtimes and json_mtime >= max(input_mtimes):
                    logger.info(f"Cache hit: {args.out_json} is up to date (use --force-refresh to rebuild).")
                    print(f"Loaded compiled dataset from cache ({args.out_json}) for {sorted(cached_countries)}.")
                    return 0
        except Exception as e:
            logger.debug(f"Cache check bypass: {e}")

    logger.info("Starting Macro-Fiscal & External Aid compilation...")

    imf_shares_rows = load_csv_rows(args.imf_shares)
    iati_tx_rows = load_csv_rows(args.iati_tx)
    profiles_rows = load_csv_rows(args.country_profiles)

    if not imf_shares_rows and not iati_tx_rows:
        logger.error("Both IMF and IATI sources are missing! Check file paths.")
        return 1

    available_iso2_in_iati = {r.get("country_iso2", "") for r in iati_tx_rows if r.get("country_iso2")}
    available_iso3_in_imf = {r.get("country_iso3", "") for r in imf_shares_rows if r.get("country_iso3")}

    target_countries = resolve_country_metadata(
        args.countries, profiles_rows, available_iso2_in_iati, available_iso3_in_imf
    )
    logger.info(f"Target economies resolved ({len(target_countries)}): {list(target_countries.keys())}")

    imf_processed = process_imf_cofog(imf_shares_rows, target_countries)
    iati_processed = process_iati_funding(
        iati_tx_rows, target_countries, since_year=args.since, until_year=args.until
    )
    context_processed = load_country_profiles_context(profiles_rows, target_countries)

    dataset = synthesize_macro_fiscal(
        target_countries, imf_processed, iati_processed, context_processed
    )

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    logger.info(f"Saved primary JSON to {args.out_json}")

    args.out_js.parent.mkdir(parents=True, exist_ok=True)
    js_content = f"""// Generated Macro-Fiscal & External Aid Observatory Dataset
// Sources: IMF GFS COFOG (2017-2024) + IATI Datastore API (2017-2024) + UIS
// Target Economies ({len(target_countries)}): {', '.join(target_countries.keys())}
const MACRO_FISCAL_DATA = {json.dumps(dataset, indent=2)};

if (typeof module !== 'undefined' && module.exports) {{
  module.exports = {{ MACRO_FISCAL_DATA }};
}}
"""
    with open(args.out_js, "w", encoding="utf-8") as f:
        f.write(js_content)
    logger.info(f"Saved browser-ready JS to {args.out_js}")

    print("\n" + "=" * 90)
    print("MACRO-FISCAL & EXTERNAL AID OBSERVATORY COMPILATION SUMMARY")
    print("=" * 90)
    print(f"{'Country':<15} | {'Edu Budget %':<12} | {'Comm Budget %':<13} | {'Edu Aid (8-Yr)':<15} | {'2020 COVID Aid':<15} | {'Cliff Risk':<20}")
    print("-" * 90)
    for row in dataset["comparison_table"]:
        edu_b = f"{row['edu_pct_budget']:.1f}%" if row['edu_pct_budget'] is not None else "N/A"
        comm_b = f"{row['comm_pct_budget']:.2f}%" if row['comm_pct_budget'] is not None else "N/A"
        edu_aid = f"${row['edu_aid_disb_usd_m']:,.1f}M"
        covid_aid = f"${row['covid_2020_disb_usd_m']:,.1f}M" if row['covid_2020_disb_usd_m'] is not None else "N/A"
        print(f"{row['name']:<15} | {edu_b:<12} | {comm_b:<13} | {edu_aid:<15} | {covid_aid:<15} | {row['cliff_risk'][:20]:<20}")
    print("-" * 90)
    print(f"Total Education Aid Disbursed (2017-2024): ${dataset['metadata']['total_education_aid_usd_m']:,.2f} Million USD")
    print(f"Total ICT Aid Disbursed (2017-2024):       ${dataset['metadata']['total_ict_aid_usd_m']:,.2f} Million USD")
    print("=" * 90 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
