#!/usr/bin/env python3
"""Lane-based Chutes model router.

Implements the Chutes Model Routing and Execution policy: every LLM task is
assigned to a lane (A-H), each lane has a primary model and fallbacks, and the
live catalog (GET /v1/models, cached <= 24h) controls availability while this
policy controls purpose and quality tier.

Requires CHUTES_API_KEY in the environment.
Base URL: https://llm.chutes.ai/v1

Usage as a library:
    from route_llm import chutes_text, chutes_batch, chutes_critic, pick_model
    out = chutes_text("Summarize in 3 bullets.", lane="C")

Usage as a CLI:
    python3 route_llm.py lanes                 # lane table with live availability
    python3 route_llm.py catalog [--refresh]   # live catalog summary
    python3 route_llm.py chat "prompt" --lane C
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any

BASE_URL = "https://llm.chutes.ai/v1"
CATALOG_MAX_AGE_HOURS = 24

# Central lane configuration, maintained by the Juvor.ai-Legal-Ops coordinator
# agent in the Juvorai/legal-agent-infrastructure repo. Fetched at runtime,
# cached <= 24h, validated, with the bundled table below as offline fallback.
REMOTE_LANES_URL = (
    "https://raw.githubusercontent.com/Juvorai/legal-agent-infrastructure/"
    "main/chutes-routing/lanes.json"
)
LANES_CONFIG_MAX_AGE_HOURS = 24

# ---------------------------------------------------------------------------
# Lane definitions (policy source of truth for purpose and quality tier)
# ---------------------------------------------------------------------------

LANES: dict[str, dict[str, Any]] = {
    "A": {
        "name": "Ultra-cheap bounded operations",
        "primary": "GLM-4.7-Flash-NVFP4-TEE",
        "fallbacks": ["google/gemma-4-31B-turbo-TEE"],
        "use": "Routing labels, binary relevance decisions, normalization, "
               "simple entity tagging, metadata cleanup, short format conversions.",
        "max_input_tokens": 20_000,
        "max_output_tokens": 1_000,
        "temperature": 0.0,
    },
    "B": {
        "name": "Standard extraction and structured transformation",
        "primary": "google/gemma-4-31B-turbo-TEE",
        "fallbacks": ["Qwen/Qwen3.8-27B-TEE"],
        "use": "Document classification, clause extraction, triage, structured "
               "summaries, table generation, citation metadata extraction.",
        "temperature": 0.1,
    },
    "C": {
        "name": "Standard substantive text work (DEFAULT)",
        "primary": "Qwen/Qwen3.5-397B-A17B-TEE",
        "fallbacks": ["Qwen/Qwen3.8-27B-TEE"],
        "use": "Ordinary drafting, rewriting, synthesis of verified research, "
               "document analysis, memoranda from supplied sources, final prose.",
        "temperature": 0.2,
    },
    "D": {
        "name": "Agentic planning, coding, and high-stakes synthesis",
        "primary": "zai-org/GLM-5.2-TEE",
        "fallbacks": ["Qwen/Qwen3.5-397B-A17B-TEE", "deepseek-ai/DeepSeek-V3.2-TEE"],
        "use": "Multi-step planning, sustained tool use, difficult debugging, "
               "repository-scale coding, >5 dependent actions, >200K-token prompts, "
               "consequential final synthesis.",
        "temperature": 0.2,
    },
    "E": {
        "name": "Maximum-quality escalation (gated)",
        "primary": "moonshotai/Kimi-K3-TEE",
        "fallbacks": ["zai-org/GLM-5.2-TEE"],
        "use": "Only when an escalation gate is met: express user request, "
               "material uncertainty after Lane D + verification, >500K-token "
               "synthesis, Lane D acceptance failure, or final adversarial review.",
        "temperature": 0.2,
    },
    "F": {
        "name": "Bulk million-token preprocessing (provisional output)",
        "primary": "deepseek-ai/DeepSeek-V4-Flash-0731-TEE",
        "fallbacks": ["zai-org/GLM-5.2-TEE"],
        "use": "Preliminary extraction, corpus mapping, chronology construction, "
               "candidate-issue collection over very large inputs. Outputs are "
               "provisional and must be verified against primary text.",
        "temperature": 0.2,
    },
    "G": {
        "name": "Model-family-diverse critic",
        "primary": None,  # resolved by critic_for()
        "fallbacks": ["deepseek-ai/DeepSeek-V3.2-TEE"],
        "use": "Independent critique of a draft produced by a different model "
               "family. Never the same checkpoint as the author.",
        "temperature": 0.1,
    },
    "H": {
        "name": "Vision and multimodal understanding",
        "primary": "Qwen/Qwen3.8-27B-TEE",
        "fallbacks": ["moonshotai/Kimi-K2.6-TEE", "moonshotai/Kimi-K3-TEE"],
        "use": "Screenshots, scanned-page interpretation after OCR, diagrams, "
               "visual UI work. Prefer specialized OCR/transcription endpoints "
               "first when the task is primarily reading text or speech.",
        "temperature": 0.2,
    },
}

DEFAULT_LANE = "C"

# Lane G critic pairing: critic must be a different model family than the author.
CRITIC_PAIRING = {
    "Qwen/Qwen3.5-397B-A17B-TEE": "zai-org/GLM-5.2-TEE",
    "Qwen/Qwen3.8-27B-TEE": "zai-org/GLM-5.2-TEE",
    "zai-org/GLM-5.2-TEE": "Qwen/Qwen3.5-397B-A17B-TEE",
    "moonshotai/Kimi-K3-TEE": "zai-org/GLM-5.2-TEE",
    "moonshotai/Kimi-K2.6-TEE": "Qwen/Qwen3.5-397B-A17B-TEE",
    "deepseek-ai/DeepSeek-V4-Flash-0731-TEE": "zai-org/GLM-5.2-TEE",
    "deepseek-ai/DeepSeek-V3.2-TEE": "Qwen/Qwen3.5-397B-A17B-TEE",
    "google/gemma-4-31B-turbo-TEE": "Qwen/Qwen3.5-397B-A17B-TEE",
}

EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-8B-TEE"

# Models never used as primaries (second opinions / compatibility fallbacks only).
NON_PRIMARY_MODELS = {
    "Qwen/Qwen3-235B-A22B-Thinking-2507-TEE",
    "Qwen/Qwen3-32B-TEE",
    "Qwen/Qwen3.6-27B-TEE",
    "zai-org/GLM-5.1-TEE",
    "moonshotai/Kimi-K2.6-TEE",
    "unsloth/Mistral-Nemo-Instruct-2407-TEE",
}

# Bundled fallback lane table. Used only when the central config is
# unreachable AND no valid cache exists. The central config controls.
_BUNDLED_LANES = LANES
_BUNDLED_CRITIC_PAIRING = CRITIC_PAIRING
_BUNDLED_EMBEDDING = EMBEDDING_MODEL
_BUNDLED_DEFAULT_LANE = DEFAULT_LANE

# ---------------------------------------------------------------------------
# Catalog (live availability source of truth, cached <= 24h)
# ---------------------------------------------------------------------------

def _cache_paths() -> list[str]:
    paths = []
    ws = "/home/user/.workspace/agent"
    if os.path.isdir(ws) and os.access(ws, os.W_OK):
        paths.append(os.path.join(ws, "chutes_catalog_cache.json"))
    paths.append("/tmp/chutes_catalog_cache.json")
    return paths


def _lanes_cache_paths() -> list[str]:
    paths = []
    ws = "/home/user/.workspace/agent"
    if os.path.isdir(ws) and os.access(ws, os.W_OK):
        paths.append(os.path.join(ws, "chutes_lanes_cache.json"))
    paths.append("/tmp/chutes_lanes_cache.json")
    return paths


# ---------------------------------------------------------------------------
# Central lane configuration (Juvor.ai-Legal-Ops coordinator maintains it)
# ---------------------------------------------------------------------------

_lanes_loaded = False


def _validate_lanes_config(cfg: dict) -> bool:
    """Structural validation of the central lanes.json before trusting it."""
    try:
        if not isinstance(cfg, dict):
            return False
        lanes = cfg.get("lanes")
        if not isinstance(lanes, dict) or not lanes:
            return False
        for lane_id, spec in lanes.items():
            if not isinstance(spec, dict):
                return False
            if "primary" not in spec or "fallbacks" not in spec:
                return False
            if spec["primary"] is not None and not isinstance(spec["primary"], str):
                return False
            if not isinstance(spec["fallbacks"], list):
                return False
        return True
    except Exception:
        return False


def get_lanes_config(refresh: bool = False) -> dict:
    """Load the central lane config: remote -> cache -> bundled fallback.

    The central config in Juvorai/legal-agent-infrastructure controls lane
    assignments fleet-wide. The bundled table is used only when both the
    remote fetch and any valid cache fail.
    """
    global LANES, CRITIC_PAIRING, EMBEDDING_MODEL, DEFAULT_LANE, _lanes_loaded
    if _lanes_loaded and not refresh:
        return {"lanes": LANES, "critic_pairing": CRITIC_PAIRING,
                "embedding_model": EMBEDDING_MODEL, "default_lane": DEFAULT_LANE,
                "source": "memory"}

    cfg = None
    source = "bundled"

    if not refresh:
        for p in _lanes_cache_paths():
            try:
                with open(p) as f:
                    cache = json.load(f)
                age_h = (time.time() - cache.get("fetched_at", 0)) / 3600
                if age_h <= LANES_CONFIG_MAX_AGE_HOURS and _validate_lanes_config(cache.get("config") or {}):
                    cfg = cache["config"]
                    source = f"cache:{p}"
                    break
            except Exception:
                continue

    if cfg is None or refresh:
        try:
            req = urllib.request.Request(REMOTE_LANES_URL, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                remote = json.loads(resp.read().decode("utf-8"))
            if _validate_lanes_config(remote):
                cfg = remote
                source = "remote"
                entry = {"fetched_at": time.time(), "config": remote}
                for p in _lanes_cache_paths():
                    try:
                        with open(p, "w") as f:
                            json.dump(entry, f)
                        break
                    except Exception:
                        continue
        except Exception:
            pass  # keep cache or bundled fallback

    if cfg is not None:
        LANES = cfg["lanes"]
        CRITIC_PAIRING = cfg.get("critic_pairing") or _BUNDLED_CRITIC_PAIRING
        EMBEDDING_MODEL = cfg.get("embedding_model") or _BUNDLED_EMBEDDING
        DEFAULT_LANE = cfg.get("default_lane") or _BUNDLED_DEFAULT_LANE
    else:
        LANES = _BUNDLED_LANES
        CRITIC_PAIRING = _BUNDLED_CRITIC_PAIRING
        EMBEDDING_MODEL = _BUNDLED_EMBEDDING
        DEFAULT_LANE = _BUNDLED_DEFAULT_LANE

    _lanes_loaded = True
    return {"lanes": LANES, "critic_pairing": CRITIC_PAIRING,
            "embedding_model": EMBEDDING_MODEL, "default_lane": DEFAULT_LANE,
            "source": source, "updated_at": (cfg or {}).get("updated_at"),
            "updated_by": (cfg or {}).get("updated_by")}


def _api_key() -> str:
    key = os.environ.get("CHUTES_API_KEY")
    if not key:
        raise RuntimeError(
            "CHUTES_API_KEY is not set. Bind it with bind_env_vars before calling Chutes."
        )
    return key


def _request(method: str, path: str, payload: dict | None = None,
             timeout: float = 120) -> dict:
    url = f"{BASE_URL}{path}"
    headers = {"Authorization": f"Bearer {_api_key()}", "Accept": "application/json"}
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


def get_catalog(refresh: bool = False) -> dict[str, dict]:
    """Return {model_id: catalog_entry} from GET /v1/models, cached <= 24h."""
    if not refresh:
        for p in _cache_paths():
            try:
                with open(p) as f:
                    cache = json.load(f)
                age_h = (time.time() - cache.get("fetched_at", 0)) / 3600
                if age_h <= CATALOG_MAX_AGE_HOURS and cache.get("models"):
                    return cache["models"]
            except Exception:
                continue
    data = _request("GET", "/models", timeout=60)
    models = {m["id"]: m for m in data.get("data", []) if m.get("id")}
    entry = {"fetched_at": time.time(), "models": models}
    for p in _cache_paths():
        try:
            with open(p, "w") as f:
                json.dump(entry, f)
            break
        except Exception:
            continue
    return models


def is_available(model_id: str, catalog: dict | None = None) -> bool:
    catalog = catalog if catalog is not None else get_catalog()
    return model_id in catalog


def is_confidential(model_id: str, catalog: dict | None = None) -> bool:
    """True only if the live catalog entry reports confidential_compute truthy.

    Do not infer TEE status from the model name alone.
    """
    catalog = catalog if catalog is not None else get_catalog()
    entry = catalog.get(model_id) or {}
    flags = entry.get("confidential_compute")
    if flags is None:
        # some catalog shapes nest flags under a sub-object
        for key in ("features", "flags", "security"):
            sub = entry.get(key)
            if isinstance(sub, dict) and "confidential_compute" in sub:
                flags = sub["confidential_compute"]
                break
    if flags is None:
        # Flag absent from the live catalog: do not infer TEE status from the
        # model name alone. Treat as non-confidential and refuse sensitive data.
        return False
    return bool(flags)


# ---------------------------------------------------------------------------
# Model selection
# ---------------------------------------------------------------------------

def pick_model(lane: str = DEFAULT_LANE, catalog: dict | None = None,
               author_model: str | None = None) -> str:
    """Resolve the model for a lane against the live catalog.

    For lane G pass author_model so the critic is a different family.
    Falls back through the lane's fallback chain; raises if nothing is live.
    """
    get_lanes_config()  # ensure central config is loaded
    lane = lane.upper()
    if lane not in LANES:
        raise ValueError(f"Unknown lane '{lane}'. Valid: {sorted(LANES)}")
    catalog = catalog if catalog is not None else get_catalog()
    spec = LANES[lane]

    if lane == "G":
        if not author_model:
            raise ValueError("Lane G requires author_model to pick a diverse critic.")
        candidates = [CRITIC_PAIRING.get(author_model), *spec["fallbacks"]]
    else:
        candidates = [spec["primary"], *spec["fallbacks"]]

    for cand in candidates:
        if cand and cand in catalog:
            return cand
    raise RuntimeError(
        f"No live model for lane {lane} ({spec['name']}). "
        f"Tried: {[c for c in candidates if c]}. Refresh the catalog and retry."
    )


# ---------------------------------------------------------------------------
# Audit logging
# ---------------------------------------------------------------------------

def _log_path() -> str:
    ws = "/home/user/.workspace/agent"
    if os.path.isdir(ws) and os.access(ws, os.W_OK):
        return os.path.join(ws, "chutes_routing_log.jsonl")
    return "/tmp/chutes_routing_log.jsonl"


def _audit(record: dict) -> None:
    """Append a routing/usage record. Never log privileged prompt/response bodies."""
    record.setdefault("ts", time.strftime("%Y-%m-%dT%H:%M:%S%z"))
    try:
        with open(_log_path(), "a") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Chat calls
# ---------------------------------------------------------------------------

def _chat(messages: list[dict], model: str, *, max_tokens: int = 4096,
          temperature: float = 0.2, response_format: dict | None = None,
          timeout: float = 300) -> dict:
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if response_format is not None:
        payload["response_format"] = response_format
    return _request("POST", "/chat/completions", payload, timeout=timeout)


def _call_with_failover(messages: list[dict], lane: str, *, max_tokens: int,
                        temperature: float, response_format: dict | None,
                        author_model: str | None, workflow: str) -> tuple[str, str]:
    """Call the lane primary; on timeout/5xx retry once, then use the fallback."""
    catalog = get_catalog()
    model = pick_model(lane, catalog, author_model=author_model)
    attempts = [(model, 2)]  # (model, tries)
    spec = LANES[lane.upper()]
    fallbacks = spec["fallbacks"] if lane.upper() != "G" else []
    for fb in fallbacks:
        if fb in catalog and fb != model:
            attempts.append((fb, 1))
            break

    last_err: Exception | None = None
    for cand, tries in attempts:
        for attempt in range(tries):
            t0 = time.time()
            try:
                resp = _chat(messages, cand, max_tokens=max_tokens,
                             temperature=temperature, response_format=response_format)
                text = resp["choices"][0]["message"]["content"]
                usage = resp.get("usage") or {}
                _audit({
                    "workflow": workflow, "lane": lane.upper(), "model": cand,
                    "prompt_tokens": usage.get("prompt_tokens"),
                    "completion_tokens": usage.get("completion_tokens"),
                    "latency_s": round(time.time() - t0, 2),
                    "retries": attempt, "fallback_used": cand != model,
                    "status": "ok",
                })
                print(f"[chutes lane={lane.upper()} model={cand} "
                      f"prompt={usage.get('prompt_tokens')} "
                      f"completion={usage.get('completion_tokens')}]", file=sys.stderr)
                return cand, text
            except RuntimeError as e:
                last_err = e
                _audit({"workflow": workflow, "lane": lane.upper(), "model": cand,
                        "status": "error", "error": str(e)[:300],
                        "latency_s": round(time.time() - t0, 2)})
                if attempt + 1 < tries:
                    time.sleep(2 ** attempt * 2)  # exponential backoff
    raise RuntimeError(f"All lane {lane.upper()} models failed. Last error: {last_err}")


def chutes_text(prompt: str, *, lane: str = DEFAULT_LANE, system: str | None = None,
                max_tokens: int = 4096, temperature: float | None = None,
                response_format: dict | None = None, workflow: str = "adhoc",
                author_model: str | None = None) -> str:
    """Route one prompt through the given lane and return the completion text."""
    lane = lane.upper()
    spec = LANES[lane]
    if temperature is None:
        temperature = spec.get("temperature", 0.2)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    _, text = _call_with_failover(
        messages, lane, max_tokens=max_tokens, temperature=temperature,
        response_format=response_format, author_model=author_model, workflow=workflow)
    return text


def chutes_batch(items: list[str], prompt_template: str, *,
                 lane: str = DEFAULT_LANE, system: str | None = None,
                 max_tokens: int = 2048, workflow: str = "batch",
                 response_format: dict | None = None) -> list[str]:
    """Loop many items through a lane. Template must contain {item}."""
    return [
        chutes_text(prompt_template.format(item=it), lane=lane, system=system,
                    max_tokens=max_tokens, workflow=workflow,
                    response_format=response_format)
        for it in items
    ]


def chutes_critic(draft: str, source_packet: str, checklist: str, *,
                  author_model: str, max_tokens: int = 4096,
                  workflow: str = "critic") -> str:
    """Lane G independent critique. Author and critic must be different families.

    Returns alleged errors, supporting source spans, missing issues, unresolved
    uncertainty, and proposed corrections. Does not rewrite the deliverable.
    """
    system = (
        "You are an independent critic from a different model family than the "
        "draft's author. Return: (1) alleged errors with supporting source spans, "
        "(2) missing issues, (3) unresolved uncertainty, (4) proposed corrections. "
        "Do not rewrite the deliverable. Only use the supplied source packet; mark "
        "anything unsupported as unsupported."
    )
    prompt = (
        f"CHECKLIST:\n{checklist}\n\nSOURCE PACKET:\n{source_packet}\n\n"
        f"DRAFT (authored by {author_model}):\n{draft}"
    )
    return chutes_text(prompt, lane="G", system=system, max_tokens=max_tokens,
                       workflow=workflow, author_model=author_model)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description="Chutes lane router")
    sub = ap.add_subparsers(dest="cmd", required=True)

    lanes_p = sub.add_parser("lanes", help="lane table with live availability")
    lanes_p.add_argument("--refresh", action="store_true")
    cat = sub.add_parser("catalog", help="live catalog summary")
    cat.add_argument("--refresh", action="store_true")
    ch = sub.add_parser("chat", help="send one prompt through a lane")
    ch.add_argument("prompt")
    ch.add_argument("--lane", default=DEFAULT_LANE)
    ch.add_argument("--system", default=None)
    ch.add_argument("--max-tokens", type=int, default=4096)
    ch.add_argument("--workflow", default="cli")

    args = ap.parse_args()

    if args.cmd == "catalog":
        catalog = get_catalog(refresh=args.refresh)
        print(f"{len(catalog)} models (live)")
        for mid, m in sorted(catalog.items()):
            pricing = m.get("pricing") or {}
            print(f"  {mid}: ctx={m.get('context_length') or m.get('context')} "
                  f"in=${pricing.get('prompt')} out=${pricing.get('completion')}")
    elif args.cmd == "lanes":
        cfg = get_lanes_config(refresh=getattr(args, "refresh", False))
        print(f"lane config source: {cfg['source']} "
              f"(updated_at={cfg.get('updated_at')} updated_by={cfg.get('updated_by')})")
        catalog = get_catalog()
        for lane, spec in LANES.items():
            primary = spec["primary"] or "(resolved per author)"
            live = "LIVE" if spec["primary"] and spec["primary"] in catalog else "not live"
            fbs = ", ".join(f"{f}{'*' if f in catalog else ''}" for f in spec["fallbacks"])
            print(f"Lane {lane}: {spec['name']}")
            print(f"  primary: {primary} [{live}]")
            print(f"  fallbacks (* = live): {fbs}")
            print(f"  use: {spec['use']}")
    elif args.cmd == "chat":
        out = chutes_text(args.prompt, lane=args.lane, system=args.system,
                          max_tokens=args.max_tokens, workflow=args.workflow)
        print(out)


if __name__ == "__main__":
    main()
