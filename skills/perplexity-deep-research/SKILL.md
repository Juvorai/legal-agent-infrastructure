---
name: perplexity-deep-research
description: Use when the user asks a research question that should be routed to Perplexity Deep Research in the Chutes.ai project, or when submitting follow-ups to existing Perplexity threads, uploading files to Perplexity, or downloading Perplexity artifacts. Activates on any research question unless the user says "answer directly" or "just answer this".
related_server_ids:
- browserbase
---

# Perplexity Deep Research

Canonical interface for routing research questions to Perplexity Deep Research.

**Three paths, in priority order:**

1. **PRIMARY — Direct Agent API** (`pplx_api_client.py`, `PERPLEXITY_API_KEY` env var). Perplexity retired `sonar-deep-research` chat completions (403 `agent_api_migration_required`; Sonar chat completions sunset 2026-09-27). The direct path is now the Agent API: `POST https://api.perplexity.ai/v1/agent` with tier presets (`fast`, `low`, `medium` = deep-research, `high` = advanced-deep-research, `xhigh` = ultra). Use preset `high` by default for legal research; `medium` for ordinary questions. No file attachment — inline document text into the prompt (`file_text=`).
2. **DOCUMENT Q&A — Sonar file-attachment mode** (`PplxApiClient.sonar_file_qa`). Native Perplexity parsing of PDF/DOC/DOCX/TXT/RTF via `file_url` (base64 or public URL) on `sonar-pro` chat completions. Use when native file parsing beats local text extraction (complex layouts, tables, scanned-ish documents) and the task is single-pass document Q&A rather than multi-step deep research. Limits: 50MB per file, max 30 files per request. **HARD SUNSET 2026-09-27**: after that date this path raises with a migration hint; fall back to path 1 with inlined text or path 3. The client warns at 30 days out.
3. **FALLBACK — Browserbase** (`pplx_client.py`) driving the Chutes.ai Perplexity project. Use only when: (a) paths 1-2 fail (key missing, HTTP errors, quota, post-sunset file needs), (b) the task needs the project's MCP connectors (Midpage Custom, TaxMCP, AlphaCreek, Patent Connector), (c) the task needs the project file store or a saved project thread, (d) the task needs multi-step deep research grounded on attached files (never available via any API), or (e) the user explicitly asks for the project/browser path.

**Path tradeoffs:** the Agent API path is fastest, most reliable, and returns structured citations, but has NO file upload and NO access to the Chutes.ai project's connectors or file store. Sonar file mode adds native document parsing but is single-pass Q&A (no deep research agent) and dies 2026-09-27. The Browserbase path keeps connectors, project context, and deep-research-with-attachments but is slower and brittle (Cloudflare, cookie expiry, UI changes, project-file-store contamination).

## Prerequisites

- API path: `PERPLEXITY_API_KEY` env var (bound secret)
- Browserbase path: API key at `/home/user/.bb_key` or in `BROWSERBASE_API_KEY` env var; persistent config at `/home/user/.workspace/agent/pplx_config.json`; Perplexity cookies injected into the Browserbase context (context ID in config)

## Quick Start (PRIMARY: direct API)

```python
import sys
sys.path.insert(0, "/home/user/skills/perplexity-deep-research/scripts")
from pplx_api_client import PplxApiClient

client = PplxApiClient()
result = client.deep_research("What is the current state of AI regulation in the EU?", preset="high")
print(result["answer"])          # full answer text
print(result["sources"])         # structured citations (url, title)
print(result["response_id"])     # for follow-ups
print(result["elapsed_seconds"], result["usage"].get("cost"))
```

### API path commands

```python
# Deep research with a document inlined (no file upload on the API path)
result = client.deep_research(question, preset="high", file_text=open("/home/user/doc.txt").read())

# Follow-up on a prior API response
result = client.follow_up("follow-up question", previous_response_id=result["response_id"])

# Citation audit (same contract as the browser path)
audit = PplxApiClient.audit_citations(result["answer"], result["sources"], ["doc.docx"])
```

API result dict: `{"answer", "sources", "response_id", "status", "model", "usage", "search_steps", "elapsed_seconds", "path": "api", "thread_url": None}`.

### Document Q&A with native file attachment (Sonar mode, sunsets 2026-09-27)

```python
# Local files (base64-encoded automatically) and/or public URLs
result = client.sonar_file_qa(
    "What are the limitation of liability and indemnification provisions?",
    file_paths=["/home/user/contract.pdf", "/home/user/schedule_a.docx"],
    file_urls=["https://example.com/public_exhibit.pdf"],  # optional
    model="sonar-pro",
)
print(result["answer"])           # grounded in the attached files
print(result["sources"])          # web citations if any
print(result["attached_names"])   # what was attached
```

Rules: max 30 files, 50MB each; PDF/DOC/DOCX/TXT/RTF only; documents should be text-based (not scanned images — OCR those first). Single-pass Q&A, not deep research. After 2026-09-27 the method raises `PplxApiError` with a migration hint; within 30 days of sunset it emits a `DeprecationWarning`. Result dict adds `"path": "sonar_files"` and `"sunset": "2026-09-27"`.

### Fallback (Browserbase project path)

```python
from pplx_client import PplxClient

client = PplxClient()
result = client.deep_research("What is the current state of AI regulation in the EU?")
print(result["answer"])
print(result["thread_url"])
```

## Commands

### New Deep Research question

```python
result = client.deep_research(question, file_paths=None, connectors=None, timeout_seconds=600)
```

Returns: `{"answer": str, "sources": list, "thread_url": str, "thread_id": str, "status": str}`

### With connectors (Midpage, TaxMCP, etc.)

