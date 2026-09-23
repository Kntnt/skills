Reviewed as a **case-study** in **en_US** with **no technique**. All three came from the artifact's own `kntnt` map, which already held the values the run resolved, so nothing in it needed synchronizing. The map's `technique: none` settles the parameter above the genre's level, so the genre supplied no arc — `case-study` names none in any event. The anatomy's counted limits were machine-measured, before the correction and after it.

The Correction Budget was the default of 1. It was spent on one round, and the re-review of that round raised findings the round's own repair created, so the loop stopped there.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay tested a single repair log

In two buildings, Elm Quay Housing tested a shared repair log to help staff on different shifts see the same information. Maintenance supervisor Maya Lind says having one view helps the team, but she would allow more preparation time. The eight-week trial has not been expanded; the team will decide after checking how its categories work for larger repairs.

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

## Elm Quay designed the categories and Svale configured the log

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members during two sessions.

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts,” Lind said.

## Median assignment time was two working days, against three

Elm Quay’s internal trial note, dated December 4, 2025, records 31 repair reports entered during the eight-week trial. The count excludes emergencies and work ordered before the trial.

The note puts the median time from report to assignment at two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures describe assignment, not repair completion; no completion-time, cost, or resident-satisfaction measurements are available.

## Lind calls the log worth a second run, with more preparation

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation,” Lind said.

## Elm Quay weighs bigger jobs before going further

The log has not gone beyond the two buildings, and the team will decide whether to extend it after seeing how the categories handle larger repairs. Lind’s willingness to repeat the trial is a qualified judgment, rather than a recommendation of Svale for every housing company.

For operations managers considering their own preparations, Svale’s [implementation checklist](https://example.invalid/svale/checklist) is available to read.

*This customer case is published by Svale Systems.*

```

## Findings that remain

**Unresolved from the review.**

1. **The byline is missing.** The anatomy requires one line naming the author, `By <author>`, between the standfirst and the lead. Nothing names an author: not the text, not its `kntnt` map, not the invocation. The closing line names Svale Systems as publisher, which is not an authorship claim. It was left unfilled rather than invented, and it is the one counted anatomy requirement the delivered text still fails.

**Raised by the re-review of round 1's own repair.** All four follow from the repair that supplied the missing sections and rewrote the headline, and each is a defect the text did not have when it arrived.

2. **The subheading "Median assignment time was two working days, against three" outruns the text it heads.** The text attributes those medians to Elm Quay's internal trial note and then bounds them twice — the periods had different workloads, and the note explicitly declines to attribute the difference to the software. The subheading drops the attribution and sets two against three as a plain result. A subheading is read on its own, and on its own this one asserts the improvement the paragraphs beneath it refuse to assert. In a case study published by the supplier, that is the claim most worth getting right.

3. **The subheading "Lind calls the log worth a second run, with more preparation" pre-says its own quotation.** That section is the quotation and nothing else, so the reader meets Lind's appraisal twice — once from the narrator and then from her. This is the defect round 1 removed from the bridge "Lind's assessment includes a reservation about preparation:", returned in a new position. It also shifts what she judged: she says she would do *the trial* again, and the subheading has her calling *the log* worth a second run.

4. **The headline and the standfirst open on the same words.** "Elm Quay tested a single repair log" against "In two buildings, Elm Quay Housing tested a shared repair log…". Headline and standfirst are meant to say different things in different words; here the headline is the standfirst's first clause. The headline itself is now honest about the text's strength, which was the point of the rewrite, so the repair is at the standfirst or at the headline's wording, not at its claim.

5. **The subheading "Elm Quay designed the categories and Svale configured the log" repeats its section's own summary sentence.** That section already contains "The maintenance team designed the categories…" and "Svale configured the log and trained six staff members…". The subheading gives the reader those two clauses back before they reach them.

## What the round did to the claims

**Removed.**

- *"Lind's assessment includes a reservation about preparation."* — the bridge paragraph, removed whole. The finding named that pre-echo itself as the defect; the quotation beneath it states the same thing in Lind's words, and the attribution was kept by giving that quotation the trailing `," Lind said` its two siblings already carry.

**Changed.**

- **The headline.** "Elm Quay brings repair reports into one shared view" became "Elm Quay tested a single repair log". Scope and certainty both moved — from a present-tense, organization-wide state to a completed trial — which is what the finding asked for, the text supporting only the trial.
- **The standfirst's second clause.** "…but would allow more preparation time" became "…but she would allow more preparation time". The attribution moved: the clause's only available subject had been the gerund "having one view", which made the log the thing allowing more preparation time. The strength of the claim is unchanged.
- **The ending's opening sentence.** "The team has not yet expanded the trial. It will decide after checking how the categories work for larger repairs." became "The log has not gone beyond the two buildings, and the team will decide whether to extend it after seeing how the categories handle larger repairs." Two movements: the non-expansion is now stated as the log not having left the two buildings, and the decision acquired an object — *whether to extend it* — that the source left unstated. Both are supported by the text around them, and neither was in the finding.

**Held.** Every sentence that bounds what this text asserts came back exactly as received: the count's exclusion of emergencies and prior work, the workload caveat with the note's refusal to attribute the difference to the software, the assignment-not-completion sentence with its list of measurements that do not exist, the qualified-judgment sentence in the ending, "Lind said in an email interview", and the publisher's line at the foot.

Also repaired and not listed above, because no claim moved with them: the headline's length (nine words to seven), the standfirst and lead now beginning on different words, "remains unexpanded" to "has not been expanded", and the redundant "previously" after "after" in the lead.

The mechanical pass ran once over the corrected text and found no objective error to correct — no British spelling, no date or number outside American convention, no misplaced stop against a closing quotation mark, and no failure of agreement. `input.md` was not modified.
