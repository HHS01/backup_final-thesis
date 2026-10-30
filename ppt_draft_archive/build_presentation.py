import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------
# CONSTANTS & PALETTE (Matching how_to_develop_idea_final.pptx)
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
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, eyebrow_text, action_title, subtitle=None):
    # Eyebrow (Category Tracker)
    eb_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.3))
    tf_eb = eb_box.text_frame
    tf_eb.word_wrap = True
    tf_eb.margin_left = tf_eb.margin_top = tf_eb.margin_right = tf_eb.margin_bottom = 0
    p_eb = tf_eb.paragraphs[0]
    p_eb.text = eyebrow_text.upper()
    p_eb.font.name = FONT_BODY
    p_eb.font.size = Pt(11)
    p_eb.font.bold = True
    p_eb.font.color.rgb = CORAL

    # Action Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.75))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = action_title
    p_t.font.name = FONT_TITLE
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = DARK_TEAL

    # Subtitle / context note
    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.48), Inches(11.733), Inches(0.35))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(12)
        p_s.font.color.rgb = MUTED_TEAL

def add_footer(slide, current_slide, total_slides=13):
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.733), Inches(0.3))
    tf_f = footer_box.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = f"Master in ICT for Development and Social Good (UniTO / COREP)  |  Final Project Draft  |  Slide {current_slide} of {total_slides}"
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

def add_speaker_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text

# =========================================================================
# SLIDE 1: TITLE & PURPOSE (Cover Slide)
# =========================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1, DARK_TEAL)

# Big title container card
s1_card = create_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=DARK_TEAL, border_color=CORAL)

# Header Eyebrow
s1_tb = s1.shapes.add_textbox(Inches(1.3), Inches(1.2), Inches(10.7), Inches(0.4))
tf1 = s1_tb.text_frame
tf1.word_wrap = True
p = tf1.paragraphs[0]
p.text = "MASTER IN ICT FOR DEVELOPMENT AND SOCIAL GOOD  •  ACADEMIC YEAR 2025–2026"
p.font.name = FONT_BODY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = CORAL

# Main Title
s1_title = s1.shapes.add_textbox(Inches(1.3), Inches(1.65), Inches(10.7), Inches(1.6))
tf_title = s1_title.text_frame
tf_title.word_wrap = True
p = tf_title.paragraphs[0]
p.text = "Mapping the EdTech Landscape in\nSub-Saharan Africa and MENA"
p.font.name = FONT_TITLE
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = WHITE

# Subtitle
s1_sub = s1.shapes.add_textbox(Inches(1.3), Inches(3.3), Inches(10.7), Inches(0.6))
tf_sub = s1_sub.text_frame
tf_sub.word_wrap = True
p = tf_sub.paragraphs[0]
p.text = "Bridging Macro-Level Assessment, the UNESCO 6-Pillars Framework, and Grassroots Realities"
p.font.name = FONT_BODY
p.font.size = Pt(16)
p.font.color.rgb = PALE_SAGE

# Horizontal line accent
line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.3), Inches(4.0), Inches(10.7), Inches(0.04))
line.fill.solid()
line.fill.fore_color.rgb = CORAL
line.line.fill.background()

# Key Purpose Card inside Slide 1
purp_box = s1.shapes.add_textbox(Inches(1.3), Inches(4.2), Inches(10.7), Inches(1.0))
tf_purp = purp_box.text_frame
tf_purp.word_wrap = True
p1 = tf_purp.paragraphs[0]
p1.text = "PROJECT CLINIC PURPOSE (30s Pitch):"
p1.font.bold = True
p1.font.size = Pt(11)
p1.font.color.rgb = CORAL
p2 = tf_purp.add_paragraph()
p2.text = "This research develops an evidence-based analytical framework and an open-access decision observatory to prevent the misallocation of educational technology capital in the Global South. By synthesizing OECD PISA metrics, a 69-country open-data engine, and UNESCO Global Education Coalition field surveys, it reconciles macro benchmarks with resource-constrained classroom realities."
p2.font.size = Pt(12)
p2.font.color.rgb = WHITE

# Candidate & Institutional Affiliations
meta_box = s1.shapes.add_textbox(Inches(1.3), Inches(5.4), Inches(10.7), Inches(0.8))
tf_meta = meta_box.text_frame
tf_meta.word_wrap = True
p = tf_meta.paragraphs[0]
p.text = "Candidate: Master Degree Candidate  |  Academic Reviewer: Prof. Elisa Bignante  |  UniTO · COREP · Impactskills"
p.font.size = Pt(11)
p.font.color.rgb = PALE_SAGE

add_speaker_notes(s1, """[TIMING: 0:00 - 0:30 | 30 SECONDS]
TALKING SCRIPT:
"Good morning, Professor Bignante and fellow Master colleagues. 

My final Master project is titled 'Mapping the EdTech Landscape in Sub-Saharan Africa and MENA: Bridging Macro-Level Assessment, the 6-Pillars Framework, and Grassroots Realities.'

The core purpose of this project is to address a critical flaw in global educational development: the tendency to transpose monolithic, high-income technology benchmarks onto low-resource environments. Over the next 10 minutes, I will walk you through our problem diagnosis, theoretical framing, the 3-tier triangulated methodology, our empirical findings, and our open-access decision toolkit."

TRANSITION:
"Let us begin with the specific problem and context that sparked this inquiry."
""")


# =========================================================================
# SLIDE 2: CONTEXT, ISSUE & PROBLEM IDENTIFICATION
# =========================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "1. Context & Problem Identification", 
           "Global Narratives Treat EdTech as a Monolithic Panacea, Concealing Deep Structural Divides",
           "Comparing two distinct developing regions reveals divergent systemic bottlenecks that defeat one-size-fits-all policy.")
