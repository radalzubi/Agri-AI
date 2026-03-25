# Codex: Agri-AI Dashboard Redesign — Master Prompt

## Your Role

You are executing a precision frontend upgrade of the Agri-AI analytical command center.
You are NOT rebuilding the architecture.
You are NOT changing data logic.
You ARE upgrading the visual quality, typography, component consistency, and technical correctness of the dashboard rendering layer.

The target quality bar: a supply planning operator should open this dashboard and feel they are using a purpose-built analytical command center, not a Streamlit prototype.

---

## Required Reading — Do This Before Any Code Change

Read these files in order:

1. `AGENTS.md`
2. `docs/product/dashboard_vision.md`
3. `docs/product/ui_principles.md`
4. `docs/product/information_architecture.md`
5. `docs/product/uiux_redesign_brief.md` ← primary specification for this pass
6. `dashboard_views.py` — the main file you will change
7. `dashboard_data.py` — read only, do not modify
8. `dashboard.py` — read only, do not modify

Also consult the project-local subagents in `.claude/agents/` when making decisions:
- `.claude/agents/uiux-critic.md` — for hierarchy and operator-flow decisions
- `.claude/agents/design-system-enforcer.md` — for token and typography consistency
- `.claude/agents/analytics-dashboard-designer.md` — for chart and panel composition
- `.claude/agents/information-architect.md` — for module structure questions

---

## Branch and Commit Instructions

1. Create a new branch: `codex/dashboard-redesign-v2`
2. All changes go to that branch
3. Commit at each logical phase (CSS system, typography, cards, charts, bug fixes)
4. Do not push to main — leave the PR for human review

---

## Phase 1 — Bug Fixes (do first, no visual judgment needed)

These are clear technical correctness fixes. Apply them before touching any visual code.

### Fix 1.1 — Deprecated API: `width="stretch"`

Search `dashboard_views.py` for all instances of:
```python
st.dataframe(..., width="stretch", ...)
st.altair_chart(..., width="stretch")
```

Replace ALL occurrences with `use_container_width=True`.

Also check `dashboard.py` for the same pattern.

Verify: run `grep -n "width=" dashboard_views.py dashboard.py` and confirm no `width="stretch"` remains.

### Fix 1.2 — Briefing panel dark background

In `dashboard_views.py`, find the CSS rule for `.briefing-card.dark`.
Change the background to:
```css
.briefing-card.dark {
    background: linear-gradient(180deg, #182a20 0%, #11201a 100%);
    border-color: #2a4535;
    color: #e8f4ec;
}
.briefing-card.dark p,
.briefing-card.dark li,
.briefing-card.dark span {
    color: #c8e6d3;
}
```
This aligns the briefing card with the sidebar dark green family instead of the disconnected navy.

---

## Phase 2 — Typography System

This is the single highest-impact change. Apply it completely before moving on.

### Step 2.1 — Load custom fonts

At the very top of the `_CSS` string (before `:root`), add:

```css
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&display=swap');
```

### Step 2.2 — Add font variables to `:root`

```css
:root {
    /* ... existing tokens ... */
    --font-display: 'Barlow Condensed', 'Arial Narrow', sans-serif;
    --font-body:    'DM Sans', system-ui, sans-serif;
    --font-mono:    'DM Mono', 'Courier New', monospace;
}
```

### Step 2.3 — Apply font families

Add or update these CSS rules:

```css
html, body, [class*="css"] {
    font-family: var(--font-body);
    color: var(--ink);
}

.shell-title {
    font-family: var(--font-display);
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.kpi-value {
    font-family: var(--font-display);
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.01em;
    line-height: 1;
}

.kpi-sub {
    font-family: var(--font-body);
    font-size: 0.76rem;
    color: var(--muted);
}

.micro-label {
    font-family: var(--font-body);
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
}

.panel-title {
    font-family: var(--font-body);
    font-size: 0.94rem;
    font-weight: 800;
    letter-spacing: -0.01em;
}

.panel-caption {
    font-family: var(--font-body);
    font-size: 0.77rem;
    color: var(--muted);
}

/* All data values and coverage percentages use monospace */
.detail-metric .value,
.kpi-value {
    font-family: var(--font-display);
}
```

---

## Phase 3 — Card Surface System

### Step 3.1 — Strengthen base card shadow

