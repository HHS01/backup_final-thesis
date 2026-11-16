#!/usr/bin/env python3
"""Build a public-safe dashboard aggregate from temporary Kobo exports."""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import re
import sys
from pathlib import Path


SUPPRESSION_THRESHOLD = 5

COUNTRY_NAMES = {
    "AGO": "Angola", "BEN": "Benin", "BWA": "Botswana",
    "BFA": "Burkina Faso", "BDI": "Burundi", "CPV": "Cabo Verde",
    "CMR": "Cameroon", "CAF": "Central African Republic", "TCD": "Chad",
    "COM": "Comoros", "COD": "Congo, Dem. Rep.", "COG": "Congo, Rep.",
    "CIV": "Cote d'Ivoire", "GNQ": "Equatorial Guinea", "ERI": "Eritrea",
    "SWZ": "Eswatini", "ETH": "Ethiopia", "GAB": "Gabon",
    "GMB": "Gambia, The", "GHA": "Ghana", "GIN": "Guinea",
    "GNB": "Guinea-Bissau", "KEN": "Kenya", "LSO": "Lesotho",
    "LBR": "Liberia", "MDG": "Madagascar", "MWI": "Malawi",
    "MLI": "Mali", "MRT": "Mauritania", "MUS": "Mauritius",
    "MOZ": "Mozambique", "NAM": "Namibia", "NER": "Niger",
    "NGA": "Nigeria", "RWA": "Rwanda", "STP": "Sao Tome and Principe",
    "SEN": "Senegal", "SYC": "Seychelles", "SLE": "Sierra Leone",
    "SOM": "Somalia, Fed. Rep.", "ZAF": "South Africa",
    "SSD": "South Sudan", "SDN": "Sudan", "TZA": "Tanzania",
    "TGO": "Togo", "UGA": "Uganda", "ZMB": "Zambia", "ZWE": "Zimbabwe",
}

OPTIONS = {
    "location": {
        "major_city": "A major city",
        "smaller_town": "A smaller town",
        "rural": "A rural area",
    },
    "electricity": {
        "reliable_mains": "Reliable mains power",
        "mains_cuts": "Mains power with frequent cuts",
        "solar_generator": "Solar or generator only",
        "none": "No electricity",
        "dont_know": "Don't know",
    },
    "internet": {
        "no_access": "No access",
        "unreliable": "Unreliable",
        "mostly_reliable": "Mostly reliable",
        "fully_reliable": "Fully reliable",
    },
    "workload": {
        "reduce_it_a_lot": "Reduces workload a lot",
        "reduce_it_a_little": "Reduces workload a little",
        "no_difference": "No difference",
        "add_a_little": "Adds a little workload",
        "add_a_lot": "Adds a lot of workload",
    },
    "offline": {
        "fully_offline": "Fully offline",
        "partly": "Partly offline",
        "needs_connection": "Needs a connection",
    },
    "device": {
        "basic_phone": "Basic phone",
        "low_cost_smartphone": "Low-cost smartphone",
        "tablet_computer": "Tablet or computer",
        "supplied_device": "Dedicated supplied device",
        "no_personal_device": "No personal device",
    },
    "data_payer": {
        "users_pay": "Users pay",
        "zero_rated": "Zero-rated for users",
        "we_or_programme": "Provider or programme pays",
        "not_applicable": "Not applicable",
    },
    "evidence": {
        "usage_data": "Usage and engagement data",
        "user_feedback": "User feedback or surveys",
        "own_outcome_study": "Provider's own outcome study",
        "independent_evaluation": "Independent evaluation",
        "rct_comparison": "Randomised or comparison-group study",
        "none_yet": "None yet",
        "other": "Other",
    },
    "decision_driver": {
        "ministry": "Ministry or national agency",
        "other_gov": "Other government bodies",
        "regional_local_gov": "Regional or local government",
        "schools_heads": "Schools and head teachers",
        "donors": "Donors and development agencies",
        "ngos": "NGOs and implementing organisations",
        "edtech_companies": "EdTech companies",
        "mno_bigtech": "Mobile network or large technology companies",
        "parents": "Parents and households",
        "other": "Other",
    },
    "post_pilot": {
        "sustained": "Absorbed and sustained",
        "reduced": "Continues in reduced form",
        "taken_over": "Taken over by another organisation",
        "stops": "Stops",
        "varies_widely": "Varies widely",
        "no_view": "No view",
    },
    "constraint": {
        "electricity": "Electricity",
        "connectivity": "Internet connectivity",
        "data_cost": "Cost of data",
        "devices": "Devices",
        "maintenance": "Maintenance and repair",
        "security_theft": "Security or theft",
        "teacher_capacity": "Teacher capacity",
        "language_content": "Language and content",
        "other": "Other",
    },
}

