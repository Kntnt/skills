Reviewed as a **case-study** in **en_US**, with **no technique**. All three came from the artifact's own `kntnt` map. `none` written there is a value rather than a gap: it settles the technique at that level, above the genre's, so the genre supplied no arc and none was applied. The map already said what the run resolved, so nothing in the frontmatter changed. The anatomy's counted limits were machine-measured.

The Correction Budget was its default of `1`. One correction round was delegated and verified by re-review. The loop stopped there: the budget was spent, and the re-review raised findings that round's own repair had created.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay would run its repair-log trial again

Elm Quay Housing’s maintenance team tested a shared repair log in two buildings to help staff on different shifts see the same information. Supervisor Maya Lind valued the shared view, but her assessment came with a reservation: she would allow more preparation time before repeating the trial.

*Published by Svale Systems.*

The housing company Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

## Elm Quay designed the categories and Svale set up the log

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” said Maya Lind, the maintenance team’s supervisor, in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members over two sessions. Lind described the preparation:

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.”

## The note counts 31 reports and attributes no cause

The trial lasted eight weeks. Elm Quay’s internal trial note, dated December 4, 2025, recorded 31 repair reports, excluding emergencies and work ordered before the trial.

The median time from report to assignment was two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures concern assignment, not completion; there are no measurements of repair completion time, costs, or resident satisfaction.

## Elm Quay’s supervisor weighs the eight weeks

On repeating the trial, Lind said:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

## Larger repairs come before any decision to expand

The trial has not yet expanded. The team will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is her assessment of Elm Quay’s experience, not a recommendation of Svale for every housing company.

For an optional next step, read [Svale’s implementation checklist](https://example.invalid/svale/checklist).
```

## Findings that remain

All four are unresolved.

**1. The byline is missing (requirement).** The anatomy wants one line naming the author, `By <author>`. The line in that position, *Published by Svale Systems.*, names the publisher instead, and neither the text, its frontmatter nor the invocation names an author — so it was reported and left unfilled rather than filled in. Two measured consequences follow and clear the moment an author is named: `article_anatomy.py` still reports `byline: absent`, and with no byline-shaped line to stop at, it reads the publisher line as part of the lead, so `lead` measures 2 paragraphs where the anatomy requires 1.

**2. The headline now claims more than the text does.** *Elm Quay would run its repair-log trial again* puts the organisation behind a willingness the text gives to one person. Lind says *I would choose to do the trial again*, and the closing paragraph bounds that explicitly — *Lind's willingness to repeat the trial is her assessment of Elm Quay's experience*. The body also has the company undecided: *The trial has not yet expanded. The team will decide after checking how the categories work for larger repairs.* This followed from the repair to the previous headline, *Elm Quay finds value in one view of repair reports*, which was reported at 10 words against a three-to-eight-word norm and for repeating the standfirst's wording.

**3. *Elm Quay's supervisor weighs the eight weeks* says nothing about its section.** The section's angle is that Lind would do it again and would take another week to prepare. The subheading names a subject and states none of that, and *the eight weeks* only parses for a reader carrying the trial's length forward from two sections earlier. This followed from the repair that wrote subheadings to close the missing-sections finding.

**4. *Larger repairs come before any decision to expand* repeats the sentence beneath it**, *The trial has not yet expanded.* Same repair as 3, and the smallest of the four.

The round did close the rest: the text had no subheadings and so no sections or ending at all, the standfirst and lead boundaries could not be measured, the standfirst and lead opened on the same words, and two bridges said the customer's verdict before she did. The body also relied on the standfirst to introduce Maya Lind, and now names her where it first needs her.

## What happened to the claims

**Removed.** Two, both where the finding named the whole passage as the defect:

- *Lind gave a qualified endorsement of repeating the trial* — the characterisation of her endorsement as qualified, removed with the pre-echoing bridge it was. The standfirst still records the reservation, and the quotation still carries it.
- *For Lind, the experience offered a preparation lesson* — the claim that the experience taught her a lesson about preparation, removed with the second pre-echoing bridge. The quotation under it still says what she would do differently.

**Changed.** Three claims came back standing but moved:

- The headline's claim moved from *Elm Quay finds value in one view of repair reports* to *Elm Quay would run its repair-log trial again* — a different assertion, made by the repair to the headline finding, and the ground of finding 2 above.
- The attribution at Lind's first quotation moved from *Lind said in an email interview* to *said Maya Lind, the maintenance team's supervisor, in an email interview*. The text calls her *Supervisor Maya Lind*; the repair that introduced her in the body specifies which team she supervises, which is slightly more than the text states.
- *Elm Quay manages 640 apartments* became *The housing company Elm Quay manages 640 apartments*, a descriptor added by the repair that gave the standfirst and lead different opening words. The text supports it — *Elm Quay Housing*, *every housing company*.

The sentences that bound what the text asserts came through untouched, word for word: the note's non-attribution of the median difference, the assignment-not-completion limit with the missing cost and satisfaction measures, and the closing sentence keeping Lind's willingness her own rather than a recommendation of Svale.
