#!/usr/bin/env python3
"""Sync specialist skills from Juvorai/legal-agent-infrastructure into this agent.

Run by each GC agent on its daily schedule (3:45 AM local). Pulls the skills/
tree from the repo, copies updated files into /home/user/skills/, and writes a
sync receipt to /home/user/.workspace/agent/skill-sync-receipt.json so the CTO
daily evaluation can verify the sync actually happened.

Usage: python3 sync_skills.py
Requires: GITHUB_CLASSIC env var (repo read token).
"""
import base64
import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = "Juvorai/legal-agent-infrastructure"
BRANCH = "main"
SKILLS_PREFIX = "skills/"
LOCAL_SKILLS = Path("/home/user/skills")
RECEIPT = Path("/home/user/.workspace/agent/skill-sync-receipt.json")

# Skills this sync manages. Only registry skills (practice groups + ops) are
# pulled; local-only skills (style, tooling) are never overwritten.
MANAGED = [
    "corporate-vc-finance", "securities-capital-markets", "tax-federal-international",
    "labor-employment", "privacy-data", "ai-emerging-tech", "crypto-web3",
    "biotech-life-sciences", "legal-ops-updater", "legal-ops-sources",
    "gc-agent-sources",
]


def gh_api(path):
    token = os.environ.get("GITHUB_CLASSIC", "")
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                 "User-Agent": "juvor-skill-sync"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def fetch_file(path):
    data = gh_api(f"contents/{path}?ref={BRANCH}")
    return base64.b64decode(data["content"]), data["sha"]


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def main():
    started = datetime.now(timezone.utc)
    head = gh_api(f"branches/{BRANCH}")["commit"]["sha"]
    tree = gh_api(f"git/trees/{head}?recursive=1")["tree"]
    remote_files = {
        e["path"]: e for e in tree
        if e["type"] == "blob" and e["path"].startswith(SKILLS_PREFIX)
        and e["path"].split("/")[1] in MANAGED
    }

    updated, unchanged, errors = [], [], []
    for path, entry in sorted(remote_files.items()):
        local = LOCAL_SKILLS / path[len(SKILLS_PREFIX):]
        try:
            content, _ = fetch_file(path)
            if local.exists() and sha256(local.read_bytes()) == sha256(content):
                unchanged.append(path)
                continue
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_bytes(content)
            updated.append(path)
        except Exception as e:
            errors.append({"path": path, "error": str(e)})

    receipt = {
        "synced_at": started.isoformat(),
        "repo": REPO,
        "branch": BRANCH,
        "commit_sha": head,
        "files_updated": len(updated),
        "files_unchanged": len(unchanged),
        "errors": errors,
        "status": "ok" if not errors else "partial",
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2))
    print(json.dumps(receipt, indent=2))
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