SELECT_FIELDS = {
    "teacher": {
        "A9_location": "location",
        "B6_electricity": "electricity",
        "B7_internet": "internet",
        "D3_workload_effect": "workload",
        "B1_use_digital": "yes_no",
    },
    "provider": {
        "C2_offline": "offline",
        "C3_min_device": "device",
        "C4_data_payer": "data_payer",
        "G1_evidence": "evidence",
    },
    "expert": {
        "B2_decision_drivers_1": "decision_driver",
        "B3_after_pilots": "post_pilot",
        "F1_constraints_1": "constraint",
    },
}

EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_PATTERN = re.compile(r"(?<!\w)\+?\d[\d\s().-]{7,}\d(?!\w)")
IDENTIFIER_KEY_PATTERN = re.compile(
    r"(?:email|phone|mobile|whatsapp|full.?name|organisation|organization|"
    r"school.?name|gps|geolocation|instance.?id|submission.?id|respondent.?id|"
    r"uuid|uid|_?id$)",
    re.I,
)


def _read_records(path):
    try:
        records = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read {path.name} as valid Kobo JSON.") from exc
    if not isinstance(records, list) or not all(isinstance(row, dict) for row in records):
        raise ValueError(f"{path.name} must contain a JSON array of submission objects.")
    if any("_synthetic" in row for row in records):
        raise ValueError(f"{path.name} contains synthetic records; refusing real-data processing.")
    return records


def _value(record, field):
    value = record.get(field)
    if not isinstance(value, str):
        return ""
    return value.strip()


def _codes(value):
    if isinstance(value, list):
        return {str(item).strip() for item in value}
    if isinstance(value, str):
        return set(value.replace(",", " ").split())
    return set()


def _distribution(counts, denominator, include_percentage=True):
    small_groups = any(0 < count < SUPPRESSION_THRESHOLD for count in counts.values())
    if denominator < SUPPRESSION_THRESHOLD or small_groups:
        return {
            "n": denominator if denominator == 0 else None,
            "suppressed": True,
            "items": [],
        }

    items = []
    for code, count in counts.items():
        if count == 0:
            continue
        item = {
            "name": code,
            "count": count,
        }
        if include_percentage:
            item["percentage"] = round(count * 100 / denominator, 1)
        items.append(item)
    return {
        "n": denominator,
        "suppressed": False,
        "items": items,
    }


def _map_distribution(distribution, options):
    mapped = dict(distribution)
    mapped["items"] = [
        {**item, "name": options.get(item["name"], "Other")}
        for item in distribution["items"]
    ]
    return mapped


def _single_choice(records, field, option_key, include_percentage=True):
    counts = Counter()
    denominator = 0
    options = OPTIONS.get(option_key, {})
    for record in records:
        code = _value(record, field)
        if code in options:
            counts[code] += 1
            denominator += 1
        elif option_key == "yes_no" and code in ("yes", "no"):
            counts[code] += 1
            denominator += 1
    distribution = _distribution(counts, denominator, include_percentage)
    if option_key == "yes_no":
        labels = {"yes": "Yes", "no": "No"}
        return _map_distribution(distribution, labels)
    return _map_distribution(distribution, options)


def _multi_select(records, field, option_key):
    options = OPTIONS[option_key]
    counts = Counter()
    denominator = 0
    for record in records:
        selected = _codes(record.get(field)) & options.keys()
        if selected:
            denominator += 1
            counts.update(selected)
    return _map_distribution(_distribution(counts, denominator), options)


