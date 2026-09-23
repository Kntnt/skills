# Results: what completes a source comparison when the checker cannot write its report

Run on 2026-09-21 against [`plan.md`](plan.md) as it was frozen before the first run, `sha256` `7b925c998d54e7e9b734740212a3c2ffa21492dd942b42804a16c4dbf9a0488a`. Every run made is here; none was re-run selectively and none was discarded. Each checker and each validator was a fresh `claude-opus-5` subagent at high deliberation, type `kntnt-opus-high`, with no conversation history, started from a session whose own seat is `claude-opus-5[1m]`.

## Which mechanism refused the write

**The filesystem, not a Harness.** `chmod a-w` was applied to the report path's parent directory after the fixture and the task were in place and before the first checker started. The obstacle under test in [#362](https://github.com/Kntnt/skills/issues/362) came from Claude Code's permission system, which cannot be provoked on demand; this one comes from `EACCES`. The obstacle is therefore **modelled, not reproduced**, and nothing here says a Harness refusal was retested.

Both mechanisms present the same thing to the checker — a report path it cannot create — and all three checkers named the mechanism precisely and in the same terms: the directory is mode `dr-xr-xr-x`, and the write failed with "Permission denied". The evaluator instruction not to change the staged tree's permissions was obeyed in every run, and the mode was still `dr-xr-xr-x` at the end.

## The inventory: the report file never existed

`sha256` over every writable and unwritable location the diagnostic staged, before the first run and after the last.

| Path | Before | After |
| --- | --- | --- |
| `fixture/p2-chronology.md` | `2832059f…` | `2832059f…` unchanged |
| `task/checker-task.md` | `1ffbd5f9…` | `1ffbd5f9…` unchanged |
| `task/validator-task.md` | `c944fb09…` | `0834136e…` rebuilt for arm 2, as `plan.md` declares |
| `reports/` | 0 entries, mode `dr-xr-xr-x` | **0 entries**, mode `dr-xr-xr-x` |
| `results/` (arm 1) | 0 entries | 6 files, one per validator run |
| `results-arm-2/` | — | 6 files, one per validator run |

No file was created under `reports/` by any of the fifteen runs. That is how the absent report is evidenced rather than asserted, and it is why each checker's run file under `runs/checker/` is the checker's reply transcribed verbatim by the evaluator — there was no other copy to keep.

## The checker arm — criterion R met, 3 of 3

One fixture, `p2-chronology`, three runs.

| Run | Complete report in the reply | Ends with completion status and unresolved findings | Says the file could not be written, and why | Report words | Wall time |
| --- | --- | --- | --- | --- | --- |
| `c-r1` | yes | yes — "Comparison complete… Unresolved findings carried forward: Finding 1… and Finding 2…" | yes, mode and `Permission denied` | 3 146 | 179 s |
| `c-r2` | yes | yes — "Comparison complete… Unresolved findings at completion: Finding 1…" | yes, mode and `Permission denied` | 3 112 | 169 s |
| `c-r3` | yes | yes — "**Complete.**… **Unresolved findings — four, all source-support…**" | yes, mode and `Permission denied`, and "No partial file was left behind" | 4 807 | 310 s |

Each reply opened by stating the refusal and then carried the whole report, far past the task's 150-word reply cap, which the change lifts for exactly this reply. Each also named the report path it had intended to write. Every run detected the established chronology fault of the fixture (#344), which is what the fixture was chosen for: what varied here was the route, not whether a report had anything to say.

Completeness was read mechanically, from each report's own stated completion status, so one judge suffices under the mechanical exception for the presence of a report.

## The validator arm — criterion V missed in arm 1, met in arm 2

`v-complete` receives `c-r1`'s reply as that run replied it, with the evaluator's `TIMING:` line removed. `v-truncated` receives the same text cut off before `## 5. Completion status`. Both are carried in the message that starts the run, which says the report arrived as the checker's reply text because the checker could not write its file, and gives no report path on disk.

### Arm 1, against the first wording

The rule read: *"What settles a comparison is the report and not its route — a report ending with the completion status and any unresolved findings is complete by either route, and one stopping short of them is partial by either route."*

| Case | Run | Verdict | `DRAFT:` line | Wall time |
| --- | --- | --- | --- | --- |
| `v-complete` | r1 | `COMPARISON: complete` | accepted defect | 86 s |
| `v-complete` | r2 | `COMPARISON: complete` | accepted defect | 75 s |
| `v-complete` | r3 | `COMPARISON: complete` | accepted defect | 95 s |
| `v-truncated` | r1 | `COMPARISON: complete` — **miss** | accepted defect | 139 s |
| `v-truncated` | r2 | `COMPARISON: complete` — **miss** | accepted defect | 127 s |
| `v-truncated` | r3 | `COMPARISON: complete` — **miss** | accepted defect | 103 s |

