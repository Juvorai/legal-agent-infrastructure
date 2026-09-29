# Multi-Agent Legal Infrastructure Architecture
## Shared Firm Layer, Team-Per-Company Isolation

This document describes the architecture for running legal agents for multiple
client companies (Chutes, Molecule, Hey, etc.) that share firm infrastructure
without any data leakage between clients.

## Principles

1. **The team is the privilege boundary.** Each client company gets its own
   Gumloop team. Client data connectors (Drive, Gmail, Slack, etc.) are
   configured at the team level, so credentials for one client's accounts
   physically do not exist in another client's team. No agent misconfiguration
   can cross the boundary.

2. **Infrastructure is shared.** Skills, scripts, methodology, style rules, and
   formatting rules are identical across all client teams. One copy, synced
   from the GitHub repo to every GC agent.

3. **Configuration is isolated.** Company context, Perplexity project, vector
   store, knowledge sources, and credentials are unique per client team.
   Never shared.

## The Firm Layer (shared across all client teams)

Three resources serve every client team and are the only things that cross
team boundaries:

| Resource | Role |
|----------|------|
| GitHub repo `Juvorai/legal-agent-infrastructure` | Canonical source of skills, templates, shared infrastructure text, VERSION.json, CHANGELOG.md |
| Legal Ops agent | Maintains the repo: legal-developments monitoring, skill updates, version bumps, weekly managing-partner digest |
| CTO agent | Platform side: provisions new teams and agents, wires connectors and secrets, manages triggers/schedules/MCP rules, opens repo PRs for infrastructure changes |

The firm layer holds NO client data. Skills are company-agnostic by design:
no hardcoded company names, project URLs, or personal references in skill
scripts. Company context is always read from AGENT.md or pplx_config.json
at runtime.

## The Client Layer (one team per company)

Each client team contains exactly two agents:

### 1. `[Company]_GC_Agent` (generalist GC, attorney-facing)

The privileged workhorse used by the attorney (Ben). Does the legal work:
research, memos, contract drafting and redlining, diligence.

- Knowledge sources: the client's full Drive folder (privileged material
  included; only the attorney uses this agent)
- Full skill set from the repo
- Research servers: Midpage (with the "Midpage Custom" connector preference
  rule), Browserbase, Exa, Firecrawl, tax tools
- Perplexity: dedicated project for this client, dedicated Browserbase
  persistent context, navigation MCP rule scoped to that project
- Repo sync schedule (see Propagation)

### 2. `[Company]_Legal_Privileged` (client-company-facing)

The surface the client's employees interact with, per the client-lookup-agent
pattern: answers company and legal-information questions from a curated,
non-privileged corpus, inside the client's own Slack workspace or by email
from the client domain. No Gumloop accounts needed for employees.

- Knowledge sources: a curated NON-PRIVILEGED subset only (policies, FAQs,
  approved templates). This is the privilege firewall inside the team.
- No research tools, no Perplexity, no document drafting
- Anything requiring legal judgment escalates to the attorney; it is never
  answered directly

### AGENT.md Structure (per agent)

```
---
name: [Agent Name]
description: [One-line description]
icon: [icon]
---

# COMPANY CONFIGURATION (unique per client team, never shared)
- Company context (name, jurisdiction, entity type, key personnel)
- Agent name and email
- Tracked changes author
- Perplexity project URL and name (GC agent only)
- Browserbase navigation rule ID (GC agent only)
- Knowledge sources
- Midpage connector rule

---

# SHARED INFRASTRUCTURE (identical across all GC agents)
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

The SHARED INFRASTRUCTURE section is synced from
templates/SHARED_INFRASTRUCTURE.md in the repo. Never edit it directly on an
individual agent; edit the repo and sync.

### Workspace Files (isolated per agent)

Each agent's /home/user/.workspace/agent/ contains:
- pplx_config.json (Perplexity project config - UNIQUE per client, GC agent only)
- perplexity_methodology_reference.md (shared methodology - synced)
- competitive_reflection.md (per-agent observations)
- doc_rag_store/ (vector store - UNIQUE per client, contains only that company's docs)
- requirements.txt (shared dependencies - synced)

## Propagation Mechanism

### GitHub Repo (primary)

```
github.com/Juvorai/legal-agent-infrastructure (private)
├── skills/
│   ├── ben-writing-style-2/
│   ├── legal-deep-research/
│   ├── office-doc-engine/
│   ├── docx-redlining/
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

