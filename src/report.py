"""
report.py — Assembles the full machine health report dictionary.

Imports individual recommendation helpers and combines their outputs
into a single structured report dict consumed by pages and the PDF generator.
"""

from src.recommendation import (
    get_risk_level,
    calculate_health_score,
    estimated_downtime,
    estimated_cost,
    detect_failure_causes,
    maintenance_actions,
)


def generate_machine_report(probability: float, data: dict) -> dict:
    """
    Build a comprehensive machine health report.

    Parameters
    ----------
    probability : float  Model failure probability in [0, 1].
    data        : dict   Feature dictionary (must contain operating parameter keys).

    Returns
    -------
    dict with keys:
        Failure Probability, Risk Level, Health Score, Downtime,
        Estimated Cost, Failure Causes, Recommendations
    """
    return {
        "Failure Probability": round(probability * 100, 2),
        "Risk Level":          get_risk_level(probability),
        "Health Score":        calculate_health_score(probability),
        "Downtime":            estimated_downtime(probability),
        "Estimated Cost":      estimated_cost(probability),
        "Failure Causes":      detect_failure_causes(data),
        "Recommendations":     maintenance_actions(probability, data),
    }
