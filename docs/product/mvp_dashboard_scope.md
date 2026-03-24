# MVP Dashboard Scope

## MVP Decision

The current product should ship as a pilot control tower, not a full multi-user platform.

That means:

- local first
- operator-facing
- weekly planning centered
- rule-based where possible
- additive to existing spreadsheets and systems

## Current Data Available In The Repo

The existing pipeline produces:

- `gap_analysis.csv`
- `demand_by_crop_week.csv`
- `supply_by_crop_week.csv`
- `unresolved_skus.csv`
- `weekly_memo.txt`

This supports a strong planning dashboard, but it does not yet support:

- buyer account pages
- grower scorecards
- site-level plans
- weather-driven risk
- tasks with persistence
- approvals
- scenario versions

## MVP Users

- `Supply planner`
  - primary operator
  - runs weekly review
- `Aggregator manager`
  - reviews top risks and approvals
- `Executive / owner`
  - checks pilot value and season health
- `Data steward`
  - resolves unresolved SKUs and input quality issues

## MVP Dashboard Modules

### 1. Control Tower

- Purpose: one-screen weekly operating review
- Current data:
  - weighted coverage
  - demand at risk
  - overage exposure
  - risk-flagged crop-weeks
  - unresolved SKU count
  - memo summary
- Actions:
  - open the highest-risk crop-weeks
  - review recommended actions
  - export or copy weekly memo
- Deferred:
  - approvals
  - recent change feed
  - buyer service confidence
  - bottleneck ownership

### 2. Demand And Coverage

- Purpose: show how expected supply compares to expected demand by crop and week
- Current data:
  - demand by crop-week
  - supply by crop-week
  - crop-level coverage ratios
- Actions:
  - filter by crop and week
  - inspect season imbalance
- Deferred:
  - buyer drill-down
  - demand confidence adjustments
  - scenario overlays

### 3. Risk Desk

- Purpose: turn gap rows into a usable exception queue
- Current data:
  - shortage and overage math
  - risk flags
  - unresolved inputs
- Actions:
  - filter to risk only
  - sort by severity
  - review action queue
- Deferred:
  - task assignment persistence
  - owner routing
  - approval workflow

### 4. Planning Memo

- Purpose: give operators a meeting-ready written output
- Current data:
  - weekly memo text
- Actions:
  - copy memo
  - use memo in weekly meeting
- Deferred:
  - editable notes
  - scenario commentary
  - meeting pack export

### 5. Data Quality

- Purpose: make trust issues visible before decisions are made
- Current data:
  - unresolved SKUs
  - output file freshness
- Actions:
  - review unresolved names
  - confirm pipeline output freshness
- Deferred:
  - import diagnostics
  - stale grower assumptions
  - missing buyer fields

## MVP Metrics That Matter

- weighted supply coverage
- shortage pounds in risk-flagged crop-weeks
- overage pounds above watch threshold
- count of risk-flagged crop-weeks
- unresolved SKU count
- number of recommended actions generated this week

## MVP Design Rules

- Start on the Control Tower, not a raw table.
- Show what changed and what needs action before showing all data.
- Use crop-week as the core grain of the dashboard.
- Treat unresolved inputs as blockers to trust, not as footnotes.
- Keep filters simple:
  - season
  - crop
  - week range
  - risk only
- Do not fake features the data cannot support.

## Phase 2 Additions

- buyer and account pages
- grower, farm, and site workspace
- production plan object with plan versions
- yield forecasting inputs
- weather and disruption feed
- persistent tasks and approvals
- basic scenario planner

## Phase 3 Additions

- financial exposure and margin-at-risk layer
- allocation engine with service-tier rules
- external grower portal
- logistics and harvest exception integration
- full audit trail and role-based access
- broader analytics and benchmarking

## Do Not Build Yet

- warehouse workflows
- route optimization
- full inventory management
- buyer marketplace
- lender or financing products
- autonomous AI planner
- mobile app
- multi-tenant deployment stack

## Recommended Next Build Steps

1. Upgrade `dashboard.py` into a clearer Control Tower plus risk desk.
2. Add a crop-week coverage heatmap and action queue derived from current outputs.
3. Add a thin buyer-level demand view once raw order history is surfaced in the dashboard layer.
4. Define the first persistent product objects:
   - buyer
   - production plan
   - task
   - scenario
5. Add a manual weather and disruption register before attempting automated feeds.
