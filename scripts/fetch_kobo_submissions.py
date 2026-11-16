#!/usr/bin/env python3
"""
Fetch all four KoboToolbox survey instruments.

Live submissions require explicit Kobo configuration and an output directory
outside the repository. Synthetic records are available only with --demo (or
the legacy --offline alias) and are written to a separate demo directory.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse

import requests

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DEMO_DIR = ROOT_DIR / "data" / "demo" / "kobo"


def load_env_file(env_path=ROOT_DIR / ".env"):
    """Load key-value pairs from .env without overriding existing variables."""
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    key, value = key.strip(), value.strip().strip("'\"")
                    if key and key not in os.environ and value:
                        os.environ[key] = value


load_env_file()

ASSET_UIDS = {
    "teacher": os.getenv("KOBO_UID_TEACHER", ""),
    "provider": os.getenv("KOBO_UID_PROVIDER", ""),
    "expert": os.getenv("KOBO_UID_EXPERT", ""),
    "followup": os.getenv("KOBO_UID_FOLLOWUP", ""),
}
KOBO_SERVER = os.getenv("KOBO_SERVER", "").rstrip("/")
KOBO_TOKEN = os.getenv("KOBO_TOKEN", "")
INSTRUMENTS = ("teacher", "provider", "expert", "followup")


def fetch_from_api(asset_uid, instrument_name, server, token):
    """Fetch every paginated submission for one Kobo asset or raise an error."""
    endpoint = f"{server}/api/v2/assets/{quote(asset_uid, safe='')}/data.json"
    headers = {"Authorization": f"Token {token}"}
    next_url = endpoint
    results = []
    seen_urls = set()
    server_origin = (urlparse(server).scheme, urlparse(server).netloc)

    while next_url:
        if next_url in seen_urls:
            raise RuntimeError(f"Kobo pagination loop while fetching {instrument_name}.")
        seen_urls.add(next_url)

        try:
            response = requests.get(
                next_url,
                headers=headers,
                params={"format": "json"} if next_url == endpoint else None,
                timeout=30,
            )
        except requests.RequestException as exc:
            raise RuntimeError(f"Network error fetching {instrument_name} submissions.") from exc

        if response.status_code != 200:
            raise RuntimeError(
                f"Kobo API returned HTTP {response.status_code} for {instrument_name} submissions."
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(f"Kobo returned invalid JSON for {instrument_name} submissions.") from exc

        page_results = payload.get("results") if isinstance(payload, dict) else None
        if not isinstance(page_results, list) or not all(isinstance(row, dict) for row in page_results):
            raise RuntimeError(f"Kobo returned an unexpected response schema for {instrument_name}.")
        results.extend(page_results)

        next_page = payload.get("next")
        if next_page is not None and not isinstance(next_page, str):
            raise RuntimeError(f"Kobo returned an invalid pagination link for {instrument_name}.")
        if next_page:
            response_url = getattr(response, "url", None) or next_url
            next_url = urljoin(response_url, next_page)
            next_origin = (urlparse(next_url).scheme, urlparse(next_url).netloc)
            if next_origin != server_origin:
                raise RuntimeError(f"Kobo returned an unexpected pagination host for {instrument_name}.")
        else:
            next_url = None

    print(f"{instrument_name.capitalize()}: fetched {len(results)} submissions.")
    return results


def generate_synthetic_demo_sample(instrument_name):
    """Generate clearly marked demo records; never used by the live workflow."""
    import random

    countries = ["KEN", "TZA", "NGA", "GHA", "RWA", "ZMB", "SEN", "ETH"]
    sample = []
    for i in range(1, 51):
        country = random.choice(countries)
        if instrument_name == "teacher":
            record = {
                "_id": f"demo_teacher_{i:04d}",
                "A1_country": country,
                "A2_school_type": random.choice(["public", "low_fee_private", "community"]),
                "A9_location": random.choice(["major_city", "smaller_town", "rural"]),
                "B1_use_digital": random.choice(["yes", "yes", "no"]),
                "B6_electricity": random.choice(["always", "often", "sometimes", "rarely", "never"]),
                "B7_internet": random.choice(["reliable", "often_cuts", "rarely_works", "no_internet"]),
                "B8_approved_tools": random.choice(["mandatory", "recommended", "no_rules"]),
                "C1_lang_teach": random.choice(["strongly_agree", "agree", "disagree"]),
                "D3_workload": random.choice(["saves_time", "about_same", "adds_time"]),
                "E1_ai_familiar": random.choice(["frequently", "occasionally", "never"]),
            }
        elif instrument_name == "provider":
            record = {
                "_id": f"demo_provider_{i:04d}",
                "A1_org_name": f"Demo EdTech Provider {i}",
                "A2_hq_country": country,
                "A3_operate_countries": f"{country} KEN RWA",
                "A4_org_type": random.choice(["for_profit", "social_enterprise", "ngo"]),
                "B1_connectivity": random.choice(["fully_offline", "occasional_sync", "continuous_broadband"]),
                "B2_hardware": random.choice(["basic_feature_phone", "smartphone", "laptop_pc"]),
                "D1_languages": random.choice(["English Kiswahili", "French", "Local languages"]),
            }
        else:
            record = {
                "_id": f"demo_expert_{i:04d}",
                "A1_system": country,
                "A3_based": random.choice(["in_country", "elsewhere_africa", "outside_africa"]),
                "A4_perspective": random.choice(["policy", "research_eval", "provision"]),
                "D4_agree_i": random.choice(["agree", "strongly_agree", "neither"]),
                "F1_constraints_1": random.choice(
                    ["electricity", "internet_connectivity", "devices", "teacher_capacity"]
                ),
            }
        record["_synthetic"] = True
        sample.append(record)
    return sample


def resolve_output_dir(raw_path, demo):
    if demo:
        output_dir = Path(raw_path) if raw_path else DEFAULT_DEMO_DIR
        output_dir = output_dir.expanduser().resolve()
        if output_dir.is_relative_to((ROOT_DIR / "data" / "raw").resolve()):
            raise ValueError("Demo submissions must not be written under data/raw.")
        return output_dir

    if not raw_path:
        raise ValueError("Live fetches require --output-dir outside the repository.")
    output_dir = Path(raw_path).expanduser().resolve()
    if output_dir == ROOT_DIR or ROOT_DIR in output_dir.parents:
        raise ValueError("Live submissions must be written outside the repository.")
    return output_dir


def validate_live_configuration(server, token, asset_uids):
    missing = []
    if not token:
        missing.append("KOBO_TOKEN")
    if not server:
        missing.append("KOBO_SERVER")
    for instrument in INSTRUMENTS:
        uid = asset_uids.get(instrument, "")
        if not uid or "placeholder" in uid.lower():
            missing.append(f"KOBO_UID_{instrument.upper()}")
    if missing:
        raise ValueError("Missing or invalid Kobo configuration: " + ", ".join(missing))

    parsed_server = urlparse(server)
    if parsed_server.scheme != "https" or not parsed_server.netloc:
        raise ValueError("KOBO_SERVER must be an HTTPS Kobo server URL.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Fetch or explicitly generate Kobo survey data.")
    parser.add_argument("--server", default=None, help="Kobo server URL; otherwise KOBO_SERVER is required.")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory. Required for live data and must be outside the repository.",
    )
    parser.add_argument(
        "--demo",
        "--offline",
        dest="demo",
        action="store_true",
        help="Explicitly generate synthetic demo records in data/demo/kobo (never a live fallback).",
    )
    args = parser.parse_args(argv)

    if args.demo:
        try:
            output_dir = resolve_output_dir(args.output_dir, demo=True)
        except ValueError as exc:
            parser.error(str(exc))
        submissions = {
            instrument: (
                [] if instrument == "followup" else generate_synthetic_demo_sample(instrument)
            )
            for instrument in INSTRUMENTS
        }
        output_dir.mkdir(parents=True, exist_ok=True)
        for instrument, records in submissions.items():
            output_file = output_dir / f"kobo_{instrument}_submissions.json"
            output_file.write_text(json.dumps(records, indent=2), encoding="utf-8")
            print(f"DEMO ONLY — {instrument.capitalize()}: {len(records)} records -> {output_file}")
        return

    server = (args.server or KOBO_SERVER).rstrip("/")
    try:
        validate_live_configuration(server, KOBO_TOKEN, ASSET_UIDS)
        output_dir = resolve_output_dir(args.output_dir, demo=False)
    except ValueError as exc:
        parser.error(str(exc))

    submissions = {}
    try:
        for instrument in INSTRUMENTS:
            submissions[instrument] = fetch_from_api(
                ASSET_UIDS[instrument], instrument, server=server, token=KOBO_TOKEN
            )
    except RuntimeError as exc:
        print(f"ERROR: Kobo ingestion stopped: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    output_dir.mkdir(parents=True, exist_ok=True)
    for instrument, records in submissions.items():
        output_file = output_dir / f"kobo_{instrument}_submissions.json"
        output_file.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"{instrument.capitalize()}: wrote {len(records)} submissions.")


if __name__ == "__main__":
    main()
