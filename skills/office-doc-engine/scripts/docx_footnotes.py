#!/usr/bin/env python3
"""
docx_footnotes.py - Real Word footnote implementation for python-docx.
Creates native footnotes part in .docx files.
"""

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from copy import deepcopy
import re


class FootnoteManager:
    """Manages real Word footnotes for a document."""
    
    def __init__(self, doc):
        self.doc = doc
        self.footnotes = []
        self._footnote_id_counter = 1
        self._ensure_footnotes_part()
    
    def _ensure_footnotes_part(self):
        """Ensure the document has a footnotes part."""
        # Check if footnotes part exists
        package = self.doc.part.package
        footnotes_part = None
        
        for rel in self.doc.part.rels.values():
            if "footnotes" in rel.reltype:
                footnotes_part = rel.target_part
                break
        
        if footnotes_part is None:
            # Create footnotes part
            from docx.opc.part import Part
            from docx.opc.constants import RELATIONSHIP_TYPE as RT
            
            footnotes_xml = (
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:footnotes xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
                'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
                'xmlns:o="urn:schemas-microsoft-com:office:office" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
                'xmlns:v="urn:schemas-microsoft-com:vml" '
                'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
                'xmlns:w10="urn:schemas-microsoft-com:office:word" '
                'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
                'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
                'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
                'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
                'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">'
                '<w:footnote w:type="separator" w:id="-1">'
                '<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
                '<w:r><w:separator/></w:r></w:p></w:footnote>'
                '<w:footnote w:type="continuationSeparator" w:id="0">'
                '<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
                '<w:r><w:continuationSeparator/></w:r></w:p></w:footnote>'
                '</w:footnotes>'
            )
            
            from docx.opc.part import Part
            from lxml import etree
            
            footnotes_element = etree.fromstring(footnotes_xml.encode('utf-8'))
            
            partname = '/word/footnotes.xml'
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml'
            
            footnotes_part = Part(
                partname, content_type, footnotes_xml.encode('utf-8'), package
            )
            
            self.doc.part.relate_to(
                footnotes_part,
                'http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes'
            )
        
        self._footnotes_part = footnotes_part
    
    def add_footnote(self, paragraph, text):
        """
        Add a footnote reference to a paragraph and create the footnote content.
        
        Args:
            paragraph: The paragraph to add the footnote reference to.
            text: The footnote text.
        
        Returns:
            The footnote ID.
        """
        footnote_id = self._footnote_id_counter
        self._footnote_id_counter += 1
        
        # Add footnote reference run to paragraph
        run = paragraph.add_run()
        run.font.size = Pt(10.5)
        run.font.name = 'Times New Roman'
        
        # Create footnoteReference element
        footnote_ref = OxmlElement('w:footnoteReference')
        footnote_ref.set(qn('w:id'), str(footnote_id))
        run._r.append(footnote_ref)
        
        # Add footnote content to footnotes part
        self._add_footnote_content(footnote_id, text)
        
        self.footnotes.append({"id": footnote_id, "text": text})
        return footnote_id
    
    def _add_footnote_content(self, footnote_id, text):
        """Add footnote content to the footnotes XML part."""
        from lxml import etree
        
        # Parse existing footnotes
        footnotes_element = etree.fromstring(self._footnotes_part.blob)
        
        # Create footnote element
        nsmap = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        
        footnote = etree.SubElement(footnotes_element, qn('w:footnote'))
        footnote.set(qn('w:id'), str(footnote_id))
        
        # Create paragraph
        p = etree.SubElement(footnote, qn('w:p'))
        
        # Paragraph properties (8pt, no space)
        pPr = etree.SubElement(p, qn('w:pPr'))
        spacing = etree.SubElement(pPr, qn('w:spacing'))
        spacing.set(qn('w:before'), '0')
        spacing.set(qn('w:after'), '0')
        
        # Footnote reference mark run
        r1 = etree.SubElement(p, qn('w:r'))
        rPr1 = etree.SubElement(r1, qn('w:rPr'))
        rStyle = etree.SubElement(rPr1, qn('w:rStyle'))
        rStyle.set(qn('w:val'), 'FootnoteReference')
        footnoteRef = etree.SubElement(r1, qn('w:footnoteRef'))
        
        # Space after reference mark
        r2 = etree.SubElement(p, qn('w:r'))
        t2 = etree.SubElement(r2, qn('w:t'))
        t2.set(qn('xml:space'), 'preserve')
        t2.text = ' '
        
        # Footnote text run
        r3 = etree.SubElement(p, qn('w:r'))
        rPr3 = etree.SubElement(r3, qn('w:rPr'))
        sz = etree.SubElement(rPr3, qn('w:sz'))
        sz.set(qn('w:val'), '16')  # 8pt = 16 half-points
        szCs = etree.SubElement(rPr3, qn('w:szCs'))
        szCs.set(qn('w:val'), '16')
        t3 = etree.SubElement(r3, qn('w:t'))
        t3.set(qn('xml:space'), 'preserve')
        t3.text = text
        
        # Update the part blob
        self._footnotes_part._blob = etree.tostring(
            footnotes_element, xml_declaration=True, encoding='UTF-8', standalone=True
        )


def add_footnote_to_paragraph(paragraph, text):
    """
    Convenience function: add a real Word footnote to a paragraph.
    Creates a FootnoteManager if one doesn't exist on the document.
    """
    doc = paragraph.part.document if hasattr(paragraph.part, 'document') else None
    if doc is None:
        # Try to get document from the paragraph's parent
        raise ValueError("Cannot determine document from paragraph")
    
    if not hasattr(doc, '_footnote_manager'):
        doc._footnote_manager = FootnoteManager(doc)
    
    return doc._footnote_manager.add_footnote(paragraph, text)
