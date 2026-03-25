"""Rendering helpers for the Agri-AI command center."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from dashboard_data import (
    MODULE_CAPTIONS,
    OVERAGE_WATCH_THRESHOLD,
    REQUIRED_OUTPUT_FILES,
    build_crop_chart_data,
    build_crop_week_table,
    format_crop_label,
    format_week_label,
)


_BLUE = "#2f6fe4"
_GREEN = "#2b7a4b"
_AMBER = "#c27a19"
_RED = "#b64a3c"
_INK = "#12202a"

_CSS = """
<style>
:root {
    --bg: #eef1ea;
    --surface: #ffffff;
    --surface-soft: #f7f8f4;
    --line: #d6ddd2;
    --ink: #12202a;
    --muted: #60707a;
    --nav: #13271f;
    --nav-ink: #d7eadf;
    --green: #2b7a4b;
    --amber: #c27a19;
    --red: #b64a3c;
    --blue: #2f6fe4;
    --dark: #1d2b34;
}

html, body, [class*="css"] {
    color: var(--ink);
}

[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(180deg, #eef1ea 0%, #f4f6f1 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #13271f 0%, #173328 100%) !important;
}

[data-testid="stSidebar"] section {
    padding-top: 1.2rem;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: var(--nav-ink) !important;
    font-size: 0.82rem;
}

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] select,
[data-testid="stSidebar"] textarea {
    background: rgba(255, 255, 255, 0.05) !important;
    color: #f7fbf8 !important;
    border: 1px solid rgba(165, 212, 180, 0.28) !important;
    border-radius: 8px !important;
}

.shell-title {
    margin: 0 0 0.1rem 0;
    color: var(--ink);
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.03em;
}

.shell-subtitle {
    margin: 0 0 1rem 0;
    color: var(--muted);
    font-size: 0.92rem;
}

.context-strip,
.surface-card,
.kpi-card,
.briefing-card,
.confidence-card,
.detail-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: 0 1px 4px rgba(14, 28, 23, 0.05);
}

.context-strip {
    padding: 1rem 1rem 0.65rem 1rem;
    margin-bottom: 1rem;
}

.surface-card,
.briefing-card,
.confidence-card,
.detail-card {
    padding: 1rem 1rem 0.85rem 1rem;
}

.briefing-card.dark {
    background: linear-gradient(180deg, #203038 0%, #18252d 100%);
    border-color: #31424a;
    color: #f3f6f7;
}

.briefing-card.dark p,
.briefing-card.dark li,
.briefing-card.dark span {
    color: #d8e2e6;
}

.panel-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.85rem;
}

.panel-title {
    color: var(--ink);
    font-size: 0.95rem;
    font-weight: 800;
    letter-spacing: -0.01em;
    margin: 0;
}

.panel-caption {
    color: var(--muted);
    font-size: 0.77rem;
    margin-top: 0.12rem;
}

.micro-label {
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 0.8rem;
    margin-bottom: 1rem;
}

.kpi-card {
    padding: 1rem 1rem 0.8rem 1rem;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    margin-top: 0.4rem;
    color: var(--ink);
}

.tone-green { color: var(--green) !important; }
.tone-amber { color: var(--amber) !important; }
.tone-red { color: var(--red) !important; }
.tone-blue { color: var(--blue) !important; }
.tone-dark { color: var(--ink) !important; }

.kpi-sub {
    color: var(--muted);
    font-size: 0.76rem;
    margin-top: 0.38rem;
}

.status-pill {
    display: inline-block;
    padding: 0.28rem 0.56rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.03em;
}

