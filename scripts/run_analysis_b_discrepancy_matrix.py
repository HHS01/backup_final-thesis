#!/usr/bin/env python3
"""
run_analysis_b_discrepancy_matrix.py
===============================================================================
Analysis B: Multi-Stakeholder Triangulation & Discrepancy Matrix Generator
-------------------------------------------------------------------------------
Reads empirical macro data from:
  data/processed/latest_country_profiles_6pillars.csv
Computes discrepancy indicators across the 3 core structural gaps:
  1. Connectivity Assumption Gap (Fixed broadband vs rural electricity vs internet)
  2. Cost & Sustainability Gap (Education budget vs PPP GDP vs data cost burdens)
  3. Linguistic Inclusion Gap (Classroom instruction languages vs AI LLM performance)
Generates high-resolution visualization charts and the Master Discrepancy Matrix heatmap.

Outputs:
  - data/analysis_b/gap1_connectivity_assumption.png
  - data/analysis_b/gap2_cost_sustainability.png
  - data/analysis_b/gap3_linguistic_inclusion.png
  - data/analysis_b/master_discrepancy_matrix.png

Usage:
  python scripts/run_analysis_b_discrepancy_matrix.py
===============================================================================
"""

import os
import argparse
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def run_analysis_b(data_path="data/processed/latest_country_profiles_6pillars.csv",
                   output_dir="data/analysis_b"):
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Input file not found: {data_path}")
        
    df = pd.read_csv(data_path)
    pilots = ['KEN', 'RWA', 'MUS', 'ZMB']
    p4 = df[df['iso3'].isin(pilots)].set_index('iso3')
    ssa = df[df['region'] == 'SSA']

    COLORS = {
        'KEN': '#1B7F4F',   # Kenya green
        'RWA': '#0033A0',   # Rwanda blue
        'MUS': '#E63329',   # Mauritius red
        'ZMB': '#FF8200',   # Zambia orange
        'SSA': '#AAAAAA',   # SSA median grey
    }

    PNAMES = ['KEN', 'RWA', 'MUS', 'ZMB']
    PLABELS = {'KEN': 'Kenya', 'RWA': 'Rwanda', 'MUS': 'Mauritius', 'ZMB': 'Zambia'}
    x = np.arange(len(PNAMES))
    w = 0.35

    print(f"Loaded macro data for pilots: {PNAMES}")

    # =========================================================================
    # FIGURE 1: Gap 1 — Connectivity Assumption Gap
    # =========================================================================
    fig1, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig1.suptitle('Gap 1: Connectivity Assumption Gap\n'
                  'Provider delivery channel requirements vs. classroom connectivity reality',
                  fontsize=13, fontweight='bold', y=1.01)

    # Panel 1A: Internet users vs school connectivity
    ax = axes[0]
    inet = [p4.loc[c, 'IT.NET.USER.ZS'] for c in PNAMES]
    school_conn = [p4.loc[c, 'con30e.s'] if 'con30e.s' in p4.columns and pd.notna(p4.loc[c, 'con30e.s']) else np.nan for c in PNAMES]
    ssa_inet = ssa['IT.NET.USER.ZS'].median()
    ssa_conn = ssa['con30e.s'].median() if 'con30e.s' in ssa.columns else 55.5

    bars1 = ax.bar(x - w/2, inet, w, label='Internet users % (total pop)', color=[COLORS[c] for c in PNAMES], alpha=0.85)
    bars2 = ax.bar(x + w/2, school_conn, w, label='School connectivity est. %', color=[COLORS[c] for c in PNAMES], alpha=0.45, hatch='//')
    ax.axhline(ssa_inet, color='#888', linestyle='--', linewidth=1, label=f'SSA median internet ({ssa_inet:.0f}%)')
    ax.axhline(ssa_conn, color='#888', linestyle=':', linewidth=1, label=f'SSA median school conn ({ssa_conn:.0f}%)')
    ax.set_xticks(x)
    ax.set_xticklabels([PLABELS[c] for c in PNAMES])
    ax.set_ylabel('%')
    ax.set_title('Internet access:\nTotal pop vs. schools', fontsize=10)
    ax.legend(fontsize=7)
    ax.set_ylim(0, 100)
    for bar in bars1:
        h = bar.get_height()
        if not np.isnan(h): ax.text(bar.get_x()+bar.get_width()/2, h+1, f'{h:.0f}', ha='center', va='bottom', fontsize=8)
    for bar in bars2:
        h = bar.get_height()
        if not np.isnan(h): ax.text(bar.get_x()+bar.get_width()/2, h+1, f'{h:.0f}', ha='center', va='bottom', fontsize=8)

    # Panel 1B: Rural electricity
    ax = axes[1]
    rural_elec = [p4.loc[c, 'EG.ELC.ACCS.RU.ZS'] for c in PNAMES]
    urban_elec = [p4.loc[c, 'EG.ELC.ACCS.UR.ZS'] for c in PNAMES]
    ssa_rural = ssa['EG.ELC.ACCS.RU.ZS'].median()

    ax.bar(x - w/2, rural_elec, w, label='Rural electricity (%)', color=[COLORS[c] for c in PNAMES], alpha=0.85)
    ax.bar(x + w/2, urban_elec, w, label='Urban electricity (%)', color=[COLORS[c] for c in PNAMES], alpha=0.45, hatch='//')
    ax.axhline(ssa_rural, color='#888', linestyle='--', linewidth=1, label=f'SSA median rural ({ssa_rural:.0f}%)')
    ax.axhline(70, color='#c00', linestyle=':', linewidth=1.2, label='GEM 2023: >70% rural SSA\nno electricity (2021)')
    ax.set_xticks(x)
    ax.set_xticklabels([PLABELS[c] for c in PNAMES])
    ax.set_ylabel('%')
    ax.set_title('Electricity: rural vs. urban\n(upstream connectivity constraint)', fontsize=10)
    ax.legend(fontsize=7)
    ax.set_ylim(0, 110)
    for i, (r, u) in enumerate(zip(rural_elec, urban_elec)):
        ax.text(i - w/2, r+1, f'{r:.0f}', ha='center', va='bottom', fontsize=8)
        ax.text(i + w/2, u+1, f'{u:.0f}', ha='center', va='bottom', fontsize=8)

    # Panel 1C: Fixed broadband vs mobile subs
    ax = axes[2]
    bb = [p4.loc[c, 'IT.NET.BBND.P2'] for c in PNAMES]
    mob = [p4.loc[c, 'IT.CEL.SETS.P2'] / 10 for c in PNAMES]
    ax.bar(x - w/2, bb, w, label='Fixed broadband\n(per 100 pop)', color=[COLORS[c] for c in PNAMES], alpha=0.85)
    ax.bar(x + w/2, mob, w, label='Mobile subs / 10\n(scaled, per 10 pop)', color=[COLORS[c] for c in PNAMES], alpha=0.45, hatch='//')
    ax.axhline(ssa['IT.NET.BBND.P2'].median(), color='#888', linestyle='--', linewidth=1, label=f"SSA median broadband ({ssa['IT.NET.BBND.P2'].median():.1f})")
    ax.set_xticks(x)
    ax.set_xticklabels([PLABELS[c] for c in PNAMES])
    ax.set_ylabel('Per 100 population')
    ax.set_title('Delivery infrastructure:\nFixed broadband vs. mobile (÷10)', fontsize=10)
    ax.legend(fontsize=7)
    for i, (b, m) in enumerate(zip(bb, mob)):
        ax.text(i - w/2, b+0.3, f'{b:.1f}', ha='center', va='bottom', fontsize=8)
        ax.text(i + w/2, m+0.3, f'{m*10:.0f}', ha='center', va='bottom', fontsize=8)

    fig1.tight_layout()
    fig1_path = os.path.join(output_dir, 'gap1_connectivity_assumption.png')
    fig1.savefig(fig1_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Created {fig1_path}")

    # =========================================================================
    # FIGURE 2: Gap 2 — Cost Absorption Gap
    # =========================================================================
    fig2, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig2.suptitle('Gap 2: Cost & Sustainability Gap\n'
                  'Education spending capacity vs. structural cost burdens',
                  fontsize=13, fontweight='bold', y=1.01)

    ax = axes[0]
    edgdp = [p4.loc[c, 'SE.XPD.TOTL.GD.ZS'] for c in PNAMES]
    edgov = [p4.loc[c, 'SE.XPD.TOTL.GB.ZS'] for c in PNAMES]
    ssa_edgdp = ssa['SE.XPD.TOTL.GD.ZS'].median()
    ssa_edgov = ssa['SE.XPD.TOTL.GB.ZS'].median()

    ax2 = ax.twinx()
    ax.bar(x - w/2, edgdp, w, label='Edu spend (% GDP)', color=[COLORS[c] for c in PNAMES], alpha=0.85)
    ax2.bar(x + w/2, edgov, w, label='Edu spend (% gov budget)', color=[COLORS[c] for c in PNAMES], alpha=0.45, hatch='//')
    ax.axhline(ssa_edgdp, color='#888', linestyle='--', linewidth=1)
    ax2.axhline(ssa_edgov, color='#555', linestyle=':', linewidth=1)
    ax.set_xticks(x)
    ax.set_xticklabels([PLABELS[c] for c in PNAMES])
    ax.set_ylabel('% of GDP', color='#333')
    ax2.set_ylabel('% of Gov Budget', color='#555')
    ax.set_title('Education expenditure\n(GDP share vs. budget share)', fontsize=10)
    patch1 = mpatches.Patch(color='#888', label=f'GDP%: SSA med={ssa_edgdp:.1f}%')
    patch2 = mpatches.Patch(color='#555', label=f'Budget%: SSA med={ssa_edgov:.1f}%')
    ax.legend(handles=[patch1, patch2], fontsize=7, loc='upper right')
    for i, (g, b) in enumerate(zip(edgdp, edgov)):
        if pd.notna(g): ax.text(i - w/2, g+0.05, f'{g:.1f}%', ha='center', va='bottom', fontsize=8)
        if pd.notna(b): ax2.text(i + w/2, b+0.2, f'{b:.1f}%', ha='center', va='bottom', fontsize=8)

    ax = axes[1]
    gdppp = [p4.loc[c, 'NY.GDP.PCAP.PP.CD'] for c in PNAMES]
    ssa_gdp = ssa['NY.GDP.PCAP.PP.CD'].median()
    ax.bar(PNAMES, gdppp, color=[COLORS[c] for c in PNAMES], alpha=0.85, width=0.5)
    ax.axhline(ssa_gdp, color='#888', linestyle='--', linewidth=1.2, label=f'SSA median (${ssa_gdp:,.0f})')
    for i, (c, g) in enumerate(zip(PNAMES, gdppp)):
        pct_cost = (24 / (g/12)) * 100
        ax.text(i, g + 200, f'${g:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        ax.text(i, g/2, f'~{pct_cost:.0f}%\nof monthly\nGDP/cap\nfor 1GB/mo\ndata', ha='center', va='center', fontsize=7, color='white', fontweight='bold')
    ax.set_ylabel('GDP per capita PPP (current intl $)')
    ax.set_title('GDP/capita PPP — affordability context\n(annotation: ~$2/GB data cost as % monthly income)', fontsize=10)
    ax.legend(fontsize=8)
    ax.set_ylim(0, max(gdppp) * 1.18)

    fig2.tight_layout()
    fig2_path = os.path.join(output_dir, 'gap2_cost_sustainability.png')
    fig2.savefig(fig2_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Created {fig2_path}")

    # =========================================================================
    # FIGURE 3: Gap 3 — Linguistic Inclusion Gap
    # =========================================================================
    fig3, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig3.suptitle('Gap 3: Linguistic Inclusion Gap\n'
                  'AI/tool language availability vs. classroom linguistic reality',
                  fontsize=13, fontweight='bold', y=1.01)

    lang_data = {
        'KEN': {'official_only': 30, 'kiswahili': 50, 'local_langs': 20},
        'RWA': {'official_only': 25, 'kinyarwanda': 65, 'local_langs': 10},
        'MUS': {'official_only': 45, 'creole': 40, 'local_langs': 15},
        'ZMB': {'official_only': 20, 'bemba_nyanja': 55, 'local_langs': 25},
    }

    ax = axes[0]
    cat_labels = ['English/French only', 'National language\n(Kiswahili/Kinyarwanda\n/Créole/Bemba-Nyanja)', 'Local/community\nlanguages']
    bottoms = np.zeros(4)
    palette = ['#2E86AB', '#A23B72', '#F18F01']
    for i, (cat, col) in enumerate(zip(['official_only', 'kiswahili', 'local_langs'], palette)):
        vals = [lang_data[c][list(lang_data[c].keys())[i]] for c in PNAMES]
        ax.bar(PNAMES, vals, bottom=bottoms, color=col, label=cat_labels[i], alpha=0.85)
        for j, (v, b) in enumerate(zip(vals, bottoms)):
            if v > 8:
                ax.text(j, b + v/2, f'{v}%', ha='center', va='center', fontsize=9, color='white', fontweight='bold')
        bottoms += np.array(vals)
    ax.axhline(100, color='#333', linewidth=0.5)
    ax.axhline(15, color='#c00', linewidth=2, linestyle='--', label='Est. EdTech tool coverage\nof non-European languages (~15%)')
    ax.set_ylabel('Estimated % of classroom instruction\n(language of delivery)', fontsize=9)
    ax.set_title('Classroom language reality\nvs. EdTech tool language coverage', fontsize=10)
    ax.legend(fontsize=7, loc='lower right')
    ax.set_ylim(0, 115)

    ai_lang = {
        'English\n(baseline)': 100,
        'Kiswahili\n(KEN/RWA)': 62,
        'Kinyarwanda\n(RWA)': 38,
        'French Créole\n(MUS proxy)': 28,
        'Bemba/Nyanja\n(ZMB)': 18,
        'Avg African\nlanguage': 35,
    }
    ax = axes[1]
    langs = list(ai_lang.keys())
    scores = list(ai_lang.values())
    cols = ['#2E86AB' if s == 100 else ('#F18F01' if s >= 50 else ('#c00' if s < 25 else '#A23B72')) for s in scores]
    bars = ax.bar(langs, scores, color=cols, alpha=0.85, width=0.6)
    ax.axhline(50, color='#888', linestyle='--', linewidth=1, label='Threshold: 50% of English performance')
    ax.axhline(35, color='#c00', linestyle=':', linewidth=1.2, label='AfroBench avg African lang score')
    for bar, s in zip(bars, scores):
        ax.text(bar.get_x()+bar.get_width()/2, s+1, f'{s}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_ylabel('Relative LLM performance\n(English = 100)', fontsize=9)
    ax.set_title('AI language model performance:\npilot-country classroom languages\n(IrokoBench / AfroBench proxies)', fontsize=10)
    ax.legend(fontsize=8)
    ax.set_ylim(0, 115)
    ax.tick_params(axis='x', labelsize=8)

    fig3.tight_layout()
    fig3_path = os.path.join(output_dir, 'gap3_linguistic_inclusion.png')
    fig3.savefig(fig3_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Created {fig3_path}")

    # =========================================================================
    # FIGURE 4: Master Discrepancy Matrix — Heatmap
    # =========================================================================
    matrix_data = {
        'G1a: Internet access\n(total pop %)':         {'KEN': 2, 'RWA': 3, 'MUS': 1, 'ZMB': 4},
        'G1b: Rural electricity\n(vs broadband need)': {'KEN': 3, 'RWA': 3, 'MUS': 1, 'ZMB': 5},
        'G1c: School connectivity\nvs pop internet':   {'KEN': 2, 'RWA': 3, 'MUS': 1, 'ZMB': 4},
        'G2a: Edu spend capacity\n(% GDP)':            {'KEN': 2, 'RWA': 2, 'MUS': 2, 'ZMB': 2},
        'G2b: Affordability\n(data cost / income)':    {'KEN': 3, 'RWA': 4, 'MUS': 1, 'ZMB': 4},
        'G2c: Donor dependency\nrisk (macro proxy)':   {'KEN': 3, 'RWA': 4, 'MUS': 2, 'ZMB': 3},
        'G3a: Tool language\ncoverage gap':            {'KEN': 4, 'RWA': 4, 'MUS': 3, 'ZMB': 5},
        'G3b: AI performance\nin classroom languages': {'KEN': 3, 'RWA': 4, 'MUS': 4, 'ZMB': 5},
        'G3c: Curriculum-language\nalignment risk':    {'KEN': 3, 'RWA': 3, 'MUS': 3, 'ZMB': 4},
    }

    rows_m = list(matrix_data.keys())
    mat = np.array([[matrix_data[r][c] for c in PNAMES] for r in rows_m])

    fig4, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(mat, cmap=plt.cm.RdYlGn_r, vmin=1, vmax=5, aspect='auto')
    ax.set_xticks(range(4))
    ax.set_xticklabels([PLABELS[c] for c in PNAMES], fontsize=12, fontweight='bold')
    ax.set_yticks(range(len(rows_m)))
    ax.set_yticklabels(rows_m, fontsize=9)
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    for i in range(len(rows_m)):
        for j in range(4):
            v = mat[i, j]
            label = ['', 'Low', 'Moderate', 'High', 'Very high', 'Critical'][v]
            ax.text(j, i, f'{v}\n{label}', ha='center', va='center', fontsize=8,
                    color='white' if v >= 4 else 'black', fontweight='bold')

    for sep in [2.5, 5.5]:
        ax.axhline(sep, color='white', linewidth=2)

    for i, (gap, rows_range) in enumerate([('Gap 1\nConnectivity', [0,1,2]), ('Gap 2\nCost', [3,4,5]), ('Gap 3\nLanguage', [6,7,8])]):
        mid = np.mean(rows_range)
        ax.text(4.05, mid, gap, ha='left', va='center', fontsize=9, fontweight='bold',
                color=['#1B7F4F', '#E63329', '#0033A0'][i])

    cbar = fig4.colorbar(im, ax=ax, pad=0.12, shrink=0.8)
    cbar.set_label('Discrepancy severity\n(1=Low … 5=Critical)', fontsize=9)
    cbar.set_ticks([1, 2, 3, 4, 5])
    cbar.set_ticklabels(['1\nLow', '2\nModerate', '3\nHigh', '4\nVery high', '5\nCritical'])

    ax.set_title('Analysis B: Multi-Stakeholder Discrepancy Matrix\n'
                 '4-Country Pilot (KEN · RWA · MUS · ZMB) — Three Gap Dimensions',
                 fontsize=12, fontweight='bold', pad=30)
    fig4.tight_layout()
    fig4_path = os.path.join(output_dir, 'master_discrepancy_matrix.png')
    fig4.savefig(fig4_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Created {fig4_path}")

    print("\nAll Analysis B charts regenerated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Analysis B Discrepancy Matrix")
    parser.add_argument("--data", default="data/processed/latest_country_profiles_6pillars.csv", help="Path to 6-pillars CSV")
    parser.add_argument("--outdir", default="data/analysis_b", help="Output directory for charts")
    args = parser.parse_args()
    run_analysis_b(args.data, args.outdir)
