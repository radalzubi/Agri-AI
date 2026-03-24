# Dashboard System

## Objective

Define the operator-grade dashboard and management system for Agri-AI without drifting out of the actual wedge:
planning buyer demand, grower commitments, and supply risk before inventory fully exists.

## Repo-Grounded Design Brief

### What the repo already proves

- The paying user is not the individual farm. The clearest first buyer is the buyer-facing aggregator, food hub, or regional produce operator managing recurring demand across multiple growers.
- The product has to earn value inside one season. The value signal is earlier shortage visibility, fewer emergency buys, lower overproduction, and faster weekly planning.
- The current MVP is a Python planning pipeline plus a local Streamlit dashboard. It already produces crop-week demand, supply, gap flags, unresolved SKU lists, and a weekly memo.
- The Indiana and Midwest pilot context matters. The first product must work for operators with messy data, limited budgets, seasonal cycles, and heavy spreadsheet dependence.

### What the repo does not have yet

- Buyer account pages and order-pattern drill-downs
- Production plans as first-class objects
- Scenario planning and plan approvals
- Yield forecasts beyond static grower capacity assumptions
- Weather, disruption, and crop-failure event tracking
- Task ownership and exception routing
- Grower, farm, and site operating views
- Financial exposure views tied to margin, not just pounds
- Audit trails for plan changes

### Gap between current repo and full product

The repo is correct about the wedge and underdeveloped on the product system.

Current build:

- CSV in
- rule-based aggregation
- crop-week risk math
- local dashboard

Missing product system:

- role-specific workspaces
- planning workflows
- operating actions
- handoffs between sales, planning, grower coordination, and ops
- durable management objects

### Design decisions this brief resolves

- Use ERP and control-tower patterns, but only where they improve pre-season and in-season planning decisions.
- Treat Agri-AI as a planning operating system, not a warehouse ERP, buyer marketplace, or generic farm suite.
- Extend into execution modules only when execution signals change planning quality.
- Make the main unit of management the crop x week x buyer x grower-network decision, not inventory-on-hand.
- Put exceptions, approvals, and scenario comparisons at the center of the UX.

## Product System Stance

### What Agri-AI is

- planning infrastructure for buyer-facing specialty-crop operators
- a decision cockpit for matching recurring demand with expected supply
- a risk and commitment layer that sits upstream of warehouse and commerce tools

### What Agri-AI is not

- full farm management for independent farms
- a commodity-agriculture system
- a produce-distributor ERP replacement
- a route optimizer or warehouse platform
- an AI autopilot making unreviewed commitments

## Operating Loop

1. Ingest demand history, buyer requirements, grower capacity, and seasonal assumptions.
2. Generate a baseline demand view by buyer, crop, and week.
3. Build or adjust the production plan by crop, farm, site, and grower.
4. Score supply risk, overage risk, and execution bottlenecks.
5. Allocate expected supply against buyer demand and service priorities.
6. Create approvals, follow-ups, and owner-assigned tasks.
7. Monitor live disruptions, harvest progress, and fulfillment drift.
8. Feed actuals back into future planning assumptions.

## Product Principles

- Planning first: every major screen should help decide what to commit, protect, reallocate, or escalate.
- Exception driven: the interface should surface what changed, what is at risk, and who needs to act next.
- Role based: executives, planners, account managers, ops users, and grower coordinators should not share the same default view.
- Human override first: every recommendation needs a visible manual override and a reason trail.
- Additive integration: Agri-AI should fit beside spreadsheets, commerce tools, and produce ERPs before it tries to replace them.
- Data quality visible: stale inputs, unresolved SKUs, and weak assumptions must be obvious.
- Financially grounded: pounds matter, but margin at risk and service failure cost matter more.
- Trust before automation: AI outputs must be explainable, confidence-scored, and easy to challenge.

## Core Data Objects