def _grouped_electricity(records):
    grouped = defaultdict(list)
    for record in records:
        location = _value(record, "A9_location")
        if location not in OPTIONS["location"]:
            continue
        if _value(record, "B6_electricity") not in OPTIONS["electricity"]:
            continue
        grouped[location].append(record)

    result = []
    for code, location_name in OPTIONS["location"].items():
        sample = grouped.get(code, [])
        if not sample:
            continue
        distribution = _single_choice(sample, "B6_electricity", "electricity")
        result.append({
            "location": location_name,
            "n": distribution["n"],
            "suppressed": distribution["suppressed"],
            "distribution": distribution["items"],
            "none": next(
                (item["percentage"] for item in distribution["items"] if item["name"] == "No electricity"),
                None,
            ),
            "unreliable": next(
                (item["percentage"] for item in distribution["items"] if item["name"] == "Mains power with frequent cuts"),
                None,
            ),
        })
    return result


def _country_signals(records):
    grouped = defaultdict(list)
    for record in records:
        code = _value(record, "A1_country").upper()
        country = COUNTRY_NAMES.get(code)
        answer = _value(record, "B1_use_digital")
        power = _value(record, "B6_electricity")
        if country:
            grouped[country].append((answer, power))

    signals = {}
    for country, answers in grouped.items():
        signal = {}
        digital_n = 0
        power_n = 0
        digital_answers = [answer for answer, _ in answers if answer in ("yes", "no")]
        if digital_answers:
            digital_counts = Counter(digital_answers)
            digital_distribution = _distribution(digital_counts, len(digital_answers))
            if not digital_distribution["suppressed"]:
                signal["pct"] = round(
                    digital_counts.get("yes", 0) * 100 / len(digital_answers), 1
                )
                digital_n = len(digital_answers)

        power_answers = [power for _, power in answers if power in OPTIONS["electricity"]]
        if power_answers:
            power_counts = Counter(power_answers)
            power_distribution = _distribution(power_counts, len(power_answers))
            if not power_distribution["suppressed"]:
                signal["reliablePowerPct"] = round(
                    power_counts.get("reliable_mains", 0) * 100 / len(power_answers), 1
                )
                power_n = len(power_answers)

        if signal:
            signals[country] = {
                "n": _published_sample_size(digital_n),
                "powerN": _published_sample_size(power_n),
                **signal,
            }
    return signals


def _count_for_codes(distribution, names):
    if distribution["suppressed"]:
        return None
    return sum(
        item["count"] for item in distribution["items"]
        if item["name"] in names
    )


def _published_sample_size(value):
    return value if value == 0 or value >= SUPPRESSION_THRESHOLD else None


def _assert_public_safe(payload):
    def visit(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if IDENTIFIER_KEY_PATTERN.search(str(key)):
                    raise ValueError("Public aggregate contains a prohibited identifier-like field.")
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
        elif isinstance(value, str):
            is_timestamp = bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}T.*", value))
            if EMAIL_PATTERN.search(value) or (not is_timestamp and PHONE_PATTERN.search(value)):
                raise ValueError("Public aggregate contains an email address or phone number.")
            if re.search(r"\b(?:demo|synthetic)\b", value, re.I):
                raise ValueError("Public aggregate contains a synthetic-data marker.")

    visit(payload)


