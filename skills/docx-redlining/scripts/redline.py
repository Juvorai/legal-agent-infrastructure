"""
redline.py -- true Word tracked changes (w:ins / w:del) at WORD level.

A human reviewer redlines the words that change and nothing else. This module
exists so agents do the same: never strike a whole paragraph to change one
word. All edits carry an explicit author name and date, exactly like a human
using Track Changes in Word.

Two ways to use it:

1. Targeted edits (preferred -- the agent knows what it wants to change):

    from redline import Redliner
    r = Redliner("contract.docx", author="Jane Smith")
    r.replace_text(
        "shall be governed by the laws of Delaware",
        "shall be governed by the laws of New York",
    )
    r.save("contract_redline.docx")

   replace_text finds the paragraph(s) containing the old text, diffs old vs
   new at word level, and marks ONLY the differing words as deletions and
   insertions. Unchanged words are left byte-identical.

2. Whole-document diff (agent has an original and a revised copy):

    from redline import redline_documents
    redline_documents("original.docx", "revised.docx",
                      author="Jane Smith", out="redline.docx")

   Paragraphs are aligned by similarity, then each aligned pair is diffed at
   word level. Paragraphs with no counterpart are marked inserted or deleted
   as a whole (that is the correct human behavior for genuinely new or
   removed paragraphs).

Author name is REQUIRED. There is no default. Callers must ask the user in
whose name the redlines should be made before constructing a Redliner.
"""

from __future__ import annotations

import copy
import difflib
import re
from datetime import datetime, timezone
from docx import Document
from docx.oxml.ns import qn
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _make(tag: str, **attrs) -> etree._Element:
    el = etree.Element(qn(tag))
    for k, v in attrs.items():
        el.set(qn(k), v)
    return el


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


_WORD_RE = re.compile(r"\S+|\s+")


def _tokenize(text: str) -> list[str]:
    """Split into words and whitespace, keeping whitespace as tokens so we can
    reassemble the paragraph exactly."""
    return _WORD_RE.findall(text)


def _para_text(p) -> str:
    return "".join(node.text or "" for node in p._p.iter(qn("w:t")))


def _base_rpr(p):
    """Formatting (rPr) to reuse for inserted/deleted runs: take it from the
    first run that has text, so redlined words look like their neighbors."""
    for r in p._p.findall(qn("w:r")):
        if r.find(qn("w:t")) is not None:
            rpr = r.find(qn("w:rPr"))
            if rpr is not None:
                return copy.deepcopy(rpr)
    return None


def _run(text: str, rpr=None) -> etree._Element:
    r = _make("w:r")
    if rpr is not None:
        r.append(copy.deepcopy(rpr))
    t = _make("w:t")
    t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    r.append(t)
    return r


def _del_run(text: str, author: str, date: str, rev_id: int, rpr=None) -> etree._Element:
    """A deleted word: <w:del><w:r><w:delText>word</w:delText></w:r></w:del>."""
    d = _make("w:del", **{"w:id": str(rev_id), "w:author": author, "w:date": date})
    r = _make("w:r")
    if rpr is not None:
        r.append(copy.deepcopy(rpr))
    dt = _make("w:delText")
    dt.text = text
    dt.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    r.append(dt)
    d.append(r)
    return d


def _ins_run(text: str, author: str, date: str, rev_id: int, rpr=None) -> etree._Element:
    """An inserted word: <w:ins><w:r><w:t>word</w:t></w:r></w:ins>."""
    i = _make("w:ins", **{"w:id": str(rev_id), "w:author": author, "w:date": date})
    i.append(_run(text, rpr))
    return i


def _clear_runs(p) -> None:
    """Remove all runs and any existing ins/del wrappers from a paragraph,
    keeping paragraph properties (pPr)."""
    for child in list(p._p):
        if child.tag in (qn("w:r"), qn("w:ins"), qn("w:del"), qn("w:hyperlink")):
            p._p.remove(child)


class _IdGen:
    def __init__(self, start: int = 1000):
        self._n = start

    def next(self) -> int:
        self._n += 1
        return self._n


def redline_paragraph(p, new_text: str, author: str, date: str, ids: _IdGen) -> bool:
    """Diff the paragraph's current text against new_text at WORD level and
    rewrite the paragraph with tracked changes for the differing words only.
    Returns True if any change was marked."""
    old_text = _para_text(p)
    if old_text == new_text:
        return False
    rpr = _base_rpr(p)
    old_toks = _tokenize(old_text)
    new_toks = _tokenize(new_text)
    sm = difflib.SequenceMatcher(a=old_toks, b=new_toks, autojunk=False)
    _clear_runs(p)
    changed = False
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for tok in old_toks[i1:i2]:
                p._p.append(_run(tok, rpr))
        elif tag == "delete":
            changed = True
            for tok in old_toks[i1:i2]:
                p._p.append(_del_run(tok, author, date, ids.next(), rpr))
        elif tag == "insert":
            changed = True
            for tok in new_toks[j1:j2]:
                p._p.append(_ins_run(tok, author, date, ids.next(), rpr))
        elif tag == "replace":
            changed = True
            for tok in old_toks[i1:i2]:
                p._p.append(_del_run(tok, author, date, ids.next(), rpr))
            for tok in new_toks[j1:j2]:
                p._p.append(_ins_run(tok, author, date, ids.next(), rpr))
    return changed


