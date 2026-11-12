#!/usr/bin/env python3
"""
Build the data bundle the admin-1 explorer (admin1_explorer.js) reads. Static files only,
so you can serve them from wherever your dashboard already lives (behind its login).

Inputs  (all produced by the other scripts in out/)
  boundaries/<ISO3>_ADM1.geojson, boundaries/crosswalk.csv (only applied=True rows are used)
  mlab/<slice>.csv                                    (see config "dashboard.sources")
Output  (default out/dashboard/)
  manifest.json            countries, metrics (labels/help), attribution, caveats, build time
  <ISO3>.geojson           simplified shapes (coordinates rounded), properties: shapeID, shapeName
  <ISO3>.series.json       per shape: metric arrays aligned to `periods`, sample counts, low-sample flags,
                           how the region was matched; plus national reference lines

Adding another admin-1 dataset (e.g. a survey, population, a poverty map)
  Put a CSV with columns  iso3, shape_id, value  (optional: year; the latest year is used) and list it
  under "dashboard.extra_layers" in config.json:
    {"id": "layer:literacy", "label": "Children who can read (%)", "unit": "%", "kind": "need",
     "csv": "layers/literacy_admin1.csv"}
  It then appears in the explorer's metric menus and can be paired with any other metric (bivariate map).
  Join on shape_id: run new datasets through the same name-matching step first so a wrong match can't slip in.

Usage
  python build_dashboard_data.py [--countries KEN GHA ...] [--out out] [--dest out/dashboard]
"""
import argparse
import csv
import datetime
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import fetch_boundaries as fb

DEFAULT_CAVEATS = [
    "Speeds come from voluntary internet speed tests by the general public, not from schools. "
    "They describe regions, not individual schools, and tests are not a random sample of users.",
    "Hatched regions have few tests (under the minimum sample size), so their figures are unreliable.",
    "Grey regions have no usable data this period, or could not be matched to a boundary with confidence.",
    "Region boundaries and names can change over time; a few regions may be matched approximately.",
]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else round(v, 4)


def truthy(x):
    return str(x).strip().lower() in ("true", "1", "1.0")


def round_coords(c, nd=4):
    if isinstance(c, (int, float)):
        return round(c, nd)
    return [round_coords(x, nd) for x in c]


def get_names(iso3s, cache_path):
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    need = [c for c in iso3s if c not in cache]
    if need:
        try:
            data = json.loads(fb.fetch_bytes(f"{fb.WB_COUNTRY_API}/{';'.join(need)}?format=json&per_page=100"))
            for r in data[1]:
                cache[r["id"]] = r["name"]
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(cache, indent=1, ensure_ascii=False))
        except Exception as e:  # names are cosmetic
            print(f"(could not fetch country names, using codes: {e})", file=sys.stderr)
    return {c: cache.get(c, c) for c in iso3s}


def load_sources(out, dc):
    src = {}
    for name, spec in dc["sources"].items():
        sub, nat = defaultdict(dict), defaultdict(dict)
        p = out / spec["subdivision_csv"]
        if p.exists():
            for r in read_csv(p):
                sub[((r.get("country_code") or "").upper(), (r.get("subdivision1") or "").strip())][r["period"]] = r
        else:
            print(f"! source '{name}': {p} not found", file=sys.stderr)
        if spec.get("country_csv") and (out / spec["country_csv"]).exists():
            for r in read_csv(out / spec["country_csv"]):
                nat[(r.get("country_code") or "").upper()][r["period"]] = r
        src[name] = (sub, nat)
    return src


def load_layers(out, dc):
    layers = {}
    for lay in dc.get("extra_layers", []):
        vals = {}
        for r in read_csv(out / lay["csv"]):
            key = (r["iso3"].upper(), str(r["shape_id"]))
            yr = num(r.get("year")) or 0
            if num(r.get("value")) is not None and (key not in vals or yr >= vals[key][0]):
                vals[key] = (yr, num(r["value"]))
        layers[lay["id"]] = {k: v[1] for k, v in vals.items()}
    return layers


