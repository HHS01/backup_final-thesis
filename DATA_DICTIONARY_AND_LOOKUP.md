# EdTech Observatory: Data Dictionary & Indicator Lookup Registry

This registry provides a complete, auditable mapping of every indicator, metric, source dataset, sample size, file path, and recency used across the Observatory and Master's Thesis.

---

## 1. Summary of Processed Data Assets

| File Path | Description | Engine / Generator Script | Geographical Scope | Sample Size / Units | Primary Year(s) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `data/processed/latest_country_profiles_6pillars.csv` | Wide matrix of UNESCO 6-Pillars macro indicators | `fetch_6pillars_pipeline.py` | 48 SSA nations (focus subset of 69 panel) | 69 country records | 2015–2024 (Latest: 2023–24) |
| `data/processed/indicators_timeseries.csv` | Tidy long-format timeseries across all 6 pillars | `fetch_6pillars_pipeline.py` | 69 nations | 11,393 observations | 2015–2024 |
| `data/processed/wb_digital_education_projects.csv` | Active World Bank digital learning financing loans | `fetch_6pillars_pipeline.py` | 69 nations | 237 investment projects | Active portfolio |
| `data/processed/afrobarometer_{ISO3}_r9.json` | Citizen demand, national problem ranking, delivery satisfaction | `scripts/extract_afrobarometer_education.py` | 6 SSA economies (KEN, TZA, GHA, NGA, ZMB, MUS) | N = 11,169 citizens (weighted) | 2021–2023 (Round 9 Merged Panel) |
| `data/processed/afrobarometer_{ISO3}_r10.json` | Longitudinal citizen sentiment & government performance comparison | `scripts/extract_afrobarometer_education.py` | 6 SSA economies (KEN, TZA, GHA, NGA, ZMB, MUS) | N = 11,200 citizens (weighted) | 2024–2025 (Round 10 Merged Panel) |
| `data/processed/uwezo_KEN_latest.json` | Foundational literacy/numeracy & household devices | `scripts/extract_citizen_assessments.py` | Kenya (National, Urban, Rural, Sex) | N = 135,000 children | 2021–2023 (6th/7th Assessments) |
| `data/processed/uwezo_TZA_latest.json` | Foundational literacy/numeracy & household devices | `scripts/extract_citizen_assessments.py` | Tanzania (National, Urban, Rural, Sex) | N = 108,000 children | 2021–2023 (Twaweza Uwezo Assessments) |
| `data/processed/academic_learning_benchmarks.json` | Standardized foundational learning proficiencies | `scripts/fetch_academic_benchmarks.py` | 7 focus economies | Harmonized proficiencies | 2021–2024 (SACMEQ, PASEC, Uwezo) |
| `data/processed/modality_reach_KEN.json` | Empirical delivery reach, access & friction indices | `scripts/compile_modality_reach.py` | Kenya | Multi-study synthesis | 2020–2024 |
| `data/processed/interactive_triangulation_heatmap.json` | 7-country triangulation bridging macro claims with citizen reality | `scripts/generate_interactive_heatmap.py` | 7 focus economies | Multi-metric matrix | 2021–2025 |
| `data/processed/afrobarometer_triangulation.json` | Citizen vs official infrastructure access comparison | `scripts/run_monthly_triangulation.py` | 6 focus economies | Aggregated indicators | 2021–2025 |
| `data/processed/connectivity/ookla_tiles_*.csv` | Ground-truth network speed, latency & device tests (mobile + fixed) | `scripts/fetch_connectivity_data.py` | 7 economies (KEN, RWA, TZA, GHA, NGA, ZMB, MUS) | 41,754 spatial tiles (2024 Q1) | 2024 Q1 (Ookla Open Data, CC BY-NC-SA 4.0) |
| `data/processed/connectivity/mlab/*.csv` | Measurement Lab NDT download/upload speed and latency | `scripts/fetch_mlab.py` | 7 economies (KEN, GHA, MUS, NGA, RWA, TZA, ZMB) | Monthly Admin-1 samples | 2020–2024 (M-Lab NDT) |
| `out/dashboard/{ISO3}.geojson` | Rewound GeoJSON boundary polygons for Admin-1 regions | `scripts/build_dashboard_data.py` | 7 focus economies | Subnational polygons | geoBoundaries ADM1 |
| `out/dashboard/{ISO3}.series.json` | Monthly time series of subnational QoS metrics | `scripts/build_dashboard_data.py` | 7 focus economies | Monthly metrics per Admin-1 | 2020–2024 |
| `out/dashboard/{ISO3}.changes.json` | 3-month, 6-month, and 12-month statistical shift detections | `scripts/build_changes.py` | 7 focus economies | Trend markers | 2020–2024 |
| `out/dashboard/{ISO3}_schools.json` | GeoJSON schoolhouse connectivity layers | `scripts/build_giga_layer.py` | 7 focus economies | 3,000 schools / country (21,000 total) | 2024–2026 (Giga schema) |
| `out/giga_qc.json` | School connectivity quality control audit and distributions | `scripts/build_giga_layer.py` | 7 focus economies | Multi-metric audit | 2024–2026 |
| `out/boundaries/crosswalk.csv` | Crosswalk matching M-Lab subdivision codes with geoBoundaries | `scripts/fetch_boundaries.py` | 7 focus economies | 121 administrative units | ISO 3166-2 / geoBoundaries |
| `data/processed/survey_dashboard_live.json` | De-identified, allowlist-only field survey aggregates | `scripts/process_kobo_surveys.py` | Active survey respondents | Aggregated distributions (PII scrubbed) | 2026 (KoboToolbox live) |
| `data/processed/survey_data_calibrated.json` | Calibrated baseline synthesis & fallback demo priors | `scripts/process_survey_data_calibrated.py` | 48 SSA nations | N = 800 respondents | 2024–2026 (Demo seed) |
| `data/processed/supply_demand_matrix_data.js` | 48 SSA Demand vs 148 Supply Matrix with proxy badges | `scripts/build_matrix_dataset.py` | 48 SSA nations & 148 EdTech players | 48 countries × 148 players | 2024–2026 |

