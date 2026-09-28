---
name: office-doc-engine
description: "Create and edit Microsoft Office deliverables (.docx, .xlsx, .pptx) and PDFs with full formatting control. Use whenever the user asks for a Word document, memo, brief, contract, spreadsheet, workbook, slide deck, presentation, or PDF output. Word documents support real footnotes (required for legal citations unless the user asks otherwise), styles, headers/footers, tables, and section formatting. Always export the finished file with export_to_user."
icon: file-text
color: Green
---

# Office Document Engine

Produce professional Office files and PDFs from the sandbox. All generation goes through the scripts here; never hand-assemble OOXML.

## Libraries (pre-installed)

- Word: `python-docx`
- Excel: `openpyxl`
- PowerPoint: `python-pptx`
- PDF: `reportlab` (generation), `weasyprint` (HTML to PDF), `pypdf` / `PyMuPDF` (read/merge/inspect)

## Word (.docx)

Use `scripts/docx_builder.py`. It wraps python-docx and adds the one thing python-docx lacks natively: **real Word footnotes** (the kind that render at the bottom of the page and renumber automatically), implemented by injecting the footnotes part into the document package.

### Citation policy for legal documents

Citations in legal memos and briefs go in **real footnotes**, not inline bracket cites, unless the user asks otherwise. Pass citations as footnote text; the builder places the reference mark and the footnote body.

### Quick start

```python
import sys
sys.path.insert(0, "/home/user/skills/office-doc-engine/scripts")
from docx_builder import MemoBuilder

doc = MemoBuilder(title="Memorandum", author="Chutes_Legal_AI")
doc.heading("Issue", level=1)
doc.paragraph("Whether the token constitutes an investment contract.")
doc.heading("Bottom line", level=1)
doc.paragraph_with_footnote(
    "Likely yes under the Howey test.",
    footnote="SEC v. W.J. Howey Co., 328 U.S. 293 (1946).",
)
doc.heading("Analysis", level=1)
doc.paragraph("...")
doc.save("/home/user/memo.docx")
```

Capabilities: headings (levels 1-4), body paragraphs, bold/italic runs, footnotes, tables, numbered and bulleted lists, page numbers in footer, custom margins, block quotes, horizontal rules. For anything beyond the builder's API, drop to python-docx directly; the builder exposes `.document`.

### Formatting controls

- Styles: modify `doc.document.styles` for fonts (default body: 12pt serif), spacing, heading look.
- Sections: `doc.document.sections[0]` for margins, page size, orientation, headers/footers.
- Tables: `doc.table(rows, cols, header=[...])` then fill cells.

## Excel (.xlsx)

Use `openpyxl` directly, following the `spreadsheet-output` skill for viewer-friendly formatting. Standard pattern:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active
ws.append(["Column A", "Column B"])
for cell in ws[1]:
    cell.font = Font(bold=True)
ws.freeze_panes = "A2"
wb.save("/home/user/output.xlsx")
```

Number formats, column widths, conditional formatting, and formulas are all supported via openpyxl. Keep one header row, no merged cells in data regions, ISO dates.

## PowerPoint (.pptx)

Use `python-pptx` directly:

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Title"
slide.placeholders[1].text = "Body"
prs.save("/home/user/deck.pptx")
```

Use layouts from the default template, set fonts explicitly, and keep text short. For board decks, follow the voice rules in `ben-writing-style-2`.

## PDF

- Generate: `reportlab` for programmatic PDFs, or write HTML and convert with `weasyprint` for styled documents.
- Read/extract: `PyMuPDF` (`fitz`) for text extraction from uploaded PDFs; `pypdf` for merge/split/rotate.

## Reading uploaded Office files

- .docx: `python-docx` (paragraphs, tables) or `markitdown` for quick text.
- .xlsx: `openpyxl` or `pandas.read_excel`.
- .pptx: `python-pptx` or `markitdown`.
- .pdf: `PyMuPDF`.

## Redlining / tracked changes

For any request to redline, mark up, or show edits in a .docx, use the `docx-redlining` skill (`scripts/redline.py`): real Word tracked changes at word level, never whole-paragraph strikes for small edits, and always ask the user in whose name the redlines should be made before editing.

## Delivery

Always `export_to_user` the finished file. Keep the same filename on revisions so versions chain.

## Scripts

- `scripts/docx_builder.py`: MemoBuilder class with real footnote support and legal memo conveniences.
