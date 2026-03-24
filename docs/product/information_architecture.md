# Information Architecture

## Architecture Rule

Use enterprise-grade structure, but keep the product narrow:
planning, allocation, and exception management before and during seasonal supply execution.

## Top-Level Navigation

| Section | Purpose | Primary Users | Key Widgets Or Tables | Primary Actions | Secondary Actions | Related Modules |
| --- | --- | --- | --- | --- | --- | --- |
| `Control Tower` | Run the weekly and daily decision cycle from one place | aggregator manager, supply planner, executive | KPI strip, alert rail, action queue, scenario highlights, risk heatmap, bottleneck panel | open exception, assign owner, approve plan change, compare scenario | export review pack, open linked object | all modules |
| `Demand` | Understand demand shape before supply is committed | supply planner, buyer account manager, executive | buyer forecast table, crop-week demand graph, demand change feed, concentration chart | update forecast, lock demand assumption, flag demand anomaly | export buyer summary | Buyers, Analytics |
| `Plans` | Build and revise production commitments | supply planner, grower/network manager | production plan board, crop calendar, yield forecast cards, scenario compare | create plan, revise quantity, shift timing, approve plan | clone scenario, add note | Allocation, Risk |
| `Allocation` | Match expected supply to buyer demand | supply planner, aggregator manager | allocation table, shortfall queue, surplus queue, buyer priority view | allocate, reallocate, reserve supply, escalate shortage | export commitment sheet | Control Tower, Workflows |
| `Network` | Manage growers, farms, and sites as planning assets | grower/network manager, planner | grower cards, farm-site map, reliability table, crop roster | update capacity, change status, add partner note | review certifications, import roster | Plans, Risk |
| `Risk` | Centralize disruptions and exposure | supply planner, ops manager, executive | risk register, weather feed, crop-risk map, service exposure table | acknowledge event, change severity, trigger mitigation, open task | subscribe to alert, add manual note | Weather, Workflows |
| `Operations` | Track execution signals that affect planning quality | ops manager, logistics coordinator, planner | harvest readiness board, shipment status, available supply view, bottleneck tracker | update harvest status, confirm shipment, adjust available supply | log issue, export pick list | Logistics, Inventory |
| `Analytics` | Show outcomes, trends, and forecast quality | executive, finance/admin, planner | fill-rate trend, emergency-buy trend, forecast-vs-actual, grower scorecard | save report, compare season, investigate variance | export board deck | all modules |
| `Workflows` | Turn insight into owned action | supply planner, manager, ops users | task queue, approvals inbox, exception board, change log | assign task, approve/reject change, close issue | add comment, reopen issue | Control Tower, Risk |
| `Admin` | Keep data, permissions, and assumptions clean | admin, finance/admin, data steward | import status, lookup tables, role settings, audit log | import file, resolve SKU, edit threshold, manage access | review stale data | all modules |

## Submodule Map

- `Demand`
  - Demand Intelligence
  - Buyers / Accounts / Order Patterns
- `Plans`
  - Production Planning
  - Yield Forecasting
  - Scenarios
- `Allocation`
  - Supply Allocation
  - Service Priority Rules
- `Network`
  - Farms / Growers / Sites
- `Risk`
  - Risk Management
  - Weather + Disruption Monitoring
- `Operations`
  - Operations / Execution
  - Logistics / Delivery Coordination
  - Inventory / Harvest / Available Supply
- `Workflows`
  - Tasks / Exceptions / Approvals

## Drill-Down Hierarchy

- `Control Tower` -> `Exception` -> linked `buyer`, `crop`, `week`, `site`, and `task`
- `Demand` -> `Buyer account` -> `crop demand pattern` -> `weekly forecast line`
- `Plans` -> `Production plan` -> `site commitment line` -> `yield assumption`
- `Allocation` -> `Crop-week gap` -> `buyer allocation choices` -> `approval history`
- `Network` -> `Grower` -> `farm/site` -> `crop roster` -> `performance history`
- `Risk` -> `Risk event` -> `impacted objects` -> `mitigation tasks`
- `Operations` -> `Harvest or shipment event` -> `affected allocations` -> `service outcome`

## Role-Based Default Workspaces