---

## 2. Macro Indicators: UNESCO 6 Pillars (`fetch_6pillars_pipeline.py`)

All indicators originate from the **World Bank World Development Indicators (WDI)**, **UNESCO Institute for Statistics (UIS)**, and **International Telecommunication Union (ITU)** APIs.

### Pillar 1: Coordination and Leadership
| Indicator Code | Full Indicator Name | Source Agency | Unit / Scale | Kenya Latest Value (Year) |
| :--- | :--- | :--- | :--- | :--- |
| `SE.XPD.TOTL.GD.ZS` | Government expenditure on education (% of GDP) | World Bank / UIS | % | 4.02% (2024) |
| `SE.XPD.TOTL.GB.ZS` | Government expenditure on education (% of total budget) | World Bank / UIS | % | 27.92% (2024) |
| `SE.XPD.CTOT.ZS` | Current education expenditure (% of total public education spend) | World Bank / UIS | % (OpEx vs CapEx) | 92.54% (2015) |
| `IQ.SPI.OVRL` | Statistical Performance Indicators (SPI) overall score | World Bank | Score (0–100) | 73.36 (2024) |

### Pillar 2: Connectivity and Infrastructure
| Indicator Code | Full Indicator Name | Source Agency | Unit / Scale | Kenya Latest Value (Year) |
| :--- | :--- | :--- | :--- | :--- |
| `EG.ELC.ACCS.ZS` | Access to electricity (% of population) | World Bank / SE4ALL | % | 77.00% (2024) |
| `EG.ELC.ACCS.RU.ZS` | Access to electricity, rural (% of rural population) | World Bank / SE4ALL | % | 67.10% (2024) |
| `EG.ELC.ACCS.UR.ZS` | Access to electricity, urban (% of urban population) | World Bank / SE4ALL | % | 98.10% (2024) |
| `UIS.SCHBSP.1.WELEC`| Proportion of primary schools with access to electricity | UNESCO UIS | % | 82.62% (2016) |
| `IT.NET.USER.ZS` | Individuals using the Internet (% of population) | ITU / World Bank | % | 34.98% (2024) |
| `IT.CEL.SETS.P2` | Mobile cellular subscriptions (per 100 people) | ITU / World Bank | Subscriptions / 100 | 126.48 (2024) |
| `IT.NET.BBND.P2` | Fixed broadband subscriptions (per 100 people) | ITU / World Bank | Subscriptions / 100 | 3.04 (2024) |

