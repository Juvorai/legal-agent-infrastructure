# edgar-search

Search and extract from SEC EDGAR filings, including full-text search across all filings since 2001 and downloading exhibits (EX-10 material contracts) as clean text. Use when the user asks about SEC filings, public company disclosures, securities filings, or wants to mine material contracts and other exhibits for contractual precedent, clause language, or deal terms.

## Important Legal Note

EDGAR filings are cited as **precedent or market-practice evidence only, never as legal authority**. They show what companies actually agree to in practice, which is valuable for contract negotiation and drafting, but they do not establish legal rules.

## EDGAR Full-Text Search API

The SEC provides a full-text search API at:
```
https://efts.sec.gov/LATEST/search-index?q={query}&dateRange=custom&startdt={start}&enddt={end}&forms={form_types}
```

### Search Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| q | Search query (supports quoted phrases) | "limitation of liability" |
| forms | Comma-separated form types | 10-K,10-Q,8-K,S-1 |
| dateRange | "custom" for date filtering | custom |
| startdt | Start date (YYYY-MM-DD) | 2020-01-01 |
| enddt | End date (YYYY-MM-DD) | 2024-12-31 |
| entityName | Filter by company name | "Apple Inc" |
| ciks | Filter by CIK number | 0000320193 |

### Exhibit Types for Contract Mining

| Exhibit | Description |
|---------|-------------|
| EX-10.* | Material contracts (MSAs, SaaS agreements, employment agreements) |
| EX-10.1 | Often the primary material contract |
| EX-10.2+ | Additional material contracts |
| EX-21 | Subsidiaries |
| EX-23 | Auditor consent |
| EX-31 | CEO/CFO certifications |
| EX-32 | Section 1350 certifications |

## Usage

### Search for Filings

```python
from scripts.edgar_search import search_edgar

results = search_edgar(
    query='"limitation of liability" "shall not exceed"',
    forms="10-K,8-K",
    start_date="2022-01-01",
    end_date="2024-12-31",
)
```

### Download Exhibit Text

```python
from scripts.edgar_search import get_exhibit_text

text = get_exhibit_text(
    accession_number="0000320193-24-000123",
    exhibit="ex10-1.htm",
)
```

### Extract Clause Language

```python
from scripts.edgar_search import extract_clauses

clauses = extract_clauses(
    text=exhibit_text,
    clause_type="limitation_of_liability",
)
```

## Clause Extraction Patterns

The skill includes regex patterns for common clause types:

- **Limitation of Liability**: "limitation of liability", "shall not exceed", "aggregate liability", "cap on liability"
- **Indemnification**: "indemnify", "indemnification", "hold harmless", "defend"
- **IP Assignment**: "assign", "intellectual property", "work product", "inventions"
- **Data Protection**: "data protection", "personal data", "GDPR", "CCPA", "data processing"
- **Termination**: "termination", "terminate for cause", "terminate for convenience"
- **Governing Law**: "governing law", "governed by", "jurisdiction", "venue"

## Scripts

- `scripts/edgar_search.py` - EDGAR full-text search and exhibit download
- `scripts/clause_extractor.py` - Extract specific clause types from contract text

## Rate Limiting

SEC EDGAR requires a User-Agent header identifying your application:
```
User-Agent: Chutes Legal Research ben@chutes.ai
```

Rate limit: 10 requests per second maximum. The scripts include built-in rate limiting.
