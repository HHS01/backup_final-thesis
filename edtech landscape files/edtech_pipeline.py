#!/usr/bin/env python3
"""
EdTech Africa data pipeline
===========================
Pulls open, non-paywalled data to complement the UNDP/timbuktoo report
"Strategic Mapping of the EdTech Ecosystem in Africa" (Dec 2025).

Sub-commands (each writes tidy CSVs under ./data and logs to data/manifest.jsonl):

  pdf        Reverse-engineer the report PDF: URLs cited, key-player directory
             (annex 5), and every sentence containing a figure (%, $, million..).
  wb         World Bank Indicators API (includes UNESCO-UIS teacher series and
             ITU connectivity series mirrored by the World Bank).
  projects   World Bank Projects API: education/digital-learning financing.
  dhs        DHS Program API: household electricity/radio/TV/internet/phone.
  openalex   OpenAlex: prior academic work (use it to check overlap).
  zenodo     Zenodo: EdTech Hub and other open-access reports.
  all        Everything above (pdf needs --pdf).

Raw API responses are cached in data/raw/, so re-runs are free and offline-safe.
No API keys are required. Pass --mailto with a real address for OpenAlex's
polite pool. Check each source's licence before redistributing (see manifest).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

OUT = Path("data")
UA = "edtech-africa-pipeline/0.1 (academic research)"

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
# World Bank "Sub-Saharan Africa" economies (48). Override with --countries.
SSA_ISO3 = (
    "AGO BEN BWA BFA BDI CPV CMR CAF TCD COM COD COG CIV GNQ ERI SWZ ETH GAB GMB "
    "GHA GIN GNB KEN LSO LBR MDG MWI MLI MUS MRT MOZ NAM NER NGA RWA STP SEN SYC "
    "SLE SOM ZAF SSD SDN TZA TGO UGA ZMB ZWE"
).split()

# code -> why we want it. Codes are validated against the API at run time;
# any that do not resolve are skipped and listed in data/wb_skipped.txt.
WB_INDICATORS = {
    # Teacher side (UNESCO-UIS series mirrored in the WB API; CC BY-4.0 on data.worldbank.org)
    "SE.PRE.TCAQ.ZS": "Trained teachers, pre-primary (% of teachers)",
    "SE.PRM.TCAQ.ZS": "Trained teachers, primary (% of teachers)",
    "SE.SEC.TCAQ.ZS": "Trained teachers, secondary (% of teachers)",
    "SE.PRM.ENRL.TC.ZS": "Pupil-teacher ratio, primary",
    "SE.SEC.ENRL.TC.ZS": "Pupil-teacher ratio, secondary",
    # Infrastructure / access
    "EG.ELC.ACCS.ZS": "Access to electricity (% of population)",
    "IT.NET.USER.ZS": "Individuals using the Internet (%)",
    "IT.CEL.SETS.P2": "Mobile subscriptions (per 100 people)",
    # Context
    "SP.POP.TOTL": "Population, total",
    "SP.URB.TOTL.IN.ZS": "Urban population (% of total)",
    "NY.GDP.PCAP.CD": "GDP per capita (current US$)",
    "SE.XPD.TOTL.GD.ZS": "Government expenditure on education (% of GDP)",
    "SE.PRM.NENR": "Net enrolment rate, primary (%)",
    "SE.ADT.LITR.ZS": "Adult literacy rate (%)",
}

PROJECT_QUERIES = [
    "education technology", "digital learning", "e-learning",
    "teacher training ICT", "distance education", "digital skills education",
]
# Region names seen in the Projects API for sub-Saharan Africa.
PROJECT_REGIONS = {"Eastern and Southern Africa", "Western and Central Africa", "Africa"}

DHS_KEYWORDS = r"electricity|radio|television|internet|mobile (tele)?phone|computer"

OPENALEX_QUERIES = [
    "EdTech Africa teachers",
    "educational technology sub-Saharan Africa",
    "teacher professional development digital sub-Saharan Africa",
    "EdTech startups Africa",
    "ICT in education Africa policy",
    "mobile learning low-resource schools Africa",
]
ZENODO_QUERIES = ['"EdTech Hub"', "edtech Africa"]

LICENSE_NOTES = {
    "worldbank": "World Bank Open Data; UIS-sourced series CC BY-4.0. Check indicator-level terms.",
    "wb_projects": "World Bank Projects & Operations open data. Check terms of use.",
    "dhs": "DHS Program open API. Check DHS terms of use; cite the survey.",
    "openalex": "OpenAlex data is CC0.",
    "zenodo": "Per-record licence (see 'license' column).",
}

# --------------------------------------------------------------------------
# HTTP helpers: caching, retries, provenance
# --------------------------------------------------------------------------
_SESSION: requests.Session | None = None


def _session() -> requests.Session:
    global _SESSION
    if _SESSION is None:
        s = requests.Session()
        retry = Retry(total=4, backoff_factor=1.5,
                      status_forcelist=(429, 500, 502, 503, 504),
                      allowed_methods=("GET",))
        s.mount("https://", HTTPAdapter(max_retries=retry))
        s.headers["User-Agent"] = UA
        _SESSION = s
    return _SESSION


def _log_manifest(source: str, url: str, nbytes: int) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rec = {"source": source, "url": url, "bytes": nbytes,
           "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "licence_note": LICENSE_NOTES.get(source, "")}
    with open(OUT / "manifest.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def get_json(url: str, params: dict | None = None, *, source: str, sleep: float = 0.4):
    """GET + JSON with on-disk cache keyed by (url, params)."""
    key = hashlib.sha1((url + json.dumps(params or {}, sort_keys=True)).encode()).hexdigest()[:16]
    path = OUT / "raw" / source / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    r = _session().get(url, params=params, timeout=60)
    r.raise_for_status()
    data = r.json()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")
    _log_manifest(source, r.url, len(r.content))
    time.sleep(sleep)
    return data


def save(df: pd.DataFrame, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / name, index=False)
    print(f"  wrote data/{name}  ({len(df)} rows)")


# --------------------------------------------------------------------------
# 1. PDF reverse-engineering
# --------------------------------------------------------------------------
CAT_MAP = {"ups": "Upskilling", "upskilling": "Upskilling", "ia": "AI", "ai": "AI",
           "platforms": "Platform", "platform": "Platform", "contents": "Content",
           "content": "Content", "k-12": "K-12", "lms": "LMS", "tvet": "TVET",
           "higher ed": "Higher Ed", "marketplace": "Marketplace", "data": "Data",
           "inclusion": "Inclusion"}
NUMERIC_CLAIM = re.compile(r"\d[\d.,]*\s?%|\$\s?\d|USD\s?\d|\d[\d.,]*\s?(?:million|billion)", re.I)


def norm_category(raw: str) -> str:
    parts = [p.strip() for p in re.split(r"\s*/\s*", raw) if p.strip()]
    out = []
    for p in parts:
        base = re.sub(r"\(.*?\)", "", p).strip().lower()
        out.append(CAT_MAP.get(base, p))
    return "; ".join(out)


def _cluster_rows(words, tol=3.0):
    rows: list[list[dict]] = []
    for w in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if rows and abs(rows[-1][0]["top"] - w["top"]) <= tol:
            rows[-1].append(w)
        else:
            rows.append([w])
    return rows


def extract_players(pdf_path: str) -> pd.DataFrame:
    """Annex 5 'Key players by country': rows of `Name -> Category` laid out by
    coordinates. Country headers are the large (>=15pt) capitalised lines."""
    import pdfplumber
    recs, country, started = [], None, False
    with pdfplumber.open(pdf_path) as pdf:
        for pno, page in enumerate(pdf.pages, start=1):
            words = page.extract_words(extra_attrs=["size"])
            has_arrow = any(w["text"] == "\u2192" for w in words)
            if not started:
                if has_arrow and "Key players by country" in (page.extract_text() or ""):
                    started = True
                else:
                    continue
            elif not has_arrow:
                break
            arrows = [w for w in words if w["text"] == "\u2192"]
            headers = _cluster_rows([w for w in words if w["size"] >= 15])
            header_list = [(h[0]["top"], " ".join(w["text"] for w in h).title()) for h in headers]
            body = [w for w in words if w["size"] < 15 and w["text"] != "\u2192"]
            for row in _cluster_rows(body):
                top = row[0]["top"]
                for htop, hname in header_list:
                    if htop <= top + 1:
                        country = hname
                text = " ".join(w["text"] for w in sorted(row, key=lambda w: w["x0"]))
                if country is None or text.strip().isdigit() or min(w["x0"] for w in row) > 110:
                    continue
                # The arrow glyph renders ~7pt ABOVE its entry's text, so take the
                # closest unused arrow at/above this row (the next row's arrow is below it).
                cand = [a for a in arrows if -2 <= top - a["top"] <= 14]
                flag = ""
                if cand:
                    a = min(cand, key=lambda a: top - a["top"] if top - a["top"] >= 0 else 99)
                    arrows.remove(a)
                    name = " ".join(w["text"] for w in row if w["x0"] < a["x0"])
                    cat = " ".join(w["text"] for w in row if w["x0"] > a["x0"])
                else:  # no arrow glyph: last word is the category (e.g. truncated 'Ups')
                    toks = [w["text"] for w in sorted(row, key=lambda w: w["x0"])]
                    name, cat, flag = " ".join(toks[:-1]), toks[-1], "no_arrow"
                if name and cat:
                    recs.append({"country": country, "name": name.strip(),
                                 "category_raw": cat.strip(), "category": norm_category(cat),
                                 "pdf_page": pno, "parse_flag": flag})
    df = pd.DataFrame(recs)
    if df.empty:
        return df
    # QA flags for things a reader should double-check before reuse
    sets = df.groupby("country")["name"].apply(frozenset)
    dup_lists = {c: [o for o in sets.index if o != c and sets[o] == sets[c]] for c in sets.index}
    df["qa_flag"] = df.apply(lambda r: "; ".join(filter(None, [
        f"identical_list_to:{','.join(dup_lists[r.country])}" if dup_lists[r.country] else "",
        "university_not_startup" if re.search(r"universit", r["name"], re.I) else "",
        r.parse_flag])), axis=1)
    return df.drop(columns="parse_flag")


def extract_urls_and_claims(pdf_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    import pdfplumber
    urls, claims = [], []
    with pdfplumber.open(pdf_path) as pdf:
        for pno, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            joined = re.sub(r"(https?://\S*-)\n(\S)", r"\1\2", text)  # re-join wrapped URLs
            for u in re.findall(r"https?://[^\s)>\"]+", joined):
                urls.append({"url": u.rstrip(".,;"), "pdf_page": pno})
            flat = re.sub(r"\s+", " ", text)
            for s in re.split(r"(?<=[.!?])\s+", flat):
                if NUMERIC_CLAIM.search(s) and 25 < len(s) < 500:
                    claims.append({"pdf_page": pno, "sentence": s.strip()})
    u = pd.DataFrame(urls).drop_duplicates("url") if urls else pd.DataFrame(columns=["url", "pdf_page"])
    return u, pd.DataFrame(claims)


def run_pdf(pdf_path: str) -> None:
    print("PDF extraction")
    players = extract_players(pdf_path)
    save(players, "pdf_key_players.csv")
    urls, claims = extract_urls_and_claims(pdf_path)
    save(urls, "pdf_urls.csv")
    save(claims, "pdf_numeric_claims.csv")


# --------------------------------------------------------------------------
# 2. World Bank Indicators API
# --------------------------------------------------------------------------
WB = "https://api.worldbank.org/v2"


def parse_wb(data) -> tuple[list[dict], int]:
    """Indicators API returns [meta, rows]; errors come back as [{'message': [...]}]."""
    if not isinstance(data, list) or not data:
        raise ValueError(f"unexpected response: {str(data)[:120]}")
    if isinstance(data[0], dict) and "message" in data[0]:
        raise ValueError(f"API error: {data[0]['message']}")
    meta, rows = data[0], (data[1] if len(data) > 1 else None)
    out = [{"iso3": r.get("countryiso3code") or r["country"]["id"], "country": r["country"]["value"],
            "indicator": r["indicator"]["id"], "indicator_name": r["indicator"]["value"],
            "year": int(r["date"]), "value": r["value"]} for r in (rows or [])]
    return out, int(meta.get("pages", 1) or 1)


def wb_fetch(code: str, countries: list[str], start: int, end: int) -> list[dict]:
    rows, page = [], 1
    while True:
        data = get_json(f"{WB}/country/{';'.join(countries)}/indicator/{code}",
                        {"format": "json", "per_page": 20000, "page": page,
                         "date": f"{start}:{end}"}, source="worldbank")
        part, pages = parse_wb(data)
        rows += part
        if page >= pages:
            return rows
        page += 1


def run_wb(countries: list[str], start: int, end: int) -> None:
    print("World Bank indicators")
    all_rows, skipped = [], []
    for code in WB_INDICATORS:
        try:
            all_rows += wb_fetch(code, countries, start, end)
        except Exception as e:  # keep going; report at the end
            skipped.append(f"{code}\t{e}")
    df = pd.DataFrame(all_rows)
    if not df.empty:
        df = df.dropna(subset=["value"])
        save(df, "wb_indicators_long.csv")
        latest = (df.sort_values("year").groupby(["iso3", "indicator"]).tail(1)
                  .pivot(index="iso3", columns="indicator", values="value"))
        years = (df.sort_values("year").groupby(["iso3", "indicator"]).tail(1)
                 .pivot(index="iso3", columns="indicator", values="year").add_suffix("_year"))
        save(latest.join(years).reset_index(), "wb_latest_wide.csv")
    if skipped:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "wb_skipped.txt").write_text("\n".join(skipped), encoding="utf-8")
        print(f"  {len(skipped)} indicator(s) skipped -> data/wb_skipped.txt")


# --------------------------------------------------------------------------
# 3. World Bank Projects API
# --------------------------------------------------------------------------
def _name(v):
    return v.get("Name") if isinstance(v, dict) else v


def _text(v):
    return v.get("cdata!") if isinstance(v, dict) else v


def _num(v):
    try:
        return float(str(v).replace(",", ""))
    except (TypeError, ValueError):
        return None


def parse_projects(data: dict) -> tuple[list[dict], int]:
    out = []
    for pid, p in (data.get("projects") or {}).items():
        out.append({"project_id": p.get("id", pid), "name": p.get("project_name"),
                    "country": p.get("countryshortname"), "country_code": p.get("countrycode"),
                    "region": p.get("regionname"),
                    "status": p.get("projectstatusdisplay") or p.get("status"),
                    "approval_date": p.get("boardapprovaldate"), "closing_date": p.get("closingdate"),
                    "commitment_usd": _num(p.get("totalcommamt") or p.get("totalamt")),
                    "sector1": _name(p.get("sector1")), "theme1": _name(p.get("theme1")),
                    "borrower": p.get("borrower"), "agency": p.get("impagency"),
                    "url": p.get("url"), "abstract": _text(p.get("project_abstract"))})
    return out, int(data.get("total", 0) or 0)


def run_projects(max_per_query: int) -> None:
    print("World Bank projects")
    rows = {}
    for q in PROJECT_QUERIES:
        os_ = 0
        while os_ < max_per_query:
            data = get_json("https://search.worldbank.org/api/v2/projects",
                            {"format": "json", "qterm": q, "rows": 100, "os": os_},
                            source="wb_projects")
            part, total = parse_projects(data)
            for r in part:
                r["matched_query"] = q
                rows.setdefault(r["project_id"], r)
            os_ += 100
            if not part or os_ >= total:
                break
    df = pd.DataFrame(rows.values())
    if not df.empty:
        df = df[df["region"].isin(PROJECT_REGIONS)]
    save(df, "wb_projects_education_ssa.csv")


# --------------------------------------------------------------------------
# 4. DHS API (household assets relevant to radio/TV/online delivery)
# --------------------------------------------------------------------------
DHS = "https://api.dhsprogram.com/rest/dhs"


def dhs_paged(path: str, params: dict | None = None) -> list[dict]:
    rows, page = [], 1
    while True:
        d = get_json(f"{DHS}/{path}", {**(params or {}), "f": "json", "perpage": 1000, "page": page},
                     source="dhs")
        rows += d.get("Data") or []
        if page >= int(d.get("TotalPages") or 1):
            return rows
        page += 1


def run_dhs(iso3: list[str]) -> None:
    print("DHS")
    countries = pd.DataFrame(dhs_paged("countries"))
    if "ISO3_CountryCode" not in countries:
        sys.exit("  DHS /countries changed shape; inspect api.dhsprogram.com/rest/dhs/countries/fields")
    codes = countries[countries["ISO3_CountryCode"].isin(iso3)]["DHS_CountryCode"].tolist()
    inds = pd.DataFrame(dhs_paged("indicators"))
    text = inds["Label"].fillna("") + " " + inds.get("Definition", pd.Series("", index=inds.index)).fillna("")
    sel = inds[text.str.contains(DHS_KEYWORDS, case=False, regex=True)]
    save(sel[["IndicatorId", "Label"]], "dhs_indicator_catalog_filtered.csv")
    rows = []
    ids = sel["IndicatorId"].tolist()[:60]
    for i in range(0, len(ids), 10):
        rows += dhs_paged("data", {"indicatorIds": ",".join(ids[i:i + 10]),
                                   "countryIds": ",".join(codes), "breakdown": "national"})
    keep = ["IndicatorId", "Indicator", "CountryName", "DHS_CountryCode", "SurveyYear", "Value", "SurveyId"]
    df = pd.DataFrame(rows)
    save(df[[c for c in keep if c in df]] if not df.empty else df, "dhs_household_assets.csv")


# --------------------------------------------------------------------------
# 5. OpenAlex (prior work / overlap check)
# --------------------------------------------------------------------------
def reconstruct_abstract(inv: dict | None) -> str | None:
    if not inv:
        return None
    pos = {i: w for w, idxs in inv.items() for i in idxs}
    return " ".join(pos[i] for i in sorted(pos))


def parse_openalex(data: dict) -> list[dict]:
    out = []
    for w in data.get("results", []):
        loc = (w.get("primary_location") or {}).get("source") or {}
        countries = sorted({i.get("country_code") for a in w.get("authorships", [])
                            for i in a.get("institutions", []) if i.get("country_code")})
        out.append({"openalex_id": w.get("id"), "doi": w.get("doi"), "title": w.get("title"),
                    "year": w.get("publication_year"), "cited_by": w.get("cited_by_count"),
                    "type": w.get("type"), "venue": loc.get("display_name"),
                    "oa_status": (w.get("open_access") or {}).get("oa_status"),
                    "author_countries": ";".join(countries),
                    "abstract": reconstruct_abstract(w.get("abstract_inverted_index"))})
    return out


def run_openalex(mailto: str | None, from_year: int, max_pages: int) -> None:
    print("OpenAlex")
    rows = {}
    for q in OPENALEX_QUERIES:
        cursor = "*"
        for _ in range(max_pages):
            params = {"search": q, "filter": f"from_publication_date:{from_year}-01-01",
                      "per-page": 100, "cursor": cursor,
                      "select": "id,doi,title,publication_year,cited_by_count,type,primary_location,"
                                "open_access,authorships,abstract_inverted_index"}
            if mailto:
                params["mailto"] = mailto
            data = get_json("https://api.openalex.org/works", params, source="openalex")
            for r in parse_openalex(data):
                r["matched_query"] = q
                rows.setdefault(r["openalex_id"], r)
            cursor = (data.get("meta") or {}).get("next_cursor")
            if not cursor:
                break
    save(pd.DataFrame(rows.values()), "openalex_prior_work.csv")


# --------------------------------------------------------------------------
# 6. Zenodo
# --------------------------------------------------------------------------
def parse_zenodo(data: dict) -> list[dict]:
    out = []
    for h in (data.get("hits") or {}).get("hits", []):
        md = h.get("metadata", {})
        out.append({"title": md.get("title"), "doi": h.get("doi") or md.get("doi"),
                    "date": md.get("publication_date"),
                    "creators": "; ".join(c.get("name", "") for c in md.get("creators", [])),
                    "license": (md.get("license") or {}).get("id"),
                    "url": (h.get("links") or {}).get("self_html")})
    return out


def run_zenodo() -> None:
    print("Zenodo")
    rows = {}
    for q in ZENODO_QUERIES:
        for page in range(1, 6):
            data = get_json("https://zenodo.org/api/records",
                            {"q": q, "size": 100, "page": page, "sort": "mostrecent"}, source="zenodo")
            part = parse_zenodo(data)
            for r in part:
                rows.setdefault(r["doi"] or r["title"], r)
            if len(part) < 100:
                break
    save(pd.DataFrame(rows.values()), "zenodo_records.csv")


# --------------------------------------------------------------------------
def main(argv=None) -> None:
    global OUT
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["pdf", "wb", "projects", "dhs", "openalex", "zenodo", "all"])
    ap.add_argument("--pdf", help="path to the report PDF")
    ap.add_argument("--out", default="data")
    ap.add_argument("--countries", nargs="+", default=SSA_ISO3, help="ISO3 codes")
    ap.add_argument("--start", type=int, default=2010)
    ap.add_argument("--end", type=int, default=datetime.now().year)
    ap.add_argument("--mailto", help="your email, for OpenAlex's polite pool")
    ap.add_argument("--max-per-query", type=int, default=1000)
    ap.add_argument("--max-pages", type=int, default=3, help="OpenAlex pages (100 works each) per query")
    a = ap.parse_args(argv)
    OUT = Path(a.out)
    cmds = ["pdf", "wb", "projects", "dhs", "openalex", "zenodo"] if a.command == "all" else [a.command]
    for c in cmds:
        if c == "pdf":
            if not a.pdf:
                sys.exit("--pdf PATH is required for the pdf step")
            run_pdf(a.pdf)
        elif c == "wb":
            run_wb(a.countries, a.start, a.end)
        elif c == "projects":
            run_projects(a.max_per_query)
        elif c == "dhs":
            run_dhs(a.countries)
        elif c == "openalex":
            run_openalex(a.mailto, a.start, a.max_pages)
        elif c == "zenodo":
            run_zenodo()


if __name__ == "__main__":
    main()
