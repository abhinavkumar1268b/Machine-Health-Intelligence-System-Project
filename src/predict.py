"""
predict.py — Model loading and inference helpers.

The model (a sklearn Pipeline with preprocessor + XGBoost) already
contains the ColumnTransformer, so raw feature dicts can be passed
directly as a one-row DataFrame.
"""

import warnings
import pandas as pd
import joblib

from src.config import MODEL_PATH, FEATURE_ORDER


def load_model():
    """
    Load the trained pipeline from disk.

    Returns
    -------
    sklearn.pipeline.Pipeline

    Raises
    ------
    FileNotFoundError  If the model pickle is missing.
    RuntimeError       If the model cannot be unpickled.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at: {MODEL_PATH}\n"
            "Please ensure 'models/best_model.pkl' exists."
        )
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return joblib.load(MODEL_PATH)
    except Exception as exc:
        raise RuntimeError(f"Failed to load model: {exc}") from exc


def predict_machine(input_data: dict) -> tuple[int, float]:
    """
    Run the model pipeline on a single feature dictionary.

    Parameters
    ----------
    input_data : dict   Feature dict produced by `create_features()`.

    Returns
    -------
    (prediction, probability)
        prediction  : int   1 = Failure, 0 = Healthy
        probability : float Failure probability in [0, 1]
    """
    model = load_model()

    # Build DataFrame with exactly the expected columns in order
    df = pd.DataFrame([input_data])[FEATURE_ORDER]

    prediction  = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])

    return prediction, probability