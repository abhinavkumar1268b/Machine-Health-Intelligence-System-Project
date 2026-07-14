"""
pdf_generator.py — Generate a PDF machine health report using ReportLab.

ReportLab's default PDF encoding does not support emoji characters.
This module strips emojis from any string before writing to the PDF.
"""

import re
import unicodedata
from pathlib import Path
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors

from src.config import REPORT_DIR


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _strip_emoji(text: str) -> str:
    """Remove emoji / non-latin-1 characters that ReportLab cannot encode."""
    # Remove characters outside the Basic Multilingual Plane (most emojis)
    cleaned = re.sub(
        r"[^\u0000-\uFFFF]",
        "",
        text,
        flags=re.UNICODE,
    )
    # Also strip category So (other symbol) which includes coloured circles
    cleaned = "".join(
        ch for ch in cleaned
        if unicodedata.category(ch) not in ("So", "Mn")
    )
    return cleaned.strip()


def _p(text: str, style) -> Paragraph:
    """Convenience: strip emoji then return a Paragraph."""
    return Paragraph(_strip_emoji(str(text)), style)


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def create_pdf(report: dict, input_data: dict, output_file: str | None = None) -> str:
    """
    Generate a PDF Machine Health Report.

    Parameters
    ----------
    report      : dict  Output of generate_machine_report().
    input_data  : dict  Raw feature dictionary from the prediction form.
    output_file : str   Optional absolute path for the PDF.
                        Defaults to reports/Machine_Health_Report_<timestamp>.pdf

    Returns
    -------
    str  Absolute path to the generated PDF file.
    """
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = str(REPORT_DIR / f"Machine_Health_Report_{timestamp}.pdf")

    # Ensure output directory exists
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    title_style  = styles["Title"]
    h2_style     = styles["Heading2"]
    normal_style = styles["Normal"]
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=normal_style,
        leftIndent=20,
        spaceAfter=4,
    )

    story = []

    # ── Title ─────────────────────────────────────────────────────────────
    story.append(_p("<b>Machine Health Intelligence (MHI)</b>", title_style))
    story.append(_p("AI-Powered Predictive Maintenance Report", normal_style))
    story.append(Spacer(1, 0.4 * cm))

    # ── Machine Parameters ────────────────────────────────────────────────
    story.append(_p("<b>Machine Parameters</b>", h2_style))
    param_map = {
        "Machine Type":      input_data.get("Type", "—"),
        "Air Temperature":   f"{input_data.get('Air temperature [K]', '—')} K",
        "Process Temp":      f"{input_data.get('Process temperature [K]', '—')} K",
        "Rotational Speed":  f"{input_data.get('Rotational speed [rpm]', '—')} RPM",
        "Torque":            f"{input_data.get('Torque [Nm]', '—')} Nm",
        "Tool Wear":         f"{input_data.get('Tool wear [min]', '—')} min",
    }
    for label, value in param_map.items():
        story.append(_p(f"<b>{label}:</b> {value}", normal_style))
    story.append(Spacer(1, 0.3 * cm))

    # ── Prediction Summary ────────────────────────────────────────────────
    story.append(_p("<b>Prediction Summary</b>", h2_style))
    story.append(_p(f"Failure Probability : {report.get('Failure Probability', '—')}%", normal_style))
    story.append(_p(f"Health Score        : {report.get('Health Score', '—')}%",        normal_style))
    story.append(_p(f"Risk Level          : {report.get('Risk Level', '—')}",            normal_style))
    story.append(_p(f"Estimated Downtime  : {report.get('Downtime', '—')}",              normal_style))
    story.append(_p(f"Estimated Cost      : {report.get('Estimated Cost', '—')}",        normal_style))
    story.append(Spacer(1, 0.3 * cm))

    # ── Failure Causes ────────────────────────────────────────────────────
    story.append(_p("<b>Failure Causes</b>", h2_style))
    for cause in report.get("Failure Causes", []):
        story.append(_p(f"• {cause}", bullet_style))
    story.append(Spacer(1, 0.3 * cm))

    # ── Recommendations ───────────────────────────────────────────────────
    story.append(_p("<b>Maintenance Recommendations</b>", h2_style))
    for i, rec in enumerate(report.get("Recommendations", []), 1):
        story.append(_p(f"{i}. {rec}", bullet_style))
    story.append(Spacer(1, 0.5 * cm))

    # ── Footer ────────────────────────────────────────────────────────────
    story.append(_p(
        f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ParagraphStyle("Footer", parent=normal_style, textColor=colors.grey, fontSize=8),
    ))

    # Build PDF
    doc = SimpleDocTemplate(output_file)
    doc.build(story)

    return output_file