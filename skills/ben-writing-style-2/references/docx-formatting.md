# Docx Formatting Rules (permanent)

These rules apply to every .docx deliverable produced for Ben, unless he instructs otherwise for a specific document. They are in addition to the voice and anti-AI-tell rules in SKILL.md.

1. 10.5 point font on all body text and all headings except the title.
2. 13.5 point font on the title.
3. Times New Roman on all text.
4. All footnotes in 8 point font.
5. All footnotes as real Word footnotes (native footnotes part), as if made directly in MS Word.
6. Zero space before or after footnotes.
7. All body text fully justified.
8. Header text is a short, accurate summary of the document in a few words (not necessarily the literal title), right justified, 9 point italic, starting on the second page only (different first page header). Example: "Chutes Equity Grant Structure" for the equity grant memo.
9. Page numbers on all pages, centered in the footer, formatted "X of Y" (PAGE of NUMPAGES fields), e.g. page one of ten reads "1 of 10".
10. Overall professionalism equal to an AmLaw 100 law firm work product.

Implementation: the `office-doc-engine` skill's `scripts/docx_builder.py` implements all ten rules. Use `MemoBuilder` for memos and briefs and the rules are applied automatically.
