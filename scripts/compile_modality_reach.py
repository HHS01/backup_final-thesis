#!/usr/bin/env python3
"""
compile_modality_reach.py
=========================

Compile empirical EdTech *delivery-modality reach*, *friction indices* and a
*policy-investment discrepancy* for one country into dashboard-ready JSON.
Standard library only (Python 3.8+).

USAGE
-----
    python compile_modality_reach.py # KEN, default output
    python compile_modality_reach.py --country GHA --output out/gha.json
    python compile_modality_reach.py --country KEN --custom-input my_survey.json

DESIGN PRINCIPLES (read these before trusting any number)
---------------------------------------------------------
1. Nothing is invented. A modality with no empirical estimate gets
   reach = null and status "no_empirical_data". It is never imputed.
2. Reach is NOT additive. Households use several modalities at once, so the
   six reach figures can sum to more than 100 %. Only "share of summed reach"
   is computed for the policy comparison, and it is labelled as such.
3. Denominators matter. Only estimates whose denominator is "all_students"
   enter the reach summary. Conditional figures (e.g. "% of children who had
   access to learning continuity") are kept but excluded, with the reason.
4. Friction indices are ANALYST-ASSIGNED, not measured. Each is
   1 + 4 x dependency x stress, where "dependency" (0-1) is a documented prior
   for how much a modality relies on that infrastructure and "stress" (0-1)
   is a country-level indicator transform. Every component is exported so a
   reviewer can challenge it. Missing indicators fall back to a neutral 0.5
   stress and are flagged.
5. Budget shares are never defaulted. They must come from --custom-input.
   Without them the policy discrepancy is null.
6. Built-in baseline values are transcribed from secondary write-ups and are
   all marked verify=true. Check them against the primary sources.

CUSTOM INPUT (--custom-input)
-----------------------------
JSON object (any key optional):
{
  "country": "KEN", # must match --country if present
  "replace_default_estimates": false, # true = discard ALL built-in estimates
  "estimates": [
    {"modality": "radio", "metric": "reach_pct", "value": 31.5,
     "study": "My survey", "year": 2025, "scope": "National",
     "denominator": "all_students", "confidence": "medium",
     "n": 1200, "source": "https://...", "note": ""}
  ],
  "context": {"electricity_access_pct": 76.5,
              "handset_cost_pct_monthly_income": 40,
              "data_cost_pct_monthly_income": 4.1},
  "budget_share_pct": {"radio": 5, "tv": 10, "app_lms": 60, "genai": 5},
  "friction_overrides": {"radio": {"hardware": 1.5}}
}
Modalities: radio, tv, sms_ussd, offline_sneakernet, app_lms, genai
            (+ "any" with metric any_pct for "used at least one platform").
Metrics: reach_pct (usage), access_pct (household access/ownership), any_pct.
A custom estimate REPLACES the built-in estimates for the same
(modality, metric) pair; other built-ins are kept.

CSV (long format), header row required:
  record_type,modality,key,value,study,year,scope,denominator,confidence,n,source,note
  record_type = estimate | context | budget | friction
  estimate: key = reach_pct | access_pct | any_pct (modality "any" for any_pct)
  context: modality blank, key = electricity_access_pct | ...
  budget: key = budget_share_pct
  friction: key = hardware | data | electricity (value 1-5)
"""

import argparse
import csv
import json
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_VERSION = "1.0.0"
SCHEMA_VERSION = "1.0"

# --------------------------------------------------------------------------
# Configuration (all assumptions live here so they are easy to audit/change)
# --------------------------------------------------------------------------
NEUTRAL_STRESS = 0.5  # used when a country indicator is missing
DATA_COST_CEILING_PCT = 10.0  # 1 GB at >=10 % of monthly income => stress 1.0
DIVERGENCE_THRESHOLD_PP = 15.0  # flag when studies disagree by more than this
POLICY_ALIGNED_BAND_PP = 5.0  # |budget share - reach share| <= 5 pp => aligned

DIMENSIONS = ("hardware", "data", "electricity")
DIM_LABELS = {
    "hardware": "Hardware capital barrier",
    "data": "Recurring data/airtime cost",
    "electricity": "Electricity grid dependency",
}