### Pillar 3: Cost and Sustainability
| Indicator Code | Full Indicator Name | Source Agency | Unit / Scale | Kenya Latest Value (Year) |
| :--- | :--- | :--- | :--- | :--- |
| `NY.GDP.PCAP.CD` | GDP per capita (current US$) | World Bank | US$ | $2,133.46 (2024) |
| `NY.GDP.PCAP.PP.CD`| GDP per capita, PPP (current international $) | World Bank | Int$ | $6,649.68 (2024) |
| `SE.XPD.PRIM.PC.ZS` | Gov expenditure per primary student (% of GDP per capita) | World Bank / UIS | % | 10.95% (2015) |
| `SE.XPD.SECO.PC.ZS` | Gov expenditure per secondary student (% of GDP per capita) | World Bank / UIS | % | 19.30% (2015) |

### Pillar 4: Capacity and Culture
| Indicator Code | Full Indicator Name | Source Agency | Unit / Scale | Kenya Latest Value (Year) |
| :--- | :--- | :--- | :--- | :--- |
| `SE.LPV.PRIM` | Learning Poverty Rate (% children end-of-primary below min reading) | World Bank / UIS | % | **79.29% (2023)** |
| `SE.LPV.PRIM.SD` | Primary school-age children out-of-school (%) | World Bank / UIS | % | **18.77% (2023)** |
| `SE.PRM.ENRL.TC.ZS` | Pupil-teacher ratio, primary | World Bank / UIS | Ratio (Pupils:Teacher)| 30.65:1 (2015) |
| `SE.PRM.TCAQ.ZS` | Trained teachers in primary education (% of total) | World Bank / UIS | % | 100.0% (2023) |
| `SE.ADT.LITR.ZS` | Adult literacy rate (% ages 15+) | World Bank / UIS | % | 82.60% (2022) |

### Pillar 5: Content and Solutions
| Indicator Code | Full Indicator Name | Source Agency | Unit / Scale | Kenya Latest Value (Year) |
| :--- | :--- | :--- | :--- | :--- |
| `con30e.s` | Accessed online information to learn/educate (% users 15+) | World Bank Global Findex | % | 65.56% (2024) |
| `IT.NET.SECR.P6` | Secure Internet servers (per 1 million people) | Netcraft / World Bank | Count / 1M people | 399.70 (2024) |
| `TM.VAL.ICTG.ZS.UN` | ICT goods imports (% of total goods imports) | UN Comtrade / WB | % | 3.03% (2023) |

### Pillar 6: Data and Evidence
| Indicator Code | Full Indicator Name | Source Agency | Unit / Scale | Kenya Latest Value (Year) |
| :--- | :--- | :--- | :--- | :--- |
| `IQ.SPI.OVRL` | Statistical Performance Indicators (SPI) overall score | World Bank | Score (0–100) | 73.36 (2024) |
| `IQ.SPI.PIL1` | SPI Pillar 1: Data use score | World Bank | Score (0–100) | 90.00 (2024) |
| `IQ.SPI.PIL5` | SPI Pillar 5: Data infrastructure and standards score | World Bank | Score (0–100) | 80.00 (2024) |

---

## 3. Subnational M-Lab Admin-1 QoS & Longitudinal Shift Layer

* **Source Agency:** Measurement Lab (M-Lab) Network Diagnostic Tool (NDT) & geoBoundaries.
* **Geographical Coverage:** 7 Focus Economies (KEN, GHA, MUS, NGA, RWA, TZA, ZMB) spanning 121 Admin-1 subnational jurisdictions.
* **Temporal Horizon:** Monthly time series from January 2020 through late 2024.
* **Generator Pipeline:** `scripts/fetch_mlab.py`, `scripts/fetch_boundaries.py`, `scripts/build_dashboard_data.py`, `scripts/build_changes.py`.

### Admin-1 Quality of Service (QoS) Indicators

