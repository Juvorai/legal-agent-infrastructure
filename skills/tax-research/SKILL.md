# tax-research

Guides professional tax research using the connected tax-law MCP tools (app__* server). Activates when the user asks tax-related questions; references IRC sections, Treasury Regulations, IRS publications, or revenue rulings; discusses tax planning strategies; analyzes client tax scenarios; or mentions tax research, tax code, or IRS. Use this skill whenever conducting tax law research, even if the user doesn't explicitly mention the tools.

## Available Tools

| Tool | Purpose |
|------|---------|
| `app__search-tax-law-tool` | Search across all tax law sources (IRC, regs, rulings, cases) |
| `app__lookup-section-tool` | Look up a specific IRC section by number |
| `app__get-publication-tool` | Retrieve an IRS publication by number |
| `app__get-ruling-tool` | Retrieve a revenue ruling or procedure |
| `app__get-case-tool` | Retrieve a Tax Court case |

## Research Methodology

### Step 1: Identify the Code Section

Start with the relevant IRC section. Use `app__lookup-section-tool` for known sections, or `app__search-tax-law-tool` for topic searches.

### Step 2: Check Treasury Regulations

For every IRC section cited, check the corresponding Treasury Regulation. Regulations provide the operative rules and examples.

### Step 3: Check IRS Guidance

Look for:
- Revenue Rulings (Rev. Rul.)
- Revenue Procedures (Rev. Proc.)
- IRS Publications
- Private Letter Rulings (PLR) - note these are taxpayer-specific
- Notices and Announcements

### Step 4: Check Case Law

Tax Court and other court decisions interpreting the relevant provisions.

### Step 5: Verify Currency

Tax law changes frequently. Verify:
- Is the section still in effect?
- Have regulations been updated?
- Are there pending legislative changes?

## Citation Format

- IRC: I.R.C. § Section
- Treasury Regulations: Treas. Reg. § Section
- Revenue Rulings: Rev. Rul. Year-Number, Year-Week I.R.B. Page
- Revenue Procedures: Rev. Proc. Year-Number, Year-Week I.R.B. Page
- Tax Court: *Name v. Commissioner*, Volume T.C. Page (Year)
- IRS Publications: IRS Pub. Number, Title (Year)

## Common Research Topics

| Topic | Starting Point |
|-------|---------------|
| 83(b) elections | I.R.C. § 83(b); Treas. Reg. § 1.83-1 |
| 409A valuation | I.R.C. § 409A; Treas. Reg. § 1.409A-1 |
| QSBS (1202) | I.R.C. § 1202 |
| Token taxation | IRS Notice 2014-21; Rev. Rul. 2019-24 |
| S corp eligibility | I.R.C. § 1361 |
| Partnership allocations | I.R.C. § 704(b) |
| Foreign tax credit | I.R.C. § 901-904 |
| R&D credits | I.R.C. § 41 |