class Redliner:
    """Apply targeted, word-level tracked changes to a .docx file.

    author is mandatory and must come from the user -- never invent one.
    """

    def __init__(self, path: str, author: str, date: str | None = None):
        if not author or not author.strip():
            raise ValueError(
                "author is required. Ask the user in whose name the redlines "
                "should be made before redlining."
            )
        self.author = author.strip()
        self.date = date or _now_iso()
        self.doc = Document(path)
        self.ids = _IdGen()

    def replace_text(self, old: str, new: str, occurrence: int = 1) -> int:
        """Find the paragraph containing `old`, substitute `new`, and redline
        only the words that differ. Returns the number of paragraphs changed.
        Raises if `old` is not found."""
        hits = 0
        for p in self.doc.paragraphs:
            text = _para_text(p)
            if old in text:
                hits += 1
                if hits == occurrence:
                    redline_paragraph(p, text.replace(old, new, 1),
                                      self.author, self.date, self.ids)
                    return 1
        raise ValueError(f"Text not found in document: {old[:80]!r}")

    def redline_paragraph_at(self, index: int, new_text: str) -> bool:
        """Redline the paragraph at `index` against new_text, word-level."""
        return redline_paragraph(self.doc.paragraphs[index], new_text,
                                 self.author, self.date, self.ids)

    def save(self, out: str) -> str:
        self.doc.save(out)
        return out


def _similarity(a: str, b: str) -> float:
    if not a and not b:
        return 1.0
    return difflib.SequenceMatcher(a=a, b=b, autojunk=False).ratio()


def redline_documents(original: str, revised: str, author: str, out: str,
                      date: str | None = None,
                      align_threshold: float = 0.55) -> str:
    """Build a redline from an original and a revised document.

    Paragraphs are aligned greedily by similarity. Aligned pairs are diffed
    at word level. Unmatched revised paragraphs are inserted wholesale;
    unmatched original paragraphs are deleted wholesale. Output is written to
    `out` based on the ORIGINAL file (so all original formatting survives).
    """
    if not author or not author.strip():
        raise ValueError(
            "author is required. Ask the user in whose name the redlines "
            "should be made before redlining."
        )
    author = author.strip()
    date = date or _now_iso()
    ids = _IdGen()

    doc = Document(original)
    rev = Document(revised)
    orig_paras = doc.paragraphs
    rev_texts = [_para_text(p) for p in rev.paragraphs]
    orig_texts = [_para_text(p) for p in orig_paras]

    # Greedy alignment: for each original paragraph, best matching revised index.
    used_rev: set[int] = set()
    pairs: list[tuple[int, int | None]] = []
    for oi, ot in enumerate(orig_texts):
        best_j, best_s = None, 0.0
        for j, rt in enumerate(rev_texts):
            if j in used_rev:
                continue
            s = _similarity(ot, rt)
            if s > best_s:
                best_s, best_j = s, j
        if best_j is not None and best_s >= align_threshold:
            used_rev.add(best_j)
            pairs.append((oi, best_j))
        else:
            pairs.append((oi, None))

    # Apply word-level diffs for aligned pairs; delete unmatched originals.
    for oi, rj in pairs:
        p = orig_paras[oi]
        if rj is None:
            if orig_texts[oi].strip():
                rpr = _base_rpr(p)
                _clear_runs(p)
                for tok in _tokenize(orig_texts[oi]):
                    p._p.append(_del_run(tok, author, date, ids.next(), rpr))
        else:
            redline_paragraph(p, rev_texts[rj], author, date, ids)

    # Insert revised paragraphs that had no original counterpart, after the
    # paragraph they followed in the revised document.
    # Anchor: the original paragraph aligned to the previous used revised para.
    rev_to_orig = {rj: oi for oi, rj in pairs if rj is not None}
    for j, rt in enumerate(rev_texts):
        if j in used_rev or not rt.strip():
            continue
        # find nearest preceding aligned revised paragraph
        anchor_oi = None
        for k in range(j - 1, -1, -1):
            if k in rev_to_orig:
                anchor_oi = rev_to_orig[k]
                break
        new_p = _make("w:p")
        rpr = None
        for tok in _tokenize(rt):
            new_p.append(_ins_run(tok, author, date, ids.next(), rpr))
        if anchor_oi is not None:
            orig_paras[anchor_oi]._p.addnext(new_p)
        else:
            doc.paragraphs[0]._p.addprevious(new_p)

    doc.save(out)
    return out
