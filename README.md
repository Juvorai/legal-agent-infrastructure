# Legal Agent Infrastructure

Shared infrastructure for Benjamin Snipes' multi-agent legal practice.

## Purpose

This repository is the single source of truth for shared legal agent infrastructure.
All legal agents (Chutes_Legal_Privileged, IOVI_Legal_Privileged, etc.) pull their
shared skills, methodology, and formatting rules from here.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full multi-agent architecture,
isolation guarantees, and new-agent creation checklist.

## Repository Structure

```
├── README.md
├── ARCHITECTURE.md              # Multi-agent architecture documentation
├── VERSION.json                 # Version tracking for sync
├── CHANGELOG.md                 # Change history
├── templates/
│   ├── AGENT_TEMPLATE.md        # Template for creating new agents
│   └── SHARED_INFRASTRUCTURE.md # Canonical shared infrastructure section
├── skills/                      # Shared skills (company-agnostic)
│   ├── ben-writing-style-2/
│   ├── legal-deep-research/
│   ├── office-doc-engine/
│   ├── perplexity-deep-research/
│   ├── chutes-api/
│   ├── chutes-first-routing/
│   ├── edgar-search/
│   ├── tax-research/
│   ├── gc-clo-tech-startup-2/
│   └── private-tech-financial-analysis-2/
├── clause-library/              # Market-standard clause language from EDGAR EX-10
│   ├── limitation-of-liability/
│   ├── indemnification/
│   ├── ip-assignment/
│   ├── data-protection/
│   ├── termination/
│   └── governing-law/
└── scripts/                     # Shared utility scripts
    ├── chutes_client.py
    ├── style_check.py
    └── verify_redline.py
```

## Isolation Rules

1. **Shared infrastructure never references client configuration.**
2. **Client configuration never enters this repository.**
3. **Skills must be company-agnostic.** No hardcoded company names, project URLs, or personal references.
4. **The clause library contains only publicly available market language** (from EDGAR filings), never client-specific terms.

## Sync Protocol

Each agent checks VERSION.json on session start. If the repo version is newer:
1. Pull updated skills
2. Update the SHARED INFRASTRUCTURE section of AGENT.md
3. Log the update

## Maintenance

- General improvements: develop in a client agent, validate on real work, then push here.
- Client-specific adaptations: stay local to the client agent. Never pushed here.
