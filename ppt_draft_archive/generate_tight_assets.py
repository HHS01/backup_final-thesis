import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Color Palette matching how_to_develop_idea_final.pptx
BG_COLOR = '#FAF6EE'
DARK_TEAL = '#143E42'
MUTED_TEAL = '#456367'
CORAL = '#D85643'
SAGE_LIGHT = '#E5EADD'
WHITE = '#FFFFFF'
BORDER_GRAY = '#D0D8C8'

# -------------------------------------------------------------
# 1. Inverted-U Hypothesis (TIGHT & HIGH CONTRAST)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=220, facecolor=BG_COLOR)
ax.set_facecolor(BG_COLOR)

x = np.linspace(0.1, 10, 500)
y = 11.5 * (1 - np.exp(-0.65 * x)) - 0.22 * (x**1.85)
ax.plot(x, y, color=DARK_TEAL, linewidth=3.5)

# Points
x_ssa = 1.6
y_ssa = 11.5 * (1 - np.exp(-0.65 * x_ssa)) - 0.22 * (x_ssa**1.85)
ax.scatter([x_ssa], [y_ssa], color=CORAL, s=150, zorder=5)
ax.annotate("Sub-Saharan Africa\nSteep Initial Gains\n(Solar/Offline tech)",
            xy=(x_ssa, y_ssa), xytext=(x_ssa + 0.3, y_ssa + 2.0),
            arrowprops=dict(facecolor=CORAL, edgecolor=CORAL, width=1.5, headwidth=6, shrink=0.08),
            fontsize=9, fontweight='bold', color=DARK_TEAL)

x_oecd = 7.0
y_oecd = 11.5 * (1 - np.exp(-0.65 * x_oecd)) - 0.22 * (x_oecd**1.85)
ax.scatter([x_oecd], [y_oecd], color=MUTED_TEAL, s=150, zorder=5)
ax.annotate("OECD Saturation\nScreens Everywhere;\nDiminishing Returns",
            xy=(x_oecd, y_oecd), xytext=(x_oecd - 2.8, y_oecd - 3.2),
            arrowprops=dict(facecolor=MUTED_TEAL, edgecolor=MUTED_TEAL, width=1.5, headwidth=6, shrink=0.08),
            fontsize=9, fontweight='bold', color=DARK_TEAL)

x_mena = 9.2
y_mena = 11.5 * (1 - np.exp(-0.65 * x_mena)) - 0.22 * (x_mena**1.85)
ax.scatter([x_mena], [y_mena], color=CORAL, s=150, zorder=5)
ax.annotate("MENA Hardware Trap\n100% Saturation,\n35%+ Guidance Gap",
            xy=(x_mena, y_mena), xytext=(x_mena - 2.8, y_mena + 1.8),
            arrowprops=dict(facecolor=CORAL, edgecolor=CORAL, width=1.5, headwidth=6, shrink=0.08),
            fontsize=9, fontweight='bold', color=CORAL)

ax.set_title("The Saturation vs. Scarcity Divide", fontsize=12, fontweight='bold', color=DARK_TEAL, pad=10)
ax.set_xlabel("Technology Saturation & Screen Exposure  \u2192", fontsize=9.5, fontweight='bold', color=MUTED_TEAL)
ax.set_ylabel("Learning Impact  \u2192", fontsize=9.5, fontweight='bold', color=MUTED_TEAL)
ax.set_xlim(0, 10.5)
ax.set_ylim(-0.5, 10.5)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color(MUTED_TEAL)

ax.set_xticks([])
ax.set_yticks([])
plt.savefig('tight_inverted_u.png', dpi=220, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.02)
plt.close()

# -------------------------------------------------------------
# 2. Causal Feedback Loop (TIGHT)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=220, facecolor=BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.axis('off')

# Left Loop: Wicked Problem
c_left = patches.Circle((0.26, 0.50), 0.35, facecolor=WHITE, edgecolor=CORAL, linewidth=2.2, linestyle='--')
ax.add_patch(c_left)
ax.text(0.26, 0.74, "Data Scarcity", fontsize=9, fontweight='bold', color=CORAL, ha='center')
ax.text(0.44, 0.50, "Unfit\nSolutions", fontsize=9, fontweight='bold', color=CORAL, ha='center')
ax.text(0.26, 0.24, "Low Adoption\n(Shelfware)", fontsize=9, fontweight='bold', color=CORAL, ha='center')
ax.text(0.08, 0.50, "<3% VC\nFreeze", fontsize=9, fontweight='bold', color=CORAL, ha='center')
ax.text(0.26, 0.50, "WICKED\nPROBLEM\nTRAP", fontsize=10, fontweight='bold', color=CORAL, ha='center', va='center')

