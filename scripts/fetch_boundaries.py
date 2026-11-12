#!/usr/bin/env python3
"""
Admin-1 boundaries (geoBoundaries) + a conservative crosswalk to M-Lab subdivision names.

Commands
  fetch    download one ADM1 GeoJSON per configured country, plus licence/attribution metadata
  match    build the crosswalk between M-Lab `subdivision1` names and boundary shapes

Matching rules (a wrong match is worse than a blank one)
  1. overrides.csv    your manual decisions always win ('shape_name' empty = "no shape exists")
  2. exact            identical strings
  3. normalised       same after lowercasing, removing accents/punctuation and words like
                      Region/County/State (also with spaces removed: North-Western = Northwestern)
  4. fuzzy            SUGGESTIONS ONLY by default. Needs a high score, a clear margin over the
                      runner-up (on both sides), mutual best match, and one name must not simply
                      contain the other ("Western" vs "Western North" is blocked).
                      Suggestions are written to suggested_overrides.csv; approve a line by
                      copying it into overrides.csv. `--accept-fuzzy` applies them for a quick preview
                      (marked match_type=fuzzy; keep applied=False rows off the final map).
  Matching is per country and one-to-one: a shape can be claimed by only one name.
  Anything else stays unmatched and is listed in review.csv. Count mismatches (M-Lab has a
  different number of regions than the boundary file) are flagged as possible splits/merges.

Config (config.json)
  "boundaries": {"release": "gbOpen", "adm": "ADM1", "simplified": true,
                 "name_field": "shapeName", "id_field": "shapeID",
                 "mlab_csv": "mlab/downloads_by_country_subdivision1.csv",
                 "fuzzy_threshold": 0.86, "fuzzy_margin": 0.08, "stop_tokens": [...]}

Outputs (in <out>/boundaries/)
  <ISO3>_ADM1.geojson, boundaries_meta.json       from `fetch`
  crosswalk.csv           one row per M-Lab name: shape, match_type, score, applied, note
  review.csv              everything that is not an exact/override match (look at this)
  suggested_overrides.csv fuzzy suggestions in overrides.csv format
  country_summary.csv     counts per country, shapes with no M-Lab data, count-mismatch flag
  overrides.csv           yours: country_code (ISO2), mlab_name, shape_name

Attribution: geoBoundaries data requires crediting the source; see boundaries_meta.json
(per-country licence and source). Individual files can carry different licences.
"""
import argparse
import csv
import datetime
import difflib
import json
import sys
import time
import unicodedata
import re
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

API = "https://www.geoboundaries.org/api/current/{release}/{iso3}/{adm}/"
WB_COUNTRY_API = "https://api.worldbank.org/v2/country"
UA = {"User-Agent": "edtech-ssa-fetch/0.1"}
DEFAULT_STOP = ["region", "province", "county", "state", "district", "city", "division", "prefecture",
                "department", "municipality", "governorate", "capital", "territory", "of", "the"]
WEAK_FLOOR = 0.6  # below this, don't even mention a candidate


# ----------------------------------------------------------------- network / countries
def fetch_bytes(url, retries=4, pause=1.5):
    last = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            time.sleep(pause * 2 ** i)
    raise RuntimeError(f"Failed after {retries} tries: {url}\n  {last}")


def country_pairs(codes, cache_path):
    """ISO3/ISO2 codes -> {iso3: iso2} using the shared cache (same file fetch_mlab.py uses)."""
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    inv = {v: k for k, v in cache.items()}
    out, need = {}, []
    for c in codes:
        if len(c) == 3 and c in cache:
            out[c] = cache[c]
        elif len(c) == 2 and c in inv:
            out[inv[c]] = c
        else:
            need.append(c)
    if need:
        data = json.loads(fetch_bytes(f"{WB_COUNTRY_API}/{';'.join(need)}?format=json&per_page=100"))
        recs = data[1] if isinstance(data, list) and len(data) > 1 and data[1] else []
        found = {r["id"]: r["iso2Code"] for r in recs}
        bad = [c for c in need if c not in found and c not in found.values()]
        if bad:
            sys.exit(f"Unknown country codes (use ISO3 or ISO2): {bad}")
        cache.update(found)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, indent=1))
        out.update(found)
    return {k: v.upper() for k, v in out.items() if k in codes or v in codes}


