import sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path="/workspaces/CC_3/Project_Idea_Check-in.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Definitions
    C_NAVY_DARK = RGBColor(15, 28, 54)      # #0F1C36
    C_NAVY_CARD = RGBColor(24, 38, 68)      # #182644
    C_WHITE = RGBColor(255, 255, 255)       # #FFFFFF
    C_OFFWHITE = RGBColor(248, 250, 252)    # #F8FAFC
    C_BORDER_LIGHT = RGBColor(226, 232, 240)# #E2E8F0
    C_BORDER_DARK = RGBColor(51, 65, 85)    # #334155
    C_CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF
    C_CARD_ALT = RGBColor(241, 245, 249)    # #F1F5F9
    
    C_BLUE = RGBColor(2, 132, 199)          # #0284C7 - UNESCO Blue
    C_BLUE_LIGHT = RGBColor(224, 242, 254)  # #E0F2FE
    C_AMBER = RGBColor(224, 98, 43)         # #E0622B - Warm Terracotta/Amber
    C_AMBER_LIGHT = RGBColor(254, 237, 222) # #FEedDE
    C_CYAN = RGBColor(8, 145, 178)          # #0891B2 - Giga Cyan
    C_CYAN_LIGHT = RGBColor(207, 250, 254)  # #CFFAFE
    C_TEAL = RGBColor(13, 148, 136)         # #0D9488
    
    C_TEXT_DARK = RGBColor(30, 41, 59)      # #1E293B
    C_TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B
    C_TEXT_LIGHT = RGBColor(241, 245, 249)  # #F1F5F9
    C_TEXT_SUBDUE = RGBColor(148, 163, 184) # #94A3B8

    FONT_TITLE = "Trebuchet MS"
    FONT_BODY = "Calibri"

    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_notes(slide, text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = text

    def add_header(slide, tag_text, title_text, dark_mode=False):
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.733), Inches(0.35))
        tf = tag_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = ""
        r = p.add_run()
        r.text = tag_text.upper()
        r.font.name = FONT_BODY
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = C_BLUE if not dark_mode else C_BLUE_LIGHT

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(11.733), Inches(0.75))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = ""
        r = p.add_run()
        r.text = title_text
        r.font.name = FONT_TITLE
        r.font.size = Pt(22)
        r.font.bold = True
        r.font.color.rgb = C_TEXT_DARK if not dark_mode else C_WHITE

    # =========================================================================
    # SLIDE 1: TITLE & EXECUTIVE HOOK (Dark Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, C_NAVY_DARK)

    # Tag
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(0.9), Inches(11.333), Inches(0.4))
    tf = t_box.text_frame
    p = tf.paragraphs[0]
    p.text = ""
    r = p.add_run()
    r.text = "MASTER IN ICT FOR DEVELOPMENT AND SOCIAL GOOD  ·  PROJECT CLINIC CHECK-IN"
    r.font.name = FONT_BODY
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = C_BLUE_LIGHT

    # Main Title
    t_box2 = s1.shapes.add_textbox(Inches(1.0), Inches(1.4), Inches(11.333), Inches(1.8))
    tf2 = t_box2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = ""
    r1 = p2.add_run()
    r1.text = "Context Over Devices:"
    r1.font.name = FONT_TITLE
    r1.font.size = Pt(40)
    r1.font.bold = True
    r1.font.color.rgb = C_WHITE

    p2b = tf2.add_paragraph()
    r2 = p2b.add_run()
    r2.text = "A Six-Pillars EdTech Observatory for Sub-Saharan Africa"
    r2.font.name = FONT_TITLE
    r2.font.size = Pt(28)
    r2.font.bold = True
    r2.font.color.rgb = C_AMBER

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(1.0), Inches(3.2), Inches(11.333), Inches(0.6))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = ""
    r_sub = p_sub.add_run()
    r_sub.text = "Vertical Traceability: Linking National Policy, School-Level Maps, and Classroom Realities"
    r_sub.font.name = FONT_BODY
    r_sub.font.size = Pt(15)
    r_sub.font.color.rgb = C_TEXT_SUBDUE

    # 30-Sec Pitch Card
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.1), Inches(11.333), Inches(1.6))
    card.fill.solid()
    card.fill.fore_color.rgb = C_NAVY_CARD
    card.line.color.rgb = C_BORDER_DARK
    tf_card = card.text_frame
    tf_card.word_wrap = True
    tf_card.margin_left = tf_card.margin_right = Inches(0.5)
    tf_card.margin_top = Inches(0.25)
    
    pc1 = tf_card.paragraphs[0]
    pc1.text = ""
    rc1 = pc1.add_run()
    rc1.text = "THE CORE THESIS:"
    rc1.font.name = FONT_BODY
    rc1.font.size = Pt(11.5)
    rc1.font.bold = True
    rc1.font.color.rgb = C_BLUE_LIGHT
    
    pc2 = tf_card.add_paragraph()
    pc2.space_before = Pt(4)
    rc2 = pc2.add_run()
    rc2.text = "EdTech failure in Sub-Saharan Africa is not a software defect—it is a structural disconnect between national procurement models and classroom realities. This project delivers an open-access diagnostic observatory to evaluate infrastructure, teacher capacity, and linguistic fit before capital is spent."
    rc2.font.name = FONT_BODY
    rc2.font.size = Pt(13.5)
    rc2.font.color.rgb = C_WHITE

    # Footer
    f_box = s1.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.333), Inches(0.5))
    tf_f = f_box.text_frame
    pf = tf_f.paragraphs[0]
    pf.text = ""
    rf = pf.add_run()
    rf.text = "Candidate: Master Degree Candidate   |   Reviewer: Prof. Elisa Bignante   |   UniTO · COREP · Impactskills (A.Y. 2025–2026)"
    rf.font.name = FONT_BODY
    rf.font.size = Pt(11)
    rf.font.color.rgb = C_TEXT_SUBDUE

    add_notes(s1,
        "Good morning Professor Bignante. Today I am presenting the concept and working prototype for my final project: 'Context Over Devices: A Six-Pillars EdTech Observatory for Sub-Saharan Africa'.\n\n"
        "In this 5-minute check-in, I will show you why traditional EdTech interventions in Africa chronically fail, who the primary stakeholders are, how our 3-tiered methodology links national policies directly to classroom desks, and the concrete tools we have built.\n\n"
        "Our core argument is simple: technology fit starts with the physical, pedagogical, and linguistic conditions of the classroom—not with buying devices."
    )

    # =========================================================================
    # SLIDE 2: THE STAKEHOLDERS (Voices, Bottlenecks & Benefits)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, C_OFFWHITE)
    add_header(s2, "1. Stakeholder Reality", "Who This Serves: Real Voices, Bottlenecks & Concrete Benefits")

    stakeholder_cards = [
        ("FRONTLINE TEACHERS",
         "The Lived Bottleneck:",
         "\"We teach 50+ pupils with daily blackouts. The ministry gave us a portal with zero data budget. We spend 4%–8% of our salary on mobile data just to log student marks.\"",
         "How This Project Benefits Them:",
         "• Screener halts unfeasible app mandates.\n• 3-Station Rotation makes 50:1 classes work.\n• Promotes 100% offline tools with zero data cost.",
         C_AMBER, Inches(0.8), Inches(1.7)),

        ("HEADTEACHERS & SMCS",
         "The Lived Bottleneck:",
         "\"Donors drop boxes of tablets for photo-ops. After 6 months, cracked screens and dead batteries turn them into bricks. Shady apps harvest our children's data.\"",
         "How This Project Benefits Them:",
         "• 40/60 Lifecycle Rule guarantees repair funds.\n• SMC Safeguarding Rubric audits apps.\n• Blocks commercial child tracking & ads.",
         C_BLUE, Inches(6.88), Inches(1.7)),

        ("AFRICAN INNOVATORS",
         "The Lived Bottleneck:",
         "\"Public tenders demand cloud-first SaaS that locks us out. Meanwhile foreign AI drops from 90% accuracy in English to 18% in local African languages.\"",
         "How This Project Benefits Them:",
         "• Discrepancy Matrix proves offline tools win.\n• Promotes certified Digital Public Goods (DPGs).\n• Levels playing field against foreign tech giants.",
         C_TEAL, Inches(0.8), Inches(4.3)),

        ("MINISTRIES & DONORS",
         "The Lived Bottleneck:",
         "\"We borrow tens of millions in digital learning loans, yet 85% of pilots fail to scale, 87% learning poverty persists, and national statistics hide rural reality.\"",
         "How This Project Benefits Them:",
         "• Six-Pillars Observatory diagnoses bottlenecks.\n• Flags power & teacher gaps before tenders.\n• Prevents multi-million-dollar capital waste.",
         C_NAVY_DARK, Inches(6.88), Inches(4.3))
    ]

    for title, lbl1, quote, lbl2, benefits, acc_col, left_p, top_p in stakeholder_cards:
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_p, top_p, Inches(5.65), Inches(2.35))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        tf_b = box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = Inches(0.28)
        tf_b.margin_top = Inches(0.18)

        # Top tag
        p0 = tf_b.paragraphs[0]
        p0.text = ""
        r0 = p0.add_run()
        r0.text = title
        r0.font.name = FONT_BODY
        r0.font.size = Pt(11)
        r0.font.bold = True
        r0.font.color.rgb = acc_col

        # Quote / Bottleneck
        p1 = tf_b.add_paragraph()
        p1.space_before = Pt(3)
        r_q = p1.add_run()
        r_q.text = quote
        r_q.font.name = FONT_BODY
        r_q.font.size = Pt(10)
        r_q.font.italic = True
        r_q.font.color.rgb = C_TEXT_DARK

        # Benefit
        p2 = tf_b.add_paragraph()
        p2.space_before = Pt(4)
        r_b_lbl = p2.add_run()
        r_b_lbl.text = lbl2 + " "
        r_b_lbl.font.name = FONT_BODY
        r_b_lbl.font.size = Pt(10)
        r_b_lbl.font.bold = True
        r_b_lbl.font.color.rgb = acc_col

        p3 = tf_b.add_paragraph()
        p3.text = ""
        r3 = p3.add_run()
        r3.text = benefits
        r3.font.name = FONT_BODY
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = C_TEXT_MUTED

    add_notes(s2,
        "To ground our research in human reality, we mapped out the four key actors in African educational technology.\n\n"
        "First, frontline teachers: they face 50-student classrooms, load-shedding blackouts, and an informal salary tax where they spend 4% to 8% of their own wages buying mobile data bundles to sync attendance apps. Our project gives them a feasibility screener and rotation planner to make shared devices work offline.\n\n"
        "Second, school heads and School Management Committees: they receive donated tablets that break within six months because there is zero repair budget—what we call the 'pilot graveyard'. Our framework provides a 40/60 lifecycle budgeting rule and a child data protection rubric.\n\n"
        "Third, local African EdTech innovators: they are locked out of government tenders that mandate cloud software, even though imported Western AI tools collapse from 90% accuracy in English to 18% in indigenous languages like Swahili and Hausa. Our observatory provides evidence that offline, mother-tongue tools are pedagogically superior.\n\n"
        "Fourth, education ministries and donors: they spend millions on loans without knowing whether schools have power or trained teachers. Our observatory diagnoses these bottleneck pillars before contracts are signed."
    )

    # =========================================================================
    # SLIDE 3: THE PISA BLIND SPOT & SCARCITY DIVIDE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, C_OFFWHITE)
    add_header(s3, "2. Theoretical Critique", "The PISA Blind Spot: Why Global Benchmarks Misdirect African Policy")

    pisa_cards = [
        ("THE PISA DATA DESERT",
         "Sub-Saharan Africa is Excluded",
         "• Standard OECD PISA databases contain virtually zero Sub-Saharan African countries.\n• PISA tests only enrolled 15-year-olds; it renders 30%–50% of out-of-school African youth completely invisible.\n• International reports rely on OECD samples to formulate 'global' EdTech rules ungrounded in Africa.",
         C_BLUE, Inches(0.8)),

        ("SCARCITY VS. SATURATION",
         "The Digital Threshold of Access",
         "• OECD Schools (Saturation): Screen exposure correlates with distraction, multitasking, and AI offloading.\n• African Schools (Scarcity): A single solar screen or offline library yields steep, positive cognitive gains.\n• Non-Linear Returns: Moving from 0 to 1 device is transformative; moving from 1 to 30 adds diminishing value.",
         C_AMBER, Inches(4.78)),

        ("THE TRANSPOSITION TRAP",
         "Policy Invariance Fallacy",
         "• When global agencies import OECD findings to Africa, they prescribe digital austerity ('cut screen time').\n• Advising African schools to limit devices when they lack basic textbooks is a severe category error.\n• Africa needs metrics grounded in infrastructure thresholds, teacher coaching, and local languages.",
         C_TEAL, Inches(8.76))
    ]

    for title, subtitle, bullets, col, left_p in pisa_cards:
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_p, Inches(1.7), Inches(3.77), Inches(4.3))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        tf_b = box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = Inches(0.28)
        tf_b.margin_top = Inches(0.22)

        p0 = tf_b.paragraphs[0]
        p0.text = ""
        r0 = p0.add_run()
        r0.text = title
        r0.font.name = FONT_BODY
        r0.font.size = Pt(11)
        r0.font.bold = True
        r0.font.color.rgb = col

        p1 = tf_b.add_paragraph()
        r1 = p1.add_run()
        r1.text = subtitle
        r1.font.name = FONT_TITLE
        r1.font.size = Pt(13)
        r1.font.bold = True
        r1.font.color.rgb = C_TEXT_DARK

        p2 = tf_b.add_paragraph()
        p2.space_before = Pt(8)
        r2 = p2.add_run()
        r2.text = bullets
        r2.font.name = FONT_BODY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_TEXT_MUTED

    # Bottom Callout Bar
    bar3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.8))
    bar3.fill.solid()
    bar3.fill.fore_color.rgb = C_CARD_ALT
    bar3.line.color.rgb = C_BORDER_LIGHT
    tf_bar3 = bar3.text_frame
    tf_bar3.word_wrap = True
    p_b3 = tf_bar3.paragraphs[0]
    p_b3.text = ""
    rb3 = p_b3.add_run()
    rb3.text = "THE TAKEAWAY: PISA measures what happens when high-income schools reach digital saturation. African educational policy cannot be guided by the symptoms of wealthy-school distraction."
    rb3.font.name = FONT_BODY
    rb3.font.size = Pt(11.5)
    rb3.font.color.rgb = C_TEXT_DARK

    add_notes(s3,
        "A critical question is: what is our link to PISA and global assessments?\n\n"
        "International development policy is dominated by PISA metrics. But PISA has a massive blind spot: Sub-Saharan Africa is an absolute data desert in PISA datasets. Furthermore, PISA samples only 15-year-olds enrolled in formal schools, completely missing the 30% to 50% of African youth who are out of school.\n\n"
        "This leads to what we identify as the 'Scarcity vs. Saturation Divide'. In OECD schools, technology is saturated; more screen time often correlates with distraction and AI offloading. But in rural African schools, classrooms operate in acute scarcity. Moving from zero devices to just one solar-powered screen or offline library creates massive learning gains.\n\n"
        "When global whitepapers cite PISA to recommend 'limiting screen exposure in classrooms', they impose digital austerity on African schools that are starving for learning media. Our thesis establishes why Africa needs its own grounded evidence architecture."
    )

    # =========================================================================
    # SLIDE 4: VERTICAL TRACEABILITY (The Golden Thread: Macro -> GigaMaps -> Micro)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, C_OFFWHITE)
    add_header(s4, "3. Narrative Architecture", "Vertical Traceability: Linking National Policy, School Maps & Classrooms")

    levels = [
        ("LEVEL 1: MACRO OPEN DATA",
         "National Policy & Census Indicators",
         "• Aggregated statistics from World Bank, UIS, and ITU across 48 SSA nations.\n• Tracks 237 active World Bank digital education loan projects ($ billions).\n• THE BLIND SPOT: National averages (e.g. 70% national power) conceal acute rural infrastructure deserts.",
         C_BLUE, Inches(0.8)),

        ("LEVEL 2: MESO SPATIAL MAPPING",
         "UNICEF-ITU GigaMaps & Project Flows",
         "• THE CONNECTIVE BRIDGE: Mapping school-by-school GPS coordinates and real-time connectivity.\n• Spatial ground-truth: Reveals that while capital cities are connected, 70% of rural schools have ZERO grid.\n• IN PROGRESS: Integrating the live Giga API feed into the observatory over the next month.",
         C_CYAN, Inches(4.78)),

        ("LEVEL 3: MICRO CLASSROOM REALITY",
         "Practitioner Diagnostics & Agency",
         "• Grounded in UNESCO Global Education Coalition (AoA) practitioner instruments.\n• Class realities: 50:1 pupil-teacher ratios, 4%–8% teacher airtime burdens, and indigenous language gaps.\n• OPERATIONAL TOOLS: Classroom Feasibility Screener, 3-Station Rotation Planner, and offline DPGs.",
         C_AMBER, Inches(8.76))
    ]

    for title, subtitle, bullets, col, left_p in levels:
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_p, Inches(1.7), Inches(3.77), Inches(4.3))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        tf_b = box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = Inches(0.28)
        tf_b.margin_top = Inches(0.22)

        p0 = tf_b.paragraphs[0]
        p0.text = ""
        r0 = p0.add_run()
        r0.text = title
        r0.font.name = FONT_BODY
        r0.font.size = Pt(11)
        r0.font.bold = True
        r0.font.color.rgb = col

        p1 = tf_b.add_paragraph()
        r1 = p1.add_run()
        r1.text = subtitle
        r1.font.name = FONT_TITLE
        r1.font.size = Pt(13)
        r1.font.bold = True
        r1.font.color.rgb = C_TEXT_DARK

        p2 = tf_b.add_paragraph()
        p2.space_before = Pt(8)
        r2 = p2.add_run()
        r2.text = bullets
        r2.font.name = FONT_BODY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_TEXT_MUTED

    # Bottom Connective Thread Bar
    bar4 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.8))
    bar4.fill.solid()
    bar4.fill.fore_color.rgb = C_CARD_ALT
    bar4.line.color.rgb = C_BORDER_LIGHT
    tf_bar4 = bar4.text_frame
    tf_bar4.word_wrap = True
    p_b4 = tf_bar4.paragraphs[0]
    p_b4.text = ""
    rb4 = p_b4.add_run()
    rb4.text = "THE GOLDEN THREAD: An EdTech tender can be traced vertically: National Policy (Macro) → School-by-School Connectivity via GigaMaps (Meso) → Teacher's Desk & Chalkboard Feasibility (Micro)."
    rb4.font.name = FONT_BODY
    rb4.font.size = Pt(11.5)
    rb4.font.bold = True
    rb4.font.color.rgb = C_TEXT_DARK

    add_notes(s4,
        "Here is the coherent narrative thread that connects our entire project: Vertical Traceability.\n\n"
        "Previous EdTech research failed because it looked at only one level in isolation. A Ministry looks at Level 1 Macro data—seeing that Kenya has 75% electricity and an approved national ICT plan—and approves a cloud laptop contract.\n\n"
        "But when you zoom into Level 2 Meso spatial mapping—using UNICEF-ITU GigaMaps—you discover that while Nairobi schools have broadband, 65% of rural primary schools have zero grid power and zero internet.\n\n"
        "Then zoom into Level 3 Micro classroom reality: the teacher has 55 pupils, speaks Kikuyu, and is expected to pay out-of-pocket for airtime.\n\n"
        "Our observatory links these levels together. GigaMaps is the spatial bridge connecting national indicators to school desks. In our web prototype, the GIGA monitor interface is already staged, and over the next month we are working to finalize the live school data connection."
    )

    # =========================================================================
    # SLIDE 5: COMPONENT B: THE OBSERVATORY PROTOTYPE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, C_OFFWHITE)
    add_header(s5, "4. Practical Component", "The Observatory Prototype: Live Decision Tools for Sub-Saharan Africa")

    tools = [
        ("7 SSA COUNTRY PROFILES",
         "Comparative Discrepancy Matrix",
         "• In-depth profiles: Kenya, Rwanda, Tanzania, Ghana, Nigeria, Zambia, and Mauritius.\n• Discrepancy Matrix directly exposes the gap where national plans assume grid power that classrooms lack.\n• Real-time filtering across UNESCO's Six Pillars.",
         C_BLUE, Inches(0.8)),

        ("FEASIBILITY SCREENER",
         "Classroom Diagnostic & 3-Station Planner",
         "• 7-point audit: grid cuts, airtime costs, device ratios, mother-tongue alignment.\n• 3-Station Rotation Calculator: schedules 10 tablets to serve 50 pupils with 100% weekly digital engagement.\n• Eliminates need for costly 1:1 hardware mandates.",
         C_AMBER, Inches(4.78)),

        ("RESILIENT DPG DIRECTORY",
         "Offline Tools & Child Safeguarding",
         "• Curated catalog of certified Digital Public Goods: Kolibri, RACHEL, African Storybook, PhET simulations.\n• School Management Committee (SMC) Scorecard to audit commercial tracking and child data sovereignty.\n• 100% offline-compatible architectures.",
         C_TEAL, Inches(8.76))
    ]

    for title, subtitle, bullets, col, left_p in tools:
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_p, Inches(1.7), Inches(3.77), Inches(4.3))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        tf_b = box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = Inches(0.28)
        tf_b.margin_top = Inches(0.22)

        p0 = tf_b.paragraphs[0]
        p0.text = ""
        r0 = p0.add_run()
        r0.text = title
        r0.font.name = FONT_BODY
        r0.font.size = Pt(11)
        r0.font.bold = True
        r0.font.color.rgb = col

        p1 = tf_b.add_paragraph()
        r1 = p1.add_run()
        r1.text = subtitle
        r1.font.name = FONT_TITLE
        r1.font.size = Pt(13)
        r1.font.bold = True
        r1.font.color.rgb = C_TEXT_DARK

        p2 = tf_b.add_paragraph()
        p2.space_before = Pt(8)
        r2 = p2.add_run()
        r2.text = bullets
        r2.font.name = FONT_BODY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_TEXT_MUTED

    # Bottom URLs bar
    bar5 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.8))
    bar5.fill.solid()
    bar5.fill.fore_color.rgb = C_CARD_ALT
    bar5.line.color.rgb = C_BORDER_LIGHT
    tf_bar5 = bar5.text_frame
    tf_bar5.word_wrap = True
    p_b5 = tf_bar5.paragraphs[0]
    p_b5.text = ""
    rb5 = p_b5.add_run()
    rb5.text = "LIVE CLIENT-SIDE PROTOTYPE (STATIC GITHUB PAGES, ZERO HOSTING COST):"
    rb5.font.name = FONT_BODY
    rb5.font.size = Pt(10.5)
    rb5.font.bold = True
    rb5.font.color.rgb = C_BLUE

    p_b5b = tf_bar5.add_paragraph()
    rb5b = p_b5b.add_run()
    rb5b.text = "Primary Observatory: https://rsnl42.github.io/CC_3/    ·    Comparative Engine: https://rsnl42.github.io/EEA_2/"
    rb5b.font.name = FONT_BODY
    rb5b.font.size = Pt(11.5)
    rb5b.font.bold = True
    rb5b.font.color.rgb = C_TEXT_DARK

    add_notes(s5,
        "In fulfillment of Component B of the Master's guidelines, this project has produced a live, interactive software prototype.\n\n"
        "Hosted openly on GitHub Pages, the observatory includes:\n"
        "First, seven SSA country profiles with our Discrepancy Matrix, contrasting policy ambitions against verified classroom data.\n"
        "Second, a practical Classroom Feasibility Screener and 3-Station Rotation Planner. Instead of requiring an impossible 50 laptops, our scheduling tool shows how 10 tablets and one solar charging kit give 50 students weekly hands-on digital learning.\n"
        "Third, a vetted catalog of Digital Public Goods—tools like Kolibri and African Storybook that run 100% offline—coupled with an SMC data privacy checklist.\n\n"
        "The application is static, runs client-side with zero server upkeep, and loads in under 1.5 seconds even on 3G connections."
    )

    # =========================================================================
    # SLIDE 6: FOUR CONCRETE POLICY REFORMS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, C_OFFWHITE)
    add_header(s6, "5. Grounded Reforms", "Four Actionable Policies to Halt the 85% Pilot Failure Rate")

    policy_cards = [
        ("1. ABOLISH 1:1 PROCUREMENT MANDATES",
         "The 3-Station Rotational Model",
         "• Ground Reality: Ministries spend 90% of funds buying 1:1 tablets that fail in 50:1 classrooms.\n• Actionable Policy: Mandate 3-station rotational setups (10 tablets + 1 solar charging kit per 50 pupils).\n• Impact: Cuts capital expenditure by 75%–80% while guaranteeing weekly digital engagement.",
         C_AMBER, Inches(0.8), Inches(1.7)),

        ("2. STOP THE TEACHER SALARY TAX",
         "Mandatory Zero-Rating Before Rollout",
         "• Ground Reality: Teachers spend 4% to 8% of personal wages on cellular data to submit school records.\n• Actionable Policy: Legislate that no educational software can be adopted unless telecoms zero-rate access.\n• Impact: Eliminates teacher out-of-pocket costs and prevents administrative burnout.",
         C_BLUE, Inches(6.88), Inches(1.7)),

        ("3. ENFORCE 40/60 LIFECYCLE BUDGETING",
         "Ending the 85% Pilot Collapse Rate",
         "• Ground Reality: 85% of EdTech pilots collapse within 18 months once external donor seed grants expire.\n• Actionable Policy: Cap hardware at 40% and ring-fence 60% for teacher coaching (Pillar 4) and repairs.\n• Impact: Replaces short-term photo-ops with sustained, multi-year pedagogical lifecycles.",
         C_TEAL, Inches(0.8), Inches(4.3)),

        ("4. MOTHER-TONGUE FIRST & OPEN DPGS",
         "Countering AI Linguistic Collapse",
         "• Ground Reality: AI evaluation drops from 90% in English to 18%–38% in indigenous African languages.\n• Actionable Policy: Condition public tenders on local dialect benchmarks (AfroBench) and open DPGs.\n• Impact: Halts cognitive penalties against non-anglophone pupils and avoids proprietary vendor lock-in.",
         C_NAVY_DARK, Inches(6.88), Inches(4.3))
    ]

    for title, subtitle, bullets, col, left_p, top_p in policy_cards:
        box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_p, top_p, Inches(5.65), Inches(2.35))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        tf_b = box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = Inches(0.28)
        tf_b.margin_top = Inches(0.18)

        p0 = tf_b.paragraphs[0]
        p0.text = ""
        r0 = p0.add_run()
        r0.text = title
        r0.font.name = FONT_BODY
        r0.font.size = Pt(11)
        r0.font.bold = True
        r0.font.color.rgb = col

        p1 = tf_b.add_paragraph()
        r1 = p1.add_run()
        r1.text = subtitle
        r1.font.name = FONT_TITLE
        r1.font.size = Pt(12.5)
        r1.font.bold = True
        r1.font.color.rgb = C_TEXT_DARK

        p2 = tf_b.add_paragraph()
        p2.space_before = Pt(4)
        r2 = p2.add_run()
        r2.text = bullets
        r2.font.name = FONT_BODY
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_TEXT_MUTED

    add_notes(s6,
        "Rather than offering generic advice, our framework translates findings into four concrete policy directives:\n\n"
        "First, abolish 1-to-1 procurement mandates. In classrooms of 50 students, buying 50 laptops is fiscal suicide. Our 3-station rotational model uses 10 tablets and one solar charging kit, cutting capital costs by 75%.\n\n"
        "Second, end the informal teacher salary tax. We propose legislation requiring that no software can be mandated in public schools without official zero-rated telecom access or complete offline functionality.\n\n"
        "Third, enforce the 40/60 Lifecycle Allocation Rule. 85% of EdTech pilots fail because 95% of budgets go to hardware photo-ops. We mandate a statutory cap of 40% for hardware, with 60% reserved for teacher coaching and local repair technicians.\n\n"
        "Fourth, mandate mother-tongue first procurement. Natural language processing benchmarks prove that AI accuracy drops from 90% in English to 18% in indigenous African languages. Public tenders must prioritize open Digital Public Goods with local dialect support."
    )

    # =========================================================================
    # SLIDE 7: PROJECT CLINIC CHECK-IN (Dark Navy)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7, C_NAVY_DARK)
    add_header(s7, "6. Advisory Check-In", "Project Clinic Alignment: What Is Established & Where We Seek Guidance", dark_mode=True)

    # Left Column: The Master Formula Card
    c_form = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.65), Inches(5.2))
    c_form.fill.solid()
    c_form.fill.fore_color.rgb = C_NAVY_CARD
    c_form.line.color.rgb = C_BORDER_DARK
    tf_f = c_form.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_right = Inches(0.35)
    tf_f.margin_top = Inches(0.3)

    pf0 = tf_f.paragraphs[0]
    pf0.text = ""
    rf0 = pf0.add_run()
    rf0.text = "THE MASTER PROJECT CLINIC FORMULA"
    rf0.font.name = FONT_BODY
    rf0.font.size = Pt(11.5)
    rf0.font.bold = True
    rf0.font.color.rgb = C_AMBER

    formula_items = [
        ("My project addresses...", "The recurring failure of EdTech procurement in Sub-Saharan Africa caused by ignoring classroom physical, pedagogical, and linguistic constraints."),
        ("Its main objective is...", "To deliver an open-access Six-Pillars observatory providing pre-procurement decision support for ministries, donors, and school leaders."),
        ("I will produce...", "A comprehensive Master thesis (Component A) alongside a live interactive web observatory and open-source data pipeline (Component B)."),
        ("Feasibility boundaries...", "Public APIs and secondary studies are verified; synthetic panels are strictly labeled. No unvalidated causal claims are made.")
    ]
    for lbl, body in formula_items:
        p = tf_f.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = lbl + "\n"
        r1.font.name = FONT_TITLE
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = C_WHITE

        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_BODY
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_TEXT_SUBDUE

    # Right Column: Targeted Reviewer Feedback Questions
    c_quest = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.88), Inches(1.7), Inches(5.65), Inches(5.2))
    c_quest.fill.solid()
    c_quest.fill.fore_color.rgb = C_NAVY_CARD
    c_quest.line.color.rgb = C_BORDER_DARK
    tf_q = c_quest.text_frame
    tf_q.word_wrap = True
    tf_q.margin_left = tf_q.margin_right = Inches(0.35)
    tf_q.margin_top = Inches(0.3)

    pq0 = tf_q.paragraphs[0]
    pq0.text = ""
    rq0 = pq0.add_run()
    rq0.text = "TARGETED QUESTIONS FOR REVIEWER GUIDANCE"
    rq0.font.name = FONT_BODY
    rq0.font.size = Pt(11.5)
    rq0.font.bold = True
    rq0.font.color.rgb = C_BLUE_LIGHT

    questions = [
        ("1. Comparative Depth vs. Breadth:", "We currently profile seven SSA countries. Would you recommend narrowing the final comparative chapter to 2–3 contrasting focal cases (e.g. Kenya's market model vs. Rwanda's state digitisation vs. Zambia)?"),
        ("2. GigaMaps Integration Scope:", "For the Level 2 spatial bridge, should we integrate school-level GigaMaps as an illustrative case study (e.g., Kenya & Rwanda) to prove the vertical traceability concept?"),
        ("3. Practitioner Testing Priority:", "For our user-testing cycle ahead of the Nov 30 final deadline, should we prioritize practitioner feedback on the Classroom Feasibility Screener or the 3-Station Rotation Planner?")
    ]
    for q_t, q_b in questions:
        p = tf_q.add_paragraph()
        p.space_before = Pt(12)
        rq1 = p.add_run()
        rq1.text = q_t + "\n"
        rq1.font.name = FONT_TITLE
        rq1.font.size = Pt(12)
        rq1.font.bold = True
        rq1.font.color.rgb = C_WHITE

        rq2 = p.add_run()
        rq2.text = q_b
        rq2.font.name = FONT_BODY
        rq2.font.size = Pt(11)
        rq2.font.color.rgb = C_TEXT_SUBDUE

    add_notes(s7,
        "To conclude, I map our project directly to Professor Bignante's workshop guidance:\n\n"
        "My project addresses the failure of EdTech procurement in Sub-Saharan Africa.\n"
        "Its main objective is to build an open decision observatory to evaluate fit before money is spent.\n"
        "I plan to deliver the full academic thesis alongside our live web observatory.\n"
        "Our feasibility is secured by using verified open data, clearly labeling simulation models, and focusing on realistic tools.\n\n"
        "I would deeply appreciate your guidance on three points: "
        "First, should we narrow our seven SSA profiles to 2–3 deep focal cases? "
        "Second, how far should we take the GigaMaps school connectivity integration? "
        "And third, which tool should we prioritize for user feedback before our November 30 deadline?\n\n"
        "Thank you very much, and I welcome your feedback."
    )

    # =========================================================================
    # BACKUP SLIDE A: GIGAMAPS & TECHNICAL ARCHITECTURE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, C_OFFWHITE)
    add_header(s8, "Backup Slide A: Technical Architecture", "The Meso Bridge: UNICEF-ITU GigaMaps & Automated Python Pipeline")

    b_cards = [
        ("UNICEF-ITU GIGAMAPS",
         "School-Level Spatial Connectivity",
         "• Maps individual school GPS coordinates, electrification status, and internet speeds.\n• Acts as the empirical bridge between national macro indicators and local classroom feasibility.\n• Staged in index.html, awaiting endpoint activation for real-time school telemetry.",
         C_CYAN, Inches(0.8), Inches(1.7)),

        ("MESO DATA PIPELINE",
         "Automated Multi-Source Extraction",
         "• fetch_6pillars_pipeline.py queries World Bank (WDI/SPI), UIS, and ITU endpoints.\n• Ingests 11,393 longitudinal observations across 48 SSA nations (2015–2024).\n• Tracks 237 active digital learning loans; cached on disk to survive network rate limits.",
         C_BLUE, Inches(6.88), Inches(1.7)),

        ("CLIENT-SIDE WEB ARCHITECTURE",
         "Zero-Cost GitHub Pages Deployment",
         "• Built with vanilla HTML5, Tailwind CSS, and lightweight client-side JavaScript.\n• Sub-1.5s load times on 3G mobile connections; zero database or server hosting fees.\n• Offline-resilient and easily cloneable by African ministries, universities, or local hubs.",
         C_TEAL, Inches(0.8), Inches(4.3)),

        ("DATA HYGIENE PROTOCOL",
         "Academic Integrity & Stratification",
         "• Census Data: Real historical indicators from official UN/WB statistical systems.\n• Field Voices: Verified secondary quotations from GEM reports and published literature.\n• Calibrated Synthetic Panels: Used strictly for UI testing and simulation; explicitly labeled.",
         C_NAVY_DARK, Inches(6.88), Inches(4.3))
    ]

    for title, subtitle, bullets, col, left_p, top_p in b_cards:
        box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_p, top_p, Inches(5.65), Inches(2.35))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        tf_b = box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = Inches(0.28)
        tf_b.margin_top = Inches(0.18)

        p0 = tf_b.paragraphs[0]
        p0.text = ""
        r0 = p0.add_run()
        r0.text = title
        r0.font.name = FONT_BODY
        r0.font.size = Pt(11)
        r0.font.bold = True
        r0.font.color.rgb = col

        p1 = tf_b.add_paragraph()
        r1 = p1.add_run()
        r1.text = subtitle
        r1.font.name = FONT_TITLE
        r1.font.size = Pt(12.5)
        r1.font.bold = True
        r1.font.color.rgb = C_TEXT_DARK

        p2 = tf_b.add_paragraph()
        p2.space_before = Pt(4)
        r2 = p2.add_run()
        r2.text = bullets
        r2.font.name = FONT_BODY
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_TEXT_MUTED

    add_notes(s8,
        "Backup Slide A details the technical architecture of our meso layer. "
        "GigaMaps is UNICEF and ITU's joint initiative to map the connectivity of every school in the world. Integrating this data provides the spatial bridge that explains why national electricity statistics fail to reflect rural school reality. "
        "Our automated Python pipeline ingests indicators across 48 Sub-Saharan African nations and tracks 237 active World Bank digital education projects, while our web prototype remains completely serverless and hosted on GitHub Pages."
    )

    # =========================================================================
    # BACKUP SLIDE B: ANALYTICAL FRAMEWORK 2 MAPPING
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9, C_OFFWHITE)
    add_header(s9, "Backup Slide B: Master Analytical Rubric", "Analytical Framework 2 Alignment Matrix: Addressing All 13 Dimensions")

    af_dimensions = [
        ("TECHNOLOGY FOCUS (Q1–Q3)",
         "• Q1 Output: Live web observatory (CC_3 & EEA_2) + Python pipeline + decision rubric.\n• Q2 Social Good: Informed public resource allocation; equity for off-grid learners.\n• Q3 Ideology: Exposes donor/vendor standardization vs. teacher/learner realities.",
         C_BLUE, Inches(0.8), Inches(1.7)),

        ("RESEARCH APPROACH (Q4–Q6)",
         "• Q4 Modalities: Observation (PISA), development (pipeline), participatory audit (AoA).\n• Q5 Power Matrix: High power of donors/ministries vs. zero power of frontline teachers.\n• Q6 Participatory: Grounded in UNESCO GEC survey design; open-access dissemination.",
         C_AMBER, Inches(6.88), Inches(1.7)),

        ("DEVELOPMENT & DIVIDES (Q7–Q9)",
         "• Q7 Developer: Researcher-developer hybrid; AI used strictly per UniTO Section 26.\n• Q8 Constraints: Electrification <30%, mobile data tariffs, client-side static constraints.\n• Q9 Divides: Physical infrastructure, 4–8% teacher airtime tax, indigenous NLP drop.",
         C_TEAL, Inches(0.8), Inches(4.3)),

        ("ADAPTABILITY & ETHICS (Q10–Q13)",
         "• Q10 Adaptability: Modular 3-tier architecture (off-grid solar, local Wi-Fi, urban hybrid).\n• Q11 Scalability: Static serverless hosting; reproducible open-source licensing.\n• Q12–13 Ethics: Anti-extractivism; child data privacy; compliance with Kenya DPA & POPIA.",
         C_NAVY_DARK, Inches(6.88), Inches(4.3))
    ]

    for title, txt, col, left_p, top_p in af_dimensions:
        box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_p, top_p, Inches(5.65), Inches(2.35))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.28)
        tf.margin_top = Inches(0.18)

        p1 = tf.paragraphs[0]
        p1.text = ""
        r1 = p1.add_run()
        r1.text = title
        r1.font.name = FONT_BODY
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.space_before = Pt(6)
        r2 = p2.add_run()
        r2.text = txt
        r2.font.name = FONT_BODY
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_TEXT_DARK

    add_notes(s9,
        "Backup Slide B maps our thesis directly to the 13 questions of Analytical Framework 2. "
        "Every requirement—from technology output and social good goals, to stakeholder power dynamics, technical constraints, adaptability tiers, and ethical governance under African data protection laws—is addressed both in our thesis document and in our practical tools."
    )

    prs.save(output_path)
    print(f"Successfully generated {output_path} with {len(prs.slides)} slides!")

if __name__ == "__main__":
    build_presentation()
