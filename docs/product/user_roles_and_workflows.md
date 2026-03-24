# User Roles And Workflows

## User Roles

| Role | Main Goal | What They Need To See First | Daily / Weekly Decisions | Critical Data And Actions | Hide By Default |
| --- | --- | --- | --- | --- | --- |
| `Aggregator manager` | Keep the season commercially stable | Control Tower with shortage exposure, buyer confidence, approvals, and top tasks | approve plan changes, resolve tradeoffs between buyers, escalate bottlenecks | season coverage, demand at risk, key accounts, open approvals | raw imports, SKU lookup tables, low-level site metrics |
| `Supply planner` | Turn demand into workable grower commitments | Control Tower plus crop-week risk queue | adjust production plans, reallocate supply, choose scenarios, open tasks | crop-week gaps, scenarios, yield assumptions, allocation table | finance settings, low-signal admin logs |
| `Buyer account manager` | Protect buyer service levels and demand quality | Demand workspace with buyer change feed and allocation risk | confirm buyer demand, negotiate substitutions, escalate at-risk orders | buyer forecast, service tier, affected weeks, recommended account actions | site-level agronomic detail, deep admin settings |
| `Grower / network manager` | Keep grower commitments realistic and current | Plans and Network workspaces | confirm capacity, update constraints, compare grower reliability, flag field issues | grower roster, site capacity, crop calendars, reliability notes | buyer margin detail, broad executive analytics |
| `Field manager` | Convert site conditions into credible yield expectations | Site-level plan and risk view | update yield estimate, note disease or labor risk, adjust harvest readiness | yield forecast, weather risk, labor constraints, plan variance | buyer hierarchy, corporate reporting |
| `Operations manager` | Keep in-season execution from degrading the plan | Operations workspace with harvest, shipment, and bottleneck status | resolve bottlenecks, sync available supply, escalate service risk | harvest readiness, cold storage, outbound issues, open tasks | long-horizon scenario tools |
| `Logistics coordinator` | Protect delivery commitments once product moves | Operations or Logistics view | confirm loads, change delivery timing, flag route or cold-chain issues | shipment schedule, buyer windows, source locations, exception queue | pre-season planning assumptions, broad analytics |
| `Finance / admin` | Validate economic outcomes and data hygiene | Analytics and Admin | review margin at risk, validate pricing assumptions, clean imports, manage roles | financial exposure, season outcomes, audit log, lookup tables | field-level operational details unless tied to margin |
| `Executive / owner` | Make strategic calls quickly | Executive Control Tower | approve scenario posture, allocate resources, review pilot outcome, assess account risk | fill confidence, revenue or margin at risk, pilot KPIs, plan-change summary | raw line items unless drilling down |
| `Farm owner / operator contributor` | Confirm what they are expected to grow and flag constraints | Limited partner workspace, not the full internal dashboard | accept or challenge commitments, share risk notes, confirm capacity updates | assigned commitments, crop windows, required actions, communication log | buyer list, account pricing, internal approvals |

## Role Notes

- MVP internal users: aggregator manager, supply planner, executive, and a lightweight data steward role.
- Phase 2 users: buyer account manager, grower/network manager, field manager, operations manager.
- Phase 3 users: logistics coordinator, finance/admin depth, and external farm contributor portal.

## Key Decision Workflows

### 1. Review buyer demand trends

- Starting point: `Control Tower` or `Demand`
- User: buyer account manager or supply planner
- Trigger: weekly planning review, sudden buyer increase, or forecast drift alert
- Steps:
  1. open the buyer change feed
  2. review crop-week demand deltas and concentration risk
  3. inspect affected crops and required service levels
  4. confirm whether change is real, seasonal, or a one-off
- Key screens: buyer account page, demand trend chart, crop-week table
- Decision points: lock forecast, request clarification, or downgrade confidence
- Outputs: updated demand forecast, buyer notes, optional follow-up task
- Good UX: show change magnitude, affected weeks, and top impacted supply lines on one screen

### 2. Adjust production plans

- Starting point: `Plans`
- User: supply planner
- Trigger: new forecast, grower update, or scenario review
- Steps:
  1. review uncovered or surplus crop-weeks
  2. inspect production plans by crop and site
  3. edit planned quantities or harvest timing
  4. compare updated plan against scenario benchmarks
- Key screens: production plan board, crop calendar, scenario compare
- Decision points: increase commitments, reduce commitments, or leave unchanged
- Outputs: plan revision, version log entry, optional approval request
- Good UX: preserve side-by-side before and after values with an explicit reason field

### 3. Respond to weather risk

- Starting point: `Risk`
- User: supply planner, field manager, or grower/network manager
- Trigger: weather event or site-level risk spike
- Steps:
  1. open the event card
  2. review impacted crops, weeks, and sites
  3. inspect exposed buyer allocations
  4. choose mitigation actions
- Key screens: weather event detail, impacted plan lines, allocation exposure
- Decision points: revise yield forecast, move demand, trigger buyer warning, or monitor only
- Outputs: updated risk severity, tasks, revised forecast inputs
- Good UX: event detail must show exactly which crop-weeks and buyers are at risk, not just a weather headline

