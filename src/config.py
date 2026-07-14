"""
config.py — Centralised project-wide constants and path definitions.

All other modules import from here so that changing a path in one place
propagates everywhere automatically.
"""

from pathlib import Path

# ──────────────────────────────────────────────
# Directory layout
# ──────────────────────────────────────────────
BASE_DIR: Path = Path(__file__).resolve().parent.parent   # project root

DATA_DIR: Path = BASE_DIR / "data"
MODEL_DIR: Path = BASE_DIR / "models"
REPORT_DIR: Path = BASE_DIR / "reports"

# ──────────────────────────────────────────────
# File paths
# ──────────────────────────────────────────────
DATA_PATH: Path = DATA_DIR / "cleanData.csv"
MODEL_PATH: Path = MODEL_DIR / "best_model.pkl"
PREPROCESSOR_PATH: Path = MODEL_DIR / "preprocessor.pkl"
HISTORY_FILE: Path = BASE_DIR / "prediction_history.csv"
REPORT_FOLDER: Path = REPORT_DIR            # kept for backward-compat alias

# ──────────────────────────────────────────────
# Feature definitions (must match training exactly)
# ──────────────────────────────────────────────
FEATURE_ORDER = [
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
    "Temp_Diff",
    "Power_Index",
    "Wear_Speed_Ratio",
    "Temperature_Stress",
]

MACHINE_TYPES = ["L", "M", "H"]

# ──────────────────────────────────────────────
# Ensure writable directories exist at import time
# ──────────────────────────────────────────────
REPORT_DIR.mkdir(parents=True, exist_ok=True)