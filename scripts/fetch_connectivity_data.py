#!/usr/bin/env python3
"""
fetch_connectivity_data.py
==========================
Retrieve open connectivity / affordability data relevant to EdTech access:

  giga        Giga Maps school locations + connectivity (UNICEF-ITU). Needs an
              API token you request from Giga; endpoint paths are CONFIGURABLE
              because they could not be verified (docs are a JS app).
  gsma        Download GSMA report PDFs (free direct links) and extract every
              sentence with a connectivity/affordability statistic, with page.
  itu-prices  Load an ITU DataHub CSV export of ICT price baskets (% of GNI
              per capita): the open, country-level affordability source.
  ookla       Speedtest by Ookla open tiles (AWS S3, no account) for one
              country/quarter; optionally aggregated to admin units you supply.
  mlab        M-Lab NDT speed tests from BigQuery (free; needs a Google Cloud
              project) aggregated by month x region/city for one country.

Each command writes CSV(s) under --out and appends to manifest.jsonl.

LICENCE WARNINGS (read before reuse)
  * Ookla open data is CC BY-NC-SA 4.0: non-commercial, share-alike, attribution.
  * GSMA reports are copyright GSMA: fine for research reading/citation; do not
    redistribute the PDFs. This script stores only your local copy.
  * Giga/ITU/M-Lab: check each source's current terms of use.

Install: pip install pandas numpy requests pyarrow shapely pdfplumber
         (+ google-cloud-bigquery for `mlab`)
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

__version__ = "1.0.0"
log = logging.getLogger("connectivity")
UA = "connectivity-fetcher/1.0 (academic research)"


class FetchError(Exception):
    """A problem the user must fix (missing token, bad file, bad argument)."""


# --------------------------------------------------------------------------
# Shared helpers
# --------------------------------------------------------------------------
def _session():
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=Retry(total=4, backoff_factor=1.5,
                                                       status_forcelist=(429, 500, 502, 503, 504),
                                                       allowed_methods=("GET",))))
    s.headers["User-Agent"] = UA
    return s


def manifest(out: Path, source: str, url: str, note: str, nbytes: int | None = None, rows: int | None = None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    rec = {"source": source, "url": url, "licence_note": note, "bytes": nbytes, "rows": rows,
           "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "script_version": __version__}
    with open(out / "manifest.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def save_csv(df: pd.DataFrame, out: Path, name: str) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    p = out / name
    df.to_csv(p, index=False)
    print(f"  wrote {p}  ({len(df)} rows)")
    return p


# --------------------------------------------------------------------------
# 1. Giga Maps (token-based; paths configurable)
# --------------------------------------------------------------------------
GIGA_NOTE = "Giga open data via API on request; check Giga terms. https://maps.giga.global/docs/explore-api"
# UNVERIFIED defaults: the docs page is JavaScript-rendered and could not be read.
# Confirm paths/pagination in the docs you get with your API access and override.
GIGA_PATHS = {"schools": "schools_location/country/{iso3}", "connectivity": "schools_connectivity/country/{iso3}"}
_WRAP_KEYS = ("data", "results", "items", "schools", "records")


def unwrap(payload: Any) -> tuple[list[dict], str | None]:
    """Return (rows, next_url) from a list or a {data|results|...: [...]} response."""
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)], None
    if isinstance(payload, dict):
        nxt = payload.get("next") if isinstance(payload.get("next"), str) else None
        for k in _WRAP_KEYS:
            v = payload.get(k)
            if isinstance(v, list):
                return [r for r in v if isinstance(r, dict)], nxt
            if isinstance(v, dict):  # nested {"data": {"results": [...]}}
                rows, n2 = unwrap(v)
                if rows:
                    return rows, n2 or nxt
    return [], None


def giga_fetch(session, base_url: str, path_tpl: str, iso3: str, headers: dict, page_size: int = 1000,
               max_pages: int = 500, sleep: float = 0.3) -> list[dict]:
    """Page through one endpoint. Follows a 'next' URL if present, otherwise page/size params.
    Stops on an empty page, a short page, or a page identical to the previous one."""
    url = base_url.rstrip("/") + "/" + path_tpl.format(iso3=iso3).lstrip("/")
    rows: list[dict] = []
    prev_sig = None
    params: dict | None = {"page": 1, "size": page_size}
    for page in range(1, max_pages + 1):
        r = session.get(url, params=params, headers=headers, timeout=60)
        if r.status_code in (401, 403):
            raise FetchError(f"Giga API returned {r.status_code}: token missing/invalid or no access to {iso3}.")
        if r.status_code == 404:
            raise FetchError(f"Giga API 404 for {url}: the path template is probably wrong; set --schools-path / "
                             "--connectivity-path from the API docs.")
        r.raise_for_status()
        chunk, nxt = unwrap(r.json())
        if not chunk:
            break
        sig = json.dumps(chunk[0], sort_keys=True, default=str)
        if sig == prev_sig:
            log.warning("Giga page %d repeats the previous page; the endpoint may ignore page/size. Stopping.", page)
            break
        prev_sig = sig
        rows += chunk
        if nxt:
            url, params = nxt, None
        elif len(chunk) < page_size:
            break
        else:
            params = {"page": page + 1, "size": page_size}
        time.sleep(sleep)
    return rows


def run_giga(a) -> None:
    token = os.environ.get(a.token_env, "")
    base = a.base_url or os.environ.get("GIGA_API_BASE", "")
    if not token or not base:
        raise FetchError(f"Giga needs an API token and base URL. Request access at https://maps.giga.global "
                         f"(see its API docs), then export {a.token_env}=... and GIGA_API_BASE=... (or --base-url).")
    headers = {"Authorization": a.auth_template.format(token=token)} if "{token}" in a.auth_template else \
        {a.auth_template.split(":")[0].strip(): token}
    iso3, out = a.country.upper(), Path(a.out)
    s = _session()
    for name, tpl in (("schools", a.schools_path), ("connectivity", a.connectivity_path)):
        if not tpl:
            continue
        print(f"Giga {name} for {iso3}")
        rows = giga_fetch(s, base, tpl, iso3, headers, a.page_size)
        if not rows:
            print(f"  no rows returned for {name}")
            continue
        df = pd.json_normalize(rows)
        save_csv(df, out, f"giga_{name}_{iso3}.csv")
        manifest(out, f"giga_{name}", f"{base.rstrip('/')}/{tpl.format(iso3=iso3)}", GIGA_NOTE, rows=len(df))
        if a.summarise_by and a.summarise_by in df.columns:
            save_csv(df.groupby(a.summarise_by, dropna=False).size().rename("schools").reset_index(), out,
                     f"giga_{name}_{iso3}_by_{a.summarise_by}.csv")


# --------------------------------------------------------------------------
# 2. GSMA reports (free direct-link PDFs) -> statistic sentences with pages
# --------------------------------------------------------------------------
GSMA_NOTE = "GSMA copyright. Local research copy only; cite the report; do not redistribute."
GSMA_PDFS = [  # direct links seen in search results; the Africa 2025/2026 editions sit behind a registration form
    "https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/wp-content/uploads/2024/11/"
    "GSMA_ME_SSA_2024_Web.pdf",
    "https://www.gsma.com/r/wp-content/uploads/2023/10/State-of-Mobile-Internet-Connectivity-2023-Sub-Saharan-Africa.pdf",
]
STAT_RX = re.compile(r"\d[\d.,]*\s?(%|per cent|percent|mbps|gb\b|million|billion|bn\b|m\b|usd|us\$)|[$\u20ac]\s?\d", re.I)
TOPIC_RX = re.compile(r"coverage|usage gap|afford|smartphone|handset|\bdata\b|4g|5g|3g|broadband|penetration|"
                      r"subscriber|internet|speed|income|gdp", re.I)


def extract_statistics(pdf_path: Path, topic_only: bool = True) -> pd.DataFrame:
    import pdfplumber
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for pno, page in enumerate(pdf.pages, start=1):
            flat = re.sub(r"\s+", " ", page.extract_text() or "")
            for s in re.split(r"(?<=[.!?])\s+", flat):
                if 25 < len(s) < 500 and STAT_RX.search(s) and (not topic_only or TOPIC_RX.search(s)):
                    rows.append({"file": pdf_path.name, "pdf_page": pno, "sentence": s.strip()})
    return pd.DataFrame(rows, columns=["file", "pdf_page", "sentence"])


def run_gsma(a) -> None:
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    frames = []
    sess = _session()
    sources = list(a.pdf or []) + list(a.url or ([] if a.pdf else GSMA_PDFS))
    for src in sources:
        path = Path(src)
        if not path.exists():  # treat as URL
            path = out / Path(src.split("?")[0]).name
            if not path.exists():
                r = sess.get(src, timeout=120)
                if r.status_code in (401, 403) or "pdf" not in r.headers.get("content-type", "").lower():
                    print(f"  could not download {src} (HTTP {r.status_code}). Download it manually in a browser "
                          f"and pass the file with --pdf.", file=sys.stderr)
                    continue
                path.write_bytes(r.content)
                manifest(out, "gsma_pdf", src, GSMA_NOTE, nbytes=len(r.content))
        frames.append(extract_statistics(path, topic_only=not a.all_sentences))
    if frames:
        save_csv(pd.concat(frames, ignore_index=True), out, "gsma_statistics.csv")


# --------------------------------------------------------------------------
# 3. ITU DataHub export (price baskets) -- best-effort schema detection
# --------------------------------------------------------------------------
ITU_NOTE = "ITU DataHub terms of use apply; cite as 'ITU DataHub, https://datahub.itu.int/' with access date."


def _pick(cols: list[str], *patterns: str) -> str | None:
    for p in patterns:
        for c in cols:
            if re.search(p, c, re.I):
                return c
    return None


def load_itu_prices(path: Path, iso3: list[str] | None) -> pd.DataFrame:
    if not path.exists():
        raise FetchError(f"ITU file not found: {path}")
    df = pd.read_csv(path, low_memory=False)
    cols = list(df.columns)
    c_iso = _pick(cols, r"iso.?3|^code$|entity.?code|economy.?code")
    c_name = _pick(cols, r"^(entity|country|economy)(.?name)?$", r"country|economy|entity")
    c_year = _pick(cols, r"^(year|period|time.?period|date)$", r"year|period")
    c_ind = _pick(cols, r"indicator.?name|^indicator$|series|basket", r"indicator")
    c_val = _pick(cols, r"^(value|data.?value|obs.?value)$", r"value")
    missing = [n for n, c in (("year", c_year), ("indicator", c_ind), ("value", c_val)) if c is None]
    if missing or not (c_iso or c_name):
        raise FetchError(f"Could not identify columns {missing or ['country']} in {path.name}; columns are {cols}. "
                         "Expected a long-format DataHub export (country, year, indicator, value).")
    out = pd.DataFrame({"country": df[c_name] if c_name else df[c_iso], "iso3": df[c_iso] if c_iso else None,
                        "year": pd.to_numeric(df[c_year].astype(str).str.extract(r"(\d{4})")[0], errors="coerce"),
                        "indicator": df[c_ind], "value": pd.to_numeric(df[c_val], errors="coerce")})
    out = out.dropna(subset=["year", "value"])
    if iso3:
        if c_iso:
            out = out[out["iso3"].astype(str).str.upper().isin([c.upper() for c in iso3])]
        else:
            logging.warning("No ISO3 column; --countries ignored (filter by name yourself).")
    return out.reset_index(drop=True)


def run_itu(a) -> None:
    out = Path(a.out)
    df = load_itu_prices(Path(a.input), a.countries)
    save_csv(df, out, "itu_price_baskets_long.csv")
    key = "iso3" if df["iso3"].notna().any() else "country"
    latest = df.sort_values("year").groupby([key, "indicator"]).tail(1)
    wide = latest.pivot(index=key, columns="indicator", values="value")
    save_csv(wide.reset_index(), out, "itu_price_baskets_latest_wide.csv")
    manifest(out, "itu_datahub", str(a.input), ITU_NOTE, rows=len(df))


# --------------------------------------------------------------------------
# 4. Ookla open data tiles
# --------------------------------------------------------------------------
OOKLA_NOTE = ("CC BY-NC-SA 4.0 (non-commercial, share-alike). Cite: Speedtest by Ookla Global Fixed and Mobile "
              "Network Performance Maps, based on analysis by Ookla of Speedtest Intelligence data; "
              "https://registry.opendata.aws/speedtest-global-performance")
OOKLA_BUCKET = "ookla-open-data"
OOKLA_REGION = "us-west-2"
OOKLA_COLS = ["quadkey", "avg_d_kbps", "avg_u_kbps", "avg_lat_ms", "tests", "devices"]
# APPROXIMATE country boxes (min_lon, min_lat, max_lon, max_lat): verify, or pass --bbox / --boundaries.
BBOX = {"KEN": (33.9, -4.7, 41.9, 5.5), "TZA": (29.3, -11.8, 40.5, -0.9), "UGA": (29.5, -1.5, 35.0, 4.3),
        "RWA": (28.8, -2.9, 30.9, -1.0), "SLE": (-13.4, 6.9, -10.2, 10.0), "NER": (0.1, 11.7, 16.0, 23.5),
        "ZWE": (25.2, -22.5, 33.1, -15.6), "GHA": (-3.3, 4.7, 1.2, 11.2), "NGA": (2.7, 4.2, 14.7, 13.9),
        "ETH": (33.0, 3.4, 48.0, 14.9), "SEN": (-17.6, 12.3, -11.3, 16.7), "ZMB": (21.9, -18.1, 33.7, -8.2),
        "MWI": (32.7, -17.2, 35.9, -9.3)}
_QMONTH = {1: "01", 2: "04", 3: "07", 4: "10"}


def ookla_key(kind: str, year: int, quarter: int) -> str:
    if kind not in ("fixed", "mobile") or quarter not in _QMONTH:
        raise FetchError("--type must be fixed|mobile and --quarter 1-4")
    return (f"parquet/performance/type={kind}/year={year}/quarter={quarter}/"
            f"{year}-{_QMONTH[quarter]}-01_performance_{kind}_tiles.parquet")


def quadkey_to_xyz(qk: str) -> tuple[int, int, int]:
    x = y = 0
    z = len(qk)
    for i, ch in enumerate(qk):
        mask = 1 << (z - i - 1)
        d = int(ch)
        if d & 1:
            x |= mask
        if d & 2:
            y |= mask
    return x, y, z


def tile_center(x: np.ndarray, y: np.ndarray, z: int) -> tuple[np.ndarray, np.ndarray]:
    n = 2.0 ** z
    lon = (x + 0.5) / n * 360.0 - 180.0
    lat = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * (y + 0.5) / n))))
    return lon, lat


def quadkeys_to_lonlat(qks: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    """Vectorised centroid of Bing-style quadkeys (all keys must share one zoom level)."""
    arr = qks.astype(str).to_numpy()
    z = len(arr[0]) if len(arr) else 0
    if len(arr) == 0:
        return np.array([]), np.array([])
    if not all(len(q) == z for q in arr[:1000]) or qks.str.len().nunique() != 1:
        raise FetchError("Quadkeys have mixed lengths; expected one zoom level (Ookla uses zoom 16).")
    digits = np.frombuffer("".join(arr).encode("ascii"), dtype=np.uint8).reshape(len(arr), z) - 48
    xs = np.zeros(len(arr), dtype=np.int64)
    ys = np.zeros(len(arr), dtype=np.int64)
    for i in range(z):
        shift = z - i - 1
        xs |= ((digits[:, i] & 1).astype(np.int64)) << shift
        ys |= (((digits[:, i] >> 1) & 1).astype(np.int64)) << shift
    return tile_center(xs, ys, z)


def lonlat_to_xy(lon: float, lat: float, z: int) -> tuple[int, int]:
    n = 2 ** z
    x = int(math.floor((lon + 180.0) / 360.0 * n))
    y = int(math.floor((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n))
    return min(max(x, 0), n - 1), min(max(y, 0), n - 1)


def xy_to_quadkey(x: int, y: int, z: int) -> str:
    out = []
    for i in range(z, 0, -1):
        mask = 1 << (i - 1)
        out.append(str((1 if x & mask else 0) + (2 if y & mask else 0)))
    return "".join(out)


def bbox_prefixes(bbox: tuple[float, float, float, float], z: int = 8) -> set[str]:
    x0, y1 = lonlat_to_xy(bbox[0], bbox[1], z)   # south-west -> max y
    x1, y0 = lonlat_to_xy(bbox[2], bbox[3], z)   # north-east -> min y
    return {xy_to_quadkey(x, y, z) for x in range(min(x0, x1), max(x0, x1) + 1)
            for y in range(min(y0, y1), max(y0, y1) + 1)}


def select_tiles(tbl: pd.DataFrame, bbox: tuple[float, float, float, float], prefix_zoom: int = 8) -> pd.DataFrame:
    """Keep tiles whose centroid lies in bbox; adds lon/lat. Prefix test first (cheap) then exact box."""
    pre = bbox_prefixes(bbox, prefix_zoom)
    sub = tbl[tbl["quadkey"].str[:prefix_zoom].isin(pre)].copy()
    lon, lat = quadkeys_to_lonlat(sub["quadkey"])
    sub["lon"], sub["lat"] = lon, lat
    m = (sub.lon >= bbox[0]) & (sub.lon <= bbox[2]) & (sub.lat >= bbox[1]) & (sub.lat <= bbox[3])
    return sub[m].reset_index(drop=True)


def read_ookla(kind: str, year: int, quarter: int, local_file: str | None) -> pd.DataFrame:
    import pyarrow.parquet as pq
    if local_file:
        pf = pq.ParquetFile(local_file)
    else:
        from pyarrow import fs
        s3 = fs.S3FileSystem(anonymous=True, region=OOKLA_REGION)
        pf = pq.ParquetFile(s3.open_input_file(f"{OOKLA_BUCKET}/{ookla_key(kind, year, quarter)}"))
    have = set(pf.schema_arrow.names)
    cols = [c for c in OOKLA_COLS if c in have]
    if "quadkey" not in have:
        raise FetchError(f"Ookla file has no 'quadkey' column (columns: {sorted(have)}).")
    return pf.read(columns=cols).to_pandas()


def load_boundaries(path: Path, name_prop: str | None) -> tuple[list, list[str], str]:
    """Polygons + unit names from GeoJSON (e.g. geoBoundaries ADM1 'shapeName')."""
    from shapely.geometry import shape
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    feats = data.get("features", [])
    if not feats:
        raise FetchError(f"No features in boundaries file {path}")
    props0 = feats[0].get("properties", {})
    prop = name_prop or next((k for k in ("shapeName", "NAME_1", "ADM1_EN", "name", "NAME", "county", "COUNTY")
                              if k in props0), None)
    if prop is None or prop not in props0:
        raise FetchError(f"Pass --name-prop; properties available: {list(props0)}")
    return [shape(f["geometry"]) for f in feats], [str(f["properties"].get(prop)) for f in feats], prop


def assign_units(tiles: pd.DataFrame, geoms: list, names: list[str]) -> pd.DataFrame:
    import shapely
    from shapely import STRtree
    pts = shapely.points(tiles["lon"].to_numpy(), tiles["lat"].to_numpy())
    pairs = STRtree(geoms).query(pts, predicate="within")      # [point_idx, geom_idx]
    first = pd.DataFrame({"i": pairs[0], "g": pairs[1]}).drop_duplicates("i")
    unit = pd.Series([None] * len(tiles), dtype=object)
    unit.iloc[first["i"].to_numpy()] = [names[g] for g in first["g"]]
    out = tiles.copy()
    out["unit"] = unit.to_numpy()
    return out


def summarise_tiles(tiles: pd.DataFrame, by: str | None = None) -> pd.DataFrame:
    """Test-weighted means (Ookla's tiles are already averages) + tile median. Mbps/ms."""
    def agg(g: pd.DataFrame) -> pd.Series:
        t = g["tests"].astype(float)
        tot = t.sum()
        wm = lambda c: float((g[c] * t).sum() / tot) if tot > 0 else np.nan
        return pd.Series({"tiles": len(g), "tests": int(tot), "devices_sum_upper_bound": int(g["devices"].sum()),
                          "download_mbps_testweighted": round(wm("avg_d_kbps") / 1000, 2),
                          "upload_mbps_testweighted": round(wm("avg_u_kbps") / 1000, 2),
                          "latency_ms_testweighted": round(wm("avg_lat_ms"), 1),
                          "download_mbps_median_tile": round(float(g["avg_d_kbps"].median()) / 1000, 2)})
    if by is None:
        return agg(tiles).to_frame().T
    return tiles.dropna(subset=[by]).groupby(by).apply(agg, include_groups=False).reset_index()


def run_ookla(a) -> None:
    iso3, out = a.country.upper(), Path(a.out)
    geoms = names = None
    bbox = tuple(a.bbox) if a.bbox else BBOX.get(iso3)
    if a.boundaries:
        geoms, names, prop = load_boundaries(Path(a.boundaries), a.name_prop)
        from shapely.ops import unary_union
        bbox = bbox or tuple(unary_union(geoms).bounds)
        print(f"  {len(names)} admin units from {a.boundaries} (name property '{prop}')")
    if bbox is None:
        raise FetchError(f"No bounding box for {iso3}: pass --bbox MINLON MINLAT MAXLON MAXLAT or --boundaries.")
    print(f"Ookla {a.type} {a.year} Q{a.quarter} for {iso3}; bbox={bbox}")
    tiles = select_tiles(read_ookla(a.type, a.year, a.quarter, a.local_file), bbox)
    if tiles.empty:
        raise FetchError("No tiles inside the bounding box. Check the bbox, or that the quarter exists.")
    if geoms:
        tiles = assign_units(tiles, geoms, names)
        tiles = tiles.dropna(subset=["unit"]).reset_index(drop=True)   # drop tiles outside the polygons
    tag = f"{iso3}_{a.type}_{a.year}Q{a.quarter}"
    save_csv(tiles, out, f"ookla_tiles_{tag}.csv")
    save_csv(summarise_tiles(tiles), out, f"ookla_country_{tag}.csv")
    if geoms:
        save_csv(summarise_tiles(tiles, by="unit"), out, f"ookla_by_unit_{tag}.csv")
    manifest(out, "ookla_open_data", f"s3://{OOKLA_BUCKET}/{ookla_key(a.type, a.year, a.quarter)}", OOKLA_NOTE,
             rows=len(tiles))


# --------------------------------------------------------------------------
# 5. M-Lab NDT (BigQuery)
# --------------------------------------------------------------------------
MLAB_NOTE = "M-Lab open data (BigQuery public dataset). Check M-Lab's current data licence/terms; cite M-Lab NDT."
MLAB_TABLE = "measurement-lab.ndt.unified_downloads"
# Region field: M-Lab docs show client.Geo.Region (ISO 3166-2) and forum queries use Subdivision1Name; confirm
# which exists in your table with --dry-run and override with --region-field.
MLAB_REGION_FIELD = "client.Geo.Subdivision1Name"


def build_mlab_sql(table: str, level: str, region_field: str, min_tests: int) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_.\-]+", table) or not re.fullmatch(r"[A-Za-z0-9_.]+", region_field):
        raise FetchError("Table / field names may only contain letters, digits, '.', '_' and '-'.")
    region = region_field if level in ("region", "city") else "CAST(NULL AS STRING)"
    city = "client.Geo.City" if level == "city" else "CAST(NULL AS STRING)"
    return f"""SELECT
  FORMAT_DATE('%Y-%m', date) AS month,
  {region} AS region,
  {city} AS city,
  COUNT(*) AS tests,
  ROUND(AVG(a.MeanThroughputMbps), 2) AS mean_download_mbps,
  ROUND(APPROX_QUANTILES(a.MeanThroughputMbps, 100)[OFFSET(50)], 2) AS median_download_mbps,
  ROUND(APPROX_QUANTILES(a.MinRTT, 100)[OFFSET(50)], 1) AS median_min_rtt_ms,
  ROUND(AVG(a.LossRate), 4) AS mean_loss_rate,
  COUNT(DISTINCT client.Network.ASNumber) AS n_asn
FROM `{table}`
WHERE date BETWEEN @start AND @end
  AND client.Geo.CountryCode = @cc
GROUP BY month, region, city
HAVING tests >= {int(min_tests)}
ORDER BY month, region, city"""


