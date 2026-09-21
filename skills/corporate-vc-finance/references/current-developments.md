# Current Developments — Corporate & VC Finance

Verified developments from Juvor.ai-Legal-Ops monitoring cycles. Every entry carries a verbatim quote from the primary source, a citation URL, and a verification verdict. Newest cycle first.

Tiers: **doctrine** (changes or reaffirms a legal rule practitioners rely on — flagged in the managing-partner digest), **development** (noteworthy but routine), **scan** (negative result).

---

## Cycle 2026-09-21 — window 2026-09-20 to 2026-09-21

Verification: Lane C draft (Qwen/Qwen3.8-27B-TEE fallback; Qwen3.5-397B-A17B-TEE returned empty content after hidden-reasoning budget exhaustion) → Lane G cross-family critic (zai-org/GLM-5.2-TEE; verdict fail on first draft — court mislabel in scan entry, tier inconsistency on Proxy Solicitation Modernization) → revision per critic findings → parent deterministic quote/URL check (exact-match against source packet): pass, 3/3 quotes and 3/3 URLs.

### 1. FR Publication: Rescission of Rule 14a-8 and Amendments to Rule 14a-4 — 91 FR 59904 [development]

**Source:** Federal Register

**Summary:** The SEC's proposed rescission of Rule 14a-8 (logged as doctrine in cycle 2026-09-18 from the SEC press release) was published in the Federal Register on September 21, 2026, adding the formal citation 91 FR 59904 and setting a comment deadline of November 20, 2026. Additive to the existing doctrine entry.

**Verbatim:** "The Securities and Exchange Commission (\"Commission\") is proposing to rescind Rule 14a-8 under the Securities Exchange Act of 1934 (\"Exchange Act\") and leave determinations about the role of shareholder proposals to State law and company governing documents. The Commission also is proposing to amend Rule 14a-4 under the Exchange Act to expand the circumstances under which a company may exercise, with respect to proxies it receives, discretionary voting authority on proposals that will be presented at a shareholder meeting but not included in the company's proxy materials. At the same time, the proposed amendments to Rule 14a-4 would provide shareholders with the means to elect to prevent the company from exercising such authority with respect to their individual shares."

**Citation:** https://www.federalregister.gov/documents/2026/09/21/2026-19260/rescission-of-rule-14a-8s-federal-regulation-of-shareholder-proposals-and-amendments-to-rule-14a-4

**Verification verdict:** verified (Lane G critic: verified after revision; parent quote/URL check: pass)

### 2. FR Publication: Proxy Solicitation Modernization — 91 FR 59852 [doctrine]

**Source:** Federal Register

**Summary:** The SEC's Proxy Solicitation Modernization proposal (announced alongside the 14a-8 rescission in press release 2026-89) was published in the Federal Register on September 21, 2026 as 91 FR 59852, with comments due November 20, 2026. The proposal would eliminate the annual-report delivery requirement, eliminate the delivery deadline for documents incorporated by reference, eliminate filing of soliciting material for certain exempt solicitations, and shorten the minimum broker search period. Tiered doctrine per Lane G critic for consistency with the companion 14a-8 proposal.

**Verbatim:** "The Securities and Exchange Commission (\"Commission\") is proposing amendments to modernize certain rules related to proxy solicitations. The proposed amendments would, among other things, eliminate the requirement that registrants deliver an annual report to security holders, eliminate the delivery deadline when documents are incorporated by reference into a proxy statement, eliminate the requirement to file soliciting material regarding certain exempt solicitations, and shorten the minimum broker search period for proxy solicitations. The proposed amendments are intended to update our rules to account for developments since their adoption or last amendment and to simplify compliance for registrants."

**Citation:** https://www.federalregister.gov/documents/2026/09/21/2026-19259/proxy-solicitation-modernization

**Verification verdict:** verified (Lane G critic: verified after revision; parent quote/URL check: pass)

### 3. Negative Scan: SEC RSS, CourtListener (delch/del), Congress.gov — 2026-09-21 [scan]

**Source:** SEC Press Releases RSS, CourtListener (delch, del), Congress.gov

**Summary:** No new SEC press releases in the window (newest RSS item dated 2026-09-17, already logged). CourtListener searches for delch and del opinions filed after 2026-09-20 returned count = 0 for both. Congress.gov's 50 most recently updated bills showed no updates in the window (latest updateDate 2026-09-08) and the capital-formation keyword screen was negative.

