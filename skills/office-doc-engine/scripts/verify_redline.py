#!/usr/bin/env python3
"""
verify_redline.py - Verify tracked changes in a redlined .docx document.
Confirms every ORIGINAL text appears as w:delText and every PROPOSED text appears as w:ins.

Usage:
    python3 verify_redline.py <docx_file> <originals_json> <proposed_json>
    
    originals_json: JSON array of original text strings that should appear as deletions
    proposed_json: JSON array of proposed text strings that should appear as insertions

Or programmatically:
    from verify_redline import verify_redline
    results = verify_redline(docx_path, originals_list, proposed_list)
"""

import sys
import json
import zipfile
from lxml import etree


WORD_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def extract_del_texts(docx_path):
    """Extract all w:delText content from a .docx file."""
    del_texts = []
    
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = etree.parse(f)
    
    root = tree.getroot()
    nsmap = {'w': WORD_NS}
    
    # Find all w:del elements
    del_elements = root.findall('.//' + f'{{{WORD_NS}}}del')
    
    for del_elem in del_elements:
        # Get all delText within this deletion
        del_text_elems = del_elem.findall('.//' + f'{{{WORD_NS}}}delText')
        text = ''.join(elem.text or '' for elem in del_text_elems)
        if text.strip():
            del_texts.append(text)
    
    return del_texts


def extract_ins_texts(docx_path):
    """Extract all w:ins content from a .docx file."""
    ins_texts = []
    
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = etree.parse(f)
    
    root = tree.getroot()
    
    # Find all w:ins elements
    ins_elements = root.findall('.//' + f'{{{WORD_NS}}}ins')
    
    for ins_elem in ins_elements:
        # Get all text within this insertion
        text_elems = ins_elem.findall('.//' + f'{{{WORD_NS}}}t')
        text = ''.join(elem.text or '' for elem in text_elems)
        if text.strip():
            ins_texts.append(text)
    
    return ins_texts


def extract_comments(docx_path):
    """Extract all comments from a .docx file."""
    comments = []
    
    with zipfile.ZipFile(docx_path, 'r') as z:
        if 'word/comments.xml' not in z.namelist():
            return comments
        with z.open('word/comments.xml') as f:
            tree = etree.parse(f)
    
    root = tree.getroot()
    
    comment_elements = root.findall('.//' + f'{{{WORD_NS}}}comment')
    
    for comment_elem in comment_elements:
        author = comment_elem.get(f'{{{WORD_NS}}}author', 'Unknown')
        text_elems = comment_elem.findall('.//' + f'{{{WORD_NS}}}t')
        text = ''.join(elem.text or '' for elem in text_elems)
        comments.append({"author": author, "text": text})
    
    return comments


def verify_redline(docx_path, originals, proposed):
    """
    Verify that a redlined document contains expected tracked changes.
    
    Args:
        docx_path: Path to the .docx file.
        originals: List of original text strings (should be in w:delText).
        proposed: List of proposed text strings (should be in w:ins).
    
    Returns:
        Dict with verification results.
    """
    del_texts = extract_del_texts(docx_path)
    ins_texts = extract_ins_texts(docx_path)
    comments = extract_comments(docx_path)
    
    # Join all del/ins text for substring matching
    all_del_text = ' '.join(del_texts)
    all_ins_text = ' '.join(ins_texts)
    
    results = {
        "originals_found": [],
        "originals_missing": [],
        "proposed_found": [],
        "proposed_missing": [],
        "comments_count": len(comments),
        "del_count": len(del_texts),
        "ins_count": len(ins_texts),
        "pass": True,
    }
    
    # Check originals appear as deletions
    for orig in originals:
        # Normalize whitespace for comparison
        orig_normalized = ' '.join(orig.split())
        found = False
        for dt in del_texts:
            dt_normalized = ' '.join(dt.split())
            if orig_normalized in dt_normalized or dt_normalized in orig_normalized:
                found = True
                break
        if found:
            results["originals_found"].append(orig[:80])
        else:
            results["originals_missing"].append(orig[:80])
            results["pass"] = False
    
    # Check proposed appear as insertions
    for prop in proposed:
        prop_normalized = ' '.join(prop.split())
        found = False
        for it in ins_texts:
            it_normalized = ' '.join(it.split())
            if prop_normalized in it_normalized or it_normalized in prop_normalized:
                found = True
                break
        if found:
            results["proposed_found"].append(prop[:80])
        else:
            results["proposed_missing"].append(prop[:80])
            results["pass"] = False
    
    return results


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 verify_redline.py <docx_file> <originals_json> <proposed_json>")
        print("  originals_json: JSON array of original text strings")
        print("  proposed_json: JSON array of proposed text strings")
        sys.exit(1)
    
    docx_path = sys.argv[1]
    
    with open(sys.argv[2], 'r') as f:
        originals = json.load(f)
    
    with open(sys.argv[3], 'r') as f:
        proposed = json.load(f)
    
    results = verify_redline(docx_path, originals, proposed)
    
    print(json.dumps(results, indent=2))
    
    if not results["pass"]:
        print("\nVERIFICATION FAILED")
        if results["originals_missing"]:
            print(f"  Missing deletions: {len(results['originals_missing'])}")
        if results["proposed_missing"]:
            print(f"  Missing insertions: {len(results['proposed_missing'])}")
        sys.exit(1)
    else:
        print("\nVERIFICATION PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