def run_mlab(a) -> None:
    sql = build_mlab_sql(a.table, a.level, a.region_field, a.min_tests)
    cc = a.country.upper()
    if len(cc) != 2:
        raise FetchError("M-Lab uses ISO2 country codes, e.g. KE, TZ, UG, RW, SL.")
    print(sql.replace("@start", f"'{a.start}'").replace("@end", f"'{a.end}'").replace("@cc", f"'{cc}'"))
    try:
        from google.cloud import bigquery
    except ImportError as e:
        raise FetchError("Install google-cloud-bigquery and authenticate (gcloud auth application-default login) "
                         "to run this query. The SQL above can also be pasted into the BigQuery console.") from e
    client = bigquery.Client(project=a.project)
    cfg = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("start", "DATE", a.start), bigquery.ScalarQueryParameter("end", "DATE", a.end),
        bigquery.ScalarQueryParameter("cc", "STRING", cc)], dry_run=a.dry_run, use_query_cache=True)
    job = client.query(sql, job_config=cfg)
    if a.dry_run:
        print(f"Dry run OK: this query would process {job.total_bytes_processed / 1e9:.2f} GB.")
        return
    df = pd.DataFrame([dict(r) for r in job.result()])
    save_csv(df, Path(a.out), f"mlab_ndt_{cc}_{a.level}_{a.start}_{a.end}.csv")
    manifest(Path(a.out), "mlab_ndt_bigquery", a.table, MLAB_NOTE, rows=len(df))
    print("  NOTE: M-Lab locations are IP-geolocated (coarse); sub-national estimates are indicative, and mobile "
          "users are often placed at the carrier's gateway city.")


