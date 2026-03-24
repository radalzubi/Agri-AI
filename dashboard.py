"""Local Streamlit dashboard for reviewing Agri-AI planning outputs."""

from __future__ import annotations

import json
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


def normalize_risk_flag(value: object) -> bool:
    """Handle bools and CSV string representations consistently."""

    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def load_output_bundle(output_dir: Path) -> Tuple[Dict[str, pd.DataFrame | str], List[str]]:
    """Load all dashboard inputs from an output directory."""

    missing_files = [
        filename for filename in REQUIRED_OUTPUT_FILES.values() if not (output_dir / filename).exists()
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
            frame["week_iso"] = pd.to_numeric(frame["week_iso"], errors="coerce").fillna(0).astype(int)
        if "year" in frame.columns:
            frame["year"] = pd.to_numeric(frame["year"], errors="coerce").fillna(0).astype(int)

    return {
        "gap_df": gap_df,
        "demand_df": demand_df,
        "supply_df": supply_df,
        "unresolved_df": unresolved_df,
        "memo_text": memo_text,
    }, []


def format_week_label(year: int, week_iso: int) -> str:
    return f"{year}-W{week_iso:02d}"


def render_missing_outputs(output_dir: Path, missing_files: List[str]) -> None:
    st.error(
        "Dashboard inputs are missing. Run the Agri-AI pipeline first, then reopen this dashboard."
    )
    st.markdown(
        "\n".join(
            [
                f"Configured output directory: `{output_dir}`",
                "",
                "Missing files:",
                *[f"- `{filename}`" for filename in missing_files],
                "",
                "Expected command:",
                "`python3 -m src.main --data-dir data --output-dir output`",
            ]
        )
    )


def render_summary_cards(gap_df: pd.DataFrame, unresolved_df: pd.DataFrame) -> None:
    total_crops = int(gap_df["crop_canonical"].nunique()) if not gap_df.empty else 0
    total_weeks = (
        int(gap_df[["year", "week_iso"]].drop_duplicates().shape[0]) if not gap_df.empty else 0
    )
    risk_count = int(gap_df["risk_flag"].sum()) if not gap_df.empty else 0
    unresolved_count = int(len(unresolved_df.index))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Crops tracked", total_crops)
    col2.metric("Weeks with data", total_weeks)
    col3.metric("Risk-flagged crop-weeks", risk_count)

    unresolved_color = "#c96a00" if unresolved_count > 0 else "#1f6f3e"
    col4.markdown(
        (
            "<div style='padding: 1rem; border: 1px solid #e5e7eb; border-radius: 0.5rem;'>"
            "<div style='font-size: 0.9rem; color: #6b7280;'>Unresolved SKUs</div>"
            f"<div style='font-size: 2rem; font-weight: 700; color: {unresolved_color};'>{unresolved_count}</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def build_risk_table(gap_df: pd.DataFrame) -> pd.DataFrame:
    table_df = gap_df.copy()
    table_df["Week"] = table_df.apply(
        lambda row: format_week_label(int(row["year"]), int(row["week_iso"])),
        axis=1,
    )
    table_df["Demand (lbs)"] = table_df["total_demand_lbs"].round(2)
    table_df["Supply (lbs)"] = table_df["total_supply_lbs"].round(2)
    table_df["Coverage %"] = (table_df["coverage_ratio"] * 100).round(1)
    table_df["Shortage (lbs)"] = table_df["shortage_lbs"].round(2)
    table_df["Overage (lbs)"] = table_df["overage_lbs"].round(2)
    table_df["Crop"] = table_df["crop_canonical"]
    table_df["Risk"] = table_df["risk_flag"].map(lambda value: "Yes" if value else "No")

    table_df = table_df.sort_values(
        by=["risk_flag", "shortage_pct", "week_iso"],
        ascending=[False, False, True],
    )

    return table_df[
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


def style_risk_column(value: object) -> str:
    if value == "Yes":
        return "background-color: #ffe3e3; color: #b00020; font-weight: 700;"
    return ""


def build_chart_data(demand_df: pd.DataFrame, supply_df: pd.DataFrame, crop_name: str) -> pd.DataFrame:
    crop_demand = demand_df[demand_df["crop_canonical"] == crop_name].copy()
    crop_supply = supply_df[supply_df["crop_canonical"] == crop_name].copy()

    chart_df = crop_demand.merge(
        crop_supply,
        on=["crop_canonical", "week_iso", "year"],
        how="outer",
    ).fillna({"total_demand_lbs": 0.0, "total_supply_lbs": 0.0})

    if chart_df.empty:
        return chart_df

    chart_df["week_label"] = chart_df.apply(
        lambda row: format_week_label(int(row["year"]), int(row["week_iso"])),
        axis=1,
    )
    chart_df = chart_df.sort_values(by=["year", "week_iso"])

    long_chart_df = chart_df.melt(
        id_vars=["week_label", "week_iso", "year"],
        value_vars=["total_demand_lbs", "total_supply_lbs"],
        var_name="series",
        value_name="pounds",
    )
    long_chart_df["series"] = long_chart_df["series"].map(
        {
            "total_demand_lbs": "Demand",
            "total_supply_lbs": "Supply",
        }
    )
    return long_chart_df


def render_copy_button(memo_text: str) -> None:
    memo_payload = json.dumps(memo_text)
    components.html(
        f"""
        <div style="margin: 0 0 0.5rem 0;">
          <button
            style="padding: 0.5rem 0.85rem; border-radius: 0.5rem; border: 1px solid #d1d5db; background: white; cursor: pointer;"
            onclick='navigator.clipboard.writeText({memo_payload}).then(() => {{
              const status = document.getElementById("copy-status");
              status.innerText = "Copied to clipboard.";
              setTimeout(() => status.innerText = "", 1500);
            }})'
          >
            Copy to clipboard
          </button>
          <span id="copy-status" style="margin-left: 0.75rem; color: #166534; font-size: 0.9rem;"></span>
        </div>
        """,
        height=48,
    )


def main() -> None:
    st.set_page_config(page_title="Agri-AI Dashboard", layout="wide")
    st.title("Agri-AI Operator Dashboard")
    st.caption("Local planning dashboard for buyer-facing agricultural operators.")

    default_output_dir = "output"
    output_dir_input = st.sidebar.text_input("Output directory", value=default_output_dir)
    output_dir = Path(output_dir_input).expanduser()

    bundle, missing_files = load_output_bundle(output_dir)
    if missing_files:
        render_missing_outputs(output_dir, missing_files)
        st.stop()

    gap_df = bundle["gap_df"]
    demand_df = bundle["demand_df"]
    supply_df = bundle["supply_df"]
    unresolved_df = bundle["unresolved_df"]
    memo_text = bundle["memo_text"]

    render_summary_cards(gap_df, unresolved_df)

    st.subheader("Risk Table")
    filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 2])

    crop_options = sorted(gap_df["crop_canonical"].dropna().unique().tolist())
    selected_crops = filter_col1.multiselect("Crop", options=crop_options, default=[])
    risk_only = filter_col2.checkbox("Show risk only", value=False)

    min_week = int(gap_df["week_iso"].min()) if not gap_df.empty else 1
    max_week = int(gap_df["week_iso"].max()) if not gap_df.empty else 52
    week_range = filter_col3.slider(
        "Week range",
        min_value=min_week,
        max_value=max_week,
        value=(min_week, max_week),
    )

    filtered_gap_df = gap_df.copy()
    if selected_crops:
        filtered_gap_df = filtered_gap_df[filtered_gap_df["crop_canonical"].isin(selected_crops)]
    if risk_only:
        filtered_gap_df = filtered_gap_df[filtered_gap_df["risk_flag"]]
    filtered_gap_df = filtered_gap_df[
        filtered_gap_df["week_iso"].between(week_range[0], week_range[1])
    ]

    risk_table_df = build_risk_table(filtered_gap_df)
    st.dataframe(
        risk_table_df.style.map(style_risk_column, subset=["Risk"]),
        width="stretch",
        hide_index=True,
    )

    st.subheader("Demand vs Supply Chart")
    if crop_options:
        chart_crop = st.selectbox("Select crop", options=crop_options, index=0)
        chart_df = build_chart_data(demand_df, supply_df, chart_crop)
        chart = (
            alt.Chart(chart_df)
            .mark_bar()
            .encode(
                x=alt.X("week_label:N", title="Week", sort=None),
                y=alt.Y("pounds:Q", title="Pounds"),
                xOffset=alt.XOffset("series:N"),
                color=alt.Color(
                    "series:N",
                    scale=alt.Scale(domain=["Demand", "Supply"], range=["#2563eb", "#16a34a"]),
                    legend=alt.Legend(title="Series"),
                ),
                tooltip=[
                    alt.Tooltip("week_label:N", title="Week"),
                    alt.Tooltip("series:N", title="Series"),
                    alt.Tooltip("pounds:Q", title="Pounds", format=".2f"),
                ],
            )
        )
        st.altair_chart(chart, width="stretch")
    else:
        st.info("No crop data available yet. Run the pipeline first.")

    st.subheader("Weekly Memo")
    render_copy_button(memo_text)
    st.text_area("Memo", value=memo_text, height=360, label_visibility="collapsed")

    if not unresolved_df.empty:
        st.subheader("Unresolved SKUs")
        st.warning(
            "Unresolved crop names were found. Review these rows before trusting all dashboard totals."
        )
        unresolved_display_df = unresolved_df.copy()
        unresolved_display_df["Week"] = unresolved_display_df.apply(
            lambda row: format_week_label(int(row["year"]), int(row["week_iso"])),
            axis=1,
        )
        st.dataframe(
            unresolved_display_df[
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


if __name__ == "__main__":
    main()
