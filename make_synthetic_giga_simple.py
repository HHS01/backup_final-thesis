#!/usr/bin/env python3
"""
Synthetic Giga-Maps data generator (offline version).

Generates:
  - <ISO3>_schools.csv
  - <ISO3>_measurements.csv
  - giga_region_summary.csv
  - giga_synthetic_meta.json
  - preview.png (optional, requires matplotlib)

Only the Python standard library + numpy are required.
"""

import argparse
import csv
import datetime
import json
import math
import os
import sys
import uuid
from pathlib import Path
from typing import List, Tuple

import numpy as np

# ---------------------------------------------------------------------------
#  Mapping from internal field names to the output column names required by the
#  downstream dashboard.  Adjust this dict once the real Giga API is available.
# ---------------------------------------------------------------------------
FIELD_MAP = {
    "school_id": "school_id_giga",
    "gov_id": "school_id_govt",
    "name": "school_name",
    "iso3": "country_iso3",
    "admin1": "admin1",
    "lat": "latitude",
    "lon": "longitude",
    "level": "education_level",
    "students": "num_students",
    "teachers": "num_teachers",
    "computers": "num_computers",
    "electricity": "electricity_availability",
    "coverage": "cellular_coverage_type",
    "tower_km": "nearest_tower_km",
    "fiber_km": "fiber_node_km",
    "tech": "connectivity_type_govt",
    "contracted": "download_speed_contracted",
    "conn_govt": "connectivity_govt",
    "has_meter": "giga_meter_installed",
    "status": "connectivity_status",
    "synthetic": "synthetic",
    "date": "date",
    "download": "download_speed",
    "upload": "upload_speed",
    "latency": "latency",
    "uptime": "uptime_pct",
    "n_tests": "n_tests",
}

TECHS = ["Fibre", "4G/LTE", "3G", "Satellite", "No connection"]
DL_MEDIAN = {"Fibre": 40.0, "4G/LTE": 12.0, "3G": 3.0, "Satellite": 6.0}
UL_RATIO = {"Fibre": 0.8, "4G/LTE": 0.3, "3G": 0.25, "Satellite": 0.15}
LAT_MEDIAN = {"Fibre": 15.0, "4G/LTE": 55.0, "3G": 120.0, "Satellite": 620.0}
COVER = {"city": [0.80, 0.18, 0.02, 0.0], "town": [0.55, 0.30, 0.13, 0.02], "village": [0.25, 0.30, 0.25, 0.20]}
COVER_TYPES = ["4G", "3G", "2G", "No coverage"]
ELEC_P = {"city": 0.97, "town": 0.88, "village": 0.55}
URBAN = {"city": 0.9, "town": 0.6, "village": 0.2}

# ---------------------------------------------------------------------------
#  Geometry helpers (pure Python – no external libs)
# ---------------------------------------------------------------------------
def polys_of(g):
    if not g:
        return []
    if g["type"] == "Polygon":
        return [g["coordinates"]]
    if g["type"] == "MultiPolygon":
        return g["coordinates"]
    return []

def in_ring(x, y, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-300) + xi:
            inside = not inside
        j = i
    return inside

def inside(x, y, polys):
    return any(in_ring(x, y, p[0]) and not any(in_ring(x, y, h) for h in p[1:]) for p in polys)

def bbox_area(polys) -> Tuple[float, float, float, float]:
    xs = [pt[0] for p in polys for pt in p[0]]
    ys = [pt[1] for p in polys for pt in p[0]]
    return min(xs), min(ys), max(xs), max(ys)

def ring_area(ring):
    return abs(
        sum(
            ring[i][0] * ring[(i + 1) % len(ring)][1]
            - ring[(i + 1) % len(ring)][0] * ring[i][1]
            for i in range(len(ring))
        )
    ) / 2

