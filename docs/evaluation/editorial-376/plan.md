# Real Skill runs for #376

Frozen on 2026-09-20, before the first run below. Nothing in this file or in [`criteria.md`](criteria.md) changed after the first run started.

Product under test: the working tree at `4a932dd6` with `skills/editorial/write/` changed for #376 — the delivery outcome of the final source comparison, the preservation rule on a stop, the placement of remaining findings, and the standpoint-and-fact boundary in the comparison task. Nothing else in the Collection differs from `4a932dd6`. `source-check.md` is 989 words before the change and 1 568 after.

## What this arm measures, and what it does not

The ticket decided the contract; this arm measures whether a real run obeys it. Three criteria here measure a model rather than a file: that no run delivers prose no comparison has read, that no run stops on an accepted finding alone, and that a run reaching that situation delivers the prose the last comparison read with each remaining finding named beside it.

Provider family `claude`, per [`../protocol.md`](../protocol.md). No Codex Harness and no GPT model is started, controlled or invoked from this session, so the GPT-family retest of #362 stays Thomas's own step and nothing here touches `../editorial-329/harness/`.

Out of scope, and not run: any other locale, any other genre, any paired `/redline` run — what Redline does to these drafts is #377's — and any checker-level diagnostic. The three focused behavioural regressions for preservation, in-document markings and the standpoint boundary have their own frozen plan at [`../regressions/376/plan.md`](../regressions/376/plan.md) and are not part of this arm.

## How a run is made

Each run is one fresh subagent with no history, of type `kntnt-opus-high` (`claude-opus-5`, high deliberation); the checkers it starts inherit that seat, as `source-check.md` says. The session's own seat is `claude-opus-5[1m]`. A run on a weaker seat measures the seat instead of the product, and the wall times this arm is compared against are that seat's.

The staged copy is not an installed Skill, so the Skill tool cannot start it. As in [`../editorial-362/runs/plan.md`](../editorial-362/runs/plan.md), the turn names the staged `SKILL.md` as its instructions and `$HERE` as its directory, and carries the Formal Invocation verbatim. The staged install is a byte copy of `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` side by side, so the shim finds the Manager beside the Skill and the global install is never read. Each run has its own working directory holding only `source.md`, a byte copy of `../corpus/editorial-quality/sources/opinion.md`.

Two evaluator instructions are added to the turn and declared here because they are not the Skill's: copy the source-check scratch directory to `evidence/` before removing it, and save the user-facing reply verbatim to `response.md` in the run directory. The turn is [`runs/write-turn.md`](runs/write-turn.md).

A `sha256` inventory is taken before and after each run over every writable location staged for it: the whole run directory and the staged install. It is what `side effects` is read from, never the Skill's own report of itself.

## Matrix

| Row | Invocation | Source | Runs |
| --- | --- | --- | --- |
| `opinion-en_US-r1` … `-r3` | `/write --genre=opinion --language=en_US --output=response source.md` | corpus `opinion.md` | 3 |

Exactly three runs and nothing else. The same row and the same source as the two `opinion-en_US` rows of [`../editorial-362/runs/results.md`](../editorial-362/runs/results.md), which both stopped, so the arms are read side by side.

## The refused write

In two of the nine #362 runs the Harness refused the checkers' file writes and only the drafts reached `evidence/`; `source-check.md` assumes the file, and that is #378's. Declared here before the first run: a run whose evidence the Harness truncates is kept and recorded with the gap named, the criterion it affects is recorded `skipped` with that reason, and that row is re-run once, both runs kept.

## Criteria, fixed before the runs

Judged by fresh judges per run from the source and the artefacts, without the ticket, the decision, this plan or any model identity. Two independent judges wherever a criterion turns on a judgement, each blind to the expected answer; both classes are recorded where they split. One judge suffices for a mechanical check — byte-identity, a comparison count, the presence of a report or of a named finding. The judge brief is [`runs/run-judge-brief.md`](runs/run-judge-brief.md).

- **F1**, **G2**, **L1** on the delivered draft, from [`../corpus/editorial-quality/README.md`](../corpus/editorial-quality/README.md); on a stopped run, on the last draft in the evidence, marked as not delivered. For this row, F1 includes: no unsupported date, scope, personal attribute or event; unknown kept apart from absent; where the draft says what the pilot report does not measure, the third item is habit, familiarity or experience, not skill or ability.
- **`gate`**, holding the delivery rule in `source-check.md` as #376 changed it: at most two comparisons; no prose change after the final comparison, the checker's own proposed wording included; a completed final comparison that left an accepted defect or a genuinely unresolved material claim delivers the prose that comparison read and reports each remaining finding beside the draft with the smallest repair the checker proposed; a stop only where no complete comparison of the current prose exists.
- **`effects`**, the protocol's side-effect check, read from the inventories.
- **`T1`** and **`R2`** are recorded `skipped` in every run, with the reason that a subagent's Harness trace is not readable from the session that started it. Neither is claimed passed and no run fails for lacking them.

## What decides this ticket, and what does not

`F1` is recorded as it falls. The protocol hard-fails an unsupported fact and forbids a criterion that would let one pass; this contract delivers prose whose residual the delivery account names, so a run that delivers with a remaining accepted finding takes an `F1` `fail` for the named passage, with the residual and the checker's proposed repair quoted. That is this contract working. A residual the delivery account names earns no `needs-triage` ticket; a residual no account names is one.

What decides this ticket is its own two criteria: that the delivered prose is byte-identical to the prose the last comparison read, and that the account names each remaining finding with its proposed repair.

## Revise and remeasure, once

Where a run delivers prose no comparison has read, or stops on an accepted finding alone, the builder gets one revise-and-remeasure round: a second arm of three runs, with its own plan and results file here and its own record, and this arm's plan, results and record left exactly as they are. If a criterion is still unmet after that round, the measured result is recorded as measured, the wording that ships is the arm with fewer runs missing either of the two criteria above — and, where the arms tie, the wording measured first — the remaining miss is filed as its own `needs-triage` ticket naming #376, and the ticket is done. No criterion is softened to fit a result, and no further round is run.

Where none of the three runs reaches the situation at all, the record says so and reports those two criteria as unverified rather than as passed.

## What is reported

Per run: the number of comparisons, the wall time, whether a draft was delivered, and whether the delivered prose is byte-identical to the prose the last comparison read — beside the figures [`../editorial-362/runs/results.md`](../editorial-362/runs/results.md) records for its two `opinion-en_US` rows (1 024 s and 963 s, both stopped after two comparisons) and its median of 896 s over nine runs.