| Variable / Metric | Technical Definition | Unit | Sampling & Aggregation |
| :--- | :--- | :--- | :--- |
| `download_mbps` | Median downstream throughput measured by NDT client | Megabits per second (Mbps) | Monthly median per Admin-1 subdivision |
| `upload_mbps` | Median upstream throughput measured by NDT client | Megabits per second (Mbps) | Monthly median per Admin-1 subdivision |
| `rtt_ms` | Median round-trip time (latency) between client and nearest M-Lab server | Milliseconds (ms) | Monthly median per Admin-1 subdivision |
| `sample_count` | Number of valid completed NDT diagnostic tests | Integer count | Monthly total per Admin-1 subdivision |
| `change_3m_pct` | Relative percentage shift in throughput/latency over preceding 3 months | % ($\Delta$) | $(M_0 - M_{-3}) / M_{-3} \times 100$ |
| `change_6m_pct` | Relative percentage shift in throughput/latency over preceding 6 months | % ($\Delta$) | $(M_0 - M_{-6}) / M_{-6} \times 100$ |
| `change_12m_pct` | Year-over-year relative percentage shift over preceding 12 months | % ($\Delta$) | $(M_0 - M_{-12}) / M_{-12} \times 100$ |

---

## 4. UNICEF-ITU Giga School Connectivity Dataset Schema

* **Reference Schema:** UNICEF-ITU Giga Global School Mapping Architecture.
* **Output Path:** `out/dashboard/{ISO3}_schools.json` and `out/giga_qc.json`.
* **Scope:** 21,000 schools across 7 focus economies (3,000 schools per country).

### Schoolhouse Feature Properties

| Property Name | Data Type | Permitted Values / Description | Analytical Function in Decision Models |
| :--- | :--- | :--- | :--- |
| `school_id` | String | Unique ISO-based identifier (e.g., `KEN-SCH-00042`) | Deterministic cross-referencing and spatial joining. |
| `school_name` | String | De-identified institutional name | Institutional display in local drill-down panels. |
| `lat` / `lon` | Float | WGS84 Geographic coordinates | Geospatial mapping and distance-to-tower analysis. |
| `admin1_code` | String | ISO 3166-2 subnational code (e.g., `KE-30`) | Aggregation into Admin-1 choropleths and crosswalks. |
| `connectivity_status` | String | `connected`, `partial`, `unconnected` | Governs Gatekeeping Tier 1 veto logic (connectivity availability). |
| `download_speed` | Float | Measured or modeled throughput in Mbps | Evaluates video streaming vs text-only pedagogical feasibility. |
| `electricity_status` | String | `grid`, `solar`, `generator`, `none` | Governs battery duty cycles and TaRL rotation device charging feasibility. |
| `coverage_type` | String | `4G`, `3G`, `2G`, `fiber`, `none` | Informs offline DPG requirement (Sneakernet vs Wi-Fi cache). |

---

## 5. Ground-Truth Layer 1: Citizen Voice (Afrobarometer Round 9 & 10 Merged Panels)

* **Sources:** Afrobarometer Round 9 (2021–2023) and Round 10 (2024–2025) National Surveys across 6 focus economies.
* **Sample Size:** $N = 11,169$ (Round 9) and $N = 11,200$ (Round 10) adult citizens (weighted with within-country demographic weights).
* **Generator:** `scripts/extract_afrobarometer_education.py`.

| Indicator / Concept | Question Code | Weighted National (%) | Urban (%) | Rural (%) | Analytical Meaning |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Education in Top 3 Priorities** | `Q45PT1–3` (Code 14) | **18.59%** (KEN R9) | **15.97%** | **19.96%** | Rural citizens rate education quality/access as an acute emergency higher than urban peers. |
| **Education as #1 Priority** | `Q45PT1` (Code 14) | **4.54%** (KEN R9) | **3.10%** | **5.32%** | Share naming education as their single most urgent national problem. |
| **Delivery Handled Well** | `Q46H` ("Fairly/Very Well") | **63.79%** (KEN R9) | **69.11%** | **61.03%** | Public satisfaction with state handling of educational needs. |
| **Delivery Handled Badly** | `Q46H` ("Fairly/Very Badly") | **36.21%** (KEN R9) | **30.89%** | **38.97%** | Acute rural dissatisfaction with education delivery. |
| **Electricity Grid Connection** | `Q93A` (Presence of Grid) | **76.2%** (KEN R10) | **95.1%** | **64.3%** | Ground-truth household access vs official national statistics. |

---

## 6. Ground-Truth Layer 2: Citizen Assessments (Uwezo Kenya & Tanzania)

* **Sources:** Usawa Agenda (Uwezo Kenya 6th & 7th National Learning Assessments, 2021–2023) and Twaweza East Africa (Uwezo Tanzania National Learning Assessments, 2021–2023).
* **Sample Size:** $N = 135,000$ assessed children across Kenya; $N = 108,000$ assessed children across Tanzania Mainland ($N = 243,000$ combined).
* **Generator:** `scripts/extract_citizen_assessments.py`.

