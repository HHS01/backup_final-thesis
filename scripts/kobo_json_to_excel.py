#!/usr/bin/env python3
"""
kobo_json_to_excel.py
=====================
Bridge script: converts the 3 raw Kobo JSON submission files into a single
Excel workbook (Teachers / Providers / Experts sheets) that
process_survey_data_calibrated.py expects as input.

Kobo field names  →  Excel column names used by the processing pipeline.
Only maps fields actually present in the Kobo JSON; everything else is left
blank (the processing script handles missing columns gracefully).

Usage:
    python scripts/kobo_json_to_excel.py
    python scripts/kobo_json_to_excel.py --input-dir data/raw/kobo \
        --output data/raw/SSA_Survey_Responses_Live.xlsx
"""

import argparse
import json
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    raise SystemExit("pandas not installed. Run: pip install pandas openpyxl")

ROOT = Path(__file__).resolve().parent.parent

# ── Field maps: Kobo JSON key → Excel column name ────────────────────────────
# Extend these dicts when new questions are added to the Kobo forms.

TEACHER_MAP = {
    "_id":               "Response_ID",
    "A1_country":        "Country",
    "A1_region":         "Region",
    "A2_school_type":    "School_Type",
    "A3_levels":         "Teaching_Levels",
    "A4_languages":      "Teaching_Languages",
    "A5_understand":     "Student_Language_Comprehension",
    "A9_location":       "School_Location",
    "A10_class_size":    "Class_Size",
    "B1_use_digital":    "Uses_Digital_Tools",
    "B5_student_devices":"Digital_Tools_Used",
    "B6_electricity":    "Electricity_Reliability",
    "B7_internet":       "Internet_Reliability",
    "B8_approved_tools": "Approved_Tools_Policy",
    "C1_lang_teach":     "Lang_Fit_Teaching",
    "C1_infrastructure": "Infrastructure_Fit",
    "D3_workload":       "Workload_Impact",
    "E1_ai_familiar":    "AI_Use_Frequency",
    "E2_ai_conf":        "AI_Confidence",
    "E3_ai_training":    "AI_Training_Received",
    "E4_ai_language":    "AI_Local_Language_Handling",
    "F1_phone_rules":    "Phone_Rules",
    "F2_harm_report":    "Harm_Reporting_Known",
    "G1_comment":        "Qualitative_Comment",
}

PROVIDER_MAP = {
    "_id":               "Provider_ID",
    "A1_org_name":       "Org_Name",
    "A2_hq_country":     "HQ_Country",
    "A3_operate_countries": "Operating_Countries",
    "A4_org_type":       "Org_Type",
    "A5_ownership":      "Ownership_Model",
    "B1_connectivity":   "Offline_Capability",
    "B2_hardware":       "Minimum_Device",
    "B3_data_payment":   "Data_Payment_Model",
    "C1_offering":       "Primary_Offering",
    "C2_revenue":        "Revenue_Model",
    "C3_team_size":      "Team_Size",
    "D1_languages":      "Local_Language_Support",
    "D2_evidence":       "Evidence_Level_Held",
    "D3_ai_features":    "AI_Features_Included",
    "E1_breakdown":      "Procurement_Breakdown_Point",
}

EXPERT_MAP = {
    "_id":               "Expert_ID",
    "A1_system":         "Evaluated_Country",
    "A3_based":          "Region",
    "A4_perspective":    "Vantage_Point",
    "B1_driver":         "Primary_Decision_Driver",
    "B2_funding":        "Primary_Funding_Source",
    "B3_donor_exit":     "Donor_Exit_Fate",
    "C1_evidence_threshold": "Realistic_Evidence_Threshold",
    "D1_constraint":     "Top_System_Constraint",
    "D2_equity_risk":    "Most_Consequential_Equity_Risk",
    "D3_telco":          "Telco_Role_Significance",
    "D4_agree_i":        "Structured_Pedagogy_Support",
    "E1_ai_score":       "AI_Classroom_Readiness_Score",
    "F1_constraints_1":  "Expert_Qualitative_Comment",
}

