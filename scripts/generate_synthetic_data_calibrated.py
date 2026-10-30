#!/usr/bin/env python3
"""
generate_synthetic_data_calibrated.py
===============================================================================
Calibrated Synthetic Generator for the Sub-Saharan Africa EdTech Landscape Review
-------------------------------------------------------------------------------
Anchored in empirical macro data from:
  1. latest_country_profiles_6pillars.csv (UNESCO/World Bank WDI 2024 indicators)
  2. GEM Report 2023 / 2024 Spotlight (Rural electricity >70% deficit, multilingual policy)
  3. HolonIQ Africa EdTech 50 (2025 cohort: 70% D2C models)
  4. Briter 2025 funding benchmarks (86% capital concentration in 'Big Four')
  5. AfroBench & IrokoBench LLM evaluation benchmarks for African languages
  6. Frontiers 2026 / mHealth pilotitis benchmarks (donor project survival)

Calibrated by Analysis C as part of the Multi-Stakeholder Triangulation framework.
===============================================================================
"""

import os
import random
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

# Load empirical macro data
DATA_CSV = "/workspaces/CC_3/data/processed/latest_country_profiles_6pillars.csv"
if not os.path.exists(DATA_CSV):
    # Fallback to relative path
    DATA_CSV = "data/processed/latest_country_profiles_6pillars.csv"

macro_df = pd.read_csv(DATA_CSV)
ssa_macro = macro_df[macro_df["region"] == "SSA"].copy().set_index("iso3")

# Median fallbacks for any missing indicators
MEDIANS = {
    "EG.ELC.ACCS.RU.ZS": float(ssa_macro["EG.ELC.ACCS.RU.ZS"].median()),
    "EG.ELC.ACCS.UR.ZS": float(ssa_macro["EG.ELC.ACCS.UR.ZS"].median()),
    "EG.ELC.ACCS.ZS": float(ssa_macro["EG.ELC.ACCS.ZS"].median()),
    "IT.NET.USER.ZS": float(ssa_macro["IT.NET.USER.ZS"].median()),
    "IT.NET.BBND.P2": float(ssa_macro["IT.NET.BBND.P2"].median()),
    "SE.PRM.ENRL.TC.ZS": float(ssa_macro["SE.PRM.ENRL.TC.ZS"].median()),
    "SE.PRM.TCAQ.ZS": float(ssa_macro["SE.PRM.TCAQ.ZS"].median()),
    "NY.GDP.PCAP.PP.CD": float(ssa_macro["NY.GDP.PCAP.PP.CD"].median()),
    "IQ.SPI.OVRL": float(ssa_macro["IQ.SPI.OVRL"].median()),
}

