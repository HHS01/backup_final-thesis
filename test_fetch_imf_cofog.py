"""Offline tests for fetch_imf_cofog.py."""
import json
import tempfile
from pathlib import Path
import pandas as pd
import fetch_imf_cofog as fi

TMP = Path(tempfile.mkdtemp())

def test_window_flags():
    assert fi.resolve_window(5, None, None, False, now_year=2026) == (2022, 2026, "last 5 years (2022-2026)")
    assert fi.resolve_window(5, 2010, 2018, False)[:2] == (2010, 2018)
    assert fi.resolve_window(5, None, None, True)[:2] == (None, None)
    assert fi.resolve_window(5, 2019, None, False)[:2] == (2019, None)
    try:
        fi.resolve_window(0, None, None, False)
        raise AssertionError
    except fi.ImfError:
        pass

def test_detect_columns_and_classification():
    sample_data = pd.DataFrame({
        "Country Name": ["Kenya", "Kenya", "Rwanda"],
        "Classification": ["09 Education", "04.6 Communication", "Total Expenditure"],
        "Year": ["2023", "2023", "2022"],
        "Value": ["500", "50", "1000"],
        "Unit": ["USD", "USD", "USD"],
        "Sector": ["General Government", "General Government", "Central Government"],
    })
    cols = fi.detect_columns(sample_data, {})
    assert cols["country"] == "Country Name"
    assert cols["function"] == "Classification"
    assert cols["time"] == "Year"
    assert cols["value"] == "Value"
    assert cols["unit"] == "Unit"
    assert cols["sector"] == "Sector"

    classified = fi.classify_functions(sample_data["Classification"], fi.FUNCTION_PATTERNS)
    assert list(classified) == ["education", "communication", "total"]

def test_process_and_shares():
    data = pd.DataFrame([
        {"Country": "Kenya", "Function": "GF09", "Time": 2023, "Value": 400.0, "Unit": "LCU", "Sector": "S13"},
        {"Country": "Kenya", "Function": "GF046", "Time": 2023, "Value": 100.0, "Unit": "LCU", "Sector": "S13"},
        {"Country": "Kenya", "Function": "GF00", "Time": 2023, "Value": 2000.0, "Unit": "LCU", "Sector": "S13"},
        {"Country": "Kenya", "Function": "GF09", "Time": 2015, "Value": 300.0, "Unit": "LCU", "Sector": "S13"},
        {"Country": "Rwanda", "Function": "GF09", "Time": 2022, "Value": 250.0, "Unit": "LCU", "Sector": "S13"},
        {"Country": "Rwanda", "Function": "GF00", "Time": 2022, "Value": 1000.0, "Unit": "LCU", "Sector": "S13"},
    ])
    long, shares, extra = fi.process(
        data,
        iso3=["KEN", "RWA"],
        lo=2020,
        hi=2025,
        overrides={},
        patterns=fi.FUNCTION_PATTERNS
    )
    assert len(long) == 5

    # Check shares calculation
    ken_edu = shares[(shares.country_iso3 == "KEN") & (shares.group == "education") & (shares.year == 2023)].iloc[0]
    assert ken_edu["share_of_total_pct"] == 20.0  # 400 / 2000 * 100

    ken_comm = shares[(shares.country_iso3 == "KEN") & (shares.group == "communication") & (shares.year == 2023)].iloc[0]
    assert ken_comm["share_of_total_pct"] == 5.0  # 100 / 2000 * 100

    rwa_edu = shares[(shares.country_iso3 == "RWA") & (shares.group == "education") & (shares.year == 2022)].iloc[0]
    assert rwa_edu["share_of_total_pct"] == 25.0  # 250 / 1000 * 100

def test_cli_paths():
    assert fi.main(["--dry-run"]) == 0
    assert fi.main(["--countries", "XXX", "--dry-run"]) == 2
    assert fi.main(["--col", "bogus=x", "--dry-run"]) == 2

    # Test file input run
    data = pd.DataFrame([
        {"Country": "Kenya", "COFOG": "09 Education", "Time_Period": 2023, "OBS_VALUE": 500.0, "Unit": "USD", "Sector": "S13"},
        {"Country": "Kenya", "COFOG": "Total", "Time_Period": 2023, "OBS_VALUE": 2500.0, "Unit": "USD", "Sector": "S13"},
        {"Country": "Kenya", "COFOG": "09 Education", "Time_Period": 2015, "OBS_VALUE": 300.0, "Unit": "USD", "Sector": "S13"},
    ])
    p = TMP / "imf_test.csv"
    data.to_csv(p, index=False)
    out = TMP / "imf_out"

    assert fi.main(["--input", str(p), "--countries", "KEN", "--years", "5", "--out", str(out)]) == 0
    assert (out / "imf_cofog_long.csv").exists()
    assert (out / "imf_cofog_shares.csv").exists()
    assert (out / "imf_cofog_coverage.csv").exists()
    assert (out / "imf_cofog_audit.json").exists()

    shares_df = pd.read_csv(out / "imf_cofog_shares.csv")
    assert len(shares_df) == 1
    assert shares_df.iloc[0]["share_of_total_pct"] == 20.0

    # Non-existent input file
    assert fi.main(["--input", str(TMP / "nonexistent.csv")]) == 2

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            f()
            print("ok ", n)
