# Mapping EdTech Fit in Sub-Saharan Africa: A Multi-Tiered Six-Pillars Decision Observatory

[![Master Degree](https://img.shields.io/badge/Degree-Master%20in%20ICT4D-blue.svg)](https://www.unito.it/)
[![Academic Year](https://img.shields.io/badge/Academic%20Year-2025--2026-green.svg)](https://www.unito.it/)
[![Automated Tests](https://img.shields.io/badge/Automated%20Tests-52%20Passing-brightgreen.svg)](./tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Live Observatory](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue)](https://SunilRaman42.github.io/CC_3/)

> **Master in ICT for Development and Social Good (UniTO · COREP · Impactskills)**  
> **Academic Year:** 2025–2026  
> **Academic Supervisor:** Prof. Elisa Bignante, Department of Cultures, Politics and Society, University of Turin  
> **Candidate Repository:** `SunilRaman42/CC_3` | **Live Web Platform:** [`https://SunilRaman42.github.io/CC_3/`](https://SunilRaman42.github.io/CC_3/)  

---

> [!IMPORTANT]
> **Comprehensive Work Summary & Audit Trail:** For an exhaustive, up-to-date dossier detailing all theoretical foundations, data engineering pipelines, interactive decision tools, test suites, and git version history, consult [**`WORK_SUMMARY.md`**](./WORK_SUMMARY.md). For field survey privacy boundaries, consult [**`KOBO_PIPELINE_CHANGELOG.md`**](./KOBO_PIPELINE_CHANGELOG.md). For granular indicator schemas, consult [**`DATA_DICTIONARY_AND_LOOKUP.md`**](./DATA_DICTIONARY_AND_LOOKUP.md).

---

## 1. Project Overview & Research Problematic

This repository hosts the academic research, reproducible data engineering pipelines, empirical subnational datasets, and interactive decision-support instruments for the Master's Thesis investigating **Educational Technology (EdTech) fit across Sub-Saharan Africa (SSA)**.

The research investigates why top-down educational technology initiatives chronically collapse when transitioning from donor-funded pilots to institutional public schooling—a phenomenon termed the **"85% Pilot Graveyard"**. Grounded in **UNESCO's Six Pillars for the Digital Transformation of Education**, the project establishes a **Vertical Traceability Architecture** connecting three interdependent operational lenses:

```
                      VERTICAL TRACEABILITY ARCHITECTURE
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. MACRO LENS: SYSTEMIC POLICY & MACRO-FISCAL FOUNDATION                    │
│    • Public Finance: IMF GFS COFOG domestic outlays (Education vs ICT)      │
│    • Development Assistance: 29,388 IATI aid transactions ($1.84B Ed/$52M)  │
│    • Digital Recurrent Cliff: 40:1 domestic ratio; 35.4:1 external aid gap   │
│    • Multi-Country Benchmarking: 48 SSA economies (WB WDI, UIS, ITU)         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. MESO LENS: SPATIAL INFRASTRUCTURE & INSTITUTIONAL CAPABILITY            │
│    • Subnational QoS Digest: M-Lab NDT Admin-1 speed, latency, 3/6/12m shifts│
│    • Cellular Mapping: Ookla 2024Q1 spatial intelligence (41,754 tiles)     │
│    • Schoolhouse Mapping: UNICEF-ITU Giga geospatial pipelines (21,000 sch) │
│    • Project Portfolio: 237 World Bank digital education investment loans   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. MICRO LENS: CLASSROOM REALITY & FRONTLINE DECISION GOVERNANCE            │
│    • Field Surveys: KoboToolbox privacy-gated multi-instrument pipeline     │
│    • Citizen Ground Truth: Afrobarometer R9 & R10 panels (N = 22,369)       │
│    • Citizen Assessments: Uwezo Kenya & Tanzania (N = 243,000 children)     │
│    • Decision Toolkits: Dual-Gatekeeping Screener (Teacher & SMC Rubrics)    │
│    • Pedagogy: Teaching at the Right Level (TaRL) 3-station rotation planner│
│    • Digital Public Goods: Vetted 100% offline-ready DPG directory          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Repository Structure

| Component | Path / File | Purpose & Contents |
| :--- | :--- | :--- |
| **Comprehensive Work Summary** | [`WORK_SUMMARY.md`](./WORK_SUMMARY.md) | Master dossier summarizing theoretical, architectural, and data milestones. |
| **Data Dictionary & Provenance** | [`DATA_DICTIONARY_AND_LOOKUP.md`](./DATA_DICTIONARY_AND_LOOKUP.md) | Exhaustive registry of indicators, source APIs, samples, schemas, and statistics. |
| **Kobo Pipeline Change Log** | [`KOBO_PIPELINE_CHANGELOG.md`](./KOBO_PIPELINE_CHANGELOG.md) | Security audit, privacy boundary, and de-identification log for field surveys. |
| **Component A: Thesis Concept** | [`Thesis_First_Draft_Concept.md`](./Thesis_First_Draft_Concept.md) | Theoretical thesis concept, stakeholder matrices, and research methodology. |
| **Analytical Frameworks** | [`Analytical_Framework_Answers.md`](./Analytical_Framework_Answers.md) | Answers aligned with UniTO Analytical Framework 1 and 2 guidelines. |
| **Defense Dossier** | [`Defense_Talking_Points.md`](./Defense_Talking_Points.md) | Defense examiner Q&A, statutory citations, and academic justifications. |
| **Reference Notes & Citations** | [`reference_notes.md`](./reference_notes.md) | Statutory laws, peer-reviewed literature, and 6-Pillars mapping. |
| **Component B: Web Observatory** | [`index.html`](./index.html) | Interactive 3-lens, multi-tool decision support web platform. |
| **Field Diagnostic Screener** | [`Teacher_Diagnostic_Survey.html`](./Teacher_Diagnostic_Survey.html) | Standalone mobile-responsive teacher feasibility screener with instant scoring. |
| **Subnational Explorer Module** | [`js/admin1_explorer.js`](./js/admin1_explorer.js)<br>[`js/dashboard_state.js`](./js/dashboard_state.js) | ES module powering D3 v7 subnational choropleth map, sparklines, and URL deep-linking. |
| **Printable Offline Packs** | [`EdTech_Readiness_Check_Printable.html`](./EdTech_Readiness_Check_Printable.html)<br>[`Rotation_Planner_Printable.html`](./Rotation_Planner_Printable.html)<br>[`Vetted_Solutions_Directory_Printable.html`](./Vetted_Solutions_Directory_Printable.html) | Standalone printable packs for off-grid teachers, headteachers, and SMCs. |
| **Data Harvesting Pipelines** | [`scripts/`](./scripts/) | Modular Python pipelines for IMF COFOG, IATI, M-Lab, WDI, UIS, and Giga layers. |
| **Survey XLSForms & Schemas** | [`AoA survey/xlsform/`](./AoA%20survey/xlsform/) | Form definitions for Teacher, Provider, Expert, and Follow-up instruments. |
| **Subnational Data Bundles** | [`out/dashboard/`](./out/dashboard/) | GeoJSON boundaries, time series, change detections, and school layers across 7 economies. |
| **Automated Workflows** | [`.github/workflows/`](./.github/workflows/) | Scheduled GitHub Actions: weekly Kobo fetch, monthly M-Lab, quarterly IMF COFOG, DPG link health. |
| **Automated Test Suite** | [`tests/`](./tests/) & [`test_*.py`](./test_decision_logic.py) | 52 automated tests covering decision logic, compilers, Kobo processing, and Giga layers. |

---

## 3. User Navigation Guide: Accessing Tools & Observatories

The web observatory (`index.html`) is structured into **three primary view canvases** accessible via the top navigation bar and contextual drill-down buttons:
* **Canvas 0: Observatory Landing Page (`#canvas-landing`)** — Executive summaries, subnational QoS explorer, Giga school maps, and field voices.
* **Canvas 1: Systemic Policy & Macro-Fiscal Canvas (`#canvas-systemic`)** — Macro-fiscal outlays, aid flows, 4-lens deep-dives, and 7-country ecosystem comparisons.
* **Canvas 2: Frontline Classroom & Field Hub Canvas (`#canvas-classroom`)** — Dual-gatekeeping screeners, TaRL rotation planner, offline DPG directory, and Kobo survey hub.

```
                                  USER NAVIGATION FLOW
                                ┌──────────────────────┐
                                │   TOP NAVIGATION     │
                                └──────────┬───────────┘
               ┌───────────────────────────┼───────────────────────────┐
               ▼                           ▼                           ▼
    ┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
    │   CANVAS 0: LANDING  │    │  CANVAS 1: SYSTEMIC  │    │  CANVAS 2: CLASSROOM │
    │ • Executive KPIs     │    │ • 4 Analytical Lenses│    │ • Dual-Gatekeeping   │
    │ • M-Lab QoS Digest   │    │ • Recurrent Cliff    │    │ • TaRL Rotation Plan │
    │ • Giga School Points │    │ • 7-Country Profiles │    │ • Offline DPG Catalog│
    │ • Field Voice Strip  │    │ • Triangulation Map  │    │ • Kobo Survey Hub    │
    └──────────────────────┘    └──────────────────────┘    └──────────────────────┘
```

### Tool-by-Tool Access Instructions

#### 1. Subnational M-Lab QoS Digest & Giga School Points Map
* **Location:** Canvas 0 (Landing Page) → Scroll down to `#section-mlab-digest` or click *"Subnational QoS & School Connectivity"*.
* **Country Selection:** Choose any of the 7 economies (`Kenya`, `Rwanda`, `Tanzania`, `Ghana`, `Nigeria`, `Zambia`, `Mauritius`) using the country dropdown or flag pills.
* **Toggling Giga School Points (Recent Feature):**
  1. In the map controls bar, locate the **"School points"** dropdown (default is *Off*).
  2. Select **"Giga school points"** to render all 3,000 geolocated school points across the selected country.
  3. In the adjacent **"Dot color"** selector, choose the visual encoding:
     - *Download speed (30d)*: Gradient color-coding by measured throughput (green $\ge 10\text{ Mbps}$, amber 2–10 Mbps, red $<2\text{ Mbps}$).
     - *Connectivity status*: Binary status (green = *Connected*, red = *Unconnected*).
     - *Power source*: Visualizes grid, solar, generator, or unpowered schools.
  4. **Interactive Telemetry:** Click directly on any school dot to trigger an interactive pop-up card displaying the school ID, coordinates, measured speed, power type, and Admin-1 province.
* **Deep Linking:** You can deep-link directly into any country and school layer via URL parameters (e.g., `index.html?country=KEN&metric=download&schools=synthetic`).

#### 2. Macro-Fiscal Observatory & "Digital Recurrent Cliff" (Quad-Lens)
* **Location:** Canvas 1 (Systemic Policy) → Subtab: *"Pilot & Macro-Fiscal Deep-Dives"* → Select **"Lens 4: Macro-Fiscal & External Aid Reality"**.
* **What You See:**
  - The domestic expenditure gap (e.g., 18.4% Education vs 0.46% ICT in Kenya, a **40:1 domestic financing gap**).
  - The external aid asymmetry (**$1.84 Billion in education aid vs $52 Million in ICT aid**, a **35.4:1 external aid ratio** across 29,388 IATI transactions).
  - 8-year cumulative timeseries (2017–2024) and the 2020 COVID-19 emergency surge spike.

#### 3. Interactive 7-Country Discrepancy Heatmap & Triangulation Hub
* **Location:** Canvas 1 (Systemic Policy) → Scroll to the *"Interactive Discrepancy Heatmap"* section.
* **Interactivity:**
  - Toggle between **Afrobarometer Round 9** (2021–2023) and **Round 10** (2024–2025) panels to observe longitudinal shifts in citizen dissatisfaction.
  - Hover over cells to compare top-down macro metrics (World Bank/UIS) against frontline citizen reality.
  - Inspect Pillar 5 linguistic exclusion and commercial AI token tax benchmarks.

#### 4. Dual-Gatekeeping Readiness Check (Teacher & SMC Diagnostic)
* **Location:** Canvas 2 (Classroom Reality) → Select **"Tool 1: EdTech Readiness Check"**.
* **Interactivity:**
  - Complete the **Tier 1 Teacher Classroom Survivability screener** (7 feasibility constraints including electricity, personal airtime tax, pupil-device ratio, and language).
  - Complete the **Tier 2 SMC Safeguarding & Community Governance rubric** (data privacy, commercial ad tracking, e-waste lifecycle).
  - Click **"Generate Decision Memorandum"** to calculate composite feasibility and output an official PDF/printable memorandum (*Approved*, *Conditional*, or *Vetoed*).

#### 5. TaRL 3-Station Rotational Pedagogy Planner
* **Location:** Canvas 2 (Classroom Reality) → Select **"Tool 2: Rotation Planner"**.
* **Interactivity:** Enter total pupil cohort size (e.g., 50 or 80 pupils) and available working devices (e.g., 10 tablets). The engine dynamically generates a 3-station rotational timetable allocating students across:
  - *Station 1:* Direct Teacher Coaching (Foundational literacy/numeracy).
  - *Station 2:* Peer Collaborative Group Work (Unplugged manipulatives).
  - *Station 3:* Resilient Offline Digital Practice (Shared tablets/laptops).

#### 6. Resilient Digital Public Goods (DPG) Directory
* **Location:** Canvas 2 (Classroom Reality) → Select **"Tool 3: Resilient DPG Directory"**.
* **Interactivity:** Filter certified 100% offline educational solutions (Kolibri, Kiwix, African Storybook, PhET) by target learner segment (Primary, Secondary, Adult CPD) and deployment architecture (Raspberry Pi, Micro-SD, local Wi-Fi hotspot).

#### 7. KoboToolbox Field Survey Evidence Hub
* **Location:** Canvas 2 (Classroom Reality) → Select **"Tool 4: Community Evidence & Field Surveys"**.
* **Mode Switching:**
  - **Live Field Aggregates (`Real Data`):** Loads de-identified, allowlist-only field survey returns (`data/processed/survey_dashboard_live.json`) with automated small-group suppression ($N < 5$).
  - **Calibrated Demo Prior (`Demo Mode`):** Loads the statistically grounded simulation prior ($N = 800$) for demonstration and conference presentations.

#### 8. Standalone Mobile & Printable Toolkits
* **Teacher Mobile Screener:** Launch [`Teacher_Diagnostic_Survey.html`](./Teacher_Diagnostic_Survey.html) directly for an ultra-lightweight, mobile-responsive offline diagnostic.
* **High-Contrast Printable Packs:** Standalone printable HTML packs equipped with top print toolbars:
  - [`EdTech_Readiness_Check_Printable.html`](./EdTech_Readiness_Check_Printable.html) (Classroom screener + SMC checklist)
  - [`Rotation_Planner_Printable.html`](./Rotation_Planner_Printable.html) (Weekly TaRL 3-station rotational schedule)
  - [`Vetted_Solutions_Directory_Printable.html`](./Vetted_Solutions_Directory_Printable.html) (Vetted offline DPG catalog)

---

## 4. Core Analytical Modules Summary

The interactive platform synthesizes the research across several core analytical models:
* **The "Digital Recurrent Cliff" Quad-Lens:** Contrasts domestic education budgets against central ICT allocations (40:1 domestic financing gap) alongside external aid asymmetries (35.4:1 external aid gap across $1.84B education vs $52M ICT aid).
* **Subnational M-Lab Admin-1 QoS & Longitudinal Shift Detector:** D3 v7 choropleth maps displaying download/upload throughput and latency across 121 subnational Admin-1 divisions with automated 3m, 6m, and 12m change markers.
* **UNICEF-ITU Giga School Connectivity Layers:** Geospatial mapping of 21,000 schools across 7 economies with power availability and broadband categorization.
* **Interactive 7-Country Discrepancy Heatmap:** Triangulates Afrobarometer citizen perceptions (R9 $N = 11,169$, R10 $N = 11,200$) with macro-fiscal metrics.
* **Pillar 5 Linguistic Exclusion & AI Token Tax:** Downstream evaluation of commercial LLMs in indigenous African languages (AfroBench/IrokoBench).
* **KoboToolbox Field Evidence Hub:** Privacy-governed multi-instrument field survey repository with live allowlisted aggregates and calibrated demo preview.
* **Dual-Gatekeeping Screener & TaRL Rotation Planner:** Actionable tools for frontline educators and school management committees to audit feasibility and schedule device sharing.

---

## 5. Quick Start & Execution

### Running the Web Observatory Locally
```bash
# Serve the repository root over HTTP using the development server
python3 scripts/serve_dev.py 8000
# Or standard python module:
python3 -m http.server 8000
# Navigate to http://localhost:8000/
```

### Running the Automated Test Suite (52 Tests)
```bash
# Run root decision logic, macro-fiscal, and compiler tests
python3 -m pytest test_decision_logic.py test_compile_macro_fiscal_indicators.py -v

# Run subsystem unit tests (Kobo pipeline, Giga layers, privacy boundaries)
python3 -m unittest discover -s tests -v
```

### Running Data Harvesting & Pipeline Scripts
```bash
# Fetch and recompile domestic IMF GFS COFOG expenditures (2017–2024)
python3 scripts/fetch_imf_cofog.py --years 2017-2024

# Ingest official external development flows from IATI Datastore
python3 scripts/fetch_iati_funding.py --years 2017-2024

# Recompile the synthesized macro-fiscal dataset and Recurrent Cliff engine
python3 scripts/compile_macro_fiscal_indicators.py

# Ingest and detect statistical shifts across M-Lab subnational time series
python3 scripts/build_changes.py

# Build Giga school connectivity layers and QC report
python3 scripts/build_giga_layer.py

# Process Kobo survey submissions in safe demo mode (synthetic fixture)
python3 scripts/fetch_kobo_submissions.py --demo
python3 scripts/process_kobo_surveys.py --input-dir data/demo/kobo --output data/processed/survey_dashboard_demo.json
```

---

## 6. Data Governance, Ethics & Academic Integrity

* **Academic Mandate:** This project is licensed under the MIT License — see [`LICENSE`](./LICENSE). All research, models, and code are produced for non-commercial academic evaluation.
* **Privacy & De-identification:** The Kobo survey ingestion pipeline operates under strict fail-closed boundaries: raw respondent records, phone numbers, email addresses, precise GPS coordinates, school names, and free text are never committed to Git or exposed via public APIs (see [`KOBO_PIPELINE_CHANGELOG.md`](./KOBO_PIPELINE_CHANGELOG.md)).
* **Institutional Provenance:** Macro indicators originate from official institutional APIs (World Bank Open Data, UNESCO UIS, ITU WTIS, IMF GFS, IATI Datastore).
* **Citizen Voice Datasets:** Afrobarometer Rounds 9 & 10 datasets and Uwezo Citizen-Led Assessments are used in strict compliance with their respective research usage covenants.
* **Third-Party Intellectual Property:** Ookla Open Data cellular and fixed tiles are used strictly for non-commercial academic research under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0). Subnational administrative boundaries are derived from geoBoundaries (CC BY 4.0).