# 48 SSA Countries with Region, Linguistic Bloc, and Sampling Weight
# Sampling weights reflect demographic population, ecosystem activity, and pilot focus
COUNTRY_TAXONOMY = [
    # Four Pilot Countries (Prioritized)
    {"name": "Kenya", "iso3": "KEN", "bloc": "Anglophone", "region": "East Africa", "weight": 14, "is_big4": True},
    {"name": "Rwanda", "iso3": "RWA", "bloc": "Anglophone", "region": "East Africa", "weight": 10, "is_big4": False},
    {"name": "Mauritius", "iso3": "MUS", "bloc": "Anglophone", "region": "East Africa", "weight": 8, "is_big4": False},
    {"name": "Zambia", "iso3": "ZMB", "bloc": "Anglophone", "region": "Southern Africa", "weight": 8, "is_big4": False},

    # Regional Powerhouses & Big Four
    {"name": "Nigeria", "iso3": "NGA", "bloc": "Anglophone", "region": "West Africa", "weight": 16, "is_big4": True},
    {"name": "South Africa", "iso3": "ZAF", "bloc": "Anglophone", "region": "Southern Africa", "weight": 12, "is_big4": True},
    {"name": "Ghana", "iso3": "GHA", "bloc": "Anglophone", "region": "West Africa", "weight": 8, "is_big4": False},

    # Francophone Hubs
    {"name": "Senegal", "iso3": "SEN", "bloc": "Francophone", "region": "West Africa", "weight": 7, "is_big4": False},
    {"name": "Cote d'Ivoire", "iso3": "CIV", "bloc": "Francophone", "region": "West Africa", "weight": 7, "is_big4": False},
    {"name": "Cameroon", "iso3": "CMR", "bloc": "Francophone", "region": "Central Africa", "weight": 5, "is_big4": False},
    {"name": "Congo, Dem. Rep.", "iso3": "COD", "bloc": "Francophone", "region": "Central Africa", "weight": 5, "is_big4": False},
    {"name": "Benin", "iso3": "BEN", "bloc": "Francophone", "region": "West Africa", "weight": 4, "is_big4": False},
    {"name": "Burkina Faso", "iso3": "BFA", "bloc": "Francophone", "region": "West Africa", "weight": 3, "is_big4": False},
    {"name": "Mali", "iso3": "MLI", "bloc": "Francophone", "region": "West Africa", "weight": 3, "is_big4": False},
    {"name": "Madagascar", "iso3": "MDG", "bloc": "Francophone", "region": "East Africa", "weight": 3, "is_big4": False},
    {"name": "Togo", "iso3": "TGO", "bloc": "Francophone", "region": "West Africa", "weight": 2, "is_big4": False},
    {"name": "Niger", "iso3": "NER", "bloc": "Francophone", "region": "West Africa", "weight": 2, "is_big4": False},
    {"name": "Guinea", "iso3": "GIN", "bloc": "Francophone", "region": "West Africa", "weight": 2, "is_big4": False},
    {"name": "Chad", "iso3": "TCD", "bloc": "Francophone", "region": "Central Africa", "weight": 2, "is_big4": False},
    {"name": "Burundi", "iso3": "BDI", "bloc": "Francophone", "region": "East Africa", "weight": 2, "is_big4": False},
    {"name": "Congo, Rep.", "iso3": "COG", "bloc": "Francophone", "region": "Central Africa", "weight": 2, "is_big4": False},
    {"name": "Gabon", "iso3": "GAB", "bloc": "Francophone", "region": "Central Africa", "weight": 2, "is_big4": False},
    {"name": "Mauritania", "iso3": "MRT", "bloc": "Francophone", "region": "West Africa", "weight": 2, "is_big4": False},
    {"name": "Central African Republic", "iso3": "CAF", "bloc": "Francophone", "region": "Central Africa", "weight": 1, "is_big4": False},
    {"name": "Comoros", "iso3": "COM", "bloc": "Francophone", "region": "East Africa", "weight": 1, "is_big4": False},

    # Lusophone SSA
    {"name": "Angola", "iso3": "AGO", "bloc": "Lusophone", "region": "Central Africa", "weight": 4, "is_big4": False},
    {"name": "Mozambique", "iso3": "MOZ", "bloc": "Lusophone", "region": "Southern Africa", "weight": 4, "is_big4": False},
    {"name": "Cabo Verde", "iso3": "CPV", "bloc": "Lusophone", "region": "West Africa", "weight": 2, "is_big4": False},
    {"name": "Guinea-Bissau", "iso3": "GNB", "bloc": "Lusophone", "region": "West Africa", "weight": 1, "is_big4": False},
    {"name": "Sao Tome and Principe", "iso3": "STP", "bloc": "Lusophone", "region": "Central Africa", "weight": 1, "is_big4": False},
    {"name": "Equatorial Guinea", "iso3": "GNQ", "bloc": "Lusophone", "region": "Central Africa", "weight": 1, "is_big4": False},

    # Other Anglophone & Horn of Africa
    {"name": "Tanzania", "iso3": "TZA", "bloc": "Anglophone", "region": "East Africa", "weight": 7, "is_big4": False},
    {"name": "Uganda", "iso3": "UGA", "bloc": "Anglophone", "region": "East Africa", "weight": 6, "is_big4": False},
    {"name": "Ethiopia", "iso3": "ETH", "bloc": "Anglophone", "region": "East Africa", "weight": 6, "is_big4": False},
    {"name": "Zimbabwe", "iso3": "ZWE", "bloc": "Anglophone", "region": "Southern Africa", "weight": 4, "is_big4": False},
    {"name": "Malawi", "iso3": "MWI", "bloc": "Anglophone", "region": "Southern Africa", "weight": 3, "is_big4": False},
    {"name": "Sierra Leone", "iso3": "SLE", "bloc": "Anglophone", "region": "West Africa", "weight": 3, "is_big4": False},
    {"name": "Liberia", "iso3": "LBR", "bloc": "Anglophone", "region": "West Africa", "weight": 2, "is_big4": False},
    {"name": "Botswana", "iso3": "BWA", "bloc": "Anglophone", "region": "Southern Africa", "weight": 2, "is_big4": False},
    {"name": "Namibia", "iso3": "NAM", "bloc": "Anglophone", "region": "Southern Africa", "weight": 2, "is_big4": False},
    {"name": "Gambia, The", "iso3": "GMB", "bloc": "Anglophone", "region": "West Africa", "weight": 2, "is_big4": False},
    {"name": "Eswatini", "iso3": "SWZ", "bloc": "Anglophone", "region": "Southern Africa", "weight": 1, "is_big4": False},
    {"name": "Lesotho", "iso3": "LSO", "bloc": "Anglophone", "region": "Southern Africa", "weight": 1, "is_big4": False},
    {"name": "Sudan", "iso3": "SDN", "bloc": "Anglophone", "region": "East Africa", "weight": 2, "is_big4": False},
    {"name": "South Sudan", "iso3": "SSD", "bloc": "Anglophone", "region": "East Africa", "weight": 1, "is_big4": False},
    {"name": "Somalia, Fed. Rep.", "iso3": "SOM", "bloc": "Anglophone", "region": "East Africa", "weight": 1, "is_big4": False},
    {"name": "Eritrea", "iso3": "ERI", "bloc": "Anglophone", "region": "East Africa", "weight": 1, "is_big4": False},
    {"name": "Seychelles", "iso3": "SYC", "bloc": "Anglophone", "region": "East Africa", "weight": 1, "is_big4": False},
]

