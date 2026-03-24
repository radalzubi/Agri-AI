# Module Specs

## A. Overview / Control Tower

- Purpose: central decision cockpit for the current season
- Primary users: aggregator manager, supply planner, executive
- Major UI components:
  - KPI strip
  - critical alerts rail
  - this-week task queue
  - scenario highlights
  - buyer confidence panel
  - risk heatmap
  - recent plan changes
- Filters: season, week range, crop group, buyer segment, geography
- Primary actions: drill into exception, approve change, assign task, open scenario compare
- Secondary actions: export weekly review pack, save filtered view
- Dependencies: Demand, Plans, Allocation, Risk, Workflows, Analytics
- Permissions: broad read access, approvals limited to managers and executives
- Polished version: live scenario strip, buyer service confidence, recent changes, embedded approvals
- MVP simplification: weighted coverage, shortage and overage exposure, action queue, memo, unresolved data issues
- Usability notes: alerts and actions appear before charts; charts support diagnosis, not first discovery

## B. Demand Intelligence

- Purpose: turn messy order history into a usable forward demand picture
- Primary users: supply planner, buyer account manager
- Major UI components:
  - demand forecast table by buyer, crop, and week
  - demand change feed
  - demand concentration chart
  - seasonality chart
  - anomaly list
- Filters: buyer, crop, week, service tier, channel
- Primary actions: edit forecast, lock forecast version, add demand note
- Secondary actions: export buyer summary, tag anomaly
- Dependencies: Buyers, Analytics, Control Tower
- Permissions: account managers and planners edit; executives read
- Polished version: multi-method forecast compare and buyer event tagging
- MVP simplification: demand-by-crop-week only, no buyer writeback
- Usability notes: show one baseline forecast first; advanced model settings stay collapsed

## C. Buyers / Accounts / Order Patterns

- Purpose: manage demand-side relationships as planning inputs
- Primary users: buyer account manager, aggregator manager
- Major UI components:
  - buyer account summary
  - recurring order pattern table
  - service window and substitution rules
  - risk by buyer panel
- Filters: buyer, crop, season, service tier
- Primary actions: update buyer assumption, log buyer conversation, mark demand confidence
- Secondary actions: export account review
- Dependencies: Demand, Allocation, Analytics
- Permissions: account team owns edits
- Polished version: buyer-specific scenario impact and service risk feed
- MVP simplification: deferred beyond crop-level dashboard
- Usability notes: default to the top issues for one buyer, not all order lines

## D. Production Planning

- Purpose: build the supply commitment plan before the season locks
- Primary users: supply planner, grower/network manager
- Major UI components:
  - crop calendar
  - production plan board
  - commitment lines by grower and site
  - capacity coverage comparison
- Filters: crop, site, grower, week, scenario
- Primary actions: create or revise plan line, shift timing, change quantity, submit for approval
- Secondary actions: clone plan, attach note
- Dependencies: Demand, Yield Forecasting, Allocation, Workflows
- Permissions: planners edit, managers approve
- Polished version: versioned plans with scenario compare and full diff
- MVP simplification: plan lives in grower capacity plus manual notes
- Usability notes: show uncovered demand beside each plan line so users do not need a second screen

## E. Yield Forecasting

- Purpose: convert agronomic or field inputs into expected usable supply
- Primary users: field manager, planner, grower/network manager
- Major UI components:
  - yield assumption cards
  - variance band chart
  - confidence driver list
  - forecast history
- Filters: crop, site, grower, week
- Primary actions: update expected yield, change confidence, flag risk driver
- Secondary actions: compare forecast revisions
- Dependencies: Plans, Risk, Network
- Permissions: field and network users edit with planner review
- Polished version: weather-linked forecast revisions and confidence scoring
- MVP simplification: use static grower capacity as the first-pass forecast
- Usability notes: ask for low-friction updates such as better / same / worse before full numeric edits

## F. Supply Allocation

- Purpose: decide where expected supply should go when it is tight or abundant
- Primary users: supply planner, aggregator manager
- Major UI components:
  - allocation table by crop-week-buyer
  - shortfall queue
  - surplus queue
  - buyer priority panel
  - substitution suggestions
- Filters: crop, week, buyer, priority tier, shortage state
- Primary actions: allocate, reallocate, reserve, escalate shortage
- Secondary actions: export commitment plan, open task
- Dependencies: Demand, Plans, Buyers, Workflows
- Permissions: planners edit, managers approve high-impact changes
- Polished version: scenario-aware allocation engine with service tier rules
- MVP simplification: crop-week gap view and rule-based recommended actions
- Usability notes: make the commercial tradeoff explicit before save

## G. Farms / Growers / Sites

- Purpose: manage the supply network as structured planning capacity
- Primary users: grower/network manager, planner
- Major UI components:
  - grower roster
  - farm/site cards
  - crop roster table
  - reliability and issue history
  - contact panel
- Filters: grower, site, region, crop, status
- Primary actions: update capacity, mark site risk, add grower note
- Secondary actions: compare partners, export network sheet
- Dependencies: Plans, Yield, Risk, Analytics
- Permissions: network owners edit
- Polished version: partner scorecards and external portal
- MVP simplification: deferred; current repo only has aggregated capacity input
- Usability notes: default view should answer who can still cover this crop, not just store contact records

