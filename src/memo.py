"""Plain-text weekly planning memo generation."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Dict, List, Set, Tuple


def _next_four_weeks(today: date) -> Set[Tuple[int, int]]:
    weeks: Set[Tuple[int, int]] = set()
    for offset in range(28):
        current_day = today + timedelta(days=offset)
        iso_year, iso_week, _ = current_day.isocalendar()
        weeks.add((iso_year, iso_week))
    return weeks


def _format_risk_line(row: Dict[str, object]) -> str:
    return (
        f"  Week {row['week_iso']}: {row['crop_canonical']} — "
        f"{round(float(row['coverage_ratio']) * 100)}% covered "
        f"(shortage: {round(float(row['shortage_lbs']), 2)} lbs)"
    )


def _sort_by_week(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    return sorted(rows, key=lambda row: (int(row["year"]), int(row["week_iso"])))


def _build_recommendation(row: Dict[str, object]) -> str | None:
    # Only generate recommendations for risk-flagged rows to avoid false signals.
    if not bool(row["risk_flag"]):
        return None

    crop_canonical = str(row["crop_canonical"])
    week_iso = row["week_iso"]
    shortage_pct = float(row["shortage_pct"])
    overage_pct = float(row["overage_pct"])

    if shortage_pct > 30:
        return f"  {crop_canonical} (Week {week_iso}): contact growers to confirm capacity and planting commitment"
    if overage_pct > 25:
        return f"  {crop_canonical} (Week {week_iso}): start buyer conversation to move expected overage"
    return None


def generate_weekly_memo(
    gap_rows: List[Dict[str, object]],
    unresolved_count: int,
    data_quality_issues: List[str],
    today: date | None = None,
) -> str:
    current_day = today or date.today()
    current_year = max((int(row["year"]) for row in gap_rows), default=current_day.year)
    next_four_week_set = _next_four_weeks(current_day)

    risk_rows = _sort_by_week([row for row in gap_rows if bool(row["risk_flag"])])
    upcoming_risk_rows = [
        row
        for row in risk_rows
        if (int(row["year"]), int(row["week_iso"])) in next_four_week_set
    ]
    overage_rows = [row for row in gap_rows if float(row["overage_pct"]) > 20]
    recommendations = [
        recommendation
        for recommendation in (_build_recommendation(row) for row in gap_rows)
        if recommendation is not None
    ]

    lines = [
        "AGRI-AI WEEKLY PLANNING MEMO",
        f"Season: {current_year}  |  Generated: {current_day.isoformat()}",
        "",
        "--- HIGH RISK: FULL SEASON ---",
    ]

    lines.extend([_format_risk_line(row) for row in risk_rows] or ["  None"])
    lines.extend(["", "--- UPCOMING RISK (NEXT 4 WEEKS) ---"])
    lines.extend([_format_risk_line(row) for row in upcoming_risk_rows] or ["  None"])
    lines.extend(["", "--- OVERAGES TO WATCH ---"])

    if overage_rows:
        for row in sorted(overage_rows, key=lambda item: -float(item["overage_pct"])):
            lines.append(
                f"  Week {row['week_iso']}: {row['crop_canonical']} — "
                f"{round(float(row['coverage_ratio']) * 100)}% covered "
                f"(overage: {round(float(row['overage_lbs']), 2)} lbs)"
            )
    else:
        lines.append("  None")

    lines.extend(["", "--- UNRESOLVED SKUS ---"])
    lines.append(
        f"  {unresolved_count} unresolved SKU row(s). Review unresolved_skus.csv before trusting all totals."
    )

    if data_quality_issues:
        lines.extend(["", "--- DATA QUALITY ISSUES ---"])
        lines.extend([f"  - {issue}" for issue in data_quality_issues])

    lines.extend(["", "--- RECOMMENDED ACTIONS ---"])
    lines.extend(recommendations or ["  None"])

    return "\n".join(lines) + "\n"