add_footer(s2, 2)

# Left Column: The MENA Paradox
c1 = create_card(s2, Inches(0.8), Inches(1.9), Inches(5.7), Inches(3.6), bg_color=WHITE)
tb1 = s2.shapes.add_textbox(Inches(1.0), Inches(2.05), Inches(5.3), Inches(3.3))
tf1 = tb1.text_frame
tf1.word_wrap = True
p = tf1.paragraphs[0]
p.text = "The MENA Paradox: Device Saturation Without Pedagogy"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = DARK_TEAL

bullets_mena = [
    ("High Hardware Penetration: ", "Gulf and upper-middle MENA economies enjoy near 100% electrical grid stability and universal 1:1 school screen access."),
    ("Surging AI Adoption: ", "OECD PISA 2025 data shows rapid student offloading to generative AI tools for drafting and homework."),
    ("The Guidance Deficit: ", "35%+ gap in teacher pedagogical guidelines; high screen exposure correlates with classroom distraction and stagnant test scores."),
    ("The Warning Lesson: ", "Procuring hardware without teacher training induces leisure displacement rather than educational transformation.")
]
for title, text in bullets_mena:
    p = tf1.add_paragraph()
    p.font.size = Pt(11)
    p.space_after = Pt(4)
    r1 = p.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.color.rgb = CORAL
    r2 = p.add_run()
    r2.text = text
    r2.font.color.rgb = MUTED_TEAL

# Right Column: Sub-Saharan Africa Realities
c2 = create_card(s2, Inches(6.8), Inches(1.9), Inches(5.7), Inches(3.6), bg_color=WHITE)
tb2 = s2.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.3), Inches(3.3))
tf2 = tb2.text_frame
tf2.word_wrap = True
p = tf2.paragraphs[0]
p.text = "Sub-Saharan Africa: Foundational Deficits & Grassroots Dynamism"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = DARK_TEAL

bullets_ssa = [
    ("Acute Grid & Connectivity Gaps: ", "Rural electrification remains at 42.0% (min 0.7%); fixed broadband penetration is just 2.48% (median 0.56%)."),
    ("High Student Exclusion: ", "30% to 50% of secondary-school-age adolescents are entirely out of formal school—rendering PISA metrics blind to the most vulnerable."),
    ("Grassroots Resilience: ", "Thriving local innovation around low-bandwidth, SMS-based, solar-powered offline servers, and mobile-money micro-learning."),
    ("The Core Bottleneck: ", "Capital misallocation: donor millions poured into cloud-first SaaS models that fail in off-grid classrooms.")
]
for title, text in bullets_ssa:
    p = tf2.add_paragraph()
    p.font.size = Pt(11)
    p.space_after = Pt(4)
    r1 = p.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.color.rgb = DARK_TEAL
    r2 = p.add_run()
    r2.text = text
    r2.font.color.rgb = MUTED_TEAL

# Bottom Problem Statement Banner
bot_card = create_card(s2, Inches(0.8), Inches(5.65), Inches(11.7), Inches(1.25), bg_color=PALE_SAGE, border_color=None)
bot_tb = s2.shapes.add_textbox(Inches(1.0), Inches(5.72), Inches(11.3), Inches(1.1))
tf_bot = bot_tb.text_frame
tf_bot.word_wrap = True
p = tf_bot.paragraphs[0]
p.text = "CORE RESEARCH PROBLEM:"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = CORAL
p_q = tf_bot.add_paragraph()
p_q.text = "International benchmarking frameworks evaluate both regions through a monolithic high-income lens. How can we rigorously map real EdTech readiness across SSA and MENA, expose international assessment biases, and build a decision-support architecture for human-centered ICT4D investment?"
p_q.font.size = Pt(12)
p_q.font.bold = True
p_q.font.color.rgb = DARK_TEAL

add_speaker_notes(s2, """[TIMING: 0:30 - 1:30 | 1 MINUTE]
GUIDANCE & FOCUS:
"The main point to notice here is the profound contrast between these two adjacent regions."

TALKING SCRIPT:
"Global narratives routinely champion educational technology as a borderless leapfrog mechanism. However, an empirical examination reveals two entirely contradictory realities:

On the left, we observe what we term the 'MENA Paradox'. In Gulf and middle-income MENA systems, device access is virtually 100%, and student AI usage is among the highest in the OECD. Yet, schools face acute teacher guidance deficits exceeding 35 percentage points. Technology is abundant, but without pedagogical integration, it induces distraction and cognitive offloading.

On the right, Sub-Saharan Africa faces acute foundational infrastructure deficits: rural electrification averages only 42%, and 30 to 50% of secondary youth are out of school. Yet, grassroots innovators—like those documented in the Dakar EdTech Hub—are creating brilliant offline-first, SMS, and solar solutions.

The fundamental problem is that international policy metrics treat both regions as if they were Silicon Valley or Western Europe, prescribing cloud platforms to schools with no electricity."

TRANSITION:
"This brings us directly to our main research objectives and intended social impact."
""")


# =========================================================================
# SLIDE 3: MAIN OBJECTIVES & SOCIAL IMPACT
# =========================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "2. Main Objective & Social Good Impact",
           "Demystifying EdTech Investments to Guide Context-Specific, Equitable Capital Allocation",
           "Three aligned research aims directly advancing Sustainable Development Goals (SDG 4, 8, 10, 16).")
add_footer(s3, 3)

