#!/usr/bin/env python3
"""
Small SQLite history store shared by the fetch scripts.

Tables
  observations  one row per (source, iso3, indicator, year); current value + first/last seen
  changes       append-only log: new / revised / missing / restored
  runs          one row per fetch run, with the scope it covered and the data version

Why a change log: statistics agencies revise past years, so "only fetch the latest
year" would silently miss revisions. For small annual datasets the cheap, correct
approach is to refetch a recent window each run and diff it against what is stored.

CLI
  python store.py export --db edtech.db --out out/     # observations.csv, changes.csv, runs.csv
  python store.py changes --db edtech.db [--limit 30]  # recent changes
"""
import argparse
import csv
import datetime
import json
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS observations(
  source TEXT, iso3 TEXT, indicator TEXT, label TEXT, year INTEGER, value REAL,
  status TEXT DEFAULT 'active', first_seen TEXT, last_seen TEXT, data_version TEXT,
  PRIMARY KEY(source, iso3, indicator, year));
CREATE TABLE IF NOT EXISTS changes(
  changed_at TEXT, source TEXT, iso3 TEXT, indicator TEXT, year INTEGER,
  change TEXT, old_value REAL, new_value REAL, data_version TEXT);
CREATE TABLE IF NOT EXISTS runs(
  run_at TEXT, source TEXT, data_version TEXT, n_rows INTEGER,
  n_new INTEGER, n_revised INTEGER, n_unchanged INTEGER, n_missing INTEGER, scope TEXT);
"""


def connect(db_path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    con.executescript(SCHEMA)
    return con


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def last_run(db_path, source):
    """Most recent run for a source as {'data_version', 'scope'} or None."""
    con = connect(db_path)
    row = con.execute("SELECT data_version, scope FROM runs WHERE source=? ORDER BY rowid DESC LIMIT 1",
                      (source,)).fetchone()
    con.close()
    if not row:
        return None
    return {"data_version": row[0], "scope": json.loads(row[1]) if row[1] else {}}


def upsert(db_path, source, rows, data_version, scope):
    """
    rows: dicts with iso3, indicator, label, year, value.
    scope: {'countries': [...], 'indicators': [...], 'start': int, 'end': int} describing what
           this run attempted to cover (used to flag values that vanished from the source).
    Returns counts.
    """
    ts = now()
    con = connect(db_path)
    cur = con.cursor()
    n_new = n_rev = n_same = 0
    seen = set()

    def log(change, iso3, ind, yr, old, new):
        cur.execute("INSERT INTO changes VALUES (?,?,?,?,?,?,?,?,?)",
                    (ts, source, iso3, ind, yr, change, old, new, data_version))

    for r in rows:
        try:
            val, yr = float(r["value"]), int(r["year"])
        except (TypeError, ValueError, KeyError):
            continue
        key = (source, r["iso3"], r["indicator"], yr)
        seen.add(key)
        ex = cur.execute("SELECT value, status FROM observations "
                         "WHERE source=? AND iso3=? AND indicator=? AND year=?", key).fetchone()
        if ex is None:
            cur.execute("INSERT INTO observations VALUES (?,?,?,?,?,?,?,?,?,?)",
                        (*key[:3], r.get("label", ""), yr, val, "active", ts, ts, data_version))
            log("new", key[1], key[2], yr, None, val)
            n_new += 1
        else:
            old, status = ex
            if abs(old - val) > 1e-9:
                cur.execute("UPDATE observations SET value=?, status='active', last_seen=?, data_version=? "
                            "WHERE source=? AND iso3=? AND indicator=? AND year=?",
                            (val, ts, data_version, *key))
                log("revised", key[1], key[2], yr, old, val)
                n_rev += 1
            else:
                cur.execute("UPDATE observations SET status='active', last_seen=? "
                            "WHERE source=? AND iso3=? AND indicator=? AND year=?", (ts, *key))
                if status == "missing":
                    log("restored", key[1], key[2], yr, None, val)
                n_same += 1

    # values stored earlier, inside this run's scope, but absent from the source now
    n_missing = 0
    for iso3, ind, yr, old in cur.execute(
            "SELECT iso3, indicator, year, value FROM observations WHERE source=? AND status='active' "
            "AND year BETWEEN ? AND ?", (source, scope["start"], scope["end"])).fetchall():
        if iso3 in scope["countries"] and ind in scope["indicators"] and (source, iso3, ind, yr) not in seen:
            cur.execute("UPDATE observations SET status='missing' "
                        "WHERE source=? AND iso3=? AND indicator=? AND year=?", (source, iso3, ind, yr))
            log("missing", iso3, ind, yr, old, None)
            n_missing += 1

    cur.execute("INSERT INTO runs VALUES (?,?,?,?,?,?,?,?,?)",
                (ts, source, data_version, len(seen), n_new, n_rev, n_same, n_missing, json.dumps(scope)))
    con.commit()
    con.close()
    return {"new": n_new, "revised": n_rev, "unchanged": n_same, "missing": n_missing}


def export(db_path, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    con = connect(db_path)
    for table, order in (("observations", "source, iso3, indicator, year"),
                         ("changes", "changed_at DESC"), ("runs", "rowid DESC")):
        cur = con.execute(f"SELECT * FROM {table} ORDER BY {order}")
        with open(out / f"{table}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([d[0] for d in cur.description])
            w.writerows(cur.fetchall())
        print(f"wrote {out / (table + '.csv')}")
    con.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["export", "changes"])
    ap.add_argument("--db", default="edtech.db")
    ap.add_argument("--out", default="out")
    ap.add_argument("--limit", type=int, default=30)
    a = ap.parse_args()
    if a.command == "export":
        export(a.db, a.out)
    else:
        con = connect(a.db)
        for r in con.execute("SELECT changed_at, source, iso3, indicator, year, change, old_value, new_value "
                             "FROM changes ORDER BY rowid DESC LIMIT ?", (a.limit,)):
            print(" | ".join("" if x is None else str(x) for x in r))


if __name__ == "__main__":
    main()
