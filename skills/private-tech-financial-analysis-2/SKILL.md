# private-tech-financial-analysis-2

Produce solid, concise financial analysis of private technology companies. Use for valuation, burn/runway, unit economics (CAC, LTV, payback), growth efficiency (Rule of 40, Magic Number, burn multiple, NRR), cap table/dilution, round terms, comps, and capital structure. Combines MBA strategy framing, VC diligence, finance rigor, and spreadsheet modeling. Activate on any private tech company financial question, fundraising model, or IC-style memo request.

## Analysis Frameworks

### Unit Economics

| Metric | Formula | Healthy Range (SaaS) |
|--------|---------|---------------------|
| CAC | Sales & Marketing / New Customers | Varies by segment |
| LTV | ARPU × Gross Margin × Avg Lifetime | LTV:CAC > 3:1 |
| Payback Period | CAC / (ARPU × Gross Margin) | < 18 months |
| NRR | (Starting ARR + Expansion - Churn) / Starting ARR | > 120% |
| Gross Margin | (Revenue - COGS) / Revenue | > 70% |

### Growth Efficiency

| Metric | Formula | Healthy Range |
|--------|---------|---------------|
| Rule of 40 | Revenue Growth % + FCF Margin % | > 40% |
| Magic Number | Net New ARR / Prior Quarter S&M | > 0.75 |
| Burn Multiple | Net Burn / Net New ARR | < 2x |
| ARR per Employee | ARR / Headcount | > $200K |

### Valuation Methods

1. **Comparable Companies**: Revenue multiple, growth-adjusted
2. **Precedent Transactions**: Recent rounds in similar companies
3. **DCF**: For later-stage with predictable cash flows
4. **VC Method**: Target return / exit valuation working backward

### Cap Table Analysis

1. **Pre/post money**: Ownership percentages
2. **Dilution waterfall**: Impact on existing holders
3. **Option pool**: Size, refresh timing
4. **Liquidation preferences**: Participation, caps, seniority
5. **Anti-dilution**: Weighted average vs. full ratchet

### Round Terms Assessment

| Term | What to Check |
|------|---------------|
| Valuation | Pre/post money, comparable rounds |
| Liquidation preference | 1x non-participating (market standard) |
| Board composition | Investor seats, independence |
| Protective provisions | Veto rights scope |
| Anti-dilution | Weighted average (broad-based) |
| Pro rata rights | Follow-on participation |
| Information rights | Frequency, scope |
| Drag-along | Threshold, mechanics |

## Output Format

### IC Memo Structure

1. **Company Overview** (2-3 sentences)
2. **Financial Summary** (key metrics table)
3. **Growth Analysis** (trajectory, efficiency)
4. **Unit Economics** (CAC, LTV, payback)
5. **Capital Structure** (cap table, round terms)
6. **Risk Factors** (top 3-5)
7. **Recommendation** (invest/pass with rationale)

### Spreadsheet Modeling

When building models, use the `office-doc-engine` skill for .xlsx output. Include:
- Assumptions tab
- P&L projection
- Cash flow / runway
- Cap table waterfall
- Sensitivity analysis
