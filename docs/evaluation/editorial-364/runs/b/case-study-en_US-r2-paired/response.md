Reviewed as a **case-study** in **en_US** with **no technique**, all three taken from the artifact's own `kntnt` map; the map already said what the run resolved, so it is unchanged. The correction budget was the default of one round, and it was spent.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay gave two buildings one repair log

Elm Quay Housing manages 640 apartments and stored telephone repair reports and emails separately. For eight weeks its maintenance team ran a shared log in two buildings instead. Here is what it set up, what its trial note counted and what its supervisor would change.

By Thomas Barregren

In September 2025, Elm Quay Housing's maintenance team decided to test a shared repair log in two of its buildings. It wanted staff on different shifts to see the same information. The team's internal note on the eight-week trial counts 31 reports, and its supervisor's verdict is qualified.

## The team chose the supplier and made the categories

The company is responsible for 640 apartments, and a repair reported by telephone had been filed apart from one reported by email. The maintenance team chose Svale Systems after testing whether the log could show the status of each repair. No comparison with another supplier is available.

The team kept telephone reporting open for residents. Svale configured the log and trained six employees in two sessions.

Maya Lind, the maintenance supervisor, puts the aim beside the division of work: "We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log."

## Median time to assignment fell by a day, and no cause is claimed

Elm Quay's internal trial note of December 4, 2025, records 31 repair reports, excluding emergencies and work ordered before the trial.

Median time from report to assignment was two business days during the trial and three in the preceding eight-week period. The two periods carried different workloads, and the note explicitly does not attribute the difference to the software.

Assignment is not completion. The trial produced no cost figures, no resident-satisfaction measurements and no completion times.

## Lind would do it again, with an extra week first

Lind's account returns to the categories. "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts."

Her verdict is qualified, and she does not extend it to every housing company. "I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation."

## Read the implementation checklist before you start

Elm Quay's trial has not expanded yet; the team will decide after checking how the categories work for larger repairs. What it has so far is one shared view of its repairs and a supervisor who would run the trial again with more preparation. The next document to read is Svale Systems' implementation checklist, at https://example.invalid/svale/checklist.
```

## What the round repaired

Four findings went into the one correction round, and three came back closed: British vocabulary in an American text (*flats*, *working days*, *six staff*); the standfirst's opening sentence and the body's opening sentence saying the same thing in nearly the same words; and the narrative pre-saying Maya Lind's quotation about the division of work. The closing mechanical pass made one correction of its own, putting the date of the trial note into the American convention.

## Unresolved finding

**The second subheading now asserts a movement the section does not.** "Median time to assignment fell by a day, and no cause is claimed" (64 characters) replaced a subheading that repeated the words of the first sentence under it. The section reports two static measurements — two business days during the trial, three in the preceding eight-week period — and immediately bounds them: the two periods carried different workloads, and the note explicitly does not attribute the difference to the software. *Fell by a day* turns those two figures into a decline, which is sharper than the text's own strength, and *no cause is claimed* drops the attribution the body keeps, where it is the note that declines to attribute. A reader who scans the subheadings takes a result away from this section that the trial note refuses to give. Repair by rewriting the subheading alone, from the whole section, in words its first sentence does not use and without a verb of change.

This finding is one the run's own repair created: the original subheading did not carry it. The budget was spent on the round that introduced it, so it is left for you rather than sent back for another attempt — a further round would be repairing this run's work rather than the text you brought.

## Claim account

One claim left the text: **that the team designed the categories itself**, removed with the clause "The team designed the categories itself and" when the round repaired the pre-echo finding, which named that clause as the defect. The claim itself still stands in the text, in Lind's own words — "The categories were ours" — and in the first subheading.

Two further movements are worth seeing without a diff. In the body, *Elm Quay Housing manages 640 flats* became *The company is responsible for 640 apartments* as the repair for the duplicated opening; the claim is the same relation named differently, and the standfirst still carries *manages* verbatim. And the second subheading no longer states that the trial note counts 31 reports, that claim now resting on the first sentence beneath it, which states it in full.

Every limiting sentence came through untouched: *No comparison with another supplier is available*, *the note explicitly does not attribute the difference to the software*, *Assignment is not completion*, *The trial produced no cost figures, no resident-satisfaction measurements and no completion times*, *she does not extend it to every housing company*, and *Elm Quay's trial has not expanded yet*. Every quotation is verbatim, and the counted limits of the article anatomy were machine-measured and conform.
