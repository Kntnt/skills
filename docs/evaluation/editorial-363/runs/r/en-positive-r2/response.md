Reviewed as a **case-study** in **en_US** with **no technique**. All three came from the artifact's own `kntnt` map; the map's `technique: none` settles the parameter above the genre's level, so no arc was applied — and `case-study` names none in any case. The Correction Budget was the default of 1, and one round was spent.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay values one view of repair reports

The maintenance team at Elm Quay Housing tested a shared repair log in two buildings to help staff on different shifts see the same information. Supervisor Maya Lind valued the shared view, but her assessment came with a reservation: she would allow more preparation time before repeating the trial.

*Published by Svale Systems.*

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log in two buildings after storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

## The trial starts with categories and training

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

The maintenance team kept telephone reporting open for residents. Svale configured the log and trained six staff members over two sessions. For Lind, the experience offered a preparation lesson:

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.”

## The median from report to assignment is two working days

The trial lasted eight weeks. Elm Quay’s internal trial note, dated December 4, 2025, recorded 31 repair reports, excluding emergencies and work ordered before the trial.

The median time from report to assignment was two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures concern assignment, not completion; there are no measurements of repair completion time, costs, or resident satisfaction.

## The supervisor would repeat the trial with more time

Lind gave her appraisal:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

## More buildings depend on how larger repairs work

The trial has not yet expanded. The team will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is her assessment of Elm Quay’s experience, not a recommendation of Svale for every housing company.

For an optional next step, read [Svale’s implementation checklist](https://example.invalid/svale/checklist).
```

## What the round repaired

The text arrived with no subheading anywhere, so it had no section and no ending section. Four subheadings were written from its own content, and every section now holds two or three paragraphs. The headline came down from ten words to eight, the standfirst no longer opens on the lead's first word, the lead now states that the trial ran in two buildings — a fact the standfirst alone carried, which the body needed for Lind's “before the next building starts” — a bridge that pre-said its quotation was made neutral, and a narrative sentence restating the quotation above it lost the restatement.

## Findings remaining — all unresolved

The loop stopped because the budget was spent with findings left.

1. **No byline.** The anatomy requires one line naming the author, in English `By <author>`. The line standing in that position, *Published by Svale Systems.*, names the publisher. Neither the text, nor its frontmatter, nor the invocation names an author, so the part is reported missing and left unfilled rather than invented.
2. **Two measured anatomy requirements still fail.** `article_anatomy.py` exits 1 on the delivered text: `byline` measured *absent*, and `lead` measured *2 paragraphs* against the one-paragraph rule, the publisher line being read into the lead because no byline separates them. The second follows from the first and cannot close until an author is known.
3. **The body first names Lind without introducing her.** She appears in the body as *“…,” Lind said in an email interview*; *Supervisor Maya Lind* is in the standfirst only. The body has to read complete without the standfirst, which is often shown apart from it, and a reader of the body alone has to supply who Lind is. Repairing this needs no new fact — only a decision about where her name and role belong — but it was not reached within the budget.
4. **The subheading *The median from report to assignment is two working days* is more general than the text.** The text says the median *was* two working days *during the trial*; the subheading drops the period and the past tense, so it reads as a standing figure. A headline claims only what its text claims, at the text's own strength.
5. **The subheading *More buildings depend on how larger repairs work* draws a conclusion the text does not.** The text says the team will decide after checking how the categories work for larger repairs. That the check is what expansion depends on is the subheading's addition.

Findings 4 and 5 are defects the text did not have when it arrived: both followed from this round's repair of the missing-sections finding, and both are repaired by rewording the subheading alone.

## Claim account

- **One claim was removed.** The narrative sentence *The maintenance team designed the categories and kept telephone reporting open for residents* lost its first clause, the finding having named that restatement itself as the defect. The claim survives in Lind's own words twice — *The categories were ours* and *We spent more time agreeing on the categories than entering the first reports* — and the rest of the sentence stands.
- **One claim was changed.** The bridge *Lind gave a qualified endorsement of repeating the trial:* became *Lind gave her appraisal:*, in repair of the finding that it pre-said its quotation. The narrative no longer itself characterises the appraisal as qualified or as being about repeating the trial; the reservation stands in full in the standfirst, and the quotation makes both the endorsement and the reservation in Lind's own words.
- Nothing else moved in scope, certainty, attribution, chronology, causality or meaning. The headline's rewording, the standfirst's recast opening and the lead's added *in two buildings* carry the same claims at the same strength, and every sentence bounding what the text asserts — the different workloads, the note's refusal to attribute the difference to the software, the absent measurements of completion time, costs and resident satisfaction, and Lind's assessment not being a general recommendation of Svale — stands verbatim.

The mechanical pass found nothing to correct. Nothing was written: `input.md` is untouched and the delivered text is in this response alone.
