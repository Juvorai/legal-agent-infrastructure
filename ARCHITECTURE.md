# Multi-Agent Legal Infrastructure Architecture
## Shared Infrastructure, Isolated Configuration

This document describes the architecture for running multiple legal agents
(Chutes_Legal_Privileged, IOVI_Legal_Privileged, etc.) that share infrastructure
improvements without any data leakage between them.

## Principles

1. **Infrastructure is shared.** Skills, scripts, methodology, style rules, and
   formatting rules are identical across all agents. One copy, synced to all.

2. **Configuration is isolated.** Company context, Perplexity project, vector store,
   knowledge sources, and credentials are unique per agent. Never shared.

3. **Data isolation is guaranteed by Gumloop architecture.** Each agent has its own
   sandbox, workspace, knowledge base sources, and secrets. No cross-agent file access.

## What Lives Where

### AGENT.md Structure (per agent)

```
---
name: [Agent Name]
description: [One-line description]
icon: [icon]
---

# COMPANY CONFIGURATION (unique per agent, never shared)
- Company context (name, jurisdiction, entity type, key personnel)
- Agent name and email
- Tracked changes author
- Perplexity project URL and name
- Browserbase navigation rule ID
- Knowledge sources
- Midpage connector rule

---

# SHARED INFRASTRUCTURE (identical across all agents)
- LLM routing (Chutes-first)
- Core doctrine (grounded legal analysis)
- Grounding rules
- Voice rules
- Orchestration and delegation
- Methodology
- Perplexity routing (references config, not hardcoded)
- Redlining rules
- Native redlining methodology
- Document output rules
- Docx formatting rules
```

### Skills (shared, company-agnostic)

All skills must be company-agnostic. No hardcoded company names, project URLs,
or personal references in skill scripts. Company context is always read from
AGENT.md or pplx_config.json at runtime.

Skills that are shared:
- ben-writing-style-2 (voice and style)
- legal-deep-research (methodology + scripts)
- office-doc-engine (document building)
- perplexity-deep-research (Perplexity client)
- chutes-api (LLM routing)
- edgar-search (SEC filings)
- tax-research (tax law)
- gc-clo-tech-startup-2 (GC analysis framework)
- private-tech-financial-analysis-2 (financial analysis)

### Workspace Files (isolated per agent)

Each agent's /home/user/.workspace/agent/ contains:
- pplx_config.json (Perplexity project config - UNIQUE per agent)
- perplexity_methodology_reference.md (shared methodology - synced)
- competitive_reflection.md (per-agent observations)
- doc_rag_store/ (vector store - UNIQUE per agent, contains only that company's docs)
- requirements.txt (shared dependencies - synced)

## Propagation Mechanism

### GitHub Repo (primary)

```
github.com/Juvorai/legal-agent-infrastructure (private)
├── skills/
│   ├── ben-writing-style-2/
│   ├── legal-deep-research/
│   ├── office-doc-engine/
│   ├── perplexity-deep-research/
│   ├── chutes-api/
│   ├── edgar-search/
│   ├── tax-research/
│   ├── gc-clo-tech-startup-2/
│   └── private-tech-financial-analysis-2/
├── templates/
│   ├── AGENT_TEMPLATE.md
│   └── SHARED_INFRASTRUCTURE.md
├── clause-library/
├── scripts/
├── VERSION.json
└── CHANGELOG.md
```

Each agent has a sync schedule:
1. Pull from the repo via GitHub integration
2. Check VERSION.json against local version
3. If newer: install updated skills, update AGENT.md infrastructure section
4. Log the update

## Creating a New Agent (checklist)

1. Create new agent in the target team
2. Copy AGENT.md template, fill in COMPANY CONFIGURATION section
3. Create Perplexity project for the new company
4. Create Browserbase persistent context for the new project
5. Configure pplx_config.json with new project URL and context ID
6. Create Browserbase navigation rule (MCP rule) for the new project
7. Connect knowledge base sources (company's Drive folder)
8. Connect required servers (Midpage, Browserbase, Exa, Firecrawl, etc.)
9. Install skills (from GitHub repo)
10. Create sync schedule
11. Test: send a test email, run a test redline, verify isolation

## Data Isolation Guarantees

| Resource | Isolation mechanism |
|----------|-------------------|
| Sandbox filesystem | Per-agent, no cross-agent access |
| Workspace files | Per-agent /home/user/.workspace/agent/ |
| Knowledge base | Configured per-agent (specific Drive sources) |
| Perplexity project | Separate project URL + separate Browserbase context |
| Vector store | Per-agent doc_rag_store directory |
| Secrets | Per-team, injected per-agent |
| Email inbox | Unique @gumloopagents.com address per agent |
| Conversation history | Per-agent, searchable only within that agent |

## What NEVER Crosses Agent Boundaries

- Document contents (contracts, memos, cap tables)
- Perplexity thread contents
- Vector store embeddings
- Knowledge base search results
- Email contents
- Credentials/secrets
- Conversation history

## What IS Shared (infrastructure only)

- Skill scripts (no company data in them)
- Methodology reference (generic legal analysis patterns)
- Style rules (Ben's voice applies to all his clients)
- Docx formatting rules
- Redlining methodology
- LLM routing configuration
- Sync schedules
