# wg2 (Agri-AI prototype) — Folder Map

The original Agri-AI prototype, predecessor to the `harvestmind` repo. The live
code is a small data pipeline in `src/`. The old Streamlit dashboard has been
retired to `archive/`.

## Root (kept minimal)

| Item | What it is |
|---|---|
| `README.md`, `AGENTS.md`, `STRUCTURE.md` | Project notes + this map. |
| `requirements.txt` | Python deps (streamlit only needed by the archived dashboard). |
| `harvestmind.duckdb` | Small local DB (gitignored). |

## The 6 folders

| Folder | What's inside |
|---|---|
| `src/` | **The live pipeline + config.** Run order: `ingest` → `normalize` → `aggregate` → `gap` → `memo`, orchestrated by `main.py`. `config.py` holds shared settings (e.g. `COVERAGE_THRESHOLD`). |
| `tests/` | Unit tests for each pipeline stage. |
| `docs/` | Project docs: `business/` (incl. the 2 Agri-AI venture brief PDFs), `pilot/`, `product/`, `research/`. |
| `data/` | Input data location for the pipeline. |
| `workspace/` | AI tooling and notes: `agents/` (agent definitions), `prompts/` (claude + codex prompt templates), `linear/` (issue-tracker notes). |
| `archive/` | Retired material: `streamlit_dashboard/` (old UI, no longer used), `old_pipeline_outputs/` (gitignored generated outputs), and `CLEANUP_CHANGELOG.md`. |

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.main --help
python -m pytest        # 23 tests
```

## Generated (not in git)

`.venv/`, `__pycache__/`, `.pytest_cache/`, `harvestmind.duckdb`,
`archive/old_pipeline_outputs/` — all regenerable.
