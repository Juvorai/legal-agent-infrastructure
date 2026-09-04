#!/usr/bin/env python3
"""Self-audit a legal memo draft before delivery.

Checks:
1. Citation grounding: every [..](..) citation link's target should appear in the
   collected tool outputs dump (deeplinkURLs, provision URLs). Flags citations
   with no matching tool output.
2. Naked citations: Bluebook-looking cites with no hyperlink.
3. Style: delegates to ben-writing-style-2 style_check.py when present, plus
   local checks for dashes/hyphens as punctuation and "not X, but Y".

Usage:
    python3 audit_memo.py <draft_file> [tool_outputs_file]

Exit code 0 when clean (no hard failures), 1 otherwise.
"""
import re
import subprocess
import sys
from pathlib import Path

STYLE_CHECK = Path("/home/user/skills/ben-writing-style-2/style_check.py")

# Bluebook-ish patterns that indicate a citation with no link
NAKED_CITE = re.compile(
    r"\b\d+\s+(?:U\.?S\.?|F\.(?:2d|3d|4th|Supp\.?\s?\d*d?)?|S\.?\s?Ct\.?|"
    r"Cal\.?(?:\s?App\.?)?(?:\s?\dd)?|N\.?Y\.?(?:\s?S\.?)?(?:\s?\dd)?|"
    r"T\.?C\.?(?:\s?Memo\.?)?|A\.?(?:\s?\dd)?|P\.?(?:\s?\dd)?|"
    r"So\.?(?:\s?\dd)?|N\.?E\.?(?:\s?\dd)?|S\.?E\.?(?:\s?\dd)?|"
    r"F\.?R\.?D\.?|B\.?R\.?)\s+\d+"
)
USC_CFR_NAKED = re.compile(r"\b\d+\s+(?:U\.?S\.?C\.?|C\.?F\.?R\.?)\s+§+\s*[\d.]+")
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
NOT_BUT = re.compile(r"\bnot\b[^.?!]{0,80}?\bbut\b", re.IGNORECASE)
DASH_PUNCT = re.compile(r"[—–]|(?<=\s)-(?=\s)|(?<=\w)\s-\s(?=\w)")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    draft_path = Path(sys.argv[1])
    outputs_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    draft = draft_path.read_text(encoding="utf-8")
    corpus = outputs_path.read_text(encoding="utf-8") if outputs_path and outputs_path.exists() else ""

    hard_failures = 0

    # 1. Citation grounding
    links = LINK.findall(draft)
    if not links:
        print("FAIL: no hyperlinked citations found in draft.")
        hard_failures += 1
    else:
        ungrounded = []
        for text, url in links:
            if corpus and url not in corpus:
                ungrounded.append((text, url))
        if corpus and ungrounded:
            print(f"FAIL: {len(ungrounded)} citation link(s) not found in tool outputs:")
            for text, url in ungrounded:
                print(f"  - [{text}]({url})")
            hard_failures += len(ungrounded)
        elif not corpus:
            print("WARN: no tool outputs file supplied; citation grounding not verified.")

    # 2. Naked citations (outside of link syntax)
    stripped = LINK.sub("", draft)
    naked = NAKED_CITE.findall(stripped) + USC_CFR_NAKED.findall(stripped)
    if naked:
        print(f"FAIL: {len(naked)} naked citation(s) without hyperlinks:")
        for n in naked[:20]:
            print(f"  - {n.strip()}")
        hard_failures += len(naked)

    # 3. Local style checks
    dashes = DASH_PUNCT.findall(draft)
    if dashes:
        print(f"FAIL: {len(dashes)} dash/hyphen punctuation instance(s).")
        hard_failures += len(dashes)
    not_but = NOT_BUT.findall(draft)
    if not_but:
        print(f"WARN: {len(not_but)} possible 'not X, but Y' construction(s); review manually.")

    # 4. Delegate to ben-writing-style-2 style_check.py
    if STYLE_CHECK.exists():
        print("\n--- ben-writing-style-2 style_check.py ---")
        result = subprocess.run(
            [sys.executable, str(STYLE_CHECK), str(draft_path)],
            capture_output=True, text=True,
        )
        print(result.stdout)
        if result.returncode != 0:
            hard_failures += 1
            if result.stderr:
                print(result.stderr, file=sys.stderr)
    else:
        print("WARN: style_check.py not found; skipped external style check.")

    print(f"\n{'CLEAN' if hard_failures == 0 else f'{hard_failures} hard failure(s)'}")
    return 0 if hard_failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
