# Mapping EdTech Fit in Sub-Saharan Africa: A Six-Pillars Decision Observatory

[![Master Degree](https://img.shields.io/badge/Degree-Master%20in%20ICT4D-blue.svg)](https://www.unito.it/)
[![Academic Year](https://img.shields.io/badge/Academic%20Year-2025--2026-green.svg)](https://www.unito.it/)
[![Tests](https://img.shields.io/badge/Tests-18%2F18%20Passing-brightgreen.svg)](test_compile_macro_fiscal_indicators.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live Observatory](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue)](https://rsnl42.github.io/CC_3/)

> **Master in ICT for Development and Social Good (UniTO · COREP · Impactskills)**  
> **Academic Year:** 2025–2026  
> **Supervisor:** Prof. Elisa Bignante, Department of Cultures, Politics and Society, University of Turin  
> **Candidate Repository:** `rsnl42/CC_3` | **Live Web App:** [`https://rsnl42.github.io/CC_3/`](https://rsnl42.github.io/CC_3/)  

---

> [!IMPORTANT]
> **Detailed Work Summary Available:** For an exhaustive, up-to-date dossier detailing all research questions, data engineering pipelines, interactive decision tools, test suites, and git milestones completed to date, see [**`WORK_SUMMARY.md`**](file:///workspaces/CC_3/WORK_SUMMARY.md).

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
| **Comprehensive Work Summary** | [`WORK_SUMMARY.md`](file:///workspaces/CC_3/WORK_SUMMARY.md) | Exhaustive dossier summarizing all theoretical, architectural, and data milestones. |
| **Component A: Thesis Concept** | [`Thesis_First_Draft_Concept.md`](file:///workspaces/CC_3/Thesis_First_Draft_Concept.md) | Complete theoretical thesis concept, stakeholder matrices, and research methodology. |
| **Analytical Frameworks** | [`Analytical_Framework_Answers.md`](file:///workspaces/CC_3/Analytical_Framework_Answers.md) | Answers aligned with UniTO Analytical Framework 1 and 2 guidelines. |
| **Defense Dossier** | [`Defense_Talking_Points.md`](file:///workspaces/CC_3/Defense_Talking_Points.md) | Defense examiner Q&A, statutory citations, and academic justifications. |
| **Reference Notes & Citations** | [`reference_notes.md`](file:///workspaces/CC_3/reference_notes.md) | Statutory laws, peer-reviewed literature, and 6-Pillars mapping. |
| **Data Dictionary** | [`DATA_DICTIONARY_AND_LOOKUP.md`](file:///workspaces/CC_3/DATA_DICTIONARY_AND_LOOKUP.md) | Registry of all macro and micro indicators, source APIs, and sample sizes. |
| **Component B: Web Observatory** | [`index.html`](file:///workspaces/CC_3/index.html) | Interactive 4-lens, 7-tool decision support web platform (12,000+ lines). |
| **Printable Offline Packs** | [`EdTech_Readiness_Check_Printable.html`](file:///workspaces/CC_3/EdTech_Readiness_Check_Printable.html)<br>[`Rotation_Planner_Printable.html`](file:///workspaces/CC_3/Rotation_Planner_Printable.html)<br>[`Vetted_Solutions_Directory_Printable.html`](file:///workspaces/CC_3/Vetted_Solutions_Directory_Printable.html) | Standalone printable packs for off-grid teachers, headteachers, and SMCs. |
| **Macro-Fiscal Pipelines** | [`fetch_imf_cofog.py`](file:///workspaces/CC_3/fetch_imf_cofog.py)<br>[`fetch_iati_funding.py`](file:///workspaces/CC_3/fetch_iati_funding.py)<br>[`compile_macro_fiscal_indicators.py`](file:///workspaces/CC_3/compile_macro_fiscal_indicators.py) | Ingests IMF COFOG outlays and 29,388 IATI aid transactions across Africa. |
| **6-Pillars Open Data Engine** | [`fetch_6pillars_pipeline.py`](file:///workspaces/CC_3/fetch_6pillars_pipeline.py) | Automated ingestion of World Bank WDI, UIS, and ITU indicator timeseries. |
| **Presentation Deck Automation** | [`build_checkin_deck.py`](file:///workspaces/CC_3/build_checkin_deck.py) | Generates `Project_Idea_Check-in.pptx` presentation slides. |

---

## 3. Interactive Decision Observatory Features (`index.html`)

The web deliverable incorporates four systemic lenses and seven interactive decision tools:
* **The "Digital Recurrent Cliff" Quad-Lens (Lens 4):** Contrasts domestic education budgets against central ICT allocations (e.g. 18.4% vs 0.46% in Kenya) alongside 29,388 external aid transactions, demonstrating why hardware donations create unfunded operational liabilities.
* **Dual-Gatekeeping Readiness Check:** Tier 1 Teacher Classroom Survivability (7-item feasibility screener) + Tier 2 SMC Safeguarding & Community Governance Rubric. Outputs dynamic decision memoranda.
* **Classroom Rotation Planner:** Teaching at the Right Level (TaRL) 3-station rotational pedagogy (Direct Coaching, Peer Collaboration, Offline Device Station) making 50:1 pupil-teacher ratios manageable with only 10 shared devices.
* **Resilient DPG Directory:** Curated, 100% offline-ready Digital Public Goods (Kolibri, Kiwix, African Storybook, PhET) with monthly link verification.
* **Supply-Demand Discrepancy Matrix:** Evaluates 148 EdTech vendor architectures against 48 SSA demand environments.
* **Community Evidence Layer & Survey Codebook:** 104-item instrument codebook with calibrated baseline ($N = 800$) and live drag-and-drop ingestion.
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
*(All 18 tests pass in ~1.2s across macro-fiscal compilers, IATI normalization, and IMF COFOG parsers).*

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

This project is licensed under the MIT License — see the [LICENSE](file:///workspaces/CC_3/LICENSE) file for details. All datasets originate from official, publicly accessible institutional APIs and survey instruments (World Bank, UNESCO UIS, ITU, IMF GFS, IATI, UNICEF-ITU Giga, Uwezo, Afrobarometer, and Alliance of Alliances).