# Sampling probabilities
_weights = [c["weight"] for c in COUNTRY_TAXONOMY]
_total_w = sum(_weights)
COUNTRY_PROBS = [w / _total_w for w in _weights]

def pick_country():
    return np.random.choice(COUNTRY_TAXONOMY, p=COUNTRY_PROBS)

def get_country_metric(iso3, metric_name):
    if iso3 in ssa_macro.index and pd.notna(ssa_macro.loc[iso3, metric_name]):
        return float(ssa_macro.loc[iso3, metric_name])
    return MEDIANS[metric_name]

def maybe_missing(val, rate=0.08):
    """Introduce authentic missing data rate (~8%) on non-mandatory fields."""
    if random.random() < rate:
        return np.nan
    return val

# =============================================================================
# 1. TEACHER SURVEY GENERATOR (Calibrated)
# =============================================================================
def generate_teacher_data(n=600):
    rows = []
    
    school_types = [
        "Public / government", "Low-fee private", "Other private (fee-paying)",
        "Faith-based or mission school", "Community school", "School in a refugee camp or serving displaced learners"
    ]
    school_type_probs = [0.56, 0.18, 0.08, 0.10, 0.05, 0.03]
    
    locations = ["A major city", "A smaller town", "A rural area"]
    # SSA demographic average: 40% rural, 32% town, 28% city
    loc_probs = [0.28, 0.32, 0.40]
    
    teaching_levels = [
        "Primary (about ages 6 to 12)",
        "Lower secondary (about ages 12 to 15)",
        "Upper secondary (about ages 15 to 18)",
        "Early years / pre-primary (about ages 3 to 5)",
        "Primary; Lower secondary"
    ]
    
    subjects = ["Maths and science", "Languages and literacy", "Humanities and social studies", "All subjects", "Other"]
    
    # Grounded qualitative remarks reflecting authentic field reports
    sample_quotes = [
        "Solar batteries installed 2 years ago died; we only use tablets when the sun shines directly.",
        "Parents struggle with data bundles. We send WhatsApp homework, but only 5 students can download PDFs.",
        "We have 78 learners in Grade 4. Individual devices are impossible, so we do rotating groups of 10.",
        "ChatGPT writes good lesson outlines, but assumes experiments with materials our rural school does not have.",
        "Kinyarwanda is the only language our early pupils understand, but all digital apps on the tablets are in English.",
        "Our Bemba pupils cannot understand the formal English math apps; I have to translate every question orally.",
        "I spend 15% of my monthly salary buying personal mobile data to submit weekly student grades on the ministry portal.",
        "The tablets arrived with donor funding, but once the grant ended there was no budget to replace broken screens.",
        "Mobile phones are banned during classes, which helps concentration, but students have no other access to technology.",
        "Without reliable grid power in the village, our computer lab remains locked for months at a time."
    ]

    for i in range(1, n + 1):
        c = pick_country()
        iso3 = c["iso3"]
        loc = np.random.choice(locations, p=loc_probs)
        st = np.random.choice(school_types, p=school_type_probs)
        
        # -------------------------------------------------------------
        # CALIBRATION: Pillar 2 (Electricity & Internet)
        # -------------------------------------------------------------
        rural_elec_rate = get_country_metric(iso3, "EG.ELC.ACCS.RU.ZS") / 100.0
        urban_elec_rate = get_country_metric(iso3, "EG.ELC.ACCS.UR.ZS") / 100.0
        net_user_rate = get_country_metric(iso3, "IT.NET.USER.ZS") / 100.0
        broadband_rate = get_country_metric(iso3, "IT.NET.BBND.P2")  # per 100
        
        # Electricity reliability conditioned on country macro & location
        if loc == "A rural area":
            has_grid = random.random() < rural_elec_rate
            if not has_grid:
                # GEM 2023: >70% rural SSA deficit
                elec = np.random.choice(["No electricity at all", "Unreliable (frequent cuts)"], p=[0.72, 0.28])
            else:
                elec = np.random.choice(["Mostly reliable", "Unreliable (frequent cuts)"], p=[0.35, 0.65])
                
            # Internet: In rural areas, broadband is near-zero across SSA
            if net_user_rate < 0.25:  # e.g., Zambia, Burundi
                internet = np.random.choice(["No internet at all", "Mobile data only (personal cost)", "Intermittent / slow"], p=[0.58, 0.34, 0.08])
            elif net_user_rate < 0.50:  # e.g., Kenya, Rwanda
                internet = np.random.choice(["No internet at all", "Mobile data only (personal cost)", "Intermittent / slow", "High-speed / reliable"], p=[0.42, 0.42, 0.14, 0.02])
            else:  # High-connectivity (Mauritius, Cabo Verde)
                internet = np.random.choice(["High-speed / reliable", "Intermittent / slow", "Mobile data only (personal cost)"], p=[0.60, 0.30, 0.10])
                
        elif loc == "A smaller town":
            has_power = random.random() < ((urban_elec_rate + rural_elec_rate) / 2.0)
            if not has_power:
                elec = np.random.choice(["No electricity at all", "Unreliable (frequent cuts)"], p=[0.40, 0.60])
            else:
                elec = np.random.choice(["Mostly reliable", "Unreliable (frequent cuts)", "Always reliable"], p=[0.45, 0.45, 0.10])
                
            internet = np.random.choice(["Mobile data only (personal cost)", "Intermittent / slow", "High-speed / reliable", "No internet at all"], p=[0.50, 0.32, 0.10, 0.08])
            
        else:  # A major city
            has_power = random.random() < urban_elec_rate
            if not has_power:
                elec = "Unreliable (frequent cuts)"
            else:
                elec = np.random.choice(["Always reliable", "Mostly reliable", "Unreliable (frequent cuts)"], p=[0.35, 0.50, 0.15])
                
            if broadband_rate > 10.0:  # Mauritius
                internet = np.random.choice(["High-speed / reliable", "Intermittent / slow", "Mobile data only (personal cost)"], p=[0.65, 0.25, 0.10])
            else:
                internet = np.random.choice(["Intermittent / slow", "Mobile data only (personal cost)", "High-speed / reliable", "No internet at all"], p=[0.42, 0.38, 0.18, 0.02])

        # Digital tool use conditioned on electricity and internet
        if elec == "No electricity at all" and "No internet" in internet:
            uses_digital = np.random.choice(["Yes", "No, not at present"], p=[0.25, 0.75])
        else:
            uses_digital = np.random.choice(["Yes", "No, not at present"], p=[0.82, 0.18])
            
        tools_pool = ["Learning or subject apps", "Messaging groups (WhatsApp/Telegram)", "Content or video platforms",
                      "Tablet or phone with lesson guides", "Assessment or quiz tools", "AI tools (ChatGPT/Gemini)", "Radio or TV lessons"]
        tools_used = "; ".join(random.sample(tools_pool, k=random.randint(1, 3))) if uses_digital == "Yes" else "None"

        # -------------------------------------------------------------
        # CALIBRATION: Pillar 4 (Class Size & Teacher Capacity)
        # -------------------------------------------------------------
        ptr = get_country_metric(iso3, "SE.PRM.ENRL.TC.ZS")
        if ptr > 50:  # Rwanda (59.5), Malawi, etc.
            class_size = np.random.choice(["Fewer than 30", "30–50", "51–80", "More than 80"], p=[0.05, 0.25, 0.45, 0.25])
        elif ptr < 25:  # Mauritius (16.2), Seychelles
            class_size = np.random.choice(["Fewer than 30", "30–50", "51–80", "More than 80"], p=[0.65, 0.30, 0.05, 0.00])
        else:  # Kenya (30.7), Zambia (42.1)
            class_size = np.random.choice(["Fewer than 30", "30–50", "51–80", "More than 80"], p=[0.15, 0.45, 0.30, 0.10])

        # -------------------------------------------------------------
        # CALIBRATION: Pillar 5 & 6 (Linguistic Gap & AI Performance)
        # Conditioned on AfroBench / IrokoBench benchmarks
        # -------------------------------------------------------------
        if iso3 == "KEN":
            # Kiswahili + English: IrokoBench relative score ~62%
            ai_lang_handling = np.random.choice(["Well", "Adequately", "Poorly", "Students mostly use English/French instead", "Don't know"], p=[0.14, 0.38, 0.28, 0.14, 0.06])
            lang_comp = np.random.choice(["Well", "Partly", "Hardly at all, it's a new language for them", "It varies a lot between students"], p=[0.45, 0.38, 0.05, 0.12])
        elif iso3 == "RWA":
            # Kinyarwanda dominant at home; IrokoBench relative score ~38%
            ai_lang_handling = np.random.choice(["Well", "Adequately", "Poorly", "Students mostly use English/French instead", "Don't know"], p=[0.06, 0.24, 0.48, 0.16, 0.06])
            lang_comp = np.random.choice(["Well", "Partly", "Hardly at all, it's a new language for them", "It varies a lot between students"], p=[0.30, 0.48, 0.12, 0.10])
        elif iso3 == "ZMB":
            # 73 languages; Bemba/Nyanja AfroBench score ~18%
            ai_lang_handling = np.random.choice(["Well", "Adequately", "Poorly", "Students mostly use English/French instead", "Don't know"], p=[0.03, 0.15, 0.62, 0.14, 0.06])
            lang_comp = np.random.choice(["Well", "Partly", "Hardly at all, it's a new language for them", "It varies a lot between students"], p=[0.28, 0.44, 0.16, 0.12])
        elif iso3 == "MUS":
            # Mauritian Creole; high bilingual English/French literacy
            ai_lang_handling = np.random.choice(["Well", "Adequately", "Poorly", "Students mostly use English/French instead", "Don't know"], p=[0.12, 0.28, 0.30, 0.24, 0.06])
            lang_comp = np.random.choice(["Well", "Partly", "Hardly at all, it's a new language for them", "It varies a lot between students"], p=[0.70, 0.22, 0.02, 0.06])
        else:
            # Regional generic SSA
            ai_lang_handling = np.random.choice(["Well", "Adequately", "Poorly", "Students mostly use English/French instead", "Don't know"], p=[0.08, 0.22, 0.42, 0.18, 0.10])
            lang_comp = np.random.choice(["Well", "Partly", "Hardly at all, it's a new language for them", "It varies a lot between students"], p=[0.38, 0.38, 0.10, 0.14])

        # AI Uptake & Confidence
        ai_use = np.random.choice(["Regularly", "Sometimes", "Tried once or twice", "Never"], p=[0.16, 0.26, 0.25, 0.33])
        ai_conf = np.random.choice(["Very confident", "Fairly confident", "A little", "Not at all"], p=[0.12, 0.32, 0.36, 0.20])
        ai_training = np.random.choice(["Yes, good support", "Yes, but limited", "No"], p=[0.08, 0.26, 0.66])
        
        # Workload
        workload = np.random.choice(["Reduce it a lot", "Reduce it a little", "No difference", "Add a little", "Add a lot"], p=[0.15, 0.32, 0.18, 0.24, 0.11])

        row = {
            "Response_ID": f"TCH-{i:04d}",
            "Country": c["name"],
            "Linguistic_Bloc": c["bloc"],
            "Region": c["region"],
            "School_Type": st,
            "School_Location": loc,
            "Class_Size": class_size,
            "Teaching_Levels": np.random.choice(teaching_levels),
            "Subject_Area": np.random.choice(subjects),
            "Experience_Years": np.random.choice(["Less than 3 years", "3–10 years", "More than 10 years"], p=[0.22, 0.46, 0.32]),
            "Uses_Digital_Tools": uses_digital,
            "Digital_Tools_Used": tools_used,
            "Electricity_Reliability": elec,
            "Internet_Reliability": internet,
            "Student_Language_Comprehension": lang_comp,
            "Workload_Impact": workload,
            "AI_Use_Frequency": ai_use,
            "AI_Confidence": ai_conf,
            "AI_Training_Received": ai_training,
            "AI_Local_Language_Handling": ai_lang_handling,
            "Phone_Rules": np.random.choice(["Phones not allowed at all", "Allowed only at certain times", "No rules", "Don't know"], p=[0.55, 0.32, 0.10, 0.03]),
            "Harm_Reporting_Known": np.random.choice(["Yes, there is a school procedure", "Yes, informally", "No"], p=[0.28, 0.44, 0.28]),
            "Private_Tutoring_Prevalence": np.random.choice(["Almost none", "A small number", "About half", "Most students", "Don't know"], p=[0.22, 0.32, 0.24, 0.16, 0.06]),
            "Qualitative_Comment": np.random.choice(sample_quotes) if random.random() < 0.40 else np.nan
        }
        
        # Introduce realistic missing fields (5-8%)
        for col in ["Class_Size", "AI_Confidence", "Student_Language_Comprehension", "Workload_Impact"]:
            row[col] = maybe_missing(row[col], 0.06)
            
        rows.append(row)
        
    return pd.DataFrame(rows)


