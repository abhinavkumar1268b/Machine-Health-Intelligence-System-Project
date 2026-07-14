"""
utils.py — Shared Streamlit UI helpers and path utilities.

Import this module at the top of every page to guarantee the project
root is on sys.path (required for `from src.xxx import ...` to work
regardless of how/where Streamlit is launched).
"""

import sys
import streamlit as st
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────────────
# Path bootstrap — must run before any `src.*` imports in pages
# ──────────────────────────────────────────────────────────────────────────────

def get_project_root() -> Path:
    """Return the absolute project root directory."""
    # utils.py lives at the project root, so __file__.parent IS the root.
    return Path(__file__).resolve().parent


def setup_path() -> None:
    """
    Ensure the project root is in sys.path so that `from src.xxx import …`
    works correctly from any page, regardless of the CWD when Streamlit runs.
    """
    root = str(get_project_root())
    if root not in sys.path:
        sys.path.insert(0, root)


# Run immediately on import so any page that does `import utils` or
# `from utils import …` automatically gets the path set up.
setup_path()


# ──────────────────────────────────────────────────────────────────────────────
# Streamlit UI helpers
# ──────────────────────────────────────────────────────────────────────────────

def page_header(title: str, subtitle: str | None = None) -> None:
    """Render a consistent page title + optional subtitle."""
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()


def metric_card(col, label: str, value, delta=None) -> None:
    """Render a st.metric inside the given column."""
    with col:
        st.metric(label=label, value=value, delta=delta)


def status_box(risk: str) -> None:
    """Render a coloured Streamlit alert based on risk level string."""
    if "Critical" in risk:
        st.error(f"🔴 {risk}")
    elif "High" in risk:
        st.warning(f"🟠 {risk}")
    elif "Medium" in risk:
        st.info(f"🟡 {risk}")
    else:
        st.success(f"🟢 {risk}")


def risk_badge(risk: str) -> None:
    """Alias for status_box — use whichever name reads better in context."""
    status_box(risk)