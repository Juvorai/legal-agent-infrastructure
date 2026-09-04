#!/usr/bin/env python3
"""bluebook_ref.py — quick-reference for common Bluebook (22nd ed.) citation formats.

Usage:
    python3 bluebook_ref.py [topic]
Topics: cases, statutes, constitutions, regulations, books, articles,
        internet, signals, short-forms, abbreviations, treasury-regs,
        irc, rev-rul, rev-proc, notices, plr, treaties, tax-court, all
"""
import sys

REFS = {
"cases": """CASES (R10 / B10)
  Full:    *Case Name*, Vol. Reporter Page, Pincite (Court Year).
           United States v. Windsor, 570 U.S. 744, 759 (2013).
  Court:   omit for U.S. Supreme Court; include for others:
           (2d Cir. 2020) | (S.D.N.Y. 2019) | (Cal. 2018)
  Later:   aff'd, rev'd, cert. denied as parentheticals.
  Short:   Windsor, 570 U.S. at 759.   |   Id. at 760.
  Always pincite. Italicize case names.""",

"statutes": """STATUTES (R12 / B12)
  U.S.C.:  26 U.S.C. § 501(c)(3) (2018).
  Multi:   §§ 501(c)(3), 509(a)(1).
  State:   official state format, e.g. N.Y. Gen. Bus. Law § 349 (McKinney 2020).
  Session: 88 Stat. 1234 (when code cite unavailable).
  Short:   § 501(c)(3).   |   id.""",

"constitutions": """CONSTITUTIONS (R11)
  U.S. Const. art. I, § 8, cl. 3.
  U.S. Const. amend. XIV, § 1.
  No year while in force; parenthetical year if repealed/superseded.""",

"regulations": """REGULATIONS (R14)
  C.F.R.:  26 C.F.R. § 1.501(c)(3)-1 (2023).
  Fed.Reg: 88 Fed. Reg. 12,345 (Mar. 1, 2023) (to be codified at 26 C.F.R. pt. 1).""",

"books": """BOOKS (R15)
  Full:    Author, *Title* Pincite (ed. Publisher Year).
           Bryan A. Garner, The Chicago Guide to Grammar, Usage,
           and Punctuation 55 (Univ. of Chi. Press 2016).
  Short:   Garner, supra note 3, at 60.""",

"articles": """PERIODICALS (R16)
  Full:    Author, *Title*, Vol. Journal FirstPage, Pincite (Year).
           John F. Coverdale, Textualism's Gaze, 85 Fordham L. Rev. 2029, 2035 (2017).
  Journal abbreviations per T13/T6. Consecutively paginated: no issue no.
  Short:   Coverdale, supra note 5, at 2036.""",

"internet": """INTERNET (R18)
  Author, *Title*, Site Name (last visited July 30, 2026), https://url.
  Undated content requires 'last visited' parenthetical.
  Archive URLs where possible (Perma.cc / archive.org).""",

"signals": """SIGNALS (R1.2)
  [no signal]  directly states the proposition
  See          clearly supports, does not directly state
  See also     additional supporting authority
  Cf.          analogous; comparison illuminates
  Compare...with...  juxtaposition instructive
  Contra       direct contradiction
  But see      clearly contradicts / different result
  But cf.      analogously contrary
  See generally    helpful background
  Order per R1.3-1.4; string cites separated by semicolons.""",

"short-forms": """SHORT FORMS (R4)
  Id.        immediately preceding cite, one authority only.
  Id. at 55. same source, new pincite.
  Supra      books/articles/other non-case material: Author, supra note 3, at 60.
  Never supra for cases/statutes/constitutions — use their short forms.
  Avoid 'infra' in court documents; say 'below' in text.""",

"abbreviations": """ABBREVIATIONS (T6 / T10 / T1 / B7)
  Case names: Ass'n, Corp., Nat'l, Int'l, Bhd., Comm'n, Univ.
  Geography per T10: Cal., N.Y., N.J. (not in case names w/ states per rule).
  Courts: 2d Cir., S.D.N.Y., D.N.J., Cal. App.
  Months: Jan. Feb. Mar. Apr. May June July Aug. Sept. Oct. Nov. Dec.
  Capitalization per R8; spacing: single-letter initials closed up (S.D.N.Y.),
  multi-letter abbreviations spaced from numbers (F. Supp. 3d, L. Rev.).""",

"treasury-regs": """TREASURY REGULATIONS (R14)
  Final:     26 C.F.R. § 1.368-2(b) (2023).
             C.F.R. title equals I.R.C. title for income-tax regs.
  Temporary: 26 C.F.R. § 1.469-5T(a) (2022).  ['T' suffix; note T.D. on first cite]
             T.D. 10001, 89 Fed. Reg. 84,672 (Oct. 22, 2024).
  Proposed:  Prop. Treas. Reg. § 1.163(j)-1, 83 Fed. Reg. 67,490 (Dec. 28, 2018).
  Tax-practice shorthand after first full cite: Treas. Reg. § 1.368-2(b).
  Court documents: use C.F.R. per Bluepages.""",

"irc": """INTERNAL REVENUE CODE (R12.9.1)
  I.R.C. § 368(a)(1)(A) (2018).
  In tax memoranda/articles, 'I.R.C. §' replaces '26 U.S.C. §' per tax convention;
  in court filings use 26 U.S.C. §.
  Subsection chains run without spaces: § 704(b)(2)(B)(ii).""",

"rev-rul": """REVENUE RULINGS
  Pre-2000:    Rev. Rul. 59-60, 1959-1 C.B. 237.        [Cumulative Bulletin]
  2000-on:     Rev. Rul. 2023-2, I.R.B. 2023-16, 658.   [weekly Internal Revenue Bulletin]
  Short form:  Rev. Rul. 59-60, supra.""",

"rev-proc": """REVENUE PROCEDURES
  Rev. Proc. 87-56, 1987-2 C.B. 674.
  Rev. Proc. 2024-40, I.R.B. 2024-45, 1100.""",

"notices": """NOTICES AND ANNOUNCEMENTS
  Notice 2020-51, I.R.B. 2020-29, 59.
  Announcement 2023-5, I.R.B. 2023-12, 996.""",

"plr": """PRIVATE LETTER RULINGS / TAMs / CCAs / FSAs (R14.5.3)
  Priv. Ltr. Rul. 201234007 (Aug. 24, 2012).
       Number = year + week + sequence; include release-date parenthetical.
  Tech. Adv. Mem. 202310001 (Mar. 10, 2023).
  Chief Couns. Adv. Mem. 202118008 (May 7, 2021).
  ALWAYS flag § 6110(k)(3): PLRs bind the Service only as to their taxpayer
  and carry no precedential force — cite as evidence of the Service's
  reasoning, never as authority for the proposition.""",

"treaties": """TAX TREATIES (R21.4)
  Convention for the Avoidance of Double Taxation and the Prevention of
  Fiscal Evasion with Respect to Taxes on Income and Capital Gains,
  U.S.–U.K., art. 7, July 24, 2001, T.I.A.S. No. 03-331.
  Protocols: cite as amendments to the parent convention w/ own signing dates.
  Models: U.S. Model Income Tax Convention (2016);
          OECD Model Tax Convention on Income and on Capital (2017),
          Commentary on art. 7, para. 32 (2017).
  Technical Explanations cite as Treasury documents accompanying the treaty.""",

"tax-court": """TAX COURT & FEDERAL TAX COURTS (R10 / B10, T1)
  Tax Court regular:   Grecian Magnesite Mining v. Comm'r, 149 T.C. 63 (2017).
  Tax Court memo:      Est. of Smith v. Comm'r, T.C. Memo. 2019-101.
  Summary opinions:    T.C. Summ. Op. 2020-12  [reasoning only, not precedent, Rule 50(f)]
  Court of Fed. Claims: Barnes v. United States, 152 Fed. Cl. 1 (2021).
  Refund suits also in district courts per 28 U.S.C. § 1346(a)(1).""",
}

def main():
    topic = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    print("BLUEBOOK QUICK REFERENCE (22nd ed.) — Bluepages default for practitioner work")
    print("=" * 68)
    if topic == "all":
        for k in REFS:
            print(REFS[k]); print()
    elif topic in REFS:
        print(REFS[topic])
    else:
        print(f"Unknown topic '{topic}'. Choose from: {', '.join(REFS)} | all")
        sys.exit(1)
    print("\nWhen a point is not covered, the current edition (legalbluebook.com) governs.")

if __name__ == "__main__":
    main()
