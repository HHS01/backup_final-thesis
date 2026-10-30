# Analysis B: Multi-Stakeholder Triangulation & Discrepancy Matrix
**Version:** 1.0 · **Date:** 2026-10-30  
**Countries:** Kenya (KEN), Rwanda (RWA), Mauritius (MUS), Zambia (ZMB)  
**Data sources:** World Bank / UNESCO macro indicators (`latest_country_profiles_6pillars.csv`); AoA Survey codebook (Analysis A); GEM Report 2023; IrokoBench / AfroBench; HolonIQ 2025 Africa EdTech 50; Synthesis doc

---

## Purpose

Analysis B quantifies the three structural discrepancies identified in Analysis A — the gaps between what EdTech *providers assume* about the contexts they operate in, what *teachers experience* on the ground, and what *macro evidence* confirms. This is the triangulation layer of the thesis: it tests whether the supply side and the demand side of EdTech operate with a shared understanding of reality.

The three gaps are:
1. **Connectivity Assumption Gap** — Providers deliver via channels that require connectivity/devices classrooms don't have
2. **Cost & Sustainability Gap** — The financial burden of EdTech falls on actors (teachers, families, governments) least able to absorb it
3. **Linguistic Inclusion Gap** — EdTech tools operate in languages that do not match classroom linguistic realities

---

## Gap 1: Connectivity Assumption Gap

### Hypothesis
EdTech providers systematically design for better connectivity than classrooms have, creating a structural mismatch between supply-side assumptions and demand-side reality.

### Macro Evidence

| Indicator | KEN | RWA | MUS | ZMB | SSA Median |
|---|---|---|---|---|---|
| Internet users — total pop (%) | 35.0 | 31.7 | **73.3** | 17.1 | 34.5 |
| School connectivity estimate (%) | 65.6 | n/a | n/a | 58.8 | ~55.5 |
| Rural electricity access (%) | 67.1 | 65.2 | **100.0** | 31.3 | 41.1 |
| Urban electricity access (%) | 98.1 | 88.0 | 100.0 | 80.3 | 85.3 |
| Fixed broadband per 100 | 3.0 | 0.6 | **28.0** | 0.8 | 0.6 |
| Mobile subscriptions per 100 | 126.5 | 93.2 | 172.7 | 108.7 | 93.7 |

**Data years:** All 2024 (World Bank WDI). School connectivity from ITU/Unicef con30e estimate.

### Key Findings

**1.1 The broadband cliff.** HolonIQ's 2025 Africa EdTech 50 shows 70% of EdTech solutions use direct-to-consumer (D2C) models delivered primarily via smartphone apps and web browsers — channels that assume reliable data connectivity. Against this, fixed broadband penetration is **3.0 per 100** in Kenya, **0.6 in Rwanda**, and **0.8 in Zambia** (SSA median: 0.6). Only Mauritius (28.0/100) has broadband infrastructure comparable to provider assumptions. The mobile-first narrative partially offsets this — mobile subscriptions exceed 100/100 in Kenya and Zambia — but mobile data is metered, expensive relative to income (see Gap 2), and latency-constrained for rich-media content.

**1.2 Electricity as the upstream constraint.** Before connectivity can be considered, power must be available. Rural electricity access is **31.3% in Zambia**, **65.2% in Rwanda**, and **67.1% in Kenya** — with urban-rural gaps of 49–67 percentage points in Zambia and Kenya. GEM Report 2023 confirms that in 2021, more than 70% of people in rural SSA had no electricity access. School connectivity estimates (~55–66% where available) are optimistic relative to rural reality: connectivity measured at school level likely includes urban-biased sampling. Any EdTech solution that requires charging — even offline apps on tablets — faces this upstream constraint in rural schools.

**1.3 The offline-first validation test.** AoA Provider Survey item P-C2 asks whether the core product can be used fully offline. The codebook identifies this as the critical triangulation item for Gap 1. Against the evidence above, *any provider answering "No, it needs a connection"* is structurally excluded from reaching rural classrooms in ZMB, RWA, and KEN. The proportion of SSA-focused providers meeting this threshold is unknown without survey responses — but HolonIQ's D2C-majority figure and the low broadband numbers suggest a significant fraction of the EdTech market is building for a connectivity level that does not yet exist at classroom scale.

**1.4 Mauritius as a structural outlier.** Mauritius (100% electricity, 73.3% internet, 28.0 fixed broadband/100) operates at a fundamentally different infrastructure tier. Any regional analysis that averages across SSA risks anchoring on Mauritius-style connectivity assumptions. This is a key methodological caveat for the thesis.

### Discrepancy Score Summary (Gap 1)

