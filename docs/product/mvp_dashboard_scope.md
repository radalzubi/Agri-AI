# MVP Dashboard Scope

## MVP Decision

The dashboard should ship as a local analytical command center for weekly supply-planning review.

It should be:

- local first
- operator facing
- crop-week driven
- exception led
- honest to current pipeline outputs

It should not behave like a full platform, ERP, or multi-user workflow engine.

## Current Data Contract

The repo currently supports the dashboard through:

- `gap_analysis.csv`
- `demand_by_crop_week.csv`
- `supply_by_crop_week.csv`
- `unresolved_skus.csv`
- `weekly_memo.txt`

This supports a serious review workspace, but it does not yet support:

- buyer account pages
- grower or site plans
- weather event models
- persistent tasks
- approvals
- scenario versions

## MVP Users

- `Supply planner`
- `Aggregator manager`
- `Executive / owner`
- `Data steward`

## MVP Command-Center Modules

### 1. Control Tower

- purpose: run the weekly planning review from one page
- must include:
  - KPI strip
  - shortage-first action board
  - overage watch
  - crop x week exposure heatmap
  - focused crop-week detail
  - memo highlights
  - trust status
- defer:
  - recent change feed
  - approvals
  - buyer service confidence
  - weather watch

### 2. Planning

- purpose: convert exposure into commitment posture
- must include:
  - planning posture buckets
  - commit-now queue
  - rebalance queue
  - crop summary
  - recommendation logic
- defer:
  - editable production plans
  - plan versions
  - approvals
  - scenario compare

### 3. Demand

- purpose: explain demand shape and supply coverage by crop-week
- must include:
  - crop-level demand vs supply trend
  - season weekly balance
  - crop summary table
  - crop-week imbalance detail
- defer:
  - buyer drill-down
  - demand confidence controls
  - forecast versioning

### 4. Operations

- purpose: support weekly review and handoff
- must include:
  - weekly memo
  - review-pack summary
  - action handoff
  - output readiness
- defer:
  - harvest board
  - live logistics tracking
  - shipment management

### 5. Intelligence

- purpose: keep exceptions and trust issues visible
- must include:
  - risk register
  - unresolved SKU blockers
  - confidence summary
  - freshness status
  - blocker impact notes
- defer:
  - anomaly detection
  - weather-driven alerts
  - richer confidence scoring

### 6. Admin

- purpose: keep the local tool understandable and operable
- must include:
  - output file status
  - threshold assumptions
  - known limits
  - run instructions
- defer:
  - import diagnostics
  - threshold editing UI
  - role management

## MVP Metrics That Matter

- weighted supply coverage
- shortage pounds in risk-flagged crop-weeks
- overage pounds above watch threshold
- count of risk-flagged crop-weeks
- unresolved SKU count
- count of active recommended actions

## MVP Design Rules

- start on the Control Tower, not on raw tables
- show what needs action before explanatory charts
- keep crop-week as the core analytical grain
- treat unresolved inputs as trust blockers, not footnotes
- keep filters visible and simple:
  - season
  - crop
  - week range
  - role lens
- do not fake unsupported product depth

## Phase 2 Additions

- buyer and account views
- grower, farm, and site workspace
- production plan objects and versions
- weather and disruption register
- persistent tasks and approvals
- scenario comparison

## Phase 3 Additions

- financial exposure and margin-at-risk
- allocation rules and service-tier logic
- forecast vs actual analytics
- execution signals
- audit trail and access controls
- external collaborator views

## Do Not Build Yet

- warehouse workflows
- route optimization
- full inventory management
- buyer marketplace
- lending or financing products
- autonomous black-box planning
- mobile app
- multi-tenant deployment stack

## Recommended Next Build Steps

1. Keep strengthening the command-center shell around real crop-week decisions.
2. Add persistent task objects only after weekly operating behavior is validated manually.
3. Add buyer and account drill-down only when raw order history is surfaced cleanly.
4. Add scenario compare only after there is a real production plan object to compare.
5. Add weather and disruption tracking only when it can change operator action, not just decorate the UI.
