#!/usr/bin/env python3
"""
Fetch UNESCO UIS indicators straight from the UIS public API (no key needed).
Countries come from config.json (ISO3) or --countries; nothing is hardcoded.

UIS indicator codes are not guessable, so config.json lists each wanted series
under "uis_indicators" by *name keywords*; the script resolves them to codes
against the live catalogue and reports anything missing or ambiguous. Once you
are happy, pin the code in config.json ("code": "...") for reproducibility.

Commands:
  version                         show default data version
  find <words...>                 search the indicator catalogue by name
  probe <CODE> <ISO3>             print the raw API response for one call (check field names)
  resolve                         map config entries -> UIS codes, write uis_resolution.csv
  fetch                           resolve + download + write CSVs and meta.json
  update                          like fetch, but only the recent window, and only if the UIS data
                                  version / your countries / indicators changed; upserts into --db

Examples:
  python fetch_uis.py find trained teachers primary
  python fetch_uis.py fetch --countries KEN RWA --start 2015
  python fetch_uis.py fetch --api-version 20260507-91260335   # pin a data version
  python fetch_uis.py fetch --db edtech.db --history-years 10 # keep a 10-year window in the store
  python fetch_uis.py update --db edtech.db                   # scheduled job: cheap no-op if unchanged

Outputs (in --out, default ./out):
  uis_long.csv, uis_latest.csv, uis_coverage.csv, uis_resolution.csv,
  uis_indicator_catalogue.json, uis_meta.json
"""
import argparse
import csv
import datetime
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

import store

BASE = "https://api.uis.unesco.org/api/public"
UA = {"User-Agent": "edtech-ssa-fetch/0.1", "Accept": "application/json"}

CODE_KEYS = ("indicatorCode", "indicatorId", "code", "id")
NAME_KEYS = ("name", "indicatorName", "label", "title")
GEO_CODE_KEYS = ("geoUnit", "geoUnitCode", "code", "id")
GEO_NAME_KEYS = ("name", "geoUnitName", "label")


class TooMuchData(Exception):
    pass


# ----------------------------------------------------------------- HTTP / parsing
def get_json(path, params=None, retries=4, pause=1.5):
    url = BASE + path
    if params:
        clean = {k: v for k, v in params.items() if v is not None}
        url += "?" + urllib.parse.urlencode(clean, doseq=True)
    last = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:500]
            if e.code == 400 and "too much data" in body.lower():
                raise TooMuchData(body)
            if e.code in (429, 502, 503, 504):
                last = f"HTTP {e.code}"
                time.sleep(pause * 2 ** i)
                continue
            raise RuntimeError(f"HTTP {e.code} for {url}\n  {body}")
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last = e
            time.sleep(pause * 2 ** i)
    raise RuntimeError(f"Failed after {retries} tries: {url}\n  {last}")


def as_list(x, prefer=("records", "items", "data", "results")):
    """API payloads may be a bare list or a dict wrapping one; be tolerant."""
    if isinstance(x, list):
        return x
    if isinstance(x, dict):
        for k in prefer:
            if isinstance(x.get(k), list):
                return x[k]
        for v in x.values():
            if isinstance(v, list):
                return v
    return []


def pick(d, keys):
    for k in keys:
        v = d.get(k)
        if v not in (None, ""):
            if isinstance(v, dict):
                v = v.get("en") or next(iter(v.values()), None)
            return v
    return None


# ----------------------------------------------------------------- catalogue
def load_catalogue(version, out):
    raw = as_list(get_json("/definitions/indicators", {"version": version}))
    cat = []
    for r in raw:
        code, name = pick(r, CODE_KEYS), pick(r, NAME_KEYS)
        if code:
            cat.append({"code": str(code), "name": str(name or "")})
    if raw and not cat:
        sys.exit("Indicator catalogue returned records but I couldn't find code/name fields.\n"
                 f"First record: {json.dumps(raw[0])[:400]}\nAdjust CODE_KEYS/NAME_KEYS.")
    out.mkdir(parents=True, exist_ok=True)
    (out / "uis_indicator_catalogue.json").write_text(json.dumps(cat, indent=1), encoding="utf-8")
    return cat


def load_geounits(version):
    raw = as_list(get_json("/definitions/geounits", {"version": version}))
    return {str(pick(r, GEO_CODE_KEYS)): str(pick(r, GEO_NAME_KEYS) or "")
            for r in raw if pick(r, GEO_CODE_KEYS)}


def matches(name, terms, exclude=()):
    n = name.lower()
    return all(t.lower() in n for t in terms) and not any(x.lower() in n for x in exclude)


