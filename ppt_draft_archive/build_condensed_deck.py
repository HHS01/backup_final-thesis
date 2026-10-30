import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------
# PALETTE MATCHING how_to_develop_idea_final.pptx
# ---------------------------------------------------------
BG_COLOR = RGBColor(0xFA, 0xF6, 0xEE)       # Warm Cream / Ivory
DARK_TEAL = RGBColor(0x14, 0x3E, 0x42)      # Deep Forest Teal
MUTED_TEAL = RGBColor(0x45, 0x63, 0x67)     # Slate Teal
CORAL = RGBColor(0xD8, 0x56, 0x43)          # Terracotta Accent
PALE_SAGE = RGBColor(0xE5, 0xEA, 0xDD)      # Container background
WHITE = RGBColor(0xFF, 0xFF, 0xFF)          # Card background
BORDER_GRAY = RGBColor(0xD0, 0xD8, 0xC8)    # Subtle outline
LIGHT_GRAY = RGBColor(0x8A, 0x9B, 0x9E)     # Subtle footer text

FONT_TITLE = 'DejaVu Sans'
FONT_BODY = 'DejaVu Sans'

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def set_slide_background(slide, color=BG_COLOR):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, eyebrow, title, subtitle=None):
    # Eyebrow (Category Tracker)
    eb_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.3))
    tf_eb = eb_box.text_frame
    tf_eb.word_wrap = True
    tf_eb.margin_left = tf_eb.margin_top = tf_eb.margin_right = tf_eb.margin_bottom = 0
    p_eb = tf_eb.paragraphs[0]
    p_eb.text = eyebrow.upper()
    p_eb.font.name = FONT_BODY
    p_eb.font.size = Pt(11)
    p_eb.font.bold = True
    p_eb.font.color.rgb = CORAL

    # Action Title (Punchy, bold takeaway)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = FONT_TITLE
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = DARK_TEAL

    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.38), Inches(11.733), Inches(0.28))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(11.5)
        p_s.font.color.rgb = MUTED_TEAL

def add_footer(slide, current_slide, total_slides=14):
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.12), Inches(11.733), Inches(0.25))
    tf_f = footer_box.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = f"Master in ICT for Development and Social Good (UniTO / COREP)  |  Draft Presentation  |  Slide {current_slide} of {total_slides}"
    p_f.font.name = FONT_BODY
    p_f.font.size = Pt(9.5)
    p_f.font.color.rgb = LIGHT_GRAY

def create_card(slide, left, top, width, height, bg_color=WHITE, border_color=BORDER_GRAY):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)
    else:
        shape.line.fill.background()
    return shape

def add_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text

# =========================================================================
# SLIDE 1: COVER SLIDE
# =========================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1, DARK_TEAL)
create_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=DARK_TEAL, border_color=CORAL)

tb = s1.shapes.add_textbox(Inches(1.3), Inches(1.2), Inches(10.7), Inches(0.4))
p = tb.text_frame.paragraphs[0]
p.text = "MASTER IN ICT FOR DEVELOPMENT AND SOCIAL GOOD  •  A.Y. 2025–2026"
p.font.name = FONT_BODY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CORAL

tb = s1.shapes.add_textbox(Inches(1.3), Inches(1.65), Inches(10.7), Inches(1.5))
p = tb.text_frame.paragraphs[0]
p.text = "Mapping the EdTech Landscape in\nSub-Saharan Africa and MENA"
p.font.name = FONT_TITLE
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = WHITE

tb = s1.shapes.add_textbox(Inches(1.3), Inches(3.3), Inches(10.7), Inches(0.6))
p = tb.text_frame.paragraphs[0]
p.text = "Bridging Macro Assessment, the UNESCO 6-Pillars Framework, and Grassroots Realities"
p.font.name = FONT_BODY
p.font.size = Pt(15)
p.font.color.rgb = PALE_SAGE

line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.3), Inches(3.95), Inches(10.7), Inches(0.04))
line.fill.solid()
line.fill.fore_color.rgb = CORAL
line.line.fill.background()

tb = s1.shapes.add_textbox(Inches(1.3), Inches(4.2), Inches(10.7), Inches(0.9))
tf = tb.text_frame
tf.word_wrap = True
p1 = tf.paragraphs[0]
p1.text = "PROJECT PURPOSE (30-SECOND PITCH):"
p1.font.bold = True
p1.font.size = Pt(11)
p1.font.color.rgb = CORAL
p2 = tf.add_paragraph()
p2.text = "An open-access diagnostic observatory and decision rubric to prevent the misallocation of EdTech capital in the Global South by reconciling macro benchmarks (OECD PISA), open development APIs, and practitioner ground truth."
p2.font.size = Pt(12)
p2.font.color.rgb = WHITE

tb = s1.shapes.add_textbox(Inches(1.3), Inches(5.4), Inches(10.7), Inches(0.8))
p = tb.text_frame.paragraphs[0]
p.text = "Candidate: Master Degree Candidate  |  Academic Reviewer: Prof. Elisa Bignante  |  UniTO · COREP · Impactskills"
p.font.size = Pt(11)
p.font.color.rgb = PALE_SAGE

add_notes(s1, """[TIMING: 0:00 - 0:30 | 30 SECONDS]
PRESENTER SCRIPT:
"Good morning, Professor Bignante and colleagues. My Master's final project addresses a systemic flaw in international digital education: the tendency to transpose monolithic, high-income technology benchmarks onto low-resource environments. Over the next 10 minutes, I will present our problem diagnosis, theoretical framing, 3-tier triangulated methodology, our live dashboard, country artefact, and decision rubric."
""")

