"""Data loading and derived view models for the Agri-AI command center."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
import streamlit as st


REQUIRED_OUTPUT_FILES = {
    "gap_analysis": "gap_analysis.csv",
    "demand": "demand_by_crop_week.csv",
    "supply": "supply_by_crop_week.csv",
    "unresolved": "unresolved_skus.csv",
    "memo": "weekly_memo.txt",
}

MODULES = [
    "Control Tower",
    "Planning",
    "Demand",
    "Operations",
    "Intelligence",
    "Admin",
]

MODULE_CAPTIONS = {
    "Control Tower": "Flagship weekly decision cockpit",
    "Planning": "Commit-now, rebalance, or monitor",
    "Demand": "Crop-week demand and coverage analytics",
    "Operations": "Weekly review and handoff pack",
    "Intelligence": "Exceptions, trust, and blockers",
    "Admin": "Local tool contract and setup status",
}

ROLE_CONFIG = {
    "Supply Planner": {
        "default_module": "Control Tower",
        "headline": "Triage shortage exposure and convert it into commitment posture.",
    },
    "Aggregator Manager": {
        "default_module": "Control Tower",
        "headline": "Protect demand, rebalance surplus, and keep the season commercially stable.",
    },
    "Executive": {
        "default_module": "Control Tower",
        "headline": "Judge season health quickly and intervene only where leverage is highest.",
    },
    "Data Steward": {
        "default_module": "Intelligence",
        "headline": "Keep the planning view trustworthy by resolving blockers and stale inputs.",
    },
}

OVERAGE_WATCH_THRESHOLD = 20.0
SHORTAGE_HIGH_THRESHOLD = 25.0
SHORTAGE_CRITICAL_THRESHOLD = 50.0
FRESH_OUTPUT_HOURS = 24.0
STALE_OUTPUT_HOURS = 72.0


def normalize_risk_flag(value: object) -> bool:
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


def hours_since_modified(path: Path) -> float | None:
    if not path.exists():
        return None
    seconds = datetime.now().timestamp() - path.stat().st_mtime
    return round(seconds / 3600.0, 1)


@st.cache_data(show_spinner=False)
def load_output_bundle(output_dir_str: str) -> Tuple[Dict[str, Any], List[str]]:
    output_dir = Path(output_dir_str).expanduser()
    missing_files = [
        file_name
        for file_name in REQUIRED_OUTPUT_FILES.values()
        if not (output_dir / file_name).exists()
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


def _shortage_priority(shortage_pct: float) -> Tuple[str, int]:
    if shortage_pct >= SHORTAGE_CRITICAL_THRESHOLD:
        return "Critical", 3
    if shortage_pct >= SHORTAGE_HIGH_THRESHOLD:
        return "High", 2
    return "Review", 1


def _overage_priority(overage_pct: float) -> Tuple[str, int]:
    if overage_pct >= 50:
        return "High", 2
    return "Watch", 1


def build_shortage_queue(gap_df: pd.DataFrame) -> pd.DataFrame:
    risk_df = gap_df[gap_df["risk_flag"]].copy()
    if risk_df.empty:
        return pd.DataFrame(
            columns=[
                "priority_rank",
                "priority_label",
                "crop_canonical",
                "year",
                "week_iso",
                "week_label",
                "crop_label",
                "coverage_pct",
                "shortage_lbs",
                "recommended_action",
            ]
        )

    priorities = risk_df["shortage_pct"].map(_shortage_priority)
    risk_df["priority_label"] = priorities.map(lambda item: item[0])
    risk_df["priority_rank"] = priorities.map(lambda item: item[1])
    risk_df["week_label"] = risk_df.apply(
        lambda row: format_week_label(int(row["year"]), int(row["week_iso"])),
        axis=1,
    )
    risk_df["crop_label"] = risk_df["crop_canonical"].map(format_crop_label)
    risk_df["coverage_pct"] = (risk_df["coverage_ratio"] * 100).round(1)
    risk_df["shortage_lbs"] = risk_df["shortage_lbs"].round(1)
    risk_df["recommended_action"] = risk_df["shortage_pct"].map(
        lambda pct: (
            "Confirm grower commitment and protect exposed demand."
            if pct >= SHORTAGE_HIGH_THRESHOLD
            else "Review demand assumptions and monitor the next review window."
        )
    )

    return risk_df.sort_values(
        by=["priority_rank", "shortage_pct", "week_iso"],
        ascending=[False, False, True],
    )[
        [
            "priority_rank",
            "priority_label",
            "crop_canonical",
            "year",
            "week_iso",
            "week_label",
            "crop_label",
            "coverage_pct",
            "shortage_lbs",
            "recommended_action",
        ]
    ]


def build_overage_queue(gap_df: pd.DataFrame) -> pd.DataFrame:
    over_df = gap_df[gap_df["overage_pct"] > OVERAGE_WATCH_THRESHOLD].copy()
    if over_df.empty:
        return pd.DataFrame(
            columns=[
                "priority_rank",
                "priority_label",
                "crop_canonical",
                "year",
                "week_iso",
                "week_label",
                "crop_label",
                "coverage_pct",
                "overage_lbs",
                "recommended_action",
            ]
        )

    priorities = over_df["overage_pct"].map(_overage_priority)
    over_df["priority_label"] = priorities.map(lambda item: item[0])
    over_df["priority_rank"] = priorities.map(lambda item: item[1])
    over_df["week_label"] = over_df.apply(
        lambda row: format_week_label(int(row["year"]), int(row["week_iso"])),
        axis=1,
    )
    over_df["crop_label"] = over_df["crop_canonical"].map(format_crop_label)
    over_df["coverage_pct"] = (over_df["coverage_ratio"] * 100).round(1)
    over_df["overage_lbs"] = over_df["overage_lbs"].round(1)
    over_df["recommended_action"] = "Pull demand forward or open buyer conversations before surplus becomes expensive."

    return over_df.sort_values(
        by=["priority_rank", "overage_pct", "week_iso"],
        ascending=[False, False, True],
    )[
        [
            "priority_rank",
            "priority_label",
            "crop_canonical",
            "year",
            "week_iso",
            "week_label",
            "crop_label",
            "coverage_pct",
            "overage_lbs",
            "recommended_action",
        ]
    ]


def build_action_queue(gap_df: pd.DataFrame, unresolved_df: pd.DataFrame) -> pd.DataFrame:
    action_rows: List[Dict[str, Any]] = []

    for row in build_shortage_queue(gap_df).head(4).itertuples():
        action_rows.append(
            {
                "priority_rank": int(row.priority_rank),
                "priority_label": row.priority_label,
                "action_type": "Shortage",
                "owner": "Supply Planner",
                "crop_canonical": row.crop_canonical,
                "year": int(row.year),
                "week_iso": int(row.week_iso),
                "week_label": row.week_label,
                "crop_label": row.crop_label,
                "issue": f"{row.crop_label} is only {row.coverage_pct:.1f}% covered in {row.week_label}.",
                "recommended_action": row.recommended_action,
            }
        )

    for row in build_overage_queue(gap_df).head(2).itertuples():
        action_rows.append(
            {
                "priority_rank": int(row.priority_rank),
                "priority_label": row.priority_label,
                "action_type": "Overage",
                "owner": "Aggregator Manager",
                "crop_canonical": row.crop_canonical,
                "year": int(row.year),
                "week_iso": int(row.week_iso),
                "week_label": row.week_label,
                "crop_label": row.crop_label,
                "issue": f"{row.crop_label} is overbuilt for {row.week_label}.",
                "recommended_action": row.recommended_action,
            }
        )

    if not unresolved_df.empty:
        unresolved_sorted = unresolved_df.sort_values(by=["year", "week_iso"])
        first_row = unresolved_sorted.iloc[0]
        action_rows.insert(
            0,
            {
                "priority_rank": 2,
                "priority_label": "Review",
                "action_type": "Trust",
                "owner": "Data Steward",
                "crop_canonical": str(first_row.get("crop_canonical", "UNRESOLVED")),
                "year": int(first_row.get("year", 0)),
                "week_iso": int(first_row.get("week_iso", 0)),
                "week_label": format_week_label(
                    int(first_row.get("year", 0)),
                    int(first_row.get("week_iso", 0)),
                ),
                "crop_label": "Unresolved input",
                "issue": f"{len(unresolved_df)} unresolved SKU row(s) are still affecting the planning view.",
                "recommended_action": "Resolve unmapped crop names before treating the current review as source-of-truth.",
            },
        )

    action_df = pd.DataFrame(action_rows)
    if action_df.empty:
        return action_df
    return action_df.sort_values(
        by=["priority_rank", "action_type"],
        ascending=[False, True],
    )


def build_planning_posture(gap_df: pd.DataFrame) -> pd.DataFrame:
    commit_now = gap_df[(gap_df["risk_flag"]) & (gap_df["shortage_pct"] >= SHORTAGE_HIGH_THRESHOLD)]
    rebalance = gap_df[gap_df["overage_pct"] > OVERAGE_WATCH_THRESHOLD]
    monitor = gap_df.drop(commit_now.index.union(rebalance.index))

    posture_rows = [
        {
            "label": "Commit Now",
            "count": int(len(commit_now)),
            "pounds": round(float(commit_now["shortage_lbs"].sum()), 1),
            "tone": "red",
            "explanation": "Shortage pressure is large enough to justify immediate commitment review.",
        },
        {
            "label": "Rebalance",
            "count": int(len(rebalance)),
            "pounds": round(float(rebalance["overage_lbs"].sum()), 1),
            "tone": "amber",
            "explanation": "Expected surplus is large enough to justify demand pull-forward or plan reduction.",
        },
        {
            "label": "Monitor",
            "count": int(len(monitor)),
            "pounds": round(float(monitor["total_demand_lbs"].sum()), 1),
            "tone": "green",
            "explanation": "Coverage is healthy enough to watch rather than intervene immediately.",
        },
    ]
    return pd.DataFrame(posture_rows)


def build_crop_summary(gap_df: pd.DataFrame) -> pd.DataFrame:
    if gap_df.empty:
        return pd.DataFrame(
            columns=[
                "crop_canonical",
                "crop_label",
                "demand_lbs",
                "supply_lbs",
                "coverage_pct",
                "risk_weeks",
                "overage_weeks",
            ]
        )

    grouped = (
        gap_df.groupby("crop_canonical", dropna=False)
        .agg(
            demand_lbs=("total_demand_lbs", "sum"),
            supply_lbs=("total_supply_lbs", "sum"),
            risk_weeks=("risk_flag", "sum"),
            overage_weeks=("overage_pct", lambda values: int((values > OVERAGE_WATCH_THRESHOLD).sum())),
        )
        .reset_index()
    )
    grouped["crop_label"] = grouped["crop_canonical"].map(format_crop_label)
    grouped["coverage_pct"] = grouped.apply(
        lambda row: (float(row["supply_lbs"]) / float(row["demand_lbs"]) * 100.0)
        if float(row["demand_lbs"])
        else 0.0,
        axis=1,
    ).round(1)

    return grouped.sort_values(
        by=["risk_weeks", "demand_lbs"],
        ascending=[False, False],
    )


def build_weekly_balance(
    demand_df: pd.DataFrame,
    supply_df: pd.DataFrame,
) -> pd.DataFrame:
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
        lambda row: format_week_label(int(row["year"]), int(row["week_iso"])),
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
        lambda row: format_week_label(int(row["year"]), int(row["week_iso"])),
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
    if gap_df.empty:
        return gap_df
    heatmap_df = gap_df.copy()
    heatmap_df["crop_label"] = heatmap_df["crop_canonical"].map(format_crop_label)
    heatmap_df["week_label"] = heatmap_df.apply(
        lambda row: format_week_label(int(row["year"]), int(row["week_iso"])),
        axis=1,
    )
    heatmap_df["coverage_pct"] = (heatmap_df["coverage_ratio"] * 100).round(1)
    heatmap_df["severity"] = heatmap_df.apply(
        lambda row: (
            "Critical shortage"
            if row["risk_flag"] and float(row["shortage_pct"]) >= SHORTAGE_CRITICAL_THRESHOLD
            else "High shortage"
            if row["risk_flag"]
            else "Overage watch"
            if float(row["overage_pct"]) > OVERAGE_WATCH_THRESHOLD
            else "Healthy"
        ),
        axis=1,
    )
    return heatmap_df.sort_values(by=["year", "week_iso", "crop_label"])


def build_risk_register(gap_df: pd.DataFrame) -> pd.DataFrame:
    register_df = gap_df[(gap_df["risk_flag"]) | (gap_df["overage_pct"] > OVERAGE_WATCH_THRESHOLD)].copy()
    if register_df.empty:
        return pd.DataFrame(
            columns=[
                "priority_label",
                "issue_type",
                "crop_canonical",
                "crop_label",
                "year",
                "week_iso",
                "week_label",
                "coverage_pct",
                "shortage_lbs",
                "overage_lbs",
            ]
        )

    register_df["issue_type"] = register_df.apply(
        lambda row: "Shortage" if bool(row["risk_flag"]) else "Overage",
        axis=1,
    )
    register_df["priority_label"] = register_df.apply(
        lambda row: (
            _shortage_priority(float(row["shortage_pct"]))[0]
            if bool(row["risk_flag"])
            else _overage_priority(float(row["overage_pct"]))[0]
        ),
        axis=1,
    )
    register_df["priority_rank"] = register_df.apply(
        lambda row: (
            _shortage_priority(float(row["shortage_pct"]))[1]
            if bool(row["risk_flag"])
            else _overage_priority(float(row["overage_pct"]))[1]
        ),
        axis=1,
    )
    register_df["crop_label"] = register_df["crop_canonical"].map(format_crop_label)
    register_df["week_label"] = register_df.apply(
        lambda row: format_week_label(int(row["year"]), int(row["week_iso"])),
        axis=1,
    )
    register_df["coverage_pct"] = (register_df["coverage_ratio"] * 100).round(1)
    register_df["shortage_lbs"] = register_df["shortage_lbs"].round(1)
    register_df["overage_lbs"] = register_df["overage_lbs"].round(1)

    return register_df.sort_values(
        by=["priority_rank", "issue_type", "week_iso"],
        ascending=[False, True, True],
    )


def build_output_status_table(output_dir: Path) -> pd.DataFrame:
    rows = []
    for file_name in REQUIRED_OUTPUT_FILES.values():
        path = output_dir / file_name
        rows.append(
            {
                "file_name": file_name,
                "status": "Ready" if path.exists() else "Missing",
                "last_updated": modified_at_str(path) if path.exists() else "Not found",
            }
        )
    return pd.DataFrame(rows)


def parse_memo_sections(memo_text: str) -> Dict[str, List[str]]:
    sections: Dict[str, List[str]] = {}
    current_section = "Summary"
    for raw_line in memo_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("--- ") and line.endswith(" ---"):
            current_section = line.strip("- ").strip()
            sections.setdefault(current_section, [])
            continue
        sections.setdefault(current_section, []).append(line)
    return sections


def build_memo_highlights(memo_sections: Dict[str, List[str]]) -> List[str]:
    highlights: List[str] = []
    section_limits = {
        "HIGH RISK: FULL SEASON": 2,
        "RECOMMENDED ACTIONS": 2,
        "DATA QUALITY ISSUES": 1,
        "UNRESOLVED SKUS": 1,
    }
    for section_name, limit in section_limits.items():
        for item in memo_sections.get(section_name, [])[:limit]:
            if item not in highlights:
                highlights.append(item)
    return highlights[:5]


def build_data_confidence(output_dir: Path, unresolved_df: pd.DataFrame) -> Dict[str, Any]:
    gap_path = output_dir / REQUIRED_OUTPUT_FILES["gap_analysis"]
    age_hours = hours_since_modified(gap_path)
    if age_hours is None:
        freshness_label = "Missing"
        freshness_tone = "red"
    elif age_hours <= FRESH_OUTPUT_HOURS:
        freshness_label = "Fresh"
        freshness_tone = "green"
    elif age_hours <= STALE_OUTPUT_HOURS:
        freshness_label = "Aging"
        freshness_tone = "amber"
    else:
        freshness_label = "Stale"
        freshness_tone = "red"

    unresolved_count = int(len(unresolved_df.index))
    affected_weeks = (
        sorted(
            {
                format_week_label(int(row.year), int(row.week_iso))
                for row in unresolved_df.itertuples()
            }
        )
        if not unresolved_df.empty
        else []
    )
    trust_blockers = unresolved_count + (1 if freshness_label in {"Missing", "Stale"} else 0)

    if unresolved_count > 0:
        state_label = "Needs review"
        state_tone = "amber"
        summary = f"{unresolved_count} unresolved SKU row(s) still affect the current view."
    elif freshness_label in {"Missing", "Stale"}:
        state_label = "Stale output"
        state_tone = "red"
        summary = "The current review is running on stale output and should be refreshed."
    else:
        state_label = "Ready"
        state_tone = "green"
        summary = "Current output is fresh enough to support planning review."

    return {
        "state_label": state_label,
        "state_tone": state_tone,
        "summary": summary,
        "freshness_label": freshness_label,
        "freshness_tone": freshness_tone,
        "age_hours": age_hours,
        "unresolved_count": unresolved_count,
        "affected_weeks": affected_weeks,
        "trust_blockers": trust_blockers,
    }


def choose_default_focus(gap_df: pd.DataFrame) -> Tuple[str, int, int] | None:
    if gap_df.empty:
        return None
    if bool(gap_df["risk_flag"].any()):
        first_row = gap_df[gap_df["risk_flag"]].sort_values(
            by=["shortage_pct", "week_iso"],
            ascending=[False, True],
        ).iloc[0]
    elif bool((gap_df["overage_pct"] > OVERAGE_WATCH_THRESHOLD).any()):
        first_row = gap_df[gap_df["overage_pct"] > OVERAGE_WATCH_THRESHOLD].sort_values(
            by=["overage_pct", "week_iso"],
            ascending=[False, True],
        ).iloc[0]
    else:
        first_row = gap_df.sort_values(by=["year", "week_iso"]).iloc[0]
    return (
        str(first_row["crop_canonical"]),
        int(first_row["year"]),
        int(first_row["week_iso"]),
    )


def focus_exists(gap_df: pd.DataFrame, crop: str, year: int, week_iso: int) -> bool:
    if gap_df.empty:
        return False
    mask = (
        (gap_df["crop_canonical"] == crop)
        & (gap_df["year"] == year)
        & (gap_df["week_iso"] == week_iso)
    )
    return bool(mask.any())


def build_focus_detail(
    gap_df: pd.DataFrame,
    crop: str | None,
    year: int | None,
    week_iso: int | None,
) -> Dict[str, Any] | None:
    if gap_df.empty or crop is None or year is None or week_iso is None:
        return None
    focus_df = gap_df[
        (gap_df["crop_canonical"] == crop)
        & (gap_df["year"] == year)
        & (gap_df["week_iso"] == week_iso)
    ]
    if focus_df.empty:
        return None

    row = focus_df.iloc[0]
    if bool(row["risk_flag"]):
        tone = "red"
        issue_label = "Shortage pressure"
        recommendation = "Protect demand and confirm grower commitment immediately."
    elif float(row["overage_pct"]) > OVERAGE_WATCH_THRESHOLD:
        tone = "amber"
        issue_label = "Overage watch"
        recommendation = "Pull demand forward or reduce expected commitment before surplus becomes expensive."
    else:
        tone = "green"
        issue_label = "Healthy coverage"
        recommendation = "Monitor this crop-week and keep the current posture."

    return {
        "crop_canonical": crop,
        "crop_label": format_crop_label(crop),
        "year": year,
        "week_iso": week_iso,
        "week_label": format_week_label(year, week_iso),
        "coverage_pct": round(float(row["coverage_ratio"]) * 100, 1),
        "demand_lbs": round(float(row["total_demand_lbs"]), 1),
        "supply_lbs": round(float(row["total_supply_lbs"]), 1),
        "shortage_lbs": round(float(row["shortage_lbs"]), 1),
        "overage_lbs": round(float(row["overage_lbs"]), 1),
        "issue_label": issue_label,
        "tone": tone,
        "recommendation": recommendation,
    }


def build_crop_week_table(gap_df: pd.DataFrame, crop: str | None) -> pd.DataFrame:
    if gap_df.empty or crop is None:
        return pd.DataFrame(
            columns=[
                "week_label",
                "demand_lbs",
                "supply_lbs",
                "coverage_pct",
                "shortage_lbs",
                "overage_lbs",
            ]
        )
    crop_df = gap_df[gap_df["crop_canonical"] == crop].copy()
    if crop_df.empty:
        return crop_df

    crop_df["week_label"] = crop_df.apply(
        lambda row: format_week_label(int(row["year"]), int(row["week_iso"])),
        axis=1,
    )
    crop_df["coverage_pct"] = (crop_df["coverage_ratio"] * 100).round(1)
    crop_df["demand_lbs"] = crop_df["total_demand_lbs"].round(1)
    crop_df["supply_lbs"] = crop_df["total_supply_lbs"].round(1)
    crop_df["shortage_lbs"] = crop_df["shortage_lbs"].round(1)
    crop_df["overage_lbs"] = crop_df["overage_lbs"].round(1)
    return crop_df.sort_values(by=["year", "week_iso"])


def build_context(
    bundle: Dict[str, Any],
    output_dir: Path,
    years: List[int],
    crops: List[str],
    week_range: Tuple[int, int],
) -> Dict[str, Any]:
    filtered_gap = apply_filters_to_frame(bundle["gap_df"], years, crops, week_range)
    filtered_demand = apply_filters_to_frame(bundle["demand_df"], years, crops, week_range)
    filtered_supply = apply_filters_to_frame(bundle["supply_df"], years, crops, week_range)
    filtered_unresolved = apply_filters_to_frame(bundle["unresolved_df"], years, [], week_range)

    total_demand = float(filtered_gap["total_demand_lbs"].sum()) if not filtered_gap.empty else 0.0
    total_supply = float(filtered_gap["total_supply_lbs"].sum()) if not filtered_gap.empty else 0.0
    weighted_coverage = (total_supply / total_demand * 100.0) if total_demand else 0.0

    confidence = build_data_confidence(output_dir, filtered_unresolved)
    shortage_queue = build_shortage_queue(filtered_gap)
    overage_queue = build_overage_queue(filtered_gap)

    context = {
        "filtered_gap": filtered_gap,
        "filtered_demand": filtered_demand,
        "filtered_supply": filtered_supply,
        "filtered_unresolved": filtered_unresolved,
        "memo_text": bundle["memo_text"],
        "memo_sections": parse_memo_sections(bundle["memo_text"]),
        "shortage_queue": shortage_queue,
        "overage_queue": overage_queue,
        "action_queue": build_action_queue(filtered_gap, filtered_unresolved),
        "planning_posture": build_planning_posture(filtered_gap),
        "crop_summary": build_crop_summary(filtered_gap),
        "weekly_balance": build_weekly_balance(filtered_demand, filtered_supply),
        "heatmap_df": build_coverage_heatmap(filtered_gap),
        "risk_register": build_risk_register(filtered_gap),
        "output_status": build_output_status_table(output_dir),
        "confidence": confidence,
        "kpis": {
            "weighted_coverage": round(weighted_coverage, 1),
            "demand_at_risk": round(float(filtered_gap.loc[filtered_gap["risk_flag"], "shortage_lbs"].sum()), 1)
            if not filtered_gap.empty
            else 0.0,
            "overage_exposure": round(float(filtered_gap.loc[filtered_gap["overage_pct"] > OVERAGE_WATCH_THRESHOLD, "overage_lbs"].sum()), 1)
            if not filtered_gap.empty
            else 0.0,
            "risk_weeks": int(filtered_gap["risk_flag"].sum()) if not filtered_gap.empty else 0,
            "trust_blockers": int(confidence["trust_blockers"]),
        },
        "memo_highlights": build_memo_highlights(parse_memo_sections(bundle["memo_text"])),
        "available_crops": sorted(filtered_gap["crop_canonical"].dropna().unique().tolist())
        if not filtered_gap.empty
        else [],
        "default_focus": choose_default_focus(filtered_gap),
    }
    return context
