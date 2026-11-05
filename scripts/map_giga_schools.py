#!/usr/bin/env python3
"""
map_giga_schools.py
===================
Map Giga school locations and connectivity: an interactive HTML map, a static
PNG, and summary tables. Works on the CSVs written by fetch_connectivity_data.py
(giga_schools_KEN.csv, giga_connectivity_KEN.csv) or any similar file/GeoJSON.

    python map_giga_schools.py --demo KEN                       # try it now, synthetic data
    python map_giga_schools.py --schools giga_schools_KEN.csv --connectivity giga_connectivity_KEN.csv
    python map_giga_schools.py --schools giga_schools_KEN.csv --boundaries kenya_adm1.geojson
    python map_giga_schools.py --schools x.csv --show-columns   # see what was detected, then fix with --col

Outputs (in --out): schools_map.html, schools_map.png, summary_overall.csv,
summary_by_<unit>.csv, map_audit.json

WHAT IS AND ISN'T KNOWN ABOUT GIGA'S SCHEMA
  Confirmed from public sources: Giga Maps colours each school green (adequate),
  yellow (minimal) or red (no connectivity); the backend has `connectivity_status`
  and `coverage_status` fields on schools; map layers include download speed,
  latency and cellular coverage.
  NOT confirmed: the API's exact field names and value codes (docs are not
  publicly readable). So columns are found heuristically by name, values are
  interpreted by meaning, and the audit file lists every choice. If something is
  mis-detected, override it with --col KEY=NAME (keys: lat lon geo id name status
  speed latency coverage admin1 level area time).

Status handling: good/adequate/green -> Good; moderate/minimal/yellow ->
Moderate; yes/true/connected -> Connected (quality unspecified); no/none/red ->
No connectivity; blank/unknown -> Unknown. "% connected" = (good + moderate +
connected) / (all with a known status). If there is no status column but a
download-speed column exists, status is derived from speed (--good-mbps is an
illustrative threshold, NOT an official Giga cut-off).

Requires: pandas, numpy, matplotlib, folium  (pip install pandas numpy matplotlib folium)
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

__version__ = "1.0.0"
log = logging.getLogger("giga-map")


class MapError(Exception):
    """A problem the user must fix (missing file, no coordinates, bad override)."""


# --------------------------------------------------------------------------
# Status vocabulary
# --------------------------------------------------------------------------
STATUS_ORDER = ["good", "moderate", "connected", "no", "unknown"]
STATUS_LABEL = {"good": "Good / adequate", "moderate": "Moderate / minimal", "connected": "Connected (quality n/a)",
                "no": "No connectivity", "unknown": "Unknown / no data"}
STATUS_COLOR = {"good": "#2e9e4f", "moderate": "#f0a30a", "connected": "#6cb98a", "no": "#d6342c",
                "unknown": "#8a8f98"}
CONNECTED = {"good", "moderate", "connected"}
_RX = {k: re.compile(p, re.I) for k, p in {
    "unknown": r"^(|nan|null|none given|unknown|n/?a|not available|unavailable|no data|-+|\?)$",
    "no": r"^(no|none|false|0|n|not connected|unconnected|disconnected|offline|red|"
          r"no (internet|connectivity|connection|service))\b",
    "good": r"^(good|adequate|high|green|fast|strong|broadband|sufficient)\b",
    "moderate": r"^(moderate|minimal|medium|yellow|amber|basic|slow|fair|limited|some|low)\b",
    "connected": r"^(yes|true|1|y|connected|online|has internet)\b"}.items()}


def _norm(v: Any) -> str:
    if v is None or (np.isscalar(v) and pd.isna(v)):
        return ""
    if isinstance(v, (bool, np.bool_)):
        return "true" if v else "false"
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    if isinstance(v, (float, np.floating)):
        return str(int(v)) if float(v).is_integer() else str(v)
    t = unicodedata.normalize("NFKC", str(v)).lower().replace("\u2019", "'")
    return re.sub(r"\s+", " ", t).strip()


def canon_status(series: pd.Series) -> tuple[pd.Series, dict[str, int]]:
    """Map raw status values to good/moderate/connected/no/unknown; also return unrecognised values."""
    unrecognised: dict[str, int] = {}
    cache: dict[str, str] = {}

    def one(v: Any) -> str:
        k = _norm(v)
        if k in cache:
            return cache[k]
        for cat in ("unknown", "no", "good", "moderate", "connected"):
            if _RX[cat].match(k):
                cache[k] = cat
                return cat
        cache[k] = "unknown"
        unrecognised[k] = unrecognised.get(k, 0) + 1
        return "unknown"

    out = series.map(one)
    if unrecognised:  # recount properly (the cache hides repeats)
        norm = series.map(_norm)
        unrecognised = {k: int((norm == k).sum()) for k in unrecognised}
    return out, unrecognised


def status_from_speed(speed: pd.Series, good_mbps: float) -> pd.Series:
    s = pd.to_numeric(speed, errors="coerce")
    return pd.Series(np.where(s.isna(), "unknown", np.where(s <= 0, "no", np.where(s >= good_mbps, "good", "moderate"))),
                     index=speed.index)


# --------------------------------------------------------------------------
# Reading + column detection
# --------------------------------------------------------------------------
_WRAP = ("data", "results", "items", "schools", "records")


def words(name: Any) -> str:
    t = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", str(name))
    return re.sub(r"\s+", " ", re.sub(r"[^A-Za-z0-9]+", " ", t).lower()).strip()


def load_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise MapError(f"File not found: {path}")
    sfx = path.suffix.lower()
    try:
        if sfx == ".csv":
            return pd.read_csv(path, low_memory=False)
        if sfx == ".parquet":
            return pd.read_parquet(path)
        if sfx in (".json", ".geojson"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("type") == "FeatureCollection":
                rows = [{**(f.get("properties") or {}), "geometry": f.get("geometry")} for f in data["features"]]
            elif isinstance(data, dict):
                rows = next((data[k] for k in _WRAP if isinstance(data.get(k), list)), [])
            else:
                rows = data
            return pd.json_normalize(rows, max_level=1)
    except MapError:
        raise
    except Exception as e:
        raise MapError(f"Could not read {path.name}: {e}") from e
    raise MapError(f"Unsupported file type '{sfx}'. Use .csv, .parquet, .json or .geojson")


def parse_point(v: Any) -> tuple[float, float] | None:
    """Return (lat, lon) from GeoJSON dict/list, WKT 'POINT(lon lat)', 'lat,lon' text or {'lat','lon'}."""
    try:
        if v is None or (np.isscalar(v) and pd.isna(v)):
            return None
        if isinstance(v, str):
            m = re.match(r"\s*(?:SRID=\d+;)?POINT\s*Z?\s*\(\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)", v, re.I)
            if m:
                return float(m.group(2)), float(m.group(1))
            m = re.match(r"\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*$", v)
            if m:
                return float(m.group(1)), float(m.group(2))
            if v.strip().startswith("{"):
                return parse_point(json.loads(v))
            return None
        if isinstance(v, dict):
            if isinstance(v.get("coordinates"), (list, tuple)) and len(v["coordinates"]) >= 2:
                return float(v["coordinates"][1]), float(v["coordinates"][0])
            for a, b in (("lat", "lon"), ("latitude", "longitude"), ("lat", "lng")):
                if a in v and b in v:
                    return float(v[a]), float(v[b])
            return None
        if isinstance(v, (list, tuple, np.ndarray)) and len(v) >= 2:
            return float(v[1]), float(v[0])          # GeoJSON order is [lon, lat]
    except (ValueError, TypeError):
        return None
    return None


def rx(p: str) -> re.Pattern:
    return re.compile(p, re.I)


SPECS: dict[str, dict[str, Any]] = {
    "lat": dict(inc=[(rx(r"\blat(itude)?\b"), 5)], exc=rx(r"nearest|tower|node|lte|distance|plat")),
    "lon": dict(inc=[(rx(r"\b(lon|lng|long|longitude)\b"), 5)], exc=rx(r"nearest|tower|node|lte|distance")),
    "geo": dict(inc=[(rx(r"\b(geopoint|geometry|geo|location|coordinates?|point|position)\b"), 3)], exc=rx(r"type$")),
    "id": dict(inc=[(rx(r"\bgiga\b.*\bid\b|\bid\b.*\bgiga\b|giga id"), 6), (rx(r"school id|school code|\bschool uid"), 4),
                    (rx(r"^id$|\bid$|\buid\b|external id"), 2)],
               exc=rx(r"country|admin|region|district|province|location|geo|county|isp|operator|contact")),
    "name": dict(inc=[(rx(r"school.?name"), 5), (rx(r"^name$|\bname$"), 3)],
                 exc=rx(r"admin|country|region|district|isp|operator|contact|province|county|file|source")),
    "status": dict(inc=[(rx(r"connectivity.?status"), 6), (rx(r"^connectivity$|\bconnectivity$"), 3),
                        (rx(r"\bconnected\b|has internet|internet access"), 2)],
                   exc=rx(r"coverage|type|speed|latency|provider|isp|technology|distance|download|upload|"
                          r"date|time|id$|contract")),
    "speed": dict(inc=[(rx(r"download"), 4), (rx(r"\bspeed\b"), 2), (rx(r"mbps"), 2)],
                  exc=rx(r"upload|contract|expected|planned|latency|ping|nearest|distance")),
    "latency": dict(inc=[(rx(r"latency|\brtt\b|\bping\b"), 4)], exc=None),
    "coverage": dict(inc=[(rx(r"coverage.?(status|type)?"), 4)], exc=rx(r"distance|nearest")),
    "admin1": dict(inc=[(rx(r"admin ?1"), 5), (rx(r"\b(region|province|county|state)\b"), 3), (rx(r"district|admin ?2"), 1)],
                   exc=rx(r"\bid$|\bid\b|code|giga")),
    "level": dict(inc=[(rx(r"education.?level|school.?level"), 5), (rx(r"\blevel\b"), 2)],
                  exc=rx(r"connectivity|speed|signal|coverage")),
    "area": dict(inc=[(rx(r"environment|area.?type|\burban\b|\brural\b|locality|settlement"), 4)], exc=rx(r"\bid\b")),
    "time": dict(inc=[(rx(r"timestamp|updated|date|\btime\b"), 3)], exc=None),
}


def find_columns(df: pd.DataFrame, key: str) -> list[tuple[str, float]]:
    spec, out = SPECS[key], []
    for c in df.columns:
        w = words(c)
        if spec["exc"] and spec["exc"].search(w):
            continue
        score = sum(wt for pat, wt in spec["inc"] if pat.search(w))
        if score > 0:
            out.append((c, float(score)))
    return sorted(out, key=lambda t: -t[1])


def detect(df: pd.DataFrame, overrides: dict[str, str]) -> tuple[dict[str, str | None], dict[str, list[str]]]:
    cols: dict[str, str | None] = {}
    alts: dict[str, list[str]] = {}
    low = {c.lower(): c for c in df.columns}
    for key in SPECS:
        if key in overrides:
            if overrides[key].lower() not in low:
                raise MapError(f"--col {key}={overrides[key]}: column not found. Columns: {list(df.columns)[:40]}")
            cols[key], alts[key] = low[overrides[key].lower()], []
            continue
        cands = find_columns(df, key)
        if key == "geo":   # keep only columns whose values actually parse as points
            cands = [(c, s) for c, s in cands
                     if (df[c].dropna().head(50).map(parse_point).notna().mean() if df[c].notna().any() else 0) >= 0.8]
        cols[key] = cands[0][0] if cands else None
        alts[key] = [c for c, _ in cands[1:4]]
    return cols, alts


def extract_points(df: pd.DataFrame, cols: dict[str, str | None], audit: dict) -> pd.DataFrame:
    if cols["lat"] and cols["lon"]:
        lat = pd.to_numeric(df[cols["lat"]], errors="coerce")
        lon = pd.to_numeric(df[cols["lon"]], errors="coerce")
        audit["coordinate_source"] = f"{cols['lat']} / {cols['lon']}"
    elif cols["geo"]:
        pts = df[cols["geo"]].map(parse_point)
        lat = pts.map(lambda p: p[0] if p else np.nan)
        lon = pts.map(lambda p: p[1] if p else np.nan)
        audit["coordinate_source"] = f"{cols['geo']} (parsed point)"
    else:
        raise MapError("No coordinates found. Expected latitude/longitude columns or a point/geometry column. "
                       "Use --show-columns to see the columns, then --col lat=NAME --col lon=NAME.")
    swapped = (lat.abs() > 90) & (lon.abs() <= 90)
    lat, lon = lat.where(~swapped, lon), lon.where(~swapped, lat)
    missing = lat.isna() | lon.isna()
    out_of_range = ~missing & ((lat.abs() > 90) | (lon.abs() > 180))
    zero = ~missing & (lat == 0) & (lon == 0)
    keep = ~(missing | out_of_range | zero)
    audit["coordinates"] = {"rows": int(len(df)), "kept": int(keep.sum()), "missing": int(missing.sum()),
                            "out_of_range": int(out_of_range.sum()), "zero_zero": int(zero.sum()),
                            "swapped_lat_lon_fixed": int(swapped.sum())}
    if not keep.any():
        raise MapError("No valid coordinates after cleaning (all missing / out of range / 0,0).")
    out = df.loc[keep].copy()
    out["_lat"], out["_lon"] = lat[keep].astype(float), lon[keep].astype(float)
    return out.reset_index(drop=True)


# --------------------------------------------------------------------------
# Merge, classify, summarise
# --------------------------------------------------------------------------
def merge_connectivity(schools: pd.DataFrame, conn: pd.DataFrame, s_cols: dict, audit: dict) -> pd.DataFrame:
    c_cols, _ = detect(conn, {})
    sid, cid = s_cols.get("id"), c_cols.get("id")
    shared = [c for c in schools.columns if c in conn.columns and re.search(r"id|code", c, re.I)]
    if shared:
        sid = cid = shared[0] if not (sid and cid and sid == cid) else sid
    if not (sid and cid):
        raise MapError("Could not find a school id in both files to join on. Use --col id=NAME (the same name must "
                       f"exist in both files). Schools columns: {list(schools.columns)[:25]}; "
                       f"connectivity columns: {list(conn.columns)[:25]}")
    conn = conn.copy()
    if c_cols.get("time"):
        conn = conn.assign(_t=pd.to_datetime(conn[c_cols["time"]], errors="coerce")).sort_values("_t")
    conn = conn.drop_duplicates(cid, keep="last")       # latest record per school
    keep = [cid] + [c_cols[k] for k in ("status", "speed", "latency", "coverage") if c_cols.get(k)]
    renamed = {c: f"{c}__conn" if c in schools.columns and c != sid else c for c in keep}
    merged = schools.merge(conn[keep].rename(columns=renamed), left_on=sid, right_on=renamed[cid], how="left",
                           suffixes=("", "__dup"))
    audit["join"] = {"schools_id": sid, "connectivity_id": cid, "connectivity_rows": int(len(conn)),
                     "schools_matched": int(merged[renamed[keep[1]]].notna().sum()) if len(keep) > 1 else 0}
    return merged


def build_status(df: pd.DataFrame, cols: dict, conn_cols: dict | None, good_mbps: float, audit: dict) -> pd.DataFrame:
    """Add _status (canonical) plus numeric _speed/_latency.
    With a merged connectivity file, its values win where present; schools without a record keep the value
    from the schools file (fallback)."""
    def series_for(key: str) -> tuple[pd.Series | None, str | None]:
        own = cols.get(key) if cols.get(key) in df.columns else None
        conn = None
        if conn_cols and conn_cols.get(key):
            alt = f"{conn_cols[key]}__conn"
            conn = alt if alt in df.columns else (conn_cols[key] if conn_cols[key] in df.columns
                                                  and conn_cols[key] != own else None)
        if conn and own:
            return df[conn].where(df[conn].notna(), df[own]), f"{conn} (fallback: {own})"
        name = conn or own
        return (df[name], name) if name else (None, None)
    st, st_name = series_for("status")
    sp, sp_name = series_for("speed")
    la, _ = series_for("latency")
    out = df.copy()
    out["_speed"] = pd.to_numeric(sp, errors="coerce") if sp is not None else np.nan
    out["_latency"] = pd.to_numeric(la, errors="coerce") if la is not None else np.nan
    if st is not None:
        out["_status"], unrec = canon_status(st)
        audit["status"] = {"source_column": st_name, "method": "value meaning", "unrecognised_values": unrec}
    elif sp is not None:
        out["_status"] = status_from_speed(sp, good_mbps)
        audit["status"] = {"source_column": sp_name, "method": f"derived from speed (good >= {good_mbps} Mbps; "
                           "illustrative threshold)"}
    else:
        out["_status"] = "unknown"
        audit["status"] = {"source_column": None, "method": "none: map shows locations only"}
    audit["status"]["counts"] = {k: int((out["_status"] == k).sum()) for k in STATUS_ORDER}
    return out


def _agg(g: pd.DataFrame) -> dict:
    n = {k: int((g["_status"] == k).sum()) for k in STATUS_ORDER}
    known = len(g) - n["unknown"]
    conn = sum(n[k] for k in CONNECTED)
    return {"schools": int(len(g)), **{f"n_{k}": v for k, v in n.items()}, "n_known_status": int(known),
            "pct_connected_of_known": round(100 * conn / known, 1) if known else np.nan,
            "pct_no_connectivity_of_known": round(100 * n["no"] / known, 1) if known else np.nan,
            "median_download_mbps": round(float(g["_speed"].median()), 2) if g["_speed"].notna().any() else np.nan}


def summarise(df: pd.DataFrame, by: str | None) -> pd.DataFrame:
    """One row overall (by=None) or per group; counts stay integers."""
    if by is None:
        return pd.DataFrame([_agg(df)])
    rows = [{by: k, **_agg(g)} for k, g in df.groupby(by, dropna=False)]
    return pd.DataFrame(rows).sort_values("schools", ascending=False).reset_index(drop=True)


# --------------------------------------------------------------------------
# Boundaries (pure GeoJSON, no geopandas)
# --------------------------------------------------------------------------
def load_boundaries(path: Path, name_prop: str | None) -> tuple[dict, str]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    feats = data.get("features") or []
    if not feats:
        raise MapError(f"No features in {path}")
    props = feats[0].get("properties", {})
    prop = name_prop or next((k for k in ("shapeName", "NAME_1", "ADM1_EN", "name", "NAME", "county") if k in props), None)
    if not prop or prop not in props:
        raise MapError(f"Pass --name-prop; boundary properties are: {list(props)}")
    return data, prop


def _key(s: Any) -> str:
    t = re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower())
    prev = None
    while prev != t:   # strip stacked suffixes: "Nairobi City County" -> "nairobi"
        prev, t = t, re.sub(r"(county|region|province|district|city|state)$", "", t) or t
    return t


def join_stats(geo: dict, prop: str, stats: pd.DataFrame, unit_col: str) -> tuple[dict, dict]:
    by_key = {_key(r[unit_col]): r for _, r in stats.iterrows()}
    matched, unmatched_geo = 0, []
    for f in geo["features"]:
        r = by_key.get(_key(f["properties"].get(prop)))
        if r is None:
            unmatched_geo.append(str(f["properties"].get(prop)))
            f["properties"].update({"schools": 0, "pct_connected": None})
        else:
            matched += 1
            pc = r["pct_connected_of_known"]
            f["properties"].update({"schools": int(r["schools"]), "pct_connected": None if pd.isna(pc) else float(pc)})
    geo_keys = {_key(f["properties"].get(prop)) for f in geo["features"]}
    unmatched_data = sorted(str(r[unit_col]) for k, r in by_key.items() if k not in geo_keys)
    return geo, {"boundary_units": len(geo["features"]), "matched": matched, "unmatched_boundaries": unmatched_geo,
                 "unmatched_data_units": unmatched_data}


def _rings(geom: dict):
    if geom["type"] == "Polygon":
        yield from geom["coordinates"]
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            yield from poly


# --------------------------------------------------------------------------
# Demo data (SYNTHETIC)
# --------------------------------------------------------------------------
CENTRES = {
    "KEN": [("Nairobi", 36.82, -1.29, 1.0), ("Mombasa", 39.67, -4.05, .8), ("Kisumu", 34.77, -0.10, .6),
            ("Nakuru", 36.07, -0.30, .6), ("Eldoret", 35.27, 0.52, .5), ("Garissa", 39.64, -0.45, .3),
            ("Lodwar", 35.60, 3.12, .2), ("Nyeri", 36.95, -0.42, .5)],
    "RWA": [("Kigali", 30.06, -1.95, 1.0), ("Huye", 29.74, -2.60, .5), ("Musanze", 29.63, -1.50, .5),
            ("Rubavu", 29.26, -1.68, .4)],
    "SLE": [("Freetown", -13.23, 8.48, 1.0), ("Bo", -11.74, 7.96, .6), ("Kenema", -11.19, 7.88, .5),
            ("Makeni", -12.04, 8.89, .5)],
    "TZA": [("Dar es Salaam", 39.28, -6.80, 1.0), ("Dodoma", 35.74, -6.17, .6), ("Mwanza", 32.90, -2.52, .6),
            ("Arusha", 36.68, -3.37, .5), ("Mbeya", 33.45, -8.90, .5)],
    "UGA": [("Kampala", 32.58, 0.35, 1.0), ("Gulu", 32.30, 2.77, .4), ("Mbarara", 30.65, -0.61, .5),
            ("Mbale", 34.17, 1.08, .5), ("Jinja", 33.20, 0.43, .5)]}


def demo_schools(iso3: str, n: int = 3000, seed: int = 7) -> pd.DataFrame:
    if iso3 not in CENTRES:
        raise MapError(f"--demo supports {sorted(CENTRES)}")
    rng = np.random.default_rng(seed)
    centres = CENTRES[iso3]
    w = np.array([c[3] for c in centres])
    idx = rng.choice(len(centres), n, p=w / w.sum())
    sd = np.where(rng.random(n) < 0.6, 0.18, 0.9)       # 60% tightly around towns, 40% rural scatter
    lon = np.array([centres[i][1] for i in idx]) + rng.normal(0, 1, n) * sd
    lat = np.array([centres[i][2] for i in idx]) + rng.normal(0, 1, n) * sd
    dist = np.array([np.hypot((lon - c[1]) * 111 * np.cos(np.radians(c[2])), (lat - c[2]) * 111) for c in centres])
    near = dist.argmin(axis=0)
    d = dist.min(axis=0)
    strength = w[near]                          # bigger/better-served centres connect more schools
    p_good = 0.03 + 0.62 * strength * np.exp(-d / 30)
    p_mod = 0.12 + 0.30 * strength * np.exp(-d / 60)
    u = rng.random(n)
    status = np.where(u < p_good, "good", np.where(u < p_good + p_mod, "moderate",
                                                   np.where(u < 0.94, "no", "unknown")))
    speed = np.where(status == "good", rng.lognormal(3.3, .5, n),
                     np.where(status == "moderate", rng.lognormal(1.2, .6, n), np.nan)).round(2)
    nearest = [min(centres, key=lambda c: np.hypot(lon[i] - c[1], lat[i] - c[2]))[0] for i in range(n)]
    return pd.DataFrame({
        "school_id": [f"DEMO-{iso3}-{i:05d}" for i in range(n)], "school_name": [f"Demo school {i}" for i in range(n)],
        "latitude": lat.round(5), "longitude": lon.round(5), "admin1": nearest,
        "education_level": rng.choice(["Primary", "Secondary"], n, p=[.7, .3]),
        "environment": np.where(d < 15, "urban", "rural"), "connectivity_status": status,
        "download_speed": speed, "latency": np.where(np.isnan(speed), np.nan, (20 + 1500 / (speed + 1)).round(1)),
        "synthetic": True})


# --------------------------------------------------------------------------
# Outputs: interactive HTML + static PNG
# --------------------------------------------------------------------------
def _popup_props(row: pd.Series, cols: dict) -> dict:
    def g(k):
        c = cols.get(k)
        return "" if not c or c not in row.index or pd.isna(row[c]) else str(row[c])
    return {"School": g("name") or "(unnamed)", "Status": STATUS_LABEL[row["_status"]], "Admin": g("admin1"),
            "Level": g("level"), "Area": g("area"),
            "Download (Mbps)": "" if pd.isna(row["_speed"]) else f"{row['_speed']:.1f}",
            "Latency (ms)": "" if pd.isna(row["_latency"]) else f"{row['_latency']:.0f}"}


def make_html(df: pd.DataFrame, cols: dict, title: str, out: Path, *, geo: dict | None, geo_prop: str | None,
              max_points: int, note: str) -> dict:
    import folium
    from branca.colormap import LinearColormap
    from folium.plugins import HeatMap
    info = {"points_shown": int(len(df)), "sampled": False}
    # Open fitted to the data (any country or multi-country file). Trim the extreme 0.5% per edge so a single
    # bad coordinate cannot zoom the view out to the whole world.
    trim = [0.5, 99.5] if len(df) >= 200 else [0, 100]
    s_, n_ = np.percentile(df["_lat"], trim)
    w_, e_ = np.percentile(df["_lon"], trim)
    if n_ - s_ < 0.05:
        s_, n_ = s_ - 0.05, n_ + 0.05
    if e_ - w_ < 0.05:
        w_, e_ = w_ - 0.05, e_ + 0.05
    info["view_bounds"] = [[round(float(s_), 4), round(float(w_), 4)], [round(float(n_), 4), round(float(e_), 4)]]
    if len(df) > max_points:
        df = df.sample(max_points, random_state=0)
        info.update(points_shown=int(max_points), sampled=True)
    m = folium.Map(location=[df["_lat"].median(), df["_lon"].median()], zoom_start=6, tiles=None, prefer_canvas=True)
    # Keyless basemaps only (CartoDB tiles now need an API key and would render blank).
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap").add_to(m)
    folium.TileLayer(tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                     attr="Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics",
                     name="Satellite (Esri)", show=False).add_to(m)
    if geo and geo_prop:
        cmap = LinearColormap(["#d6342c", "#f0a30a", "#2e9e4f"], vmin=0, vmax=100,
                              caption="% of schools connected (of those with known status)")
        folium.GeoJson(geo, name="Admin units: % connected", show=True,
                       style_function=lambda f: {"fillColor": cmap(f["properties"]["pct_connected"])
                                                 if f["properties"].get("pct_connected") is not None else "#cccccc",
                                                 "color": "#555", "weight": 1, "fillOpacity": .35},
                       tooltip=folium.GeoJsonTooltip(fields=[geo_prop, "schools", "pct_connected"],
                                                     aliases=["Unit", "Schools", "% connected"])).add_to(m)
        cmap.add_to(m)
    fields = ["School", "Status", "Admin", "Level", "Area", "Download (Mbps)", "Latency (ms)"]
    for cat in STATUS_ORDER:
        sub = df[df["_status"] == cat]
        if sub.empty:
            continue
        feats = [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [float(r["_lon"]), float(r["_lat"])]},
                  "properties": _popup_props(r, cols)} for _, r in sub.iterrows()]
        folium.GeoJson({"type": "FeatureCollection", "features": feats},
                       name=f"{STATUS_LABEL[cat]} ({int((df['_status'] == cat).sum()):,})",
                       marker=folium.CircleMarker(radius=3, color=STATUS_COLOR[cat], weight=.5, fill=True,
                                                  fill_color=STATUS_COLOR[cat], fill_opacity=.85),
                       tooltip=folium.GeoJsonTooltip(fields=fields, aliases=fields, sticky=False)).add_to(m)
    no_pts = df.loc[df["_status"] == "no", ["_lat", "_lon"]].to_numpy().tolist()
    if no_pts:
        HeatMap(no_pts, name="Heatmap: schools with no connectivity", radius=14, blur=18, show=False).add_to(m)
    legend = "".join(f'<div><span style="background:{STATUS_COLOR[k]};width:11px;height:11px;display:inline-block;'
                     f'border-radius:50%;margin-right:6px"></span>{STATUS_LABEL[k]}</div>'
                     for k in STATUS_ORDER if (df["_status"] == k).any())
    m.get_root().html.add_child(folium.Element(
        f'<div style="position:fixed;top:10px;left:50px;z-index:9999;background:#fff;padding:8px 12px;'
        f'border:1px solid #bbb;border-radius:6px;font:13px/1.5 sans-serif;max-width:340px">'
        f'<b>{title}</b><br><span style="color:#666">{note}</span>{legend}</div>'))
    m.fit_bounds(info["view_bounds"], padding=(25, 25))
    folium.LayerControl(collapsed=False).add_to(m)
    out.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(out))
    return info


def make_png(df: pd.DataFrame, title: str, out: Path, geo: dict | None, by: str | None, note: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(14, 7.2), gridspec_kw={"width_ratios": [1.35, 1]})
    if geo:
        for f in geo["features"]:
            for ring in _rings(f["geometry"]):
                xs, ys = zip(*[(p[0], p[1]) for p in ring])
                ax.plot(xs, ys, color="#9aa0a6", lw=.6, zorder=1)
    for cat in ("unknown", "no", "connected", "moderate", "good"):      # good on top
        s = df[df["_status"] == cat]
        if len(s):
            ax.scatter(s["_lon"], s["_lat"], s=5, c=STATUS_COLOR[cat], alpha=.8, linewidths=0, zorder=2,
                       label=f"{STATUS_LABEL[cat]} ({len(s):,})")
    ax.set_aspect(1 / np.cos(np.radians(df["_lat"].median())))
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    handles, labels = ax.get_legend_handles_labels()
    order = [labels.index(next(l for l in labels if l.startswith(STATUS_LABEL[k]))) for k in STATUS_ORDER
             if any(l.startswith(STATUS_LABEL[k]) for l in labels)]
    ax.legend([handles[i] for i in order], [labels[i] for i in order], loc="lower left", frameon=True,
              fontsize=9, markerscale=2.2)
    ax.grid(alpha=.2)
    if by:
        top = df.groupby(by).size().sort_values(ascending=False).head(12).index
        tab = (df[df[by].isin(top)].groupby([by, "_status"]).size().unstack(fill_value=0)
               .reindex(columns=STATUS_ORDER, fill_value=0))
        tab = tab.loc[tab.sum(axis=1).sort_values().index]
        pct = tab.div(tab.sum(axis=1), axis=0) * 100
        left = np.zeros(len(pct))
        for cat in STATUS_ORDER:
            if pct[cat].sum() > 0:
                bx.barh(pct.index.astype(str), pct[cat], left=left, color=STATUS_COLOR[cat], label=STATUS_LABEL[cat])
                left += pct[cat].to_numpy()
        for i, n in enumerate(tab.sum(axis=1)):
            bx.text(101, i, f"n={n:,}", va="center", fontsize=8, color="#444")
        bx.set_xlim(0, 112)
        bx.set_xlabel("% of schools")
        bx.set_title(f"Connectivity status by {by} (largest {len(pct)})", fontsize=11)
    else:
        counts = df["_status"].value_counts().reindex(STATUS_ORDER, fill_value=0)
        bx.bar([STATUS_LABEL[k] for k in counts.index], counts.values, color=[STATUS_COLOR[k] for k in counts.index])
        bx.tick_params(axis="x", rotation=25)
        bx.set_title("Schools by connectivity status", fontsize=11)
    fig.suptitle(title, fontsize=14, fontweight="bold", y=.98)
    fig.text(.5, .01, note, ha="center", fontsize=9, color="#b00020" if "SYNTHETIC" in note else "#555")
    fig.tight_layout(rect=(0, .03, 1, .95))
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
def run(a) -> dict:
    out = Path(a.out)
    audit: dict[str, Any] = {"script_version": __version__,
                             "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                             "schema_note": "Giga API field names are unverified; columns detected heuristically."}
    overrides = {}
    for item in a.col or []:
        if "=" not in item:
            raise MapError(f"--col expects KEY=NAME, got '{item}'")
        k, v = item.split("=", 1)
        if k.strip() not in SPECS:
            raise MapError(f"Unknown key '{k}'. Valid keys: {sorted(SPECS)}")
        overrides[k.strip()] = v.strip()
    synthetic = False
    if a.demo:
        schools, synthetic = demo_schools(a.demo.upper(), a.n_demo), True
        country = a.demo.upper()
        audit["inputs"] = [f"synthetic demo ({country}, n={a.n_demo})"]
    else:
        if not a.schools:
            raise MapError("Provide --schools FILE (or --demo KEN).")
        schools = load_table(Path(a.schools))
        country = a.label or Path(a.schools).stem
        audit["inputs"] = [str(a.schools)]
    cols, alts = detect(schools, overrides)
    audit["columns_detected"], audit["alternatives"] = cols, alts
    if a.show_columns:
        print(json.dumps({"columns": list(schools.columns)[:80], "detected": cols, "alternatives": alts}, indent=2))
        return audit
    conn_cols = None
    if a.connectivity:
        conn = load_table(Path(a.connectivity))
        conn_cols, _ = detect(conn, {})
        schools = merge_connectivity(schools, conn, cols, audit)
        audit["inputs"].append(str(a.connectivity))
        audit["connectivity_columns_detected"] = conn_cols
    pts = extract_points(schools, cols, audit)
    df = build_status(pts, cols, conn_cols, a.good_mbps, audit)
    if audit["status"]["method"].startswith("none"):
        print("  note: no connectivity/status or speed column found: map shows locations only.", file=sys.stderr)

    unit = a.summary_by or cols.get("admin1")
    unit = unit if unit in df.columns else None
    out.mkdir(parents=True, exist_ok=True)
    overall = summarise(df, None)
    overall.to_csv(out / "summary_overall.csv", index=False)
    by_df = None
    if unit:
        by_df = summarise(df, unit)
        by_df.to_csv(out / f"summary_by_{re.sub(r'[^A-Za-z0-9]+', '_', unit)}.csv", index=False)
    geo, geo_prop = None, None
    if a.boundaries:
        geo, geo_prop = load_boundaries(Path(a.boundaries), a.name_prop)
        if by_df is not None:
            geo, audit["boundary_join"] = join_stats(geo, geo_prop, by_df, unit)
        else:
            audit["boundary_join"] = "no admin column to join; boundaries drawn as outlines only"
            geo_prop = None
    note = "SYNTHETIC DEMO DATA - not real Giga data" if synthetic else \
        f"Source: Giga Maps ({', '.join(Path(i).name for i in audit['inputs'])}); statuses as reported"
    title = f"{country}: school connectivity (n={len(df):,})"
    if not a.no_html:
        audit["html"] = make_html(df, cols, title, out / "schools_map.html", geo=geo if by_df is not None else None,
                                  geo_prop=geo_prop, max_points=a.max_points, note=note)
    if not a.no_png:
        make_png(df, title, out / "schools_map.png", geo, unit, note)
    audit["summary_overall"] = overall.iloc[0].to_dict()
    (out / "map_audit.json").write_text(json.dumps(audit, indent=2, default=str), encoding="utf-8")
    print(f"Wrote outputs to {out}/  (schools mapped: {len(df):,})")
    return audit


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--schools", help="schools file (.csv/.parquet/.json/.geojson)")
    ap.add_argument("--connectivity", help="optional connectivity file, joined on a shared school id")
    ap.add_argument("--demo", metavar="ISO3", help="synthetic demo data for KEN RWA SLE TZA UGA")
    ap.add_argument("--n-demo", type=int, default=3000)
    ap.add_argument("--out", default="data/maps")
    ap.add_argument("--label", help="name shown in titles (default: file name)")
    ap.add_argument("--boundaries", help="GeoJSON of admin units (e.g. geoBoundaries ADM1); adds a choropleth")
    ap.add_argument("--name-prop", help="property holding the unit name in --boundaries")
    ap.add_argument("--summary-by", help="column to summarise by (default: detected admin1)")
    ap.add_argument("--col", action="append", metavar="KEY=NAME", help=f"force a column; keys: {', '.join(SPECS)}")
    ap.add_argument("--good-mbps", type=float, default=20.0,
                    help="ONLY used when there is no status column: speed >= this is 'good' (illustrative, not official)")
    ap.add_argument("--max-points", type=int, default=15000, help="cap points in the HTML (sampled) to keep it fast")
    ap.add_argument("--show-columns", action="store_true", help="print detected columns and exit")
    ap.add_argument("--no-html", action="store_true")
    ap.add_argument("--no-png", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    return ap


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.WARNING, format="%(levelname)s: %(message)s")
    try:
        run(a)
    except MapError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except ImportError as e:
        print(f"error: missing dependency: {e}. Install: pip install pandas numpy matplotlib folium", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