# --------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-v", "--verbose", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("giga", help="Giga Maps schools + connectivity (needs token)")
    g.add_argument("--country", required=True, help="ISO3, e.g. KEN")
    g.add_argument("--out", default="data/connectivity")
    g.add_argument("--base-url", help="API base URL (or env GIGA_API_BASE)")
    g.add_argument("--token-env", default="GIGA_API_TOKEN", help="env var holding your API token")
    g.add_argument("--auth-template", default="Authorization: Bearer {token}",
                   help="header template; UNVERIFIED default")
    g.add_argument("--schools-path", default=GIGA_PATHS["schools"], help="UNVERIFIED default; use {iso3}")
    g.add_argument("--connectivity-path", default=GIGA_PATHS["connectivity"], help="UNVERIFIED default; '' to skip")
    g.add_argument("--page-size", type=int, default=1000)
    g.add_argument("--summarise-by", help="also write counts grouped by this returned column")

    m = sub.add_parser("gsma", help="download GSMA PDFs and extract statistic sentences")
    m.add_argument("--out", default="data/connectivity/gsma")
    m.add_argument("--url", action="append", help="PDF URL (repeatable); default: two verified direct links")
    m.add_argument("--pdf", action="append", help="local PDF file(s), e.g. manually downloaded editions")
    m.add_argument("--all-sentences", action="store_true", help="keep every sentence with a number")

    i = sub.add_parser("itu-prices", help="load an ITU DataHub price-basket CSV export")
    i.add_argument("--input", required=True)
    i.add_argument("--out", default="data/connectivity")
    i.add_argument("--countries", nargs="+", help="ISO3 codes to keep")

    o = sub.add_parser("ookla", help="Ookla open tiles for one country/quarter")
    o.add_argument("--country", required=True, help="ISO3")
    o.add_argument("--year", type=int, required=True)
    o.add_argument("--quarter", type=int, required=True, choices=[1, 2, 3, 4])
    o.add_argument("--type", choices=["fixed", "mobile"], default="mobile")
    o.add_argument("--out", default="data/connectivity")
    o.add_argument("--bbox", nargs=4, type=float, metavar=("MINLON", "MINLAT", "MAXLON", "MAXLAT"))
    o.add_argument("--boundaries", help="GeoJSON of admin units (e.g. geoBoundaries ADM1) for per-unit summaries")
    o.add_argument("--name-prop", help="property holding the unit name")
    o.add_argument("--local-file", help="use an already-downloaded parquet instead of reading from S3")

    b = sub.add_parser("mlab", help="M-Lab NDT monthly aggregates from BigQuery")
    b.add_argument("--country", required=True, help="ISO2, e.g. KE")
    b.add_argument("--start", required=True, help="YYYY-MM-DD")
    b.add_argument("--end", required=True, help="YYYY-MM-DD")
    b.add_argument("--project", help="your Google Cloud project id (billing for query bytes)")
    b.add_argument("--level", choices=["country", "region", "city"], default="region")
    b.add_argument("--table", default=MLAB_TABLE)
    b.add_argument("--region-field", default=MLAB_REGION_FIELD)
    b.add_argument("--min-tests", type=int, default=30)
    b.add_argument("--dry-run", action="store_true", help="validate and report bytes, no data returned")
    b.add_argument("--out", default="data/connectivity")
    return ap


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.WARNING, format="%(levelname)s: %(message)s")
    try:
        {"giga": run_giga, "gsma": run_gsma, "itu-prices": run_itu, "ookla": run_ookla, "mlab": run_mlab}[a.cmd](a)
    except FetchError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except ImportError as e:
        print(f"error: missing dependency: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
