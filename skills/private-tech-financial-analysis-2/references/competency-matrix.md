# Core Competency Matrix

Load this file when the matter needs domain-depth rules (securities, corporate, tax, IP, regulatory, contracts, employment, privacy, litigation, or legal ops).

## Contents
- I. Securities Law
- II. Corporate Law & Governance
- III. Tax Law
- IV. Intellectual Property
- V. Regulatory Compliance (Crypto, AI, Fintech, Insurtech)
- VI. Commercial Contracts
- VII. Employment & Equity Compensation
- VIII. Data Privacy & Cybersecurity
- IX. Litigation Management
- X. AI-Augmented Legal Operations

---

### I. Securities Law

**Foundational Knowledge**
- Securities Act of 1933, Exchange Act of 1934, Investment Company Act of 1940, Investment Advisers Act of 1940
- Howey test analysis and its application to digital assets under SEC Interpretive Release No. 33-11412 (March 17, 2026)[^5]
- Regulation D exemptions: Rule 504, Rule 506(b) (no general solicitation, up to 35 non-accredited sophisticated investors), Rule 506(c) (general solicitation, all accredited investors)[^6]
- Rule 506(c) accredited investor verification: minimum investment thresholds of $200K for natural persons and $1M for legal entities per March 12, 2025 SEC no-action guidance[^7][^8][^9]
- Private Placement Memorandum (PPM) drafting, subscription agreements, investor questionnaires, Form D filings (within 15 days of first sale)[^10]
- Reg A+, Reg CF, Reg S for cross-border offerings
- Blue sky / state securities law compliance; NASAA coordination

**Digital Asset Securities Classification (2026 Framework)**
- Digital Commodities: functional blockchain assets not dependent on managerial effort (BTC, ETH, SOL, among 16 named examples in SEC Release No. 33-11412)[^5]
- Digital Securities: tokenized traditional securities (stocks, bonds, funds) — securities laws apply regardless of blockchain format[^5]
- Stablecoins: GENIUS Act-compliant payment stablecoins are explicitly excluded from SEC and CFTC jurisdiction — a jurisdictional carve-out creating a distinct regulatory category separate from both capital-market instruments and traditional banking products[^11][^12]
- Digital Collectibles, Digital Tools: generally not securities absent specific structuring red flags[^5]
- Investment Contract Assets under CLARITY Act: digital assets sold via investment contracts are not securities once codified; state securities law preemption for qualifying digital commodities[^13]

**Token Offering Structuring**
- SAFT (Simple Agreement for Future Tokens) vs. direct token sales vs. hybrid structures
- Token classification matrix: utility, governance, security, hybrid
- Insider restriction analysis: CLARITY Act's graduated restrictions on affiliated and related persons with tapering rules post-maturity of blockchain system[^13]
- DeFi safe harbor analysis: exemptions for non-custodial protocol participants (developers, validators) from registration[^13]
- Provisional registration regime for digital commodity exchanges, brokers, and dealers under CLARITY Act[^13]

***

### II. Corporate Law & Governance

**Entity Formation & Structuring**
- Delaware C-Corp: the default for VC-backed startups — certificate of incorporation, bylaws, authorized share structure, board composition, officer appointments[^14][^15]
- Delaware LLC: operating agreements, member governance, manager-managed vs. member-managed structures
- Foundation / nonprofit overlay structures for protocol governance and open-source development
- Cayman Islands exempted companies and foundations for international token projects
- Foreign qualification and multi-state registration (California, New York, and other operating states)[^16]
- Post-incorporation checklist: EIN, corporate bank account, cap table establishment, equity plan adoption, IP assignment agreements[^17]

**Cap Table & Equity Architecture**
- Common stock, preferred stock series (Seed, Series A–D+), SAFEs, convertible notes
- Pro-rata rights, information rights, drag-along, tag-along, ROFR, co-sale provisions
- Stock option plans: ISOs vs. NSOs, exercise price at 409A FMV, vesting schedules (standard 4-year / 1-year cliff)
- 83(b) election: must be filed within 30 days of restricted stock transfer; converts future appreciation from ordinary income (up to 37%) to long-term capital gains (capped at 20%)[^18][^19][^20]
- QSBS exclusion under Section 1202: up to $10M or 10x basis exclusion for qualifying C-Corp stock held 5+ years

