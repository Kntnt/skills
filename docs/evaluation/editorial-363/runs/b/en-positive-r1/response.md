Reviewed as a `case-study` in `en_US`, held to no technique. All three came from the artifact's own `kntnt` map, which already matched what the run resolved, so nothing in the frontmatter changed. The technique was settled by the map's `none` rather than by the genre — `case-study` names none in any case. The correction budget was the default of 1; one round was spent, and three findings remain.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay values one view of repair reports

Elm Quay Housing’s maintenance team tested a shared repair log in two buildings to help staff on different shifts see the same information. Supervisor Maya Lind valued the shared view, but her assessment came with a reservation: she would allow more preparation time before repeating the trial.

*Published by Svale Systems.*

The housing company Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log in two buildings after storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

## The team defined the categories itself

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” supervisor Maya Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members over two sessions. For Lind, the experience offered a preparation lesson:

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.”

## The note records 31 reports and attributes no cause

The trial lasted eight weeks. Elm Quay’s internal trial note, dated December 4, 2025, recorded 31 repair reports, excluding emergencies and work ordered before the trial.

The median time from report to assignment was two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures concern assignment, not completion; there are no measurements of repair completion time, costs, or resident satisfaction.

## Lind would repeat the trial with an extra week

Lind said:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

## The categories still have to fit larger repairs

The trial has not yet expanded. The team will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is her assessment of Elm Quay’s experience, not a recommendation of Svale for every housing company.

For an optional next step, read [Svale’s implementation checklist](https://example.invalid/svale/checklist).
```

## Findings left

All three are unresolved.

**The byline is missing.** The anatomy places one line naming the author between the standfirst and the lead. What stands there is `*Published by Svale Systems.*`, which names the publisher. Nothing in the text, in its frontmatter or in the invocation names an author, so the part is reported as missing and left unfilled rather than invented, and the publisher line was not converted into one. A reader cannot tell who wrote the account.

**The lead measures two paragraphs.** `article_anatomy.py` reports part `lead`, rule "The lead is the first paragraph of the body: one paragraph, meeting every requirement under *Paragraphs*", measured "2 paragraphs". With no byline to close the front matter of the text, the publisher line is counted into the lead. It resolves when the byline above does, and not before; moving or deleting the publisher line would answer the measurement without answering anything a reader has.

**The subheading over the third section states Lind's appraisal before she speaks it.** "Lind would repeat the trial with an extra week" says what the quotation under it says: "I would choose to do the trial again… but I would leave an extra week for preparation." This followed from this run's own repair — the round removed the bridge "Lind gave a qualified endorsement of repeating the trial:", which pre-said the same quotation, and the section subheading it added in the same pass carries the pre-echo one level up. No single rule names it: a subheading is required to describe its section, and a section whose content is one quotation will say what that quotation says. The cost is the one the original finding named — the customer's own appraisal, which this genre gives the quotation to carry, arrives paraphrased first. Settling it means deciding whether that section stands on its own or belongs with the one before it.

## Claims

**One claim was removed.** The sentence "Lind gave a qualified endorsement of repeating the trial:" went with the repair of the pre-echo, which named that bridge as the defect. Its assertion still stands twice in the text: in Lind's own quotation directly below it, and in the closing "Lind's willingness to repeat the trial is her assessment of Elm Quay's experience, not a recommendation of Svale for every housing company."

**No claim was left standing with its scope, certainty, attribution, chronology, causality or meaning moved.** Four claim-bearing lines were reworded, and each is reported here so the change is visible without a diff. The headline "Elm Quay finds value in one view of repair reports" became "Elm Quay values one view of repair reports"; the lead's opening became "The housing company Elm Quay manages 640 apartments"; the lead now says the trial ran "in two buildings"; and the first attribution in the body became "supervisor Maya Lind said in an email interview" from "Lind said in an email interview". The two additions come from the standfirst and are stated nowhere else in the body. The three sentences that bound what the text claims — that the note does not attribute the difference to the software, that the figures concern assignment and not completion, and that Lind's willingness is her own assessment and not a general recommendation — stand exactly as they arrived.
