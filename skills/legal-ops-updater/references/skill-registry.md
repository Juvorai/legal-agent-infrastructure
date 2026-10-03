# Specialist Skill Registry

The practice-group skills Legal Ops maintains. Each entry: skill directory, domain, update cadence, and status. Register a skill here before its first update cycle.

| Skill | Domain | Cadence | Status |
|---|---|---|---|
| corporate-vc-finance | Delaware corporate law, VC financing, governance, M&A | Weekly (Monday) | Active |
| securities-capital-markets | Reg D/S/CF, exempt offerings, token offerings, blue sky | Weekly (Tuesday) | Active |
| tax-federal-international | IRC, credits, QSBS, 409A, state nexus, cross-border | Weekly (Wednesday) | Active |
| labor-employment | Multi-state employment, classification, equity comp, immigration | Weekly (Thursday) | Active |
| privacy-data | State privacy laws, GDPR, cross-border transfers | Weekly (Friday) | Active |
| ip-patent-trademark | Patents, trademarks, trade secrets, OSS licensing | Biweekly (alternate Mondays) | Active |
| ai-emerging-tech-reg | EU AI Act, state AI laws, NIST frameworks | Biweekly (alternate Fridays) | Active |

Activated 2026-10-03 per user approval. Weekday-only cycles; weekends are no-cycle days by design.

## Update Target Convention

Each skill keeps:
- `references/current-developments.md` — dated, appended updates. The only file Stage 5 auto-merge writes.
- `references/CHANGELOG.md` — one line per merge; header stores the last cycle date. The rollback index.
- `references/last-run.json` — one JSON line per cycle (heartbeat). The CTO daily evaluation reads this first.
- Doctrine files (checklists, frameworks) — edited only through the flagged-review path, never auto-merged.

## Confidentiality Invariant

Every skill in this registry contains only public legal authority and methodology. No client names, matters, facts, or work product. The quarterly leak audit enforces this.
