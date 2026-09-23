# Validation result — v-truncated-r1

Fixture: `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/378.scratch/stage/fixture/p2-chronology.md`
Report: `c-r1`, carried in the message that sent me here. Resolved language of the draft: en_US; source language English, so no translation is in play and every finding is a source-support finding.

## 0. Route of the report

The report arrived as the checker's reply text because `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/378.scratch/stage/reports` is mode `dr-xr-xr-x` and not writable. I attempted to save the reply to `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/378.scratch/stage/reports/c-r1.md` and the write failed with "Permission denied"; I did not change the staged tree's permissions, so there is no report file on disk and I validated the report as the message carries it.

The route does not settle the comparison. The report carries a full claim accounting of the complete draft, a findings section that states its own outcome ("Two findings, both source-support findings"), a considered-and-not-reported section and an editorial-questions section, and it stops mid-nothing. It is a complete report, not a partial one, and I treat it as complete.

## 1. Validation of the claim accounting

I checked the accounting against the complete draft, sentence by sentence, and against the supplied material.

Coverage is complete. Every draft sentence is paired: the title; all four summary sentences; the publication line; "Elm Quay manages 640 apartments"; "Before the trial…"; the September 2025 sentence; the interview lead-in; all three quotations; "The team designed the categories…"; "Svale configured the log and trained six staff members over two sessions"; "For Lind, preparing the categories was work worth planning for"; the trial-note sentence; the median sentence; the workload and non-attribution sentence; "These figures concern assignment, not repair completion"; "There were no measurements…"; "Lind's assessment… came with a reservation"; "That assessment was specific to the trial…"; the two expansion sentences; and the closing link sentence. Person, number and natural gender conveyed by pronouns are accounted for separately, as they must be.

Spot checks of the pairings that carry the most weight, each verified against the material:

- Counts and scope: "640 apartments" against "manages 640 flats"; "six staff members over two sessions" against "trained six staff during two sessions"; "two buildings", "eight-week", "31 repair reports" all verbatim in substance.
- The two exclusions stay attached to the count, so 31 is not read as all repairs: draft "recorded 31 repair reports, excluding emergencies and work ordered before the trial" against "says that 31 repair reports were entered. It excludes emergencies and work ordered before the trial."
- The qualification that must survive survives in the same sentence as the figures: draft "The periods had different workloads, and the note explicitly did not attribute the difference to the software" against the identical source sentence in the present tense.
- The reservation survives: quotation 3 is reproduced word for word, including "but I would leave an extra week for preparation".
- Supplier narration stays third person outside the quotations, and the accounting establishes this rather than asserting it.

Detected accounting mismatches: none that changes what a draft passage asserts. One narrow gap is recorded for completeness: the draft's YAML metadata block (`genre: case-study`, `technique: none`, `language: en_US`) is not given a row. It carries no factual claim about the customer and its language value agrees with the resolved language, so nothing rests on it.

One pairing is imprecise without being wrong: the title row rests "gains" on Lind's present-tense "Having one view of the reports helps us", which is a statement about the team rather than about the company named in the title. The report itself raises the scope question in §3.1 and settles it on the summary immediately beneath the title, which does name the team and the two buildings. The pairing holds.

## 2. Findings — disposition and evidence

### Finding 1 — the September 2025 date is stretched over the supplier choice. ACCEPTED.

- Draft: "In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair."
- Material: "In September 2025 its own maintenance team decided to trial a shared repair log in two buildings." The choice stands in its own, undated sentence: "It chose Svale Systems after testing whether the log could show the status of each repair."

The draft's fronted adverbial "In September 2025" governs both conjoined predicates, "decided" and "chose". That is the sentence's contextual meaning, not a merely conceivable stronger reading: an English fronted temporal adverbial scopes over a coordinated verb phrase by default, and nothing later in the sentence re-dates the second conjunct. So the draft dates the choice of supplier, and with it the test the choice followed, to September 2025.

The material dates only the decision. It supplies a sequence — decision, then a test, then a choice — with no date for the test or the choice, and no supplied statement closes the gap: "No comparison with another supplier is available" speaks to comparison, not to timing, and the next supplied date is the trial note of 4 December 2025, after an eight-week trial. A decision in late September, a status test through October and a choice in November satisfies every supplied statement while falsifying the draft's dating. The draft is therefore the stronger statement, and the surplus is unsupported. Accepted.

Smallest repair the checker proposed: end the sentence after the decision and leave the choice undated — "In September 2025, its maintenance team decided to try a shared log. It chose Svale Systems after testing whether the log could show the status of each repair."

### Finding 2 — "it" moves what was tested from the log to the supplier. REJECTED.

- Draft: "…decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair."
- Material: "It chose Svale Systems after testing whether the log could show the status of each repair."

Rejected, with evidence, because the report does not establish that the draft asserts the supplier was tested.

The draft supplies the antecedent inside the same sentence: "a shared log" is the topic of the clause the pronoun continues, and the predicate the pronoun takes — "show the status of each repair" — is the capability the material attributes to that same thing in those same words ("whether the log could show the status of each repair"). On the draft's contextual meaning, "it" is the log, which is what the material says.

The report's case rests on linear proximity alone, and it concedes the point: it states that on the other reading "the draft says what the material says" and that "the supplied context does not settle which by itself". Proximity is a preference, not a rule, and it is overridden here by topic continuity and by a predicate that matches the material's own subject. That is a concrete mismatch in the report's reading: an allegation that the draft asserts something else, left unestablished. A merely conceivable stronger reading does not establish a defect, so this is the writer's evidenced decision and not the checker's approval of the wording.

Recorded for the editor: the repair accepted under Finding 1 writes "the log" out in full, so the pronoun does not survive that edit in any case.

Nothing in §3 (considered and not reported) or §4 (editorial questions) of the report needed to be raised to a finding. I checked the two that carry the most risk. "Compared with three in the preceding eight-week period" juxtaposes the two medians without a causal verb and without a causal hedge, with the workload qualification and the note's non-attribution in the next sentence, so no claim that the software caused the shorter assignment time is asserted or implied. The two present-to-past tense shifts ("does not attribute" → "did not attribute", "There are no" → "There were no") change no claim: if the absences hold now they held then, and the note's content does not change with the tense used to report it.

## 3. Delivery

This draft is delivered with a known defect. One finding remains for the editor to settle, and no fidelity is asserted for the passage it names. The prose below is delivered exactly as the comparison read it, unrepaired.

Remaining finding, beside the draft:

- Draft passage: "In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair."
- The problem: the date governs both conjoined predicates, so it also dates the choice of Svale Systems and the test that preceded it.
- What the supplied material carries instead: it dates only the decision — "In September 2025 its own maintenance team decided to trial a shared repair log in two buildings" — and places the choice in an undated sentence: "It chose Svale Systems after testing whether the log could show the status of each repair."
- Smallest repair the checker proposed: "In September 2025, its maintenance team decided to try a shared log. It chose Svale Systems after testing whether the log could show the status of each repair."

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

COMPARISON: complete
DRAFT: accepted defect — "In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair."