.status-pill.green { background: #e3f4ea; color: var(--green); }
.status-pill.amber { background: #fff3da; color: var(--amber); }
.status-pill.red { background: #fde7e3; color: var(--red); }
.status-pill.blue { background: #e6eefc; color: var(--blue); }

.action-card {
    border: 1px solid var(--line);
    border-left-width: 5px;
    border-radius: 12px;
    padding: 0.85rem 0.9rem;
    margin-bottom: 0.7rem;
    background: #fafbf8;
}

.action-card.red { border-left-color: var(--red); }
.action-card.amber { border-left-color: var(--amber); }
.action-card.green { border-left-color: var(--green); }
.action-card.blue { border-left-color: var(--blue); }

.action-topline {
    display: flex;
    gap: 0.55rem;
    align-items: center;
    margin-bottom: 0.35rem;
}

.action-title {
    color: var(--ink);
    font-size: 0.9rem;
    font-weight: 700;
}

.action-meta {
    color: var(--muted);
    font-size: 0.76rem;
    margin-bottom: 0.35rem;
}

.action-copy {
    color: var(--ink);
    font-size: 0.84rem;
    line-height: 1.45;
    margin-bottom: 0.3rem;
}

.action-reco {
    color: var(--muted);
    font-size: 0.78rem;
    line-height: 1.42;
}

.detail-head {
    display: flex;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.9rem;
}

.detail-metrics {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.75rem;
    margin-bottom: 0.9rem;
}

.detail-metric {
    background: var(--surface-soft);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 0.65rem 0.75rem;
}

.detail-metric .value {
    margin-top: 0.25rem;
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--ink);
}

.dash-footer {
    text-align: center;
    color: #7d8a92;
    font-size: 0.75rem;
    padding: 1rem 0 1.5rem 0;
    margin-top: 2rem;
    border-top: 1px solid var(--line);
}

</style>
"""


def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def _tone_to_class(tone: str) -> str:
    return {
        "green": "green",
        "amber": "amber",
        "red": "red",
        "blue": "blue",
    }.get(tone, "blue")


def _priority_to_tone(priority: str) -> str:
    if priority == "Critical":
        return "red"
    if priority in {"High", "Review"}:
        return "amber"
    if priority == "Watch":
        return "blue"
    return "green"


def _style_priority_cell(value: object) -> str:
    value_str = str(value)
    if value_str == "Critical":
        return "background-color: #fde7e3; color: #9f3f33; font-weight: 800;"
    if value_str in {"High", "Review"}:
        return "background-color: #fff3da; color: #9c6015; font-weight: 800;"
    if value_str == "Watch":
        return "background-color: #e6eefc; color: #2f5db8; font-weight: 800;"
    return "background-color: #e3f4ea; color: #2b7a4b; font-weight: 700;"


def _style_coverage_cell(value: object) -> str:
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return ""
    if numeric_value >= 100:
        return "background-color: #e3f4ea; color: #2b7a4b; font-weight: 800;"
    if numeric_value >= 85:
        return "background-color: #fff3da; color: #9c6015; font-weight: 800;"
    return "background-color: #fde7e3; color: #9f3f33; font-weight: 800;"


def _style_issue_cell(value: object) -> str:
    if str(value) == "Shortage":
        return "background-color: #fde7e3; color: #9f3f33; font-weight: 800;"
    return "background-color: #fff3da; color: #9c6015; font-weight: 800;"


def render_missing_outputs(output_dir: Path, missing_files: List[str]) -> None:
    st.error(
        "The command center cannot load because required output files are missing. Run the pipeline first, then reload this page.",
        icon="🚫",
    )
    st.markdown(
        "\n".join(
            [
                f"**Output directory:** `{output_dir}`",
                "",
                "**Missing files:**",
                *[f"- `{file_name}`" for file_name in missing_files],
                "",
                "**Run the pipeline:**",
                "```bash",
                "python3 -m src.main --data-dir data --output-dir output",
                "```",
            ]
        )
    )


def render_header(module: str, role_lens: str, role_headline: str) -> None:
    st.markdown(
        f"<div class='shell-title'>Agri-AI Command Center</div>"
        f"<div class='shell-subtitle'>{MODULE_CAPTIONS[module]} · {role_lens} mode · {role_headline}</div>",
        unsafe_allow_html=True,
    )


def render_status_badge(label: str, tone: str) -> str:
    return f"<span class='status-pill {_tone_to_class(tone)}'>{label}</span>"


def render_panel_header(title: str, caption: str, icon: str = "") -> None:
    display_title = f"{icon} {title}".strip()
    st.markdown(
        "<div class='panel-head'>"
        f"<div><div class='panel-title'>{display_title}</div>"
        f"<div class='panel-caption'>{caption}</div></div>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_kpi_strip(kpis: Dict[str, Any], confidence: Dict[str, Any]) -> None:
    coverage_tone = "green" if kpis["weighted_coverage"] >= 100 else "amber" if kpis["weighted_coverage"] >= 85 else "red"
    risk_tone = "red" if kpis["risk_weeks"] else "green"
    blocker_tone = confidence["state_tone"]
    cards = [
        ("Weighted Coverage", f"{kpis['weighted_coverage']:.1f}%", coverage_tone, "season-wide supply vs demand"),
        ("Demand At Risk", f"{kpis['demand_at_risk']:,.0f}", "red" if kpis["demand_at_risk"] > 0 else "green", "shortage lbs in flagged crop-weeks"),
        ("Overage Exposure", f"{kpis['overage_exposure']:,.0f}", "amber" if kpis["overage_exposure"] > 0 else "green", f"overage lbs above {int(OVERAGE_WATCH_THRESHOLD)}% watch"),
        ("Risk Weeks", str(kpis["risk_weeks"]), risk_tone, "crop-weeks below the coverage threshold"),
        ("Trust Blockers", str(kpis["trust_blockers"]), blocker_tone, confidence["state_label"].lower()),
    ]
    columns = st.columns(5)
    for column, (label, value, tone, sub) in zip(columns, cards):
        column.markdown(
            "<div class='kpi-card'>"
            f"<div class='micro-label'>{label}</div>"
            f"<div class='kpi-value tone-{tone}'>{value}</div>"
            f"<div class='kpi-sub'>{sub}</div>"
            "</div>",
            unsafe_allow_html=True,
        )


def _set_focus(row: pd.Series | Dict[str, Any]) -> None:
    st.session_state["focus_crop"] = str(row["crop_canonical"])
    st.session_state["focus_year"] = int(row["year"])
    st.session_state["focus_week"] = int(row["week_iso"])
    st.rerun()


def render_action_board(action_queue: pd.DataFrame, max_rows: int = 5) -> None:
    if action_queue.empty:
        st.info("No action items are active in the current view.")
        return

    for row in action_queue.head(max_rows).to_dict("records"):
        tone = _priority_to_tone(str(row["priority_label"]))
        cols = st.columns([5, 1])
        with cols[0]:
            st.markdown(
                f"<div class='action-card {tone}'>"
                "<div class='action-topline'>"
                f"{render_status_badge(str(row['priority_label']), tone)}"
                f"<span class='action-title'>{row['action_type']}</span>"
                "</div>"
                f"<div class='action-meta'>{row['crop_label']} · {row['week_label']} · {row['owner']}</div>"
                f"<div class='action-copy'>{row['issue']}</div>"
                f"<div class='action-reco'>{row['recommended_action']}</div>"
                "</div>",
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.button(
                "Focus",
                key=f"action-focus-{row['action_type']}-{row['crop_canonical']}-{row['year']}-{row['week_iso']}",
                on_click=_set_focus,
                args=(row,),
                use_container_width=True,
            )


def _render_dataframe(styled: Any) -> None:
    st.dataframe(styled, use_container_width=True, hide_index=True)


def render_shortage_queue(queue_df: pd.DataFrame, title: str = "Commit-now shortages") -> None:
    render_panel_header(title, "The most exposed crop-weeks that need commitment review.", "⛳")
    if queue_df.empty:
        st.success("No shortage rows are active in the current view.")
        return
    display_df = queue_df.copy()
    display_df = display_df.rename(
        columns={
            "priority_label": "Priority",
            "crop_label": "Crop",
            "week_label": "Week",
            "coverage_pct": "Coverage %",
            "shortage_lbs": "Shortage (lbs)",
            "recommended_action": "Next move",
        }
    )[
        ["Priority", "Crop", "Week", "Coverage %", "Shortage (lbs)", "Next move"]
    ]
    styled = display_df.style.map(_style_priority_cell, subset=["Priority"]).map(
        _style_coverage_cell,
        subset=["Coverage %"],
    )
    _render_dataframe(styled)


def render_overage_queue(queue_df: pd.DataFrame, title: str = "Overage watch") -> None:
    render_panel_header(title, "Surplus-heavy crop-weeks that need demand pull-forward or plan reduction.", "📦")
    if queue_df.empty:
        st.success("No overage rows are above the watch threshold.")
        return
    display_df = queue_df.copy()
    display_df = display_df.rename(
        columns={
            "priority_label": "Priority",
            "crop_label": "Crop",
            "week_label": "Week",
            "coverage_pct": "Coverage %",
            "overage_lbs": "Overage (lbs)",
            "recommended_action": "Next move",
        }
    )[
        ["Priority", "Crop", "Week", "Coverage %", "Overage (lbs)", "Next move"]
    ]
    styled = display_df.style.map(_style_priority_cell, subset=["Priority"]).map(
        _style_coverage_cell,
        subset=["Coverage %"],
    )
    _render_dataframe(styled)


def render_briefing_panel(highlights: List[str]) -> None:
    render_panel_header("Weekly Briefing", "Memo-derived signals that should frame the current review.", "📝")
    if not highlights:
        st.info("No briefing highlights are available for the current output.")
        return
    items = "".join([f"<li>{item}</li>" for item in highlights])
    st.markdown(
        f"<div class='briefing-card dark'><ul style='margin:0 0 0 1rem; padding:0'>{items}</ul></div>",
        unsafe_allow_html=True,
    )


def render_confidence_panel(confidence: Dict[str, Any]) -> None:
    render_panel_header("Data Confidence", "Trust state for the current review window.", "🛡️")
    affected_weeks = ", ".join(confidence["affected_weeks"][:3]) if confidence["affected_weeks"] else "None"
    hours_text = f"{confidence['age_hours']} hours" if confidence["age_hours"] is not None else "Unknown"
    st.markdown(
        "<div class='confidence-card'>"
        f"<div style='margin-bottom:0.65rem'>{render_status_badge(confidence['state_label'], confidence['state_tone'])}</div>"
        f"<div class='action-copy'>{confidence['summary']}</div>"
        f"<div class='action-meta'>Freshness: {confidence['freshness_label']} · Output age: {hours_text}</div>"
        f"<div class='action-meta'>Affected weeks: {affected_weeks}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_focus_detail(detail: Dict[str, Any] | None) -> None:
    render_panel_header("Focused Crop-Week", "Drill into one exposed crop-week without losing command-center context.", "🔎")
    if detail is None:
        st.info("No crop-week is focused in the current view.")
        return
    st.markdown(
        "<div class='detail-card'>"
        "<div class='detail-head'>"
        f"<div><div class='panel-title'>{detail['crop_label']} · {detail['week_label']}</div>"
        f"<div class='panel-caption'>{detail['issue_label']}</div></div>"
        f"{render_status_badge(detail['issue_label'], detail['tone'])}"
        "</div>"
        "<div class='detail-metrics'>"
        f"<div class='detail-metric'><div class='micro-label'>Coverage</div><div class='value tone-{detail['tone']}'>{detail['coverage_pct']:.1f}%</div></div>"
        f"<div class='detail-metric'><div class='micro-label'>Demand</div><div class='value'>{detail['demand_lbs']:,.1f}</div></div>"
        f"<div class='detail-metric'><div class='micro-label'>Supply</div><div class='value'>{detail['supply_lbs']:,.1f}</div></div>"
        f"<div class='detail-metric'><div class='micro-label'>Net Gap</div><div class='value'>{max(detail['shortage_lbs'], detail['overage_lbs']):,.1f}</div></div>"
        "</div>"
        f"<div class='action-copy'>{detail['recommendation']}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_crop_summary(summary_df: pd.DataFrame, max_rows: int = 8) -> None:
    render_panel_header("Crop Concentration", "Crop-level season shape ranked by risk and demand size.", "🌾")
    if summary_df.empty:
        st.info("No crop summary is available for the current view.")
        return
    display_df = summary_df.head(max_rows).copy()
    display_df = display_df.rename(
        columns={
            "crop_label": "Crop",
            "demand_lbs": "Demand (lbs)",
            "supply_lbs": "Supply (lbs)",
            "coverage_pct": "Coverage %",
            "risk_weeks": "Risk Weeks",
            "overage_weeks": "Overage Weeks",
        }
    )[
        ["Crop", "Demand (lbs)", "Supply (lbs)", "Coverage %", "Risk Weeks", "Overage Weeks"]
    ]
    styled = display_df.style.map(_style_coverage_cell, subset=["Coverage %"])
    _render_dataframe(styled)


def render_heatmap(heatmap_df: pd.DataFrame) -> None:
    render_panel_header("Exposure Map", "Coverage by crop and week. Use it to see where problems cluster.", "🧭")
    if heatmap_df.empty:
        st.info("No heatmap data is available for the current view.")
        return
    chart = (
        alt.Chart(heatmap_df)
        .mark_rect(cornerRadius=3)
        .encode(
            x=alt.X("week_label:N", title="Week", sort=None, axis=alt.Axis(labelAngle=-35)),
            y=alt.Y("crop_label:N", title="Crop", sort="-x"),
            color=alt.Color(
                "coverage_pct:Q",
                title="Coverage %",
                scale=alt.Scale(
                    domain=[0, 85, 100, 150],
                    range=["#fde7e3", "#fff3da", "#e3f4ea", "#2b7a4b"],
                ),
            ),
            tooltip=[
                alt.Tooltip("crop_label:N", title="Crop"),
                alt.Tooltip("week_label:N", title="Week"),
                alt.Tooltip("coverage_pct:Q", title="Coverage %", format=",.1f"),
                alt.Tooltip("shortage_lbs:Q", title="Shortage lbs", format=",.1f"),
                alt.Tooltip("overage_lbs:Q", title="Overage lbs", format=",.1f"),
                alt.Tooltip("severity:N", title="Signal"),
            ],
        )
        .properties(height=320)
        .configure_view(strokeWidth=0)
        .configure_axis(grid=False)
    )
    st.altair_chart(chart, use_container_width=True)


def render_weekly_balance_chart(balance_df: pd.DataFrame, title: str = "Season weekly balance") -> None:
    render_panel_header(title, "Demand and supply by week across the current review horizon.", "📈")
    if balance_df.empty:
        st.info("No weekly balance data is available.")
        return
    chart = (
        alt.Chart(balance_df)
        .mark_line(point=True, strokeWidth=2.5)
        .encode(
            x=alt.X("week_label:N", title="Week", sort=None, axis=alt.Axis(labelAngle=-35)),
            y=alt.Y("pounds:Q", title="Pounds"),
            color=alt.Color(
                "series:N",
                scale=alt.Scale(domain=["Demand", "Supply"], range=[_BLUE, _GREEN]),
                title=None,
            ),
            tooltip=[
                alt.Tooltip("week_label:N", title="Week"),
                alt.Tooltip("series:N", title="Series"),
                alt.Tooltip("pounds:Q", title="Pounds", format=",.1f"),
            ],
        )
        .properties(height=260)
        .configure_view(strokeWidth=0)
        .configure_axis(gridColor="#e9eee6")
    )
    st.altair_chart(chart, use_container_width=True)


def render_crop_chart(demand_df: pd.DataFrame, supply_df: pd.DataFrame, crop_name: str | None) -> None:
    render_panel_header("Selected Crop", "Weekly demand vs supply for the focused crop.", "📊")
    if crop_name is None:
        st.info("No crop is focused in the current view.")
        return
    chart_df = build_crop_chart_data(demand_df, supply_df, crop_name)
    if chart_df.empty:
        st.info("No chart data is available for the selected crop.")
        return
    chart = (
        alt.Chart(chart_df)
        .mark_line(point=True, strokeWidth=2.5)
        .encode(
            x=alt.X("week_label:N", title="Week", sort=None, axis=alt.Axis(labelAngle=-35)),
            y=alt.Y("pounds:Q", title="Pounds"),
            color=alt.Color(
                "series:N",
                scale=alt.Scale(domain=["Demand", "Supply"], range=[_BLUE, _GREEN]),
                title=None,
            ),
            tooltip=[
                alt.Tooltip("week_label:N", title="Week"),
                alt.Tooltip("series:N", title="Series"),
                alt.Tooltip("pounds:Q", title="Pounds", format=",.1f"),
            ],
        )
        .properties(height=300)
        .configure_view(strokeWidth=0)
        .configure_axis(gridColor="#e9eee6")
    )
    st.altair_chart(chart, use_container_width=True)


def render_crop_week_table(gap_df: pd.DataFrame, crop_name: str | None) -> None:
    render_panel_header("Crop-Week Imbalance", "Detail rows for the focused crop across the active horizon.", "🗂️")
    table_df = build_crop_week_table(gap_df, crop_name)
    if table_df.empty:
        st.info("No crop-week detail rows are available for the current focus.")
        return
    display_df = table_df.rename(
        columns={
            "week_label": "Week",
            "demand_lbs": "Demand (lbs)",
            "supply_lbs": "Supply (lbs)",
            "coverage_pct": "Coverage %",
            "shortage_lbs": "Shortage (lbs)",
            "overage_lbs": "Overage (lbs)",
        }
    )[
        ["Week", "Demand (lbs)", "Supply (lbs)", "Coverage %", "Shortage (lbs)", "Overage (lbs)"]
    ]
    styled = display_df.style.map(_style_coverage_cell, subset=["Coverage %"])
    _render_dataframe(styled)


def render_risk_register(register_df: pd.DataFrame) -> None:
    render_panel_header("Risk Register", "Exception register built from shortage and overage thresholds.", "🚨")
    if register_df.empty:
        st.success("No active shortage or overage exceptions are in the current view.")
        return
    display_df = register_df.rename(
        columns={
            "priority_label": "Priority",
            "issue_type": "Issue",
            "crop_label": "Crop",
            "week_label": "Week",
            "coverage_pct": "Coverage %",
            "shortage_lbs": "Shortage (lbs)",
            "overage_lbs": "Overage (lbs)",
        }
    )[
        ["Priority", "Issue", "Crop", "Week", "Coverage %", "Shortage (lbs)", "Overage (lbs)"]
    ]
    styled = (
        display_df.style
        .map(_style_priority_cell, subset=["Priority"])
        .map(_style_issue_cell, subset=["Issue"])
        .map(_style_coverage_cell, subset=["Coverage %"])
    )
    _render_dataframe(styled)


def render_unresolved_table(unresolved_df: pd.DataFrame) -> None:
    render_panel_header("Unresolved Inputs", "SKU names that still require canonical mapping.", "🔍")
    if unresolved_df.empty:
        st.success("No unresolved SKU rows are blocking the current view.")
        return
    display_df = unresolved_df.copy()
    display_df["week_label"] = display_df.apply(
        lambda row: format_week_label(int(row["year"]), int(row["week_iso"])),
        axis=1,
    )
    display_df = display_df.rename(
        columns={
            "buyer": "Buyer",
            "crop_raw": "Raw SKU",
            "quantity_lbs": "Quantity (lbs)",
            "week_label": "Week",
            "crop_canonical": "Status",
        }
    )[
        ["Buyer", "Raw SKU", "Quantity (lbs)", "Week", "Status"]
    ]
    _render_dataframe(display_df)


def render_output_status(status_df: pd.DataFrame) -> None:
    render_panel_header("Output Readiness", "File-by-file status for the local dashboard bundle.", "🧱")
    display_df = status_df.rename(
        columns={
            "file_name": "File",
            "status": "Status",
            "last_updated": "Last Updated",
        }
    )
    _render_dataframe(display_df)


def render_copy_button(memo_text: str) -> None:
    payload = json.dumps(memo_text)
    components.html(
        f"""
        <div style="margin:0 0 0.6rem 0;font-family:-apple-system,BlinkMacSystemFont,sans-serif">
          <button
            style="padding:0.46rem 1rem;border-radius:8px;border:none;background:#203038;
                   color:white;font-size:0.82rem;font-weight:700;cursor:pointer;"
            onclick='navigator.clipboard.writeText({payload}).then(()=>{{
              const status=document.getElementById("memo-copy-status");
              status.textContent="Copied";
              status.style.color="#2b7a4b";
              setTimeout(()=>status.textContent="",1800);
            }})'
          >Copy Memo</button>
          <span id="memo-copy-status" style="margin-left:0.7rem;font-size:0.8rem;color:#60707a"></span>
        </div>
        """,
        height=48,
    )


def render_control_tower(context: Dict[str, Any], role_lens: str, focus_detail: Dict[str, Any] | None) -> None:
    if context["filtered_gap"].empty:
        st.info("No crop-week records match the current filters.")
        return

    render_kpi_strip(context["kpis"], context["confidence"])
    left_col, right_col = st.columns([1.6, 1])

    with left_col:
        render_panel_header("What Needs Action Now", "Exception-led queue for the current review window.", "⚡")
        render_action_board(context["action_queue"], max_rows=3 if role_lens == "Executive" else 5)

    with right_col:
        render_briefing_panel(context["memo_highlights"])
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        render_confidence_panel(context["confidence"])

    queue_left, queue_right = st.columns([1, 1])
    with queue_left:
        render_shortage_queue(context["shortage_queue"])
    with queue_right:
        render_overage_queue(context["overage_queue"])

    render_heatmap(context["heatmap_df"])

    lower_left, lower_right = st.columns([1.15, 0.85])
    with lower_left:
        render_weekly_balance_chart(context["weekly_balance"])
    with lower_right:
        render_focus_detail(focus_detail)
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        if role_lens == "Executive":
            with st.expander("Open crop concentration detail", expanded=False):
                render_crop_summary(context["crop_summary"], max_rows=8)
        else:
            render_crop_summary(context["crop_summary"], max_rows=8)


def render_planning(context: Dict[str, Any], focus_detail: Dict[str, Any] | None) -> None:
    posture_df = context["planning_posture"]
    posture_cols = st.columns(3)
    for column, row in zip(posture_cols, posture_df.to_dict("records")):
        column.markdown(
            "<div class='kpi-card'>"
            f"<div class='micro-label'>{row['label']}</div>"
            f"<div class='kpi-value tone-{row['tone']}'>{row['count']}</div>"
            f"<div class='kpi-sub'>{row['pounds']:,.0f} lbs · {row['explanation']}</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    left_col, right_col = st.columns([1.25, 0.95])
    with left_col:
        render_panel_header("Planning Queue", "Use the current gaps to decide where commitment follow-up is due.", "🧠")
        render_action_board(context["action_queue"], max_rows=6)
        render_shortage_queue(context["shortage_queue"], title="Commit-now queue")
        render_overage_queue(context["overage_queue"], title="Rebalance queue")
    with right_col:
        render_focus_detail(focus_detail)
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        render_crop_summary(context["crop_summary"], max_rows=10)

    render_crop_chart(context["filtered_demand"], context["filtered_supply"], focus_detail["crop_canonical"] if focus_detail else None)


def render_demand(context: Dict[str, Any], focus_detail: Dict[str, Any] | None) -> None:
    render_crop_chart(context["filtered_demand"], context["filtered_supply"], focus_detail["crop_canonical"] if focus_detail else None)

    top_left, top_right = st.columns([1.05, 0.95])
    with top_left:
        render_weekly_balance_chart(context["weekly_balance"], title="Whole-season balance")
    with top_right:
        render_crop_summary(context["crop_summary"], max_rows=10)

    render_crop_week_table(context["filtered_gap"], focus_detail["crop_canonical"] if focus_detail else None)


def render_operations(context: Dict[str, Any]) -> None:
    left_col, right_col = st.columns([1.35, 0.85])
    with left_col:
        render_panel_header("Weekly Review Memo", "Use the memo as the narrative layer for the current operating review.", "📘")
        render_copy_button(context["memo_text"])
        st.text_area(
            "Weekly Memo",
            value=context["memo_text"],
            height=380,
            label_visibility="collapsed",
        )
    with right_col:
        render_briefing_panel(context["memo_highlights"])
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        render_confidence_panel(context["confidence"])
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        render_output_status(context["output_status"])

    queue_left, queue_right = st.columns(2)
    with queue_left:
        render_shortage_queue(context["shortage_queue"], title="Meeting shortage queue")
    with queue_right:
        render_overage_queue(context["overage_queue"], title="Meeting overage watch")


def render_intelligence(context: Dict[str, Any], role_lens: str) -> None:
    summary_cols = st.columns(3)
    trust = context["confidence"]
    summary_cards = [
        ("Trust State", trust["state_label"], trust["state_tone"], trust["summary"]),
        ("Freshness", trust["freshness_label"], trust["freshness_tone"], f"output age: {trust['age_hours']} hours" if trust["age_hours"] is not None else "output age: unknown"),
        ("Affected Weeks", str(len(trust["affected_weeks"])), "amber" if trust["affected_weeks"] else "green", ", ".join(trust["affected_weeks"][:3]) if trust["affected_weeks"] else "none"),
    ]
    for column, (label, value, tone, sub) in zip(summary_cols, summary_cards):
        column.markdown(
            "<div class='kpi-card'>"
            f"<div class='micro-label'>{label}</div>"
            f"<div class='kpi-value tone-{tone}'>{value}</div>"
            f"<div class='kpi-sub'>{sub}</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    left_col, right_col = st.columns([1.2, 0.8])
    with left_col:
        render_risk_register(context["risk_register"])
    with right_col:
        render_confidence_panel(context["confidence"])
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        render_unresolved_table(context["filtered_unresolved"])

    if role_lens != "Data Steward":
        render_heatmap(context["heatmap_df"])


def render_admin(context: Dict[str, Any]) -> None:
    assumption_cols = st.columns(3)
    assumption_cards = [
        ("Coverage Threshold", "85%", "blue", "risk-flag threshold used by the pipeline"),
        ("Overage Watch", f"{int(OVERAGE_WATCH_THRESHOLD)}%", "blue", "commercial surplus threshold in the dashboard"),
        ("Tool Contract", "Local First", "green", "reads pipeline outputs directly from the local output directory"),
    ]
    for column, (label, value, tone, sub) in zip(assumption_cols, assumption_cards):
        column.markdown(
            "<div class='kpi-card'>"
            f"<div class='micro-label'>{label}</div>"
            f"<div class='kpi-value tone-{tone}'>{value}</div>"
            f"<div class='kpi-sub'>{sub}</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    left_col, right_col = st.columns([1.1, 0.9])
    with left_col:
        render_output_status(context["output_status"])
    with right_col:
        render_panel_header("Known Limits", "Keep the local tool honest to the current repo and data model.", "📎")
        st.markdown(
            "<div class='surface-card'>"
            "<ul style='margin:0 0 0 1rem; padding:0'>"
            "<li>No buyer-level commercial model yet</li>"
            "<li>No scenario objects or change history</li>"
            "<li>No weather, grower, or site-level operational feeds</li>"
            "<li>No persistent tasks or approvals</li>"
            "<li>No forecast confidence bands</li>"
            "</ul>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        render_panel_header("Run Contract", "How to refresh the local command center bundle.", "⚙️")
        st.code(
            "python3 -m src.main --data-dir data --output-dir output",
            language="bash",
        )


def render_footer() -> None:
    st.markdown(
        "<div class='dash-footer'>Agri-AI · Local analytical command center · Supplier-side planning only</div>",
        unsafe_allow_html=True,
    )
