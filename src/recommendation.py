"""
recommendation.py — Risk classification and maintenance recommendation engine.

All functions are pure (no side-effects) and operate on plain Python types
so they can be used by any page or by the PDF generator without issue.

Note: emoji characters are intentionally kept in risk-level strings because
the PDF generator strips them before writing (see pdf_generator.py).
"""

# ─────────────────────────────────────────────────────────────────────────────
# Thresholds (single source of truth)
# ─────────────────────────────────────────────────────────────────────────────
CRITICAL_THRESHOLD = 0.80
HIGH_THRESHOLD     = 0.60
MEDIUM_THRESHOLD   = 0.40

# Operating-condition alarm limits (from domain knowledge / dataset analysis)
AIR_TEMP_LIMIT      = 305.0   # K
PROCESS_TEMP_LIMIT  = 315.0   # K
TORQUE_LIMIT        = 60.0    # Nm
TOOL_WEAR_LIMIT     = 180     # min
LOW_RPM_LIMIT       = 1300    # rpm


def get_risk_level(probability: float) -> str:
    """Return a human-readable risk level string for a failure probability."""
    if probability >= CRITICAL_THRESHOLD:
        return "Critical 🔴"
    if probability >= HIGH_THRESHOLD:
        return "High 🟠"
    if probability >= MEDIUM_THRESHOLD:
        return "Medium 🟡"
    return "Low 🟢"


def calculate_health_score(probability: float) -> float:
    """Return machine health score in [0, 100] (higher = healthier)."""
    return round((1.0 - probability) * 100, 2)


def estimated_downtime(probability: float) -> str:
    """Estimate potential downtime based on failure probability."""
    if probability >= CRITICAL_THRESHOLD:
        return "6–8 Hours"
    if probability >= HIGH_THRESHOLD:
        return "3–5 Hours"
    if probability >= MEDIUM_THRESHOLD:
        return "1–2 Hours"
    return "No Downtime Expected"


def estimated_cost(probability: float) -> str:
    """Estimate maintenance cost based on failure probability."""
    if probability >= CRITICAL_THRESHOLD:
        return "₹30,000+"
    if probability >= HIGH_THRESHOLD:
        return "₹15,000"
    if probability >= MEDIUM_THRESHOLD:
        return "₹7,000"
    return "₹2,000"


def detect_failure_causes(data: dict) -> list[str]:
    """
    Identify likely failure causes from machine operating parameters.

    Parameters
    ----------
    data : dict  Feature dictionary (keys match training column names).

    Returns
    -------
    list[str]  List of detected anomalies; never empty.
    """
    causes = []

    if data.get("Air temperature [K]", 0) > AIR_TEMP_LIMIT:
        causes.append("High Air Temperature")

    if data.get("Process temperature [K]", 0) > PROCESS_TEMP_LIMIT:
        causes.append("High Process Temperature")

    if data.get("Torque [Nm]", 0) > TORQUE_LIMIT:
        causes.append("High Torque")

    if data.get("Tool wear [min]", 0) > TOOL_WEAR_LIMIT:
        causes.append("Excessive Tool Wear")

    if 0 < data.get("Rotational speed [rpm]", 1) < LOW_RPM_LIMIT:
        causes.append("Low Rotational Speed")

    if not causes:
        causes.append("No critical operating condition detected")

    return causes


def maintenance_actions(probability: float, data: dict) -> list[str]:
    """
    Generate a prioritised maintenance action list.

    Parameters
    ----------
    probability : float  Failure probability in [0, 1].
    data        : dict   Feature dictionary (used for context-aware actions).

    Returns
    -------
    list[str]  Ordered list of recommended actions.
    """
    actions: list[str] = []

    if probability >= CRITICAL_THRESHOLD:
        actions = [
            "Stop machine immediately.",
            "Perform complete mechanical inspection.",
            "Replace worn cutting tool.",
            "Check and service the cooling system.",
            "Inspect spindle bearings.",
            "Reduce operating load before restart.",
        ]

    elif probability >= HIGH_THRESHOLD:
        actions = [
            "Schedule maintenance within 24 hours.",
            "Inspect spindle bearings.",
            "Check lubrication levels.",
            "Monitor temperature continuously.",
        ]

    elif probability >= MEDIUM_THRESHOLD:
        actions = [
            "Inspect machine this week.",
            "Monitor vibration and torque trends.",
            "Perform scheduled preventive maintenance.",
        ]

    else:
        actions = ["Machine operating normally. Continue regular monitoring."]

    return actions