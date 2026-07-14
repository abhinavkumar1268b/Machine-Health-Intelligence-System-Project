"""
home.py — MHI Home Dashboard (Streamlit entry point).

Run with:
    streamlit run home.py
"""

import sys
from pathlib import Path

# ── Ensure project root is on sys.path before any src.* imports ───────────
ROOT_DIR = Path(__file__).resolve().parent   # home.py IS at the project root
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from utils import page_header, metric_card  # noqa: E402

# ── Page config — must be first Streamlit call ────────────────────────────
st.set_page_config(
    page_title="Machine Health Intelligence (MHI)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Header ────────────────────────────────────────────────────────────────
page_header(
    "🤖 Machine Health Intelligence (MHI)",
    "AI-Powered Predictive Maintenance Platform",
)

# ── Introduction ──────────────────────────────────────────────────────────
st.markdown(
    """
    ### Welcome 👋

    **Machine Health Intelligence (MHI)** is an end-to-end machine learning
    application that predicts machine failures **before they occur**.

    The platform helps engineers and maintenance teams reduce downtime,
    increase machine availability, and make proactive maintenance decisions.
    """
)

st.divider()

# ── KPI Metrics ───────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
metric_card(c1, "ML Models",      "5")
metric_card(c2, "Input Features", "10")
metric_card(c3, "Prediction",     "Real-Time")
metric_card(c4, "Status",         "✅ Ready")

st.divider()

# ── Feature Highlights ────────────────────────────────────────────────────
st.subheader("🚀 Platform Features")

left, right = st.columns(2)

with left:
    st.success("🤖 Machine Failure Prediction")
    st.success("❤️ Machine Health Score")
    st.success("📊 Failure Probability")
    st.success("🛠️ Maintenance Recommendations")

with right:
    st.success("📜 Prediction History")
    st.success("🔍 What-If Scenario Analysis")
    st.success("📄 PDF Health Report")
    st.success("📈 Model Explainability")

st.divider()

# ── Workflow ──────────────────────────────────────────────────────────────
st.subheader("⚙️ Prediction Workflow")

steps = [
    ("1️⃣", "Enter Machine Parameters"),
    ("⬇️", ""),
    ("2️⃣", "AI Model Predicts Failure"),
    ("⬇️", ""),
    ("3️⃣", "Calculate Health Score"),
    ("⬇️", ""),
    ("4️⃣", "Generate Maintenance Recommendation"),
    ("⬇️", ""),
    ("5️⃣", "Download Machine Health Report (PDF)"),
]

for icon, label in steps:
    if label:
        st.markdown(f"{icon} &nbsp; **{label}**", unsafe_allow_html=True)
    else:
        st.markdown(icon)

st.divider()

# ── Quick navigation hint ─────────────────────────────────────────────────
st.info("👈 Use the sidebar to navigate between pages.")