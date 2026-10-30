import matplotlib.pyplot as plt
import numpy as np

# Palette matching how_to_develop_idea_final.pptx
BG_COLOR = '#FAF6EE'
TEAL_DARK = '#143E42'
TEAL_MUTED = '#456367'
CORAL = '#D85643'
SAGE_LIGHT = '#E5EADD'

# 1. Inverted-U Hypothesis
fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=200, facecolor=BG_COLOR)
ax.set_facecolor(BG_COLOR)

x = np.linspace(0.1, 10, 500)
y = 11.5 * (1 - np.exp(-0.65 * x)) - 0.22 * (x**1.85)

ax.plot(x, y, color=TEAL_DARK, linewidth=3.5, label='Net Learning Impact')

# Annotations
x_ssa = 1.6
y_ssa = 11.5 * (1 - np.exp(-0.65 * x_ssa)) - 0.22 * (x_ssa**1.85)
ax.scatter([x_ssa], [y_ssa], color=CORAL, s=140, zorder=5)
ax.annotate("Sub-Saharan Africa\n(Steep Initial Gain from\nSolar / Offline Media)",
            xy=(x_ssa, y_ssa), xytext=(x_ssa + 0.2, y_ssa + 2.4),
            arrowprops=dict(facecolor=CORAL, edgecolor=CORAL, width=1.5, headwidth=7, shrink=0.08),
            fontsize=9, fontweight='bold', color=TEAL_DARK)

x_oecd = 6.8
y_oecd = 11.5 * (1 - np.exp(-0.65 * x_oecd)) - 0.22 * (x_oecd**1.85)
ax.scatter([x_oecd], [y_oecd], color=TEAL_MUTED, s=140, zorder=5)
ax.annotate("High-Income OECD Peak\n(Device Ubiquity;\nDiminishing Returns)",
            xy=(x_oecd, y_oecd), xytext=(x_oecd - 2.5, y_oecd - 3.4),
            arrowprops=dict(facecolor=TEAL_MUTED, edgecolor=TEAL_MUTED, width=1.5, headwidth=7, shrink=0.08),
            fontsize=9, fontweight='bold', color=TEAL_DARK)

x_mena = 9.2
y_mena = 11.5 * (1 - np.exp(-0.65 * x_mena)) - 0.22 * (x_mena**1.85)
ax.scatter([x_mena], [y_mena], color=CORAL, s=140, zorder=5)
ax.annotate("MENA Hardware Trap\n(100% Saturation, High AI,\n35%+ Guidance Deficit)",
            xy=(x_mena, y_mena), xytext=(x_mena - 2.7, y_mena + 1.8),
            arrowprops=dict(facecolor=CORAL, edgecolor=CORAL, width=1.5, headwidth=7, shrink=0.08),
            fontsize=9, fontweight='bold', color=CORAL)

ax.set_title("The Saturation vs. Scarcity Divide (Inverted-U Hypothesis)", fontsize=12, fontweight='bold', color=TEAL_DARK, pad=12)
ax.set_xlabel("Technology Saturation & Device Access  \u2192", fontsize=10, fontweight='bold', color=TEAL_MUTED)
ax.set_ylabel("Educational Impact  \u2192", fontsize=10, fontweight='bold', color=TEAL_MUTED)
ax.set_xlim(0, 10.5)
ax.set_ylim(-0.5, 10.5)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color(TEAL_MUTED)
    ax.spines[spine].set_linewidth(1.2)

ax.set_xticks([])
ax.set_yticks([])
plt.tight_layout()
plt.savefig('chart_inverted_u.png', dpi=200, facecolor=BG_COLOR)
plt.close()

# 2. Regional Benchmark Comparison Chart
fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=200, facecolor=BG_COLOR)
ax.set_facecolor(BG_COLOR)

indicators = [
    'Rural Electricity\n(% pop)',
    'Internet Users\n(% pop)',
    'Fixed Broadband\n(per 100)',
    'Trained Teachers\nSec. (%)',
    'Pupil-Teacher\nRatio (Sec)'
]
ssa_vals = [42.0, 38.8, 2.48, 69.3, 23.65]
mena_vals = [94.8, 82.1, 14.91, 87.2, 13.21]

