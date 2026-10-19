# Agri-AI

Agri-AI is an agricultural supply planning venture focused on one narrow problem:
helping buyer-facing agricultural operators decide what to produce, when to produce it, and how much to commit before inventory exists.

## Problem

Specialty-crop supply chains break before harvest.

Buyer demand is uneven.
Grower commitments are made with incomplete information.
Aggregators absorb the mismatch through shortages, emergency buys, substitutions, and waste.

Most current tools handle inventory, ordering, or farm operations after supply is already in motion.
Agri-AI is focused earlier than that:
pre-season and in-season production planning.

## Who It Is For

Primary target:

- regional food hubs
- specialty produce aggregators
- buyer-facing produce distributors
- local sourcing operators coordinating multiple growers for recurring buyers

Secondary users:

- growers participating in those supply networks
- planning and procurement operators managing buyer demand, grower capacity, and seasonal supply risk

## What Makes It Different

Agri-AI is not a generic ERP, warehouse system, or post-harvest traceability tool.

It is a planning layer that helps operators answer:

- what should be grown
- how much should be committed
- when the commitment should happen
- where shortage and overage risk will appear

## System Of Work

This repository is the source of truth for venture work.

- GitHub = source of truth for business docs, research, strategy, product scope, and prompts
- Linear = task coordination and execution tracking
- Codex = builder, reviewer, document structurer, and repo maintainer
- Claude = researcher, refiner, issue executor, and synthesis engine

## Running the MVP

The MVP is a Python CSV-in / report-out planning pipeline (`src/`) with a local Streamlit dashboard on top of its outputs. It needs Python 3.12 or newer (CI runs 3.12 and 3.14).

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt pytest
```

1. Put three CSV files in `data/` (git ignores everything in it except `.gitkeep`, so buyer and grower data stays local):

   | File | Required columns |
   | --- | --- |
   | `order_history.csv` | `buyer`, `crop_raw`, `quantity_lbs`, `week_iso`, `year` |
   | `grower_capacity.csv` | `grower`, `crop_canonical`, `estimated_lbs`, `week_iso`, `year` |
   | `sku_lookup.csv` | `crop_raw`, `crop_canonical` (maps buyer SKU names to canonical crops) |

2. Run the pipeline:

   ```bash
   python3 -m src.main --data-dir data --output-dir output
   ```

   It writes `demand_by_crop_week.csv`, `supply_by_crop_week.csv`, `gap_analysis.csv`, `unresolved_skus.csv` and `weekly_memo.txt` to `output/` (gitignored). Rows below a coverage ratio of 0.85 (`COVERAGE_THRESHOLD` in `config.py`) are flagged as risk; override it with `--coverage-threshold`.

3. Open the dashboard and point the sidebar's "Output directory" at the pipeline output (it defaults to `output`):

   ```bash
   streamlit run dashboard.py
   ```

4. Run the tests: `python -m pytest`. The suite covers each pipeline stage, plus a smoke test that runs the CLI on a small dataset and renders every dashboard module.

## Repository Layout

- `src/` the planning pipeline: ingest, normalize, aggregate, gap analysis, weekly memo, and the `main.py` CLI
- `dashboard.py`, `dashboard_data.py`, `dashboard_views.py` the Streamlit command center
- `config.py` pipeline settings (coverage threshold)
- `tests/` pytest suite
- `data/` local pipeline inputs (not committed)
- `docs/business/` venture framing, economics, GTM, and operating direction
- `docs/research/` market notes, competitor analysis, and validation findings
- `docs/pilot/` pilot design and execution planning
- `docs/product/` MVP boundaries and product decisions
- `prompts/claude/` reusable execution prompts for Claude
- `prompts/codex/` reusable review and repo-structuring prompts for Codex
- `linear/` Linear workflow and board structure

## Working Principle

Keep the company thesis sharp and the repo clean.

- prefer execution-ready docs over long essays
- validate with manual workflows before building software
- avoid bloated AI claims early
- keep all strategy tied to a real customer wedge
