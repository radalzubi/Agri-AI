# Dashboard Vision

## Objective

Define Agri-AI's flagship interface as an analytical command center for supplier-side agricultural planning.

The interface must help a buyer-facing operator answer five questions quickly:

- what should we commit
- where is risk building
- what needs action now
- what changed in the current review window
- where should we drill deeper

## Product Truth

Agri-AI is not a generic farm dashboard and not a warehouse ERP.

It is a planning workspace for the period before inventory fully exists.
The operator is using demand history, grower capacity assumptions, crop calendars, and risk signals to decide how much supply to commit and where exposure is building.

The interface therefore has to feel:

- analytical
- operational
- dense but controlled
- commercially grounded
- trustworthy under messy pilot data

## Interface Stance

### What the UI should feel like

- a weekly decision board, not a reporting portal
- a control tower with context preserved while drilling down
- a serious operator workspace where exceptions dominate the page

### What the UI should not feel like

- a CRUD-heavy back office
- a BI export full of detached charts
- a template admin dashboard with giant empty cards
- a fake ERP shell with empty modules

## Product Shell

Use a tight top-level shell:

1. `Control Tower`
2. `Planning`
3. `Demand`
4. `Operations`
5. `Intelligence`
6. `Admin`

This shell is small on purpose.
It keeps the product legible while still allowing future expansion into buyer views, grower views, scenarios, and execution signals.

## Flagship Screen: Control Tower

The Control Tower is the home screen and the operating heart of the product.

### Layout zones

#### 1. Context bar

- role lens
- current season
- week horizon
- crop scope
- output freshness
- data confidence state

#### 2. Health strip

- weighted coverage
- demand at risk
- overage exposure
- risk-flagged crop-weeks
- trust blockers

#### 3. Action board

- critical shortage actions
- overage watch actions
- operator action queue

#### 4. Exposure map

- crop x week coverage heatmap
- focus crop-week detail

#### 5. Diagnostic band

- weekly balance trend
- crop concentration summary
- current planning posture

#### 6. Insight rail

- weekly briefing highlights
- trust and data quality warnings
- file/output readiness

### Control Tower priority order

The page should answer these in sequence:

1. what needs intervention now
2. where the exposure is concentrated
3. what the recommended next move is
4. how much confidence to place in the current view

## MVP Honest Boundaries

Current repo outputs support:

- crop-week coverage
- shortage and overage exposure
- unresolved SKU blockers
- memo-driven weekly review
- rule-based recommendations

Current repo outputs do not support:

- buyer account intelligence
- site-level planning
- grower reliability scoring
- real scenarios
- change history
- approvals
- persistent tasks
- weather-driven event models

The UI must stay premium without pretending those layers exist.

## Design Consequences

- prioritize exceptions over charts
- keep memo and data confidence inside the command flow
- make role lenses materially change defaults, not just copy
- preserve drill-down context around crop and week
- use tables as operational tools, not as the default first screen
- keep future enterprise structure visible in docs, but only expose MVP reality in code
