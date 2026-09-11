---
name: chutes-model-routing
description: Route every LLM task through the Chutes API using lane-based model routing. Lane A (GLM 4.7 Flash) for ultra-cheap bounded ops, Lane B (Gemma 4 31B) for extraction and classification, Lane C (Qwen3.5 397B) as the default substantive text lane, Lane D (GLM 5.2) for agent planning and high-stakes synthesis, Lane E (Kimi K3) for gated maximum-quality escalation, Lane F (DeepSeek V4 Flash) for bulk million-token preprocessing, Lane G for model-family-diverse critics, Lane H (Qwen3.8 27B) for vision. Use for any Chutes call, model selection, failover, critic pairing, or embedding routing. Supersedes single-default-model policies.
icon: cpu
color: Teal
---

# Chutes Model Routing

Lane-based routing for all Chutes LLM work. Replaces any single-default-model
policy (e.g. the old `Qwen/Qwen3-235B-A22B-Thinking-2507-TEE` universal default).

## Controlling principle

Gumloop is the orchestrator. Research and authority retrieval belong to the
designated research layer (Perplexity Deep Research, Midpage, tax tools, patent
tools, EDGAR, knowledge base, or whatever domain sources the adopting agent
uses). Chutes models plan workflows, transform verified source packets, draft,
synthesize, and criticize.

The Gumloop runtime may choose tools, parse simple values, and apply
deterministic branches. It may not itself generate, summarize, classify,
extract, rewrite, translate, analyze, or synthesize substantive content. Every
such operation calls Chutes through this skill. If Chutes is unavailable,
report the failure; never silently fall back to a Gumloop model.

Use deterministic code instead of an LLM for exact string matching, arithmetic,
sorting, deduplication, schema validation, citation-link checking, and
file-format verification.

## Endpoint and confidentiality

- Endpoint: `https://llm.chutes.ai/v1` (OpenAI-compatible).
- `CHUTES_API_KEY` lives only in the approved secret store. Never in prompts,
  artifacts, checked-in config, logs, or user-visible responses.
- For confidential, privileged, personal, contractual, financial, security, or
  company information, use only a model whose live catalog entry reports
  `confidential_compute=true`. If the flag is absent or false, do not send the
  material. Do not infer TEE status from a model name alone; check the live
  flag (`route_llm.is_confidential`).

## Live catalog rule

At the start of a workflow, or from a cache no older than 24 hours, call
`GET /v1/models` (`route_llm.get_catalog()` handles the cache). The live API
response controls availability and technical limits; this policy controls model
purpose and quality tier. Do not auto-promote a newly listed model into
production; new models enter shadow evaluation first.

## Central lane configuration (fleet-wide, maintained by Juvor.ai-Legal-Ops)

The lane table in this SKILL.md and in `route_llm.py` is a bundled fallback.
The controlling configuration is `chutes-routing/lanes.json` in the
`Juvorai/legal-agent-infrastructure` GitHub repo:

- URL: https://raw.githubusercontent.com/Juvorai/legal-agent-infrastructure/main/chutes-routing/lanes.json
- `route_llm.py` fetches it at runtime (cache <= 24h in the agent workspace,
  structural validation, then bundled fallback). Resolution order:
  remote -> cache -> bundled. Agents never hard-fail when GitHub is unreachable.
