# chutes-first-routing

Route all LLM work through the Chutes API (llm.chutes.ai) instead of the Gumloop agent runtime, to keep LLM costs on Chutes' covered billing. Use when an agent should default every content-generation task (summaries, extraction, classification, drafting, translation, bulk LLM processing, scheduled/trigger runs) to Chutes and never generate content inline on the Gumloop runtime. Includes the routing policy text, a helper script, and install steps for other agents.

## Routing Policy

The Gumloop agent runtime powers chat reasoning and replies and cannot be rerouted.
But ALL actual LLM *work* done as part of a task MUST go through Chutes.

### What Routes to Chutes

- Summaries / digests of documents, emails, data
- Classification, tagging, categorization
- Extraction of structured fields from unstructured text
- Drafting / rewriting / translation
- Any bulk LLM processing (loop rows/items through Chutes)
- Scheduled runs and trigger-driven LLM work
- Subagent (clone) LLM work

### What Stays Inline (no Chutes call needed)

- Choosing a tool
- Parsing a number
- Picking a branch in logic
- Trivial decisions that don't generate content

### Failure Mode

If Chutes is unavailable, report the error. Do NOT silently fall back to the Gumloop runtime.

## Helper Script

See `scripts/route_to_chutes.py` for a convenience wrapper.

## Install Steps for Other Agents

1. Add this skill to the agent's skills directory.
2. Add the routing policy text to the agent's AGENT.md under "LLM Routing".
3. Ensure CHUTES_API_KEY is configured in the agent's secrets.
4. Test with a simple completion call.