MODALITY_ORDER = ["radio", "tv", "sms_ussd", "offline_sneakernet", "app_lms", "genai"]

# dependency = analyst prior (0-1) of how much the modality relies on each
# infrastructure dimension. These are judgements, not measurements.
MODALITIES = {
    "radio": {
        "label": "Broadcast Radio (Interactive Radio Instruction)",
        "examples": ["Interactive Radio Instruction", "ministry radio lessons"],
        "dependency": {"hardware": 0.2, "data": 0.0, "electricity": 0.3},
        "rationale": "Cheap, often already owned; free-to-air; battery/solar sets work off-grid.",
    },
    "tv": {
        "label": "Educational Television",
        "examples": ["Ubongo", "ministry TV lessons"],
        "dependency": {"hardware": 0.6, "data": 0.0, "electricity": 0.9},
        "rationale": "Needs a TV set and mains power; free-to-air reception assumed.",
    },
    "sms_ussd": {
        "label": "Basic SMS / USSD",
        "examples": ["Eneza Shupavu291"],
        "dependency": {"hardware": 0.1, "data": 0.5, "electricity": 0.3},
        "rationale": "Works on any basic phone; airtime/SMS fees; only phone charging needed.",
    },
    "offline_sneakernet": {
        "label": "Asynchronous Offline / Sneakernet",
        "examples": ["SD cards", "Kolibri", "local microservers"],
        "dependency": {"hardware": 0.7, "data": 0.05, "electricity": 0.5},
        "rationale": "Devices/servers are a capital cost; little recurring data; needs charging.",
    },
    "app_lms": {
        "label": "Mobile App / Web LMS (cloud-native)",
        "examples": ["curriculum apps", "web learning platforms"],
        "dependency": {"hardware": 0.8, "data": 1.0, "electricity": 0.6},
        "rationale": "Smartphone or computer plus continuous data; regular charging.",
    },
    "genai": {
        "label": "Generative AI / Cloud AI tools",
        "examples": ["general-purpose chatbots", "AI tutors"],
        "dependency": {"hardware": 0.8, "data": 1.0, "electricity": 0.7},
        "rationale": "Smartphone/computer, heavy data use and reliable connectivity.",
    },
}

VALID_METRICS = {"reach_pct", "access_pct", "any_pct"}
VALID_CONTEXT_KEYS = {
    "electricity_access_pct",
    "handset_cost_pct_monthly_income",
    "data_cost_pct_monthly_income",
}

# --------------------------------------------------------------------------
# Built-in baseline (Kenya). ALL values are verify=true: transcribed from
# secondary write-ups, not from the primary datasets.
# --------------------------------------------------------------------------
BUSIA_URL = ("https://medium.com/center-for-effective-global-action/"
             "how-well-are-remote-learning-tools-reaching-students-in-kenya-d8c8461c7f88")
UWEZO_URL = "https://docs.edtechhub.org/lib/LHJ3UUUE/download/UTJVFEWG"

