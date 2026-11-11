#!/usr/bin/env python3
"""
Fetch country-level EdTech-context indicators from the World Bank API (v2).

Many UNESCO UIS education series (teachers, pupil-teacher ratios, trained
teachers) are republished in the World Bank's WDI / Education Statistics, so
this gives one uniform, keyless route for every country. Countries and
indicators come from config.json (or --countries), nothing is hardcoded here.

Usage:
  python fetch_wb_indicators.py check                 # validate countries + indicator codes
  python fetch_wb_indicators.py fetch                 # download, write CSVs
  python fetch_wb_indicators.py fetch --countries KEN RWA --start 2015
  python fetch_wb_indicators.py fetch --config other.json --out data/

Outputs (in --out, default ./out):
  wb_long.csv        iso3, country, theme, indicator, indicator_name, year, value
  wb_latest.csv      latest non-null value per country x indicator
  wb_coverage.csv    obs count, first/last year, staleness per country x indicator
"""
import argparse
import csv
import datetime
import json
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

import store

API = "https://api.worldbank.org/v2"
UA = {"User-Agent": "edtech-ssa-fetch/0.1"}


def get_json(url, retries=4, pause=1.5):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last = e
            time.sleep(pause * (2 ** i))
    raise RuntimeError(f"Request failed after {retries} tries: {url}\n  {last}")