def build(cfg, pairs, out, dest):
    dc = cfg.get("dashboard") or sys.exit("config.json needs a 'dashboard' section")
    bc = cfg.get("boundaries", {})
    adm, name_f, id_f = bc.get("adm", "ADM1"), bc.get("name_field", "shapeName"), bc.get("id_field", "shapeID")
    out, dest = Path(out), Path(dest)
    bdir = out / "boundaries"
    if not (bdir / "crosswalk.csv").exists():
        sys.exit("boundaries/crosswalk.csv missing: run fetch_boundaries.py fetch, then match")
    crosswalk = defaultdict(dict)
    for r in read_csv(bdir / "crosswalk.csv"):
        if truthy(r["applied"]):
            crosswalk[r["iso3"]][r["shape_id"]] = r

    src, layers = load_sources(out, dc), load_layers(out, dc)
    specs = dc["metrics"] + dc.get("extra_layers", [])
    dest.mkdir(parents=True, exist_ok=True)
    names = get_names(list(pairs), dest / "country_names.json")
    available, countries = set(), []

    for iso3, iso2 in pairs.items():
        gpath = bdir / f"{iso3}_{adm}.geojson"
        if not gpath.exists():
            print(f"{iso3}: ! no boundary file, skipped", file=sys.stderr)
            continue
        gj = json.loads(gpath.read_text(encoding="utf-8"))
        periods = sorted({per for sub, _ in src.values() for (cc, _n), d in sub.items() if cc == iso2 for per in d})
        feats, shapes, n_data = [], {}, 0
        for i, f in enumerate(gj.get("features", [])):
            p = f.get("properties") or {}
            if not p.get(name_f) or not f.get("geometry"):
                continue
            sid = str(p.get(id_f) or i)
            g = dict(f["geometry"])
            g["coordinates"] = round_coords(g["coordinates"])
            feats.append({"type": "Feature", "properties": {"shapeID": sid, "shapeName": p[name_f]}, "geometry": g})
            cw = crosswalk[iso3].get(sid)
            e = {"name": p[name_f], "match": cw["match_type"] if cw else None, "metrics": {}, "n": {}, "low": {}}
            if cw:
                for sname, (sub, _nat) in src.items():
                    rows = sub.get((iso2, cw["mlab_name"]), {})
                    if not rows:
                        continue
                    e["n"][sname] = [num(rows.get(per, {}).get("sample_count")) for per in periods]
                    e["low"][sname] = [1 if truthy(rows.get(per, {}).get("low_sample")) else 0 for per in periods]
                    for sp in dc["metrics"]:
                        if sp["source"] != sname:
                            continue
                        arr = [num(rows.get(per, {}).get(sp.get("column", sp["id"]))) for per in periods]
                        if any(v is not None for v in arr):
                            e["metrics"][sp["id"]] = arr
            for lid, vals in layers.items():
                if (iso3, sid) in vals:
                    e["metrics"][lid] = [vals[(iso3, sid)]]
            n_data += bool(e["metrics"])
            available.update(e["metrics"])
            shapes[sid] = e

        national = {}
        for sp in dc["metrics"]:
            nat = src.get(sp["source"], (None, {}))[1].get(iso2, {})
            arr = [num(nat.get(per, {}).get(sp.get("column", sp["id"]))) for per in periods]
            if any(v is not None for v in arr):
                national[sp["id"]] = arr
        series = {"iso3": iso3, "iso2": iso2, "periods": periods, "shapes": shapes, "national": national}
        (dest / f"{iso3}.geojson").write_text(
            json.dumps({"type": "FeatureCollection", "features": feats}, separators=(",", ":")), encoding="utf-8")
        (dest / f"{iso3}.series.json").write_text(json.dumps(series, separators=(",", ":"), ensure_ascii=False),
                                                  encoding="utf-8")
        countries.append({"iso3": iso3, "iso2": iso2, "name": names[iso3], "n_shapes": len(feats),
                          "n_with_data": n_data, "first_period": periods[0] if periods else None,
                          "last_period": periods[-1] if periods else None})
        print(f"{iso3}: {len(feats)} shapes, {n_data} with data, {len(periods)} periods")

    meta = json.loads((bdir / "boundaries_meta.json").read_text()) if (bdir / "boundaries_meta.json").exists() else {}
    keep = ("id", "label", "unit", "kind", "decimals", "help", "source", "higher_is_better")
    metrics = [{**{k: sp[k] for k in keep if k in sp}, "static": sp["id"].startswith("layer:")}
               for sp in specs if sp["id"] in available]
    manifest = {"built": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                "countries": countries, "metrics": metrics,
                "caveats": dc.get("caveats", DEFAULT_CAVEATS),
                "attribution": dc.get("attribution", ["Internet speed data: Measurement Lab (M-Lab) NDT tests.",
                                                      "Boundaries: geoBoundaries (William & Mary geoLab)."]),
                "boundary_licences": {k: {"licence": v.get("licence"), "source": v.get("source")}
                                      for k, v in meta.items() if k in pairs}}
    (dest / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote bundle to {dest} ({len(metrics)} metrics). Serve this folder to admin1_explorer.js.")


def main():
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=str(here / "config.json"))
    ap.add_argument("--countries", nargs="+")
    ap.add_argument("--out", default="out")
    ap.add_argument("--dest")
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    codes = [c.upper() for c in (a.countries or cfg["countries"])]
    pairs = fb.country_pairs(codes, Path(a.out) / "mlab" / "iso2_map.json")
    build(cfg, pairs, a.out, a.dest or Path(a.out) / "dashboard")


if __name__ == "__main__":
    main()
