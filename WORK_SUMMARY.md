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

This repository houses the end-to-end research, analytical frameworks, open-data harvesting pipelines, subnational geospatial datasets, interactive decision tools, and field evidence assets for the Master's Thesis investigating **Educational Technology (EdTech) fit across Sub-Saharan Africa (SSA)**.

### The Core Problematic
Across Sub-Saharan Africa, digital education initiatives chronically collapse when transitioning from donor-funded pilot phases to routine public classroom operations:
* **The 85% Pilot Graveyard:** Over 85% of EdTech pilot programs collapse within 18 months once initial seed funding or capital grant expenditure terminates.
* **The 1:1 Device Trap:** Ministries spend 80%–90% of digital education budgets purchasing imported tablets or laptops for political ribbon-cutting, ignoring that rural primary electrification is <30% and median school broadband penetration is 0.56%.
* **The Informal Teacher Salary Tax:** Frontline teachers are forced to expend **4% to 8% of their personal wages** purchasing commercial cellular data bundles simply to submit attendance, download syllabi, or enter assessment marks.
* **The PISA & Benchmark Blind Spot:** Transposing OECD educational measurement models into low-resource SSA classrooms generates policy distortion, mistaking hardware procurement saturation for pedagogical learning effectiveness.
* **Monolingual & Western AI Bias:** Commercial LLM accuracy drops from ~90% in English to **18%–38% in indigenous African languages** (AfroBench/IrokoBench benchmarks), imposing an extractive "token tax" on African vernacular queries.
* **Subnational Bandwidth Inequalities:** National connectivity averages conceal acute Admin-1 regional disparities, where secondary cities and rural provinces experience QoS latency spikes >300 ms and median throughput <2 Mbps.

### The Solution: Vertical Traceability Architecture
To break the cycle of procurement waste, this project operationalizes UNESCO's *Six Pillars for the Digital Transformation of Education* through a **Vertical Traceability Architecture** connecting three interdependent operational layers:
1. **Macro Lens:** Systemic public finance (IMF GFS COFOG), official development assistance (IATI Datastore), and open-data macro indicators (World Bank WDI, UNESCO UIS, ITU) across 48 Sub-Saharan African economies.
2. **Meso Lens:** Subnational infrastructure quality of service (M-Lab NDT Admin-1 speed/latency digest with 3/6/12m change detection), geospatial schoolhouse connectivity (UNICEF-ITU Giga maps spatial pipeline across 21,000 schools), cellular coverage (41,754 Ookla 2024Q1 spatial tiles), and 237 World Bank digital education investment projects.
3. **Micro Lens:** Frontline classroom ground truth structured around the Alliance of Alliances (AoA) practitioner framework (UNESCO Global Education Coalition), privacy-gated KoboToolbox field survey pipelines, Citizen-Led Assessments (Uwezo Kenya & Tanzania, $N = 243,000$), citizen voice panels (Afrobarometer R9 & R10, $N = 22,369$), Teaching at the Right Level (TaRL) 3-station rotation pedagogy, and vetted offline Digital Public Goods (DPGs).

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
│ • Kobo Pipeline Security & Privacy Boundary Log (KOBO_PIPELINE_CHANGELOG.md)│
├─────────────────────────────────────────────────────────────────────────────┤
│ COMPONENT B: INTERACTIVE DECISION OBSERVATORY (index.html)                  │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ 1. MACRO-FISCAL & AID OBSERVATORY (IMF COFOG + IATI DATASTORE)          │ │
│ │    • 2017-2024 Domestic COFOG Outlays (Education vs ICT shares)         │ │
│ │    • 29,388 IATI Aid Transactions ($1.84B Ed vs $52M ICT aid)           │ │
│ │    • The "Digital Recurrent Cliff" Quad-Lens (40:1 Domestic; 35.4:1 Aid)│ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ 2. MESO SPATIAL INFRASTRUCTURE & SUBNATIONAL QOS (M-LAB + GIGA + OOKLA) │ │
│ │    • Subnational Admin-1 QoS Digest: M-Lab NDT Speed/Latency Timeseries │ │
│ │    • 3m / 6m / 12m Statistical Shift Detector across 7 Economies        │ │
│ │    • UNICEF-ITU Giga School Mapping (21,000 school layers + QC report)  │ │
│ │    • 41,754 Ookla 2024Q1 Cellular & Fixed Spatial Intelligence Tiles    │ │
│ │    • 237 World Bank Digital Education Investment Loans                  │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ 3. MICRO GROUND-TRUTH & TRIANGULATION HUB                               │ │
│ │    • Interactive 7-Country Discrepancy Heatmap (Citizen vs Macro)       │ │
│ │    • Afrobarometer R9 & R10 Longitudinal Panel (N = 22,369 citizens)    │ │
│ │    • Uwezo Citizen Assessments (N = 243,000 children in Kenya & TZA)    │ │
│ │    • Pillar 5 Linguistic Exclusion & Commercial AI Token Tax Matrix     │ │
│ │    • Academic Learning Benchmarks & Multi-Stakeholder Sankey Diagram    │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ 4. FRONTLINE DECISION TOOLKITS & FIELD HUBS                             │ │
│ │    • Tool 1: EdTech Readiness Check (Dual Gatekeeping: Teacher & SMC)   │ │
│ │    • Tool 2: TaRL 3-Station Rotational Pedagogy Planner                 │ │
│ │    • Tool 3: Vetted Resilient Digital Public Goods (DPG) Directory      │ │
│ │    • Tool 4: Supply-Demand Discrepancy Matrix (48 Demand × 148 Supply)  │ │
│ │    • Tool 5: KoboToolbox Field Hub (XLSForms + Live/Demo Safe Modes)    │ │
│ │    • Tool 6: Standalone Mobile Screener (Teacher_Diagnostic_Survey.html)│ │
│ │    • Tool 7: 16-Quote Qualitative Field Voice Carousel Strip            │ │
│ │    • Tool 8: Standalone High-Contrast Printable Field Toolkits          │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ AUTOMATED DATA ENGINES, REPOSITORIES & CI/CD WORKFLOWS                      │
│ • scripts/fetch_imf_cofog.py (IMF GFS COFOG domestic outlays 2017–2024)     │
│ • scripts/fetch_iati_funding.py (IATI Datastore API 29k+ aid transactions)  │
│ • scripts/compile_macro_fiscal_indicators.py (Digital Recurrent Cliff)     │
│ • scripts/fetch_mlab.py & build_dashboard_data.py (M-Lab Admin-1 QoS)       │
│ • scripts/build_changes.py (Statistical shift detection over M-Lab series)  │
│ • scripts/build_giga_layer.py & make_synthetic_giga.py (Giga school layers) │
│ • scripts/fetch_kobo_submissions.py & process_kobo_surveys.py (Kobo Hub)    │
│ • .github/workflows/ (weekly_kobo_fetch, monthly_mlab, quarterly_cofog)     │
│ • Automated Test Suite (52 tests passing in tests/ and root)                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Inventory of Completed Work & Deliverables