**Board & Governance**
- Board composition best practices: independent directors, audit/compensation/nominating committees
- Fiduciary duties: duty of care, duty of loyalty, business judgment rule
- D&O insurance procurement and policy review
- Written consents, meeting minutes, resolutions — governance hygiene as litigation defense
- Dual-class share structures for founder control

***

### III. Tax Law

**Equity Compensation Taxation**
- Section 83: property received for services — taxable at transfer (unrestricted) or vesting (restricted) unless 83(b) election filed[^21]
- Section 409A: deferred compensation compliance; 409A valuation (independent appraisal required); violations trigger 20% excise tax plus interest[^20]
- ISO vs. NSO tax treatment; AMT exposure on ISO exercise
- QSBS: Section 1202 exclusion planning at entity formation and financing rounds

**Token & Crypto Tax**
- Token awards under Section 83: unrestricted grants taxed as ordinary income at FMV at grant; restricted tokens taxed at vesting unless 83(b) filed within 30 days[^21]
- Restricted Token Units (RTUs): ordinary income recognized when tokens transferred to digital wallet, analogous to RSUs[^21]
- Employer withholding obligations: cash withholding required; token reduction-in-lieu mechanism[^21]
- Crypto-to-crypto swaps: taxable events under IRS Notice 2014-21 and Revenue Ruling 2023-14
- Hard forks, airdrops: ordinary income at FMV of received tokens
- DeFi staking/yield: ordinary income treatment; pending regulatory guidance on timing
- Mining income: ordinary income + self-employment tax for sole proprietors
- Wash sale rules: currently do not apply to cryptocurrency (pending legislation)
- FBAR and Form 8938 obligations for foreign digital asset accounts
- Section 1256 contracts: mark-to-market treatment for certain regulated futures on crypto

**Corporate Tax Planning**
- Choice of entity analysis: C-Corp vs. pass-through
- R&D tax credits: Section 41 credits for qualifying AI and crypto development activities
- Transfer pricing for international IP ownership structures
- State and local tax (SALT): nexus analysis for digital businesses; California FTB obligations

***

### IV. Intellectual Property

**Patent Strategy**
- Software patent eligibility under Alice/Mayo: identify technical improvements that overcome § 101 rejection; emphasize specific technical solutions over abstract ideas
- AI-generated inventions: USPTO guidance (February 2024) — AI cannot be named inventor; human contribution requirement
- Provisional applications: 12-month priority window; file early, file often
- Patent portfolio strategy for crypto protocols, AI models, fintech payment rails, insurtech underwriting algorithms
- Freedom-to-operate (FTO) analysis before product launch
- Post-grant proceedings: IPR, PGR as both offensive and defensive tools

**Trade Secrets**
- Uniform Trade Secrets Act (UTSA) and Defend Trade Secrets Act (DTSA): federal civil cause of action
- AI-era trade secret strategy: source code, model weights, training data, algorithms, and prompt engineering as protectable trade secrets[^22]
- Trade secret audit: identify assets, assess competitive value, document protection measures[^23]
- IP assignment agreements: update to specifically include AI-generated outputs and AI-related IP[^23]
- Vendor agreements: AI-specific clauses, audit rights, definition of proprietary AI trade secrets, output ownership[^23]
- NDAs: mutual vs. one-way; definitions of confidential information to encompass model outputs and training data
- Exit interview protocols; non-solicitation and non-compete enforceability by state (California: near-total prohibition under Bus. & Prof. Code § 16600)

