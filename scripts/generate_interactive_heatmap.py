import json

with open('/workspaces/backup_final-thesis/data/processed/afrobarometer_triangulation.json') as f:
    ab_data = json.load(f)

with open('/workspaces/backup_final-thesis/data/processed/macro_for_triangulation.json') as f:
    macro_data = json.load(f)

with open('/workspaces/backup_final-thesis/data/processed/survey_data_calibrated.json') as f:
    survey_data = json.load(f)

teacher_records = survey_data.get("teachers", {}).get("records", [])

countries = [
    {"iso3": "KEN", "name": "Kenya", "flag": "🇰🇪"},
    {"iso3": "GHA", "name": "Ghana", "flag": "🇬🇭"},
    {"iso3": "NGA", "name": "Nigeria", "flag": "🇳🇬"},
    {"iso3": "TZA", "name": "Tanzania", "flag": "🇹🇿"},
    {"iso3": "ZMB", "name": "Zambia", "flag": "🇿🇲"},
    {"iso3": "MUS", "name": "Mauritius", "flag": "🇲🇺"},
    {"iso3": "RWA", "name": "Rwanda", "flag": "🇷🇼", "note": "Absent from AB R10 Release"}
]

heatmap_dataset = []

for c in countries:
    iso = c["iso3"]
    ab = ab_data.get(iso, {})
    m = macro_data.get(iso, {})
    
    # 1. Electricity (National vs Household Mains)
    wb_elec = m.get("wb_total_elec_access_%")
    ab_elec = ab.get("hh_mains_electricity_pct")
    elec_gap = round(ab_elec - wb_elec, 1) if (ab_elec is not None and wb_elec is not None) else None
    
    # 2. Rural Electricity Gap (WB Rural vs AB Rural Grid presence)
    wb_rural_elec = m.get("wb_rural_elec_access_%")
    ab_rural_grid = ab.get("ea_rural_electricity_grid_pct")
    rural_elec_gap = round(ab_rural_grid - wb_rural_elec, 1) if (ab_rural_grid is not None and wb_rural_elec is not None) else None

    # 3. Internet Connectivity (WB Users vs AB Mobile Internet)
    wb_int = m.get("wb_internet_users_%")
    ab_int = ab.get("mobile_internet_pct")
    int_gap = round(ab_int - wb_int, 1) if (ab_int is not None and wb_int is not None) else None

    # 4. Governance Paradox (AB Edu Satisfaction vs UIS School Electrification)
    ab_gov_edu = ab.get("gov_edu_well_pct")
    uis_elec = m.get("uis_schools_w_electricity_%")
    gov_infra_gap = round(ab_gov_edu - uis_elec, 1) if (ab_gov_edu is not None and uis_elec is not None) else None

    # 5. Financial Precarity (Data Cost Feasibility)
    never_no_cash = ab.get("never_without_income_pct")
    precarity_rate = round(100.0 - never_no_cash, 1) if never_no_cash is not None else None

    # 6. Synthetic practitioner audit: teacher reports of mostly/always reliable power
    teacher_sample = [r for r in teacher_records if r.get("country") == c["name"]]
    reliable_power_n = sum(
        r.get("elec") in ("Mostly reliable", "Always reliable")
        for r in teacher_sample
    )
    reliable_power_pct = round(100.0 * reliable_power_n / len(teacher_sample), 1) if teacher_sample else None
    synthetic_n = len(teacher_sample)
    synthetic_macro_gap = (
        round(reliable_power_pct - uis_elec, 1)
        if reliable_power_pct is not None and uis_elec is not None
        else None
    )

    entry = {
        "iso3": iso,
        "name": c["name"],
        "flag": c["flag"],
        "sample_size_ab": ab.get("n_total", 0),
        "note": c.get("note", "Afrobarometer Round 10 (2024-2026)"),
        "dimensions": {
            "electricity": {
                "name": "Household Electricity Access",
                "macro_val": wb_elec,
                "macro_src": "World Bank WDI (EG.ELC.ACCS.ZS)",
                "field_val": ab_elec,
                "field_src": "Afrobarometer R10 Q93A (Connected to Mains)",
                "gap": elec_gap,
                "unit": "%",
                "type": "overstatement" if elec_gap and elec_gap < -5 else ("understatement" if elec_gap and elec_gap > 5 else "aligned"),
                "desc": f"Macro claims {wb_elec}% access; citizens report {ab_elec}% mains connection ({elec_gap}pp gap)." if elec_gap is not None else "Data missing in R10."
            },
            "rural_grid": {
                "name": "Rural Grid Infrastructure",
                "macro_val": wb_rural_elec,
                "macro_src": "World Bank WDI Rural (EG.ELC.ACCS.RU.ZS)",
                "field_val": ab_rural_grid,
                "field_src": "Afrobarometer R10 EA_SVC_A (Grid observed in Rural EA)",
                "gap": rural_elec_gap,
                "unit": "%",
                "type": "divergence" if rural_elec_gap and abs(rural_elec_gap) > 10 else "aligned",
                "desc": f"Interviewer observed grid in {ab_rural_grid}% of rural clusters vs WB rural estimate {wb_rural_elec}%." if rural_elec_gap is not None else "Data missing in R10."
            },
            "internet": {
                "name": "Active Mobile Internet",
                "macro_val": wb_int,
                "macro_src": "World Bank / ITU (IT.NET.USER.ZS)",
                "field_val": ab_int,
                "field_src": "Afrobarometer R10 Q90H (Mobile Internet Access)",
                "gap": int_gap,
                "unit": "%",
                "type": "understatement" if int_gap and int_gap > 10 else ("overstatement" if int_gap and int_gap < -10 else "aligned"),
                "desc": f"Macro estimates {wb_int}% users; citizen survey shows {ab_int}% active mobile web access." if int_gap is not None else "Data missing in R10."
            },
            "gov_paradox": {
                "name": "Governance vs School Infra Paradox",
                "macro_val": uis_elec,
                "macro_src": "UIS (% Primary Schools with Electricity)",
                "field_val": ab_gov_edu,
                "field_src": "Afrobarometer R10 Q47H (Gov Handles Education Well)",
                "gap": gov_infra_gap,
                "unit": "%",
                "type": "paradox" if gov_infra_gap and gov_infra_gap > 20 else "standard",
                "desc": f"Satisfaction is {ab_gov_edu}%, yet only {uis_elec}% of primary schools have electricity." if gov_infra_gap is not None else "School electrification data missing."
            },
            "economic_precarity": {
                "name": "Teacher/Citizen Cash Precarity",
                "macro_val": round(m.get("NY.GDP.PCAP.PP.CD", 0), 0) if m.get("NY.GDP.PCAP.PP.CD") else None,
                "macro_src": "World Bank GDP per Capita PPP ($)",
                "field_val": precarity_rate,
                "field_src": "Afrobarometer R10 Q7E (Gone without cash income)",
                "gap": None,
                "unit": "% precarity",
                "type": "critical" if precarity_rate and precarity_rate > 80 else "moderate",
                "desc": f"{precarity_rate}% of households have gone without cash income. Data-heavy apps impose punitive burden." if precarity_rate is not None else "Data missing."
            },
            "practitioner_audit": {
                "name": "Synthetic Teacher Power Signal",
                "macro_val": uis_elec,
                "macro_src": "UIS (% Primary Schools with Electricity)",
                "field_val": reliable_power_pct,
                "field_src": "Synthetic AoA teacher baseline (mostly/always reliable school power)",
                "sample_size": synthetic_n,
                "gap": synthetic_macro_gap,
                "unit": "%",
                "type": "synthetic",
                "desc": (
                    f"Illustrative synthetic baseline: {reliable_power_pct}% of {synthetic_n} teacher responses "
                    f"report mostly or always reliable school power; UIS reports {uis_elec}% of primary schools "
                    "with electricity. This is simulated, not observed field evidence."
                    if reliable_power_pct is not None and uis_elec is not None
                    else "No synthetic teacher responses or UIS school-power estimate available for this country."
                )
            }
        }
    }
    heatmap_dataset.append(entry)

with open('/workspaces/backup_final-thesis/data/processed/interactive_triangulation_heatmap.json', 'w') as f:
    json.dump(heatmap_dataset, f, indent=2)

print("Generated interactive_triangulation_heatmap.json with", len(heatmap_dataset), "countries.")
