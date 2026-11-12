#!/usr/bin/env python3
"""
Find notable changes in each region's time series and write <ISO3>.changes.json next to the
dashboard bundle (read by admin1_explorer.js to highlight shifts on the map and charts).

Method (kept simple on purpose, every setting is visible and changeable)
  For each region and metric, compare the average of the latest WINDOW months ("now") with the average
  of an earlier window of the same length ("before"), where "before" ends K months earlier
  (K = 3, 6, 12; 12 compares like-for-like months a year apart, which damps seasonality).
  Only months with enough tests count (months flagged low_sample are ignored).
  A change is marked only if BOTH hold:
    1. it is large relative to the region's own usual month-to-month variation (z >= z_min), and
    2. it is large in absolute terms (relative change >= rel_min), so very stable regions don't flag
       trivial moves.
  Also reported: "new" (usable data appeared where there was none) and "missing" (it vanished).
  Restated past figures (revisions) are a different thing and are not handled here.

Honest limits
  - z_min / rel_min are PROVISIONAL tuning values, not validated cutoffs. With the defaults, simulated
    stable series with 10% random noise were wrongly marked about 3 times in 100 checks; expect more where
    data are seasonal or autocorrelated, and with many regions x metrics a few false marks are normal
    (run with --simulate to measure the rate for your settings).
  - "Usual variation" is estimated from the region's own history, so it needs --min-history valid months.
    Regions with less history are skipped and counted, never guessed at.
  - A mark is a measured change in speed-test data. It says nothing about why.

Usage
  python build_changes.py [--dest out/dashboard] [--window 3] [--since 3m 6m 12m]
                          [--z-min 2.5] [--rel-min 0.10] [--min-valid 2] [--min-history 8]
  python build_changes.py --simulate        # false-mark rate on synthetic stable series
Settings can also live in config.json under "changes".
"""
import argparse
import datetime
import json
import math
import random
import statistics
import sys
from pathlib import Path

DEFAULTS = {"window": 3, "since": ["3m", "6m", "12m"], "z_min": 2.5, "rel_min": 0.10,
            "min_valid": 2, "min_history": 8}


def mi(period):
    y, m = period.split("-")[:2]
    return int(y) * 12 + int(m)


def label(n):
    return f"{(n - 1) // 12}-{(n - 1) % 12 + 1:02d}"


def level_noise(points):
    """Month-to-month noise of a region's level, from first differences of consecutive months."""
    diffs = [b[1] - a[1] for a, b in zip(points, points[1:]) if b[0] - a[0] == 1]
    if len(diffs) < 3:
        return None
    med = statistics.median(diffs)
    mad = statistics.median(abs(d - med) for d in diffs)
    return 1.4826 * mad / math.sqrt(2)


def compare(points, latest, k, p, higher_is_better, cur_low=0):
    """-> (record or None, status) where status in ok / short_history."""
    W = p["window"]
    base_hi = latest - k
    cur = [v for m, v in points if latest - W + 1 <= m <= latest]
    base = [v for m, v in points if base_hi - W + 1 <= m <= base_hi]
    now_p, before_p = [label(latest - W + 1), label(latest)], [label(base_hi - W + 1), label(base_hi)]
    if len(cur) >= p["min_valid"] and not base:
        return {"type": "new", "fromPeriods": before_p, "toPeriods": now_p}, "ok"
    if len(base) >= p["min_valid"] and not cur:
        return {"type": "missing", "reason": "too_few_tests" if cur_low else "no_data",
                "fromPeriods": before_p, "toPeriods": now_p}, "ok"
    if len(cur) < p["min_valid"] or len(base) < p["min_valid"]:
        return None, "ok"
    if len(points) < p["min_history"]:
        return None, "short_history"
    sigma = level_noise(points)
    if sigma is None:
        return None, "short_history"
    mc, mb = statistics.mean(cur), statistics.mean(base)
    sigma = max(sigma, 0.02 * abs(mb), 1e-9)
    se = sigma * math.sqrt(1 / len(cur) + 1 / len(base))
    delta = mc - mb
    z = abs(delta) / se
    rel = abs(delta) / abs(mb) if mb else float("inf")
    if z < p["z_min"] or rel < p["rel_min"]:
        return None, "ok"
    effect = "neutral" if higher_is_better is None else ("improved" if (delta > 0) == higher_is_better else "worsened")
    return {"type": "shift", "direction": "up" if delta > 0 else "down", "effect": effect,
            "from": round(mb, 3), "to": round(mc, 3), "usual": [round(mb - 2 * sigma, 3), round(mb + 2 * sigma, 3)],
            "strength": round(z, 2), "relChange": round(rel, 3), "nFrom": len(base), "nTo": len(cur),
            "fromPeriods": before_p, "toPeriods": now_p}, "ok"