| Sub-dimension | KEN | RWA | MUS | ZMB |
|---|---|---|---|---|
| G1a: Internet access gap | 2 – High | 3 – High | 1 – Low | 4 – Very high |
| G1b: Rural electricity vs. broadband need | 3 – High | 3 – High | 1 – Low | 5 – Critical |
| G1c: School connectivity vs. total pop internet | 2 – Moderate | 3 – High | 1 – Low | 4 – Very high |

*Scale: 1 (low discrepancy) → 5 (critical discrepancy)*

---

## Gap 2: Cost & Sustainability Gap

### Hypothesis
The financial model of EdTech in SSA places cost burdens on the actors least able to bear them — teachers (personal airtime/data), families (private spend), and governments (underfunded EdTech line items) — while providers rely on donor funding that is structurally fragile.

### Macro Evidence

| Indicator | KEN | RWA | MUS | ZMB | SSA Median |
|---|---|---|---|---|---|
| GDP per capita PPP (current intl $) | 6,650 | 3,785 | **31,697** | 4,221 | 4,221 |
| Gov education spend (% of GDP) | 4.0 | 4.6 | 4.2 | 4.1 | 3.3 |
| Gov education spend (% of gov budget) | **27.9** | 14.2 | 14.2 | 15.4 | 14.9 |
| Primary: qualified teachers (%) | 100.0 | 67.6 | 100.0 | 98.8 | 82.4 |
| Primary: pupils per teacher | 30.7 | 59.5 | 16.2 | 42.1 | 37.1 |
| ICT goods imports (% total imports) | 3.0 | 3.9 | 4.8 | 1.6 | 2.1 |

**Derived:** Approximate annual data cost burden for 1GB/month EdTech use at ~$2/GB as % of monthly GDP/capita:
- **KEN:** ~4.3% of monthly income | **RWA:** ~7.6% | **MUS:** ~0.9% | **ZMB:** ~6.8%

### Key Findings

**2.1 The data-cost burden.** If a teacher or student uses 1GB/month for EdTech — a conservative estimate for regular app use — at a typical SSA mobile data price of ~$2/GB (AfricaChecker / GSMA 2024), this represents **7.6% of a Rwandan's monthly per-capita income** and **6.8% of a Zambian's**. For teachers on government salaries that typically lag GDP/capita, this proportion is likely higher. AoA Teacher Survey item T-B1 asks about non-use barriers including "Cost" — but no item directly asks what teachers personally spend. This is the confirmed instrument gap from Analysis A. The implication for triangulation: provider C4 tells us whether users pay for data; teacher survey cannot yet confirm how much this costs teachers personally relative to salary.

**2.2 Education spending is above-average but structurally constrained.** All four pilot countries allocate 4.0–4.6% of GDP to education (SSA median: 3.3%) — a positive signal. Kenya's 27.9% of government budget is notably high (SSA median: 14.9%). However, per-pupil spending data (SE.XPD.PRIM.PC.ZS) is unavailable for most countries, and the composition of spending matters: if the majority is salaries (typical in SSA), capital and technology budgets are residual and first-to-cut. AoA Expert Consultation item E-B3 probes what happens when donor pilots end — the most common answer in comparable research contexts (EdTech Hub, Frontiers 2026 review) is that programmes stop, not that governments absorb them. Rwanda's 59.5 primary pupils per teacher further signals that capacity constraints are fiscal, not merely technical.

**2.3 Donor dependency as structural fragility.** HolonIQ 2025 Africa EdTech 50 shows 70% D2C models — which are theoretically more sustainable — but a 2022 Briter estimate shows 86% of SSA EdTech investment concentrated in Nigeria, Kenya, South Africa, and Egypt. Rwanda, Zambia, and most of the SSA tail are substantially donor-dependent for EdTech infrastructure. AoA Provider Survey item P-E3 asks directly about product continuity if main funding ends. The Uganda mHealth precedent (23 of 36 projects in 2008–9 never scaled past pilot) and the Frontiers 2026 "pilot graveyard" characterisation of SSA apply directly: without line-item government budget commitment, provider sustainability is contingent on external funding cycles.

**2.4 The missing teacher cost instrument.** The key limitation of Gap 2 triangulation is the instrument gap identified in Analysis A: no AoA survey item asks teachers what they personally spend on data, charging, or devices for work purposes. This should be flagged in the thesis as a recommendation for survey revision in Round 2 or a subsequent study.

### Discrepancy Score Summary (Gap 2)

| Sub-dimension | KEN | RWA | MUS | ZMB |
|---|---|---|---|---|
| G2a: Education spend capacity (% GDP) | 2 – Moderate | 2 – Moderate | 2 – Moderate | 2 – Moderate |
| G2b: Affordability (data cost as % income) | 3 – High | 4 – Very high | 1 – Low | 4 – Very high |
| G2c: Donor dependency risk (macro proxy) | 3 – High | 4 – Very high | 2 – Moderate | 3 – High |

