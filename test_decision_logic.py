"""
test_decision_logic.py
===============================================================================
Unit Test Suite for Decision Observatory Interactive Tools (Component B)
-------------------------------------------------------------------------------
Tests the deterministic business logic and arithmetic powering:
1. Dual-Stakeholder Gatekeeping Screener (Teacher Feasibility + SMC Governance)
   - Green Light / Amber Light / Red Light thresholds
   - Statutory Red-Flag Veto triggers (Airtime tax, Grid failure, TCO deficit,
     Malabo child privacy breach, Unaccredited curriculum)
2. Classroom Rotation Planner (TaRL 3-Station Model)
   - Synchronous 3-cohort balancing
   - Usable timetable rotation block calculations
   - Digital device capacity and deficit calculations (solo vs paired)
   - High-density edge cases (e.g., 80:1 pupil-to-device ratio, non-divisible N)
===============================================================================
"""

import math
import pytest


# =============================================================================
# Pure Python Re-implementation of Decision Logic from index.html
# =============================================================================

def calculate_readiness_audit(scores: dict[str, int]) -> dict:
    """
    Replicates calculateAudit() from index.html (lines 3480-3750).
    Scale: -37 (worst) to +32 (best) -> 69 pt range.
    """
    q1 = scores.get("q1", 0)  # Curriculum Accreditation
    q2 = scores.get("q2", 0)  # Energy & Power
    q3 = scores.get("q3", 0)  # Data & Connectivity
    q4 = scores.get("q4", 0)  # Classroom Density
    q5 = scores.get("q5", 0)  # Linguistic & Cultural Fit
    q6 = scores.get("q6", 0)  # Administrative Double Entry
    q7 = scores.get("q7", 0)  # Pedagogical Purpose

    q8 = scores.get("q8", 0)   # 40/60 Lifecycle Maintenance
    q9 = scores.get("q9", 0)   # Child Data Safeguarding
    q10 = scores.get("q10", 0) # Custody & Storage
    q11 = scores.get("q11", 0) # Teacher Dignity & Autonomy

    stream_a = q1 + q2 + q3 + q4 + q5 + q6 + q7
    stream_b = q8 + q9 + q10 + q11
    total_score = stream_a + stream_b

    # Critical Red Flag Gatekeepers
    rejection_triggers = []
    if q3 == -5:
        rejection_triggers.append("Informal Salary Tax Breach")
    if q2 == -3:
        rejection_triggers.append("Daily Grid Failure Vulnerability")
    if q8 == -5:
        rejection_triggers.append("40/60 Lifecycle Deficit (Pilot Graveyard Trigger)")
    if q9 == -4:
        rejection_triggers.append("Minor Exploitation & Malabo Convention Breach")
    if q1 == -3:
        rejection_triggers.append("Unaccredited Curriculum Penalty")

    has_fatal_breach = len(rejection_triggers) > 0

    if not has_fatal_breach and total_score >= 16:
        verdict = "GREEN_LIGHT"
        resolution = "RATIFIED"
    elif not has_fatal_breach and total_score >= 5:
        verdict = "AMBER_LIGHT"
        resolution = "CONDITIONAL"
    else:
        verdict = "RED_LIGHT"
        resolution = "VETO" if has_fatal_breach else "HIGH_RISK"

    return {
        "stream_a": stream_a,
        "stream_b": stream_b,
        "total_score": total_score,
        "has_fatal_breach": has_fatal_breach,
        "rejection_triggers": rejection_triggers,
        "verdict": verdict,
        "resolution": resolution,
    }


def js_round(x: float) -> int:
    """Emulates JavaScript Math.round() behavior (rounds half up towards +infinity)."""
    return math.floor(x + 0.5)