# =========================================================================
# SLIDE 2: STATE OF ED & TECH (SSA VS MENA)
# =========================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "1. State of Education & Technology",
           "Divergent Crises: Acute Foundational Scarcity in SSA vs. Saturation Without Pedagogy in MENA",
           "Included VC & World Bank data show why monolithic global policies misdirect regional investments.")
add_footer(s2, 2)

# Left Column: Sub-Saharan Africa
create_card(s2, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), bg_color=WHITE)
tb = s2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "SUB-SAHARAN AFRICA: FOUNDATIONAL CRISIS"
p.font.bold = True
p.font.size = Pt(12)
p.font.color.rgb = CORAL

stats_ssa = [
    ("87%", "Learning Poverty Rate", "Children unable to read simple text by age 10"),
    ("<3%", "Global EdTech VC Share", "Severe underfunding (Included VC analysis)"),
    ("42%", "Rural Electrification", "Fixed broadband stands at only 2.48% (median 0.56%)")
]
for num, lbl, desc in stats_ssa:
    p = tf.add_paragraph()
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = num + " "
    r1.font.bold = True
    r1.font.size = Pt(24)
    r1.font.color.rgb = CORAL
    r2 = p.add_run()
    r2.text = lbl + "\n"
    r2.font.bold = True
    r2.font.size = Pt(11)
    r2.font.color.rgb = DARK_TEAL
    r3 = p.add_run()
    r3.text = desc
    r3.font.size = Pt(10)
    r3.font.color.rgb = MUTED_TEAL

# Right Column: MENA Paradox
create_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), bg_color=WHITE)
tb = s2.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "MENA REGION: THE SATURATION PARADOX"
p.font.bold = True
p.font.size = Pt(12)
p.font.color.rgb = DARK_TEAL

stats_mena = [
    ("100%", "Device Saturation", "Universal electricity & near-100% internet access"),
    ("Top Tier", "Student AI Drafting Adoption", "High offloading to generative AI for schoolwork"),
    (">35%", "Teacher Guidance Deficit", "School rules lag adoption -> leisure distraction")
]
for num, lbl, desc in stats_mena:
    p = tf.add_paragraph()
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = num + " "
    r1.font.bold = True
    r1.font.size = Pt(24)
    r1.font.color.rgb = DARK_TEAL
    r2 = p.add_run()
    r2.text = lbl + "\n"
    r2.font.bold = True
    r2.font.size = Pt(11)
    r2.font.color.rgb = CORAL
    r3 = p.add_run()
    r3.text = desc
    r3.font.size = Pt(10)
    r3.font.color.rgb = MUTED_TEAL

add_notes(s2, """[TIMING: 0:30 - 1:30 | 60 SECONDS]
PRESENTER SCRIPT:
"In Sub-Saharan Africa, World Bank data reveals learning poverty at a staggering 87%—nearly 9 in 10 children cannot read a simple sentence by age 10. UNESCO estimates an acute deficit of 15 million qualified teachers by 2030. Yet, as Michelle Jideofor's analysis for Included VC highlights, less than 3% of global EdTech venture capital reaches Africa. Traditional Silicon Valley VC models fail because low household purchasing power and infrastructural hurdles require longer runways and infrastructure-level investment.

Conversely, our PISA 2025 dataset reveals the 'MENA Paradox'. In Gulf economies, electricity and devices are virtually 100% saturated. Students are among the highest global adopters of generative AI. Yet, there is a guidance deficit exceeding 35 percentage points: teachers are not trained to integrate AI, resulting in heavy leisure displacement and cognitive offloading."
""")

# =========================================================================
# SLIDE 3: CAUSAL FEEDBACK LOOP
# =========================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "2. Problem Framing",
           "The Cyclical Causal Feedback Loop: Wicked Problem vs. Bottom-Up Opportunity",
           "How structural data scarcity paralyzes EdTech design—and how participatory planning breaks the cycle.")
add_footer(s3, 3)

# Insert the tightly cropped Causal Loop image
if os.path.exists("tight_causal_loop.png"):
    s3.shapes.add_picture("tight_causal_loop.png", Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.1))

create_card(s3, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.1), bg_color=WHITE)
tb = s3.shapes.add_textbox(Inches(8.1), Inches(2.1), Inches(4.1), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "STRATEGIC TAKEAWAY"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = CORAL

p = tf.add_paragraph()
p.text = "Breaking the Trap"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = DARK_TEAL
p.space_after = Pt(8)

loop_bullets = [
    ("The Wicked Trap: ", "Data scarcity obscures classroom realities -> vendors build cloud SaaS -> solutions fail -> donors freeze capital."),
    ("The Opportunity: ", "Bottom-up planning centers teacher constraints and offline architectures before buying software."),
    ("Our Contribution: ", "Bridging macro open APIs with Alliance of Alliances (AoA) ground surveys to create actionable, data-informed investment roadmaps.")
]
for t, b in loop_bullets:
    p = tf.add_paragraph()
    p.space_after = Pt(8)
    p.font.size = Pt(11)
    r1 = p.add_run()
    r1.text = "• " + t
    r1.font.bold = True
    r1.font.color.rgb = DARK_TEAL
    r2 = p.add_run()
    r2.text = b
    r2.font.color.rgb = MUTED_TEAL

add_notes(s3, """[TIMING: 1:30 - 2:30 | 60 SECONDS]
PRESENTER SCRIPT:
"On the left is the 'Wicked Problem Loop': Because developing educational systems suffer from severe data scarcity, international donors and startups build blind solutions—often importing high-bandwidth cloud software. These tools fail in off-grid classrooms. As tablets gather dust in locked cupboards, donors see zero return on investment, cementing skepticism and keeping venture funding below 3%.

However, on the right is the 'Bottom-Up Opportunity': When we anchor planning in participatory ground-truthing—such as the UNESCO Alliance of Alliances teacher surveys—we capture real constraints: intermittent power, shared mobile phones, and language barriers. This enables context-first design, creating resilient field adoption."
""")

# =========================================================================
# SLIDE 4: EDTECH 4.0 EVOLUTION
# =========================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "3. Conceptual Evolution",
           "Paradigm Shift: The Four Generations of Educational Technology to EdTech 4.0",
           "Sustainable digital transformation requires shifting from top-down device distribution to human-centric, offline-first AI.")
