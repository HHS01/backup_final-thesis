#!/usr/bin/env python3
"""
M-Lab "Monthly Stats" -> small, rolling, per-country tables. Raw files are never kept.

How it works
  M-Lab publishes one Parquet file per calendar month per slice (e.g.
  downloads_by_country_subdivision1), listed in a public manifest. For each month
  we download the file to a temp location, read ONLY the columns and countries we
  need, append the result to a small CSV, and delete the download. So you never
  store the archive, only your countries x months.

Commands
  manifest             list slices / months the manifest offers (run this first to verify names)
  backfill             (re)build the rolling window: the latest N months for every configured slice
  update               scheduled job: fetch only new months (+ re-fetch the latest stored month to
                       catch revisions). Rebuilds the window if you add a country or slice.

Config (config.json)
  "countries": ISO3 or ISO2 codes (shared with the other fetchers; ISO3 -> ISO2 via World Bank, cached)
  "mlab": {"slices": [...], "percentiles": [...], "metrics": [...], "history_months": 36,
           "min_sample_count": 100, "refresh_last": 1}

Examples
  python fetch_mlab.py manifest
  python fetch_mlab.py backfill --months 24
  python fetch_mlab.py update
  python fetch_mlab.py update --countries KEN RWA UGA     # a new country triggers a window rebuild

Outputs (in <out>/mlab/)
  <slice>.csv          period (YYYY-MM), id columns, sample_count, selected metric columns, low_sample
  <slice>.state.json   which months/countries have been fetched (drives `update`)

Needs: pandas, pyarrow.  Note: rows with few tests are unreliable (M-Lab suggests ~100+);
they are kept and flagged in `low_sample`, not dropped.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

MANIFEST_URL = "https://raw.githubusercontent.com/m-lab/iqb/main/data/state/ghremote/manifest.json"
PATH_RE = re.compile(r"cache/v\d+/(\d{8}T\d{6}Z)/(\d{8}T\d{6}Z)/([^/]+)/data\.parquet$")
TS = "%Y%m%dT%H%M%SZ"
ID_COLS = ["country_code", "asn", "as_name", "subdivision1_iso_code", "subdivision1_name", "city"]
WB_COUNTRY_API = "https://api.worldbank.org/v2/country"
UA = {"User-Agent": "edtech-ssa-fetch/0.1"}


# ----------------------------------------------------------------- network
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


def download(url, dest, retries=4, pause=1.5):
    last = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r, \
                    open(dest, "wb") as f:
                shutil.copyfileobj(r, f)
            return
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            time.sleep(pause * 2 ** i)
    raise RuntimeError(f"Download failed after {retries} tries: {url}\n  {last}")


# ----------------------------------------------------------------- manifest
def load_manifest(url):
    return json.loads(fetch_bytes(url))


def index_manifest(manifest):
    """-> {slice: {'YYYY-MM': {'url':..., 'size':...}}}, monthly files only."""
    files = manifest.get("files") if isinstance(manifest, dict) else None
    if not isinstance(files, dict):
        keys = list(manifest)[:10] if isinstance(manifest, dict) else type(manifest).__name__
        sys.exit(f"Unexpected manifest layout (no 'files' mapping). Top-level: {keys}")
    idx = defaultdict(dict)
    for path, meta in files.items():
        m = PATH_RE.search(path)
        if not m:
            continue
        s, e, slc = m.groups()
        try:
            sd, ed = datetime.datetime.strptime(s, TS), datetime.datetime.strptime(e, TS)
        except ValueError:
            continue
        nxt = (sd.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        if sd.day != 1 or ed.date() != nxt.date():  # skip anything that isn't one calendar month
            continue
        url = meta.get("url") if isinstance(meta, dict) else None
        if url:
            size = meta.get("size") or meta.get("size_bytes") if isinstance(meta, dict) else None
            idx[slc][sd.strftime("%Y-%m")] = {"url": url, "size": size}
    return idx


# ----------------------------------------------------------------- countries
def resolve_iso2(codes, cache_path):
    """ISO3 (or ISO2) codes -> ISO2, using World Bank country metadata, cached locally."""
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    out, need = {}, []
    for c in codes:
        if len(c) == 2:
            out[c] = c
        elif c in cache:
            out[c] = cache[c]
        else:
            need.append(c)
    if need:
        data = json.loads(fetch_bytes(f"{WB_COUNTRY_API}/{';'.join(need)}?format=json&per_page=100"))
        found = {r["id"]: r["iso2Code"] for r in (data[1] if isinstance(data, list) and len(data) > 1 and data[1] else [])}
        missing = [c for c in need if c not in found]
        if missing:
            sys.exit(f"Unknown country codes (use ISO3 or ISO2): {missing}")
        cache.update(found)
        out.update({c: found[c] for c in need})
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, indent=1))
    return {c: out[c].upper() for c in codes}


# ----------------------------------------------------------------- one month, one slice
def fetch_month(url, iso2s, metrics, percentiles, min_sample):
    import pyarrow.parquet as pq  # lazy: lets --help / manifest work without the libs
    tmp = tempfile.NamedTemporaryFile(suffix=".parquet", delete=False)
    tmp.close()
    try:
        download(url, tmp.name)
        names = pq.ParquetFile(tmp.name).schema_arrow.names
        if "country_code" not in names:
            raise RuntimeError(f"No country_code column in file; columns are {names}")
        wanted_metrics = {f"{m}_p{p}" for m in metrics for p in percentiles}
        cols = [c for c in names if c in ID_COLS or c == "sample_count" or c in wanted_metrics]
        df = pq.read_table(tmp.name, columns=cols, filters=[("country_code", "in", sorted(iso2s))]).to_pandas()
    finally:
        os.unlink(tmp.name)
    if "sample_count" in df.columns:
        df["low_sample"] = df["sample_count"] < min_sample
    return df


# ----------------------------------------------------------------- store
def merge_into_store(csv_path, new_df, fetched_periods, history):
    import pandas as pd
    if csv_path.exists():
        old = pd.read_csv(csv_path, keep_default_na=False, na_values=[""])
        old = old[~old["period"].isin(fetched_periods)]
        df = pd.concat([old, new_df], ignore_index=True) if len(new_df) else old
    else:
        df = new_df
    if df is None or not len(df):
        return df
    keep = sorted(df["period"].unique())[-history:]
    df = df[df["period"].isin(keep)]
    ids = [c for c in ID_COLS if c in df.columns]
    df = df.sort_values(ids + ["period"]).reset_index(drop=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    return df


def plan_months(mode, avail_months, state, countries, history, refresh_last):
    window = sorted(avail_months)[-history:]
    if mode == "backfill" or not state or not set(countries) <= set(state.get("countries", [])):
        return window, True
    have = set(state.get("periods", []))
    new = [m for m in window if m not in have]
    refresh = sorted(have & set(window))[-refresh_last:] if refresh_last > 0 else []
    return sorted(set(new) | set(refresh)), False


def run(mode, cfg, countries, out, manifest_url, months_override, refresh_override):
    import pandas as pd
    mc = cfg.get("mlab", {})
    slices = mc.get("slices") or sys.exit("config.json needs mlab.slices (run `manifest` to see names)")
    metrics = mc.get("metrics", ["download", "upload", "latency", "loss"])
    pcts = mc.get("percentiles", [10, 25, 50, 75, 90])
    history = months_override or mc.get("history_months", 36)
    refresh_last = mc.get("refresh_last", 1) if refresh_override is None else refresh_override
    min_sample = mc.get("min_sample_count", 100)

    base = Path(out) / "mlab"
    iso2 = resolve_iso2(countries, base / "iso2_map.json")
    iso2s = sorted(set(iso2.values()))
    print("Countries:", ", ".join(f"{k}->{v}" for k, v in iso2.items()))

    idx = index_manifest(load_manifest(manifest_url))
    for slc in slices:
        print(f"\n[{slc}]")
        if slc not in idx:
            print(f"  ! slice not in manifest. Available: {sorted(idx)}", file=sys.stderr)
            continue
        state_path, csv_path = base / f"{slc}.state.json", base / f"{slc}.csv"
        state = json.loads(state_path.read_text()) if state_path.exists() else None
        todo, full = plan_months(mode, idx[slc].keys(), state, iso2s, history, refresh_last)
        if not todo:
            print("  up to date (no new months).")
            continue
        if full and mode == "update":
            print("  new country/slice or first run: rebuilding the full window.")
        print(f"  months to fetch: {todo[0]} .. {todo[-1]} ({len(todo)})")
        frames = []
        for mon in todo:
            df = fetch_month(idx[slc][mon]["url"], iso2s, metrics, pcts, min_sample)
            df.insert(0, "period", mon)
            frames.append(df)
            print(f"  {mon}: {len(df)} rows kept")
        new_df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
        final = merge_into_store(csv_path, new_df, set(todo), history)
        periods = sorted(set((state or {}).get("periods", [])) | set(todo))[-history:]
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps({"countries": iso2s, "periods": periods,
                                          "updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")},
                                         indent=1))
        if final is not None and len(final):
            low = final["low_sample"].mean() * 100 if "low_sample" in final else float("nan")
            print(f"  store: {len(final)} rows, {final['period'].nunique()} months, "
                  f"{final['country_code'].nunique()} countries, {low:.0f}% rows flagged low_sample")
            missing = set(iso2s) - set(final["country_code"].unique())
            if missing:
                print(f"  ! no rows at all for: {sorted(missing)} (absent from M-Lab files this period)")


def cmd_manifest(manifest_url):
    idx = index_manifest(load_manifest(manifest_url))
    if not idx:
        sys.exit("No monthly files recognised. Paths expected like cache/v1/<start>/<end>/<slice>/data.parquet")
    for slc in sorted(idx):
        months = sorted(idx[slc])
        sizes = [v["size"] for v in idx[slc].values() if isinstance(v["size"], (int, float))]
        sz = f", ~{sum(sizes) / len(sizes) / 1e6:.1f} MB/file avg" if sizes else ""
        print(f"{slc:44s} {len(months):4d} months  {months[0]} .. {months[-1]}{sz}")


def main():
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["manifest", "backfill", "update"])
    ap.add_argument("--config", default=str(here / "indicators_config.json"))
    ap.add_argument("--countries", nargs="+", help="ISO3/ISO2 codes; overrides config")
    ap.add_argument("--months", type=int, help="window length in months; overrides config")
    ap.add_argument("--refresh-last", type=int, help="months already stored to re-fetch on update")
    ap.add_argument("--out", default="out")
    ap.add_argument("--manifest-url", default=MANIFEST_URL)
    a = ap.parse_args()

    if a.command == "manifest":
        return cmd_manifest(a.manifest_url)
    cfg = json.load(open(a.config, encoding="utf-8"))
    countries = [c.upper() for c in (a.countries or cfg["countries"])]
    run(a.command, cfg, countries, a.out, a.manifest_url, a.months, a.refresh_last)


if __name__ == "__main__":
    main()
