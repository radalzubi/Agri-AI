"""Local Streamlit dashboard for reviewing Agri-AI planning outputs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


REQUIRED_OUTPUT_FILES = {
    "gap_analysis": "gap_analysis.csv",
    "demand": "demand_by_crop_week.csv",
    "supply": "supply_by_crop_week.csv",
    "unresolved": "unresolved_skus.csv",
    "memo": "weekly_memo.txt",
}

_GREEN = "#16a34a"
_BLUE  = "#2563eb"

_CSS = """
<style>

[data-testid="stAppViewContainer"] > .main {
    background: #f0f4f0;
}

[data-testid="stSidebar"] {
    background: #14532d !important;
}
[data-testid="stSidebar"] section { padding-top: 1.5rem; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: #bbf7d0 !important; font-size: 0.82rem; }
[data-testid="stSidebar"] input {
    background: #166534 !important;
    color: #f0fdf4 !important;
    border: 1px solid #4ade80 !important;
    border-radius: 6px !important;
}

.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1.4rem 1rem 1.4rem;
    border: 1px solid #d1fae5;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 0.25rem;
}
.kpi-label {
    font-size: 0.71rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #6b7280;
    margin-bottom: 0.45rem;
}
.kpi-value {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1;
    color: #111827;
}
.kpi-value.green { color: #16a34a; }
.kpi-value.red   { color: #dc2626; }
.kpi-value.amber { color: #d97706; }
.kpi-value.gray  { color: #374151; }
.kpi-sub { font-size: 0.73rem; color: #9ca3af; margin-top: 0.3rem; }

.sec-head {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin: 0 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid #d1fae5;
}
.sec-head-icon { font-size: 1.1rem; }
.sec-head-text { font-size: 1rem; font-weight: 700; color: #166534; letter-spacing: -0.01em; }

.filter-strip {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 0.9rem 1.1rem 0.4rem 1.1rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}

[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    border: 1px solid #d1fae5 !important;
    overflow: hidden;
}

.chart-card {
    background: white;
    border-radius: 14px;
    border: 1px solid #d1fae5;
    padding: 1.25rem 1.25rem 0.5rem 1.25rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.memo-card {
    background: white;
    border-radius: 14px;
    border: 1px solid #d1fae5;
    padding: 1.25rem 1.4rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 0.75rem;
}

hr.agri-hr {
    border: none;
    border-top: 1px solid #d1fae5;
    margin: 2rem 0 1.5rem 0;
}

.sb-pill {
    border-radius: 8px;
    padding: 0.55rem 0.85rem;
    font-size: 0.8rem;
    font-weight: 600;
    margin-top: 0.5rem;
    line-height: 1.4;
}
.sb-pill.danger { background: #7f1d1d; color: #fca5a5; }
.sb-pill.warn   { background: #78350f; color: #fde68a; }
.sb-pill.ok     { background: #14532d; color: #86efac; border: 1px solid #4ade80; }

.dash-footer {
    text-align: center;
    color: #9ca3af;
    font-size: 0.75rem;
    padding: 1rem 0 1.5rem 0;
    border-top: 1px solid #e5e7eb;
    margin-top: 2.5rem;
}

</style>
"""


def normalize_risk_flag(value: object) -> bool:
    """Handle bools and CSV string representations consistently."""
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def load_output_bundle(
    output_dir: Path,
) -> Tuple[Dict[str, pd.DataFrame | str], List[str]]:
    """Load all dashboard inputs from an output directory."""
    missing_files = [
        name for name in REQUIRED_OUTPUT_FILES.values()
        if not (output_dir / name).exists()
    ]
    if missing_files:
        return {}, missing_files

    gap_df        = pd.read_csv(output_dir / REQUIRED_OUTPUT_FILES["gap_analysis"])
    demand_df     = pd.read_csv(output_dir / REQUIRED_OUTPUT_FILES["demand"])
    supply_df     = pd.read_csv(output_dir / REQUIRED_OUTPUT_FILES["supply"])
    unresolved_df = pd.read_csv(output_dir / REQUIRED_OUTPUT_FILES["unresolved"])
    memo_text     = (output_dir / REQUIRED_OUTPUT_FILES["memo"]).read_text(encoding="utf-8")

    if "risk_flag" in gap_df.columns:
        gap_df["risk_flag"] = gap_df["risk_flag"].map(normalize_risk_flag)

    for frame in (gap_df, demand_df, supply_df, unresolved_df):
        if "week_iso" in frame.columns:
            frame["week_iso"] = (
                pd.to_numeric(frame["week_iso"], errors="coerce").fillna(0).astype(int)
            )
        if "year" in frame.columns:
            frame["year"] = (
                pd.to_numeric(frame["year"], errors="coerce").fillna(0).astype(int)
            )

    return {
        "gap_df": gap_df,
        "demand_df": demand_df,
        "supply_df": supply_df,
        "unresolved_df": unresolved_df,
        "memo_text": memo_text,
    }, []


def format_week_label(year: int, week_iso: int) -> str:
    return f"{year}-W{week_iso:02d}"


def last_modified_str(output_dir: Path) -> str:
    """Human-readable mtime for gap_analysis.csv, or empty string if missing."""
    path = output_dir / REQUIRED_OUTPUT_FILES["gap_analysis"]
    if not path.exists():
        return ""
    dt = datetime.fromtimestamp(path.stat().st_mtime)
    return dt.strftime("%d %b %Y, %I:%M %p").lstrip("0")


def _sec(icon: str, title: str) -> None:
    st.markdown(
        f'<div class="sec-head">'
        f'<span class="sec-head-icon">{icon}</span>'
        f'<span class="sec-head-text">{title}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _hr() -> None:
    st.markdown('<hr class="agri-hr">', unsafe_allow_html=True)


def render_missing_outputs(output_dir: Path, missing_files: List[str]) -> None:
    st.error(
        "Pipeline outputs not found. Run the Agri-AI pipeline first, then reload this page.",
        icon="🚫",
    )
    st.markdown(
        "\n".join([
            f"**Output directory:** `{output_dir}`",
            "",
            "**Missing files:**",
            *[f"- `{f}`" for f in missing_files],
            "",
            "**Run the pipeline:**",
            "```bash",
            "python3 -m src.main --data-dir data --output-dir output",
            "```",
        ])
    )


def render_sidebar(risk_count: int, unresolved_count: int, last_run: str) -> None:
    if last_run:
        st.sidebar.markdown(
            f"<p style='color:#d1fae5;font-size:0.78rem;margin:0.4rem 0 1rem 0'>"
            f"Last run: <strong style='color:white'>{last_run}</strong></p>",
            unsafe_allow_html=True,
        )
    st.sidebar.markdown(
        "<p style='color:#86efac;font-size:0.72rem;font-weight:700;"
        "text-transform:uppercase;letter-spacing:0.07em;margin:1.2rem 0 0.4rem 0'>"
        "Season status</p>",
        unsafe_allow_html=True,
    )
    if risk_count > 0:
        label = f"&#9888;  {risk_count} risk-flagged crop-week{'s' if risk_count != 1 else ''}"
        st.sidebar.markdown(f'<div class="sb-pill danger">{label}</div>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<div class="sb-pill ok">&#10003;  No risk flags</div>', unsafe_allow_html=True)
    if unresolved_count > 0:
        label = f"&#128269;  {unresolved_count} unresolved SKU{'s' if unresolved_count != 1 else ''}"
        st.sidebar.markdown(f'<div class="sb-pill warn">{label}</div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        "<p style='color:#4ade80;font-size:0.72rem;margin-top:2rem'>Run pipeline:</p>"
        "<code style='color:#d1fae5;font-size:0.72rem;background:#166534;"
        "padding:0.4rem 0.6rem;border-radius:6px;display:block;line-height:1.7'>"
        "python3 -m src.main<br>  --data-dir data<br>  --output-dir output</code>",
        unsafe_allow_html=True,
    )


def render_summary_cards(gap_df: pd.DataFrame, unresolved_df: pd.DataFrame) -> None:
    total_crops      = int(gap_df["crop_canonical"].nunique()) if not gap_df.empty else 0
    total_weeks      = (
        int(gap_df[["year", "week_iso"]].drop_duplicates().shape[0]) if not gap_df.empty else 0
    )
    risk_count       = int(gap_df["risk_flag"].sum()) if not gap_df.empty else 0
    unresolved_count = int(len(unresolved_df.index))

    risk_cls       = "red"   if risk_count > 0       else "green"
    unresolved_cls = "amber" if unresolved_count > 0 else "green"
    risk_sub       = "action required" if risk_count > 0 else "all clear"
    unresolved_sub = "needs review"    if unresolved_count > 0 else "all matched"

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, label, value, cls, sub in [
        (c1, "&#127807;", "Crops Tracked",           total_crops,       "gray",        "in gap analysis"),
        (c2, "&#128197;", "Weeks with Data",          total_weeks,       "gray",        "planning horizon"),
        (c3, "&#9888;",   "Risk-Flagged Crop-Weeks",  risk_count,        risk_cls,      risk_sub),
        (c4, "&#128269;", "Unresolved SKUs",           unresolved_count,  unresolved_cls, unresolved_sub),
    ]:
        col.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">{icon} {label}</div>'
            f'<div class="kpi-value {cls}">{value}</div>'
            f'<div class="kpi-sub">{sub}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def build_risk_table(gap_df: pd.DataFrame) -> pd.DataFrame:
    t = gap_df.copy()
    t["Week"]           = t.apply(
        lambda r: format_week_label(int(r["year"]), int(r["week_iso"])), axis=1
    )
    t["Demand (lbs)"]   = t["total_demand_lbs"].round(2)
    t["Supply (lbs)"]   = t["total_supply_lbs"].round(2)
    t["Coverage %"]     = (t["coverage_ratio"] * 100).round(1)
    t["Shortage (lbs)"] = t["shortage_lbs"].round(2)
    t["Overage (lbs)"]  = t["overage_lbs"].round(2)
    t["Crop"]           = t["crop_canonical"]
    t["Risk"]           = t["risk_flag"].map(lambda v: "Yes" if v else "No")

    t = t.sort_values(
        by=["risk_flag", "shortage_pct", "week_iso"],
        ascending=[False, False, True],
    )
    return t[["Week", "Crop", "Demand (lbs)", "Supply (lbs)", "Coverage %",
              "Shortage (lbs)", "Overage (lbs)", "Risk"]]


def _style_row(row: pd.Series) -> list[str]:
    """Highlight the full row for risk-flagged entries."""
    if row.get("Risk") == "Yes":
        return ["background-color: #fff1f2; color: #7f1d1d;"] * len(row)
    return [""] * len(row)


def _style_coverage(val: object) -> str:
    try:
        v = float(val)
    except (ValueError, TypeError):
        return ""
    if v >= 100:
        return "background-color: #dcfce7; color: #166534; font-weight: 700;"
    if v >= 75:
        return "background-color: #fef9c3; color: #854d0e; font-weight: 700;"
    return "background-color: #fee2e2; color: #991b1b; font-weight: 700;"


def _style_risk_cell(val: object) -> str:
    if str(val) == "Yes":
        return "background-color: #fee2e2; color: #991b1b; font-weight: 700;"
    return "background-color: #dcfce7; color: #166534; font-weight: 600;"


def build_chart_data(
    demand_df: pd.DataFrame,
    supply_df: pd.DataFrame,
    crop_name: str,
) -> pd.DataFrame:
    crop_demand = demand_df[demand_df["crop_canonical"] == crop_name].copy()
    crop_supply = supply_df[supply_df["crop_canonical"] == crop_name].copy()

    merged = crop_demand.merge(
        crop_supply,
        on=["crop_canonical", "week_iso", "year"],
        how="outer",
    ).fillna({"total_demand_lbs": 0.0, "total_supply_lbs": 0.0})

    if merged.empty:
        return merged

    merged["week_label"] = merged.apply(
        lambda r: format_week_label(int(r["year"]), int(r["week_iso"])), axis=1
    )
    merged = merged.sort_values(by=["year", "week_iso"])

    long_df = merged.melt(
        id_vars=["week_label", "week_iso", "year"],
        value_vars=["total_demand_lbs", "total_supply_lbs"],
        var_name="series",
        value_name="pounds",
    )
    long_df["series"] = long_df["series"].map(
        {"total_demand_lbs": "Demand", "total_supply_lbs": "Supply"}
    )
    return long_df


def render_copy_button(memo_text: str) -> None:
    payload = json.dumps(memo_text)
    components.html(
        f"""
        <div style="margin:0 0 0.6rem 0;font-family:-apple-system,BlinkMacSystemFont,sans-serif">
          <button
            style="padding:0.45rem 1.1rem;border-radius:8px;border:none;background:#166534;
                   color:white;font-size:0.84rem;font-weight:600;cursor:pointer;"
            onmouseover="this.style.background='#14532d'"
            onmouseout="this.style.background='#166534'"
            onclick='navigator.clipboard.writeText({payload}).then(()=>{{
              const s=document.getElementById("cs");
              s.textContent="Copied to clipboard";
              s.style.color="#166534";
              setTimeout(()=>s.textContent="",2000);
            }})'
          >Copy Memo</button>
          <span id="cs" style="margin-left:0.8rem;font-size:0.82rem;color:#6b7280"></span>
        </div>
        """,
        height=50,
    )


def main() -> None:
    st.set_page_config(
        page_title="Agri-AI Dashboard",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(_CSS, unsafe_allow_html=True)

    st.sidebar.markdown(
        "<h2 style='color:#4ade80;font-size:1.05rem;font-weight:800;margin:0 0 1.2rem 0'>"
        "Agri-AI</h2>",
        unsafe_allow_html=True,
    )
    output_dir_input = st.sidebar.text_input("Output directory", value="output")
    output_dir = Path(output_dir_input).expanduser()

    bundle, missing_files = load_output_bundle(output_dir)
    if missing_files:
        st.markdown(
            "<h1 style='font-size:1.75rem;font-weight:800;color:#14532d'>"
            "Agri-AI Operator Dashboard</h1>",
            unsafe_allow_html=True,
        )
        render_missing_outputs(output_dir, missing_files)
        st.stop()

    gap_df        = bundle["gap_df"]
    demand_df     = bundle["demand_df"]
    supply_df     = bundle["supply_df"]
    unresolved_df = bundle["unresolved_df"]
    memo_text     = bundle["memo_text"]

    risk_count       = int(gap_df["risk_flag"].sum()) if not gap_df.empty else 0
    unresolved_count = int(len(unresolved_df.index))
    last_run         = last_modified_str(output_dir)

    render_sidebar(risk_count, unresolved_count, last_run)

    st.markdown(
        "<h1 style='font-size:1.75rem;font-weight:800;color:#14532d;margin:0 0 0.2rem 0'>"
        "Agri-AI Operator Dashboard</h1>"
        "<p style='color:#6b7280;font-size:0.88rem;margin:0 0 1.75rem 0'>"
        "Weekly supply planning — buyer demand vs grower commitments</p>",
        unsafe_allow_html=True,
    )

    render_summary_cards(gap_df, unresolved_df)
    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)

    # ── Risk table ──
    _hr()
    _sec("📋", "Risk Table")

    with st.container():
        st.markdown('<div class="filter-strip">', unsafe_allow_html=True)
        fc1, fc2, fc3 = st.columns([2, 1, 2])
        crop_options   = sorted(gap_df["crop_canonical"].dropna().unique().tolist())
        selected_crops = fc1.multiselect("Filter by crop", options=crop_options, default=[])
        risk_only      = fc2.checkbox("Risk only", value=False)
        min_week = int(gap_df["week_iso"].min()) if not gap_df.empty else 1
        max_week = int(gap_df["week_iso"].max()) if not gap_df.empty else 52
        week_range = fc3.slider(
            "Week range",
            min_value=min_week,
            max_value=max_week,
            value=(min_week, max_week),
        )
        st.markdown("</div>", unsafe_allow_html=True)

    filtered = gap_df.copy()
    if selected_crops:
        filtered = filtered[filtered["crop_canonical"].isin(selected_crops)]
    if risk_only:
        filtered = filtered[filtered["risk_flag"]]
    filtered = filtered[filtered["week_iso"].between(week_range[0], week_range[1])]

    risk_table = build_risk_table(filtered)
    styled = (
        risk_table.style
        .apply(_style_row, axis=1)
        .map(_style_coverage, subset=["Coverage %"])
        .map(_style_risk_cell, subset=["Risk"])
    )
    st.dataframe(styled, use_container_width=True, hide_index=True)

    # ── Demand vs Supply chart ──
    _hr()
    _sec("📊", "Demand vs Supply")

    if crop_options:
        chart_crop = st.selectbox("Select crop", options=crop_options, index=0)
        chart_df   = build_chart_data(demand_df, supply_df, chart_crop)

        if not chart_df.empty:
            crop_title = chart_crop.replace("_", " ").title()
            chart = (
                alt.Chart(chart_df)
                .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                .encode(
                    x=alt.X(
                        "week_label:N",
                        title="Week",
                        sort=None,
                        axis=alt.Axis(labelAngle=-40, labelFontSize=11, titleFontSize=12),
                    ),
                    y=alt.Y(
                        "pounds:Q",
                        title="Pounds",
                        axis=alt.Axis(labelFontSize=11, titleFontSize=12),
                    ),
                    xOffset=alt.XOffset("series:N"),
                    color=alt.Color(
                        "series:N",
                        scale=alt.Scale(domain=["Demand", "Supply"], range=[_BLUE, _GREEN]),
                        legend=alt.Legend(
                            title=None,
                            orient="top-right",
                            labelFontSize=12,
                            symbolSize=80,
                        ),
                    ),
                    tooltip=[
                        alt.Tooltip("week_label:N", title="Week"),
                        alt.Tooltip("series:N",     title="Series"),
                        alt.Tooltip("pounds:Q",     title="Pounds", format=",.1f"),
                    ],
                )
                .properties(
                    height=360,
                    title=alt.TitleParams(
                        text=f"{crop_title} — Weekly Demand vs Supply",
                        fontSize=13,
                        fontWeight=600,
                        color="#166534",
                        anchor="start",
                    ),
                )
                .configure_view(strokeWidth=0, fill="white")
                .configure_axis(
                    grid=True,
                    gridColor="#f1f5f9",
                    gridOpacity=1,
                    domainColor="#d1d5db",
                )
                .configure_title(offset=14)
            )
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.altair_chart(chart, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No chart data available for the selected crop.")
    else:
        st.info("No crop data available. Run the pipeline first.")

    # ── Weekly memo ──
    _hr()
    _sec("📝", "Weekly Memo")
    st.markdown('<div class="memo-card">', unsafe_allow_html=True)
    render_copy_button(memo_text)
    st.markdown("</div>", unsafe_allow_html=True)
    st.text_area("Memo", value=memo_text, height=340, label_visibility="collapsed")

    # ── Unresolved SKUs ──
    if not unresolved_df.empty:
        _hr()
        _sec("🔍", "Unresolved SKUs")
        st.warning(
            f"**{len(unresolved_df)} unresolved crop name(s) found.** "
            "Review these rows before trusting dashboard totals.",
            icon="⚠️",
        )
        display_df = unresolved_df.copy()
        display_df["Week"] = display_df.apply(
            lambda r: format_week_label(int(r["year"]), int(r["week_iso"])), axis=1
        )
        st.dataframe(
            display_df[
                ["buyer", "crop_raw", "quantity_lbs", "Week", "crop_canonical"]
            ].rename(
                columns={
                    "buyer": "Buyer",
                    "crop_raw": "Raw SKU",
                    "quantity_lbs": "Quantity (lbs)",
                    "crop_canonical": "Status",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown(
        "<div class='dash-footer'>"
        "Agri-AI &nbsp;&middot;&nbsp; Local operator tool &nbsp;&middot;&nbsp; Not for distribution"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
