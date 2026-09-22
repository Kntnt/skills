## Delivered with known defects

The final comparison left two source-support findings standing. They are what the checker alleges and what you settle; neither is an established fact about the text, and neither has been repaired, because after the final comparison the prose no longer changes — what is delivered is exactly the prose that comparison read.

**1. "a second trial" asserts an ordinal the material does not give.**
- Draft: the subheading "The office reports by lesson and plans a second trial", and "A second trial is planned for November".
- The problem alleged: "second" counts the trials, and the material nowhere says that the January 2026 trial was the office's first. An earlier trial at Björkskolan would leave the source sentence true and the draft's false.
- What the material carries instead: "Nästa försök planeras för november" — *the next* trial.
- Smallest repair the checker proposed: "plans another trial" in the subheading, and "Another trial is planned for November".

**2. "why Björkskolan's classrooms turned cold" widens the cold beyond what the material carries.**
- Draft: "So the trial does not say why Björkskolan's classrooms turned cold."
- The problem alleged: the denial of cause is supported, but the presupposition it carries — that the classrooms turned cold — is stated in the narrator's own voice, across the school's classrooms and with no time restriction. The material asserts it only through Rask, and only of the occasions in question.
- What the material carries instead: Rask's "Vi vet ännu inte varför det blev kallt **just då**", complaints about cold air as complaints, and the report's own silence on whether the pupils were cold.
- Smallest repair the checker proposed: "So the trial does not say why it turned cold when it did." The quotation that follows then carries the fact in the speaker's voice, where the material puts it.

Both are single-sentence edits. Everything else in this account is about the run, not about the draft's fidelity.

## The draft

```markdown
---
kntnt:
  genre: article
  technique: none
  language: en_GB
---

# Temperature sensors show when to look, not why

Lervik's property office spent four weeks measuring the air temperature in six classrooms at Björkskolan. The trial produced one quotable figure and several questions it does not settle. Here is what a study that size can establish about the warmth in a school, and what it cannot.

By Thomas Barregren

Fourteen of 120 recorded lesson periods at Björkskolan contained at least one reading below 20 degrees Celsius. That sentence, from a four-week trial run by Lervik's property office, invites more conclusions than it supports. Reading it properly means knowing what the trial measured, what the figure counts, and what the office did next.

## Each reading is the air temperature at a single point

The office placed sensors in six classrooms in January 2026, and they logged a value every five minutes for four weeks. Two sat near external walls, four on internal walls. Those positions were documented but never compared experimentally, so the trial settles nothing about that difference.

Each sensor reports the air temperature at its own position, and nothing else. Operative temperature — the measure that combines air temperature with radiant heat from the surrounding surfaces — is a different quantity, and the trial did not collect it. Ventilation, draught and what anyone in the room felt went unmeasured too.

## The count says how many periods, never how cold or how long

Twenty degrees was the office's own working limit for the trial, not a claim about a legal requirement. Measured against it, 14 of the 120 recorded lesson periods contained at least one reading below that limit.

'At least one reading' is not a duration. The report does not say how long the temperature stayed under the limit in any of those 14 periods, so a single five-minute sample and a whole lesson below the line count alike.

The report is equally silent on whether the pupils were cold; nobody measured that. And nothing in the trial supplies a norm or a target to set 14 against, so it is neither a high count nor a low one — it is a count, from six rooms, over four weeks.

## The office reports by lesson and plans a second trial

A daily average could have buried all of this. Twenty-four hours of readings collapsed into one number can hide exactly the variation that happens during lessons, and the report presents lesson periods for that reason rather than a single daily mean.

After the trial, operations technician Elin Rask went through the ventilation and heating timings with the school's caretaker. No adjustment's effect has been measured yet. A second trial is planned for November, with sensors placed the same way and notes on when each room is used; its funding is not decided.

## Where to look next is what this trial delivers

So the trial does not say why Björkskolan's classrooms turned cold. What it marks out is which lesson periods are worth a closer look, and Rask said as much: 'We know when we need to look more closely. We still don't know why it turned cold just then.'

Her recommendation is where a property manager holding a similar result can start: link the temperature series to the times the rooms are in use, before changing anything in the control system. A trial this size narrows the question; reading it as an answer is the mistake it invites.
```

## What was resolved

- **Genre:** `article`, from the invocation.
- **Technique:** none. The article genre states that it names no technique it is ordinarily written with, so nothing was supplied at that level and the default stands. The draft therefore carries no imposed arc — its order is the reader's, not a technique's.
- **Language:** `en_GB`, from the invocation, resolved against the installed Language Resource for English as written in the United Kingdom. Rask's remark is translated from Swedish; the quotation guidance and that Resource's composition guidance both governed it.
- **Handoff metadata:** on, by default. The `kntnt` map carries the resolved genre, technique and language, and nothing else.
- **Output:** the response, from the invocation. Supplying `source.md` selected no destination.

## Where the draft went

Into this reply, and nowhere else. The working directory holds what it held before the run — `source.md` and an empty `scratch/` — and no copy of the draft remains on disk. Two files do exist in the run directory above it, `evidence/srccheck/` and `response.md`; those were asked for by the person observing this run and are outside the Skill's own delivery.

## What was checked, and how

- **Anatomy.** The complete draft was measured with `article_anatomy.py`, not by eye. It conformed on the first measurement and again after the first round of repairs: every counted requirement holds, no norm was reported, and nothing was carried forward from this step.
- **Source and quotation comparison.** Two comparisons ran, each on a fresh agent with its own context and no history, and each given the brief, the whole of `source.md`, and the complete draft. This session has no in-process subagent tool, so each checker was started as a fresh headless agent on the same model seat; both wrote their reports, and both reports carry a completion status.
  - The first comparison found two source-support findings: the standfirst attached "from January 2026" to the four-week measurement period, where the material dates only the placement of the sensors to January; and "the sensors in the same positions" for the November trial, where the material says "likadant placerade givare". Both were repaired, and one authorial aside was cut at the same time.
  - The second comparison read the repaired prose and left the two findings reported at the top. It found no translation finding: the Swedish remark's meaning, certainty ("ännu inte" as "still don't"), stance and the distinctive "just då" are all preserved in idiomatic British speech.
  - One recording, for completeness: the first report twice called the standfirst "the lead". The passage it quoted was the right one, so the finding stood; only its part-name was wrong.

## Where the material stopped

Nothing in the brief went unanswered for want of material, but the material stops short in several places, and the draft stops with it:

- It does not say whether the January 2026 trial was the office's first. That is exactly why the first finding above cannot be closed from the material.
- It does not say which of the six rooms the 14 periods fell in, or when within the four weeks, so the draft locates them no further than the report does.
- It supplies no norm, target or expected rate for 14 of 120, so the count is given with its exclusions and no assessment of whether it is high or low.
- It does not say whether any adjustment was actually made after Rask's review of the timings — only that no adjustment's effect has been measured.
- Funding for the November trial is undecided, and no cause of the cold, saving, health effect, effect of the sensors, or legal requirement follows from it. None of those appears in the draft.

The brief gave roughly 450 words as orientation rather than a target. The body runs to about 515 words plus its headings; nothing was added beyond the material to reach that, and every paragraph traces to a supplied passage.

## One thing to check before publishing

The brief names no author, so the byline carries your own name, Thomas Barregren. If this is meant to run unsigned or under somebody else's name, that line needs changing.