# Right Loop: Bottom-Up Opportunity
c_right = patches.Circle((0.74, 0.50), 0.35, facecolor=SAGE_LIGHT, edgecolor=DARK_TEAL, linewidth=2.2)
ax.add_patch(c_right)
ax.text(0.74, 0.74, "Teacher Input\n(AoA Surveys)", fontsize=9, fontweight='bold', color=DARK_TEAL, ha='center')
ax.text(0.92, 0.50, "EdTech 4.0\nDesign", fontsize=9, fontweight='bold', color=DARK_TEAL, ha='center')
ax.text(0.74, 0.24, "Resilient\nAdoption", fontsize=9, fontweight='bold', color=DARK_TEAL, ha='center')
ax.text(0.56, 0.50, "Open Data\nConfidence", fontsize=9, fontweight='bold', color=DARK_TEAL, ha='center')
ax.text(0.74, 0.50, "BOTTOM-UP\nOPPORTUNITY", fontsize=9.5, fontweight='bold', color=DARK_TEAL, ha='center', va='center')

ax.text(0.5, 0.94, "Cyclical Causal Loops: Breaking the Trap", fontsize=12, fontweight='bold', color=DARK_TEAL, ha='center')
plt.savefig('tight_causal_loop.png', dpi=220, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.02)
plt.close()

# -------------------------------------------------------------
# 3. EdTech 4.0 Evolution (TIGHT)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=220, facecolor=BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.axis('off')

generations = [
    ("1.0", "Hardware Drops", "2000–2010\n• OLPC & tablets\n• No power/training\n• High failure", MUTED_TEAL, WHITE),
    ("2.0", "E-Portals & LMS", "2010–2018\n• Desktop portals\n• Broadband bias\n• Urban elite focus", MUTED_TEAL, WHITE),
    ("3.0", "Cloud Apps/SaaS", "2018–2023\n• Silicon Valley VC\n• Low ARPU crisis\n• Post-boom crunch", CORAL, WHITE),
    ("4.0", "Offline-First AI", "2024+\n• Solar micro-servers\n• SMS/USSD & local\n• Teacher co-design", DARK_TEAL, SAGE_LIGHT)
]

for idx, (gen, title, desc, color, card_bg) in enumerate(generations):
    x0 = 0.02 + idx * 0.245
    y0 = 0.12
    w = 0.225
    h = 0.72
    rect = patches.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.02", facecolor=card_bg, edgecolor=color, linewidth=2.0)
    ax.add_patch(rect)
    ax.text(x0 + w/2, y0 + h - 0.08, f"EdTech {gen}", fontsize=9.5, fontweight='bold', color=color, ha='center')
    ax.text(x0 + w/2, y0 + h - 0.18, title, fontsize=8.5, fontweight='bold', color=DARK_TEAL, ha='center')
    ax.text(x0 + w/2, y0 + 0.20, desc, fontsize=7.5, color=MUTED_TEAL, ha='center', va='center')

ax.text(0.5, 0.94, "Evolution of EdTech Paradigms", fontsize=12, fontweight='bold', color=DARK_TEAL, ha='center')
plt.savefig('tight_edtech_evolution.png', dpi=220, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.02)
plt.close()

# -------------------------------------------------------------
# 4. Realistic Mockup of the EEA_2 Dashboard Interface (TIGHT)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=220, facecolor='#F6F7F9')
ax.set_facecolor('#F6F7F9')
ax.axis('off')

# Browser Header bar
rect_bar = patches.Rectangle((0, 0.88), 1.0, 0.12, transform=ax.transAxes, facecolor='#1E242E', zorder=2)
ax.add_patch(rect_bar)
for idx, c in enumerate(['#E34948', '#F59E0B', '#10B981']):
    circle = patches.Circle((0.03 + idx * 0.025, 0.94), 0.014, transform=ax.transAxes, facecolor=c, zorder=3)
    ax.add_patch(circle)
ax.text(0.14, 0.94, "https://rsnl42.github.io/EEA_2/  |  PISA 2025 AI Observatory",
        transform=ax.transAxes, fontsize=8, color='#ECEFF4', va='center', zorder=3)

# Dashboard Hero Title inside
ax.text(0.04, 0.80, "OECD PISA 2025: Cross-National AI & Device Dashboard",
        transform=ax.transAxes, fontsize=10, fontweight='bold', color='#14181F')
ax.text(0.04, 0.74, "85 Systems  |  MENA Deep-Dive: UAE, Jordan, Morocco, Qatar, Saudi Arabia",
        transform=ax.transAxes, fontsize=7.5, color='#4A5361')

