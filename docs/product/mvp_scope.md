# MVP Scope

## Status

Phase 1 pipeline complete. A working Python CSV-in / report-out pipeline exists in `src/`.

Built:
- `src/ingest.py` — load and validate CSV inputs, collapse duplicates
- `src/normalize.py` — SKU normalization via lookup table
- `src/aggregate.py` — demand and supply aggregation by crop and week
- `src/gap.py` — coverage ratio, shortage/overage math, risk flagging
- `src/memo.py` — operator-facing plain-text weekly planning memo
- `src/main.py` — CLI entry point orchestrating the full pipeline

Outputs: `gap_analysis.csv`, `demand_by_crop_week.csv`, `supply_by_crop_week.csv`, `unresolved_skus.csv`, `weekly_memo.txt`

Run: `python3 -m src.main --data-dir data --output-dir output`

Next phase: local operator dashboard (Streamlit or lightweight web UI) on top of this pipeline.

---

## MVP Goal

Build the smallest useful planning product for an operator managing buyer demand and grower commitments before the season is locked.

## Must-Have Features

- import historical demand data
- normalize crop and SKU names
- show demand by crop and week
- show expected grower capacity by crop and week
- flag shortage and overage risk
- generate operator-facing recommendations

## Manual Or Operational Parts That Can Happen Before Software

These can remain manual during early pilots:

- data cleanup
- grower outreach
- buyer follow-up
- weather interpretation
- weekly recommendation writing
- spreadsheet-based scenario analysis

## What Should Not Be Built Yet

- full farm management suite
- inventory system
- warehouse workflows
- route planning
- buyer marketplace
- lending products
- mobile app
- general-purpose AI assistant

## AI vs Non-AI Early On

### Non-AI first

- spreadsheet logic
- crop calendars
- rule-based shortage and overage flags
- weekly planning dashboards
- operator workflow templates

### AI where useful later

- messy SKU normalization
- note summarization
- anomaly detection
- probabilistic forecasting once enough clean data exists

Early-stage rule:

do not use AI where simple logic and operator judgment are enough to prove value.