def calculate_rotation_plan(students: int, devices: int, minutes: int, pairing_mode: int = 2) -> dict:
    """
    Replicates updateRotationPlanner() from index.html (lines 3832-3930).
    """
    if students <= 0 or devices <= 0 or minutes <= 0:
        raise ValueError("Inputs must be strictly positive integers.")

    # 1. 3-Cohort Balancing (matching index.html JS logic exactly)
    cohort_a = math.ceil(students / 3)
    cohort_b = js_round((students - cohort_a) / 2)
    cohort_c = students - cohort_a - cohort_b
    assert cohort_a + cohort_b + cohort_c == students, "Cohorts must sum exactly to total students"

    max_cohort = max(cohort_a, cohort_b, cohort_c)

    # 2. Digital Capacity
    digital_seats = devices * pairing_mode
    is_fully_covered = digital_seats >= max_cohort
    deficit = max(0, max_cohort - digital_seats)
    ratio = round(students / devices, 1)

    # 3. Timetable Timing (5m Priming + 3 equal rotations + 5m Synthesis)
    usable_time = minutes - 10
    time_per_rotation = max(6, math.floor(usable_time / 3))
    total_rotations_time = time_per_rotation * 3
    synthesis_slack = usable_time - total_rotations_time

    return {
        "cohort_a": cohort_a,
        "cohort_b": cohort_b,
        "cohort_c": cohort_c,
        "max_cohort": max_cohort,
        "digital_seats": digital_seats,
        "is_fully_covered": is_fully_covered,
        "deficit": deficit,
        "pupil_to_device_ratio": ratio,
        "usable_time": usable_time,
        "time_per_rotation": time_per_rotation,
        "synthesis_slack": synthesis_slack,
    }


# =============================================================================
# Test Suite: Gatekeeping Screener & Statutory Veto Logic
# =============================================================================

class TestReadinessGatekeepingLogic:

    def test_ideal_solution_dual_certified_green_light(self):
        """A compliant solution with all checkpoints passing receives Green Light / Ratified."""
        scores = {
            "q1": 3, "q2": 3, "q3": 3, "q4": 3, "q5": 3, "q6": 2, "q7": 3,  # Stream A = 20
            "q8": 3, "q9": 3, "q10": 3, "q11": 3                             # Stream B = 12 -> Total = 32
        }
        res = calculate_readiness_audit(scores)
        assert res["total_score"] == 32
        assert not res["has_fatal_breach"]
        assert res["verdict"] == "GREEN_LIGHT"
        assert res["resolution"] == "RATIFIED"

    def test_amber_light_conditional_adoption(self):
        """A solution with minor frictions (total score between 5 and 15, no veto) is Amber."""
        scores = {
            "q1": 1, "q2": 1, "q3": 2, "q4": 1, "q5": 1, "q6": 1, "q7": 1,  # Stream A = 8
            "q8": 1, "q9": 1, "q10": 1, "q11": 1                             # Stream B = 4 -> Total = 12
        }
        res = calculate_readiness_audit(scores)
        assert res["total_score"] == 12
        assert not res["has_fatal_breach"]
        assert res["verdict"] == "AMBER_LIGHT"
        assert res["resolution"] == "CONDITIONAL"

    def test_red_light_high_risk_without_veto(self):
        """A solution with low cumulative score (<5) but no single fatal breach is Red Light (High Risk)."""
        scores = {
            "q1": 1, "q2": 1, "q3": 2, "q4": -3, "q5": 1, "q6": -2, "q7": 1, # Stream A = 1
            "q8": 1, "q9": 1, "q10": 1, "q11": -3                             # Stream B = 0 -> Total = 1
        }
        res = calculate_readiness_audit(scores)
        assert res["total_score"] == 1
        assert not res["has_fatal_breach"]
        assert res["verdict"] == "RED_LIGHT"
        assert res["resolution"] == "HIGH_RISK"

    @pytest.mark.parametrize("veto_key,veto_val,expected_clause", [
        ("q3", -5, "Informal Salary Tax Breach"),
        ("q2", -3, "Daily Grid Failure Vulnerability"),
        ("q8", -5, "40/60 Lifecycle Deficit (Pilot Graveyard Trigger)"),
        ("q9", -4, "Minor Exploitation & Malabo Convention Breach"),
        ("q1", -3, "Unaccredited Curriculum Penalty"),
    ])
    def test_statutory_veto_overrides_high_aggregate_score(self, veto_key, veto_val, expected_clause):
        """Even if all other items are perfect (+3), a single fatal breach triggers statutory Veto."""
        scores = {
            "q1": 3, "q2": 3, "q3": 3, "q4": 3, "q5": 3, "q6": 2, "q7": 3,
            "q8": 3, "q9": 3, "q10": 3, "q11": 3
        }
        scores[veto_key] = veto_val  # Inject statutory breach
        res = calculate_readiness_audit(scores)
        assert res["has_fatal_breach"] is True
        assert expected_clause in res["rejection_triggers"]
        assert res["verdict"] == "RED_LIGHT"
        assert res["resolution"] == "VETO"

    def test_multiple_simultaneous_vetoes(self):
        """Tests that multiple simultaneous statutory violations are all recorded."""
        scores = {
            "q1": -3,  # Unaccredited
            "q2": -3,  # No power
            "q3": -5,  # Airtime tax
            "q8": -5,  # Zero TCO
            "q9": -4,  # Data tracking
        }
        res = calculate_readiness_audit(scores)
        assert len(res["rejection_triggers"]) == 5
        assert res["verdict"] == "RED_LIGHT"
        assert res["resolution"] == "VETO"


