#!/usr/bin/env python3
"""
clause_extractor.py - Extract specific clause types from contract text.
Used with EDGAR EX-10 filings to build the clause library.
"""

import re
from typing import List, Dict, Optional


# Clause detection patterns
CLAUSE_PATTERNS = {
    "limitation_of_liability": {
        "section_headers": [
            r"(?:LIMITATION\s+OF\s+LIABILITY|LIMITATION\s+ON\s+LIABILITY|LIABILITY\s+LIMITATIONS|EXCLUSION\s+OF\s+LIABILITY|EXCLUSIONS\s+AND\s+LIMITATIONS)",
        ],
        "content_indicators": [
            r"shall\s+not\s+exceed",
            r"aggregate\s+liability",
            r"total\s+liability",
            r"maximum\s+liability",
            r"cap\s+on\s+liability",
            r"liability\s+cap",
            r"in\s+no\s+event\s+shall",
            r"not\s+be\s+liable\s+for",
            r"exclusion\s+of\s+(?:consequential|indirect|incidental|special)\s+damages",
        ],
    },
    "indemnification": {
        "section_headers": [
            r"(?:INDEMNIFICATION|INDEMNITY|MUTUAL\s+INDEMNIFICATION|HOLD\s+HARMLESS)",
        ],
        "content_indicators": [
            r"shall\s+indemnify",
            r"agree[s]?\s+to\s+indemnify",
            r"hold\s+harmless",
            r"defend\s+(?:and|,)\s+indemnify",
            r"indemnification\s+obligations",
            r"indemnified\s+party",
            r"indemnifying\s+party",
        ],
    },
    "ip_assignment": {
        "section_headers": [
            r"(?:INTELLECTUAL\s+PROPERTY|IP\s+ASSIGNMENT|ASSIGNMENT\s+OF\s+INVENTIONS|WORK\s+PRODUCT|OWNERSHIP\s+OF\s+INTELLECTUAL\s+PROPERTY)",
        ],
        "content_indicators": [
            r"assign[s]?\s+(?:to|all\s+right)",
            r"intellectual\s+property\s+(?:rights|shall)",
            r"work\s+product",
            r"inventions\s+(?:shall|created|developed)",
            r"proprietary\s+rights",
            r"ownership\s+of\s+(?:all|any)\s+(?:intellectual\s+property|inventions|works)",
        ],
    },
    "data_protection": {
        "section_headers": [
            r"(?:DATA\s+PROTECTION|DATA\s+PRIVACY|DATA\s+PROCESSING|PRIVACY|PERSONAL\s+DATA|GDPR|CCPA)",
        ],
        "content_indicators": [
            r"personal\s+data",
            r"data\s+protection\s+laws?",
            r"data\s+processing\s+agreement",
            r"GDPR",
            r"CCPA",
            r"California\s+Consumer\s+Privacy",
            r"data\s+subject",
            r"data\s+controller",
            r"data\s+processor",
            r"appropriate\s+(?:technical|organizational)\s+measures",
        ],
    },
    "termination": {
        "section_headers": [
            r"(?:TERMINATION|TERM\s+AND\s+TERMINATION|TERMINATION\s+FOR\s+CAUSE|TERMINATION\s+FOR\s+CONVENIENCE|EFFECTS?\s+OF\s+TERMINATION)",
        ],
        "content_indicators": [
            r"terminate\s+(?:this\s+)?(?:agreement|contract)",
            r"termination\s+for\s+(?:cause|convenience|material\s+breach)",
            r"upon\s+termination",
            r"effect\s+of\s+termination",
            r"survival\s+(?:of|shall\s+survive)",
            r"notice\s+of\s+termination",
            r"cure\s+period",
        ],
    },
    "governing_law": {
        "section_headers": [
            r"(?:GOVERNING\s+LAW|GOVERNING\s+LAW\s+AND\s+JURISDICTION|CHOICE\s+OF\s+LAW|APPLICABLE\s+LAW|JURISDICTION\s+AND\s+VENUE)",
        ],
        "content_indicators": [
            r"governed\s+by",
            r"construed\s+in\s+accordance\s+with",
            r"laws\s+of\s+the\s+(?:State|Commonwealth)",
            r"exclusive\s+jurisdiction",
            r"venue\s+(?:shall|lies)",
            r"submit[s]?\s+to\s+the\s+jurisdiction",
        ],
    },
    "confidentiality": {
        "section_headers": [
            r"(?:CONFIDENTIALITY|CONFIDENTIAL\s+INFORMATION|NON-DISCLOSURE|PROTECTION\s+OF\s+CONFIDENTIAL\s+INFORMATION)",
        ],
        "content_indicators": [
            r"confidential\s+information",
            r"shall\s+(?:not|keep)\s+(?:disclose|confidential)",
            r"non-disclosure",
            r"proprietary\s+information",
            r"trade\s+secrets?",
            r"receiving\s+party",
            r"disclosing\s+party",
        ],
    },
    "warranty_disclaimer": {
        "section_headers": [
            r"(?:DISCLAIMER\s+OF\s+WARRANTIES|WARRANTY\s+DISCLAIMER|NO\s+WARRANTIES|DISCLAIMER)",
        ],
        "content_indicators": [
            r"AS\s+IS",
            r"AS\s+AVAILABLE",
            r"disclaims?\s+all\s+warranties",
            r"without\s+warranty",
            r"express\s+or\s+implied",
            r"merchantability",
            r"fitness\s+for\s+a\s+particular\s+purpose",
        ],
    },
}


