#!/usr/bin/env python3
"""
SYNTHETIC stand-in for Giga Maps data (schools + connectivity measurements). For demos and plumbing tests
only. Every output is labelled synthetic, and nothing here is calibrated to any real country.

What it imitates (structure, not truth)
  - A school master table: one row per school with location, admin-1 region, level, size, electricity,
    cellular coverage, distances, reported ("government") connectivity, and a Giga Meter flag.
  - A measurements table: daily download / upload / latency / uptime, ONLY for schools with a meter
    (a minority, and skewed toward schools that already have electricity and a connection, like the real
    coverage gap).
  - Features worth testing a dashboard against: urban/rural gradients, regional and country quality
    differences, outages and degradation episodes, stale "reported connected" records that measure poorly
    (paper vs ground), a different naming scheme for regions, and a few data-quality quirks.
  Locations are drawn inside your real admin-1 boundaries (boundaries/<ISO3>_ADM1.geojson), clustered around
  synthetic settlements.

Field names: only school_id_giga, school_name, date, download_speed, upload_speed, latency were seen in a third-party
project that used Giga Meter data. The rest are PLAUSIBLE GUESSES. Edit FIELD_MAP below to match the real
API when you have access, so downstream code needs only the mapping changed.

Independence: regional quality here is random and NOT tied to M-Lab, on purpose. Do not read any
agreement or disagreement between this file and M-Lab as a finding.

Outputs (default TEMP/giga_synthetic/)
  <ISO3>_schools.csv/json, <ISO3>_measurements.csv, giga_region_summary.csv/json,
  giga_synthetic_meta.json, data_status.json, preview.png (--preview)

Usage
  python make_synthetic_giga.py [--countries KEN GHA] [--schools 400] [--days 180] [--seed 7] [--preview]
  python make_synthetic_giga.py --boundaries out/boundaries --out TEMP/giga_synthetic
"""

import argparse
import datetime
import json
import math
import sys
import uuid
from pathlib import Path

import numpy as np
import pandas as pd

FIELD_MAP = {  # internal name -> output column. EDIT to match the real Giga schema.
    "school_id": "school_id_giga",
    "gov_id": "school_id_govt",
    "name": "school_name",
    "iso3": "country_iso3",
    "admin1": "admin1",
    "admin1_id": "admin1_id",
    "admin1_boundary": "admin1_boundary",
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
    "download_median_30d": "download_median_30d_mbps",
    "latency_median_30d": "latency_median_30d_ms",
    "uptime_mean_30d": "uptime_mean_30d_pct",
    "synthetic": "synthetic",
    "date": "date",
    "download": "download_speed",
    "upload": "upload_speed",
    "latency": "latency",
    "uptime": "uptime_pct",
    "n_tests": "n_tests",
}

TECHS = ["Fibre", "4G/LTE", "3G", "Satellite", "No connection"]
# Illustrative parameters. Not calibrated to any country. (15% of connected schools get a degraded link: 'connected' but poor.)
DL_MEDIAN = {"Fibre": 40.0, "4G/LTE": 12.0, "3G": 3.0, "Satellite": 6.0}
UL_RATIO = {"Fibre": 0.8, "4G/LTE": 0.3, "3G": 0.25, "Satellite": 0.15}
LAT_MEDIAN = {"Fibre": 15.0, "4G/LTE": 55.0, "3G": 120.0, "Satellite": 620.0}
COVER = {"city": [0.80, 0.18, 0.02, 0.0], "town": [0.55, 0.30, 0.13, 0.02], "village": [0.25, 0.30, 0.25, 0.20]}
COVER_TYPES = ["4G", "3G", "2G", "No coverage"]
ELEC_P = {"city": 0.97, "town": 0.88, "village": 0.55}
URBAN = {"city": 0.9, "town": 0.6, "village": 0.2}

