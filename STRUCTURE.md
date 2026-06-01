# wg2 (Agri-AI prototype) — Folder Map

Plain-English guide to what each part of this folder is.

This is the **original Agri-AI prototype**, the predecessor to the
`harvestmind` repo (the productized successor). The live code here is a small
data pipeline in `src/`. The old Streamlit dashboard has been **retired** and
moved to `archive/` (we no longer use Streamlit).

---

## Live code — the pipeline (`src/`)

Run order:

| File | What it does |
|---|---|
| `src/ingest.py` | 1. Load grower capacity, order history, SKU lookup |
| `src/normalize.py` | 2. Clean and normalize orders |
| `src/aggregate.py` | 3. Aggregate supply and demand by crop-week |
| `src/gap.py` | 4. Gap analysis (supply vs demand) |
| `src/memo.py` | 5. Generate the weekly memo |
| `src/main.py` | Orchestrates the pipeline (argparse CLI) |
| `config.py` | Shared config (e.g. `COVERAGE_THRESHOLD`), imported by `src/main.py` |
| `tests/` | Unit tests for each pipeline stage |

Run it:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.main --help
```

---

## Supporting

| Folder / file | What it is |
|---|---|
| `docs/` | Project docs: `business/` (incl. the two Agri-AI venture brief PDFs), `pilot/`, `product/`, `research/`. |
| `agents/` | Claude agent definitions (dashboard designer, design-system enforcer, information architect, UI/UX critic). |
| `prompts/` | Prompt templates: `claude/`, `codex/`. |
| `linear/` | Linear (issue tracker) notes. |
| `data/` | Input data. |
| `requirements.txt` | Python deps: streamlit, pandas, altair. (streamlit is only needed by the archived dashboard.) |
| `AGENTS.md`, `README.md` | Project notes. |
| `harvestmind.duckdb` | Small local DB (12K). |

---

## Archived (retired, kept for reference)

| Folder | What it is |
|---|---|
| `archive/streamlit_dashboard/` | The old Streamlit UI (`dashboard.py`, `dashboard_data.py`, `dashboard_views.py`). No longer used. Preserved in git history; not part of the live pipeline. |
| `_archive_cleanup_review/` | Old generated outputs from the cleanup pass (gitignored). See `CLEANUP_CHANGELOG.md` inside. |

---

## What gets generated (not in git, safe to delete)

| Item | Regenerate with |
|---|---|
| `.venv/` | `python3 -m venv .venv && pip install -r requirements.txt` |
| `__pycache__/`, `.pytest_cache/` | run code / tests |
| `harvestmind.duckdb` | re-run the pipeline |
