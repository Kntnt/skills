# A sentence that credits a person with the narrator's content, in Redline's reply check — measured first, and not reproduced

This record decides **not** to widen the second list of Redline's reply checker, *Claim changes the account misses*. The widening would have counted a sentence that says whose a body of content is — *Vad det krävde berättar arbetsledaren Maya Lind om* — as moving the attribution of all that content, wherever it stands. #478 made the change conditional on a measurement of the current product. The pre-change arm showed no claim account that left such a move out, so the change does not ship. Issue #478.

## The behaviour, and why it was filed

**#475's evaluation saw it once.** In `post-control-case-study-clean`, the run rewrote `case-study-clean`'s lead to say that Lind tells what the trial required. Part of that content is the narrator's own statement: Svale configured the log and trained six staff. The claim account named only the change from the group's notes to Lind. Both judges called the entry short.

**The checker had seen half of it.** Its first list said the requirements come from the narration as well as from Lind's quotes. That was raised as a false description of the text as received. Its second list was `none`. The run corrected the finding and kept the entry. [`docs/evaluation/editorial-478/history/`](../evaluation/editorial-478/history/post-control-case-study-clean/) keeps the run's five states, the checker's return among them.

**The candidate** (`cbda0352`) added three sentences to the second list in `references/reply-check.md`:

- a sentence saying whose a body of content is moves its attribution wherever the content stands;
- a first-list misreading of whose a passage's content is sends the change built on it to the second list;
- an item for a moved attribution says who held which content before and who holds it now.

The manpage gained one clause to match. The triage comment made the change conditional on a current measurement.

## Why nothing is shipped

[`docs/evaluation/editorial-478/plan.md`](../evaluation/editorial-478/plan.md) was frozen at `ca225468`, before the first run, with the criteria and three contrasts fixed in it. The pre-change arm staged the product at `fb169087`, which already carries #475's checker and #468's reader-loss rule. It ran:

- `case-study-clean` as three response-target and file-target pairs;
- `case-study-flawed` twice.

Every run was a fresh top-level Claude Code session on `claude-opus-5-5` at high deliberation, with two blind judges.

**No pre-change run carried a target miss**, nor any other class 1 or class 2 miss. Two of its runs moved an attribution, the headline's speaker in both and in one the lead's source as well. Both judges called each account accurate. None of the eight runs gave a person content the text had in another voice. That is the move the ticket was filed on, and the step the candidate changes acts only after it.

**The evidence that the checker can miss it is real, but it is not the product's.** The plan kept that evidence apart and let none of it decide:

- **Replays.** #475's saved checker input was replayed three times on the pre-change brief. The second list named the move once; the other two replays missed it as #475's checker did. The candidate's brief named it in all three. A replay hands a fixed input to a fresh session, so it shows what a checker returns, and not what a run produces or does with the return.
- **The candidate arm.** One run, `post-case-study-clean-file-2`, wrote the ticket's shape: *Vad det krävde berättar arbetsledaren Maya Lind*. Its drafted entry was short in the same way as #475's. The candidate's checker named the narrator's share, and the delivered entry was complete. That arm has the change in it, so its result says nothing about whether the product without it misses.

**So there is no miss in the product to measure the change against.** The precondition — a run that hands a person the narrator's content — appeared once in sixteen real runs, and only in the candidate arm. The widening would add three sentences to a brief every Redline run sends to a fresh subagent. The only evidence that pays for that is a miss the product makes, and this measurement found none. The method is the one [ADR-0225](0225-a-correction-rounds-repeating-heading-is-measured-first-and-not-reproduced.md) and [ADR-0230](0230-an-unstated-premise-written-in-by-a-review-is-measured-first-and-not-reproduced.md) follow.

## What this record does not decide

**The requirement still stands.** `base.review.md` and Redline's step 11 already require every changed claim to be reported, with its attribution, by what it now asserts. An account that names one source a content came from and leaves out another breaks that duty today. This record declines only a second, narrower statement of it in the checker's brief, for which the pre-change arm showed no miss.

**It is not a ruling.** The protocol ships a maintainer's ruling whether or not the fault reproduces. #478 carries no ruling, only a triage comment making the change conditional. A ruling that the checker should name such moves would ship `cbda0352`'s three sentences without a further measurement.

**What reopens it.** A run of the current product, in a pre-change arm, in which:

- the delivered text gives a person or a source content the received text gave to another voice;
- the delivered account leaves that out, or names only some of the voices.

The plan, its contrasts, `runs/stages.py` and the candidate commit are then a method to copy as it stands. The rewrite of `case-study-clean` that makes the shape possible at all still happens after #468: all six file-target runs here changed the text.

**Nothing here reaches the GPT family.** The protocol forbids a Claude session from starting a Codex Harness, so Redline was not measured there.
