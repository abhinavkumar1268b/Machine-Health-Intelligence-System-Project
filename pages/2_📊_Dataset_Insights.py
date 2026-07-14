"""
2_Dataset_Insights.py — Explore the machine failure dataset used for training.
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

from src.config import DATA_PATH

# ── Page config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dataset Insights — MHI",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Dataset Insights")
st.caption("Explore the machine failure dataset used for training the MHI model.")

# ── Data loading (cached) ─────────────────────────────────────────────────

@st.cache_data(show_spinner="Loading dataset…")
def load_data() -> pd.DataFrame:
    """Load the cleaned training dataset from disk."""
    return pd.read_csv(DATA_PATH)


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        f"Dataset not found at `{DATA_PATH}`.\n\n"
        "Please ensure `data/cleanData.csv` exists in the project root."
    )
    st.stop()
except Exception as exc:
    st.error(f"Failed to load dataset: {exc}")
    st.stop()

# ── KPI metrics ───────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows",              f"{len(df):,}")
c2.metric("Columns",           len(df.columns))
c3.metric("Missing Values",    int(df.isna().sum().sum()))
c4.metric("Memory (KB)",       round(df.memory_usage(deep=True).sum() / 1024, 1))

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Preview",
    "📐 Statistics",
    "📊 Distributions",
    "🔥 Correlation",
    "🎯 Target Analysis",
])

# ── Tab 1: Preview ────────────────────────────────────────────────────────
with tab1:
    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "⬇️ Download Dataset (CSV)",
        data=df.to_csv(index=False),
        file_name="machine_dataset.csv",
        mime="text/csv",
    )

# ── Tab 2: Statistics ─────────────────────────────────────────────────────
with tab2:
    st.subheader("Column Information")
    info = pd.DataFrame({
        "Column":    df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing":   df.isna().sum().values,
        "Unique":    df.nunique().values,
        "% Missing": (df.isna().sum() / len(df) * 100).round(2).values,
    })
    st.dataframe(info, use_container_width=True, hide_index=True)

    st.subheader("Statistical Summary (Numeric Columns)")
    st.dataframe(df.describe().T.round(3), use_container_width=True)

# ── Tab 3: Distributions ──────────────────────────────────────────────────
with tab3:
    num_cols = df.select_dtypes(include="number").columns.tolist()

    if not num_cols:
        st.warning("No numeric columns found in the dataset.")
    else:
        feature = st.selectbox("Select Feature", num_cols, key="dist_feature")

        col_a, col_b = st.columns(2)

        with col_a:
            fig_hist = px.histogram(
                df, x=feature, nbins=30,
                title=f"{feature} — Histogram",
                color_discrete_sequence=["#636EFA"],
            )
            fig_hist.update_layout(bargap=0.05)
            st.plotly_chart(fig_hist, use_container_width=True)

        with col_b:
            fig_box = px.box(
                df, y=feature,
                title=f"{feature} — Box Plot",
                color_discrete_sequence=["#636EFA"],
            )
            st.plotly_chart(fig_box, use_container_width=True)

# ── Tab 4: Correlation ────────────────────────────────────────────────────
with tab4:
    corr = df.corr(numeric_only=True)

    fig_heat = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        title="Feature Correlation Heatmap",
        aspect="auto",
    )
    fig_heat.update_layout(height=550)
    st.plotly_chart(fig_heat, use_container_width=True)

    with st.expander("View Correlation Table"):
        st.dataframe(corr.round(3), use_container_width=True)

# ── Tab 5: Target Analysis ────────────────────────────────────────────────
with tab5:
    target = "Machine failure"

    if target not in df.columns:
        st.warning(f"Target column `{target}` not found in dataset.")
    else:
        counts = df[target].value_counts().rename(index={0: "Healthy", 1: "Failure"})

        col1, col2 = st.columns(2)

        with col1:
            fig_pie = px.pie(
                values=counts.values,
                names=counts.index,
                title="Target Class Distribution",
                color_discrete_map={"Healthy": "#2ecc71", "Failure": "#e74c3c"},
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            fig_bar = px.bar(
                x=counts.index,
                y=counts.values,
                labels={"x": "Class", "y": "Count"},
                title="Failure vs Healthy Count",
                color=counts.index,
                color_discrete_map={"Healthy": "#2ecc71", "Failure": "#e74c3c"},
                text_auto=True,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()

        num_cols_target = [c for c in df.columns if c != target]
        compare_feature = st.selectbox(
            "Compare Feature with Target",
            num_cols_target,
            key="target_compare",
        )

        fig_compare = px.box(
            df,
            x=target,
            y=compare_feature,
            color=target,
            title=f"{compare_feature} vs Machine Failure",
            labels={target: "Machine Failure"},
            color_discrete_map={0: "#2ecc71", 1: "#e74c3c"},
        )
        st.plotly_chart(fig_compare, use_container_width=True)