add_footer(s4, 4)

if os.path.exists("tight_edtech_evolution.png"):
    s4.shapes.add_picture("tight_edtech_evolution.png", Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.1))

create_card(s4, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.1), bg_color=WHITE)
tb = s4.shapes.add_textbox(Inches(8.1), Inches(2.1), Inches(4.1), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "PARADIGM SHIFT"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = CORAL

p = tf.add_paragraph()
p.text = "Defining EdTech 4.0"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = DARK_TEAL
p.space_after = Pt(8)

edtech_bullets = [
    ("Context-Aware Architecture: ", "Designs for intermittent solar micro-grids, SMS channels, and local caching."),
    ("Pedagogy Over Hardware: ", "Treats teachers as co-designers, reversing the 20-year legacy of unused devices."),
    ("Human-Centric AI: ", "Leverages lightweight, localized AI for teacher assistance and differentiated instruction, avoiding unguided student offloading.")
]
for t, b in edtech_bullets:
    p = tf.add_paragraph()
    p.space_after = Pt(8)
    p.font.size = Pt(11)
    r1 = p.add_run()
    r1.text = "• " + t
    r1.font.bold = True
    r1.font.color.rgb = DARK_TEAL
    r2 = p.add_run()
    r2.text = b
    r2.font.color.rgb = MUTED_TEAL

add_notes(s4, """[TIMING: 2:30 - 3:30 | 60 SECONDS]
PRESENTER SCRIPT:
"To understand why so many EdTech interventions fail, we trace the four generations of educational technology:
EdTech 1.0 (2000–2010) was defined by 'Hardware Drops'—initiatives like One Laptop Per Child, distributed without electricity or teacher training.
EdTech 2.0 (2010–2018) brought E-Learning Portals and LMS platforms, assuming broadband that excluded rural schools.
EdTech 3.0 (2018–2023) brought the cloud and mobile app boom, but Silicon Valley SaaS models cannot survive on African ARPU levels.
We are now entering EdTech 4.0: Context-aware, hybrid, and human-centric. EdTech 4.0 uses offline-first caching, solar micro-servers, SMS channels, and local-language AI tutors to empower teachers."
""")

# =========================================================================
# SLIDE 5: HOLONIQ 2025 AFRICA EDTECH 50 MARKET MAP
# =========================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "3. Market Reality",
           "HolonIQ 2025 Africa EdTech 50: Grounding Supply in Ecosystem Realities",
           "Official market intelligence reveals subsector demand, geographic concentration, and post-VC resilience.")
add_footer(s5, 5)

# Insert the official HolonIQ Market Map image
if os.path.exists("holoniq_2025_ssa_market_map.png"):
    # 16:9 ratio: 6.8 x 3.825 inches
    s5.shapes.add_picture("holoniq_2025_ssa_market_map.png", Inches(0.8), Inches(2.2), Inches(6.8), Inches(3.825))

create_card(s5, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.1), bg_color=WHITE)
tb = s5.shapes.add_textbox(Inches(8.1), Inches(2.1), Inches(4.1), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "HOLONIQ 2025 BREAKDOWN"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = CORAL

p = tf.add_paragraph()
p.text = "Subsector & Hub Dynamics"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = DARK_TEAL
p.space_after = Pt(8)

holoniq_bullets = [
    ("50% K-12 Dominance: ", "Acute demand for foundational learning and curriculum-aligned STEM tools."),
    ("33% Workforce & Upskilling: ", "Bootcamps and vocational training bridging the youth employment mismatch."),
    ("Geographic Concentration: ", "Nigeria (34%) and South Africa (28%) anchor the ecosystem; Kenya & Ghana emerging."),
    ("Post-VC Crunch Shift: ", "Transition from growth-at-all-costs to operational sustainability and low-data delivery.")
]
for t, b in holoniq_bullets:
    p = tf.add_paragraph()
    p.space_after = Pt(6)
    p.font.size = Pt(10.5)
    r1 = p.add_run()
    r1.text = "• " + t
    r1.font.bold = True
    r1.font.color.rgb = DARK_TEAL
    r2 = p.add_run()
    r2.text = b
    r2.font.color.rgb = MUTED_TEAL

add_notes(s5, """[TIMING: 3:30 - 4:30 | 60 SECONDS]
PRESENTER SCRIPT:
"On the left is the newly released 2025 Africa EdTech 50 Market Map from HolonIQ:
- 50% of top startups focus on K-12 foundational learning, directly reflecting the 87% learning poverty crisis.
- 33% focus on workforce upskilling, driven by severe youth unemployment.
- 62% of ventures are concentrated in just two markets: Nigeria (34%) and South Africa (28%), though Kenya and Ghana are decentralizing the landscape.
- Most importantly, post-2023 funding contractions have forced African startups to pivot toward operational resilience, low-data delivery (WhatsApp, SMS), and institutional B2B stability."
""")

# =========================================================================
# SLIDE 6: EPISTEMOLOGICAL CRITIQUE: INVERTED-U HYPOTHESIS
# =========================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "3. Epistemological Critique",
           "The Inverted-U Hypothesis: Why Transposing OECD Metrics Misleads African Policy",
           "Device saturation causes distraction in high-income contexts, but steep positive gains in resource-scarce schools.")
