#!/usr/bin/env python3
"""Minimal Chutes.ai OpenAI-compatible client helpers.

Requires CHUTES_API_KEY in the environment.
Base URL: https://llm.chutes.ai/v1
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

BASE_URL = "https://llm.chutes.ai/v1"
DEFAULT_MODEL = "unsloth/Mistral-Nemo-Instruct-2407-TEE"


def _api_key() -> str:
    key = os.environ.get("CHUTES_API_KEY")
    if not key:
        raise RuntimeError(
            "CHUTES_API_KEY is not set. Bind it with bind_env_vars before calling Chutes."
        )
    return key


def _request(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    timeout: float = 120,
) -> dict[str, Any]:
    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {_api_key()}",
        "Accept": "application/json",
    }
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Chutes API {method} {path} failed ({e.code}): {err}") from e


def list_models() -> list[dict[str, Any]]:
    """Return model objects from GET /v1/models."""
    data = _request("GET", "/models", timeout=60)
    return data.get("data", [])


def chat(
    messages: list[dict[str, str]],
    model: str = DEFAULT_MODEL,
    *,
    max_tokens: int = 256,
    temperature: float = 0.2,
    **extra: Any,
) -> dict[str, Any]:
    """Create a chat completion. Returns the full API response dict."""
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    payload.update(extra)
    return _request("POST", "/chat/completions", payload=payload)


def chat_text(
    prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    system: str | None = None,
    max_tokens: int = 256,
    temperature: float = 0.2,
    **extra: Any,
) -> str:
    """Convenience wrapper that returns assistant text only."""
    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = chat(
        messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        **extra,
    )
    return resp["choices"][0]["message"]["content"]


def account_me(timeout: float = 60) -> dict[str, Any]:
    """Fetch account info from the management API (balance, username)."""
    url = "https://api.chutes.ai/users/me"
    headers = {
        "Authorization": f"Bearer {_api_key()}",
        "Accept": "application/json",
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Chutes API GET /users/me failed ({e.code}): {err}") from e


def _print_models() -> None:
    models = sorted(list_models(), key=lambda m: m.get("id", ""))
    print(f"{len(models)} models\n")
    for m in models:
        mid = m.get("id", "")
        pricing = m.get("pricing") or {}
        ctx = m.get("context_length") or m.get("max_model_len")
        pin = pricing.get("prompt")
        pout = pricing.get("completion")
        feats = ",".join(m.get("supported_features") or [])
        mods = ",".join(m.get("input_modalities") or [])
        print(f"{mid}")
        print(
            f"  $/MTok in={pin} out={pout} | ctx={ctx} | "
            f"tee={m.get('confidential_compute')} | modalities={mods or '-'} | features={feats or '-'}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Chutes.ai helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("models", help="List available models")
    sub.add_parser("whoami", help="Show account username and balance")

    p_chat = sub.add_parser("chat", help="Send a one-shot chat prompt")
    p_chat.add_argument("prompt", help="User prompt")
    p_chat.add_argument("--model", default=DEFAULT_MODEL)
    p_chat.add_argument("--system", default=None)
    p_chat.add_argument("--max-tokens", type=int, default=256)
    p_chat.add_argument("--temperature", type=float, default=0.2)
    p_chat.add_argument("--raw", action="store_true", help="Print full JSON response")

    args = parser.parse_args(argv)

    if args.cmd == "models":
        _print_models()
        return 0

    if args.cmd == "whoami":
        me = account_me()
        print(f"username: {me.get('username')}")
        print(f"user_id: {me.get('user_id')}")
        print(f"balance: {me.get('balance')}")
        return 0

    if args.cmd == "chat":
        messages: list[dict[str, str]] = []
        if args.system:
            messages.append({"role": "system", "content": args.system})
        messages.append({"role": "user", "content": args.prompt})
        resp = chat(
            messages,
            model=args.model,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )
        if args.raw:
            print(json.dumps(resp, indent=2))
        else:
            print(resp["choices"][0]["message"]["content"])
            usage = resp.get("usage")
            if usage:
                print(
                    f"\n[usage model={resp.get('model')} "
                    f"prompt={usage.get('prompt_tokens')} "
                    f"completion={usage.get('completion_tokens')} "
                    f"total={usage.get('total_tokens')}]",
                    file=sys.stderr,
                )
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
