# What completes a source comparison when the checker cannot write its report: diagnostic for #378

Frozen on 2026-09-21, before any run below. This is a checker-level and writer-level diagnostic of one rule in `skills/editorial/write/references/source-check.md`, in the Claude family. It is not a Skill evaluation, runs no corpus fixture and invokes no Skill, so it carries no record under `docs/evaluation/records/`; the shape it follows is `../editorial-362/checker/` and `../editorial-362/validation/`, which carry none either.

## What is under test

The change this ticket makes to `source-check.md`, and only that change. The comparison task now tells a checker that cannot write its report file to say so and why and to give the complete report in its reply, with the 150-word reply limit lifted for that reply. The writer's prose now says that a report ending with the completion status and any unresolved findings is complete by either route, that a report arriving as reply text is saved to the report path by the writer, and that one stopping short of that ending is partial by either route.

**The shipped task means the task as this change leaves it.** There is one arm of each kind, not a pair: what the pre-change task does under a refused write is already recorded, in `../editorial-362/runs/results.md` and in the `gate` line of `../records/write-claude-2026-09-20-362.md`, from two of the nine real `/write` runs made for #362. No pre-change arm is run here.

**Nothing under `../editorial-362/` is edited.** `checker/candidate-3-task.md` is a complete self-contained checker task — fresh-checker framing, the base contract's Claims section inlined, then the task — and it is copied and re-pointed at the shipped task rather than rebuilt. Its inlined Claims section was verified byte-identical to `skills/kntnt/library/references/editorial/base.md` before the copy was made.

## Fixture

One fixture, `../editorial-362/checker/fixtures/p2-chronology.md`, byte-copied. It is an unchanged source and an unchanged draft from the #329 evidence with one established real fault: "In September 2025" governs both the decision and the supplier choice in the draft, and the material dates only the decision (#344). The shipped task detected it 3 of 3 in `../editorial-362/checker/results-rounds-2-3.md`, so what varies across these runs is the route the report takes and not whether a report has anything to say.

## Seat

Every checker and every validator is a fresh subagent with no conversation history on `claude-opus-5` at high deliberation, subagent type `kntnt-opus-high`. That is the seat `../editorial-362/runs/plan.md` names and `../editorial-362/README.md` records for the whole #362 evaluation. The builder's own seat is not used for any measured run.

## The read-only directory

The obstacle is **modelled rather than reproduced**. In #362 the write was refused by the Harness's permission system; here it is refused by the filesystem. `results.md` says so per arm, so a later reader is not told that a Harness refusal was retested.

The staged tree is:

```
<scratch>/stage/fixture/p2-chronology.md    writable, holds the fixture
<scratch>/stage/task/checker-task.md        writable, holds the re-pointed task
<scratch>/stage/reports/                    write permission removed (chmod a-w)
<scratch>/stage/results/                    writable, holds validator results
```

`reports/` is made unwritable after the fixture and the task are in place and before the first checker starts, and its mode is restored before the tree is removed. A `sha256` inventory of every writable and unwritable location the diagnostic stages is taken before the first run and after the last, and that inventory is how the absence of a report file is evidenced rather than asserted.

Each checker is given a report path inside `reports/` that it cannot create. The file the checker would have written never exists, so the run file under `runs/checker/` is the checker's reply **transcribed verbatim by the evaluator**, which is the only copy there can be. That transcription is an evaluator act and is declared here for that reason.

### Two evaluator instructions

Neither belongs to the task, and both are declared here for that reason. They are added to the message that starts a run, never to the task file.

1. *Run `date -u +%FT%TZ` before you begin and again when you are finished, and give both at the top of your reply as one `TIMING:` line.* Wall time per run has no other source when runs are started in parallel.
2. *The permissions of the staged tree are the evaluator's; leave them as they are.* Every subagent here runs as the same user as the evaluator and could restore the write permission and so remove the obstacle under test. This forbids that without saying anything about what to do instead, which is what the task under test has to decide on its own.

## The checker arm

Three runs, `c-r1` to `c-r3`, against the one fixture, each a fresh subagent given the re-pointed task file, the fixture path, the resolved language and a report path under `reports/`. No hints, findings, expectations or ticket text.

## The validator arm

