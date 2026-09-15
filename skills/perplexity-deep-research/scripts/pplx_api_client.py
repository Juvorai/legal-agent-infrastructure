"""Direct Perplexity Agent API client (primary path).

Perplexity retired sonar-deep-research chat completions (403
agent_api_migration_required; Sonar chat completions sunset 2026-09-27).
The direct path is now the Agent API: POST https://api.perplexity.ai/v1/agent
with tier presets: fast, low, medium (= deep-research), high
(= advanced-deep-research), xhigh (= ultra).

Usage:
    from pplx_api_client import PplxApiClient
    client = PplxApiClient()
    result = client.deep_research("question", preset="high")
    result = client.follow_up("follow-up", previous_response_id=result["response_id"])
"""

import json
import os
import time
from typing import Optional

import requests

API_URL = "https://api.perplexity.ai/v1/agent"
DEFAULT_PRESET = "high"  # advanced-deep-research equivalent


class PplxApiError(RuntimeError):
    pass


class PplxApiClient:
    def __init__(self, api_key: Optional[str] = None, timeout: int = 900):
        self.api_key = api_key or os.environ.get("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise PplxApiError("PERPLEXITY_API_KEY not set")
        self.timeout = timeout

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _post(self, payload: dict) -> dict:
        r = requests.post(API_URL, headers=self._headers(), json=payload, timeout=self.timeout)
        if r.status_code != 200:
            raise PplxApiError(f"HTTP {r.status_code}: {r.text[:500]}")
        return r.json()

    @staticmethod
    def _extract(data: dict) -> dict:
        """Extract answer text, citations, and tool activity from a response object."""
        answer_parts = []
        citations = []
        search_steps = 0
        seen_urls = set()
        for item in data.get("output", []):
            itype = item.get("type")
            if itype == "message":
                for c in item.get("content", []):
                    if c.get("type") == "output_text":
                        answer_parts.append(c.get("text", ""))
                        for ann in c.get("annotations", []) or []:
                            url = ann.get("url")
                            if url:
                                citations.append({
                                    "url": url,
                                    "title": ann.get("title", ""),
                                    "citations": ann.get("citations", []),
                                })
            elif itype in ("web_search_call", "web_search"):
                search_steps += 1
            elif itype in ("search_results", "fetch_url_results"):
                search_steps += 1
                for res in item.get("results", []) or []:
                    url = res.get("url")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        citations.append({
                            "url": url,
                            "title": res.get("title", ""),
                            "date": res.get("date", ""),
                        })
        return {
            "answer": "\n\n".join(answer_parts),
            "sources": citations,
            "search_steps": search_steps,
            "response_id": data.get("id"),
            "status": data.get("status"),
            "model": data.get("model"),
            "usage": data.get("usage", {}),
            "path": "api",
        }

    def deep_research(
        self,
        question: str,
        preset: str = DEFAULT_PRESET,
        instructions: Optional[str] = None,
        file_text: Optional[str] = None,
        extra_tools: Optional[list] = None,
    ) -> dict:
        """Run a deep research question directly against the Agent API.

        file_text: optional document text to inline into the prompt (the Agent
        API has no file_url/pdf_url equivalent; inline the text instead).
        """
        prompt = question
        if file_text:
            prompt = (
                question
                + "\n\n=== DOCUMENT BEGIN ===\n"
                + file_text
                + "\n=== DOCUMENT END ===\n"
                + "Ground every claim about the document in the text above. "
                "Quote section numbers and verbatim clause text."
            )
        payload = {"preset": preset, "input": prompt}
        if instructions:
            payload["instructions"] = instructions
        if extra_tools:
            payload["tools"] = extra_tools
        t0 = time.time()
        data = self._post(payload)
        result = self._extract(data)
        result["elapsed_seconds"] = round(time.time() - t0, 1)
        result["thread_url"] = None  # API path has no web thread
        return result

    def follow_up(
        self,
        question: str,
        previous_response_id: str,
        preset: str = DEFAULT_PRESET,
    ) -> dict:
        payload = {
            "preset": preset,
            "input": question,
            "previous_response_id": previous_response_id,
        }
        t0 = time.time()
        data = self._post(payload)
        result = self._extract(data)
        result["elapsed_seconds"] = round(time.time() - t0, 1)
        result["thread_url"] = None
        return result

    @staticmethod
    def audit_citations(answer: str, sources: list, attachment_names: list) -> dict:
        """Same contract as PplxClient.audit_citations for the browser path."""
        if not attachment_names:
            return {"ok": True, "reason": "no attachments"}
        mentioned = [n for n in attachment_names if n.lower() in answer.lower()]
        if not mentioned:
            return {
                "ok": False,
                "reason": "CORPUS_MISMATCH: none of the attached filenames appear in the answer",
                "mentioned": [],
            }
        return {"ok": True, "reason": "attachment names present", "mentioned": mentioned}

    # ── Path 2b: Sonar file-attachment mode (document Q&A) ──────────────
    #
    # SUNSET WARNING (hard-coded): Sonar Chat Completions shuts down on
    # September 27, 2026. After that date this method returns HTTP 403
    # agent_api_migration_required and NO Perplexity API supports file
    # attachment — fall back to inlining extracted text into the Agent API
    # (deep_research(file_text=...)) or the Browserbase project path.
    #
    # Use this path when native Perplexity file parsing (PDF/DOC/DOCX/TXT/RTF)
    # beats local text extraction: scanned-ish layouts, tables, or when the
    # caller wants Perplexity's own document understanding. Limits: 50MB per
    # file, max 30 files per request. This is single-pass Q&A with web
    # grounding, NOT multi-step deep research.

    SONAR_SUNSET_DATE = "2026-09-27"

    def sonar_file_qa(
        self,
        question: str,
        file_paths: Optional[list] = None,
        file_urls: Optional[list] = None,
        model: str = "sonar-pro",
        instructions: Optional[str] = None,
        web_search: bool = False,
    ) -> dict:
        """Document Q&A with native file attachment via Sonar Chat Completions.

        file_paths: local files, base64-encoded (no data: prefix).
        file_urls: publicly accessible URLs returning the file directly.
        model: sonar-pro (default) or sonar. NOT sonar-deep-research (403).
        web_search: enable web_search_domain_filter-free grounding (sonar
            models search the web by default; set search_recency_filter etc.
            via extra params if needed).

        Raises PplxApiError with a migration hint on 403 after sunset.
        """
        import base64
        import datetime as _dt

        today = _dt.date.today()
        sunset = _dt.date.fromisoformat(self.SONAR_SUNSET_DATE)
        if today > sunset:
            raise PplxApiError(
                "Sonar Chat Completions sunset on 2026-09-27. File attachment "
                "is no longer available on any Perplexity API. Use "
                "deep_research(file_text=...) with locally extracted text, or "
                "the Browserbase project path."
            )
        days_left = (sunset - today).days
        if days_left <= 30:
            import warnings
            warnings.warn(
                f"Sonar file-attachment mode sunsets in {days_left} days "
                f"({self.SONAR_SUNSET_DATE}). Migrate document Q&A to inlined "
                "text on the Agent API.",
                DeprecationWarning,
                stacklevel=2,
            )

        content = [{"type": "text", "text": question}]
        attached_names = []
        for fp in file_paths or []:
            import os as _os
            b64 = base64.b64encode(open(fp, "rb").read()).decode("utf-8")
            content.append({"type": "file_url", "file_url": {"url": b64}})
            attached_names.append(_os.path.basename(fp))
        for url in file_urls or []:
            content.append({"type": "file_url", "file_url": {"url": url}})
            attached_names.append(url.rsplit("/", 1)[-1])

        if len((file_paths or []) + (file_urls or [])) > 30:
            raise PplxApiError("Sonar file limit: max 30 files per request")

        messages = [{"role": "user", "content": content}]
        if instructions:
            messages.insert(0, {"role": "system", "content": instructions})

        payload = {"model": model, "messages": messages}
        t0 = time.time()
        r = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=self._headers(),
            json=payload,
            timeout=self.timeout,
        )
        if r.status_code == 403 and "agent_api_migration_required" in r.text:
            raise PplxApiError(
                "Sonar Chat Completions has sunset (403 "
                "agent_api_migration_required). Use deep_research(file_text=...) "
                "with locally extracted text, or the Browserbase project path."
            )
        if r.status_code != 200:
            raise PplxApiError(f"HTTP {r.status_code}: {r.text[:500]}")
        data = r.json()
        choice = data["choices"][0]["message"]
        citations = data.get("citations", []) or []
        return {
            "answer": choice.get("content", ""),
            "sources": [{"url": u, "title": ""} for u in citations],
            "model": data.get("model"),
            "usage": data.get("usage", {}),
            "elapsed_seconds": round(time.time() - t0, 1),
            "path": "sonar_files",
            "attached_names": attached_names,
            "thread_url": None,
            "response_id": data.get("id"),
            "sunset": self.SONAR_SUNSET_DATE,
        }