### 4. Reallocate supply across buyers

- Starting point: `Allocation`
- User: supply planner or aggregator manager
- Trigger: shortage exposure, priority buyer request, or late supply loss
- Steps:
  1. open the crop-week shortfall queue
  2. review service tier, margin, and buyer obligations
  3. simulate alternative allocations
  4. approve the chosen allocation
- Key screens: allocation table, buyer priority panel, scenario strip
- Decision points: protect key buyer, split shortage, substitute product, or reduce lower-tier allocation
- Outputs: approved allocation change, buyer-facing tasks, audit trail
- Good UX: make the tradeoff explicit by showing winner, loser, and service impact before save

### 5. Spot expected shortages early

- Starting point: `Control Tower`
- User: aggregator manager or supply planner
- Trigger: routine weekly review
- Steps:
  1. scan demand at risk and high-risk crop-weeks
  2. drill into top shortages by crop and week
  3. review impacted plans, growers, and buyers
  4. assign follow-up actions
- Key screens: Control Tower, risk desk, action queue
- Decision points: escalate now, watch, or ignore due to low commercial impact
- Outputs: priority queue for the week
- Good UX: shortage severity, buyer impact, and recommended owner should appear together

### 6. Identify overproduction

- Starting point: `Control Tower` or `Allocation`
- User: supply planner or account manager
- Trigger: overage exposure alert
- Steps:
  1. review surplus crop-weeks
  2. inspect whether demand can be pulled forward or redirected
  3. assess whether production should be reduced
  4. assign follow-up with buyer or grower
- Key screens: surplus queue, demand workspace, plan board
- Decision points: sell forward, shift planting, accept controlled surplus, or find secondary outlet
- Outputs: revised plan or buyer follow-up task
- Good UX: show time remaining before surplus becomes expensive

### 7. Resolve execution bottlenecks

- Starting point: `Operations`
- User: operations manager
- Trigger: labor gap, harvest delay, cold storage issue, outbound failure
- Steps:
  1. open the bottleneck board
  2. review affected harvests, shipments, and allocations
  3. decide whether to resequence work, reduce scope, or escalate shortage risk
  4. assign owner and due date
- Key screens: operations board, linked allocations, task panel
- Decision points: operational fix versus plan revision
- Outputs: updated execution status, task assignment, optional risk event
- Good UX: every bottleneck card should list downstream buyer impact

### 8. Approve plan changes

- Starting point: `Workflows`
- User: aggregator manager or executive
- Trigger: planner submits plan revision or scenario change
- Steps:
  1. open approval inbox
  2. compare old state and proposed state
  3. review reason, risk impact, and buyer effect
  4. approve, reject, or request changes
- Key screens: approval card, diff view, linked control tower metrics
- Decision points: accept risk posture or send back for revision
- Outputs: approved plan version or rejection note
- Good UX: approvals need a tight diff, not a full page of raw tables

### 9. Assign follow-up tasks

- Starting point: any exception or plan line
- User: any internal user
- Trigger: issue needs a named owner
- Steps:
  1. click create task from the linked object
  2. assign owner, due date, and priority
  3. attach context automatically
  4. close when resolved
- Key screens: embedded task drawer, workflow board
- Decision points: who owns it and when it is due
- Outputs: task record with linked source object
- Good UX: task creation should never require retyping the crop, week, buyer, or site context

### 10. Compare forecast versus actual

- Starting point: `Analytics`
- User: executive, planner, finance/admin
- Trigger: weekly review or season-end retrospective
- Steps:
  1. open forecast variance by crop, buyer, and week
  2. isolate major misses
  3. review whether the miss came from demand, yield, or execution
  4. update assumptions for the next cycle
- Key screens: analytics variance page, demand and plan history
- Decision points: change forecast method, change confidence, retrain heuristics, or fix process
- Outputs: updated planning assumptions, lessons logged
- Good UX: variance should always be decomposed by cause, not just displayed as a number

### 11. Evaluate farm or grower performance

- Starting point: `Network` or `Analytics`
- User: grower/network manager or executive
- Trigger: pre-season planning, partner review, or repeated service failures
- Steps:
  1. open grower scorecard
  2. review delivery reliability, yield accuracy, issue history, and crop performance
  3. compare against alternative growers or sites
  4. decide how much future volume to route to that partner
- Key screens: grower detail, scorecard, crop history
- Decision points: increase reliance, keep flat, or reduce planned volume
- Outputs: partner note, reliability score update, next-season planning change
- Good UX: use a short scorecard with reasons, not a generic CRM timeline

### 12. Prepare the weekly operations review

- Starting point: `Control Tower`
- User: aggregator manager or supply planner
- Trigger: standing weekly meeting
- Steps:
  1. review critical alerts, demand at risk, overage exposure, and tasks due
  2. compare current scenario against last week
  3. walk through top shortages and bottlenecks
  4. export or share the review pack
- Key screens: Control Tower, action queue, memo summary
- Decision points: what changed, what needs approval, and who owns follow-up
- Outputs: meeting-ready summary, refreshed task list, approved changes
- Good UX: the review pack should come from one screen instead of a manual slide assembly process
