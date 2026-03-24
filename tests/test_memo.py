"""Tests for weekly memo generation."""

from datetime import date

from src.memo import generate_weekly_memo


def test_generate_weekly_memo_orders_risk_rows_by_week() -> None:
    gap_rows = [
        {
            "crop_canonical": "tomato",
            "week_iso": 22,
            "year": 2025,
            "coverage_ratio": 0.7,
            "shortage_lbs": 120.0,
            "overage_lbs": 0.0,
            "shortage_pct": 30.0,
            "overage_pct": 0.0,
            "risk_flag": True,
        },
        {
            "crop_canonical": "sweet_corn",
            "week_iso": 20,
            "year": 2025,
            "coverage_ratio": 0.6,
            "shortage_lbs": 200.0,
            "overage_lbs": 0.0,
            "shortage_pct": 40.0,
            "overage_pct": 0.0,
            "risk_flag": True,
        },
    ]

    memo = generate_weekly_memo(
        gap_rows=gap_rows,
        unresolved_count=0,
        data_quality_issues=[],
        today=date(2025, 5, 10),
    )

    high_risk_section = memo.split("--- HIGH RISK: FULL SEASON ---\n", maxsplit=1)[1].split(
        "\n\n--- UPCOMING RISK (NEXT 4 WEEKS) ---",
        maxsplit=1,
    )[0]

    assert high_risk_section.index("Week 20") < high_risk_section.index("Week 22")