def resolve_entries(cfg, catalogue):
    by_code = {c["code"]: c["name"] for c in catalogue}
    rows = []
    for theme, entries in cfg["uis_indicators"].items():
        for e in entries:
            label = e["label"]
            if e.get("code"):
                ok = e["code"] in by_code
                rows.append({"theme": theme, "label": label, "code": e["code"],
                             "name": by_code.get(e["code"], ""),
                             "status": "pinned" if ok else "pinned-NOT-IN-CATALOGUE", "candidates": ""})
                continue
            cands = [c for c in catalogue if matches(c["name"], e.get("match", []), e.get("exclude", []))]
            narrowed = cands
            for pref in e.get("prefer", ["both sexes"]):
                sub = [c for c in narrowed if pref.lower() in c["name"].lower()]
                if len(narrowed) > 1 and len(sub) == 1:
                    narrowed = sub
            if len(narrowed) == 1:
                rows.append({"theme": theme, "label": label, "code": narrowed[0]["code"],
                             "name": narrowed[0]["name"],
                             "status": "auto-resolved" if len(cands) == 1 else "auto-resolved(prefer)",
                             "candidates": ""})
            else:
                status = "NOT FOUND" if not cands else "AMBIGUOUS"
                shown = " | ".join(f'{c["code"]}: {c["name"]}' for c in cands[:8])
                rows.append({"theme": theme, "label": label, "code": "", "name": "",
                             "status": status, "candidates": shown + (" ..." if len(cands) > 8 else "")})
    return rows


def print_resolution(rows):
    for r in rows:
        mark = "OK " if r["code"] and "NOT" not in r["status"] else "!! "
        print(f'{mark}{r["theme"]:24s} {r["label"][:46]:46s} {r["code"]:14s} {r["status"]}')
        if r["name"]:
            print(f'      {r["name"]}')
        if r["candidates"]:
            print(f'      candidates: {r["candidates"]}')


# ----------------------------------------------------------------- data
def fetch_code(code, countries, start, end, version, footnotes):
    params = {"indicator": code, "geoUnit": countries, "start": start, "end": end,
              "footnotes": "true" if footnotes else "false", "indicatorMetadata": "false",
              "version": version}
    try:
        return as_list(get_json("/data/indicators", params), prefer=("records",))
    except TooMuchData:
        if len(countries) == 1:
            raise
        mid = len(countries) // 2  # split and retry
        return (fetch_code(code, countries[:mid], start, end, version, footnotes)
                + fetch_code(code, countries[mid:], start, end, version, footnotes))


def to_row(rec, theme, label, code, name, geonames):
    iso3 = str(rec.get("geoUnit") or rec.get("geoUnitId") or "")
    known = {"indicatorId", "geoUnit", "geoUnitId", "year", "value"}
    extra = {k: v for k, v in rec.items() if k not in known and v not in (None, "", [])}
    return {"iso3": iso3, "country": geonames.get(iso3, ""), "theme": theme, "label": label,
            "indicator_code": code, "indicator_name": name, "year": rec.get("year"),
            "value": rec.get("value"), "extra": json.dumps(extra, ensure_ascii=False) if extra else ""}


def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