**Verbatim:** ZERO items in window.

**Citation:** https://www.sec.gov/news/pressreleases.rss

**Verification verdict:** verified (Lane G critic: verified after revision; parent quote/URL check: pass — negative scan result, no single document URL)

---

## Cycle 2026-09-20 — window 2026-09-19 to 2026-09-20

Verification: Lane C draft (Qwen/Qwen3.8-27B-TEE fallback; Qwen3.5-397B-A17B-TEE exhausted its token budget on hidden reasoning twice) → Lane G cross-family critic (zai-org/GLM-5.2-TEE) → revision per critic findings → parent deterministic quote/URL check (exact-match against source packet) → parent primary-source review. Initial critic verdict: fail (fabricated quote, wrong citation URL, court mislabel); revised entry passed all deterministic checks.

### 1. No New Capital Formation Developments — 2026-09-20 [scan]

**Source:** SEC Press Releases RSS, Federal Register API, CourtListener (Del. Ch. & Del.), Congress.gov

**Summary:** A scan of the 24-hour window from 2026-09-19T07:30Z to 2026-09-20T07:30Z revealed no new developments in the queried sources. The SEC RSS feed showed no new releases in the window (the newest item, dated 2026-09-17, was already logged in cycle 2026-09-18). The Federal Register API returned 0 SEC documents. CourtListener searches for Del. Ch. and Del. returned 0 opinions. A keyword screen of 50 updated bills on Congress.gov using the terms capital/securities/investment/venture/crowdfund/accredited/offering/emerging growth found no capital-formation items.

**Verbatim:** count = 0

**Citation:** https://www.sec.gov/news/pressreleases.rss

**Verification verdict:** verified (Lane G critic findings resolved; parent quote/URL check: pass)

---

## Cycle 2026-09-18 — window 2026-09-11 to 2026-09-18

Verification: Lane C draft (Qwen/Qwen3.5-397B-A17B-TEE) → Lane G cross-family critic (deepseek-ai/DeepSeek-V3.2-TEE; GLM-5.2-TEE unavailable, timed out twice) → parent deterministic quote/URL check (exact-match against source packet) → parent primary-source review. Critic overall verdict: **pass** (one cosmetic flag on source-label abbreviation, accepted as standard citation form). All 7 quotes exact-match verified; 6/7 URLs exact-match (item 7 is a negative scan result with no single document URL).

### 1. SEC Issues 'Innovation Exemption' for Tokenized NMS Stock — Sept. 17, 2026 [development]

**Source:** SEC

The SEC issued an order granting temporary, conditional exemptive relief to Tokenized Securities Venues (TSVs) from the definition of "exchange" to trade tokenized NMS stock using automated market makers and liquidity pools. The exemptions are set to expire five years after publication.

**Practice relevance:** VC and finance practices monitoring crypto-asset integration with traditional equities need to track this temporary regulatory pathway for tokenized stock trading.

**Verbatim:** "The Securities and Exchange Commission today issued an order granting temporary, conditional exemptive relief to Tokenized Securities Venues each a “TSV” from the definition of “exchange” in the Securities Exchange Act of 1934 (Exchange Act) to trade tokenized National Market System (NMS) stock using innovative permissioned automated market makers and liquidity pools (together “AMM Liquidity Pools”)."

**Citation:** https://www.sec.gov/newsroom/press-releases/2026-90-sec-issues-innovation-exemption-facilitate-trading-tokenized-nms-stock-request-comment

**Verification verdict:** verified (Lane G critic: verified; parent quote/URL check: pass)

### 2. SEC Proposes Rescission of Shareholder Proposal Rule — Sept. 16, 2026 [doctrine]

**Source:** SEC

The SEC proposed to rescind Rule 14a-8 under the Exchange Act, stating it exceeds the Commission's statutory authority and intrudes into matters of state law. Public comment periods will remain open for 60 days following publication in the Federal Register.

**Practice relevance:** Corporate governance teams must prepare for potential shifts in shareholder engagement strategies if the federal framework for shareholder proposals is removed.

**Verbatim:** "The Securities and Exchange Commission today proposed to rescind Rule 14a-8 under the Securities Exchange Act of 1934, which exceeds the scope of the Commission's statutory authority and intrudes into matters of state law."

**Citation:** https://www.sec.gov/newsroom/press-releases/2026-89-sec-proposes-rescission-shareholder-proposal-rule-reforms-proxy-solicitation-process

