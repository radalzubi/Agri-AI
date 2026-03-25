# UI/UX Redesign Brief

## Current Build State

The command center is architecturally sound. The data layer (`dashboard_data.py`), rendering layer (`dashboard_views.py`), and orchestration layer (`dashboard.py`) are clean. The module structure (Control Tower → Planning → Demand → Operations → Intelligence → Admin) and the context/build-context pattern are correct and should not change.

The product docs (`dashboard_vision.md`, `ui_principles.md`, `information_architecture.md`, `module_specs.md`) describe a premium analytical command center. The implementation does not yet match that description.

---

## Why the Current UI is Failing

### 1. No distinctive typeface
The CSS loads no custom font. The entire dashboard renders in Streamlit's browser fallback (system-ui or sans-serif). This is the single biggest visual quality gap. At the quality bar of Bloomberg Terminal or Shopify Admin, typeface is non-negotiable.

**Target font system:**
- Display / headers / KPI values: `Barlow Condensed` (800 weight) — gives the dense, confident analytical character of financial data terminals
- Body / labels / captions: `DM Sans` (400, 500, 600) — clean, modern, readable at small sizes without being Inter
- Data / numbers / inline codes: `DM Mono` (400, 500) — monospace alignment for percentages, lbs values, week codes

Load via Google Fonts `@import` at the top of the CSS block.

### 2. Card surfaces lack visual weight
Cards use `border: 1px solid #d6ddd2` against a `#f4f6f1` background. The contrast is too low — panels barely register as distinct surfaces.

**Fix:** Add box-shadow: `0 2px 8px rgba(14, 28, 23, 0.06), 0 1px 3px rgba(14, 28, 23, 0.04)` to all surface cards. Slightly warm the card background to `#fafcf9`.

### 3. Action cards lack severity drama
Critical shortage cards use identical visual weight to Overage Watch cards. Left border color changes but background is the same `#fafbf8`. An operator under time pressure should immediately distinguish Critical from Watch.

**Fix:**
- Critical: background `#fff5f4`, border-left 4px `#b64a3c`, subtle shadow `0 2px 8px rgba(182,74,60,0.10)`
- High: background `#fff9f2`, border-left 4px `#c27a19`
- Review/Watch: background `#f4f8fe`, border-left 4px `#2f6fe4`
- All clear: background `#f3fbf5`, border-left 4px `#2b7a4b`

### 4. Technical deprecations in dashboard_views.py
Three locations use `width="stretch"` in `st.dataframe()` and `st.altair_chart()`. This is a deprecated Streamlit API that generates console warnings and may break in newer Streamlit versions.

**Fix:** Replace all with `use_container_width=True`.

### 5. Briefing panel dark color is disconnected
`briefing-card.dark` uses `background: linear-gradient(#203038, #18252d)` — a dark teal/navy that matches nothing else in the product. The sidebar uses dark green `#13271f`. These should be in the same family.

**Fix:** Change briefing card dark background to `linear-gradient(180deg, #182a20 0%, #11201a 100%)`.

### 6. HTML div wrappers around Streamlit widgets are purely decorative
`<div class='context-strip'>` is opened via `st.markdown()`, then Streamlit widget calls are made, then the div is "closed" via another `st.markdown()`. Streamlit does not render widget HTML inside these divs — the CSS class applies only to the empty divs, not the actual widget containers. The visual effect is inconsistent.

**Fix:** Either accept this limitation and use the div only for visual boundary (not for widget wrapping) or remove the redundant open/close pattern. The CSS should style `[data-testid="stVerticalBlockBorderWrapper"]` selectors or similar Streamlit component targets.

### 7. KPI strip column structure doesn't use the CSS kpi-grid class
`.kpi-grid` is defined in CSS but never applied. The KPI strip uses `st.columns(5)` with `.kpi-card` injected inside each column. The card heights are inconsistent because Streamlit columns don't enforce equal height. The KPI strip looks uneven across different data states.

**Fix:** Render the entire KPI strip as one `st.markdown()` HTML block with a real CSS grid layout instead of 5 separate `st.columns()` calls.

### 8. Charts use line marks where area fills would be more readable
Weekly balance and crop charts use `mark_line(point=True, strokeWidth=2.5)`. For two series (Demand vs Supply), an area chart with 15% opacity fill + a solid line gives significantly more analytical clarity, especially when the two series cross.

**Fix:** Replace with stacked `mark_area(opacity=0.12)` + `mark_line(strokeWidth=2)` layered charts.

---

## What to Preserve Exactly

- `dashboard_data.py` — do not change any logic
- The `build_context()` function and all derived views
- The six-module shell and role lens system
- The action queue, focus state, and `_sync_focus_state` logic
- The heatmap color scale and tooltip structure
- `AGENTS.md`, all product docs in `docs/`
- The `prompts/` directory structure

---

## Design Target Description

The finished interface should feel like:

> A senior supply planner opened a purpose-built cockpit that knows agricultural planning, not a web admin panel that was adapted for it.

Visual reference points (extract principles, do not copy literally):
- **Bloomberg Terminal**: information density, monospace data values, clear severity zones
- **Power BI Premium**: clean surfaces, strong panel hierarchy, purposeful color use
- **Shopify Admin**: confident typography, calm background, frictionless scanning

Aesthetic in one sentence: *clean slate-and-forest palette, condensed display type for all data values, strong card shadows, severity-first color logic.*

---

## Implementation Constraints

- Single-file CSS block inside `dashboard_views.py._CSS` string
- All CSS must be compatible with Streamlit's HTML injection via `st.markdown(unsafe_allow_html=True)`
- No external JavaScript beyond what's already used in `render_copy_button()`
- No additional Python packages beyond current `requirements.txt` (streamlit, pandas, altair)
- Font loading via Google Fonts CDN `@import` inside the CSS block is acceptable

---

## Success Criteria

After the redesign pass:
1. A non-technical operator who opens the dashboard for the first time sees the biggest risk immediately
2. The typography is visibly distinct — Barlow Condensed is unmistakable in the KPI values
3. Action cards at Critical severity look visually urgent compared to Watch cards
4. All console warnings about deprecated Streamlit APIs are gone
5. The briefing panel dark background matches the sidebar dark green family
6. The weekly balance and crop charts use area fills for improved supply/demand legibility
7. The KPI strip renders with equal-height cards regardless of data state
