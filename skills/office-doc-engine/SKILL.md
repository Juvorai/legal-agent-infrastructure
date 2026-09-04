# office-doc-engine

Create and edit Microsoft Office deliverables (.docx, .xlsx, .pptx) and PDFs with full formatting control. Use whenever the user asks for a Word document, memo, brief, contract, spreadsheet, workbook, slide deck, presentation, or PDF output. Word documents support real footnotes (required for legal citations unless the user asks otherwise), styles, headers/footers, tables, and section formatting. Always export the finished file with export_to_user.

## Docx Formatting Rules (permanent, all .docx output unless the user says otherwise)

1. 10.5 point font on all body text and all headings except the title.
2. 13.5 point font on the title.
3. Times New Roman on all text.
4. All text in black color (Automatic).
5. All footnotes in 8 point font.
6. All footnotes as real Word footnotes (native footnotes part), as if made directly in MS Word.
7. Zero space before or after footnotes.
8. All body text fully justified.
9. Header text is a short, accurate summary of the document in a few words (not necessarily the literal title), right justified, 8 point italic, starting on the second page only (different first page header).
10. Page numbers on all pages, centered in the footer, formatted "X of Y" (PAGE of NUMPAGES fields), e.g. page one of ten reads "1 of 10", at 8 point font.
11. Summary metadata: Author set to the configured author (see COMPANY CONFIGURATION in AGENT.md) and nothing else. No reference to "python" or any tooling anywhere in the metadata.
12. Contracts: each signature page and each exhibit, schedule, or appendix begins on its own page (use page_break()).
13. Writing: no hyphens or em dashes except grammatically correct word hyphenation. One space after each sentence.
14. Overall professionalism equal to an AmLaw 100 law firm work product.

## Implementation with python-docx

### Document Setup

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import datetime

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(10.5)
font.color.rgb = RGBColor(0, 0, 0)

# Set paragraph formatting
pf = style.paragraph_format
pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
pf.space_before = Pt(0)
pf.space_after = Pt(6)
```

### Title

```python
title_para = doc.add_paragraph()
title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title_para.add_run("Document Title")
title_run.font.size = Pt(13.5)
title_run.font.name = 'Times New Roman'
title_run.font.bold = True
title_run.font.color.rgb = RGBColor(0, 0, 0)
```

### Headings

```python
def add_heading(doc, text, level=1):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.font.size = Pt(10.5)
    run.font.name = 'Times New Roman'
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    para.paragraph_format.space_before = Pt(12)
    para.paragraph_format.space_after = Pt(6)
    return para
```

### Real Footnotes

```python
def add_footnote(paragraph, footnote_text):
    """Add a real Word footnote to a paragraph."""
    from docx.oxml import OxmlElement
    
    # Create footnote reference in the paragraph
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:footnoteReference')
    
    # Get or create footnotes part
    # This requires direct OOXML manipulation
    # See scripts/docx_footnotes.py for the full implementation
    pass
```

For real footnotes, use `scripts/docx_footnotes.py` which handles the full OOXML footnotes part creation.

### Headers and Footers

```python
def setup_header_footer(doc, header_text):
    """Set up header (page 2+) and footer (all pages) with X of Y numbering."""
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    
    # Header (second page onward)
    header = section.header
    header_para = header.paragraphs[0]
    header_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    header_run = header_para.add_run(header_text)
    header_run.font.size = Pt(8)
    header_run.font.italic = True
    header_run.font.name = 'Times New Roman'
    
    # Footer with page X of Y
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add PAGE field
    run = footer_para.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run._r.append(fldChar1)
    
    run2 = footer_para.add_run()
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' PAGE '
    run2._r.append(instrText)
    
    run3 = footer_para.add_run()
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run3._r.append(fldChar2)
    
    # " of "
    footer_para.add_run(" of ")
    
    # Add NUMPAGES field
    run4 = footer_para.add_run()
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'begin')
    run4._r.append(fldChar3)
    
    run5 = footer_para.add_run()
    instrText2 = OxmlElement('w:instrText')
    instrText2.set(qn('xml:space'), 'preserve')
    instrText2.text = ' NUMPAGES '
    run5._r.append(instrText2)
    
    run6 = footer_para.add_run()
    fldChar4 = OxmlElement('w:fldChar')
    fldChar4.set(qn('w:fldCharType'), 'end')
    run6._r.append(fldChar4)
    
    # Set footer font
    for run in footer_para.runs:
        run.font.size = Pt(8)
        run.font.name = 'Times New Roman'
```

### Metadata

```python
def set_metadata(doc, author):
    """Set document metadata with author only."""
    core_props = doc.core_properties
    core_props.author = author
    core_props.title = ""
    core_props.subject = ""
    core_props.keywords = ""
    core_props.comments = ""
    core_props.last_modified_by = author
```

### Tracked Changes (Redlining)

For tracked changes, use OOXML revision markup directly. See the redlining rules in AGENT.md and `scripts/verify_redline.py` for verification.

Key elements:
- `w:ins` for insertions (with `w:author` and `w:date` attributes)
- `w:del` containing `w:delText` for deletions
- `w:comment` in `word/comments.xml` for annotations
- `w:commentReference` and `w:commentRangeStart`/`w:commentRangeEnd` in document body

## Scripts

- `scripts/docx_footnotes.py` - Real Word footnote implementation
- `scripts/verify_redline.py` - Verify tracked changes in redlined documents
