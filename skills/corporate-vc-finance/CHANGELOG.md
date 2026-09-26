# Changelog — corporate-vc-finance

Rollback index. Every merge into references/ writes a line here.

## 2026-09-26 — Daily monitoring cycle (window 2026-09-25 → 2026-09-26)

- No new verified developments: 5 scan-tier entries merged (SEC press negative — latest release 2026-93 dated Sept. 23; 15 routine FR SEC notices, all SRO/OMB extensions; Skotta v. Mears, Del. Ch. (C.A. No. 2024-1085-CCB) reviewed and found non-corporate (real-property lane dispute); Del. Supreme 0 opinions; Congress.gov 250 updated bills / 0 capital-formation hits — H.R. 1672 title match is Health policy area, no window action).
- Verification chain: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE, succeeded) → Lane G critic (zai-org/GLM-5.2-TEE empty-content failure ×4, Qwen3.5-397B pairing also empty; cross-family critic completed via Lane B google/gemma-4-31B-turbo-TEE; verdict fail on first draft — meta-language verbatim fields, missing URLs) → revision → parent deterministic quote/URL check: pass (Skotta verbatim exact match in opinion text; CourtListener and Federal Register URLs live; SEC press page and Congress.gov bill page return 403 to automated requests — content verified via web fetch / api.congress.gov respectively).
- No doctrine-level items. No source changes.

## 2026-09-25 — Daily monitoring cycle (window 2026-09-24 → 2026-09-25)

- Merged 4 verified entries + 1 scan-tier entry: Gendreau v. Movora LLC, Del. (No. 447, 2025) — M&A indemnification fee-shifting requires clear and unequivocal language [doctrine, flagged]; In re Care One, LLC Advancement Litigation, Del. Ch. (C.A. No. 2025-1286-NAC) — advancement denied under unclean hands [doctrine, flagged]; Curonix LLC v. Perryman, Del. Ch. (C.A. No. 2019-1003-BWD) summary judgment [development]; Castle Tire Disposal v. Liberty Tire Services, Del. Ch. (C.A. No. 2025-1497-LWW) metadata-only, no text available [development]; scan entry (SEC press negative; 23 routine FR notices; Congress.gov 250 updated bills / 0 capital-formation hits).
- Verification chain: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE empty-content failure, recurring) → fallback draft (google/gemma-4-31B-turbo-TEE) → Lane G critic (Qwen3.5 empty again; fallback deepseek-ai/DeepSeek-V3.2-TEE; verdict fail on first draft — meta-language verbatim fields) → revision → parent deterministic quote/URL check: pass (3/3 quotes exact; CourtListener ×4 and SEC URLs HTTP 200; Congress.gov homepage 403 to bots, API verified).
- Doctrine-level items flagged to user: Gendreau (fee-shifting drafting standard); Care One (unclean-hands limit on advancement). No source changes.

## 2026-09-24 — Daily monitoring cycle (window 2026-09-23 → 2026-09-24)

- Merged 4 verified entries: SEC DERA updated capital-markets statistics showing IPO/follow-on growth (press release 2026-93) [development]; Coinbase Derivatives proposed rule change on customer margin for security futures (91 FR 60670, Release 34-106443, SR-COIN-2026-001) [development]; Tillman v. Tillman, Del. Ch. (C.A. No. 2025-0475-PAF) — family-LLC derivative suit dismissed on existing doctrine [development]; 1 scan-tier entry (SEC 2026-92 fraud enforcement non-doctrinal; Del. Supreme Carter v. State criminal; 17 routine FR notices; Congress.gov 250 updated bills / 0 capital-formation hits).
- Verification chain: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE empty-content failure, recurring reasoning-budget issue) → fallback draft (google/gemma-4-31B-turbo-TEE) → Lane G critic (Qwen3.5-397B empty again; fallback deepseek-ai/DeepSeek-V3.2-TEE; verdict fail on first draft — unsourced time reference, N/A verbatim in scan entry) → revision → parent deterministic quote/URL check: pass (4/4 quotes exact match after whitespace normalization; 4/4 URLs HTTP 200/202).
- No doctrine-level items. No source changes.

## 2026-09-23 — Daily monitoring cycle (window 2026-09-22 → 2026-09-23)

- Merged 3 verified entries: FR publication of tokenized NMS stock Innovation Exemption order (91 FR 60168, Release 34-106402; additive to cycle 2026-09-18 doctrine item) [development]; SEC censure of OTC Link LLC, Reg SCI, $575,000 penalty (press release 2026-91) [development]; 1 scan-tier entry (3 routine SRO notices — Cboe C2 91 FR 60184, Nasdaq PHLX 91 FR 60186, NYSE 91 FR 60165; CourtListener delch/del 0 opinions; Congress.gov 250 updated bills / 0 capital-formation hits).
- Verification chain: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE empty-content failure, recurring reasoning-budget issue) → fallback draft (google/gemma-4-31B-turbo-TEE) → Lane G critic (zai-org/GLM-5.2-TEE; verdict fail on first draft — synthesized verbatim and invented URLs in scan entries) → revision → parent deterministic quote/URL check: pass (2/2 quotes, 5/5 URLs).
- No doctrine-level items. No source changes.

## 2026-09-22 — Daily monitoring cycle (window 2026-09-21 → 2026-09-22)

- Merged 2 verified entries: Nasdaq Texas LLC FR notice — proposal to amend Equity 1/Equity 4 rules to become a primary listing venue (91 FR 59815) [development]; 1 scan-tier negative result (SEC press RSS newest item 2026-09-17, CourtListener delch 0 opinions, del 3 non-corporate opinions, Congress.gov 99 updated bills / 0 keyword hits).
- Verification chain: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE) → Lane G critic (zai-org/GLM-5.2-TEE; verdict fail on first draft — synthesized scan text mislabeled verbatim, invented citation URLs/keyword list, omitted source detail) → revision → parent deterministic quote/URL check: pass (exact-string match on FR raw text; URL HTTP 200).
- No doctrine-level items. No source changes.

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

## 2026-09-21 — Daily monitoring cycle (window 2026-09-20 → 2026-09-21)

- Merged 3 verified entries: FR publication of Rule 14a-8 rescission proposal (91 FR 59904, comments due 2026-11-20; additive to cycle 2026-09-18 doctrine item) [development]; FR publication of Proxy Solicitation Modernization (91 FR 59852, comments due 2026-11-20) [doctrine]; 1 scan-tier negative result (SEC RSS, CourtListener delch/del, Congress.gov).
- Verification chain: Lane C draft (Qwen/Qwen3.8-27B-TEE fallback; Qwen3.5-397B-A17B-TEE returned empty content after hidden-reasoning budget exhaustion) → Lane G critic (zai-org/GLM-5.2-TEE; verdict fail on first draft — court mislabel, tier inconsistency) → revision → parent deterministic quote/URL check: pass (3/3).
- Doctrine-level items flagged to user: Proxy Solicitation Modernization FR publication (91 FR 59852). No source changes.
