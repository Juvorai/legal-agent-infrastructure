# chutes-routing

Central Chutes lane-routing configuration for all Juvor.ai legal agents.

## How it works

- `lanes.json` is the single source of truth for lane -> model assignments, consumed at runtime by the `chutes-model-routing` skill installed on each agent (`scripts/route_llm.py`).
- Each agent fetches this file (raw.githubusercontent.com, cached <= 24h, structurally validated). If the fetch fails, the agent uses its cached copy; if that fails, its bundled fallback table. Agents never break when this repo is unreachable.
- The live Chutes catalog (`GET https://llm.chutes.ai/v1/models`) controls model availability. This file controls lane purpose and quality tier. A model listed here but absent from the live catalog is skipped in favor of the lane's fallbacks.
- Skill files on individual agents never need updating when models change. Only this file changes.

## Governance

Maintained by **Juvor.ai-Legal-Ops** (central coordinator agent, https://www.gumloop.com/agents/w2cGii2yfj3UphB8EZ5nWn) under a weekly catalog-watch schedule plus on-demand runs.

Coordinator procedure (full runbook in `COORDINATOR.md`):
1. Diff `GET /v1/models` against `lanes.json`.
2. Evaluate candidates for promotion/demotion (quality floor first, then cost/latency/context).
3. Auto-promotion is authorized for ALL lanes without human sign-off (per Benjamin Snipes, 2026-09-11). Every change is still committed with a descriptive message, logged in `CHANGELOG.md` here, and reported to Ben.
4. Never route to a model merely because it is newer. Catalog recency does not establish superiority.
5. Rollback = revert the commit. Agents pick up the reverted file within 24h (or immediately with `route_llm.py lanes --refresh`).

## Consuming agents

- Chutes_GC_Agent (formerly Chutes_Legal_Privileged) (https://www.gumloop.com/agents/gWFwHxE4rrdUuXinu8BbjS)
- Molecule_Legal_Privileged (https://www.gumloop.com/agents/qFb8CuAd8vbKUbBWXZvyBh)
- Juvor.ai-Legal-Ops (https://www.gumloop.com/agents/w2cGii2yfj3UphB8EZ5nWn)

## Files

- `lanes.json` - the live configuration (schema_version 1)
- `lanes.schema.json` - JSON Schema for validation
- `COORDINATOR.md` - Juvor.ai-Legal-Ops runbook for catalog watch, evaluation, promotion, and rollback
- `CHANGELOG.md` - every routing change with date, agent, reason, and evidence
