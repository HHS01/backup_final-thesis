import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Color Palette matching presentation
BG_COLOR = '#FAF6EE'
DARK_TEAL = '#143E42'
MUTED_TEAL = '#456367'
CORAL = '#D85643'
SAGE_LIGHT = '#E5EADD'
WHITE = '#FFFFFF'
BORDER_GRAY = '#D0D8C8'

# -------------------------------------------------------------
# 1. Causal Feedback Loop: Wicked Problem vs. Bottom-Up Opportunity
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=200, facecolor=BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.axis('off')

# Title
ax.text(0.5, 0.95, "The Cyclical Causal Feedback Loop: Wicked Problem vs. Opportunity",
        fontsize=11.5, fontweight='bold', color=DARK_TEAL, ha='center', va='top')

# Left Loop: The Vicious Cycle (Wicked Problem)
circle_left = patches.Circle((0.26, 0.48), 0.36, facecolor=WHITE, edgecolor=CORAL, linewidth=2.2, linestyle='--')
ax.add_patch(circle_left)

ax.text(0.26, 0.74, "1. Severe Data Scarcity", fontsize=8.5, fontweight='bold', color=CORAL, ha='center', va='center')
ax.text(0.26, 0.67, "(No localized classroom metrics)", fontsize=7.5, color=MUTED_TEAL, ha='center', va='center')

ax.text(0.44, 0.48, "2. Harder to\nBuild Fit Solutions", fontsize=8.5, fontweight='bold', color=CORAL, ha='center', va='center')
ax.text(0.44, 0.38, "(Imported SaaS fails)", fontsize=7.5, color=MUTED_TEAL, ha='center', va='center')

ax.text(0.26, 0.22, "3. Low Adoption & Attrition", fontsize=8.5, fontweight='bold', color=CORAL, ha='center', va='center')
ax.text(0.26, 0.16, "(Hardware locked in cupboards)", fontsize=7.5, color=MUTED_TEAL, ha='center', va='center')

ax.text(0.08, 0.48, "4. Disinvestment &\nSkepticism", fontsize=8.5, fontweight='bold', color=CORAL, ha='center', va='center')
ax.text(0.08, 0.38, "(<3% Global VC to Africa)", fontsize=7.5, color=MUTED_TEAL, ha='center', va='center')

ax.text(0.26, 0.48, "WICKED\nPROBLEM\nLOOP", fontsize=10, fontweight='bold', color=CORAL, ha='center', va='center')

# Arrows for left loop
ax.annotate("", xy=(0.38, 0.66), xytext=(0.32, 0.73), arrowprops=dict(arrowstyle="->", color=CORAL, lw=2))
ax.annotate("", xy=(0.38, 0.30), xytext=(0.44, 0.37), arrowprops=dict(arrowstyle="->", color=CORAL, lw=2))
ax.annotate("", xy=(0.14, 0.30), xytext=(0.20, 0.23), arrowprops=dict(arrowstyle="->", color=CORAL, lw=2))
ax.annotate("", xy=(0.14, 0.66), xytext=(0.08, 0.59), arrowprops=dict(arrowstyle="->", color=CORAL, lw=2))

# Right Loop: The Bottom-Up Opportunity (The Solution)
circle_right = patches.Circle((0.74, 0.48), 0.36, facecolor=SAGE_LIGHT, edgecolor=DARK_TEAL, linewidth=2.2)
ax.add_patch(circle_right)

ax.text(0.74, 0.74, "1. Participatory Ground-Truthing", fontsize=8.5, fontweight='bold', color=DARK_TEAL, ha='center', va='center')
ax.text(0.74, 0.67, "(AoA Surveys & Teacher Voices)", fontsize=7.5, color=MUTED_TEAL, ha='center', va='center')

ax.text(0.92, 0.48, "2. Context-First\nDesign (EdTech 4.0)", fontsize=8.5, fontweight='bold', color=DARK_TEAL, ha='center', va='center')
ax.text(0.92, 0.38, "(Offline, SMS, Solar)", fontsize=7.5, color=MUTED_TEAL, ha='center', va='center')

ax.text(0.74, 0.22, "3. Resilient Field Efficacy", fontsize=8.5, fontweight='bold', color=DARK_TEAL, ha='center', va='center')
ax.text(0.74, 0.16, "(Sustained teacher adoption)", fontsize=7.5, color=MUTED_TEAL, ha='center', va='center')