## H. Risk Management

- Purpose: consolidate planning risk into one operating register
- Primary users: planner, operations manager, executive
- Major UI components:
  - risk register
  - severity filters
  - impact matrix
  - mitigation status
- Filters: severity, crop, week, site, buyer, status
- Primary actions: open event, change severity, start mitigation, create task
- Secondary actions: subscribe, add note
- Dependencies: Weather, Plans, Allocation, Workflows
- Permissions: planners and ops users edit; executives read and escalate
- Polished version: composite risk scores with audit trail
- MVP simplification: risk flags from coverage thresholds plus unresolved data issues
- Usability notes: risk cards must say what is impacted and who owns response

## I. Weather + Disruption Monitoring

- Purpose: bring outside signals into the planning loop
- Primary users: planner, field manager, ops manager
- Major UI components:
  - weather event feed
  - map or region summary
  - impacted crop-week list
  - disruption severity panel
- Filters: geography, event type, week, severity
- Primary actions: acknowledge event, link to impacted plans, trigger mitigation
- Secondary actions: snooze, annotate
- Dependencies: Risk, Yield, Network
- Permissions: planners and field users edit notes
- Polished version: automated weather ingest with manual review
- MVP simplification: manual event notes only
- Usability notes: never show weather data without linked operational impact

## J. Operations / Execution

- Purpose: capture execution signals that change planning truth
- Primary users: operations manager, planner
- Major UI components:
  - harvest readiness board
  - open bottlenecks list
  - outbound readiness panel
  - available supply adjustments
- Filters: week, site, crop, bottleneck type
- Primary actions: update status, flag issue, adjust available supply
- Secondary actions: attach note, create task
- Dependencies: Allocation, Logistics, Inventory, Workflows
- Permissions: ops team edits, planners read
- Polished version: live operational board tied to allocations
- MVP simplification: thin issue log only; do not build a full execution system yet
- Usability notes: show downstream buyer impact for each issue

## K. Logistics / Delivery Coordination

- Purpose: coordinate delivery exceptions that threaten service or available supply
- Primary users: logistics coordinator, ops manager
- Major UI components:
  - shipment list
  - delivery window conflicts
  - load status board
  - exception queue
- Filters: buyer, route, date, shipment status
- Primary actions: update shipment status, change load timing, flag service risk
- Secondary actions: export dispatch sheet
- Dependencies: Operations, Buyers, Allocation
- Permissions: logistics users edit
- Polished version: route constraints and cold-chain issue handling
- MVP simplification: keep out of scope unless delivery failure changes weekly planning
- Usability notes: no route optimizer in MVP; focus only on decision-relevant exceptions

## L. Inventory / Harvest / Available Supply

- Purpose: show what supply is actually becoming real as harvest approaches
- Primary users: ops manager, planner
- Major UI components:
  - harvest availability table
  - expected versus actual harvested supply
  - spoilage or rejection flags
  - reserve inventory summary
- Filters: crop, site, harvest date, quality status
- Primary actions: update available supply, flag spoilage, convert planned to actual
- Secondary actions: export availability sheet
- Dependencies: Operations, Allocation, Analytics
- Permissions: ops users edit
- Polished version: near-harvest available-to-allocate view
- MVP simplification: not a warehouse system; only include near-harvest availability signals later
- Usability notes: keep it planning-adjacent, not lot-traceability heavy

## M. Tasks / Exceptions / Approvals

- Purpose: convert insight into owned work and controlled decisions
- Primary users: all internal roles
- Major UI components:
  - task board
  - approval inbox
  - exception board
  - linked activity feed
- Filters: owner, due date, priority, object type, status
- Primary actions: assign, approve, reject, complete, reopen
- Secondary actions: comment, mention teammate
- Dependencies: all operational modules
- Permissions: broad; approvals role-limited
- Polished version: embedded task drawer from any object page
- MVP simplification: action queue derived from risk and memo outputs
- Usability notes: task creation should inherit context automatically

## N. Analytics / Reporting

- Purpose: measure whether the system improves outcomes
- Primary users: executive, finance/admin, planner
- Major UI components:
  - fill-rate trend
  - emergency-buy trend
  - overage and waste trend
  - forecast-accuracy report
  - grower performance scorecard
- Filters: season, buyer, crop, site, region
- Primary actions: save view, compare seasons, export report
- Secondary actions: annotate outcome
- Dependencies: Demand, Plans, Allocation, Operations
- Permissions: mostly read-only
- Polished version: pilot KPI pack and board-ready review pages
- MVP simplification: weighted coverage, shortage pounds, overage pounds, unresolved inputs
- Usability notes: start with pilot success metrics, not vanity charts

## O. Settings / Admin / Data Input

- Purpose: keep assumptions, imports, and access clean
- Primary users: admin, finance/admin, data steward
- Major UI components:
  - import status
  - lookup table management
  - threshold settings
  - role management
  - audit log
- Filters: source file, import date, object type, user
- Primary actions: import data, resolve SKU, edit thresholds, manage roles
- Secondary actions: export audit log
- Dependencies: all modules
- Permissions: restricted
- Polished version: import diagnostics, stale data alerts, approval policies
- MVP simplification: unresolved SKUs, output freshness, and threshold visibility only
- Usability notes: admin depth should stay away from the default user path
