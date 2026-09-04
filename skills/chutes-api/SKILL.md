# chutes-api

Call Chutes.ai OpenAI-compatible LLM APIs from the sandbox. Use when listing Chutes models, running chat completions, or binding CHUTES_API_KEY for another agent/team.

## Configuration

- **Base URL:** https://llm.chutes.ai/v1
- **API Key:** Read from environment variable `CHUTES_API_KEY`
- **Default model:** `Qwen/Qwen3-235B-A22B-Thinking-2507-TEE`
- **Chute slug:** chutes-qwen-qwen3-235b-a22b-thinking-2507-tee

## Usage

Use `scripts/chutes_client.py` for all LLM calls:

```python
from scripts.chutes_client import chutes_chat, chutes_chat_json

# Simple completion
response = chutes_chat("Summarize this contract clause: ...")

# With specific model
response = chutes_chat("...", model="deepseek-ai/DeepSeek-V3-0324")

# JSON output
result = chutes_chat_json("Extract these fields from the text: ...", schema_hint={"fields": ["name", "date"]})
```

## Available Models (common)

| Model | Use Case |
|-------|----------|
| Qwen/Qwen3-235B-A22B-Thinking-2507-TEE | Default. General reasoning, drafting, analysis. |
| deepseek-ai/DeepSeek-V3-0324 | Heavy reasoning, complex analysis. |
| deepseek-ai/DeepSeek-R1-0528 | Chain-of-thought reasoning tasks. |
| Qwen/Qwen2.5-VL-72B-Instruct | Vision tasks (document images). |

## Rules

1. Always use this skill for LLM work. Never use Gumloop platform LLM APIs.
2. If CHUTES_API_KEY is not set, report the error. Do not fall back silently.
3. For bulk processing, batch requests with appropriate delays.
4. Log model used and token counts when available.
