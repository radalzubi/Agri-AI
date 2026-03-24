"""SKU normalization logic for Agri-AI order history."""

from __future__ import annotations

from typing import Dict, List, Tuple


def normalize_orders(
    order_rows: List[Dict[str, object]],
    sku_lookup: Dict[str, str],
) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    """Normalize raw crop names and collect unresolved SKU rows."""

    normalized_orders: List[Dict[str, object]] = []
    unresolved_rows: List[Dict[str, object]] = []

    for row in order_rows:
        lookup_key = str(row["crop_raw"]).strip().lower()
        crop_canonical = sku_lookup.get(lookup_key)

        if crop_canonical is None:
            unresolved_rows.append(
                {
                    "buyer": row["buyer"],
                    "crop_raw": row["crop_raw"],
                    "quantity_lbs": row["quantity_lbs"],
                    "week_iso": row["week_iso"],
                    "year": row["year"],
                    "crop_canonical": "UNRESOLVED",
                }
            )
            continue

        normalized_row = dict(row)
        normalized_row["crop_canonical"] = crop_canonical
        normalized_orders.append(normalized_row)

    return normalized_orders, unresolved_rows