obj_cards = [
    ("Diagnostic Objective", "Evaluate Multi-Pillar Readiness Across 69 Countries",
     "Construct a comprehensive, open-access indicators pipeline synthesizing UNESCO's Six Pillars (infrastructure, funding, teacher capacity, governance) across all 48 Sub-Saharan and 21 MENA nations.",
     "SDG 4.A & 16.6: Transparent institutional benchmarking", CORAL),
    ("Epistemological Objective", "Formally Critique Assessment Transposition Biases",
     "Demonstrate mathematically and theoretically why standardized global metrics (OECD PISA) produce distorted policy prescriptions when transposed uncritically to resource-constrained environments.",
     "SDG 10.2: Counteracting digital extractivism and data bias", DARK_TEAL),
    ("Actionable Deliverable", "Deliver an Open Decision-Support Observatory & Rubric",
     "Equip educational ministries, multilateral donors (UNDP timbuktoo, World Bank), and local innovators (Dakar EdTech Hub) with an interactive dashboard and alignment rubric to prevent wasteful procurement.",
     "SDG 4.4 & 8.3: Directing investment to resilient local solutions", MUTED_TEAL)
]

for idx, (badge, title, desc, sdg, color) in enumerate(obj_cards):
    left_pos = Inches(0.8 + idx * 4.0)
    card = create_card(s3, left_pos, Inches(1.9), Inches(3.73), Inches(4.9), bg_color=WHITE)
    
    tb = s3.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.1), Inches(3.33), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = badge.upper()
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = title
    p2.font.bold = True
    p2.font.size = Pt(14)
    p2.font.color.rgb = DARK_TEAL
    p2.space_before = Pt(6)
    p2.space_after = Pt(12)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.size = Pt(11.5)
    p3.font.color.rgb = MUTED_TEAL
    p3.space_after = Pt(16)
    
    # Bottom SDG Badge
    p4 = tf.add_paragraph()
    p4.text = "Social Good Contribution:"
    p4.font.bold = True
    p4.font.size = Pt(10)
    p4.font.color.rgb = CORAL
    
    p5 = tf.add_paragraph()
    p5.text = sdg
    p5.font.size = Pt(10.5)
    p5.font.color.rgb = DARK_TEAL

add_speaker_notes(s3, """[TIMING: 1:30 - 3:00 | 1.5 MINUTES]
GUIDANCE & FOCUS:
"Notice how our objective, methods, and tangible output are tightly coherent, as required by the Master project guidelines."

TALKING SCRIPT:
"What does this Master final project aim to achieve? We have structured our work around three mutually reinforcing objectives:

First, a Diagnostic Objective: to establish an empirical baseline across 69 nations in Sub-Saharan Africa and MENA by tracking 20+ live indicators categorized under UNESCO's Six Pillars of Digital Transformation.

Second, an Epistemological Objective: to provide a rigorous, critical ICT4D critique of international comparative assessments. We prove that using OECD metrics as a universal standard creates a 'transposition fallacy' that actively harms developing educational systems.

Third, an Actionable Deliverable: in fulfillment of Component B, we deliver not just a theoretical thesis, but a live, client-side interactive web explorer and a multi-stakeholder decision matrix.

In terms of social good, this work directly addresses SDG 4 for quality education, SDG 10 for reduced inequalities, and SDG 16 for effective institutions. It prevents public ministries and donors from wasting hundreds of millions on hardware that ends up abandoned in locked cupboards."

TRANSITION:
"To anchor this investigation, let us examine the theoretical foundations that guide our analytical decisions."
""")


# =========================================================================
# SLIDE 4: THEORETICAL FOUNDATION: UNESCO 6 PILLARS & ECOSYSTEM TYPOLOGY
# =========================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "3. Theoretical Foundation",
           "Grounded in UNESCO's Six Pillars for Systemic Digital Transformation",
           "Moving beyond device procurement toward a holistic ecosystem model (DTC 2024 & Dakar EdTech Hub).")
add_footer(s4, 4)

# Left Column: Theory Explanation
c_left = create_card(s4, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9), bg_color=WHITE)
tb_th = s4.shapes.add_textbox(Inches(1.0), Inches(2.05), Inches(5.2), Inches(4.6))
tf_th = tb_th.text_frame
tf_th.word_wrap = True

p = tf_th.paragraphs[0]
p.text = "Holistic Architecture: Interdependent Domains"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = DARK_TEAL

theories = [
    ("UNESCO DTC Six Pillars (2024): ", "Digital transformation succeeds only when infrastructure is balanced by pedagogical capacity, sustainable funding, and ethical data governance."),
    ("Pouye / Dakar EdTech Hub Typologies (2024): ", "Supply-side categorisation across African ecosystems: Foundational K-12 platforms, TVET upskilling, School ERPs, and low-connectivity adaptations (offline/radio/SMS)."),
    ("CapEx vs. OpEx Lifecycle Theory: ", "Hardware procurement (CapEx) accounts for only ~20% of total ownership cost. Without recurrent OpEx maintenance and continuous teacher training, tech investments rapidly depreciate."),
    ("Human-Centered ICT4D Lens: ", "Adheres to the Principles for Digital Development: design with the user, understand the ecosystem, and design for scale from offline foundations.")
]
for title, text in theories:
    p = tf_th.add_paragraph()
    p.font.size = Pt(11)
    p.space_after = Pt(6)
    r1 = p.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.color.rgb = CORAL
    r2 = p.add_run()
    r2.text = text
    r2.font.color.rgb = MUTED_TEAL

# Right Column: Insert Chart 3 (Six Pillars visual)
if os.path.exists("chart_six_pillars.png"):
    s4.shapes.add_picture("chart_six_pillars.png", Inches(6.6), Inches(1.9), Inches(5.9), Inches(4.9))