### Comparative Uwezo Foundational Learning Benchmarks

| Metric | Target Population | Kenya National (Rural) | Tanzania National (Rural) | Analytical Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **Foundational Literacy** | Grade 3–5 pupils reading Grade 2 story | **41.6%** (36.8%) | **52.0%** (44.0%) | High learning poverty; hardware-first initiatives bypass basic literacy prerequisites. |
| **Foundational Numeracy** | Grade 3–5 pupils solving Grade 2 arithmetic | **46.8%** (42.4%) | **51.5%** (45.2%) | Over half of primary students lack foundational numeracy. |
| **Out-of-School Rate** | Children ages 6–16 not enrolled | **8.5%** (10.1%) | **9.2%** (11.4%) | Severe regional variance (>25% in arid pastoral counties). |
| **Household Radio** | All households owning working radio | **62.0%** (59.0%) | **69.0%** (67.0%) | Dominant broadcast reach for remote audio instruction. |
| **Household Television** | All households owning working TV | **45.0%** (32.0%) | **28.0%** (12.0%) | Severe rural exclusion from video-based digital learning. |
| **Household Mobile Phone** | All households owning mobile phone | **91.0%** (88.0%) | **88.0%** (83.0%) | Universal penetration enabling SMS/USSD and micro-learning. |

---

## 7. Delivery Modality & Friction Layer (`modality_reach_KEN.json`)

* **Sources:** CEGA Busia Remote Learning Evaluation, Uwezo household surveys, GSMA 2025, ITU/A4AI Price Baskets.
* **Output Path:** `data/processed/modality_reach_KEN.json`

| Modality Name | Typical Examples | Empirical Reach (%) | Household Access (%) | Friction Index (1–5) | Key Operational Bottleneck |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Broadcast Radio** | Interactive Radio Instruction, KBC lessons | **31.5%** | **62.0%** | **1.3 / 5.0** | Lowest barrier; portable, battery/solar operable. |
| **Educational Television** | Ubongo Kids, Akili and Me, EDU TV | **26.0%** | **45.0%** | **2.0 / 5.0** | Mains power dependency; 32% rural access limit. |
| **Basic SMS / USSD** | Eneza Shupavu291, Arifu | **18.0%** | **91.0% (Phone)** | **1.5 / 5.0** | High reach; airtime micro-costs limit long sessions. |
| **Asynchronous Offline / Sneakernet** | Kolibri on Raspberry Pi, SD cards, RACHEL | *No empirical macro data* | N/A | **2.0 / 5.0** | High initial hardware setup; zero recurring data cost. |
| **Mobile App / Web LMS** | uLesson, Google Classroom, Zeraki | *0% empirical reach* | <15% (Laptops/Broadband) | **2.6 / 5.0** | Prohibitive daily data costs; requires smartphones. |
| **Generative AI / Cloud AI** | ChatGPT, AI tutors | *0% empirical reach* | <5% | **2.6 / 5.0** | Severe language degradation in Swahili/vernacular. |
| **Any Platform Combined** | Used at least one tool during closures | **67.0%** | N/A | N/A | Busia empirical benchmark. |

---

## 8. KoboToolbox Field Survey Hub & Privacy Boundary Specification

* **Protocol Definitions:** `AoA survey/xlsform/*.xlsx` (Teacher, Provider, Expert, Follow-up).
* **Ingestion Pipelines:** `scripts/fetch_kobo_submissions.py` and `scripts/process_kobo_surveys.py`.
* **Security & Audit Log:** `KOBO_PIPELINE_CHANGELOG.md`.

### Survey Instrument Architecture & 6-Pillars Mapping