```python
result = client.deep_research(
    "What case law exists on 83(b) election deadlines?",
    connectors=["Midpage Custom", "TaxMCP"]
)
```

Available connectors in the Chutes.ai project (as of 2026-09-03):
- Midpage Custom (preferred; fall back to "Midpage (Perplexity Premium)" if Midpage Custom fails)
- TaxMCP
- AlphaCreek
- Patent Connector
- Gmail with Calendar
- Google Drive
- Org Files
- Airtable
- CB Insights

Read `references/niche_mcp_connectors.md` for detailed connector capabilities and selection rules.

### Connector selection rules

| Research type | Connector(s) |
|---------------|-------------|
| Case law, statutes, regulations | Midpage Custom |
| Tax law (IRC, regs, rulings, Tax Court) | TaxMCP |
| SEC filings, securities disclosures | AlphaCreek |
| Patents, trademarks, designs | Patent Connector |
| Multi-domain legal research | Midpage Custom + relevant specialist |

### Follow-up on existing thread

```python
result = client.follow_up(question, thread_url, file_paths=None, connectors=None, timeout_seconds=600)
```

### Find a saved thread by topic

```python
url = client.find_thread("AI regulation")
```

### List all saved threads

```python
threads = client.list_threads()
```

### Upload files with a question

```python
result = client.deep_research(question, file_paths=["/home/user/doc.pdf"])
```

### Download artifacts from a session

```python
downloads = client.download_artifact(session_id)
content = client.get_download_content(download_id)
```

## Routing Rules

1. Research questions default to Perplexity Deep Research. Do NOT answer inline.
2. Default execution path is the direct Agent API (`PplxApiClient`, preset `high` for legal research). For document-grounded Q&A where native file parsing beats local text extraction, use `sonar_file_qa` (until 2026-09-27). Fall back to Browserbase (`PplxClient`) only per the fallback conditions above; if the API fails, retry once, then fall back and note the fallback in the answer to the user.
3. Override phrases: "answer directly", "just answer this", "don't use Perplexity", "quick answer".
4. Each distinct topic gets its own thread (Browserbase path) or response chain via `previous_response_id` (API path). Follow-ups go to the matching saved thread/response.
5. The MCP navigation rule (policy `RhgoSt6DwTrSuwMC2WAqa7`) restricts Browserbase to the Chutes.ai project URL, Perplexity search/thread URLs, and the Perplexity homepage only.

## UI Selectors (mapped 2026-09-03)

| Element | Selector |
|---------|----------|
| Compose textbox | `#ask-input` |
| Submit button | `button[aria-label='Submit']` |
| Search mode dropdown | `button:has-text('Search')` |
| Deep Research option | `text=Deep research` |
| Model selector | `button[aria-label='Model']` |
| File input | `input[multiple][accept]` |
| Attach button | `button[aria-label='Add files or tools']` |

## Error Handling

- **Cloudflare challenge**: If title is "Just a moment...", cookies have expired. Re-inject cookies from user.
- **Timeout**: Deep Research can take 1-5 minutes. Default timeout is 600s. Increase for complex queries.
- **Session expired**: Create a new session. The persistent context retains cookies.

## Thread Management

Threads are saved in `/home/user/.workspace/agent/pplx_config.json` under `active_threads`:

```json
{
  "active_threads": {
    "topic label": {
      "url": "https://www.perplexity.ai/search/<thread-id>",
      "thread_id": "<thread-id>",
      "created": "2026-09-03T12:00:00Z"
    }
  }
}
```

## Corpus integrity (mandatory when attaching files)

The Chutes.ai project file store may contain stale document sets. A 2026-09-06 run grounded on old project files (`Formation/Equity/*`) instead of the attached corpus and produced a wholly wrong audit. Guards, all required:

0. **Pre-flight store check**: before an attached-file run, check the project file store (project URL `?tab=files`) for stale documents on the same topic. Stale same-topic files make the run unreliable even with the fence — remove them or use a clean project first. The fence changes what Perplexity cites, not what it reads.
1. **Upload verification** is built into `_upload_file` — it raises if a filename never appears in the compose area. Never bypass it.
2. **Corpus fence**: when passing `file_paths`, append `PplxClient.corpus_fence([os.path.basename(f) for f in file_paths])` to the question text.
3. **Citation audit**: after completion, run `PplxClient.audit_citations(result["answer"], result["sources"], attachment_names)`. If `ok` is False, the result is CORPUS_MISMATCH — discard the answer, report the mismatch to the user, and rerun (optionally in a fresh thread or after the project files are cleaned). Never present a mismatched answer as findings. Note: a passing citation audit does NOT rule out blended-content contamination (2026-09-07 rerun cited only attached files yet repeated stale-document claims).
4. **Substantive claim verification**: pick the load-bearing claims in the answer and check each against the primary text with exact-string searches. Zero hits on a phrase Perplexity quotes means the claim came from another corpus. Perplexity output is a research lead, never a final authority.

## Chain of Verification (default architecture for high-stakes research)

1. Draft with Chutes (Qwen), grounded on primary documents.
2. Plan verification questions with Chutes: extract every factual claim from the draft as targeted questions.
3. Fact-check with Perplexity Deep Research (this skill), with all corpus guards above.
4. Synthesize with Chutes: correct the draft against verified facts.
5. Parent verification: independently check every load-bearing claim against the primary source before delivery.

Research-First variant (no prior draft): Perplexity gathers cited data first, Chutes analyzes. Double-Perplexity variant (highest accuracy): Perplexity research → Chutes argument → Perplexity audit of final draft → parent verification.

## Done Conditions

- Research question submitted and answer extracted: `result["status"] == "completed"`
- When files were attached: citation audit passed (`ok == True`)
- Thread URL saved to config for future follow-ups
- Answer presented to user with sources