DEFAULT_ESTIMATES = [
    # --- Busia County remote-learning study (sub-national, school closures) ---
    {"country": "KEN", "modality": "radio", "metric": "reach_pct", "value": 44.0,
     "study": "Busia County remote learning study", "year": 2020,
     "scope": "Busia County (sub-national)", "denominator": "all_students",
     "confidence": "medium", "n": None, "source": BUSIA_URL,
     "note": "Used in the previous week.", "verify": True},
    {"country": "KEN", "modality": "tv", "metric": "reach_pct", "value": 26.0,
     "study": "Busia County remote learning study", "year": 2020,
     "scope": "Busia County (sub-national)", "denominator": "all_students",
     "confidence": "medium", "n": None, "source": BUSIA_URL,
     "note": "Used in the previous week.", "verify": True},
    {"country": "KEN", "modality": "sms_ussd", "metric": "reach_pct", "value": 18.0,
     "study": "Busia County remote learning study", "year": 2020,
     "scope": "Busia County (sub-national)", "denominator": "all_students",
     "confidence": "medium", "n": None, "source": BUSIA_URL,
     "note": "Used in the previous week.", "verify": True},
    {"country": "KEN", "modality": "any", "metric": "any_pct", "value": 67.0,
     "study": "Busia County remote learning study", "year": 2020,
     "scope": "Busia County (sub-national)", "denominator": "all_students",
     "confidence": "medium", "n": None, "source": BUSIA_URL,
     "note": "Used at least one EdTech platform in the previous week.", "verify": True},
    # --- Uwezo Kenya household survey (national) ---
    {"country": "KEN", "modality": "radio", "metric": "reach_pct", "value": 19.0,
     "study": "Uwezo Kenya household survey", "year": 2021,
     "scope": "Kenya (national household survey)", "denominator": "all_students",
     "confidence": "low", "n": None, "source": UWEZO_URL,
     "note": "Listened to radio lessons. Denominator and year to be verified.",
     "verify": True},
    {"country": "KEN", "modality": "radio", "metric": "access_pct", "value": 62.0,
     "study": "Uwezo Kenya household survey", "year": 2021,
     "scope": "Kenya (national household survey)", "denominator": "all_households",
     "confidence": "medium", "n": None, "source": UWEZO_URL,
     "note": "Household owns a radio.", "verify": True},
    {"country": "KEN", "modality": "tv", "metric": "access_pct", "value": 45.0,
     "study": "Uwezo Kenya household survey", "year": 2021,
     "scope": "Kenya (national household survey)", "denominator": "all_households",
     "confidence": "medium", "n": None, "source": UWEZO_URL,
     "note": "Household owns a TV.", "verify": True},
    # Conditional denominator: kept for the record, excluded from reach.
    {"country": "KEN", "modality": "tv", "metric": "reach_pct", "value": 42.0,
     "study": "Uwezo Kenya household survey", "year": 2021,
     "scope": "Kenya (national household survey)",
     "denominator": "conditional_students_with_learning_continuity_access",
     "confidence": "medium", "n": None, "source": UWEZO_URL,
     "note": "Share among children who had access to learning continuity, "
             "NOT among all students.", "verify": True},
]

DEFAULT_CONTEXT = {
    "handset_cost_pct_monthly_income": {
        "value": 87.0,
        "status": "regional_proxy",
        "source": "GSMA State of Mobile Internet Connectivity 2025 (Sub-Saharan Africa, "
                  "entry-level handset, poorest 20% of users)",
        "caveat": "Regional, poorest-quintile figure; overstates stress for the average household.",
    },
    "electricity_access_pct": {
        "value": 77.0,
        "status": "world_bank_wdi",
        "source": "World Bank SE4ALL Database 2024 (Kenya national electrification)",
        "caveat": "National aggregate; rural electrification is lower (67.1%).",
    },
    "data_cost_pct_monthly_income": {
        "value": 3.8,
        "status": "itu_a4ai",
        "source": "ITU / A4AI 2023 Price Basket (Kenya, 1GB data as % of monthly income)",
        "caveat": "National average; can consume 8-15% of lower-quintile rural monthly income.",
    }
}


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------
class InputError(Exception):
    """Raised for invalid user input; reported without a traceback."""


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def to_float(value, label):
    if isinstance(value, bool):
        raise InputError("%s: boolean is not a number" % label)
    try:
        f = float(str(value).strip().replace("%", ""))
    except (TypeError, ValueError):
        raise InputError("%s: %r is not a number" % (label, value))
    if f != f or f in (float("inf"), float("-inf")):
        raise InputError("%s: value must be finite" % label)
    return f


def pct(value, label):
    f = to_float(value, label)
    if not 0.0 <= f <= 100.0:
        raise InputError("%s: %s is outside 0-100" % (label, f))
    return f


def opt_int(value, label):
    if value in (None, ""):
        return None
    f = to_float(value, label)
    if f < 0 or f != int(f):
        raise InputError("%s: must be a non-negative integer" % label)
    return int(f)


def r1(x):
    return None if x is None else round(x, 1)