# ----------------------------------------------------------------- geometry (pure python)
def polys_of(g):
    if not g:
        return []
    return [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"] if g["type"] == "MultiPolygon" else []


def in_ring(x, y, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi, xj, yj = ring[i][0], ring[i][1], ring[j][0], ring[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-300) + xi:
            inside = not inside
        j = i
    return inside


def inside(x, y, polys):
    return any(in_ring(x, y, p[0]) and not any(in_ring(x, y, h) for h in p[1:]) for p in polys)


def bbox_area(polys):
    xs = [pt[0] for p in polys for pt in p[0]]
    ys = [pt[1] for p in polys for pt in p[0]]
    return min(xs), min(ys), max(xs), max(ys)


def ring_area(ring):
    return abs(sum(ring[i][0] * ring[(i + 1) % len(ring)][1] - ring[(i + 1) % len(ring)][0] * ring[i][1]
                   for i in range(len(ring)))) / 2


def sample_inside(rng, polys, box, tries=4000):
    x0, y0, x1, y1 = box
    for _ in range(tries):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if inside(x, y, polys):
            return x, y
    return polys[0][0][0][0], polys[0][0][0][1]


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# ----------------------------------------------------------------- schools
def make_country(rng, iso3, regions, n_schools, days, end_date, meter_rate):
    if not regions:
        raise ValueError(f"{iso3} has no usable admin-1 boundaries")
    cq = rng.lognormal(0, 0.30)                      # country quality
    weights = np.array([math.sqrt(r["area"]) * rng.lognormal(0, 0.35) for r in regions])
    counts = rng.multinomial(n_schools, weights / weights.sum())
    rows = []
    n = 0
    for r, cnt in zip(regions, counts):
        if not cnt:
            continue
        rq = rng.lognormal(0, 0.35)                 # region quality
        q = math.log(cq * rq)
        box = r["box"]
        ext = max(box[2] - box[0], box[3] - box[1])
        n_set = int(rng.integers(5, 12))
        stypes = ["city"] + ["town"] * max(1, n_set // 4) + ["village"] * n_set
        stypes = stypes[:n_set + 1]
        cent = [sample_inside(rng, r["polys"], box) for _ in stypes]
        sw = np.array([{"city": 6, "town": 2, "village": 1}[t] * rng.lognormal(0, 0.5) for t in stypes])
        sig = {"city": 0.03 * ext, "town": 0.06 * ext, "village": 0.10 * ext}
        for _ in range(cnt):
            k = rng.choice(len(stypes), p=sw / sw.sum())
            st, (cx, cy) = stypes[k], cent[k]
            for _try in range(30):
                x, y = cx + rng.normal(0, sig[st]), cy + rng.normal(0, sig[st])
                if inside(x, y, r["polys"]):
                    break
            else:
                x, y = cx, cy
            n += 1
            level = rng.choice(["Primary", "Secondary", "Pre-Primary"], p=[0.65, 0.25, 0.10])
            students = int(max(15, rng.lognormal(math.log({"Primary": 300, "Secondary": 450, "Pre-Primary": 80}[level]), 0.5)))
            ptr = rng.lognormal(math.log(32 if level == "Secondary" else 40), 0.25) * (1.25 if st == "village" else 1.0)
            elec = bool(rng.random() < sigmoid(math.log(ELEC_P[st] / (1 - ELEC_P[st])) + 0.6 * q))
            cov = str(rng.choice(COVER_TYPES, p=COVER[st]))
            u = URBAN[st] + rng.normal(0, 0.1)
            allowed = {"No connection": 0.0, "Satellite": -0.6 - 0.8 * u - 0.3 * q}
            if cov in ("4G", "3G"):
                allowed["3G"] = 0.4 + 0.2 * q
            if cov == "4G":
                allowed["4G/LTE"] = 0.1 + 1.4 * u + 0.5 * q
            if st in ("city", "town"):
                allowed["Fibre"] = -1.6 + 2.6 * u + q
            allowed["No connection"] = 1.1 * (1 - u) - 0.8 * q - 0.1
            tech = str(rng.choice(list(allowed), p=np.exp(list(allowed.values())) / np.exp(list(allowed.values())).sum()))
            conn_govt = "Yes" if (tech != "No connection" and rng.random() < 0.92) or (tech == "No connection" and rng.random() < 0.06) else "No"
            contracted = float(rng.choice([2, 5, 10, 20, 50, 100], p=[.2, .25, .25, .15, .1, .05])) if tech != "No connection" else np.nan
            meter = bool(tech != "No connection" and elec and rng.random() < meter_rate)
            rows.append({
                "school_id": str(uuid.UUID(bytes=rng.bytes(16), version=4)),
                "gov_id": f"{iso3}{n:06d}",
                "name": f"Demo {level} School {n:04d}",
                "iso3": iso3,
                "admin1": r["name"],
                "admin1_id": r["id"],
                "admin1_boundary": r["name"],
                "lat": y,
                "lon": x,
                "level": level,
                "students": students,
                "teachers": int(max(1, round(students / ptr))),
                "computers": int(rng.poisson(8 if (elec and tech != "No connection") else 0.8)),
                "electricity": elec,
                "coverage": cov,
                "tower_km": round(float(rng.lognormal({"city": -0.2, "town": 1.0, "village": 2.0}[st], 0.6)), 1),
                "fiber_km": round(float(rng.lognormal({"city": 1.5, "town": 3.0, "village": 4.2}[st], 0.6)), 1),
                "tech": tech,
                "contracted": contracted,
                "conn_govt": conn_govt,
                "has_meter": meter,
                "base_dl": DL_MEDIAN.get(tech, 0) * rng.lognormal(0, 0.55) * (rng.uniform(0.1, 0.4) if rng.random() < 0.15 else 1.0),
                "install_day": int(rng.integers(0, max(1, days - 14))),
            })
    return pd.DataFrame(rows)


def make_measurements(rng, schools, days, end_date):
    out = []
    dates = pd.date_range(end=end_date, periods=days, freq="D")
    wk = np.where(dates.day_of_week < 5, 0.9, 1.0)
    for s in schools[schools["has_meter"]].itertuples():
        t0 = s.install_day
        n = days - t0
        if n < 5:
            continue
        ar = np.zeros(n)
        for i in range(1, n):
            ar[i] = 0.97 * ar[i - 1] + rng.normal(0, 0.04)
        f = np.exp(ar) * wk[t0:]
        for _ in range(rng.poisson(n / 60)):
            a = int(rng.integers(0, n))
            f[a:a + int(rng.integers(3, 11))] *= rng.uniform(0.2, 0.6)
        p_out = rng.uniform(0.01, 0.04) * (1.5 if s.tech == "Satellite" else 1.0)
        outage = rng.random(n) < p_out
        k = rng.choice([1, 2, 3, 4], size=n, p=[.1, .15, .25, .5])
        dl = s.base_dl * f * rng.lognormal(0, 0.22, n)
        ul = dl * UL_RATIO[s.tech] * rng.lognormal(0, 0.2, n)
        lat = LAT_MEDIAN[s.tech] * rng.lognormal(0, 0.25, n) / np.sqrt(f.clip(0.3, 2))
        up = np.where(outage, rng.uniform(0, 60, n), 100 - rng.exponential(0.8, n)).clip(0, 100)
        dl, ul = np.where(outage, np.nan, dl), np.where(outage, np.nan, ul)
        keep = rng.random(n) > 0.05
        frame = pd.DataFrame({
            "school_id": s.school_id,
            "date": dates[t0:].date,
            "download": dl,
            "upload": ul,
            "latency": np.where(outage, np.nan, lat),
            "uptime": up,
            "n_tests": np.where(outage, 0, k),
        })
        out.append(frame[keep])
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=["school_id", "date", "download", "upload", "latency", "uptime", "n_tests"])


def add_status(schools, meas, benchmark, window=30):
    if len(meas):
        last = pd.to_datetime(meas["date"]).max()
        recent = meas[pd.to_datetime(meas["date"]) > last - pd.Timedelta(days=window)]
        per = recent.groupby("school_id").agg(
            download_median_30d=("download", "median"),
            latency_median_30d=("latency", "median"),
            uptime_mean_30d=("uptime", "mean"),
        )
    else:
        per = pd.DataFrame(columns=["download_median_30d", "latency_median_30d", "uptime_mean_30d"])
    per.index.name = "school_id"
    schools = schools.join(per, on="school_id")
    schools["status"] = np.where(schools["download_median_30d"].isna(), "unknown",
                                 np.where(schools["download_median_30d"] >= benchmark, "good",
                                          np.where(schools["download_median_30d"] >= 1, "moderate", "no")))
    return schools


def apply_quirks(rng, schools):
    n = len(schools)
    log = {}
    idx = rng.choice(n, size=max(1, int(0.01 * n)), replace=False)
    schools.loc[schools.index[idx], ["lat", "lon"]] = np.nan
    log["missing_coordinates"] = len(idx)
    idx = rng.choice(n, size=max(1, int(0.005 * n)), replace=False)
    schools.loc[schools.index[idx], ["lat", "lon"]] = schools.loc[schools.index[idx], ["lon", "lat"]].values
    log["swapped_lat_lon"] = len(idx)
    idx = rng.choice(n, size=max(1, int(0.003 * n)), replace=False)
    schools.loc[schools.index[idx], ["lat", "lon"]] = 0.0
    log["zero_coordinates"] = len(idx)
    idx = rng.choice(n, size=max(1, int(0.02 * n)), replace=False)
    schools.loc[schools.index[idx[1:]], "name"] = schools.loc[schools.index[idx[0]], "name"]
    log["duplicated_names"] = len(idx) - 1
    idx = rng.random(n) < 0.12
    schools.loc[idx, "admin1"] = [
        [a.upper(), a + " Region", a + " County", a + " Province"][int(rng.integers(4))]
        for a in schools.loc[idx, "admin1"]
    ]
    log["admin1_name_variants"] = int(idx.sum())
    return schools, log


def summarise(schools, benchmark, min_n):
    s = schools.copy()
    s["dl30"] = s["download_median_30d"]
    s["lat_ms"] = s["latency_median_30d"]
    s["up30"] = s["uptime_mean_30d"]
    rows = []
    for (iso3, adm), g in s.groupby(["iso3", "admin1"]):
        m = g[g["dl30"].notna()]
        sup = len(m) < min_n
        rows.append({
            "iso3": iso3,
            "admin1": adm,
            "n_schools": len(g),
            "reported_connected_share": round((g["conn_govt"] == "Yes").mean(), 3),
            "n_metered": len(m),
            "metered_share": round(len(m) / len(g), 3),
            "suppressed_small_n": sup,
            "median_download_mbps": None if sup else round(float(m["dl30"].median()), 2),
            "p25_download_mbps": None if sup else round(float(m["dl30"].quantile(.25)), 2),
            "share_below_1mbps": None if sup else round(float((m["dl30"] < 1).mean()), 3),
            f"share_meeting_{benchmark:g}mbps": None if sup else round(float((m["dl30"] >= benchmark).mean()), 3),
            "median_latency_ms": None if sup else round(float(m["lat_ms"].median()), 1),
            "mean_uptime_pct": None if sup else round(float(m["up30"].mean()), 1),
            "reported_connected_but_under_1mbps": None if sup else int(((m["conn_govt"] == "Yes") & (m["dl30"] < 1)).sum()),
            "synthetic": True,
        })
    return pd.DataFrame(rows)


def main(argv=None):
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=str(here / "config.json"))
    ap.add_argument("--boundaries", default="out/boundaries", help="directory containing admin-1 GeoJSON boundaries")
    ap.add_argument("--countries", nargs="+")
    ap.add_argument("--schools", type=int, default=400, help="schools per country")
    ap.add_argument("--days", type=int, default=180)
    ap.add_argument("--benchmark", type=float, default=5.0, help="Mbps for 'good'")
    ap.add_argument("--min-n", type=int, default=5, help="min metered schools for region")
    ap.add_argument("--meter-rate", type=float, nargs=2, default=[0.10, 0.45], help="range of meter coverage")
    ap.add_argument("--end-date", default=datetime.date.today().isoformat())
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--no-quirks", action="store_true")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--out", default="TEMP/giga_synthetic", help="directory for generated placeholder data")
    a = ap.parse_args(argv)
    config_path = Path(a.config)
    cfg = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    boundaries = Path(a.boundaries)
    bc = cfg.get("boundaries", {})
    name_f, adm = bc.get("name_field", "shapeName"), bc.get("adm", "ADM1")
    id_f = bc.get("id_field", "shapeID")
    codes = [c.upper() for c in (a.countries or cfg.get("countries", []))]
    if not codes:
        codes = sorted(p.name.split("_", 1)[0] for p in boundaries.glob(f"*_{adm}.geojson"))
    if not codes:
        sys.exit(f"No countries: pass --countries or provide boundary files in {boundaries}")
    if any(len(code) != 3 or not code.isalpha() for code in codes):
        ap.error("Country codes must be three-letter ISO-3 codes.")
    if len(set(codes)) != len(codes):
        ap.error("Country codes must not be repeated.")
    if a.schools < 1 or a.days < 5 or a.min_n < 1 or a.benchmark < 0:
        ap.error("--schools and --min-n must be positive, --days must be at least 5, and --benchmark cannot be negative.")
    if len(a.meter_rate) != 2 or not (0 <= a.meter_rate[0] <= a.meter_rate[1] <= 1):
        ap.error("--meter-rate must be two values from 0 to 1 in ascending order.")
    try:
        end_date = datetime.date.fromisoformat(a.end_date)
    except ValueError:
        ap.error("--end-date must be an ISO date (YYYY-MM-DD).")
    dest = Path(a.out)
    dest.mkdir(parents=True, exist_ok=True)
    master = np.random.SeedSequence(a.seed)
    all_s, all_m, quirk_log, shapes = [], [], {}, {}
    for iso3, ss in zip(codes, master.spawn(len(codes))):
        gp = boundaries / f"{iso3}_{adm}.geojson"
        if not gp.exists():
            print(f"{iso3}: ! no boundary file ({gp}); skipped", file=sys.stderr)
            continue
        rng = np.random.default_rng(ss)
        regions = []
        for f in json.loads(gp.read_text(encoding="utf-8"))["features"]:
            polys = polys_of(f.get("geometry"))
            props = f.get("properties") or {}
            if polys and props.get(name_f) and props.get(id_f):
                regions.append({"name": f["properties"][name_f], "polys": polys, "box": bbox_area(polys),
                                "id": props[id_f],
                                "area": max(1e-9, sum(ring_area(p[0]) for p in polys))})
        if not regions:
            print(f"{iso3}: ! no usable admin-1 features in {gp}; skipped", file=sys.stderr)
            continue
        shapes[iso3] = regions
        meter_rate = rng.uniform(*a.meter_rate)
        sch = make_country(rng, iso3, regions, a.schools, a.days, end_date, meter_rate)
        meas = make_measurements(rng, sch, a.days, end_date)
        sch = add_status(sch, meas, a.benchmark)
        sch["admin1_clean"] = sch["admin1"]
        if not a.no_quirks:
            sch, ql = apply_quirks(rng, sch)
            quirk_log[iso3] = ql
        all_s.append(sch)
        all_m.append(meas)
        print(f"{iso3}: {len(sch)} schools in {len(regions)} regions, {len(meas):,} daily records for {int(sch['has_meter'].sum())} metered schools (meter rate {meter_rate:.0%})")
    if not all_s:
        sys.exit("Nothing generated (no usable boundary files found)")
    schools = pd.concat(all_s, ignore_index=True)
    meas = pd.concat(all_m, ignore_index=True)
    summary = summarise(schools, a.benchmark, a.min_n)
    schools["synthetic"] = True
    meas["synthetic"] = True
    out_s = schools.drop(columns=[c for c in schools.columns if c.startswith("_") or c in ("admin1_clean", "base_dl", "install_day")]).rename(columns=FIELD_MAP)
    for iso3, g in out_s.groupby(FIELD_MAP["iso3"]):
        g.to_csv(dest / f"{iso3}_schools.csv", index=False)
        (dest / f"{iso3}_schools.json").write_text(g.to_json(orient="records"), encoding="utf-8")
        sid = set(g[FIELD_MAP["school_id"]])
        meas[meas["school_id"].isin(sid)].rename(columns=FIELD_MAP).to_csv(dest / f"{iso3}_measurements.csv", index=False)
    summary.to_csv(dest / "giga_region_summary.csv", index=False)
    (dest / "giga_region_summary.json").write_text(summary.to_json(orient="records"), encoding="utf-8")
    meta = {
        "synthetic": True,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "seed": a.seed,
        "params": {k: v for k, v in vars(a).items() if k not in ("config", "countries")},
        "countries": list(shapes),
        "quirks_injected": quirk_log,
        "benchmark_note": "good/moderate/no thresholds are placeholders",
        "field_names_note": "Only school_id_giga, school_name, date, download_speed, upload_speed, latency are confirmed; others are guesses.",
        "independence_note": "Not tied to M-Lab.",
        "status_counts": schools["status"].value_counts().to_dict(),
        "tech_shares": schools["tech"].value_counts(normalize=True).round(3).to_dict(),
    }
    (dest / "giga_synthetic_meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    (dest / "data_status.json").write_text(json.dumps({
        "mode": "demo",
        "updated": meta["generated"][:10],
        "note": "School-level Giga placeholder records are fully synthetic. M-Lab regional measurements are a separate measured dataset.",
    }, indent=2), encoding="utf-8")
    print(f"\nWrote {dest}/ . Status counts: {meta['status_counts']}")
    if a.preview:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib not installed; skipping preview", file=sys.stderr)
            return
        cols = {"good": "#1D9E75", "moderate": "#E0A100", "no": "#D85A30", "unknown": "#9aa5b1"}
        isos = list(shapes)
        fig, axes = plt.subplots(1, len(isos), figsize=(5.2 * len(isos), 5), squeeze=False)
        for ax, iso3 in zip(axes[0], isos):
            for r in shapes[iso3]:
                for p in r["polys"]:
                    for ring in p:
                        xs, ys = zip(*ring)
                        ax.plot(xs, ys, color="#555", lw=0.8)
            g = schools[(schools["iso3"] == iso3) & schools["lat"].notna() & (schools["lat"] != 0)]
            x0, y0, x1, y1 = [f(v) for f, v in zip((min, min, max, max), zip(*[r["box"] for r in shapes[iso3]]))]
            g = g[(g["lon"].between(x0, x1)) & (g["lat"].between(y0, y1))]
            for st, c in cols.items():
                h = g[g["status"] == st]
                ax.scatter(h["lon"], h["lat"], s=9, c=c, label=f"{st} ({len(h)})", alpha=.85, linewidths=0)
            ax.set_title(f"{iso3}: SYNTHETIC schools by measured status")
            ax.set_aspect("equal")
            ax.legend(loc="lower left", fontsize=8)
        fig.tight_layout()
        fig.savefig(dest / "preview.png", dpi=110)
        print(f"Preview: {dest / 'preview.png'}")

if __name__ == "__main__":
    main()
