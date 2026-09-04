"""Minimal Streamable HTTP MCP client for the AlphaCreek filing server.

Usage:
    from alphacreek_client import AlphaCreekMCP
    mcp = AlphaCreekMCP()                      # reads ALPHACREEK_API_KEY from env
    tools = mcp.list_tools()
    filings = mcp.call("list_filings", {"ticker": "NVDA"})
"""
import os
import requests


class AlphaCreekMCP:
    BASE_URL = "https://mcp.alphacreek.ai/mcp"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ["ALPHACREEK_API_KEY"]
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        })
        self._id = 0
        self._initialize()

    def _rpc(self, method, params=None):
        self._id += 1
        payload = {"jsonrpc": "2.0", "id": self._id, "method": method}
        if params is not None:
            payload["params"] = params
        r = self.session.post(self.BASE_URL, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        if "error" in data:
            raise RuntimeError(f"MCP error {data['error'].get('code')}: {data['error'].get('message')}")
        return data.get("result")

    def _initialize(self):
        return self._rpc("initialize", {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "gumloop-agent", "version": "1.0"},
        })

    def list_tools(self):
        return self._rpc("tools/list")

    def call(self, tool_name, arguments=None):
        """Call an AlphaCreek tool and return the text content."""
        result = self._rpc("tools/call", {"name": tool_name, "arguments": arguments or {}})
        contents = result.get("content", [])
        return "\n".join(c.get("text", "") for c in contents if c.get("type") == "text")

    # Convenience wrappers -------------------------------------------------
    def list_filings(self, ticker, document_type=None, limit=10):
        args = {"ticker": ticker, "limit": limit}
        if document_type:
            args["document_type"] = document_type
        return self.call("list_filings", args)

    def get_filing_toc(self, artifact_document_id=None, ticker=None):
        args = {}
        if artifact_document_id:
            args["artifact_document_id"] = artifact_document_id
        if ticker:
            args["ticker"] = ticker
        return self.call("get_filing_toc", args)

    def read_node_content(self, node_ids):
        if isinstance(node_ids, str):
            node_ids = [node_ids]
        return self.call("read_node_content", {"node_ids": node_ids})