# --------------------------------------------------------------------------
# Custom input parsing
# --------------------------------------------------------------------------
def normalise_estimate(raw, country, origin, where):
    modality = str(raw.get("modality", "")).strip().lower()
    metric = str(raw.get("metric", "")).strip().lower()
    if metric not in VALID_METRICS:
        raise InputError("%s: metric %r not in %s" % (where, metric, sorted(VALID_METRICS)))
    if metric == "any_pct":
        if modality != "any":
            raise InputError("%s: any_pct requires modality 'any'" % where)
    elif modality not in MODALITIES:
        raise InputError("%s: unknown modality %r (valid: %s)"
                         % (where, modality, ", ".join(MODALITY_ORDER)))
    default_den = "all_households" if metric == "access_pct" else "all_students"
    year = raw.get("year")
    year = None if year in (None, "") else int(to_float(year, where + " year"))
    return {
        "country": country,
        "modality": modality,
        "metric": metric,
        "value": pct(raw.get("value"), where + " value"),
        "study": str(raw.get("study") or "Custom input"),
        "year": year,
        "scope": str(raw.get("scope") or "Custom input"),
        "denominator": str(raw.get("denominator") or default_den).strip().lower(),
        "confidence": str(raw.get("confidence") or "medium").strip().lower(),
        "n": opt_int(raw.get("n"), where + " n"),
        "source": str(raw.get("source") or ""),
        "note": str(raw.get("note") or ""),
        "verify": False,
        "origin": origin,
    }


def parse_custom_json(path, country):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise InputError("cannot read custom JSON %s: %s" % (path, exc))
    if not isinstance(data, dict):
        raise InputError("custom JSON must be an object at top level")
    file_country = data.get("country")
    if file_country and str(file_country).upper() != country:
        raise InputError("custom input is for country %s but --country is %s"
                         % (file_country, country))
    out = {"replace": bool(data.get("replace_default_estimates", False)),
           "estimates": [], "context": {}, "budget": {}, "friction": {}}
    for i, raw in enumerate(data.get("estimates") or [], 1):
        out["estimates"].append(
            normalise_estimate(raw, country, "custom_input", "estimates[%d]" % i))
    for key, val in (data.get("context") or {}).items():
        out["context"][key] = val
    for mod, val in (data.get("budget_share_pct") or {}).items():
        out["budget"][mod] = val
    for mod, dims in (data.get("friction_overrides") or {}).items():
        for dim, val in (dims or {}).items():
            out["friction"][(mod, dim)] = val
    return out


def parse_custom_csv(path, country):
    out = {"replace": False, "estimates": [], "context": {}, "budget": {}, "friction": {}}
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            rows = list(csv.DictReader(fh))
    except OSError as exc:
        raise InputError("cannot read custom CSV %s: %s" % (path, exc))
    if not rows:
        raise InputError("custom CSV has no data rows")
    for i, row in enumerate(rows, 2):  # header is line 1
        row = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
        rtype = row.get("record_type", "").lower()
        where = "CSV line %d" % i
        key = row.get("key", "").lower()
        mod = row.get("modality", "").lower()
        if rtype == "estimate":
            raw = dict(row, metric=key)
            out["estimates"].append(normalise_estimate(raw, country, "custom_input", where))
        elif rtype == "context":
            out["context"][key] = row.get("value")
        elif rtype == "budget":
            out["budget"][mod] = row.get("value")
        elif rtype == "friction":
            out["friction"][(mod, key)] = row.get("value")
        else:
            raise InputError("%s: unknown record_type %r" % (where, rtype))
    return out


def load_custom(path, country):
    if not path:
        return {"replace": False, "estimates": [], "context": {}, "budget": {}, "friction": {}}
    suffix = Path(path).suffix.lower()
    if suffix == ".json":
        return parse_custom_json(path, country)
    if suffix == ".csv":
        return parse_custom_csv(path, country)
    raise InputError("--custom-input must be a .json or .csv file")


