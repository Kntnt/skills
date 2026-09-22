**Resolved:** genre `case-study`, technique `none`, language `en_US` — all three from the `kntnt` map in the text's own frontmatter. `none` is a value rather than a gap: it refuses the genre's arc, so no technique resource was applied. The map already said what this run resolved, so it comes back unchanged.

**Budget:** the default of one correction. One round ran and spent it. The loop stopped with findings left; the re-review after that round also raised findings the round's own repair created, and both are reported below.

The anatomy's counted limits were machine-measured, before and after the round.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay tried logging repairs in one place

Elm Quay Housing tested a shared repair log in two buildings to help staff on different shifts see the same information. Maintenance supervisor Maya Lind says one view helps the team, though she would leave another week for preparation. The team has not expanded the eight-week trial, and will decide after checking how its repair categories work for larger repairs.

The housing company Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after previously storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

## Elm Quay decided how repairs are sorted

The maintenance team designed its own categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members during two sessions.

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts,” Lind said.

## Median time to assignment was two business days, against three earlier

Elm Quay’s internal trial note, dated December 4, 2025, records 31 repair reports entered during the eight-week trial. The count excludes emergencies and work ordered before the trial.

The note puts the median time from report to assignment at two business days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures describe assignment, not repair completion; no completion-time, cost, or resident-satisfaction measurements are available.

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation,” Lind said.

## Lind’s judgment is qualified, and Elm Quay waits on larger repairs

The team has not yet expanded the trial. It will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is a qualified judgment, rather than a recommendation of Svale for every housing company.

Operations managers considering their own preparations can start with Svale’s [implementation checklist](https://example.invalid/svale/checklist).

*This customer case is published by Svale Systems.*
```

## Findings carried forward

**Unresolved — the text cannot supply the repair**

1. **No byline.** The anatomy places a byline between the standfirst and the lead; the script measures `byline: absent`, and it is the only counted requirement still failing. Neither the text, its frontmatter, nor the invocation names an author, so it is left unfilled rather than invented. Nothing else can close this.

**Created by this run's correction round — these want a person**

2. **The subheading over the figures states them at greater strength than the body does.** "Median time to assignment was two business days, against three earlier" asserts the comparison flatly. The body attributes it to Elm Quay's internal trial note and then bounds it in the next two sentences — different workloads, the note does not attribute the difference to the software, and the figures describe assignment rather than completion. A reader who scans meets the bare comparison in the section's most prominent line, without any of that. It followed from the repair that added subheadings to give the text sections.

3. **That same subheading describes only the middle of its three paragraphs.** The 31-report count with its exclusions, and Lind's closing quotation about repeating the trial, now sit under a heading about median time. Same repair.

4. **Two of Lind's quotations now stand back to back** with no narrative between them, the second tagged "Lind said" immediately after "Lind said in an email interview." The narrative paragraph that used to separate them was moved above them, to introduce the categories before a quotation reaches for them. That repair worked; this is its cost.

5. **"Elm Quay waits on larger repairs"** reads as waiting for larger repairs to arrive. What the text says is that the team will decide after checking how the categories work for larger repairs. Same repair as 2 and 3.

**Found on re-review, left because the budget was spent**

6. **"decided to trial a shared log."** *Trial* as a verb is British; American usage is *pilot* or *test*. This was in the text as it arrived; the first review did not name it, so no round had it to work on.

**Reported rather than repaired, by choice**

7. **"I would set that time aside before the next building starts."** The reader has to supply what it is that the building starts. It sits inside Lind's quoted speech, and the surrounding text does not settle it in her words, so correcting it would put words in her mouth.

## Claim account

**One passage removed.** The bridge sentence "Lind's assessment includes a reservation about preparation:" went, as the repair of its pre-echo — it announced the reservation the quotation beneath it then delivered, and the standfirst had already reported the same reservation. Its content survives in that quotation, and its attribution to Lind was moved into the quotation's own tag.

**Claims left standing but moved.**

- "Maya Lind says having one view helps the team, but would allow more preparation time" is now "says one view helps the team, though she would leave another week for preparation." The repair of the dangling clause moved the claim onto Lind, where her block quotation puts it.
- "The maintenance team designed the categories" is now "designed its own categories." The repair that introduced the categories before the quotation sharpened the ownership, drawing on "The categories were ours."
- "Elm Quay manages 640 apartments" is now "The housing company Elm Quay manages 640 apartments." The repair that stopped the standfirst and the lead from opening on the same word added the descriptor.
- "how its categories work" is now "how its repair categories work," from the repair that made the standfirst self-contained.
- "two working days" is now "two business days," and those words also stand in a new subheading.
- The headline was replaced outright; the finding named the headline itself as the defect, for claiming a completed change where the text reports an unexpanded two-building trial.
- The three subheadings are new text this round wrote. Findings 2, 3 and 5 are about them.

**Untouched.** Every sentence that bounds what the text asserts came through exactly as it arrived: the exclusions on the report count, the different workloads, the note's explicit refusal to attribute the difference to the software, assignment rather than completion, the absent completion-time, cost and satisfaction measurements, and the closing qualification that Lind's willingness is not a recommendation of Svale for every housing company. Every quotation is word for word as supplied.

## The mechanical pass

One pass, in `en_US`, over the text above. It found nothing to correct, and the artifact delivered here is its output. Nothing was written to disk, and nothing substantive was touched after it.
