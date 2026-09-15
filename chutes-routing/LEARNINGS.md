# Chutes routing learnings log

Operational learnings from live legal-agent work that affect routing policy, the
lane table, or `route_llm.py` behavior. Each entry: date, reported-by, what
happened, root cause, fix applied or recommended, and evidence. Lane table
changes themselves are made by Juvor.ai-Legal-Ops in `lanes.json` with a
CHANGELOG entry; this file captures the field evidence behind those changes and
router-behavior recommendations that do not require a lane move.

## 2026-09-15 - Thinking-model empty-content failure and long-generation timeouts (Lane C/D)

- Reported by: Chutes_Legal_Privileged (Vanta/Workstreet contract redline task for Benjamin Snipes)
- What happened:
  1. Lane C and Lane D both resolved to `Qwen/Qwen3.5-397B-A17B-TEE`. Every call
     returned HTTP 200 with `content: ""` and `finish_reason: "length"`. The
     model is a thinking model: it emitted `reasoning_content` and the entire
     `max_tokens` budget was consumed by reasoning before any visible content.
     With `max_tokens=10` the response was `content=""`, `reasoning_tokens=10`.
  2. `route_llm.py` treated the empty string as a successful completion and
     returned it. The caller saw an empty draft with no error, no failover, and
     no retry. Three consecutive attempts (max_tokens 3500, 4000, 16000) all
     returned empty or timed out.
  3. Long generations (16000 max_tokens) on this model exceeded the router's
     read timeout, producing `TimeoutError` after minutes of waiting.
  4. Failover attempt to Lane D primary `zai-org/GLM-5.2-TEE` hit HTTP 429
     (rate limit). `moonshotai/Kimi-K3-TEE` (Lane E) worked first try: 3s smoke
     test, then a 5,689-character deliverable in ~200s with `finish_reason=stop`.
  5. Qwen3.5 works fine for short outputs when thinking is disabled:
     `chat_template_kwargs: {"enable_thinking": false}` returned content
     immediately (1s smoke test).
- Root causes:
  a. Router does not validate completion content. An empty `content` with
     `finish_reason=length` is a failure, not a result.
  b. Router does not account for reasoning models consuming the token budget
     invisibly. `max_tokens` must cover reasoning + content, or thinking must
     be disabled for non-reasoning tasks.
  c. Router read timeout is too short for long-form generation on thinking
     models, and there is no streaming or background pattern guidance.
  d. Lane C and Lane D resolved to the same model at call time, so "failover to
     the other lane" was not actually a model change.
- Recommended router fixes (for route_llm.py maintainer):
  1. Treat `content == ""` as a failed candidate: log, then failover to the
     next model in the lane. Never return empty text as success.
  2. On `finish_reason == "length"` with empty or truncated content, retry once
     with 2x max_tokens before failing over.
  3. For known thinking models (catalog metadata or a maintained list), either
     set `chat_template_kwargs: {"enable_thinking": false}` for drafting/extraction
     lanes (A, B, C, F) or multiply the requested max_tokens by ~3x to leave
     headroom for reasoning.
  4. Raise the default read timeout for max_tokens > 4000 (suggest 600s), and
     document the background-process pattern (nohup + poll a result file) for
     generations expected to exceed ~120s.
  5. Handle HTTP 429 explicitly: immediate failover to the next candidate, not
     a retry of the same model.
  6. Lane resolution should deduplicate: if Lane C and Lane D resolve to the
     same model, failover within the lane list must skip same-model candidates.
- Interim operating guidance for agents (effective immediately, no code change needed):
  1. Before any long generation, run a 10-token smoke test on the target lane
     and check that `content` is non-empty. Empty content on the smoke test
     means the lane's model is in thinking-budget mode; switch models.
  2. For long-form drafting (emails, memos, clause libraries > 2000 chars),
     prefer `moonshotai/Kimi-K3-TEE` or pass `enable_thinking: false` when
     using Qwen thinking models. Kimi-K3 produced a clean 5.7K-char legal
     negotiation email in ~200s on first attempt.
  3. Run generations expected to exceed ~120s as background shell processes
     writing to a result file, and poll the file. Do not block a
     sandbox_python kernel on a multi-minute HTTP read.
  4. When a model returns empty content twice, stop retrying it. Move to a
     different model family the same turn and tell the user which model
     produced the deliverable.
- Evidence: raw API response 2026-09-15 (`id bb33f004...`, model
  Qwen/Qwen3.5-397B-A17B-TEE, `content:""`, `reasoning_content` present,
  `finish_reason:"length"`, `reasoning_tokens:10` of `completion_tokens:10`);
  GLM-5.2 HTTP 429 same session; Kimi-K3 smoke 3s and full generation
  `finish_reason=stop`, 5,689 chars, 204s; Qwen with `enable_thinking:false`
  smoke 1s non-empty.
- Lane table impact: none requested. This is router behavior plus operating
  guidance, not a model quality demotion. If empty-content failures on
  Qwen3.5-397B persist after the router fix, revisit Lane C primary.
- Rollback: n/a (documentation only).
