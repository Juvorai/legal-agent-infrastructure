#!/usr/bin/env python3
"""
bluebook_ref.py - Bluebook (22nd ed.) citation reference for legal agent deliverables.
Usage: python3 bluebook_ref.py [category]
Categories: cases, statutes, regulations, tax, transactional, all
"""

import sys
import json

REFERENCE = {
    "cases": {
        "format": "*Name v. Name*, Volume Reporter Page (Court Year)",
        "examples": [
            "*Brown v. Board of Education*, 347 U.S. 483 (1954).",
            "*Roe v. Wade*, 410 U.S. 113, 152 (1973).",
            "*United States v. Nixon*, 418 U.S. 683, 707 (1974).",
        ],
        "rules": [
            "Italicize case names in citations.",
            "Include pinpoint page when referencing specific language.",
            "Include court and year in parentheses.",
            "For subsequent history, add: aff'd, rev'd, cert. denied, etc.",
            "No short cites (id., supra) in agent deliverables.",
        ],
    },
    "statutes": {
        "format": "Title Code § Section (Year)",
        "examples": [
            "15 U.S.C. § 78j(b) (2024).",
            "17 C.F.R. § 240.10b-5 (2024).",
            "Del. Code Ann. tit. 8, § 141 (2024).",
        ],
        "rules": [
            "Use official code abbreviation.",
            "Include year of code edition.",
            "For state statutes, include state abbreviation.",
            "Hyperlink to official source.",
        ],
    },
    "regulations": {
        "format": "Title C.F.R. § Section (Year)",
        "examples": [
            "17 C.F.R. § 230.506 (2024).",
            "26 C.F.R. § 1.83-1(a) (2024).",
        ],
        "rules": [
            "Include year of C.F.R. edition.",
            "For proposed rules, note 'proposed' status.",
        ],
    },
    "tax": {
        "format": "I.R.C. § Section; Treas. Reg. § Section",
        "examples": [
            "I.R.C. § 83(b).",
            "I.R.C. § 409A(a)(2)(A)(i).",
            "Treas. Reg. § 1.83-1(a)(1).",
            "Rev. Rul. 2024-15, 2024-30 I.R.B. 1.",
            "IRS Priv. Ltr. Rul. 2024-01-001 (Jan. 5, 2024).",
        ],
        "rules": [
            "Use I.R.C. for Internal Revenue Code sections.",
            "Use Treas. Reg. for Treasury Regulations.",
            "Revenue Rulings: Rev. Rul. Year-Number, Year-Week I.R.B. Page.",
            "Private Letter Rulings: IRS Priv. Ltr. Rul. Year-Week-Number (Date).",
            "Tax Court: *Name v. Commissioner*, Volume T.C. Page (Year).",
        ],
    },
    "transactional": {
        "format": "Document-specific citation formats",
        "examples": [
            "Master Services Agreement § 12.3 (2024).",
            "Amended and Restated Certificate of Incorporation art. IV, § 2.",
            "Form of Indemnification Agreement (Exhibit 10.1 to Registration Statement on Form S-1).",
        ],
        "rules": [
            "For contracts: cite by section number and document title.",
            "For charter documents: cite by article and section.",
            "For SEC exhibits: cite exhibit number and filing.",
            "EDGAR filings are market-practice evidence, not legal authority.",
        ],
    },
    "general_rules": [
        "Every legal proposition carries a hyperlinked citation.",
        "No naked citations. No short cites. No invented pin cites.",
        "Midpage deeplinkURL for case law propositions.",
        "Provision URL for statutory propositions.",
        "Distinguish holding from dicta.",
        "Distinguish majority from concurrence or dissent.",
        "Never characterize a non-majority proposition as controlling.",
    ],
}


def main():
    category = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if category == "all":
        print(json.dumps(REFERENCE, indent=2))
    elif category in REFERENCE:
        print(json.dumps(REFERENCE[category], indent=2))
    else:
        print(f"Unknown category: {category}")
        print(f"Available: {', '.join(REFERENCE.keys())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
