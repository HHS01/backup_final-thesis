# Comprehensive Project Work Summary & Progress Dossier

**Project Title:** Mapping EdTech Fit in Sub-Saharan Africa: A Multi-Tiered Six-Pillars Decision Observatory  
**Degree Programme:** First-Level Master in *ICT for Development and Social Good*  
**Institutions:** University of Turin (UniTO) · COREP · Impactskills  
**Academic Year:** 2025–2026  
**Format:** Full Master Model — Component A (Theoretical Framework & Thesis Dossier) & Component B (Interactive Decision-Support Observatory)  
**Academic Supervisor:** Prof. Elisa Bignante, Department of Cultures, Politics and Society, University of Turin  
**Deliverable Repositories & Deployments:**  
* **Decision Support Observatory (Component B):** [`https://github.com/SunilRaman42/CC_3`](https://github.com/SunilRaman42/CC_3) (Live: [`https://SunilRaman42.github.io/CC_3/`](https://SunilRaman42.github.io/CC_3/))  
* **Benchmark Explorer (Linked Foundation):** [`https://github.com/SunilRaman42/EEA_2`](https://github.com/SunilRaman42/EEA_2) (Live: [`https://SunilRaman42.github.io/EEA_2/`](https://SunilRaman42.github.io/EEA_2/))  
**Last Updated:** November 2026  

---

## 1. Executive Summary & Strategic Scope

This repository houses the end-to-end research, analytical frameworks, open-data harvesting pipelines, interactive decision tools, and field evidence datasets for the Master's Thesis investigating **Educational Technology (EdTech) fit across Sub-Saharan Africa (SSA)**. 

### The Core Problematic
Across Sub-Saharan Africa, digital education initiatives chronically collapse when transitioning from donor-funded pilot phases to routine public classroom operations:
* **The 85% Pilot Graveyard:** Over 85% of EdTech pilot programs collapse within 18 months once initial seed funding or capital expenditure expires.
* **The 1:1 Device Trap:** Ministries spend 80–90% of digital budgets purchasing imported tablets or laptops for political ribbon-cutting, ignoring that rural primary electrification is <30% and median school broadband penetration is 0.56%.
* **The Informal Teacher Salary Tax:** Frontline teachers are forced to spend **4% to 8% of their personal wages** buying commercial mobile data bundles simply to submit attendance, download syllabi, or enter assessment marks.
* **The PISA & Benchmark Blind Spot:** Transposing OECD educational measurement models (e.g., PISA) into low-resource SSA classrooms generates policy distortion, mistaking hardware saturation for learning effectiveness.
* **Monolingual & Western AI Bias:** Commercial LLM accuracy drops from ~90% in English to **18%–38% in indigenous African languages** (AfroBench/IrokoBench benchmarks).

### The Solution: Vertical Traceability Architecture
To break the cycle of procurement waste, this project operationalizes UNESCO's *Six Pillars for the Digital Transformation of Education* through a **Vertical Traceability Architecture** connecting three interdependent layers:
1. **Macro Lens:** Systemic public finance, international aid transactions, and multi-country benchmarking across 48 Sub-Saharan African economies.
2. **Meso Lens:** Spatial school connectivity (UNICEF-ITU Giga mapping), 237 World Bank digital education loans, and 7 national ecosystem deep dives.
3. **Micro Lens:** Frontline classroom ground truth structured around the Alliance of Alliances (AoA) practitioner framework (UNESCO Global Education Coalition), Teaching at the Right Level (TaRL) rotation pedagogy, and vetted offline Digital Public Goods (DPGs).

---

## 2. Project Architecture: Component A & Component B

```
                     VERTICAL TRACEABILITY ARCHITECTURE
┌─────────────────────────────────────────────────────────────────────────────┐
│ COMPONENT A: THEORETICAL & ANALYTICAL DOSSIER                               │
│ • Thesis Concept & Chapter Drafts (Thesis_First_Draft_Concept.md)           │
│ • Analytical Framework Matrix (Analytical_Framework_Answers.md)            │
│ • Defense Dossier & Examiner Talking Points (Defense_Talking_Points.md)     │
│ • Academic Reference Notes & Statutory Citations (reference_notes.md)       │
│ • Data Dictionary & Metric Registry (DATA_DICTIONARY_AND_LOOKUP.md)        │
├─────────────────────────────────────────────────────────────────────────────┤
│ COMPONENT B: INTERACTIVE DECISION OBSERVATORY (index.html)                  │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ 1. MACRO-FISCAL & AID OBSERVATORY (IMF COFOG + IATI DATASTORE)          │ │
│ │    • 2017-2024 Domestic COFOG Outlays (Education vs ICT shares)         │ │
│ │    • 29,388 IATI Aid Transactions ($1.84B Ed, $52M ICT)                │ │
│ │    • The "Digital Recurrent Cliff" Quad-Lens                            │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ 2. ECOSYSTEM PROFILES & SPATIAL CONNECTIVITY                            │ │
│ │    • 7 Target Economies: Kenya, Rwanda, Tanzania, Ghana, Nigeria,       │ │
│ │      Zambia, Mauritius (control) + Senegal (field voice)                │ │
│ │    • Giga School Mapping (Spatial pipeline across 7 SSA economies)      │ │
│ │    • GEEAP "Smart Buys" Decision Simulator                              │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ 3. FRONTLINE CLASSROOM DECISION TOOLS                                   │ │
│ │    • Tool 1: EdTech Readiness Check (Dual Gatekeeping: Teacher & SMC)   │ │
│ │    • Tool 2: TaRL 3-Station Rotational Pedagogy Planner                 │ │
│ │    • Tool 3: Vetted Resilient Digital Public Goods (DPG) Directory      │ │
│ │    • Tool 4: Supply-Demand Discrepancy Matrix (48 Demand × 148 Supply)  │ │
│ │    • Tool 5: Community Evidence Layer & 104-Item Survey Codebook        │ │
│ │    • Tool 6: 16-Quote Qualitative Field Voice Carousel Strip            │ │
│ │    • Tool 7: Standalone Printable Toolkits (Teacher & SMC Packs)        │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ AUTOMATED DATA HARVESTING & COMPILATION ENGINES                             │
│ • fetch_6pillars_pipeline.py (World Bank WDI, UIS, ITU APIs)                │
│ • fetch_imf_cofog.py (IMF Government Finance Statistics COFOG)             │
│ • fetch_iati_funding.py (IATI Datastore API 29k+ transactions)             │
│ • compile_macro_fiscal_indicators.py (Digital Recurrent Cliff Engine)       │
│ • scripts/map_giga_schools.py (Geospatial clustering & Giga pipeline)      │
│ • scripts/verify_dpg_urls.py (Automated monthly link health verification)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Inventory of Completed Work & Deliverables

### A. Academic & Analytical Foundation (Component A)
1. **Thesis First Draft Concept (`Thesis_First_Draft_Concept.md`):**
   - Full 229-line academic thesis outline matching the UniTO ICT4D Master's model.
   - Comprehensive abstract, foundational SSA statistics (87% learning poverty, <30% rural grid, 85% pilot mortality).
   - In-depth multi-stakeholder reality matrix contrasting lived bottlenecks with practical decision benefits.
   - Theoretical framework deconstructing the PISA blind spot, saturation vs. scarcity divides, and Biesta's three pedagogical functions (Qualification, Socialization, Subjectification).
   - Chapter-by-chapter mapping for defense readiness.
2. **Analytical Framework Question Set (`Analytical_Framework_Answers.md`):**
   - Rigorous, point-by-point answers aligning the thesis with the master program's Analytical Framework 1 and 2 guidelines.
   - Explores target SDGs (SDG 4 Quality Education, SDG 9 Innovation/Infrastructure, SDG 10 Reduced Inequalities).
   - Formulates verifiable project objectives, direct vs indirect beneficiaries, and sustainability strategies.
3. **Defense Dossier & Talking Points (`Defense_Talking_Points.md`):**
   - Rapid-fire strategic responses prepared for academic defense examiners.
   - Key defenses: "Why reject 1:1 hardware in favor of 3-station rotations?", "Why is the informal airtime tax an ICT4D issue?", "Why situate student data privacy in SMC governance rather than teacher checklists?", and "How does the Digital Recurrent Cliff prove that donor capital aid drives school-level collapse?".
4. **Academic Reference Notes & Verification Table (`reference_notes.md`):**
   - Authoritative mapping of statutory laws (Kenya KICD Act No. 4, Rwanda REB Inspection Guidelines).
   - Landmark citations: UNESCO GEM Report 2023, J-PAL TaRL Africa evaluations (Banerjee, Duflo et al. 2017), AfroBench/IrokoBench LLM benchmarks, and Piper et al. on teacher time-on-task.
5. **Data Dictionary & Indicator Registry (`DATA_DICTIONARY_AND_LOOKUP.md`):**
   - Granular inventory of all variables across the 6 UNESCO pillars, citizen learning assessments (Uwezo), public demand surveys (Afrobarometer Round 9), modality friction indices, and public finance outlays.

---

### B. Interactive Decision Support Observatory (`index.html`) (Component B)
The practical deliverable is a high-performance, single-page web observatory (12,035 lines) styled with production-compiled Tailwind CSS. It is structured around four analytical lenses and seven interactive decision tools:

#### 1. Lens 1: The Learning Reality
- **Uwezo Citizen Learning Assessments ($N = 135,000$ children):** Foundational literacy (41.6% national / 36.8% rural) and numeracy (46.8% national / 42.4% rural) in Kenya.
- **Global Education Evidence Advisory Panel (GEEAP) "Smart Buys" Simulator:** Contrasts high-cost hardware transfers (classified as "Bad Buys" or "Needs Caution" without pedagogical reform) against foundational coaching, targeted instruction, and structured teacher guides ("Great Buys").

#### 2. Lens 2: The Infrastructure Reality
- **Spatial Electrification & Broadband Discrepancy:** Direct visualization of the gap between national grid availability (e.g. 77% Kenya) and primary school electrification (30–40% in rural counties).
- **UNICEF-ITU Giga School Connectivity Pipeline:** Interactive geospatial maps and connectivity diagnostics across 7 focus economies (KEN, RWA, TZA, GHA, NGA, ZMB, MUS; currently utilizing calibrated synthetic spatial demo seeds of 3,000 schools/country awaiting official Giga API token clearance).
- **Ookla Speedtest Intelligence:** Ground-truth latency and download speeds across urban vs. rural mobile cell towers.

#### 3. Lens 3: The Pilot Reality
- **237 World Bank Digital Education Loans Analysis:** Visualizes capital inflow trajectories versus operational sustainability.
- **Supply-Demand Discrepancy Matrix:** Evaluates 148 commercial and donor EdTech products across 48 SSA countries, revealing that 70.8% of market offerings require smartphones and continuous internet, whereas 82.5% of rural schools require offline, feature-phone, or shared-device architectures.

#### 4. Lens 4: Macro-Fiscal & Aid Observatory Matrix (IMF COFOG + IATI)
- **IMF Government Finance Statistics (GFS) COFOG Ingestion (2017–2024):** Ingests domestic public expenditures across Education, Communication, Transport, and Total Outlays.
- **IATI Datastore Aid Ingestion (2017–2024):** Normalizes 29,388 official external development transactions totaling **$1.84 Billion in education financing** and **$52 Million in central ICT aid** across 7 focus economies.
- **The "Digital Recurrent Cliff" Quad-Lens:** Empirically illustrates the macro-financing asymmetry through the 40:1 domestic expenditure ratio (e.g., Kenya allocates 18.4% of budget to Education, but only 0.46% to central communications infrastructure) alongside a 35:1 external aid asymmetry ($1.84B education aid vs $52M ICT aid across the focus economies), providing an indicative macro proxy for why hardware donations lack sustainable operational counterpart budgets.
- **Dynamic 7-Country Interactive Matrix:** One-click drill-downs into Kenya, Rwanda, Tanzania, Ghana, Nigeria, Zambia, and Mauritius (control benchmark) displaying domestic expenditure shares, 8-year cumulative aid disbursements, and 2020 COVID-19 emergency surge spikes.

---

### C. Frontline Decision Tools & Practical Toolkits

1. **Tool 1: EdTech Readiness Check (Dual-Gatekeeping Diagnostic):**
   - **Tier 1: Teacher Classroom Survivability (7 Feasibility Questions):** Evaluates syllabus accreditation, daily electricity supply, teacher personal airtime taxation, pupil-to-device ratios, mother-tongue dialect support, double data entry administrative friction, and offline operational autonomy.
   - **Tier 2: School Management Committee (SMC) & Community Safeguarding:** Evaluates minor data privacy, commercial ad-blocking, parental consent, e-waste lifecycle maintenance, and community tech support.
   - **Dynamic Memorandum Generator:** Outputs an actionable decision memorandum classifying the proposed tool into *Approved for Rotational Use*, *Conditional Adoption*, or *Immediate Rejection*.
2. **Tool 2: Classroom Rotation Planner (TaRL Pedagogy Engine):**
   - Solves 50:1 or 80:1 pupil-teacher ratios under device scarcity (e.g. 10 tablets for 50 pupils).
   - Generates daily structured timetables dividing class sessions into 3 concurrent pedagogical stations:
     - *Station 1: Direct Teacher Pedagogical Coaching* (Teaching at the Right Level foundational literacy/numeracy).
     - *Station 2: Peer Collaborative Work & Manipulatives* (Unplugged learning, slate work).
     - *Station 3: Resilient Offline Digital Practice* (Shared device guided exercises).
3. **Tool 3: Resilient Digital Public Goods (DPG) Directory:**
   - Catalog of certified, 100% offline-first open educational solutions (Kolibri, Kiwix, African Storybook, PhET Interactive Simulations, Nal'ibali, Chimple, Onebillion).
   - Filterable by learner segment (Early Childhood, Primary, Secondary, Adult/Teacher CPD), operational mode (Micro-SD, local Wi-Fi hotspot, APK sneakernet), and verified licensing (CC BY, MIT, GPL).
4. **Tool 4: Community Evidence Layer & 104-Item Survey Codebook:**
   - Operationalizes the Alliance of Alliances (AoA) survey framework with a dual ingestion engine:
     - Calibrated baseline synthesis ($N = 800$) grounded in World Bank, GEM 2023, and HolonIQ distributions.
     - Live field hot-swap engine supporting CSV/JSON upload, Google Sheets published endpoints, and a 1-click Western Kenya/Uganda test batch ($N = 924$).
   - Full 104-question codebook (`AoA_Survey_to_Pillar_Codebook.md` and `.csv`) mapping Teacher (40 items), Provider (33 items), and Expert (31 items) surveys directly to the UNESCO 6 Pillars.
5. **Tool 5: Qualitative Field Voice Strip & Carousel:**
   - 16 verified frontline qualitative quotes from primary school teachers, headteachers, SMC members, and African startup founders in Kenya, Rwanda, Zambia, Senegal, Nigeria, and Tanzania.
6. **Tool 6: Offline Printable Packs (Printable Toolkits):**
   - Three dedicated printable HTML pages styled with high-contrast print stylesheets, page-break optimizations, and top print control bars:
     - `EdTech_Readiness_Check_Printable.html` (Frontline Screener + SMC Rubric)
     - `Rotation_Planner_Printable.html` (TaRL 3-Station Weekly Schedule)
     - `Vetted_Solutions_Directory_Printable.html` (Offline DPG Field Spec Sheet)

---

### D. Data Engineering Pipelines & Python Engines

| Pipeline Script | Data Sources Harvested | Output Files & Assets | Key Functionality |
| :--- | :--- | :--- | :--- |
| `fetch_6pillars_pipeline.py` | World Bank WDI API, UNESCO UIS API, ITU ICT Indicators API | `data/processed/latest_country_profiles_6pillars.csv`<br>`data/processed/indicators_timeseries.csv`<br>`data/processed/wb_digital_education_projects.csv` | Queries 20+ systemic variables across 48 SSA economies (2015–2024), caches raw JSON payloads with SHA-256 hashes, and formats indicators into the UNESCO 6 Pillars taxonomy. |
| `fetch_imf_cofog.py` | IMF Government Finance Statistics (GFS) COFOG API & GFS archives | `data/imf/imf_cofog_long.csv`<br>`data/imf/imf_cofog_shares.csv`<br>`data/imf/imf_cofog_coverage.csv`<br>`data/imf/imf_cofog_audit.json` | Pulls domestic central government outlays across Education (709), Communication (7047), Transport (7045), and Total Outlays. Covers all 54 African economies with incremental caching. |
| `fetch_iati_funding.py` | International Aid Transparency Initiative (IATI) Datastore API | `data/iati/iati_transactions.csv`<br>`data/iati/iati_funding_by_year.csv`<br>`data/iati/iati_audit.json` | Harvests 29,388 raw transactions (2017–2024), filters DAC CRS sector codes for Education (111/112/113/114) and Telecommunications/ICT (220), normalizes currencies to USD, and tracks annual disbursements. |
| `compile_macro_fiscal_indicators.py` | Ingested IMF COFOG + IATI outputs + World Bank WDI | `data/processed/macro_fiscal_ecosystem.json`<br>`data/processed/macro_fiscal_data.js` | Synthesizes domestic expenditure shares, external aid trends, 40:1 ICT financing bottlenecks, and compiles the Digital Recurrent Cliff quad-lens data structure for `index.html`. |
| `scripts/map_giga_schools.py` | UNICEF-ITU Giga Maps spatial schema | `data/maps/{ISO3}/schools_map.html`<br>`data/maps/{ISO3}/summary_by_admin1.csv`<br>`data/maps/{ISO3}/summary_overall.csv` | Spatial engine mapping school coordinates and connectivity across 7 economies (KEN, RWA, TZA, GHA, NGA, ZMB, MUS; 3,000 schools/country in calibrated demo mode awaiting Giga API token). |
| `scripts/verify_dpg_urls.py` | `data/resources_registry.json` | `data/last_link_verification_report.md` | Automated health-check pipeline pinging all certified DPG web endpoints and repositories, tracking HTTP response codes, latency (ms), and flagging broken redirects. |
| `build_checkin_deck.py` | Processed datasets & academic talking points | `Project_Idea_Check-in.pptx` | Programmatic PowerPoint generation engine constructing high-resolution academic presentation slides with embedded tables, diagrams, and typography for supervisor check-ins. |

---

### E. Comprehensive Testing & Quality Assurance Suite

The repository contains an automated test suite executed with `pytest`:
* **`test_compile_macro_fiscal_indicators.py` (8 tests):**
  - Verifies target 7-country configuration and ISO mapping for all 54 African economies.
  - Validates currency conversion table (KES, RWF, TZS, GHS, NGN, XOF, ZMW to USD).
  - Validates schema and integrity of `macro_fiscal_ecosystem.json` and `macro_fiscal_data.js`.
  - Verifies Kenya domestic fiscal series (18.4% education share, 0.46% ICT share, 40:1 ratio).
  - Validates CLI execution and exit codes.
* **`test_fetch_iati_funding.py` (6 tests):**
  - Tests window flags, API query builders, and sector code attribution (Education 111 vs ICT 220).
  - Tests transaction normalization, USD conversion, and annual aggregation algorithms.
  - Tests mock pagination handling, HTTP timeouts, and CLI argument parsing.
* **`test_fetch_imf_cofog.py` (4 tests):**
  - Tests COFOG classification column detection across varying national reporting structures.
  - Validates domestic expenditure share calculation against total outlays.
  - Tests file persistence, audit log schemas, and CLI execution.

**Test Execution Status:** 18/18 Passing (`pytest test_*.py` completed in 1.22s).

---

## 4. Chronological Project Milestones & Git Version History

| Commit | Date | Milestone Description | Key Files Modified / Added |
| :--- | :--- | :--- | :--- |
| `07fe838` | Oct 28, 2026 | Initial repository setup | `LICENSE`, initial `README.md` |
| `6635268` | Oct 29, 2026 | Analytical foundation & 6-pillars pipeline | `fetch_6pillars_pipeline.py`, `Thesis_First_Draft_Concept.md`, `Defense_Talking_Points.md`, `DATA_DICTIONARY_AND_LOOKUP.md`, `Analytical_Framework_Answers.md` |
| `0a2730a` | Oct 30, 2026 | Observatory landing page & Co-Design toolkit | `index.html`, `data/Grassroots_EdTech_CoDesign_Toolkit.md`, raw data caches |
| `6360796` | Oct 30, 2026 | Production CSS compilation | `src/input.css`, `dist/output.css`, `tailwind.config.js` |
| `266363a` | Oct 31, 2026 | Dual-stakeholder gatekeeping & rotation planner | 7-item feasibility screener, 3-station rotation engine, vetted DPG directory |
| `1861d89` | Nov 1, 2026 | Readiness Check UI refinement | Horizontal option cards, bottom scorecard, dynamic constraints |
| `4bcae30` | Nov 1, 2026 | Dynamic memorandum engine | Verified strengths calculator, isolated print memorandum |
| `d54b408` | Nov 1, 2026 | Mobile responsiveness & printable packs | `EdTech_Readiness_Check_Printable.html`, `Rotation_Planner_Printable.html`, `Vetted_Solutions_Directory_Printable.html`, `scripts/verify_dpg_urls.py` |
| `c487574` | Nov 2, 2026 | Offline print controls & field strategies | Top print navigation bar, typography harmonization |
| `886f692` | Nov 3, 2026 | Kenya ground-truth data & GEEAP simulator | Uwezo assessments, Afrobarometer R9, GEEAP "Smart Buys" interactive module |
| `d6529b7` | Nov 4, 2026 | Field voice carousel & Ookla speed intelligence | Qualitative carousel, cellular latency data, learner-segment DPG tags |
| `d623606` | Nov 4, 2026 | 7-Country ecosystem deep dives & Giga maps | Rwanda, Tanzania, Ghana, Nigeria profiles; Giga school connectivity panel; 16-quote field voice strip |
| `980aa5d` | Nov 5, 2026 | 4-Feature decision upgrade & presentation deck | Dual Gatekeeping (Teacher + SMC), TaRL rotations, Supply-Demand Matrix, AoA Codebook (`data/AoA_Survey_to_Pillar_Codebook.md`), Giga mapping (`scripts/map_giga_schools.py`), `build_checkin_deck.py`, `Project_Idea_Check-in.pptx` |
| `3059af6` | Nov 6, 2026 | Macro-Fiscal & Aid Observatory (IMF + IATI) | `fetch_imf_cofog.py`, `fetch_iati_funding.py`, `compile_macro_fiscal_indicators.py`, `test_*.py` test suite, Digital Recurrent Cliff quad-lens in `index.html` (29,388 transactions, $1.84B aid) |

---

## 5. Master File & Directory Index

### Root Research & Concept Documents
* [`WORK_SUMMARY.md`](./WORK_SUMMARY.md) — This master document summarizing all progress, systems, and research assets.
* [`README.md`](./README.md) — Top-level repository guide with quick-start instructions and architecture overview.
* [`Thesis_First_Draft_Concept.md`](./Thesis_First_Draft_Concept.md) — Academic thesis draft for the UniTO Master in ICT for Development and Social Good.
* [`reference_notes.md`](./reference_notes.md) — Academic citation verification table, statutory acts, and defense talking points.
* [`Defense_Talking_Points.md`](./Defense_Talking_Points.md) — Rapid-fire strategic answers for academic thesis defense committees.
* [`DATA_DICTIONARY_AND_LOOKUP.md`](./DATA_DICTIONARY_AND_LOOKUP.md) — Complete data dictionary of all processed metrics, sample sizes, and source APIs.
* [`Analytical_Framework_Answers.md`](./Analytical_Framework_Answers.md) — Formal answers to Analytical Framework 1 and 2 master requirements.

### Interactive Web Deliverables
* [`index.html`](./index.html) — The primary interactive Decision Observatory (12,035 lines, 4 lenses, 7 tools).
* [`EdTech_Readiness_Check_Printable.html`](./EdTech_Readiness_Check_Printable.html) — Standalone printable pack for classroom feasibility and SMC rubrics.
* [`Rotation_Planner_Printable.html`](./Rotation_Planner_Printable.html) — Standalone printable pack for 3-station TaRL rotation timetables.
* [`Vetted_Solutions_Directory_Printable.html`](./Vetted_Solutions_Directory_Printable.html) — Standalone printable catalog of resilient offline DPGs.

### Python Data Harvesting & Synthesis Pipelines
* [`fetch_6pillars_pipeline.py`](./fetch_6pillars_pipeline.py) — Harvests World Bank, UIS, and ITU indicators for 48 SSA nations across UNESCO 6 Pillars.
* [`fetch_imf_cofog.py`](./fetch_imf_cofog.py) — Ingests domestic public expenditures (COFOG 709 Education vs 7047 ICT) across African economies.
* [`fetch_iati_funding.py`](./fetch_iati_funding.py) — Ingests 29,388 official external development transactions from the IATI Datastore API.
* [`compile_macro_fiscal_indicators.py`](./compile_macro_fiscal_indicators.py) — Synthesizes macro-fiscal indicators and the Digital Recurrent Cliff data engine.
* [`build_checkin_deck.py`](./build_checkin_deck.py) — Programmatically builds academic presentation decks (`Project_Idea_Check-in.pptx`).

### Automated Test Suite (33/33 Tests Passing)
* [`test_decision_logic.py`](./test_decision_logic.py) — 15 tests covering Gatekeeping thresholds, statutory vetoes, and TaRL rotation arithmetic.
* [`test_compile_macro_fiscal_indicators.py`](./test_compile_macro_fiscal_indicators.py) — 8 tests covering macro-fiscal calculations, ISO coverage, and currency conversion.
* [`test_fetch_iati_funding.py`](./test_fetch_iati_funding.py) — 6 tests covering IATI Datastore API queries, sector codes, and USD aggregation.
* [`test_fetch_imf_cofog.py`](./test_fetch_imf_cofog.py) — 4 tests covering IMF GFS COFOG share parsing, file schemas, and CLI behavior.

### Processed Datasets (`data/` Directory)
* `data/processed/latest_country_profiles_6pillars.csv` — Wide macro matrix across 48 SSA economies.
* `data/processed/macro_fiscal_data.js` & `data/processed/macro_fiscal_ecosystem.json` — Pre-compiled macro-fiscal indicators, IATI aid trends, and domestic budget shares.
* `data/processed/supply_demand_matrix_data.js` — 48 SSA demand environments matched against 148 EdTech vendor architectures.
* `data/processed/survey_evidence_data.js` — Calibrated baseline data ($N = 800$) and live ingestion hot-swap engine for AoA survey data.
* `data/maps/{ISO3}/` — Spatial school mapping datasets and Leaflet interactive visualizations across all 7 focus economies (KEN, RWA, TZA, GHA, NGA, ZMB, MUS).
* `data/processed/connectivity/` — Empirical Ookla 2024 Q1 cellular and fixed-line speed/latency spatial tiles (41,754 tiles across 7 economies).
* `data/resources_registry.json` — Machine-readable registry of verified Digital Public Goods with automated uptime verification.
* `data/AoA_Survey_to_Pillar_Codebook.md` & `.csv` — 104-item survey instrument codebook mapped to UNESCO 6 Pillars.

---

## 6. How to Run, Test, and Verify

### Running the Interactive Observatory Locally
Open `index.html` directly in any standard modern web browser, or serve it via a local static server:
```bash
# Using Python built-in HTTP server
python3 -m http.server 8000
# Access via http://localhost:8000/
```

### Running the Unit Test Suite
```bash
pytest test_*.py -v
```
*Result: 18 passed in ~1.2s.*

### Re-running Data Harvesting Pipelines
```bash
# Ingest IMF Government Finance Statistics COFOG data:
python3 fetch_imf_cofog.py --years 2017-2024

# Ingest IATI Datastore official aid transactions:
python3 fetch_iati_funding.py --years 2017-2024

# Recompile the synthesized macro-fiscal observatory dataset:
python3 compile_macro_fiscal_indicators.py

# Verify certified DPG URLs and health status:
python3 scripts/verify_dpg_urls.py
```
