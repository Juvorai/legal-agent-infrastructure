#!/usr/bin/env python3
"""
Drive Context Loader — diff engine and context summarizer.

Takes the current folder file listing (JSON from GoogleDriveSearchFiles) and the
previous manifest (JSON), computes what's new/changed/removed, and emits an
action plan plus a structured context summary.

Usage:
    python3 load_context.py <folder_id> <files_json_path> [manifest_json_path]

Inputs:
    folder_id          — Google Drive folder ID
    files_json_path    — Path to JSON file with current folder contents
                         (array of {id, name, mimeType, modifiedTime})
    manifest_json_path — Path to previous manifest (optional; omit on first run)

Output (stdout JSON):
    {
        "run_type": "baseline" | "delta",
        "summary": "Human-readable context summary",
        "stats": { "total": N, "new": N, "modified": N, "removed": N, "unchanged": N },
        "to_download": [{ "id": "...", "name": "...", "reason": "new"|"modified" }],
        "removed": [{ "name": "...", "id": "..." }],
        "manifest": { ... updated manifest to upload back ... }
    }

The manifest is a JSON object mapping file ID → {name, mimeType, modifiedTime}.
"""

import json
import sys
from datetime import datetime


def load_manifest(path):
    """Load existing manifest from a JSON file, or return empty dict."""
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def parse_files(raw):
    """Normalize the file listing from GoogleDriveSearchFiles output."""
    files = []
    for item in raw:
        fid = item.get("id")
        name = item.get("name", "unknown")
        mime = item.get("mimeType", "application/octet-stream")
        mod_time = item.get("modifiedTime", "")
        # Skip folders and the manifest itself
        if mime == "application/vnd.google-apps.folder":
            continue
        if name == "manifest.json":
            continue
        files.append({"id": fid, "name": name, "mimeType": mime, "modifiedTime": mod_time})
    return files


def classify_name(name, mime):
    """Return a human-readable label for a file's type."""
    if mime == "application/vnd.google-apps.document":
        return f"Google Doc: {name}"
    elif mime == "application/vnd.google-apps.spreadsheet":
        return f"Google Sheet: {name}"
    elif mime == "application/vnd.google-apps.presentation":
        return f"Google Slides: {name}"
    elif mime == "application/pdf":
        return f"PDF: {name}"
    elif mime and mime.startswith("image/"):
        return f"Image: {name}"
    elif mime and mime.startswith("text/"):
        return f"Text: {name}"
    elif "markdown" in (mime or ""):
        return f"Markdown: {name}"
    else:
        return f"File: {name}"


def build_summary(run_type, current_files, added, modified, removed, unchanged):
    """Build a human-readable context summary."""
    lines = []
    lines.append(f"=== Drive Context Loader: {run_type.upper()} RUN ===\n")

    if run_type == "baseline":
        lines.append(f"First run — loaded {len(current_files)} files from the context folder.\n")
    else:
        lines.append(f"Total files: {len(current_files)}")
        if added:
            lines.append(f"  + {len(added)} new")
        if modified:
            lines.append(f"  ~ {len(modified)} modified")
        if removed:
            lines.append(f"  - {len(removed)} removed")
        lines.append(f"  = {len(unchanged)} unchanged\n")

    if added:
        lines.append("NEW FILES:")
        for f in added:
            lines.append(f"  • {classify_name(f['name'], f.get('mimeType', ''))}")
        lines.append("")

    if modified:
        lines.append("MODIFIED FILES:")
        for f in modified:
            lines.append(f"  • {classify_name(f['name'], f.get('mimeType', ''))}")
        lines.append("")

    if removed:
        lines.append("REMOVED FILES:")
        for f in removed:
            lines.append(f"  • {f['name']}")
        lines.append("")

    if run_type == "baseline":
        lines.append("CURRENT FILES:")
        for f in current_files:
            lines.append(f"  • {classify_name(f['name'], f['mimeType'])}")
        lines.append("")

    return "\n".join(lines)


def build_manifest(files):
    """Build a manifest dict from the current file listing."""
    return {
        f["id"]: {
            "name": f["name"],
            "mimeType": f["mimeType"],
            "modifiedTime": f["modifiedTime"],
        }
        for f in files
    }


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: load_context.py <folder_id> <files_json_path> [manifest_json_path]"}))
        sys.exit(1)

    folder_id = sys.argv[1]
    files_path = sys.argv[2]
    manifest_path = sys.argv[3] if len(sys.argv) > 3 else None

    # Load current file listing
    with open(files_path) as f:
        raw_files = json.load(f)

    current_files = parse_files(raw_files)
    old_manifest = load_manifest(manifest_path) if manifest_path else {}

    # Diff
    current_ids = {f["id"] for f in current_files}
    old_ids = set(old_manifest.keys())

    added = []
    modified = []
    unchanged = []

    for f in current_files:
        fid = f["id"]
        if fid not in old_ids:
            added.append(f)
        elif f["modifiedTime"] != old_manifest[fid].get("modifiedTime"):
            modified.append(f)
        else:
            unchanged.append(f)

    removed_ids = old_ids - current_ids
    removed = [
        {"id": rid, "name": old_manifest[rid]["name"]} for rid in removed_ids
    ]

    run_type = "baseline" if not old_manifest else "delta"

    # Build output
    new_manifest = build_manifest(current_files)

    result = {
        "run_type": run_type,
        "summary": build_summary(run_type, current_files, added, modified, removed, unchanged),
        "stats": {
            "total": len(current_files),
            "new": len(added),
            "modified": len(modified),
            "removed": len(removed),
            "unchanged": len(unchanged),
        },
        "to_download": [
            {"id": f["id"], "name": f["name"], "reason": "new"}
            for f in added
        ]
        + [
            {"id": f["id"], "name": f["name"], "reason": "modified"}
            for f in modified
        ],
        "removed": removed,
        "manifest": new_manifest,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
