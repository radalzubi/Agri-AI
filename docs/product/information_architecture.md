# Information Architecture

## Architecture Rule

Keep the top-level shell tight, analytical, and decision-first.

Agri-AI should look like a planning command center, not a sprawling ERP tree.
The shell must stay small enough for repeat weekly use and expressive enough to scale later.

## Top-Level Product Structure

| Section | Exact Purpose | Main Users | Decisions Supported | What Belongs Here | What Does Not Belong Here |
| --- | --- | --- | --- | --- | --- |
| `Control Tower` | Run the weekly planning review from one workspace | supply planner, aggregator manager, executive | what needs intervention now, where exposure is concentrated, what deserves follow-up | KPI strip, action board, exception queues, coverage heatmap, briefing, trust status | raw import tables, long admin forms, future-only workflow objects |
| `Planning` | Translate exposure into commitment posture | supply planner, grower/network manager, aggregator manager | what to commit now, what to rebalance, what to watch | shortage queue, overage watch, planning posture, crop-week detail, recommendation logic | buyer CRM, warehouse activity, fake scenario modeling |
| `Demand` | Understand crop-week demand shape and coverage patterns | supply planner, buyer/account manager, executive | where demand clusters, where supply diverges, which crop needs deeper review | crop demand vs supply charts, crop summary, weekly balance, focus crop detail | grower records, logistics events, admin settings |
| `Operations` | Support the weekly handoff from planning to execution review | aggregator manager, ops manager, executive | what the team should review this week, what needs escalation, what gets shared in meeting cadence | memo, review pack, action summary, output readiness, current assumptions | live dispatch, route optimization, inventory management |
| `Intelligence` | Centralize exception analysis and data trust | supply planner, data steward, executive | whether the plan is trustworthy enough to act on, which issues are real vs input-driven | risk register, unresolved inputs, data confidence, file freshness, blocker summary | decorative analytics, fake predictive layers, unsupported commercial metrics |
| `Admin` | Show setup assumptions and operating contract for the local tool | data steward, admin, founder/operator | whether the local tool is configured and run correctly | output file status, thresholds, glossary, usage rules, data contract | deep product settings, role management UI, enterprise config trees |

## MVP Navigation

The current MVP code should expose the same six top-level sections, but with uneven depth:

- `Control Tower` is the primary screen.
- `Planning`, `Demand`, `Operations`, and `Intelligence` are real supporting workspaces.
- `Admin` stays thin and operational.

This preserves architectural truth without pretending later modules already exist.

## Future Supporting Subviews

These should live under the shell later, not as immediate top-level clutter:

- buyers / accounts
- farms / sites / growers
- scenarios
- approvals
- tasks / exceptions
- weather events
- allocation changes
- historical performance

## Drill-Down Model

### MVP drill path

- `Control Tower` -> `exception card` -> `crop-week focus detail`
- `KPI` -> filtered queue or filtered heatmap state
- `heatmap cell` -> focused crop-week detail
- `crop summary row` -> crop-level weekly view
- `memo highlight` -> supporting queue or chart
- `data confidence issue` -> unresolved row or affected week

### Focus-detail contract

Every crop-week detail view should answer:

- demand
- supply
- coverage
- shortage or overage magnitude
- recommended next move
- whether trust is reduced by unresolved inputs

## Control Tower Layout

### Zone A: Context bar

- role lens
- season
- crop scope
- week horizon
- output freshness
- data confidence

### Zone B: Health strip

- weighted coverage
- demand at risk
- overage exposure
- risk-flagged crop-weeks
- trust blocker count

### Zone C: Immediate action board

- shortage-first decision queue
- overage watch
- derived action queue

### Zone D: Exposure map

- crop x week heatmap
- focus crop-week detail

### Zone E: Diagnostics

- weekly balance trend
- crop concentration summary
- planning posture summary

### Zone F: Insight rail

- weekly briefing
- trust warnings
- output readiness

## Role-Based Defaults

| Role | Default Landing | Emphasis | Hidden By Default |
| --- | --- | --- | --- |
| `Supply planner` | Control Tower | shortage queue, focus detail, demand coverage | admin status detail, long memo text |
| `Aggregator manager` | Control Tower | demand at risk, overage watch, briefing, next actions | raw unresolved rows unless blocking a key decision |
| `Executive` | Control Tower | KPI strip, briefing, trust status, top exceptions | dense tables until drilling deeper |
| `Data steward` | Intelligence | unresolved inputs, freshness, trust blockers | exposure charts unless tied to a blocker |
| `Buyer/account manager` | Demand | crop demand shape, risk weeks, review summary | admin, field detail, fake account analytics |
| `Ops manager` | Operations | weekly review pack, action handoff, readiness status | broad diagnostic tables unrelated to current meeting cadence |

## Design Rules

- summary before diagnosis
- diagnosis before raw tables
- keep filters visible
- keep crop and week context visible while drilling down
- do not promote unsupported modules into the main shell
- if a panel does not influence a real decision, demote it