# ----------------------------------------------------------------- fetch
def cmd_fetch(cfg, pairs, out, refresh):
    bc = cfg.get("boundaries", {})
    release, adm = bc.get("release", "gbOpen"), bc.get("adm", "ADM1")
    simplified = bc.get("simplified", True)
    bdir = Path(out) / "boundaries"
    bdir.mkdir(parents=True, exist_ok=True)
    meta_path = bdir / "boundaries_meta.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    for iso3 in pairs:
        dest = bdir / f"{iso3}_{adm}.geojson"
        if dest.exists() and iso3 in meta and not refresh:
            print(f"{iso3}: already have {dest.name} (use --refresh to re-download)")
            continue
        try:
            info = json.loads(fetch_bytes(API.format(release=release, iso3=iso3, adm=adm)))
        except (RuntimeError, json.JSONDecodeError) as e:
            print(f"{iso3}: ! could not read boundary metadata: {e}", file=sys.stderr)
            continue
        if isinstance(info, list):
            info = info[0] if info else {}
        url = (info.get("simplifiedGeometryGeoJSON") if simplified else None) or info.get("gjDownloadURL")
        if not url:
            print(f"{iso3}: ! no {adm} download link in metadata (keys: {sorted(info)[:12]})", file=sys.stderr)
            continue
        raw = fetch_bytes(url)
        gj = json.loads(raw)
        if gj.get("type") != "FeatureCollection":
            print(f"{iso3}: ! downloaded file is not a FeatureCollection", file=sys.stderr)
            continue
        dest.write_bytes(raw)
        source = next((info[k] for k in info if k.lower().startswith("boundarysource") and info[k]), "")
        meta[iso3] = {"product": release, "adm": adm, "boundaryID": info.get("boundaryID"),
                      "year_represented": info.get("boundaryYearRepresented"),
                      "licence": info.get("boundaryLicense"), "licence_detail": info.get("licenseDetail"),
                      "licence_source": info.get("licenseSource"), "source": source,
                      "unit_count": info.get("admUnitCount"), "features": len(gj.get("features", [])),
                      "downloaded_from": url,
                      "retrieved": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}
        print(f"{iso3}: {len(gj.get('features', []))} shapes, licence: {meta[iso3]['licence']}")
    meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    print(f"\nMetadata (licences/sources) in {meta_path}. Credit geoBoundaries and the per-country sources.")


# ----------------------------------------------------------------- matching
class Norm:
    def __init__(self, stop):
        self.stop = set(s.lower() for s in stop)

    def tokens(self, s):
        s = unicodedata.normalize("NFKD", s)
        s = "".join(ch for ch in s if not unicodedata.combining(ch)).lower().replace("&", " and ")
        toks = re.sub(r"[^a-z0-9]+", " ", s).split()
        kept = [t for t in toks if t not in self.stop]
        return kept or toks

    def key(self, s):
        return " ".join(self.tokens(s))

    def compact(self, s):
        return "".join(self.tokens(s))


def load_shapes(path, name_field, id_field):
    gj = json.loads(Path(path).read_text(encoding="utf-8"))
    feats = gj.get("features", [])
    shapes = []
    for i, f in enumerate(feats):
        p = f.get("properties") or {}
        if p.get(name_field):
            shapes.append({"idx": len(shapes), "name": str(p[name_field]).strip(), "id": str(p.get(id_field) or i)})
    if feats and not shapes:
        sys.exit(f"{path}: no '{name_field}' property. Available: {sorted((feats[0].get('properties') or {}))}")
    return shapes


