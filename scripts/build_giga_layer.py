#!/usr/bin/env python3
"""Clean Giga school exports for the regional dashboard and create regional layers.

Writes map-compatible <ISO3>_schools.json files to the dashboard directory and
CSV layers to <out>/layers. Synthetic data stays explicitly labelled.

Usage
  python scripts/build_giga_layer.py --dir TEMP/giga_synthetic --out out
  python scripts/build_dashboard_data.py --out out
"""

import argparse
from collections import Counter
import csv
import datetime
import json
import math
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

import fetch_boundaries as fb
from make_synthetic_giga import FIELD_MAP as F, bbox_area, inside, polys_of

POINT_FIELDS = (
    "school_name", "longitude", "latitude", "admin1_id", "admin1_boundary",
    "education_level", "connectivity_govt", "giga_meter_installed",
    "download_median_30d_mbps", "latency_median_30d_ms",
    "uptime_mean_30d_pct", "connectivity_status", "synthetic",
)
LAYER_NAMES = (
    "median_download",
    "below_1mbps",
    "metered_share",
    "reported_poor",
)


def load_regions(path, name_field, id_field):
    """Load polygons and the dashboard's stable boundary IDs."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    regions = []
    for index, feature in enumerate(data.get("features", [])):
        props = feature.get("properties") or {}
        polygons = polys_of(feature.get("geometry"))
        if polygons and props.get(name_field):
            regions.append({
                "id": str(props.get(id_field) or index),
                "name": str(props[name_field]),
                "polys": polygons,
                "box": bbox_area(polygons),
            })
    if not regions:
        raise ValueError(f"{path}: no usable admin-1 boundaries")
    return regions


def locate(lon, lat, regions):
    for region in regions:
        x0, y0, x1, y1 = region["box"]
        if x0 <= lon <= x1 and y0 <= lat <= y1 and inside(lon, lat, region["polys"]):
            return region["id"]
    return None


def clean_points(schools, regions, qc):
    """Assign regions by point-in-polygon; repair swapped coordinates when possible."""
    lon_field, lat_field = F["lon"], F["lat"]
    missing = [field for field in (lon_field, lat_field) if field not in schools]
    if missing:
        raise ValueError(f"school file is missing coordinate columns: {', '.join(missing)}")
    cleaned = schools.copy().reset_index(drop=True)
    cleaned[lon_field] = pd.to_numeric(cleaned[lon_field], errors="coerce")
    cleaned[lat_field] = pd.to_numeric(cleaned[lat_field], errors="coerce")
    shape_ids, keep = [], []
    for index, (lon, lat) in enumerate(zip(cleaned[lon_field], cleaned[lat_field])):
        if pd.isna(lon) or pd.isna(lat):
            qc["dropped_missing_coordinates"] += 1
            shape_ids.append(None)
            keep.append(False)
            continue
        if lon == 0 and lat == 0:
            qc["dropped_zero_coordinates"] += 1
            shape_ids.append(None)
            keep.append(False)
            continue
        shape_id = locate(lon, lat, regions)
        if shape_id is None:
            swapped_id = locate(lat, lon, regions)
            if swapped_id is None:
                qc["dropped_outside_all_regions"] += 1
                shape_ids.append(None)
                keep.append(False)
                continue
            cleaned.at[index, lon_field] = lat
            cleaned.at[index, lat_field] = lon
            shape_id = swapped_id
            qc["repaired_swapped_lat_lon"] += 1
        shape_ids.append(shape_id)
        keep.append(True)
    cleaned["shape_id"] = shape_ids
    return cleaned.loc[keep].copy()


def check_name_agreement(cleaned, regions, iso3, iso2, config, qc):
    """Record whether the source region-name cross-check agrees with point location."""
    if cleaned.empty:
        qc["name_matched_share"] = None
        qc["name_agrees_with_location_share"] = None
        return
    boundary_config = config.get("boundaries", {})
    names = sorted(cleaned[F["admin1"]].dropna().astype(str).unique())
    shapes = [{"idx": index, "name": region["name"], "id": region["id"]}
              for index, region in enumerate(regions)]
    try:
        rows, _ = fb.match_country(
            iso2,
            iso3,
            names,
            shapes,
            {},
            fb.Norm(boundary_config.get("stop_tokens", fb.DEFAULT_STOP)),
            boundary_config.get("fuzzy_threshold", 0.86),
            boundary_config.get("fuzzy_margin", 0.08),
            False,
        )
    except (KeyError, TypeError, ValueError) as error:
        qc["name_check_skipped"] = str(error)[:160]
        return
    name_to_shape = {row["mlab_name"]: row["shape_id"] for row in rows if row["applied"]}
    matched = cleaned[F["admin1"]].astype(str).map(name_to_shape)
    has_match = matched.notna()
    qc["name_matched_share"] = round(float(has_match.mean()), 3)
    qc["name_agrees_with_location_share"] = (
        round(float((matched[has_match] == cleaned.loc[has_match, "shape_id"]).mean()), 3)
        if has_match.any() else None
    )


def load_recent_measurements(path, window_days):
    """Return one recent metric row per school, based on per-school observations."""
    required = (F["school_id"], F["date"], F["download"])
    if not path.exists():
        return pd.DataFrame(columns=["dl", "ul", "latency", "uptime"]), None, 0
    measurements = pd.read_csv(path)
    missing = [field for field in required if field not in measurements]
    if missing:
        raise ValueError(f"{path.name} is missing measurement columns: {', '.join(missing)}")
    for field in (F["upload"], F["latency"], F["uptime"]):
        if field not in measurements:
            measurements[field] = np.nan
    measurements[F["date"]] = pd.to_datetime(measurements[F["date"]], errors="coerce", utc=True)
    invalid_dates = int(measurements[F["date"]].isna().sum())
    measurements = measurements.dropna(subset=[F["date"]])
    if measurements.empty:
        return pd.DataFrame(columns=["dl", "ul", "latency", "uptime"]), None, invalid_dates
    latest = measurements[F["date"]].max()
    recent = measurements[measurements[F["date"]] > latest - pd.Timedelta(days=window_days)].copy()
    for field in (F["download"], F["upload"], F["latency"], F["uptime"]):
        recent[field] = pd.to_numeric(recent[field], errors="coerce")
    per_school = recent.groupby(F["school_id"]).agg(
        dl=(F["download"], "median"),
        ul=(F["upload"], "median"),
        latency=(F["latency"], "median"),
        uptime=(F["uptime"], "mean"),
    )
    return per_school, latest.date().isoformat(), invalid_dates


def _nullable(value, digits):
    if pd.isna(value):
        return None
    number = float(value)
    if not math.isfinite(number):
        return None
    return round(number, digits)


def _truthy(value):
    if pd.isna(value):
        return False
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    return str(value).strip().lower() in ("true", "1", "yes", "y")


def school_payload_rows(schools, max_points):
    rows = schools.reset_index(drop=True)
    if len(rows) > max_points:
        step = math.ceil(len(rows) / max_points)
        rows = rows.iloc[::step]
    output = []
    for _, row in rows.iterrows():
        output.append({
            "school_name": str(row.get(F["name"], "")),
            "longitude": _nullable(row.get(F["lon"]), 5),
            "latitude": _nullable(row.get(F["lat"]), 5),
            "admin1_id": str(row["shape_id"]),
            "admin1_boundary": str(row.get("admin1_boundary_name", row.get(F["admin1_boundary"], ""))),
            "education_level": str(row.get(F["level"], "")),
            "connectivity_govt": str(row.get(F["conn_govt"], "")),
            "giga_meter_installed": _truthy(row.get(F["has_meter"], False)),
            "download_median_30d_mbps": _nullable(row.get("dl"), 2),
            "latency_median_30d_ms": _nullable(row.get("latency"), 1),
            "uptime_mean_30d_pct": _nullable(row.get("uptime"), 1),
            "connectivity_status": str(row.get(F["status"], "unknown")),
            "synthetic": _truthy(row.get(F["synthetic"], False)),
        })
    return output


def regional_layers(schools, iso3, year, min_n):
    rows = {name: [] for name in LAYER_NAMES}
    for shape_id, group in schools.groupby("shape_id"):
        metered = group[group["dl"].notna()]
        if len(group):
            rows["metered_share"].append(
                (iso3, shape_id, round(100 * len(metered) / len(group), 1), year)
            )
        if len(metered) >= min_n:
            rows["median_download"].append(
                (iso3, shape_id, round(float(metered["dl"].median()), 2), year)
            )
            rows["below_1mbps"].append(
                (iso3, shape_id, round(100 * float((metered["dl"] < 1).mean()), 1), year)
            )
        reported = metered[
            metered[F["conn_govt"]].astype(str).str.strip().str.lower().isin(("yes", "true", "1"))
        ]
        if len(reported) >= min_n:
            rows["reported_poor"].append(
                (iso3, shape_id, round(100 * float((reported["dl"] < 1).mean()), 1), year)
            )
    return rows


def write_layer(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["iso3", "shape_id", "value", "year"])
        writer.writerows(rows)


def main(argv=None):
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", default=str(here / "indicators_config.json"))
    parser.add_argument("--countries", nargs="+")
    parser.add_argument("--out", default=str(ROOT / "out"))
    parser.add_argument("--dir", help="folder with <ISO3>_schools.csv and <ISO3>_measurements.csv")
    parser.add_argument("--dest", help="dashboard directory for cleaned <ISO3>_schools.json files")
    parser.add_argument("--window", type=int, default=30)
    parser.add_argument("--min-n", type=int, default=5)
    parser.add_argument("--max-points", type=int, default=3000)
    parser.add_argument("--benchmark", type=float, default=5.0)
    args = parser.parse_args(argv)
    if args.window < 1 or args.min_n < 1 or args.max_points < 1 or args.benchmark < 0:
        parser.error("--window, --min-n, and --max-points must be positive; --benchmark cannot be negative")

    config_path = Path(args.config)
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    out = Path(args.out)
    school_dir = Path(args.dir) if args.dir else ROOT / "TEMP" / "giga_synthetic"
    destination = Path(args.dest) if args.dest else out / "dashboard"
    destination.mkdir(parents=True, exist_ok=True)
    (out / "layers").mkdir(parents=True, exist_ok=True)

    boundary_config = config.get("boundaries", {})
    adm = boundary_config.get("adm", "ADM1")
    name_field = boundary_config.get("name_field", "shapeName")
    id_field = boundary_config.get("id_field", "shapeID")
    countries = [code.upper() for code in (args.countries or config.get("countries", []))]
    if not countries:
        countries = sorted(path.name.split("_", 1)[0] for path in school_dir.glob("*_schools.csv"))
    if not countries:
        parser.error("No countries configured or found in the school directory.")

    pairs = fb.country_pairs(countries, out / "mlab" / "iso2_map.json")
    metadata_path = school_dir / "giga_synthetic_meta.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
    synthetic = _truthy(metadata.get("synthetic", False))
    layers = {name: [] for name in LAYER_NAMES}
    qc = {"synthetic": synthetic, "countries": {}}
    processed = 0

    for iso3 in countries:
        schools_path = school_dir / f"{iso3}_schools.csv"
        measurements_path = school_dir / f"{iso3}_measurements.csv"
        dashboard_boundary = destination / f"{iso3}.geojson"
        use_dashboard_boundary = dashboard_boundary.exists()
        boundary_path = dashboard_boundary if use_dashboard_boundary else out / "boundaries" / f"{iso3}_{adm}.geojson"
        if not schools_path.exists() or not boundary_path.exists():
            print(f"{iso3}: skipped; missing {schools_path.name} or {boundary_path.name}", file=sys.stderr)
            continue

        regions = load_regions(
            boundary_path,
            "shapeName" if use_dashboard_boundary else name_field,
            "shapeID" if use_dashboard_boundary else id_field,
        )
        schools = pd.read_csv(schools_path)
        required = (F["school_id"], F["name"], F["iso3"], F["admin1"], F["admin1_boundary"],
                    F["level"], F["students"], F["teachers"], F["electricity"],
                    F["tech"], F["conn_govt"], F["has_meter"], F["status"])
        missing = [field for field in required if field not in schools]
        if missing:
            raise ValueError(f"{schools_path.name} is missing school columns: {', '.join(missing)}")

        country_qc = Counter()
        input_count = len(schools)
        cleaned = clean_points(schools, regions, country_qc)
        check_name_agreement(cleaned, regions, iso3, pairs.get(iso3, ""), config, country_qc)
        per_school, as_of, invalid_dates = load_recent_measurements(measurements_path, args.window)
        country_qc["invalid_measurement_dates"] = invalid_dates
        per_school.index.name = F["school_id"]
        cleaned = cleaned.join(per_school, on=F["school_id"])
        for field in ("dl", "ul", "latency", "uptime"):
            if field not in cleaned:
                cleaned[field] = np.nan
        if cleaned.empty:
            print(f"{iso3}: no schools left after coordinate validation", file=sys.stderr)
            continue

        boundary_names = {region["id"]: region["name"] for region in regions}
        cleaned["admin1_boundary_name"] = cleaned["shape_id"].map(boundary_names)
        year = int(as_of[:4]) if as_of else datetime.date.today().year
        for layer_name, values in regional_layers(cleaned, iso3, year, args.min_n).items():
            layers[layer_name].extend(values)

        points = school_payload_rows(cleaned, args.max_points)
        payload = {
            "synthetic": synthetic,
            "asOf": as_of,
            "windowDays": args.window,
            "minN": args.min_n,
            "benchmark": args.benchmark,
            "n_total": input_count,
            "n_shown": len(points),
            "fields": list(POINT_FIELDS),
            "rows": points,
        }
        (destination / f"{iso3}_schools.json").write_text(
            json.dumps(payload, separators=(",", ":"), ensure_ascii=False),
            encoding="utf-8",
        )
        country_qc_summary = dict(country_qc)
        country_qc_summary.update({
            "schools_input": input_count,
            "schools_kept": len(cleaned),
            "schools_shown": len(points),
            "schools_metered_recently": int(cleaned["dl"].notna().sum()),
            "measurement_latest_date": as_of,
        })
        qc["countries"][iso3] = country_qc_summary
        processed += 1
        print(
            f"{iso3}: kept {len(cleaned)}/{input_count} school points; "
            f"{int(cleaned['dl'].notna().sum())} with recent meter data"
        )

    if not processed:
        parser.error("No countries could be processed; check the input and boundary directories.")
    for layer_name, rows in layers.items():
        write_layer(out / "layers" / f"giga_{layer_name}.csv", rows)
    qc_path = out / "giga_qc.json"
    qc_path.write_text(json.dumps(qc, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote cleaned school points to {destination}; regional CSV layers to {out / 'layers'}")
    print(f"QC summary: {qc_path}")
    print("Rebuild the regional dashboard with scripts/build_dashboard_data.py to expose Giga metrics.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: Giga layer build failed: {error}", file=sys.stderr)
        raise SystemExit(1)