add_speaker_notes(s4, """[TIMING: 3:00 - 4:30 | 1.5 MINUTES]
GUIDANCE & FOCUS:
"The main point to notice here is that digital transformation cannot be reduced to hardware."

TALKING SCRIPT:
"Our research is anchored in UNESCO's Six Pillars for the Digital Transformation of Education, developed by the Digital Transformation Collaborative in 2024. 

As shown on the right, the framework establishes six interdependent pillars:
1. Coordination and Leadership,
2. Connectivity and Infrastructure,
3. Cost and Sustainability,
4. Capacity and Culture,
5. Content and Solutions, and
6. Data and Evidence.

We synthesize this with Abdou Khadre Pouye’s 2024 strategic mapping of the African EdTech ecosystem from the Dakar EdTech Hub and UNDP timbuktoo. 

The core theoretical lesson from the Master is the CapEx vs. OpEx lifecycle balance: purchasing tablets or smartboards represents less than 20% of the lifecycle cost. If ministries do not budget for electricity, device maintenance, and continuous teacher capacity (Pillar 4), the entire investment collapses. Technology is never self-executing."

TRANSITION:
"Building on this theory, we articulate our core methodological critique of global metrics."
""")


# =========================================================================
# SLIDE 5: CORE METHODOLOGICAL CRITIQUE: THE FOUR BIASES
# =========================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "3. Theoretical Foundation — Epistemological Critique",
           "Standardized Global Metrics Incur a Transposition Fallacy in Resource-Scarce Contexts",
           "The Inverted-U Hypothesis proves that OECD screening correlation cannot be naively transferred to Africa.")
add_footer(s5, 5)

# Left Column: Insert Chart 1 (Inverted-U curve)
if os.path.exists("chart_inverted_u.png"):
    s5.shapes.add_picture("chart_inverted_u.png", Inches(0.8), Inches(1.9), Inches(5.8), Inches(4.9))

# Right Column: Four Biases Summary Card
c_r = create_card(s5, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9), bg_color=WHITE)
tb_b = s5.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.3), Inches(4.6))
tf_b = tb_b.text_frame
tf_b.word_wrap = True

p = tf_b.paragraphs[0]
p.text = "Four Systemic Biases in Global Educational Datasets"
p.font.bold = True
p.font.size = Pt(13.5)
p.font.color.rgb = DARK_TEAL

biases = [
    ("1. Transposition Fallacy: ", "Assuming technology adoption exhibits universal utility across all economic contexts. OECD policy advice cannot be transposed directly to Africa."),
    ("2. Saturation vs. Scarcity Divide: ", "In high-income OECD schools, screens are ubiquitous—leading to distraction and negative correlation. In rural Africa, a single solar device yields steep initial learning gains (Inverted-U curve)."),
    ("3. The MENA Hardware Trap: ", "Our PISA 2025 dashboard proves that 100% device penetration and high AI usage without teacher pedagogical guidance creates leisure displacement, not learning."),
    ("4. PISA Survivorship Bias: ", "PISA samples only enrolled 15-year-olds (grade 7+). In SSA, 30–50% of youth are out of school, rendering the most vulnerable completely invisible to policy.")
]
for title, text in biases:
    p = tf_b.add_paragraph()
    p.font.size = Pt(10.5)
    p.space_after = Pt(4)
    r1 = p.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.color.rgb = CORAL
    r2 = p.add_run()
    r2.text = text
    r2.font.color.rgb = MUTED_TEAL

add_speaker_notes(s5, """[TIMING: 4:30 - 6:00 | 1.5 MINUTES]
GUIDANCE & FOCUS:
"The main point to notice on this slide is the curve on the left—the Inverted-U Hypothesis."

TALKING SCRIPT:
"A primary theoretical contribution of this thesis is the formal articulation of four systemic biases in international comparative assessments.

Look at the Inverted-U curve on the left:
In high-income OECD economies, schools are past the saturation threshold. Extra screen time often correlates negatively with cognitive performance due to multitasking, distraction, and cognitive offloading via AI.

However, Sub-Saharan Africa sits on the steep initial slope of that curve. Access to a single solar-powered tablet, a digital radio lesson, or an offline server creates massive positive gains. If policymakers naively read OECD reports warning against 'too much screen time', they might prescribe digital austerity to African schools that are actively starving for educational media!

Furthermore, MENA serves as our primary empirical warning: pouring hardware into schools without teacher training produces leisure displacement. Finally, PISA only measures enrolled 15-year-olds, completely ignoring the 30 to 50% of African youth outside the formal secondary system."

TRANSITION:
"To overcome these structural biases, how do we gather and triangulate our data?"
""")


# =========================================================================
# SLIDE 6: ICT TOOLS & METHODS: 3-TIER TRIANGULATED ARCHITECTURE
# =========================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "4. ICT Tools & Methods",
           "A 3-Tier Triangulated Architecture Combines Macro, Meso, and Micro Evidence",
           "Synthesizing OECD assessments, open development APIs, and Global Education Coalition ground truth.")
add_footer(s6, 6)

tiers = [
    ("Tier 1: Macro Benchmark Engine", "OECD PISA 2025 Dashboard (EEA_2)",
     "• Analyzes 85 educational systems globally with focus on MENA (Jordan, Morocco, Qatar, UAE, Saudi Arabia).\n• Explores 10 analytical domains: AI tool adoption for drafting vs learning, screen distraction, equity divides, and institutional guidance rules.\n• Static client-side web application deployed on GitHub Pages.",
     CORAL, "Macro Assessment Layer"),
    ("Tier 2: Meso 6-Pillars Open Data", "Automated Python Pipeline across 69 Nations",
     "• Custom engine (fetch_6pillars_pipeline.py) querying World Bank, UIS, and ITU APIs.\n• Complete coverage of 48 Sub-Saharan and 21 MENA countries spanning 2015–2024.\n• Tracks 20+ live indicators categorized across UNESCO's 6 Pillars with disk-based caching and rate-limiting resilience.",
     DARK_TEAL, "Meso Open-API Pipeline"),
    ("Tier 3: Micro Ground-Truth Layer", "Alliance of Alliances (AoA) Survey Instruments",
     "• Co-designed with UNESCO Global Education Coalition.\n• Captures empirical classroom reality: rural grid failure, language barriers, mobile data costs.\n• Validates startup business models (freemium vs B2G procurement) and teacher pedagogical support needs.",
     MUTED_TEAL, "Micro Ground-Truth Layer")
]

