import json
import tempfile
import unittest
from pathlib import Path

from scripts.process_kobo_surveys import build_aggregate


def fixture_records():
    teachers = []
    for index in range(10):
        teachers.append({
            "_id": f"private-id-{index}",
            "A1_country": "GHA",
            "A9_location": "rural" if index < 5 else "major_city",
            "B1_use_digital": "yes" if index < 5 else "no",
            "B6_electricity": "reliable_mains" if index < 5 else "none",
            "B7_internet": "no_access" if index < 5 else "unreliable",
            "D3_workload_effect": "reduce_it_a_lot" if index < 5 else "no_difference",
            "free_text": "private quote@example.org, +254 712 345 678",
        })

    providers = []
    for index in range(10):
        providers.append({
            "_id": f"private-provider-{index}",
            "C2_offline": "fully_offline" if index < 5 else "needs_connection",
            "C3_min_device": "basic_phone" if index < 5 else "low_cost_smartphone",
            "C4_data_payer": "users_pay" if index < 5 else "we_or_programme",
            "G1_evidence": "independent_evaluation rct_comparison" if index < 5 else "none_yet",
            "organisation_name": "Private provider name",
        })

    experts = []
    for index in range(10):
        experts.append({
            "_id": f"private-expert-{index}",
            "B2_decision_drivers_1": "ministry" if index < 5 else "schools_heads",
            "B3_after_pilots": "stops" if index < 5 else "sustained",
            "F1_constraints_1": "electricity" if index < 5 else "connectivity",
            "full_name": "Private expert name",
            "email_address": "expert@example.org",
        })

    followup = [{
        "_id": "private-followup-id",
        "full_name": "Private follow-up name",
        "email_address": "followup@example.org",
        "phone_whatsapp": "+254 712 345 678",
        "delphi_anon_code": "private-linkage-code",
    }]
    return {
        "teacher": teachers,
        "provider": providers,
        "expert": experts,
        "followup": followup,
    }


class ProcessKoboSurveysTests(unittest.TestCase):
    def write_inputs(self, root, records):
        root.mkdir(parents=True, exist_ok=True)
        for instrument, rows in records.items():
            path = root / f"kobo_{instrument}_submissions.json"
            path.write_text(json.dumps(rows), encoding="utf-8")

    def test_builds_public_aggregate_without_raw_or_followup_pii(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "raw"
            self.write_inputs(input_dir, fixture_records())

            payload = build_aggregate(input_dir, generated_at="2026-11-13T06:00:00+00:00")
            serialized = json.dumps(payload)

        self.assertEqual(payload["mode"], "real")
        self.assertEqual(payload["status"], "available")
        self.assertEqual(payload["metadata"]["summaryStats"]["totalRespondents"], 30)
        self.assertEqual(payload["countrySignals"]["Ghana"], {
            "n": 10,
            "powerN": 10,
            "pct": 50.0,
            "reliablePowerPct": 50.0,
        })
        self.assertEqual(payload["experts"]["postGrantRiskCount"], 5)
        self.assertTrue(all(
            "percentage" not in item
            for item in payload["experts"]["donorExitDist"]["items"]
        ))
        evidence = payload["providers"]["evidenceDist"]["items"]
        self.assertEqual(
            {item["name"]: item["percentage"] for item in evidence},
            {
                "Independent evaluation": 50.0,
                "Randomised or comparison-group study": 50.0,
                "None yet": 50.0,
            },
        )
        self.assertNotIn("followup@example.org", serialized)
        self.assertNotIn("private quote", serialized)
        self.assertNotIn("private-linkage-code", serialized)
        self.assertNotIn("_id", serialized)
        self.assertFalse(payload["followup"]["includedInPublicOutput"])

    def test_suppresses_a_distribution_with_small_groups(self):
        rows = fixture_records()
        rows["provider"][0]["C2_offline"] = "partly"
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "raw"
            self.write_inputs(input_dir, rows)

            payload = build_aggregate(input_dir)

        offline = payload["providers"]["offlineDist"]
        self.assertTrue(offline["suppressed"])
        self.assertEqual(offline["items"], [])

    def test_rejects_synthetic_records_in_real_processing(self):
        rows = fixture_records()
        rows["teacher"][0]["_synthetic"] = True
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "raw"
            self.write_inputs(input_dir, rows)

            with self.assertRaisesRegex(ValueError, "synthetic records"):
                build_aggregate(input_dir)

    def test_rejects_unmapped_schema_instead_of_emitting_empty_charts(self):
        records = {name: [] for name in ("teacher", "provider", "expert", "followup")}
        records["teacher"] = [{"old_field_name": "some value"}]
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "raw"
            self.write_inputs(input_dir, records)

            with self.assertRaisesRegex(ValueError, "No recognized teacher survey answers"):
                build_aggregate(input_dir)

    def test_rejects_unknown_choice_codes_instead_of_silently_dropping_them(self):
        records = fixture_records()
        records["provider"][0]["C2_offline"] = "unmapped_choice"
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "raw"
            self.write_inputs(input_dir, records)

            with self.assertRaisesRegex(ValueError, "Unrecognized choice code in provider.C2_offline"):
                build_aggregate(input_dir)

    def test_empty_instruments_produce_explicit_no_data_state(self):
        records = {name: [] for name in ("teacher", "provider", "expert", "followup")}
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "raw"
            self.write_inputs(input_dir, records)

            payload = build_aggregate(input_dir)

        self.assertEqual(payload["status"], "no_data")
        self.assertEqual(payload["metadata"]["summaryStats"]["totalRespondents"], 0)

    def test_require_responses_fails_without_writing_an_empty_aggregate(self):
        from scripts.process_kobo_surveys import main

        records = {name: [] for name in ("teacher", "provider", "expert", "followup")}
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "raw"
            output = Path(temp_dir) / "aggregate.json"
            self.write_inputs(input_dir, records)

            result = main([
                "--input-dir", str(input_dir),
                "--output", str(output),
                "--require-responses",
            ])

        self.assertEqual(result, 1)
        self.assertFalse(output.exists())

    def test_cli_writes_allowlisted_aggregate(self):
        from scripts.process_kobo_surveys import main

        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "raw"
            output = Path(temp_dir) / "processed" / "aggregate.json"
            self.write_inputs(input_dir, fixture_records())

            result = main([
                "--input-dir", str(input_dir),
                "--output", str(output),
            ])
            serialized = output.read_text(encoding="utf-8")
            payload = json.loads(serialized)

        self.assertEqual(result, 0)
        self.assertEqual(payload["status"], "available")
        self.assertNotIn("private quote", serialized)
        self.assertNotIn("private-expert", serialized)


if __name__ == "__main__":
    unittest.main()
