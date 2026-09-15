# Changelog

## [1.2.0] - 2026-09-15

### Changed
- skills/perplexity-deep-research: rewritten from Browserbase-only to three-path routing
  - PRIMARY: direct Perplexity Agent API (POST /v1/agent) via new scripts/pplx_api_client.py (PplxApiClient).
    Presets: medium = deep-research, high = advanced-deep-research (use high for legal research).
    Requires PERPLEXITY_API_KEY bound secret. No file upload; inline document text via deep_research(file_text=...).
  - DOCUMENT Q&A: PplxApiClient.sonar_file_qa() - native PDF/DOC/DOCX/TXT/RTF parsing via sonar-pro
    chat completions with base64 file_url (max 30 files, 50MB each). HARD SUNSET GUARD: raises after
    2026-09-27, DeprecationWarning within 30 days of sunset.
  - FALLBACK: Browserbase project path (scripts/pplx_client.py) for project MCP connectors, project
    file store, saved threads, and deep-research-with-attached-files.
- skills/perplexity-deep-research/scripts/pplx_client.py: Browserbase UI-drift fixes from live testing
  - completion marker now 'Researched' (was 'Finished')
  - deep research reports render in artifact panel; extractor clicks 'Deep research report' for full text
  - upload verification accepts truncated filename chips (regex on stem prefix + extension)
  - mode-dropdown selection skips stale 'Researched' buttons from prior threads
  - session timeout extended to timeout_seconds + 300
- skills/perplexity-deep-research/README.md added: portable install guide for new agents

### Critical
- Perplexity killed sonar-deep-research chat completions (HTTP 403 agent_api_migration_required).
  Sonar chat completions sunsets entirely 2026-09-27. Any agent still calling sonar-deep-research
  via /chat/completions is broken NOW and must adopt this update.

### Verified (live parallel tests, 2026-09-14/15)
- API path beat Browserbase on two legal research questions and a contract redline: zero failures,
  $1.81 total, 3-5 min per run; all 34 verbatim-quote redline edits verified against source contract.
- Browserbase redline failed corpus audit (grounded on stale project files). Citation audit caught it.

### Action required for consuming agents
- Bind PERPLEXITY_API_KEY via bind_env_vars (org-scoped Perplexity key).
- Non-Chutes agents: strip Chutes-specific config (navigation rule ID RhgoSt6DwTrSuwMC2WAqa7,
  Chutes.ai project URL, connector list) or keep Browserbase path disabled.

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