for idx, (tier_title, sub_title, text, color, badge) in enumerate(tiers):
    left_pos = Inches(0.8 + idx * 4.0)
    card = create_card(s6, left_pos, Inches(1.9), Inches(3.73), Inches(4.9), bg_color=WHITE)
    
    tb = s6.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.1), Inches(3.33), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = badge.upper()
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = tier_title
    p2.font.bold = True
    p2.font.size = Pt(13.5)
    p2.font.color.rgb = DARK_TEAL
    p2.space_before = Pt(4)
    p2.space_after = Pt(4)
    
    p3 = tf.add_paragraph()
    p3.text = sub_title
    p3.font.bold = True
    p3.font.size = Pt(11)
    p3.font.color.rgb = CORAL
    p3.space_after = Pt(10)
    
    p4 = tf.add_paragraph()
    p4.text = text
    p4.font.size = Pt(10.5)
    p4.font.color.rgb = MUTED_TEAL

add_speaker_notes(s6, """[TIMING: 6:00 - 7:30 | 1.5 MINUTES]
GUIDANCE & FOCUS:
"Notice how each tier addresses the blind spots of the others—this is true triangulation."

TALKING SCRIPT:
"To overcome the biases of single-source studies, our methodology deploys a three-tiered triangulated architecture:

Tier 1 is our Macro Benchmark Engine. We examine OECD PISA 2025 data across 85 systems, deploying our interactive web explorer (`EEA_2`) to analyze AI use, screen exposure, and school guidelines across MENA and global benchmarks.

Tier 2 is our Meso Open-Data Pipeline. We developed a robust, reproducible Python engine (`fetch_6pillars_pipeline.py`) that queries open APIs from the World Bank, UNESCO UIS, and ITU across 69 countries—48 in Sub-Saharan Africa and 21 in MENA—generating time-series datasets structured around the 6 Pillars.

Tier 3 is our Micro Ground-Truth Layer. We incorporate the survey instruments from the Alliance of Alliances under UNESCO's Global Education Coalition. This captures the lived experience of teachers and EdTech founders—factors like load-shedding, battery degradation, and multi-lingual classrooms that no macro database can see."

TRANSITION:
"What empirical insights emerge when we run this pipeline?"
""")


# =========================================================================
# SLIDE 7: EMPIRICAL INSIGHTS & CROSS-REGIONAL CONTRASTS
# =========================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, "4. Empirical Findings",
           "Data Confirms Divergent Bottlenecks: SSA Faces Grid Scarcity, MENA Faces Pedagogical Deficits",
           "Empirical panel across 69 nations highlights where infrastructure spending dangerously outpaces teacher training.")
add_footer(s7, 7)

# Left Column: Insert Chart 2 (Regional Benchmarks)
if os.path.exists("chart_regional_benchmarks.png"):
    s7.shapes.add_picture("chart_regional_benchmarks.png", Inches(0.8), Inches(1.9), Inches(5.8), Inches(4.9))

# Right Column: Empirical Takeaways Card
c_f = create_card(s7, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9), bg_color=WHITE)
tb_f = s7.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.3), Inches(4.6))
tf_f = tb_f.text_frame
tf_f.word_wrap = True

p = tf_f.paragraphs[0]
p.text = "Key Cross-Regional Empirical Insights"
p.font.bold = True
p.font.size = Pt(13.5)
p.font.color.rgb = DARK_TEAL

findings = [
    ("Pillar 2 (Connectivity & Power): ", "SSA rural electrification averages only 42.0% (and as low as 0.7%), with fixed broadband at 2.48%. Cloud-only platforms are structurally inviable outside capital cities."),
    ("Pillar 3 (Cost & Financing Reality): ", "Analysis of 237 active World Bank digital education projects shows massive CapEx inflows ($200M in Mozambique, $200M in Jordan), yet recurrent maintenance (OpEx) is systematically neglected."),
    ("Pillar 4 (Capacity & Pedagogy): ", "Trained teachers in secondary education average 69.3% in SSA vs 87.2% in MENA; pupil-teacher ratios exceed 37:1. Pedagogical training is the universal bottleneck in both regions."),
    ("Pillar 6 (Data Maturity Divide): ", "Statistical Performance Indicators (SPI) reveal strong national variance: MENA leads in administrative data, but SSA shows high community data agility.")
]
for title, text in findings:
    p = tf_f.add_paragraph()
    p.font.size = Pt(10.5)
    p.space_after = Pt(4)
    r1 = p.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.color.rgb = CORAL
    r2 = p.add_run()
    r2.text = text
    r2.font.color.rgb = MUTED_TEAL

add_speaker_notes(s7, """[TIMING: 7:30 - 8:30 | 1 MINUTE]
GUIDANCE & FOCUS:
"The main point to notice on this slide is how the empirical data directly refutes monolithic assumptions."

TALKING SCRIPT:
"Looking at the chart on the left, which extracts real data from our 6-Pillars pipeline:

In Pillar 2, while MENA enjoys 95% rural electrification and 82% internet penetration, Sub-Saharan Africa averages only 42% rural electricity and 2.48% fixed broadband. This proves that any project assuming always-on connectivity will fail in over half of African communities.

In Pillar 3, our pipeline cataloged 237 active World Bank digital learning projects totaling hundreds of millions of dollars. Yet, virtually all funding targets hardware procurement, leaving schools unable to replace broken chargers or renew software licenses after year two.

And in Pillar 4, teacher capacity emerges as the universal limiting factor. Technology succeeds or fails based on teacher readiness. In MENA, unguided technology leads to distraction; in SSA, undertrained teachers are overwhelmed by complex software interfaces."

TRANSITION:
"How do we translate these analytical insights into a tangible product for stakeholders?"
""")


