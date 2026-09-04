"""
Perplexity Deep Research client via Browserbase.

Canonical interface for this agent (and any Chutes-scoped agent) to interact
with Perplexity Deep Research through browser automation.

Usage:
    from pplx_client import PplxClient
    
    client = PplxClient()
    result = client.deep_research("What is the current state of AI regulation in the EU?")
    print(result["answer"])
    print(result["thread_url"])
"""

import json
import os
import re
import time
import asyncio
import requests
from pathlib import Path
from typing import Optional

# Config path (persistent across conversations)
CONFIG_PATH = "/home/user/.workspace/agent/pplx_config.json"
BB_API_BASE = "https://api.browserbase.com/v1"

# Perplexity UI selectors (mapped 2026-09-03)
SELECTORS = {
    "textbox": "#ask-input",
    "submit_btn": "button[aria-label='Submit']",
    "search_mode_btn": "button:has-text('Search')",
    "deep_research_option": "[data-radix-popper-content-wrapper] >> text=Deep research",
    "model_btn": "button[aria-label='Model']",
    "file_input": "input[multiple][accept]",
    "attach_btn": "button[aria-label='Add files or tools']",
    "new_link": "a[aria-label='New']",
    "project_tabs": "[aria-label='Project tabs']",
}

# Completion indicators
COMPLETION_MARKERS = [
    "Finished",
]

IN_PROGRESS_MARKERS = [
    "Researching",
    "Searching",
    "Reading",
    "Analyzing",
    "Thinking",
    "Working on it",
    "Starting",
]