def sample_inside(rng, polys, box, tries=4000):
    x0, y0, x1, y1 = box
    for _ in range(tries):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if inside(x, y, polys):
            return x, y
    return (x0 + x1) / 2, (y0 + y1) / 2

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# ---------------------------------------------------------------------------
#  Synthetic data generators
# ---------------------------------------------------------------------------
def make_country(rng, iso3, regions, n_schools, days, meter_rate):
    country_quality = rng.lognormal(0, 0.30)
    weights = np.array(
        [math.sqrt(r["area"]) * rng.lognormal(0, 0.35) for r in regions]
    )
    counts = np.maximum(
        3,
        np.round(weights / weights.sum() * n_schools).astype(int),
    )
    rows = []
    school_counter = 0
    for region, target_cnt in zip(regions, counts):
        region_quality = rng.lognormal(0, 0.35)
        q = math.log(country_quality * region_quality)
        box = region["box"]
        ext = max(box[2] - box[0], box[3] - box[1])
        n_settlements = int(rng.integers(5, 12))
        settlement_types = ["city"] + ["town"] * max(1, n_settlements // 4) + ["village"] * n_settlements
        settlement_types = settlement_types[: n_settlements + 1]
        centroids = [sample_inside(rng, region["polys"], box) for _ in settlement_types]
        settlement_weights = np.array(
            [
                {"city": 6, "town": 2, "village": 1}[t]
                * rng.lognormal(0, 0.5)
                for t in settlement_types
            ]
        )
        for _ in range(target_cnt):
            st_idx = rng.choice(len(settlement_types), p=settlement_weights / settlement_weights.sum())
            stype = settlement_types[st_idx]
            cx, cy = centroids[st_idx]
            for _ in range(30):
                x = cx + rng.normal(0, 0.03 * ext if stype == "city" else 0.06 * ext if stype == "town" else 0.10 * ext)
                y = cy + rng.normal(0, 0.03 * ext if stype == "city" else 0.06 * ext if stype == "town" else 0.10 * ext)
                if inside(x, y, region["polys"]):
                    break
            else:
                x, y = cx, cy
            school_counter += 1
            level = rng.choice(["Primary", "Secondary", "Pre-Primary"], p=[0.65, 0.25, 0.10])
            student_base = {"Primary": 300, "Secondary": 450, "Pre-Primary": 80}[level]
            students = int(max(15, rng.lognormal(math.log(student_base), 0.5)))
            ptr = rng.lognormal(math.log(32 if level == "Secondary" else 40), 0.25)
            ptr *= 1.25 if stype == "village" else 1.0
            teachers = max(1, round(students / ptr))
            elec_prob = sigmoid(math.log(ELEC_P[stype] / (1 - ELEC_P[stype])) + 0.6 * q)
            electricity = rng.random() < elec_prob
            cov = str(rng.choice(COVER_TYPES, p=COVER[stype]))
            urban_factor = URBAN[stype] + rng.normal(0, 0.1)
            allowed = {"No connection": 0.0, "Satellite": -0.6 - 0.8 * urban_factor - 0.3 * q}
            if cov in ("4G", "3G"):
                allowed["3G"] = 0.4 + 0.2 * q
            if cov == "4G":
                allowed["4G/LTE"] = 0.1 + 1.4 * urban_factor + 0.5 * q
            if stype in ("city", "town"):
                allowed["Fibre"] = -1.6 + 2.6 * urban_factor + q
            allowed["No connection"] = 1.1 * (1 - urban_factor) - 0.8 * q - 0.1
            probs = np.exp(list(allowed.values()))
            probs = probs / probs.sum()
            tech = str(rng.choice(list(allowed.keys()), p=probs))
            gov_conn = "Yes" if (tech != "No connection" and rng.random() < 0.92) or (tech == "No connection" and rng.random() < 0.06) else "No"
            contracted = (
                float(
                    rng.choice(
                        [2, 5, 10, 20, 50, 100],
                        p=[0.2, 0.25, 0.25, 0.15, 0.1, 0.05],
                    )
                )
                if tech != "No connection"
                else np.nan
            )
            has_meter = tech != "No connection" and electricity and rng.random() < meter_rate
            rows.append({
                "school_id": str(uuid.UUID(bytes=rng.bytes(16), version=4)),
                "gov_id": f"{iso3}{school_counter:06d}",
                "name": f"Demo {level} School {school_counter:04d}",
                "iso3": iso3,
                "admin1": region["name"],
                "lat": y,
                "lon": x,
                "level": level,
                "students": students,
                "teachers": int(teachers),
                "computers": int(rng.poisson(8 if (electricity and tech != "No connection") else 0.8)),
                "electricity": electricity,
                "coverage": cov,
                "tower_km": round(float(rng.lognormal({"city": -0.2, "town": 1.0, "village": 2.0}[stype], 0.6)), 1),
                "fiber_km": round(float(rng.lognormal({"city": 1.5, "town": 3.0, "village": 4.2}[stype], 0.6)), 1),
                "tech": tech,
                "contracted": contracted,
                "conn_govt": gov_conn,
                "has_meter": has_meter,
                "base_dl": DL_MEDIAN.get(tech, 0) * rng.lognormal(0, 0.55) * (rng.uniform(0.1, 0.4) if rng.random() < 0.15 else 1.0),
                "install_day": int(rng.integers(0, max(1, days - 14))),
            })
    return rows

def make_measurements(rng, schools, days, end_date):
    date_range = [
        (datetime.date.fromisoformat(end_date) - datetime.timedelta(days=i)).isoformat()
        for i in reversed(range(days))
    ]
    weekday_factor = np.where(
        [datetime.datetime.fromisoformat(d).weekday() < 5 for d in date_range], 0.9, 1.0
    )
    out = []
    for s in schools:
        if not s["has_meter"]:
            continue
        t0 = s["install_day"]
        n = days - t0
        if n < 5:
            continue
        ar = np.zeros(n)
        for i in range(1, n):
            ar[i] = 0.97 * ar[i - 1] + rng.normal(0, 0.04)
        f = np.exp(ar) * weekday_factor[t0:]
        for _ in range(rng.poisson(n / 60)):
            a = int(rng.integers(0, n))
            f[a : a + int(rng.integers(3, 11))] *= rng.uniform(0.2, 0.6)
        outage_prob = rng.uniform(0.01, 0.04) * (1.5 if s["tech"] == "Satellite" else 1.0)
        outage = rng.random(n) < outage_prob
        k = rng.choice([1, 2, 3, 4], size=n, p=[.1, .15, .25, .5])
        dl = s["base_dl"] * f * rng.lognormal(0, 0.22, n)
        ul = dl * UL_RATIO[s["tech"]] * rng.lognormal(0, 0.2, n)
        lat = LAT_MEDIAN[s["tech"]] * rng.lognormal(0, 0.25, n) / np.sqrt(f.clip(0.3, 2))
        up = np.where(outage, rng.uniform(0, 60, n), 100 - rng.exponential(0.8, n)).clip(0, 100)
        dl = np.where(outage, np.nan, dl)
        ul = np.where(outage, np.nan, ul)
        keep = rng.random(n) > 0.05
        for i, keep_row in enumerate(keep):
            if not keep_row:
                continue
            out.append({
                "school_id": s["school_id"],
                "date": date_range[t0 + i],
                "download": dl[i],
                "upload": ul[i],
                "latency": np.where(outage, np.nan, lat)[i],
                "uptime": up[i],
                "n_tests": k[i],
            })
    return out

def compute_status(schools, measurements, benchmark):
    recent_cutoff = None
    if measurements:
        recent_cutoff = datetime.date.fromisoformat(measurements[-1]["date"]) - datetime.timedelta(days=30)
    recent = [m for m in measurements if recent_cutoff and datetime.date.fromisoformat(m["date"]) > recent_cutoff]
    med_by_school = {}
    for sid, recs in group_by(recent, key=lambda r: r["school_id"]).items():
        dl_vals = [r["download"] for r in recs if r["download"] is not None]
        med_by_school[sid] = np.median(dl_vals) if dl_vals else None
    for s in schools:
        med = med_by_school.get(s["school_id"])
        if med is None:
            s["status"] = "unknown"
        elif med >= benchmark:
            s["status"] = "good"
        elif med >= 1.0:
            s["status"] = "moderate"
        else:
            s["status"] = "no"
    return schools

def group_by(seq, key):
    d = {}
    for item in seq:
        k = key(item)
        d.setdefault(k, []).append(item)
    return d

def inject_quirks(rng, schools):
    n = len(schools)
    log = {}
    idx = rng.choice(n, size=max(1, int(0.01 * n)), replace=False)
    for i in idx:
        schools[i]["lat"] = None
        schools[i]["lon"] = None
    log["missing_coordinates"] = len(idx)
    idx = rng.choice(n, size=max(1, int(0.005 * n)), replace=False)
    for i in idx:
        # swap lat/lon to simulate a common data-entry error
        schools[i]["lat"], schools[i]["lon"] = schools[i]["lon"], schools[i]["lat"]
    log["swapped_lat_lon"] = len(idx)
    idx = rng.choice(n, size=max(1, int(0.003 * n)), replace=False)
    for i in idx:
        schools[i]["lat"] = 0.0
        schools[i]["lon"] = 0.0
    log["zero_coordinates"] = len(idx)
    idx = rng.choice(n, size=max(1, int(0.02 * n)), replace=False)
    if len(idx) > 1:
        name_source = schools[idx[0]]["name"]
        for i in idx[1:]:
            schools[i]["name"] = name_source
    log["duplicated_names"] = len(idx) - 1
    for s in schools:
        if rng.random() < 0.12:
            variant = int(rng.integers(4))
            s["admin1"] = [s["admin1"].upper(), s["admin1"] + " Region", s["admin1"] + " County", s["admin1"] + " Province"][variant]
    log["admin1_name_variants"] = int(sum(1 for s in schools if rng.random() < 0.12))
    return schools, log

def summarise(schools, measurements, benchmark, min_n):
    recent_cutoff = None
    if measurements:
        recent_cutoff = datetime.date.fromisoformat(measurements[-1]["date"]) - datetime.timedelta(days=30)
    recent = [m for m in measurements if recent_cutoff and datetime.date.fromisoformat(m["date"]) > recent_cutoff]
    med_by_school = {}
    for sid, recs in group_by(recent, key=lambda r: r["school_id"]).items():
        dl_vals = [r["download"] for r in recs if r["download"] is not None]
        med_by_school[sid] = np.median(dl_vals) if dl_vals else None
    rows = []
    for (iso3, admin), group in group_by(schools, key=lambda s: (s["iso3"], s["admin1"])) .items():
        n_schools = len(group)
        n_metered = sum(1 for s in group if s["has_meter"])
        reported_connected = sum(1 for s in group if s["conn_govt"] == "Yes")
        metric = [med_by_school.get(s["school_id"]) for s in group if s["has_meter"] and med_by_school.get(s["school_id"]) is not None]
        suppressed = len(metric) < min_n
        if not suppressed and metric:
            median_dl = round(float(np.median(metric)), 2)
            p25_dl = round(float(np.percentile(metric, 25)), 2)
            below_1 = round(float(np.mean(np.array(metric) < 1.0)), 3)
            meet_thr = round(float(np.mean(np.array(metric) >= benchmark)), 3)
            relevant_ids = {s["school_id"] for s in group if s["has_meter"] and med_by_school.get(s["school_id"]) is not None}
            lat_vals = [m["latency"] for m in measurements if m["school_id"] in relevant_ids and m["latency"] is not None]
            up_vals = [m["uptime"] for m in measurements if m["school_id"] in relevant_ids and m["uptime"] is not None]
            median_latency = round(float(np.median(lat_vals)), 1) if lat_vals else None
            mean_uptime = round(float(np.mean(up_vals)), 1) if up_vals else None
            conn_under_1 = sum(1 for s in group if s["conn_govt"] == "Yes" and (med_by_school.get(s["school_id"]) or 0) < 1.0)
        else:
            median_dl = p25_dl = below_1 = meet_thr = median_latency = mean_uptime = conn_under_1 = None
        rows.append({
            "iso3": iso3,
            "admin1": admin,
            "n_schools": n_schools,
            "reported_connected_share": round(reported_connected / n_schools, 3) if n_schools else None,
            "n_metered": n_metered,
            "metered_share": round(n_metered / n_schools, 3) if n_schools else None,
            "suppressed_small_n": suppressed,
            "median_download_mbps": median_dl,
            "p25_download_mbps": p25_dl,
            "share_below_1mbps": below_1,
            f"share_meeting_{benchmark:g}mbps": meet_thr,
            "median_latency_ms": median_latency,
            "mean_uptime_pct": mean_uptime,
            "reported_connected_but_under_1mbps": conn_under_1,
            "synthetic": True,
        })
    return rows

def write_csv(path: Path, fieldnames: List[str], rows: List[dict]):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--countries", nargs="+", help="ISO-3 codes, e.g. KEN GHA")
    parser.add_argument("--schools", type=int, default=400, help="Schools per country")
    parser.add_argument("--days", type=int, default=180, help="Number of daily records")
    parser.add_argument("--benchmark", type=float, default=5.0, help="Mbps threshold for 'good'")
    parser.add_argument("--min-n", type=int, default=5, help="Minimum metered schools for a regional figure")
    parser.add_argument(
        "--meter-rate",
        type=float,
        nargs=2,
        default=[0.10, 0.45],
        help="Range (low,high) of Giga-Meter coverage per country",
    )
    parser.add_argument("--end-date", default=datetime.date.today().isoformat())
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--no-quirks", action="store_true")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--out", default="out")
    args = parser.parse_args()

    cfg = {}
    if Path(args.config).exists():
        with open(args.config) as f:
            cfg = json.load(f)

    country_codes = [c.upper() for c in (args.countries or cfg.get("countries", []))]
    if not country_codes:
        sys.exit("No countries supplied – use --countries or set them in config.json")

    bc = cfg.get("boundaries", {})
    name_field = bc.get("name_field", "shapeName")
    adm = bc.get("adm", "ADM1")
    boundary_dir = Path(args.out) / "boundaries"
    dest = Path(args.out) / "giga_synthetic"
    dest.mkdir(parents=True, exist_ok=True)

    master = np.random.SeedSequence(args.seed)
    all_schools = []
    all_measurements = []
    quirk_logs = {}
    region_shapes = {}

    for iso3, ss in zip(country_codes, master.spawn(len(country_codes))):
        boundary_path = boundary_dir / f"{iso3}_{adm}.geojson"
        if not boundary_path.is_file():
            print(f"{iso3}: ! boundary file not found ({boundary_path}) – skipped", file=sys.stderr)
            continue
        rng = np.random.default_rng(ss)
        with open(boundary_path) as f:
            geo = json.load(f)
        regions = []
        for ftr in geo["features"]:
            polys = polys_of(ftr.get("geometry"))
            if not polys:
                continue
            props = ftr.get("properties", {})
            if name_field not in props:
                continue
            regions.append({
                "name": props[name_field],
                "polys": polys,
                "box": bbox_area(polys),
                "area": max(1e-9, sum(ring_area(p[0]) for p in polys)),
            })
        region_shapes[iso3] = regions
        meter_rate = rng.uniform(*args.meter_rate)
        schools = make_country(rng, iso3, regions, args.schools, args.days, args.end_date, meter_rate)
        if not args.no_quirks:
            schools, qlog = inject_quirks(rng, schools)
            quirk_logs[iso3] = qlog
        measurements = make_measurements(rng, schools, args.days, args.end_date)
        schools = compute_status(schools, measurements, args.benchmark)
        all_schools.extend(schools)
        all_measurements.extend(measurements)
        print(
            f"{iso3}: {len(schools)} schools, {len(measurements):,} measurement rows, "
            f"{int(sum(s['has_meter'] for s in schools))} with meters (rate {meter_rate:.0%})"
        )

    if not all_schools:
        sys.exit("No data generated – check that boundary files exist for the requested countries.")

    # write per-country CSVs
    schools_by_iso = group_by(all_schools, key=lambda s: s["iso3"])
    meas_by_iso = group_by(all_measurements, key=lambda m: next(s["iso3"] for s in all_schools if s["school_id"] == m["school_id"]))
    for iso3, sch_list in schools_by_iso.items():
        sch_out = [{FIELD_MAP[k]: v for k, v in rec.items() if k in FIELD_MAP} for rec in sch_list]
        write_csv(dest / f"{iso3}_schools.csv", list(FIELD_MAP.values()), sch_out)
        meas_list = meas_by_iso.get(iso3, [])
        meas_out = [{FIELD_MAP[k]: v for k, v in rec.items() if k in FIELD_MAP} for rec in meas_list]
        write_csv(dest / f"{iso3}_measurements.csv", list(FIELD_MAP.values()), meas_out)

    summary_rows = summarise(all_schools, all_measurements, args.benchmark, args.min_n)
    write_csv(dest / "giga_region_summary.csv", list(summary_rows[0].keys()), summary_rows)

    meta = {
        "synthetic": True,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "seed": args.seed,
        "params": {k: v for k, v in vars(args).items() if k not in ("config", "countries")},
        "countries": country_codes,
        "quirks_injected": quirk_logs,
        "benchmark_note": "good/moderate/no thresholds are placeholders",
        "field_names_note": "Only a subset of column names (school_id_giga, school_name, date, download_speed, upload_speed, latency) were confirmed from a third‑party Giga project; others are best‑guess placeholders.",
        "independence_note": "Data are synthetic and not tied to real M‑Lab or Giga measurements.",
        "status_counts": {k: sum(1 for s in all_schools if s["status"] == k) for k in set(s["status"] for s in all_schools)},
        "tech_shares": {k: round(v / len(all_schools), 3) for k, v in group_by(all_schools, key=lambda s: s["tech"]).items()},
    }
    (dest / "giga_synthetic_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"\n✅ Synthetic data written to {dest}/")

    if args.preview:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as e:
            print(f"Preview skipped – matplotlib not available ({e})", file=sys.stderr)
            return
        colours = {"good": "#1D9E75", "moderate": "#E0A100", "no": "#D85A30", "unknown": "#9aa5b1"}
        iso_list = sorted(schools_by_iso.keys())
        fig, axes = plt.subplots(1, len(iso_list), figsize=(5.2 * len(iso_list), 5), squeeze=False)
        for ax, iso3 in zip(axes[0], iso_list):
            for rg in region_shapes[iso3]:
                for p in rg["polys"]:
                    for ring in p:
                        xs, ys = zip(*ring)
                        ax.plot(xs, ys, color="#555", lw=0.8)
            schools_iso = [s for s in all_schools if s["iso3"] == iso3 and s.get("lat") and s.get("lon") and s["lat"] != 0.0 and s["lon"] != 0.0]
            for st, col in colours.items():
                pts = [(s["lon"], s["lat"]) for s in schools_iso if s["status"] == st]
                if not pts:
                    continue
                xs, ys = zip(*pts)
                ax.scatter(xs, ys, s=9, c=col, label=f"{st} ({len(xs)})", alpha=0.85, linewidths=0)
            ax.set_title(f"{iso3}: synthetic schools by status")
            ax.set_aspect("equal")
            ax.legend(loc="lower left", fontsize=8)
        fig.tight_layout()
        preview_path = dest / "preview.png"
        fig.savefig(preview_path, dpi=110)
        print(f"🖼️ Preview image saved to {preview_path}")

if __name__ == "__main__":
    main()