# =========================================================================
# SLIDE 8: TANGIBLE PRODUCT & DELIVERABLE (Component B)
# =========================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_header(s8, "5. Tangible Product & Intended Contribution",
           "An Open-Access Decision Observatory and Multi-Stakeholder Alignment Rubric",
           "Component B delivers actionable, client-side tools directly serving ministries, multilateral donors, and local innovators.")
add_footer(s8, 8)

deliverables = [
    ("Live Interactive Web Explorer", "EEA_2 Dashboard on GitHub Pages",
     "• URL: https://rsnl42.github.io/EEA_2/\n• Interactive client-side dashboard benchmarking AI usage, screen time, and institutional guidance rules across 85 systems.\n• Zero backend requirement: runs in low-bandwidth browser environments without paywalls or login walls.",
     CORAL, "Artefact 1: Web Dashboard"),
    ("Open-Source Data Pipeline", "Reproducible 6-Pillars Engine & CSVs",
     "• Fully documented Python engine: fetch_6pillars_pipeline.py.\n• Structured outputs: indicators_timeseries.csv, latest_country_profiles_6pillars.csv, and wb_digital_education_projects.csv.\n• Equipped with disk-based caching and retry resilience for low-bandwidth researchers.",
     DARK_TEAL, "Artefact 2: Data Pipeline"),
    ("Multi-Stakeholder Alignment Rubric", "Decision-Support Matrix for Capital Allocation",
     "• Practical diagnostic rubric mapping school connectivity constraints to appropriate EdTech modalities.\n• Prevents procurement mismatch (e.g., directing off-grid schools to solar/offline servers rather than cloud LMS).\n• Bridges local startups (Dakar Hub) with ministerial procurement requirements.",
     MUTED_TEAL, "Artefact 3: Policy Matrix")
]

for idx, (deliv_title, sub_title, text, color, badge) in enumerate(deliverables):
    left_pos = Inches(0.8 + idx * 4.0)
    card = create_card(s8, left_pos, Inches(1.9), Inches(3.73), Inches(4.9), bg_color=WHITE)
    
    tb = s8.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.1), Inches(3.33), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = badge.upper()
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = deliv_title
    p2.font.bold = True
    p2.font.size = Pt(13.5)
    p2.font.color.rgb = DARK_TEAL
    p2.space_before = Pt(4)
    p2.space_after = Pt(4)
    
    p3 = tf.add_paragraph()
    p3.text = sub_title
    p3.font.bold = True
    p3.font.size = Pt(11)
    p3.font.color.rgb = CORAL
    p3.space_after = Pt(10)
    
    p4 = tf.add_paragraph()
    p4.text = text
    p4.font.size = Pt(10.5)
    p4.font.color.rgb = MUTED_TEAL

add_speaker_notes(s8, """[TIMING: 8:30 - 9:30 | 1 MINUTE]
GUIDANCE & FOCUS:
"Notice how this fulfills Component B of the Master model—translating scholarship into a tangible practical artefact."

TALKING SCRIPT:
"In fulfillment of Component B of the Master's programme, this project produces three tangible deliverables:

First, our live interactive web explorer, `EEA_2`, accessible at `https://rsnl42.github.io/EEA_2/`. Built entirely with client-side architecture, it allows any ministry official or researcher to explore AI adoption, device policies, and screen distribution with zero login or subscription fees.

Second, our open-source 6-Pillars data pipeline. The entire Python script and cached CSVs are open-source, allowing researchers across the Global South to reproduce our 69-country analysis or add their own national datasets.

Third, our Multi-Stakeholder Alignment Rubric. This decision-support tool acts as a bridge between three worlds:
1. Ministries of Education, preventing misallocation of public funds;
2. Multilateral donors like UNDP timbuktoo, targeting high-impact gaps;
3. Grassroots EdTech startups, helping them design products that fit verified classroom conditions."

TRANSITION:
"Let us now reflect honestly on feasibility, limitations, and ethical considerations."
""")


# =========================================================================
# SLIDE 9: FEASIBILITY, LIMITATIONS & REFLEXIVE LEARNING
# =========================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9)
add_header(s9, "6. Feasibility, Constraints & Learning",
           "Navigating Technical Boundaries, Data Lag, and Ethical Reflexivity",
           "Critical reflection on project execution, methodological trade-offs, and researcher positionality.")
add_footer(s9, 9)

feas_cards = [
    ("Demonstrated Feasibility", "What Has Been Successfully Delivered",
     "• Data pipeline fully operational, fetching and caching 20+ indicators across 69 nations.\n• Client-side dashboard (EEA_2) tested and live on GitHub Pages.\n• Theoretical framework, critical epistemological critique, and rubric completed.\n• Within scope of a single researcher-developer.",
     DARK_TEAL),
    ("Technical & Data Constraints", "Boundaries and Operational Bottlenecks",
     "• Macro Data Lag: World Bank/UIS indicators carry a 1- to 3-year publication delay.\n• Indicator Missingness: Rural metrics and teacher ICT training data sparse in remote areas.\n• Client-Side Limits: Dashboard cannot run heavy server-side regression modeling.\n• API Rate-Limiting: Required disk-based caching architecture.",
     CORAL),
    ("Reflexive & Ethical Learning", "Principles for Digital Development",
     "• Data Sovereignty: Preventing 'digital extractivism' by keeping all tools open-access.\n• AI Ethics: In line with UniTO Guidelines §26, Generative AI used only for code syntax/debugging; all analysis is original scholarship.\n• Avoiding Stigmatization: Low infrastructure must not be equated with low capacity for innovation.",
     MUTED_TEAL)
]

