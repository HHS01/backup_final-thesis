"""Offline tests. Run:  python test_pipeline.py [path/to/report.pdf]

The API payloads below are small fixtures shaped like the documented responses
(World Bank, OpenAlex, Zenodo, World Bank Projects). They verify our parsing,
pagination and caching logic; they do NOT prove the live endpoints still behave
the same -- run the real commands once and inspect data/raw/ to confirm.
"""
import sys
import tempfile
from pathlib import Path

import edtech_pipeline as ep


def test_parse_wb():
    ok = [{"page": 1, "pages": 1, "total": 2},
          [{"indicator": {"id": "SE.PRM.TCAQ.ZS", "value": "Trained teachers, primary"},
            "country": {"id": "KE", "value": "Kenya"}, "countryiso3code": "KEN",
            "date": "2019", "value": 98.4},
           {"indicator": {"id": "SE.PRM.TCAQ.ZS", "value": "Trained teachers, primary"},
            "country": {"id": "KE", "value": "Kenya"}, "countryiso3code": "KEN",
            "date": "2020", "value": None}]]
    rows, pages = ep.parse_wb(ok)
    assert pages == 1 and rows[0]["iso3"] == "KEN" and rows[0]["year"] == 2019 and rows[1]["value"] is None
    assert ep.parse_wb([{"page": 1, "pages": 0, "total": 0}, None])[0] == []
    try:
        ep.parse_wb([{"message": [{"id": "120", "value": "Invalid value"}]}])
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_wb_pagination_and_cache():
    calls = []

    def fake_get_json(url, params=None, *, source, sleep=0):
        calls.append(params["page"])
        meta = {"page": params["page"], "pages": 2, "total": 2}
        row = {"indicator": {"id": "X", "value": "x"}, "country": {"id": "NG", "value": "Nigeria"},
               "countryiso3code": "NGA", "date": str(2010 + params["page"]), "value": 1.0}
        return [meta, [row]]

    real = ep.get_json
    ep.get_json = fake_get_json
    try:
        rows = ep.wb_fetch("X", ["NGA"], 2010, 2020)
    finally:
        ep.get_json = real
    assert calls == [1, 2] and len(rows) == 2


def test_get_json_cache():
    class R:
        url, content = "https://example.org/a", b"{}"
        def raise_for_status(self): pass
        def json(self): return {"hello": "world"}

    class S:
        n = 0
        def get(self, url, params=None, timeout=0):
            S.n += 1
            return R()

    ep.OUT = Path(tempfile.mkdtemp())
    ep._SESSION = S()
    a = ep.get_json("https://example.org/a", {"q": 1}, source="t", sleep=0)
    b = ep.get_json("https://example.org/a", {"q": 1}, source="t", sleep=0)
    assert a == b and S.n == 1, "second call should be served from cache"
    assert (ep.OUT / "manifest.jsonl").read_text().count("\n") == 1
    ep._SESSION = None


def test_parse_projects():
    data = {"total": 1, "projects": {"P1": {
        "id": "P1", "project_name": "Digital Learning", "countryshortname": "Kenya",
        "regionname": "Eastern and Southern Africa", "totalcommamt": "50,000,000",
        "sector1": {"Name": "Education"}, "project_abstract": {"cdata!": "Text"}}}}
    rows, total = ep.parse_projects(data)
    assert total == 1 and rows[0]["commitment_usd"] == 5e7
    assert rows[0]["sector1"] == "Education" and rows[0]["abstract"] == "Text"


def test_parse_openalex():
    data = {"results": [{"id": "W1", "doi": "d", "title": "T", "publication_year": 2023,
                         "cited_by_count": 3, "type": "article",
                         "primary_location": {"source": {"display_name": "J"}},
                         "open_access": {"oa_status": "gold"},
                         "authorships": [{"institutions": [{"country_code": "KE"}, {"country_code": "GB"}]}],
                         "abstract_inverted_index": {"Teachers": [0], "matter": [1]}}]}
    r = ep.parse_openalex(data)[0]
    assert r["abstract"] == "Teachers matter" and r["author_countries"] == "GB;KE"


def test_parse_zenodo():
    data = {"hits": {"hits": [{"doi": "10.5281/zenodo.1", "links": {"self_html": "u"},
                               "metadata": {"title": "T", "publication_date": "2021-01-01",
                                            "creators": [{"name": "A"}, {"name": "B"}],
                                            "license": {"id": "cc-by-4.0"}}}]}}
    r = ep.parse_zenodo(data)[0]
    assert r["creators"] == "A; B" and r["license"] == "cc-by-4.0"


def test_norm_category():
    assert ep.norm_category("Ups") == "Upskilling"
    assert ep.norm_category("IA") == "AI"
    assert ep.norm_category("K-12 (STEM)") == "K-12"
    assert ep.norm_category("AI / Inclusion") == "AI; Inclusion"


def test_pdf(pdf):
    df = ep.extract_players(pdf)
    counts = df.groupby("country").size().to_dict()
    # Counts verified by hand against the annex text of the report.
    assert counts["Senegal"] == 18 and counts["Benin"] == 14 and counts["Ivory Coast"] == 20
    assert counts["Nigeria"] == 12 and counts["Kenya"] == 3
    assert df["qa_flag"].fillna("").str.contains("identical_list").any()  # Niger == Guinea in the report
    urls, claims = ep.extract_urls_and_claims(pdf)
    assert "https://edtechecosystem.org/" in set(urls["url"]) and len(claims) > 20


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and name != "test_pdf":
            fn()
            print("ok ", name)
    if len(sys.argv) > 1:
        test_pdf(sys.argv[1])
        print("ok  test_pdf")
    else:
        print("skip test_pdf (pass the PDF path to run it)")
