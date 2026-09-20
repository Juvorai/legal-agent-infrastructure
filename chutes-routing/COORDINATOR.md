# COORDINATOR.md - Juvor.ai-Legal-Ops routing governance runbook

Juvor.ai-Legal-Ops is the central coordinator for Juvor.ai company legal agents
(Chutes_GC_Agent, Molecule_Legal_Privileged, and any future agents that
install the chutes-model-routing skill). It owns `chutes-routing/lanes.json` in
this repository. Consuming agents read the file at runtime; they never need
skill-file updates when Chutes models change.

## Authority

Per Benjamin Snipes (2026-09-11): Juvor.ai-Legal-Ops may auto-promote and
demote models in ALL lanes (A through H) without human sign-off. Every change
must still satisfy the quality floor below, be committed with a descriptive
message, be logged in CHANGELOG.md, and be reported to Ben (summary of what
moved, which lanes, evidence, rollback commit).

## Schedule

Weekly catalog watch (Monday 09:00 America/New_York) plus on-demand runs when
Ben or another agent requests a routing review.

## Procedure (each run)

1. FETCH. `GET https://llm.chutes.ai/v1/models` (CHUTES_API_KEY). Record model
   IDs, context limits, modalities, prices, feature flags, confidential_compute.
2. LOAD current `chutes-routing/lanes.json` from this repo (github get_contents).
3. DIFF. Identify:
   - New models not referenced anywhere in lanes.json.
   - Lane primaries or fallbacks that are no longer live (delisted).
   - Price moves > 25% on any lane primary.
   - Context-limit or modality changes on lane primaries.
   - confidential_compute flag changes (treat any loss of the flag on a lane
     primary as an immediate demotion: privileged material must not route to a
     model without confidential_compute=true).
4. EVALUATE candidates before any promotion:
   - Quality floor first: run the lane's representative eval set (extraction
     accuracy, unsupported-claim rate, quotation fidelity, schema compliance,
     tool-call correctness) against incumbent and candidate on identical inputs.
     If no eval set exists for the lane yet, build a small one (10-20
     synthetic-safe items) before promoting.
   - Then cost, latency, context, and reliability.
   - A candidate must meet the lane's quality floor AND improve at least one of
     quality, cost, latency, context, or reliability. Never promote merely
     because a model is newer or has a higher version number.
   - Lane E (Kimi-class maximum quality) keeps its escalation gates regardless
     of price changes; a price drop does not move Kimi-class models into the
     default path.
5. COMMIT. Update lanes.json (bump updated_at, set updated_by to
   "Juvor.ai-Legal-Ops: <reason>"), commit via github create_or_update_file with
   a descriptive message, and append a CHANGELOG.md entry in the same commit.
6. VERIFY. Re-fetch the raw URL
   (https://raw.githubusercontent.com/Juvorai/legal-agent-infrastructure/main/chutes-routing/lanes.json),
   validate against lanes.schema.json, and run
   `route_llm.py lanes --refresh` locally to confirm every lane resolves.
7. REPORT. Post a summary to Ben: what moved, which lanes, eval evidence,
   commit SHA, and the revert command. If a lane primary was delisted and an
   emergency fallback took over, say so explicitly.

## Hard rules

- The live catalog controls availability; lanes.json controls purpose. Never
  assign a lane primary that is not live on the catalog (the router skips it,
  but the config should not carry dead IDs except as documented pending launches).
- Confidentiality gate: any lane that can receive privileged or confidential
  material (all of them, in practice) may only list models whose live catalog
  entry reports confidential_compute=true. Do not infer TEE status from names.
- Lane G critic pairing must always cross model families (Qwen <-> GLM;
  Kimi -> GLM). Never author and critique with the same checkpoint.
- Embeddings stay on a dedicated embedding model; never substitute a chat model.
- Do not change schema_version without coordinating a route_llm.py update
  across agents (schema_version 1 is what current routers validate).
- Rollback: `git revert <sha>` on the lanes.json commit. Agents converge within
  24h automatically, or immediately on `route_llm.py lanes --refresh`.

## Consuming-agent contract

Each agent's route_llm.py: fetches lanes.json (cache <= 24h) -> validates
structure -> applies. On fetch failure: cached copy. On cache failure: bundled
fallback table inside the skill. Agents therefore never hard-fail when this
repo or GitHub is unreachable, and stale-but-valid config is preferred over
no config.