for idx, (title, sub_title, text, color) in enumerate(feas_cards):
    left_pos = Inches(0.8 + idx * 4.0)
    card = create_card(s9, left_pos, Inches(1.9), Inches(3.73), Inches(4.9), bg_color=WHITE)
    
    tb = s9.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.1), Inches(3.33), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title.upper()
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = sub_title
    p2.font.bold = True
    p2.font.size = Pt(13)
    p2.font.color.rgb = DARK_TEAL
    p2.space_before = Pt(4)
    p2.space_after = Pt(10)
    
    p3 = tf.add_paragraph()
    p3.text = text
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = MUTED_TEAL

add_speaker_notes(s9, """[TIMING: 9:30 - 10:30 | 1 MINUTE]
GUIDANCE & FOCUS:
"As emphasized in Slide 4 and Slide 17 of the professor's presentation, a rigorous project must acknowledge constraints and demonstrate self-awareness."

TALKING SCRIPT:
"In Slide 4 of the Project Clinic, Professor Bignante asks: 'What can realistically be completed, and what could be learned if things do not go as planned?'

First, feasibility: our deliverables are already built and verified. The automated pipeline functions reliably across 69 nations, the datasets are generated, and the live dashboard is online.

Second, constraints: we encountered significant data lag in official UIS indicators—often 1 to 3 years behind—and substantial missing data for rural pedagogical metrics. We mitigated this through local disk-caching and cross-referencing with project-level multilateral data.

Third, ethical reflexivity: in developing this ICT4D tool, we adhered strictly to the Principles for Digital Development. We took explicit steps to prevent 'digital extractivism'—ensuring our tools remain free and open. Furthermore, per UniTO Guidelines Section 26, generative AI was utilized strictly for syntax debugging and code optimization; all conceptual interpretations are my own original scholarship."

TRANSITION:
"This brings us to our immediate next steps and questions for the Clinic."
""")


# =========================================================================
# SLIDE 10: NEXT STEPS & FEEDBACK REQUEST (Project Clinic Conclusion)
# =========================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)
add_header(s10, "7. Next Steps & Feedback Request",
           "Immediate Roadmap Toward Graduation and Targeted Questions for the Commission",
           "Structured timeline leading to the December 10–11 Master Defense and specific areas for peer feedback.")
add_footer(s10, 10)

# Left Column: Timeline & Concrete Next Steps
c_tl = create_card(s10, Inches(0.8), Inches(1.9), Inches(5.7), Inches(4.9), bg_color=WHITE)
tb_tl = s10.shapes.add_textbox(Inches(1.0), Inches(2.05), Inches(5.3), Inches(4.6))
tf_tl = tb_tl.text_frame
tf_tl.word_wrap = True

p = tf_tl.paragraphs[0]
p.text = "Milestones & Delivery Timeline"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = DARK_TEAL

timeline = [
    ("13 November 2026: ", "Submission of First Full Master Thesis Draft to Academic Reviewer."),
    ("20 November 2026: ", "Receipt of Reviewer Feedback and initial revision cycle."),
    ("25 November 2026: ", "Stakeholder Ground-Truthing: Review decision rubric with Dakar EdTech Hub & AoA field contacts."),
    ("30 November 2026 (23:59 CET): ", "Final submission of completed Project and supplementary code repositories."),
    ("10–11 December 2026: ", "Official Master Thesis Defense and Public Online Presentation in front of Commission.")
]
for date_str, desc in timeline:
    p = tf_tl.add_paragraph()
    p.font.size = Pt(11)
    p.space_after = Pt(6)
    r1 = p.add_run()
    r1.text = "• " + date_str
    r1.font.bold = True
    r1.font.color.rgb = CORAL
    r2 = p.add_run()
    r2.text = desc
    r2.font.color.rgb = MUTED_TEAL

# Right Column: Targeted Clinic Questions for Feedback
c_fb = create_card(s10, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9), bg_color=PALE_SAGE, border_color=CORAL)
tb_fb = s10.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.3), Inches(4.6))
tf_fb = tb_fb.text_frame
tf_fb.word_wrap = True

p = tf_fb.paragraphs[0]
p.text = "Targeted Questions for Reviewer & Clinic Feedback"
p.font.bold = True
p.font.size = Pt(14)
p.font.color.rgb = DARK_TEAL

questions = [
    ("1. Composite Pillar Weighting: ", "When computing an aggregate national digital readiness score, should pillars be weighted equally, or should foundational infrastructure (Pillar 2) and teacher capacity (Pillar 4) carry heavier priority coefficients?"),
    ("2. Triangulating Qualitative Survey Data: ", "What is the most effective visualization method to juxtapose qualitative AoA teacher pain points alongside quantitative World Bank macro indicators in the final document?"),
    ("3. Framing the MENA-SSA Contrast: ", "How can we best frame the MENA findings so they serve constructively as a diagnostic warning for African ministries without appearing to oversimplify MENA's internal variations?")
]
for q_title, q_text in questions:
    p = tf_fb.add_paragraph()
    p.font.size = Pt(11)
    p.space_after = Pt(8)
    r1 = p.add_run()
    r1.text = q_title
    r1.font.bold = True
    r1.font.color.rgb = DARK_TEAL
    r2 = p.add_run()
    r2.text = q_text
    r2.font.color.rgb = MUTED_TEAL

