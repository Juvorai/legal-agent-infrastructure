# Changelog — corporate-vc-finance

Rollback index. Every merge into references/ writes a line here.

## 2026-10-07 — Daily monitoring cycle (window 2026-10-06 07:30Z → 2026-10-07 07:30Z)

- 7 entries merged into references/current-developments.md: (1) SEC proposed rule — Investment Adviser Performance-Based Compensation Modernization; Rule 205-3 "qualified client" would expand to all Reg D accredited investors; performance fees from regulated funds (91 FR 63676; Release Nos. 33-11443/IA-7022; File S7-2026-28; comments due 2026-12-07) [doctrine — flagged]; (2) SEC proposed rule — Adviser and Regulated Fund Custody Rules; Crypto Custody Rules; new ICA custody rules + Advisers Act custody amendments, tokenized-private-fund Form ADV/N-CEN questions (91 FR 63870; IA-7023/IC-36353; File S7-2026-35; comments due 2026-12-07) [doctrine — flagged]; (3) SEC order approving FINRA exemption of specified collective trust funds from Rules 5130/5131(b) IPO restrictions (91 FR 64205) [development]; (4) SEC press releases 2026-103 (Western Asset/Ken Leech cherry-picking final judgment) and 2026-102 (compliance outreach seminar) [development]; (5)-(7) negative scans — CourtListener delch (0 opinions), del (2 non-corporate), Congress.gov (250 updated bills, no capital-formation) [scan]. Verification: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE, JSON mode after one empty completion) → Lane G critic (zai-org/GLM-5.2-TEE; 3 corrections — items 1-2 re-tiered to doctrine, missing PR 2026-102 added) → parent deterministic quote checks pass (5/5 exact matches against FR API metadata, sec.gov listing, CourtListener snippet). Doctrine-level items flagged for user review; no doctrine auto-resolved.

## 2026-10-06 — Daily monitoring cycle (window 2026-10-05 07:30Z → 2026-10-06 07:30Z)

- 3 entries merged into references/current-developments.md: (1) Mendoza v. Distributed Creation, Inc. (Del. Ch. Oct. 5, 2026) — post-trial § 220 partial-inspection order applying amended-§ 220 burden framework [development]; (2) Cornice Ventures I LLC v. Silberstein (Del. Oct. 5, 2026) — investor claims time-barred on inquiry notice from missed audited-financials delivery [development]; (3) negative scans — SEC press (2026-101 World Investor Week only), Federal Register (17 docs all prior-cycle or routine SRO/Sunshine), Congress.gov (no capital-formation bills, 0 introductions), 4 other Delaware opinions screened out [scan]. Lane C draft Qwen3.5-397B → Lane G critic GLM-5.2 (5 corrections applied) → parent quote checks pass. Note: commit 85d0146 clobbered both files with placeholder content (tool-call error); restored and merged in 5938483.

## 2026-10-05 — Daily monitoring cycle (window 2026-10-04 07:30Z → 2026-10-05 07:30Z)

- 5 entries merged into references/current-developments.md: (1) SEC proposed rule — Interval Fund Modernization; multiple share class expansion for closed-end funds/BDCs; rescission of related exemptive orders (91 FR 63388; comments due 2026-12-04) [development, FLAGGED doctrine-level if adopted]; (2) five SEC notices considering accredited-investor credential designations under Rule 501(a)(10) — CFA charter, FINRA exam, CFP, Series 79/86/87, CPA (91 FR 63314/63335/63345/63357/63368; comments due 2026-12-04) [development, FLAGGED doctrine-level if adopted]; (3) SLR Secured Lending BDC multiple-share-class exemptive application (91 FR 63323) [development]; (4) LTSE Rule 15.120 fee-collection amendment (91 FR 63352) [development]; (5) negative scans — SEC press releases, CourtListener delch/del, Congress.gov [scan]. Verification: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE) → Lane G critic (zai-org/GLM-5.2-TEE, pass) → parent exact-match on all 9 quotes against FR full texts; all citation URLs confirmed via FR API. Doctrine-level flags raised for user review; no doctrine auto-merged.

## 2026-10-04 — Daily monitoring cycle (window 2026-10-03 07:30Z → 2026-10-04 07:30Z)

- 4 scan-tier entries merged into references/current-developments.md (negative results): SEC press releases (latest Oct. 1, already covered), Federal Register SEC feed (count=0), CourtListener delch/del (count=0), Congress.gov capital-formation screen (52 updated bills, 4 keyword matches all false positives). No Chutes verification pass required — no candidate updates. No doctrine changes.

## 2026-10-02 — Daily monitoring cycle (window 2026-10-01 07:30Z → 2026-10-02 07:30Z)

- 4 development + 1 scan-tier entries merged into references/current-developments.md: SEC press release 2026-100 (proposed crypto-custody framework for advisers and regulated funds under Advisers Act/ICA — self-custody in certain circumstances, state trust companies as custodians; PROPOSAL, 60-day comment period — flagged doctrine-level if adopted); FR final rule Commission Quorum Requirement (91 FR 62654, Release No. 34-106537, effective 2026-10-02 — amends 17 CFR 200.41); CourtListener delch 2 opinions (Mitchell Partners v. AMFI — post-trial judgment for defendants in 1982 reorganization/Class B stock challenge; Pinczower v. Hava Nation — Rule 144 magistrate report, Section 327 derivative standing fails on unexecuted employment agreement, cleanup doctrine retains two counts); del 0 corporate opinions (2 non-corporate: insurance, criminal); Congress.gov scan negative (20 bills updated, no capital-formation topics).
- Verification chain: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE, 2 calls — first truncated, completed via continuation) → Lane G critic (deepseek-ai/DeepSeek-V3.2-TEE after zai-org/GLM-5.2-TEE 429 capacity errors ×4; verdict fail — truncated FR verbatim quote, unsupported "concludes the litigation" inference) → corrections applied → parent deterministic quote check: pass (6/6 quotes exact/normalized-exact against SEC release body, FR rule body, and CourtListener opinion text).

