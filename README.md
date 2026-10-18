#  Machine Health Intelligence (MHI) System

**An End-to-End Predictive Maintenance & Machine Learning Project**

An interactive machine health assessment system that uses machine learning to estimate equipment failure risk, analyze operating conditions, and support data-driven maintenance decisions.

<p align="center">
  <a href="https://mhisproject.streamlit.app/">🚀 Live Demo</a> •
  <a href="https://github.com/abhinavkumar1268b/Machine-Health-Intelligence-System-Project">📂 GitHub Repository</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?logo=scikitlearn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/XGBoost-Classifier-179c7d" alt="XGBoost">
</p>

---

##  1. Project Overview

Unexpected machine failures can cause production downtime, higher maintenance costs, and operational inefficiencies.

The **Machine Health Intelligence System (MHI)** uses historical machine sensor data and machine learning to estimate failure risk and present machine health information through a Streamlit dashboard.

The project combines **Data Analytics, Exploratory Data Analysis (EDA), Feature Engineering, Machine Learning, and Interactive Visualization** in one application.

##  2. Business Objectives

- Analyze machine operating conditions and failure patterns.
- Identify relationships between sensor parameters and machine failures.
- Compare machine learning models using classification metrics.
- Estimate failure probability and calculate a machine health score.
- Provide risk-based maintenance guidance.
- Enable what-if analysis for different operating conditions.

##  3. Key Features

- **Failure Prediction:** Estimates failure probability using an XGBoost classifier.
- **Health Score:** Converts predicted failure probability into a 0–100 score.
- **Risk Classification:** Categorizes predictions into Low, Medium, High, and Critical risk.
- **What-If Analysis:** Explore the effect of changing machine input parameters.
- **Maintenance Recommendations:** Provides guidance based on the assigned risk category.
- **Exploratory Data Analysis:** Visualizes dataset distributions and feature relationships.
- **PDF Reports:** Supports downloadable reports, where implemented in the application.
- **Interactive Dashboard:** Presents predictions and analytical insights through Streamlit.

##  4. Dataset Overview

**Dataset:** AI4I 2020 Predictive Maintenance Dataset  
**Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset)

| Dataset Metric | Value |
|---|---:|
| Total Records | 10,000 |
| Healthy Records | 9,661 |
| Failure Records | 339 |
| Healthy Rate | 96.61% |
| Failure Rate | 3.39% |

### Important Features

- `Type` — Product or machine type
- `Air temperature` — Ambient temperature
- `Process temperature` — Operating process temperature
- `Rotational speed` — Machine speed in RPM
- `Torque` — Machine torque
- `Tool wear` — Accumulated tool wear

### Engineered Features

| Feature | Purpose |
|---|---|
| `Temp_Diff` | Difference between process and air temperature |
| `Power_Index` | Represents the relationship between torque and rotational speed |
| `Wear_Speed_Ratio` | Relates tool wear to rotational speed |
| `Temperature_Stress` | Represents a temperature-related operating condition |

*Feature definitions should match the formulas implemented in the project's preprocessing pipeline.*

##  5. Data Analytics Workflow

```text
Raw Dataset
    ↓
Data Cleaning & Validation
    ↓
Exploratory Data Analysis
    ↓
Feature Engineering
    ↓
Model Training & Comparison
    ↓
Model Evaluation
    ↓
Failure Risk Prediction
    ↓
Streamlit Dashboard & Insights
```

The dataset has a significant class imbalance, with failure cases representing only 3.39% of observations. Therefore, failure-class recall, precision, F1-score, and the confusion matrix are important alongside accuracy.

##  6. Machine Learning Model Performance

The project compares four classification algorithms to evaluate their ability to identify machine failures.

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 96.00% | 0.880 | 0.790 | 0.830 | 0.920 |
| Random Forest | 98.50% | 0.950 | 0.940 | 0.945 | 0.990 |
| SVM | 97.20% | 0.910 | 0.860 | 0.885 | 0.950 |
| **XGBoost** | **98.90%** | **0.970** | **0.960** | **0.965** | **0.995** |

**Selected Model:** XGBoost, according to the current project report.

*Note: These metrics are reported project results and should be verified against the actual test-set evaluation output before publication. Use the same test set and evaluation procedure for a fair comparison.*

### Confusion Matrix

The confusion matrix should be generated from the final model's actual test predictions to report:

- **True Positive (TP):** Failure cases correctly detected.
- **True Negative (TN):** Healthy cases correctly identified.
- **False Positive (FP):** Healthy cases incorrectly flagged as failures.
- **False Negative (FN):** Actual failures missed by the model.

##  7. Health Score & Risk Classification

The application translates model-estimated failure probability into a more understandable health score.

**Formula:**

`Health Score = (1 − Failure Probability) × 100`

| Risk Level | Health Score | Suggested Action |
|---|---:|---|
| 🟢 Low | 85–100 | Routine monitoring |
| 🟡 Medium | 70–84 | Schedule maintenance |
| 🟠 High | 50–69 | Prompt inspection |
| 🔴 Critical | 0–49 | Urgent engineering assessment |

*Risk categories are application-defined thresholds for decision support, not validated industrial safety limits.*

##  8. Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Visualization | Plotly, Matplotlib, Seaborn |
| Dashboard | Streamlit |
| Explainable AI | SHAP, where integrated |
| Reporting | FPDF / ReportLab, as implemented |
| Version Control | Git, GitHub |


##  9. Business Value

This project demonstrates how machine data can be transformed into actionable analytical outputs.

- **Risk visibility:** Helps users identify observations with higher model-estimated failure risk.
- **Data-driven decisions:** Combines sensor data, model predictions, and risk categories.
- **Operational awareness:** Highlights the importance of detecting failures in an imbalanced dataset.
- **Interactive exploration:** Enables users to investigate different operating conditions.
- **Scalable direction:** Provides a foundation for future monitoring and reporting automation.

*Potential benefits are described qualitatively; actual reductions in downtime or maintenance costs have not been established without real-world validation.*

##  10. Future Enhancements

- Real-time IoT sensor integration using MQTT.
- Remaining Useful Life (RUL) estimation.
- SHAP-based prediction explanations.
- Automated high-risk alerts and scheduled reports.
- Model monitoring and data-drift detection.
- Validation using real industrial operating data.

##  Author

**Abhinav Kumar**  
*Data Analytics & Machine Learning Practitioner*

- GitHub: [@abhinavkumar1268b](https://github.com/abhinavkumar1268b)
- Live Demo: [Machine Health Intelligence System](https://mhisproject.streamlit.app/)

---

⭐ If you find this project useful, consider starring the repository.


