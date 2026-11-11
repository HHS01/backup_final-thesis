#!/usr/bin/env python3
"""
pillar_delta_engine.py
======================
Step 3 Implementation:
Scores primary survey responses (KoboToolbox submissions) across UNESCO Six Pillars,
triangulates against macro baseline data (World Bank / UIS / ITU from indicators_timeseries.csv),
and computes perception-reality discrepancy deltas.

Outputs:
  - data/processed/survey_pillar_scores.json
  - data/processed/pillar_perception_deltas.json
  - Updates data/processed/survey_evidence_data.js
"""

import json
import csv
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_KOBO_DIR = DATA_DIR / "raw" / "kobo"
PROCESSED_DIR = DATA_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

CODEBOOK_FILE = DATA_DIR / "AoA_Survey_to_Pillar_Codebook.csv"
TIMESERIES_FILE = PROCESSED_DIR / "indicators_timeseries.csv"

# Likert / Ordinal Response normalizers (0 to 100 scale)
SCORE_MAPS = {
    "electricity": {
        "always": 100.0,
        "often": 75.0,
        "sometimes": 50.0,
        "rarely": 25.0,
        "never": 0.0,
    },
    "internet": {
        "reliable": 100.0,
        "often_cuts": 60.0,
        "rarely_works": 25.0,
        "no_internet": 0.0,
    },
    "agree_5pt": {
        "strongly_agree": 100.0,
        "agree": 75.0,
        "neither": 50.0,
        "disagree": 25.0,
        "strongly_disagree": 0.0,
    },
    "binary": {
        "yes": 100.0,
        "no": 0.0,
    },
    "frequency": {
        "every_lesson": 100.0,
        "most_days": 80.0,
        "once_twice_week": 60.0,
        "once_twice_month": 30.0,
        "less_often": 15.0,
        "never": 0.0,
    }
}