### Sync schedule (on every GC agent)

1. Pull from the repo via GitHub integration
2. Check VERSION.json against local version
3. If newer: install updated skills, update AGENT.md infrastructure section
4. Log the update

### Change flow

- Legal Ops agent: legal-developments monitoring, practice-skill updates,
  version bumps, weekly digest. Opens or merges repo changes.
- CTO agent: platform and infrastructure changes (new skills, script changes,
  template changes). Opens repo PRs.
- Every GC agent picks changes up on its next sync. Client-facing agents
  receive only the minimal skill surface per the client-lookup-agent pattern
  and do not run the full sync.

## Onboarding a New Client Company (checklist)

Executed by the CTO agent; team creation and membership done by the user in
the Gumloop UI (billing and membership are user decisions).

1. Create a new Gumloop team for the client (user action)
2. Add only people who should see that client's matters (user action)
3. Create `[Company]_GC_Agent` in the new team; write AGENT.md from
   templates/AGENT_TEMPLATE.md (COMPANY CONFIGURATION filled, SHARED
   INFRASTRUCTURE pasted verbatim)
4. Create `[Company]_Legal_Privileged` in the new team per the
   client-lookup-agent pattern
5. Connect the client's accounts as TEAM-LEVEL connectors (Drive, plus
   Slack if the client-facing agent will live in the client's workspace)
6. Bind team-level secrets: PERPLEXITY_API_KEY, CHUTES_API_KEY, Browserbase
   keys, any client-specific credentials
7. Knowledge sources: full client Drive folder on the GC agent; curated
   non-privileged subset only on the client-facing agent
8. Create a new Perplexity project for the client; new Browserbase persistent
   context; pplx_config.json on the GC agent; Browserbase navigation MCP rule
   scoped to the client project
9. Install skills from the repo (current VERSION) on the GC agent; minimal
   surface on the client-facing agent
10. Connect research servers on the GC agent (Midpage, Browserbase, Exa,
    Firecrawl, tax tools); no Legal Ops monitoring feeds on any GC agent
11. Create the repo sync schedule on the GC agent
12. Test: test email to both agents; test redline on the GC agent (must ask
    for author name, must produce word-level tracked changes); isolation test
    (only this client's connectors and credentials visible); privilege test
    (client-facing agent escalates rather than answers privileged questions)

## Data Isolation Guarantees

| Resource | Isolation mechanism |
|----------|--------------------|
| Team connectors | Team-scoped; credentials exist only in the client team |
| Secrets | Team-scoped, injected only into that team's agents |
| Sandbox filesystem | Per-agent, no cross-agent access |
| Workspace files | Per-agent /home/user/.workspace/agent/ |
| Knowledge base | Per-agent sources; client-facing agent restricted to non-privileged subset |
| Perplexity project | Separate project URL + separate Browserbase context per client |
| Vector store | Per-agent doc_rag_store directory |
| Email inbox | Unique @gumloopagents.com address per agent |
| Conversation history | Per-agent, searchable only within that agent |

## What NEVER Crosses Team Boundaries

- Document contents (contracts, memos, cap tables)
- Perplexity thread contents
- Vector store embeddings
- Knowledge base search results
- Email contents
- Credentials/secrets
- Conversation history
- Client identity itself, where disclosure would be adverse

## What IS Shared (firm layer only)

- The GitHub repo (skills, templates, scripts, clause library)
- The Legal Ops agent
- The CTO agent
- Skill scripts (no company data in them)
- Methodology reference (generic legal analysis patterns)
- Style rules (Ben's voice applies to all his clients)
- Docx formatting and redlining methodology
- LLM routing configuration (Chutes-first; CHUTES_API_KEY is firm
  infrastructure, reused across teams with team-scoped bindings)
- Sync schedules