def extract_clauses(text: str, clause_type: str, context_chars: int = 2000) -> List[str]:
    """
    Extract clauses of a specific type from contract text.
    
    Args:
        text: Full contract text.
        clause_type: One of the keys in CLAUSE_PATTERNS.
        context_chars: Number of characters to include around each match.
    
    Returns:
        List of extracted clause text snippets.
    """
    if clause_type not in CLAUSE_PATTERNS:
        raise ValueError(f"Unknown clause type: {clause_type}. Available: {list(CLAUSE_PATTERNS.keys())}")
    
    patterns = CLAUSE_PATTERNS[clause_type]
    clauses = []
    
    # Try section headers first (most reliable)
    for header_pattern in patterns["section_headers"]:
        matches = list(re.finditer(header_pattern, text, re.IGNORECASE))
        
        for match in matches:
            start = match.start()
            # Get context after the header
            end = min(start + context_chars, len(text))
            clause_text = text[start:end].strip()
            
            # Try to find the end of the section (next section header or double newline)
            next_section = re.search(r'\n\s*\d+[\.\)]\s+[A-Z]', clause_text[100:])
            if next_section:
                clause_text = clause_text[:100 + next_section.start()]
            
            if len(clause_text) > 50:  # Minimum meaningful length
                clauses.append(clause_text)
    
    # If no section headers found, try content indicators
    if not clauses:
        for indicator in patterns["content_indicators"]:
            matches = list(re.finditer(indicator, text, re.IGNORECASE))
            
            for match in matches[:3]:  # Limit to 3 matches per indicator
                start = max(0, match.start() - 200)
                end = min(len(text), match.end() + context_chars)
                clause_text = text[start:end].strip()
                
                if len(clause_text) > 50:
                    clauses.append(clause_text)
    
    # Deduplicate (remove near-identical extractions)
    unique_clauses = []
    seen = set()
    for clause in clauses:
        # Use first 100 chars as dedup key
        key = clause[:100].lower()
        if key not in seen:
            seen.add(key)
            unique_clauses.append(clause)
    
    return unique_clauses


def classify_clause(text: str) -> List[str]:
    """
    Classify what type(s) of clause a text snippet contains.
    
    Args:
        text: Clause text to classify.
    
    Returns:
        List of matching clause types.
    """
    matches = []
    
    for clause_type, patterns in CLAUSE_PATTERNS.items():
        score = 0
        
        for header in patterns["section_headers"]:
            if re.search(header, text, re.IGNORECASE):
                score += 3
        
        for indicator in patterns["content_indicators"]:
            if re.search(indicator, text, re.IGNORECASE):
                score += 1
        
        if score >= 2:
            matches.append(clause_type)
    
    return matches


def extract_all_clauses(text: str, context_chars: int = 2000) -> Dict[str, List[str]]:
    """
    Extract all clause types from a contract.
    
    Args:
        text: Full contract text.
        context_chars: Context size for each extraction.
    
    Returns:
        Dict mapping clause_type to list of extracted texts.
    """
    results = {}
    
    for clause_type in CLAUSE_PATTERNS:
        clauses = extract_clauses(text, clause_type, context_chars)
        if clauses:
            results[clause_type] = clauses
    
    return results


if __name__ == "__main__":
    # Test with sample text
    sample = """
    12. LIMITATION OF LIABILITY
    
    IN NO EVENT SHALL EITHER PARTY'S TOTAL AGGREGATE LIABILITY UNDER THIS AGREEMENT 
    EXCEED THE TOTAL AMOUNTS PAID OR PAYABLE BY CUSTOMER TO PROVIDER IN THE TWELVE (12) 
    MONTHS PRECEDING THE EVENT GIVING RISE TO THE CLAIM. IN NO EVENT SHALL EITHER PARTY 
    BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES.
    
    13. INDEMNIFICATION
    
    Provider shall indemnify, defend, and hold harmless Customer from and against any 
    and all claims, damages, losses, and expenses arising from Provider's breach of 
    this Agreement or Provider's negligence.
    """
    
    results = extract_all_clauses(sample)
    for clause_type, clauses in results.items():
        print(f"\n=== {clause_type} ({len(clauses)} found) ===")
        for c in clauses:
            print(c[:200])
            print("---")
