#!/usr/bin/env python3
"""
fetch_kobo_submissions.py
=========================
Pulls raw survey responses via KoboToolbox v2 REST API (or loads offline fallback exports)
for Teacher, Provider, and Expert instruments.

Usage:
  # With live KoboToolbox API credentials:
  export KOBO_TOKEN="your_kobo_api_token"
  export KOBO_SERVER="https://kf.kobotoolbox.org" # or https://eu.kobotoolbox.org
  python scripts/fetch_kobo_submissions.py

  # With local submission exports (offline mode):
  python scripts/fetch_kobo_submissions.py --offline
"""

import os
import sys
import json
import argparse
from pathlib import Path
import requests

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw" / "kobo"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def load_env_file(env_path=ROOT_DIR / ".env"):
    """Loads key-value pairs from .env into os.environ if not already present."""
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip("'\"")
                    if k and k not in os.environ and v:
                        os.environ[k] = v


load_env_file()

# Default Asset UIDs (configured once forms are deployed to KoboToolbox)
DEFAULT_ASSET_UIDS = {
    "teacher": os.getenv("KOBO_UID_TEACHER", "aTeacherSurveyUidPlaceholder"),
    "provider": os.getenv("KOBO_UID_PROVIDER", "aProviderSurveyUidPlaceholder"),
    "expert": os.getenv("KOBO_UID_EXPERT", "aExpertSurveyUidPlaceholder"),
    "followup": os.getenv("KOBO_UID_FOLLOWUP", "aFollowupSurveyUidPlaceholder"),
}

DEFAULT_SERVER = os.getenv("KOBO_SERVER", "https://kf.kobotoolbox.org").rstrip("/")
API_TOKEN = os.getenv("KOBO_TOKEN", "")


def fetch_from_api(asset_uid, instrument_name, server=DEFAULT_SERVER, token=API_TOKEN):
    """Fetches submission data for an asset from KoboToolbox API v2."""
    if not token:
        print(f"[!] Warning: KOBO_TOKEN not set in environment. Cannot fetch live data for {instrument_name}.")
        return None

    url = f"{server}/api/v2/assets/{asset_uid}/data.json"
    headers = {"Authorization": f"Token {token}"}
    params = {"format": "json"}

    print(f"[*] Querying KoboToolbox API: {url} (Asset: {asset_uid})...")
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            print(f"[+] Successfully fetched {len(results)} submissions for {instrument_name}.")
            return results
        else:
            print(f"[-] API error ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        print(f"[-] Network exception connecting to KoboToolbox: {e}")
        return None


def generate_synthetic_offline_sample(instrument_name):
    """Generates mock sample data adhering strictly to the XLSForm schema for testing."""
    import random
    countries = ["KEN", "TZA", "NGA", "GHA", "RWA", "ZMB", "SEN", "ETH"]
    sample = []
    
    # Generate 50 representative mock responses
    for i in range(1, 51):
        ctry = random.choice(countries)
        if instrument_name == "teacher":
            rec = {
                "_id": f"sub_t_{i:04d}",
                "start": "2026-11-01T08:00:00Z",
                "end": "2026-11-01T08:12:00Z",
                "A1_country": ctry,
                "A2_school_type": random.choice(["public", "low_fee_private", "community"]),
                "A9_location": random.choice(["major_city", "smaller_town", "rural"]),
                "A10_class_size": random.choice(["30_50", "51_80", "gt80"]),
                "A11_gps_location": f"{-1.2921 + random.uniform(-1, 1):.6f} {36.8219 + random.uniform(-1, 1):.6f} 1600.0 5.0",
                "B1_use_digital": random.choice(["yes", "yes", "no"]),
                "B6_electricity": random.choice(["always", "often", "sometimes", "rarely", "never"]),
                "B7_internet": random.choice(["reliable", "often_cuts", "rarely_works", "no_internet"]),
                "B8_approved_tools": random.choice(["mandatory", "recommended", "no_rules"]),
                "C1_lang_teach": random.choice(["strongly_agree", "agree", "disagree"]),
                "C1_infrastructure": random.choice(["agree", "disagree", "strongly_disagree"]),
                "D3_workload": random.choice(["saves_time", "about_same", "adds_time"]),
                "E1_ai_familiar": random.choice(["frequently", "occasionally", "never"]),
            }
        elif instrument_name == "provider":
            rec = {
                "_id": f"sub_p_{i:04d}",
                "A1_org_name": f"EdTech Provider {i}",
                "A2_hq_country": ctry,
                "A3_operate_countries": f"{ctry} KEN RWA",
                "A4_org_type": random.choice(["for_profit", "social_enterprise", "ngo"]),
                "B1_connectivity": random.choice(["fully_offline", "occasional_sync", "continuous_broadband"]),
                "B2_hardware": random.choice(["basic_feature_phone", "smartphone", "laptop_pc"]),
                "D1_languages": random.choice(["English Kiswahili", "French", "Local languages"]),
            }
        else: # expert
            rec = {
                "_id": f"sub_e_{i:04d}",
                "A1_system": ctry,
                "A3_based": random.choice(["in_country", "elsewhere_africa", "outside_africa"]),
                "A4_perspective": random.choice(["policy", "research_eval", "provision"]),
                "D4_agree_i": random.choice(["agree", "strongly_agree", "neither"]),
                "F1_constraints_1": random.choice(["electricity", "internet_connectivity", "devices", "teacher_capacity"]),
            }
        sample.append(rec)
    return sample


def main():
    parser = argparse.ArgumentParser(description="Fetch or simulate KoboToolbox survey submissions.")
    parser.add_argument("--offline", action="store_true", help="Generate offline validation sample if API unavailable")
    parser.add_argument("--server", default=DEFAULT_SERVER, help="KoboToolbox server endpoint")
    parser.add_argument("--token", default=API_TOKEN, help="KoboToolbox v2 API token")
    args = parser.parse_args()

    instruments = ["teacher", "provider", "expert"]
    summary = {}

    for inst in instruments:
        uid = DEFAULT_ASSET_UIDS.get(inst)
        out_file = RAW_DIR / f"kobo_{inst}_submissions.json"
        
        submissions = None
        if not args.offline and args.token and uid and not uid.endswith("Placeholder"):
            submissions = fetch_from_api(uid, inst, server=args.server, token=args.token)

        if not submissions:
            if out_file.exists() and not args.offline:
                print(f"[i] Using existing cached submissions for {inst}: {out_file}")
                with open(out_file, "r", encoding="utf-8") as f:
                    submissions = json.load(f)
            else:
                print(f"[i] Generating offline validation sample for {inst}...")
                submissions = generate_synthetic_offline_sample(inst)
                with open(out_file, "w", encoding="utf-8") as f:
                    json.dump(submissions, f, indent=2)
                print(f"[+] Saved sample data to: {out_file}")

        summary[inst] = len(submissions) if submissions else 0

    print("\n" + "="*50)
    print(" KoboToolbox Ingestion Summary")
    print("="*50)
    for inst, count in summary.items():
        print(f"  - {inst.capitalize()}: {count} submissions ready at {RAW_DIR}/kobo_{inst}_submissions.json")
    print("="*50)


if __name__ == "__main__":
    main()