add_footer(s6, 6)

if os.path.exists("tight_inverted_u.png"):
    s6.shapes.add_picture("tight_inverted_u.png", Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.1))

create_card(s6, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.1), bg_color=WHITE)
tb = s6.shapes.add_textbox(Inches(8.1), Inches(2.1), Inches(4.1), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "THE FOUR SYSTEMIC BIASES"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = CORAL

p = tf.add_paragraph()
p.text = "Flaws in Global Comparative Data"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = DARK_TEAL
p.space_after = Pt(8)

biases_brief = [
    ("1. Transposition Fallacy: ", "Assuming tech adoption tools work identically across all economic settings."),
    ("2. Saturation vs. Scarcity: ", "OECD screen distraction vs. SSA high marginal return on single devices."),
    ("3. MENA Hardware Trap: ", "100% saturation + AI adoption without teacher pedagogy induces distraction."),
    ("4. Survivorship Bias: ", "PISA measures only enrolled 15-year-olds; 30–50% of SSA youth are out of school.")
]
for t, b in biases_brief:
    p = tf.add_paragraph()
    p.space_after = Pt(6)
    p.font.size = Pt(10.5)
    r1 = p.add_run()
    r1.text = "• " + t
    r1.font.bold = True
    r1.font.color.rgb = CORAL
    r2 = p.add_run()
    r2.text = b
    r2.font.color.rgb = MUTED_TEAL

add_notes(s6, """[TIMING: 4:30 - 5:30 | 60 SECONDS]
PRESENTER SCRIPT:
"The main point to notice on this slide is the curve on the left: the Inverted-U Hypothesis.
In high-income OECD economies, screen exposure has surpassed the saturation threshold. More time on devices correlates negatively with PISA test scores due to social media, multitasking, and AI cognitive offloading.
However, Sub-Saharan Africa is on the steep initial slope of that curve. Access to a single solar tablet or digitized library creates transformative learning gains. If an African ministry follows OECD advice to 'limit screen time', it is prescribing digital austerity to classrooms that are starving for basic textbooks!
Furthermore, PISA suffers from severe Survivorship Bias: it samples only enrolled 15-year-olds at grade 7 or above, completely ignoring the 30 to 50% of African youth out of school."
""")

# =========================================================================
# SLIDE 7: ICT TOOLS & METHODS: 3-TIER ARCHITECTURE
# =========================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, "4. ICT Tools & Methods",
           "A 3-Tier Triangulated Architecture Reconciles Macro, Meso, and Micro Evidence",
           "Combining OECD benchmark datasets, a 69-country automated open-API engine, and practitioner field instruments.")
add_footer(s7, 7)

tier_cards = [
    ("Tier 1: Macro Benchmark Engine", "OECD PISA 2025 AI Dashboard",
     "• Analyzes 85 school systems globally.\n• Focus on MENA: UAE, Qatar, Jordan, Morocco, Saudi Arabia.\n• 10 analytical domains: AI drafting vs learning, screen distraction, equity divides.",
     CORAL, "Macro Assessment"),
    ("Tier 2: Meso 6-Pillars Pipeline", "Automated Python Open-API Engine",
     "• Custom pipeline (fetch_6pillars_pipeline.py) querying World Bank, UIS, and ITU APIs.\n• 69 countries (48 SSA, 21 MENA) across 2015–2024.\n• 20+ live indicators structured into UNESCO's 6 Pillars.",
     DARK_TEAL, "Meso Open-API Pipeline"),
    ("Tier 3: Micro Ground Truth", "Alliance of Alliances Field Surveys",
     "• Instruments co-framed with UNESCO Global Education Coalition.\n• Captures lived classroom bottlenecks: rural load-shedding, device fragility, teacher digital anxiety.\n• Validates startup unit economics.",
     MUTED_TEAL, "Micro Ground Truth")
]

for idx, (t_title, t_sub, t_text, color, badge) in enumerate(tier_cards):
    left_pos = Inches(0.8 + idx * 4.0)
    create_card(s7, left_pos, Inches(1.8), Inches(3.73), Inches(5.1), bg_color=WHITE)
    tb = s7.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.0), Inches(3.33), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = badge.upper()
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = t_title
    p2.font.bold = True
    p2.font.size = Pt(13)
    p2.font.color.rgb = DARK_TEAL
    p2.space_before = Pt(4)
    
    p3 = tf.add_paragraph()
    p3.text = t_sub
    p3.font.bold = True
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = CORAL
    p3.space_after = Pt(8)
    
    p4 = tf.add_paragraph()
    p4.text = t_text
    p4.font.size = Pt(10)
    p4.font.color.rgb = MUTED_TEAL

