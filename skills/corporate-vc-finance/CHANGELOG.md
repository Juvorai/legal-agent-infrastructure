# Changelog — corporate-vc-finance

Rollback index. Every merge into references/ writes a line here.

## 2026-09-18 — Skill bootstrap + first monitoring cycle (window 2026-09-11 → 2026-09-18)

- Created skill structure: SKILL.md, references/sources.md, references/current-developments.md, CHANGELOG.md.
- Merged 7 verified entries from cycle 2026-09-18: 2 SEC releases (2026-90 tokenized NMS stock Innovation Exemption; 2026-89 proposed Rule 14a-8 rescission + proxy solicitation modernization), 3 Delaware decisions (IsZo Capital v. Brandenburg, Del.; Wisconsin Laborers' v. Joshi, Del. Ch.; Freiberg v. Xonar, Del. Ch.), 1 Federal Register item (PCAOB QC 1000, 91 FR 59354), 1 Congress.gov negative scan.
- Verification chain: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE) → Lane G critic (deepseek-ai/DeepSeek-V3.2-TEE, fallback after GLM-5.2-TEE timeouts) → parent deterministic quote/URL verification → parent primary-source review. Critic verdict: pass.
- Doctrine-level items flagged to user: SEC 14a-8 rescission proposal; IsZo (Celera opt-out reaffirmed); Joshi (Corwin cleansing in controller take-private); Freiberg (§ 228 consent aggregation).
- Approved source defaults: SEC, Federal Register, CourtListener (delch/del), Congress.gov. NVCA and others deferred pending baseline review.

## 2026-09-20 — Daily monitoring cycle (window 2026-09-19 → 2026-09-20)

- Merged 1 scan-tier entry: negative result across all four approved sources (SEC press RSS, Federal Register SEC feed, CourtListener delch/del, Congress.gov keyword screen of 50 updated bills).
- Verification chain: Lane C draft (Qwen/Qwen3.8-27B-TEE fallback after Qwen3.5-397B-A17B-TEE reasoning-budget exhaustion) → Lane G critic (zai-org/GLM-5.2-TEE; verdict fail on first draft — fabricated quote, wrong citation URL, court mislabel) → revision → parent deterministic quote/URL check: pass.
- No doctrine-level items. No source changes.
