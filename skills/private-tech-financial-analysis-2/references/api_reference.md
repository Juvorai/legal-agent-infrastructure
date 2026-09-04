# Chutes API reference

## Auth

```http
Authorization: Bearer <CHUTES_API_KEY>
```

Create keys in the Chutes dashboard. Prefer agent-scoped secret binding in Gumloop so team members share one mapping without pasting keys into chat.

## LLM gateway

Base: `https://llm.chutes.ai/v1`

OpenAI-compatible. Works with the official `openai` Python package:

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["CHUTES_API_KEY"],
    base_url="https://llm.chutes.ai/v1",
)
r = client.chat.completions.create(
    model="unsloth/Mistral-Nemo-Instruct-2407-TEE",
    messages=[{"role": "user", "content": "Hi"}],
)
print(r.choices[0].message.content)
```

Stdlib-only path: `scripts/chutes_client.py` (no extra pip deps).

## GET /v1/models

Returns `{ "object": "list", "data": [ model, ... ] }`.

Useful model fields:

| Field | Meaning |
|-------|---------|
| `id` | Model string for chat/completions |
| `pricing.prompt` / `pricing.completion` | USD per 1M tokens |
| `context_length` / `max_model_len` | Context window |
| `input_modalities` / `output_modalities` | e.g. text, image, video |
| `supported_features` | json_mode, tools, structured_outputs, reasoning |
| `confidential_compute` | TEE when true |
| `quantization` | e.g. fp8, fp4, int4 |

Model inventory changes; always re-list rather than relying on a static table.

## POST /v1/chat/completions

Standard OpenAI chat payload:

```json
{
  "model": "unsloth/Mistral-Nemo-Instruct-2407-TEE",
  "messages": [
    {"role": "system", "content": "Be brief."},
    {"role": "user", "content": "Hello"}
  ],
  "max_tokens": 256,
  "temperature": 0.2
}
```

Response: OpenAI-style `choices[0].message.content` and `usage`.

Streaming: supported on chat and text completions (`"stream": true`) if the client handles SSE.

## Management API

Base: `https://api.chutes.ai`

- `GET /users/me` — username, balance, keys metadata (with API key auth)
- Other chute/image/node management endpoints exist; LLM inference should use `llm.chutes.ai`

## Cost tips

1. Default to the cheapest text model that works.
2. Cap `max_tokens`.
3. Prefer short system prompts.
4. Check balance via `whoami` / `/users/me` before large batch jobs.

## Docs

- Auth: https://chutes.ai/docs/api-reference/authentication
- API reference hub: https://chutes.ai/docs/api-reference
