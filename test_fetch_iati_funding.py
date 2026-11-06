"""Offline tests for fetch_iati_funding.py. Fixtures follow the DOCUMENTED field-naming convention
(sector_code, transaction_value, ...); the live API's exact responses are unverified (key pending)."""
import json, tempfile
from pathlib import Path
import pandas as pd
import fetch_iati_funding as fi

TMP = Path(tempfile.mkdtemp())
D = lambda **k: k
DOCS = [
 D(iati_identifier="A1", title_narrative=["Digital learning for schools"], description_narrative=["Tablets"],
   reporting_org_ref="ORG1", recipient_country_code=["KE"], sector_code=["11220", "22040"],
   sector_percentage=[60.0, 40.0], sector_vocabulary=["1", "1"], transaction_transaction_type_code="3",
   transaction_value=[1000.0], transaction_value_currency="USD",
   transaction_transaction_date_iso_date=["2024-05-01T00:00:00Z"]),
 D(iati_identifier="A2", title_narrative=["Old school grant"], reporting_org_ref="ORG2", recipient_country_code=["KE"],
   sector_code=["11120"], sector_percentage=[100.0], sector_vocabulary=["1"], transaction_transaction_type_code="3",
   transaction_value=[777.0], transaction_value_currency="USD", transaction_transaction_date_iso_date=["2015-02-01T00:00:00Z"]),
 D(iati_identifier="A3", title_narrative=["EdTech pilot for teachers"], reporting_org_ref="ORG1", recipient_country_code=["RW"],
   sector_code=["16050"], sector_percentage=[100.0], sector_vocabulary=["1"], transaction_transaction_type_code="2",
   transaction_value=[300.0], transaction_value_currency="USD", transaction_transaction_date_iso_date=["2023-03-01T00:00:00Z"]),
 D(iati_identifier="A4", title_narrative=["Health"], reporting_org_ref="ORG3", recipient_country_code=["KE"],
   sector_code=["16050", "3", "10"], sector_percentage=[100.0, 50.0, 50.0], sector_vocabulary=["1", "7", "7"],
   transaction_transaction_type_code="3", transaction_value=[50.0], transaction_value_currency="USD",
   transaction_transaction_date_iso_date=["2024-01-01T00:00:00Z"]),
 D(iati_identifier="A5", title_narrative=["Schools"], reporting_org_ref="ORG4", recipient_country_code=["NG"],
   sector_code=["11220"], transaction_transaction_type_code="4", transaction_value=[500.0], transaction_value_currency="EUR",
   transaction_transaction_date_iso_date=["2025-06-01T00:00:00Z"]),
]

def test_window_flags():
    assert fi.resolve_window(5, None, None, False, now_year=2026) == (2022, 2026, "last 5 years (2022-2026)")
    assert fi.resolve_window(5, 2010, 2018, False)[:2] == (2010, 2018)
    assert fi.resolve_window(5, None, None, True)[:2] == (None, None)
    assert fi.resolve_window(5, 2019, None, False)[:2] == (2019, None)
    try: fi.resolve_window(0, None, None, False); raise AssertionError
    except fi.IatiError: pass

def test_query_and_as_list():
    f = {k: v[0] for k, v in fi.FIELD_CANDIDATES.items()}
    q = fi.build_query(["KE", "RW"], 2022, 2026, True, f)
    assert "recipient_country_code:(KE OR RW)" in q and "sector_code:(111* OR 112* OR 113* OR 114* OR 220*)" in q
    assert "[2022-01-01T00:00:00Z TO 2026-12-31T23:59:59Z]" in q and "edtech" in q
    assert "TO" not in fi.build_query(["KE"], None, None, False, f) and "edtech" not in fi.build_query(["KE"], None, None, False, f)
    assert "[2010-01-01T00:00:00Z TO *]" in fi.build_query(["KE"], 2010, None, False, f)
    assert fi.as_list(["a"]) == ["a"] and fi.as_list("['3','10']") == ["3", "10"] and fi.as_list("3;10") == ["3", "10"]
    assert fi.as_list(None) == [] and fi.as_list(5.0) == [5.0] and fi.as_list(float("nan")) == []

def test_sector_attribution():
    a = fi.sector_attribution(["11220", "22040"], [60, 40], ["1", "1"])
    assert a == {"education": (0.6, True), "ict_communications": (0.4, True)}
    assert fi.sector_attribution(["16050", "3", "10"], [100, 50, 50], ["1", "7", "7"]) == {}
    assert fi.sector_attribution(["11220"], [], []) == {"education": (1.0, False)}   # cannot align -> flagged