add_speaker_notes(s10, """[TIMING: 10:30 - 11:30 | 1 MINUTE]
GUIDANCE & FOCUS:
"Conclude cleanly, reaffirm the project's contribution to ICT4D, and open the floor with specific questions as recommended in Slide 17."

TALKING SCRIPT:
"To conclude, our immediate roadmap is firmly set: our first complete draft will be submitted on November 13th, followed by stakeholder validation with our field contacts and final submission on November 30th, ahead of our official graduation defense on December 10th and 11th.

To help strengthen our final submission, I would particularly value the Commission's guidance on three specific questions:
1. First, on composite index weighting across UNESCO's Six Pillars;
2. Second, on the optimal visual synthesis between macro API data and qualitative teacher survey quotes; and
3. Third, on refining our comparative framing of MENA as a diagnostic cautionary tale for Sub-Saharan planners.

Thank you very much for your time and guidance. I look forward to your questions and feedback."
""")


# =========================================================================
# BACKUP SLIDE 11: METHODOLOGICAL BIASES MATRIX (Backup / Q&A)
# =========================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11)
add_header(s11, "Backup Slide A — Epistemological Framework",
           "Detailed Analysis: The Four Biases in International Educational Metrics",
           "Deconstructing the systemic flaws of applying high-income benchmarks to Global South environments.")
add_footer(s11, 11)

# Create a clean table for the 4 biases
table_shape = s11.shapes.add_table(5, 4, Inches(0.8), Inches(1.9), Inches(11.733), Inches(4.9))
table = table_shape.table

# Set column widths
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

add_speaker_notes(s11, """[BACKUP SLIDE A: EPISTEMOLOGICAL MATRIX]
USE THIS SLIDE TO ANSWER:
"Can you elaborate on the theoretical critique of international comparative assessments?"

KEY TALKING POINTS:
- Refer to Row 2: Inverted-U hypothesis. The negative correlation between screens and PISA scores found in OECD studies is a product of cognitive saturation and distraction, NOT inherent toxicity of screens. In Africa, where students lack physical books, digital readers have enormous marginal utility.
- Refer to Row 3: MENA empirical evidence confirms that capital expenditure without teacher capacity expenditure is doomed.
- Refer to Row 4: Explain that PISA cannot be an equity metric for Africa because it measures only the enrolled elite, excluding up to half the youth population.
""")


# =========================================================================
# BACKUP SLIDE 12: TECHNICAL PIPELINE ARCHITECTURE (Backup / Q&A)
# =========================================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12)
add_header(s12, "Backup Slide B — Technical Pipeline & Architecture",
           "Data Engineering: Automated Open-API Ingestion and Client-Side Delivery",
           "How the Python pipeline and GitHub Pages dashboard achieve high reproducibility and resilience.")
add_footer(s12, 12)

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
    card = create_card(s12, left_pos, Inches(1.9), Inches(3.73), Inches(4.9), bg_color=WHITE)
    
    tb = s12.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.1), Inches(3.33), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title.upper()
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = sub_title
    p2.font.bold = True
    p2.font.size = Pt(13)
    p2.font.color.rgb = DARK_TEAL
    p2.space_before = Pt(4)
    p2.space_after = Pt(10)
    
    p3 = tf.add_paragraph()
    p3.text = text
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = MUTED_TEAL

add_speaker_notes(s12, """[BACKUP SLIDE B: TECHNICAL ARCHITECTURE]
USE THIS SLIDE TO ANSWER:
"How was the data extracted and cleaned? What ensures technical reproducibility?"

KEY TALKING POINTS:
- Emphasize that the entire pipeline is automated in Python and fully reproducible.
- Explain the rate-limiting and caching architecture: World Bank and UIS endpoints frequently drop or throttle during large batch requests; local caching ensures tests run without repeated API calls.
- Highlight the zero-cost, static hosting decision for `EEA_2`: by hosting on GitHub Pages with client-side JSON parsing, the tool requires zero recurring server maintenance and can even be run offline on a local school server.
""")


# =========================================================================
# BACKUP SLIDE 13: EXAMINERS' DEFENSE Q&A STRATEGY (Backup / Q&A)
# =========================================================================
s13 = prs.slides.add_slide(blank_layout)
set_slide_background(s13)
add_header(s13, "Backup Slide C — Defense Q&A Strategy",
           "Anticipated Examiner Challenges & Structured Academic Rebuttals",
           "Prepared speaking strategies for the online graduation defense in front of the Master's Commission.")
add_footer(s13, 13)

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
    card = create_card(s13, left_pos, Inches(1.9), Inches(3.73), Inches(4.9), bg_color=WHITE)
    
    tb = s13.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.1), Inches(3.33), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title.upper()
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = sub_title
    p2.font.bold = True
    p2.font.size = Pt(13)
    p2.font.color.rgb = DARK_TEAL
    p2.space_before = Pt(4)
    p2.space_after = Pt(10)
    
    p3 = tf.add_paragraph()
    p3.text = text
    p3.font.size = Pt(10)
    p3.font.color.rgb = MUTED_TEAL

add_speaker_notes(s13, """[BACKUP SLIDE C: DEFENSE Q&A STRATEGY]
USE THIS SLIDE TO GUIDE YOUR LIVE Q&A PERFORMANCE (PER SLIDE 17 IN PROFESSOR'S DECK):
- Remember Slide 17 advice: Listen to the full question, pause, give a direct answer, then provide the brief explanation.
- Use the recommended phrases: 'Based on the work so far...', 'This has not been tested yet; the next step would be...', 'That is a valuable point to consider in the final revision.'
- Distinguish clearly between empirical findings (what the data proves) and theoretical critique (what the frameworks suggest).
""")

# Save the presentation
output_pptx = "EdTech_Thesis_Presentation_First_Draft.pptx"
prs.save(output_pptx)
print(f"Presentation saved successfully to {output_pptx} with {len(prs.slides)} slides!")
