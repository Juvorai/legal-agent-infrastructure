# Niche Legal MCP Connectors Reference

These are the specialized MCP connectors available in the Chutes Perplexity project.
Always prefer the custom/paid versions over native Perplexity Premium versions.

## Midpage Custom (ALWAYS use this, never "Midpage (Perplexity Premium)")

- **URL:** https://www.midpage.ai/
- **What it does:** Legal research data for AI. Full US case law (16M+ opinions), statutes, regulations, and agency guidance. AI-powered citator with treatment signals (negative, caution, neutral). Docket retrieval. Brief drafting and cite checking.
- **Coverage:** All federal case law (appellate + district, including unpublished). All 50 states + DC appellate courts. Select state trial courts. Statutes and regulations across federal and state jurisdictions.
- **Key capabilities:**
  - Case search with citator signals
  - Statute and regulation lookup
  - Docket fetching and briefing retrieval
  - Brief/memo drafting with hyperlinked citations
  - Cite checking
- **Why custom over premium:** The custom version hits Ben's own Midpage API with no usage limits. The native "Midpage (Perplexity Premium)" version has rate limits. Prefer Midpage Custom; fall back to "Midpage (Perplexity Premium)" only if Midpage Custom fails or is unavailable.
- **Perplexity picker name:** "Midpage Custom" (fallback: "Midpage (Perplexity Premium)")

## TaxMCP

- **URL:** https://taxmcp.io/
- **What it does:** AI tax research with real citations. Searches the IRC, Treasury Regulations, IRS Publications, Revenue Rulings, state tax codes, and US Tax Court opinions. Returns source-linked primary authority.
- **Coverage:** Internal Revenue Code, Treasury Regulations, IRS Publications, Revenue Rulings, Revenue Procedures, Private Letter Rulings, state tax codes, US Tax Court opinions.
- **Key capabilities:**
  - IRC section lookup with full text
  - Treasury Regulation retrieval
  - IRS guidance search (publications, rulings, procedures)
  - Tax Court opinion search
  - State tax code lookup
  - Source-linked citations for verification
- **Design philosophy:** "Research, not autonomous tax prep." Returns primary authority so the reviewer can verify. 20 searches/day free tier.
- **Perplexity picker name:** "TaxMCP"

## AlphaCreek

- **URL:** https://www.alphacreek.ai/
- **What it does:** SEC filing context for AI agents. Hosted MCP connection to regulatory filings that are ingested, structured, and citation-ready. Covers SEC EDGAR and UK FCA NSM.
- **Coverage:** 6,000+ US tickers. SEC filings (10-K, 10-Q, 20-F, 6-K, 8-K). UK FCA filings (annual reports, half-year reports, regulatory announcements). EU/Germany integrating next.
- **Key capabilities:**
  - Filing metadata retrieval
  - Table-of-contents navigation per filing
  - Section-level text/table retrieval
  - Citation URLs for source verification
  - < 500ms tool response time
  - < 5 min filing freshness
- **Use for:** Securities filings analysis, risk factor review, MD&A analysis, disclosure comparison, contractual precedent from EX-10 exhibits.
- **Perplexity picker name:** "AlphaCreek"

## Patent Connector

- **URL:** https://patent.dev/
- **What it does:** MCP server connecting directly to official patent offices. Patents, trademarks, and designs across six jurisdictions. No scraping, no aggregators. Official office data.
- **Coverage:** USPTO (US), EPO (Europe), DPMA (Germany), IP Australia, JPO (Japan), TIPO (Taiwan), INPI (France). Patents, trademarks, and designs.
- **Key capabilities:**
  - Patent bibliography, abstract, and search-report citations
  - Legal status from official office records
  - Trademark search including sound/multimedia marks
  - Design registration lookup
  - Classification code explanation (human-readable)
  - Office action retrieval
  - Assignment and continuity data
- **Use for:** Patent prosecution research, prior art searches, trademark clearance, design registration checks, IP portfolio analysis.
- **Perplexity picker name:** Check the @ picker for the exact name (may be "Patent Connector" or similar)

## Connector Selection Rules

| Research type | Connector(s) to use |
|---------------|-------------------|
| Case law, statutes, regulations | Midpage Custom |
| Tax law (IRC, regs, rulings, Tax Court) | TaxMCP |
| SEC filings, securities disclosures | AlphaCreek |
| Patents, trademarks, designs | Patent Connector |
| Multi-domain legal research | Midpage Custom + relevant specialist |
| Securities + corporate law | Midpage Custom + AlphaCreek |
| Tax + corporate structure | Midpage Custom + TaxMCP |
| IP + corporate | Midpage Custom + Patent Connector |
