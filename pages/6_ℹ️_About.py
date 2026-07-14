"""
6_About.py — Project information and technology stack page.
"""

import sys
from pathlib import Path

# ── Path bootstrap ────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="About — MHI",
    page_icon="ℹ️",
    layout="wide",
)

st.title("ℹ️ About Machine Health Intelligence (MHI)")
st.caption("AI-Powered Predictive Maintenance & Machine Health Monitoring Platform")

st.divider()

# ── Introduction ──────────────────────────────────────────────────────────
st.markdown("""
**Machine Health Intelligence (MHI)** is an end-to-end Machine Learning application
designed to help manufacturing industries predict machine failures before they occur.

Instead of waiting for a machine to break down, MHI analyses machine operating
conditions and estimates the **probability of failure**, allowing maintenance teams
to take preventive action and significantly reduce unplanned downtime.
""")

st.divider()

# ── High-level metrics ────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("ML Models", "4")
    st.caption("Logistic Regression, Random Forest, SVM, XGBoost")

with col2:
    st.metric("Input Features", "10")
    st.caption("6 operational + 4 engineered features")

with col3:
    st.metric("Prediction", "Real-Time")
    st.caption("Instant failure probability & health score")

st.divider()

# ── Objectives ────────────────────────────────────────────────────────────
st.subheader("🎯 Project Objectives")

objectives = [
    "Predict machine failures before they occur.",
    "Reduce unexpected production downtime.",
    "Improve maintenance planning and scheduling.",
    "Increase equipment reliability and lifespan.",
    "Support data-driven maintenance decisions.",
]
for obj in objectives:
    st.success(f"✔ {obj}")

st.divider()

# ── How MHI works ─────────────────────────────────────────────────────────
st.subheader("⚙️ How MHI Works")

st.markdown("""
### Step 1 — Enter Machine Parameters
Provide the following operational values:
- Machine Type (L / M / H)
- Air Temperature (K)
- Process Temperature (K)
- Rotational Speed (RPM)
- Torque (Nm)
- Tool Wear (min)

⬇️

### Step 2 — Automatic Feature Engineering
MHI derives four additional predictive features:

| Engineered Feature | Formula |
|--------------------|---------|
| Temperature Difference | Process Temp − Air Temp |
| Power Index | Torque × RPM |
| Wear-Speed Ratio | Tool Wear ÷ RPM |
| Temperature Stress | Temp Diff × Torque |

⬇️

### Step 3 — Machine Learning Prediction
The trained XGBoost pipeline predicts:
- **Healthy** or **Failure**
- Failure probability (0 – 100 %)
- Machine health score (100 – 0 %)

⬇️

### Step 4 — Intelligent Recommendations
Based on prediction results, MHI generates:
- Risk level classification (Low / Medium / High / Critical)
- Root-cause failure analysis
- Prioritised maintenance action list
- Estimated downtime & repair cost

⬇️

### Step 5 — Downloadable PDF Report
A formatted PDF report is generated on demand for offline use.
""")

st.divider()

# ── Key features ──────────────────────────────────────────────────────────
st.subheader("🚀 Key Features")

left, right = st.columns(2)

with left:
    st.info("🤖 Machine Failure Prediction")
    st.info("📊 Dataset Insights & EDA")
    st.info("📈 Model Performance Dashboard")
    st.info("📜 Prediction History")

with right:
    st.info("🔍 What-If Scenario Analysis")
    st.info("❤️ Machine Health Score")
    st.info("🛠️ Maintenance Recommendations")
    st.info("📄 PDF Report Generation")

st.divider()

# ── ML Pipeline ───────────────────────────────────────────────────────────
st.subheader("🧠 Machine Learning Pipeline")

st.code("""
Raw Machine Data
      │
      ▼
Data Cleaning & EDA
      │
      ▼
Feature Engineering (+ 4 derived features)
      │
      ▼
ColumnTransformer  (StandardScaler + OneHotEncoder)
      │
      ▼
Model Training (LR, RF, SVM, XGBoost)
      │
      ▼
Model Evaluation (Accuracy, F1, ROC-AUC)
      │
      ▼
Best Model Serialisation (joblib pickle)
      │
      ▼
Real-Time Prediction → Recommendation → PDF Report
""", language="text")

st.divider()

# ── Technology stack ──────────────────────────────────────────────────────
st.subheader("🛠️ Technology Stack")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.markdown("""
### 🐍 Core
- Python 3.10+
- Pandas
- NumPy
- Joblib
""")

with tech2:
    st.markdown("""
### 🤖 Machine Learning
- Scikit-Learn
- XGBoost
""")

with tech3:
    st.markdown("""
### 📊 Visualisation & UI
- Streamlit
- Plotly
- ReportLab (PDF)
""")

st.divider()

# ── Benefits ──────────────────────────────────────────────────────────────
st.subheader("🌟 Benefits")

c1, c2 = st.columns(2)

with c1:
    st.success("✔ Reduce Machine Downtime")
    st.success("✔ Lower Maintenance Cost")
    st.success("✔ Improve Productivity")

with c2:
    st.success("✔ Increase Equipment Life")
    st.success("✔ Better Maintenance Planning")
    st.success("✔ Real-Time Decision Support")

st.divider()

# ── Future enhancements ───────────────────────────────────────────────────
st.subheader("🔮 Future Enhancements")

future_items = [
    "IoT Sensor Real-Time Integration",
    "Live Machine Monitoring Dashboard",
    "Cloud Deployment (AWS / GCP / Azure)",
    "Email & SMS Failure Alerts",
    "Remaining Useful Life (RUL) Prediction",
    "Deep Learning (LSTM) Models",
    "Multi-Machine Fleet Monitoring",
]
for item in future_items:
    st.write(f"• {item}")

st.divider()

# ── Footer ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center; color:#888; padding:12px 0;">
        <h4>🤖 Machine Health Intelligence (MHI)</h4>
        <p>AI-Powered Predictive Maintenance Platform &nbsp;|&nbsp; Version 1.0</p>
    </div>
    """,
    unsafe_allow_html=True,
)