def build_aggregate(input_dir, generated_at=None):
    input_dir = Path(input_dir)
    records = {
        instrument: _read_records(input_dir / f"kobo_{instrument}_submissions.json")
        for instrument in ("teacher", "provider", "expert", "followup")
    }

    for instrument, fields in SELECT_FIELDS.items():
        instrument_answers = 0
        for field, option_key in fields.items():
            allowed = set(OPTIONS.get(option_key, {"yes", "no"}))
            for row in records[instrument]:
                raw_value = row.get(field)
                if raw_value is None or raw_value == "":
                    continue
                if option_key == "evidence":
                    codes = _codes(raw_value)
                    if codes - allowed:
                        raise ValueError(f"Unrecognized choice code in {instrument}.{field}.")
                    instrument_answers += bool(codes)
                else:
                    if not isinstance(raw_value, str) or raw_value.strip() not in allowed:
                        raise ValueError(f"Unrecognized choice code in {instrument}.{field}.")
                    instrument_answers += 1
        if records[instrument] and instrument_answers == 0:
            raise ValueError(f"No recognized {instrument} survey answers; verify Kobo field mappings.")

    teachers = records["teacher"]
    providers = records["provider"]
    experts = records["expert"]

    teacher_internet = _single_choice(teachers, "B7_internet", "internet")
    teacher_workload = _single_choice(teachers, "D3_workload_effect", "workload")
    teacher_power = _grouped_electricity(teachers)
    provider_offline = _single_choice(providers, "C2_offline", "offline")
    provider_device = _single_choice(providers, "C3_min_device", "device")
    provider_payment = _single_choice(providers, "C4_data_payer", "data_payer")
    provider_evidence = _multi_select(providers, "G1_evidence", "evidence")
    expert_driver = _single_choice(experts, "B2_decision_drivers_1", "decision_driver", False)
    expert_exit = _single_choice(experts, "B3_after_pilots", "post_pilot", False)
    expert_constraints = _single_choice(experts, "F1_constraints_1", "constraint", False)

    total_primary = len(teachers) + len(providers) + len(experts)
    has_small_stream = any(
        0 < len(stream) < SUPPRESSION_THRESHOLD
        for stream in (teachers, providers, experts)
    )
    status = (
        "no_data" if total_primary == 0
        else "insufficient" if total_primary < SUPPRESSION_THRESHOLD
        else "available"
    )
    mobile_items = [
        item for item in provider_device["items"]
        if item["name"] in ("Basic phone", "Low-cost smartphone")
    ]
    provider_phone_pct = None
    if not provider_device["suppressed"] and provider_device["n"] is not None:
        provider_phone_pct = round(
            sum(item["count"] for item in mobile_items) * 100 / provider_device["n"], 1
        )

    expert_risk_count = _count_for_codes(
        expert_exit,
        {"Stops", "Continues in reduced form"},
    )
    if expert_exit["n"] is None or expert_exit["n"] < SUPPRESSION_THRESHOLD:
        expert_risk_count = None

    payload = {
        "schemaVersion": 1,
        "mode": "real",
        "status": status,
        "generatedAt": generated_at or datetime.now(timezone.utc).isoformat(),
        "suppressionThreshold": SUPPRESSION_THRESHOLD,
        "metadata": {
            "source": "KoboToolbox",
            "summaryStats": {
                "totalRespondents": None if has_small_stream else total_primary,
                "totalTeachers": _published_sample_size(len(teachers)),
                "totalProviders": _published_sample_size(len(providers)),
                "totalExperts": _published_sample_size(len(experts)),
                "countriesRepresented": len(_country_signals(teachers)),
            },
        },
        "teachers": {
            "total": _published_sample_size(len(teachers)),
            "elecByLocation": teacher_power,
            "internetDist": teacher_internet,
            "workloadDist": teacher_workload,
            "quotes": [],
        },
        "providers": {
            "total": _published_sample_size(len(providers)),
            "offlineDist": provider_offline,
            "deviceDist": provider_device,
            "handsetPercentage": provider_phone_pct,
            "dataPaymentDist": provider_payment,
            "evidenceDist": provider_evidence,
        },
        "experts": {
            "total": _published_sample_size(len(experts)),
            "decisionDriverDist": expert_driver,
            "donorExitDist": expert_exit,
            "systemConstraintDist": expert_constraints,
            "postGrantRiskCount": expert_risk_count,
        },
        "countrySignals": _country_signals(teachers),
        "followup": {
            "includedInPublicOutput": False,
        },
    }
    _assert_public_safe(payload)
    return payload


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True, help="Temporary directory with four Kobo JSON exports.")
    parser.add_argument("--output", required=True, help="Path for the sanitized aggregate JSON.")
    parser.add_argument(
        "--require-responses",
        action="store_true",
        help="Fail instead of writing a no-data aggregate when all primary forms are empty.",
    )
    args = parser.parse_args(argv)

    try:
        payload = build_aggregate(args.input_dir)
        if args.require_responses and payload["status"] == "no_data":
            raise ValueError("No teacher, provider, or expert submissions were returned.")
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"ERROR: Kobo processing stopped: {exc}", file=sys.stderr)
        return 1

    summary = payload["metadata"]["summaryStats"]
    print(
        "Processed submissions: "
        f"teacher={summary['totalTeachers']}, provider={summary['totalProviders']}, "
        f"expert={summary['totalExperts']}, follow-up fetched but excluded from output. "
        f"Dashboard status={payload['status']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
