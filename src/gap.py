"""Gap analysis and risk flagging logic."""

from __future__ import annotations

from typing import Dict, List, Tuple


def build_gap_analysis(
    demand_rows: List[Dict[str, object]],
    supply_rows: List[Dict[str, object]],
    coverage_threshold: float,
) -> List[Dict[str, object]]:
    """Build crop-week gap analysis for all demand-present rows."""

    supply_lookup: Dict[Tuple[str, int, int], float] = {
        (str(row["crop_canonical"]), int(row["week_iso"]), int(row["year"])): float(
            row["total_supply_lbs"]
        )
        for row in supply_rows
    }

    gap_rows: List[Dict[str, object]] = []

    for row in demand_rows:
        crop_canonical = str(row["crop_canonical"])
        week_iso = int(row["week_iso"])
        year = int(row["year"])
        total_demand_lbs = float(row["total_demand_lbs"])
        total_supply_lbs = supply_lookup.get((crop_canonical, week_iso, year), 0.0)

        coverage_ratio = total_supply_lbs / total_demand_lbs if total_demand_lbs else 0.0
        shortage_lbs = max(0.0, total_demand_lbs - total_supply_lbs)
        overage_lbs = max(0.0, total_supply_lbs - total_demand_lbs)
        shortage_pct = (shortage_lbs / total_demand_lbs * 100.0) if total_demand_lbs else 0.0
        overage_pct = (overage_lbs / total_supply_lbs * 100.0) if total_supply_lbs else 0.0
        risk_flag = coverage_ratio < coverage_threshold

        gap_rows.append(
            {
                "crop_canonical": crop_canonical,
                "week_iso": week_iso,
                "year": year,
                "total_demand_lbs": total_demand_lbs,
                "total_supply_lbs": total_supply_lbs,
                "coverage_ratio": round(coverage_ratio, 4),
                "shortage_lbs": round(shortage_lbs, 2),
                "overage_lbs": round(overage_lbs, 2),
                "shortage_pct": round(shortage_pct, 2),
                "overage_pct": round(overage_pct, 2),
                "risk_flag": risk_flag,
            }
        )

    return sorted(
        gap_rows,
        key=lambda row: (
            not bool(row["risk_flag"]),
            -float(row["shortage_pct"]),
            int(row["year"]),
            int(row["week_iso"]),
        ),
    )