class PplxClient:
    """Client for Perplexity Deep Research via Browserbase cloud browser."""

    def __init__(self, config_path: str = CONFIG_PATH):
        self.config_path = config_path
        self.config = self._load_config()
        self.api_key = self._get_api_key()
        self.headers = {
            "X-BB-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        self._pw = None
        self._browser = None
        self._page = None
        self._context = None
        self._session_id = None

    def _load_config(self) -> dict:
        with open(self.config_path) as f:
            return json.load(f)

    def _save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def _get_api_key(self) -> str:
        # Try env var first, then key file
        key = os.environ.get("BROWSERBASE_API_KEY")
        if key:
            return key
        key_file = "/home/user/.bb_key"
        if os.path.exists(key_file):
            with open(key_file) as f:
                return f.read().strip()
        raise RuntimeError("No Browserbase API key found")

    def _create_session(self, timeout: int = 900) -> dict:
        """Create a new Browserbase session with persistent context."""
        resp = requests.post(
            f"{BB_API_BASE}/sessions",
            headers=self.headers,
            json={
                "projectId": self.config["project_id"],
                "keepAlive": True,
                "timeout": timeout,
                "browserSettings": {
                    "context": {
                        "id": self.config["context_id"],
                        "persist": True,
                    },
                    "viewport": {"width": 1440, "height": 900},
                },
            },
            timeout=30,
        )
        resp.raise_for_status()
        session = resp.json()
        self._session_id = session["id"]
        self.config["session_id"] = session["id"]
        self.config["connect_url"] = session.get("connectUrl")
        self._save_config()
        return session

    def _end_session(self):
        """End the current Browserbase session."""
        if self._session_id:
            try:
                requests.post(
                    f"{BB_API_BASE}/sessions/{self._session_id}",
                    headers=self.headers,
                    json={"status": "REQUEST_RELEASE"},
                    timeout=15,
                )
            except Exception:
                pass
            self._session_id = None

    async def _connect(self):
        """Connect Playwright to the Browserbase session."""
        from playwright.async_api import async_playwright

        if not self._session_id:
            self._create_session()

        self._pw = await async_playwright().start()
        self._browser = await self._pw.chromium.connect_over_cdp(
            self.config["connect_url"]
        )
        self._context = self._browser.contexts[0]
        self._page = (
            self._context.pages[0]
            if self._context.pages
            else await self._context.new_page()
        )

    async def _disconnect(self):
        """Disconnect Playwright and end session."""
        if self._browser:
            try:
                await self._browser.close()
            except Exception:
                pass
        if self._pw:
            try:
                await self._pw.stop()
            except Exception:
                pass
        self._end_session()

    async def _navigate_to_project(self):
        """Navigate to the Chutes.ai project page."""
        project_url = self.config["project_url"]
        await self._page.goto(project_url, wait_until="domcontentloaded", timeout=45000)
        await self._page.wait_for_timeout(3000)

        # Verify we're on the project page
        title = await self._page.title()
        if "Just a moment" in title:
            raise RuntimeError("Cloudflare challenge detected. Cookies may have expired.")
        return title

    async def _navigate_to_thread(self, thread_url: str):
        """Navigate to an existing thread."""
        await self._page.goto(thread_url, wait_until="domcontentloaded", timeout=45000)
        await self._page.wait_for_timeout(3000)

    async def _type_question(self, question: str, connectors: Optional[list] = None):
        """Type a question into the compose area, optionally with @connector mentions."""
        textbox = self._page.locator(SELECTORS["textbox"])
        await textbox.click(timeout=10000)
        await self._page.wait_for_timeout(500)

        # Clear any existing text
        await self._page.keyboard.press("Control+a")
        await self._page.keyboard.press("Backspace")
        await self._page.wait_for_timeout(300)

        # Add connectors via @ mentions if specified
        if connectors:
            for connector in connectors:
                await self._page.keyboard.type(f"@{connector}")
                await self._page.wait_for_timeout(1500)

                # Click the matching option in the typeahead picker
                picker = self._page.locator("[role='listbox']#typeahead-menu")
                option = picker.locator(f"text={connector}")
                count = await option.count()
                if count > 0:
                    await option.first.click(timeout=5000)
                    await self._page.wait_for_timeout(500)
                else:
                    # Fallback: press Enter to select first match
                    await self._page.keyboard.press("Enter")
                    await self._page.wait_for_timeout(500)

        # Type the question
        await self._page.keyboard.type(question, delay=10)
        await self._page.wait_for_timeout(500)

    async def _select_deep_research_mode(self):
        """Select Deep Research mode from the Search dropdown."""
        # Click the Search mode button to open dropdown
        search_btn = self._page.locator(SELECTORS["search_mode_btn"]).first
        await search_btn.click(timeout=5000)
        await self._page.wait_for_timeout(1000)

        # Click "Deep research" option within the popover dropdown
        # Must scope to the radix popper wrapper to avoid matching sidebar text
        popover = self._page.locator("[data-radix-popper-content-wrapper]")
        dr_option = popover.locator("text=Deep research").first
        await dr_option.click(timeout=5000)
        await self._page.wait_for_timeout(500)

    async def _submit(self):
        """Click the Submit button."""
        submit_btn = self._page.locator(SELECTORS["submit_btn"])
        await submit_btn.click(timeout=10000)
        await self._page.wait_for_timeout(2000)

    async def _wait_for_completion(self, timeout_seconds: int = 600) -> bool:
        """Wait for Deep Research to complete. Returns True if completed."""
        start = time.time()
        poll_interval = 8  # seconds

        while time.time() - start < timeout_seconds:
            await self._page.wait_for_timeout(poll_interval * 1000)

            # Check for completion marker in the main content area
            # "Finished" appears when all research steps are done
            completed = await self._page.evaluate("""() => {
                const containers = document.querySelectorAll('[class*="scrollable-container"]');
                for (const c of containers) {
                    const text = c.innerText || '';
                    if (text.includes('Finished')) return true;
                }
                // Also check the main content area
                const mainDivs = document.querySelectorAll('[class*="@container/main"]');
                for (const div of mainDivs) {
                    if ((div.innerText || '').includes('Finished')) return true;
                }
                return false;
            }""")

            if completed:
                return True

        return False

    async def _extract_answer(self) -> dict:
        """Extract the answer text and sources from the completed thread."""
        url = self._page.url
        thread_id = None
        if "/search/" in url:
            thread_id = url.split("/search/")[-1].split("?")[0]

        # Extract the main answer text from the scrollable container
        answer_text = await self._page.evaluate("""() => {
            const containers = document.querySelectorAll('[class*="scrollable-container"]');
            for (const c of containers) {
                const text = c.innerText || '';
                if (text.length > 100 && !text.includes('Sessions')) {
                    return text;
                }
            }
            // Fallback: find the main content area
            const mainDivs = document.querySelectorAll('[class*="@container/main"]');
            for (const div of mainDivs) {
                return div.innerText || '';
            }
            return document.body.innerText;
        }""")

        # Extract sources
        sources = []
        try:
            source_links = await self._page.query_selector_all(
                "a[href^='http']:not([href*='perplexity.ai'])"
            )
            for link in source_links[:30]:
                href = await link.get_attribute("href")
                text = (await link.inner_text()).strip()[:100]
                if href and text and len(text) > 5:
                    sources.append({"title": text, "url": href})
        except Exception:
            pass

        # Extract artifact info if present
        artifacts = []
        try:
            artifact_els = await self._page.query_selector_all(
                "[class*='artifact'], [data-testid*='artifact']"
            )
            for el in artifact_els[:5]:
                text = (await el.inner_text()).strip()[:200]
                if text:
                    artifacts.append(text)
        except Exception:
            pass

        return {
            "answer": answer_text,
            "sources": sources,
            "artifacts": artifacts,
            "thread_url": url,
            "thread_id": thread_id,
        }

    async def _upload_file(self, file_path: str):
        """Upload a file to the compose area."""
        file_input = self._page.locator(SELECTORS["file_input"])
        await file_input.set_input_files(file_path)
        await self._page.wait_for_timeout(2000)

    # ─── Public API ───────────────────────────────────────────────────────

    def deep_research(
        self,
        question: str,
        file_paths: Optional[list] = None,
        connectors: Optional[list] = None,
        timeout_seconds: int = 600,
    ) -> dict:
        """
        Submit a Deep Research question in the Chutes.ai project.

        Args:
            question: The research question to submit.
            file_paths: Optional list of file paths to attach.
            connectors: Optional list of connector names to @-mention
                        (e.g. ["Midpage Custom", "TaxMCP", "AlphaCreek"]).
            timeout_seconds: Max time to wait for completion.

        Returns:
            dict with keys: answer, sources, thread_url, thread_id
        """
        return asyncio.get_event_loop().run_until_complete(
            self._deep_research_async(question, file_paths, connectors, timeout_seconds)
        )

    async def _deep_research_async(
        self,
        question: str,
        file_paths: Optional[list] = None,
        connectors: Optional[list] = None,
        timeout_seconds: int = 600,
    ) -> dict:
        try:
            await self._connect()
            await self._navigate_to_project()
            await self._type_question(question, connectors=connectors)

            # Upload files if provided
            if file_paths:
                for fp in file_paths:
                    await self._upload_file(fp)

            # Select Deep Research mode
            await self._select_deep_research_mode()

            # Submit
            await self._submit()

            # Wait for completion
            completed = await self._wait_for_completion(timeout_seconds)

            if not completed:
                return {
                    "answer": "TIMEOUT: Deep Research did not complete within the time limit.",
                    "sources": [],
                    "thread_url": self._page.url,
                    "thread_id": None,
                    "status": "timeout",
                }

            # Extract results
            result = await self._extract_answer()
            result["status"] = "completed"

            # Save thread to config for follow-ups
            thread_id = result.get("thread_id")
            if thread_id:
                topic_label = question[:60]
                self.config.setdefault("active_threads", {})[topic_label] = {
                    "url": result["thread_url"],
                    "thread_id": thread_id,
                    "created": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                }
                self._save_config()

            return result

        finally:
            await self._disconnect()

    def follow_up(
        self,
        question: str,
        thread_url: str,
        file_paths: Optional[list] = None,
        connectors: Optional[list] = None,
        timeout_seconds: int = 600,
    ) -> dict:
        """
        Submit a follow-up question in an existing thread.

        Args:
            question: The follow-up question.
            thread_url: The URL of the existing thread.
            file_paths: Optional list of file paths to attach.
            connectors: Optional list of connector names to @-mention.
            timeout_seconds: Max time to wait for completion.

        Returns:
            dict with keys: answer, sources, thread_url, thread_id
        """
        return asyncio.get_event_loop().run_until_complete(
            self._follow_up_async(question, thread_url, file_paths, connectors, timeout_seconds)
        )

    async def _follow_up_async(
        self,
        question: str,
        thread_url: str,
        file_paths: Optional[list] = None,
        connectors: Optional[list] = None,
        timeout_seconds: int = 600,
    ) -> dict:
        try:
            await self._connect()
            await self._navigate_to_thread(thread_url)
            await self._type_question(question, connectors=connectors)

            if file_paths:
                for fp in file_paths:
                    await self._upload_file(fp)

            # For follow-ups, just submit (mode is already set from the thread)
            await self._submit()

            completed = await self._wait_for_completion(timeout_seconds)

            if not completed:
                return {
                    "answer": "TIMEOUT: Follow-up did not complete within the time limit.",
                    "sources": [],
                    "thread_url": thread_url,
                    "thread_id": None,
                    "status": "timeout",
                }

            result = await self._extract_answer()
            result["status"] = "completed"
            return result

        finally:
            await self._disconnect()

    def find_thread(self, topic: str) -> Optional[str]:
        """Find a saved thread URL by topic label."""
        threads = self.config.get("active_threads", {})
        # Exact match first
        if topic in threads:
            return threads[topic]["url"]
        # Fuzzy match
        topic_lower = topic.lower()
        for label, info in threads.items():
            if topic_lower in label.lower() or label.lower() in topic_lower:
                return info["url"]
        return None

    def list_threads(self) -> dict:
        """List all saved threads."""
        return self.config.get("active_threads", {})

    def download_artifact(self, session_id: str) -> list:
        """
        List downloads from a Browserbase session.

        Args:
            session_id: The Browserbase session ID.

        Returns:
            List of download metadata dicts.
        """
        resp = requests.get(
            f"{BB_API_BASE}/sessions/{session_id}/downloads",
            headers=self.headers,
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()

    def get_download_content(self, download_id: str) -> bytes:
        """Get the content of a downloaded file."""
        resp = requests.get(
            f"{BB_API_BASE}/downloads/{download_id}",
            headers=self.headers,
            params={"content": "true"},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.content


# ─── CLI entry point ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pplx_client.py <command> [args]")
        print("Commands:")
        print("  research <question>     - Submit Deep Research question")
        print("  follow-up <url> <q>     - Follow up on existing thread")
        print("  threads                 - List saved threads")
        sys.exit(1)

    client = PplxClient()
    cmd = sys.argv[1]

    if cmd == "research":
        question = " ".join(sys.argv[2:])
        result = client.deep_research(question)
        print(json.dumps(result, indent=2, default=str))
    elif cmd == "follow-up":
        url = sys.argv[2]
        question = " ".join(sys.argv[3:])
        result = client.follow_up(question, url)
        print(json.dumps(result, indent=2, default=str))
    elif cmd == "threads":
        threads = client.list_threads()
        print(json.dumps(threads, indent=2))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