| Role | Default Landing | Secondary Sections | Hidden By Default |
| --- | --- | --- | --- |
| Aggregator manager | Control Tower | Allocation, Risk, Workflows | raw imports, advanced settings |
| Supply planner | Control Tower | Demand, Plans, Allocation, Risk | finance details beyond risk exposure |
| Buyer account manager | Demand | Control Tower, Allocation | agronomic inputs, site-level detail |
| Grower/network manager | Plans | Network, Risk | buyer margin detail |
| Ops manager | Operations | Control Tower, Risk, Workflows | long-range scenario tools |
| Logistics coordinator | Operations | Workflows | buyer history, scenario planning |
| Finance/admin | Analytics | Admin, Control Tower | field operations detail |
| Executive/owner | Control Tower | Analytics | raw line items unless drilling down |

## Executive Control Tower Layout

### Page zones

1. Global filter bar
   - season
   - week horizon
   - crop group
   - buyer segment
   - geography or site cluster
2. KPI strip
   - current season coverage
   - demand at risk
   - overage exposure
   - buyer service confidence
   - data freshness
3. Exceptions and action column
   - critical alerts
   - this week actions
   - approvals waiting
4. Plan intelligence band
   - current scenario vs alternatives
   - recent plan changes
   - top bottlenecks
5. Outcome and drift panels
   - forecast vs actual
   - fill-risk by buyer
   - risk heatmap by crop and week

## Control Tower Widget Specs

| Widget | Exact Purpose | Why It Matters | Visualization | Click Behavior | Level | Decisions Supported |
| --- | --- | --- | --- | --- | --- | --- |
| `Season Coverage` | Show weighted expected supply coverage for active crop-weeks | Gives one fast health read on whether the season plan is fundamentally undercommitted or overbuilt | KPI card with trend sparkline | opens Allocation filtered to uncovered or surplus weeks | summary | tighten or relax commitments |
| `Demand At Risk` | Quantify pounds and margin tied to risk-flagged crop-weeks | Puts urgency on shortage exposure, not just alert count | KPI card | opens Risk desk filtered to shortage exposure | actionable summary | escalate grower outreach, buyer conversation |
| `Overage Exposure` | Show expected surplus volume and margin risk | Prevents the dashboard from being shortage-only | KPI card | opens surplus queue in Allocation | actionable summary | pull demand forward, reduce planting, find alternate buyers |
| `Buyer Fulfillment Confidence` | Rank or color buyers by expected fill confidence | Buyers drive retention and pilot ROI | heatmap or ranked table | opens Buyer account detail | actionable | protect key accounts first |
| `High-Risk Crops / Sites` | Identify top crop-site combinations by risk severity | Makes the risk concrete enough to act on | ranked list | opens Network or Plan line | actionable | inspect weak assumptions or vulnerable sites |
| `Critical Alerts` | Surface the exceptions that need human review now | Prevents users from scanning the whole system for trouble | alert rail with severity badges | opens linked risk event or task | actionable | triage and assign owners |
| `This Week Tasks` | Show owner-assigned actions due before next planning review | Insight is wasted without ownership | task list | opens task board | actionable | clear blockers before demand or harvest windows close |
| `Plan Change Feed` | Show recently edited plan lines, approvals, and reversals | Operators need auditability and context before making another change | chronological feed | opens change log or plan version | summary to actionable | confirm whether plan drift is controlled |
| `Scenario Comparison Highlights` | Compare base plan against conservative and aggressive alternatives | Lets management choose posture instead of arguing from memory | comparison cards | opens full scenario workspace | summary to actionable | commit to a scenario and lock assumptions |
| `Top Bottlenecks` | Show the main operational constraints hurting plan confidence | Planning quality degrades when labor, harvest windows, or logistics fail | ranked constraint table | opens Operations detail | actionable | re-sequence work or reduce commitments |
| `Forecast Drift` | Compare current forecast against actual demand or latest updates | Keeps the system honest and improves future trust | variance chart | opens Analytics variance page | summary | revise assumptions and confidence levels |
| `Data Confidence` | Show stale inputs, unresolved SKUs, missing grower updates, and manual overrides | Planning software fails when users trust bad inputs | scorecard or banner | opens Admin / Data Quality | actionable | clean inputs before approving decisions |

## Usability Rules

- Show one primary action per panel. Extra actions live in overflow or drill-down.
- Default filters to the current season and active decision horizon, not all history.
- Put severe exceptions above charts.
- Collapse advanced assumptions, raw imports, and audit details until the user drills down.
- Use the same color logic everywhere:
  - red = shortage or service risk
  - amber = review or uncertainty
  - green = healthy coverage
  - blue = neutral baseline
- Keep entity pages shallow:
  - page overview
  - current exceptions
  - history tab
  - attachments or notes tab
- AI suggestions should appear as recommended next steps, never as the only visible state.