# --------------------------------------------------------------------------
# Core computations
# --------------------------------------------------------------------------
def build_estimates(country, custom):
    base = [] if custom["replace"] else [
        dict(e, origin="default_baseline") for e in DEFAULT_ESTIMATES if e["country"] == country]
    overridden = {(e["modality"], e["metric"]) for e in custom["estimates"]}
    kept = [e for e in base if (e["modality"], e["metric"]) not in overridden]
    dropped = [e for e in base if (e["modality"], e["metric"]) in overridden]
    return kept + custom["estimates"], sorted(overridden), dropped


def summarise_reach(estimates):
    """Summarise reach_pct estimates for one modality."""
    reach = [e for e in estimates if e["metric"] == "reach_pct"]
    usable = [e for e in reach if e["denominator"] == "all_students"]
    excluded = [{"value": e["value"], "study": e["study"],
                 "reason": "denominator is '%s', not 'all_students'" % e["denominator"]}
                for e in reach if e["denominator"] != "all_students"]
    flags = []
    if not usable:
        status = "only_conditional_estimates" if excluded else "no_empirical_data"
        return {"central_pct": None, "low_pct": None, "high_pct": None,
                "n_estimates": 0, "status": status, "estimates": [],
                "excluded_estimates": excluded, "flags": flags}
    values = [e["value"] for e in usable]
    low, high = min(values), max(values)
    central = statistics.median(values)
    status = "single_study" if len(values) == 1 else "multi_study"
    if len(values) > 1 and (high - low) > DIVERGENCE_THRESHOLD_PP:
        flags.append("estimates diverge by %.1f pp (different populations, "
                     "periods or denominators); treat the central value as indicative"
                     % (high - low))
    if len({e["scope"] for e in usable}) > 1:
        flags.append("mixes sub-national and national scopes")
    if any(e["confidence"] == "low" for e in usable):
        flags.append("includes a low-confidence estimate")
    if any(e.get("verify") for e in usable):
        flags.append("built-in value(s) not yet checked against the primary source")
    clean = [{k: e[k] for k in ("value", "study", "year", "scope", "denominator",
                                 "confidence", "n", "source", "note", "origin")}
             for e in usable]
    return {"central_pct": r1(central), "low_pct": r1(low), "high_pct": r1(high),
            "n_estimates": len(values), "status": status, "estimates": clean,
            "excluded_estimates": excluded, "flags": flags}


def summarise_access(estimates):
    acc = [e for e in estimates if e["metric"] == "access_pct"]
    if not acc:
        return {"central_pct": None, "status": "no_empirical_data", "estimates": []}
    values = [e["value"] for e in acc]
    return {"central_pct": r1(statistics.median(values)),
            "status": "single_study" if len(values) == 1 else "multi_study",
            "estimates": [{k: e[k] for k in ("value", "study", "year", "scope",
                                              "denominator", "source", "origin")}
                          for e in acc]}


