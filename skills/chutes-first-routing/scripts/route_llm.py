"""Chutes-first routing helper.

Wraps the chutes-api client for easy single and batch LLM calls.
Default model is DeepSeek V4 Flash (TEE). Requires CHUTES_API_KEY env var
bound and the chutes-api skill installed.

Usage:
    from route_llm import chutes_text, chutes_batch
    out = chutes_text("Summarize this.", system="Be concise.")
    results = chutes_batch(items, "Classify: {item}")
"""

import os
import sys

sys.path.insert(0, "/home/user/skills/chutes-api/scripts")
from chutes_client import chat_text  # noqa: E402

DEFAULT_MODEL = "deepseek-ai/DeepSeek-V4-Flash-0731-TEE"


def _require_key() -> str:
    key = os.getenv("CHUTES_API_KEY")
    if not key:
        raise RuntimeError(
            "CHUTES_API_KEY is not bound. Call bind_env_vars for CHUTES_API_KEY "
            "before using Chutes."
        )
    return key


def chutes_text(
    prompt: str,
    system: str | None = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 512,
    temperature: float = 0.2,
) -> str:
    """Run a single Chutes chat completion and return the text."""
    _require_key()
    return chat_text(
        prompt,
        model=model,
        system=system,
        max_tokens=max_tokens,
        temperature=temperature,
    )


def chutes_batch(
    items: list,
    prompt_template: str,
    system: str | None = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 512,
    temperature: float = 0.2,
) -> list[str]:
    """Run one Chutes completion per item. Use {item} in the template."""
    _require_key()
    results = []
    for item in items:
        prompt = prompt_template.format(item=item)
        results.append(
            chat_text(
                prompt,
                model=model,
                system=system,
                max_tokens=max_tokens,
                temperature=temperature,
            )
        )
    return results


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Chutes-first routing helper")
    p.add_argument("prompt", help="Prompt to send")
    p.add_argument("--system", default=None)
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--max-tokens", type=int, default=512)
    a = p.parse_args()
    print(chutes_text(a.prompt, system=a.system, model=a.model, max_tokens=a.max_tokens))
