# Browserbase API Reference for Perplexity Skill

## Session Management

### Create Session
```
POST https://api.browserbase.com/v1/sessions
Headers: X-BB-API-Key: <key>, Content-Type: application/json
Body: {
  "projectId": "<project-id>",
  "keepAlive": true,
  "timeout": 900,
  "browserSettings": {
    "context": {"id": "<context-id>", "persist": true},
    "viewport": {"width": 1440, "height": 900}
  }
}
Response: {id, connectUrl, status, expiresAt, ...}
```

### End Session
```
POST https://api.browserbase.com/v1/sessions/{id}
Body: {"status": "REQUEST_RELEASE"}
```

### Get Session Debug/Live View
```
GET https://api.browserbase.com/v1/sessions/{id}/debug
Response: {debuggerFullscreenUrl, debuggerUrl, pages, wsUrl}
```

## Contexts

### Create Context
```
POST https://api.browserbase.com/v1/contexts
Body: {"projectId": "<project-id>"}
Response: {id, uploadUrl, publicKey, ...}
```

### List Contexts
```
GET https://api.browserbase.com/v1/contexts?projectId=<id>
```

## Downloads

### List Downloads
```
GET https://api.browserbase.com/v1/sessions/{sessionId}/downloads
Response: [{id, sessionId, filename, mimeType, size, checksum, createdAt}]
```

### Get Download Content
```
GET https://api.browserbase.com/v1/downloads/{id}?content=true
Response: binary file content
```

## Uploads

### Create Upload
```
POST https://api.browserbase.com/v1/sessions/{sessionId}/uploads
Body: multipart/form-data with file
Response: {id, filename, size}
```

## Playwright Connection

```python
from playwright.async_api import async_playwright

pw = await async_playwright().start()
browser = await pw.chromium.connect_over_cdp(session["connectUrl"])
context = browser.contexts[0]
page = context.pages[0]
```

## Cookie Injection

```python
# Cookies must be in Playwright format:
# {name, value, domain, path, expires, httpOnly, secure, sameSite}
await context.add_cookies(normalized_cookies)
```

## Key Notes

- Free plan does NOT include Proxies or Verified mode
- Cloudflare-protected sites may block datacenter IPs without proxies
- Cookie injection bypasses Cloudflare for authenticated sessions
- Contexts persist cookies across sessions when `persist: true`
- Session timeout max is 900s on free plan