**Copyright**
- AI-generated works: Copyright Office position — human authorship required; "sufficient human control" standard developing
- Open-source license compliance: GPL, LGPL, MIT, Apache 2.0 — avoid copyleft contamination in proprietary AI/crypto stacks
- DMCA safe harbor maintenance for platforms: § 512 notice-and-takedown compliance
- Training data copyright issues: pending litigation (Authors Guild, Getty Images); fair use analysis

**Trademark**
- Brand protection: register core marks in IC 9, 35, 36, 42 (tech, financial services, software)
- Crypto/token name clearance: USPTO and international (Madrid Protocol) filings
- Domain name strategy; UDRP proceedings
- Trade dress protection for UX/UI

***

### V. Regulatory Compliance

#### A. Crypto / Digital Assets

**US Federal Framework**
- GENIUS Act (Public Law 119-27, enacted July 18, 2025): comprehensive framework for payment stablecoins; 1:1 reserve backing in permissible assets; AML/BSA obligations; issuer licensing via OCC, Fed, or state regulators[^24][^12][^25][^11]
- CLARITY Act (pending Senate action as of July 2026): SEC/CFTC jurisdictional split; CFTC primary oversight for digital commodities spot markets; SEC retains jurisdiction over digital securities; provisional registration for intermediaries[^26][^5][^13]
- BSA/AML: FinCEN MSB registration; KYC/CIP program; SAR filing obligations; OFAC sanctions screening
- SEC enforcement posture (2026): decreased direct enforcement but increased private securities litigation in digital asset space[^26]
- CFTC jurisdiction over crypto derivatives, perpetuals, and commodity spot markets for digital commodities

**State Frameworks**
- BitLicense (New York DFS): required for NY-based crypto business activity
- Money transmitter licenses: 48-state licensing analysis; NMLS filing; surety bond requirements
- California DFPI: Digital Financial Assets Law (DFAL) registration and compliance
- Wyoming SPDI (Special Purpose Depository Institution) charter considerations

**International**
- MiCA (EU Regulation 2023/1114): fully applicable December 30, 2024; CASP licensing required for exchanges, custodians, wallet services, and token issuers offering services to EU users — operating without authorization after July 1, 2026 is illegal[^27][^28][^29]
- MiCA whitepaper requirements for token launches; stablecoin capital requirements; passporting across EU member states once licensed in one jurisdiction[^28]
- DORA (Digital Operational Resilience Act): applies to MiCA-licensed crypto firms; ICT risk identification and assessment requirements[^28]
- Swiss FINMA: DLT Act, banking license considerations for Swiss foundations and token issuers

#### B. Artificial Intelligence

**US Federal**
- Executive Orders on AI: EO 14110 (Biden) revoked; EO 14179 (Trump, January 2025) — "Removing Barriers to American Leadership in Artificial Intelligence"; focus on innovation over precautionary regulation
- NIST AI Risk Management Framework (AI RMF 1.0): voluntary but de facto standard for enterprise AI governance[^30]
- FTC guidance on AI-driven deception and unfair practices; CFPB guidance on AI in credit decisioning (adverse action notices)
- Sector-specific: FDA regulation of AI/ML-enabled Software as a Medical Device (SaMD); OCC/FDIC guidance on AI in banking

**EU AI Act**
- Risk-based classification: unacceptable risk (banned), high-risk (subject to conformity assessment), limited risk (transparency obligations), minimal risk (largely unregulated)[^31][^32]
- GPAI (General-Purpose AI Model) obligations effective August 2, 2025: capability disclosures, copyright transparency, systemic risk assessment for frontier models[^33]
- Prohibited practices (effective February 2, 2025): social scoring, real-time biometric surveillance in public spaces, subliminal manipulation, predictive policing[^34]
- Core compliance obligations mandatory August 2, 2026: high-risk AI system requirements; transparency rules including AI-generated content labeling[^35][^33]
- Penalties: up to €35M or 7% of global annual turnover for violations of prohibited practices
- US companies: extraterritorial reach — if AI system output is used in EU, EU AI Act applies[^32][^35]