Find the shared card CSS block. Replace or augment the `box-shadow`:

```css
.surface-card,
.kpi-card,
.briefing-card,
.confidence-card,
.detail-card {
    background: #fafcf9;
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow:
        0 1px 3px rgba(14, 28, 23, 0.04),
        0 4px 12px rgba(14, 28, 23, 0.06);
}
```

### Step 3.2 — Severity-differentiated action cards

Replace the current `.action-card` rules with:

```css
.action-card {
    border: 1px solid var(--line);
    border-left-width: 4px;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.7rem;
    transition: box-shadow 0.12s;
}

.action-card:hover {
    box-shadow: 0 4px 14px rgba(14, 28, 23, 0.10);
}

.action-card.red {
    border-left-color: var(--red);
    background: #fff5f4;
    box-shadow: 0 2px 8px rgba(182, 74, 60, 0.08);
}

.action-card.amber {
    border-left-color: var(--amber);
    background: #fff9f2;
    box-shadow: 0 2px 8px rgba(194, 122, 25, 0.07);
}

.action-card.blue {
    border-left-color: var(--blue);
    background: #f4f8fe;
}

.action-card.green {
    border-left-color: var(--green);
    background: #f3fbf6;
}
```

### Step 3.3 — KPI card equal height via HTML grid

Replace the `render_kpi_strip()` function's column-based rendering with a single `st.markdown()` block using an inline grid. Build the HTML in one call:

```python
def render_kpi_strip(kpis: Dict[str, Any], confidence: Dict[str, Any]) -> None:
    # ... compute tones and values ...
    
    cards_html = "".join([
        f"<div class='kpi-card'>"
        f"<div class='micro-label'>{label}</div>"
        f"<div class='kpi-value tone-{tone}'>{value}</div>"
        f"<div class='kpi-sub'>{sub}</div>"
        f"</div>"
        for label, value, tone, sub in cards
    ])
    
    st.markdown(
        f"<div class='kpi-grid'>{cards_html}</div>",
        unsafe_allow_html=True,
    )
```

And add a real CSS grid definition for `.kpi-grid`:

```css
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.8rem;
    margin-bottom: 1.1rem;
    align-items: stretch;
}

.kpi-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 96px;
    padding: 0.9rem 1rem 0.75rem 1rem;
}
```

This ensures equal card heights regardless of value length.

---

## Phase 4 — Chart Upgrades

### Step 4.1 — Weekly balance: line → area

In `render_weekly_balance_chart()`, replace `mark_line` with a layered area + line:

```python
base = alt.Chart(balance_df)

area_layer = base.mark_area(opacity=0.12, interpolate="monotone").encode(
    x=alt.X("week_label:N", title="Week", sort=None,
             axis=alt.Axis(labelAngle=-35, labelFontSize=11)),
    y=alt.Y("pounds:Q", title="Pounds",
             axis=alt.Axis(labelFontSize=11)),
    color=alt.Color("series:N",
        scale=alt.Scale(domain=["Demand", "Supply"], range=[_BLUE, _GREEN]),
        title=None),
)

line_layer = base.mark_line(strokeWidth=2, interpolate="monotone").encode(
    x="week_label:N",
    y="pounds:Q",
    color=alt.Color("series:N",
        scale=alt.Scale(domain=["Demand", "Supply"], range=[_BLUE, _GREEN])),
    tooltip=[
        alt.Tooltip("week_label:N", title="Week"),
        alt.Tooltip("series:N", title="Series"),
        alt.Tooltip("pounds:Q", title="Pounds", format=",.1f"),
    ],
)

chart = (
    (area_layer + line_layer)
    .properties(height=260)
    .configure_view(strokeWidth=0)
    .configure_axis(gridColor="#eff1ed", gridOpacity=1, domainColor="#d6ddd2",
                    labelColor="#60707a", titleColor="#12202a")
)
```

Apply the same pattern to `render_crop_chart()`.

### Step 4.2 — Chart title consistency

All charts must use:
```python
.properties(
    title=alt.TitleParams(
        text="Chart title here",
        fontSize=13, fontWeight=700,
        color="#12202a", anchor="start",
    ),
    height=<height>,
)
```

### Step 4.3 — Heatmap tooltip enhancement

Add `alt.Tooltip("severity:N", title="Signal")` to the heatmap tooltip list if not already present.
Verify the heatmap uses `use_container_width=True`.

