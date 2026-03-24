"""Input loading and validation for the Agri-AI MVP pipeline."""

from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import Dict, List


logger = logging.getLogger(__name__)


class InputFileMissingError(FileNotFoundError):
    """Raised when a required input file is missing."""


def ensure_file_exists(path: Path) -> None:
    if not path.exists():
        raise InputFileMissingError(
            f"Missing required input file: {path}. "
            f"Add the file and rerun the pipeline."
        )


def validate_columns(fieldnames: List[str] | None, required_columns: List[str], path: Path) -> None:
    if fieldnames is None:
        raise ValueError(f"Input file has no header row: {path}")

    missing_columns = [column for column in required_columns if column not in fieldnames]
    if missing_columns:
        raise ValueError(
            f"Input file {path} is missing required columns: {', '.join(missing_columns)}"
        )


def _is_blank(value: object) -> bool:
    return value is None or str(value).strip() == ""


def load_order_history(path: Path) -> List[Dict[str, object]]:
    """Load order history and collapse exact duplicates by buyer/raw crop/week/year."""

    ensure_file_exists(path)
    required_columns = ["buyer", "crop_raw", "quantity_lbs", "week_iso", "year"]

    collapsed_rows: Dict[tuple[str, str, int, int], Dict[str, object]] = {}

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        validate_columns(reader.fieldnames, required_columns, path)

        for row_number, row in enumerate(reader, start=2):
            if _is_blank(row.get("crop_raw")) or _is_blank(row.get("quantity_lbs")):
                logger.warning(
                    "Skipping order row %s in %s: missing crop_raw or quantity_lbs",
                    row_number,
                    path,
                )
                continue

            try:
                buyer = str(row["buyer"]).strip()
                crop_raw = str(row["crop_raw"]).strip()
                quantity_lbs = float(row["quantity_lbs"])
                week_iso = int(row["week_iso"])
                year = int(row["year"])
            except (TypeError, ValueError) as error:
                logger.warning(
                    "Skipping order row %s in %s: %s",
                    row_number,
                    path,
                    error,
                )
                continue

            key = (buyer, crop_raw, week_iso, year)
            if key not in collapsed_rows:
                collapsed_rows[key] = {
                    "buyer": buyer,
                    "crop_raw": crop_raw,
                    "quantity_lbs": quantity_lbs,
                    "week_iso": week_iso,
                    "year": year,
                }
            else:
                collapsed_rows[key]["quantity_lbs"] = float(collapsed_rows[key]["quantity_lbs"]) + quantity_lbs

    return list(collapsed_rows.values())


def load_grower_capacity(path: Path) -> List[Dict[str, object]]:
    """Load grower capacity rows with basic type validation."""

    ensure_file_exists(path)
    required_columns = ["grower", "crop_canonical", "estimated_lbs", "week_iso", "year"]

    cleaned_rows: List[Dict[str, object]] = []

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        validate_columns(reader.fieldnames, required_columns, path)

        for row_number, row in enumerate(reader, start=2):
            try:
                cleaned_rows.append(
                    {
                        "grower": str(row["grower"]).strip(),
                        "crop_canonical": str(row["crop_canonical"]).strip(),
                        "estimated_lbs": float(row["estimated_lbs"]),
                        "week_iso": int(row["week_iso"]),
                        "year": int(row["year"]),
                    }
                )
            except (TypeError, ValueError) as error:
                logger.warning(
                    "Skipping grower capacity row %s in %s: %s",
                    row_number,
                    path,
                    error,
                )

    return cleaned_rows


def load_sku_lookup(path: Path) -> Dict[str, str]:
    """Load SKU normalization lookup keyed by cleaned raw crop value."""

    ensure_file_exists(path)
    required_columns = ["crop_raw", "crop_canonical"]

    lookup: Dict[str, str] = {}

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        validate_columns(reader.fieldnames, required_columns, path)

        for row_number, row in enumerate(reader, start=2):
            crop_raw = row.get("crop_raw")
            crop_canonical = row.get("crop_canonical")

            if _is_blank(crop_raw) or _is_blank(crop_canonical):
                logger.warning(
                    "Skipping SKU lookup row %s in %s: missing crop_raw or crop_canonical",
                    row_number,
                    path,
                )
                continue

            lookup[str(crop_raw).strip().lower()] = str(crop_canonical).strip()

    return lookup