## 2026-10-01 — Daily monitoring cycle (window 2026-09-30 → 2026-10-01)

- 2 development + 4 scan-tier entries merged: SEC press release 2026-96 (proposed amendments — performance-based compensation modernization, interval fund modernization, closed-end fund share classes, plus accredited-investor exam/credential comment requests; PROPOSAL, 60-day comment period — flagged doctrine-level if adopted); FR SEC feed 23 routine Notices (PRA extensions, SRO filings, ICA 8(f) deregistration — no corporate/VC substance); CourtListener delch 2 opinions (Vera Bradley v. Project Aster — True Up/GAAP-consistency contract interpretation; Fetras v. Richards — indemnification ripeness/bylaw condition precedent; both routine applications, scan tier); del 0 opinions; Congress.gov H.R. 1190 Senate passage (action dated 2026-09-29, surfaced in window feed; SEC small-business reporting bill).
- Verification chain: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE, 2 calls) → Lane G critic (zai-org/GLM-5.2-TEE; verdict fail on first draft — misapplied doctrine tier on proposed rule, 5 missing tiers, 1 unsupported truncated-text completion, missing URL, unflagged date/window discrepancy) → revision → parent deterministic quote/URL check: pass (3/3 quotes exact/normalized-exact; CL URLs 202; sec.gov/congress.gov 403 to datacenter HEAD but reachable via feeds during collection).
- Doctrine-level items flagged to user: SEC 2026-96 proposed private-markets retailization package (accredited-investor definition expansion; adviser performance-fee modernization). No source changes.

## 2026-09-29 — Daily monitoring cycle (window 2026-09-28 → 2026-09-29)

- 1 development + 4 scan-tier entries merged: SEC press release 2026-94 (settled conflict-of-interest charges against investment adviser Zoe Financial — enforcement, not corporate/VC rule change); FR SEC feed 7 routine Notices (PRA extensions ×2, Sunshine Act meeting, SRO fee/procedure ×4 — no corporate/VC substance); CourtListener delch 1 procedural recusal letter decision (Brandao v. HerdDogg, C.A. No. 2026-0824-TJF, Fox, M. — no doctrine); del 0 opinions; Congress.gov 50 updated bills / 0 capital-formation actions (H.RES.1455 hit was 2024 metadata refresh).
- Verification chain: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE empty content ×2 — recurring hidden-reasoning budget issue; draft via Lane B google/gemma-4-31B-turbo-TEE) → Lane G critic (zai-org/GLM-5.2-TEE empty ×2; critic via deepseek-ai/DeepSeek-V3.2-TEE; verdict fail on first draft — three verbatim-label issues) → revision → parent deterministic quote/URL check: pass (4/4).
- No doctrine-level items flagged. No source changes.

## 2026-09-28 — Daily monitoring cycle (window 2026-09-27 → 2026-09-28)

- No new verified developments: 5 scan-tier entries merged (SEC press negative — latest release remains 2026-93 dated Sept. 23; FR SEC feed 7 routine Notices: PRA extensions ×2, Sunshine Act meeting, SRO fee/procedure ×4 — no corporate/VC substance; CourtListener delch 0 opinions; del 0 opinions; Congress.gov 1 updated bill / 0 capital-formation keyword hits).
- Verification chain: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE empty content ×2 — recurring hidden-reasoning budget issue; draft via Lane B google/gemma-4-31B-turbo-TEE) → Lane G critic (zai-org/GLM-5.2-TEE empty; cross-family critic via deepseek-ai/DeepSeek-V3.2-TEE; verdict fail on first draft — heading format, FR document-number list, FR citation URL) → revision → parent deterministic quote/URL check: pass (5/5 sources re-verified).
- No doctrine-level items. No source changes.

## 2026-09-27 — Daily monitoring cycle (window 2026-09-26 → 2026-09-27)

- No new verified developments: 5 scan-tier entries merged (SEC press negative — latest release remains 2026-93 dated Sept. 23; FR SEC feed 0 documents; CourtListener delch 0 opinions; del 0 opinions; Congress.gov 136 updated bills / 0 capital-formation keyword hits).
- Verification chain: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE empty content ×2; Qwen3.8-27B-TEE fallback empty; draft via Lane B google/gemma-4-31B-turbo-TEE) → Lane G critic (GLM-5.2-TEE, Qwen3.5-397B, Qwen3.8-27B all empty; cross-family critic via deepseek-ai/DeepSeek-V3.2-TEE; verdict fail on first draft — court mislabels, missing [scan] markers, verbatim-label format, heading format, missing release name) → revision → parent deterministic quote/URL check: pass (5/5 sources re-verified live).
- No doctrine-level items. No source changes.

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

- 2026-10-02: Daily monitoring cycle (window 2026-10-01 07:30Z–2026-10-02 07:30Z). Merged 5 verified entries into references/current-developments.md: SEC crypto custody proposal (2026-100, flagged doctrine-if-adopted), SEC quorum final rule (91 FR 62654), Mitchell Partners v. AMFI (Del. Ch. post-trial), Pinczower v. Hava Nation (Del. Ch. Rule 144 report), Congress.gov capital-formation scan (negative). Lane C draft Qwen3.5-397B → Lane G critic DeepSeek-V3.2 (GLM-5.2 429 fallback) → parent quote checks pass.