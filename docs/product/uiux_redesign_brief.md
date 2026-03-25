# UI/UX Redesign Brief — Radical Dark Command Center

## Verdict on Current State

The current dashboard looks like a Streamlit prototype with a green color scheme applied.
It does not look like a purpose-built analytical command center.
An operator who opens it does not feel like they are looking at serious planning software.

This brief specifies a radical visual departure.

---

## Target Aesthetic

**"Dark Terminal Agriculture"**

The closest reference is a Bloomberg Terminal crossed with a mission-control dispatch board, designed specifically for agricultural supply planning.

What it must feel like:
- You are looking at a precision instrument, not a web app
- Every number matters; the design treats numbers as the primary objects
- Risk is visually urgent; healthy state is calm
- The operator knows immediately where danger is

Visual properties:
- **Dark background everywhere**: near-black forest green `#080f0b`, not gray, not navy
- **Cards as raised dark surfaces**: `#111a14` with a faint green-glow border
- **Data values dominate**: large, monospace, vivid color-coded numbers
- **Signal colors are vivid, not muted**: electric green `#00e676`, vivid amber `#ffab00`, bright red `#ff5252`, clear blue `#40c4ff`
- **Typography is distinctive**: condensed display for headers, mono for all data
- **No rounded-corner softness**: 8-10px radius max on cards

---

## Font System

### Required Google Fonts
```
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=IBM+Plex+Mono:wght@400;500;700&family=DM+Sans:wght@400;500;600&display=swap');
```

| Variable | Font | Usage |
|---|---|---|
| `--font-display` | `'Syne'` | Page title, section headers, panel titles |
| `--font-mono` | `'IBM Plex Mono'` | ALL numeric KPI values, data percentages, week codes, lbs values |
| `--font-body` | `'DM Sans'` | Labels, captions, body copy, micro-labels |

**Syne** is geometric, bold, and distinctive — not generic.
**IBM Plex Mono** gives data the weight of financial terminal output.

---

## Color System

### Background layers
```css
--bg:           #080f0b    /* page background — near-black forest */
--surface:      #111a14    /* card surface — slightly raised */
--surface-mid:  #182314    /* intermediate — hover states, alternate rows */
--surface-hi:   #1e2d1e    /* top surface — focused card, detail panel */
```

### Signal colors (vivid, not muted)
```css
--green:        #00e676    /* healthy coverage, all-clear */
--amber:        #ffab00    /* overage watch, caution */
--red:          #ff5252    /* shortage, critical, risk */
--blue:         #40c4ff    /* trust, informational, neutral */
```

### Signal backgrounds (dark-mode tinted cards)
```css
--green-bg:     rgba(0, 230, 118, 0.08)
--amber-bg:     rgba(255, 171, 0, 0.08)
--red-bg:       rgba(255, 82, 82, 0.10)
--blue-bg:      rgba(64, 196, 255, 0.08)
```

### Text hierarchy
```css
--ink:          #e8f0eb    /* primary text — off-white green-tinted */
--muted:        #7a9383    /* secondary text, captions */
--faint:        #3d5446    /* disabled, very secondary */
```

### Border and glow
```css
--line:         rgba(0, 230, 118, 0.12)    /* default card border — green glow */
--line-bright:  rgba(0, 230, 118, 0.30)    /* focused / hover border */
--glow-red:     0 0 0 1px rgba(255, 82, 82, 0.25), 0 4px 16px rgba(255, 82, 82, 0.15)
--glow-amber:   0 0 0 1px rgba(255, 171, 0, 0.20), 0 4px 12px rgba(255, 171, 0, 0.12)
--glow-green:   0 0 0 1px rgba(0, 230, 118, 0.20), 0 4px 12px rgba(0, 230, 118, 0.10)
```

---

## Component Specifications

### Page background
```css
[data-testid="stAppViewContainer"] > .main {
    background: #080f0b;
}
```

### Sidebar
```css
[data-testid="stSidebar"] {
    background: #040a06 !important;
    border-right: 1px solid rgba(0, 230, 118, 0.10);
}
```

Sidebar brand mark: `AGRI-AI` in Syne 800, large, color `#00e676`.
Role lens displayed as active badge with green border.
Navigation radio buttons should look like tab selectors.

