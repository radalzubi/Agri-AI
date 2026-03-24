"""Demand and supply aggregation logic."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple


def _sorted_rows(grouped_data: Dict[Tuple[str, int, int], float], value_field: str) -> List[Dict[str, object]]:
    sorted_keys = sorted(grouped_data.keys(), key=lambda key: (key[2], key[1], key[0]))
    rows: List[Dict[str, object]] = []
    for crop_canonical, week_iso, year in sorted_keys:
        rows.append(
            {
                "crop_canonical": crop_canonical,
                "week_iso": week_iso,
                "year": year,
                value_field: grouped_data[(crop_canonical, week_iso, year)],
            }
        )
    return rows


def aggregate_demand(order_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped_data: Dict[Tuple[str, int, int], float] = defaultdict(float)

    for row in order_rows:
        key = (str(row["crop_canonical"]), int(row["week_iso"]), int(row["year"]))
        grouped_data[key] += float(row["quantity_lbs"])

    return _sorted_rows(grouped_data, "total_demand_lbs")


def aggregate_supply(capacity_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped_data: Dict[Tuple[str, int, int], float] = defaultdict(float)

    for row in capacity_rows:
        key = (str(row["crop_canonical"]), int(row["week_iso"]), int(row["year"]))
        grouped_data[key] += float(row["estimated_lbs"])

    return _sorted_rows(grouped_data, "total_supply_lbs")