---

## Gap 3: Linguistic Inclusion Gap

### Hypothesis
EdTech tools are predominantly available in European languages (English, French, Portuguese), while actual classroom instruction in SSA pilot countries involves national and local languages for the majority of students — and AI tools perform significantly worse in those languages.

### Macro Evidence & Published Benchmarks

**Supply side (provider language coverage):**
- HolonIQ 2025 Africa EdTech 50: no published systematic language-availability breakdown
- AfroBench (2024): spans 64 African languages across 22 datasets — concludes African languages remain "a significant hurdle for current LLMs"
- IrokoBench: benchmarks 16 African languages; tokenisation inefficiency creates a "token tax" (higher cost, lower accuracy) for African languages
- Published estimate from AoA Synthesis doc: minority of EdTech tools support languages beyond English/French/Portuguese — estimate ~15% (conservative; from EdTech Hub evidence library scan)

**Classroom language reality (per-country, from GEM Spotlight 2024 + EdTech Hub):**

| Country | Est. % instruction in English/French only | National language share | Local/community language share |
|---|---|---|---|
| Kenya | ~30% (English dominant secondary) | ~50% (Kiswahili) | ~20% (community languages) |
| Rwanda | ~25% (English post-2008 switch) | ~65% (Kinyarwanda; dominant early grades) | ~10% |
| Mauritius | ~45% (English/French official) | ~40% (Mauritian Créole) | ~15% |
| Zambia | ~20% (English official) | ~55% (Bemba/Nyanja/Tonga) | ~25% (73 languages total) |

*Note: These are classroom-level approximations synthesised from GEM Spotlight 2024, Trudell (2025), and EdTech Hub 11-country scans. Not nationally representative without AoA Teacher Survey responses.*

**AI model performance relative to English (IrokoBench / AfroBench proxies):**

| Language | Relative LLM performance (English = 100) |
|---|---|
| Kiswahili (KEN/RWA) | ~62 |
| Kinyarwanda (RWA) | ~38 |
| French Créole (MUS proxy) | ~28 |
| Bemba/Nyanja (ZMB) | ~18 |
| Average African language (AfroBench) | ~35 |

### Key Findings

**3.1 The 15% vs. 70–80% gap.** Approximately 70–80% of classroom instruction in three of the four pilot countries (KEN, RWA, ZMB) occurs in non-European languages, yet published evidence suggests fewer than ~15% of EdTech tools available in SSA support those languages in any meaningful way. This is the most structurally dramatic of the three gaps. The AoA Teacher Survey items T-A4 (language of instruction) and T-E4 (AI performance in local languages) will be critical for ground-truthing this estimate once survey responses are received.

**3.2 Rwanda's specific linguistic tension.** Rwanda made a deliberate switch from French to English as the medium of instruction in 2008. But Kinyarwanda remains the language most Rwandan children actually think and speak in, particularly in early grades. LLM performance in Kinyarwanda is approximately 38% of English performance (IrokoBench). AI tutors or chatbot tools deployed in Rwanda in English are therefore doubly misaligned: they use a language students are still acquiring, and AI assistance in Kinyarwanda is significantly degraded.

**3.3 Zambia's linguistic fragmentation.** Zambia has 73 recognised languages; the four dominant lingua francas (Bemba, Nyanja, Tonga, Lozi) serve different regions. Even a well-resourced EdTech provider targeting Zambia faces a content localisation cost that is at least 4–5× what is required for a linguistically homogeneous market. LLM performance in Bemba/Nyanja is approximately 18% of English — the lowest among the four pilot countries.

**3.4 The AI token tax.** AfroBench's finding on tokenisation inefficiency is a structural barrier with economic implications: because current LLMs tokenise African languages inefficiently (more tokens per word), running AI in Kinyarwanda or Bemba costs 2–4× more per inference than English. For providers serving price-sensitive markets on thin margins, this creates a commercial disincentive to African-language AI — compounding the linguistic exclusion gap.

**3.5 Mauritius as partial exception.** Mauritius's dominant classroom language is Mauritian Créole, which has no close LLM equivalent and relatively low benchmark scores. However, Mauritius's higher income level (GDP/capita PPP: $31,697) and fully English/French-literate teaching workforce means teacher-mediated translation partially offsets this gap in practice. Language remains a challenge but is less acute than in the other three pilot countries.

### Discrepancy Score Summary (Gap 3)

| Sub-dimension | KEN | RWA | MUS | ZMB |
|---|---|---|---|---|
| G3a: Tool language coverage gap | 4 – Very high | 4 – Very high | 3 – High | 5 – Critical |
| G3b: AI performance in classroom languages | 3 – High | 4 – Very high | 4 – Very high | 5 – Critical |
| G3c: Curriculum-language alignment risk | 3 – High | 3 – High | 3 – High | 4 – Very high |

