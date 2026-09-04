---
name: alphacreek-mcp-2
description: Retrieve SEC and UK FCA filings (10-K, 10-Q, 20-F, 6-K, 8-K) through the AlphaCreek hosted MCP server. Use when the user asks about public company filings, risk factors, MD&A, financial statements, or wants citation-linked filing passages for a ticker. Requires the ALPHACREEK_API_KEY secret.
icon: file-text
color: Blue
---

# AlphaCreek MCP Connector

AlphaCreek is a hosted, read-only MCP server for SEC/FCA filing navigation with citation URLs.

- Endpoint: `https://mcp.alphacreek.ai/mcp` (Streamable HTTP, JSON-RPC 2.0)
- Auth: `Authorization: Bearer $ALPHACREEK_API_KEY` (secret already configured on this agent)
- Tools: `list_filings`, `get_filing_toc`, `read_node_content` (plus one navigation helper)

## How to use

Run the helper client from the sandbox (imports only work inside a skill):

```bash
python3 -c "
import sys; sys.path.insert(0, '/home/user/skills/alphacreek-mcp/scripts')
from alphacreek_client import AlphaCreekMCP
mcp = AlphaCreekMCP()
print(mcp.list_filings('NVDA', document_type='10-K', limit=3))
"
```

Or from sandbox_python, add the scripts dir to sys.path first, then import.

## When to use AlphaCreek vs edgar-search

- Use AlphaCreek (this skill) when the user asks about a public company's filings, risk factors, MD&A, financial statements, or wants citation-linked filing passages for a ticker. It is the default for narrative filing content because every passage comes with a verifiable citation URL.
- Use the `edgar-search` skill instead for full-text search across all EDGAR filings since 2001 and for downloading EX-10 material contract exhibits (clause precedent, deal terms).
- Either way, cite filing content as disclosure or market-practice evidence only, never as legal authority.

## Agent workflow (from the server's own instructions)

1. Call `list_filings` with a ticker (optionally `document_type`, `limit`) to pick a reporting period. Stable filing identity is `artifact_document_id` (e.g. `NVDA_10-K_<accession>`).
2. Call `get_filing_toc` with the `artifact_document_id` to get the filing's navigation map of node IDs.
3. Call `read_node_content` with the specific `node_ids` you need. Content returns with `CITATION_URL` / `CITATION_MARKDOWN` per node.

## Citation rule (required by the server)

If an answer uses text from `read_node_content`, every paragraph or bullet derived from that text MUST end with the inline markdown citation link from the matching `CITATION_MARKDOWN` (or `[TITLE](CITATION_URL)`). Prefer the child node closest to the quoted fact, not the parent TOC node. Do not state filing facts without a citation link beside them.