def load_config(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def flatten_indicators(cfg):
    """-> list of (theme, code, name)"""
    return [(theme, code, name)
            for theme, inds in cfg["indicators"].items()
            for code, name in inds.items()]


def validate_countries(codes):
    """Return {iso3: name}; raise if any code is unknown to the API."""
    url = f"{API}/country/{';'.join(codes)}?format=json&per_page=100"
    data = get_json(url)
    if not isinstance(data, list) or len(data) < 2 or not data[1]:
        raise SystemExit(f"Country lookup failed or empty: {data}")
    found = {c["id"]: c["name"] for c in data[1]}
    missing = [c for c in codes if c not in found]
    if missing:
        raise SystemExit(f"Unknown country codes (use ISO3): {missing}")
    return found


def indicator_exists(code):
    data = get_json(f"{API}/indicator/{code}?format=json")
    if isinstance(data, list) and len(data) > 1 and data[1]:
        meta = data[1][0]
        return True, meta.get("name", ""), (meta.get("source") or {}).get("value", "")
    return False, "", ""


def fetch_indicator(codes, indicator, start, end):
    rows, page = [], 1
    while True:
        url = (f"{API}/country/{';'.join(codes)}/indicator/{indicator}"
               f"?format=json&per_page=1000&page={page}&date={start}:{end}")
        data = get_json(url)
        if not isinstance(data, list) or len(data) < 2:
            msg = data[0].get("message") if data and isinstance(data[0], dict) else data
            print(f"  ! {indicator}: API returned {msg}", file=sys.stderr)
            return rows
        meta, recs = data[0], data[1] or []
        for r in recs:
            rows.append({
                "iso3": r.get("countryiso3code") or "",
                "country": (r.get("country") or {}).get("value", ""),
                "year": int(r["date"]),
                "value": r["value"],
            })
        if page >= int(meta.get("pages", 1)):
            return rows
        page += 1


def cmd_check(cfg, countries):
    names = validate_countries(countries)
    print("Countries OK:", ", ".join(f"{k} ({v})" for k, v in names.items()))
    bad = 0
    for theme, code, name in flatten_indicators(cfg):
        ok, real_name, source = indicator_exists(code)
        flag = "OK " if ok else "BAD"
        bad += not ok
        print(f"[{flag}] {code:22s} {theme:26s} -> {real_name or 'NOT FOUND'}"
              f"{'  [' + source + ']' if source else ''}")
    print(f"\n{bad} indicator code(s) not found." if bad else "\nAll indicator codes found.")


def cmd_fetch(cfg, countries, start, end, out, db=None):
    out.mkdir(parents=True, exist_ok=True)
    names = validate_countries(countries)
    long_rows = []
    for theme, code, name in flatten_indicators(cfg):
        print(f"Fetching {code} ({name})")
        for r in fetch_indicator(countries, code, start, end):
            long_rows.append({"iso3": r["iso3"], "country": r["country"], "theme": theme,
                              "indicator": code, "indicator_name": name,
                              "year": r["year"], "value": r["value"]})
        time.sleep(0.3)  # be polite

    cols = ["iso3", "country", "theme", "indicator", "indicator_name", "year", "value"]
    with open(out / "wb_long.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(sorted(long_rows, key=lambda r: (r["iso3"], r["indicator"], r["year"])))

    # Coverage + latest, built for every country x indicator (including ones with no data)
    obs = defaultdict(list)
    for r in long_rows:
        if r["value"] is not None:
            obs[(r["iso3"], r["indicator"])].append((r["year"], r["value"]))

    latest_rows, cov_rows = [], []
    for theme, code, name in flatten_indicators(cfg):
        for iso3, cname in names.items():
            pts = sorted(obs.get((iso3, code), []))
            if pts:
                ly, lv = pts[-1]
                latest_rows.append({"iso3": iso3, "country": cname, "theme": theme,
                                    "indicator": code, "year": ly, "value": lv})
            cov_rows.append({
                "iso3": iso3, "country": cname, "indicator": code, "n_obs": len(pts),
                "first_year": pts[0][0] if pts else "", "last_year": pts[-1][0] if pts else "",
                "years_stale": (end - pts[-1][0]) if pts else "",
            })

    with open(out / "wb_latest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["iso3", "country", "theme", "indicator", "year", "value"])
        w.writeheader()
        w.writerows(latest_rows)
    with open(out / "wb_coverage.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["iso3", "country", "indicator", "n_obs",
                                          "first_year", "last_year", "years_stale"])
        w.writeheader()
        w.writerows(cov_rows)

    if db:
        stats = store.upsert(db, "wb",
                             [{"iso3": x["iso3"], "indicator": x["indicator"], "label": x["indicator_name"],
                               "year": x["year"], "value": x["value"]} for x in long_rows],
                             "", {"countries": countries,
                                   "indicators": [c for _, c, _ in flatten_indicators(cfg)],
                                   "start": start, "end": end})
        print(f"Store {db}: {stats['new']} new, {stats['revised']} revised, {stats['unchanged']} unchanged, "
              f"{stats['missing']} missing from source")

    empty = [c for c in cov_rows if c["n_obs"] == 0]
    print(f"\nWrote {len(long_rows)} rows to {out}/")
    print(f"{len(empty)} of {len(cov_rows)} country x indicator pairs have NO data:")
    for c in empty:
        print(f"  - {c['iso3']} {c['indicator']}")
    old = [c for c in cov_rows if c["n_obs"] and c["years_stale"] >= 5]
    if old:
        print(f"{len(old)} pairs are 5+ years stale (see wb_coverage.csv); state this on the dashboard.")


def main():
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["check", "fetch"])
    ap.add_argument("--config", default=str(here / "indicators_config.json"))
    ap.add_argument("--countries", nargs="+", help="ISO3 codes; overrides config")
    ap.add_argument("--start", type=int, help="start year; overrides config")
    ap.add_argument("--end", type=int, default=datetime.date.today().year)
    ap.add_argument("--out", default="out")
    ap.add_argument("--db", default=None, help="SQLite history store (see store.py)")
    ap.add_argument("--history-years", type=int, help="window: fetch from (end - N) onward")
    a = ap.parse_args()

    cfg = load_config(a.config)
    countries = [c.upper() for c in (a.countries or cfg["countries"])]
    start = a.start or (a.end - a.history_years if a.history_years else cfg.get("start_year", 2010))

    if a.command == "check":
        cmd_check(cfg, countries)
    else:
        cmd_fetch(cfg, countries, start, a.end, Path(a.out), a.db)


if __name__ == "__main__":
    main()