def build_context(country, custom_ctx):
    """Return {key: {value, stress, status, source, caveat}} with custom overrides."""
    out = {}
    # 1. Electricity access
    if "electricity_access_pct" in custom_ctx:
        val = pct(custom_ctx["electricity_access_pct"], "context.electricity_access_pct")
        stress = clamp((100.0 - val) / 100.0, 0.0, 1.0)
        out["electricity"] = {"value": val, "stress": round(stress, 3), "status": "custom_input",
                              "source": "Custom input", "caveat": ""}
    elif country == "KEN" and "electricity_access_pct" in DEFAULT_CONTEXT:
        item = DEFAULT_CONTEXT["electricity_access_pct"]
        val = item["value"]
        stress = clamp((100.0 - val) / 100.0, 0.0, 1.0)
        out["electricity"] = {"value": val, "stress": round(stress, 3), "status": item["status"],
                              "source": item["source"], "caveat": item["caveat"]}
    else:
        out["electricity"] = {"value": None, "stress": NEUTRAL_STRESS, "status": "neutral_fallback",
                              "source": "Fallback default", "caveat": "Missing national indicator."}

    # 2. Hardware / Handset cost
    if "handset_cost_pct_monthly_income" in custom_ctx:
        val = to_float(custom_ctx["handset_cost_pct_monthly_income"], "context.handset_cost_pct_monthly_income")
        stress = clamp(val / 100.0, 0.0, 1.0)
        out["hardware"] = {"value": val, "stress": round(stress, 3), "status": "custom_input",
                           "source": "Custom input", "caveat": ""}
    elif "handset_cost_pct_monthly_income" in DEFAULT_CONTEXT:
        item = DEFAULT_CONTEXT["handset_cost_pct_monthly_income"]
        val = item["value"]
        stress = clamp(val / 100.0, 0.0, 1.0)
        out["hardware"] = {"value": val, "stress": round(stress, 3), "status": item["status"],
                           "source": item["source"], "caveat": item["caveat"]}
    else:
        out["hardware"] = {"value": None, "stress": NEUTRAL_STRESS, "status": "neutral_fallback",
                           "source": "Fallback default", "caveat": "Missing handset cost indicator."}

    # 3. Data / Airtime cost
    if "data_cost_pct_monthly_income" in custom_ctx:
        val = to_float(custom_ctx["data_cost_pct_monthly_income"], "context.data_cost_pct_monthly_income")
        stress = clamp(val / DATA_COST_CEILING_PCT, 0.0, 1.0)
        out["data"] = {"value": val, "stress": round(stress, 3), "status": "custom_input",
                       "source": "Custom input", "caveat": ""}
    elif country == "KEN" and "data_cost_pct_monthly_income" in DEFAULT_CONTEXT:
        item = DEFAULT_CONTEXT["data_cost_pct_monthly_income"]
        val = item["value"]
        stress = clamp(val / DATA_COST_CEILING_PCT, 0.0, 1.0)
        out["data"] = {"value": val, "stress": round(stress, 3), "status": item["status"],
                       "source": item["source"], "caveat": item["caveat"]}
    else:
        out["data"] = {"value": None, "stress": NEUTRAL_STRESS, "status": "neutral_fallback",
                       "source": "Fallback default", "caveat": "Missing data cost indicator."}
    return out


def compute_friction(modality, context, overrides):
    """Compute 1-5 friction index per dimension and composite score."""
    dep = MODALITIES[modality]["dependency"]
    dim_scores = {}
    for dim in DIMENSIONS:
        if (modality, dim) in overrides:
            val = to_float(overrides[(modality, dim)], f"friction_override.{modality}.{dim}")
            dim_scores[dim] = {"score": r1(clamp(val, 1.0, 5.0)), "dependency": dep[dim],
                               "stress": None, "status": "override"}
        else:
            stress = context[dim]["stress"]
            score = 1.0 + 4.0 * dep[dim] * stress
            dim_scores[dim] = {"score": r1(clamp(score, 1.0, 5.0)), "dependency": dep[dim],
                               "stress": stress, "status": "computed"}
    composite = statistics.mean([dim_scores[d]["score"] for d in DIMENSIONS])
    return {"dimensions": dim_scores, "composite_friction": r1(composite),
            "rationale": MODALITIES[modality]["rationale"]}


