import json
from collections import Counter

import pandas as pd

from make_synthetic_giga import FIELD_MAP as F
from scripts.build_giga_layer import clean_points, load_recent_measurements, load_regions, regional_layers


def test_clean_points_repairs_swaps_and_drops_invalid_coordinates(tmp_path):
    boundary = tmp_path / "regions.geojson"
    boundary.write_text(json.dumps({
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"shapeName": "Test Region", "shapeID": "region-1"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[10, 0], [20, 0], [20, 5], [10, 5], [10, 0]]],
            },
        }],
    }), encoding="utf-8")
    regions = load_regions(boundary, "shapeName", "shapeID")
    schools = pd.DataFrame({
        F["lon"]: [15, 2, None, 0, 30],
        F["lat"]: [2, 15, 2, 0, 30],
    })
    qc = Counter()

    cleaned = clean_points(schools, regions, qc)

    assert cleaned["shape_id"].tolist() == ["region-1", "region-1"]
    assert (cleaned.iloc[1][F["lon"]], cleaned.iloc[1][F["lat"]]) == (15, 2)
    assert qc == {
        "repaired_swapped_lat_lon": 1,
        "dropped_missing_coordinates": 1,
        "dropped_zero_coordinates": 1,
        "dropped_outside_all_regions": 1,
    }


def test_recent_school_medians_produce_coverage_and_quality_layers(tmp_path):
    measurements_path = tmp_path / "measurements.csv"
    school_ids = ["s1", "s1", "s2", "s3", "s4"]
    measurements = pd.DataFrame({
        F["school_id"]: school_ids,
        F["date"]: ["2026-01-30", "2026-01-29", "2026-01-30", "2026-01-30", "2026-01-30"],
        F["download"]: [0.5, 0.8, 2.0, 3.0, 4.0],
        F["conn_govt"]: ["Yes", "Yes", "Yes", "No", "Yes"],
    }).drop(columns=F["conn_govt"])
    measurements.to_csv(measurements_path, index=False)
    per_school, as_of, invalid_dates = load_recent_measurements(measurements_path, 30)
    schools = pd.DataFrame({
        F["school_id"]: ["s1", "s2", "s3", "s4", "s5"],
        F["conn_govt"]: ["Yes", "Yes", "No", "Yes", "Yes"],
        "shape_id": ["region-1"] * 5,
    }).join(per_school, on=F["school_id"])

    layers = regional_layers(schools, "TST", 2026, min_n=3)

    assert as_of == "2026-01-30"
    assert invalid_dates == 0
    assert layers["median_download"] == [("TST", "region-1", 2.5, 2026)]
    assert layers["below_1mbps"] == [("TST", "region-1", 25.0, 2026)]
    assert layers["metered_share"] == [("TST", "region-1", 80.0, 2026)]
    assert layers["reported_poor"] == [("TST", "region-1", 33.3, 2026)]
