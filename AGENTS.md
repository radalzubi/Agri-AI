# AGENTS.md

## Project Purpose

Agri-AI is a new venture repository for an agricultural supply planning business.
The repo exists to organize business research, product boundaries, pilot planning, GTM decisions, workflow prompts, and operating instructions.

The core venture thesis:

build a planning layer that helps buyer-facing agricultural operators decide what to produce, when to produce it, and how much to commit before inventory exists.

## Separation Rule

This project is completely separate from Wasel.

- do not reference Wasel logic, product decisions, code, or operations
- do not reuse Wasel naming, workflows, or assumptions
- if a comparison is necessary, keep it to one sentence and only to maintain separation

## Expected Writing Style

Write like an operator, not a marketer.

- concise
- structured
- specific
- execution-oriented
- low-fluff
- commercially grounded

Avoid:

- generic startup clichés
- inflated AI language
- bloated strategy memos
- repeating the same idea across multiple files

## Folder Conventions

- `docs/business/` venture framing, business model, GTM, and strategic direction
- `docs/research/` market notes, competitor analysis, validation findings, and source-backed insight
- `docs/pilot/` pilot plans, outreach logic, success metrics, and execution cadence
- `docs/product/` MVP boundaries, workflow scope, and product decisions
- `prompts/claude/` reusable prompts for research, issue execution, and repo editing
- `prompts/codex/` reusable prompts for review, structuring, and converting notes into durable docs
- `linear/` board setup, issue flow, and operating rules for task coordination

## Workflow Between GitHub, Linear, Codex, and Claude

- GitHub holds durable knowledge and final decisions
- Linear tracks active work and issue-level execution
- Claude handles research, refinement, synthesis, and issue execution drafts
- Codex reviews, structures, integrates, and upgrades outputs into the permanent repo

Working rule:

1. research or issue work starts in Linear or a prompt-driven session
2. Claude produces draft analysis, options, or issue output
3. Codex reviews the output critically
4. only strong work gets promoted into repo docs
5. GitHub remains the final source of truth

## Documentation Rules

- keep business docs concise, structured, and execution-oriented
- use headings and compact bullets
- put each idea in the correct file instead of dumping everything into one document
- update an existing file before creating a duplicate
- if a topic becomes too large, split it into a focused research or product note

## Product Discipline

Early-stage Agri-AI work should stay focused on:

- the aggregator or buyer-facing operator wedge
- pre-season planning
- shortage and overage risk visibility
- manual-first validation

Do not expand early docs into:

- full ERP scope
- marketplace claims without proof
- lending or fintech execution
- generic farm software positioning