def compute_policy_discrepancy(reach_dict, budget_dict):
    """Compare share of summed reach against ministerial budget share."""
    valid_mods = [m for m in MODALITY_ORDER if reach_dict[m]["central_pct"] is not None]
    tot_reach = sum(reach_dict[m]["central_pct"] for m in valid_mods) if valid_mods else 0.0

    out = {}
    has_budget = bool(budget_dict)
    if not has_budget:
        for m in MODALITY_ORDER:
            r_share = (r1(100.0 * reach_dict[m]["central_pct"] / tot_reach)
                       if reach_dict[m]["central_pct"] is not None and tot_reach > 0 else None)
            out[m] = {"budget_share_pct": None, "share_of_summed_reach_pct": r_share,
                      "discrepancy_pp": None, "alignment": "no_budget_data"}
        return out, "no_budget_data"

    overlap = [m for m in valid_mods if m in budget_dict]
    if len(overlap) < 2:
        for m in MODALITY_ORDER:
            b_val = pct(budget_dict[m], f"budget.{m}") if m in budget_dict else None
            r_share = (r1(100.0 * reach_dict[m]["central_pct"] / tot_reach)
                       if reach_dict[m]["central_pct"] is not None and tot_reach > 0 else None)
            out[m] = {"budget_share_pct": b_val, "share_of_summed_reach_pct": r_share,
                      "discrepancy_pp": None, "alignment": "insufficient_overlap"}
        return out, "insufficient_overlap"

    tot_overlap_reach = sum(reach_dict[m]["central_pct"] for m in overlap)
    tot_overlap_budget = sum(to_float(budget_dict[m], f"budget.{m}") for m in overlap)

    for m in MODALITY_ORDER:
        b_raw = budget_dict.get(m)
        r_val = reach_dict[m]["central_pct"]
        if m in overlap and tot_overlap_reach > 0 and tot_overlap_budget > 0:
            b_norm = 100.0 * to_float(b_raw, f"budget.{m}") / tot_overlap_budget
            r_norm = 100.0 * r_val / tot_overlap_reach
            diff = b_norm - r_norm
            if abs(diff) <= POLICY_ALIGNED_BAND_PP:
                align = "aligned"
            elif diff > POLICY_ALIGNED_BAND_PP:
                align = "overinvested_relative_to_reach"
            else:
                align = "underinvested_relative_to_reach"
            out[m] = {"budget_share_pct": r1(b_norm), "share_of_summed_reach_pct": r1(r_norm),
                      "discrepancy_pp": r1(diff), "alignment": align}
        else:
            b_val = r1(to_float(b_raw, f"budget.{m}")) if b_raw is not None else None
            out[m] = {"budget_share_pct": b_val, "share_of_summed_reach_pct": None,
                      "discrepancy_pp": None, "alignment": "not_comparable"}
    return out, "comparative_analysis_complete"


# --------------------------------------------------------------------------
# Main compilation
# --------------------------------------------------------------------------
def compile_data(country, custom_path=None):
    custom = load_custom(custom_path, country)
    estimates, overridden_pairs, dropped_base = build_estimates(country, custom)
    context = build_context(country, custom["context"])

    modalities_output = {}
    reach_summary = {}

    for mod in MODALITY_ORDER:
        mod_ests = [e for e in estimates if e["modality"] == mod]
        reach_info = summarise_reach(mod_ests)
        access_info = summarise_access(mod_ests)
        friction_info = compute_friction(mod, context, custom["friction"])
        reach_summary[mod] = reach_info

        modalities_output[mod] = {
            "label": MODALITIES[mod]["label"],
            "examples": MODALITIES[mod]["examples"],
            "reach": reach_info,
            "access": access_info,
            "friction": friction_info,
        }

    policy_summary, policy_status = compute_policy_discrepancy(reach_summary, custom["budget"])
    for mod in MODALITY_ORDER:
        modalities_output[mod]["policy_alignment"] = policy_summary[mod]

    any_platform_ests = [e for e in estimates if e["metric"] == "any_pct"]
    any_platform = {
        "reach_pct": statistics.median([e["value"] for e in any_platform_ests]) if any_platform_ests else None,
        "n_estimates": len(any_platform_ests),
        "estimates": any_platform_ests,
    }

    return {
        "metadata": {
            "country_iso3": country,
            "compilation_timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "script_version": SCRIPT_VERSION,
            "schema_version": SCHEMA_VERSION,
            "custom_input_file": str(custom_path) if custom_path else None,
            "replaced_baseline_estimates": overridden_pairs,
            "policy_discrepancy_status": policy_status,
        },
        "context_indicators": context,
        "any_platform_summary": any_platform,
        "modalities": modalities_output,
    }


def build_parser():
    p = argparse.ArgumentParser(description="Compile EdTech modality reach and friction indices.")
    p.add_argument("--country", default="KEN", help="ISO3 country code (default: KEN)")
    p.add_argument("--output", type=Path, help="Output JSON path (default: modality_reach_<ISO3>.json)")
    p.add_argument("--custom-input", type=Path, help="Path to custom survey JSON or CSV")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    country = args.country.strip().upper()
    out_path = args.output or Path(f"modality_reach_{country}.json")
    try:
        data = compile_data(country, args.custom_input)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote {out_path} for {country}")
        return 0
    except InputError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