---

## Master Discrepancy Matrix

| Dimension | KEN | RWA | MUS | ZMB |
|---|---|---|---|---|
| G1a: Internet access gap | 2 Moderate | 3 High | 1 Low | 4 Very high |
| G1b: Rural electricity vs. broadband need | 3 High | 3 High | 1 Low | **5 Critical** |
| G1c: School connectivity vs. pop internet | 2 Moderate | 3 High | 1 Low | 4 Very high |
| G2a: Education spend capacity | 2 Moderate | 2 Moderate | 2 Moderate | 2 Moderate |
| G2b: Affordability (data cost / income) | 3 High | 4 Very high | 1 Low | 4 Very high |
| G2c: Donor dependency risk | 3 High | 4 Very high | 2 Moderate | 3 High |
| G3a: Tool language coverage gap | 4 Very high | 4 Very high | 3 High | **5 Critical** |
| G3b: AI performance in classroom languages | 3 High | 4 Very high | 4 Very high | **5 Critical** |
| G3c: Curriculum-language alignment risk | 3 High | 3 High | 3 High | 4 Very high |
| **Country composite** | **25 / 45** | **30 / 45** | **18 / 45** | **37 / 45** |

*Scale: 1 (low) → 5 (critical). Max possible: 45.*

### Country Profiles Summary

**Mauritius (MUS):** Lowest composite discrepancy (18/45). Infrastructure near-complete; high income offsets data cost burden; language gap exists but is partially mediated by high teacher literacy. Functions as a *control* / upper-bound case for the SSA pilot.

**Kenya (KEN):** Moderate composite (25/45). Silicon Savannah positioning, high teacher qualification rates, and above-SSA-average internet access give KEN relative advantages. Language gap is the main structural risk, particularly for Kiswahili-medium instruction contexts.

**Rwanda (RWA):** High composite (30/45). State-led digital push (Smart Rwanda) and strong data governance scores contrast with low broadband, heavy donor dependency, and the acute Kinyarwanda AI performance gap. The linguistic-policy tension (English mandate / Kinyarwanda reality) is the thesis's most analytically rich case.

**Zambia (ZMB):** Highest composite discrepancy (37/45). Rural electricity at 31.3%, broadband near-zero, 73 languages, and the worst AI language performance scores among the pilot countries. ZMB represents the *lower-bound* SSA case — the context where all three gaps are simultaneously most severe.

---

## Analytical Implications for Thesis

### 1. The Triangulation Argument
The three-gap framework demonstrates that EdTech cannot be evaluated on a single axis (e.g., "does the tool work?"). A tool that works in Mauritius may fail on all three dimensions in Zambia — not because the tool is bad, but because the structural conditions differ. This supports the thesis's central claim that systemic, multi-stakeholder analysis is required.

### 2. Cyclical Causality (Wicked Problem Framing)
The gaps are not independent:
- Low connectivity → limited data on learning outcomes → harder to build evidence-based EdTech → solutions designed without local context → tools that don't fit → low adoption → limited data
- This data-scarcity ↔ solution-scarcity feedback loop was identified in the user's original pointers as a defining feature of EdTech in SSA as a *wicked problem*. The discrepancy matrix quantifies where in this loop the structural breaks are sharpest.

### 3. The Instrument Gap Limitation
As flagged in Analysis A, the absence of a teacher-side personal cost item means Gap 2's teacher cost burden dimension can only be *inferred* from macro GDP/capita data, not directly measured. This is a legitimate thesis limitation and grounds a recommendation for survey revision.

### 4. EEA_3 Calibration Implications (Preview for Analysis C)
The matrix provides concrete calibration targets:
- Electricity distribution for rural schools: draw from country-specific rural electricity % (31–67% range across pilot countries), not a single SSA-average
- Internet access: bimodal (urban: 80–98%; rural: 17–67%)
- Teacher data cost burden: modelled as proportion of monthly income (4–8% for non-MUS countries)
- AI language performance: tiered degradation factor by language (18–62% relative to English baseline)

---

## Figures

1. `gap1_connectivity_assumption.png` — Internet + electricity + broadband by country
2. `gap2_cost_sustainability.png` — Education spend + affordability by country
3. `gap3_linguistic_inclusion.png` — Classroom language reality + AI performance
4. `master_discrepancy_matrix.png` — Heatmap, all 9 sub-dimensions × 4 countries

---

*Analysis B is an original analytical synthesis by the thesis author. Country macro data from World Bank WDI (2024). Language and AI performance figures are approximations derived from published benchmarks (IrokoBench, AfroBench, GEM Spotlight 2024, EdTech Hub) — they will be superseded by AoA survey responses when available. All caveats noted.*
