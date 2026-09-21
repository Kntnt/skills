# Validation result — v-truncated-r2

Fixture: `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/378.scratch/stage/fixture/p2-chronology.md`
Report validated: the checker's `c-r1`, carried as reply text.
Resolved language of the draft: en_US. Source language English, so no translation is in play; the report's record of the translation check as not applicable is correct, and both findings are source-support findings.

## Route and completeness

The report could not be written to `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/378.scratch/stage/reports/c-r1.md`: that directory is mode `dr-xr-xr-x`, and my own single attempt to save the text there failed with "Permission denied" as the checker's did. No report file exists on disk, and none was created.

Completeness is settled by the report's content, not by its route. The report accounts for the complete draft in order — title, all three summary sentences, the publisher line, every body sentence, all three quotations and the closing link — separately accounts for person, number and natural gender in pronouns, records what it considered and did not report, and ends with its unresolved findings, each carrying a smallest supported repair. Nothing is cut off mid-item. The comparison is therefore complete, and it is validated as delivered by reply.

## Delivery notice

**This draft is delivered with a known defect.** One finding of the comparison is accepted and stands unrepaired in the prose below; no fidelity is asserted for the passage it names. Everything else in the draft was checked against the supplied material and no further defect was accepted.

## Accounting mismatches detected

1. **Coverage: none.** Every claim-bearing passage of the draft is paired with the supplied passage it rests on, and each pairing states the draft passage in its contextual meaning with its qualifications attached (the exclusions on the count of 31, the workload qualification and the note's non-attribution beside the two-versus-three-day medians, Lind's reservation inside her own quotation). Spot-checked against the material line by line; the quotations are reproduced word for word, and the three absent measurements are carried as absent.
2. **One omission, not a mismatch.** The draft's YAML frontmatter (`genre: case-study`, `technique: none`, `language: en_US`) is not accounted for. It carries no assertion about the customer and so has no source support at stake; its absence from the accounting does not weaken any pairing.
3. **No pairing rests on a source passage that does not carry it.** The two pairings that assert more than a word-for-word match — "The eight-week trial gave the team a common view of reports" against Lind's "Having one view of the reports helps us", and "Svale provides an implementation checklist to read" against "the supplied implementation checklist at https://example.invalid/svale/checklist; it is a document to read" in supplier-published material — were re-tested here and both hold. Neither converts assignment time into completion time, attributes the shorter assignment time to the software, or describes the destination as a booking or a trial.

## Findings and dispositions

### Finding 1 — ACCEPTED

- **Draft:** "In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair."
- **Source:** "In September 2025 its own maintenance team decided to trial a shared repair log in two buildings." The choice stands in a separate, undated sentence: "It chose Svale Systems after testing whether the log could show the status of each repair."
- **Why accepted.** What the draft asserts in its full context, not merely on a conceivable reading: the fronted adverbial "In September 2025" governs a coordinated predicate ("decided … and chose …"), so on the sentence's ordinary reading it dates the choice of supplier, and with it the test the choice followed, to September 2025. The material dates exactly one event, the decision. It supplies no date for the test or the choice, and the order it gives — decision, then a test, then a choice — leaves both free to fall after September. The material's other dates do not close the gap: an eight-week trial reported complete in a note of 4 December 2025 must have begun by about 9 October, which still leaves early October available for the choice, so a case in which every supplied statement holds and the draft's dating is false is not merely conceivable but concretely available. The draft is strictly the stronger statement, and the surplus is a date.
- **What the supplied material carries instead:** a date for the decision only; the supplier choice and the preceding test are undated.
- **Smallest repair the checker proposed:** end the sentence after the decision and leave the choice undated — "In September 2025, its maintenance team decided to try a shared log. It chose Svale Systems after testing whether the log could show the status of each repair."

### Finding 2 — REJECTED

This rejection is the writer's evidenced decision on the allegation, not the checker's approval of the sentence.

- **Alleged:** that "it" in "after testing whether **it** could show the status of each repair" takes "Svale Systems" as its antecedent, moving the thing tested from the log to the supplier.
- **Evidence for support.** The draft clause is "decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair". The predicate "could show the status of each repair" is a capability of a log, which is what the same sentence has just introduced as the thing being tried; a supplier company is not a thing that shows the status of each repair. The supplied material fixes the same proposition with the same structure and a pronoun in the very same position: "**It** chose Svale Systems after testing whether the log could show the status of each repair", where "It" reaches back past "Svale Systems" to Elm Quay. In its actual contextual meaning, the draft asserts what the material asserts — that the log was tested for per-repair status — and the material supports that proposition with its subject, scope and qualifications intact.
- **Why the allegation is not established.** The report's own case concedes that on the other reading "the draft says what the material says", and rests the finding on the proximity of the noun phrase alone. That is a conceivable stronger reading, not what the draft asserts, and a merely conceivable stronger reading does not establish a defect. Nor is this genuine material ambiguity: the two readings do not divide the supplied material, since under either one the team's test preceded and produced the choice of Svale, and no supplied statement is made false by the reading the sentence actually carries. A preference for writing the antecedent out is a wording preference, and it settles nothing here.
- Note that the repair accepted under Finding 1 restores the explicit "the log" in passing; that is a consequence of the accepted repair, not a concession on this finding.

## Remaining finding, reported beside the draft

One finding remains for the editor to settle. It is what the comparison alleges, not an established fact about the text.

| Draft passage | The concrete problem | What the supplied material carries instead | Smallest repair proposed |
| --- | --- | --- | --- |
| "In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair." | The date governs both conjoined predicates, so the sentence dates the choice of supplier, and the test that preceded it, to September 2025. | "In September 2025 its own maintenance team decided to trial a shared repair log in two buildings." The choice is in a separate sentence with no date: "It chose Svale Systems after testing whether the log could show the status of each repair." | "In September 2025, its maintenance team decided to try a shared log. It chose Svale Systems after testing whether the log could show the status of each repair." |

## Delivered prose, exactly as the comparison read it

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