---

## Phase 5 — Sidebar Polish

In `dashboard.py`, enhance the sidebar brand section:

```python
st.sidebar.markdown(
    "<div style='padding:0.5rem 0 1.2rem 0; border-bottom: 1px solid rgba(165,212,180,0.2); margin-bottom:1rem'>"
    "<div style='font-family:\"Barlow Condensed\",sans-serif; font-size:1.35rem; font-weight:800; "
    "color:#86efac; letter-spacing:-0.01em; line-height:1'>AGRI-AI</div>"
    "<div style='font-size:0.72rem; color:#6aab82; font-weight:500; margin-top:0.2rem'>"
    "Supply planning command center</div>"
    "</div>",
    unsafe_allow_html=True,
)
```

---

## Phase 6 — Panel Head Hierarchy

The current `render_panel_header()` uses identical visual weight for all panels.
Add a `level` parameter: `"primary"` (Control Tower action board, heatmap) vs `"secondary"` (default all others).

```python
def render_panel_header(title: str, caption: str, icon: str = "", level: str = "secondary") -> None:
    border = "border-bottom: 2px solid var(--line);" if level == "primary" else "border-bottom: 1px solid var(--line);"
    title_size = "1.05rem" if level == "primary" else "0.94rem"
    display_title = f"{icon} {title}".strip()
    st.markdown(
        f"<div class='panel-head' style='{border} padding-bottom:0.65rem; margin-bottom:0.9rem'>"
        f"<div><div class='panel-title' style='font-size:{title_size}'>{display_title}</div>"
        f"<div class='panel-caption'>{caption}</div></div>"
        "</div>",
        unsafe_allow_html=True,
    )
```

Call `render_panel_header(..., level="primary")` for:
- "What Needs Action Now" in Control Tower
- "Exposure Map" heatmap
- "Weekly Review Memo" in Operations

---

## Phase 7 — Final Verification Checklist

After all phases are complete, verify each item:

- [ ] `grep -c "width=\"stretch\"" dashboard_views.py dashboard.py` returns 0
- [ ] `grep -c "@import" dashboard_views.py` returns 1 (the Google Fonts import)
- [ ] `.briefing-card.dark` background uses `#182a20` family (not `#203038`)
- [ ] `.action-card.red` has `background: #fff5f4` and a red-tinted shadow
- [ ] `.kpi-grid` CSS is defined with `grid-template-columns: repeat(5, 1fr)`
- [ ] `render_kpi_strip()` uses a single `st.markdown()` HTML block, not 5 `st.columns()`
- [ ] Weekly balance chart uses `mark_area` + `mark_line` layer
- [ ] All `st.altair_chart()` calls use `use_container_width=True`
- [ ] Sidebar has the Barlow Condensed brand mark
- [ ] `render_panel_header()` accepts `level` parameter

Run:
```bash
source .venv/bin/activate
python3 -m src.main --data-dir data --output-dir output
streamlit run dashboard.py
```

Open http://localhost:8501 and verify:
1. Barlow Condensed renders visibly in KPI values and page title
2. Action cards have distinct background tints per severity
3. No browser console warnings about deprecated APIs
4. Weekly balance chart shows area fills, not just lines
5. The briefing panel dark background matches the sidebar green family

---

## Constraints — Do Not Violate

- Do NOT change `dashboard_data.py`
- Do NOT change `dashboard.py` beyond the sidebar brand mark (Phase 5)
- Do NOT add new Python packages to `requirements.txt`
- Do NOT change the six-module structure
- Do NOT add new views or panels not already in the current implementation
- Do NOT add scenario, buyer, or weather panels
- Do NOT use JavaScript beyond what's already in `render_copy_button()`
- Do NOT remove the existing color token system — extend it

---

## Definition of Done

The redesign pass is complete when:
1. All seven phases above are done
2. The verification checklist passes
3. The dashboard runs cleanly on `streamlit run dashboard.py`
4. Branch `codex/dashboard-redesign-v2` has clean commits by phase
5. A summary of what changed is written to `prompts/codex/dashboard_redesign_v2_summary.md`

If you find additional clear bugs during the pass (wrong Altair API usage, missing error handling, visual inconsistencies not listed above), fix them and document in the summary. Do not use this permission to expand scope.
