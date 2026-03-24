# User Roles And Workflows

## User Roles

| Role | Core Goal | Daily / Weekly Decisions | Ideal Landing View | What Must Be Visible | What Should Stay Hidden |
| --- | --- | --- | --- | --- | --- |
| `Supply planner` | turn crop-week exposure into commitments | where to intervene, what to commit, what to monitor | Control Tower | shortage queue, focus detail, planning posture, demand coverage | admin detail, fake scenario controls |
| `Aggregator manager` | keep the season commercially stable | which shortages to escalate, which overages to rebalance, what the team should do next | Control Tower | demand at risk, overage watch, briefing, next actions | raw unresolved rows unless blocking a decision |
| `Executive` | judge season health quickly | is the plan acceptable, where is risk concentrated, can current data be trusted | Control Tower | KPI strip, briefing, trust status, top exceptions | dense operational tables by default |
| `Data steward` | keep the planning view trustworthy | which unresolved items block the current review, whether outputs are fresh | Intelligence | unresolved inputs, freshness, blocker impact | wide planning diagnostics unless tied to a blocker |
| `Buyer/account manager` | understand demand pressure | which crop demand patterns matter, where shortage affects service | Demand | crop trends, coverage, review summary | admin, farm/site detail, unsupported buyer analytics |
| `Operations manager` | support weekly review handoff | what the operating team needs to know this week | Operations | memo, action summary, readiness state | speculative planning modules |
| `Grower/network manager` | prepare for future partner-facing planning depth | which crop commitments need partner follow-up | Planning | planning posture, crop-week focus detail | buyer-side analytics |
| `Finance/admin` | keep assumptions and outputs understandable | whether the local tool is run correctly and what limits the numbers have | Admin | file status, thresholds, glossary | raw planning tables not tied to setup |

## MVP Role Notes

- Real MVP role modes in code:
  - supply planner
  - aggregator manager
  - executive
  - data steward
- Additional roles are documented now so later product expansion has a coherent frame.

## Key Workflows

### 1. Review weekly production recommendation

- Trigger: standing weekly review
- User: supply planner
- Steps:
  1. open Control Tower
  2. scan KPI strip and trust status
  3. review commit-now shortage queue
  4. focus the most exposed crop-week
  5. move into Planning if deeper posture review is needed
- Main screens:
  - Control Tower
  - Planning
- Outputs:
  - clear decision on what needs commitment follow-up
- UX pitfall to avoid:
  - forcing the planner to open charts before seeing the action queue

### 2. Investigate risk buildup

- Trigger: high shortage exposure or trust warning
- User: supply planner or executive
- Steps:
  1. open Control Tower or Intelligence
  2. inspect risk register or coverage heatmap
  3. focus a crop-week
  4. determine whether the issue is real exposure or weak input quality
- Main screens:
  - Control Tower
  - Intelligence
- Outputs:
  - escalation, monitor, or data-cleanup decision
- UX pitfall to avoid:
  - separating data quality from the exposed crop-week

### 3. Adjust production plan

- Trigger: shortage or overage concentration
- User: supply planner
- Steps:
  1. open Planning
  2. review posture buckets
  3. inspect shortage and overage queues
  4. focus the relevant crop-week
  5. note the required follow-up
- Main screens:
  - Planning
  - Demand
- Outputs:
  - commit now, rebalance, or monitor posture
- UX pitfall to avoid:
  - pretending true editable plan objects exist before the data model supports them

### 4. Reallocate supply across buyers

- Trigger: shortage exposure on a key crop-week
- User: aggregator manager
- Current MVP state:
  - not fully supported in code
- MVP behavior:
  - identify the crop-week and flag the need for manual commercial review
- Future outputs:
  - buyer-facing reallocation workflow

### 5. Resolve shortages / surpluses

- Trigger: exposure crosses threshold
- User: supply planner or aggregator manager
- Steps:
  1. review shortage queue or overage watch
  2. inspect focus detail
  3. use Demand to understand season shape
  4. use Operations to prepare review handoff
- Outputs:
  - follow-up decision and weekly review action
- UX pitfall to avoid:
  - giving equal visual weight to shortages and surpluses all the time

### 6. Respond to weather disruption

- Trigger: future weather or disruption feed
- User: supply planner, grower/network manager
- MVP state:
  - deferred
- Future screens:
  - Intelligence
  - Planning

### 7. Review forecast vs actual

- Trigger: later analytics maturity
- User: executive, planner, finance/admin
- MVP state:
  - deferred
- Future screens:
  - Demand
  - Intelligence
  - Analytics extension

### 8. Run weekly operations review

- Trigger: weekly meeting
- User: aggregator manager or executive
- Steps:
  1. open Operations
  2. review briefing and output readiness
  3. review top shortage and overage items
  4. use memo as the meeting narrative
- Outputs:
  - meeting-ready review pack
- UX pitfall to avoid:
  - making users build the review manually from multiple tabs

### 9. Turn exceptions into tasks

- Trigger: later persistent workflow support
- User: all internal users
- MVP state:
  - action queue is derived, not persistent
- Future extension:
  - Planning and Intelligence should create persistent tasks with inherited context
