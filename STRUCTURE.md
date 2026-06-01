# wg2 (Agri-AI prototype) — Folder Map

Plain-English guide to what each part of this folder is.

This is the **original Agri-AI prototype** — a Streamlit dashboard plus a small
data pipeline. It predates the `harvestmind` repo (which is the productized
successor). Kept as the early prototype / reference.

---

## The app

| File / folder | What it is |
|---|---|
| `dashboard.py` | **Streamlit dashboard entry point.** Run with `streamlit run dashboard.py`. |
| `dashboard_views.py` | The dashboard's page/view layouts. |
| `dashboard_data.py` | Data prep feeding the dashboard. |
| `config.py` | App configuration. |

## The data pipeline

| File | What it does (run order) |
|---|---|
| `src/ingest.py` | 1. Pull raw data in |
| `src/normalize.py` | 2. Clean and normalize |
| `src/aggregate.py` | 3. Aggregate to supply/demand by crop-week |
| `src/gap.py` | 4. Gap analysis (supply vs demand) |
| `src/memo.py` | 5. Generate the weekly memo |
| `src/main.py` | Orchestrates the pipeline end to end |

## Supporting

| Folder / file | What it is |
|---|---|
| `agents/` | Claude agent definitions (dashboard designer, design-system enforcer, information architect, UI/UX critic). |
| `docs/` | Project docs: `business/`, `pilot/`, `product/`, `research/`. |
| `data/` | Input data. |
| `linear/` | Linear (issue tracker) integration. |
| `prompts/` | Prompt templates. |
| `requirements.txt` | Python deps: streamlit, pandas, altair. |
| `AGENTS.md`, `README.md` | Project notes. |
| `Agri-AI Venture Feasibility Brief.pdf`, `agri-ai-brief.pdf` | Venture briefs. |
| `harvestmind.duckdb` | Small local DB (12K). |

---

## What gets generated (not in git, safe to delete)

| Item | Regenerate with |
|---|---|
| `.venv/` | `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` |
| `__pycache__/`, `.pytest_cache/` | run code / tests |
| `output/` | re-run the pipeline (archived in `_archive_cleanup_review/`) |
| `_archive_cleanup_review/` | archived old outputs — see CLEANUP_CHANGELOG.md inside |

> The virtualenv was removed in cleanup. Recreate it with the command above
> before running the dashboard or pipeline.

---

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run dashboard.py
```