# =============================================================================
# 2. PROVIDER SURVEY GENERATOR (Calibrated)
# =============================================================================
def generate_provider_data(n=120):
    rows = []
    
    org_types = ["For-profit company", "Social enterprise", "NGO or non-profit", "Public body or state-owned organisation"]
    
    offerings = [
        "Learning content or apps for learners",
        "Tutoring or exam preparation",
        "Tools for teachers (lesson plans, coaching)",
        "School or learning-management systems",
        "Skills, vocational or workforce training",
        "Hardware, devices or connectivity"
    ]
    
    breakdown_stages = [
        "Budget availability or delays in funding release",
        "Lengthy or opaque public procurement cycles",
        "Lack of clear technical specifications from ministry",
        "Political changes or leadership turnover",
        "Teacher resistance or lack of continuous PD support"
    ]

    for i in range(1, n + 1):
        c = pick_country()
        is_big4 = c.get("is_big4", False)
        
        # -------------------------------------------------------------
        # CALIBRATION: Pillar 3 (Capital & Revenue Models)
        # HolonIQ 2025: 70% D2C models
        # Briter 2025: 86% capital concentration in 'Big Four'
        # -------------------------------------------------------------
        revenue_model = np.random.choice(
            ["Direct from families (B2C)", "Donor grants / philanthropic", "Ministry / public procurement (B2G)", "Schools fee (B2B)"],
            p=[0.68, 0.16, 0.10, 0.06]  # HolonIQ 70% D2C calibrated
        )
        
        # Team size & Ownership conditioned on Big Four vs peripheral
        if is_big4:
            team_size = np.random.choice(["1–10", "11–50", "51–200", "More than 200"], p=[0.24, 0.44, 0.24, 0.08])
            ownership = np.random.choice([
                "Founded in Sub-Saharan Africa, mainly locally owned",
                "Founded in Sub-Saharan Africa, with foreign investment",
                "Subsidiary/branch of organization based outside SSA"
            ], p=[0.42, 0.40, 0.18])
            active_users = np.random.choice([
                "Fewer than 1,000", "1,000–10,000", "10,001–100,000", "100,001–1 million", "More than 1 million"
            ], p=[0.10, 0.26, 0.34, 0.22, 0.08])
        else:
            team_size = np.random.choice(["1–10", "11–50", "51–200", "More than 200"], p=[0.55, 0.35, 0.08, 0.02])
            ownership = np.random.choice([
                "Founded in Sub-Saharan Africa, mainly locally owned",
                "Founded in Sub-Saharan Africa, with foreign investment",
                "Subsidiary/branch of organization based outside SSA"
            ], p=[0.72, 0.18, 0.10])
            active_users = np.random.choice([
                "Fewer than 1,000", "1,000–10,000", "10,001–100,000", "100,001–1 million", "More than 1 million"
            ], p=[0.26, 0.40, 0.24, 0.08, 0.02])

        # -------------------------------------------------------------
        # CALIBRATION: Pillar 2 (Delivery Channel & Data Payment)
        # -------------------------------------------------------------
        data_payment = np.random.choice(
            ["Users pay", "Covered by programme/donor", "Free via zero-rated telco deal", "Offline / no data needed"],
            p=[0.64, 0.18, 0.10, 0.08]
        )
        
        # Offline capability: ~26% require broadband connection
        offline_cap = np.random.choice(
            ["Yes, fully offline", "Partly (syncs when connected)", "No, it needs a connection"],
            p=[0.28, 0.46, 0.26]
        )

        # -------------------------------------------------------------
        # CALIBRATION: Pillar 5 (Local Language Support Gap)
        # EdTech Hub / Analysis B: <15% of solutions support indigenous SSA languages
        # -------------------------------------------------------------
        lang_support = np.random.choice(
            ["English/French/Portuguese only", "1–2 local languages", "3 or more local languages"],
            p=[0.76, 0.17, 0.07]  # Calibrated down from arbitrary 24% for 3+
        )

        # -------------------------------------------------------------
        # CALIBRATION: Pillar 6 (Evidence Base Held)
        # GEEAP 2023: rigorous RCTs are exceedingly rare (<6% in practice)
        # -------------------------------------------------------------
        evidence = np.random.choice([
            "Internal user metrics / analytics only",
            "Qualitative feedback / teacher testimonials",
            "Quasi-experimental study / independent evaluation",
            "Full Randomized Controlled Trial (RCT)"
        ], p=[0.46, 0.34, 0.15, 0.05])

        # Country operations
        op_count = np.random.choice([1, 2, 3, 5, 8], p=[0.50, 0.25, 0.14, 0.08, 0.03])
        ops = [c["name"]] + [other["name"] for other in random.sample(COUNTRY_TAXONOMY, min(op_count - 1, len(COUNTRY_TAXONOMY)-1))]
        ops = list(set(ops))
        operating_str = "; ".join(ops) if random.random() > 0.3 else ", ".join(ops)

        row = {
            "Provider_ID": f"PRV-{i:03d}",
            "Org_Name": f"EdTech Venture {i:03d}",
            "HQ_Country": c["name"],
            "Operating_Countries": operating_str,
            "Org_Type": np.random.choice(org_types, p=[0.52, 0.28, 0.16, 0.04]),
            "Ownership_Model": ownership,
            "Founded_Period": np.random.choice(["Before 2010", "2010–2015", "2016–2020", "2021 or later"], p=[0.10, 0.26, 0.38, 0.26]),
            "Team_Size": team_size,
            "Primary_Offering": np.random.choice(offerings),
            "Target_Users": "; ".join(random.sample(["Learners", "Teachers", "School leaders", "Parents", "Ministries"], k=random.randint(1, 3))),
            "Active_Users_Past_12M": active_users,
            "Delivery_Channels": "; ".join(random.sample([
                "Smartphone app", "Web browser", "Basic phone (SMS, USSD)", "Messaging apps (WhatsApp)", "Preloaded offline devices"
            ], k=random.randint(1, 2))),
            "Offline_Capability": offline_cap,
            "Minimum_Device": np.random.choice(["A basic phone", "A low-cost smartphone", "A tablet or computer", "Dedicated device"], p=[0.14, 0.56, 0.26, 0.04]),
            "Data_Payment_Model": data_payment,
            "Local_Language_Support": lang_support,
            "Revenue_Model": revenue_model,
            "Evidence_Level_Held": evidence,
            "Procurement_Breakdown_Point": np.random.choice(breakdown_stages),
            "AI_Features_Included": np.random.choice(["Yes, embedded into core product", "Piloting / in development", "No AI features"], p=[0.24, 0.36, 0.40]),
            "Meaningful_Wellbeing_Safeguards": np.random.choice(["Strongly agree", "Agree", "Neither", "Disagree"], p=[0.28, 0.50, 0.16, 0.06])
        }
        
        for col in ["Active_Users_Past_12M", "Data_Payment_Model", "Evidence_Level_Held"]:
            row[col] = maybe_missing(row[col], 0.07)
            
        rows.append(row)
        
    return pd.DataFrame(rows)