- Juvor.ai-Legal-Ops (central coordinator,
  https://www.gumloop.com/agents/w2cGii2yfj3UphB8EZ5nWn) owns the file, runs a
  weekly catalog watch, and has authority to auto-promote/demote models in all
  lanes without human sign-off (per Benjamin Snipes, 2026-09-11). Runbook:
  `chutes-routing/COORDINATOR.md` in the repo.
- When Chutes adds or changes models, NO skill update is needed on consuming
  agents. The coordinator edits lanes.json; every agent converges within 24h
  or immediately via `route_llm.py lanes --refresh`.
- The lane table printed below reflects the seed config (2026-09-11). Treat
  `route_llm.py lanes` output (which shows the config source and updated_at)
  as authoritative over the static table.

## Lane table

| Lane | Primary | Fallback(s) | Use |
|---|---|---|---|
| A: ultra-cheap bounded | `GLM-4.7-Flash-NVFP4-TEE` | `google/gemma-4-31B-turbo-TEE` | Routing labels, binary relevance, normalization, tagging, metadata cleanup. Input <20K tokens, output <1K, strict JSON schema, low temperature, validate every field, retry once on schema failure, escalate after second failure. Never for legal conclusions, contract interpretation, open-ended drafting, or final client-facing prose. |
| B: extraction/structured | `google/gemma-4-31B-turbo-TEE` | `Qwen/Qwen3.8-27B-TEE` | Classification, clause extraction, triage, structured summaries, tables, citation metadata, controlled rewriting directly supported by supplied text. JSON mode whenever available; require source spans and null for absent fields; never let inferred text appear in a field labeled quote. Escalate to C for cross-document reconciliation or substantive prose. |
| C: substantive text (DEFAULT) | `Qwen/Qwen3.5-397B-A17B-TEE` | `Qwen/Qwen3.8-27B-TEE` | Drafting, rewriting, synthesis of verified research, document analysis, issue lists, memoranda from supplied sources, final prose below higher escalation conditions. Non-thinking or low/medium reasoning for straightforward drafting. |
| D: agent planning / high-stakes | `zai-org/GLM-5.2-TEE` | `Qwen/Qwen3.5-397B-A17B-TEE`, then `deepseek-ai/DeepSeek-V3.2-TEE` | Multi-step planning, sustained tool use, difficult debugging, repository-scale coding, >5 dependent actions, tool-failure recovery, >200K-token prompts, consequential final synthesis. Planning calls must return a bounded plan with success criteria, tools, artifacts, verification checks, stop and escalation conditions. The parent retains tool execution; the model never invents tool results. |
| E: maximum quality (GATED) | `moonshotai/Kimi-K3-TEE` | `zai-org/GLM-5.2-TEE` | Only when: (1) user expressly requests the strongest model, (2) high-consequence deliverable remains materially uncertain after a Lane D pass and verification, (3) synthesis across >500K usable tokens, (4) complex multimodal/long-horizon problem where Lane D failed acceptance, or (5) final adversarial review of a draft from a different model family. Never for classification, bulk extraction, routine drafting, first-pass summaries, or incomplete source packets. |
| F: bulk preprocessing | `deepseek-ai/DeepSeek-V4-Flash-0731-TEE` | `zai-org/GLM-5.2-TEE` | Preliminary extraction, corpus mapping, chronologies, candidate-issue collection over very large inputs. Every output is provisional; quotes, load-bearing facts, and final conclusions must be verified against primary text. Never the sole author of final work product. |
| G: diverse critic | resolved per author | `deepseek-ai/DeepSeek-V3.2-TEE` | Qwen author -> GLM 5.2 critic; GLM author -> Qwen3.5 397B critic; Kimi author -> GLM 5.2 critic. Critic receives draft + verified source packet + objective checklist; returns alleged errors with source spans, missing issues, unresolved uncertainty, proposed corrections. Never the same checkpoint as author. |
| H: vision/multimodal | `Qwen/Qwen3.8-27B-TEE` | `moonshotai/Kimi-K2.6-TEE`, then `moonshotai/Kimi-K3-TEE` | Screenshots, scanned pages after OCR, diagrams, visual UI work. Use specialized OCR/transcription endpoints first when the task is primarily reading text or speech; give the LLM extracted text plus page/frame/timestamp references. |

## Specialized non-chat routing

- Embeddings: `Qwen/Qwen3-Embedding-8B-TEE`. Never substitute a chat model.
  Store the embedding model ID and version with every index; rebuild or
  segregate the index when the model changes.
- OCR / PDF extraction: docuextract endpoint. Preserve page numbers, tables,
  headers, footnotes, confidence. Route extracted text to a text lane after.
- Speech: AudioDojo for transcription, diarization, denoising, VAD. Never use
  voice cloning without express user authorization.
- Image generation: Qwen-Image-2512 (generation), Qwen-Image-Edit-2511
  (editing), z-image-turbo or imageclassic (low-cost/style). Only when the user
  requested visual output.
- Object detection: sam3. Do not ask a chat model for pixel coordinates.
- Moderation: halo-guard / halo4b-guard-alpha (input), halo-output-guard
  (output). Moderation models never decide privilege, work-product protection,
  legal relevance, retention, export-control status, or whether a legal
  instruction may be followed.

## Models not used as primaries

`Qwen/Qwen3-235B-A22B-Thinking-2507-TEE` (cheap reasoning second opinion or
compatibility fallback only), `Qwen/Qwen3-32B-TEE` (short-text compatibility
fallback), `Qwen/Qwen3.6-27B-TEE` (fallback for Qwen3.8 or validated
workflows), `zai-org/GLM-5.1-TEE` (fallback when 5.2 unavailable),
`moonshotai/Kimi-K2.6-TEE` (lower-cost multimodal fallback),
`unsloth/Mistral-Nemo-Instruct-2407-TEE` (low-risk plain-text fallback only).

## Output contracts

Every substantive Chutes call specifies: task and permitted scope,
authoritative source packet, facts the model may assume, facts it must not
infer, required output schema, citation/source-span requirements, uncertainty
behavior, stop conditions, acceptance tests, maximum output length.

- Extraction: require `source_document`, `page_or_section`, `exact_quote`,
  `normalized_value`, `confidence`, `missing_or_ambiguous`.
- Drafting: require a separate list of unsupported assumptions and unresolved
  questions; remove it from the deliverable only after the parent resolves
  each item.
- Tool plans: require a plan, never fabricated execution. A proposed tool
  result is an expectation, never an observed fact.

No-source, no-claim: if the source packet does not support a proposition, mark
it unsupported, uncertain, or requiring research. Never fill gaps from
parametric memory. Quoted text must be copied verbatim from a verified source
span.

## Context and data handling

Send only the minimum necessary data. Strip irrelevant personal information,
credentials, secrets, and unrelated privileged material before routing.
Preserve document boundaries; attach filename, date, version, and page or
section identifiers to every chunk. Near the context limit, do not truncate
silently: build a source map, split by issue or document, preserve overlap,
synthesize from structured findings. Use a million-token model only when
decomposition would materially harm the task.

## Failover and retries

- Concrete model IDs for high-stakes calls (auditable selection).
- Comma-separated Chutes pools and `:latency`/`:throughput` routing only for
  availability-sensitive low-risk work where every pool member passed the same
  evaluation threshold. Never mix quality lanes in one automatic pool for
  consequential work.
- Timeout or 5xx: retry the same model once with exponential backoff, then the
  listed fallback, and record the switch. (`route_llm.py` does this.)
- Malformed output: retry once with the validation error and no additional
  substantive prompting, then escalate one lane.
- Unsupported citations, invented quotations, corpus mismatch, or failed
  primary-source check: discard the output. Do not repair it cosmetically.

## Audit logging

`route_llm.py` appends to `chutes_routing_log.jsonl` (agent workspace when
writable, else /tmp): workflow, lane, model ID, token counts, latency,
retries, fallback use, status. Never log privileged prompt or response bodies.
Track cost per accepted task, including retry cost and correction time. Set
task-specific token ceilings; thinking and maximum-quality models never get an
unlimited output budget.

## Evaluation and model changes

Maintain a representative evaluation set per lane (anonymized or synthetic
examples, objective acceptance criteria): extraction accuracy,
unsupported-claim rate, quotation fidelity, citation accuracy, schema
compliance, tool-call correctness, completion rate, latency, retry rate,
review time, total cost. Shadow-test replacements against the incumbent on the
same inputs; promote only on a quality-floor pass plus improvement in quality,
cost, latency, or reliability. Re-run lane evaluation when a model revision,
quantization, context implementation, tool interface, or system prompt
changes. Catalog recency does not establish superiority; never route to the
newest model merely because its version number is higher.

## Quick start

```python
import sys
sys.path.insert(0, "/home/user/skills/chutes-model-routing/scripts")
from route_llm import chutes_text, chutes_batch, chutes_critic, get_catalog, is_confidential

# Default substantive work (Lane C, Qwen3.5 397B)
out = chutes_text("Draft the summary from this packet: ...", lane="C", workflow="memo")

# Cheap bounded op (Lane A) with strict JSON
labels = chutes_text("Label urgency: ...", lane="A",
                     response_format={"type": "json_object"}, workflow="triage")

# Bulk extraction (Lane B)
rows = chutes_batch(chunks, "Extract parties, date, term from this clause. "
                    "Return JSON with exact_quote and source_section.\n{item}",
                    lane="B", workflow="extract")

# Independent critic (Lane G), different family from the author
crit = chutes_critic(draft, source_packet, checklist,
                     author_model="Qwen/Qwen3.5-397B-A17B-TEE")

# Confidentiality gate before sending sensitive material
assert is_confidential("zai-org/GLM-5.2-TEE"), "do not send sensitive data"
```

CLI:

```bash
python3 /home/user/skills/chutes-model-routing/scripts/route_llm.py lanes
python3 /home/user/skills/chutes-model-routing/scripts/route_llm.py catalog --refresh
python3 /home/user/skills/chutes-model-routing/scripts/route_llm.py chat "prompt" --lane D
```

## Research workflow integration

Research-first (default for research, market intelligence, new-source synthesis):
1. The research layer (e.g. Perplexity Deep Research or domain source tools)
   gathers and cites evidence.
2. The parent verifies corpus integrity, document identity, dates, availability.
3. Lane C synthesizes an ordinary source packet; Lane D for difficult,
   high-consequence, or long-horizon packets.
4. Lane G audits load-bearing claims when verification is warranted.
5. The parent verifies every material quotation, number, citation, and
   conclusion against primary source text.
6. Style and document-verification procedures run before delivery.

Draft-then-check (primary documents supplied, external research verifies a draft):
1. Lane C or D produces the baseline strictly from the supplied record.
2. A different-family Chutes critic (Lane G) identifies objective verification
   questions.
3. The research layer answers those questions with sources.
4. Lane C or D incorporates verified corrections.
5. The parent independently checks every load-bearing proposition against the
   primary record.

No model may supply a legal proposition from memory, fabricate an authority,
or convert an unverified web statement into legal authority.

## Installing on another agent

1. Copy this `chutes-model-routing/` folder into the target agent's
   `/home/user/skills/chutes-model-routing/` (or fetch the three files from
   `skills/chutes-model-routing/` in the `Juvorai/legal-agent-infrastructure`
   GitHub repo via raw.githubusercontent.com).
2. Ensure `CHUTES_API_KEY` is bound (see `bind_env_vars`).
3. Replace the target agent's AGENT.md "LLM Routing" / "Chutes-first routing
   rule" sections with the policy block in
   `references/routing-policy-block.md` (adjust the research-layer names to
   that agent's domain sources).
4. Validate: `python3 /home/user/skills/.tools/quick_validate.py chutes-model-routing`
5. Smoke test: `python3 scripts/route_llm.py lanes --refresh` (confirm
   `lane config source: remote`) then a Lane A chat call.

## Error handling

- Missing `CHUTES_API_KEY`: bind the secret; never ask the user to paste it.
- HTTP 401: key invalid or revoked; re-bind.
- HTTP 402 / balance errors: check `GET https://api.chutes.ai/users/me`.
- Unknown or missing model: refresh the catalog (`catalog --refresh`); the
  router falls back through the lane chain and raises if nothing is live.
- Lane A model not yet live on the catalog: the router falls back to Gemma 4
  31B automatically; note the switch in the audit log.
