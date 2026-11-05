// Generated Supply-Demand Matrix Dataset
// Countries: 48 Sub-Saharan Africa + 21 MENA Reference
// Players: 25 Core Representative Cohort + 123 Indexed Catalog
const MATRIX_COUNTRIES = [
  {
    "iso3": "AGO",
    "country": "Angola",
    "region": "SSA",
    "learning_poverty": 31.8,
    "is_lp_proxy": true,
    "adult_literacy": 68.2,
    "rural_electrification": 1.3,
    "fixed_broadband_per100": 0.36
  },
  {
    "iso3": "BEN",
    "country": "Benin",
    "region": "SSA",
    "learning_poverty": 55.8,
    "is_lp_proxy": false,
    "adult_literacy": 51.4,
    "rural_electrification": 45.0,
    "fixed_broadband_per100": 0.28
  },
  {
    "iso3": "BWA",
    "country": "Botswana",
    "region": "SSA",
    "learning_poverty": null,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 45.9,
    "fixed_broadband_per100": 7.44
  },
  {
    "iso3": "BFA",
    "country": "Burkina Faso",
    "region": "SSA",
    "learning_poverty": 73.9,
    "is_lp_proxy": false,
    "adult_literacy": 41.6,
    "rural_electrification": 12.7,
    "fixed_broadband_per100": 0.85
  },
  {
    "iso3": "BDI",
    "country": "Burundi",
    "region": "SSA",
    "learning_poverty": 95.8,
    "is_lp_proxy": false,
    "adult_literacy": 71.3,
    "rural_electrification": 3.6,
    "fixed_broadband_per100": 0.02
  },
  {
    "iso3": "CPV",
    "country": "Cabo Verde",
    "region": "SSA",
    "learning_poverty": 11.5,
    "is_lp_proxy": true,
    "adult_literacy": 88.5,
    "rural_electrification": 97.7,
    "fixed_broadband_per100": 8.31
  },
  {
    "iso3": "CMR",
    "country": "Cameroon",
    "region": "SSA",
    "learning_poverty": 71.9,
    "is_lp_proxy": false,
    "adult_literacy": 72.6,
    "rural_electrification": 42.7,
    "fixed_broadband_per100": 2.13
  },
  {
    "iso3": "CAF",
    "country": "Central African Republic",
    "region": "SSA",
    "learning_poverty": 57.6,
    "is_lp_proxy": true,
    "adult_literacy": 42.4,
    "rural_electrification": 2.0,
    "fixed_broadband_per100": 0.02
  },
  {
    "iso3": "TCD",
    "country": "Chad",
    "region": "SSA",
    "learning_poverty": 94.4,
    "is_lp_proxy": false,
    "adult_literacy": 30.6,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 0.0
  },
  {
    "iso3": "COM",
    "country": "Comoros",
    "region": "SSA",
    "learning_poverty": 24.4,
    "is_lp_proxy": true,
    "adult_literacy": 75.6,
    "rural_electrification": 88.2,
    "fixed_broadband_per100": 0.39
  },
  {
    "iso3": "COD",
    "country": "Congo, Dem. Rep.",
    "region": "SSA",
    "learning_poverty": 96.6,
    "is_lp_proxy": false,
    "adult_literacy": 68.5,
    "rural_electrification": 1.0,
    "fixed_broadband_per100": 0.03
  },
  {
    "iso3": "COG",
    "country": "Congo, Rep.",
    "region": "SSA",
    "learning_poverty": 70.0,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 19.4,
    "fixed_broadband_per100": 1.27
  },
  {
    "iso3": "CIV",
    "country": "Cote d'Ivoire",
    "region": "SSA",
    "learning_poverty": 79.9,
    "is_lp_proxy": false,
    "adult_literacy": 50.0,
    "rural_electrification": 47.7,
    "fixed_broadband_per100": 1.6
  },
  {
    "iso3": "GNQ",
    "country": "Equatorial Guinea",
    "region": "SSA",
    "learning_poverty": null,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 5.1,
    "fixed_broadband_per100": 0.1
  },
  {
    "iso3": "ERI",
    "country": "Eritrea",
    "region": "SSA",
    "learning_poverty": null,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 43.2,
    "fixed_broadband_per100": 0.17
  },
  {
    "iso3": "SWZ",
    "country": "Eswatini",
    "region": "SSA",
    "learning_poverty": 9.2,
    "is_lp_proxy": true,
    "adult_literacy": 90.8,
    "rural_electrification": 88.3,
    "fixed_broadband_per100": 2.51
  },
  {
    "iso3": "ETH",
    "country": "Ethiopia",
    "region": "SSA",
    "learning_poverty": 90.4,
    "is_lp_proxy": false,
    "adult_literacy": 60.5,
    "rural_electrification": 44.8,
    "fixed_broadband_per100": 0.59
  },
  {
    "iso3": "GAB",
    "country": "Gabon",
    "region": "SSA",
    "learning_poverty": 30.7,
    "is_lp_proxy": false,
    "adult_literacy": 88.9,
    "rural_electrification": 51.3,
    "fixed_broadband_per100": 4.69
  },
  {
    "iso3": "GMB",
    "country": "Gambia, The",
    "region": "SSA",
    "learning_poverty": 48.4,
    "is_lp_proxy": true,
    "adult_literacy": 51.6,
    "rural_electrification": 39.2,
    "fixed_broadband_per100": 0.52
  },
  {
    "iso3": "GHA",
    "country": "Ghana",
    "region": "SSA",
    "learning_poverty": 23.5,
    "is_lp_proxy": true,
    "adult_literacy": 76.5,
    "rural_electrification": 82.6,
    "fixed_broadband_per100": 0.66
  },
  {
    "iso3": "GIN",
    "country": "Guinea",
    "region": "SSA",
    "learning_poverty": 82.7,
    "is_lp_proxy": false,
    "adult_literacy": 39.6,
    "rural_electrification": 29.4,
    "fixed_broadband_per100": 0.01
  },
  {
    "iso3": "GNB",
    "country": "Guinea-Bissau",
    "region": "SSA",
    "learning_poverty": 36.1,
    "is_lp_proxy": true,
    "adult_literacy": 63.9,
    "rural_electrification": 24.9,
    "fixed_broadband_per100": 0.39
  },
  {
    "iso3": "KEN",
    "country": "Kenya",
    "region": "SSA",
    "learning_poverty": 79.3,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 67.1,
    "fixed_broadband_per100": 3.04
  },
  {
    "iso3": "LSO",
    "country": "Lesotho",
    "region": "SSA",
    "learning_poverty": 96.9,
    "is_lp_proxy": false,
    "adult_literacy": 90.4,
    "rural_electrification": 41.4,
    "fixed_broadband_per100": 0.38
  },
  {
    "iso3": "LBR",
    "country": "Liberia",
    "region": "SSA",
    "learning_poverty": null,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 9.2,
    "fixed_broadband_per100": 0.27
  },
  {
    "iso3": "MDG",
    "country": "Madagascar",
    "region": "SSA",
    "learning_poverty": 95.2,
    "is_lp_proxy": false,
    "adult_literacy": 74.7,
    "rural_electrification": 26.5,
    "fixed_broadband_per100": 0.12
  },
  {
    "iso3": "MWI",
    "country": "Malawi",
    "region": "SSA",
    "learning_poverty": 29.8,
    "is_lp_proxy": true,
    "adult_literacy": 70.2,
    "rural_electrification": 6.4,
    "fixed_broadband_per100": 0.09
  },
  {
    "iso3": "MLI",
    "country": "Mali",
    "region": "SSA",
    "learning_poverty": 64.4,
    "is_lp_proxy": true,
    "adult_literacy": 35.6,
    "rural_electrification": 31.4,
    "fixed_broadband_per100": 0.77
  },
  {
    "iso3": "MRT",
    "country": "Mauritania",
    "region": "SSA",
    "learning_poverty": 40.5,
    "is_lp_proxy": true,
    "adult_literacy": 59.5,
    "rural_electrification": null,
    "fixed_broadband_per100": 0.95
  },
  {
    "iso3": "MUS",
    "country": "Mauritius",
    "region": "SSA",
    "learning_poverty": 5.7,
    "is_lp_proxy": true,
    "adult_literacy": 94.3,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 27.97
  },
  {
    "iso3": "MOZ",
    "country": "Mozambique",
    "region": "SSA",
    "learning_poverty": 38.3,
    "is_lp_proxy": true,
    "adult_literacy": 61.7,
    "rural_electrification": 12.3,
    "fixed_broadband_per100": 0.14
  },
  {
    "iso3": "NAM",
    "country": "Namibia",
    "region": "SSA",
    "learning_poverty": 12.4,
    "is_lp_proxy": true,
    "adult_literacy": 87.6,
    "rural_electrification": 41.1,
    "fixed_broadband_per100": 2.83
  },
  {
    "iso3": "NER",
    "country": "Niger",
    "region": "SSA",
    "learning_poverty": 90.4,
    "is_lp_proxy": false,
    "adult_literacy": 35.6,
    "rural_electrification": 10.8,
    "fixed_broadband_per100": 0.11
  },
  {
    "iso3": "NGA",
    "country": "Nigeria",
    "region": "SSA",
    "learning_poverty": 29.6,
    "is_lp_proxy": true,
    "adult_literacy": 70.4,
    "rural_electrification": 23.5,
    "fixed_broadband_per100": 0.08
  },
  {
    "iso3": "RWA",
    "country": "Rwanda",
    "region": "SSA",
    "learning_poverty": 21.2,
    "is_lp_proxy": true,
    "adult_literacy": 78.8,
    "rural_electrification": 65.2,
    "fixed_broadband_per100": 0.6
  },
  {
    "iso3": "STP",
    "country": "Sao Tome and Principe",
    "region": "SSA",
    "learning_poverty": 12.6,
    "is_lp_proxy": true,
    "adult_literacy": 87.4,
    "rural_electrification": 75.1,
    "fixed_broadband_per100": 2.99
  },
  {
    "iso3": "SEN",
    "country": "Senegal",
    "region": "SSA",
    "learning_poverty": 68.6,
    "is_lp_proxy": false,
    "adult_literacy": 50.4,
    "rural_electrification": 67.1,
    "fixed_broadband_per100": 4.04
  },
  {
    "iso3": "SYC",
    "country": "Seychelles",
    "region": "SSA",
    "learning_poverty": null,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 31.6
  },
  {
    "iso3": "SLE",
    "country": "Sierra Leone",
    "region": "SSA",
    "learning_poverty": 56.4,
    "is_lp_proxy": true,
    "adult_literacy": 43.6,
    "rural_electrification": 24.9,
    "fixed_broadband_per100": 0.0
  },
  {
    "iso3": "SOM",
    "country": "Somalia, Fed. Rep.",
    "region": "SSA",
    "learning_poverty": 45.9,
    "is_lp_proxy": true,
    "adult_literacy": 54.1,
    "rural_electrification": 24.4,
    "fixed_broadband_per100": 0.72
  },
  {
    "iso3": "ZAF",
    "country": "South Africa",
    "region": "SSA",
    "learning_poverty": 82.0,
    "is_lp_proxy": false,
    "adult_literacy": 91.2,
    "rural_electrification": 86.3,
    "fixed_broadband_per100": 5.35
  },
  {
    "iso3": "SSD",
    "country": "South Sudan",
    "region": "SSA",
    "learning_poverty": null,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 0.7,
    "fixed_broadband_per100": 0.0
  },
  {
    "iso3": "SDN",
    "country": "Sudan",
    "region": "SSA",
    "learning_poverty": null,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 54.2,
    "fixed_broadband_per100": 0.06
  },
  {
    "iso3": "TZA",
    "country": "Tanzania",
    "region": "SSA",
    "learning_poverty": 21.8,
    "is_lp_proxy": true,
    "adult_literacy": 78.2,
    "rural_electrification": 33.7,
    "fixed_broadband_per100": 0.25
  },
  {
    "iso3": "TGO",
    "country": "Togo",
    "region": "SSA",
    "learning_poverty": 81.7,
    "is_lp_proxy": false,
    "adult_literacy": 72.6,
    "rural_electrification": 33.9,
    "fixed_broadband_per100": 1.42
  },
  {
    "iso3": "UGA",
    "country": "Uganda",
    "region": "SSA",
    "learning_poverty": 23.0,
    "is_lp_proxy": true,
    "adult_literacy": 77.0,
    "rural_electrification": 44.8,
    "fixed_broadband_per100": 0.21
  },
  {
    "iso3": "ZMB",
    "country": "Zambia",
    "region": "SSA",
    "learning_poverty": 98.5,
    "is_lp_proxy": false,
    "adult_literacy": 71.8,
    "rural_electrification": 31.3,
    "fixed_broadband_per100": 0.79
  },
  {
    "iso3": "ZWE",
    "country": "Zimbabwe",
    "region": "SSA",
    "learning_poverty": 6.8,
    "is_lp_proxy": true,
    "adult_literacy": 93.2,
    "rural_electrification": 46.6,
    "fixed_broadband_per100": 1.94
  },
  {
    "iso3": "DZA",
    "country": "Algeria",
    "region": "MENA",
    "learning_poverty": null,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 13.32
  },
  {
    "iso3": "BHR",
    "country": "Bahrain",
    "region": "MENA",
    "learning_poverty": 30.2,
    "is_lp_proxy": false,
    "adult_literacy": 97.8,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 16.99
  },
  {
    "iso3": "DJI",
    "country": "Djibouti",
    "region": "MENA",
    "learning_poverty": null,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 53.9,
    "fixed_broadband_per100": 1.47
  },
  {
    "iso3": "EGY",
    "country": "Egypt, Arab Rep.",
    "region": "MENA",
    "learning_poverty": 56.1,
    "is_lp_proxy": false,
    "adult_literacy": 79.5,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 11.69
  },
  {
    "iso3": "IRN",
    "country": "Iran, Islamic Rep.",
    "region": "MENA",
    "learning_poverty": 41.5,
    "is_lp_proxy": false,
    "adult_literacy": 88.9,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 12.06
  },
  {
    "iso3": "IRQ",
    "country": "Iraq",
    "region": "MENA",
    "learning_poverty": 15.9,
    "is_lp_proxy": true,
    "adult_literacy": 84.1,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 17.63
  },
  {
    "iso3": "ISR",
    "country": "Israel",
    "region": "MENA",
    "learning_poverty": 14.4,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 29.18
  },
  {
    "iso3": "JOR",
    "country": "Jordan",
    "region": "MENA",
    "learning_poverty": 62.2,
    "is_lp_proxy": false,
    "adult_literacy": 94.4,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 7.02
  },
  {
    "iso3": "KWT",
    "country": "Kuwait",
    "region": "MENA",
    "learning_poverty": 51.1,
    "is_lp_proxy": false,
    "adult_literacy": 96.5,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 1.01
  },
  {
    "iso3": "LBN",
    "country": "Lebanon",
    "region": "MENA",
    "learning_poverty": 8.0,
    "is_lp_proxy": true,
    "adult_literacy": 92.0,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 7.29
  },
  {
    "iso3": "LBY",
    "country": "Libya",
    "region": "MENA",
    "learning_poverty": null,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": null,
    "fixed_broadband_per100": 4.52
  },
  {
    "iso3": "MLT",
    "country": "Malta",
    "region": "MENA",
    "learning_poverty": 10.2,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 44.51
  },
  {
    "iso3": "MAR",
    "country": "Morocco",
    "region": "MENA",
    "learning_poverty": 59.8,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 7.3
  },
  {
    "iso3": "OMN",
    "country": "Oman",
    "region": "MENA",
    "learning_poverty": 40.6,
    "is_lp_proxy": false,
    "adult_literacy": 97.3,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 11.06
  },
  {
    "iso3": "QAT",
    "country": "Qatar",
    "region": "MENA",
    "learning_poverty": 21.1,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 11.82
  },
  {
    "iso3": "SAU",
    "country": "Saudi Arabia",
    "region": "MENA",
    "learning_poverty": 32.4,
    "is_lp_proxy": false,
    "adult_literacy": 97.9,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 44.07
  },
  {
    "iso3": "SYR",
    "country": "Syrian Arab Republic",
    "region": "MENA",
    "learning_poverty": 5.6,
    "is_lp_proxy": true,
    "adult_literacy": 94.4,
    "rural_electrification": 61.6,
    "fixed_broadband_per100": 6.86
  },
  {
    "iso3": "TUN",
    "country": "Tunisia",
    "region": "MENA",
    "learning_poverty": 13.8,
    "is_lp_proxy": true,
    "adult_literacy": 86.2,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 14.97
  },
  {
    "iso3": "ARE",
    "country": "United Arab Emirates",
    "region": "MENA",
    "learning_poverty": 25.9,
    "is_lp_proxy": false,
    "adult_literacy": 98.8,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 40.84
  },
  {
    "iso3": "PSE",
    "country": "West Bank and Gaza",
    "region": "MENA",
    "learning_poverty": 2.1,
    "is_lp_proxy": true,
    "adult_literacy": 97.9,
    "rural_electrification": 100.0,
    "fixed_broadband_per100": 8.16
  },
  {
    "iso3": "YEM",
    "country": "Yemen, Rep.",
    "region": "MENA",
    "learning_poverty": null,
    "is_lp_proxy": false,
    "adult_literacy": null,
    "rural_electrification": 81.3,
    "fixed_broadband_per100": 1.27
  }
];
const MATRIX_PLAYERS = [
  {
    "name": "Xarala",
    "country": "Senegal",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": true
  },
  {
    "name": "Yello App",
    "country": "Senegal",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": true
  },
  {
    "name": "Tooshare",
    "country": "Senegal",
    "category": "Marketplace",
    "domain": "Ecosystem & Marketplaces",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Databeez",
    "country": "Senegal",
    "category": "AI; Data",
    "domain": "AI, Inclusion & Frontier",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": true
  },
  {
    "name": "Bakeli School of Technology",
    "country": "Senegal",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": true
  },
  {
    "name": "Neolean Academy",
    "country": "Senegal",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Ashita-ICC",
    "country": "Senegal",
    "category": "TVET",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Jangalma",
    "country": "Senegal",
    "category": "TVET",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Cashew",
    "country": "Senegal",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Steamtastic",
    "country": "Senegal",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "20/20 EdTech",
    "country": "Senegal",
    "category": "Platform",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": true
  },
  {
    "name": "Education Channel",
    "country": "Senegal",
    "category": "Content",
    "domain": "Digital Content & Literacy",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": true
  },
  {
    "name": "Digital School Technologies",
    "country": "Senegal",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": true
  },
  {
    "name": "Edacy",
    "country": "Senegal",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Grow Academy",
    "country": "Senegal",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Mjangale",
    "country": "Senegal",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Meelam",
    "country": "Senegal",
    "category": "Content",
    "domain": "Digital Content & Literacy",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Volkeno",
    "country": "Senegal",
    "category": "TVET; Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "LOGECO",
    "country": "Benin",
    "category": "TVET",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "TAMA",
    "country": "Benin",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "IRAWO",
    "country": "Benin",
    "category": "Content",
    "domain": "Digital Content & Literacy",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Ecolia",
    "country": "Benin",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Kankode",
    "country": "Benin",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Malam",
    "country": "Benin",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Mobidoto",
    "country": "Benin",
    "category": "Marketplace",
    "domain": "Ecosystem & Marketplaces",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Steamy",
    "country": "Benin",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Pocket Tutor",
    "country": "Benin",
    "category": "Marketplace",
    "domain": "Ecosystem & Marketplaces",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Problems",
    "country": "Benin",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Epitech Technology",
    "country": "Benin",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Ilewemi",
    "country": "Benin",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Mara Academy",
    "country": "Benin",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "Seven",
    "country": "Benin",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "80",
    "is_core_25": false
  },
  {
    "name": "BACprep",
    "country": "Ivory Coast",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Bibliosave",
    "country": "Ivory Coast",
    "category": "Content",
    "domain": "Digital Content & Literacy",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Chalkboard Education",
    "country": "Ivory Coast",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Coach\u2019ON",
    "country": "Ivory Coast",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Dictable",
    "country": "Ivory Coast",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Educate",
    "country": "Ivory Coast",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "EducforMooc",
    "country": "Ivory Coast",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Edudesk",
    "country": "Ivory Coast",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Edugate",
    "country": "Ivory Coast",
    "category": "Platform",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Eduweb",
    "country": "Ivory Coast",
    "category": "Platform",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Expand Education",
    "country": "Ivory Coast",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": true
  },
  {
    "name": "Enko Education",
    "country": "Ivory Coast",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Fatala Digital House",
    "country": "Ivory Coast",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Gomycode",
    "country": "Ivory Coast",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "EdTech CASE",
    "country": "Ivory Coast",
    "category": "Platform",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Nan Academy",
    "country": "Ivory Coast",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Nimba Edition",
    "country": "Ivory Coast",
    "category": "Content",
    "domain": "Digital Content & Literacy",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Qelasy",
    "country": "Ivory Coast",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "TOOTREE CI",
    "country": "Ivory Coast",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Trace Academia",
    "country": "Ivory Coast",
    "category": "Upskilling; Content",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "RobotsMali (AI4D Lab)",
    "country": "Mali",
    "category": "AI; Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Kabakoo Academies",
    "country": "Mali",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Emera AI",
    "country": "Burkina Faso",
    "category": "AI",
    "domain": "AI, Inclusion & Frontier",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "DigiClass",
    "country": "Burkina Faso",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Faso e-Education",
    "country": "Burkina Faso",
    "category": "Platform",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "ANFCT e-Learning",
    "country": "Togo",
    "category": "Platform",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Suisco",
    "country": "Togo",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Zonoa",
    "country": "Togo",
    "category": "Marketplace",
    "domain": "Ecosystem & Marketplaces",
    "is_mena": false,
    "qa_flag": "",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "CET ASNI",
    "country": "Niger",
    "category": "TVET",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "identical_list_to:Guinea",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Codeloccol",
    "country": "Niger",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "identical_list_to:Guinea",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "Karatou Post-Bac",
    "country": "Niger",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "identical_list_to:Guinea",
    "page": "81",
    "is_core_25": false
  },
  {
    "name": "CET ASNI",
    "country": "Guinea",
    "category": "TVET",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "identical_list_to:Niger",
    "page": "82",
    "is_core_25": false
  },
  {
    "name": "Codeloccol",
    "country": "Guinea",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "identical_list_to:Niger",
    "page": "82",
    "is_core_25": false
  },
  {
    "name": "Karatou Post-Bac",
    "country": "Guinea",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "identical_list_to:Niger",
    "page": "82",
    "is_core_25": false
  },
  {
    "name": "Dext Technology",
    "country": "Ghana",
    "category": "AI",
    "domain": "AI, Inclusion & Frontier",
    "is_mena": false,
    "qa_flag": "",
    "page": "82",
    "is_core_25": true
  },
  {
    "name": "Ayaprep",
    "country": "Ghana",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "82",
    "is_core_25": true
  },
  {
    "name": "QKnow EdTech",
    "country": "Ghana",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "82",
    "is_core_25": true
  },
  {
    "name": "DeafCanTalk",
    "country": "Ghana",
    "category": "AI; Inclusion",
    "domain": "AI, Inclusion & Frontier",
    "is_mena": false,
    "qa_flag": "",
    "page": "82",
    "is_core_25": true
  },
  {
    "name": "Firefly IO",
    "country": "Ghana",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "82",
    "is_core_25": false
  },
  {
    "name": "Coral Reef Innovation Hub",
    "country": "Ghana",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "82",
    "is_core_25": false
  },
  {
    "name": "University of Nairobi",
    "country": "Kenya",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "university_not_startup",
    "page": "82",
    "is_core_25": false
  },
  {
    "name": "Aga Khan University",
    "country": "Kenya",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "university_not_startup",
    "page": "82",
    "is_core_25": false
  },
  {
    "name": "Expand Education",
    "country": "Kenya",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "82",
    "is_core_25": true
  },
  {
    "name": "Genoskul",
    "country": "Chad",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "82",
    "is_core_25": false
  },
  {
    "name": "ChadEducationPlus",
    "country": "Chad",
    "category": "Platform",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "82",
    "is_core_25": false
  },
  {
    "name": "EduCare",
    "country": "Gambia",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "82",
    "is_core_25": false
  },
  {
    "name": "Leap Learning",
    "country": "Gambia",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "82",
    "is_core_25": false
  },
  {
    "name": "DoLessons",
    "country": "Nigeria",
    "category": "Marketplace",
    "domain": "Ecosystem & Marketplaces",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": true
  },
  {
    "name": "Tuteria",
    "country": "Nigeria",
    "category": "Marketplace",
    "domain": "Ecosystem & Marketplaces",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": true
  },
  {
    "name": "SchoolsFocus",
    "country": "Nigeria",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": true
  },
  {
    "name": "Afribary",
    "country": "Nigeria",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "uLesson",
    "country": "Nigeria",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": true
  },
  {
    "name": "Teesas",
    "country": "Nigeria",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": true
  },
  {
    "name": "Gradely",
    "country": "Nigeria",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": true
  },
  {
    "name": "Nigenius",
    "country": "Nigeria",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": true
  },
  {
    "name": "Prepclass",
    "country": "Nigeria",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Edusko",
    "country": "Nigeria",
    "category": "Marketplace",
    "domain": "Ecosystem & Marketplaces",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Traindemy",
    "country": "Nigeria",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "ScholarX",
    "country": "Nigeria",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Sweetch",
    "country": "Cameroon",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Studirium",
    "country": "Cameroon",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Maya Academy",
    "country": "Cameroon",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "OSIA Technologies",
    "country": "Cameroon",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Mashidano",
    "country": "Congo",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Schoolap",
    "country": "Congo",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Congo-Education",
    "country": "Congo",
    "category": "Platform",
    "domain": "Learning Platforms & LMS",
    "is_mena": false,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Yool.education",
    "country": "Morocco",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": true,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Kezakoo",
    "country": "Morocco",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": true,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Prove",
    "country": "Morocco",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": true,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "NOBOX LAB",
    "country": "Morocco",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": true,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Sprints",
    "country": "Egypt",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": true,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "El Kheta",
    "country": "Egypt",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": true,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "TeacherKit",
    "country": "Egypt",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": true,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Crafty Workshop",
    "country": "Egypt",
    "category": "TVET",
    "domain": "Workforce, TVET & Skills",
    "is_mena": true,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "iSchool",
    "country": "Egypt",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": true,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "ShareEdu",
    "country": "Egypt",
    "category": "Platform",
    "domain": "Learning Platforms & LMS",
    "is_mena": true,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Nafham",
    "country": "Egypt",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": true,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "Egypt Education Platform",
    "country": "Egypt",
    "category": "Platform",
    "domain": "Learning Platforms & LMS",
    "is_mena": true,
    "qa_flag": "",
    "page": "83",
    "is_core_25": false
  },
  {
    "name": "LabLabee",
    "country": "Algeria",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": true,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Esaboura",
    "country": "Algeria",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": true,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Edutech.dz",
    "country": "Algeria",
    "category": "Platform",
    "domain": "Learning Platforms & LMS",
    "is_mena": true,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Gomycode Algeria",
    "country": "Algeria",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": true,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "IFRISQ e-Learning",
    "country": "Algeria",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": true,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "ClassQuiz",
    "country": "Tunisia",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": true,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "OBM Education",
    "country": "Tunisia",
    "category": "TVET",
    "domain": "Workforce, TVET & Skills",
    "is_mena": true,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Atom Academy",
    "country": "Tunisia",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": true,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "School Upgrader",
    "country": "Tunisia",
    "category": "LMS",
    "domain": "Learning Platforms & LMS",
    "is_mena": true,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Rosco Edutec",
    "country": "Angola",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Mitrelli Education",
    "country": "Angola",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Grade",
    "country": "Angola",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Colossus App",
    "country": "Zambia",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Omni Learning",
    "country": "Zambia",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Simba Education",
    "country": "Zambia",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Ambani Africa",
    "country": "South Africa",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Book Village",
    "country": "South Africa",
    "category": "Marketplace",
    "domain": "Ecosystem & Marketplaces",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "GetSmarter",
    "country": "South Africa",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": true
  },
  {
    "name": "Snapplify",
    "country": "South Africa",
    "category": "Content",
    "domain": "Digital Content & Literacy",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": true
  },
  {
    "name": "WeThinkCode",
    "country": "South Africa",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": true
  },
  {
    "name": "Zaio",
    "country": "South Africa",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "FoondaMate",
    "country": "South Africa",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": true
  },
  {
    "name": "Reflective Learning",
    "country": "South Africa",
    "category": "Content",
    "domain": "Digital Content & Literacy",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": true
  },
  {
    "name": "Valenture Institute",
    "country": "South Africa",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "84",
    "is_core_25": false
  },
  {
    "name": "Sikul",
    "country": "Gabon",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": false
  },
  {
    "name": "Prepdia",
    "country": "Gabon",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": false
  },
  {
    "name": "ESTIM Gabon",
    "country": "Gabon",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": false
  },
  {
    "name": "ESIITECH",
    "country": "Gabon",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": false
  },
  {
    "name": "AltSchool Africa",
    "country": "Rwanda",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": false
  },
  {
    "name": "ALX",
    "country": "Rwanda",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": false
  },
  {
    "name": "SOLVIT AFRICA",
    "country": "Rwanda",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": false
  },
  {
    "name": "Cyber University / SoftBank",
    "country": "Rwanda",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "university_not_startup",
    "page": "85",
    "is_core_25": false
  },
  {
    "name": "O\u2019Genius",
    "country": "Rwanda",
    "category": "Upskilling",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": false
  },
  {
    "name": "Rwanda Coding Academy",
    "country": "Rwanda",
    "category": "TVET",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": true
  },
  {
    "name": "CEATECH-SL",
    "country": "Liberia",
    "category": "TVET",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": false
  },
  {
    "name": "YONER Liberia",
    "country": "Liberia",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": false
  },
  {
    "name": "AIIST",
    "country": "Liberia",
    "category": "Higher Ed",
    "domain": "Workforce, TVET & Skills",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": false
  },
  {
    "name": "Weeglo",
    "country": "Liberia",
    "category": "K-12",
    "domain": "K-12 & Foundational",
    "is_mena": false,
    "qa_flag": "",
    "page": "85",
    "is_core_25": false
  }
];
