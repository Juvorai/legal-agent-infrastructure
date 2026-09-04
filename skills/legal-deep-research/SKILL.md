# legal-deep-research

Conduct grounded, citation-disciplined legal research and analysis in the style of a deep-research report. Use when the user asks a legal research question, wants a memo or analysis of a legal issue, needs multi-source authority gathered and verified, or asks for a deep dive on statutes, cases, or regulations. Enforces tool-grounded citations, verification of authority, Chutes-routed synthesis, and a self-audit pass before delivery.

## When to Activate

Activate for any research question beyond a single lookup:
- Multi-issue legal analysis
- Statutory interpretation questions
- Case law surveys across jurisdictions
- Regulatory compliance analysis
- Memo drafting with citations

## Methodology

### Phase 1: Decompose

Break the research question into discrete sub-questions. Each sub-question should be answerable with 1-3 tool calls.

Example: "Can Chutes enforce its non-compete against a former employee in California?"
- Sub-question 1: What does California Business & Professions Code § 16600 say?
- Sub-question 2: What are the exceptions to § 16600?
- Sub-question 3: What is the relevant case law on out-of-state non-competes?
- Sub-question 4: Does the contract have a choice-of-law provision?
- Sub-question 5: What is the enforceability analysis under the applicable law?

### Phase 2: Gather in Parallel

Execute sub-questions using the appropriate domain tools:
- **Case law and statutes:** Midpage (`midpage__search`, `midpage__analyzeOpinion`, `midpage__searchLaws`)
- **Tax law:** Tax tools (`app__search-tax-law-tool`, `app__lookup-section-tool`)
- **IP/Patent:** Patent Connector (`patent_connector__*`)
- **SEC filings/contractual precedent:** edgar-search skill
- **Internal knowledge:** knowledge_base_search
- **Currency checks/news:** web_search_tool (supplement only, never as legal authority)

Use `invoke_agent` to parallelize when sub-questions are independent.

### Phase 3: Verify

Before relying on any authority:
1. Check `doesNotAddress` fields
2. Check citator treatment (is it still good law?)
3. Check `isCurrent` for statutes
4. Verify jurisdiction match
5. Check procedural posture
6. Distinguish holding from dicta
7. Distinguish majority from concurrence/dissent

If an authority cannot be verified, label it "unverified" and state what would verify it.

### Phase 4: Synthesize Through Chutes

Route the synthesis step through the Chutes API:
1. Compile all gathered authorities with their citations
2. Send to Chutes with a synthesis prompt
3. Chutes produces the analytical narrative
4. Review and refine

Never synthesize inline on the Gumloop runtime.

### Phase 5: Self-Audit

Before delivery, verify:
- [ ] Every legal proposition has a hyperlinked citation
- [ ] No naked citations
- [ ] No short cites (id., supra)
- [ ] No invented pin cites
- [ ] All quotations are verbatim from tool output
- [ ] Non-majority propositions are labeled as such
- [ ] Unverified authorities are flagged
- [ ] Style check passes (run style_check.py)
- [ ] Bluebook format is correct

## Output Format

### Research Memo Structure

1. **Question Presented** (1-2 sentences)
2. **Short Answer** (2-3 sentences, conclusion first)
3. **Analysis** (organized by sub-issue, each with citations)
4. **Conclusion and Recommendations**
5. **Authorities Relied Upon** (full citation list)

### Citation Format

Every citation is a hyperlink. Format per Bluebook rules (see ben-writing-style-2 skill).

## Scripts

- `scripts/research_tracker.py` - Track research progress and citations gathered
