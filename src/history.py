"""
history.py — Prediction history persistence layer.

Reads and writes the prediction_history.csv file that stores every
prediction made through the MHI application.
"""

import pandas as pd
from datetime import datetime
from pathlib import Path

from src.config import HISTORY_FILE

# Expected CSV columns (defines schema on first write)
_COLUMNS = [
    "Timestamp",
    "Machine Type",
    "Air Temperature",
    "Process Temperature",
    "RPM",
    "Torque",
    "Tool Wear",
    "Prediction",
    "Failure Probability",
    "Health Score",
    "Risk Level",
]


def save_prediction(
    input_data: dict,
    prediction: int,
    probability: float,
    report: dict,
) -> None:
    """
    Append one prediction record to the history CSV.

    Parameters
    ----------
    input_data  : dict  Feature dictionary produced by create_features().
    prediction  : int   0 = Healthy, 1 = Failure.
    probability : float Failure probability in [0, 1].
    report      : dict  Output of generate_machine_report().
    """
    record = {
        "Timestamp":            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Machine Type":         input_data.get("Type", ""),
        "Air Temperature":      input_data.get("Air temperature [K]", ""),
        "Process Temperature":  input_data.get("Process temperature [K]", ""),
        "RPM":                  input_data.get("Rotational speed [rpm]", ""),
        "Torque":               input_data.get("Torque [Nm]", ""),
        "Tool Wear":            input_data.get("Tool wear [min]", ""),
        "Prediction":           "Failure" if prediction == 1 else "Healthy",
        "Failure Probability":  round(probability * 100, 2),
        "Health Score":         report.get("Health Score", ""),
        "Risk Level":           report.get("Risk Level", ""),
    }

    df_new = pd.DataFrame([record], columns=_COLUMNS)

    history_path = Path(HISTORY_FILE)

    if history_path.exists():
        df_new.to_csv(history_path, mode="a", index=False, header=False)
    else:
        df_new.to_csv(history_path, index=False)


def load_history() -> pd.DataFrame:
    """
    Load prediction history from CSV.

    Returns
    -------
    pd.DataFrame  May be empty if no history exists yet.
    """
    history_path = Path(HISTORY_FILE)

    if not history_path.exists():
        return pd.DataFrame(columns=_COLUMNS)

    try:
        df = pd.read_csv(history_path)
        if df.empty:
            return pd.DataFrame(columns=_COLUMNS)
        return df
    except Exception:
        return pd.DataFrame(columns=_COLUMNS)


def clear_history() -> None:
    """Overwrite the history CSV with an empty (header-only) file."""
    pd.DataFrame(columns=_COLUMNS).to_csv(Path(HISTORY_FILE), index=False)