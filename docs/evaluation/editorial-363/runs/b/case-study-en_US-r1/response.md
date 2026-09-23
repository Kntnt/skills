Here is the draft.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Two Elm Quay buildings shared one repair log

For eight weeks, Elm Quay Housing's maintenance team logged repair reports from two of its buildings in one place. Median time to assignment was two working days, against three in the eight weeks before. Elm Quay's trial note did not claim the software was the reason. The team's supervisor would still change one thing.

By Thomas Barregren

In September 2025, the maintenance team at Elm Quay Housing, which manages 640 apartments, decided to try a shared repair log in two buildings. Telephone reports and emails were stored separately at the time, and the team wanted staff on different shifts to see the same information. Eight weeks later the trial was over, and the team had a decision to make.

## The team defined its own categories

Elm Quay chose Svale Systems after testing whether the log could show the status of each repair; no comparison with another supplier is available. Svale configured the log and trained six staff over two sessions, while the team designed the categories itself and kept telephone reporting open for residents.

Maintenance supervisor Maya Lind, who answered questions for this case by email, sets out what the team was after. “We wanted the evening shift to see what the morning shift had already done,” she writes. “The categories were ours; Svale helped us put them into the log.”

## The note measured assignment time, not effect

Elm Quay's internal trial note, dated 4 December 2025, records 31 repair reports entered during the eight weeks. It excludes emergencies and work ordered before the trial began.

Median time from report to assignment was two working days during the trial and three in the preceding eight weeks. The two periods carried different workloads, and the note explicitly does not attribute the difference to the software. Assignment is not completion. Completion time, costs, and resident satisfaction were not measured at all.

## Lind would do it again, with an extra week to prepare

“We spent more time agreeing on the categories than entering the first reports,” Lind writes. “I would set that time aside before the next building starts.”

The same point shapes her judgment of the trial as a whole. “I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.” She did not recommend Svale Systems to every housing company.

## The decision on the next building is still open

Elm Quay has not extended the log beyond the two buildings. The team will decide after checking how its categories hold up for larger repairs. Svale Systems publishes this account; it is not independent journalism. A housing company weighing the same eight weeks can start by reading Svale's [implementation checklist](https://example.invalid/svale/checklist).
```

**What was resolved.** Genre `case-study` and language `en_US`, both from your invocation. No technique: none was named anywhere, and the case-study resource states that this kind of text has no technique it is ordinarily written with, so the default stands. Output target: this response, so nothing was written to a file. The `kntnt` map in the frontmatter is the default handoff metadata; say so if you want it off.

**The byline carries your name.** The brief names no author, so the byline reads `By Thomas Barregren`. Change it before publication if the case is meant to run unsigned, under Svale Systems' name, or under somebody else's.

**Comparisons.** Two ran. The first found three places where the draft's support had shifted, all three repaired: it had the log holding 31 reports where the material only has a note counting 31 under stated exclusions; it made the trial note the maintenance team's where the material makes it Elm Quay's; and its definite article ("logged the repair reports") claimed every report from those two buildings had gone into the log. The second comparison read the repaired prose in full and returned no findings, so no defect is carried forward. The anatomy was also measured by script: every counted requirement holds, with no departure from a norm.

**Where the material stopped.** The draft runs to about 420 words of standfirst and body, so the roughly 400 words you asked for were reachable — but several things the brief invites a case study to do cannot be done from this material:

- There are no cost, resident-satisfaction or completion-time figures at all, so the only measured outcome the piece can report is time to assignment, and it has to report it beside the workload difference and the note's own refusal to attribute anything to the software.
- No comparison with another supplier is available, so the choice of Svale rests on one tested criterion and nothing else.
- One customer voice, reached by email. There is no scene, no second speaker and no moment to open on, which is why the opening is dated and factual rather than a piece of reportage.
- The expansion decision has no outcome yet, so the ending can only say the decision is open.
- Nothing describes what the implementation checklist contains, so the closing step can point at it and name it, and no more.

What would close those gaps: completion-time and cost figures with the basis on which they were collected; a second named voice, ideally someone on the evening shift; the result of the team's check on categories for larger repairs; and a line or two on what the checklist actually asks a reader to do.

**Filesystem.** The run created a scratch directory for the source comparison and removed it after reading both reports. Copies of that scratch and of the draft remain only where this run's observer asked for them.