def test_normalise_filter_aggregate():
    tx, fm, _ = fi.normalise(DOCS)
    assert fm["tx_value"] == "transaction_value" and len(tx) == 5     # A1x2, A2, A3(keyword), A5 ; A4 dropped
    a1 = tx[tx.iati_id == "A1"].set_index("group")
    assert a1.loc["education", "value_attributed"] == 600.0 and a1.loc["ict_communications", "value_attributed"] == 400.0
    assert tx[tx.iati_id == "A3"].iloc[0]["group"] == "edtech_keyword" and tx[tx.iati_id == "A3"].iloc[0]["tx_type"] == "commitment"
    assert not tx[tx.iati_id == "A5"].iloc[0]["sector_share_known"]
    rec = fi.filter_window(tx, 2022, 2026, ["KE", "RW", "NG"])
    assert "A2" not in set(rec.iati_id), "2015 transaction must fall outside the recent window"
    hist = fi.filter_window(tx, None, None, ["KE"])
    assert "A2" in set(hist.iati_id) and "A3" not in set(hist.iati_id), "country filter applies; no date filter in history"
    fy = fi.funding_by_year(rec)
    k = fy.set_index(["country_iso2", "year", "group", "tx_type", "currency"])["value"]
    assert k[("KE", 2024, "education", "disbursement", "USD")] == 600.0
    assert k[("NG", 2025, "education", "expenditure", "EUR")] == 500.0 and k[("RW", 2023, "edtech_keyword", "commitment", "USD")] == 300.0
    try: fi.normalise([{"foo": 1}]); raise AssertionError
    except fi.IatiError as e: assert "--field" in str(e)
    tx2, fm2, _ = fi.normalise([{**DOCS[0], "my_val": [9.0]}], {"tx_value": "my_val"})
    assert tx2.iloc[0]["value"] == 9.0

class R:
    def __init__(s, payload=None, status=200, text=""): s._p, s.status_code, s.text = payload, status, text
    def json(s): return s._p
    def raise_for_status(s):
        if s.status_code >= 400: raise RuntimeError(s.status_code)
class S:
    def __init__(s, rs): s.rs, s.calls = list(rs), []
    def get(s, url, params=None, headers=None, timeout=0): s.calls.append((url, params, headers)); return s.rs.pop(0)

def test_client_paging_and_errors():
    s = S([R({"response": {"numFound": 3, "docs": [DOCS[0], DOCS[1]]}}), R({"response": {"numFound": 3, "docs": [DOCS[2]]}})])
    docs, total = fi.IatiClient(s, "https://x/datastore/", "K", "Hdr").select("transaction", "q", rows=2, sleep=0)
    assert len(docs) == 3 and total == 3 and s.calls[1][1]["start"] == 2 and s.calls[0][2] == {"Hdr": "K"}
    assert s.calls[0][0] == "https://x/datastore/transaction/select".replace("datastore/", "datastore/")
    s = S([R({"response": {"numFound": 9, "docs": [DOCS[0]] * 4}})])
    assert len(fi.IatiClient(s, "https://x", "K", "H").select("transaction", "q", rows=4, max_rows=2, sleep=0)[0]) == 2
    for status, word in ((401, "developer.iatistandard.org"), (400, "--q"), (404, "--base-url")):
        try: fi.IatiClient(S([R(status=status, text="bad")]), "https://x", "K", "H").select("transaction", "q"); raise AssertionError
        except fi.IatiError as e: assert word in str(e)

def test_cli_paths(capsys=None):
    import os
    os.environ.pop("IATI_API_KEY", None)
    assert fi.main(["--dry-run"]) == 0 and fi.main(["--out", str(TMP / "nokey")]) == 2     # key required for API mode
    assert fi.main(["--countries", "XXX", "--dry-run"]) == 2 and fi.main(["--field", "bogus=x", "--dry-run"]) == 2
    rows = []
    for d in DOCS:
        r = {k: (";".join(map(str, v)) if isinstance(v, list) else v) for k, v in d.items()}
        rows.append(r)
    p = TMP / "download.csv"; pd.DataFrame(rows).to_csv(p, index=False)
    out = TMP / "o"
    assert fi.main(["--input", str(p), "--countries", "KEN", "RWA", "NGA", "--years", "5", "--out", str(out)]) == 0
    fy = pd.read_csv(out / "iati_funding_by_year.csv")
    assert not fy.empty and 2015 not in set(fy.year), "default window must exclude 2015"
    audit = json.loads((out / "iati_audit.json").read_text())
    assert audit["latest_year_with_data"]["NG"] == 2025 and "USD" in audit["currencies_seen"] and "EUR" in audit["currencies_seen"]
    out2 = TMP / "o2"
    assert fi.main(["--input", str(p), "--countries", "KEN", "--all-years", "--out", str(out2)]) == 0
    assert 2015 in set(pd.read_csv(out2 / "iati_funding_by_year.csv").year), "history flag must include 2015"
    assert fi.main(["--input", str(TMP / "nope.csv"), "--out", str(TMP / "o3")]) == 2

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print("ok ", n)
