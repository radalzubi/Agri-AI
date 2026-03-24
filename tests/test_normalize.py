"""Tests for SKU normalization."""

from src.normalize import normalize_orders


def test_normalize_orders_maps_known_skus() -> None:
    rows = [
        {
            "buyer": "IU Health",
            "crop_raw": "Heirloom Tomato",
            "quantity_lbs": 240.0,
            "week_iso": 22,
            "year": 2025,
        }
    ]
    lookup = {"heirloom tomato": "tomato"}

    normalized_rows, unresolved_rows = normalize_orders(rows, lookup)

    assert len(normalized_rows) == 1
    assert normalized_rows[0]["crop_canonical"] == "tomato"
    assert unresolved_rows == []


def test_normalize_orders_collects_unresolved_skus() -> None:
    rows = [
        {
            "buyer": "IU Health",
            "crop_raw": "Mystery Squash",
            "quantity_lbs": 100.0,
            "week_iso": 33,
            "year": 2025,
        }
    ]

    normalized_rows, unresolved_rows = normalize_orders(rows, {})

    assert normalized_rows == []
    assert len(unresolved_rows) == 1
    assert unresolved_rows[0]["crop_canonical"] == "UNRESOLVED"
