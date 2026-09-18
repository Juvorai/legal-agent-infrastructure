# Sources — Corporate & VC Finance

Authoritative primary sources scanned each monitoring cycle. Approved defaults (2026-09-18, B. Snipes: "Defaults are fine for this first run").

| Source | What is scanned | Access |
|---|---|---|
| SEC press releases | Rulemaking, exemptive orders, enforcement with corporate/VC relevance | https://www.sec.gov/newsroom/press-releases |
| Federal Register (SEC agency feed) | Proposed/final rules, SRO notices of substance, PCAOB filings | https://www.federalregister.gov/api/v1/documents.json?conditions[agencies][]=securities-and-exchange-commission |
| CourtListener — Court of Chancery (delch) | Corporate opinions: DGCL §§ 220/225/228/262, fiduciary duty, M&A | courtlistener MCP search, court=delch |
| CourtListener — Delaware Supreme Court (del) | Corporate appeals | courtlistener MCP search, court=del |
| Congress.gov | Capital-formation bills (keyword screen: capital, securities, investment, venture, crowdfund, accredited, offering, emerging growth) | https://api.congress.gov/v3/bill (API key in secret store) |

## Candidate sources (pending user approval — do not scan yet)

- NVCA model document updates (nvca.org)
- PitchBook-NVCA Venture Monitor
- Delaware General Assembly DGCL amendment tracking
