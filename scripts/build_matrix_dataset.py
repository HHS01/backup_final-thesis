import csv, json

# 1. Load Country Profiles (48 SSA + 21 MENA)
with open('/workspaces/CC_3/data/processed/latest_country_profiles_6pillars.csv', 'r', encoding='utf-8') as f:
    country_rows = list(csv.DictReader(f))

countries_data = []
for r in country_rows:
    lp = r.get('SE.LPV.PRIM', '').strip()
    lit = r.get('SE.ADT.LITR.ZS', '').strip()
    
    # Transparent Proxy Logic:
    # If Learning Poverty is missing, Adult Literacy Rate is used as the foundational proxy anchor.
    is_lp_proxy = False
    lp_val = None
    if lp:
        try:
            lp_val = round(float(lp), 1)
        except:
            lp_val = None
    
    lit_val = None
    if lit:
        try:
            lit_val = round(float(lit), 1)
        except:
            lit_val = None
            
    if lp_val is None and lit_val is not None:
        is_lp_proxy = True
        lp_val = round(100.0 - lit_val, 1) # Estimated deficit proxy
        
    elec_ru = None
    if r.get('EG.ELC.ACCS.RU.ZS'):
        try:
            elec_ru = round(float(r['EG.ELC.ACCS.RU.ZS']), 1)
        except: pass

    bb = None
    if r.get('IT.NET.BBND.P2'):
        try:
            bb = round(float(r['IT.NET.BBND.P2']), 2)
        except: pass

    countries_data.append({
        'iso3': r['iso3'],
        'country': r['country'],
        'region': r.get('region', 'SSA'),
        'learning_poverty': lp_val,
        'is_lp_proxy': is_lp_proxy,
        'adult_literacy': lit_val,
        'rural_electrification': elec_ru,
        'fixed_broadband_per100': bb
    })

# Sort countries by region (SSA first, then MENA) and name
countries_data.sort(key=lambda x: (0 if x['region'] == 'SSA' else 1, x['country']))

# 2. Load Players & Categorize
with open('/workspaces/CC_3/edtech landscape files/pdf_key_players.csv', 'r', encoding='utf-8') as f:
    player_rows = list(csv.DictReader(f))

mena_countries = {'Egypt', 'Algeria', 'Morocco', 'Tunisia'}
flagged_types = {'identical_list_to:Guinea', 'identical_list_to:Niger', 'university_not_startup'}

# Clustered Domain Classification:
def get_domain(cat):
    c = cat.lower()
    if 'k-12' in c: return 'K-12 & Foundational'
    if 'upskilling' in c or 'tvet' in c or 'higher ed' in c: return 'Workforce, TVET & Skills'
    if 'lms' in c or 'platform' in c: return 'Learning Platforms & LMS'
    if 'content' in c: return 'Digital Content & Literacy'
    if 'ai' in c or 'inclusion' in c or 'data' in c: return 'AI, Inclusion & Frontier'
    return 'Ecosystem & Marketplaces'

all_players = []
for p in player_rows:
    c_name = p['country']
    cat = p['category']
    domain = get_domain(cat)
    is_mena = c_name in mena_countries
    is_flagged = bool(p['qa_flag'])
    all_players.append({
        'name': p['name'],
        'country': c_name,
        'category': cat,
        'domain': domain,
        'is_mena': is_mena,
        'qa_flag': p['qa_flag'],
        'page': p['pdf_page']
    })

# 3. Select 25 Core Representative SSA Cohort
# Criteria: Cross-category, high prominence, foundational relevance, distributed across core SSA hubs
core_25_names = [
    # K-12 & Foundational (8)
    "uLesson", "Gradely", "Nigenius", "FoondaMate", "Ayaprep", "QKnow EdTech", "Yello App", "Expand Education",
    # Digital Content & Literacy (3)
    "Snapplify", "Reflective Learning", "Education Channel",
    # Learning Platforms & LMS (4)
    "Teesas", "SchoolsFocus", "20/20 EdTech", "Digital School Technologies",
    # Workforce, TVET & Skills (5)
    "WeThinkCode", "GetSmarter", "Xarala", "Rwanda Coding Academy", "Bakeli School of Technology",
    # AI, Inclusion & Frontier (3)
    "Dext Technology", "DeafCanTalk", "Databeez",
    # Ecosystem & Marketplaces (2)
    "Tuteria", "DoLessons"
]

for p in all_players:
    p['is_core_25'] = (p['name'] in core_25_names)

print(f"Total countries: {len(countries_data)} (SSA: {len([c for c in countries_data if c['region']=='SSA'])}, MENA: {len([c for c in countries_data if c['region']=='MENA'])})")
print(f"Total players: {len(all_players)} (Core 25: {len([p for p in all_players if p['is_core_25']])}, Non-core SSA: {len([p for p in all_players if not p['is_core_25'] and not p['is_mena'] and not p['qa_flag']])}, MENA: {len([p for p in all_players if p['is_mena']] )}, Flagged: {len([p for p in all_players if p['qa_flag']] )})")

# Export to a standalone clean JS file for dashboard consumption
output_js = f"""// Generated Supply-Demand Matrix Dataset
// Countries: 48 Sub-Saharan Africa + 21 MENA Reference
// Players: 25 Core Representative Cohort + 123 Indexed Catalog
const MATRIX_COUNTRIES = {json.dumps(countries_data, indent=2)};
const MATRIX_PLAYERS = {json.dumps(all_players, indent=2)};
"""

with open('/workspaces/CC_3/data/processed/supply_demand_matrix_data.js', 'w', encoding='utf-8') as f:
    f.write(output_js)

print("Saved data/processed/supply_demand_matrix_data.js successfully!")
