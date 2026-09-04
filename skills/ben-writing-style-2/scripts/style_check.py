#!/usr/bin/env python3
"""
style_check.py - Validates text against Ben's writing style rules.
Usage: python3 style_check.py <file_or_text>
Returns: JSON with hard_failures, warnings, and stats.
"""

import sys
import re
import json

BANNED_WORDS = [
    "delve", "dive deep", "deep dive", "leverage", "utilize", "facilitate",
    "streamline", "cutting-edge", "state-of-the-art", "game-changer",
    "paradigm shift", "holistic", "synergy", "robust", "seamless",
    "frictionless", "empower", "unlock", "unleash", "tapestry", "mosaic",
    "in today's world", "in the current environment", "it's important to note",
    "at the end of the day", "moving forward", "circle back", "touch base",
    "low-hanging fruit", "best-in-class", "world-class", "next-level",
]

BANNED_CONSTRUCTIONS = [
    (r"not\s+(?:just|merely|only|simply)?\s*\w+[^.]*,\s*but\s+", "not X, but Y juxtaposition"),
    (r"(?:Great question|Absolutely|I'd be happy to help|Sure thing|Of course)[!.,]", "assistant-voice sycophancy"),
    (r"(?:I hope this helps|Let me know if you need anything else)", "trailing qualifier"),
    (r"(?:Let me explain|Here's what I found)", "announcement prefix"),
]

# Compound words where hyphens are grammatically correct
ALLOWED_HYPHENS = [
    "well-known", "state-of-the-art", "long-term", "short-term", "real-time",
    "high-quality", "low-cost", "best-practice", "case-by-case", "day-to-day",
    "end-to-end", "first-class", "full-time", "part-time", "multi-year",
    "non-compete", "non-disclosure", "non-solicitation", "non-infringement",
    "non-exclusive", "non-transferable", "non-refundable", "non-waiver",
    "co-founder", "co-own", "co-author", "re-enter", "re-establish",
    "self-insured", "self-funded", "self-executing", "self-insurance",
    "third-party", "third-parties", "arm's-length", "attorney-client",
    "work-product", "e-discovery", "e-mail", "IP-based", "AI-powered",
    "SaaS-based", "cloud-based", "web-based", "API-based",
]


def check_text(text):
    results = {
        "hard_failures": [],
        "warnings": [],
        "stats": {},
    }

    # Check banned words (case-insensitive)
    text_lower = text.lower()
    for word in BANNED_WORDS:
        if word in text_lower:
            results["hard_failures"].append(f"Banned word/phrase: '{word}'")

    # Check banned constructions
    for pattern, label in BANNED_CONSTRUCTIONS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            results["hard_failures"].append(f"Banned construction ({label}): '{m.strip()}'")

    # Check dashes/hyphens
    # Find all hyphens and em/en dashes
    em_dashes = re.findall(r'\u2014', text)
    en_dashes = re.findall(r'\u2013', text)
    
    if em_dashes:
        results["hard_failures"].append(f"Em dash found ({len(em_dashes)} occurrences). Remove all em dashes.")
    if en_dashes:
        results["hard_failures"].append(f"En dash found ({len(en_dashes)} occurrences). Remove all en dashes.")

    # Check hyphens - allow compound words
    hyphen_words = re.findall(r'\b\w+-\w+(?:-\w+)*\b', text)
    disallowed_hyphens = []
    for hw in hyphen_words:
        hw_lower = hw.lower()
        if hw_lower not in ALLOWED_HYPHENS:
            # Check if it's a prefix pattern (re-, co-, non-, self-, etc.)
            if re.match(r'^(re|co|non|self|multi|anti|pro|sub|pre|post|inter|intra|cross|over|under|out|up|down)-', hw_lower):
                continue
            disallowed_hyphens.append(hw)
    
    if disallowed_hyphens:
        results["hard_failures"].append(
            f"Disallowed hyphenated words: {', '.join(disallowed_hyphens[:10])}"
        )

    # Check colons outside series (warning)
    colon_sentences = re.findall(r'[^:]+:\s+[^:\n]+', text)
    for cs in colon_sentences:
        # If what follows the colon is not a list item, flag it
        after_colon = cs.split(':')[1].strip()
        if not re.match(r'^\d+[\.\)]\s', after_colon) and not re.match(r'^[-•*]\s', after_colon):
            results["warnings"].append(f"Colon possibly outside series: '{cs.strip()[:80]}'")

    # Check semicolons (warning)
    semicolons = text.count(';')
    if semicolons > 0:
        results["warnings"].append(f"Semicolons found ({semicolons}). Verify they are in genuine series only.")

    # Stats
    sentences = re.split(r'[.!?]+\s', text)
    sentences = [s for s in sentences if len(s.strip()) > 3]
    if sentences:
        lengths = [len(s.split()) for s in sentences]
        results["stats"] = {
            "sentence_count": len(sentences),
            "avg_sentence_length": round(sum(lengths) / len(lengths), 1),
            "min_sentence_length": min(lengths),
            "max_sentence_length": max(lengths),
            "word_count": len(text.split()),
        }

    results["pass"] = len(results["hard_failures"]) == 0
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 style_check.py <file_or_text>")
        sys.exit(1)

    arg = sys.argv[1]
    
    # Check if it's a file
    try:
        with open(arg, 'r') as f:
            text = f.read()
    except (FileNotFoundError, IsADirectoryError):
        text = arg

    results = check_text(text)
    print(json.dumps(results, indent=2))
    
    if not results["pass"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
