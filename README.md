# Mapping EdTech Fit in Sub-Saharan Africa: A Six-Pillars Decision Observatory

[![Master Degree](https://img.shields.io/badge/Degree-Master%20in%20ICT4D-blue.svg)](https://www.unito.it/)
[![Academic Year](https://img.shields.io/badge/Academic%20Year-2025--2026-green.svg)](https://www.unito.it/)
[![Tests](https://img.shields.io/badge/Tests-33%2F33%20Passing-brightgreen.svg)](test_decision_logic.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Live Observatory](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue)](https://SunilRaman42.github.io/CC_3/)

> **Master in ICT for Development and Social Good (UniTO · COREP · Impactskills)**  
> **Academic Year:** 2025–2026  
> **Supervisor:** Prof. Elisa Bignante, Department of Cultures, Politics and Society, University of Turin  
> **Candidate Repository:** `SunilRaman42/CC_3` | **Live Web App:** [`https://SunilRaman42.github.io/CC_3/`](https://SunilRaman42.github.io/CC_3/)  

---

> [!IMPORTANT]
> **Detailed Work Summary Available:** For an exhaustive, up-to-date dossier detailing all research questions, data engineering pipelines, interactive decision tools, test suites, and git milestones completed to date, see [**`WORK_SUMMARY.md`**](./WORK_SUMMARY.md).

---

## 1. Project Overview

This repository hosts the academic research, data engineering pipelines, empirical field datasets, and interactive decision-support tools for the Master's Thesis investigating **Educational Technology (EdTech) fit across Sub-Saharan Africa (SSA)**.

The inquiry addresses why top-down digital education initiatives chronically collapse in low-resource African schools (the **"85% Pilot Graveyard"**). Grounded in **UNESCO's Six Pillars for the Digital Transformation of Education**, the project establishes a **Vertical Traceability Architecture** connecting three interdependent levels:
1. **Macro Lens:** Systemic public finance (IMF GFS COFOG), official development aid (IATI Datastore), and open data benchmarking across 48 Sub-Saharan African economies.
2. **Meso Lens:** Spatial schoolhouse connectivity (UNICEF-ITU Giga maps for 78,432 schools) and project portfolio tracking (237 World Bank digital education loans).
3. **Micro Lens:** Frontline classroom reality (Alliance of Alliances field surveys), dual-gatekeeping feasibility audits, 3-station rotational pedagogy (TaRL), and resilient offline Digital Public Goods (DPGs).

---

## 2. Core Repository Structure

| Component | Path / File | Purpose & Contents |
| :--- | :--- | :--- |
| **Comprehensive Work Summary** | [`WORK_SUMMARY.md`](./WORK_SUMMARY.md) | Exhaustive dossier summarizing all theoretical, architectural, and data milestones. |
| **Component A: Thesis Concept** | [`Thesis_First_Draft_Concept.md`](./Thesis_First_Draft_Concept.md) | Complete theoretical thesis concept, stakeholder matrices, and research methodology. |
| **Analytical Frameworks** | [`Analytical_Framework_Answers.md`](./Analytical_Framework_Answers.md) | Answers aligned with UniTO Analytical Framework 1 and 2 guidelines. |
| **Defense Dossier** | [`Defense_Talking_Points.md`](./Defense_Talking_Points.md) | Defense examiner Q&A, statutory citations, and academic justifications. |
| **Reference Notes & Citations** | [`reference_notes.md`](./reference_notes.md) | Statutory laws, peer-reviewed literature, and 6-Pillars mapping. |
| **Data Dictionary & Provenance** | [`DATA_DICTIONARY_AND_LOOKUP.md`](./DATA_DICTIONARY_AND_LOOKUP.md) | Registry of all macro/micro indicators, source APIs, vintages, and sample sizes. |
| **Component B: Web Observatory** | [`index.html`](./index.html) | Interactive 4-lens, 7-tool decision support web platform (12,000+ lines). |
| **Printable Offline Packs** | [`EdTech_Readiness_Check_Printable.html`](./EdTech_Readiness_Check_Printable.html)<br>[`Rotation_Planner_Printable.html`](./Rotation_Planner_Printable.html)<br>[`Vetted_Solutions_Directory_Printable.html`](./Vetted_Solutions_Directory_Printable.html) | Standalone printable packs for off-grid teachers, headteachers, and SMCs. |
| **Macro-Fiscal Pipelines** | [`fetch_imf_cofog.py`](./fetch_imf_cofog.py)<br>[`fetch_iati_funding.py`](./fetch_iati_funding.py)<br>[`compile_macro_fiscal_indicators.py`](./compile_macro_fiscal_indicators.py) | Ingests IMF COFOG outlays and 29,388 IATI aid transactions across Africa. |
| **6-Pillars Open Data Engine** | [`fetch_6pillars_pipeline.py`](./fetch_6pillars_pipeline.py) | Automated ingestion of World Bank WDI, UIS, and ITU indicator timeseries. |
| **Presentation Deck Automation** | [`build_checkin_deck.py`](./build_checkin_deck.py) | Generates `Project_Idea_Check-in.pptx` presentation slides. |

---

## 3. Interactive Decision Observatory Features (`index.html`)

The web deliverable incorporates four systemic lenses and seven interactive decision tools:
* **The "Digital Recurrent Cliff" Quad-Lens (Lens 4):** Contrasts domestic education budgets against central ICT allocations (e.g. 18.4% vs 0.46% in Kenya, a 40:1 domestic financing gap) alongside external aid asymmetries ($1.84B education aid vs $52M ICT aid, a ~35:1 gap), demonstrating an indicative macro proxy for why hardware donations lack sustainable operational counterpart budgets.
* **Dual-Gatekeeping Readiness Check:** Tier 1 Teacher Classroom Survivability (7-item feasibility screener) + Tier 2 SMC Safeguarding & Community Governance Rubric. Evaluates statutory veto thresholds (airtime tax, grid failure, TCO lifecycle deficit, minor data privacy breach) and outputs dynamic decision memoranda.
* **Classroom Rotation Planner:** Teaching at the Right Level (TaRL) 3-station rotational pedagogy (Direct Coaching, Peer Collaboration, Offline Device Station) making 50:1 pupil-teacher ratios manageable with only 10 shared devices.
* **Resilient DPG Directory:** Curated, 100% offline-ready Digital Public Goods (Kolibri, Kiwix, African Storybook, PhET) with monthly link verification.
* **Supply-Demand Discrepancy Matrix:** Evaluates 148 EdTech vendor architectures against 48 SSA demand environments.
* **Community Evidence Layer & Survey Codebook:** 104-item instrument codebook with calibrated baseline ($N = 800$ simulation seed) and live drag-and-drop ingestion computing all metrics dynamically without hardcoded outputs.
* **Qualitative Field Voice Carousel:** 16 verified quotes from teachers and innovators across SSA.

---

## 4. Quick Start & Verification

### Running the Web Observatory Locally
```bash
# Serve the repository root over HTTP
python3 -m http.server 8000
# Open http://localhost:8000/ in your browser
```

### Running the Automated Test Suite
```bash
pytest test_*.py -v
```
*(All 33 tests pass in ~1.4s across macro-fiscal compilers, IATI normalization, IMF COFOG parsers, gatekeeping veto logic, and rotation planner arithmetic).*

### Updating the Macro-Fiscal Data Pipeline
```bash
# Fetch IMF COFOG domestic public expenditures (2017-2024)
python3 fetch_imf_cofog.py --years 2017-2024

# Ingest IATI official aid transactions
python3 fetch_iati_funding.py --years 2017-2024

# Recompile the macro-fiscal indicators and Digital Recurrent Cliff dataset
python3 compile_macro_fiscal_indicators.py
```

---

## 5. License & Academic Integrity

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details. All datasets originate from official, publicly accessible institutional APIs and survey instruments (World Bank, UNESCO UIS, ITU, IMF GFS, IATI, UNICEF-ITU Giga, Uwezo, Afrobarometer, and Alliance of Alliances). Third-party cellular connectivity tiles derived from Ookla Open Data are used strictly for non-commercial academic research and master thesis evaluation under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0).
