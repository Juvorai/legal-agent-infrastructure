# Changelog

## [1.1.0] - 2026-09-04

### Added
- skills/ directory: all 15 shared skills synced from Chutes_Legal_Privileged
  - alphacreek-mcp-2, ben-writing-style-2, chutes-api, chutes-first-routing
  - design, edgar-search, gc-clo-tech-startup-2, legal-deep-research
  - office-doc-engine, perplexity-deep-research, private-tech-financial-analysis-2
  - server-discovery, shared-config, tax-research, tone
- clause-library/limitation-of-liability: 7 clauses from EDGAR EX-10 filings
- clause-library/indemnification: 8 clauses from EDGAR EX-10 filings
- scripts/: chutes_client.py, style_check.py, verify_redline.py, agent_config.py
- shared-config/agent_config.py: parameterized config reader for multi-agent use

### Notes
- Skills contain some hardcoded references (edgar-search USER_AGENT, docx_builder AUTHOR)
  that need parameterization via agent_config.py in a future update
- Clause library will grow over time as more EDGAR filings are processed

## [1.0.0] - 2026-09-03

### Added
- Initial repository structure
- ARCHITECTURE.md with multi-agent design, isolation guarantees, and new-agent checklist
- templates/AGENT_TEMPLATE.md for creating new legal agents
- templates/SHARED_INFRASTRUCTURE.md (canonical shared infrastructure section)
- VERSION.json for sync tracking
- CHANGELOG.md: change history
