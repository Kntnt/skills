# Focused behavioural regression for #376 — plan

Frozen on 2026-09-20, before the first run below. This packet is governed by [`../README.md`](../README.md) and not by the corpus protocol or its `records/` format.

Product under test: the working tree at `4a932dd6` with `skills/editorial/write/` changed for #376, staged as a byte copy beside `skills/kntnt`, exactly as [`../../editorial-376/plan.md`](../../editorial-376/plan.md) stages the main arm. Every run and every judge is a fresh `claude-opus-5` subagent at high deliberation. Provider family `claude`; no Codex Harness and no GPT model is started from this session.

## Why this packet exists, and what it is not

The main arm measures the delivery outcome at the final comparison on the corpus `opinion` source in `en_US`. Three requirements this ticket absorbed from #381 are not reachable from that row, because they turn on a file Output Target, on a comparison that cannot finish, and on the boundary between a commissioning party's standpoint and a factual assertion. They are measured here instead, bounded and declared in advance.

This is not a second genre or locale sweep and not a re-run of anything. Three seams, four runs, one blinded judgement. The client material behind the incident reported in #381 is not published here: the fixtures are synthetic and unrelated.

## The seams, and what each run verifies

### R-A — a file target, remaining findings, and markings asked for in the document

One `/write` run. Working directory holds `source.md`, a byte copy of [`fixtures/cargo-pilot-source.md`](fixtures/cargo-pilot-source.md). Invocation:

```
/write --genre=article --language=en_GB --output=article.md source.md -- Mark any remaining findings in the document itself, so I can see which passages they touch.
```

The fixture plants the three kinds of late finding the #381 report describes, in an unrelated synthetic setting: a published objective whose percentage is attached to two conjoined things (`routing and loading`); a company expectation about noise beside project sources that document monitoring but not the expectation; and a design fact that supports flat loading and lower maintenance while easy service access is already in the design.

Verified, from the filesystem after the run and from the reply:

1. `article.md` exists and holds a complete article after the run's own cleanup.
2. The prose in it is byte-identical to the prose the last comparison read, once the markings and the Handoff Metadata are set aside.
3. Where a finding remained, each marking is separable from the prose and names the passage, the problem, what the material carries, and the smallest repair the checker proposed.
4. Nothing the run created besides the Output Target and the markings survives, and no scratch holding the draft was the only copy at any exit.

Where the final comparison leaves no finding, 3 is recorded **not exercised** rather than passed, and 1, 2 and 4 are recorded as they fall. A run cannot be made to find a defect, and a regression that reported an unexercised criterion as passed would be worse than one that reported nothing.

### R-B — a comparison that cannot finish

One `/write` run, the same fixture and genre, `--output=article.md`, no Contextual Instruction. The run directory's `scratch/` is created in advance with mode `0500`, so the writer cannot save the prose for a checker to read and no complete comparison of the current prose can exist. This is the #378 situation — the Harness refusing the checker's file writes — forced rather than waited for.

Verified: the Output Target is left unwritten; the current prose is preserved at a distinct path beside it whose name cannot be mistaken for the requested artifact; the reply reports that path, the comparison status and what was and was not compared; and the preserved prose is not presented as checked or delivered. A stop that leaves no reachable copy of the draft is the failure this seam exists to catch.

### R-C — a standpoint, a generalisation and a number

Two independent checker runs, each a fresh subagent given the comparison task from the shipped `source-check.md` verbatim, the material [`fixtures/cargo-pilot-source.md`](fixtures/cargo-pilot-source.md), and the draft [`fixtures/standpoint-draft.md`](fixtures/standpoint-draft.md). The checker is given no expectation and no ticket. The task is at [`tasks/checker-task.md`](tasks/checker-task.md), copied from the shipped file before the first run.

Four passages, fixed here before the runs:

| Passage | What ought to happen |
| --- | --- |
| `Everybody finds delivery vans in a city centre ugly and intrusive, the company says, and a quiet street is simply a better street; cargo cycles are, in its view, the right answer` | Not a defect with a repair. The brief carries it as the commissioning party's own standpoint, and it is expressed as theirs. An editorial question about the reach of "everybody" is acceptable; a demand for external evidence is not. |
| `Residents agree. Delivery vans are unpopular wherever they park.` | A finding. A claim about an actual population, asserted by the writer rather than attributed, with nothing in the material behind it. |
| `a 25 % reduction in kerbside dwell time through improved routing` | A finding. The objective attaches the figure to routing **and** loading. |
| `412 deliveries were made by cycle — 40 % more than the vans managed on the same streets` | A finding. The operator states it makes no claim about that comparison. |

One blinded judge reads both reports against these four rows without being told which answer is expected for which passage, and classes each report row. The seam passes where the standpoint draws no repair in either run and the three factual passages are found in both; it is reported as it falls otherwise.

## What is reported

Per run: what was invoked, what reached the filesystem before and after (a `sha256` inventory over the run directory and the staged install), the number of comparisons, the wall time, and the verdict on each numbered item above. Incomplete coverage is marked as such. No further round is run and no criterion is softened to fit a result.
