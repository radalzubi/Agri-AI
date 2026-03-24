# Agri-AI

Agri-AI is an agricultural supply planning venture focused on one narrow problem:
helping farms, aggregators, and buyer-facing produce operators decide what to produce, when to produce it, and how much to commit before inventory exists.

## Problem

Specialty-crop supply chains break before harvest.

Buyer demand is uneven.
Grower commitments are made with incomplete information.
Aggregators absorb the mismatch through shortages, emergency buys, substitutions, and waste.

Most current tools handle inventory, ordering, or farm operations after supply is already in motion.
Agri-AI is focused earlier than that:
pre-season and in-season production planning.

## Who It Is For

Primary target:

- regional food hubs
- specialty produce aggregators
- buyer-facing produce distributors
- local sourcing operators coordinating multiple growers for recurring buyers

Secondary users:

- growers participating in those supply networks
- operators managing buyer demand, grower capacity, and seasonal supply risk

## What Makes It Different

Agri-AI is not a generic ERP.
It is not warehouse software.
It is not a post-harvest traceability system.

It is a planning layer that helps operators answer:

- what should be grown
- how much should be committed
- when the commitment should happen
- where shortage and overage risk will appear

## System Of Work

This repository is the source of truth for venture work.

- GitHub = source of truth for business docs, research, strategy, product scope, and prompts
- Linear = task coordination and execution tracking
- Codex = builder, reviewer, document structurer, and repo maintainer
- Claude = researcher, refiner, issue executor, and synthesis engine

## Repository Layout

- `docs/business/` venture framing, economics, GTM, and operating direction
- `docs/research/` market notes, competitor analysis, and validation findings
- `docs/pilot/` pilot design and execution planning
- `docs/product/` MVP boundaries and product decisions
- `prompts/claude/` reusable execution prompts for Claude
- `prompts/codex/` reusable review and repo-structuring prompts for Codex
- `linear/` Linear workflow and board structure

## Working Principle

Keep the company thesis sharp and the repo clean.

- prefer execution-ready docs over long essays
- validate with manual workflows before building software
- avoid bloated AI claims early
- keep all strategy tied to a real customer wedge
