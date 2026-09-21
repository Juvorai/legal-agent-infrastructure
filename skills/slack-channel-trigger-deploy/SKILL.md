---
name: slack-channel-trigger-deploy
description: Use when the user asks to connect an agent to a company Slack workspace so team members can use it without Gumloop accounts, deploy a Slack channel trigger, point an agent at a specific Slack workspace credential, or verify which Slack workspace a credential resolves to. Covers the accountless channel-trigger pattern (no Enterprise plan needed), per-company credential separation, workspace verification guardrails, mention-gated trigger prompts, and end-to-end testing.
related_server_ids: [slack]
---

# Slack Channel Trigger Deployment (Accountless Access)

Deploy an agent into a company Slack workspace via a Slack Message Reader trigger so channel members need no Gumloop account. Requests run under the trigger owner's identity and credentials. This is the non-Enterprise alternative to Organization Service Accounts; if the org is on Enterprise and wants @mention UX with per-request attribution, tell the user about Settings → Organization → Service account instead and stop.

## Hard guardrails (privilege separation)

Agents serving different companies must never touch each other's Slack workspaces. A leaked credential binding can break legal privilege or cross company confidentiality walls.

1. Verify before acting. Before any Slack read, post, or trigger creation, call `slack__get_workspace_info` and confirm the returned `url` matches the target company's workspace URL. If it does not match, stop, disable any trigger just created, and report to the user. Never operate in an unverified workspace.
2. One credential per company workspace. Gumloop holds multiple Slack credentials side by side; each authenticates into exactly one workspace. Bind triggers explicitly to the correct `secret_id`.
3. Nicknames lie. Credential nicknames are user-set and frequently wrong (a credential nicknamed "Chutes" once resolved to a different company entirely). Trust only `get_workspace_info` output and the channel list, never the nickname.
4. Never store another company's workspace IDs, credential IDs, domains, or channel data in this agent's workspace files. Keep only the mapping for the company this agent serves.
5. If the credential picker shows multiple Slack credentials, ask the user which company the task is for. Never default to `is_default: true`.

## Deployment steps

### Step 1: Connect and verify the Slack server

1. If `slack` is not in the agent's servers, call `add_server_awaiter(server_id="slack")`. The user completes OAuth; in the popup they must pick the correct workspace with the workspace switcher (it defaults to their last-used workspace, a common source of wrong-workspace bindings).
2. Call `slack__get_workspace_info`. Done condition: returned `url` and `email_domain` match the target company. If wrong, have the user add a new Slack credential (Settings → Connectors → Slack → Add Credential) selecting the right workspace, and re-verify. Do not delete credentials other agents may use; recommend renaming instead.

### Step 2: Resolve the channel

1. `trigger_discovery(operator_name="Slack Message Reader")` to get the schema and `credentials_to_use`. If the secret has an `options` array (multiple credentials), apply guardrail 5.
2. `list_trigger_options(param_name="Channel", ...)` with the chosen credential. Done condition: the returned channel list visibly belongs to the target company (channel names match the company's naming). Keep the `_option_maps` from the response; it is required in later calls.
3. Have the user pick the channel via `ask_human_input`, inlining the fetched channel names as options. Also ask the response mode: mention-gated (recommended for shared channels) or all-messages.

### Step 3: Get output fields, then create the trigger

1. `list_trigger_options` without `param_name` to get exact output field names. Use them verbatim as `{{field}}` badges; never guess.
2. `create_integration_trigger` with:
   - `credentials_to_use`: the verified credential's `secret_id`.
   - `parameters`: `Channel` (picked name), `Ignore Bot Messages?` = true (loop protection, mandatory), `Ignore Replies?` = false, `Read Full Thread?` = true, `Include Bot Messages In Thread?` = true, plus `_option_maps`.
   - `prompt`: build from references/trigger_prompt_template.md, filling the gating phrases and channel name.
3. Done condition: trigger created and activated; record the `trigger_id`.

### Step 4: Remove the @mention path

Tell the user to run `/gummie remove` in the target channel if the Gumloop mention bot is present. The @mention path runs under each poster's identity and prompts non-Gumloop users to sign up, defeating the accountless goal. Done condition: user confirms, or the bot was never in the channel.

### Step 5: Test

1. The agent cannot fire its own trigger: messages it posts through the connector carry the Gumloop bot identity, and `Ignore Bot Messages` correctly swallows them. Do not treat a silent test as failure; it confirms loop protection works.
2. Ask the user (or any human member) to post a gated message in the channel, e.g. "hey legal, are you live?" Expected: one in-thread reply within about a minute.
3. Then have them post an ungated ordinary message. Expected: silence.
4. Verify with `slack__get_message_thread` on the parent ts. Done condition: gated message got an in-thread reply, ungated message got none.

## Post-deployment record

Persist a small JSON map in `/home/user/.workspace/agent/` (e.g. `slack_workspace_map.json`) containing ONLY: this company's workspace URL, workspace ID, credential `secret_id`, the active trigger IDs with channel and credential bindings, and the guardrail rules. No other company's data.

## Known limitations to state to the user

- No DMs; channel trigger only. DMs require a Custom Slack App, which puts users back on per-user Gumloop accounts.
- All runs use the trigger owner's credentials and credits; set expectations on cost.
- The agent sees sender names for attribution, but Gumloop-side history lives under the owner's account.
- Everyone in the channel can query the agent and everything it can reach (knowledge bases, connectors). If channel membership is broader than the audience for the agent's data, tighten channel membership or use a restricted channel.
- If the org later upgrades to Enterprise, the Organization Service Account path can replace the trigger without rebuilding the agent: re-add the bot, opt the agent in (General Access = Organization + "Allow Slack members without Gumloop accounts", all connectors agent-owned), then disable this trigger.