### KPI cards
Each KPI card:
- Background: `var(--surface)`
- Border: `1px solid var(--line)`
- No rounded corners beyond 8px
- Value: `IBM Plex Mono`, 2.4rem, 700 weight, vivid signal color
- Sub-label: `DM Sans`, 0.72rem, `var(--muted)`
- Render as a single `st.markdown()` HTML grid (not `st.columns()`), enforcing equal height

```css
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.65rem;
    margin-bottom: 1.1rem;
}

.kpi-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 0.9rem 1rem;
    min-height: 88px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
```

### Action cards (severity-differentiated)

```css
.action-card { border-radius: 8px; border-left: 3px solid; padding: 0.85rem 1rem; margin-bottom: 0.6rem; }
.action-card.red   { border-left-color: var(--red);   background: var(--red-bg);   box-shadow: var(--glow-red);   }
.action-card.amber { border-left-color: var(--amber); background: var(--amber-bg); box-shadow: var(--glow-amber); }
.action-card.blue  { border-left-color: var(--blue);  background: var(--blue-bg);  }
.action-card.green { border-left-color: var(--green); background: var(--green-bg); }
```

### Status pills
```css
.status-pill.green { background: rgba(0,230,118,0.15); color: #00e676; border: 1px solid rgba(0,230,118,0.35); }
.status-pill.amber { background: rgba(255,171,0,0.15); color: #ffab00; border: 1px solid rgba(255,171,0,0.35); }
.status-pill.red   { background: rgba(255,82,82,0.15);  color: #ff5252; border: 1px solid rgba(255,82,82,0.35);  }
.status-pill.blue  { background: rgba(64,196,255,0.15); color: #40c4ff; border: 1px solid rgba(64,196,255,0.35); }
```

### Panel headers
All panel titles: `Syne` 700, 0.92rem, color `var(--ink)`.
Panel caption: `DM Sans`, 0.75rem, `var(--muted)`.
Section separator: 1px solid `rgba(0, 230, 118, 0.12)`.

### Heatmap color scale
Dark-mode friendly scale:
```python
scale=alt.Scale(
    domain=[0, 75, 100, 150],
    range=["#4a1010", "#3d2d00", "#0d2e1a", "#00e676"]
)
```

### Chart styling (dark-mode)
```python
.configure_view(strokeWidth=0, fill="#111a14")
.configure_axis(
    gridColor="rgba(0,230,118,0.07)",
    domainColor="rgba(0,230,118,0.15)",
    labelColor="#7a9383",
    titleColor="#e8f0eb",
)
.configure_legend(
    labelColor="#e8f0eb",
    titleColor="#7a9383",
)
```

Chart series colors:
- Demand: `#40c4ff` (blue)
- Supply: `#00e676` (green)

### Area charts
Weekly balance and crop charts must use `mark_area(opacity=0.10)` + `mark_line(strokeWidth=2)` layers — NOT `mark_line` alone.

---

## Streamlit Global Dark Overrides

Streamlit renders many internal elements with light backgrounds. These must be overridden:

```css
/* Native Streamlit elements dark override */
.stSelectbox > div > div,
.stMultiSelect > div > div,
.stTextInput > div > div > input,
.stSlider > div {
    background: var(--surface) !important;
    color: var(--ink) !important;
    border-color: var(--line) !important;
}

/* Table dark mode */
[data-testid="stDataFrame"] {
    background: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: 8px !important;
}

/* Override Streamlit's white page background */
.stApp {
    background: var(--bg) !important;
}
```

---

## What Must NOT Change

- `dashboard_data.py` — do not touch
- `dashboard.py` — only sidebar brand markup changes
- Six-module shell structure
- Role lens system
- `build_context()` and all derived view functions
- All product docs in `docs/`

---

## Success Test

After the redesign, show the dashboard to someone who hasn't seen it before.
They should say: "This looks like a real operations tool" — not "this is a Streamlit dashboard."

The page title in Syne 800 against a dark background with a glowing green KPI value and a red-glowing critical action card is the moment that should stop a user in their tracks.

That is the quality bar.
