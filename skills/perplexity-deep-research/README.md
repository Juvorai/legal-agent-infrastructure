# perplexity-deep-research — portable skill package

Drop-in skill for calling Perplexity directly from any Gumloop agent. Three paths:

1. **Agent API** (`scripts/pplx_api_client.py`, `PplxApiClient`) — primary. Deep research via `POST /v1/agent` with tier presets (`medium` = deep-research, `high` = advanced-deep-research). No file upload; inline document text with `file_text=`.
2. **Sonar file-attachment mode** (`PplxApiClient.sonar_file_qa`) — document Q&A with native PDF/DOC/DOCX/TXT/RTF parsing (base64 or public URL, max 30 files, 50MB each). **Hard sunset 2026-09-27**: after that date the method raises with a migration hint; within 30 days it emits a DeprecationWarning.
3. **Browserbase project path** (`scripts/pplx_client.py`, `PplxClient`) — fallback. Drives a Perplexity web project via Browserbase for MCP connectors (Midpage, TaxMCP, etc.), project file store, saved threads, and deep-research-with-attachments. Optional: skip this path entirely if the new agent has no Browserbase server.

## Install on another agent

1. Copy this folder to the target agent's sandbox at `/home/user/skills/perplexity-deep-research/` (keep the internal layout: `SKILL.md`, `scripts/`, `references/`).
2. Bind the secret: ask that agent to run `bind_env_vars` for `PERPLEXITY_API_KEY` (same key works; Perplexity keys are org-scoped). Paths 1-2 need nothing else.
3. Path 3 only: the target agent needs the Browserbase server connected, a `BROWSERBASE_API_KEY` secret, a Perplexity persistent context with logged-in cookies, and a `pplx_config.json` at `/home/user/.workspace/agent/pplx_config.json` with `project_id`, `context_id`, and `project_url`. If you don't need project connectors, delete `scripts/pplx_client.py` and the Browserbase sections of SKILL.md.
4. Chutes-specific bits to strip or adapt for a non-Chutes agent: the MCP navigation rule ID (`RhgoSt6DwTrSuwMC2WAqa7`), the Chutes.ai project URL, and the connector list in SKILL.md / `references/niche_mcp_connectors.md`.

## Quick smoke test

```python
import sys
sys.path.insert(0, "/home/user/skills/perplexity-deep-research/scripts")
from pplx_api_client import PplxApiClient
c = PplxApiClient()
print(c.deep_research("What is Section 102(b)(7) DGCL?", preset="medium")["answer"][:300])
print(c.sonar_file_qa("Who are the parties?", file_paths=["/path/to/contract.docx"])["answer"][:300])
```

## Verified behavior (2026-09-15, live tests)

- `sonar-deep-research` on `/chat/completions` → HTTP 403 `agent_api_migration_required` (dead).
- `sonar-pro` on `/chat/completions` with base64 `file_url` → HTTP 200, correct document-grounded answer (8.7s on a 53KB .docx).
- `/v1/agent` preset `high` → multi-step deep research, 3-5 min, structured `search_results` items with source URLs, usage cost reported per call.
- Browserbase path works but is brittle (UI drift, session deaths, project-file-store corpus contamination — see the Corpus integrity section of SKILL.md; always run `audit_citations` after attached-file runs).