ax.text(0.56, 0.48, "4. Open 6-Pillars\nEvidence", fontsize=8.5, fontweight='bold', color=DARK_TEAL, ha='center', va='center')
ax.text(0.56, 0.38, "(Data-informed funding)", fontsize=7.5, color=MUTED_TEAL, ha='center', va='center')

ax.text(0.74, 0.48, "BOTTOM-UP\nOPPORTUNITY\nBREAKTHROUGH", fontsize=9.5, fontweight='bold', color=DARK_TEAL, ha='center', va='center')

# Arrows for right loop
ax.annotate("", xy=(0.86, 0.66), xytext=(0.80, 0.73), arrowprops=dict(arrowstyle="->", color=DARK_TEAL, lw=2))
ax.annotate("", xy=(0.86, 0.30), xytext=(0.92, 0.37), arrowprops=dict(arrowstyle="->", color=DARK_TEAL, lw=2))
ax.annotate("", xy=(0.62, 0.30), xytext=(0.68, 0.23), arrowprops=dict(arrowstyle="->", color=DARK_TEAL, lw=2))
ax.annotate("", xy=(0.62, 0.66), xytext=(0.56, 0.59), arrowprops=dict(arrowstyle="->", color=DARK_TEAL, lw=2))

plt.tight_layout()
plt.savefig('chart_causal_loop.png', dpi=200, facecolor=BG_COLOR)
plt.close()

# -------------------------------------------------------------
# 2. EdTech 4.0 Evolution Diagram
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.0), dpi=200, facecolor=BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.axis('off')

generations = [
    ("EdTech 1.0", "Hardware Drops", "2000–2010\nOLPC, smartboards\nNo teacher training\nHigh failure rate", MUTED_TEAL, WHITE),
    ("EdTech 2.0", "E-Learning Portals", "2010–2018\nDesktop LMS, PDFs\nBroadband assumed\nUrban school bias", MUTED_TEAL, WHITE),
    ("EdTech 3.0", "Cloud & Mobile Apps", "2018–2023\nSaaS, video streaming\nSilicon Valley model\nVC crunch & low ARPU", CORAL, WHITE),
    ("EdTech 4.0", "Context-Aware & AI", "2024+\nOffline-first, solar\nHuman-centric AI\nBottom-up pedagogy", DARK_TEAL, SAGE_LIGHT)
]

for idx, (gen, title, desc, color, card_bg) in enumerate(generations):
    x0 = 0.03 + idx * 0.245
    y0 = 0.15
    w = 0.225
    h = 0.68
    
    rect = patches.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.02",
                                  facecolor=card_bg, edgecolor=color, linewidth=2.0)
    ax.add_patch(rect)
    
    # Badge
    ax.text(x0 + w/2, y0 + h - 0.08, gen, fontsize=10, fontweight='bold', color=color, ha='center')
    ax.text(x0 + w/2, y0 + h - 0.18, title, fontsize=9, fontweight='bold', color=DARK_TEAL, ha='center')
    ax.text(x0 + w/2, y0 + 0.18, desc, fontsize=8, color=MUTED_TEAL, ha='center', va='center')
    
    # Arrow between stages
    if idx < 3:
        ax.annotate("", xy=(x0 + w + 0.022, y0 + h/2), xytext=(x0 + w - 0.005, y0 + h/2),
                    arrowprops=dict(arrowstyle="->", color=CORAL, lw=2.2))

ax.text(0.5, 0.94, "The Evolution of Educational Technology Paradigms",
        fontsize=12, fontweight='bold', color=DARK_TEAL, ha='center')
plt.tight_layout()
plt.savefig('chart_edtech_evolution.png', dpi=200, facecolor=BG_COLOR)
plt.close()

# -------------------------------------------------------------
# 3. Country Case Comparison: Nigeria (SSA) vs. Jordan (MENA)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=200, facecolor=BG_COLOR)
ax.set_facecolor(BG_COLOR)

pillars = [
    'P1: Governance\n(SPI Index)',
    'P2: Power\n(Rural Elec. %)',
    'P2: Telecom\n(Internet %)',
    'P3: Spend\n(Edu % Budget)',
    'P4: Teacher\n(Sec. Trained %)'
]
# Nigeria vs Jordan
nigeria = [69.1, 23.5, 41.2, 3.0, 66.8]
jordan = [78.8, 100.0, 95.6, 9.8, 100.0]

x = np.arange(len(pillars))
width = 0.35

