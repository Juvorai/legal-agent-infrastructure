# ASD-STE100 Simplified Technical English — clarity reference

Source: https://www.asd-ste100.org/ (official site of the ASD Simplified Technical English Maintenance Group, STEMG). Current release: Issue 9, January 15, 2025, the first issued as an international standard ("Standard for Technical Documentation"). Referenced in ISO 24620-4:2023 and required or recommended by ATA iSpec 2200, S1000D, EASA, FAA, and CAAC for technical documentation.

Rule tables, modes, process, and output format below are adapted from the open-source `asd-ste100` skill (https://github.com/danyuchn/asd-ste100-skill, MIT license), which encodes the rule categories of Issue 9 without reproducing the proprietary dictionary.

## What it is

STE is a controlled natural language built to make technical text unambiguous for readers who do not have English as a first language. It has two parts:

1. **Writing rules.** 53 rules in 9 sections covering word choice, grammar, sentence structure, and style.
2. **Controlled dictionary.** Roughly 900 approved words, each with one meaning and one part of speech, plus roughly 1,200 non-approved words with approved alternatives. Company or subject-specific terms are allowed as "technical nouns" and "technical verbs" under their own rules.

## Why it matters for this skill

STE is the strongest published antidote to AI-flavored prose. Its core disciplines map directly onto the anti-AI module:

- **One word, one meaning.** Never use a synonym for variety. If "use" is the word, do not rotate through "utilize," "leverage," "employ," and "harness." AI prose rotates synonyms; STE forbids it.
- **Approved vocabulary only.** Prefer the short, common word over the decorative one. This is the same instinct as the banned-words list, systematized.
- **Short sentences, one instruction each.** STE caps sentence length and forbids stacking multiple actions or conditions in one sentence. Break long AI-style compound sentences into separate ones.
- **Active voice, imperative for instructions.** "Remove the bolt," not "the bolt should be removed."
- **No ambiguity in verb forms.** Use the base verb; avoid nominalizations ("perform an installation of" becomes "install").
- **Explicit articles and connectors.** Do not drop "the" or "that" where omission creates parsing ambiguity, a habit AI text shares with telegraphic jargon.
- **Warnings and conditions come first.** Put the condition or caution before the action, so the reader never acts on incomplete information.

## How to apply it here

Use STE as a cross-check, not a straitjacket. Ben's voice governs register and rhythm; STE governs clarity of mechanism. When a sentence in a deliverable could be read two ways, or when a paragraph piles clauses into one long sentence, apply the STE discipline: one idea per sentence, the common word, active voice, conditions first. The full rule set and dictionary are in the official Issue 9 document, available free on request from the site above.

## Source and scope (dictionary limits)

This reference encodes the **rule categories** of ASD-STE100 Issue 9 (Jan 2025): 53 writing rules across 9 sections, backed by a dictionary of ~900 approved words and ~1,200 words to avoid. See `ste100_writing_rules.md` in this directory for the fuller rule summary and citations.

It does **not** reproduce ASD's ~900-word approved dictionary verbatim. ASD-STE100 is free to obtain but not free to redistribute: Issue 9, page 2 states that "no reproduction or publication of it, in whole or in part, shall be made without the written authority of an officer of ASD," and grants free reproduction rights only to eight listed categories. Apply the *underlying principle* (pick the plainest, most common word available and use it the same way every time) rather than checking against a fixed word list. When exact ASD-approved wording matters, request the standard from the [official downloads page](https://www.asd-ste100.org/STE_downloads.html).

## Two modes

Pick a mode before rewriting. If the user does not say which, infer it from the text type.

**Strict** — procedures, error messages, tool and function descriptions, inter-agent instructions, safety text. Anywhere a wrong reading has a cost. Apply every rule below, including the hard length caps and one-word-one-meaning discipline.

**STE-flavored** — READMEs, PR descriptions, changelogs, explanatory prose. Apply the structural rules in full and treat the lexical rules as advisory: keep the sentence length caps, active voice, simple tenses, no phrasal verbs, no semicolons, no nominalization and no marketing adjectives, while dropping the one-word-one-meaning lockdown. A strict rewrite of prose reads as a personality transplant rather than a clarification.

## Core rewrite rules

STE's rules divide into two kinds. **Structural rules** are self-contained: they describe sentence shape, and you can apply them from the description alone. **Lexical rules** are defined entirely by the official ~900-word dictionary, which this reference deliberately does not reproduce. Without that dictionary, the lexical rules degrade from a checkable standard into a preference for plain words.

Apply the structural rules with confidence. Apply the lexical rules as a direction of travel, and say so rather than implying dictionary compliance you cannot verify.

### Structural rules — apply these

| Rule | Do | Don't |
|---|---|---|
| Active voice | "The agent deletes the file." | "The file is deleted (by the agent)." — unless the actor is genuinely unknown or irrelevant |
| No phrasal verbs (Rule 9.3) | "Remove the panel." / "Start the job." | "Take off the panel." / "Spin up the job." — a two-word verb has meanings the parts do not predict |
| One instruction per sentence | "Open the file. Read line 3." | "Open the file and read line 3, then check if it matches." |
| Sentence length | ≤20 words for instructions/procedures, ≤25 words for descriptions | Long compound/subordinate-clause sentences |
| No semicolons (Rule 8.1) | Split into separate sentences | Any semicolon at all — STE bans the mark outright. (The em dash is *not* banned by STE, though it often signals a sentence that should be split. Note: this skill's own standing rules already ban dashes as punctuation, which is stricter than STE.) |
| Noun clusters | ≤3 words stacked as a noun phrase ("fuel pump valve") | 4+ word noun stacks ("high pressure fuel pump inlet valve assembly") |
| No ellipsis | Keep the subject, verb, and article explicit even if it reads longer | Drop words to save space ("Files not backed up will be lost" → ambiguous which files) |
| Keep modality | "The request **may have** failed." stays "may have" | Promote a hedge to a fact ("The request failed.") or invent a certainty the source did not state |
| Paragraph limits | One topic per paragraph, ≤6 sentences | Multi-topic paragraphs |
| Lists for sequences | Use a numbered or bulleted list for 3+ steps or conditions | Bury a sequence inside one prose sentence |

### Lexical rules — direction of travel only

| Rule | Do | Don't | Why it is weaker here |
|---|---|---|---|
| One word, one meaning | Pick one verb for one action and reuse it every time (e.g. always "check", never mix "check"/"verify"/"confirm" for the same action) | Rotate synonyms for the same idea across a document | Consistency within a document is checkable. Which word is the *approved* one is not, without the dictionary. |
| One part of speech per word | "Apply oil to the valve" (oil = noun) | "Oil the valve" (oil = verb) | Whether "oil" is approved as a noun only is a dictionary fact. Prefer the noun form when both read equally well. Do not claim compliance. |
| Verb, not noun (Rule 3.7) | "Analyze the log." | "Perform an analysis of the log." — a noun form of an action makes the sentence longer and hides who acts | Rule 3.7 says "use an **approved** verb to describe an action." Preferring the verb form is safe to apply anywhere. Knowing which verb is the approved one needs the dictionary. |
| Domain terms | Keep necessary technical nouns/verbs, but define them once if not common English (STE allows a project-specific glossary beyond its base dictionary) | Use jargon without ever defining it | The glossary allowance is real STE, but the base dictionary it extends is absent. |

### Simple tenses — apply with one exception

STE permits infinitive, imperative, simple present, simple past, simple future, and past participle as adjective. It excludes present perfect and other compound forms: "we received the report", not "we have received the report".

Aircraft manuals never need present perfect, so the exclusion costs the standard nothing. Other text is not always so lucky. "The job has completed" (and its output is available now) and "the job completed" (at some past point) are different statements, and status text frequently needs the first. **Where the compound form carries information the simple form loses, keep it and say why.** Otherwise prefer the simple form.

## Scan checklist — six habits that make text hard to parse

Each one is mechanical: you can point at the exact word or punctuation mark that breaks the rule, with no judgment call. Scan for all six before you rewrite anything.

1. **Synonym rotation** — the same thing gets several names in one document ("the user", "the customer", "the client"). Fix: pick one name, use it every time.
2. **Hedge stacking** — helper verbs and qualifiers pile up until the sentence asserts nothing ("it is important to note that this may potentially help to improve"). Fix: state the claim, or delete it.
3. **Nominalization** — an action frozen into a noun ("perform an analysis of", "provides assistance to"). Fix: use the verb ("analyze", "helps").
4. **Marketing adjectives** — words that claim quality instead of showing it: seamless, robust, powerful, cutting-edge, effortless, blazing-fast. Fix: delete, or replace with the measurement that earns the claim.
5. **Run-on sentences** — several ideas joined by semicolons or em dashes. Fix: one idea per sentence.
6. **Soft phrasal verbs** — spin up, reach out, dive into, kick off. Fix: use the single plain verb (start, contact, read, begin).

## Process

1. Pick the mode (Strict or STE-flavored).
2. Read the input text once for meaning — do not start rewriting before you understand what it must still say afterward.
3. Walk it sentence by sentence. Flag every rule violation from the Core Rewrite Rules tables and every habit from the Scan Checklist. In STE-flavored mode, flag the lexical rules but do not enforce them. For a mechanical first pass over the structural rules, run `scripts/ste_lint.py` (stdin or file args, `--json` for structured output); it checks semicolons, sentence length, phrasal verbs, nominalization, noun clusters, and synonym rotation.
4. Rewrite. Preserve every fact, condition, and scope qualifier. Preserve the strength of every hedge. When a longer phrasing carries precision the short one loses, keep the longer one.
5. Re-scan the rewrite. New violations creep in during step 4.

## Output format

**Default: the rewritten text, and nothing else.** Do not add a preamble, a mode announcement, a violation count, a summary of what changed, a rule table, or a closing offer to explain further.

The one permitted addition: if step 4 kept a longer phrasing on purpose, add a single line after the text, prefixed `Kept as-is:`, naming the phrase and the precision that would have been lost.

**On request: the rule table.** When the user asks to see the reasoning ("show the diff", "which rules did it break", "before/after"), output this table instead:

```markdown
| Rule violated | Original | Simplified |
|---|---|---|
| Present perfect tense | "We have received your request." | "We received your request." |
| Noun cluster (4+ words) | "the agent task queue priority handler" | "the handler that sets task-queue priority" |

Mode: Strict. 7 violations found.
```

Follow the table with a one-line note on anything you deliberately did **not** simplify, and why (usually: simplifying would lose required precision).

## Boundaries

**Will:**
- Rewrite ambiguous or dense English into short, single-meaning, active-voice sentences.
- Preserve every fact, condition, and scope qualifier in the original.
- Preserve the strength of every hedge, and add no claim the source did not make.
- Suggest a one-line glossary entry for domain terms that must stay.

**Will not:**
- Reproduce ASD's official ~900-word dictionary as if it were memorized verbatim.
- Simplify creative, marketing, or persuasive copy where voice and nuance are the point. In this skill, Ben's voice always governs register; STE only governs clarity of mechanism.
- Silently drop a safety condition, exception, or scope qualifier to shorten a sentence — flag the trade-off instead.
- Convert "may have failed" into "failed", or "could be caused by X" into "X is the cause" — losing a hedge changes the claim.
- Guarantee an aerospace/defense-grade STE-compliant document. This is a general-purpose clarity tool inspired by STE, not a certified STE authoring tool.
- Make weak content true or useful. STE fixes the *form* of a text, not its substance.
- Shorten past the point of clarity. Removing ambiguity is the goal, not cutting words. Stop when the sentence is unambiguous, not when it is shortest.

## Additional resources in this skill

- **`references/ste100_writing_rules.md`** — fuller summary of the 9 rule sections and dictionary structure, with citations to the official standard and secondary sources.
- **`examples/ste100_before_after.md`** — worked examples, including official STE examples and agent-output examples.
- **`scripts/ste_lint.py`** — deterministic, stdlib-only linter for the structural rules, including dangling-conjunction in supported list items, plus a synonym-rotation check scoped per file. Exit 1 when hard violations exceed `--baseline` (default 0); advisory findings (passive voice, compound tenses) never fail the run; `--disable` silences named rules. It never flags hedges or modality: those are content, not style, and `--selftest` asserts that "may have failed" passes clean.
