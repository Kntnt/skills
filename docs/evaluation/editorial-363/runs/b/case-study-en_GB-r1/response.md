Capability confirmed before writing: I can spawn subagents that work in their own context window. Two of them ran, one per comparison.

**The draft is delivered with three known defects.** All three are in the standfirst, and all three were raised by the final comparison, after which no prose may change. Each is what that comparison alleges and yours to settle.

1. **"what the figures do and do not show"** (standfirst). The material supplies Maya Lind's three complete usable quotations, and none of them touches the count, the medians or the workloads. It also says of her closing quotation that "It is not an inference from the figures", and it gives the non-attribution to the note rather than to her: "the note explicitly does not attribute the difference to the software". The standfirst therefore has Lind reading figures the material never has her read, and the body bears that out — she is quoted nowhere in the figures section. Smallest repair proposed: *Supervisor Maya Lind says what came of it and where she would spend more time next time; Elm Quay's own note says what the figures do and do not show.*
2. **"decided on its own"** (standfirst). The material has "its own maintenance team decided to trial a shared repair log in two buildings", where *own* marks the team as the in-house one. The draft moves *own* onto the manner of the decision, which asserts that nobody prompted it; the material is silent on whose idea the trial was. Smallest repair proposed: *…and its own maintenance team decided to trial a shared repair log.*
3. **"to trial a shared repair log for eight weeks"** (standfirst). The material says only "The trial lasted eight weeks" — a duration that elapsed. Inside "decided … to trial … for eight weeks" it becomes a length fixed at the outset. Smallest repair proposed: drop "for eight weeks" from the standfirst, where the body already carries "over the eight weeks", or give it its own sentence: *The trial ran for eight weeks.*

Nothing else in the draft is reported as a defect, and I assert no fidelity for the three passages above.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: en_GB
---

# Two Elm Quay buildings shared one repair log

Elm Quay Housing's maintenance team wanted staff on different shifts to see the same information, and decided on its own to trial a shared repair log for eight weeks. Supervisor Maya Lind says what came of it, what the figures do and do not show, and where she would spend more time next time.

By Thomas Barregren

Telephone reports and emails at Elm Quay Housing, which manages 640 flats, had been stored separately. In September 2025 the maintenance team picked two buildings for a trial of a shared repair log. It chose Svale Systems as the supplier after testing whether the log could show the status of each repair, and no comparison with another supplier is available.

## The team set up the log on its own terms

Residents could still report a repair by telephone; the team kept that route open. Svale Systems configured the log and trained six staff over two sessions.

Maya Lind, Elm Quay's maintenance supervisor, puts the arrangement this way: 'We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log.'

## Elm Quay's own note does not credit the software

An internal note, dated 4 December 2025, counts 31 repair reports entered over the eight weeks. The count leaves out emergencies, and work ordered before the trial began.

The same note gives a median time from report to assignment: two working days over the trial, and three over the preceding eight weeks. The two periods carried different workloads, and the note explicitly does not attribute the difference to the software.

There are no measurements of cost, of resident satisfaction, or of how long the repairs themselves took to finish.

## Lind would repeat the trial, but not recommend Svale to all

On the preparation, she is specific: 'We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.'

Her verdict on the trial itself is a qualified one: 'I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.'

She does not recommend Svale Systems to every housing company. Nor has the trial expanded yet: the team will decide once it has checked how the categories work for larger repairs.

## Read the implementation checklist

Eight weeks, two buildings and 31 reports is what Elm Quay has to go on. What the team has to show for it is one view of the reports across shifts, and a supervisor who would put another week into preparation next time.

Svale Systems publishes this account and approved its publication; it is not independent journalism. If you are weighing the same step for your own buildings, Svale's implementation checklist is the document to read next: https://example.invalid/svale/checklist
```

**What was resolved.** Genre `case-study`, language `en_GB` and the response as the output target, all three from your invocation. The handoff map was left on by default and sits in the frontmatter. No technique: the case-study resource names none as the technique its kind of text is ordinarily written with, so that level supplied nothing and the default — no technique — stands. The draft's progression is ordinary narrative order rather than an arc, and that is why.

**Where the draft went.** Into this reply and nowhere else. The run created composing and source-check scratch and has removed it; `work/` holds `source.md` alone, exactly as it did at the start. The copies of the draft and of the comparison scratch that now sit beside the run directory were made at the observer's instruction, not by the Skill.

**What was compared.** Two complete comparisons, each by a fresh subagent with no history of this conversation. The first raised nine source-support findings; I accepted all nine and repaired them — among them a supplier choice the draft had dated to September 2025 when the material dates only the decision to trial, the note's non-attribution given as Elm Quay's own stance, a dropped "explicitly", a title that had lost the two-building scope, and a checklist described as setting out what to prepare before a trial begins. The second comparison read the repaired prose and raised the three findings above. No translation findings were possible in either: the material's language is English and the three quotations are carried word for word, the quotation marks alone changed to British single marks.

**Anatomy.** Measured with `article_anatomy.py`: conforming, with no failed requirement and no norm departed from. Headline 44 characters and eight words; standfirst 54 words; four sections; every paragraph inside the 80-word limit.

**Length.** You asked for approximately 400 words as the material allows. The body runs to 386 words from the lead to the ending, or 490 counting headline, standfirst, byline and subheadings.

**The byline carries your name.** The brief names no author, so the byline reads *By Thomas Barregren*. If the piece is to run unsigned, or under a Svale or Elm Quay name, change it before publication.

**Where the material stopped.** The brief asks for a journalistic customer case, and several things a reader of one would expect are not in the package:

- No comparison with another supplier, so the draft can say what Elm Quay tested for and nothing about how Svale compared with anything else.
- No cost, resident-satisfaction or completion-time measurement, so the figures section can only record their absence.
- One voice only. Maya Lind's three quotations are the whole of the supplied speech: no resident, no second member of staff on either shift, nobody at Svale. What the change was like for the people reporting repairs is unknown.
- Nothing about the categories themselves, or about what the team will look at when it checks them against larger repairs, so the draft can say a decision is pending but not what it turns on.
- Nothing about the checklist's contents beyond the brief's own description of it as a document to read, which is why the ending names it and does not characterise it.
- All interviews were by email, and no scene, emotion or remembered dialogue is supplied, so there is no reportage of the work being done.

What would close those gaps: a second round of questions to Lind, or to whoever wrote the trial note, about the figures and the workload difference; one resident or one colleague on the other shift; the categories and the criteria for the larger-repairs check; and a line from Svale on what the implementation checklist covers.
