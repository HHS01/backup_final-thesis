"""
Tests for compile_macro_fiscal_indicators.py
============================================
Validates the synthesis of IMF COFOG, IATI Datastore external aid,
and World Bank/UNESCO UIS indicators.
"""

import json
import subprocess
import sys
from pathlib import Path
import pytest

from scripts.compile_macro_fiscal_indicators import (
    DEFAULT_PILOT_COUNTRIES,
    CURATED_ARCHETYPES,
    AFRICA_ISO_MAP,
    CURRENCY_TO_USD,
    resolve_country_metadata,
    process_imf_cofog,
    process_iati_funding,
    synthesize_macro_fiscal,
)


ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"


def test_target_countries_configuration():
    assert len(DEFAULT_PILOT_COUNTRIES) == 7
    expected = {"KEN", "RWA", "TZA", "MUS", "GHA", "NGA", "ZMB"}
    assert set(DEFAULT_PILOT_COUNTRIES) == expected
    for iso3, meta in CURATED_ARCHETYPES.items():
        assert "name" in meta
        assert "archetype" in meta
        assert "cliff_tier" in meta


def test_africa_iso_map_coverage():
    assert len(AFRICA_ISO_MAP) >= 54
    assert AFRICA_ISO_MAP["KEN"] == ("KE", "Kenya")
    assert AFRICA_ISO_MAP["UGA"] == ("UG", "Uganda")
    assert AFRICA_ISO_MAP["SEN"] == ("SN", "Senegal")


def test_currency_conversion_rates():
    assert CURRENCY_TO_USD["USD"] == 1.0
    assert CURRENCY_TO_USD["GBP"] > 1.0
    assert CURRENCY_TO_USD["EUR"] > 1.0
    assert CURRENCY_TO_USD["JPY"] < 0.1
    assert "KES" in CURRENCY_TO_USD
    assert "TZS" in CURRENCY_TO_USD
    assert "ZMK" in CURRENCY_TO_USD


def test_generated_json_exists_and_valid():
    json_path = PROCESSED_DIR / "macro_fiscal_ecosystem.json"
    assert json_path.is_file(), f"Missing {json_path}"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "metadata" in data
    assert "comparison_table" in data
    assert "countries" in data

    meta = data["metadata"]
    assert meta["coverage_window"] == "2017-2024"
    assert meta["total_education_aid_usd_m"] > 5000.0  # Over $5B in education aid
    assert meta["total_ict_aid_usd_m"] > 300.0

    # Ensure all 7 countries exist
    for iso3 in DEFAULT_PILOT_COUNTRIES:
        assert iso3 in data["countries"], f"Missing {iso3} in countries"
        c_obj = data["countries"][iso3]

        assert "domestic_fiscal" in c_obj
        assert "external_assistance" in c_obj
        assert "recurrent_cliff_analysis" in c_obj
        assert "macro_context" in c_obj

        # Test external assistance timeseries
        ext = c_obj["external_assistance"]
        assert "annual_timeseries" in ext
        ts = ext["annual_timeseries"]
        for yr in range(2017, 2025):
            assert str(yr) in ts, f"Missing year {yr} in {iso3} external assistance"

        # Check 2020 COVID surge data
        assert "covid_2020_surge" in ext
        covid = ext["covid_2020_surge"]
        assert "disbursed_2019_usd_m" in covid
        assert "disbursed_2020_usd_m" in covid


def test_generated_js_exists_and_parseable():
    js_path = PROCESSED_DIR / "macro_fiscal_data.js"
    assert js_path.is_file(), f"Missing {js_path}"

    with open(js_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "const MACRO_FISCAL_DATA =" in content
    prefix = "const MACRO_FISCAL_DATA = "
    start_idx = content.find(prefix) + len(prefix)
    end_idx = content.rfind(";\n\nif (typeof module")
    json_str = content[start_idx:end_idx].strip()
    data = json.loads(json_str)
    assert len(data["countries"]) >= 7


def test_kenya_domestic_fiscal_series():
    json_path = PROCESSED_DIR / "macro_fiscal_ecosystem.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    ken = data["countries"]["KEN"]
    dom = ken["domestic_fiscal"]
    assert dom["has_imf_cofog"] is True
    assert dom["education_pct_budget"] == pytest.approx(18.43, 0.5)
    assert dom["communication_pct_budget"] == pytest.approx(0.46, 0.1)

    # Check timeseries completeness
    ts = dom["annual_timeseries"]
    for yr in range(2017, 2024):
        assert str(yr) in ts
        assert ts[str(yr)]["education_pct_budget"] is not None
        assert ts[str(yr)]["communication_pct_budget"] is not None

    cliff = ken["recurrent_cliff_analysis"]
    assert "High Tension" in cliff["cliff_risk_tier"]
    assert cliff["domestic_edu_to_comm_ratio"] > 35.0


def test_dynamic_country_resolution():
    profiles = [{"iso3": "UGA", "country": "Uganda", "region": "SSA", "EG.ELC.ACCS.ZS": "55.3", "IT.NET.USER.ZS": "8.9"}]
    res = resolve_country_metadata(["UGA", "SEN"], profiles, {"UG", "SN"}, {"UGA"})
    assert "UGA" in res
    assert "SEN" in res
    assert res["UGA"]["name"] == "Uganda"
    assert res["UGA"]["iso2"] == "UG"
    assert res["SEN"]["name"] == "Senegal"
    assert res["SEN"]["iso2"] == "SN"
    assert "Educational Infrastructure" in res["UGA"]["archetype"]


def test_cli_execution():
    cmd = [sys.executable, "scripts/compile_macro_fiscal_indicators.py", "--force-refresh"]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    assert res.returncode == 0
    assert "MACRO-FISCAL & EXTERNAL AID OBSERVATORY COMPILATION SUMMARY" in res.stdout

    # Test cache hit on second run
    cmd_cached = [sys.executable, "scripts/compile_macro_fiscal_indicators.py"]
    res_cached = subprocess.run(cmd_cached, capture_output=True, text=True, cwd=str(ROOT))
    assert res_cached.returncode == 0
    assert "Loaded compiled dataset from cache" in res_cached.stdout