def load_codebook():
    """Loads survey to pillar codebook mappings."""
    mappings = {}
    if not CODEBOOK_FILE.exists():
        print(f"[!] Warning: Codebook not found at {CODEBOOK_FILE}")
        return mappings

    with open(CODEBOOK_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row.get("q_id", "").strip()
            p1 = row.get("pillar_primary", "").strip()
            flag = row.get("gap_flag", "").strip()
            mappings[qid] = {
                "pillar": p1,
                "gap_flag": flag,
                "condensed": row.get("question_condensed", "")
            }
    return mappings


def load_macro_baselines():
    """Extracts latest available country macro indicator values from timeseries."""
    # Mapping UNESCO Pillars to key representative World Bank indicators
    pillar_macro_indicators = {
        "1": "SE.XPD.TOTL.GD.ZS", # Gov expenditure on education (% of GDP)
        "2": "EG.ELC.ACCS.RU.ZS", # Access to electricity, rural (%)
        "3": "IT.NET.USER.ZS",     # Individuals using the Internet (% of pop)
        "4": "SE.PRM.TCAQ.ZS",     # Trained teachers in primary education (%)
        "5": "UIS.SCHBSP.1.WELEC",# Primary schools with electricity (%)
        "6": "IQ.SPI.OVRL",        # Statistical Performance Indicator (Governance & ethics)
    }

    macro_data = defaultdict(dict)
    if not TIMESERIES_FILE.exists():
        print(f"[!] Warning: Timeseries file not found at {TIMESERIES_FILE}")
        return macro_data

    with open(TIMESERIES_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            iso3 = row.get("iso3", "").strip()
            code = row.get("indicator_code", "").strip()
            val = row.get("value", "")
            yr = row.get("year", "")
            if iso3 and code and val:
                try:
                    num_val = float(val)
                    yr_val = int(float(yr))
                    # Retain the most recent year for each country and indicator
                    if code not in macro_data[iso3] or yr_val > macro_data[iso3][code]["year"]:
                        macro_data[iso3][code] = {"year": yr_val, "value": num_val}
                except ValueError:
                    continue

    return macro_data, pillar_macro_indicators


def score_submissions(codebook):
    """Parses teacher submissions and scores pillar dimensions."""
    teacher_file = RAW_KOBO_DIR / "kobo_teacher_submissions.json"
    if not teacher_file.exists():
        print(f"[!] No teacher submissions found at {teacher_file}")
        return {}

    with open(teacher_file, "r", encoding="utf-8") as f:
        teachers = json.load(f)

    # Accumulate scores per country and pillar: country -> pillar -> [scores]
    country_pillar_scores = defaultdict(lambda: defaultdict(list))

    for rec in teachers:
        ctry = rec.get("A1_country", "UNKNOWN")
        if not ctry or ctry == "OTH":
            continue

        # Pillar 2: Infrastructure & Connectivity (T-B6, T-B7)
        if "B6_electricity" in rec:
            val = SCORE_MAPS["electricity"].get(rec["B6_electricity"])
            if val is not None:
                country_pillar_scores[ctry]["2"].append(val)
        if "B7_internet" in rec:
            val = SCORE_MAPS["internet"].get(rec["B7_internet"])
            if val is not None:
                country_pillar_scores[ctry]["2"].append(val)

        # Pillar 5: Inclusion & Language (T-C1)
        if "C1_lang_teach" in rec:
            val = SCORE_MAPS["agree_5pt"].get(rec["C1_lang_teach"])
            if val is not None:
                country_pillar_scores[ctry]["5"].append(val)

        # Pillar 1: Governance & Leadership (T-B8)
        if "B8_approved_tools" in rec:
            val = 100.0 if rec["B8_approved_tools"] == "mandatory" else (70.0 if rec["B8_approved_tools"] == "recommended" else 20.0)
            country_pillar_scores[ctry]["1"].append(val)

        # Pillar 4: Capacity & Teacher Workload (T-D3)
        if "D3_workload" in rec:
            val = 80.0 if rec["D3_workload"] == "saves_time" else (50.0 if rec["D3_workload"] == "about_same" else 20.0)
            country_pillar_scores[ctry]["4"].append(val)

    # Compute aggregate indices (0-100) per country
    aggregated = {}
    for ctry, p_dict in country_pillar_scores.items():
        aggregated[ctry] = {
            "sample_size": sum(1 for r in teachers if r.get("A1_country") == ctry),
            "pillars": {}
        }
        for pillar_id, scores in p_dict.items():
            if scores:
                mean_score = sum(scores) / len(scores)
                aggregated[ctry]["pillars"][pillar_id] = round(mean_score, 2)

    return aggregated


def compute_perception_deltas(aggregated_scores, macro_data, pillar_macro_map):
    """
    Computes Delta 1: Perception (Ground Truth Index) minus Macro Baseline (0-100 normalized).
    Negative delta implies frontline reality is harsher than official macro metrics report.
    """
    deltas = {}
    for ctry, data in aggregated_scores.items():
        deltas[ctry] = {
            "sample_size": data["sample_size"],
            "pillar_comparisons": {}
        }
        for pillar_id, ground_score in data["pillars"].items():
            ind_code = pillar_macro_map.get(pillar_id)
            macro_val = None
            macro_yr = None
            if ctry in macro_data and ind_code in macro_data[ctry]:
                macro_val = macro_data[ctry][ind_code]["value"]
                macro_yr = macro_data[ctry][ind_code]["year"]

            # Compute delta if macro metric exists
            delta_val = None
            if macro_val is not None:
                # Most WB indicators are already percentages (0-100)
                delta_val = round(ground_score - macro_val, 2)

            deltas[ctry]["pillar_comparisons"][pillar_id] = {
                "ground_truth_score": ground_score,
                "macro_baseline": macro_val,
                "macro_year": macro_yr,
                "macro_indicator": ind_code,
                "delta_perception": delta_val,
                "gap_assessment": "Under-reporting friction" if (delta_val and delta_val < -10) else ("Aligned" if (delta_val and abs(delta_val) <= 10) else "Over-performing")
            }
    return deltas


def main():
    print("=" * 60)
    print(" Executing Pillar Scoring & Delta Analysis Engine")
    print("=" * 60)

    codebook = load_codebook()
    macro_data, pillar_macro_map = load_macro_baselines()

    # 1. Score Primary Submissions
    survey_scores = score_submissions(codebook)
    score_out = PROCESSED_DIR / "survey_pillar_scores.json"
    with open(score_out, "w", encoding="utf-8") as f:
        json.dump(survey_scores, f, indent=2)
    print(f"[+] Computed pillar scores for {len(survey_scores)} countries -> {score_out}")

    # 2. Compute Triangulation Deltas
    deltas = compute_perception_deltas(survey_scores, macro_data, pillar_macro_map)
    delta_out = PROCESSED_DIR / "pillar_perception_deltas.json"
    with open(delta_out, "w", encoding="utf-8") as f:
        json.dump(deltas, f, indent=2)
    print(f"[+] Computed triangulation deltas for {len(deltas)} countries -> {delta_out}")

    # Print summary highlights
    print("\n--- Highlight: Pillar 2 (Infrastructure/Connectivity) Triangulation Deltas ---")
    for ctry, res in list(deltas.items())[:5]:
        p2 = res["pillar_comparisons"].get("2")
        if p2:
            print(f"  [{ctry}] Ground Truth: {p2['ground_truth_score']:.1f} | Macro ({p2['macro_indicator']}): {p2['macro_baseline']} | Delta: {p2['delta_perception']} ({p2['gap_assessment']})")
    print("=" * 60)


if __name__ == "__main__":
    main()
