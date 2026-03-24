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

ROLE_LENS_COPY = {
    "Supply Planner": "Start with shortage exposure, the action queue, and crop-week coverage gaps.",
    "Aggregator Manager": "Use the control tower to protect demand, balance surplus, and decide where intervention is required.",
    "Executive": "Focus on season health, demand at risk, and whether the current plan is commercially acceptable.",
}

_GREEN = "#16a34a"
_BLUE = "#2563eb"
_RED = "#dc2626"
_AMBER = "#d97706"

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
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] select {
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
    font-size: 2.2rem;
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
    padding: 0.95rem 1.1rem 0.55rem 1.1rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}

.role-callout {
    background: white;
    border: 1px solid #d1fae5;
    border-left: 5px solid #16a34a;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    margin: 0 0 1rem 0;
    color: #374151;
    font-size: 0.86rem;
}

.chart-card,
.memo-card,
.panel-card {
    background: white;
    border-radius: 14px;
    border: 1px solid #d1fae5;
    padding: 1.2rem 1.25rem 0.75rem 1.25rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.dash-footer {
    text-align: center;
    color: #9ca3af;
    font-size: 0.75rem;
    padding: 1rem 0 1.5rem 0;
    border-top: 1px solid #e5e7eb;
    margin-top: 2.5rem;
}

hr.agri-hr {
    border: none;
    border-top: 1px solid #d1fae5;
    margin: 1.35rem 0 1.2rem 0;
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

</style>
"""


def normalize_risk_flag(value: object) -> bool:
    """Handle bools and CSV string representations consistently."""
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def format_crop_label(crop_name: object) -> str:
    text = str(crop_name).strip()
    if not text:
        return ""
    if text.upper() == "UNRESOLVED":
        return "Unresolved"
    return text.replace("_", " ").title()


def format_week_label(year: int, week_iso: int) -> str:
    return f"{year}-W{week_iso:02d}"


def modified_at_str(path: Path) -> str:
    if not path.exists():
        return ""
    dt = datetime.fromtimestamp(path.stat().st_mtime)
    return dt.strftime("%d %b %Y, %I:%M %p").lstrip("0")


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

    gap_df = pd.read_csv(output_dir / REQUIRED_OUTPUT_FILES["gap_analysis"])
    demand_df = pd.read_csv(output_dir / REQUIRED_OUTPUT_FILES["demand"])
    supply_df = pd.read_csv(output_dir / REQUIRED_OUTPUT_FILES["supply"])
    unresolved_df = pd.read_csv(output_dir / REQUIRED_OUTPUT_FILES["unresolved"])
    memo_text = (output_dir / REQUIRED_OUTPUT_FILES["memo"]).read_text(encoding="utf-8")

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


def apply_filters_to_frame(
    frame: pd.DataFrame,
    years: List[int],
    crops: List[str],
    week_range: Tuple[int, int],
) -> pd.DataFrame:
    """Apply shared dashboard filters when the frame contains the relevant columns."""
    filtered = frame.copy()
    if filtered.empty:
        return filtered
    if "year" in filtered.columns and years:
        filtered = filtered[filtered["year"].isin(years)]
    if "crop_canonical" in filtered.columns and crops:
        filtered = filtered[filtered["crop_canonical"].isin(crops)]
    if "week_iso" in filtered.columns:
        filtered = filtered[filtered["week_iso"].between(week_range[0], week_range[1])]
    return filtered


def _sec(icon: str, title: str) -> None:
    st.markdown(
        f'<div class="sec-head">'
        f'<span class="sec-head-icon">{icon}</span>'
        f'<span class="sec-head-text">{title}</span>'
        f"</div>",
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


def render_sidebar(
    risk_count: int,
    unresolved_count: int,
    last_run: str,
    role_lens: str,
) -> None:
    if last_run:
        st.sidebar.markdown(
            f"<p style='color:#d1fae5;font-size:0.78rem;margin:0.35rem 0 0.9rem 0'>"
            f"Last run: <strong style='color:white'>{last_run}</strong></p>",
            unsafe_allow_html=True,
        )
    st.sidebar.markdown(
        "<p style='color:#86efac;font-size:0.72rem;font-weight:700;"
        "text-transform:uppercase;letter-spacing:0.07em;margin:1rem 0 0.4rem 0'>"
        "Role focus</p>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        f"<p style='color:#d1fae5;font-size:0.8rem;line-height:1.5;margin:0'>"
        f"<strong style='color:white'>{role_lens}</strong><br>{ROLE_LENS_COPY[role_lens]}</p>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        "<p style='color:#86efac;font-size:0.72rem;font-weight:700;"
        "text-transform:uppercase;letter-spacing:0.07em;margin:1.3rem 0 0.4rem 0'>"
        "Season status</p>",
        unsafe_allow_html=True,
    )
    if risk_count > 0:
        label = f"&#9888;  {risk_count} risk-flagged crop-week{'s' if risk_count != 1 else ''}"
        st.sidebar.markdown(f'<div class="sb-pill danger">{label}</div>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown(
            '<div class="sb-pill ok">&#10003;  No risk flags in view</div>',
            unsafe_allow_html=True,
        )
    if unresolved_count > 0:
        label = f"&#128269;  {unresolved_count} unresolved SKU row{'s' if unresolved_count != 1 else ''}"
        st.sidebar.markdown(f'<div class="sb-pill warn">{label}</div>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown(
            '<div class="sb-pill ok">&#10003;  No data quality blockers</div>',
            unsafe_allow_html=True,
        )
    st.sidebar.markdown(
        "<p style='color:#4ade80;font-size:0.72rem;margin-top:1.6rem'>Run pipeline:</p>"
        "<code style='color:#d1fae5;font-size:0.72rem;background:#166534;"
        "padding:0.4rem 0.6rem;border-radius:6px;display:block;line-height:1.7'>"
        "python3 -m src.main<br>  --data-dir data<br>  --output-dir output</code>",
        unsafe_allow_html=True,
    )


def render_overview_cards(gap_df: pd.DataFrame, unresolved_df: pd.DataFrame) -> None:
    total_demand = float(gap_df["total_demand_lbs"].sum()) if not gap_df.empty else 0.0
    total_supply = float(gap_df["total_supply_lbs"].sum()) if not gap_df.empty else 0.0
    weighted_coverage = (total_supply / total_demand * 100.0) if total_demand else 0.0
    demand_at_risk = float(gap_df.loc[gap_df["risk_flag"], "shortage_lbs"].sum()) if not gap_df.empty else 0.0
    overage_watch = float(gap_df.loc[gap_df["overage_pct"] > 20, "overage_lbs"].sum()) if not gap_df.empty else 0.0
    risk_count = int(gap_df["risk_flag"].sum()) if not gap_df.empty else 0
    unresolved_count = int(len(unresolved_df.index))

    coverage_cls = "green" if weighted_coverage >= 100 else "amber" if weighted_coverage >= 85 else "red"
    risk_cls = "red" if risk_count > 0 else "green"
    unresolved_cls = "amber" if unresolved_count > 0 else "green"

    columns = st.columns(5)
    cards = [
        ("Season Coverage", f"{weighted_coverage:.1f}%", coverage_cls, "weighted supply vs demand"),
        ("Demand At Risk", f"{demand_at_risk:,.0f}", "red" if demand_at_risk > 0 else "green", "shortage lbs in flagged weeks"),
        ("Overage Exposure", f"{overage_watch:,.0f}", "amber" if overage_watch > 0 else "green", "overage lbs above watch threshold"),
        ("Risk Weeks", str(risk_count), risk_cls, "crop-weeks below coverage threshold"),
        ("Data Issues", str(unresolved_count), unresolved_cls, "unresolved SKU rows in current view"),
    ]
    for col, (label, value, cls, sub_text) in zip(columns, cards):
        col.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value {cls}">{value}</div>'
            f'<div class="kpi-sub">{sub_text}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )


def build_shortage_queue(gap_df: pd.DataFrame) -> pd.DataFrame:
    """Return the shortage queue ordered by severity."""
    risk_df = gap_df[gap_df["risk_flag"]].copy()
    if risk_df.empty:
        return pd.DataFrame(columns=["Priority", "Week", "Crop", "Coverage %", "Shortage (lbs)"])

    def priority(row: pd.Series) -> str:
        shortage_pct = float(row["shortage_pct"])
        if shortage_pct >= 50:
            return "Critical"
        if shortage_pct >= 25:
            return "High"
        return "Review"

    risk_df["Priority"] = risk_df.apply(priority, axis=1)
    risk_df["Week"] = risk_df.apply(
        lambda record: format_week_label(int(record["year"]), int(record["week_iso"])),
        axis=1,
    )
    risk_df["Crop"] = risk_df["crop_canonical"].map(format_crop_label)
    risk_df["Coverage %"] = (risk_df["coverage_ratio"] * 100).round(1)
    risk_df["Shortage (lbs)"] = risk_df["shortage_lbs"].round(1)
    return risk_df.sort_values(
        by=["shortage_pct", "week_iso"],
        ascending=[False, True],
    )[["Priority", "Week", "Crop", "Coverage %", "Shortage (lbs)"]]


def build_overage_queue(gap_df: pd.DataFrame) -> pd.DataFrame:
    """Return overage watch rows with commercial relevance."""
    over_df = gap_df[gap_df["overage_pct"] > 20].copy()
    if over_df.empty:
        return pd.DataFrame(columns=["Priority", "Week", "Crop", "Coverage %", "Overage (lbs)"])

    def priority(row: pd.Series) -> str:
        overage_pct = float(row["overage_pct"])
        if overage_pct >= 50:
            return "High"
        return "Watch"

    over_df["Priority"] = over_df.apply(priority, axis=1)
    over_df["Week"] = over_df.apply(
        lambda record: format_week_label(int(record["year"]), int(record["week_iso"])),
        axis=1,
    )
    over_df["Crop"] = over_df["crop_canonical"].map(format_crop_label)
    over_df["Coverage %"] = (over_df["coverage_ratio"] * 100).round(1)
    over_df["Overage (lbs)"] = over_df["overage_lbs"].round(1)
    return over_df.sort_values(
        by=["overage_pct", "week_iso"],
        ascending=[False, True],
    )[["Priority", "Week", "Crop", "Coverage %", "Overage (lbs)"]]


def build_action_queue(gap_df: pd.DataFrame, unresolved_count: int) -> pd.DataFrame:
    """Translate gap rows into recommended operator actions."""
    action_rows: List[Dict[str, object]] = []

    for row in gap_df.sort_values(by=["risk_flag", "shortage_pct", "overage_pct"], ascending=[False, False, False]).itertuples():
        week_label = format_week_label(int(row.year), int(row.week_iso))
        crop_label = format_crop_label(row.crop_canonical)
        if row.risk_flag:
            shortage_pct = float(row.shortage_pct)
            priority = "Critical" if shortage_pct >= 50 else "High" if shortage_pct >= 25 else "Review"
            action_rows.append(
                {
                    "Priority": priority,
                    "Owner": "Supply Planner",
                    "Week": week_label,
                    "Crop": crop_label,
                    "Issue": "Shortage risk",
                    "Recommended action": "Confirm grower capacity and protect the most exposed demand.",
                }
            )
        elif float(row.overage_pct) > 20:
            overage_pct = float(row.overage_pct)
            priority = "High" if overage_pct >= 50 else "Watch"
            action_rows.append(
                {
                    "Priority": priority,
                    "Owner": "Account Manager",
                    "Week": week_label,
                    "Crop": crop_label,
                    "Issue": "Overage risk",
                    "Recommended action": "Pull demand forward or open buyer conversations before surplus becomes expensive.",
                }
            )

    if unresolved_count > 0:
        action_rows.insert(
            0,
            {
                "Priority": "Review",
                "Owner": "Data Steward",
                "Week": "Now",
                "Crop": "Data quality",
                "Issue": "Unresolved SKU rows",
                "Recommended action": "Resolve unmapped crop names before using the dashboard as a planning source of truth.",
            },
        )

    return pd.DataFrame(action_rows)


def build_crop_summary(gap_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize season health by crop."""
    if gap_df.empty:
        return pd.DataFrame(
            columns=[
                "Crop",
                "Demand (lbs)",
                "Supply (lbs)",
                "Coverage %",
                "Risk Weeks",
                "Overage Weeks",
            ]
        )

    grouped = (
        gap_df.groupby("crop_canonical", dropna=False)
        .agg(
            demand_lbs=("total_demand_lbs", "sum"),
            supply_lbs=("total_supply_lbs", "sum"),
            risk_weeks=("risk_flag", "sum"),
            overage_weeks=("overage_pct", lambda series: int((series > 20).sum())),
        )
        .reset_index()
    )
    grouped["Crop"] = grouped["crop_canonical"].map(format_crop_label)
    grouped["Demand (lbs)"] = grouped["demand_lbs"].round(1)
    grouped["Supply (lbs)"] = grouped["supply_lbs"].round(1)
    grouped["Coverage %"] = (
        grouped.apply(
            lambda row: (row["supply_lbs"] / row["demand_lbs"] * 100.0) if row["demand_lbs"] else 0.0,
            axis=1,
        ).round(1)
    )
    grouped["Risk Weeks"] = grouped["risk_weeks"].astype(int)
    grouped["Overage Weeks"] = grouped["overage_weeks"].astype(int)
    return grouped.sort_values(
        by=["Risk Weeks", "Demand (lbs)"],
        ascending=[False, False],
    )[["Crop", "Demand (lbs)", "Supply (lbs)", "Coverage %", "Risk Weeks", "Overage Weeks"]]


def build_weekly_balance(demand_df: pd.DataFrame, supply_df: pd.DataFrame) -> pd.DataFrame:
    """Build weekly demand versus supply totals for the filtered view."""
    demand_by_week = (
        demand_df.groupby(["year", "week_iso"], dropna=False)["total_demand_lbs"]
        .sum()
        .reset_index()
    )
    supply_by_week = (
        supply_df.groupby(["year", "week_iso"], dropna=False)["total_supply_lbs"]
        .sum()
        .reset_index()
    )
    merged = demand_by_week.merge(
        supply_by_week,
        on=["year", "week_iso"],
        how="outer",
    ).fillna({"total_demand_lbs": 0.0, "total_supply_lbs": 0.0})
    if merged.empty:
        return merged
    merged["week_label"] = merged.apply(
        lambda record: format_week_label(int(record["year"]), int(record["week_iso"])),
        axis=1,
    )
    merged = merged.sort_values(by=["year", "week_iso"])
    long_df = merged.melt(
        id_vars=["year", "week_iso", "week_label"],
        value_vars=["total_demand_lbs", "total_supply_lbs"],
        var_name="series",
        value_name="pounds",
    )
    long_df["series"] = long_df["series"].map(
        {
            "total_demand_lbs": "Demand",
            "total_supply_lbs": "Supply",
        }
    )
    return long_df


def build_crop_chart_data(
    demand_df: pd.DataFrame,
    supply_df: pd.DataFrame,
    crop_name: str,
) -> pd.DataFrame:
    """Build demand and supply rows for one crop across weeks."""
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
        lambda record: format_week_label(int(record["year"]), int(record["week_iso"])),
        axis=1,
    )
    merged = merged.sort_values(by=["year", "week_iso"])
    long_df = merged.melt(
        id_vars=["year", "week_iso", "week_label"],
        value_vars=["total_demand_lbs", "total_supply_lbs"],
        var_name="series",
        value_name="pounds",
    )
    long_df["series"] = long_df["series"].map(
        {
            "total_demand_lbs": "Demand",
            "total_supply_lbs": "Supply",
        }
    )
    return long_df


def build_coverage_heatmap(gap_df: pd.DataFrame) -> pd.DataFrame:
    """Prepare crop-week coverage for the heatmap."""
    if gap_df.empty:
        return gap_df
    heatmap_df = gap_df.copy()
    heatmap_df["Crop"] = heatmap_df["crop_canonical"].map(format_crop_label)
    heatmap_df["week_label"] = heatmap_df.apply(
        lambda record: format_week_label(int(record["year"]), int(record["week_iso"])),
        axis=1,
    )
    heatmap_df["coverage_pct"] = (heatmap_df["coverage_ratio"] * 100).round(1)
    return heatmap_df.sort_values(by=["year", "week_iso", "Crop"])


def build_output_status_table(output_dir: Path) -> pd.DataFrame:
    """Show file readiness and freshness for the output bundle."""
    rows: List[Dict[str, object]] = []
    for file_name in REQUIRED_OUTPUT_FILES.values():
        path = output_dir / file_name
        rows.append(
            {
                "File": file_name,
                "Status": "Ready" if path.exists() else "Missing",
                "Last Updated": modified_at_str(path) if path.exists() else "Not found",
            }
        )
    return pd.DataFrame(rows)


def build_risk_table(gap_df: pd.DataFrame) -> pd.DataFrame:
    """Create the detailed risk desk table."""
    if gap_df.empty:
        return pd.DataFrame(
            columns=[
                "Week",
                "Crop",
                "Demand (lbs)",
                "Supply (lbs)",
                "Coverage %",
                "Shortage (lbs)",
                "Overage (lbs)",
                "Risk",
            ]
        )
    table_df = gap_df.copy()
    table_df["Week"] = table_df.apply(
        lambda record: format_week_label(int(record["year"]), int(record["week_iso"])),
        axis=1,
    )
    table_df["Crop"] = table_df["crop_canonical"].map(format_crop_label)
    table_df["Demand (lbs)"] = table_df["total_demand_lbs"].round(1)
    table_df["Supply (lbs)"] = table_df["total_supply_lbs"].round(1)
    table_df["Coverage %"] = (table_df["coverage_ratio"] * 100).round(1)
    table_df["Shortage (lbs)"] = table_df["shortage_lbs"].round(1)
    table_df["Overage (lbs)"] = table_df["overage_lbs"].round(1)
    table_df["Risk"] = table_df["risk_flag"].map(lambda value: "Yes" if value else "No")
    return table_df.sort_values(
        by=["risk_flag", "shortage_pct", "overage_pct", "week_iso"],
        ascending=[False, False, False, True],
    )[
        [
            "Week",
            "Crop",
            "Demand (lbs)",
            "Supply (lbs)",
            "Coverage %",
            "Shortage (lbs)",
            "Overage (lbs)",
            "Risk",
        ]
    ]


def _style_priority_cell(value: object) -> str:
    value_str = str(value)
    if value_str == "Critical":
        return "background-color: #fee2e2; color: #991b1b; font-weight: 700;"
    if value_str == "High":
        return "background-color: #ffedd5; color: #9a3412; font-weight: 700;"
    if value_str == "Review":
        return "background-color: #fef3c7; color: #92400e; font-weight: 700;"
    if value_str == "Watch":
        return "background-color: #e0f2fe; color: #0c4a6e; font-weight: 700;"
    return ""


def _style_coverage_cell(value: object) -> str:
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return ""
    if numeric_value >= 100:
        return "background-color: #dcfce7; color: #166534; font-weight: 700;"
    if numeric_value >= 85:
        return "background-color: #fef3c7; color: #854d0e; font-weight: 700;"
    return "background-color: #fee2e2; color: #991b1b; font-weight: 700;"


def _style_risk_cell(value: object) -> str:
    if str(value) == "Yes":
        return "background-color: #fee2e2; color: #991b1b; font-weight: 700;"
    return "background-color: #dcfce7; color: #166534; font-weight: 600;"


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
              const status=document.getElementById("copy-status");
              status.textContent="Copied to clipboard";
              status.style.color="#166534";
              setTimeout(()=>status.textContent="",2000);
            }})'
          >Copy Memo</button>
          <span id="copy-status" style="margin-left:0.8rem;font-size:0.82rem;color:#6b7280"></span>
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
        "<h2 style='color:#4ade80;font-size:1.05rem;font-weight:800;margin:0 0 1.1rem 0'>"
        "Agri-AI</h2>",
        unsafe_allow_html=True,
    )
    output_dir_input = st.sidebar.text_input("Output directory", value="output")
    role_lens = st.sidebar.selectbox(
        "Role lens",
        options=list(ROLE_LENS_COPY.keys()),
        index=0,
    )
    output_dir = Path(output_dir_input).expanduser()

    bundle, missing_files = load_output_bundle(output_dir)
    if missing_files:
        st.markdown(
            "<h1 style='font-size:1.75rem;font-weight:800;color:#14532d'>"
            "Agri-AI Pilot Control Tower</h1>",
            unsafe_allow_html=True,
        )
        render_missing_outputs(output_dir, missing_files)
        st.stop()

    gap_df = bundle["gap_df"]
    demand_df = bundle["demand_df"]
    supply_df = bundle["supply_df"]
    unresolved_df = bundle["unresolved_df"]
    memo_text = bundle["memo_text"]

    year_options = sorted(gap_df["year"].dropna().unique().tolist()) if not gap_df.empty else []
    default_years = year_options[-1:] if year_options else []
    crop_options = sorted(gap_df["crop_canonical"].dropna().unique().tolist()) if not gap_df.empty else []
    min_week = int(gap_df["week_iso"].min()) if not gap_df.empty else 1
    max_week = int(gap_df["week_iso"].max()) if not gap_df.empty else 52

    st.markdown(
        "<h1 style='font-size:1.8rem;font-weight:800;color:#14532d;margin:0 0 0.15rem 0'>"
        "Agri-AI Pilot Control Tower</h1>"
        "<p style='color:#6b7280;font-size:0.9rem;margin:0 0 1rem 0'>"
        "Pre-season and in-season supply planning for buyer-facing agricultural operators</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="role-callout"><strong>{role_lens}</strong><br>{ROLE_LENS_COPY[role_lens]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="filter-strip">', unsafe_allow_html=True)
    filter_col1, filter_col2, filter_col3 = st.columns([1, 2, 2])
    selected_years = filter_col1.multiselect(
        "Season",
        options=year_options,
        default=default_years,
    )
    selected_years = selected_years or year_options
    selected_crops = filter_col2.multiselect(
        "Crop filter",
        options=crop_options,
        default=[],
        format_func=format_crop_label,
    )
    week_range = filter_col3.slider(
        "Week range",
        min_value=min_week,
        max_value=max_week,
        value=(min_week, max_week),
    )
    st.markdown("</div>", unsafe_allow_html=True)

    filtered_gap = apply_filters_to_frame(gap_df, selected_years, selected_crops, week_range)
    filtered_demand = apply_filters_to_frame(demand_df, selected_years, selected_crops, week_range)
    filtered_supply = apply_filters_to_frame(supply_df, selected_years, selected_crops, week_range)
    filtered_unresolved = apply_filters_to_frame(unresolved_df, selected_years, [], week_range)
    active_crop_options = (
        sorted(filtered_gap["crop_canonical"].dropna().unique().tolist())
        if not filtered_gap.empty
        else []
    )

    risk_count = int(filtered_gap["risk_flag"].sum()) if not filtered_gap.empty else 0
    unresolved_count = int(len(filtered_unresolved.index))
    render_sidebar(
        risk_count=risk_count,
        unresolved_count=unresolved_count,
        last_run=modified_at_str(output_dir / REQUIRED_OUTPUT_FILES["gap_analysis"]),
        role_lens=role_lens,
    )

    active_weeks = int(filtered_gap[["year", "week_iso"]].drop_duplicates().shape[0]) if not filtered_gap.empty else 0
    active_crops = int(filtered_gap["crop_canonical"].nunique()) if not filtered_gap.empty else 0
    st.caption(f"Current view: {active_crops} crops across {active_weeks} active crop-weeks")

    tabs = st.tabs(
        [
            "Control Tower",
            "Demand & Coverage",
            "Risk Desk",
            "Planning Memo",
            "Data Quality",
        ]
    )

    with tabs[0]:
        _sec("🎯", "Control Tower")
        if filtered_gap.empty:
            st.info("No crop-week records match the current filters.")
        else:
            render_overview_cards(filtered_gap, filtered_unresolved)

            _hr()
            shortage_queue = build_shortage_queue(filtered_gap)
            overage_queue = build_overage_queue(filtered_gap)
            left_col, right_col = st.columns(2)

            with left_col:
                _sec("🚨", "Critical Shortages")
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                if shortage_queue.empty:
                    st.success("No shortage rows in the current view.")
                else:
                    styled_shortage = shortage_queue.head(8).style.map(
                        _style_priority_cell,
                        subset=["Priority"],
                    ).map(
                        _style_coverage_cell,
                        subset=["Coverage %"],
                    )
                    st.dataframe(styled_shortage, width="stretch", hide_index=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with right_col:
                _sec("📦", "Overage Watch")
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                if overage_queue.empty:
                    st.success("No commercial overage rows in the current view.")
                else:
                    styled_overage = overage_queue.head(8).style.map(
                        _style_priority_cell,
                        subset=["Priority"],
                    ).map(
                        _style_coverage_cell,
                        subset=["Coverage %"],
                    )
                    st.dataframe(styled_overage, width="stretch", hide_index=True)
                st.markdown("</div>", unsafe_allow_html=True)

            _hr()
            _sec("✅", "Action Queue")
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            action_queue = build_action_queue(filtered_gap, unresolved_count)
            if action_queue.empty:
                st.success("No recommended actions for the current view.")
            else:
                styled_actions = action_queue.style.map(
                    _style_priority_cell,
                    subset=["Priority"],
                )
                st.dataframe(styled_actions, width="stretch", hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

            _hr()
            heatmap_col, balance_col = st.columns(2)
            with heatmap_col:
                _sec("🧭", "Coverage Heatmap")
                heatmap_df = build_coverage_heatmap(filtered_gap)
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                if heatmap_df.empty:
                    st.info("No coverage rows available.")
                else:
                    heatmap_chart = (
                        alt.Chart(heatmap_df)
                        .mark_rect(cornerRadius=4)
                        .encode(
                            x=alt.X(
                                "week_label:N",
                                title="Week",
                                sort=None,
                                axis=alt.Axis(labelAngle=-35, labelFontSize=11, titleFontSize=12),
                            ),
                            y=alt.Y(
                                "Crop:N",
                                title="Crop",
                                sort=alt.EncodingSortField(field="Crop", order="ascending"),
                                axis=alt.Axis(labelFontSize=11, titleFontSize=12),
                            ),
                            color=alt.Color(
                                "coverage_pct:Q",
                                title="Coverage %",
                                scale=alt.Scale(
                                    domain=[0, 85, 100, 150],
                                    range=["#fee2e2", "#fef3c7", "#dcfce7", "#16a34a"],
                                ),
                            ),
                            tooltip=[
                                alt.Tooltip("week_label:N", title="Week"),
                                alt.Tooltip("Crop:N", title="Crop"),
                                alt.Tooltip("coverage_pct:Q", title="Coverage %", format=",.1f"),
                                alt.Tooltip("shortage_lbs:Q", title="Shortage lbs", format=",.1f"),
                                alt.Tooltip("overage_lbs:Q", title="Overage lbs", format=",.1f"),
                            ],
                        )
                        .properties(height=320)
                        .configure_view(strokeWidth=0)
                    )
                    st.altair_chart(heatmap_chart, width="stretch")
                st.markdown("</div>", unsafe_allow_html=True)

            with balance_col:
                _sec("📉", "Weekly Demand Vs Supply")
                balance_df = build_weekly_balance(filtered_demand, filtered_supply)
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                if balance_df.empty:
                    st.info("No weekly demand or supply rows in the current view.")
                else:
                    balance_chart = (
                        alt.Chart(balance_df)
                        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                        .encode(
                            x=alt.X(
                                "week_label:N",
                                title="Week",
                                sort=None,
                                axis=alt.Axis(labelAngle=-35, labelFontSize=11, titleFontSize=12),
                            ),
                            y=alt.Y(
                                "pounds:Q",
                                title="Pounds",
                                axis=alt.Axis(labelFontSize=11, titleFontSize=12),
                            ),
                            xOffset=alt.XOffset("series:N"),
                            color=alt.Color(
                                "series:N",
                                title=None,
                                scale=alt.Scale(domain=["Demand", "Supply"], range=[_BLUE, _GREEN]),
                            ),
                            tooltip=[
                                alt.Tooltip("week_label:N", title="Week"),
                                alt.Tooltip("series:N", title="Series"),
                                alt.Tooltip("pounds:Q", title="Pounds", format=",.1f"),
                            ],
                        )
                        .properties(height=320)
                        .configure_view(strokeWidth=0)
                    )
                    st.altair_chart(balance_chart, width="stretch")
                st.markdown("</div>", unsafe_allow_html=True)

    with tabs[1]:
        _sec("📊", "Demand And Coverage")
        if filtered_gap.empty:
            st.info("No crop-week rows match the current filters.")
        else:
            summary_col, chart_col = st.columns([1.1, 1])
            with summary_col:
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                crop_summary = build_crop_summary(filtered_gap)
                styled_summary = crop_summary.style.map(
                    _style_coverage_cell,
                    subset=["Coverage %"],
                )
                st.dataframe(styled_summary, width="stretch", hide_index=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with chart_col:
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                crop_choice = st.selectbox(
                    "Crop",
                    options=active_crop_options,
                    format_func=format_crop_label,
                )
                crop_chart_df = build_crop_chart_data(filtered_demand, filtered_supply, crop_choice)
                if crop_chart_df.empty:
                    st.info("No demand or supply rows for the selected crop.")
                else:
                    crop_chart = (
                        alt.Chart(crop_chart_df)
                        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                        .encode(
                            x=alt.X(
                                "week_label:N",
                                title="Week",
                                sort=None,
                                axis=alt.Axis(labelAngle=-35, labelFontSize=11, titleFontSize=12),
                            ),
                            y=alt.Y(
                                "pounds:Q",
                                title="Pounds",
                                axis=alt.Axis(labelFontSize=11, titleFontSize=12),
                            ),
                            xOffset=alt.XOffset("series:N"),
                            color=alt.Color(
                                "series:N",
                                title=None,
                                scale=alt.Scale(domain=["Demand", "Supply"], range=[_BLUE, _GREEN]),
                            ),
                            tooltip=[
                                alt.Tooltip("week_label:N", title="Week"),
                                alt.Tooltip("series:N", title="Series"),
                                alt.Tooltip("pounds:Q", title="Pounds", format=",.1f"),
                            ],
                        )
                        .properties(height=320, title=format_crop_label(crop_choice))
                        .configure_view(strokeWidth=0)
                    )
                    st.altair_chart(crop_chart, width="stretch")
                st.markdown("</div>", unsafe_allow_html=True)

    with tabs[2]:
        _sec("📋", "Risk Desk")
        if filtered_gap.empty:
            st.info("No risk desk rows match the current filters.")
        else:
            local_filter_col1, local_filter_col2 = st.columns(2)
            show_risk_only = local_filter_col1.checkbox("Show risk only", value=False)
            show_overage_only = local_filter_col2.checkbox("Show overage watch only", value=False)

            risk_desk_df = filtered_gap.copy()
            if show_risk_only:
                risk_desk_df = risk_desk_df[risk_desk_df["risk_flag"]]
            if show_overage_only:
                risk_desk_df = risk_desk_df[risk_desk_df["overage_pct"] > 20]

            risk_table = build_risk_table(risk_desk_df)
            if risk_table.empty:
                st.info("No rows match the risk desk filters.")
            else:
                styled_risk_table = risk_table.style.map(
                    _style_coverage_cell,
                    subset=["Coverage %"],
                ).map(
                    _style_risk_cell,
                    subset=["Risk"],
                )
                st.dataframe(styled_risk_table, width="stretch", hide_index=True)

    with tabs[3]:
        _sec("📝", "Planning Memo")
        st.markdown('<div class="memo-card">', unsafe_allow_html=True)
        render_copy_button(memo_text)
        st.markdown("</div>", unsafe_allow_html=True)
        st.text_area("Memo", value=memo_text, height=360, label_visibility="collapsed")

    with tabs[4]:
        _sec("🔍", "Data Quality")
        status_df = build_output_status_table(output_dir)
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.dataframe(status_df, width="stretch", hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        _hr()
        if filtered_unresolved.empty:
            st.success("No unresolved SKU rows in the current filtered horizon.")
        else:
            st.warning(
                f"**{len(filtered_unresolved)} unresolved SKU row(s) found.** "
                "Review these rows before trusting the dashboard as a planning source of truth.",
                icon="⚠️",
            )
            display_df = filtered_unresolved.copy()
            display_df["Week"] = display_df.apply(
                lambda record: format_week_label(int(record["year"]), int(record["week_iso"])),
                axis=1,
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
                width="stretch",
                hide_index=True,
            )

    st.markdown(
        "<div class='dash-footer'>"
        "Agri-AI · Pilot control tower · Decision support before inventory exists"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
