"""
4_Prediction_History.py — View, filter and manage past machine predictions.
"""

import sys
from pathlib import Path

# ── Path bootstrap ────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.config import HISTORY_FILE
from src.history import load_history, clear_history

# ── Page config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prediction History — MHI",
    page_icon="📜",
    layout="wide",
)

st.title("📜 Prediction History")
st.caption("View, search, filter and analyse previous machine health predictions.")

# ── Load history ──────────────────────────────────────────────────────────
df = load_history()

if df.empty:
    st.info(
        "No prediction history found yet.\n\n"
        "Go to **🤖 Predict Machine** and make your first prediction!"
    )
    st.stop()

# ── Ensure expected columns exist (graceful degradation) ──────────────────
required_cols = {
    "Timestamp", "Machine Type", "Prediction",
    "Health Score", "Risk Level", "Failure Probability",
}
missing_cols = required_cols - set(df.columns)
if missing_cols:
    st.error(
        f"History file is missing columns: {missing_cols}.\n\n"
        "The history file may be corrupted. Use the button below to reset it."
    )
    if st.button("🗑️ Reset History File"):
        clear_history()
        st.success("History reset.")
        st.rerun()
    st.stop()

# ── KPI metrics ───────────────────────────────────────────────────────────
total       = len(df)
failures    = int((df["Prediction"] == "Failure").sum())
healthy     = int((df["Prediction"] == "Healthy").sum())
avg_health  = df["Health Score"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Predictions", total)
c2.metric("🔴 Failures",       failures)
c3.metric("🟢 Healthy",        healthy)
c4.metric("❤️ Avg Health",    f"{avg_health:.1f}%")

st.divider()

# ── Sidebar filters ───────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Filters")

    search = st.text_input("Search Machine Type", placeholder="e.g. L, M, H")

    all_risks = sorted(df["Risk Level"].dropna().unique().tolist())
    risk_filter = st.multiselect(
        "Risk Level",
        options=all_risks,
        default=all_risks,
    )

    all_preds = sorted(df["Prediction"].dropna().unique().tolist())
    pred_filter = st.multiselect(
        "Prediction",
        options=all_preds,
        default=all_preds,
    )

# ── Apply filters ─────────────────────────────────────────────────────────
filtered = df.copy()

if search:
    filtered = filtered[
        filtered["Machine Type"].astype(str).str.contains(search, case=False, na=False)
    ]

if risk_filter:
    filtered = filtered[filtered["Risk Level"].isin(risk_filter)]

if pred_filter:
    filtered = filtered[filtered["Prediction"].isin(pred_filter)]

# ── Results table ─────────────────────────────────────────────────────────
st.subheader(f"Prediction Records ({len(filtered)} of {total})")

st.dataframe(filtered, use_container_width=True, hide_index=True)

st.download_button(
    "⬇️ Download Filtered History (CSV)",
    filtered.to_csv(index=False),
    "prediction_history.csv",
    "text/csv",
)

st.divider()

# ── Charts ────────────────────────────────────────────────────────────────
if filtered.empty:
    st.warning("No records match the selected filters.")
else:
    tab1, tab2, tab3 = st.tabs([
        "🥧 Prediction Distribution",
        "❤️ Health Analysis",
        "🚨 Risk Analysis",
    ])

    with tab1:
        counts = filtered["Prediction"].value_counts()
        fig_pie = px.pie(
            values=counts.values,
            names=counts.index,
            title="Prediction Distribution",
            color=counts.index,
            color_discrete_map={"Healthy": "#2ecc71", "Failure": "#e74c3c"},
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        col_a, col_b = st.columns(2)

        with col_a:
            fig_hist = px.histogram(
                filtered,
                x="Health Score",
                nbins=20,
                title="Health Score Distribution",
                color_discrete_sequence=["#3498db"],
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with col_b:
            fig_box = px.box(
                filtered,
                y="Health Score",
                color="Prediction",
                title="Health Score by Prediction",
                color_discrete_map={"Healthy": "#2ecc71", "Failure": "#e74c3c"},
            )
            st.plotly_chart(fig_box, use_container_width=True)

    with tab3:
        risk_counts = filtered["Risk Level"].value_counts()

        color_map = {
            "Critical 🔴": "#e74c3c",
            "High 🟠":     "#e67e22",
            "Medium 🟡":   "#f39c12",
            "Low 🟢":      "#2ecc71",
        }

        fig_risk = px.bar(
            x=risk_counts.index,
            y=risk_counts.values,
            labels={"x": "Risk Level", "y": "Count"},
            title="Risk Level Distribution",
            color=risk_counts.index,
            color_discrete_map=color_map,
            text_auto=True,
        )
        st.plotly_chart(fig_risk, use_container_width=True)

st.divider()

# ── Recent predictions ─────────────────────────────────────────────────────
st.subheader("🕐 Most Recent Predictions (top 10)")

if "Timestamp" in filtered.columns:
    recent = filtered.sort_values("Timestamp", ascending=False).head(10)
else:
    recent = filtered.head(10)

st.dataframe(recent, use_container_width=True, hide_index=True)

st.divider()

# ── History management ─────────────────────────────────────────────────────
st.subheader("⚙️ History Management")

with st.expander("⚠️ Danger Zone — Clear History"):
    st.warning("This action will permanently delete all prediction records.")
    confirm = st.checkbox("I understand — delete all history")

    if st.button("🗑️ Clear All History", disabled=not confirm, type="secondary"):
        try:
            clear_history()
            st.success("✅ Prediction history cleared successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to clear history: {e}")
