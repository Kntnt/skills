Reviewed as a **case-study** in **en_US**, held to **no technique**. All three came from the artifact's own `kntnt` map; because that map sets `technique: none`, no arc was applied and the genre's ordinary arc was never reached. The correction budget was the default of 1, and one round was spent.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Two Elm Quay buildings tried one repair log

Elm Quay Housing tested a shared repair log in two buildings to help staff on different shifts see the same information. Maintenance supervisor Maya Lind says having one view helps the team, but that she would set aside more preparation time. The eight-week trial remains unexpanded; the team will decide after checking how its categories work for larger repairs.

The housing company Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after previously storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

## Elm Quay’s own categories went into the log

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Maya Lind, Elm Quay’s maintenance supervisor, said in an email interview.

The maintenance team kept telephone reporting open for residents. Svale configured the log and trained six staff members during two sessions.

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts,” Lind said.

## The note compares two periods and claims no cause

Elm Quay’s internal trial note, dated December 4, 2025, records 31 repair reports entered during the eight-week trial. The count excludes emergencies and work ordered before the trial.

The note puts the median time from report to assignment at two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures describe assignment, not repair completion; no completion-time, cost, or resident-satisfaction measurements are available.

## The supervisor would run the trial again

Lind gave her own assessment of the eight weeks:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

## Expansion waits on a check of the categories

The trial has not gone beyond the two buildings. Before the team decides on any more, it will look at how the categories handle larger repairs. Lind’s willingness to repeat the trial is a qualified judgment, rather than a recommendation of Svale for every housing company.

Read Svale’s [implementation checklist](https://example.invalid/svale/checklist).

*This customer case is published by Svale Systems.*
```

## Findings still standing

The budget was spent with these left, so they are all unresolved and want a person.

**1. The byline is missing, and nobody here can fill it.** `article_anatomy.py` measures `byline` as `absent` against the rule that every part is present in the order shown. It is the only counted requirement the text still fails. Neither the text, its `kntnt` frontmatter, nor the invocation names an author, so the line is reported rather than invented. A supplier-published customer account reaches the reader with nobody accountable for having written it.

**2. "the two buildings" in the ending has no referent in the body.** The ending opens "The trial has not gone beyond the two buildings." The body never says the trial ran in two buildings — only the standfirst and the headline do, and the anatomy requires the body to read complete without the standfirst. This one followed from the repair of the ending: before the round it read "The team has not yet expanded the trial", which needed nothing from the standfirst. Repair by naming the two buildings where the body first needs them, most naturally in the lead.

**3. The subheading "The supervisor would run the trial again" pre-says the quotation under it.** The quotation two lines below is "I would choose to do the trial again." The round removed that pre-echo from the bridge, which now reads "Lind gave her own assessment of the eight weeks:", and the subheading it added in the same round put the pre-echo back one level up. A subheading is worded in words its section does not already use.

**4. The headline and the standfirst now say the same thing in nearly the same words.** "Two Elm Quay buildings tried one repair log" against "Elm Quay Housing tested a shared repair log in two buildings". Headline and standfirst complement each other rather than repeat, and the new headline also states the event rather than the angle — it could head most texts about this trial. It is accurate, which the previous one was not, but it bought that accuracy with the overlap. This followed from the headline rewrite.

**5. The publisher disclosure now sits under an unrelated subheading.** "*This customer case is published by Svale Systems.*" is the third paragraph of the section headed "Expansion waits on a check of the categories", which does not describe it. Adding subheadings swept a standing disclosure into the last section.

Findings 2 to 5 are all repairs of the round creating new work, which is why the review stopped where it did rather than spending another round answering for its own.

## What the round did to the claims

**Removed.**

- "The maintenance team designed the categories" — the finding named that clause itself as the defect: it restated the quotation directly above it ("The categories were ours"). The narrative no longer asserts it; Lind still does, inside her quotation.
- "includes a reservation about preparation" (from the bridge "Lind's assessment includes a reservation about preparation:") — the finding named the pre-echo as the defect. The reservation stands in Lind's own words in the quotation that follows.
- "For operations managers considering their own preparations" and "is available to read" — the finding named both: the audience phrase named no preparation the account describes, and the passive named no step.

**Changed but standing.**

- Lind's reservation in the standfirst. "…but would allow more preparation time" became "…but that she would set aside more preparation time". The old clause had no subject of its own and read as a claim that one shared view *grants* more preparation time. The repair moves it back to what her quotations say — what she would do differently next time.
- The team's decision condition in the ending. "The team has not yet expanded the trial. It will decide after checking how the categories work for larger repairs." became "The trial has not gone beyond the two buildings. Before the team decides on any more, it will look at how the categories handle larger repairs." Same agent, same condition, same certainty, with the two clauses reversed — and with the referent problem in finding 2.
- The first attribution. "Lind said in an email interview" became "Maya Lind, Elm Quay's maintenance supervisor, said in an email interview", and the lead now opens "The housing company Elm Quay manages 640 apartments." Both move material the standfirst was carrying into the body, where the anatomy needs it.

Every quotation came back verbatim. Every sentence that bounds what the text claims came back untouched: the exclusions on the count, the note's explicit non-attribution, the absence of completion-time, cost and satisfaction measurements, and the qualified-judgment sentence.
