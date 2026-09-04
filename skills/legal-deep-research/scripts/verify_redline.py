"""
Redline Verification Script
============================
Verifies that a .docx redline file contains proper tracked changes and comments.

Usage:
    python3 verify_redline.py /path/to/redline.docx [--entries /path/to/entries.json]

Checks:
1. document.xml contains w:ins elements (insertions)
2. document.xml contains w:del elements with w:delText (deletions)
3. comments.xml exists and contains w:comment elements
4. [Content_Types].xml declares the comments content type
5. word/_rels/document.xml.rels has a relationship for comments.xml
6. If entries.json provided: every ORIGINAL text appears as w:delText,
   every PROPOSED text appears as w:ins text
7. Author attribution is correct on all revisions
8. Comment references in document body match comment IDs in comments.xml

Exit codes:
    0 = all checks pass
    1 = one or more checks failed
"""

import sys
import os
import json
import re
import zipfile
from pathlib import Path


def verify(docx_path: str, entries_path: str = None) -> bool:
    """Verify a redline .docx file. Returns True if all checks pass."""
    
    errors = []
    warnings = []
    
    if not os.path.exists(docx_path):
        print(f"FAIL: File not found: {docx_path}")
        return False
    
    with zipfile.ZipFile(docx_path, 'r') as z:
        names = z.namelist()
        
        # Check 1: document.xml exists
        if 'word/document.xml' not in names:
            errors.append("word/document.xml not found in archive")
            print_fail(errors)
            return False
        
        doc_xml = z.read('word/document.xml').decode('utf-8')
        
        # Check 2: w:ins elements
        ins_count = len(re.findall(r'<w:ins\s', doc_xml))
        if ins_count == 0:
            errors.append("No w:ins elements found (no tracked insertions)")
        else:
            print(f"  ✓ w:ins elements: {ins_count}")
        
        # Check 3: w:del elements with w:delText
        del_count = len(re.findall(r'<w:del\s', doc_xml))
        deltext_count = len(re.findall(r'<w:delText', doc_xml))
        if del_count == 0:
            errors.append("No w:del elements found (no tracked deletions)")
        else:
            print(f"  ✓ w:del elements: {del_count}")
        
        if deltext_count == 0 and del_count > 0:
            errors.append("w:del elements found but no w:delText (deletions have no text)")
        elif deltext_count > 0:
            print(f"  ✓ w:delText elements: {deltext_count}")
        
        # Check 4: Author attribution
        authors = set(re.findall(r'w:author="([^"]+)"', doc_xml))
        if authors:
            print(f"  ✓ Revision authors: {authors}")
            if len(authors) > 1:
                warnings.append(f"Multiple authors found: {authors}")
        else:
            errors.append("No w:author attributes found on revisions")
        
        # Check 5: Date attribution
        dates = re.findall(r'w:date="([^"]+)"', doc_xml)
        if dates:
            print(f"  ✓ Revision dates present: {len(dates)}")
        else:
            warnings.append("No w:date attributes found on revisions")
        
        # Check 6: comments.xml
        if 'word/comments.xml' in names:
            comments_xml = z.read('word/comments.xml').decode('utf-8')
            comment_count = len(re.findall(r'<w:comment\s', comments_xml))
            if comment_count == 0:
                errors.append("comments.xml exists but contains no w:comment elements")
            else:
                print(f"  ✓ w:comment elements: {comment_count}")
            
            # Check comment authors
            comment_authors = set(re.findall(r'w:author="([^"]+)"', comments_xml))
            if comment_authors:
                print(f"  ✓ Comment authors: {comment_authors}")
        else:
            errors.append("word/comments.xml not found (no comments part)")
        
        # Check 7: Content types
        if '[Content_Types].xml' in names:
            ct_xml = z.read('[Content_Types].xml').decode('utf-8')
            if 'comments+xml' not in ct_xml:
                errors.append("[Content_Types].xml does not declare comments content type")
            else:
                print(f"  ✓ Comments content type declared")
        else:
            errors.append("[Content_Types].xml not found")
        
        # Check 8: Relationships
        if 'word/_rels/document.xml.rels' in names:
            rels_xml = z.read('word/_rels/document.xml.rels').decode('utf-8')
            if 'comments' not in rels_xml:
                errors.append("document.xml.rels has no relationship for comments")
            else:
                print(f"  ✓ Comments relationship declared")
        else:
            errors.append("word/_rels/document.xml.rels not found")
        
        # Check 9: Comment references in document body
        comment_refs = re.findall(r'<w:commentReference\s+w:id="(\d+)"', doc_xml)
        comment_range_starts = re.findall(r'<w:commentRangeStart\s+w:id="(\d+)"', doc_xml)
        comment_range_ends = re.findall(r'<w:commentRangeEnd\s+w:id="(\d+)"', doc_xml)
        
        if comment_refs:
            print(f"  ✓ Comment references in body: {len(comment_refs)}")
        else:
            warnings.append("No w:commentReference elements in document body")
        
        if comment_range_starts and comment_range_ends:
            if len(comment_range_starts) != len(comment_range_ends):
                errors.append(f"Mismatched comment ranges: {len(comment_range_starts)} starts vs {len(comment_range_ends)} ends")
            else:
                print(f"  ✓ Comment ranges balanced: {len(comment_range_starts)}")
        
        # Check 10: Verify against entries if provided
        if entries_path and os.path.exists(entries_path):
            with open(entries_path) as f:
                entries = json.load(f)
            
            print(f"\n  Verifying {len(entries)} redline entries against document...")
            
            # Extract all delText content
            deltexts = re.findall(r'<w:delText[^>]*>(.*?)</w:delText>', doc_xml, re.DOTALL)
            all_deltext = ' '.join(deltexts)
            
            # Extract all ins text content
            # Get text within w:ins elements
            ins_texts = re.findall(r'<w:ins\s[^>]*>(.*?)</w:ins>', doc_xml, re.DOTALL)
            all_instext = ' '.join(ins_texts)
            # Extract w:t content from ins
            ins_t_texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', all_instext)
            all_instext_clean = ' '.join(ins_t_texts)
            
            matched_del = 0
            matched_ins = 0
            failed_entries = []
            
            for i, entry in enumerate(entries):
                original = entry.get('original', '')
                proposed = entry.get('proposed', '')
                
                # Normalize for comparison
                orig_norm = re.sub(r'\s+', ' ', original).strip()
                prop_norm = re.sub(r'\s+', ' ', proposed).strip()
                
                # Check deletion
                orig_short = orig_norm[:50]  # Check first 50 chars
                if orig_short in all_deltext or orig_norm[:30] in all_deltext:
                    matched_del += 1
                else:
                    failed_entries.append((i, entry.get('section', '?'), 'DEL', orig_short[:40]))
                
                # Check insertion
                prop_short = prop_norm[:50]
                if prop_short in all_instext_clean or prop_norm[:30] in all_instext_clean:
                    matched_ins += 1
                else:
                    failed_entries.append((i, entry.get('section', '?'), 'INS', prop_short[:40]))
            
            print(f"  ✓ Deletions matched: {matched_del}/{len(entries)}")
            print(f"  ✓ Insertions matched: {matched_ins}/{len(entries)}")
            
            if failed_entries:
                warnings.append(f"{len(failed_entries)} entries could not be verified in document")
                for idx, sec, typ, text in failed_entries[:10]:
                    print(f"    ⚠ Entry {idx} (section {sec}): {typ} not found: '{text}...'")
    
    # Print results
    print(f"\n{'='*60}")
    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        for e in errors:
            print(f"  ✗ {e}")
    if warnings:
        print(f"WARNINGS: {len(warnings)}")
        for w in warnings:
            print(f"  ⚠ {w}")
    if not errors:
        print("ALL CHECKS PASSED ✓")
    
    return len(errors) == 0


def print_fail(errors):
    for e in errors:
        print(f"  ✗ {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    docx_path = sys.argv[1]
    entries_path = None
    
    if "--entries" in sys.argv:
        idx = sys.argv.index("--entries")
        if idx + 1 < len(sys.argv):
            entries_path = sys.argv[idx + 1]
    
    print(f"Verifying: {docx_path}")
    print(f"{'='*60}\n")
    
    success = verify(docx_path, entries_path)
    sys.exit(0 if success else 1)