| Instrument Protocol | Total Items | Mapped UNESCO Pillars | Key Quantifiable Variables | Primary Methodological Focus |
| :--- | :--- | :--- | :--- | :--- |
| **Teacher Survey** (`SSA_Teacher_Survey_v1_EN_XLSForm.xlsx`) | **40 Items** | Pillars 1, 2, 3, 4, 5, 6 | `elecByLocation`, `internetDist`, `deviceDist`, `aiFrequency`, `aiConfidence` | Grid reliability, personal airtime taxation, hardware scarcity, time-on-task, vernacular AI accuracy. |
| **Provider Survey** (`SSA_Provider_Survey_v1_EN_XLSForm.xlsx`) | **33 Items** | Pillars 1, 2, 3, 4, 5 | `deviceDist`, `offlineDist`, `monetization`, `grantDep` | Form factor (mobile vs laptop), offline-first caching, business model grant dependency. |
| **Expert Consultation** (`SSA_Expert_Consultation_R1_v1_EN_XLSForm.xlsx`) | **31 Items** | Pillars 1, 2, 3, 4, 6 | `donorExitDist`, `procurementDrivers`, `curriculumFit`, `safeguardEnforcement` | Post-grant sustainability cliff, political ribbon-cutting, child data protection enforcement. |
| **Follow-up Opt-in** (`SSA_Followup_Contact_Optin_v1_EN_XLSForm.xlsx`) | **8 Items** | Governance / Ethics | `contact_email`, `contact_phone`, `interview_consent` | **Strictly excluded from all public aggregates and dashboards.** |

### Privacy Boundary & De-identification Rules
1. **Zero Raw Storage in Repo:** Raw submissions are fetched only to temporary runtime storage (`RUNNER_TEMP`) and never committed to Git.
2. **Strict Allowlist Processing:** The normalizer extracts exclusively approved numerical choice codes. All respondent IDs, school names, telephone numbers, emails, and free-text fields are discarded.
3. **Small-Group Suppression:** If any subnational or categorical grouping contains fewer than **5 respondents**, the distribution is suppressed to prevent deductive re-identification.
4. **Demo Mode Isolation:** Explicit `--demo` mode generates synthetic fixtures in `data/demo/kobo` with `sub_t_`, `sub_p_` prefixes. Real and demo records are never combined.

---

## 9. Macro-Fiscal & External Aid Observatory Layer (`data/processed/macro_fiscal_data.js` & `.json`)

* **Engines:** `scripts/fetch_imf_cofog.py`, `scripts/fetch_iati_funding.py`, `scripts/compile_macro_fiscal_indicators.py`.
* **Coverage Scope:** All 54 African economies (intensive deep-dive analytics across 7 focus economies).
* **Time Horizon:** 2017–2024 annual time series.

### Core Macro-Fiscal & Aid Indicators

| Metric / Indicator Code | Metric Definition | Source Agency | Empirical Finding (Kenya Baseline) | Analytical Meaning / Digital Recurrent Cliff |
| :--- | :--- | :--- | :--- | :--- |
| `COFOG 709 Share` | General government education outlays (% of total outlays) | IMF GFS COFOG | **18.4%** | Shows strong domestic political commitment to national schooling in aggregate public budgets. |
| `COFOG 7047 Share` | General government communication/ICT outlays (% of total outlays) | IMF GFS COFOG | **0.46%** | Less than 0.5% of total budget is allocated to central communications and telecom infrastructure. |
| `Dual Expenditure Gap (Domestic)` | Ratio of Domestic Education Outlays to Central ICT Outlays | Derived (`COFOG 709 / 7047`) | **40 : 1** | Demonstrates that national education spending exceeds central ICT spending by 40:1. Serves as a macro-level financing asymmetry proxy. |
| `External Aid Asymmetry (Aid Flows)` | Ratio of Cumulative External Education Aid to External ICT Aid | Derived (`IATI CRS 111-114 / 220`) | **35.4 : 1** ($1.84B vs $52M across 7 economies) | Demonstrates that external development finance heavily favors educational program transfers over telecom infrastructure by 35.4:1. |
| `IATI Total Education Aid` | Cumulative external aid commitments/disbursements to education (2017–2024) | IATI Datastore (CRS 111, 112, 113, 114) | **$1.84 Billion** (Across 7 economies) | Heavy external donor subsidization of pedagogical initiatives and school capital projects. |
| `IATI Total ICT Aid` | Cumulative external aid to telecommunications/ICT (2017–2024) | IATI Datastore (CRS 220) | **$52 Million** (Across 7 economies) | External ICT aid is less than 3% of education aid, illustrating the telecommunications funding gap. |
| `2020 COVID Surge Ratio` | Ratio of 2020 emergency external disbursements to 2019 pre-pandemic baseline | IATI Datastore | **1.85× to 3.20×** | Emergency donor surges financed rapid remote learning pilots that suffered contraction post-pandemic. |

