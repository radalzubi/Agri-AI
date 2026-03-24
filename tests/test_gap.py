"""Tests for gap analysis logic."""

from src.gap import build_gap_analysis


def test_gap_analysis_calculates_shortage_metrics() -> None:
    demand_rows = [
        {"crop_canonical": "tomato", "week_iso": 22, "year": 2025, "total_demand_lbs": 400.0}
    ]
    supply_rows = [
        {"crop_canonical": "tomato", "week_iso": 22, "year": 2025, "total_supply_lbs": 300.0}
    ]

    gap_rows = build_gap_analysis(demand_rows, supply_rows, coverage_threshold=0.85)

    assert gap_rows[0]["coverage_ratio"] == 0.75
    assert gap_rows[0]["shortage_lbs"] == 100.0
    assert gap_rows[0]["shortage_pct"] == 25.0
    assert gap_rows[0]["risk_flag"] is True


def test_gap_analysis_calculates_overage_metrics() -> None:
    demand_rows = [
        {
            "crop_canonical": "butternut_squash",
            "week_iso": 36,
            "year": 2025,
            "total_demand_lbs": 400.0,
        }
    ]
    supply_rows = [
        {
            "crop_canonical": "butternut_squash",
            "week_iso": 36,
            "year": 2025,
            "total_supply_lbs": 600.0,
        }
    ]

    gap_rows = build_gap_analysis(demand_rows, supply_rows, coverage_threshold=0.85)

    assert gap_rows[0]["coverage_ratio"] == 1.5
    assert gap_rows[0]["overage_lbs"] == 200.0
    assert gap_rows[0]["overage_pct"] == 33.33
    assert gap_rows[0]["risk_flag"] is False


def test_gap_analysis_handles_zero_supply() -> None:
    demand_rows = [
        {"crop_canonical": "sweet_corn", "week_iso": 24, "year": 2025, "total_demand_lbs": 300.0}
    ]

    gap_rows = build_gap_analysis(demand_rows, supply_rows=[], coverage_threshold=0.85)

    assert gap_rows[0]["coverage_ratio"] == 0.0
    assert gap_rows[0]["shortage_lbs"] == 300.0
    assert gap_rows[0]["overage_pct"] == 0.0