**AI Governance Framework Construction**
1. Inventory all AI systems; classify by risk tier (high / medium / low)[^36][^30]
2. Establish AI Oversight Committee: legal, privacy, IT, HR, procurement, data science[^30]
3. Draft AI Usage Policy: permitted vs. prohibited uses; mandatory human review for high-risk outputs; disclosure requirements[^36][^30]
4. Update employment policies: EEO compliance for AI-assisted hiring; accommodation processes
5. Vendor management: AI-specific contractual provisions, audit rights, indemnification, insurance coverage for AI-related claims[^30]
6. Quarterly review cycle: governance as a living document, not a one-time exercise[^36]

#### C. Fintech

- Bank Secrecy Act / Anti-Money Laundering: FinCEN compliance, SAR/CTR filing, MSB registration
- Payment services: NACHA rules, card network agreements (Visa/MC), state money transmission
- Lending: Truth in Lending Act (TILA), Equal Credit Opportunity Act (ECOA), Fair Credit Reporting Act (FCRA), state usury laws
- CFPB supervision thresholds and examination readiness
- Open banking / Section 1033 (CFPB Final Rule, 2024): personal financial data rights; API standards
- SPAC structures and de-SPAC transactions for fintech public market access
- Bank partnership agreements (BaaS): risk allocation, charter responsibility, oversight obligations

#### D. Insurtech

- State insurance regulation: insurance is primarily state-regulated; identify operating model (carrier, MGA, TPOA, or vendor) before licensing strategy[^37]
- Carrier formation: certificate of authority in each operating state; domicile selection (Delaware, Vermont, Cayman for captives)
- MGA regulation: delegated authority arrangements, binding authority limits, auditable compliance programs
- NAIC Model Bulletin on AI (2023): insurers remain responsible for algorithmic underwriting decisions made by third-party AI vendors[^37]
- New York DFS Circular Letter 2024-7: AI fairness in underwriting and claims; prohibits proxy discrimination[^37]
- Algorithmic fairness counsel role: document and audit AI models to demonstrate non-discrimination on protected class proxies[^37]
- Rate and form filing: state approval requirements for insurance products; speed-to-market strategies
- Parametric insurance: novel regulatory treatment; contract vs. insurance characterization analysis
- Data privacy in insurance: state comprehensive privacy laws intersecting with insurance data use[^37]
- Embedded insurance partnerships: compliant distribution structures, delegated authority agreements[^37]

***

### VI. Commercial Contracts

**Contract Architecture**
- Master Services Agreements (MSA): key provisions — limitation of liability (cap at 12 months fees is baseline), indemnification (IP, data breach, third-party claims), representations and warranties, termination rights, SLAs
- SaaS Agreements: subscription terms, uptime SLAs, data processing agreements (DPAs), acceptable use policies
- API and developer agreements: rate limits, IP ownership of outputs, prohibited use cases
- Data license agreements: permitted use definitions, sublicensing restrictions, audit rights
- Token sale agreements and SAFTs: regulatory analysis embedded in drafting
- Smart contract audits: legal enforceability overlay on code audits; DAO legal wrappers

**AI-Specific Contractual Provisions**
- AI output ownership: clear IP assignment to company for AI-generated work product
- Training data rights: warranty of authority to use; indemnification for infringement claims
- Model performance: accuracy benchmarks, hallucination liability, output validation obligations
- AI tool vendor agreements: data handling protocol, no training on proprietary data, model confidentiality[^30]

**Negotiation Strategy**
- Default position: standard market position for your company's leverage stage
- Red-line triggers: mutual NDA → unilateral; uncapped liability → negotiated caps; broad IP assignment → scoped to deliverables
- Playbook development: pre-approved fallback positions for each key clause to enable business-speed contracting

***

### VII. Employment & Equity Compensation

- Offer letters, employment agreements, severance agreements
- IP assignment and confidentiality agreements: California requirements under Labor Code § 2870 (carve-out for inventions unrelated to company business)
- Non-compete enforceability: California ban (§ 16600); FTC non-compete rule litigation status (2026 — rule struck down, state law governs)
- Equity plan administration: Section 422 ISO requirements, 83(b) election monitoring, 409A annual re-appraisal or triggering events
- Token compensation: Section 83 analysis; withholding obligations; written plan documentation[^21]
- Remote workforce: multi-state employer obligations, payroll tax nexus, workers' compensation

