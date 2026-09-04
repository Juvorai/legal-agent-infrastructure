# perplexity-deep-research

Use when the user asks a research question that should be routed to Perplexity Deep Research in the configured project, or when submitting follow-ups to existing Perplexity threads, uploading files to Perplexity, or downloading Perplexity artifacts. Activates on any research question unless the user says "answer directly" or "just answer this".

## Configuration

All Perplexity configuration is read from `/home/user/.workspace/agent/pplx_config.json`. This file contains:
- `project_url`: The Perplexity project URL (from COMPANY CONFIGURATION)
- `context_id`: Browserbase persistent context ID
- `active_threads`: Dict mapping topic labels to thread URLs
- `session_info`: Last session details

## Routing Rule

Research questions default to Perplexity Deep Research. Do NOT answer inline unless:
- User says "answer directly", "just answer this", "don't use Perplexity", or "quick answer"
- Question is purely operational (e.g., "what time is it", "format this file")

## Browser Flow

### New Research Question

1. Load config from `/home/user/.workspace/agent/pplx_config.json`
2. Create Browserbase session using persistent context (cookies already saved)
3. Navigate to configured project URL
4. Click "New Thread" or compose area
5. Type the research question
6. Select Deep Research mode
7. Submit
8. Poll for completion (typically 1-5 minutes)
9. Extract full response text and sources
10. Save thread URL to `pplx_config.json` under `active_threads`
11. Present results labeled as "Perplexity Deep Research"

### Follow-Up on Existing Thread

1. Load config, check `active_threads` for matching topic
2. Create Browserbase session
3. Navigate to saved thread URL
4. Type follow-up in reply box
5. Submit
6. Poll for completion
7. Extract response
8. Update thread URL if changed

### Connector Selection

When using Perplexity connectors:
- Prefer "Midpage Custom" (hits Ben's own Midpage API with no limits)
- In the @ picker, type "@Midpage" and select "Midpage Custom"
- If Midpage Custom fails, fall back to "Midpage (Perplexity Premium)"

## Thread Management

- Each distinct research topic gets its own thread
- Thread URLs stored in `pplx_config.json` under `active_threads`
- Topic labels should be descriptive (e.g., "non-compete-enforceability-ca", "saas-liability-caps")
- When user says "new thread" or "start fresh", create new thread

## Scripts

- `scripts/pplx_browser.py` - Browserbase automation for Perplexity interaction