add_notes(s7, """[TIMING: 5:30 - 6:30 | 60 SECONDS]
PRESENTER SCRIPT:
"To bridge the gap between global theory and local realities, we deploy a three-tiered triangulated methodology:
Tier 1 is our Macro Benchmark Engine, evaluating OECD PISA 2025 AI tables across 85 educational systems, focusing on MENA.
Tier 2 is our Meso 6-Pillars Open Data Pipeline. We engineered an automated, disk-cached Python pipeline querying the World Bank, UNESCO UIS, and ITU across 69 nations (48 SSA and 21 MENA).
Tier 3 is our Micro Ground-Truth Layer, incorporating UNESCO Global Education Coalition / Alliance of Alliances teacher and startup survey instruments. 
This ensures our policy recommendations are never based on macro assumptions alone, but validated by real teachers and founders."
""")

# =========================================================================
# SLIDE 8: MACRO EXPLORER DASHBOARD (EEA_2)
# =========================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_header(s8, "4. Macro Explorer in Action",
           "The Live PISA 2025 AI & Device Observatory (`EEA_2`)",
           "Public client-side observatory (https://rsnl42.github.io/EEA_2/) exploring 85 school systems across 10 analytical domains.")
add_footer(s8, 8)

if os.path.exists("tight_dashboard_mockup.png"):
    s8.shapes.add_picture("tight_dashboard_mockup.png", Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.1))

create_card(s8, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.1), bg_color=WHITE)
tb = s8.shapes.add_textbox(Inches(8.1), Inches(2.1), Inches(4.1), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "CORE DASHBOARD MODULES"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = CORAL

p = tf.add_paragraph()
p.text = "Key PISA 2025 Findings"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = DARK_TEAL
p.space_after = Pt(8)

dash_findings = [
    ("AI Drafting vs. Learning: ", "Students frequently use generative AI to draft text (homework offloading) rather than for deeper concept learning."),
    ("The School Guidance Deficit: ", "Across Gulf systems, student AI adoption outpaces school guidelines by over 35 percentage points."),
    ("Capacity Bottlenecks: ", "Richer schools report higher teacher digital readiness, but device counts alone show no correlation with pedagogical quality."),
    ("Zero Server Overhead: ", "Hosted purely on GitHub Pages; static, lightweight, and accessible to low-bandwidth researchers.")
]
for t, b in dash_findings:
    p = tf.add_paragraph()
    p.space_after = Pt(6)
    p.font.size = Pt(10)
    r1 = p.add_run()
    r1.text = "• " + t
    r1.font.bold = True
    r1.font.color.rgb = DARK_TEAL
    r2 = p.add_run()
    r2.text = b
    r2.font.color.rgb = MUTED_TEAL

add_notes(s8, """[TIMING: 6:30 - 7:30 | 60 SECONDS]
PRESENTER SCRIPT:
"On the left is a direct view of our live web explorer, EEA_2, accessible at https://rsnl42.github.io/EEA_2/. Built purely with client-side architecture on GitHub Pages, it requires no backend server, no login, and runs seamlessly in low-bandwidth environments.
Notice the four primary research modules:
1. AI Portfolios: Revealing that students in MENA use AI primarily to draft assignments—an offloading mechanism—rather than to learn concepts.
2. Use Guidance: Quantifying the dangerous 35-percentage-point guidance lag in schools.
3. Capacity Bottlenecks: Breaking down why raw device counts do not correlate with pedagogical success.
4. Time-Use: Mapping student leisure distraction tails exceeding 5 to 7 hours per day."
""")

# =========================================================================
# SLIDE 9: TANGIBLE ARTEFACT OUTPUT: KENYA COUNTRY SCORECARD
# =========================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9)
add_header(s9, "5. Tangible Artefact Output",
           "Country Diagnostic Scorecard: Kenya 6-Pillars Modality Alignment",
           "Sample country deliverable showing how empirical pipeline metrics translate directly into actionable policy decisions.")
add_footer(s9, 9)

# Insert the tight Kenya Scorecard image
if os.path.exists("tight_artefact_output_kenya.png"):
    s9.shapes.add_picture("tight_artefact_output_kenya.png", Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.1))

