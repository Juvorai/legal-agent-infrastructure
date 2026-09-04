#!/usr/bin/env python3
"""
edgar_search.py - SEC EDGAR full-text search and exhibit download.
Used for mining material contracts for contractual precedent and clause language.

IMPORTANT: EDGAR filings are market-practice evidence only, never legal authority.
"""

import requests
import time
import json
import re
from typing import List, Dict, Optional, Any
from urllib.parse import quote

# SEC requires a User-Agent header
USER_AGENT = "Chutes Legal Research ben@chutes.ai"
BASE_SEARCH_URL = "https://efts.sec.gov/LATEST/search-index"
BASE_FILING_URL = "https://www.sec.gov/Archives/edgar/data"

# Rate limiting: 10 requests per second
_last_request_time = 0
_MIN_INTERVAL = 0.11  # slightly more than 100ms


def _rate_limit():
    """Enforce SEC rate limiting."""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - elapsed)
    _last_request_time = time.time()


def _headers():
    return {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }


def search_edgar(
    query: str,
    forms: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    entity_name: Optional[str] = None,
    ciks: Optional[str] = None,
    max_results: int = 20,
) -> List[Dict[str, Any]]:
    """
    Search SEC EDGAR full-text search API.
    
    Args:
        query: Search query (supports quoted phrases).
        forms: Comma-separated form types (e.g., "10-K,8-K,S-1").
        start_date: Start date filter (YYYY-MM-DD).
        end_date: End date filter (YYYY-MM-DD).
        entity_name: Filter by company name.
        ciks: Filter by CIK number.
        max_results: Maximum results to return.
    
    Returns:
        List of filing results with accession numbers, dates, and links.
    """
    _rate_limit()
    
    params = {"q": query}
    
    if forms:
        params["forms"] = forms
    if start_date and end_date:
        params["dateRange"] = "custom"
        params["startdt"] = start_date
        params["enddt"] = end_date
    if entity_name:
        params["entityName"] = entity_name
    if ciks:
        params["ciks"] = ciks
    
    response = requests.get(
        BASE_SEARCH_URL,
        params=params,
        headers=_headers(),
        timeout=30,
    )
    
    if response.status_code != 200:
        raise RuntimeError(f"EDGAR search error {response.status_code}: {response.text[:500]}")
    
    data = response.json()
    
    results = []
    hits = data.get("hits", {}).get("hits", [])
    
    for hit in hits[:max_results]:
        source = hit.get("_source", {})
        results.append({
            "accession_number": source.get("adsh", ""),
            "form_type": source.get("form", ""),
            "filed_date": source.get("file_date", ""),
            "entity_name": source.get("entity_name", ""),
            "cik": source.get("cik", ""),
            "file_num": source.get("file_num", ""),
            "display_names": source.get("display_names", []),
            "file_type": source.get("file_type", ""),
            "adsh": source.get("adsh", ""),
        })
    
    return results


def get_filing_index(accession_number: str) -> List[Dict[str, str]]:
    """
    Get the filing index (list of documents) for an accession number.
    
    Args:
        accession_number: SEC accession number (e.g., "0000320193-24-000123").
    
    Returns:
        List of documents with filenames and types.
    """
    _rate_limit()
    
    # Convert accession number to directory format
    acc_clean = accession_number.replace("-", "")
    cik = accession_number.split("-")[0]
    
    url = f"{BASE_FILING_URL}/{cik}/{acc_clean}/index.json"
    
    response = requests.get(url, headers=_headers(), timeout=30)
    
    if response.status_code != 200:
        raise RuntimeError(f"EDGAR index error {response.status_code}: {response.text[:500]}")
    
    data = response.json()
    
    documents = []
    for item in data.get("directory", {}).get("item", []):
        documents.append({
            "filename": item.get("name", ""),
            "size": item.get("size", ""),
        })
    
    return documents


def get_exhibit_text(accession_number: str, exhibit_filename: str) -> str:
    """
    Download and extract text from an exhibit file.
    
    Args:
        accession_number: SEC accession number.
        exhibit_filename: Filename of the exhibit (e.g., "ex10-1.htm").
    
    Returns:
        Clean text content of the exhibit.
    """
    _rate_limit()
    
    acc_clean = accession_number.replace("-", "")
    cik = accession_number.split("-")[0]
    
    url = f"{BASE_FILING_URL}/{cik}/{acc_clean}/{exhibit_filename}"
    
    response = requests.get(url, headers=_headers(), timeout=60)
    
    if response.status_code != 200:
        raise RuntimeError(f"EDGAR exhibit error {response.status_code}: {response.text[:500]}")
    
    # Extract text from HTML
    text = response.text
    
    # Remove HTML tags
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r' +', ' ', text)
    
    # Decode HTML entities
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    text = text.replace('&nbsp;', ' ')
    text = text.replace('\u2019', "'")
    text = text.replace('\u2018', "'")
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    text = text.replace('\u2014', ' ')
    text = text.replace('\u2013', ' ')
    
    return text.strip()


def find_exhibits(accession_number: str, exhibit_prefix: str = "ex10") -> List[str]:
    """
    Find exhibit files in a filing that match a prefix.
    
    Args:
        accession_number: SEC accession number.
        exhibit_prefix: Prefix to match (default "ex10" for material contracts).
    
    Returns:
        List of matching exhibit filenames.
    """
    documents = get_filing_index(accession_number)
    
    exhibits = []
    for doc in documents:
        filename = doc["filename"].lower()
        if filename.startswith(exhibit_prefix) and (
            filename.endswith(".htm") or filename.endswith(".html") or filename.endswith(".txt")
        ):
            exhibits.append(doc["filename"])
    
    return exhibits


def search_and_extract(
    query: str,
    clause_type: str,
    forms: str = "10-K,8-K",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    max_filings: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search EDGAR for filings containing a query, then extract clause text.
    
    Args:
        query: Search query.
        clause_type: Type of clause to extract (see clause_extractor.py).
        forms: Form types to search.
        start_date: Start date filter.
        end_date: End date filter.
        max_filings: Maximum filings to process.
    
    Returns:
        List of extracted clauses with source information.
    """
    from clause_extractor import extract_clauses
    
    results = search_edgar(
        query=query,
        forms=forms,
        start_date=start_date,
        end_date=end_date,
        max_results=max_filings,
    )
    
    extracted = []
    
    for filing in results:
        accession = filing["accession_number"]
        
        try:
            exhibits = find_exhibits(accession)
            
            for exhibit in exhibits[:2]:  # Limit to 2 exhibits per filing
                try:
                    text = get_exhibit_text(accession, exhibit)
                    clauses = extract_clauses(text, clause_type)
                    
                    for clause in clauses:
                        extracted.append({
                            "source_filing": accession,
                            "source_exhibit": exhibit,
                            "entity_name": filing["entity_name"],
                            "filed_date": filing["filed_date"],
                            "clause_text": clause,
                        })
                except Exception as e:
                    continue  # Skip exhibits that fail to download
                    
        except Exception as e:
            continue  # Skip filings that fail
    
    return extracted


if __name__ == "__main__":
    # Quick test
    results = search_edgar(
        query='"limitation of liability"',
        forms="10-K",
        max_results=3,
    )
    print(json.dumps(results, indent=2))