def build_country(series, metrics, p):
    periods = series["periods"]
    if not periods:
        return None
    latest = max(mi(x) for x in periods)
    out = {k: [] for k in p["since"]}
    short = set()
    for sid, sh in series["shapes"].items():
        for mid, arr in sh["metrics"].items():
            spec = metrics.get(mid)
            if not spec or spec.get("static") or len(arr) != len(periods):
                continue
            lows = sh["low"].get(spec.get("source"), [0] * len(periods))
            pts = sorted((mi(per), v) for per, v, lo in zip(periods, arr, lows) if v is not None and not lo)
            cur_low = sum(1 for per, v, lo in zip(periods, arr, lows)
                          if v is not None and lo and latest - p["window"] + 1 <= mi(per) <= latest)
            for key in p["since"]:
                k = int(key[:-1])
                rec, status = compare(pts, latest, k, p, spec.get("higher_is_better"), cur_low)
                if status == "short_history":
                    short.add((sid, mid))
                if rec:
                    out[key].append({"shapeId": sid, "metric": mid, **rec})
    for key in out:
        out[key].sort(key=lambda r: (r["type"] != "shift", -r.get("strength", 0)))
    return {"iso3": series["iso3"], "built": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "latest_period": label(latest), "params": {k: p[k] for k in ("window", "z_min", "rel_min", "min_valid", "min_history")},
            "since": out, "skipped_short_history": len(short)}


def simulate(p, n=2000, months=24, cv=0.10, seed=7):
    rng = random.Random(seed)
    flagged = {k: 0 for k in p["since"]}
    for _ in range(n):
        pts = [(i, max(0.01, rng.gauss(100, 100 * cv))) for i in range(1, months + 1)]
        for key in p["since"]:
            rec, _ = compare(pts, months, int(key[:-1]), p, True)
            flagged[key] += bool(rec and rec["type"] == "shift")
    print(f"Stable synthetic series (noise {cv:.0%} of level, {months} months, no real change), settings "
          f"z_min={p['z_min']}, rel_min={p['rel_min']}:")
    for k, v in flagged.items():
        print(f"  vs {k}: {v / n:.1%} wrongly marked")


def main():
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=str(here / "config.json"))
    ap.add_argument("--dest", default="out/dashboard")
    ap.add_argument("--window", type=int)
    ap.add_argument("--since", nargs="+")
    ap.add_argument("--z-min", type=float)
    ap.add_argument("--rel-min", type=float)
    ap.add_argument("--min-valid", type=int)
    ap.add_argument("--min-history", type=int)
    ap.add_argument("--simulate", action="store_true")
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8")) if Path(a.config).exists() else {}
    p = {**DEFAULTS, **cfg.get("changes", {})}
    for k, v in (("window", a.window), ("since", a.since), ("z_min", a.z_min), ("rel_min", a.rel_min),
                 ("min_valid", a.min_valid), ("min_history", a.min_history)):
        if v is not None:
            p[k] = v
    for key in p["since"]:
        if not key.endswith("m") or int(key[:-1]) < p["window"]:
            sys.exit(f"--since '{key}' must look like 6m and be at least as long as the window ({p['window']}m)")
    if a.simulate:
        return simulate(p)

    dest = Path(a.dest)
    man = json.loads((dest / "manifest.json").read_text(encoding="utf-8"))
    metrics = {m["id"]: m for m in man["metrics"]}
    for c in man["countries"]:
        series = json.loads((dest / f"{c['iso3']}.series.json").read_text(encoding="utf-8"))
        res = build_country(series, metrics, p)
        if not res:
            print(f"{c['iso3']}: no periods, skipped")
            continue
        (dest / f"{c['iso3']}.changes.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
        counts = ", ".join(f"{k}: {sum(r['type'] == 'shift' for r in v)} shifts, "
                           f"{sum(r['type'] != 'shift' for r in v)} coverage" for k, v in res["since"].items())
        print(f"{c['iso3']} (latest {res['latest_period']}): {counts}; {res['skipped_short_history']} region-metrics "
              f"skipped for short history")


if __name__ == "__main__":
    main()
