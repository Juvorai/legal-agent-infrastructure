#!/usr/bin/env python3
"""style_check.py — scan draft text for AI-tell phrases and Ben-style fingerprint stats.

Usage:
    python3 style_check.py draft.txt
    cat draft.txt | python3 style_check.py -

Reports:
  1. Banned AI-tell words/phrases (Part 2.1 of the skill)
  2. Structural risks: "It is important to note"-type constructions, negation
     parallelism runs, hedge piles, uniform sentence-length runs, orphan bullets
  3. Fingerprint stats to compare with Ben's baseline:
     avg sentence length ~26.7 words, stdev ~14.7; heavy use of Thus/However/
     For example; ~0 occurrences of furthermore/moreover/in conclusion.
"""
import re, sys, statistics, collections

BANNED = [
    "delve into", "delve", "tapestry", "rich tapestry", "multifaceted", "plethora",
    "myriad", "cornucopia", "symphony of", "dance of",
    "in today's fast-paced world", "in today's world", "in an increasingly",
    "ever-evolving landscape", "it is important to note", "it's important to note",
    "it's worth noting", "it is worth noting", "it should be noted", "notably,",
    "navigate the complexities", "shed light on", "sheds light", "underscore",
    "highlights the importance", "highlight the importance", "pivotal",
    "crucial role", "plays a crucial", "game-changer", "paradigm shift",
    "cutting-edge", "state-of-the-art", "revolutionize", "groundbreaking",
    "testament to", "stands as a testament", "elevate", "unlock", "unleash",
    "harness the power", "embark on", "journey of", "seamless", "robust",
    "holistic", "leverage", "utilize", "utilise",
    "furthermore", "moreover", "additionally,", "firstly", "secondly", "thirdly",
    "in conclusion", "to sum up", "to summarize", "in summary", "overall,",
    "when it comes to", "at its core", "in essence", "at the end of the day",
    "bustling", "vibrant", "stark contrast", "dive into", "deep dive", "unpack",
    "look no further", "we've got you covered", "whether you're a",
    "i hope this email finds you well", "i hope this message finds you well",
    "i hope this finds you well", "as an ai", "i'm just an ai",
]

BEN_WORKHORSES = ["thus", "however", "for example", "while", "since", "because",
                  "generally", "ultimately", "likewise", "in fact", "in other words",
                  "that is", "and yet", "nonetheless", "ideally", "instead"]

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "-"
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    low = text.lower()
    words = re.findall(r"[A-Za-z'’/-]+", text)
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'\u201c(])", text) if len(s.strip()) > 3]
    lens = [len(re.findall(r"[A-Za-z'’/-]+", s)) for s in sents]

    print("=" * 64)
    print("STYLE CHECK — ben-writing-style")
    print("=" * 64)

    hits = []
    for b in BANNED:
        c = low.count(b)
        if c:
            hits.append((c, b))
    print("\n1. AI-TELL PHRASES (banned — must be zero)")
    if hits:
        for c, b in sorted(hits, reverse=True):
            print(f"   FLAG  {c:3d}x  \"{b}\"")
    else:
        print("   clean — no banned phrases found.")

    print("\n2. STRUCTURAL RISKS")
    risks = 0
    neg = len(re.findall(r"not (just|only)[^.]{0,120}?(it's|it is|but also|—|but)", low))
    if neg > 1:
        print(f"   FLAG  {neg}x negation-parallelism ('not just X — it's Y') — one per document max"); risks += 1
    hedge_piles = len(re.findall(r"\b(may|might|could)\s+(arguably|potentially|possibly)\s+(suggest|indicate)", low))
    if hedge_piles:
        print(f"   FLAG  {hedge_piles}x hedge-pile (may+arguably+suggest) — use a single modal"); risks += 1
    if lens:
        uniform_runs = 0
        run = 1
        for i in range(1, len(lens)):
            if abs(lens[i] - lens[i-1]) <= 3:
                run += 1
                if run == 3: uniform_runs += 1
            else:
                run = 1
        if uniform_runs:
            print(f"   FLAG  {uniform_runs} run(s) of 3+ sentences within 3 words of each other — vary the rhythm"); risks += 1
    openers = [re.match(r"^[\"'\u201c(]*([A-Za-z'-]+)", s) for s in sents]
    subj_first = sum(1 for o in openers if o and o.group(1).lower() in
                     ("the", "this", "these", "that", "a", "an", "it", "they", "we", "he", "she"))
    if sents and subj_first / len(sents) > 0.55:
        print(f"   FLAG  {subj_first/len(sents)*100:.0f}% of sentences open subject-first (The/This/It/We...) — vary openings with Thus/However/For example/clauses"); risks += 1
    bullets_frag = len(re.findall(r"^\s*[-*•]\s+[^.!?]{1,60}$", text, flags=re.M))
    if bullets_frag > 3:
        print(f"   FLAG  {bullets_frag} short bullet fragments — Ben's list items are full sentences, usually with bolded heads"); risks += 1
    if not risks:
        print("   clean — no structural risks found.")

    print("\n3. BEN FINGERPRINT STATS (compare to his baseline)")
    if lens:
        print(f"   sentences: {len(sents)}  words: {len(words)}")
        print(f"   sentence length: avg {statistics.mean(lens):.1f} (his: 26.7)  median {statistics.median(lens)} (his: 25)  stdev {statistics.stdev(lens):.1f} (his: 14.7)")
        over25 = sum(1 for L in lens if L > 25) / len(lens) * 100
        print(f"   sentences over 25 words: {over25:.0f}% (his: ~45%)")
    tw = {t: low.count(t) for t in BEN_WORKHORSES}
    used = {t: c for t, c in tw.items() if c}
    print(f"   his workhorse transitions found: {used if used else 'NONE — consider Thus/However/For example'}")
    print(f"   questions to reader: {sum(1 for s in sents if s.rstrip().endswith('?'))}")
    print(f"   second person 'you': {len(re.findall(chr(92)+'byou'+chr(92)+'b', low))}   'ought': {len(re.findall(chr(92)+'bought'+chr(92)+'b', low))}")
    print(f"   triple-dash asides: {len(re.findall('---', text))}   semicolons: {text.count(';')}   colons: {text.count(':')}")
    print("\nDone. Fix FLAGs, then read aloud — it should sound like a person who thinks for a living.")

if __name__ == "__main__":
    main()
