---
name: gc-agent-sources
description: Use when connecting, auditing, or expanding the data sources available to a company GC agent (Molecule_GC_Agent, Chutes_GC_Agent, or any new company GC). Defines the research-tool surface every GC agent needs, the client-specific connectors each GC holds for its own company only, and the monitoring feeds that must never be connected to a GC.
---

# GC Agent Source Configuration

Known GC agents: Molecule_GC_Agent (https://www.gumloop.com/agents/qFb8CuAd8vbKUbBWXZvyBh), the Molecule company GC formerly named Molecule_Legal_Privileged; Chutes_GC_Agent (https://www.gumloop.com/agents/gWFwHxE4rrdUuXinu8BbjS), the Chutes company GC formerly named Chutes_Legal_Privileged. Note: a separate new agent named Chutes_Legal_Privileged (https://www.gumloop.com/agents/2Hncte2BviCDkzH9VJoj53) is the client-facing self-service agent used directly by Chutes employees; configure that one per the client-lookup-agent skill, not this file.

A company GC agent is the client of the Juvor virtual law firm. It holds all client context and privilege. Its source surface is live legal research tools plus its own company's connectors. It never holds monitoring feeds — currency arrives through the specialist skills maintained by Juvor Legal Ops.

## Required Connections (every GC agent)

### MCP servers

| Server | Purpose |
|---|---|
| midpage | Case law, statutes, regulations, dockets; verify currency live when needed |
| tax app tools (app__*) | IRC, regs, IRS guidance, Tax Court |
| patent_connector | Patents, trademarks, PTAB, MPEP/TMEP |
| exa | Web/news discovery for non-legal facts |
| firecrawl | Reading specific pages (counterparty sites, agency pages) |

### Secrets

| Secret | Purpose |
|---|---|
| CHUTES_API_KEY | All LLM synthesis, drafting, and sanitization work |

## Client-Specific Connectors (per GC agent, its own company only)

Connect only what that company's work requires, and only that company's accounts:

| Connector | Typical use |
|---|---|
| agentmail | ALL agent email, both send and receive. Each GC agent gets its own AgentMail inbox (e.g. molecule-gc@agentmail.to). Outbound mail goes through agentmail__send so the From address is the agent's own inbox, and inbound replies arrive in that inbox and are read with the agentmail list/read tools or an inbound webhook trigger. Never use the Gmail/Outlook connectors or the Gumloop native email channel for agent-to-user mail, because those send from the user's own address and replies cannot route back to the agent. |
| gdrive | The company's own document folders |
| slack or teams | The company's own channels |
| gcalendar | The company's own calendar |
| airtable / notion | The company's own matter or contract tracking |

Gmail or Outlook connectors may still be connected only when the GC must read or search the company's own mailbox history. They are never used to send agent mail.

A GC agent's client connectors are configured per company at setup. No GC agent ever connects to another company's accounts, and no connector is shared between GC agents.

## Prohibited Connections (every GC agent)

Never connect to a GC agent:

- Monitoring feeds: Congress.gov, CourtListener, Federal Register, SEC/IRS RSS. These belong to Legal Ops. Currency reaches the GC through the specialist skills' current-developments files.
- Other companies' data sources of any kind.
- Legal Ops' changelog archive.

If a GC suspects a legal development the specialist skill has not yet captured, it verifies the point live through midpage and flags the gap to the user for Legal Ops' next cycle. It does not acquire its own feed.

## Specialist Skills

GC agents load specialist practice skills (corporate-vc-finance, and later securities, tax, labor-employment, privacy, IP, AI regulation) for domain expertise. Skills are read-only expertise: a GC never writes to a skill directory. Skill updates come only from Legal Ops.

## Daily Skill Sync (3:45 AM local)

Each GC agent runs `scripts/sync_skills.py` (in this skill) on a daily schedule at 3:45 AM local, after the Legal Ops cycle commits. The script pulls the managed skills from Juvorai/legal-agent-infrastructure main into /home/user/skills/, overwriting only files whose content hash changed, and writes a receipt to /home/user/.workspace/agent/skill-sync-receipt.json with the repo commit SHA, per-file update counts, and any errors. The CTO daily evaluation reads the receipt to verify the sync; a missing receipt or a receipt older than 26 hours on a weekday is a sync failure. The sync never touches client connectors, client files, or local-only skills.

## Quarterly Audit

Once per quarter, list the GC agent's actual connected servers and secrets and diff against this file. Confirm: research tools present, exactly one company's client connectors, zero monitoring feeds. Report discrepancies to the user. Done when the live configuration matches this file exactly.
