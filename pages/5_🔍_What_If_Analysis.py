"""
5_What_If_Analysis.py — Side-by-side scenario comparison for two machine setups.

Allows engineers to modify machine parameters and instantly see the impact
on failure probability, health score and maintenance recommendations.
"""

import sys
from pathlib import Path

# ── Path bootstrap ────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from src.feature_engg import create_features
from src.predict import predict_machine
from src.report import generate_machine_report
from utils import status_box

# ── Page config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="What-If Analysis — MHI",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 What-If Analysis")
st.caption(
    "Adjust machine parameters for two scenarios and compare failure risk side-by-side."
)

# ─────────────────────────────────────────────────────────────────────────────
# Scenario inputs in two main-area columns (not sidebar — sidebar is crowded)
# ─────────────────────────────────────────────────────────────────────────────
col_a_in, col_b_in = st.columns(2, gap="large")

with col_a_in:
    st.subheader("🅰️ Scenario A — Current Machine")
    type_a   = st.selectbox("Machine Type",          ["L", "M", "H"], key="a_type")
    air_a    = st.slider("Air Temperature (K)",       290.0, 320.0, 300.0, 0.1, key="a_air")
    proc_a   = st.slider("Process Temperature (K)",   300.0, 330.0, 310.0, 0.1, key="a_proc")
    rpm_a    = st.slider("Rotational Speed (RPM)",    1000,  3000,   1500,  10,  key="a_rpm")
    torque_a = st.slider("Torque (Nm)",               0.0,   100.0,  40.0,  0.5, key="a_torque")
    wear_a   = st.slider("Tool Wear (min)",            0,     300,    100,   1,   key="a_wear")

with col_b_in:
    st.subheader("🅱️ Scenario B — Modified Machine")
    type_b   = st.selectbox("Machine Type",          ["L", "M", "H"], key="b_type")
    air_b    = st.slider("Air Temperature (K)",       290.0, 320.0, 301.0, 0.1, key="b_air")
    proc_b   = st.slider("Process Temperature (K)",   300.0, 330.0, 312.0, 0.1, key="b_proc")
    rpm_b    = st.slider("Rotational Speed (RPM)",    1000,  3000,   1600,  10,  key="b_rpm")
    torque_b = st.slider("Torque (Nm)",               0.0,   100.0,  45.0,  0.5, key="b_torque")
    wear_b   = st.slider("Tool Wear (min)",            0,     300,    120,   1,   key="b_wear")

st.divider()

run_btn = st.button("🚀 Run What-If Analysis", use_container_width=True, type="primary")

if not run_btn:
    st.info("Set parameters for both scenarios above and click **🚀 Run What-If Analysis**.")
    st.stop()

# ── Validation ────────────────────────────────────────────────────────────
errors = []
if proc_a < air_a:
    errors.append("Scenario A: Process temperature must be ≥ air temperature.")
if proc_b < air_b:
    errors.append("Scenario B: Process temperature must be ≥ air temperature.")

if errors:
    for err in errors:
        st.error(f"⚠️ {err}")
    st.stop()

# ── Feature engineering & prediction ─────────────────────────────────────
with st.spinner("Running analysis…"):
    try:
        input_a = create_features(type_a, air_a, proc_a, rpm_a, torque_a, wear_a)
        input_b = create_features(type_b, air_b, proc_b, rpm_b, torque_b, wear_b)

        pred_a, prob_a = predict_machine(input_a)
        pred_b, prob_b = predict_machine(input_b)

        rep_a = generate_machine_report(prob_a, input_a)
        rep_b = generate_machine_report(prob_b, input_b)

    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        st.error(f"🚨 Analysis failed: {exc}")
        st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("📊 Scenario Comparison")

res_a, res_b = st.columns(2, gap="large")

with res_a:
    st.markdown("### 🅰️ Scenario A")
    if pred_a == 1:
        st.error("🔴 Failure Predicted")
    else:
        st.success("🟢 Healthy")
    st.metric("Failure Probability", f"{prob_a * 100:.2f}%")
    st.metric("Health Score",        f"{rep_a['Health Score']}%")
    status_box(rep_a["Risk Level"])
    st.metric("Downtime",     rep_a["Downtime"])
    st.metric("Est. Cost",    rep_a["Estimated Cost"])