INSTRUMENT_CONFIG = {
    "teacher":  ("kobo_teacher_submissions.json",  TEACHER_MAP,  "Teachers"),
    "provider": ("kobo_provider_submissions.json", PROVIDER_MAP, "Providers"),
    "expert":   ("kobo_expert_submissions.json",   EXPERT_MAP,   "Experts"),
}


def _add_linguistic_bloc(df: "pd.DataFrame") -> "pd.DataFrame":
    """Derive Linguistic_Bloc from Country using the same taxonomy as the
    processing pipeline."""
    BLOC = {
        # Anglophone
        **{c: "Anglophone" for c in [
            "Botswana","Eritrea","Eswatini","Ethiopia","Gambia, The","Ghana",
            "Kenya","Lesotho","Liberia","Malawi","Mauritius","Namibia","Nigeria",
            "Rwanda","Seychelles","Sierra Leone","Somalia, Fed. Rep.","South Africa",
            "South Sudan","Sudan","Tanzania","Uganda","Zambia","Zimbabwe",
        ]},
        # Francophone
        **{c: "Francophone" for c in [
            "Benin","Burkina Faso","Burundi","Cameroon","Central African Republic",
            "Chad","Comoros","Congo, Dem. Rep.","Congo, Rep.","Cote d'Ivoire",
            "Côte d'Ivoire","Gabon","Guinea","Madagascar","Mali","Mauritania",
            "Niger","Senegal","Togo",
        ]},
        # Lusophone
        **{c: "Lusophone" for c in [
            "Angola","Cabo Verde","Equatorial Guinea","Guinea-Bissau","Mozambique",
            "Sao Tome and Principe","São Tomé and Príncipe",
        ]},
    }
    if "Country" in df.columns:
        df["Linguistic_Bloc"] = df["Country"].map(BLOC).fillna("Other")
    elif "HQ_Country" in df.columns:
        df["Linguistic_Bloc"] = df["HQ_Country"].map(BLOC).fillna("Other")
    return df


def load_and_map(json_path: Path, field_map: dict) -> "pd.DataFrame":
    """Load a Kobo JSON file and rename fields to Excel column names."""
    if not json_path.exists():
        print(f"  [!] Not found: {json_path} — skipping.")
        return pd.DataFrame()

    with open(json_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    if not records:
        print(f"  [i] {json_path.name}: 0 submissions (forms freshly deployed).")
        return pd.DataFrame(columns=list(field_map.values()))

    df = pd.DataFrame(records)
    # Keep only mapped columns, rename them
    keep = {k: v for k, v in field_map.items() if k in df.columns}
    df = df[list(keep.keys())].rename(columns=keep)
    df = _add_linguistic_bloc(df)
    print(f"  [+] {json_path.name}: {len(df)} submissions → {len(df.columns)} columns mapped.")
    return df


def main():
    parser = argparse.ArgumentParser(description="Bridge: Kobo JSON → Excel for processing pipeline.")
    parser.add_argument("--input-dir", default=str(ROOT / "data" / "raw" / "kobo"),
                        help="Directory containing kobo_*_submissions.json files")
    parser.add_argument("--output", default=str(ROOT / "data" / "raw" / "SSA_Survey_Responses_Live.xlsx"),
                        help="Output Excel path")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n── Kobo JSON → Excel Bridge ──────────────────────────────")
    print(f"   Input dir : {input_dir}")
    print(f"   Output    : {output_path}\n")

    sheets = {}
    for inst, (filename, field_map, sheet_name) in INSTRUMENT_CONFIG.items():
        json_path = input_dir / filename
        df = load_and_map(json_path, field_map)
        sheets[sheet_name] = df

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    total = sum(len(df) for df in sheets.values())
    print(f"\n✓ Written {total} total records across {len(sheets)} sheets → {output_path}")
    if total == 0:
        print("  Note: All sheets are empty (no live responses yet). "
              "Re-run after submissions arrive.")


if __name__ == "__main__":
    main()