> [!NOTE]
> **Macro Proxy Scope & Methodological Caveats:**
> COFOG 7047 (Communication) and IATI Sector 220 (Telecommunications) capture *national central communications infrastructure* rather than line-item school-level recurrent operational costs (such as local device repair, battery replacements, or monthly classroom SIM airtime). These figures are indicative macro-level financing proxies illustrating structural capital-versus-operational asymmetry, rather than direct causal proof of school-level pilot collapse. Granular public-expenditure databases (such as World Bank BOOST) represent the logical next micro-level proxy for disaggregated school-level recurrent versus capital budget lines.

---

## 10. Headline Statistics Provenance Registry

Every headline statistic cited in the thesis concept, analytical frameworks, and decision observatory is registered below with its originating agency, formal definition, measurement vintage, and denominator boundaries:

| Headline Statistic | Source Agency & Academic Citation | Vintage | Formal Definition & Measurement Scope | Denominator & Sampling Boundaries |
| :--- | :--- | :--- | :--- | :--- |
| **85% Pilot Graveyard** | World Bank EduTech (Trucano, 2013, 2016); Unwin (*ICT4D*, 2009; 2019) | 2016, 2019 | Proportion of donor-funded digital education initiatives that contract severely or cease operations within 18 months post-grant. | Donor-funded EdTech pilot projects across Sub-Saharan Africa without ring-fenced domestic recurrent budget line absorption. |
| **80%–90% Digital Budget on Hardware** | UNESCO Global Education Monitoring (GEM) Report; Kenya Auditor General DLP Performance Audit | 2019, 2023 | Share of initial digital learning capital procurement spent exclusively on physical devices (tablets/laptops). | Capital expenditure (CapEx) component of national educational technology rollouts; excludes ongoing maintenance and training. |
| **0.56% Median School Broadband** | UNICEF-ITU Giga School Connectivity Initiative; ITU WTIS Indicators | 2023–2024 | Median proportion of rural public primary schools with verified $\ge 10\text{ Mbps}$ broadband internet connectivity. | Rural public primary schools surveyed across Giga mapping partner countries in Sub-Saharan Africa. |
| **4%–8% Informal Teacher Salary Tax** | GSMA Mobile for Development; Uwezo East Africa Frontline Educator Surveys | 2021, 2023 | Share of monthly net teacher salary expended personally on commercial cellular data bundles to upload school administrative returns. | Frontline public primary teachers in schools without state-funded institutional internet or active zero-rating covenants. |
| **18%–38% African Language LLM Accuracy** | AfroBench / Masakhane NLP / IrokoBench Benchmarks (Ogueji et al., 2023; Adelani et al., 2024) | 2023–2024 | Downstream diagnostic and comprehension task accuracy of frontier commercial LLMs in major African languages vs. $\ge 88\%$ in English. | Benchmarked across major regional African languages (Swahili, Hausa, Yoruba, Amharic, isiZulu). |
| **70.8% Products vs. 82.5% Rural Schools** | *Dual Denominator Finding:* Supply-Demand Discrepancy Matrix ($N=148$) vs. World Bank/UNESCO Rural Baseline | 2024 | **Product Denominator ($N=148$):** 70.8% of surveyed EdTech products require continuous smartphone/tablet and broadband connectivity.<br>**School Denominator ($N=\text{SSA rural schools}$):** 82.5% of rural public schools lack reliable grid power or broadband. | **Crucial Denominator Separation:** Contrasts the technical architectural assumptions of vendor offerings against rural structural classroom realities. |
| **87% Learning Poverty Rate** | World Bank & UNESCO Institute for Statistics (UIS) Joint Learning Poverty Report | 2022 | Proportion of 10-year-olds in Sub-Saharan Africa unable to read and understand a simple narrative text. | Regional aggregate for Sub-Saharan Africa; composite of out-of-school rate and below-minimum-reading-proficiency rate. |
| **Kenya 78,432 Verified Schools** | Kenya Ministry of Education Basic Education Statistical Booklet / NEMIS Registry / Giga Project | 2020–2022 | Total census count of all registered basic education learning institutions in Kenya. | **Institutional Composition:** Includes Early Childhood Development Education (ECDE pre-primary: ~46,530), primary schools (~32,437), and secondary schools (~10,487), spanning both public and registered private sectors. |
