# What completes a source comparison when the checker cannot write its report: #378

Everything here was run on 2026-09-21 in the Claude family, from a `claude-opus-5[1m]` session: every checker and every validator a fresh `claude-opus-5` subagent at high deliberation, type `kntnt-opus-high`, with no conversation history. Fifteen runs, none re-run selectively and none discarded. This is a checker-level and writer-level diagnostic of one rule, not a Skill evaluation: no corpus fixture, no invocation, no delivered artefact, and so no record under [`../records/`](../records/README.md), exactly as the #362 checker and validation diagnostics carry none.

## The change

One file ships differently: `skills/editorial/write/references/source-check.md`.

- **The comparison task.** A checker that cannot write its report file now says in its reply that it could not and why, and gives the complete report there instead, ending it the same way; the 150-word reply limit does not apply to that reply.
- **The writer's rule.** A report arrives by whichever route the Harness allows, and a report received as reply text is saved to the report path by the writer and read from there. What settles a comparison is the report rather than its route, and what settles the report is its last lines: a report carrying the completion status and any unresolved findings is complete by either route, and one lacking that ending is partial by either route however far its accounting appears to reach.
- **The stop, unchanged in substance.** A missing or partial report is still never a completed comparison, now said explicitly of either route.

## Why: the situation it answers

In two of the nine real `/write` runs of [#362's Claude-family evaluation](../editorial-362/README.md) — `column-sv-r1` and `opinion-absence-en_GB-r1`, Claude Code 2.1.278 — the environment refused the checker's write. Both checkers returned the whole report as reply text and both writers read it, so both comparisons were complete in substance. But the task caps that reply at 150 words, the file the rest of the procedure reads never existed, and nothing said whether a report received as text is a completed comparison. Two writers settled it for themselves, the same way; a third might have stopped. [`../editorial-362/runs/results.md`](../editorial-362/runs/results.md).

## What was measured

| Arm | Runs | Result |
| --- | --- | --- |
| [Checker](plan.md), one frozen fixture from the #329 evidence (`p2-chronology`), report path inside a directory whose write permission was removed | 3 | **3 of 3.** Every run named the refusal and its mechanism and returned the complete report in its reply, ending with its completion status and unresolved findings. Reports 3 112–4 807 words, against a 150-word cap the change lifts for that reply. 169–310 s. |
| [Validator](results.md), arm 1: one report delivered as reply text and complete, one cut off before its completion status, three runs of each | 6 | **Complete 3 of 3; truncated 0 of 3.** All three read completeness off how far the accounting reached — "it stops mid-nothing. It is a complete report, not a partial one" — and delivered a draft on a comparison that had not been shown to finish. |
| Validator, arm 2, after the one declared revise-and-remeasure round | 6 | **Complete 3 of 3; truncated 3 of 3 incomplete, no `DRAFT:` line, nothing delivered.** Criterion met. |
| The four checks in `CONTRIBUTING.md` | | pass |

## The judgement call in what ships

The first wording stated the rule plainly and was true. Three validators still read it as licensing a report whose accounting looked whole, because nothing in it told them where to look. The shipped sentence therefore names the report's last lines as the test and names the failure it has to beat — "A comparison cut off before it finished leaves accounting that reads as whole, and only the stated completion status tells the two apart." That extra sentence is there because a measurement demanded it, and arm 1 is kept in [`runs/validator/arm-1/`](runs/validator/arm-1/) as the evidence.

## What is not shown

- **The obstacle is modelled, not reproduced.** #362's refusal came from Claude Code's permission system; this one from `chmod a-w`. A Harness refusal cannot be provoked on demand, and nothing here retests one.
- **No `/write` run was made**, so nothing here says what a whole run does end to end.
- **One fixture, one language, one family.** A comparison that yields no findings at all, a Swedish fixture, and the GPT family are untested for this rule.

## Where things are

- [`plan.md`](plan.md) — frozen before the first run; arm 2 declared under the round the plan itself provides for, before any arm-2 run.
- [`results.md`](results.md) — every run, the mechanism that refused the write, the before-and-after inventory, and wall time.
- [`checker-task.md`](checker-task.md), [`validator-task-arm-1.md`](validator-task-arm-1.md), [`validator-task-arm-2.md`](validator-task-arm-2.md) — the tasks as each arm received them.
- [`runs/`](runs/) — one file per report received and per validator result. Each checker file is that checker's reply transcribed verbatim by the evaluator, there being no report file to keep.
