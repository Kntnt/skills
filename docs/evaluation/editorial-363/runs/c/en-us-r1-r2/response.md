**Resolved configuration** — genre `case-study`, technique none, language `en_US`. The invocation named none of the three; all three came from the artifact's own `kntnt` frontmatter map. The map's `technique: none` settles that parameter above the genre's level, so no arc was applied and the `case-study` resource supplied nothing there. The Correction Budget was the default of 1, and one round was spent.

**The text**

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay piloted one log for repair reports

Elm Quay Housing tested a shared repair log in two buildings to help staff on different shifts see the same information. Maintenance supervisor Maya Lind says having one view helps the team, but that preparation time was too short. The eight-week trial remains unexpanded; the team will decide after checking how its categories work for larger repairs.

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to pilot a shared log after previously storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

## Elm Quay set the categories, Svale configured the log

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members during two sessions.

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts,” Lind said.

## Two working days to assignment, not to completion

Elm Quay’s internal trial note, dated December 4, 2025, records 31 repair reports entered during the eight-week trial. The count excludes emergencies and work ordered before the trial.

The note puts the median time from report to assignment at two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures describe assignment, not repair completion; no completion-time, cost, or resident-satisfaction measurements are available.

## Elm Quay’s supervisor would do it again, better prepared

Lind gave this assessment of the trial:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

## Elm Quay will check its categories against larger repairs

The team has not yet expanded the trial. It will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is a qualified judgment, rather than a recommendation of Svale for every housing company.

Operations managers preparing a trial of their own can read Svale’s [implementation checklist](https://example.invalid/svale/checklist).

*This customer story is published by Svale Systems.*
```

**Findings that remain**

Unresolved from the review:

1. **The text has no byline.** The article anatomy requires one, between the standfirst and the lead, and the anatomy script measures it as absent. Neither the text, nor its frontmatter, nor this invocation names an author, so it is reported and left unfilled rather than invented. Everything else the anatomy requires now holds: the headline measures 43 characters and 8 words, the standfirst is one paragraph of 57 words, the lead is one paragraph, and the body runs in four sections of two or three paragraphs each, with subheadings of 53, 49, 56 and 57 characters.

Raised when the corrected text was reviewed again, and created by this run's own repair — the four subheadings that were added to repair the missing sections:

2. **Every subheading restates the sentence directly under it.** "Elm Quay set the categories, Svale configured the log" stands over the quotation "The categories were ours; Svale helped us put them into the log". "Elm Quay's supervisor would do it again, better prepared" stands over a bridge and then the quotation "I would choose to do the trial again … but I would leave an extra week for preparation". "Elm Quay will check its categories against larger repairs" stands over "It will decide after checking how the categories work for larger repairs". A subheading and the first sentence under it complement each other rather than repeat, and in the two sections that open on a quotation the cost is the one this genre guards against specifically: the customer's own words arrive second, with their force already spent by a writer's paraphrase. The third case makes the pending decision the text's third statement of it, after the standfirst and before the closing paragraph.

3. **"Two working days to assignment, not to completion" states a median as a flat figure, and has no verb.** The text says the note puts the *median* time from report to assignment at two working days during the trial, against three in a period with different workloads that the note declines to attribute to the software. A scanner who reads only the subheading takes away a plain two-working-day figure the text does not claim. The second half does carry the completion bound, which is the part worth keeping. The subheading is also a verbless noun phrase where a headline takes a full clause.

4. **Three of the four subheadings open on "Elm Quay".** The most important keyword comes first in a subheading, and here the customer's name occupies that position three times over while the section's actual subject waits behind it.

A norm the text was already departing from, and which only became measurable once the parts were delimited:

5. **The standfirst and the lead both open on "Elm"** (measured). They should begin with different first words. Following the norm was possible — the lead's own material offers another opening — and the text is no better for the departure.

**Why the loop stopped.** Two of step 7's conditions arrived together: the Correction Budget of 1 was spent, and the re-review raised findings that the round's own repair had created. Findings 2, 3 and 4 all follow from the same repair — the subheadings written to supply the sections the text was missing — so another round would have been a round repairing the round before it. That repair is the thing to settle: the sections are genuinely needed, and the four subheadings that supply them need rewriting from each section as a whole, in words its first sentence does not use.

**Claim account**

Changed:

- **The headline's claim.** "Elm Quay brings repair reports into one shared view" became "Elm Quay piloted one log for repair reports". The present-tense, organization-wide assertion was reduced to the past-tense trial the text actually reports. Scope and certainty moved deliberately, to answer the finding that the headline claimed more than the text claims.
- **The standfirst's report of Lind's appraisal.** "says having one view helps the team, but would allow more preparation time" became "says having one view helps the team, but that preparation time was too short". The second half moved from a second benefit to the reservation Lind's quoted appraisal states. Attribution to Lind is unchanged.
- **Who the closing paragraph addresses.** "For operations managers considering their own preparations" became "Operations managers preparing a trial of their own", which supplies the object the text itself carries.

Removed:

- **The bridge's characterization "includes a reservation about preparation."** The finding named that pre-echo as the defect, and the quotation that follows still carries the reservation in Lind's own words. The bridge now reads "Lind gave this assessment of the trial:", keeping the attribution the quotation has nowhere else.
- **"is available to read"** from the closing paragraph. The finding named that statement of availability as the defect; the offer and the link survive in the call to action.

No sentence that bounds what the text asserts was removed or weakened. The count's exclusions, the differing workloads, the note's refusal to attribute the difference to the software, the assignment-not-completion limit, the absence of completion-time, cost and resident-satisfaction measurements, and the sentence marking Lind's willingness as a qualified judgment rather than a recommendation all stand exactly as they arrived.

The closing mechanical pass found no errors to correct, so the text above is the corrected text as the review left it.
