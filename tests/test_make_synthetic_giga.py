import csv
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np

MODULE_PATH = Path(__file__).resolve().parents[1] / "make_synthetic_giga.py"
SPEC = importlib.util.spec_from_file_location("make_synthetic_giga", MODULE_PATH)
GENERATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = GENERATOR
SPEC.loader.exec_module(GENERATOR)

apply_quirks = GENERATOR.apply_quirks
main = GENERATOR.main
make_country = GENERATOR.make_country


def test_school_count_is_exact_and_region_link_is_preserved():
    region = {
        "name": "Demo Region",
        "id": "region-1",
        "polys": [[[
            [0, 0], [1, 0], [1, 1], [0, 1], [0, 0],
        ]]],
        "box": (0, 0, 1, 1),
        "area": 1,
    }

    schools = make_country(np.random.default_rng(12), "TST", [region], 7, 10, "2026-01-01", 0.5)

    assert len(schools) == 7
    assert set(schools["admin1_id"]) == {"region-1"}
    assert set(schools["admin1_boundary"]) == {"Demo Region"}


def test_quirks_add_name_variants_without_losing_boundary_names():
    region = {
        "name": "Demo Region",
        "id": "region-1",
        "polys": [[[
            [0, 0], [1, 0], [1, 1], [0, 1], [0, 0],
        ]]],
        "box": (0, 0, 1, 1),
        "area": 1,
    }
    schools = make_country(np.random.default_rng(2), "TST", [region], 100, 10, "2026-01-01", 0.5)

    changed, log = apply_quirks(np.random.default_rng(3), schools)

    assert log["admin1_name_variants"] > 0
    assert set(changed["admin1_boundary"]) == {"Demo Region"}


def test_cli_generates_labeled_placeholder_files(tmp_path):
    boundaries = tmp_path / "boundaries"
    boundaries.mkdir()
    geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"shapeName": "Demo Region", "shapeID": "region-1"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
            },
        }],
    }
    (boundaries / "TST_ADM1.geojson").write_text(json.dumps(geojson), encoding="utf-8")
    output = tmp_path / "giga_synthetic"

    result = main([
        "--countries", "TST",
        "--boundaries", str(boundaries),
        "--out", str(output),
        "--schools", "12",
        "--days", "8",
        "--seed", "7",
        "--end-date", "2026-01-01",
    ])

    assert result is None
    with (output / "TST_schools.csv").open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 12
    assert all(row["synthetic"] == "True" for row in rows)
    assert all(row["admin1_id"] == "region-1" for row in rows)
    assert (output / "TST_schools.json").is_file()
    assert (output / "TST_measurements.csv").is_file()
    assert (output / "giga_region_summary.json").is_file()
    status = json.loads((output / "data_status.json").read_text(encoding="utf-8"))
    assert status["mode"] == "demo"
    assert "synthetic" in status["note"].lower()
