"""Entry point for the Agri-AI MVP CSV-in / report-out pipeline."""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path
from typing import Dict, Iterable, List

from config import COVERAGE_THRESHOLD
from src.aggregate import aggregate_demand, aggregate_supply
from src.gap import build_gap_analysis
from src.ingest import InputFileMissingError, load_grower_capacity, load_order_history, load_sku_lookup
from src.memo import generate_weekly_memo
from src.normalize import normalize_orders


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Agri-AI planning pipeline.")
    parser.add_argument("--data-dir", default="data", help="Directory containing CSV inputs.")
    parser.add_argument("--output-dir", default="output", help="Directory to write outputs.")
    parser.add_argument(
        "--coverage-threshold",
        type=float,
        default=COVERAGE_THRESHOLD,
        help="Coverage ratio threshold below which a row is flagged as risk.",
    )
    return parser.parse_args()


def write_csv(path: Path, rows: Iterable[Dict[str, object]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def collect_data_quality_issues(unresolved_rows: List[Dict[str, object]]) -> List[str]:
    issues: List[str] = []
    if unresolved_rows:
        unique_skus = sorted({str(row["crop_raw"]) for row in unresolved_rows})
        issues.append(
            f"{len(unique_skus)} unresolved SKU name(s) found: {', '.join(unique_skus[:5])}"
            + (" ..." if len(unique_skus) > 5 else "")
        )
    return issues


def run_pipeline(args: argparse.Namespace) -> int:
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)

    try:
        order_rows = load_order_history(data_dir / "order_history.csv")
        capacity_rows = load_grower_capacity(data_dir / "grower_capacity.csv")
        sku_lookup = load_sku_lookup(data_dir / "sku_lookup.csv")
    except (InputFileMissingError, ValueError) as error:
        logger.error("%s", error)
        return 1

    normalized_orders, unresolved_rows = normalize_orders(order_rows, sku_lookup)
    demand_by_crop_week = aggregate_demand(normalized_orders)
    supply_by_crop_week = aggregate_supply(capacity_rows)
    gap_analysis = build_gap_analysis(
        demand_by_crop_week,
        supply_by_crop_week,
        coverage_threshold=args.coverage_threshold,
    )

    write_csv(
        output_dir / "demand_by_crop_week.csv",
        demand_by_crop_week,
        ["crop_canonical", "week_iso", "year", "total_demand_lbs"],
    )
    write_csv(
        output_dir / "supply_by_crop_week.csv",
        supply_by_crop_week,
        ["crop_canonical", "week_iso", "year", "total_supply_lbs"],
    )
    write_csv(
        output_dir / "gap_analysis.csv",
        gap_analysis,
        [
            "crop_canonical",
            "week_iso",
            "year",
            "total_demand_lbs",
            "total_supply_lbs",
            "coverage_ratio",
            "shortage_lbs",
            "overage_lbs",
            "shortage_pct",
            "overage_pct",
            "risk_flag",
        ],
    )
    write_csv(
        output_dir / "unresolved_skus.csv",
        unresolved_rows,
        ["buyer", "crop_raw", "quantity_lbs", "week_iso", "year", "crop_canonical"],
    )

    memo_text = generate_weekly_memo(
        gap_rows=gap_analysis,
        unresolved_count=len(unresolved_rows),
        data_quality_issues=collect_data_quality_issues(unresolved_rows),
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "weekly_memo.txt").write_text(memo_text, encoding="utf-8")

    logger.info("Pipeline complete. Outputs written to %s", output_dir)
    return 0


def main() -> int:
    return run_pipeline(parse_args())


if __name__ == "__main__":
    sys.exit(main())