# =============================================================================
# Test Suite: TaRL Rotation Scheduler Arithmetic
# =============================================================================

class TestRotationPlannerArithmetic:

    def test_standard_cohort_balancing_even_division(self):
        """Tests a 45-pupil cohort dividing cleanly into 15, 15, 15."""
        plan = calculate_rotation_plan(students=45, devices=15, minutes=45, pairing_mode=2)
        assert plan["cohort_a"] == 15
        assert plan["cohort_b"] == 15
        assert plan["cohort_c"] == 15
        assert plan["max_cohort"] == 15
        assert plan["digital_seats"] == 30  # 15 devices * 2 students/pair
        assert plan["is_fully_covered"] is True
        assert plan["deficit"] == 0

    def test_standard_cohort_balancing_uneven_division(self):
        """Tests a 50-pupil cohort dividing into 17, 17, 16."""
        plan = calculate_rotation_plan(students=50, devices=5, minutes=45, pairing_mode=2)
        assert plan["cohort_a"] == 17
        assert plan["cohort_b"] == 17
        assert plan["cohort_c"] == 16
        assert plan["max_cohort"] == 17
        assert plan["digital_seats"] == 10  # 5 devices * 2
        assert plan["is_fully_covered"] is False
        assert plan["deficit"] == 7  # 17 max cohort - 10 seats = 7 peer scribes

    def test_rotation_timing_guide(self):
        """
        45 minute lesson: 5m priming + 3 rotations * 11m (33m) + 5m synthesis + 2m slack = 45m.
        """
        plan = calculate_rotation_plan(students=50, devices=10, minutes=45)
        assert plan["usable_time"] == 35  # 45 - 10
        assert plan["time_per_rotation"] == 11  # floor(35 / 3) = 11
        assert plan["synthesis_slack"] == 2  # 35 - 33 = 2

    def test_high_density_classroom_crowding_edge_case(self):
        """
        Severe crowding: 80 pupils with only 10 devices in solo mode (ratio 8:1).
        Max cohort = ceil(80/3) = 27 pupils.
        Digital seats = 10 solo. Deficit = 17 scribes.
        """
        plan = calculate_rotation_plan(students=80, devices=10, minutes=60, pairing_mode=1)
        assert plan["cohort_a"] == 27
        assert plan["cohort_b"] == 27
        assert plan["cohort_c"] == 26
        assert plan["max_cohort"] == 27
        assert plan["digital_seats"] == 10
        assert plan["is_fully_covered"] is False
        assert plan["deficit"] == 17
        assert plan["pupil_to_device_ratio"] == 8.0

    def test_paired_mode_solves_small_cohort_deficit(self):
        """With 30 students and 8 devices, solo has a deficit, but paired mode covers 100%."""
        solo = calculate_rotation_plan(students=30, devices=8, minutes=45, pairing_mode=1)
        assert solo["max_cohort"] == 10
        assert solo["digital_seats"] == 8
        assert solo["deficit"] == 2

        paired = calculate_rotation_plan(students=30, devices=8, minutes=45, pairing_mode=2)
        assert paired["digital_seats"] == 16
        assert paired["is_fully_covered"] is True
        assert paired["deficit"] == 0

    def test_invalid_negative_or_zero_inputs_raise_value_error(self):
        """Ensures planner rejects invalid physical inputs."""
        with pytest.raises(ValueError):
            calculate_rotation_plan(students=-10, devices=5, minutes=45)
        with pytest.raises(ValueError):
            calculate_rotation_plan(students=50, devices=0, minutes=45)
        with pytest.raises(ValueError):
            calculate_rotation_plan(students=50, devices=5, minutes=-5)
