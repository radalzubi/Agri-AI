# Fieldline

Fieldline is an AI-native agricultural supply planning startup focused on one narrow problem:
turning buyer demand into pre-season production decisions before inventory exists.

This repository is the operating workspace for:

- business strategy and venture positioning
- pilot design and field execution
- product definition
- research and market validation
- reusable prompts for Claude and Codex
- Linear planning structure

## Current Wedge

The initial target is not the individual farmer.
The target is the buyer-facing aggregator, food hub, or regional produce operator that must translate uncertain buyer demand into grower commitments.

Core outcome:

- reduce supply shortfalls
- reduce overplanting and waste
- improve fill rate on planned demand
- lower emergency buy activity

## What We Are Building First

The first version is a planning layer, not a full ERP and not a generic AI assistant.

Initial scope:

- collect buyer demand history
- map demand by crop and week
- compare demand against grower capacity
- flag shortage and overage risk before planting
- generate weekly operator-facing recommendations

## Repository Layout

- `docs/business/` venture framing, economics, and strategy
- `docs/pilot/` pilot plans, execution notes, and success criteria
- `docs/product/` product scope, workflows, and requirements
- `docs/research/` market, customer, and competitor findings
- `prompts/claude/` execution prompts for Claude
- `prompts/codex/` review and implementation prompts for Codex
- `linear/` board structure and workstream organization

## Operating Principle

Do not overbuild.

If a workflow can be validated with spreadsheets, operator judgment, and a lightweight interface, validate it there first.
Only productize after a real customer pays for the outcome.
