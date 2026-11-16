import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

for key in (
    "KOBO_TOKEN",
    "KOBO_SERVER",
    "KOBO_UID_TEACHER",
    "KOBO_UID_PROVIDER",
    "KOBO_UID_EXPERT",
    "KOBO_UID_FOLLOWUP",
):
    os.environ.setdefault(key, "")

from scripts import fetch_kobo_submissions as fetcher


class FetchKoboSubmissionsTests(unittest.TestCase):
    def test_fetch_follows_pages_and_aggregates_results(self):
        first_url = "https://ee.kobotoolbox.org/api/v2/assets/asset/data.json"
        second_url = first_url + "?page=2"
        first = Mock(
            status_code=200,
            url=first_url,
        )
        first.json.return_value = {"results": [{"_id": 1}], "next": "?page=2"}
        second = Mock(
            status_code=200,
            url=second_url,
        )
        second.json.return_value = {"results": [{"_id": 2}], "next": None}

        with patch.object(fetcher.requests, "get", side_effect=[first, second]) as get:
            records = fetcher.fetch_from_api("asset", "teacher", "https://ee.kobotoolbox.org", "token")

        self.assertEqual(records, [{"_id": 1}, {"_id": 2}])
        self.assertEqual(get.call_count, 2)
        self.assertEqual(get.call_args_list[0].kwargs["params"], {"format": "json"})

    def test_rejects_pagination_to_another_host(self):
        response = Mock(
            status_code=200,
            url="https://ee.kobotoolbox.org/api/v2/assets/asset/data.json",
        )
        response.json.return_value = {
            "results": [],
            "next": "https://example.invalid/collect",
        }

        with patch.object(fetcher.requests, "get", return_value=response) as get:
            with self.assertRaisesRegex(RuntimeError, "unexpected pagination host"):
                fetcher.fetch_from_api("asset", "teacher", "https://ee.kobotoolbox.org", "token")

        self.assertEqual(get.call_count, 1)

    def test_live_fetch_requires_all_configuration_before_writing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "raw"
            with (
                patch.object(fetcher, "KOBO_SERVER", ""),
                patch.object(fetcher, "KOBO_TOKEN", ""),
                patch.object(fetcher, "ASSET_UIDS", {}),
            ):
                with self.assertRaises(SystemExit) as raised:
                    fetcher.main(["--output-dir", str(output_dir)])

            self.assertNotEqual(raised.exception.code, 0)
            self.assertFalse(output_dir.exists())

    def test_live_fetch_writes_all_four_successful_empty_responses_without_demo_data(self):
        expected = set(fetcher.INSTRUMENTS)
        asset_uids = {instrument: f"asset-{instrument}" for instrument in expected}

        with tempfile.TemporaryDirectory() as temp_dir:
            with (
                patch.object(fetcher, "KOBO_SERVER", "https://ee.kobotoolbox.org"),
                patch.object(fetcher, "KOBO_TOKEN", "test-token"),
                patch.object(fetcher, "ASSET_UIDS", asset_uids),
                patch.object(fetcher, "fetch_from_api", return_value=[]) as fetch,
            ):
                fetcher.main(["--output-dir", temp_dir])

            self.assertEqual({call.args[1] for call in fetch.call_args_list}, expected)
            for instrument in expected:
                path = Path(temp_dir) / f"kobo_{instrument}_submissions.json"
                self.assertEqual(json.loads(path.read_text(encoding="utf-8")), [])

    def test_live_output_cannot_be_written_inside_repository(self):
        asset_uids = {instrument: f"asset-{instrument}" for instrument in fetcher.INSTRUMENTS}
        with (
            patch.object(fetcher, "KOBO_SERVER", "https://ee.kobotoolbox.org"),
            patch.object(fetcher, "KOBO_TOKEN", "test-token"),
            patch.object(fetcher, "ASSET_UIDS", asset_uids),
            patch.object(fetcher, "fetch_from_api") as fetch,
        ):
            with self.assertRaises(SystemExit):
                fetcher.main(["--output-dir", str(fetcher.ROOT_DIR / "data" / "raw" / "kobo")])
        fetch.assert_not_called()

    def test_demo_records_are_explicitly_marked_and_separate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            fetcher.main(["--demo", "--output-dir", temp_dir])
            teachers = json.loads(
                (Path(temp_dir) / "kobo_teacher_submissions.json").read_text(encoding="utf-8")
            )
            followup = json.loads(
                (Path(temp_dir) / "kobo_followup_submissions.json").read_text(encoding="utf-8")
            )

        self.assertTrue(teachers)
        self.assertTrue(all(record["_synthetic"] is True for record in teachers))
        self.assertEqual(followup, [])


if __name__ == "__main__":
    unittest.main()
