# Monday.com Build an External Agent — protocol reference

Source: https://developer.monday.com/api-reference/docs/build-an-external-agent (fetched 2026-10-09). All agent API calls require the `API-Version: dev` header.

## Flow

```
monday.com --(signed POST: "agent_triggered")--> your callback URL
your service --(SSE stream / JSON response)--> monday.com (the chat reply)
your service --(GraphQL with the agent's token)--> monday.com (actions on items)
```

Credentials shown once at setup:

- `signing_secret`: verify incoming webhooks (HMAC). Rotated whenever callback_url is set or updated.
- `api_token`: act as the agent when calling the monday.com GraphQL API.

## Who sees what (30 second webhook window)

| Trigger | What monday waits for | What the user sees |
| --- | --- | --- |
| chat | HTTP 200 body within ~30s (SSE or JSON) | That HTTP body is the chat reply |
| mention | HTTP 200 ack (body not shown) | Threaded update posted via GraphQL with the agent token |
| assigned | HTTP 200 ack (body not shown) | Update (or other mutation) posted via GraphQL with the agent token |

## GraphQL helper

```javascript
async function mondayApi(token, query, variables = {}) {
  const res = await fetch('https://api.monday.com/v2', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: token,
      'API-Version': 'dev',
    },
    body: JSON.stringify({ query, variables }),
  });
  return res.json();
}
```

## Create the agent (owner token)

```graphql
mutation ConnectCustomAgent($input: ConnectExternalAgentSyncInput!) {
  connect_external_agent_sync(input: $input) {
    agent_id
    signing_secret
    api_token
    instructions
  }
}
```

Variables: `{"input": {"custom": {"name": "My Custom Agent", "callback_url": "https://..."}}}`. Synchronous and slow (~25s); use a 40s+ client timeout. signing_secret and api_token are returned only once.

## Update callback URL

`update_custom_agent(input: {callback_url})`. With the agent's own api_token, omit agent_id (monday resolves the agent from the token). Setting or changing callback_url rotates the signing_secret; name-only updates return `signing_secret: null` (do not overwrite a stored secret with null).

## Confirm an agent token

```graphql
query { me { id name kind email } }
```

Accept only `me.kind` of `external_agent_member` or `external_agent_detached_member`. Custom agent emails look like `agent-<CUSTOM_AGENT_ID>@agent.monday.com`.

## Activate

Newly created agents start inactive:

```graphql
mutation { activate_agent(id: 1234567890) { success } }
```

## Grant board access

The agent acts under its own identity; user access does not carry over.

```graphql
mutation {
  add_agent_resource_access(
    id: 1234567890,
    resource_id: 9876543210,
    scope_type: BOARD,
    permission_type: READ_WRITE
  ) { success }
}
```

scope_type BOARD or DOC; READ_WRITE required to create/edit items or post updates. Also grantable in the UI from the agent page, Knowledge and access.

## Webhook headers

| Header | Example | Use |
| --- | --- | --- |
| x-monday-agent-id | 139988 | Which agent fired |
| x-monday-signature | sha256=a3a6ce... | HMAC of the body |
| x-monday-timestamp | 1782326623754 | Epoch milliseconds; part of the signed string |
| content-type | application/json | Body is JSON |

## Body envelope

```json
{
  "event": "agent_triggered",
  "triggerType": "chat",
  "payload": { "text": "..." },
  "timestamp": "2026-06-24T18:43:43.754Z",
  "stream": true
}
```

triggerType: chat, assigned, mention, or unknown. Aliases mentioned/assign may appear; normalize them. stream defaults to true: reply with SSE. When false, reply with JSON `{"message": "..."}`.

### chat payload

Minimal, no IDs, only text: `{"text": "sent this message through agent chat"}`. The reply must be in the HTTP response.

### assigned payload

```json
{
  "text": "You were assigned to an item. Follow these steps:\n1. ...\n\nTRIGGER DATA:\n- itemId: 12334011531\n- boardId: 18418747579\n- groupId: topics",
  "itemId": 12334011531,
  "boardId": 18418747579,
  "groupId": "topics",
  "updateId": null,
  "replyId": null,
  "updateBody": null,
  "files": null
}
```

Item name not included; fetch via GraphQL if needed. Ack quickly, then act via the API.

### mention payload

```json
{
  "text": "<monday-generated instruction prompt>",
  "itemId": 123456789,
  "boardId": 987654321,
  "updateId": 111222333,
  "updateBody": "user update text where @agent was mentioned",
  "replyId": null,
  "files": null
}
```

Prefer `payload.updateBody` for the user's words. Reply with create_update using item_id + parent_id (= updateId). Limits: 30s timeout, response body <= 1 MB.

## Signature verification

HMAC-SHA256 over `${timestamp}.${rawBody}` with the signing_secret, hex digest prefixed with `sha256=`, constant-time compare against x-monday-signature. HMAC the raw unparsed body bytes; re-serializing parsed JSON breaks the check.

```javascript
function verifySignature(signingSecret, rawBody, headers) {
  const timestamp = headers['x-monday-timestamp'];
  const received  = headers['x-monday-signature'];
  if (!timestamp || !received) return false;
  const expected = 'sha256=' + crypto
    .createHmac('sha256', signingSecret)
    .update(`${timestamp}.${rawBody}`)
    .digest('hex');
  const a = Buffer.from(expected);
  const b = Buffer.from(received);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}
```

## Responding

- chat: keep the request open; return SSE or JSON. Plain JSON like `{"text": "..."}` does NOT render; the run shows "Something went wrong while running the agent."
- mention/assigned: return HTTP 200 quickly with an empty SSE ack (`data: [DONE]`) or empty JSON `{"message": ""}` if stream is false, then work via GraphQL.

SSE format: `Content-Type: text/event-stream`, events `data: {"type":"text","content":"<piece>"}` separated by blank lines, terminated by `data: [DONE]`. monday concatenates the content pieces. Rules: respond within 30 seconds, body <= 1 MB, status 200.

## Acting as the agent

```graphql
mutation ($itemId: ID!, $body: String!, $parentId: ID) {
  create_update(item_id: $itemId, body: $body, parent_id: $parentId) { id text_body }
}
```

For assigned items, create_update without parent_id. For mentions, parent_id = payload.updateId.

## Disconnect

```graphql
mutation { disconnect_external_agent(id: 1234567890) { success } }
```

Revokes the token and deletes the agent (owner token). To rotate lost credentials, disconnect and reconnect.
