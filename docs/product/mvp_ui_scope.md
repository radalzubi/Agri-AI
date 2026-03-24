# MVP UI Scope

## Purpose

Define the UI that should ship now for the current Agri-AI MVP.

The MVP should already feel premium and operator-grade, but it must remain honest to the repo's current data model:

- crop-week demand
- crop-week supply
- gap analysis
- unresolved SKU blockers
- weekly memo

## MVP User Set

- `Supply planner`
- `Aggregator manager`
- `Executive`
- `Data steward`

## MVP Sections

### 1. Control Tower

Ship now.

Must include:

- context bar
- health strip
- shortage-first action board
- overage watch
- crop x week coverage heatmap
- weekly briefing highlights
- trust status
- focused crop-week detail

### 2. Planning

Ship now, but keep it heuristic.

Must include:

- planning posture buckets
- shortage queue
- overage watch
- recommended actions
- crop summary

Do not imply:

- real production plan editing
- scenario versioning
- approvals

### 3. Demand

Ship now.

Must include:

- weekly demand vs supply by crop
- crop summary table
- crop-week imbalance detail
- season weekly balance trend

### 4. Operations

Ship now as a review-and-handoff workspace, not as a live execution system.

Must include:

- weekly memo
- review pack summary
- action handoff
- output readiness

Do not build:

- harvest board
- logistics routing
- shipment management

### 5. Intelligence

Ship now.

Must include:

- risk register
- unresolved SKU blockers
- data confidence summary
- file freshness
- trust-impact summary

### 6. Admin

Ship now as a thin utility workspace.

Must include:

- output file status
- threshold assumptions
- glossary and data contract
- run instructions

## MVP Exclusions

Do not build now:

- buyer accounts
- grower/site pages
- scenario modeling
- persistent tasks
- approvals
- weather event layer
- financial exposure
- change history
- route or warehouse flows

## Phase 2

- buyer and account views
- grower/farm/site structure
- production plan objects
- weather and disruption register
- persistent tasks and approvals
- scenario comparison

## Phase 3

- financial exposure
- allocation rules
- forecast vs actual analytics
- operational execution signals
- audit trails
- external collaborator views

## MVP Quality Standard

The MVP UI succeeds if a planner can open the app and within two minutes answer:

- what is the biggest shortage
- what overage needs attention
- which crop-week deserves focus
- whether the current view is trustworthy enough to act on