create_card(s9, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.1), bg_color=WHITE)
tb = s9.shapes.add_textbox(Inches(8.1), Inches(2.1), Inches(4.1), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "ARTEFACT VALUE PATHS"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = CORAL

p = tf.add_paragraph()
p.text = "How Stakeholders Use It"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = DARK_TEAL
p.space_after = Pt(8)

artefact_bullets = [
    ("Ministries of Education: ", "Prevents capital misallocation (e.g. Kenya: 67% rural power & 3% broadband -> buy offline servers, NOT cloud SaaS)."),
    ("Multilateral Donors: ", "Pinpoints exact rate-limiting bottlenecks (e.g. high teacher certification but missing digital pedagogy)."),
    ("EdTech Innovators: ", "Guides product design to verified classroom constraints (SMS micro-learning, zero-rated WhatsApp, offline caching)."),
    ("Component B Delivered: ", "Replicable across all 69 countries using our open Python pipeline engine.")
]
for t, b in artefact_bullets:
    p = tf.add_paragraph()
    p.space_after = Pt(6)
    p.font.size = Pt(10)
    r1 = p.add_run()
    r1.text = "• " + t
    r1.font.bold = True
    r1.font.color.rgb = DARK_TEAL
    r2 = p.add_run()
    r2.text = b
    r2.font.color.rgb = MUTED_TEAL

add_notes(s9, """[TIMING: 7:30 - 8:30 | 60 SECONDS]
PRESENTER SCRIPT:
"Here is a concrete sample of what our project deliverable produces: a 6-Pillars Diagnostic Scorecard and Modality Alignment Rubric for Kenya.
On the left, you see the actual output from our Python engine:
- In Pillar 2, Kenya has 67% rural electricity and 126% mobile penetration, but only 3% fixed broadband.
- In Pillar 3, government commitment is high with 28% of the budget allocated to education.
- In Pillar 4, 100% of primary teachers are formally certified, but lack digital pedagogical training.
Our alignment matrix translates these numbers into a clear policy verdict: Kenya must NOT procure cloud SaaS platforms. Instead, capital should be directed to solar-powered offline servers and SMS micro-learning channels."
""")

# =========================================================================
# SLIDE 10: FEASIBILITY, CONSTRAINTS & AI REFLEXIVITY
# =========================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)
add_header(s10, "6. Feasibility & Reflexive Learning",
           "Navigating Technical Boundaries, Data Lag, and Ethical Reflexivity",
           "Critical reflection on project execution, data asymmetries, and researcher positionality.")
add_footer(s10, 10)

feas_cards = [
    ("Demonstrated Feasibility", "What Is Built and Verified",
     "• Complete 69-country panel generated and cached.\n• EEA_2 web application live on GitHub Pages.\n• Conceptual and epistemological critique finalized.\n• Executable by an individual researcher-developer.",
     DARK_TEAL),
    ("Technical & Data Limits", "Operational Bottlenecks",
     "• Official UN/UIS data carries a 1- to 3-year publication lag.\n• Rural teacher ICT metrics remain sparse.\n• Client-side static architecture prevents complex real-time regression modeling on the web.",
     CORAL),
    ("Reflexive & Ethical Learning", "Principles for Digital Development",
     "• Data Sovereignty: Preventing digital extractivism by keeping all tools open-access.\n• AI Ethics: Strict compliance with UniTO Guidelines §26 (AI used exclusively for syntax/debugging).\n• Avoiding deficit stigmatization of low-infrastructure systems.",
     MUTED_TEAL)
]

for idx, (title, sub_title, text, color) in enumerate(feas_cards):
    left_pos = Inches(0.8 + idx * 4.0)
    create_card(s10, left_pos, Inches(1.8), Inches(3.73), Inches(5.1), bg_color=WHITE)
    tb = s10.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.0), Inches(3.33), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title.upper()
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = sub_title
    p2.font.bold = True
    p2.font.size = Pt(12.5)
    p2.font.color.rgb = DARK_TEAL
    p2.space_before = Pt(3)
    p2.space_after = Pt(8)
    
    p3 = tf.add_paragraph()
    p3.text = text
    p3.font.size = Pt(10)
    p3.font.color.rgb = MUTED_TEAL

add_notes(s10, """[TIMING: 8:30 - 9:15 | 45 SECONDS]
PRESENTER SCRIPT:
"Following Slide 4 of the Project Clinic, feasibility and self-awareness are critical:
Feasibility is fully demonstrated: our data pipeline is written, all 69 country profiles are generated, and the interactive web application is live.
In terms of constraints, we acknowledge that international databases carry a 1- to 3-year publication delay, and rural pedagogical indicators have significant missing data. We mitigated this by caching indicators locally and cross-referencing with project-level multilateral data.
Ethically, we strictly uphold the Principles for Digital Development. All outputs are open-access to counteract 'digital extractivism'. Furthermore, in full compliance with UniTO Final Project Guidelines Section 26, generative AI was utilized strictly for syntax debugging; all conceptual interpretations represent my own scholarly work."
""")

# =========================================================================
# SLIDE 11: NEXT STEPS & TARGETED CLINIC QUESTIONS
# =========================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11)
add_header(s11, "7. Next Steps & Feedback Request",
           "Roadmap Toward Graduation and Targeted Questions for the Commission",
           "Structured delivery schedule leading to the December 10–11 Master Defense and specific clinic feedback areas.")
add_footer(s11, 11)

# Left Column: Milestones
create_card(s11, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1), bg_color=WHITE)
tb = s11.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "DELIVERY MILESTONES"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = CORAL

p = tf.add_paragraph()
p.text = "Roadmap to Graduation"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = DARK_TEAL
p.space_after = Pt(8)

timeline_brief = [
    ("13 Nov 2026: ", "Submission of First Full Master Thesis Draft to Reviewer."),
    ("20 Nov 2026: ", "Receipt of Reviewer feedback and revision cycle."),
    ("25 Nov 2026: ", "Field Ground-Truthing with Dakar EdTech Hub & AoA contacts."),
    ("30 Nov 2026 (23:59 CET): ", "Final submission of Project and repositories."),
    ("10–11 Dec 2026: ", "Official Master Thesis Defense and Public Presentation.")
]
for t, b in timeline_brief:
    p = tf.add_paragraph()
    p.space_after = Pt(6)
    p.font.size = Pt(10.5)
    r1 = p.add_run()
    r1.text = "• " + t
    r1.font.bold = True
    r1.font.color.rgb = CORAL
    r2 = p.add_run()
    r2.text = b
    r2.font.color.rgb = MUTED_TEAL

# Right Column: Targeted Clinic Questions
create_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), bg_color=PALE_SAGE, border_color=CORAL)
tb = s11.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "CLINIC FEEDBACK REQUEST"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = DARK_TEAL

p = tf.add_paragraph()
p.text = "Targeted Questions for Reviewers"
p.font.bold = True
p.font.size = Pt(13)
p.font.color.rgb = DARK_TEAL
p.space_after = Pt(8)