rects1 = ax.bar(x - width/2, nigeria, width, label='Nigeria (SSA Case Study)', color=CORAL)
rects2 = ax.bar(x + width/2, jordan, width, label='Jordan (MENA Case Study)', color=DARK_TEAL)

ax.set_ylabel('Score / Percentage (%)', fontsize=9.5, fontweight='bold', color=MUTED_TEAL)
ax.set_title('Pillar Diagnostic: Nigeria (Grassroots Surge) vs. Jordan (Hardware Saturation)',
             fontsize=11.5, fontweight='bold', color=DARK_TEAL, pad=12)
ax.set_xticks(x)
ax.set_xticklabels(pillars, fontsize=8.5, fontweight='bold', color=DARK_TEAL)
ax.legend(loc='upper right', frameon=True, facecolor=WHITE, edgecolor=BORDER_GRAY, fontsize=8.5)
ax.set_ylim(0, 115)

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}%' if h > 10 else f'{h:.1f}',
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=CORAL)

for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}%' if h > 10 else f'{h:.1f}',
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=DARK_TEAL)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color(MUTED_TEAL)

plt.tight_layout()
plt.savefig('chart_country_deepdive.png', dpi=200, facecolor=BG_COLOR)
plt.close()

# -------------------------------------------------------------
# 4. Realistic Mockup of the EEA_2 Dashboard Interface
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.4), dpi=200, facecolor=WHITE)
ax.set_facecolor('#F6F7F9')
ax.axis('off')

# Browser Header bar
rect_bar = patches.Rectangle((0, 0.90), 1.0, 0.10, transform=ax.transAxes, facecolor='#1E242E', zorder=2)
ax.add_patch(rect_bar)
# Window dots
for idx, c in enumerate(['#E34948', '#F59E0B', '#10B981']):
    circle = patches.Circle((0.03 + idx * 0.02, 0.95), 0.012, transform=ax.transAxes, facecolor=c, zorder=3)
    ax.add_patch(circle)
ax.text(0.12, 0.95, "https://rsnl42.github.io/EEA_2/  •  PISA 2025: Digital Devices & AI in School",
        transform=ax.transAxes, fontsize=8, color='#ECEFF4', va='center', zorder=3)

# Dashboard Hero Title inside
ax.text(0.04, 0.83, "OECD PISA 2025: Cross-National AI & Device Observatory",
        transform=ax.transAxes, fontsize=10.5, fontweight='bold', color='#14181F')
ax.text(0.04, 0.77, "85 School Systems  |  MENA Deep Dive: UAE, Qatar, Jordan, Morocco, Saudi Arabia  |  10 Core Domains",
        transform=ax.transAxes, fontsize=8, color='#4A5361')

# 4 Cards representing actual EEA_2 modules
cards_info = [
    ("AI Portfolios: Drafting vs. Learning", "OECD I.B1.4.53\nDrafting offloading (48%) vs Guided learning (22%)\nHigh intensity among MENA students", "#FAF5FF", "#6B21A8", 0.04, 0.44),
    ("Use Guidance: The School Policy Gap", "OECD I.B1.4.55 & 68\nGuidance lags adoption by 35+ percentage pts\nUniversal bottleneck in Gulf & OECD", "#FFF7ED", "#C2410C", 0.52, 0.44),
    ("Capacity Bottlenecks & Weakest Links", "OECD I.B1.4.14\nBandwidth, hardware shortages vs teacher PD\n4 recurring national bottleneck shapes", "#F0FDF4", "#166534", 0.04, 0.08),
    ("Time-Use: Learning vs. Leisure", "OECD I.B1.4.21\nWeekday vs weekend leisure ratios\nHeavy screen tails (>5h/day) in high-access hubs", "#EEF6FF", "#1E65BD", 0.52, 0.08)
]

for title, body, bg, border, x_pos, y_pos in cards_info:
    rect = patches.FancyBboxPatch((x_pos, y_pos), 0.44, 0.28, boxstyle="round,pad=0.015",
                                  facecolor=bg, edgecolor=border, linewidth=1.5, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(x_pos + 0.02, y_pos + 0.22, title, transform=ax.transAxes, fontsize=8.5, fontweight='bold', color=border)
    ax.text(x_pos + 0.02, y_pos + 0.08, body, transform=ax.transAxes, fontsize=7.5, color='#14181F', va='bottom')

plt.tight_layout()
plt.savefig('dashboard_mockup.png', dpi=200, facecolor=WHITE)
plt.close()

print("All new charts and diagrams generated successfully!")