***

### VIII. Data Privacy & Cybersecurity

- GDPR (EU): lawful basis for processing, DPAs, SCCs for data transfers, DPO appointment triggers, breach notification (72-hour window)
- CCPA/CPRA (California): consumer rights, privacy notice, opt-out of sale/sharing, sensitive personal information handling, annual cybersecurity audit obligation
- State comprehensive privacy laws: Virginia, Colorado, Connecticut, Texas, and 15+ additional states enacted through 2025
- HIPAA: PHI handling if insurtech or health AI application
- SOC 2 Type II: GC role in vendor selection and contractual SOC 2 requirements
- Incident response: retainer with outside forensic counsel; breach notification obligations by jurisdiction; SEC cybersecurity disclosure rules (Form 8-K Item 1.05 for material incidents)

***

### IX. Litigation Management

**Defensive Posture**
- Litigation hold procedures: immediate document preservation upon reasonably anticipated litigation; ESI protocols; Slack, email, and blockchain data preservation[^38]
- Outside counsel management: scope of engagement letters; budget approval gates at $25K, $50K, $100K; preferred provider panels
- Alternative dispute resolution: arbitration clause strategy (AAA, JAMS, ICC); class action waiver enforceability by jurisdiction
- Insurance program: D&O, E&O, cyber liability, EPL — coordinate with litigation strategy
- Regulatory investigation response: Wells process for SEC matters; FinCEN civil money penalty response; state AG investigations[^39]

**Offensive/Enforcement**
- IP enforcement: cease and desist strategy; DMCA takedowns; patent assertion vs. licensing
- Trade secret misappropriation: TRO/preliminary injunction standards; DTSA seizure orders[^23]
- Contract disputes: demand letter strategy; arbitration initiation; emergency relief

**Digital Asset Litigation (2026 Landscape)**
- Private securities litigation in digital asset space increased in 2025 and continues into 2026[^26]
- Token purchaser class actions: primary defenses — asset classification, disclosure adequacy, statute of limitations
- Smart contract exploit claims: DAO governance liability; protocol developer liability theories
- Regulatory defense: SEC formal order response; cooperation credit strategy

***

### X. AI-Augmented Legal Operations

**Perplexity-Specific Workflow**
- Use Perplexity with web search enabled for all regulatory research: statutes, SEC releases, no-action letters, CFTC guidance, MiCA ESMA Q&As
- Prompt structure for legal research: [Jurisdiction] + [Legal issue] + [Applicable statute/regulation] + [Recent developments as of current date]
- Prompt structure for document drafting: [Document type] + [Parties/context] + [Key commercial terms] + [Risk tolerance: aggressive/market/conservative] + [Governing law]
- Always request citation to primary sources; verify against SEC.gov, FinCEN.gov, ESMA.europa.eu, CFTC.gov
- Use follow-up queries to stress-test analysis: "What is the strongest counterargument to this position?" / "What additional facts would change this analysis?"

**AI Tool Governance for Legal Department**
- 87% of GCs use AI tools as of 2026, up from 44% in 2025[^40]
- Approved platforms for confidential matter work: specify in written policy; never use unapproved tools for privileged material
- Human-in-the-loop requirement: every AI output reviewed before external use or reliance[^40][^30]
- Matter management: all AI-assisted analysis to be documented in matter management system
- Prompt engineering competency: in-house legal team training on effective legal AI prompting as core professional development[^36]

**Contract Automation**
- Template library: pre-approved fallbacks for all standard commercial agreements
- AI contract review: flag inconsistencies with playbook; auto-negotiate routine clauses[^41]
- KPI dashboard: contract volume, turnaround time (target: <2 business days for NDAs, <5 for MSAs), litigation status, legal spend vs. budget[^38]

***