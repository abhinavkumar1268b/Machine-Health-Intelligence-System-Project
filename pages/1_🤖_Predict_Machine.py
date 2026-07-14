"""
1_Predict_Machine.py — Real-time machine failure prediction page.

Bugs fixed vs original:
• SyntaxError: Plotly figure code was pasted inside an f-string markdown block.
• NameError: create_pdf / download_button ran at module level before prediction.
• Duplicate save_prediction function (now uses src.history.save_prediction).
• st.set_page_config was defined after function definitions (Streamlit requires
  it as the very first Streamlit call).
• No sys.path setup (pages couldn't import src.*).
• Failure causes & recommendations were fetched but never displayed properly.
• Gauge charts now rendered as proper st.plotly_chart() calls.
"""

import sys
from pathlib import Path

# ── Path bootstrap (must be before any src.* import) ─────────────────────
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import io
import streamlit as st
import plotly.graph_objects as go

from src.feature_engg import create_features
from src.predict import predict_machine
from src.report import generate_machine_report
from src.history import save_prediction
from src.pdf_generator import create_pdf
from utils import page_header, status_box

# ── Page config — must be very first Streamlit call ──────────────────────
st.set_page_config(
    page_title="Predict Machine — MHI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

page_header("🤖 Predict Machine Failure", "Enter machine parameters to predict health status.")

# ─────────────────────────────────────────────────────────────────────────────
# Layout: left = input form | right = results
# ─────────────────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")


# ══════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN — Input Form
# ══════════════════════════════════════════════════════════════════════════════
with left_col:
    st.subheader("⚙️ Machine Parameters")

    with st.form("prediction_form"):

        machine_type = st.selectbox(
            "Machine Type",
            ["L", "M", "H"],
            help="L = Light duty, M = Medium duty, H = Heavy duty",
        )

        air_temp = st.number_input(
            "Air Temperature (K)",
            min_value=290.0,
            max_value=320.0,
            value=300.0,
            step=0.1,
            help="Ambient air temperature in Kelvin",
        )

        process_temp = st.number_input(
            "Process Temperature (K)",
            min_value=300.0,
            max_value=330.0,
            value=310.0,
            step=0.1,
            help="Machine process temperature in Kelvin",
        )

        rpm = st.number_input(
            "Rotational Speed (RPM)",
            min_value=1,           # > 0 avoids division-by-zero in feature engineering
            max_value=3000,
            value=1500,
            step=10,
            help="Spindle rotational speed in revolutions per minute",
        )

        torque = st.number_input(
            "Torque (Nm)",
            min_value=0.0,
            max_value=100.0,
            value=40.0,
            step=0.5,
            help="Torque applied to the spindle in Newton-metres",
        )

        tool_wear = st.number_input(
            "Tool Wear (Minutes)",
            min_value=0,
            max_value=300,
            value=100,
            step=1,
            help="Cumulative tool usage in minutes",
        )

        predict_btn = st.form_submit_button(
            "🚀 Predict Machine Health",
            use_container_width=True,
            type="primary",
        )


# ══════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN — Results (only rendered after form submit)
# ══════════════════════════════════════════════════════════════════════════════
with right_col:
    st.subheader("📊 Prediction Result")

    if not predict_btn:
        st.info(
            "Fill in the machine parameters on the left and click "
            "**🚀 Predict Machine Health** to generate a prediction."
        )
        st.stop()

    # ── Input validation ──────────────────────────────────────────────────
    if process_temp < air_temp:
        st.error(
            "⚠️ Process temperature cannot be lower than air temperature. "
            "Please correct your inputs."
        )
        st.stop()

    # ── Feature engineering ───────────────────────────────────────────────
    try:
        input_data = create_features(
            machine_type=machine_type,
            air_temp=air_temp,
            process_temp=process_temp,
            rpm=rpm,
            torque=torque,
            tool_wear=tool_wear,
        )
    except ValueError as ve:
        st.error(f"⚠️ Input error: {ve}")
        st.stop()

    # ── Prediction ────────────────────────────────────────────────────────
    with st.spinner("Running prediction…"):
        try:
            prediction, probability = predict_machine(input_data)
        except (FileNotFoundError, RuntimeError) as model_err:
            st.error(f"🚨 Model error: {model_err}")
            st.stop()

    # ── Report generation ─────────────────────────────────────────────────
    report = generate_machine_report(probability, input_data)

    # ── Save to history ───────────────────────────────────────────────────
    try:
        save_prediction(input_data, prediction, probability, report)
    except Exception as hist_err:
        st.warning(f"History could not be saved: {hist_err}")

    # ════════════════════════════════════════════════════════════════════
    # RESULTS DISPLAY
    # ════════════════════════════════════════════════════════════════════

    # 1. Overall status banner
    if prediction == 1:
        st.error("🔴 **Machine Failure Predicted**")
    else:
        st.success("🟢 **Machine is Healthy**")

    st.divider()

    # 2. Gauge charts — failure probability & health score side by side
    g1, g2 = st.columns(2)

    with g1:
        prob_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(probability * 100, 2),
            number={"suffix": "%"},
            title={"text": "Failure Probability"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar":  {"color": "crimson"},
                "steps": [
                    {"range": [0,  40],  "color": "#d4edda"},
                    {"range": [40, 70],  "color": "#fff3cd"},
                    {"range": [70, 100], "color": "#f8d7da"},
                ],
                "threshold": {
                    "line":  {"color": "darkred", "width": 3},
                    "thickness": 0.75,
                    "value": probability * 100,
                },
            },
        ))
        prob_gauge.update_layout(height=260, margin=dict(t=60, b=20, l=20, r=20))
        st.plotly_chart(prob_gauge, use_container_width=True)

    with g2:
        health_score = report["Health Score"]
        health_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            number={"suffix": "%"},
            title={"text": "Machine Health Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar":  {"color": "seagreen"},
                "steps": [
                    {"range": [0,  40],  "color": "#f8d7da"},
                    {"range": [40, 70],  "color": "#fff3cd"},
                    {"range": [70, 100], "color": "#d4edda"},
                ],
            },
        ))
        health_gauge.update_layout(height=260, margin=dict(t=60, b=20, l=20, r=20))
        st.plotly_chart(health_gauge, use_container_width=True)

    st.divider()

    # 3. Risk Level
    st.write("### 🚨 Risk Level")
    status_box(report["Risk Level"])

    st.divider()

    # 4. Downtime & Cost metrics
    mc1, mc2 = st.columns(2)
    mc1.metric("⏱️ Estimated Downtime",  report["Downtime"])
    mc2.metric("💰 Maintenance Cost",   report["Estimated Cost"])

    st.divider()

    # 5. Failure causes
    st.subheader("⚠️ Possible Failure Causes")
    for cause in report["Failure Causes"]:
        st.warning(f"• {cause}")

    st.divider()

    # 6. Maintenance recommendations
    st.subheader("🛠️ Maintenance Recommendations")
    for i, rec in enumerate(report["Recommendations"], 1):
        st.success(f"{i}. {rec}")

    st.divider()

    # 7. Input summary (collapsible)
    with st.expander("📋 View Input Summary"):
        import pandas as pd
        summary_df = pd.DataFrame(
            list(input_data.items()),
            columns=["Feature", "Value"],
        )
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.divider()

    # 8. PDF download
    with st.spinner("Generating PDF report…"):
        try:
            pdf_path = create_pdf(report, input_data)
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()

            st.download_button(
                label="📥 Download Machine Health Report (PDF)",
                data=pdf_bytes,
                file_name="Machine_Health_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="secondary",
            )
        except Exception as pdf_err:
            st.warning(f"PDF generation failed: {pdf_err}")

    st.success("✅ Prediction completed successfully.")