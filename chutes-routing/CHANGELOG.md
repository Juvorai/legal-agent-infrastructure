# Chutes routing changelog

Every change to `lanes.json` gets an entry: date, changed-by, lanes affected, reason, and evidence (eval results or catalog data).

## 2026-09-11 - Seed (schema_version 1)

- Changed by: Chutes_Legal_Privileged (seed on behalf of Juvor.ai-Legal-Ops)
- Lanes affected: all (A-H)
- Reason: initial externalization of the lane table from the chutes-model-routing skill into central config.
- Evidence: live catalog GET /v1/models fetched 2026-09-11; all lane primaries live except Lane A primary GLM-4.7-Flash-NVFP4-TEE (not yet listed; router auto-falls back to google/gemma-4-31B-turbo-TEE). Smoke tests passed: Lane A chat call, Lane G critic pairing (Qwen->GLM, GLM->Qwen), confidentiality gate.

## 2026-09-14 - Lane A primary demotion (delisted model)

- Changed by: Juvor.ai-Legal-Ops (weekly catalog watch, authorized auto-promotion per Benjamin Snipes 2026-09-11)
- Lanes affected: A
- Change: Lane A primary GLM-4.7-Flash-NVFP4-TEE -> google/gemma-4-31B-turbo-TEE (already the lane fallback). Lane A fallbacks now [Qwen/Qwen3.8-27B-TEE]. GLM-4.7-Flash-NVFP4-TEE moved to non_primary_models as a documented pending launch.
- Reason: GLM-4.7-Flash-NVFP4-TEE is not listed in the live catalog (GET /v1/models, 2026-09-14). Hard rule: no dead IDs as lane primaries; router was auto-falling back to gemma-4-31B-turbo-TEE, so this makes the effective routing explicit.
- Evidence: live catalog snapshot 2026-09-14 (14 models); gemma-4-31B-turbo-TEE live, confidential_compute=true, ctx=131072, text+image, $0.12/$0.37 per Mtok (cheapest live TEE chat model, consistent with Lane A ultra-cheap purpose). Seed CHANGELOG (2026-09-11) already documented gemma as the effective Lane A model. No quality-floor eval required: this is a delisting demotion of a non-live ID, not a new-model promotion; the promoted model was already the operating primary in practice.
- Other catalog observations (no action): Nemotron-3-Nano-Omni-30B-TEE newly listed (omni triage candidate; enters shadow evaluation, not promoted). Qwen/Qwen3-Embedding-8B-TEE absent from chat completions catalog; embedding_model left unchanged pending verification against the embeddings endpoint class. No price moves >25%, no context/modality changes, no confidential_compute flag losses on any live lane model.
- Rollback: git revert <commit-sha>