y_pos = np.arange(len(indicators))
bar_height = 0.35

rects1 = ax.barh(y_pos + bar_height/2, ssa_vals, bar_height, label='Sub-Saharan Africa (48 nations)', color=CORAL)
rects2 = ax.barh(y_pos - bar_height/2, mena_vals, bar_height, label='MENA (21 nations)', color=TEAL_DARK)

ax.set_yticks(y_pos)
ax.set_yticklabels(indicators, fontsize=9, fontweight='bold', color=TEAL_DARK)
ax.invert_yaxis()
ax.set_xlabel('Indicator Metric / Percentage', fontsize=9.5, fontweight='bold', color=TEAL_MUTED)
ax.set_title('Meso-Level Structural Reality: SSA vs. MENA Divide', fontsize=12, fontweight='bold', color=TEAL_DARK, pad=12)
ax.legend(loc='lower right', frameon=True, facecolor='white', edgecolor=SAGE_LIGHT, fontsize=8.5)

# Value labels
for rect in rects1:
    width = rect.get_width()
    ax.annotate(f'{width:.1f}',
                xy=(width, rect.get_y() + rect.get_height() / 2),
                xytext=(4, 0), textcoords="offset points",
                ha='left', va='center', fontsize=8, fontweight='bold', color=CORAL)

for rect in rects2:
    width = rect.get_width()
    ax.annotate(f'{width:.1f}',
                xy=(width, rect.get_y() + rect.get_height() / 2),
                xytext=(4, 0), textcoords="offset points",
                ha='left', va='center', fontsize=8, fontweight='bold', color=TEAL_DARK)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color(TEAL_MUTED)
ax.set_xlim(0, 110)

plt.tight_layout()
plt.savefig('chart_regional_benchmarks.png', dpi=200, facecolor=BG_COLOR)
plt.close()

# 3. UNESCO 6 Pillars Icon / Card Layout Diagram
fig, ax = plt.subplots(figsize=(7.5, 4.0), dpi=200, facecolor=BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.axis('off')

pillars = [
    ("1. Coordination & Leadership", "National digital policies, procurement, governance", CORAL),
    ("2. Connectivity & Infrastructure", "Grid power, rural 4G/solar, offline servers, devices", TEAL_DARK),
    ("3. Cost & Sustainability", "OpEx lifecycle, $200M+ WB loans, maintenance funds", TEAL_MUTED),
    ("4. Capacity & Culture", "Teacher digital pedagogy, guidance, parental buy-in", CORAL),
    ("5. Content & Solutions", "OER, curriculum alignment, local languages, edtech hubs", TEAL_DARK),
    ("6. Data & Evidence", "SPI statistical capacity, ethical AI, privacy & protection", TEAL_MUTED),
]

for idx, (title, desc, color) in enumerate(pillars):
    row = idx // 2
    col = idx % 2
    x0 = 0.05 + col * 0.48
    y0 = 0.68 - row * 0.32
    w = 0.44
    h = 0.26
    
    # Draw rounded-like box
    box = plt.Rectangle((x0, y0), w, h, transform=ax.transAxes,
                        facecolor='white', edgecolor=color, linewidth=2.0, zorder=2)
    ax.add_patch(box)
    
    # Title badge
    ax.text(x0 + 0.02, y0 + h - 0.065, title, transform=ax.transAxes,
            fontsize=9.5, fontweight='bold', color=color, zorder=3)
    ax.text(x0 + 0.02, y0 + 0.05, desc, transform=ax.transAxes,
            fontsize=8, color=TEAL_MUTED, wrap=True, zorder=3, verticalalignment='bottom')

ax.set_title("UNESCO DTC Six Pillars for Digital Transformation in Education", fontsize=12, fontweight='bold', color=TEAL_DARK, y=1.02)
plt.tight_layout()
plt.savefig('chart_six_pillars.png', dpi=200, facecolor=BG_COLOR)
plt.close()

print("All charts generated successfully!")