with res_b:
    st.markdown("### 🅱️ Scenario B")
    prob_delta = (prob_b - prob_a) * 100          # positive = worse
    health_delta = rep_b["Health Score"] - rep_a["Health Score"]

    if pred_b == 1:
        st.error("🔴 Failure Predicted")
    else:
        st.success("🟢 Healthy")
    st.metric(
        "Failure Probability",
        f"{prob_b * 100:.2f}%",
        delta=f"{prob_delta:+.2f}%",
        delta_color="inverse",          # red if positive (higher risk)
    )
    st.metric(
        "Health Score",
        f"{rep_b['Health Score']}%",
        delta=f"{health_delta:+.2f}%",
    )
    status_box(rep_b["Risk Level"])
    st.metric("Downtime",     rep_b["Downtime"])
    st.metric("Est. Cost",    rep_b["Estimated Cost"])

st.divider()

# ── Change summary banner ─────────────────────────────────────────────────
delta = (prob_b - prob_a) * 100
if delta > 0:
    st.error(
        f"⚠️ Failure probability **increased by {delta:.2f}%** in Scenario B. "
        "Consider reviewing the modified parameters."
    )
elif delta < 0:
    st.success(
        f"✅ Failure probability **decreased by {abs(delta):.2f}%** in Scenario B. "
        "The modifications improve machine health."
    )
else:
    st.info("ℹ️ No change in failure probability between scenarios.")

st.divider()

# ── Comparison charts ─────────────────────────────────────────────────────
st.subheader("📈 Visual Comparison")

chart_a, chart_b = st.columns(2)

with chart_a:
    fig_prob = go.Figure(go.Bar(
        x=["Scenario A", "Scenario B"],
        y=[prob_a * 100, prob_b * 100],
        text=[f"{prob_a * 100:.1f}%", f"{prob_b * 100:.1f}%"],
        textposition="outside",
        marker_color=["#3498db", "#e74c3c" if prob_b > prob_a else "#2ecc71"],
    ))
    fig_prob.update_layout(
        title="Failure Probability (%)",
        yaxis=dict(range=[0, 105]),
        height=350,
    )
    st.plotly_chart(fig_prob, use_container_width=True)

with chart_b:
    fig_health = go.Figure(go.Bar(
        x=["Scenario A", "Scenario B"],
        y=[rep_a["Health Score"], rep_b["Health Score"]],
        text=[rep_a["Health Score"], rep_b["Health Score"]],
        textposition="outside",
        marker_color=["#3498db", "#2ecc71" if rep_b["Health Score"] >= rep_a["Health Score"] else "#e74c3c"],
    ))
    fig_health.update_layout(
        title="Machine Health Score (%)",
        yaxis=dict(range=[0, 105]),
        height=350,
    )
    st.plotly_chart(fig_health, use_container_width=True)

st.divider()

# ── Parameter comparison table ────────────────────────────────────────────
st.subheader("📋 Parameter Comparison")

compare_df = pd.DataFrame({
    "Parameter": [
        "Machine Type",
        "Air Temperature (K)",
        "Process Temperature (K)",
        "Rotational Speed (RPM)",
        "Torque (Nm)",
        "Tool Wear (min)",
    ],
    "Scenario A": [type_a, air_a, proc_a, rpm_a, torque_a, wear_a],
    "Scenario B": [type_b, air_b, proc_b, rpm_b, torque_b, wear_b],
})
compare_df["Changed"] = compare_df.apply(
    lambda r: "✏️ Yes" if str(r["Scenario A"]) != str(r["Scenario B"]) else "—",
    axis=1,
)
st.dataframe(compare_df, use_container_width=True, hide_index=True)

st.divider()

# ── Recommendations ───────────────────────────────────────────────────────
st.subheader("🛠️ Maintenance Recommendations")

rec_a_col, rec_b_col = st.columns(2, gap="large")

with rec_a_col:
    st.markdown("**Scenario A**")
    for rec in rep_a["Recommendations"]:
        st.success(rec)

    st.markdown("**Failure Causes**")
    for cause in rep_a["Failure Causes"]:
        st.warning(f"• {cause}")

with rec_b_col:
    st.markdown("**Scenario B**")
    for rec in rep_b["Recommendations"]:
        st.success(rec)

    st.markdown("**Failure Causes**")
    for cause in rep_b["Failure Causes"]:
        st.warning(f"• {cause}")
