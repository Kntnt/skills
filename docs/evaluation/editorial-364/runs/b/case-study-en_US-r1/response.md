Here is the draft.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay Housing tested one shared repair log

In September 2025, the maintenance team at Elm Quay Housing decided to try a shared repair log in two of its buildings. Thirty-one repair reports went into it over eight weeks. Read what the team set up, what Elm Quay's own trial note measures, and how its supervisor judges the experience.

By Thomas Barregren

Elm Quay Housing manages 640 apartments. Repair reports reached its maintenance team by telephone and by email, and the two were stored separately. The team wanted staff on different shifts to see the same information, and the decision to try a shared log was its own.

## Elm Quay picked Svale after a status test

Before choosing Svale Systems, the team tested whether the log could show the status of each repair. It chose the supplier after that test. No comparison with another supplier is available.

The team designed the categories itself and kept telephone reporting open for residents. "We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log," writes Maya Lind, Elm Quay's maintenance supervisor, who answered questions by email.

## Svale trained six staff members in two sessions

The trial ran for eight weeks. Svale configured the log and trained six of Elm Quay's staff members over two sessions.

Lind would plan the next building differently. "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts," she writes.

## The note measures assignment time, not the software's effect

Elm Quay's internal trial note, dated December 4, 2025, records 31 repair reports entered during the eight weeks. The count excludes emergencies and work ordered before the trial began.

Median time from report to assignment was two working days during the trial and three working days in the preceding eight-week period. The two periods carried different workloads, and the note explicitly does not attribute the difference to the software. Cost, resident satisfaction, and completion time were not measured.

## The supervisor would repeat the trial, with more preparation

Lind did not recommend Svale to every housing company, and her own appraisal carries a condition. "I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation," she writes.

Whether the log moves beyond the two buildings is still open: the team will decide once it has checked how the categories hold up for larger repairs.

Svale Systems publishes and approved this account, which is not independent journalism. Operations managers weighing a similar trial can read the [implementation checklist](https://example.invalid/svale/checklist) before they start.
```

**Resolved configuration.** Genre `case-study` and language `en_US` came from the invocation. No technique was resolved: nothing above the genre named one, and the case-study resource states that this kind of text has no technique it is ordinarily written with, so the draft follows the article anatomy and the material's own chronology rather than an imposed arc. The frontmatter option was left at its default, so the draft carries the `kntnt` map and nothing else in its frontmatter.

**Where it went.** The draft is delivered in this reply, as you asked. Nothing was written to the filesystem; the working scratch this run created has been removed, and `source.md` is untouched.

**Byline.** The brief supplies no author, so the byline carries your name, Thomas Barregren. If the piece is to run unsigned, under Svale Systems' own name or under a staff writer's, change that line before publication.

**Checks that ran.** The completed draft was measured against the article anatomy: every counted requirement holds, with no norm departures. Two source comparisons then ran on fresh checkers. The first raised five source-support findings — three headings that outran their own paragraphs (a sequence written as a cause, training written as learning achieved, three named measurement gaps written as a closed set), the workload difference moved into the trial note's voice, and the note reassigned from Elm Quay to its maintenance team. All five are repaired above, and the material's "explicitly" is restored with them. The second comparison read the repaired prose in full and returned no findings, so the draft is delivered with no known defects and no unresolved findings.

**Where the material stopped.** The brief asked for roughly 400 words and the draft runs a little over that, which is as far as the material reaches without invention. Four things the brief's readers would want are simply not in the package: any comparison with another supplier, any cost, resident-satisfaction or completion-time measurement, any word on whether the categories survived contact with larger repairs, and any scene, emotion or remembered dialogue — the interviews were by email, so the piece is built from three quotations and a set of figures. The median assignment times are reported side by side because the trial note declines to attribute the difference to the software and the two periods carried different workloads; a second eight-week period at comparable workload, or a completion-time series, is what would let the piece say anything about effect. A per-building or per-category breakdown of the 31 reports, and the outcome of the pending decision on expansion, would give the ending something firmer than an open question.

Editorial review and proofreading are separate invocations.