def match_country(cc, iso3, mnames, shapes, overrides, norm, thr, margin, accept_fuzzy):
    rows, claimed, amb = {}, {}, {}
    by_idx = {s["idx"]: s for s in shapes}

    def put(m, i, mtype, score=1.0, applied=True, note=""):
        s = by_idx[i] if i is not None else {"id": "", "name": ""}
        rows[m] = {"country_code": cc, "iso3": iso3, "mlab_name": m, "shape_id": s["id"], "shape_name": s["name"],
                   "match_type": mtype, "score": round(score, 3), "applied": applied, "note": note}
        if i is not None and (applied or mtype == "fuzzy_suggested"):
            claimed[i] = m

    # 1. overrides
    for m in mnames:
        if (cc, m) not in overrides:
            continue
        target = overrides[(cc, m)]
        if target == "":
            put(m, None, "no_shape", applied=False, note="override: no matching shape exists")
            continue
        hit = [s["idx"] for s in shapes if s["name"] == target]
        if hit:
            put(m, hit[0], "override")
        else:
            put(m, None, "unmatched", applied=False, note=f"override target '{target}' not found in boundary file")

    def remaining():
        return ([m for m in mnames if m not in rows], [s["idx"] for s in shapes if s["idx"] not in claimed])

    # 2-3. deterministic tiers
    def tier(keyfn, label):
        rm, rs = remaining()
        mk, sk = defaultdict(list), defaultdict(list)
        for m in rm:
            mk[keyfn(m)].append(m)
        for i in rs:
            sk[keyfn(by_idx[i]["name"])].append(i)
        for k, ms in mk.items():
            ss = sk.get(k, [])
            if not k or not ss:
                continue
            if len(ms) == 1 and len(ss) == 1:
                put(ms[0], ss[0], label)
            else:
                for m in ms:
                    amb[m] = f"ambiguous: {ms} vs shapes {[by_idx[i]['name'] for i in ss]}"

    tier(lambda x: x, "exact")
    tier(norm.key, "normalised")
    tier(norm.compact, "normalised")

    # 4. fuzzy (suggest; apply only if asked)
    rm, rs = remaining()
    cand = {m: sorted(((difflib.SequenceMatcher(None, norm.key(m), norm.key(by_idx[i]["name"])).ratio(), i)
                       for i in rs), reverse=True) for m in rm}
    rev = defaultdict(list)
    for m, sc in cand.items():
        for s_, i in sc:
            rev[i].append((s_, m))
    for i in rev:
        rev[i].sort(reverse=True)
    for m in rm:
        sc = cand[m]
        if not sc or sc[0][0] < WEAK_FLOOR:
            continue
        best, i = sc[0]
        second = sc[1][0] if len(sc) > 1 else 0.0
        rb = rev[i]
        rsecond = rb[1][0] if len(rb) > 1 else 0.0
        tm, ts = set(norm.tokens(m)), set(norm.tokens(by_idx[i]["name"]))
        sname = by_idx[i]["name"]
        if tm != ts and (tm < ts or ts < tm):
            put(m, None, "unmatched", best, False,
                note=f"blocked: '{m}' vs '{sname}' (one name contains the other; risk of a wrong match)")
        elif best >= thr and best - second >= margin and rb[0][1] == m and rb[0][0] - rsecond >= margin:
            put(m, i, "fuzzy" if accept_fuzzy else "fuzzy_suggested", best, accept_fuzzy,
                note="" if accept_fuzzy else "suggestion only; approve via overrides.csv")
        else:
            put(m, None, "unmatched", best, False, note=f"weak/ambiguous candidate: '{sname}' ({best:.2f})")

    # leftovers
    for m in mnames:
        if m in rows:
            continue
        note = amb.get(m, "")
        if not note:
            k = norm.key(m)
            owner = next((claimed[i] for i in claimed if norm.key(by_idx[i]["name"]) == k), None)
            note = f"same normalised name as '{owner}', which already owns that shape" if owner else "no candidate"
        put(m, None, "unmatched", 0.0, False, note=note)

    applied_ids = {r["shape_id"] for r in rows.values() if r["applied"]}
    counts = defaultdict(int)
    for r in rows.values():
        counts[r["match_type"]] += 1
    summary = {"country_code": cc, "iso3": iso3, "n_shapes": len(shapes), "n_mlab_names": len(mnames),
               **{f"n_{t}": counts.get(t, 0) for t in
                  ("exact", "normalised", "override", "fuzzy", "fuzzy_suggested", "no_shape", "unmatched")},
               "count_mismatch": len(shapes) != len(mnames),
               "shapes_without_data": "; ".join(s["name"] for s in shapes if s["id"] not in applied_ids)}
    return list(rows.values()), summary


