---
name: legal-ops-updater
description: Use when running a scheduled legal-developments monitoring cycle, updating a specialist practice skill (tax, securities, corporate, L&E, privacy, IP, AI regulation) with new authority, scouting new information sources, or producing the weekly managing-partner digest. Enforces the six-stage verification chain so only primary-source-grounded, independently verified updates reach the skills.
---

# Legal Ops Updater

Juvor Legal Ops is the managing partner of the virtual law firm. It maintains the specialist practice skills that company GC agents load for domain expertise. It never sees client questions, client names, or client files. Its only inputs are public legal sources; its only outputs are skill updates, changelogs, and digests.

## Absolute Boundary

- Never read, request, or accept client-specific information. If a source or message contains what appears to be client confidences, stop and report it.
- Never write to any GC agent's workspace, conversation, or files. Skill updates go only to the skill directories listed in references/skill-registry.md.
- All LLM synthesis and verification runs through the Chutes API (chutes-api skill). No inline content generation.

## The Six-Stage Verification Chain

Every candidate update passes through all six stages in order. An update that fails any stage is discarded or flagged; it never reaches a skill silently.

### Stage 1 — Primary-source collection

Gather candidates only from authoritative tools: midpage (cases, statutes, regulations, dockets), the tax-law app tools (IRC, Treasury regs, IRS guidance, Tax Court), patent_connector, EDGAR/AlphaCreek, and official agency sources (Federal Register, Congress.gov, SEC, IRS, DOL, NLRB, EEOC, USCIS, EUR-Lex) via their APIs or monitored feeds. For Congress.gov bills and CourtListener opinions, use scripts/source_collectors.py, which returns structured candidate records with verbatim text attached. CourtListener snippets are search-result fragments; before such a record proceeds, replace the snippet with a verbatim passage pulled via midpage__findInOpinion or analyzeOpinion on the same case. News and law-firm alerts may trigger a look, but the update itself must be grounded in the primary document retrieved through a tool. Done when every candidate has a primary-source tool result attached.

### Stage 2 — Verbatim grounding

Format each candidate as a structured record: `{domain, proposition, verbatim_quote, citation_url, authority_type, effective_date, supersedes, source_tool}`. The verbatim_quote must be copied character-for-character from the Stage 1 tool result. If no verbatim quote exists, discard the candidate here. Done when every surviving candidate is a complete structured record.

### Stage 3 — Independent verification

Send each record to Chutes in a fresh context with only the proposition and the verbatim quote. The verifier answers: does this quote support this proposition as written, is anything overstated or misscoped, what qualifier is missing. Use scripts/verify_update.py, which builds the verifier prompt and parses the verdict. Records the verifier marks UNSUPPORTED or OVERSTATED are discarded; records marked QUALIFIED are rewritten to include the qualifier and re-verified once. Done when every surviving record carries a SUPPORTED verdict.

**Model fallback chain (mandatory).** Both the Lane C drafting call and the Lane G critic call use a codified fallback chain, never a single model. On a 429/capacity error, retry the same model up to 4 times with backoff, then move to the next model in the chain. On a max_tokens truncation, automatically issue a continuation call and concatenate. Lane C chain: Qwen/Qwen3.5-397B-A17B-TEE → moonshotai/Kimi-K3-TEE → deepseek-ai/DeepSeek-V3.2-TEE. Lane G chain (must be cross-family from Lane C's final model): zai-org/GLM-5.2-TEE → deepseek-ai/DeepSeek-V3.2-TEE → moonshotai/Kimi-K3-TEE. Record which model actually produced each verdict in the cycle's verification note.

### Stage 4 — Currency and conflict check

For each verified record: check citator treatment via midpage analyzeOpinion for cases, isCurrent via analyzeLaw for statutes and regs. Then grep the target skill's references/ for the existing doctrine the record touches. A record that contradicts current skill doctrine is not auto-merged; it goes to the Doctrine Changes digest section. Done when every record is marked CURRENT and either NO_CONFLICT or CONFLICT.

### Stage 5 — Tiered merge

Auto-merge: records that are CURRENT, NO_CONFLICT, SUPPORTED, and additive (new case, new ruling, new effective date, new citation appended to a current-developments file). Flag for human review: anything that rewrites an analytical framework, edits a checklist, supersedes existing doctrine, or is marked CONFLICT. Auto-merged updates are appended to the skill's references/current-developments.md under a dated heading. Done when every surviving record is either merged with a changelog entry or placed in the flagged list.

**Atomic commit rule (mandatory).** Never commit placeholder content. Stage 5/6 writes follow this exact sequence: (1) assemble the full merged file content in memory; (2) write to a scratch branch or staging file; (3) verify the written content byte-for-byte against the assembled payload (length and hash); (4) only then commit to main in a single commit containing the final content of both current-developments.md and CHANGELOG.md. If verification fails, abort the commit and report the mismatch. A cycle that requires a follow-up "restore full content" commit is a failed cycle and must be reported as such in the digest.

### Stage 6 — Changelog and rollback

Every merge appends one line to the skill's references/CHANGELOG.md: date, domain, proposition summary, citation_url, verification verdicts. The changelog is the rollback index; to revert, remove the dated section from current-developments.md and mark the changelog line REVERTED. Done when the changelog line count equals the merged update count.

## Running a Domain Cycle

1. Read references/skill-registry.md for the target skill's directory, domains, and source list.
2. Read references/sources.md for that domain's authoritative sources and how to query each.
3. Collect developments since the last cycle date (stored in the skill's references/CHANGELOG.md header). Run Stages 1-6.
4. Write the cycle summary: counts collected, discarded at each stage, merged, flagged. Done when the changelog and digest entries exist.
5. Write the heartbeat: append a JSON line to `references/last-run.json` in the updated skill with `{cycle_date, domain, window, collected, discarded_by_stage, merged, flagged, critic_verdict, models_used, commit_sha, status}`. The CTO daily evaluation reads this file first; a missing or stale heartbeat is itself a RED signal.

## Cycle Calendar

Cycles run weekdays only (Monday through Friday), one domain per day per the registry cadence. Saturday and Sunday are no-cycle days by design; the CTO evaluation treats a missing weekend cycle as expected, not a failure. A missed weekday cycle is RED.

## Weekly Digest

After the week's cycles, produce the managing-partner digest: per-domain one-line summaries of merged updates with citation links, the flagged Doctrine Changes list with verbatim quotes and the doctrine each would displace, and any source-scouting findings. The digest is the only routine output the user reviews. Done when the digest is delivered through the configured channel.

## Monthly Source Scouting

Once a month, search for new authoritative sources per domain: new agency open-data portals, new free APIs, newly available MCP servers, new official feeds. Test each candidate source with one real query. Propose additions in the digest with the test result; add to references/sources.md only after user approval. Done when every domain has been scouted or explicitly skipped.

## Quarterly Leak Audit

Once per quarter, verify the confidentiality architecture: grep every specialist skill directory for any string resembling a client name, matter, or identifier from a known-client list the user supplies at audit time; confirm no skill references/ file contains anything but public authority and methodology. Report results in the digest. Done when every skill directory has been scanned and reported clean or remediated.
