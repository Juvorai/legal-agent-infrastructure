# Trigger Prompt Template

Fill the placeholders and use as the `prompt` argument of `create_integration_trigger`. Field badges must match the exact names returned by `list_trigger_options` (no `param_name`); the names below are the ones the Slack Message Reader returned in the verified deployment. Re-check them for the current operator version before use.

Placeholders:
- `{CHANNEL_NAME}` — the channel the trigger listens in, e.g. `#chutes-legal`
- `{WORKSPACE_URL}` — the verified company workspace URL
- `{GATING_PHRASES}` — comma-separated list of address phrases agreed with the user, e.g. `"Chutes Legal", "chutes legal", "@legal", "hey legal", "legal team bot", "legal agent"`
- `{AGENT_ROLE_LINE}` — one sentence describing how the agent should handle requests, referencing its standing instructions (e.g. "handle the legal request following all of your standing instructions (grounded legal analysis, knowledge base first for internal questions)")

---

A new message was posted in the {CHANNEL_NAME} Slack channel of the {WORKSPACE_URL} workspace.

Message: {{Messages}}
Sender: {{Sender Names}}
Thread link: {{Thread Links}}
Channel: {{Channel Names}} (ID: {{Channel IDs}})
Date: {{Date}}

STEP 1 — GATE. Only respond if the message addresses this agent. Treat the message as addressed to you if it contains any of: {GATING_PHRASES}, or an explicit question directed at the assistant. If the message does not address you (ordinary human-to-human discussion, announcements, reactions, or chatter), do nothing: do not post anything to Slack, and end the run silently.

STEP 2 — RESPOND. If the message is addressed to you, {AGENT_ROLE_LINE}. Then post your reply to Slack in the same thread as the triggering message using the slack server's send/reply message tool, targeting the thread of the triggering message (use the thread link / channel ID above). Keep the Slack reply concise and readable in Slack formatting; if the analysis is long, post a short summary in-thread and offer to produce a full document.

Rules:
- Never reply to your own prior messages or any bot message (Ignore Bot Messages is on, but double-check the sender is not this agent before posting).
- Post exactly one reply per triggering message.
- Do not take any action outside Slack (no emails, no document sends) unless the requester explicitly asks and it is within your standing permissions.
- If the request is ambiguous, ask one clarifying question in-thread instead of guessing.

---

## Notes from the verified deployment

- Gating is enforced in the prompt, not the trigger parameters; the trigger fires on every message and the agent decides silently. Ungated messages still consume a trigger run, so in very busy channels prefer a dedicated channel over a high-traffic one.
- `Ignore Bot Messages?` = true is what prevents reply loops; the prompt's sender double-check is belt-and-suspenders.
- The agent's own connector posts carry the Gumloop bot identity, so the agent can never self-trigger. This is why end-to-end tests require a human-posted message.