def write_csv(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def cmd_match(cfg, pairs, out, mlab_csv, accept_fuzzy):
    bc = cfg.get("boundaries", {})
    adm, name_field, id_field = bc.get("adm", "ADM1"), bc.get("name_field", "shapeName"), bc.get("id_field", "shapeID")
    thr, margin = bc.get("fuzzy_threshold", 0.86), bc.get("fuzzy_margin", 0.08)
    norm = Norm(bc.get("stop_tokens", DEFAULT_STOP))
    bdir = Path(out) / "boundaries"
    bdir.mkdir(parents=True, exist_ok=True)

    csv_path = Path(mlab_csv or Path(out) / bc.get("mlab_csv", "mlab/downloads_by_country_subdivision1.csv"))
    if not csv_path.exists():
        sys.exit(f"M-Lab file not found: {csv_path}. Run fetch_mlab.py backfill (subdivision slice) first.")
    names, blank = defaultdict(set), 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            n = (r.get("subdivision1") or r.get("subdivision1_name") or "").strip()
            if n:
                names[(r.get("country_code") or "").upper()].add(n)
            else:
                blank += 1
    if blank:
        print(f"({blank} M-Lab rows have no subdivision name and are skipped)")

    ov_path = bdir / "overrides.csv"
    overrides = {}
    if ov_path.exists():
        with open(ov_path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                overrides[((r.get("country_code") or "").upper(), (r.get("mlab_name") or "").strip())] = \
                    (r.get("shape_name") or "").strip()
    else:
        write_csv(ov_path, ["country_code", "mlab_name", "shape_name", "note"], [])

    all_rows, summaries = [], []
    for iso3, iso2 in pairs.items():
        gpath = bdir / f"{iso3}_{adm}.geojson"
        if not gpath.exists():
            print(f"{iso3}: ! no boundary file (run `fetch`)", file=sys.stderr)
            continue
        mnames = sorted(names.get(iso2, []))
        if not mnames:
            print(f"{iso3}: ! no M-Lab subdivision rows for {iso2}", file=sys.stderr)
            continue
        rows, summ = match_country(iso2, iso3, mnames, load_shapes(gpath, name_field, id_field),
                                   overrides, norm, thr, margin, accept_fuzzy)
        all_rows += rows
        summaries.append(summ)

    cf = ["country_code", "iso3", "mlab_name", "shape_id", "shape_name", "match_type", "score", "applied", "note"]
    all_rows.sort(key=lambda r: (r["country_code"], r["match_type"], r["mlab_name"]))
    write_csv(bdir / "crosswalk.csv", cf, all_rows)
    write_csv(bdir / "review.csv", cf, [r for r in all_rows if r["match_type"] not in ("exact", "override")])
    write_csv(bdir / "suggested_overrides.csv", ["country_code", "mlab_name", "shape_name", "note"],
              [{"country_code": r["country_code"], "mlab_name": r["mlab_name"], "shape_name": r["shape_name"],
                "note": f"fuzzy score {r['score']}; copy into overrides.csv to approve"}
               for r in all_rows if r["match_type"] == "fuzzy_suggested"])
    sf = list(summaries[0]) if summaries else []
    write_csv(bdir / "country_summary.csv", sf, summaries)

    for s in summaries:
        print(f"\n{s['iso3']} ({s['country_code']}): {s['n_mlab_names']} M-Lab names, {s['n_shapes']} shapes -> "
              f"{s['n_exact']} exact, {s['n_normalised']} normalised, {s['n_override']} override, "
              f"{s['n_fuzzy'] + s['n_fuzzy_suggested']} fuzzy ({s['n_fuzzy_suggested']} awaiting approval), "
              f"{s['n_unmatched']} unmatched")
        if s["count_mismatch"]:
            print("  ! region counts differ: possible split/merge/renaming or regions with no tests")
        if s["shapes_without_data"]:
            print(f"  shapes with no M-Lab data (grey on map): {s['shapes_without_data']}")
    act = [r for r in all_rows if r["match_type"] in ("unmatched", "fuzzy_suggested", "fuzzy")]
    auto = sum(r["match_type"] == "normalised" for r in all_rows)
    print(f"\n{len(act)} names need a decision (unmatched / fuzzy), {auto} were matched automatically after "
          f"normalising. All listed in {bdir / 'review.csv'}")
    print("Map only rows with applied=True from crosswalk.csv.")


def main():
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["fetch", "match"])
    ap.add_argument("--config", default=str(here / "config.json"))
    ap.add_argument("--countries", nargs="+", help="ISO3/ISO2 codes; overrides config")
    ap.add_argument("--out", default="out")
    ap.add_argument("--refresh", action="store_true", help="fetch: re-download existing files")
    ap.add_argument("--mlab-csv", help="match: path to the M-Lab subdivision CSV")
    ap.add_argument("--accept-fuzzy", action="store_true", help="match: apply fuzzy suggestions (preview only)")
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    codes = [c.upper() for c in (a.countries or cfg["countries"])]
    pairs = country_pairs(codes, Path(a.out) / "mlab" / "iso2_map.json")
    if a.command == "fetch":
        cmd_fetch(cfg, pairs, a.out, a.refresh)
    else:
        cmd_match(cfg, pairs, a.out, a.mlab_csv, a.accept_fuzzy)


if __name__ == "__main__":
    main()
