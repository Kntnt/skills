# Validation result — v-complete-r3

Fixture: `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/378.scratch/stage/fixture/p2-chronology.md`
Report validated: the checker's report `c-r1`, carried as reply text because the report directory is mode `dr-xr-xr-x` and the file could not be written. It was not saved to the report path for that reason, and the staged tree's permissions were left alone. The route does not settle the comparison: the report ends with its completion status ("Comparison complete") and its unresolved findings, which is the ending the task requires of every report, so it is validated as a complete comparison by that ending and not by its delivery route.
Resolved language of the draft: en_US. Source language of the material: English, so no translation is in play and no translation finding arises.

## 1. Delivery

**This draft is delivered with known defects.** One finding stands unresolved in the prose below, and no fidelity is asserted for the passage it names. The prose is delivered exactly as the comparison read it, unrepaired, and the remaining finding is reported beside it for the editor to settle. A remaining finding is an allegation the editor settles, not an established fact about the text. The one rejected finding below is the writer's evidenced decision, not the checker's approval.

### Remaining finding — September 2025 is stretched over the choice of supplier

- **Draft passage:** "In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair."
- **The concrete problem:** the fronted time adverbial "In September 2025" governs both conjoined predicates, so on the sentence's available reading it dates the choice of Svale Systems, and the testing the choice followed, to September 2025 as well.
- **What the supplied material carries instead:** "In September 2025 its own maintenance team decided to trial a shared repair log in two buildings." The choice stands in a separate, undated sentence: "It chose Svale Systems after testing whether the log could show the status of each repair." The material dates the decision only, and leaves the test and the choice free to fall later — the trial ran eight weeks and the note is dated 4 December 2025, so a choice in October is compatible with everything supplied.
- **Smallest repair the checker proposed:** "In September 2025, its maintenance team decided to try a shared log. It chose Svale Systems after testing whether the log could show the status of each repair."

### The prose, as the comparison read it

---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay gains a shared view of repair reports

Elm Quay Housing’s maintenance team tested a shared repair log in two buildings to help staff on different shifts see the same information. The eight-week trial gave the team a common view of reports, but its supervisor would allow more preparation time before starting again. Expansion remains undecided.

*Published by Svale Systems.*

Elm Quay manages 640 apartments. Before the trial, telephone reports and emails were stored separately. In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair.

In an email interview, maintenance supervisor Maya Lind described what the team wanted:

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log.”

The team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members over two sessions. For Lind, preparing the categories was work worth planning for:

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.”

Elm Quay’s internal trial note, dated December 4, 2025, recorded 31 repair reports, excluding emergencies and work ordered before the trial. Median time from report to assignment was two working days during the trial, compared with three in the preceding eight-week period.

The periods had different workloads, and the note explicitly did not attribute the difference to the software. These figures concern assignment, not repair completion. There were no measurements of costs, resident satisfaction, or completion times.

Lind’s assessment of the experience came with a reservation:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

That assessment was specific to the trial; Lind did not recommend Svale to every housing company. The team has not yet expanded the trial. It will decide after checking how the categories work for larger repairs.

For operations managers considering their own implementation, Svale provides an [implementation checklist to read](https://example.invalid/svale/checklist).

## 2. Validation of the report's claim accounting

Coverage checked passage by passage against the draft as delivered. Every prose passage of the draft is paired with the supplied passage it rests on: the title; all four summary sentences; the publisher line; each sentence of the five body paragraphs; all three quotations; the two attributive sentences that introduce quotations two and three; and the closing link sentence including its URL and link text. The pairings quote the material in its own words and, where the draft compresses or reorders, state what differs rather than asserting sameness. Person, number and natural gender conveyed by pronouns are accounted for separately from reference, and the accounting correctly records that the draft asserts no natural gender for Lind while the material conveys one, and that dropping it adds and removes no supported claim.

### Detected accounting mismatches

1. **Unaccounted block (no consequence).** The draft's YAML frontmatter (`genre: case-study`, `technique: none`, `language: en_US`) appears in no row. It carries no claim about the world, and the report does use the declared language when it judges "apartments" and "December 4, 2025" as variety and date-format localisation, so nothing supported or unsupported goes unchecked. Recorded as a gap in the accounting, not as a defect in the draft.
2. **A disposition stated inside the claim table rather than in the pairing.** The title row ends "Considered and not reported — see §3.1" in place of stating what, if anything, differs in support. The substance is present in §3.1 and is sound; the mismatch is one of placement.
3. **No other mismatch found.** Each remaining row's source quotation is verbatim in the material, and no row asserts a difference the material does not show. Checked in particular: "flats" → "apartments" and "4 December 2025" → "December 4, 2025" as en_US localisation, not changed claims; "and" → "compared with" as juxtaposition without a causal verb; "during two sessions" → "over two sessions"; "says that 31 repair reports were entered" → "recorded 31 repair reports", with both exclusions kept attached to the count; and the two present-to-past tense shifts, correctly recorded in §3.2 rather than as findings.

## 3. Finding dispositions

### Finding 1 — "In September 2025" stretched over the choice of supplier: **accepted**

Draft evidence, exact: "In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair."
Source evidence, exact: "In September 2025 its own maintenance team decided to trial a shared repair log in two buildings." and, separately and without a date, "It chose Svale Systems after testing whether the log could show the status of each repair."

Established in the draft's own contextual meaning, not on a merely conceivable stronger reading: a fronted time adverbial followed by a coordinated past-tense verb phrase carries its scope across both conjuncts by default, so the sentence as written places the choice, and the test it followed, in September 2025. No supplied statement supports that dating, and one is available that would make the material true and the draft false — the decision late in September, the status test through October, the choice in November, with the eight-week trial and the note of 4 December 2025 all still holding. The support is therefore genuinely unresolved in the draft, not merely unestablished by the report. Accepted as an unresolved material claim; the smallest supported repair is the one the checker proposed, and it is reported above rather than applied.

### Finding 2 — the pronoun "it" moves the tested thing from the log to the supplier: **rejected**

Draft evidence, exact: "…decided to try a shared log and chose Svale Systems after testing whether **it** could show the status of each repair."
Source evidence, exact: "It chose Svale Systems after testing whether the log could show the status of each repair."

Rejected on the draft's actual contextual meaning. Both "a shared log" and "Svale Systems" stand as candidate antecedents in the sentence, and the predicate settles which one the sentence asserts: showing the status of each repair is a capability of a log, the thing the clause "decided to try a shared log" has just introduced as the object under trial, and the material's own sentence puts exactly that capability on the log. Read in full context, the draft asserts what the material asserts, with its subject, scope and qualification intact. The supplier reading the report relies on is available only as a conceivable alternative parse, and a merely conceivable stronger reading establishes no defect. The report also does not establish falsity on that parse: it grants in the same finding that the other reading "says what the material says", and on the supplier parse the only thing Svale Systems could be tested for showing per-repair status is its log, so no case is offered in which the material is true and the draft false. The report has not established its allegation, and the qualification it prefers — writing the antecedent out — is a preference about wording, which settles no finding. Note that the repair accepted for Finding 1 rewrites this clause in any case; that is a consequence of the accepted finding, not an acceptance of this one.

COMPARISON: complete
DRAFT: accepted defect — "In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair."
