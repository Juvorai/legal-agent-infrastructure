---
name: docx-redlining
description: "Redline .docx documents with true Word tracked changes (w:ins / w:del) at word level, exactly like a human reviewer. Use whenever the user asks to redline, mark up, or show edits in a Word document, compare two versions of a contract, or produce a blackline. Enforces two rules: only the words that actually change get marked (never strike and retype a whole paragraph for a one-word change), and the tracked-changes author is always Benjamin Snipes (never ask the user for an author name)."
icon: file-diff
color: Red
---

# DOCX Redlining — Human-Style Tracked Changes

Produce real Word tracked changes that open in Word's Review pane as insertions and deletions, attributed to a named author. Never fake redlines with strikethrough formatting, colored text, or a separate markup table.

## The Two Standing Rules

1. **Mark only what changes.** If one word in a paragraph changes, only that word is deleted and its replacement inserted. The rest of the paragraph stays byte-identical. Striking an entire paragraph and retyping it to change a single word is a failure mode — it buries the real edit, destroys negotiation history, and no competent human reviewer does it. Whole-paragraph deletion or insertion is correct ONLY when the paragraph is genuinely removed or genuinely new.
2. **The author is always Benjamin Snipes. Never ask.** Hard and fast rule: every redline, tracked change, and blackline produced by this agent is authored as "Benjamin Snipes". Do not ask the user in whose name the redlines should be made; do not offer author-name options; do not use any other name unless the user expressly overrides it for a specific document in that conversation. The script still enforces a non-empty author (`Redliner` and `redline_documents` raise `ValueError` on an empty author); always pass `author="Benjamin Snipes"`. If the user names a different author in the request, use that name verbatim for that document only; the standing default reverts to Benjamin Snipes for every subsequent redline.

## How To Redline

All work goes through `scripts/redline.py`. Do not hand-assemble OOXML.

### Targeted edits (preferred)

Use this when you know the specific changes to make — the normal case for contract review.

```python
import sys
sys.path.insert(0, "/home/user/skills/docx-redlining/scripts")
from redline import Redliner

r = Redliner("/home/user/contract.docx", author="Benjamin Snipes")  # standing author; never ask
r.replace_text(
    "shall be governed by the laws of Delaware",
    "shall be governed by the laws of New York",
)
r.replace_text("three (3) years", "five (5) years")
r.save("/home/user/contract_redline.docx")
```

`replace_text(old, new)` locates the paragraph containing `old`, substitutes `new`, and diffs old against new at word level. Only the differing words are wrapped in `w:del` / `w:ins`; everything else is untouched. Raises `ValueError` if `old` is not found — fix the search text, do not fall back to rewriting the paragraph.

For edits you have already composed paragraph by paragraph, use `r.redline_paragraph_at(index, new_text)`.

### Whole-document comparison

Use this when you have an original and a revised file and need the blackline between them.

```python
from redline import redline_documents
redline_documents("original.docx", "revised.docx",
                  author="Benjamin Snipes", out="redline.docx")
```

Paragraphs are aligned by similarity, each aligned pair is diffed at word level, and paragraphs with no counterpart are marked inserted or deleted as a whole (the correct treatment for genuinely new or removed paragraphs). Output is built on the original file so its styles and formatting survive.

## Workflow

1. Read the source document (python-docx or markitdown) and decide the edits.
2. **Use `author="Benjamin Snipes"`** (standing rule; never ask the user). Only a different name expressly given by the user in the request overrides it, for that document only.
3. Apply edits with `Redliner.replace_text` (targeted) or `redline_documents` (two versions).
4. Save and `export_to_user`. Keep the same filename on revisions so versions chain.
5. Tell the user the redlines are tracked changes under the given name and can be accepted or rejected in Word's Review pane.

## Verification

Before delivering, unzip the output and confirm the `w:ins` / `w:del` elements wrap only the changed words and every one carries `w:author` with the author name (Benjamin Snipes by default, or the user's express override):

```python
import zipfile, re
xml = zipfile.ZipFile("redline.docx").read("word/document.xml").decode()
re.findall(r'<w:delText[^>]*>([^<]*)</w:delText>', xml)  # deleted words only
```

If a whole paragraph appears inside `w:del` when only a word changed, the edit was done wrong — redo it with `replace_text`.

## Scripts

- `scripts/redline.py`: `Redliner` class (targeted word-level edits), `redline_documents` (two-file blackline), and the paragraph diff engine. Author is mandatory; there is no default.
