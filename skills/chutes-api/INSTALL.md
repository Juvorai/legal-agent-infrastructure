# Install Chutes API skill on another Gumloop agent

## What you get

```
chutes-api/
├── SKILL.md                 # Agent instructions (required)
├── INSTALL.md               # This file
├── scripts/
│   └── chutes_client.py     # CLI + importable helpers
└── references/
    └── api_reference.md     # Endpoint details
```

## Option A — Copy into the agent skills folder

1. Place the folder at:
   ```
   /home/user/skills/chutes-api/
   ```
2. Validate:
   ```bash
   python3 /home/user/skills/.tools/quick_validate.py chutes-api
   ```
3. Bind the secret on **that** agent:
   - Env var name: `CHUTES_API_KEY`
   - Scope: **agent** (recommended for team sharing) or **user**
4. Smoke test:
   ```bash
   python3 /home/user/skills/chutes-api/scripts/chutes_client.py whoami
   python3 /home/user/skills/chutes-api/scripts/chutes_client.py models
   python3 /home/user/skills/chutes-api/scripts/chutes_client.py chat "ping" --max-tokens 16
   ```

## Option B — Tell the receiving agent

Paste this to the other agent:

> Install the attached `chutes-api` skill under `/home/user/skills/chutes-api/`.
> Bind secret env `CHUTES_API_KEY` (agent scope). Then run
> `python3 /home/user/skills/chutes-api/scripts/chutes_client.py models`
> and confirm chat works. Never print the API key.

## Secret handling

- Do **not** put API keys in SKILL.md, git, Slack, or chat.
- Each Gumloop agent/workspace needs its own secret binding (or shared org secret mapped to `CHUTES_API_KEY`).
- Teams can share one Chutes account key via agent-scoped binding, or use separate keys per team.

## CLI cheat sheet

```bash
# Account
python3 /home/user/skills/chutes-api/scripts/chutes_client.py whoami

# Models
python3 /home/user/skills/chutes-api/scripts/chutes_client.py models

# Chat
python3 /home/user/skills/chutes-api/scripts/chutes_client.py chat "Your prompt" \
  --model Qwen/Qwen3-235B-A22B-Thinking-2507-TEE \
  --max-tokens 256
```

## Python import

```python
import sys
sys.path.insert(0, "/home/user/skills/chutes-api/scripts")
from chutes_client import chat_text, list_models, account_me
```
