# Ready-to-paste AGENT.md policy block

Replace the target agent's existing "LLM Routing", "Chutes-first routing rule",
and the Chutes portions of any chain-of-verification section with the block
below. Keep the agent's company configuration, grounding rules, research
workflow, and document rules unless they conflict. Adjust bracketed research
layer names to the adopting agent's domain sources.

```text
CHUTES MODEL ROUTING AND EXECUTION

Controlling principle
Always use the Chutes API in Skills for model inference. Gumloop is the orchestrator. [Perplexity Deep Research and the designated domain tools] are the research and authority layer. Chutes models are the planning, transformation, drafting, synthesis, and criticism layer.

The Gumloop runtime may choose tools, parse simple values, and apply deterministic branches. It may not itself generate, summarize, classify, extract, rewrite, translate, analyze, or synthesize substantive content. Every such operation must call Chutes through the chutes-model-routing skill (scripts/route_llm.py). If Chutes is unavailable, report the failure. Do not silently fall back to a Gumloop model.

Endpoint and confidentiality
Use the shared OpenAI-compatible endpoint at https://llm.chutes.ai/v1.
Keep CHUTES_API_KEY only in the approved secret store. Never place it in a prompt, artifact, checked-in configuration, log, or user-visible response.
For confidential, privileged, personal, contractual, financial, security, or company information, use only a model whose live catalog entry reports confidential_compute=true. If that flag is absent or false, do not send the material.
Before a sensitive production run, verify the requested model ID against GET /v1/models. Do not infer TEE status from a model name alone.

Live catalog rule
At the beginning of a workflow, or from a cache no older than 24 hours, call GET /v1/models and record the available model IDs, context limits, modalities, prices, tool-calling support, structured-output support, reasoning support, and confidential_compute status.
The live API response controls over these written defaults on availability and technical limits. These instructions control model purpose and quality tier.
Do not automatically promote a newly listed model into production. New models enter shadow evaluation first and require approval or passing benchmark results before becoming a primary model.

Routing objective
Use the least expensive model that has demonstrated reliable performance for the task, subject to the consequence and ambiguity of failure. Increase model strength when the task is ambiguous, long-horizon, tool-intensive, multimodal, difficult to verify, or consequential.
Do not send the same full context to several frontier models by default. Use one primary pass and one targeted critic pass only when the verification policy requires it.
Use deterministic code instead of an LLM for exact string matching, arithmetic, sorting, deduplication, schema validation, citation-link checking, and file-format verification.

MODEL LANES

Lane A: ultra-cheap bounded operations
Primary: GLM-4.7-Flash-NVFP4-TEE
Fallback: google/gemma-4-31B-turbo-TEE
Use for routing labels, binary relevance decisions, normalization, simple entity tagging, metadata cleanup, short format conversions, and other narrow operations with an objective machine-checkable answer.
Requirements: input should normally remain below 20,000 tokens; output should normally remain below 1,000 tokens; use a strict JSON schema; set low temperature; validate every field; retry once on schema failure; escalate after the second failure.
Never use this lane for legal conclusions, contract interpretation, open-ended drafting, strategic recommendations, final client-facing prose, or source synthesis involving disputed facts.

Lane B: standard extraction and structured transformation
Primary: google/gemma-4-31B-turbo-TEE
Fallback: Qwen/Qwen3.8-27B-TEE
Use for document classification, clause extraction, email triage, structured summaries, table generation, redaction suggestions, citation metadata extraction, and controlled rewriting when the answer is directly supported by supplied text.
Use JSON mode or structured output whenever available. Require source spans, page or section identifiers, and a null value when a requested field is absent. Never permit inferred text to appear in a field labeled quote.
Escalate to Lane C when the task requires reconciling inconsistent passages, understanding several documents together, or producing substantive prose.

Lane C: standard substantive text work
Primary: Qwen/Qwen3.5-397B-A17B-TEE
Fallback: Qwen/Qwen3.8-27B-TEE
Use for ordinary drafting, rewriting, synthesis of verified research, document analysis, issue-list preparation, negotiation summaries, internal memoranda from supplied sources, workflow specifications, and final prose that does not meet a higher escalation condition.
Use non-thinking or low/medium reasoning for straightforward drafting. Use higher reasoning only where analysis materially benefits from it. Do not preserve hidden reasoning in user-facing deliverables or logs.
This is the default lane for substantive Chutes text work. It replaces Qwen/Qwen3-235B-A22B-Thinking-2507-TEE as the universal default.

Lane D: agentic planning, coding, and high-stakes synthesis
Primary: zai-org/GLM-5.2-TEE
Fallback: Qwen/Qwen3.5-397B-A17B-TEE
Second fallback: deepseek-ai/DeepSeek-V3.2-TEE
Use for multi-step workflow planning, sustained tool use, difficult debugging, repository-scale coding, more than five dependent actions, recovery from tool failures, synthesis across a large workspace, and consequential final synthesis after research.
Also use this lane when the usable prompt exceeds 200,000 tokens, unless Lane E is justified.
The planning call must return a bounded plan with success criteria, required tools, expected artifacts, verification checks, stop conditions, and escalation conditions. The parent agent retains control of tool execution and must not allow the model to invent tool results.

Lane E: maximum-quality escalation
Primary: moonshotai/Kimi-K3-TEE
Fallback: zai-org/GLM-5.2-TEE
Kimi K3 may be used only when at least one of these conditions is true:
1. The user expressly requests the strongest available Chutes model.
2. A high-consequence deliverable remains materially uncertain after a Lane D pass and independent verification.
3. The task requires difficult synthesis across more than 500,000 usable tokens.
4. The task is a complex multimodal or long-horizon agent problem for which Lane D failed acceptance testing.
5. Kimi K3 is acting as the final adversarial reviewer of a draft produced by a different model family.
Do not use Kimi K3 for classification, bulk extraction, routine drafting, first-pass summarization, or a task whose source packet is incomplete. Cap output length to the minimum needed and provide only the disputed propositions or necessary context to a critic call.

Lane F: bulk million-token preprocessing
Primary: deepseek-ai/DeepSeek-V4-Flash-0731-TEE
Fallback: zai-org/GLM-5.2-TEE
Use for preliminary extraction, corpus mapping, chronology construction, candidate-issue collection, and nonfinal synthesis over very large inputs.
Every output from this lane is provisional. Exact quotations, load-bearing facts, and final conclusions must be verified against primary text by deterministic checks or a higher-quality lane.
Do not use this lane as the sole author of final legal or executive work product.

Lane G: model-family-diverse critic
Preferred critic for a Qwen primary: zai-org/GLM-5.2-TEE
Preferred critic for a GLM primary: Qwen/Qwen3.5-397B-A17B-TEE
Preferred critic for a Kimi primary: zai-org/GLM-5.2-TEE
Optional tool-use critic: deepseek-ai/DeepSeek-V3.2-TEE
A critic must receive the draft, the verified source packet, and an objective checklist. It must return alleged errors, supporting source spans, missing issues, unresolved uncertainty, and proposed corrections. It must not rewrite the entire deliverable unless asked.
Never use the same model checkpoint as both author and independent critic when the purpose is error independence.

Lane H: vision and multimodal understanding
Default vision model: Qwen/Qwen3.8-27B-TEE
Long-horizon multimodal fallback: moonshotai/Kimi-K2.6-TEE
Maximum-quality multimodal escalation: moonshotai/Kimi-K3-TEE
Low-risk audio, video, or image triage: Nemotron-3-Nano-Omni-30B-TEE or meta/Muse-Glimmer-30B-NVFP4-TEE when available and validated.
Use the specialized OCR or transcription endpoint before an LLM whenever the task primarily requires reading text or speech. Give the LLM both the extracted text and page, frame, or timestamp references. For consequential work, do not rely solely on a native multimodal impression when OCR, transcription, or source-file text can provide a verifiable record.

SPECIALIZED NON-CHAT ROUTING

Embeddings
Use Qwen/Qwen3-Embedding-8B-TEE for semantic embeddings, clustering, and retrieval indexing. Do not substitute a chat model. Store the embedding model ID and version with every index. Rebuild or segregate an index when the embedding model changes.

OCR and PDF extraction
Use docuextract for document OCR and structured PDF or image extraction. Preserve page numbers, bounding boxes when available, tables, headers, footnotes, and confidence information. Route extracted text to the appropriate text lane afterward.

Speech
Use AudioDojo for transcription, diarization, denoising, voice activity detection, and other speech-specific operations. Route the transcript to the appropriate text lane. Never use voice cloning without express user authorization and a legitimate purpose.

Image generation and editing
Use Qwen-Image-2512 for deliberate image generation, Qwen-Image-Edit-2511 for editing an existing image, and z-image-turbo or imageclassic only for low-cost or style-specific generation. Do not call image-generation endpoints unless the user requested visual output.

Object detection
Use sam3 to locate or segment objects in images. Do not ask a chat model to produce pixel coordinates when the specialized endpoint is available.

Moderation
Use halo-guard or halo4b-guard-alpha for input classification and halo-output-guard for output screening when a workflow requires moderation. Moderation models do not decide attorney-client privilege, work-product protection, legal relevance, document retention, export-control status, or whether a legal instruction may be followed. Those decisions remain with the legal workflow and the user.

MODELS NOT USED AS PRIMARIES

Qwen/Qwen3-235B-A22B-Thinking-2507-TEE
Use only as a low-cost reasoning second opinion, regression-control model, or compatibility fallback. It is no longer the default because it is thinking-only and newer models provide stronger or more controllable agent behavior.

Qwen/Qwen3-32B-TEE
Use only as a compatibility fallback for short text and tool loops. Do not use when the live context requirement exceeds its catalog limit.

Qwen/Qwen3.6-27B-TEE
Use as a fallback for Qwen3.8-27B or for a workflow specifically validated on Qwen3.6. Do not prefer it over Qwen3.8 for new deployments without an eval showing an advantage.

zai-org/GLM-5.1-TEE
Use only as a fallback when GLM 5.2 is unavailable or a saved workflow has been validated specifically on 5.1.

moonshotai/Kimi-K2.6-TEE
Use as the lower-cost fallback for multimodal and long-horizon Kimi workflows. Do not use it as the ordinary text default.

unsloth/Mistral-Nemo-Instruct-2407-TEE
Use only for low-risk plain-text fallback when structured output, tools, reasoning, and multimodal support are unnecessary. Do not use it for substantive legal or executive work.

RESEARCH ROUTING

Research ownership
Research, market intelligence, competitive intelligence, and new-source factual investigation default to [Perplexity Deep Research in the configured project] unless the user invokes an existing override phrase. Primary propositions in the agent's domain must still be retrieved and verified through [the designated authoritative source tools] under the agent's grounding doctrine.
No Chutes model may supply a domain proposition from memory, fabricate an authority, or convert an unverified web statement into authority.

Research-first workflow
1. The research layer or designated source tool gathers and cites the evidence.
2. The parent verifies corpus integrity, document identity, dates, and source availability.
3. Lane C synthesizes an ordinary source packet. Lane D synthesizes a difficult, high-consequence, or long-horizon source packet.
4. Lane G audits load-bearing claims when verification is warranted.
5. The parent verifies every material quotation, numerical value, citation, and conclusion against primary source text.
6. Style and document-verification procedures run before delivery.

Draft-then-check workflow
When primary documents are already supplied and external research is needed only to verify a draft:
1. Lane C or D produces the baseline analysis strictly from the supplied record.
2. A different-family Chutes critic identifies objective verification questions.
3. The research layer answers those questions with sources.
4. Lane C or D incorporates verified corrections.
5. The parent independently checks every load-bearing proposition against the primary record.

No-source, no-claim rule
If the source packet does not support a proposition, the model must mark it unsupported, uncertain, or requiring research. It may not fill the gap from parametric memory. Text inside quotation marks must be copied verbatim from a verified source span.

CONTEXT AND DATA HANDLING

Send only the minimum necessary data to each call. Remove irrelevant personal information, credentials, secrets, and unrelated privileged material before routing.
Preserve document boundaries and attach stable identifiers to every chunk. Never merge text from different documents without filename, date, version, and page or section metadata.
When the prompt approaches the selected model's live context limit, do not truncate silently. Build a source map, split the task by issue or document, preserve overlap where necessary, and synthesize from structured findings. Use a million-token model only when decomposition would materially harm the task.
Prompt caching or repeated context may be used only if the selected endpoint and confidentiality policy permit it.

OUTPUT CONTRACTS

Every substantive Chutes call must specify:
1. Task and permitted scope.
2. Authoritative source packet.
3. Facts the model may assume.
4. Facts the model must not infer.
5. Required output schema or format.
6. Citation or source-span requirements.
7. Uncertainty behavior.
8. Stop conditions.
9. Acceptance tests.
10. Maximum output length.

For extraction, require source_document, page_or_section, exact_quote, normalized_value, confidence, and missing_or_ambiguous fields where applicable.
For drafting, require a separate list of unsupported assumptions and unresolved questions. Remove that list from the final deliverable only after the parent resolves each item.
For tool plans, require a plan rather than fabricated execution. A model may describe a proposed tool result only as an expectation, never as an observed fact.

FAILOVER AND RETRIES

Use a concrete model ID for high-stakes calls so the selected model is auditable.
For availability-sensitive, low-risk work, a comma-separated Chutes pool may provide sequential failover. Use :latency or :throughput only when any model in the pool is acceptable for the task and has passed the same evaluation threshold.
Do not put models from materially different quality lanes into one automatic pool for consequential work.
On timeout or 5xx error, retry the same model once with exponential backoff. Then use the listed fallback and record the switch.
On malformed output, retry once with the validation error and no additional substantive prompting. Then escalate one lane.
On unsupported citations, invented quotations, corpus mismatch, or a failed primary-source check, discard the affected output. Do not repair it cosmetically.

QUALITY, COST, AND AUDIT LOGGING

For every substantive call, log the workflow name, task lane, selected model ID, catalog timestamp, context size, input tokens, output tokens, latency, retries, fallback use, estimated cost, schema-validation result, and acceptance result. Do not log privileged prompt or response bodies outside the approved protected store.
Track cost per accepted task, not merely cost per token. Include retry cost and human correction time when comparing models.
Set task-specific token ceilings. Thinking and maximum-quality models must not receive an unlimited output budget.

EVALUATION AND MODEL CHANGES

Maintain a representative evaluation set for each lane using anonymized or synthetic-safe examples and objective acceptance criteria. Include extraction accuracy, unsupported-claim rate, quotation fidelity, citation accuracy, schema compliance, tool-call correctness, completion rate, latency, retry rate, review time, and total cost.
Shadow-test a proposed replacement against the incumbent on the same inputs. Promote it only if it meets the lane's quality floor and improves quality, cost, latency, or reliability without creating an unacceptable failure mode.
Re-run the affected lane evaluation when a model revision, quantization, context implementation, tool-calling interface, or system prompt changes.
Catalog recency does not establish superiority. Never route automatically to the newest model merely because its version number is higher.

PREFERRED CURRENT ROUTING SUMMARY
Ultra-cheap bounded operations: GLM-4.7-Flash-NVFP4-TEE.
Standard extraction and classification: google/gemma-4-31B-turbo-TEE.
Standard substantive drafting and synthesis: Qwen/Qwen3.5-397B-A17B-TEE.
Agent planning, difficult coding, and consequential synthesis: zai-org/GLM-5.2-TEE.
Maximum-quality exceptional escalation: moonshotai/Kimi-K3-TEE.
Bulk million-token preprocessing: deepseek-ai/DeepSeek-V4-Flash-0731-TEE.
Standard vision and visual document analysis: Qwen/Qwen3.8-27B-TEE.
Independent critic: use a different model family under Lane G.
Research: [Perplexity Deep Research and the designated authoritative source tools], followed by verified Chutes synthesis.
```
