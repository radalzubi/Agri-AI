"""Tests for demand and supply aggregation."""

from src.aggregate import aggregate_demand, aggregate_supply


def test_aggregate_demand_sums_duplicate_rows() -> None:
    rows = [
        {"crop_canonical": "tomato", "quantity_lbs": 100.0, "week_iso": 22, "year": 2025},
        {"crop_canonical": "tomato", "quantity_lbs": 150.0, "week_iso": 22, "year": 2025},
        {"crop_canonical": "tomato", "quantity_lbs": 90.0, "week_iso": 23, "year": 2025},
    ]

    aggregated = aggregate_demand(rows)

    assert aggregated == [
        {"crop_canonical": "tomato", "week_iso": 22, "year": 2025, "total_demand_lbs": 250.0},
        {"crop_canonical": "tomato", "week_iso": 23, "year": 2025, "total_demand_lbs": 90.0},
    ]


def test_aggregate_supply_keeps_weeks_with_data_only() -> None:
    rows = [
        {"crop_canonical": "sweet_corn", "estimated_lbs": 300.0, "week_iso": 24, "year": 2025},
        {"crop_canonical": "sweet_corn", "estimated_lbs": 200.0, "week_iso": 24, "year": 2025},
    ]

    aggregated = aggregate_supply(rows)

    assert aggregated == [
        {
            "crop_canonical": "sweet_corn",
            "week_iso": 24,
            "year": 2025,
            "total_supply_lbs": 500.0,
        }
    ]