| Object | Purpose | Key Fields | Edited By | Used In |
| --- | --- | --- | --- | --- |
| `buyer` | Commercial account record | name, segment, service tier, delivery windows, buyer priority, payment terms, margin profile | sales/account manager, admin | Demand, Buyers, Allocation, Analytics |
| `order` | Raw or committed demand line | buyer, crop, quantity, pack, grade, requested week, status, price | sales/account manager, import pipeline | Demand, Buyers, Analytics |
| `demand_forecast` | Expected demand by buyer-crop-week | buyer, crop, week, baseline qty, forecast method, confidence, notes | supply planner | Demand, Control Tower, Plans |
| `crop` | Canonical planning item | crop name, category, pack assumptions, shelf-life, lead time, substitution group | admin, planner | All planning modules |
| `production_plan` | Planned supply commitment before harvest | season, crop, site, grower, planned qty, planned harvest week, status, owner | supply planner, grower/network manager | Plans, Allocation, Control Tower |
| `farm_site` | Physical production node | farm, site name, acreage, production method, region, cooling/storage notes | grower/network manager, admin | Network, Plans, Risk |
| `grower` | Supply partner record | name, contact, reliability score, crop roster, certifications, notes | grower/network manager | Network, Plans, Risk |
| `yield_forecast` | Expected output from a plan or site | production plan, expected qty, forecast window, variance band, confidence driver | planner, field manager | Plans, Risk, Analytics |
| `supply_allocation` | Supply matched to buyers | crop, week, buyer, source grower/site, allocated qty, priority rule, approval status | supply planner | Allocation, Control Tower, Workflows |
| `risk_event` | Structured exception | event type, severity, impacted crop, impacted week, impacted sites/buyers, status, owner | planner, ops manager | Risk, Control Tower, Workflows |
| `weather_event` | External disruption signal | geography, week, event type, severity, confidence, expected effect | imported feed, planner review | Risk, Weather, Yield |
| `task` | Follow-up work item | title, owner, due date, linked object, priority, status, resolution notes | any internal user | Workflows, Control Tower |
| `shipment` | Planned or actual delivery event | buyer, delivery date, crop, qty, source, status, exception flags | logistics coordinator, ops manager | Logistics, Execution, Analytics |
| `scenario` | Alternative plan version | name, assumptions, plan deltas, expected coverage, margin effect, approval status | planner, manager | Plans, Control Tower, Analytics |
| `fulfillment_metric` | Outcome metric record | fill rate, unfilled lines, emergency buys, substitutions, service failures, week/season | analytics, admin | Control Tower, Analytics |
| `financial_exposure` | Money view of planning risk | buyer, crop, week, margin at risk, revenue at risk, emergency-buy exposure | finance/admin, planner | Control Tower, Analytics |
| `planning_cycle` | Review cadence wrapper | season, weekly review date, owner, decision state, locked assumptions | planner, manager | Control Tower, Workflows, Analytics |

## AI-Native Features

| Feature | Problem Solved | Inputs | Output | MVP Approach | Trust Guardrails |
| --- | --- | --- | --- | --- | --- |
| Demand forecast assistant | Spreadsheets miss seasonal demand shifts and buyer concentration changes | order history, buyer cadence, crop seasonality, service calendars | baseline forecast plus confidence band | heuristics and moving averages first | show history used, confidence, and manual override |
| Production quantity recommendation | Operators need a first-pass commitment target before planting | forecast, crop calendar, grower capacity, yield assumptions, risk tolerance | recommended planned quantity by crop-week-site | deterministic rule set first | expose drivers and allow line-by-line edits |
| Shortage and surplus prediction | Risk must be visible before commitments harden | forecast, plan, yield, weather, live exceptions | projected shortage or overage by crop-week | current repo gap math plus simple thresholds | show formula, threshold, and affected assumptions |
| Risk scoring | Users need a single risk signal across multiple weak inputs | weather, grower reliability, yield variance, labor notes, logistics constraints | risk score and top drivers | manual weights before ML | show driver stack, severity, and source freshness |
| Reallocation recommendation | When supply tightens, users need a clear next move | buyer priority, margin, service obligations, substitute rules, allocation gaps | suggested reallocation path | rules first | show who loses volume, who gains it, and why |
| Natural-language planning summary | Weekly review prep is slow | open risks, plan deltas, actions, data quality flags | meeting-ready summary | current memo generation plus richer templates | never hide source numbers; link every statement back to data |
| Anomaly detection | Operators miss unusual demand spikes or weak forecasts | multi-season demand, actuals, buyer events, disruptions | flagged anomalies and explanation | defer until clean multi-season data exists | require human confirmation before action |

## Design Consequence

The flagship dashboard should behave like an operating review system for a supply planner and aggregator manager.
It should not behave like a generic analytics home page.
Every major panel should answer one of four questions:

- Where are we exposed?
- What changed?
- What decision is due?
- Who owns the next action?
