# Chutes routing changelog

Every change to `lanes.json` gets an entry: date, changed-by, lanes affected, reason, and evidence (eval results or catalog data).

## 2026-09-11 - Seed (schema_version 1)

- Changed by: Chutes_Legal_Privileged (seed on behalf of Juvor.ai-Legal-Ops)
- Lanes affected: all (A-H)
- Reason: initial externalization of the lane table from the chutes-model-routing skill into central config.
- Evidence: live catalog GET /v1/models fetched 2026-09-11; all lane primaries live except Lane A primary GLM-4.7-Flash-NVFP4-TEE (not yet listed; router auto-falls back to google/gemma-4-31B-turbo-TEE). Smoke tests passed: Lane A chat call, Lane G critic pairing (Qwen->GLM, GLM->Qwen), confidentiality gate.