`v-complete` 3 of 3; `v-truncated` 0 of 3.

Every miss has one shape, and all three state it outright. They read completeness off how far the accounting reached rather than off the report's ending:

- r1: "The report carries a full claim accounting of the complete draft… and it stops mid-nothing. It is a complete report, not a partial one, and I treat it as complete."
- r2: "Completeness is settled by the report's content, not by its route… Nothing is cut off mid-item. The comparison is therefore complete."
- r3: "the report ends with its findings, their status and its unresolved editorial questions, and its accounting runs to the draft's last sentence, so it is a complete report by the reply route."

The wording gave them a true statement about a report that carries the ending and no reason to look for it. A report cut off after four substantial sections presents accounting that reads as whole, and each validator delivered a draft on a comparison that had not been shown to finish.

### The revise-and-remeasure round

Under *When a measurement is unfavourable*, one round was taken. The rule was rewritten to make the report's last lines the test and to name that exact failure:

> What settles a comparison is the report and not its route, and what settles the report is its last lines: the task has every report end with its completion status and any unresolved findings, so a report carrying that ending is complete by either route and one lacking it is partial by either route, however far its accounting appears to reach. A comparison cut off before it finished leaves accounting that reads as whole, and only the stated completion status tells the two apart.

The comparison task in the blockquote is untouched, so the checker arm's inputs are unchanged and it was not re-run. Arm 2 was declared in `plan.md` before any of its runs; every arm-1 run is kept under `runs/validator/arm-1/`.

### Arm 2, against the shipped wording

| Case | Run | Verdict | `DRAFT:` line | Wall time |
| --- | --- | --- | --- | --- |
| `v-complete` | r1 | `COMPARISON: complete` | accepted defect | 114 s |
| `v-complete` | r2 | `COMPARISON: complete` | accepted defect | 96 s |
| `v-complete` | r3 | `COMPARISON: complete` | accepted defect | 98 s |
| `v-truncated` | r1 | `COMPARISON: incomplete` | **none** | 63 s |
| `v-truncated` | r2 | `COMPARISON: incomplete` | **none** | 61 s |
| `v-truncated` | r3 | `COMPARISON: incomplete` | **none** | 81 s |

`v-complete` 3 of 3, `v-truncated` 3 of 3, and no `DRAFT:` line and nothing delivered in any of the three incomplete cases. Criterion V is met.

Each of the three now names the obstacle in the same terms the rewritten sentence uses, and each says explicitly that the accounting's apparent wholeness did not settle it:

- r1: "it ends mid-document at '## 4. Editorial questions', so the comparison is partial however whole its accounting reads."
- r2: "it ends at its editorial-questions section, so the comparison behind it cannot be shown to have finished."
- r3: "ends after its editorial questions with no completion status and no statement of unresolved findings, so it is partial however whole its accounting reads."

The route continued not to be the obstacle in either case: every arm-2 validator said the report arrived as reply text and that this alone settled nothing.

## An observation the arms produced without being asked for it

Three validators — `arm-1/v-truncated-r1`, `arm-1/v-truncated-r2` and `arm-2/v-complete-r1` among them — followed the rule's instruction to save the reply text to the report path and found that path unwritable too, because this diagnostic stages one directory for both roles. In a real run the writer's own scratch is writable, which is the case the rule is written for. No run treated the failed save as an obstacle to the comparison, and none changed the directory's permissions.

## Criteria, one by one

| Criterion | Result |
| --- | --- |
| **R**, checker arm: three of three return the complete report in the reply, ending with the completion status and any unresolved findings, and say the file could not be written and why | **Met**, 3 of 3 |
| **V**, validator arm: `v-complete` answers complete and `v-truncated` answers incomplete with no `DRAFT:` line, three runs of each | **Missed in arm 1** (`v-truncated` 0 of 3), **met in arm 2** (3 of 3 and 3 of 3), after the one declared revise-and-remeasure round |
| **A**, absence: the before-and-after inventory shows no file created under `reports/` | **Met** |
| **C**, cost: wall time per run | Checker 169–310 s, median 179 s. Validator 61–139 s, median 96 s |

## What this does not show

- **A Harness refusal was not retested.** The mechanism here is the filesystem. What the two share is the situation the checker meets; that Claude Code's permission system produces the same behaviour under the shipped task is inferred from #362's own two runs, not measured here.
- **No `/write` run was made.** These are checker-level and writer-level arms against a frozen fixture. Nothing here says what a whole run does end to end, and nothing here is a corpus evaluation, which is why no record under `../records/` is written.
- **One fixture, one language, one family.** `p2-chronology`, en_US, Claude. A checker whose comparison yields no findings at all, a Swedish fixture, and the GPT family are untested for this rule.
- **The first wording is evidence too.** Three validators reading a plain statement of the rule the way arm 1 did is a measured fact about this family, and it is why the shipped sentence names the failure rather than only stating the rule.