clinic_questions = [
    ("1. Composite Pillar Weighting: ", "Should foundational infrastructure (Pillar 2) and teacher capacity (Pillar 4) carry heavier weighting coefficients when computing aggregate national digital readiness scores?"),
    ("2. Triangulating Qualitative Survey Data: ", "What is the most effective visualization method to juxtapose qualitative AoA teacher quotes alongside macro World Bank indicators in the final document?"),
    ("3. Framing the MENA-SSA Contrast: ", "How can we best frame MENA findings as a constructive cautionary case without oversimplifying internal variations across the Arab region?")
]
for t, b in clinic_questions:
    p = tf.add_paragraph()
    p.space_after = Pt(8)
    p.font.size = Pt(10.5)
    r1 = p.add_run()
    r1.text = t
    r1.font.bold = True
    r1.font.color.rgb = DARK_TEAL
    r2 = p.add_run()
    r2.text = b
    r2.font.color.rgb = MUTED_TEAL

add_notes(s11, """[TIMING: 9:15 - 10:00 | 45 SECONDS]
PRESENTER SCRIPT:
"To conclude, our timeline is firmly on schedule toward our December graduation defense. 
To help strengthen our final submission on November 30th, I would particularly welcome Professor Bignante and the Commission's guidance on three specific questions:
1. First, on composite weighting across UNESCO's Six Pillars;
2. Second, on the optimal visual synthesis between macro API data and qualitative teacher survey quotes; and
3. Third, on refining our comparative framing of MENA as a diagnostic cautionary model for Sub-Saharan planners.
Thank you very much for your time and guidance. I look forward to your feedback and opening the floor to discussion."
""")

# =========================================================================
# BACKUP SLIDE 12: METHODOLOGICAL BIASES MATRIX (BACKUP A)
# =========================================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12)
add_header(s12, "Backup Slide A — Epistemological Framework",
           "Detailed Analysis: The Four Biases in International Educational Metrics",
           "Deconstructing the systemic flaws of applying high-income benchmarks to Global South environments.")
add_footer(s12, 12)

table_shape = s12.shapes.add_table(5, 4, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.1))
table = table_shape.table
table.columns[0].width = Inches(2.2)
table.columns[1].width = Inches(3.1)
table.columns[2].width = Inches(3.2)
table.columns[3].width = Inches(3.233)

headers = ["Systemic Bias", "Underlying Fallacy / Metric Assumption", "Global South Ground Reality", "Policy Failure Risk"]
for col_idx, h in enumerate(headers):
    cell = table.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = DARK_TEAL
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = FONT_BODY
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = WHITE

matrix_data = [
    ("1. Transposition Fallacy",
     "Adoption and utility of digital tools are invariant to socio-economic infrastructure.",
     "Tools designed for 100Mbps cloud ecosystems fail in off-grid classrooms with intermittent 2G/3G.",
     "Procuring cloud-only LMS and proprietary SaaS that become unusable shelfware."),
    ("2. Saturation vs. Scarcity",
     "Linear negative correlation between student screen time and cognitive test scores.",
     "High-income OECD has reached saturation; rural SSA is at zero. A single device yields steep positive gains.",
     "Prescribing 'screen-time austerity' in environments starved of basic educational textbooks and media."),
    ("3. MENA Hardware Trap",
     "Procuring devices and high-speed internet will automatically uplift learning outcomes.",
     "Near 100% device penetration and high AI usage with severe teacher pedagogical guidance deficits.",
     "High device use induces leisure distraction, homework offloading, and stagnant academic achievement."),
    ("4. PISA Survivorship Bias",
     "Sampling 15-year-olds in formal schooling (grade 7+) reflects national adolescent readiness.",
     "30% to 50% of secondary-school-age adolescents in SSA are out of school (UNESCO UIS).",
     "Directing national budgets exclusively to elite urban schools while the most vulnerable remain invisible.")
]

for row_idx, row in enumerate(matrix_data, start=1):
    for col_idx, text in enumerate(row):
        cell = table.cell(row_idx, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 1 else PALE_SAGE
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_TEAL if col_idx == 0 else MUTED_TEAL
        if col_idx == 0:
            p.font.bold = True

add_notes(s12, """[BACKUP SLIDE A: EPISTEMOLOGICAL MATRIX]
KEY REBUTTAL POINTS:
- Inverted-U hypothesis: The negative correlation between screens and test scores in OECD studies is a product of cognitive saturation and distraction, NOT inherent toxicity. In Africa, digital readers provide steep positive marginal utility.
- MENA empirical evidence confirms that capital expenditure (CapEx) without teacher capacity expenditure (OpEx) is doomed.
- PISA measures only the enrolled secondary elite, rendering the 30–50% of out-of-school youth invisible.
""")

# =========================================================================
# BACKUP SLIDE 13: TECHNICAL PIPELINE ARCHITECTURE (BACKUP B)
# =========================================================================
s13 = prs.slides.add_slide(blank_layout)
set_slide_background(s13)
add_header(s13, "Backup Slide B — Technical Pipeline & Architecture",
           "Data Engineering: Automated Open-API Ingestion and Client-Side Delivery",
           "How the Python pipeline and GitHub Pages dashboard achieve high reproducibility and resilience.")
add_footer(s13, 13)

pipe_cards = [
    ("Data Ingestion & APIs", "Multi-Source API Queries",
     "• World Bank Indicators API: GDP, rural/urban electricity, primary/secondary completion, SPI statistical index.\n• UNESCO Institute for Statistics (UIS): Pupil-teacher ratios, trained teacher percentages.\n• International Telecommunication Union (ITU): Mobile/fixed broadband subscriptions, internet penetration.\n• World Bank Projects API: 237 active digital education loans totaling billions in investments.",
     DARK_TEAL),
    ("Caching & Resiliency Engine", "fetch_6pillars_pipeline.py",
     "• Disk-Based Caching: Stored under data/raw to survive network drops and rate limits during batch queries.\n• Normalization Engine: Cleans country ISO codes, aligns regional aggregates across 48 SSA and 21 MENA nations.\n• Output Artefacts: Generates indicators_timeseries.csv, latest_country_profiles_6pillars.csv, and pillar_regional_benchmarks.csv.",
     CORAL),
    ("Client-Side Observatory", "EEA_2 Static Web Explorer",
     "• Static GitHub Pages Hosting: Pure HTML5/JavaScript frontend with zero backend server dependency.\n• Embedded Data Model: Loads pre-processed JSON/CSV data asynchronously; instant filtering across 85 countries.\n• Resilient Deployment: Can be cloned, run locally on low-cost hardware, or cached in offline educational servers.",
     MUTED_TEAL)
]

for idx, (title, sub_title, text, color) in enumerate(pipe_cards):
    left_pos = Inches(0.8 + idx * 4.0)
    create_card(s13, left_pos, Inches(1.8), Inches(3.73), Inches(5.1), bg_color=WHITE)
    tb = s13.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.0), Inches(3.33), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title.upper()
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = sub_title
    p2.font.bold = True
    p2.font.size = Pt(12.5)
    p2.font.color.rgb = DARK_TEAL
    p2.space_before = Pt(3)
    p2.space_after = Pt(8)
    
    p3 = tf.add_paragraph()
    p3.text = text
    p3.font.size = Pt(10)
    p3.font.color.rgb = MUTED_TEAL