### A. Academic & Analytical Foundation (Component A)

1. **Thesis Concept & Analytical Core (`Thesis_First_Draft_Concept.md`):**
   - Formal master's thesis concept aligned with the UniTO ICT4D model.
   - Comprehensive abstract, foundational SSA statistics (87% learning poverty, <30% rural electrification, 85% pilot mortality).
   - In-depth multi-stakeholder reality matrix contrasting lived bottlenecks with practical decision benefits.
   - Theoretical framework deconstructing the PISA blind spot, saturation vs. scarcity divides, and Gert Biesta's three pedagogical functions (Qualification, Socialization, Subjectification).
   - Chapter-by-chapter mapping for academic defense readiness.
2. **Analytical Framework Question Set (`Analytical_Framework_Answers.md`):**
   - Point-by-point answers aligning the thesis with the master program's Analytical Framework 1 and 2 guidelines.
   - Analysis of target Sustainable Development Goals (SDG 4 Quality Education, SDG 9 Innovation/Infrastructure, SDG 10 Reduced Inequalities).
   - Formulates verifiable project objectives, direct vs indirect beneficiaries, and long-term institutional sustainability strategies.
3. **Defense Dossier & Talking Points (`Defense_Talking_Points.md`):**
   - Strategic responses prepared for academic defense examiners.
   - Key topics: "Why reject 1:1 hardware in favor of 3-station rotations?", "Why is the informal airtime tax an ICT4D issue?", "Why situate student data privacy in SMC governance rather than teacher checklists?", and "How does the Digital Recurrent Cliff prove that donor capital aid drives school-level collapse?".
4. **Academic Reference Notes & Verification Table (`reference_notes.md`):**
   - Authoritative mapping of statutory laws (Kenya KICD Act No. 4, Rwanda REB Inspection Guidelines, Nigeria Child Rights Act).
   - Landmark citations: UNESCO GEM Report 2023, J-PAL TaRL evaluations (Banerjee, Duflo et al. 2017), AfroBench/IrokoBench LLM benchmarks, and Piper et al. on teacher time-on-task.
5. **Data Dictionary & Provenance Registry (`DATA_DICTIONARY_AND_LOOKUP.md`):**
   - Auditable registry of all variables across the 6 UNESCO pillars, citizen learning assessments (Uwezo), public demand surveys (Afrobarometer Round 9 & 10), subnational M-Lab QoS metrics, Giga school connectivity layers, and macro-fiscal outlays.
6. **Kobo Pipeline Security & Privacy Boundary Log (`KOBO_PIPELINE_CHANGELOG.md`):**
   - Technical log recording Phase 1 fail-closed ingestion, token least-privilege scoping, Phase 2 allowlisted de-identification, small-sample suppression, and public dashboard gating.

---

### B. Interactive Decision Support Observatory (`index.html`) (Component B)

The web deliverable is a single-page web observatory (12,000+ lines) styled with Tailwind CSS, organized across four systemic lenses:

#### 1. Lens 1: The Learning Reality
- **Uwezo Citizen Learning Assessments ($N = 243,000$ children):** Foundational literacy (41.6% Kenya / 52.0% Tanzania) and numeracy (46.8% Kenya / 51.5% Tanzania) disaggregated by urban vs rural geography and gender.
- **Academic Learning Benchmarks & Interactive Sankey:** Ingests standardized learning proficiency distributions (`data/processed/academic_learning_benchmarks.json`) and visualizes student learning progression bottlenecks.
- **Global Education Evidence Advisory Panel (GEEAP) "Smart Buys" Simulator:** Contrasts high-cost hardware transfers (classified as "Bad Buys" or "Needs Caution" without pedagogical reform) against foundational coaching, targeted instruction, and structured teacher guides ("Great Buys").

#### 2. Lens 2: The Infrastructure & Subnational Reality
- **Subnational M-Lab Admin-1 QoS & Longitudinal Shift Detector (`#section-mlab-digest`):**
  - Interactive D3 v7 choropleth map powered by ES modules (`js/admin1_explorer.js`, `js/dashboard_state.js`, vendored `js/vendor/d3.v7.min.js`).
  - Displays monthly download throughput, upload throughput, and round-trip latency across all Admin-1 regions for Kenya, Ghana, Mauritius, Nigeria, Rwanda, Tanzania, and Zambia.
  - Automatically computes 3-month, 6-month, and 12-month percentage shifts to detect network improvements or degradation.
  - Deep-linked URL query parameters (`?country=KEN&metric=download&admin1=KE-30`) for academic verification.
- **UNICEF-ITU Giga School Connectivity Geospatial Layers:**
  - 21,000 schools mapped across the 7 focus economies (3,000 schools/country in calibrated demo mode with formal schema compliance).
  - Classifies institutional connectivity into *Connected*, *Partial*, and *Unconnected*, with power source breakdown (Grid, Solar, None).
  - Accompanied by quality control audit reports (`out/giga_qc.json`).
- **Ookla Cellular & Fixed Spatial Intelligence:**
  - Ingests 41,754 spatial tiles (2024 Q1) across the 7 focus economies, tracking ground-truth download speeds, upload speeds, latency, and test counts across mobile cell towers.

#### 3. Lens 3: The Pilot & Market Reality
- **237 World Bank Digital Education Loans Portfolio:**
  - Tracks loan commitments and operational lifecycles across 69 borrowing countries.
- **Supply-Demand Discrepancy Matrix (48 Demand × 148 Supply):**
  - Evaluates 148 commercial and donor EdTech products against 48 SSA country environments.
  - Demonstrates that **70.8% of market offerings require smartphones and continuous broadband**, whereas **82.5% of rural public schools require offline, feature-phone, or shared-device architectures**.

#### 4. Lens 4: Macro-Fiscal & External Aid Observatory Matrix (IMF COFOG + IATI)
- **IMF Government Finance Statistics (GFS) COFOG Ingestion (2017–2024):** Ingests domestic public expenditures across Education (COFOG 709), Communication (7047), Transport (7045), and Total Outlays.
- **IATI Datastore Aid Ingestion (2017–2024):** Normalizes 29,388 official external development transactions totaling **$1.84 Billion in education financing** and **$52 Million in central ICT aid** across 7 focus economies.
- **The "Digital Recurrent Cliff" Quad-Lens:** Empirically illustrates the macro-financing asymmetry through the 40:1 domestic expenditure ratio (e.g., Kenya allocates 18.4% of budget to Education, but only 0.46% to central communications infrastructure) alongside a 35.4:1 external aid asymmetry ($1.84B education aid vs $52M ICT aid), illustrating why hardware donations lack sustainable operational counterpart budgets.
- **Dynamic 7-Country Interactive Matrix:** One-click drill-downs into Kenya, Rwanda, Tanzania, Ghana, Nigeria, Zambia, and Mauritius (control benchmark) displaying domestic expenditure shares, 8-year cumulative aid disbursements, and 2020 COVID-19 emergency surge spikes.

---

### C. Frontline Decision Tools & Practical Toolkits

1. **Tool 1: EdTech Readiness Check (Dual-Gatekeeping Diagnostic):**
   - **Tier 1: Teacher Classroom Survivability (7 Feasibility Questions):** Evaluates syllabus accreditation, daily electricity supply, teacher personal airtime taxation, pupil-to-device ratios, mother-tongue dialect support, double data entry administrative friction, and offline operational autonomy.
   - **Tier 2: School Management Committee (SMC) & Community Safeguarding:** Evaluates minor data privacy, commercial ad-blocking, parental consent, e-waste lifecycle maintenance, and community tech support.
   - **Dynamic Memorandum Generator:** Outputs an actionable decision memorandum classifying the proposed tool into *Approved for Rotational Use*, *Conditional Adoption*, or *Immediate Rejection*.