**Verification verdict:** verified (Lane G critic: verified; parent quote/URL check: pass)

### 3. IsZo Capital LP v. Brandenburg (Del. Supreme Court) — Sept. 14, 2026 [doctrine]

**Source:** Del. Supreme

The Court affirmed the Court of Chancery's approval of a $32M merger class settlement without a Celera opt-out, declining to revisit the In re Celera framework. The Court held that breach-of-fiduciary claims from a single transaction at a single price are homogenous and distinguishable from Wal-Mart v. Dukes.

**Practice relevance:** M&A practitioners gain certainty that the Celera framework remains valid for class settlement approvals involving homogenous fiduciary claims.

**Verbatim:** "the faithful application of the Celera framework, as occurred in this case, affords objecting class members constitutionally sufficient due process"

**Citation:** https://www.courtlistener.com/opinion/10973323/iszo-capital-lp-v-stephen-brandenburg/

**Verification verdict:** verified (Lane G critic: verified with cosmetic source-label note; parent quote/URL check: pass)

### 4. Wisconsin Laborers' Pension Fund v. Joshi (Del. Chancery) — Sept. 16, 2026 [doctrine]

**Source:** Del. Chancery

Vice Chancellor Cook dismissed all claims arising from the $4.4B take-private of Alteryx, Inc., ruling that the stockholder vote was cleansing under Corwin. The dismissal included claims against the controlling stockholder and aiding-and-abetting claims against the acquirer.

**Practice relevance:** Confirms the continued potency of Corwin cleansing to dismiss fiduciary duty claims even in take-private transactions involving controlling stockholders.

**Verbatim:** "The stockholder vote is thus cleansing, and Plaintiffs' claims must be dismissed."

**Citation:** https://www.courtlistener.com/opinion/10974792/wisconsin-laborers-pension-fund-and-mark-b-nardella-v-anjali-joshi/

**Verification verdict:** verified (Lane G critic: verified; parent quote/URL check: pass)

### 5. Freiberg v. Xonar Technology Inc. (Del. Chancery) — Sept. 15, 2026 [doctrine]

**Source:** Del. Chancery

In a post-trial Section 225 opinion, the Court held that under Section 228, the consent period is not "closed" until the earlier of 60 days or the delivery of the requisite number of consents. Consents signed on different dates within the 60-day window aggregate, and a company's treatment of a removal as effective does not close the period.

**Practice relevance:** Provides clarity on consent solicitation timing and aggregation rules for corporate actions involving written consents.

**Verbatim:** "Under Section 228, the consent period is not “closed” until the earlier of 60 days or the delivery of the requisite number of consents."

**Citation:** https://www.courtlistener.com/opinion/10974350/gregory-freiberg-v-xonar-technology-inc/

**Verification verdict:** verified (Lane G critic: verified; parent quote/URL check: pass)

### 6. PCAOB Proposed Rules on QC 1000 Amendments — Sept. 18, 2026 [development]

**Source:** Federal Register

The PCAOB filed proposed rules on amendments to QC 1000, regarding A Firm's System of Quality Control, and related rule and forms. This notice was published in the Federal Register on September 18, 2026.

**Practice relevance:** Audit committees and finance teams should monitor changes to quality control standards affecting public company accounting oversight.

**Verbatim:** "Public Company Accounting Oversight Board; Notice of Filing of Proposed Rules on Amendments to QC 1000, A Firm's System of Quality Control, and Related Rule and Forms"

**Citation:** https://www.federalregister.gov/documents/2026/09/18/2026-19148/public-company-accounting-oversight-board-notice-of-filing-of-proposed-rules-on-amendments-to-qc

**Verification verdict:** verified (Lane G critic: verified; parent quote/URL check: pass)

### 7. Congress.gov Capital Formation Scan (No New Bills) — Sept. 11-18, 2026 [scan]

**Source:** Congress.gov

A keyword screen over 250 updated bills found no new capital-formation bill introductions or actions in the window. H.R. 1483 was reported by House Financial Services on September 1, 2026, which is outside the 7-day window.

**Practice relevance:** No capital-formation legislation moved in the window; no action required.

**Verbatim:** "keyword screen (capital/securities/investment/venture/crowdfund/accredited/offering/emerging growth) over 250 updated bills found no new capital-formation bill introductions or actions in the window."

**Citation:** https://www.congress.gov/

**Verification verdict:** verified (Lane G critic: verified; parent quote/URL check: pass — negative scan result, no single document URL)
