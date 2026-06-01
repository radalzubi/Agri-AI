# Cleanup Changelog — wg2

Date: 2026-06-01
Scope: the `wg2/` folder (the Agri-AI prototype, this session's working dir).
No working code moved or renamed. `.claude/` and `.git/` were not touched.

Result: folder shrank from **355M to 2.5M**.

---

## Deleted (regenerable, safe)

| Item | Size | How to restore |
|---|---|---|
| `.venv/` | 352M | `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` |
| `__pycache__/` (3 dirs) | ~108K | regenerate on next run |
| `.pytest_cache/` | ~20K | regenerate on next `pytest` |
| `.DS_Store` (incl. ones inside .venv) | small | macOS recreates |

> The virtualenv must be recreated (command above) before running the
> Streamlit dashboard or the pipeline. requirements.txt (streamlit, pandas,
> altair) covers the direct dependencies.

## Archived (moved, not deleted)

| Item | From | To |
|---|---|---|
| Generated pipeline outputs | `output/` | `_archive_cleanup_review/output_generated/` |

Contents: weekly_memo.txt, gap_analysis.csv, supply_by_crop_week.csv,
demand_by_crop_week.csv, unresolved_skus.csv. Gitignored generated artifacts,
regenerable by re-running the pipeline. Safe to delete once confirmed not needed.

## Kept (not touched)

- `.claude/` — active Claude Code session state. **Never touched.**
- `.git/` — version history.
- All code: `src/`, `agents/`, `dashboard*.py`, `config.py`, `linear/`, `prompts/`.
- `docs/`, `data/`, both Agri-AI brief PDFs, `harvestmind.duckdb` (12K),
  `requirements.txt`, `AGENTS.md`, `README.md`.

## Added

- `STRUCTURE.md` — plain-English map of the folder.
- `_archive_cleanup_review/` added to `.gitignore`.

---

## Organize pass (2026-06-01)

Filed the only loose documents at the repo root into their proper folder.
The root now holds just the Streamlit app code and standard config.

| Moved | From | To |
|---|---|---|
| Agri-AI Venture Feasibility Brief.pdf | root | docs/business/ |
| agri-ai-brief.pdf | root | docs/business/ |

Left at root intentionally: the app code (config.py, dashboard.py,
dashboard_data.py, dashboard_views.py) — they import each other by bare
module name and run as `streamlit run dashboard.py` from root; moving them
would break the app for no benefit. Plus standard root files (README,
AGENTS, STRUCTURE, requirements.txt, .gitignore) and the gitignored
harvestmind.duckdb the dashboard reads.

Everything else was already organized: agents/, docs/{business,pilot,
product,research}/, linear/, prompts/{claude,codex}/, src/, tests/.

---

## Retire Streamlit dashboard (2026-06-01)

Streamlit is no longer used. The dashboard files were imported by nothing
except each other (confirmed: src/ and tests/ do not import them), so they
are dead code relative to the live pipeline.

| Moved (git mv) | From | To |
|---|---|---|
| dashboard.py | root | archive/streamlit_dashboard/ |
| dashboard_data.py | root | archive/streamlit_dashboard/ |
| dashboard_views.py | root | archive/streamlit_dashboard/ |

Kept at root: config.py — it is ACTIVE (src/main.py imports COVERAGE_THRESHOLD
from it). Plus standard root files (README, AGENTS, STRUCTURE, requirements.txt)
and the gitignored harvestmind.duckdb.

Root is now: config.py + the 3 markdown files + requirements.txt + the DB,
with everything else in folders (src, tests, docs, agents, prompts, linear,
data, archive, _archive_cleanup_review). STRUCTURE.md rewritten to reflect that
the live code is the src/ pipeline and the Streamlit dashboard is retired.
