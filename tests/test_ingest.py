"""Tests for input loading and validation."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from src.ingest import (
    InputFileMissingError,
    load_grower_capacity,
    load_order_history,
    load_sku_lookup,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tmp_csv(tmp_path: Path, filename: str, content: str) -> Path:
    """Write a CSV string to a temp file and return its path."""
    path = tmp_path / filename
    path.write_text(textwrap.dedent(content).strip(), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# load_order_history
# ---------------------------------------------------------------------------

def test_load_order_history_raises_when_file_missing(tmp_path: Path) -> None:
    with pytest.raises(InputFileMissingError):
        load_order_history(tmp_path / "nonexistent.csv")


def test_load_order_history_raises_on_missing_column(tmp_path: Path) -> None:
    path = _tmp_csv(tmp_path, "orders.csv", """\
        buyer,crop_raw,quantity_lbs,week_iso
        IU Health,tomato,100,22
    """)
    with pytest.raises(ValueError, match="year"):
        load_order_history(path)


def test_load_order_history_skips_blank_quantity(tmp_path: Path) -> None:
    path = _tmp_csv(tmp_path, "orders.csv", """\
        buyer,crop_raw,quantity_lbs,week_iso,year
        IU Health,tomato,,22,2025
        IU Health,sweet_corn,100,22,2025
    """)
    rows = load_order_history(path)
    assert len(rows) == 1
    assert rows[0]["crop_raw"] == "sweet_corn"


def test_load_order_history_skips_blank_crop_raw(tmp_path: Path) -> None:
    path = _tmp_csv(tmp_path, "orders.csv", """\
        buyer,crop_raw,quantity_lbs,week_iso,year
        IU Health,,240,22,2025
        IU Health,tomato,100,22,2025
    """)
    rows = load_order_history(path)
    assert len(rows) == 1
    assert rows[0]["crop_raw"] == "tomato"


def test_load_order_history_collapses_exact_duplicates(tmp_path: Path) -> None:
    path = _tmp_csv(tmp_path, "orders.csv", """\
        buyer,crop_raw,quantity_lbs,week_iso,year
        IU Health,tomato,100,22,2025
        IU Health,tomato,150,22,2025
    """)
    rows = load_order_history(path)
    assert len(rows) == 1
    assert rows[0]["quantity_lbs"] == 250.0


def test_load_order_history_different_buyers_not_collapsed(tmp_path: Path) -> None:
    path = _tmp_csv(tmp_path, "orders.csv", """\
        buyer,crop_raw,quantity_lbs,week_iso,year
        IU Health,tomato,100,22,2025
        GrowLocal Hub,tomato,200,22,2025
    """)
    rows = load_order_history(path)
    assert len(rows) == 2


def test_load_order_history_skips_malformed_quantity(tmp_path: Path) -> None:
    path = _tmp_csv(tmp_path, "orders.csv", """\
        buyer,crop_raw,quantity_lbs,week_iso,year
        IU Health,tomato,not_a_number,22,2025
        IU Health,sweet_corn,100,23,2025
    """)
    rows = load_order_history(path)
    assert len(rows) == 1
    assert rows[0]["crop_raw"] == "sweet_corn"


# ---------------------------------------------------------------------------
# load_grower_capacity
# ---------------------------------------------------------------------------

def test_load_grower_capacity_raises_when_file_missing(tmp_path: Path) -> None:
    with pytest.raises(InputFileMissingError):
        load_grower_capacity(tmp_path / "nonexistent.csv")


def test_load_grower_capacity_raises_on_missing_column(tmp_path: Path) -> None:
    path = _tmp_csv(tmp_path, "capacity.csv", """\
        grower,crop_canonical,estimated_lbs,week_iso
        Heartland Farm,tomato,400,22
    """)
    with pytest.raises(ValueError, match="year"):
        load_grower_capacity(path)


def test_load_grower_capacity_loads_valid_rows(tmp_path: Path) -> None:
    path = _tmp_csv(tmp_path, "capacity.csv", """\
        grower,crop_canonical,estimated_lbs,week_iso,year
        Heartland Farm,tomato,400,22,2025
        Oak Ridge,butternut_squash,800,36,2025
    """)
    rows = load_grower_capacity(path)
    assert len(rows) == 2
    assert rows[0]["estimated_lbs"] == 400.0
    assert rows[1]["crop_canonical"] == "butternut_squash"


def test_load_grower_capacity_skips_malformed_row(tmp_path: Path) -> None:
    path = _tmp_csv(tmp_path, "capacity.csv", """\
        grower,crop_canonical,estimated_lbs,week_iso,year
        Heartland Farm,tomato,bad_value,22,2025
        Heartland Farm,sweet_corn,200,23,2025
    """)
    rows = load_grower_capacity(path)
    assert len(rows) == 1
    assert rows[0]["crop_canonical"] == "sweet_corn"


# ---------------------------------------------------------------------------
# load_sku_lookup
# ---------------------------------------------------------------------------

def test_load_sku_lookup_raises_when_file_missing(tmp_path: Path) -> None:
    with pytest.raises(InputFileMissingError):
        load_sku_lookup(tmp_path / "nonexistent.csv")


def test_load_sku_lookup_raises_on_missing_column(tmp_path: Path) -> None:
    path = _tmp_csv(tmp_path, "sku.csv", """\
        crop_raw
        Heirloom Tomato
    """)
    with pytest.raises(ValueError, match="crop_canonical"):
        load_sku_lookup(path)


def test_load_sku_lookup_normalizes_keys_to_lowercase(tmp_path: Path) -> None:
    path = _tmp_csv(tmp_path, "sku.csv", """\
        crop_raw,crop_canonical
        Heirloom Tomato,tomato
        SWEET CORN,sweet_corn
    """)
    lookup = load_sku_lookup(path)
    assert lookup["heirloom tomato"] == "tomato"
    assert lookup["sweet corn"] == "sweet_corn"


def test_load_sku_lookup_skips_blank_rows(tmp_path: Path) -> None:
    path = _tmp_csv(tmp_path, "sku.csv", """\
        crop_raw,crop_canonical
        Heirloom Tomato,tomato
        ,
        Butternut Squash,butternut_squash
    """)
    lookup = load_sku_lookup(path)
    assert len(lookup) == 2
