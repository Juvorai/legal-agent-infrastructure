#!/usr/bin/env python3
"""
agent_config.py - Shared configuration reader for multi-agent legal infrastructure.
Reads agent-specific configuration from /home/user/.workspace/agent/agent_config.json.
All shared skills use this to avoid hardcoding client-specific values.
"""

import json
import os
from typing import Optional, Any

CONFIG_PATH = "/home/user/.workspace/agent/agent_config.json"

# Defaults (used when config file is missing or incomplete)
DEFAULTS = {
    "author": "Benjamin Snipes",
    "user_agent": "Legal Agent Research",
    "contact_email": "",
    "company_name": "",
    "perplexity_project_url": "",
}

_config_cache = None


def load_config() -> dict:
    """Load agent configuration, with caching."""
    global _config_cache
    if _config_cache is not None:
        return _config_cache
    
    config = dict(DEFAULTS)
    
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                file_config = json.load(f)
            config.update(file_config)
        except (json.JSONDecodeError, IOError):
            pass
    
    _config_cache = config
    return config


def get_author() -> str:
    """Get the tracked changes / document author name."""
    return load_config().get("author", DEFAULTS["author"])


def get_user_agent() -> str:
    """Get the User-Agent string for external API calls (EDGAR, etc.)."""
    config = load_config()
    company = config.get("company_name", "")
    contact = config.get("contact_email", "")
    base = config.get("user_agent", DEFAULTS["user_agent"])
    
    if company and contact:
        return f"{company} {base} ({contact})"
    elif company:
        return f"{company} {base}"
    return base


def get_contact_email() -> str:
    """Get the contact email for API User-Agent headers."""
    return load_config().get("contact_email", "")


def get_company_name() -> str:
    """Get the company name this agent serves."""
    return load_config().get("company_name", "")


def get_perplexity_project_url() -> str:
    """Get the Perplexity project URL for this agent."""
    return load_config().get("perplexity_project_url", "")


def get(key: str, default: Any = None) -> Any:
    """Get any config value by key."""
    return load_config().get(key, default)


if __name__ == "__main__":
    config = load_config()
    print(json.dumps(config, indent=2))