# 4 Cards representing actual EEA_2 modules
cards_info = [
    ("AI Portfolios: Drafting vs Learning", "OECD I.B1.4.53\nDrafting offload (48%) vs Guided learning (22%)\nHigh student intensity in Gulf", "#FAF5FF", "#6B21A8", 0.04, 0.40),
    ("Use Guidance: School Policy Deficit", "OECD I.B1.4.55 & 68\nGuidance lags adoption by 35+ pts\nUniversal bottleneck across MENA", "#FFF7ED", "#C2410C", 0.52, 0.40),
    ("Capacity Bottlenecks", "OECD I.B1.4.14\nDevice count does not equal readiness\nTeacher PD is primary weakest link", "#F0FDF4", "#166534", 0.04, 0.06),
    ("Time-Use: Learning vs Leisure", "OECD I.B1.4.21\nWeekday/weekend screen split\nHeavy tails (>5h/day) cause distraction", "#EEF6FF", "#1E65BD", 0.52, 0.06)
]

for title, body, bg, border, x_pos, y_pos in cards_info:
    rect = patches.FancyBboxPatch((x_pos, y_pos), 0.44, 0.28, boxstyle="round,pad=0.015",
                                  facecolor=bg, edgecolor=border, linewidth=1.5, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(x_pos + 0.02, y_pos + 0.22, title, transform=ax.transAxes, fontsize=8, fontweight='bold', color=border)
    ax.text(x_pos + 0.02, y_pos + 0.08, body, transform=ax.transAxes, fontsize=7, color='#14181F', va='bottom')

plt.savefig('tight_dashboard_mockup.png', dpi=220, facecolor='#F6F7F9', bbox_inches='tight', pad_inches=0.02)
plt.close()

# -------------------------------------------------------------
# 5. Sample Artefact Output: Kenya 6-Pillars Scorecard
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=220, facecolor=WHITE)
ax.set_facecolor(WHITE)
ax.axis('off')

# Header
rect_head = patches.FancyBboxPatch((0.02, 0.86), 0.96, 0.12, boxstyle="round,pad=0.01",
                                   facecolor=DARK_TEAL, edgecolor=DARK_TEAL)
ax.add_patch(rect_head)
ax.text(0.05, 0.92, "Artefact Output: Kenya National EdTech Scorecard & Modality Alignment",
        fontsize=9, fontweight='bold', color=WHITE, va='center')
ax.text(0.05, 0.87, "UNESCO Six Pillars Diagnostic Output Engine  |  Source: fetch_6pillars_pipeline.py",
        fontsize=7, color=SAGE_LIGHT, va='center')

# 6 Pillars rows
scorecard_rows = [
    ("P1: Leadership & Vision", "SPI Governance Score: 73.4/100", "Strong data standards; open statistics pipeline", DARK_TEAL),
    ("P2: Infrastructure", "Rural Elec: 67.1% | Broadband: 3.0% | Mobile: 126.5%", "CRITICAL BOTTLENECK: High mobile, low fixed net", CORAL),
    ("P3: Cost & Sustainability", "Edu Budget Share: 27.9% | GDP/cap: $2,133", "High public commitment; CapEx shift needed", MUTED_TEAL),
    ("P4: Capacity & Culture", "Primary Trained: 100% | PTR: 30.7:1", "High formal certification; needs digital pedagogy", DARK_TEAL),
    ("P5: Content & Solutions", "Dakar Hub Typology: SMS & Solar Media", "Recommended Modality: Zero-rated SMS & offline cache", CORAL),
    ("P6: Data & Evidence", "Data Use Score: 90/100", "High community reporting readiness", MUTED_TEAL),
]

for idx, (p_title, p_stat, p_action, p_col) in enumerate(scorecard_rows):
    y_pos = 0.72 - idx * 0.115
    # Box
    rect_row = patches.Rectangle((0.02, y_pos), 0.96, 0.10, facecolor=SAGE_LIGHT if idx % 2 == 1 else '#FAFBF8',
                                 edgecolor=BORDER_GRAY, linewidth=1)
    ax.add_patch(rect_row)
    
    # Text
    ax.text(0.04, y_pos + 0.05, p_title, fontsize=7.5, fontweight='bold', color=p_col, va='center')
    ax.text(0.35, y_pos + 0.05, p_stat, fontsize=7, color=DARK_TEAL, va='center')
    ax.text(0.68, y_pos + 0.05, p_action, fontsize=6.8, fontweight='bold', color=p_col, va='center')

# Bottom Recommendation Badge
rect_rec = patches.FancyBboxPatch((0.02, 0.02), 0.96, 0.09, boxstyle="round,pad=0.01",
                                  facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.5)
ax.add_patch(rect_rec)
ax.text(0.04, 0.065, "DECISION MATRIX VERDICT: Prioritize Solar-Powered Offline Servers & SMS. DO NOT procure Cloud SaaS.",
        fontsize=7.5, fontweight='bold', color='#92400E', va='center')

plt.savefig('tight_artefact_output_kenya.png', dpi=220, facecolor=WHITE, bbox_inches='tight', pad_inches=0.02)
plt.close()

print("All tight, cropped assets generated successfully!")
