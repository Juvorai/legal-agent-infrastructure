# Frameworks Reference — Private Tech Financial Analysis

Use this file when a run needs precise definitions or formula detail. Keep SKILL.md lean; pull from here on demand.

## Unit economics

| Metric | Formula / definition | Notes |
|---|---|---|
| **CAC** | Sales & marketing spend attributable to new customers ÷ new customers acquired in period | Specify paid vs blended; match spend period to cohort lag |
| **LTV** | Contribution margin per customer over expected life (e.g. ARPU × gross margin × lifetime months), or discounted cash contribution | State churn and margin assumptions; logo vs revenue LTV |
| **LTV:CAC** | LTV ÷ CAC | Context-dependent; >3x often cited for healthy SaaS, not a law |
| **Gross margin** | (Revenue − COGS) ÷ Revenue | SaaS COGS usually hosting, support, third-party usage; flag if R&D is stuffed into COGS or vice versa |
| **Payback (months)** | CAC ÷ (monthly contribution margin per customer) | Cash payback preferred over accounting profit |

## Growth efficiency

| Metric | Formula / definition | Notes |
|---|---|---|
| **Rule of 40** | Revenue growth rate (%) + profit margin (%) | Often growth + FCF margin or EBITDA; state which margin |
| **Magic Number** | Net new ARR in period ÷ prior-period S&M spend | ~0.5–1.0+ bands are common heuristics, not truth |
| **NRR / NDR** | (Starting ARR + expansion − contraction − churn) ÷ Starting ARR | Logo retention is different; do not conflate |
| **Burn multiple** | Net burn ÷ Net new ARR | Lower is more efficient; rising burn multiple with slowing growth is a red flag |

## Liquidity / runway

```
Net Monthly Burn = Cash operating outflows − Cash operating inflows (exclude financing)
Runway (months) = Cash Balance ÷ Net Monthly Burn
```

- Use **cash** burn, not accounting net loss, when the question is survival.
- Scenario runway: flat burn, +20% burn, and path-to-breakeven cases.
- Flag if "burn" is GAAP loss including SBC (non-cash) without reconciliation to cash.

## Valuation

### Multiples

```
Equity value (approx) = ARR (or Revenue) × Selected multiple
```

- State trailing vs forward ARR/revenue.
- Adjust for growth, margin, NRR, and market regime before applying a peer median blindly.
- Private rounds: clarify **pre-money** vs **post-money**.  
  `Post-money = Pre-money + New primary capital` (watch option pool shuffle: pool top-up often comes from pre-money and dilutes existing holders).

### Comps and precedents

- Separate **public trading comps**, **private round comps**, and **M&A precedents**.
- Normalize fiscal periods, one-time revenue, and different ARR definitions before ranking multiples.
- Prefer a range and a selected point with rationale over a single "the" multiple.

### Dilution / waterfall (new round)

For a priced round, track at minimum:

1. Pre-round fully diluted shares (incl. option pool, convertibles as-converted if treating as converted)
2. New shares issued = New capital ÷ Price per share
3. Post-round ownership % by class
4. Option pool refresh (pre- or post-money) and who absorbs it
5. Preference stack for exit waterfall (seniority, multiple, participating vs non-participating)

SAFE / convertible notes: show conversion price (discount and/or valuation cap), resulting shares, and interaction with the priced round.

## Capital structure terms (quick defs)

- **Liquidation preference:** amount preferred gets before common on exit (e.g. 1x non-participating).
- **Participating preferred:** preferred takes preference, then shares pro rata with common in the residual (often capped).
- **Non-participating:** preferred chooses preference **or** as-converted common, not both.
- **Pro-rata rights:** right to buy enough of a future round to maintain ownership %.
- **Waterfall:** ordered distribution of exit proceeds by seniority and terms.

## Red flags checklist

- Customer or revenue concentration (top 1 / top 10 %)
- Deferred revenue growth diverging from cash collections or billings
- Related-party revenue, loans, or expense recharges
- Aggressive non-GAAP add-backs (especially "one-time" that recur)
- Headcount or opex growth outpacing revenue / ARR for multiple periods
- ARR definitions that double-count multi-year deals or include non-recurring professional services
- Runway quoted on gross burn while ignoring committed cash outflows (leases, earnouts)
- Cap table missing outstanding SAFEs, notes, warrants, or promised option grants

## Method selection notes

| Question | Default method | Alternative |
|---|---|---|
| "What is it worth?" (growth SaaS, limited profits) | Forward/trailing ARR multiple vs comps | DCF if cash flows predictable; secondary/primary round marks as cross-check |
| "How long can they operate?" | Cash runway scenarios | Path-to-breakeven months under hiring plan |
| "Is growth efficient?" | Burn multiple + Magic Number + NRR | Rule of 40 for later-stage |
| "What do I own after the round?" | Fully diluted cap table + pool shuffle | As-converted vs outstanding-only views, both labeled |

When methods disagree materially, show both and explain the driver of the gap.