# Drive Context Loader — reference

## Credential

| Name | Label | Required | Hint |
|------|-------|----------|------|
| `DRIVE_FOLDER_ID` | Google Drive Folder ID | yes | Paste the folder ID from the Drive URL (`https://drive.google.com/drive/folders/<THIS_PART>`) |

Read at runtime via `os.environ["DRIVE_FOLDER_ID"]` after the secret is bound. Do not hardcode folder IDs in the skill.

## Gumloop gdrive tools used

| Step | Tool slug | Role |
|------|-----------|------|
| List folder | `gdrive__list_contents` | Current file set (`folder_id`, `recursive: false`) |
| Find manifest | `gdrive__search` | Locate `manifest.json` in the folder |
| Download | `gdrive__download_file` | Manifest + context files |
| Delete old manifest | `gdrive__delete` | Remove prior `manifest.json` before rewrite |
| Write manifest | `gdrive__create_plain_text_file` | Persist updated manifest JSON |

Discovery first (`tool_discovery`), then `tool_executor` for one off calls. Use gumloop-sdk in sandbox only when batching or chaining needs custom logic.

## Listing JSON shape (`current_files.json`)

Array of objects (extra fields ignored):

```json
[
  {
    "id": "1abc...",
    "name": "brief.md",
    "mimeType": "text/markdown",
    "modifiedTime": "2026-08-01T12:00:00.000Z"
  }
]
```

The script drops:

- `mimeType == application/vnd.google-apps.folder`
- `name == manifest.json`

## Prior manifest shape

Object keyed by file id:

```json
{
  "1abc...": {
    "name": "brief.md",
    "mimeType": "text/markdown",
    "modifiedTime": "2026-08-01T12:00:00.000Z"
  }
}
```

## Diff script CLI

```bash
python3 /home/user/skills/drive-context-loader/scripts/load_context.py \
  <folder_id> \
  <current_files.json> \
  [manifest.json]
```

### Stdout result

```json
{
  "run_type": "baseline",
  "summary": "=== Drive Context Loader: BASELINE RUN ===\n...",
  "stats": {
    "total": 3,
    "new": 3,
    "modified": 0,
    "removed": 0,
    "unchanged": 0
  },
  "to_download": [
    { "id": "1abc...", "name": "brief.md", "reason": "new" }
  ],
  "removed": [],
  "manifest": {
    "1abc...": {
      "name": "brief.md",
      "mimeType": "text/markdown",
      "modifiedTime": "2026-08-01T12:00:00.000Z"
    }
  }
}
```

Delta classification:

- **new**: id not in old manifest
- **modified**: id present but `modifiedTime` differs
- **unchanged**: id present and `modifiedTime` matches
- **removed**: id in old manifest but missing from current listing

`run_type` is `baseline` when no prior manifest is loaded (empty or omitted); otherwise `delta`.

## Suggested local layout

```
/home/user/drive_context/
  current_files.json
  manifest_prev.json          # optional, from prior download
  diff_result.json            # optional, saved script stdout
  files/
    brief.md
    ...
```

## Original export notes

Exported from a skill package (`version: 1`, `exportedAt: 2026-08-11`) named `drive-context-loader`. Original docs referenced proprietary names (`GoogleDriveSearchFiles`, `GoogleDriveDownloadFile`, `GoogleDriveCreateFileFromText`). This Gumloop port maps those steps onto the connected `gdrive` server tools listed above. Diff engine behavior in `scripts/load_context.py` is preserved from the export.