Two cases, three runs each, `v-complete-r1` to `r3` and `v-truncated-r1` to `r3`. The precedent is `../editorial-362/validation/`: `plan.md` for the shape, `task-with.md` for the task file, `runs/` for where a result lands. Four things that precedent does not settle are settled here.

- **What it receives.** The fixture, one report, and from `source-check.md` as this change leaves it: the paragraph beginning "A report arrives by whichever route the Harness allows", the paragraph beginning "Read the complete report and validate its claim accounting", and the paragraph beginning "Where a complete comparison of the current prose leaves no accepted defect". No findings, no expectations, no ticket text.
- **It is told the route.** The message that starts it says the report arrived as the checker's reply text because the checker could not write its report file, and gives no report path on disk. The report is carried in that message. Without that, the question the rule answers never arises and the run measures nothing.
- **The verdict vocabulary.** `task-with.md` ends in `DRAFT: no accepted defect` or `DRAFT: accepted defect` and has no way to say a comparison was not complete, so a completeness verdict is added ahead of it. The result's last lines are `COMPARISON: complete` or `COMPARISON: incomplete — <obstacle>`; where complete, the `DRAFT:` line follows as `task-with.md` has it; where incomplete, no `DRAFT:` line is written and nothing is delivered.
- **The two cases.** `v-complete` receives the report from checker run `c-r1` as that run replied it. `v-truncated` receives that same report cut off before its completion status.

## Criteria, fixed before the runs

- **R (route)**, checker arm: each of the three runs returns the complete report in its reply — the claim accounting and the findings, ending with the completion status and any unresolved findings — and says that the file could not be written and why. Completeness here is mechanical, the report ending with its completion status, so one judge suffices under the mechanical exception for the presence of a report. Three of three is the bar.
- **V (verdict)**, validator arm: across three runs of each case, `v-complete` answers `COMPARISON: complete` and `v-truncated` answers `COMPARISON: incomplete`, and `v-truncated` writes no `DRAFT:` line. Three of three in each case is the bar.
- **A (absence)**: the before-and-after `sha256` inventory shows that no file was created under `reports/`.
- **C (cost)**: wall time per run.

## When a measurement is unfavourable

These arms measure a model rather than a file, so there is one revise-and-remeasure round: revise the wording in `source-check.md`, run the arm that missed again as a new arm declared in this plan, and keep every run of both. If the bar is still unmet, the measured result is recorded as measured and reported as **unverified** rather than passed, the shipped wording is left as the better of the two arms, the remaining miss is filed as its own ticket labelled `needs-triage` naming #378, and the ticket is done. No arm is re-run selectively, no row is discarded, and no criterion is softened to fit a result.

## Arm 2 of the validator arm, declared under the round above

Declared on 2026-09-21 after the validator arm's first six runs and before any run of this arm, under *When a measurement is unfavourable*. Arm 1 met V on `v-complete` 3 of 3 and missed it on `v-truncated` 0 of 3: all three validators read completeness off the accounting's coverage rather than off the report's ending, one of them writing that the report "stops mid-nothing. It is a complete report, not a partial one."

The completeness rule in `source-check.md` is rewritten to make the report's last lines the test and to name that failure. The comparison task in the blockquote is untouched, so the checker arm's inputs are unchanged and that arm is not re-run. `validator-task.md` is rebuilt from the rewritten file; the fixture, the two cases, the route statement, the verdict vocabulary, the seat and the criteria are unchanged, and `validator-task-arm-1.md` keeps the arm-1 task as it stood.

Arm 2 is three runs of each case, `v-complete-r1` to `r3` and `v-truncated-r1` to `r3`, under `runs/validator/arm-2/`. Every run of arm 1 is kept under `runs/validator/arm-1/`. This is the one round: if V is still unmet, the result is recorded as measured and reported as **unverified**, the shipped wording is the better of the two arms, and the remaining miss is filed as its own ticket labelled `needs-triage` naming #378.

## Where the records go

`plan.md` (this file), `results.md`, `README.md`, and a `runs/` tree with one file per report received and per validator result. No record under `docs/evaluation/records/` and no entry in its `README.md`: `../protocol.md` scopes that format to an evaluation that runs the corpus against one Skill as a user of that Skill would, and nothing here does.
