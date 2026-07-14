"""
feature_engg.py — Feature engineering for the MHI prediction pipeline.

The function `create_features` produces exactly the 10-column dictionary
that the trained model's ColumnTransformer expects, in the correct order.
"""

from src.config import FEATURE_ORDER


def create_features(
    machine_type: str,
    air_temp: float,
    process_temp: float,
    rpm: int,
    torque: float,
    tool_wear: int,
) -> dict:
    """
    Build the engineered feature dictionary for a single prediction.

    Parameters
    ----------
    machine_type : str     One of 'L', 'M', 'H'
    air_temp     : float   Air temperature in Kelvin
    process_temp : float   Process temperature in Kelvin
    rpm          : int     Rotational speed in RPM  (must be > 0)
    torque       : float   Torque in Nm
    tool_wear    : int     Accumulated tool wear in minutes

    Returns
    -------
    dict  Ordered feature dictionary matching FEATURE_ORDER.

    Raises
    ------
    ValueError   If rpm == 0 (would produce division-by-zero).
    """
    # ── Input validation ──────────────────────────────────────────────────
    if rpm == 0:
        raise ValueError("Rotational speed (RPM) cannot be zero.")
    if machine_type not in ("L", "M", "H"):
        raise ValueError(f"Invalid machine type '{machine_type}'. Must be L, M, or H.")
    if process_temp < air_temp:
        raise ValueError("Process temperature must be ≥ air temperature.")

    # ── Engineered features ───────────────────────────────────────────────
    temp_diff           = process_temp - air_temp
    power_index         = torque * rpm
    wear_speed_ratio    = tool_wear / rpm
    temperature_stress  = temp_diff * torque

    features = {
        "Type":                     machine_type,
        "Air temperature [K]":      air_temp,
        "Process temperature [K]":  process_temp,
        "Rotational speed [rpm]":   rpm,
        "Torque [Nm]":              torque,
        "Tool wear [min]":          tool_wear,
        "Temp_Diff":                temp_diff,
        "Power_Index":              power_index,
        "Wear_Speed_Ratio":         wear_speed_ratio,
        "Temperature_Stress":       temperature_stress,
    }

    # Guarantee key order matches training order
    return {k: features[k] for k in FEATURE_ORDER}