2. **Tool 2: Classroom Rotation Planner (TaRL Pedagogy Engine):**
   - Solves 50:1 or 80:1 pupil-teacher ratios under device scarcity (e.g., 10 tablets for 50 pupils).
   - Generates daily structured timetables dividing class sessions into 3 concurrent pedagogical stations:
     - *Station 1: Direct Teacher Pedagogical Coaching* (Teaching at the Right Level foundational literacy/numeracy).
     - *Station 2: Peer Collaborative Work & Manipulatives* (Unplugged learning, slate work).
     - *Station 3: Resilient Offline Digital Practice* (Shared device guided exercises).
3. **Tool 3: Resilient Digital Public Goods (DPG) Directory:**
   - Catalog of certified, 100% offline-first open educational solutions (Kolibri, Kiwix, African Storybook, PhET Interactive Simulations, Nal'ibali, Chimple, Onebillion).
   - Filterable by learner segment, operational mode (Micro-SD, local Wi-Fi hotspot, APK sneakernet), and verified open licensing (CC BY, MIT, GPL).
4. **Tool 4: Interactive 7-Country Discrepancy Heatmap & Triangulation Hub:**
   - Replaced static illustrations with an interactive triangulation matrix spanning all 7 focus economies.
   - Triangulates citizen ground truth from **Afrobarometer R9 ($N = 11,169$) and R10 ($N = 11,200$)** with macro-fiscal indicators.
   - Integrates Pillar 5 linguistic exclusion and commercial AI token tax metrics (AfroBench/IrokoBench).
5. **Tool 5: KoboToolbox Field Evidence Hub & Real/Demo Modes:**
   - Complete field survey management hub supporting 4 instrument protocols: Teacher Survey, EdTech Provider Survey, Expert Consultation, and Follow-up Contact Opt-in.
   - Supports live allowlisted aggregates (`data/processed/survey_dashboard_live.json`) and explicit Demo preview mode using calibrated priors (`survey_data_calibrated.json`).
   - Replaces unvetted client-side CSV uploads with a privacy-governed pipeline.
6. **Tool 6: Standalone Frontline Mobile Screener (`Teacher_Diagnostic_Survey.html`):**
   - Standalone, ultra-lightweight, mobile-responsive HTML screener designed for low-bandwidth frontline teachers.
   - Features client-side instant feasibility scoring and actionable guidance without network dependency.
7. **Tool 7: Qualitative Field Voice Carousel Strip:**
   - 16 verified frontline qualitative testimonies from primary school teachers, headteachers, SMC members, and African startup founders in Kenya, Rwanda, Zambia, Senegal, Nigeria, and Tanzania.
8. **Tool 8: Offline Printable Field Toolkits:**
   - Three dedicated printable HTML packs styled with high-contrast print stylesheets, page-break optimizations, and top print navigation bars:
     - `EdTech_Readiness_Check_Printable.html` (Frontline Screener + SMC Rubric)
     - `Rotation_Planner_Printable.html` (TaRL 3-Station Weekly Schedule)
     - `Vetted_Solutions_Directory_Printable.html` (Offline DPG Field Spec Sheet)

---

### D. Data Engineering Pipelines & Python Engines

| Pipeline Script | Data Sources Harvested | Output Files & Assets | Key Functionality |
| :--- | :--- | :--- | :--- |
| `fetch_6pillars_pipeline.py` | World Bank WDI, UNESCO UIS, ITU APIs | `data/processed/latest_country_profiles_6pillars.csv`<br>`data/processed/indicators_timeseries.csv`<br>`data/processed/wb_digital_education_projects.csv` | Queries 20+ systemic variables across 48 SSA economies (2015–2024), caches raw JSON payloads with SHA-256 hashes, and formats indicators into the UNESCO 6 Pillars taxonomy. |
| `scripts/fetch_imf_cofog.py` | IMF Government Finance Statistics (GFS) COFOG API & archives | `data/imf/imf_cofog_long.csv`<br>`data/imf/imf_cofog_shares.csv`<br>`data/imf/imf_cofog_coverage.csv`<br>`data/imf/imf_cofog_audit.json` | Pulls domestic central government outlays across Education (709), Communication (7047), Transport (7045), and Total Outlays. Covers all 54 African economies with incremental caching. |
| `scripts/fetch_iati_funding.py` | International Aid Transparency Initiative (IATI) Datastore API | `data/iati/iati_transactions.csv`<br>`data/iati/iati_funding_by_year.csv`<br>`data/iati/iati_audit.json` | Harvests 29,388 raw transactions (2017–2024), filters DAC CRS sector codes for Education (111/112/113/114) and Telecommunications/ICT (220), normalizes currencies to USD, and tracks annual disbursements. |
| `scripts/compile_macro_fiscal_indicators.py` | Ingested IMF COFOG + IATI outputs + World Bank WDI | `data/processed/macro_fiscal_ecosystem.json`<br>`data/processed/macro_fiscal_data.js` | Synthesizes domestic expenditure shares, external aid trends, 40:1 ICT financing bottlenecks, and compiles the Digital Recurrent Cliff quad-lens data structure for `index.html`. |
| `scripts/fetch_mlab.py` | Measurement Lab (M-Lab) NDT API / BigQuery | `data/processed/connectivity/mlab/*.csv` | Downloads monthly subnational download/upload speed and latency measurements across Admin-1 subdivisions. |
| `scripts/fetch_boundaries.py` | geoBoundaries API | `out/boundaries/*.geojson`<br>`out/boundaries/crosswalk.csv` | Downloads Admin-1 GeoJSON boundary polygons and builds crosswalk tables to M-Lab ISO subdivision codes. |
| `scripts/build_dashboard_data.py` | Boundaries GeoJSON + M-Lab time series | `out/dashboard/*.geojson`<br>`out/dashboard/*.series.json`<br>`out/dashboard/manifest.json` | Compiles Admin-1 GeoJSON with rewound winding order and historical monthly QoS time series for D3 v7 explorer. |
| `scripts/build_changes.py` | Subnational monthly QoS series | `out/dashboard/*.changes.json` | Performs statistical change detection (3-month, 6-month, 12-month) over subnational speed and latency. |
| `scripts/build_giga_layer.py` | School location and connectivity tables | `out/dashboard/*_schools.json`<br>`out/giga_qc.json`<br>`out/layers/` | Generates GeoJSON school layers across 7 economies with strict quality control auditing. |
| `make_synthetic_giga.py` | School coordinates & baseline distributions | `TEMP/giga_synthetic/` | High-fidelity synthetic Giga school generator calibrated for demo exploration prior to live API token activation. |
| `scripts/fetch_kobo_submissions.py` | KoboToolbox v2 REST API | Temporary staging under `RUNNER_TEMP` (or `data/demo/kobo` with `--demo`) | Fetches submissions across 4 instruments (Teacher, Provider, Expert, Follow-up) with pagination and fail-closed security. |
| `scripts/process_kobo_surveys.py` | Raw Kobo submission payloads | `data/processed/survey_dashboard_live.json` | Allowlist-only data processor that scrubs all PII, suppresses small groups ($N < 5$), excludes follow-up data, and maps responses to XLSForm choices. |
| `scripts/extract_afrobarometer_education.py` | Afrobarometer SPSS/SAV data archives | `data/processed/afrobarometer_{ISO3}_r9.json`<br>`data/processed/afrobarometer_{ISO3}_r10.json` | Extracts citizen education priorities, delivery satisfaction, and infrastructure access across Round 9 and Round 10. |
| `scripts/extract_citizen_assessments.py` | Uwezo survey summaries (Kenya & Tanzania) | `data/processed/uwezo_KEN_latest.json`<br>`data/processed/uwezo_TZA_latest.json` | Ingests foundational literacy, numeracy, and household device ownership across $N = 243,000$ children. |
| `scripts/generate_interactive_heatmap.py` | Afrobarometer + WDI + UIS + LLM benchmarks | `data/processed/interactive_triangulation_heatmap.json` | Generates interactive 7-country triangulation matrix bridging macro rhetoric with citizen ground truth. |
| `scripts/verify_dpg_urls.py` | `data/resources_registry.json` | `data/last_link_verification_report.md` | Automated health-check pipeline pinging all certified DPG web endpoints, tracking HTTP response codes and latency. |
| `AoA survey/xlsform/build_xlsforms.py` | Questionnaire specifications | `AoA survey/xlsform/*.xlsx` | Generates standard XLSForms for Teacher, Provider, Expert, and Follow-up instruments. |

---

### E. Comprehensive Testing & Quality Assurance Suite (52 Tests)

The repository incorporates 52 automated tests spanning decision logic, macro-fiscal compilers, Kobo ingestion pipelines, and geospatial layers:

#### 1. Root Test Suite (33 Tests)
* **`test_decision_logic.py` (15 tests):**
  - Verifies Teacher Gatekeeping feasibility score calculations and statutory veto triggers (electricity failure, personal airtime taxation, language mismatch, unvetted APK security).
  - Validates SMC Safeguarding veto thresholds (minor data privacy violation, commercial ad tracking, lack of parental consent).
  - Validates TaRL 3-station rotation planner arithmetic (seat allocation, student-device ratios, station cycle completeness).
* **`test_compile_macro_fiscal_indicators.py` (8 tests):**
  - Verifies target 7-country configuration and ISO mapping for all 54 African economies.
  - Validates currency conversion table (KES, RWF, TZS, GHS, NGN, XOF, ZMW to USD).
  - Validates schema and integrity of `macro_fiscal_ecosystem.json` and `macro_fiscal_data.js`.
  - Verifies Kenya domestic fiscal series (18.4% education share, 0.46% ICT share, 40:1 ratio).
  - Validates CLI execution and exit codes.
* **`test_fetch_iati_funding.py` (6 tests):**
  - Tests API query builders and DAC CRS sector code attribution (Education 111 vs ICT 220).
  - Tests transaction normalization, currency conversion, and annual aggregation algorithms.
  - Tests pagination handling, HTTP timeouts, and CLI argument parsing.
* **`test_fetch_imf_cofog.py` (4 tests):**
  - Tests COFOG classification column detection across varying national reporting structures.
  - Validates domestic expenditure share calculation against total outlays.
  - Tests file persistence, audit log schemas, and CLI execution.

#### 2. Subsystem & Ingestion Test Suite (`tests/` Directory — 19 Tests)
* **`tests/test_process_kobo_surveys.py` (8 tests):**
  - Verifies that public aggregate JSON is produced without raw submission IDs or PII.
  - Validates CLI execution and status generation (`available`, `insufficient_data`).
  - Tests suppression of distributions when response groups contain fewer than 5 respondents.
  - Verifies strict rejection of synthetic records when processing in real mode.
  - Validates rejection of unknown choice codes and unmapped schema fields.
  - Verifies fail-closed quality gate when zero submissions are returned.
* **`tests/test_fetch_kobo_submissions.py` (6 tests):**
  - Tests multi-page pagination and rejection of cross-host redirect URLs.
  - Tests strict enforcement of all four required Kobo asset UIDs and live credentials.
  - Verifies output path confinement outside the repository.
  - Validates explicit `--demo` synthetic generation mode.
* **`tests/test_make_synthetic_giga.py` (3 tests):**
  - Validates synthetic Giga school coordinate bounds within focus country borders.
  - Tests distribution fidelity of connectivity classifications.
  - Verifies output schema conformance to Giga specifications.
* **`tests/test_build_giga_layer.py` (2 tests):**
  - Validates school layer GeoJSON construction and administrative property tagging.
  - Verifies quality control audit metrics in `out/giga_qc.json`.

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
| `980aa5d` | Nov 5, 2026 | 4-Feature decision upgrade & presentation deck | Dual Gatekeeping (Teacher + SMC), TaRL rotations, Supply-Demand Matrix, AoA Codebook (`data/AoA_Survey_to_Pillar_Codebook.md`), Giga mapping (`scripts/map_giga_schools.py`), `build_checkin_deck.py` |
| `3059af6` | Nov 6, 2026 | Macro-Fiscal & Aid Observatory (IMF + IATI) | `fetch_imf_cofog.py`, `fetch_iati_funding.py`, `compile_macro_fiscal_indicators.py`, test suite, Digital Recurrent Cliff quad-lens in `index.html` (29,388 transactions, $1.84B aid) |
| `8c589a6` | Nov 7, 2026 | Thesis critique resolution & automated decision test suite | `data/data_provenance_registry.json`, `test_decision_logic.py` (15 regression tests), reframed macro-fiscal indicators |
| `99b82a8` | Nov 7, 2026 | Multi-country Ookla 2024Q1 tiles & Giga maps | 41,754 cellular tiles across 7 economies, Giga school mapping pipelines |
| `15f357e` | Nov 7, 2026 | Multi-country documentation & data transparency | `README.md`, `WORK_SUMMARY.md`, `DATA_DICTIONARY_AND_LOOKUP.md` |
| `190b35b` | Nov 7, 2026 | Afrobarometer R9 & R10 multi-country panel ingestion | 12 country-round processed files (KEN, TZA, GHA, NGA, ZMB, MUS), longitudinal comparison |
| `3c94ebc` | Nov 7, 2026 | Afrobarometer R9/R10 longitudinal toggle & Uwezo Tanzania | `index.html` dynamic R9 vs R10 toggle, `data/raw/uwezo_tanzania_national_summary.csv`, `data/processed/uwezo_TZA_latest.json` |
| `e4f048c` | Nov 8, 2026 | UI navigation & 7-country title update | Implemented `switchDashboard`, `showGapChart`, `filterCodebook`, title updated to 7-Country Observatory |
| `b156d6d` | Nov 8, 2026 | KPI card border styling & regex fix | Added kpi-card IDs, wired `updateKpiCardBorders`, fixed score parser regex |
| `fd3e950` | Nov 8, 2026 | Spatial disparity & macro-fiscal table refinement | Positioned spatial disparity above lenses, dual-country comparison, bottom-anchored chart tracks, custom flag dropdowns |
| `846bdc9` | Nov 9, 2026 | Interactive 7-country discrepancy heatmap & survey hub | Interactive heatmap, Afrobarometer R10 triangulation, Pillar 5 linguistic exclusion, `Teacher_Diagnostic_Survey.html` |
| `85a9122` | Nov 10, 2026 | Kobo survey pipeline, XLSForms & GitHub Actions | `AoA survey/xlsform/` (Teacher, Provider, Expert, Followup), `fetch_kobo_submissions.py`, `.github/workflows/weekly_kobo_fetch.yml` |
| `aa6a890` | Nov 11, 2026 | M-Lab QoS pipeline, academic benchmarks & Sankey | Ingested M-Lab NDT data, academic learning benchmarks, interactive Sankey diagram |
| `506fc38` | Nov 11, 2026 | Observatory dashboard navigation & data fixes | Restored navigation stability and data bindings |
| `f2f72f1` | Nov 12, 2026 | Unified 3-lens multi-stakeholder architecture | Aligned landing layout with Macro, Meso, and Micro lenses; integrated thesis concepts |
| `a8124b0` | Nov 12, 2026 | UI contrast & simulation controls fix | Resolved white-on-white text, collapsed simulation controls, removed unwanted borders |
| `f33e063` | Nov 12, 2026 | M-Lab subnational Admin-1 digest & shift detector | `fetch_boundaries.py`, `build_dashboard_data.py`, `build_changes.py`, `js/admin1_explorer.js`, D3 v7 choropleth, GeoJSON bundles, deep linking |
| *Working Tree* | Nov 13–16, 2026 | Fail-closed Kobo privacy boundary & Giga layer generation | Phase 1 & 2 Kobo security (`process_kobo_surveys.py`), `KOBO_PIPELINE_CHANGELOG.md`, `tests/` suite (52 tests total), `build_giga_layer.py`, `make_synthetic_giga.py`, quarterly COFOG workflow |

---

## 5. Master File & Directory Index

### Root Research & Concept Documents
* [`WORK_SUMMARY.md`](./WORK_SUMMARY.md) — This master document summarizing all progress, systems, and research assets.
* [`README.md`](./README.md) — Top-level repository guide with quick-start instructions and architecture overview.
* [`KOBO_PIPELINE_CHANGELOG.md`](./KOBO_PIPELINE_CHANGELOG.md) — Security audit trail, privacy boundary definitions, and Kobo pipeline changelog.
* [`DATA_DICTIONARY_AND_LOOKUP.md`](./DATA_DICTIONARY_AND_LOOKUP.md) — Complete data dictionary of all processed metrics, sample sizes, and source APIs.
* [`Thesis_First_Draft_Concept.md`](./Thesis_First_Draft_Concept.md) — Academic thesis draft for the UniTO Master in ICT for Development and Social Good.
* [`reference_notes.md`](./reference_notes.md) — Academic citation verification table, statutory acts, and defense talking points.
* [`Defense_Talking_Points.md`](./Defense_Talking_Points.md) — Rapid-fire strategic answers for academic thesis defense committees.
* [`Analytical_Framework_Answers.md`](./Analytical_Framework_Answers.md) — Formal answers to Analytical Framework 1 and 2 master requirements.
* [`LICENSE`](./LICENSE) — MIT License.

### Interactive Web Deliverables
* [`index.html`](./index.html) — The primary interactive Decision Observatory (12,000+ lines, 4 lenses, 8 decision tools).
* [`Teacher_Diagnostic_Survey.html`](./Teacher_Diagnostic_Survey.html) — Standalone mobile-responsive teacher feasibility screener with client-side scoring.
* [`EdTech_Readiness_Check_Printable.html`](./EdTech_Readiness_Check_Printable.html) — Standalone printable pack for classroom feasibility and SMC rubrics.
* [`Rotation_Planner_Printable.html`](./Rotation_Planner_Printable.html) — Standalone printable pack for 3-station TaRL rotation timetables.
* [`Vetted_Solutions_Directory_Printable.html`](./Vetted_Solutions_Directory_Printable.html) — Standalone printable catalog of resilient offline DPGs.
* [`example.html`](./example.html) — Standalone test harness for the M-Lab Admin-1 explorer module.

### Modular JavaScript Engines (`js/`)
* [`js/admin1_explorer.js`](./js/admin1_explorer.js) — ES module rendering D3 v7 subnational choropleth map, sparklines, and change markers.
* [`js/dashboard_state.js`](./js/dashboard_state.js) — URL query parameter state synchronization for deep linking.
* [`js/vendor/d3.v7.min.js`](./js/vendor/d3.v7.min.js) — Locally vendored D3 v7 library (no CDN dependency).

### Python Data Harvesting & Synthesis Pipelines (`scripts/`)
* [`scripts/fetch_imf_cofog.py`](./scripts/fetch_imf_cofog.py) — Ingests domestic public expenditures (COFOG 709 Education vs 7047 ICT) across African economies.
* [`scripts/fetch_iati_funding.py`](./scripts/fetch_iati_funding.py) — Ingests 29,388 official external development transactions from the IATI Datastore API.
* [`scripts/compile_macro_fiscal_indicators.py`](./scripts/compile_macro_fiscal_indicators.py) — Synthesizes macro-fiscal indicators and the Digital Recurrent Cliff data engine.
* [`scripts/fetch_mlab.py`](./scripts/fetch_mlab.py) — Downloads monthly subnational download/upload speed and latency measurements from M-Lab.
* [`scripts/fetch_boundaries.py`](./scripts/fetch_boundaries.py) — Downloads Admin-1 GeoJSON boundary polygons from geoBoundaries and builds crosswalks.
* [`scripts/build_dashboard_data.py`](./scripts/build_dashboard_data.py) — Generates static data bundles (GeoJSON, series.json, changes.json, manifest.json) for 7 economies.
* [`scripts/build_changes.py`](./scripts/build_changes.py) — Performs 3-month, 6-month, and 12-month statistical change detection on M-Lab time series.
* [`scripts/build_giga_layer.py`](./scripts/build_giga_layer.py) — Builds school geospatial layers and quality control audits.
* [`scripts/fetch_kobo_submissions.py`](./scripts/fetch_kobo_submissions.py) — Fail-closed fetcher for Kobo survey responses across 4 instruments.
* [`scripts/process_kobo_surveys.py`](./scripts/process_kobo_surveys.py) — Allowlist-only survey processor that scrubs PII and produces public dashboard aggregates.
* [`scripts/generate_interactive_heatmap.py`](./scripts/generate_interactive_heatmap.py) — Compiles 7-country discrepancy heatmap data.
* [`scripts/verify_dpg_urls.py`](./scripts/verify_dpg_urls.py) — Pings all certified DPG web endpoints and reports health status.
* [`scripts/serve_dev.py`](./scripts/serve_dev.py) — Local development static server.

### Automated Test Suite (52 Tests)
* [`test_decision_logic.py`](./test_decision_logic.py) — 15 tests covering Gatekeeping thresholds, statutory vetoes, and TaRL rotation arithmetic.
* [`test_compile_macro_fiscal_indicators.py`](./test_compile_macro_fiscal_indicators.py) — 8 tests covering macro-fiscal calculations, ISO coverage, and currency conversion.
* [`test_fetch_iati_funding.py`](./test_fetch_iati_funding.py) — 6 tests covering IATI Datastore API queries, sector codes, and USD aggregation.
* [`test_fetch_imf_cofog.py`](./test_fetch_imf_cofog.py) — 4 tests covering IMF GFS COFOG share parsing, file schemas, and CLI behavior.
* [`tests/test_process_kobo_surveys.py`](./tests/test_process_kobo_surveys.py) — 8 tests covering Kobo data sanitization, small-sample suppression, and schema validation.
* [`tests/test_fetch_kobo_submissions.py`](./tests/test_fetch_kobo_submissions.py) — 6 tests covering pagination, security boundaries, and demo mode.
* [`tests/test_make_synthetic_giga.py`](./tests/test_make_synthetic_giga.py) — 3 tests covering synthetic Giga school coordinate and attribute generation.
* [`tests/test_build_giga_layer.py`](./tests/test_build_giga_layer.py) — 2 tests covering school GeoJSON layer compilation and QC reporting.

### Automated GitHub Workflows (`.github/workflows/`)
* [`.github/workflows/weekly_kobo_fetch.yml`](./.github/workflows/weekly_kobo_fetch.yml) — Scheduled weekly fetch and de-identification of Kobo field surveys with manual approval gate.
* [`.github/workflows/monthly_mlab_fetch.yml`](./.github/workflows/monthly_mlab_fetch.yml) — Scheduled monthly harvesting of M-Lab subnational QoS metrics.
* [`.github/workflows/quarterly_imf_cofog_fetch.yml`](./.github/workflows/quarterly_imf_cofog_fetch.yml) — Scheduled quarterly update of IMF GFS COFOG domestic outlays.
* [`.github/workflows/verify_dpg_links.yml`](./.github/workflows/verify_dpg_links.yml) — Monthly health check and link verification for certified Digital Public Goods.

---

## 6. How to Run, Test, and Verify

### Running the Interactive Observatory Locally
```bash
# Option 1: Use repository development server script
python3 scripts/serve_dev.py 8000

# Option 2: Use Python built-in HTTP server
python3 -m http.server 8000
# Access via http://localhost:8000/ in any modern browser
```

### Running the Test Suite
```bash
# Run root decision logic, macro-fiscal, and compiler tests (23 tests passing synchronously)
python3 -m pytest test_decision_logic.py test_compile_macro_fiscal_indicators.py -v

# Run Kobo pipeline, privacy boundary, and subsystem tests
python3 -m unittest discover -s tests -v
```

### Executing Data Harvesting & Synthesis Pipelines
```bash
# 1. Macro-Fiscal Pipeline
python3 scripts/fetch_imf_cofog.py --years 2017-2024
python3 scripts/fetch_iati_funding.py --years 2017-2024
python3 scripts/compile_macro_fiscal_indicators.py

# 2. Subnational QoS & Shift Detection Pipeline
python3 scripts/fetch_boundaries.py
python3 scripts/build_dashboard_data.py
python3 scripts/build_changes.py

# 3. Giga School Connectivity Layers
python3 scripts/build_giga_layer.py

# 4. Kobo Field Evidence Processing (Demo Mode)
python3 scripts/fetch_kobo_submissions.py --demo
python3 scripts/process_kobo_surveys.py --input-dir data/demo/kobo --output data/processed/survey_dashboard_demo.json

# 5. DPG Link Verification
python3 scripts/verify_dpg_urls.py
```
