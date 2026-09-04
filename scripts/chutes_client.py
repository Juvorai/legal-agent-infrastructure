#!/usr/bin/env python3
"""
chutes_client.py - Client for Chutes.ai OpenAI-compatible LLM API.
All LLM work in skills and sandbox MUST route through this client.
"""

import os
import json
import requests
from typing import Optional, List, Dict, Any

BASE_URL = "https://llm.chutes.ai/v1"
DEFAULT_MODEL = "Qwen/Qwen3-235B-A22B-Thinking-2507-TEE"


def _get_api_key() -> str:
    key = os.environ.get("CHUTES_API_KEY")
    if not key:
        raise EnvironmentError(
            "CHUTES_API_KEY is not set. Cannot route LLM call through Chutes. "
            "Do not fall back to another provider silently."
        )
    return key


def chutes_chat(
    prompt: str,
    system: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 4096,
    messages: Optional[List[Dict[str, str]]] = None,
) -> str:
    """
    Send a chat completion request to Chutes API.
    
    Args:
        prompt: User message content.
        system: Optional system message.
        model: Model identifier. Defaults to Qwen3-235B Thinking.
        temperature: Sampling temperature.
        max_tokens: Maximum response tokens.
        messages: Full messages list (overrides prompt/system if provided).
    
    Returns:
        The assistant's response text.
    """
    api_key = _get_api_key()
    model = model or DEFAULT_MODEL

    if messages is None:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        },
        timeout=120,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Chutes API error {response.status_code}: {response.text[:500]}"
        )

    data = response.json()
    return data["choices"][0]["message"]["content"]


def chutes_chat_json(
    prompt: str,
    system: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.1,
    max_tokens: int = 4096,
    schema_hint: Optional[Dict] = None,
) -> Any:
    """
    Send a chat completion request expecting JSON output.
    
    Args:
        prompt: User message (should instruct JSON output).
        system: Optional system message.
        model: Model identifier.
        temperature: Lower temperature for structured output.
        max_tokens: Maximum response tokens.
        schema_hint: Optional schema to include in system prompt.
    
    Returns:
        Parsed JSON object.
    """
    if system is None:
        system = "You are a precise extraction engine. Respond ONLY with valid JSON. No markdown, no explanation."
    
    if schema_hint:
        system += f"\nExpected output schema: {json.dumps(schema_hint)}"

    raw = chutes_chat(
        prompt=prompt,
        system=system,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Try to parse JSON, handling markdown code blocks
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        # Remove first and last lines (``` markers)
        lines = [l for l in lines if not l.strip().startswith("```")]
        raw = "\n".join(lines)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to find JSON object in the response
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
        raise ValueError(f"Could not parse JSON from Chutes response: {raw[:200]}")


def list_models() -> List[Dict[str, Any]]:
    """List available models from Chutes API."""
    api_key = _get_api_key()
    response = requests.get(
        f"{BASE_URL}/models",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=30,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Chutes API error {response.status_code}: {response.text[:500]}")
    return response.json().get("data", [])


if __name__ == "__main__":
    # Quick test
    try:
        result = chutes_chat("Say 'Chutes API connected.' and nothing else.")
        print(f"SUCCESS: {result}")
    except Exception as e:
        print(f"ERROR: {e}")
