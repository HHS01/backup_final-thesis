// Generated Macro-Fiscal & External Aid Observatory Dataset
// Sources: IMF GFS COFOG (2017-2024) + IATI Datastore API (2017-2024) + UIS
// Target Economies (7): KEN, RWA, TZA, MUS, GHA, NGA, ZMB
const MACRO_FISCAL_DATA = {
  "metadata": {
    "title": "Macro-Fiscal & External Aid Observatory Dataset",
    "compiled_utc": "2026-11-07T16:07:01.546297+00:00",
    "script_version": "1.1.0",
    "coverage_window": "2017-2024",
    "target_economies": [
      "KEN",
      "RWA",
      "TZA",
      "MUS",
      "GHA",
      "NGA",
      "ZMB"
    ],
    "sources": [
      "IMF Government Finance Statistics (GFS) COFOG",
      "IATI Datastore Registry API (2017-2024 Normalized Transactions)",
      "World Bank / UNESCO UIS EdStats"
    ],
    "total_education_aid_usd_m": 6843.56,
    "total_ict_aid_usd_m": 552.13
  },
  "comparison_table": [
    {
      "iso3": "KEN",
      "name": "Kenya",
      "edu_pct_budget": 18.43,
      "comm_pct_budget": 0.46,
      "edu_aid_disb_usd_m": 1016.61,
      "ict_aid_disb_usd_m": 4.83,
      "covid_2020_disb_usd_m": 244.03,
      "electricity_pct": 77.0,
      "learning_poverty_pct": 79.3,
      "cliff_risk": "High Tension (Structural Recurrent Lock)"
    },
    {
      "iso3": "RWA",
      "name": "Rwanda",
      "edu_pct_budget": 14.19,
      "comm_pct_budget": null,
      "edu_aid_disb_usd_m": 974.68,
      "ict_aid_disb_usd_m": 30.99,
      "covid_2020_disb_usd_m": 341.46,
      "electricity_pct": 72.0,
      "learning_poverty_pct": null,
      "cliff_risk": "High External Reliance (Classroom Crowding Deficit)"
    },
    {
      "iso3": "TZA",
      "name": "Tanzania",
      "edu_pct_budget": 19.56,
      "comm_pct_budget": null,
      "edu_aid_disb_usd_m": 2052.05,
      "ict_aid_disb_usd_m": 130.67,
      "covid_2020_disb_usd_m": 159.6,
      "electricity_pct": 52.4,
      "learning_poverty_pct": null,
      "cliff_risk": "Severe Infrastructure Void vs. Aid Volume"
    },
    {
      "iso3": "MUS",
      "name": "Mauritius",
      "edu_pct_budget": 10.31,
      "comm_pct_budget": 0.09,
      "edu_aid_disb_usd_m": 2.52,
      "ict_aid_disb_usd_m": 0.0,
      "covid_2020_disb_usd_m": 0.02,
      "electricity_pct": 100.0,
      "learning_poverty_pct": null,
      "cliff_risk": "Self-Financed Universal SIDS Benchmark"
    },
    {
      "iso3": "GHA",
      "name": "Ghana",
      "edu_pct_budget": 13.18,
      "comm_pct_budget": null,
      "edu_aid_disb_usd_m": 443.54,
      "ict_aid_disb_usd_m": 223.51,
      "covid_2020_disb_usd_m": 94.51,
      "electricity_pct": 91.9,
      "learning_poverty_pct": null,
      "cliff_risk": "Expanding Donor ICT Capital vs. Rural Electrification"
    },
    {
      "iso3": "NGA",
      "name": "Nigeria",
      "edu_pct_budget": 2.98,
      "comm_pct_budget": null,
      "edu_aid_disb_usd_m": 1973.55,
      "ict_aid_disb_usd_m": 158.35,
      "covid_2020_disb_usd_m": 145.43,
      "electricity_pct": 62.5,
      "learning_poverty_pct": null,
      "cliff_risk": "Severe Macro Federal Budget Deficit"
    },
    {
      "iso3": "ZMB",
      "name": "Zambia",
      "edu_pct_budget": 14.6,
      "comm_pct_budget": 0.64,
      "edu_aid_disb_usd_m": 380.61,
      "ict_aid_disb_usd_m": 3.78,
      "covid_2020_disb_usd_m": 93.36,
      "electricity_pct": 53.6,
      "learning_poverty_pct": 98.5,
      "cliff_risk": "Moderate Domestic Envelope & Sustained Aid Reliance"
    }
  ],
  "countries": {
    "KEN": {
      "country_iso3": "KEN",
      "country_iso2": "KE",
      "country_name": "Kenya",
      "archetype": "East African Innovation Hub with High Pedagogical Qualifications",
      "domestic_fiscal": {
        "source": "IMF STA GFS (S1311B, 2023)",
        "has_imf_cofog": true,
        "education_pct_budget": 18.43,
        "education_pct_gdp": 3.83,
        "communication_pct_budget": 0.46,
        "communication_pct_gdp": 0.096,
        "transport_pct_budget": 6.06,
        "transport_pct_gdp": 1.26,
        "total_outlays_pct_gdp": 20.79,
        "annual_timeseries": {
          "2017": {
            "education_pct_gdp": 3.84,
            "education_pct_budget": 14.26,
            "communication_pct_gdp": 0.35,
            "communication_pct_budget": 1.3,
            "transport_pct_gdp": 3.59,
            "transport_pct_budget": 13.35,
            "total_outlays_pct_gdp": 26.91
          },
          "2018": {
            "education_pct_gdp": 4.42,
            "education_pct_budget": 18.63,
            "communication_pct_gdp": 0.157,
            "communication_pct_budget": 0.66,
            "transport_pct_gdp": 2.37,
            "transport_pct_budget": 10.02,
            "total_outlays_pct_gdp": 23.7
          },
          "2019": {
            "education_pct_gdp": 4.45,
            "education_pct_budget": 18.52,
            "communication_pct_gdp": 0.27,
            "communication_pct_budget": 1.13,
            "transport_pct_gdp": 2.78,
            "transport_pct_budget": 11.59,
            "total_outlays_pct_gdp": 24.0
          },
          "2020": {
            "education_pct_gdp": 4.34,
            "education_pct_budget": 19.84,
            "communication_pct_gdp": 0.211,
            "communication_pct_budget": 0.96,
            "transport_pct_gdp": 3.04,
            "transport_pct_budget": 13.9,
            "total_outlays_pct_gdp": 21.86
          },
          "2021": {
            "education_pct_gdp": 3.71,
            "education_pct_budget": 16.38,
            "communication_pct_gdp": 0.197,
            "communication_pct_budget": 0.87,
            "transport_pct_gdp": 2.04,
            "transport_pct_budget": 9.02,
            "total_outlays_pct_gdp": 22.66
          },
          "2022": {
            "education_pct_gdp": 3.55,
            "education_pct_budget": 15.86,
            "communication_pct_gdp": 0.173,
            "communication_pct_budget": 0.77,
            "transport_pct_gdp": 2.36,
            "transport_pct_budget": 10.55,
            "total_outlays_pct_gdp": 22.36
          },
          "2023": {
            "education_pct_gdp": 3.83,
            "education_pct_budget": 18.43,
            "communication_pct_gdp": 0.096,
            "communication_pct_budget": 0.46,
            "transport_pct_gdp": 1.26,
            "transport_pct_budget": 6.06,
            "total_outlays_pct_gdp": 20.79
          }
        },
        "subfunctions": {
          "GF091_T": {
            "code": "GF091_T",
            "name": "Pre-primary and primary education",
            "pct_gdp": 1.405,
            "pct_budget": 6.76
          },
          "GF092_T": {
            "code": "GF092_T",
            "name": "Secondary education",
            "pct_gdp": 1.761,
            "pct_budget": 8.47
          },
          "GF0930_T": {
            "code": "GF0930_T",
            "name": "Post-secondary non-tertiary education",
            "pct_gdp": 0.0,
            "pct_budget": 0.0
          },
          "GF094_T": {
            "code": "GF094_T",
            "name": "Tertiary education",
            "pct_gdp": 0.535,
            "pct_budget": 2.57
          },
          "GF0950_T": {
            "code": "GF0950_T",
            "name": "Education not definable by level",
            "pct_gdp": 0.0,
            "pct_budget": 0.0
          },
          "GF0960_T": {
            "code": "GF0960_T",
            "name": "Subsidiary services to education",
            "pct_gdp": 0.0,
            "pct_budget": 0.0
          },
          "GF0970_T": {
            "code": "GF0970_T",
            "name": "R&D Education",
            "pct_gdp": 0.0,
            "pct_budget": 0.0
          },
          "GF0980_T": {
            "code": "GF0980_T",
            "name": "Education n.e.c.",
            "pct_gdp": 0.13,
            "pct_budget": 0.63
          }
        }
      },
      "external_assistance": {
        "source": "IATI Datastore Solr API (2017-2024)",
        "education_disbursed_8yr_usd_m": 1016.61,
        "education_committed_8yr_usd_m": 482.74,
        "ict_disbursed_8yr_usd_m": 4.83,
        "total_aid_disbursed_8yr_usd_m": 1021.44,
        "covid_2020_surge": {
          "disbursed_2019_usd_m": 106.18,
          "disbursed_2020_usd_m": 244.03,
          "surge_absolute_usd_m": 137.85,
          "surge_growth_pct": 129.8
        },
        "annual_timeseries": {
          "2017": {
            "education_disbursements_usd_m": 93.69,
            "education_commitments_usd_m": 212.4,
            "ict_disbursements_usd_m": 0.2,
            "ict_commitments_usd_m": 0.77,
            "total_disbursements_usd_m": 93.89,
            "total_commitments_usd_m": 213.17
          },
          "2018": {
            "education_disbursements_usd_m": 150.78,
            "education_commitments_usd_m": 17.49,
            "ict_disbursements_usd_m": 0.04,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 150.82,
            "total_commitments_usd_m": 17.49
          },
          "2019": {
            "education_disbursements_usd_m": 106.18,
            "education_commitments_usd_m": 67.57,
            "ict_disbursements_usd_m": 0.11,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 106.29,
            "total_commitments_usd_m": 67.57
          },
          "2020": {
            "education_disbursements_usd_m": 244.03,
            "education_commitments_usd_m": 39.11,
            "ict_disbursements_usd_m": 0.03,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 244.06,
            "total_commitments_usd_m": 39.11
          },
          "2021": {
            "education_disbursements_usd_m": 78.55,
            "education_commitments_usd_m": 5.02,
            "ict_disbursements_usd_m": 0.01,
            "ict_commitments_usd_m": 0.96,
            "total_disbursements_usd_m": 78.56,
            "total_commitments_usd_m": 5.98
          },
          "2022": {
            "education_disbursements_usd_m": 158.45,
            "education_commitments_usd_m": 116.18,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 158.45,
            "total_commitments_usd_m": 116.18
          },
          "2023": {
            "education_disbursements_usd_m": 68.05,
            "education_commitments_usd_m": 10.1,
            "ict_disbursements_usd_m": 0.38,
            "ict_commitments_usd_m": 0.92,
            "total_disbursements_usd_m": 68.43,
            "total_commitments_usd_m": 11.01
          },
          "2024": {
            "education_disbursements_usd_m": 116.87,
            "education_commitments_usd_m": 14.87,
            "ict_disbursements_usd_m": 4.07,
            "ict_commitments_usd_m": 7.38,
            "total_disbursements_usd_m": 120.94,
            "total_commitments_usd_m": 22.25
          }
        },
        "top_initiatives": [
          {
            "title": "Kenya  Secondary Education Quality Improvement Project",
            "year": 2017,
            "group": "education",
            "value_usd": 200000000.0,
            "iati_id": "44000-P160083"
          },
          {
            "title": "Education Sector Support Program",
            "year": 2020,
            "group": "education",
            "value_usd": 119790000.0,
            "iati_id": "XI-IATI-WBTF-P087479"
          },
          {
            "title": "2019 Project - Young Africa Works-Kenya: TVET Institution Support",
            "year": 2019,
            "group": "education",
            "value_usd": 37045696.0,
            "iati_id": "CA-CRA_ACR-817387277-PROJECTS-1147"
          },
          {
            "title": "Foundations for Education and Empowerment in Africa Fondations pour l\u2019\u00e9ducation et l\u2019autonomisation en Afrique",
            "year": 2020,
            "group": "education",
            "value_usd": 34300000.0,
            "iati_id": "CA-3-P007597001"
          },
          {
            "title": "F\u00f6rderung von Schulbildung in st\u00e4dtischen und randst\u00e4dtischen Armutsgebieten, Ph. III Primary Education in Poor Areas",
            "year": 2022,
            "group": "education",
            "value_usd": 22968517.0,
            "iati_id": "DE-1-201065838"
          },
          {
            "title": "Human-Centred Digitalisation #TeamEuropeKenya (AAP-2022)",
            "year": 2022,
            "group": "education",
            "value_usd": 20160000.0,
            "iati_id": "XI-IATI-EC_INTPA-2022-ACT-60728"
          },
          {
            "title": "Learning Through Education and Access to Skills for Employment for Refugees and Host Communities Apprendre par l'\u00e9ducation et l'acc\u00e8s aux co",
            "year": 2019,
            "group": "education",
            "value_usd": 13149997.0,
            "iati_id": "CA-3-P007333001"
          },
          {
            "title": "2019 Project - YAW-K Moringa Project",
            "year": 2019,
            "group": "education",
            "value_usd": 9530713.0,
            "iati_id": "CA-CRA_ACR-817387277-PROJECTS-1168"
          }
        ]
      },
      "recurrent_cliff_analysis": {
        "cliff_risk_tier": "High Tension (Structural Recurrent Lock)",
        "domestic_edu_to_comm_ratio": 40.1,
        "narrative": "Kenya allocates 18.43% of national budget to education (strong domestic commitment), yet central ICT receives only 0.46%. With over $1B in external education aid driving hardware deployments, schools lack ongoing public connectivity and maintenance subsidies."
      },
      "macro_context": {
        "country_name": "Kenya",
        "region": "SSA",
        "gdp_per_capita_usd": 2133.0,
        "internet_users_pct": 35.0,
        "fixed_broadband_per100": 3.04,
        "electricity_access_pct": 77.0,
        "rural_electricity_pct": 67.1,
        "urban_electricity_pct": 98.1,
        "learning_poverty_pct": 79.3,
        "adult_literacy_pct": null,
        "wb_education_pct_gdp": 4.02,
        "wb_education_pct_budget": 27.92
      }
    },
    "RWA": {
      "country_iso3": "RWA",
      "country_iso2": "RW",
      "country_name": "Rwanda",
      "archetype": "State-Led Digital Push vs. Classroom Crowding & Language Transition",
      "domestic_fiscal": {
        "source": "World Bank / UNESCO UIS Benchmark",
        "has_imf_cofog": false,
        "education_pct_budget": 14.19,
        "education_pct_gdp": 4.61,
        "communication_pct_budget": null,
        "communication_pct_gdp": null,
        "transport_pct_budget": null,
        "transport_pct_gdp": null,
        "total_outlays_pct_gdp": null,
        "annual_timeseries": {},
        "subfunctions": {}
      },
      "external_assistance": {
        "source": "IATI Datastore Solr API (2017-2024)",
        "education_disbursed_8yr_usd_m": 974.68,
        "education_committed_8yr_usd_m": 1556.69,
        "ict_disbursed_8yr_usd_m": 30.99,
        "total_aid_disbursed_8yr_usd_m": 1005.67,
        "covid_2020_surge": {
          "disbursed_2019_usd_m": 66.1,
          "disbursed_2020_usd_m": 341.46,
          "surge_absolute_usd_m": 275.36,
          "surge_growth_pct": 416.6
        },
        "annual_timeseries": {
          "2017": {
            "education_disbursements_usd_m": 73.69,
            "education_commitments_usd_m": 192.28,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 73.69,
            "total_commitments_usd_m": 192.28
          },
          "2018": {
            "education_disbursements_usd_m": 44.8,
            "education_commitments_usd_m": 58.3,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 28.41,
            "total_disbursements_usd_m": 44.8,
            "total_commitments_usd_m": 86.71
          },
          "2019": {
            "education_disbursements_usd_m": 66.1,
            "education_commitments_usd_m": 297.87,
            "ict_disbursements_usd_m": 2.3,
            "ict_commitments_usd_m": 2.0,
            "total_disbursements_usd_m": 68.4,
            "total_commitments_usd_m": 299.87
          },
          "2020": {
            "education_disbursements_usd_m": 341.46,
            "education_commitments_usd_m": 209.06,
            "ict_disbursements_usd_m": 0.25,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 341.7,
            "total_commitments_usd_m": 209.06
          },
          "2021": {
            "education_disbursements_usd_m": 78.88,
            "education_commitments_usd_m": 58.39,
            "ict_disbursements_usd_m": 0.41,
            "ict_commitments_usd_m": 110.45,
            "total_disbursements_usd_m": 79.29,
            "total_commitments_usd_m": 168.84
          },
          "2022": {
            "education_disbursements_usd_m": 114.01,
            "education_commitments_usd_m": 241.12,
            "ict_disbursements_usd_m": 8.08,
            "ict_commitments_usd_m": 8.43,
            "total_disbursements_usd_m": 122.08,
            "total_commitments_usd_m": 249.55
          },
          "2023": {
            "education_disbursements_usd_m": 136.75,
            "education_commitments_usd_m": 119.26,
            "ict_disbursements_usd_m": 3.88,
            "ict_commitments_usd_m": 1.05,
            "total_disbursements_usd_m": 140.63,
            "total_commitments_usd_m": 120.31
          },
          "2024": {
            "education_disbursements_usd_m": 119.0,
            "education_commitments_usd_m": 380.41,
            "ict_disbursements_usd_m": 16.07,
            "ict_commitments_usd_m": -14.74,
            "total_disbursements_usd_m": 135.08,
            "total_commitments_usd_m": 365.67
          }
        },
        "top_initiatives": [
          {
            "title": "Rwanda Quality Basic Education for Human Capital Development Project",
            "year": 2019,
            "group": "education",
            "value_usd": 170000000.0,
            "iati_id": "44000-P168551"
          },
          {
            "title": "Rwanda Priority Skills for Growth (PSG)",
            "year": 2017,
            "group": "education",
            "value_usd": 120000000.0,
            "iati_id": "44000-P252350"
          },
          {
            "title": "Priority Skills for Growth and Youth Empowerment",
            "year": 2024,
            "group": "education",
            "value_usd": 107000000.0,
            "iati_id": "44000-P181050"
          },
          {
            "title": "Digital Acceleration Project",
            "year": 2021,
            "group": "ict_communications",
            "value_usd": 100000000.0,
            "iati_id": "44000-P173373"
          },
          {
            "title": "\u6559\u80b2\u30bb\u30af\u30bf\u30fc\u306e\u305f\u3081\u306e\u958b\u767a\u653f\u7b56\u501f\u6b3e",
            "year": 2024,
            "group": "education",
            "value_usd": 99400000.0,
            "iati_id": "XM-DAC-701-8-201902724"
          },
          {
            "title": "Human Resources Development Project",
            "year": 2020,
            "group": "education",
            "value_usd": 69300000.0,
            "iati_id": "XI-IATI-WBTF-P045091"
          },
          {
            "title": "2019 - Scholars Program Phase II",
            "year": 2019,
            "group": "education",
            "value_usd": 50737001.0,
            "iati_id": "CA-CRA_ACR-817387277-PROJECTS-1287"
          },
          {
            "title": "Scaling-up Early Childhood Development in Rwanda",
            "year": 2022,
            "group": "education",
            "value_usd": 50000000.0,
            "iati_id": "XI-IATI-EC_INTPA-2022-ACT-61240"
          }
        ]
      },
      "recurrent_cliff_analysis": {
        "cliff_risk_tier": "High External Reliance (Classroom Crowding Deficit)",
        "domestic_edu_to_comm_ratio": null,
        "narrative": "Rwanda absorbed $974.7M in external education assistance (surging 554% during COVID). However, missing domestic COFOG transparency and high student-teacher crowding limit sustainable recurring operations."
      },
      "macro_context": {
        "country_name": "Rwanda",
        "region": "SSA",
        "gdp_per_capita_usd": 1060.0,
        "internet_users_pct": 31.7,
        "fixed_broadband_per100": 0.6,
        "electricity_access_pct": 72.0,
        "rural_electricity_pct": 65.2,
        "urban_electricity_pct": 88.0,
        "learning_poverty_pct": null,
        "adult_literacy_pct": 78.8,
        "wb_education_pct_gdp": 4.61,
        "wb_education_pct_budget": 14.19
      }
    },
    "TZA": {
      "country_iso3": "TZA",
      "country_iso2": "TZ",
      "country_name": "Tanzania",
      "archetype": "Swahili Foundational Anchor vs. Severe Rural Energy Deficit",
      "domestic_fiscal": {
        "source": "IMF STA GFS (S1311B, 2018)",
        "has_imf_cofog": true,
        "education_pct_budget": 19.56,
        "education_pct_gdp": 4.07,
        "communication_pct_budget": null,
        "communication_pct_gdp": null,
        "transport_pct_budget": null,
        "transport_pct_gdp": null,
        "total_outlays_pct_gdp": 20.82,
        "annual_timeseries": {
          "2017": {
            "education_pct_gdp": 3.37,
            "education_pct_budget": 17.49,
            "communication_pct_gdp": null,
            "communication_pct_budget": null,
            "transport_pct_gdp": null,
            "transport_pct_budget": null,
            "total_outlays_pct_gdp": 19.25
          },
          "2018": {
            "education_pct_gdp": 4.07,
            "education_pct_budget": 19.56,
            "communication_pct_gdp": null,
            "communication_pct_budget": null,
            "transport_pct_gdp": null,
            "transport_pct_budget": null,
            "total_outlays_pct_gdp": 20.82
          }
        },
        "subfunctions": {}
      },
      "external_assistance": {
        "source": "IATI Datastore Solr API (2017-2024)",
        "education_disbursed_8yr_usd_m": 2052.05,
        "education_committed_8yr_usd_m": 2643.92,
        "ict_disbursed_8yr_usd_m": 130.67,
        "total_aid_disbursed_8yr_usd_m": 2182.72,
        "covid_2020_surge": {
          "disbursed_2019_usd_m": 137.2,
          "disbursed_2020_usd_m": 159.6,
          "surge_absolute_usd_m": 22.4,
          "surge_growth_pct": 16.3
        },
        "annual_timeseries": {
          "2017": {
            "education_disbursements_usd_m": 134.98,
            "education_commitments_usd_m": 175.52,
            "ict_disbursements_usd_m": 3.71,
            "ict_commitments_usd_m": 0.19,
            "total_disbursements_usd_m": 138.69,
            "total_commitments_usd_m": 175.71
          },
          "2018": {
            "education_disbursements_usd_m": 97.81,
            "education_commitments_usd_m": 81.12,
            "ict_disbursements_usd_m": 1.79,
            "ict_commitments_usd_m": 1.29,
            "total_disbursements_usd_m": 99.6,
            "total_commitments_usd_m": 82.41
          },
          "2019": {
            "education_disbursements_usd_m": 137.2,
            "education_commitments_usd_m": 157.48,
            "ict_disbursements_usd_m": 1.19,
            "ict_commitments_usd_m": 41.69,
            "total_disbursements_usd_m": 138.39,
            "total_commitments_usd_m": 199.18
          },
          "2020": {
            "education_disbursements_usd_m": 159.6,
            "education_commitments_usd_m": 516.52,
            "ict_disbursements_usd_m": 9.15,
            "ict_commitments_usd_m": 0.08,
            "total_disbursements_usd_m": 168.75,
            "total_commitments_usd_m": 516.6
          },
          "2021": {
            "education_disbursements_usd_m": 207.62,
            "education_commitments_usd_m": 1137.6,
            "ict_disbursements_usd_m": 13.72,
            "ict_commitments_usd_m": 152.44,
            "total_disbursements_usd_m": 221.34,
            "total_commitments_usd_m": 1290.05
          },
          "2022": {
            "education_disbursements_usd_m": 381.05,
            "education_commitments_usd_m": 277.32,
            "ict_disbursements_usd_m": 17.74,
            "ict_commitments_usd_m": 3.22,
            "total_disbursements_usd_m": 398.79,
            "total_commitments_usd_m": 280.54
          },
          "2023": {
            "education_disbursements_usd_m": 396.79,
            "education_commitments_usd_m": 160.86,
            "ict_disbursements_usd_m": 30.91,
            "ict_commitments_usd_m": 19.0,
            "total_disbursements_usd_m": 427.7,
            "total_commitments_usd_m": 179.87
          },
          "2024": {
            "education_disbursements_usd_m": 537.0,
            "education_commitments_usd_m": 137.5,
            "ict_disbursements_usd_m": 52.45,
            "ict_commitments_usd_m": 2.33,
            "total_disbursements_usd_m": 589.45,
            "total_commitments_usd_m": 139.82
          }
        },
        "top_initiatives": [
          {
            "title": "Tanzania Secondary Education Quality Improvement Project (SEQUIP)",
            "year": 2020,
            "group": "education",
            "value_usd": 500000000.0,
            "iati_id": "44000-P170480"
          },
          {
            "title": "Boost Primary Student Learning",
            "year": 2021,
            "group": "education",
            "value_usd": 500000000.0,
            "iati_id": "44000-P169380"
          },
          {
            "title": "Higher Education for Economic Transformation Project",
            "year": 2021,
            "group": "education",
            "value_usd": 425000000.0,
            "iati_id": "44000-P166415"
          },
          {
            "title": "Digital Tanzania Project",
            "year": 2021,
            "group": "ict_communications",
            "value_usd": 150000000.0,
            "iati_id": "44000-P160766"
          },
          {
            "title": "Tanzania Productive Social Safety Net Project II",
            "year": 2019,
            "group": "education",
            "value_usd": 121500000.0,
            "iati_id": "44000-P169165"
          },
          {
            "title": "Deliver activities at scale component and provide technical assistance to GoT to support the achievement of PbR  targets.",
            "year": 2021,
            "group": "education",
            "value_usd": 97280000.0,
            "iati_id": "GB-1-205254-102"
          },
          {
            "title": "TZ FCDO SHULE BORA (GBP)",
            "year": 2021,
            "group": "education",
            "value_usd": 89536000.0,
            "iati_id": "GB-COH-1110949-408224"
          },
          {
            "title": "TZ Education Program for Results",
            "year": 2017,
            "group": "education",
            "value_usd": 80000000.0,
            "iati_id": "44000-P147486"
          }
        ]
      },
      "recurrent_cliff_analysis": {
        "cliff_risk_tier": "Severe Infrastructure Void vs. Aid Volume",
        "domestic_edu_to_comm_ratio": null,
        "narrative": "Tanzania absorbed $2.05B in external education aid (top bilateral recipient), with 19.6% domestic education budget share, but a 47.6% national unelectrified rate creates a sharp hardware utilization barrier."
      },
      "macro_context": {
        "country_name": "Tanzania",
        "region": "SSA",
        "gdp_per_capita_usd": 1193.0,
        "internet_users_pct": 31.2,
        "fixed_broadband_per100": 0.25,
        "electricity_access_pct": 52.4,
        "rural_electricity_pct": 33.7,
        "urban_electricity_pct": 85.2,
        "learning_poverty_pct": null,
        "adult_literacy_pct": 78.2,
        "wb_education_pct_gdp": 3.16,
        "wb_education_pct_budget": 13.41
      }
    },
    "MUS": {
      "country_iso3": "MUS",
      "country_iso2": "MU",
      "country_name": "Mauritius",
      "archetype": "High-Income SIDS with Complete Electrification and Broadband",
      "domestic_fiscal": {
        "source": "IMF STA GFS (S13, 2025)",
        "has_imf_cofog": true,
        "education_pct_budget": 10.31,
        "education_pct_gdp": 3.78,
        "communication_pct_budget": 0.09,
        "communication_pct_gdp": 0.035,
        "transport_pct_budget": 3.34,
        "transport_pct_gdp": 1.22,
        "total_outlays_pct_gdp": 36.64,
        "annual_timeseries": {
          "2017": {
            "education_pct_gdp": 3.85,
            "education_pct_budget": 15.81,
            "communication_pct_gdp": null,
            "communication_pct_budget": null,
            "transport_pct_gdp": null,
            "transport_pct_budget": null,
            "total_outlays_pct_gdp": 24.36
          },
          "2018": {
            "education_pct_gdp": 3.73,
            "education_pct_budget": 15.42,
            "communication_pct_gdp": 0.038,
            "communication_pct_budget": 0.16,
            "transport_pct_gdp": 1.56,
            "transport_pct_budget": 6.45,
            "total_outlays_pct_gdp": 24.17
          },
          "2019": {
            "education_pct_gdp": 3.64,
            "education_pct_budget": 14.49,
            "communication_pct_gdp": 0.044,
            "communication_pct_budget": 0.18,
            "transport_pct_gdp": 1.47,
            "transport_pct_budget": 5.87,
            "total_outlays_pct_gdp": 25.09
          },
          "2020": {
            "education_pct_gdp": 4.2,
            "education_pct_budget": 12.53,
            "communication_pct_gdp": 0.052,
            "communication_pct_budget": 0.16,
            "transport_pct_gdp": 1.58,
            "transport_pct_budget": 4.73,
            "total_outlays_pct_gdp": 33.5
          },
          "2021": {
            "education_pct_gdp": 4.04,
            "education_pct_budget": 11.67,
            "communication_pct_gdp": 0.029,
            "communication_pct_budget": 0.08,
            "transport_pct_gdp": 1.79,
            "transport_pct_budget": 5.16,
            "total_outlays_pct_gdp": 34.63
          },
          "2022": {
            "education_pct_gdp": 3.65,
            "education_pct_budget": 12.19,
            "communication_pct_gdp": 0.031,
            "communication_pct_budget": 0.1,
            "transport_pct_gdp": 1.28,
            "transport_pct_budget": 4.28,
            "total_outlays_pct_gdp": 29.98
          },
          "2023": {
            "education_pct_gdp": 3.89,
            "education_pct_budget": 12.79,
            "communication_pct_gdp": 0.046,
            "communication_pct_budget": 0.15,
            "transport_pct_gdp": 1.52,
            "transport_pct_budget": 5.01,
            "total_outlays_pct_gdp": 30.45
          },
          "2024": {
            "education_pct_gdp": 3.36,
            "education_pct_budget": 10.32,
            "communication_pct_gdp": 0.038,
            "communication_pct_budget": 0.12,
            "transport_pct_gdp": 1.51,
            "transport_pct_budget": 4.63,
            "total_outlays_pct_gdp": 32.59
          },
          "2025": {
            "education_pct_gdp": 3.78,
            "education_pct_budget": 10.31,
            "communication_pct_gdp": 0.035,
            "communication_pct_budget": 0.09,
            "transport_pct_gdp": 1.22,
            "transport_pct_budget": 3.34,
            "total_outlays_pct_gdp": 36.64
          }
        },
        "subfunctions": {
          "GF091_T": {
            "code": "GF091_T",
            "name": "Pre-primary and primary education",
            "pct_gdp": 0.805,
            "pct_budget": 2.2
          },
          "GF092_T": {
            "code": "GF092_T",
            "name": "Secondary education",
            "pct_gdp": 0.788,
            "pct_budget": 2.15
          },
          "GF0930_T": {
            "code": "GF0930_T",
            "name": "Post-secondary non-tertiary education",
            "pct_gdp": 0.0,
            "pct_budget": 0.0
          },
          "GF094_T": {
            "code": "GF094_T",
            "name": "Tertiary education",
            "pct_gdp": 0.403,
            "pct_budget": 1.1
          },
          "GF0950_T": {
            "code": "GF0950_T",
            "name": "Education not definable by level",
            "pct_gdp": 0.226,
            "pct_budget": 0.62
          },
          "GF0960_T": {
            "code": "GF0960_T",
            "name": "Subsidiary services to education",
            "pct_gdp": 0.197,
            "pct_budget": 0.54
          },
          "GF0970_T": {
            "code": "GF0970_T",
            "name": "R&D Education",
            "pct_gdp": 0.0,
            "pct_budget": 0.0
          },
          "GF0980_T": {
            "code": "GF0980_T",
            "name": "Education n.e.c.",
            "pct_gdp": 1.36,
            "pct_budget": 3.71
          }
        }
      },
      "external_assistance": {
        "source": "IATI Datastore Solr API (2017-2024)",
        "education_disbursed_8yr_usd_m": 2.52,
        "education_committed_8yr_usd_m": 7.32,
        "ict_disbursed_8yr_usd_m": 0.0,
        "total_aid_disbursed_8yr_usd_m": 2.52,
        "covid_2020_surge": {
          "disbursed_2019_usd_m": 2.36,
          "disbursed_2020_usd_m": 0.02,
          "surge_absolute_usd_m": -2.34,
          "surge_growth_pct": -99.3
        },
        "annual_timeseries": {
          "2017": {
            "education_disbursements_usd_m": 0.02,
            "education_commitments_usd_m": 0.0,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 0.02,
            "total_commitments_usd_m": 0.0
          },
          "2018": {
            "education_disbursements_usd_m": 0.0,
            "education_commitments_usd_m": 0.01,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 0.0,
            "total_commitments_usd_m": 0.01
          },
          "2019": {
            "education_disbursements_usd_m": 2.36,
            "education_commitments_usd_m": 6.7,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 2.36,
            "total_commitments_usd_m": 6.7
          },
          "2020": {
            "education_disbursements_usd_m": 0.02,
            "education_commitments_usd_m": 0.0,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 0.02,
            "total_commitments_usd_m": 0.0
          },
          "2021": {
            "education_disbursements_usd_m": 0.0,
            "education_commitments_usd_m": 0.0,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 0.0,
            "total_commitments_usd_m": 0.0
          },
          "2022": {
            "education_disbursements_usd_m": 0.0,
            "education_commitments_usd_m": 0.0,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 0.0,
            "total_commitments_usd_m": 0.0
          },
          "2023": {
            "education_disbursements_usd_m": 0.0,
            "education_commitments_usd_m": 0.61,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 0.0,
            "total_commitments_usd_m": 0.61
          },
          "2024": {
            "education_disbursements_usd_m": 0.13,
            "education_commitments_usd_m": 0.0,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 0.13,
            "total_commitments_usd_m": 0.0
          }
        },
        "top_initiatives": [
          {
            "title": "ODA equity through Finnfund",
            "year": 2019,
            "group": "education",
            "value_usd": 6700000.0,
            "iati_id": "FI-3-2019-2019195005"
          },
          {
            "title": "Graduated Reintegration: Empowering women, girls and young people through reinforced transition from prison to community programme",
            "year": 2023,
            "group": "education",
            "value_usd": 605926.0,
            "iati_id": "XI-IATI-EC_INTPA-2023-PC-33094"
          }
        ]
      },
      "recurrent_cliff_analysis": {
        "cliff_risk_tier": "Self-Financed Universal SIDS Benchmark",
        "domestic_edu_to_comm_ratio": 114.6,
        "narrative": "Mauritius maintains complete school electrification (100%) and 73% internet saturation with minimal external aid dependency ($2.5M total), financed entirely through domestic tax revenues."
      },
      "macro_context": {
        "country_name": "Mauritius",
        "region": "SSA",
        "gdp_per_capita_usd": 11991.0,
        "internet_users_pct": 73.3,
        "fixed_broadband_per100": 27.97,
        "electricity_access_pct": 100.0,
        "rural_electricity_pct": 100.0,
        "urban_electricity_pct": 100.0,
        "learning_poverty_pct": null,
        "adult_literacy_pct": 94.3,
        "wb_education_pct_gdp": 4.25,
        "wb_education_pct_budget": 14.19
      }
    },
    "GHA": {
      "country_iso3": "GHA",
      "country_iso2": "GH",
      "country_name": "Ghana",
      "archetype": "West African Digital Frontrunner vs. Rural School Wiring Gap",
      "domestic_fiscal": {
        "source": "World Bank / UNESCO UIS Benchmark",
        "has_imf_cofog": false,
        "education_pct_budget": 13.18,
        "education_pct_gdp": 2.91,
        "communication_pct_budget": null,
        "communication_pct_gdp": null,
        "transport_pct_budget": null,
        "transport_pct_gdp": null,
        "total_outlays_pct_gdp": null,
        "annual_timeseries": {},
        "subfunctions": {}
      },
      "external_assistance": {
        "source": "IATI Datastore Solr API (2017-2024)",
        "education_disbursed_8yr_usd_m": 443.54,
        "education_committed_8yr_usd_m": 551.75,
        "ict_disbursed_8yr_usd_m": 223.51,
        "total_aid_disbursed_8yr_usd_m": 667.05,
        "covid_2020_surge": {
          "disbursed_2019_usd_m": 40.65,
          "disbursed_2020_usd_m": 94.51,
          "surge_absolute_usd_m": 53.86,
          "surge_growth_pct": 132.5
        },
        "annual_timeseries": {
          "2017": {
            "education_disbursements_usd_m": 76.04,
            "education_commitments_usd_m": 53.0,
            "ict_disbursements_usd_m": 14.8,
            "ict_commitments_usd_m": 0.6,
            "total_disbursements_usd_m": 90.83,
            "total_commitments_usd_m": 53.6
          },
          "2018": {
            "education_disbursements_usd_m": 25.37,
            "education_commitments_usd_m": 44.53,
            "ict_disbursements_usd_m": 16.07,
            "ict_commitments_usd_m": 11.3,
            "total_disbursements_usd_m": 41.45,
            "total_commitments_usd_m": 55.83
          },
          "2019": {
            "education_disbursements_usd_m": 40.65,
            "education_commitments_usd_m": 235.63,
            "ict_disbursements_usd_m": 12.6,
            "ict_commitments_usd_m": 21.36,
            "total_disbursements_usd_m": 53.25,
            "total_commitments_usd_m": 256.99
          },
          "2020": {
            "education_disbursements_usd_m": 94.51,
            "education_commitments_usd_m": 36.77,
            "ict_disbursements_usd_m": 44.47,
            "ict_commitments_usd_m": 121.54,
            "total_disbursements_usd_m": 138.98,
            "total_commitments_usd_m": 158.32
          },
          "2021": {
            "education_disbursements_usd_m": 49.23,
            "education_commitments_usd_m": 18.34,
            "ict_disbursements_usd_m": 7.19,
            "ict_commitments_usd_m": 0.39,
            "total_disbursements_usd_m": 56.41,
            "total_commitments_usd_m": 18.73
          },
          "2022": {
            "education_disbursements_usd_m": 32.49,
            "education_commitments_usd_m": 57.58,
            "ict_disbursements_usd_m": 24.71,
            "ict_commitments_usd_m": 200.33,
            "total_disbursements_usd_m": 57.2,
            "total_commitments_usd_m": 257.91
          },
          "2023": {
            "education_disbursements_usd_m": 51.05,
            "education_commitments_usd_m": 46.67,
            "ict_disbursements_usd_m": 58.42,
            "ict_commitments_usd_m": -24.79,
            "total_disbursements_usd_m": 109.48,
            "total_commitments_usd_m": 21.88
          },
          "2024": {
            "education_disbursements_usd_m": 74.19,
            "education_commitments_usd_m": 59.23,
            "ict_disbursements_usd_m": 45.25,
            "ict_commitments_usd_m": -1.43,
            "total_disbursements_usd_m": 119.45,
            "total_commitments_usd_m": 57.8
          }
        },
        "top_initiatives": [
          {
            "title": "Ghana Digital Acceleration Project",
            "year": 2022,
            "group": "ict_communications",
            "value_usd": 200000000.0,
            "iati_id": "44000-P176126"
          },
          {
            "title": "Ghana Accountability for Learning Outcomes Project",
            "year": 2019,
            "group": "education",
            "value_usd": 150000000.0,
            "iati_id": "44000-P165557"
          },
          {
            "title": "GH eTransform Ghana",
            "year": 2020,
            "group": "ict_communications",
            "value_usd": 101200000.0,
            "iati_id": "44000-P144140"
          },
          {
            "title": "2019 Scholars Program Phase II",
            "year": 2019,
            "group": "education",
            "value_usd": 51146451.0,
            "iati_id": "CA-CRA_ACR-817387277-PROJECTS-1181"
          },
          {
            "title": "Ghana Secondary Education Improvement Project",
            "year": 2017,
            "group": "education",
            "value_usd": 40000000.0,
            "iati_id": "44000-P145741"
          },
          {
            "title": "F\u00f6rderung beruflicher Bildung Promotion of vocational training IV",
            "year": 2022,
            "group": "education",
            "value_usd": 20200000.0,
            "iati_id": "DE-1-202068419"
          },
          {
            "title": "Ghana Jobs and Skills Project",
            "year": 2020,
            "group": "ict_communications",
            "value_usd": 20000000.0,
            "iati_id": "44000-P166996"
          },
          {
            "title": "Gender-Responsive Education and Transformation Transformation d'\u00e9ducation tenant compte des sexosp\u00e9cificit\u00e9s",
            "year": 2018,
            "group": "education",
            "value_usd": 19522389.0,
            "iati_id": "CA-3-D004676001"
          }
        ]
      },
      "recurrent_cliff_analysis": {
        "cliff_risk_tier": "Expanding Donor ICT Capital vs. Rural Electrification",
        "domestic_edu_to_comm_ratio": null,
        "narrative": "Ghana received $223.5M in targeted ICT aid alongside $443.5M in education disbursements, supporting rapid urban digital growth while rural primary electrification remains unfinished."
      },
      "macro_context": {
        "country_name": "Ghana",
        "region": "SSA",
        "gdp_per_capita_usd": 2419.0,
        "internet_users_pct": 72.2,
        "fixed_broadband_per100": 0.66,
        "electricity_access_pct": 91.9,
        "rural_electricity_pct": 82.6,
        "urban_electricity_pct": 98.6,
        "learning_poverty_pct": null,
        "adult_literacy_pct": 76.5,
        "wb_education_pct_gdp": 2.91,
        "wb_education_pct_budget": 13.18
      }
    },
    "NGA": {
      "country_iso3": "NGA",
      "country_iso2": "NG",
      "country_name": "Nigeria",
      "archetype": "Macro Startup Giant vs. Severe Federal Budget & Power Gap",
      "domestic_fiscal": {
        "source": "World Bank / UNESCO UIS Benchmark",
        "has_imf_cofog": false,
        "education_pct_budget": 2.98,
        "education_pct_gdp": 0.32,
        "communication_pct_budget": null,
        "communication_pct_gdp": null,
        "transport_pct_budget": null,
        "transport_pct_gdp": null,
        "total_outlays_pct_gdp": null,
        "annual_timeseries": {},
        "subfunctions": {}
      },
      "external_assistance": {
        "source": "IATI Datastore Solr API (2017-2024)",
        "education_disbursed_8yr_usd_m": 1973.55,
        "education_committed_8yr_usd_m": 3488.9,
        "ict_disbursed_8yr_usd_m": 158.35,
        "total_aid_disbursed_8yr_usd_m": 2131.91,
        "covid_2020_surge": {
          "disbursed_2019_usd_m": 148.47,
          "disbursed_2020_usd_m": 145.43,
          "surge_absolute_usd_m": -3.05,
          "surge_growth_pct": -2.1
        },
        "annual_timeseries": {
          "2017": {
            "education_disbursements_usd_m": 105.09,
            "education_commitments_usd_m": 740.88,
            "ict_disbursements_usd_m": 50.04,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 155.13,
            "total_commitments_usd_m": 740.88
          },
          "2018": {
            "education_disbursements_usd_m": 166.87,
            "education_commitments_usd_m": 73.56,
            "ict_disbursements_usd_m": 0.24,
            "ict_commitments_usd_m": 2.24,
            "total_disbursements_usd_m": 167.12,
            "total_commitments_usd_m": 75.81
          },
          "2019": {
            "education_disbursements_usd_m": 148.47,
            "education_commitments_usd_m": 128.59,
            "ict_disbursements_usd_m": 0.28,
            "ict_commitments_usd_m": 0.13,
            "total_disbursements_usd_m": 148.76,
            "total_commitments_usd_m": 128.72
          },
          "2020": {
            "education_disbursements_usd_m": 145.43,
            "education_commitments_usd_m": 991.89,
            "ict_disbursements_usd_m": 10.36,
            "ict_commitments_usd_m": 99.03,
            "total_disbursements_usd_m": 155.78,
            "total_commitments_usd_m": 1090.92
          },
          "2021": {
            "education_disbursements_usd_m": 254.76,
            "education_commitments_usd_m": 168.08,
            "ict_disbursements_usd_m": 0.2,
            "ict_commitments_usd_m": 11.92,
            "total_disbursements_usd_m": 254.96,
            "total_commitments_usd_m": 179.99
          },
          "2022": {
            "education_disbursements_usd_m": 425.31,
            "education_commitments_usd_m": 363.86,
            "ict_disbursements_usd_m": 23.76,
            "ict_commitments_usd_m": 217.32,
            "total_disbursements_usd_m": 449.08,
            "total_commitments_usd_m": 581.18
          },
          "2023": {
            "education_disbursements_usd_m": 439.07,
            "education_commitments_usd_m": 887.68,
            "ict_disbursements_usd_m": 23.89,
            "ict_commitments_usd_m": 54.28,
            "total_disbursements_usd_m": 462.95,
            "total_commitments_usd_m": 941.96
          },
          "2024": {
            "education_disbursements_usd_m": 288.56,
            "education_commitments_usd_m": 134.35,
            "ict_disbursements_usd_m": 49.58,
            "ict_commitments_usd_m": 7.57,
            "total_disbursements_usd_m": 338.13,
            "total_commitments_usd_m": 141.92
          }
        },
        "top_initiatives": [
          {
            "title": "Better Education Service Delivery for All",
            "year": 2017,
            "group": "education",
            "value_usd": 578000000.0,
            "iati_id": "44000-P160430"
          },
          {
            "title": "Adolescent Girls Initiative for Learning and Empowerment",
            "year": 2020,
            "group": "education",
            "value_usd": 465000000.0,
            "iati_id": "44000-P170664"
          },
          {
            "title": "Nigeria: State Action on Business Enabling Reforms (SABER) Program",
            "year": 2022,
            "group": "ict_communications",
            "value_usd": 210000000.0,
            "iati_id": "44000-P177442"
          },
          {
            "title": "Innovation Development and Effectiveness in the Acquisition of Skills (IDEAS) Project",
            "year": 2020,
            "group": "education",
            "value_usd": 200000000.0,
            "iati_id": "44000-P166239"
          },
          {
            "title": "Nigeria Human Capital Opportunities for Prosperity and Equity (HOPE) - Governance",
            "year": 2024,
            "group": "education",
            "value_usd": 155000000.0,
            "iati_id": "44000-P181476"
          },
          {
            "title": "Partnership for Learning for All in Nigerian Education - Procurement of Services",
            "year": 2021,
            "group": "education",
            "value_usd": 116214281.0,
            "iati_id": "GB-GOV-1-300416-101"
          },
          {
            "title": "UNICEF - Safe, Inclusive Learning and Skills for All (SILSA)",
            "year": 2022,
            "group": "education",
            "value_usd": 104000000.0,
            "iati_id": "NO-BRC-971277882-NGA-22/0001"
          },
          {
            "title": "Financement du programme d'investissement dans les entreprises digitales et cr\u00e9atives (i-DICE)",
            "year": 2023,
            "group": "education",
            "value_usd": 103896807.0,
            "iati_id": "FR-3-CNG113701"
          }
        ]
      },
      "recurrent_cliff_analysis": {
        "cliff_risk_tier": "Severe Macro Federal Budget Deficit",
        "domestic_edu_to_comm_ratio": null,
        "narrative": "Federal education budget allocation is critically low (~3.0%), leaving external development assistance ($1.97B disbursed) to shoulder foundational infrastructure and emergency learning programs."
      },
      "macro_context": {
        "country_name": "Nigeria",
        "region": "SSA",
        "gdp_per_capita_usd": 1084.0,
        "internet_users_pct": 41.2,
        "fixed_broadband_per100": 0.08,
        "electricity_access_pct": 62.5,
        "rural_electricity_pct": 23.5,
        "urban_electricity_pct": 85.5,
        "learning_poverty_pct": null,
        "adult_literacy_pct": 70.4,
        "wb_education_pct_gdp": 0.32,
        "wb_education_pct_budget": 2.98
      }
    },
    "ZMB": {
      "country_iso3": "ZMB",
      "country_iso2": "ZM",
      "country_name": "Zambia",
      "archetype": "Severe Rural Infrastructure Deficit & High Linguistic Fragmentation",
      "domestic_fiscal": {
        "source": "IMF STA GFS (S1311B, 2024)",
        "has_imf_cofog": true,
        "education_pct_budget": 14.6,
        "education_pct_gdp": 3.25,
        "communication_pct_budget": 0.64,
        "communication_pct_gdp": 0.142,
        "transport_pct_budget": 0.33,
        "transport_pct_gdp": 0.07,
        "total_outlays_pct_gdp": 22.28,
        "annual_timeseries": {
          "2017": {
            "education_pct_gdp": 3.77,
            "education_pct_budget": 15.05,
            "communication_pct_gdp": 0.002,
            "communication_pct_budget": 0.01,
            "transport_pct_gdp": 0.0,
            "transport_pct_budget": 0.01,
            "total_outlays_pct_gdp": 25.05
          },
          "2019": {
            "education_pct_gdp": 3.03,
            "education_pct_budget": 10.52,
            "communication_pct_gdp": 0.001,
            "communication_pct_budget": 0.0,
            "transport_pct_gdp": 0.0,
            "transport_pct_budget": 0.01,
            "total_outlays_pct_gdp": 28.8
          },
          "2020": {
            "education_pct_gdp": 2.84,
            "education_pct_budget": 10.74,
            "communication_pct_gdp": 0.042,
            "communication_pct_budget": 0.16,
            "transport_pct_gdp": 0.07,
            "transport_pct_budget": 0.27,
            "total_outlays_pct_gdp": 26.45
          },
          "2021": {
            "education_pct_gdp": 2.39,
            "education_pct_budget": 8.82,
            "communication_pct_gdp": 0.098,
            "communication_pct_budget": 0.36,
            "transport_pct_gdp": 0.07,
            "transport_pct_budget": 0.25,
            "total_outlays_pct_gdp": 27.11
          },
          "2022": {
            "education_pct_gdp": 2.7,
            "education_pct_budget": 10.59,
            "communication_pct_gdp": 0.2,
            "communication_pct_budget": 0.78,
            "transport_pct_gdp": 0.07,
            "transport_pct_budget": 0.29,
            "total_outlays_pct_gdp": 25.54
          },
          "2023": {
            "education_pct_gdp": 3.51,
            "education_pct_budget": 14.17,
            "communication_pct_gdp": 0.204,
            "communication_pct_budget": 0.82,
            "transport_pct_gdp": 0.1,
            "transport_pct_budget": 0.42,
            "total_outlays_pct_gdp": 24.76
          },
          "2024": {
            "education_pct_gdp": 3.25,
            "education_pct_budget": 14.6,
            "communication_pct_gdp": 0.142,
            "communication_pct_budget": 0.64,
            "transport_pct_gdp": 0.07,
            "transport_pct_budget": 0.33,
            "total_outlays_pct_gdp": 22.28
          }
        },
        "subfunctions": {
          "GF091_T": {
            "code": "GF091_T",
            "name": "Pre-primary and primary education",
            "pct_gdp": 0.012,
            "pct_budget": 0.05
          },
          "GF092_T": {
            "code": "GF092_T",
            "name": "Secondary education",
            "pct_gdp": 0.26,
            "pct_budget": 1.17
          },
          "GF0930_T": {
            "code": "GF0930_T",
            "name": "Post-secondary non-tertiary education",
            "pct_gdp": 0.0,
            "pct_budget": 0.0
          },
          "GF094_T": {
            "code": "GF094_T",
            "name": "Tertiary education",
            "pct_gdp": 0.013,
            "pct_budget": 0.06
          },
          "GF0950_T": {
            "code": "GF0950_T",
            "name": "Education not definable by level",
            "pct_gdp": 0.0,
            "pct_budget": 0.0
          },
          "GF0960_T": {
            "code": "GF0960_T",
            "name": "Subsidiary services to education",
            "pct_gdp": 0.0,
            "pct_budget": 0.0
          },
          "GF0970_T": {
            "code": "GF0970_T",
            "name": "R&D Education",
            "pct_gdp": 0.0,
            "pct_budget": 0.0
          },
          "GF0980_T": {
            "code": "GF0980_T",
            "name": "Education n.e.c.",
            "pct_gdp": 2.969,
            "pct_budget": 13.32
          }
        }
      },
      "external_assistance": {
        "source": "IATI Datastore Solr API (2017-2024)",
        "education_disbursed_8yr_usd_m": 380.61,
        "education_committed_8yr_usd_m": 537.1,
        "ict_disbursed_8yr_usd_m": 3.78,
        "total_aid_disbursed_8yr_usd_m": 384.39,
        "covid_2020_surge": {
          "disbursed_2019_usd_m": 26.58,
          "disbursed_2020_usd_m": 93.36,
          "surge_absolute_usd_m": 66.78,
          "surge_growth_pct": 251.2
        },
        "annual_timeseries": {
          "2017": {
            "education_disbursements_usd_m": 7.98,
            "education_commitments_usd_m": 67.58,
            "ict_disbursements_usd_m": 0.08,
            "ict_commitments_usd_m": 0.08,
            "total_disbursements_usd_m": 8.06,
            "total_commitments_usd_m": 67.66
          },
          "2018": {
            "education_disbursements_usd_m": 19.38,
            "education_commitments_usd_m": 5.12,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.64,
            "total_disbursements_usd_m": 19.38,
            "total_commitments_usd_m": 5.76
          },
          "2019": {
            "education_disbursements_usd_m": 26.58,
            "education_commitments_usd_m": 8.96,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 26.58,
            "total_commitments_usd_m": 8.96
          },
          "2020": {
            "education_disbursements_usd_m": 93.36,
            "education_commitments_usd_m": 166.3,
            "ict_disbursements_usd_m": 0.1,
            "ict_commitments_usd_m": 0.63,
            "total_disbursements_usd_m": 93.46,
            "total_commitments_usd_m": 166.93
          },
          "2021": {
            "education_disbursements_usd_m": 35.65,
            "education_commitments_usd_m": 62.4,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 35.65,
            "total_commitments_usd_m": 62.4
          },
          "2022": {
            "education_disbursements_usd_m": 71.68,
            "education_commitments_usd_m": 65.27,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.0,
            "total_disbursements_usd_m": 71.68,
            "total_commitments_usd_m": 65.27
          },
          "2023": {
            "education_disbursements_usd_m": 41.6,
            "education_commitments_usd_m": 88.16,
            "ict_disbursements_usd_m": 0.0,
            "ict_commitments_usd_m": 0.2,
            "total_disbursements_usd_m": 41.6,
            "total_commitments_usd_m": 88.36
          },
          "2024": {
            "education_disbursements_usd_m": 84.39,
            "education_commitments_usd_m": 73.31,
            "ict_disbursements_usd_m": 3.6,
            "ict_commitments_usd_m": 97.2,
            "total_disbursements_usd_m": 87.99,
            "total_commitments_usd_m": 170.51
          }
        },
        "top_initiatives": [
          {
            "title": "Transport Corridors for Economic Resilience (TRACER)",
            "year": 2024,
            "group": "ict_communications",
            "value_usd": 97200000.0,
            "iati_id": "44000-P180801"
          },
          {
            "title": "Transfer Agreement  FTI CF",
            "year": 2020,
            "group": "education",
            "value_usd": 60200000.0,
            "iati_id": "XI-IATI-WBTF-P118273"
          },
          {
            "title": "Zambia Education Enhancement Project",
            "year": 2017,
            "group": "education",
            "value_usd": 60000000.0,
            "iati_id": "44000-P158570"
          },
          {
            "title": "Girls' Education and Women's Empowerment and Livelihood Project",
            "year": 2020,
            "group": "education",
            "value_usd": 35500000.0,
            "iati_id": "44000-P151451"
          },
          {
            "title": "Zambeef III ZMW",
            "year": 2022,
            "group": "education",
            "value_usd": 35000000.0,
            "iati_id": "XM-DAC-903-SII-46603"
          },
          {
            "title": "STEM\uff08\u79d1\u5b66\u3001\u6280\u8853\u3001\u5de5\u5b66\u53ca\u3073\u6570\u5b66\uff09\u6559\u80b2\u5f37\u5316\u8a08\u753b",
            "year": 2024,
            "group": "education",
            "value_usd": 11672400.0,
            "iati_id": "XM-DAC-701-8-202109201"
          },
          {
            "title": "Hei Verden - Multiannual agreement 2021-2025",
            "year": 2021,
            "group": "education",
            "value_usd": 9750000.0,
            "iati_id": "NO-BRC-971277882-ZAM-20/0001"
          },
          {
            "title": "Contribution Agreement with UNICEF - Equal Chances for Human Development",
            "year": 2024,
            "group": "education",
            "value_usd": 9625776.0,
            "iati_id": "XI-IATI-EC_INTPA-2024-PC-37794"
          }
        ]
      },
      "recurrent_cliff_analysis": {
        "cliff_risk_tier": "Moderate Domestic Envelope & Sustained Aid Reliance",
        "domestic_edu_to_comm_ratio": 22.8,
        "narrative": "Zambia dedicates 14.6% of budget to education and 0.64% to communication. External assistance ($380.6M) surged 262% during COVID to bridge severe rural learning divides."
      },
      "macro_context": {
        "country_name": "Zambia",
        "region": "SSA",
        "gdp_per_capita_usd": 1187.0,
        "internet_users_pct": 17.1,
        "fixed_broadband_per100": 0.79,
        "electricity_access_pct": 53.6,
        "rural_electricity_pct": 31.3,
        "urban_electricity_pct": 80.3,
        "learning_poverty_pct": 98.5,
        "adult_literacy_pct": 71.8,
        "wb_education_pct_gdp": 4.07,
        "wb_education_pct_budget": 15.38
      }
    }
  }
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { MACRO_FISCAL_DATA };
}
