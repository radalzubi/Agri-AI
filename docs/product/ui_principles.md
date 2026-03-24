# UI Principles

## Core Philosophy

Agri-AI should feel like a premium analytical operating platform for agricultural supply planning.

The interface must be:

- dense but not chaotic
- serious but not ugly
- operational, not decorative
- analytical, not abstract
- fast for repeat weekly use

## Decision-First Rules

Every major panel must help answer one of these:

1. what should I commit
2. where am I at risk
3. what needs action now
4. what changed in the current review context
5. where do I drill deeper

If a panel answers none of them, remove it or demote it.

## Density Rules

- prefer compact panels over giant cards
- avoid dead space
- keep labels short and semantically clear
- use dense tables only after the operator knows why they are looking at them
- put exception queues ahead of exploratory charts

## Workspace Rules

- favor multi-panel workspaces over excessive page switching
- preserve context while drilling down
- keep filters and review context visible
- use a right rail for briefing, trust, and immediate follow-up
- keep one flagship diagnostic surface per module

## Hierarchy Rules

- critical shortage and trust issues come first
- overage watch comes after shortage triage
- charts explain the exposure after the action queue is clear
- memo and narrative summary should reinforce visible issues, not introduce disconnected ones

## Visualization Standards

### Use KPI strips for

- weighted season coverage
- demand at risk
- overage exposure
- risk-flagged crop-weeks
- trust blockers

### Use heatmaps for

- crop x week coverage concentration
- risk clustering across the season

### Use tables for

- shortage queues
- overage watch
- risk register
- unresolved SKU blockers
- crop summary

Tables should be:

- sortable in logic
- compact
- severity-aware
- used as operational tools, not as the full product

### Use compact trend charts for

- weekly demand vs supply balance
- selected crop detail across weeks

### Do not use

- maps without site-level data
- scenario compare visuals without scenario objects
- buyer analytics without buyer-level demand models
- operational flow diagrams without allocation objects
- predictive confidence bands without real uncertainty outputs

## Filter Rules

Default visible filters:

- season
- crop
- week range
- role lens

Advanced filters should stay secondary until the product has richer data objects.

## Role Personalization Rules

Role mode must change:

- landing view
- emphasis order
- default open panels
- visible detail level

Role mode should not only change helper copy.

## Trust Rules

- unresolved inputs must appear inline with the planning context
- stale output should downgrade confidence visibly
- rule-based recommendations must show why they were generated
- the UI should distinguish genuine exposure from weak input quality

## AI Rules

AI should appear as assistance, not theater.

Allowed in MVP:

- rule-generated recommended actions
- memo summarization
- derived planning posture

Phase 2 and later:

- scenario generation
- anomaly detection
- demand summarization by buyer
- richer explanation layers

Never ship a black-box recommendation without:

- visible drivers
- easy override
- clear confidence framing

## What To Avoid

- giant empty cards
- generic admin template layout
- cluttered ERP navigation trees
- equal visual weight for all panels
- burying the decision queue below diagnostic charts
- turning data quality into a separate back-office workflow