# =============================================================================
# 3. EXPERT CONSULTATION GENERATOR (Calibrated)
# =============================================================================
def generate_expert_data(n=80):
    rows = []
    
    vantages = [
        "Policy / ministry / regulator", "Research / academia", "Donor, funder or development partner",
        "NGO or agency delivery", "EdTech provision (building/selling)", "Mobile network or telecoms operator"
    ]
    
    # -------------------------------------------------------------
    # CALIBRATION: Pillar 3 (Frontiers 2026 / mHealth 'Pilot Graveyard')
    # 62% collapse, 26% token shrink, only 8% absorbed by ministry
    # -------------------------------------------------------------
    pilot_outcomes = [
        "It stops completely or collapses",
        "It shrinks to a small token presence",
        "Ministry absorbs and funds core operational costs",
        "Community / parents step in to sustain it"
    ]
    pilot_outcome_probs = [0.62, 0.26, 0.08, 0.04]
    
    constraints = [
        "Electricity and internet infrastructure gaps",
        "Teacher digital confidence and lack of continuous coaching",
        "Unsustainable recurrent funding when donor projects end",
        "Device procurement, maintenance and replacement costs",
        "Curriculum misalignment and language mismatch"
    ]
    
    equity_risks = [
        "Rural and remote learners",
        "Displaced, refugee and crisis-affected learners",
        "Girls and young women facing device access disparity",
        "Children with disabilities and special needs",
        "Learners speaking indigenous / non-dominant languages"
    ]

    for i in range(1, n + 1):
        c = pick_country()
        vantage = np.random.choice(vantages, p=[0.24, 0.26, 0.20, 0.16, 0.10, 0.04])
        
        # -------------------------------------------------------------
        # CALIBRATION: Pillar 6 (AI Readiness Score)
        # AfroBench & IrokoBench: AI is far from classroom ready in SSA
        # -------------------------------------------------------------
        ai_readiness = np.random.choice([1, 2, 3, 4, 5], p=[0.42, 0.36, 0.15, 0.05, 0.02])

        row = {
            "Expert_ID": f"EXP-{i:03d}",
            "Evaluated_Country": c["name"],
            "Region": c["region"],
            "Linguistic_Bloc": c["bloc"],
            "Vantage_Point": vantage,
            "Years_In_System": np.random.choice(["Less than 2", "2–5", "6–10", "More than 10"], p=[0.08, 0.26, 0.36, 0.30]),
            "Primary_Decision_Driver": np.random.choice([
                "Donors and international agencies",
                "Ministry of Education leadership",
                "Commercial EdTech vendors",
                "Regional / local governments",
                "Schools and headteachers"
            ], p=[0.44, 0.32, 0.15, 0.06, 0.03]),
            "Primary_Funding_Source": np.random.choice([
                "Donors / development banks",
                "National government budget",
                "Parents / households out of pocket",
                "Private philanthropic foundations"
            ], p=[0.50, 0.24, 0.18, 0.08]),
            "Donor_Exit_Fate": np.random.choice(pilot_outcomes, p=pilot_outcome_probs),
            "Realistic_Evidence_Threshold": np.random.choice([
                "Proof of concept and user feedback",
                "Pre-post learning gain evaluation",
                "Quasi-experimental comparison group study",
                "Full Randomized Controlled Trial (RCT)"
            ], p=[0.34, 0.44, 0.17, 0.05]),
            "AI_Classroom_Readiness_Score": ai_readiness,
            "Top_System_Constraint": np.random.choice(constraints, p=[0.36, 0.26, 0.24, 0.09, 0.05]),
            "Most_Consequential_Equity_Risk": np.random.choice(equity_risks, p=[0.40, 0.22, 0.18, 0.12, 0.08]),
            "Telco_Role_Significance": np.random.choice([
                "Essential partner in zero-rating & connectivity",
                "Transactional payment provider only",
                "Limited or passive involvement",
                "Unexplored potential"
            ], p=[0.24, 0.36, 0.28, 0.12]),
            "Structured_Pedagogy_Support": np.random.choice([
                "Strongly agree - structured tablets provide essential scaffolding",
                "Agree with caveats - risks deskilling teachers if too rigid",
                "Disagree - too prescriptive for heterogeneous classrooms"
            ], p=[0.46, 0.40, 0.14])
        }
        
        for col in ["Realistic_Evidence_Threshold", "AI_Classroom_Readiness_Score", "Most_Consequential_Equity_Risk"]:
            row[col] = maybe_missing(row[col], 0.05)
            
        rows.append(row)
        
    return pd.DataFrame(rows)


def main():
    output_dir = "/workspaces/CC_3/data/raw"
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "SSA_Survey_Responses_Calibrated.xlsx")
    
    print(f"Generating calibrated synthetic survey responses across 48 SSA countries...")
    df_teachers = generate_teacher_data(n=600)
    df_providers = generate_provider_data(n=120)
    df_experts = generate_expert_data(n=80)
    
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        df_teachers.to_excel(writer, sheet_name="Teachers", index=False)
        df_providers.to_excel(writer, sheet_name="Providers", index=False)
        df_experts.to_excel(writer, sheet_name="Experts", index=False)
        
    print(f"✓ Created {out_path}:")
    print(f"   - Teachers:  {len(df_teachers)} rows, {df_teachers.shape[1]} columns")
    print(f"   - Providers: {len(df_providers)} rows, {df_providers.shape[1]} columns")
    print(f"   - Experts:   {len(df_experts)} rows, {df_experts.shape[1]} columns")


if __name__ == "__main__":
    main()