# ----------------------------------------------------------------- commands
def cmd_fetch(cfg, countries, start, end, version, footnotes, out, db=None, skip_if_current=False):
    out.mkdir(parents=True, exist_ok=True)
    geonames = load_geounits(version)
    if geonames:
        bad = [c for c in countries if c not in geonames]
        if bad:
            sys.exit(f"Not UIS geo units (use ISO3): {bad}")
    else:
        print("  (could not read geo-unit list; skipping country validation)", file=sys.stderr)

    catalogue = load_catalogue(version, out)
    res = resolve_entries(cfg, catalogue)
    write_csv(out / "uis_resolution.csv", ["theme", "label", "code", "name", "status", "candidates"], res)
    print_resolution(res)
    todo = [r for r in res if r["code"] and "NOT-IN" not in r["status"]]
    skipped = [r for r in res if r not in todo]
    if not todo:
        sys.exit("\nNothing resolved. Use `find` to locate codes, then pin them in config.json.")

    try:
        default_version = get_json("/versions/default")
    except Exception as e:  # provenance only
        default_version = f"unavailable: {e}"
    data_version = version or json.dumps(default_version, sort_keys=True)
    codes = [r["code"] for r in todo]
    if db and skip_if_current:
        prev = store.last_run(db, "uis")
        sc = (prev or {}).get("scope", {})
        if (prev and prev["data_version"] == data_version and set(countries) <= set(sc.get("countries", []))
                and set(codes) <= set(sc.get("indicators", [])) and start >= sc.get("start", 9999)):
            print("\nUp to date: same UIS data version, countries and indicators as the last run. Nothing fetched.")
            return
        print("\nChange detected (new data version, country, indicator or wider window): refetching window.")

    long_rows = []
    for r in todo:
        print(f'\nFetching {r["code"]}  ({r["label"]})')
        recs = fetch_code(r["code"], countries, start, end, version, footnotes)
        for rec in recs:
            long_rows.append(to_row(rec, r["theme"], r["label"], r["code"], r["name"], geonames))
        print(f"  {len(recs)} records")
        time.sleep(0.2)

    cols = ["iso3", "country", "theme", "label", "indicator_code", "indicator_name", "year", "value", "extra"]
    long_rows.sort(key=lambda x: (x["iso3"], x["indicator_code"], x["year"] or 0))
    write_csv(out / "uis_long.csv", cols, long_rows)

    obs = defaultdict(list)
    for r in long_rows:
        if r["value"] is not None and r["year"] is not None:
            obs[(r["iso3"], r["indicator_code"])].append((int(r["year"]), r["value"]))
    latest, cov = [], []
    for r in todo:
        for iso3 in countries:
            pts = sorted(obs.get((iso3, r["code"]), []))
            if pts:
                latest.append({"iso3": iso3, "country": geonames.get(iso3, ""), "theme": r["theme"],
                               "label": r["label"], "indicator_code": r["code"],
                               "year": pts[-1][0], "value": pts[-1][1]})
            cov.append({"iso3": iso3, "label": r["label"], "indicator_code": r["code"], "n_obs": len(pts),
                        "first_year": pts[0][0] if pts else "", "last_year": pts[-1][0] if pts else "",
                        "years_stale": end - pts[-1][0] if pts else ""})
    write_csv(out / "uis_latest.csv", ["iso3", "country", "theme", "label", "indicator_code", "year", "value"], latest)
    write_csv(out / "uis_coverage.csv", ["iso3", "label", "indicator_code", "n_obs", "first_year",
                                         "last_year", "years_stale"], cov)

    if db:
        stats = store.upsert(db, "uis",
                             [{"iso3": x["iso3"], "indicator": x["indicator_code"], "label": x["label"],
                               "year": x["year"], "value": x["value"]} for x in long_rows],
                             data_version, {"countries": countries, "indicators": codes, "start": start, "end": end})
        print(f"Store {db}: {stats['new']} new, {stats['revised']} revised, {stats['unchanged']} unchanged, "
              f"{stats['missing']} missing from source")
    meta = {"retrieved": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "requested_version": version, "default_version_at_retrieval": default_version,
            "countries": countries, "start": start, "end": end, "n_rows": len(long_rows),
            "source": "UNESCO Institute for Statistics (UIS), https://api.uis.unesco.org/api/public",
            "note": "Check UIS terms and conditions for licence/attribution before publishing."}
    (out / "uis_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")

    empty = [c for c in cov if c["n_obs"] == 0]
    print(f"\nWrote {len(long_rows)} rows to {out}/")
    if skipped:
        print(f"{len(skipped)} config entries NOT fetched (ambiguous / not found); see uis_resolution.csv")
    print(f"{len(empty)} of {len(cov)} country x indicator pairs have NO data")
    for c in empty:
        print(f'  - {c["iso3"]}  {c["label"]}')
    stale = [c for c in cov if c["n_obs"] and c["years_stale"] >= 5]
    if stale:
        print(f"{len(stale)} pairs are 5+ years old (uis_coverage.csv); say so on the dashboard.")


def main():
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["version", "find", "probe", "resolve", "fetch", "update"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--config", default=str(here / "indicators_config.json"))
    ap.add_argument("--countries", nargs="+", help="ISO3 codes; overrides config")
    ap.add_argument("--start", type=int)
    ap.add_argument("--end", type=int, default=datetime.date.today().year)
    ap.add_argument("--out", default="out")
    ap.add_argument("--api-version", default=None, help="pin a UIS data version (default: API default)")
    ap.add_argument("--db", default=None, help="SQLite history store (see store.py)")
    ap.add_argument("--history-years", type=int, help="window: fetch from (end - N) onward")
    ap.add_argument("--force", action="store_true", help="with update: refetch even if nothing changed")
    ap.add_argument("--footnotes", action="store_true", help="request per-datapoint footnotes (larger)")
    a = ap.parse_args()
    out = Path(a.out)

    if a.command == "version":
        print(json.dumps(get_json("/versions/default"), indent=1))
        return
    if a.command == "find":
        if not a.args:
            sys.exit("usage: find <words...>")
        for c in load_catalogue(a.api_version, out):
            if matches(c["name"], a.args):
                print(f'{c["code"]:16s} {c["name"]}')
        return
    if a.command == "probe":
        if len(a.args) != 2:
            sys.exit("usage: probe <INDICATOR_CODE> <ISO3>")
        resp = get_json("/data/indicators", {"indicator": a.args[0], "geoUnit": a.args[1],
                                             "footnotes": "false", "indicatorMetadata": "false",
                                             "version": a.api_version})
        print(json.dumps(resp, indent=1, ensure_ascii=False)[:3500])
        return

    with open(a.config, encoding="utf-8") as f:
        cfg = json.load(f)
    countries = [c.upper() for c in (a.countries or cfg["countries"])]
    hist = a.history_years or (cfg.get("history_years", 10) if a.command == "update" else None)
    start = a.start or (a.end - hist if hist else cfg.get("start_year", 2010))

    if a.command == "resolve":
        res = resolve_entries(cfg, load_catalogue(a.api_version, out))
        write_csv(out / "uis_resolution.csv", ["theme", "label", "code", "name", "status", "candidates"], res)
        print_resolution(res)
    else:
        if a.command == "update" and not a.db:
            sys.exit("update needs --db")
        cmd_fetch(cfg, countries, start, a.end, a.api_version, a.footnotes, out, a.db,
                  skip_if_current=(a.command == "update" and not a.force))


if __name__ == "__main__":
    main()
