# EdTech Observatory: Data Dictionary & Indicator Lookup Registry

This registry provides a complete, auditable mapping of every indicator, metric, source dataset, sample size, file path, and recency used across the Observatory and Master's Thesis.

---

## 1. Summary of Processed Data Assets

| File Path | Description | Engine / Generator Script | Geographical Scope | Sample Size / Units | Primary Year(s) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `data/processed/latest_country_profiles_6pillars.csv` | Wide matrix of UNESCO 6-Pillars macro indicators | `fetch_6pillars_pipeline.py` | 69 nations (48 SSA, 21 MENA) | 69 country records | 2015–2024 (Latest: 2023–24) |
| `data/processed/indicators_timeseries.csv` | Tidy long-format timeseries across all 6 pillars | `fetch_6pillars_pipeline.py` | 69 nations | 11,393 observations | 2015–2024 |
| `data/processed/wb_digital_education_projects.csv` | Active World Bank digital learning financing loans | `fetch_6pillars_pipeline.py` | 69 nations | 237 investment projects | Active portfolio |
| `data/processed/afrobarometer_KEN_r9.json` | Citizen demand, school problems, public satisfaction | `scripts/extract_afrobarometer_education.py` | Kenya (National, Urban, Rural) | N = 2,400 adult citizens | 2022–2023 (Round 9) |
| `data/processed/uwezo_KEN_latest.json` | Foundational literacy/numeracy & household devices | `scripts/extract_citizen_assessments.py` | Kenya (National, Urban, Rural, Sex) | N = 135,000 children | 2021–2023 (6th/7th Assessments) |
| `data/processed/modality_reach_KEN.json` | Empirical delivery reach, access & friction indices | `scripts/compile_modality_reach.py` | Kenya | Multi-study synthesis | 2020–2024 |
| `data/processed/survey_data_calibrated.json` | Teacher conditions, airtime tax & hardware status | `scripts/process_survey_data_calibrated.py` | 48 SSA nations | N = 800 respondents | 2024 (Alliance of Alliances) |

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

## 3. Ground-Truth Layer 1: Citizen Voice (`afrobarometer_KEN_r9.json`)

* **Source:** Afrobarometer Round 9 Kenya National Survey (March 2023 release).
* **Sample Size:** $N = 2,400$ adult citizens (weighted with `withinwt_ea`).
* **Raw Dataset:** `data/raw/afrobarometer_release-dataset_ken_r9_en_2023-03-01.sav`

| Indicator / Concept | Question / Variable | National (%) | Urban (%) | Rural (%) | Analytical Meaning |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Education in Top 3 Priorities** | `Q45PT1–3` (Code 14) | **18.59%** | **15.97%** | **19.96%** | Rural citizens rate education quality/access as a higher emergency than urban citizens. |
| **Education as #1 Priority** | `Q45PT1` (Code 14) | **4.54%** | **3.10%** | **5.32%** | Share naming education as their single most urgent national problem. |
| **Delivery Handled Well** | `Q46H` ("Fairly/Very Well") | **63.79%** | **69.11%** | **61.03%** | Public satisfaction with state handling of educational needs. |
| **Delivery Handled Badly** | `Q46H` ("Fairly/Very Badly") | **36.21%** | **30.89%** | **38.97%** | Acute rural dissatisfaction with education delivery. |

---

## 4. Ground-Truth Layer 2: Citizen Assessments (`uwezo_KEN_latest.json`)

* **Source:** Usawa Agenda (Uwezo Kenya 6th & 7th National Learning Assessments, 2021–2023).
* **Sample Size:** $N = 135,000$ assessed children across households.
* **Raw Input:** `data/raw/uwezo_kenya_national_summary.csv`

| Metric | Target Population | National (%) | Urban (%) | Rural (%) | Gender Split (M / F) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Foundational Literacy** | Grade 3–5 pupils reading Grade 2 story | **41.6%** | **54.2%** | **36.8%** | 39.5% (Boys) / 43.8% (Girls) |
| **Foundational Numeracy** | Grade 3–5 pupils solving Grade 2 subtraction/division | **46.8%** | **58.1%** | **42.4%** | 47.1% (Boys) / 46.5% (Girls) |
| **Out-of-School Rate** | Children ages 6–16 not enrolled | **8.5%** | **5.2%** | **10.1%** | Reaches >25% in arid counties (Turkana/Garissa) |
| **Household Radio** | All households owning working radio | **62.0%** | **68.0%** | **59.0%** | Key broadcast vehicle for remote learning |
| **Household Television** | All households owning working TV | **45.0%** | **72.0%** | **32.0%** | Severe urban-rural disparity |
| **Household Mobile Phone** | All households owning mobile phone | **91.0%** | **96.0%** | **88.0%** | Universal reach for SMS/USSD interventions |

---

## 5. Ground-Truth Layer 3: Delivery Modality & Friction (`modality_reach_KEN.json`)

* **Sources:** CEGA Busia Remote Learning Study (Cece et al.), Uwezo household surveys, GSMA 2025, ITU/A4AI Price Baskets.
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

## 6. Frontline Practitioner Survey (`survey_data_calibrated.json`)

* **Source:** UNESCO Global Education Coalition / Alliance of Alliances Field Survey.
* **Sample:** $N = 800$ frontline educators and providers across 48 SSA nations.
* **Key Calibrated Ground-Truth Metrics:**
  * **The Informal Airtime Salary Tax:** Frontline teachers spend **4.2% to 7.8% of personal wages** buying commercial mobile data to perform official duties.
  * **Device Inoperability Rate:** Over **60% of school tablets** become inoperable within 14 months due to battery degradation or cracked screens without replacement budgets.
  * **Curricular Language Barrier:** Automated AI evaluation collapses from **90% accuracy in English** to **18–35% in indigenous African languages**.