add_notes(s13, """[BACKUP SLIDE B: TECHNICAL ARCHITECTURE]
KEY REBUTTAL POINTS:
- The entire pipeline is open-source Python, disk-cached under data/raw to handle API rate limiting and connection timeouts.
- The web explorer is static client-side on GitHub Pages, ensuring zero recurring server hosting costs and the ability to run offline on local educational servers.
""")

# =========================================================================
# BACKUP SLIDE 14: EXAMINERS' DEFENSE Q&A STRATEGY (BACKUP C)
# =========================================================================
s14 = prs.slides.add_slide(blank_layout)
set_slide_background(s14)
add_header(s14, "Backup Slide C — Defense Q&A Strategy",
           "Anticipated Examiner Challenges & Structured Academic Rebuttals",
           "Prepared speaking strategies for the online graduation defense in front of the Master's Commission.")
add_footer(s14, 14)

qa_cards = [
    ("Challenge 1: PISA in Africa", "Why use PISA if it is biased against Sub-Saharan Africa?",
     "Rebuttal: 'PISA is utilized not as a normative standard for Africa, but as a critical diagnostic baseline. First, it provides deep empirical data for MENA. Second, it quantitatively demonstrates that hardware saturation and unguided AI adoption do NOT equate to improved learning, establishing an urgent warning against repetitive hardware procurement.'",
     CORAL),
    ("Challenge 2: Triangulation", "How do AoA surveys complement macro World Bank APIs?",
     "Rebuttal: 'World Bank APIs effectively track physical and financial capital—grid electricity, broadband connections, and loan commitments. But UNESCO's Six Pillars mandate evaluating participatory culture, parental attitudes, and teacher pedagogical confidence. These human factors are invisible to macro APIs and require ground-level survey instruments.'",
     DARK_TEAL),
    ("Challenge 3: Policy Actionability", "What makes this deliverable actionable for a ministry?",
     "Rebuttal: 'Rather than generic recommendations, the toolkit provides bottleneck-specific guidance. For instance, if a country has achieved 75% electricity but only 20% connectivity, the rubric advises against costly cloud LMS contracts and guides capital toward solar-powered offline servers and localized Open Educational Resources.'",
     MUTED_TEAL)
]

for idx, (title, sub_title, text, color) in enumerate(qa_cards):
    left_pos = Inches(0.8 + idx * 4.0)
    create_card(s14, left_pos, Inches(1.8), Inches(3.73), Inches(5.1), bg_color=WHITE)
    tb = s14.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.0), Inches(3.33), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title.upper()
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = sub_title
    p2.font.bold = True
    p2.font.size = Pt(12.5)
    p2.font.color.rgb = DARK_TEAL
    p2.space_before = Pt(3)
    p2.space_after = Pt(8)
    
    p3 = tf.add_paragraph()
    p3.text = text
    p3.font.size = Pt(10)
    p3.font.color.rgb = MUTED_TEAL

add_notes(s14, """[BACKUP SLIDE C: DEFENSE Q&A STRATEGY]
USE THIS SLIDE TO GUIDE YOUR LIVE Q&A PERFORMANCE (PER SLIDE 17 IN PROFESSOR'S DECK):
- Remember Slide 17 advice: Listen to the full question, pause, give a direct answer, then provide the brief explanation.
- Use the recommended phrases: 'Based on the work so far...', 'This has not been tested yet; the next step would be...', 'That is a valuable point to consider in the final revision.'
- Distinguish clearly between empirical findings (what the data proves) and theoretical critique (what the frameworks suggest).
""")

# Save the polished deck
output_pptx = "EdTech_Thesis_Presentation_First_Draft.pptx"
prs.save(output_pptx)
print(f"Polished condensed presentation saved to {output_pptx} with {len(prs.slides)} slides!")
