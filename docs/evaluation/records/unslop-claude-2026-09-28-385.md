# unslop — claude — 2026-09-28 — #385

- **record** — `unslop-claude-2026-09-28-385`
- **date** — `2026-09-28`
- **ticket** — `#385`
- **skill** — `unslop`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session and the one correction subagent in it, and every judge
- **harness** — Claude Code 2.1.281
- **corpus commit** — `c211a1d5`

## Run conditions

The plan is [`../editorial-385/plan.md`](../editorial-385/plan.md), and the outcome is [`../editorial-385/results.md`](../editorial-385/results.md). The plan was first frozen at `e3723890`. A first wave of the four pre-change runs was made against it on 2026-09-24, and after those runs `0d7fd057` respelled one line of it for the collection's flag grammar. That wave is therefore void, is not recorded here, and is kept under `../editorial-385/runs/voided/wave-1/` with the reason. The plan was frozen again at `4d10e603`, and every run in this record was made after that commit. Neither the plan, the two turn files nor the two judge briefs was edited after the first of these runs.

The pre-change arm was staged from `c211a1d5`, the commit #385's build began from. It holds `unslop/` and `kntnt/` side by side, written by `git archive`, and the shim printed a `$LIBRARY` under the install. Each run was a fresh top-level session started by [`../editorial-385/runs/run_turn.sh`](../editorial-385/runs/run_turn.sh) with `claude --print --safe-mode --model=claude-opus-5-5 --effort=high`. Its prompt was the turn file [`../editorial-385/unslop-turn-pre.md`](../editorial-385/unslop-turn-pre.md) and the invocation, and its working directory held only `input.md`. Each artefact was judged by two fresh `kntnt-opus-high` subagents, blind to the arm, the model and the ticket, under [`../editorial-385/unslop-judge-brief.md`](../editorial-385/unslop-judge-brief.md), each working from a neutral `mktemp -d` directory.

This evaluation's criteria are `N1`, `N2`, `O1` and `S1` on the draft runs, and `C1` on the controls; where the two judges split, the stricter governs. The pre-change arm was run and judged first. It had no `N1` miss, so:

- the defect is recorded as not reproduced;
- the post-change arm and the controls were not run;
- the candidate `d84b20ae` stays reverted by `18757082` (ADR-0221).

Every entry below records `T1` and `R2` as `skipped`, because this ticket's scope runs Unslop through turn files and answers no criterion from a Harness trace. It records the editorial-quality corpus's `R1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` as `skipped`, because they are Redline's and Write's and do not apply to Unslop.

## `pre-column-sv-r1`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, pre arm, staged from `c211a1d5`
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the Swedish no-change status, *Ingen ändring: anti-slop-granskningen fann inget att rätta i texten.*, and no text.
- **side effects** — `none`: between the run's two inventories `work/input.md` and the staged install's digest are unchanged, and the only new file in the run directory is the evaluator's `response.md`; the wave's inventories show both checkouts unchanged.
- **criteria** —
  - `N1` — `pass` — both judges find no difference, and each lists seven limiting sentences, borderline cases included, every one kept.
  - `N2` — `pass` — there is no difference, so no change to what a claim says.
  - `O1` — `pass` — the response target was honoured and nothing was written beside the source.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — this ticket's scope answers no criterion from a Harness trace.
  - `R1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — Redline's and Write's criteria; they do not apply to Unslop.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — one Bash call failed, a `git status` on the working directory, which lies inside the repository's git directory; that is a failed command, not an interruption; an empty `scratch/` directory, the one the turn names, is left in the run directory with no file in it

## `pre-column-sv-r2`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, pre arm, staged from `c211a1d5`
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the Swedish no-change status, *Ingen ändring: `input.md` (språk: svenska, `sv`, från textens `kntnt`-karta) har inga anti-slop-fynd, så texten behövde inget arbete och ingen korrigering gjordes.*, and no text.
- **side effects** — `none`: between the run's two inventories `work/input.md` and the staged install's digest are unchanged, and the only new file in the run directory is the evaluator's `response.md`; the wave's inventories show both checkouts unchanged.
- **criteria** —
  - `N1` — `pass` — both judges find no difference, and list seven and six limiting sentences respectively, borderline cases included, every one kept.
  - `N2` — `pass` — there is no difference, so no change to what a claim says.
  - `O1` — `pass` — the response target was honoured and nothing was written beside the source.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — this ticket's scope answers no criterion from a Harness trace.
  - `R1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — Redline's and Write's criteria; they do not apply to Unslop.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — an empty `scratch/` directory, the one the turn names, is left in the run directory with no file in it

## `pre-opinion-en_GB-r1`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, pre arm, staged from `c211a1d5`
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the English no-change status, *No change needed.* …, and no text.
- **side effects** — `none`: between the run's two inventories `work/input.md` and the staged install's digest are unchanged, and the only new file in the run directory is the evaluator's `response.md`; the wave's inventories show both checkouts unchanged.
- **criteria** —
  - `N1` — `pass` — both judges find no difference, and list ten and eleven limiting sentences respectively, every one kept, *I am not against digital booking.* and *We make no claim to have funded or costed that trial.* among them.
  - `N2` — `pass` — there is no difference, so no change to what a claim says.
  - `O1` — `pass` — the response target was honoured and nothing was written beside the source.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — this ticket's scope answers no criterion from a Harness trace.
  - `R1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — Redline's and Write's criteria; they do not apply to Unslop.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `pre-opinion-en_GB-r2`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, pre arm, staged from `c211a1d5`
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text after one correction round on one synonym-cycling finding, with *channel(s)* replaced by *route(s)* in three places on two lines, an account saying no claim was removed, changed or added, and a closing **What changed:** paragraph.
- **side effects** — `none`: between the run's two inventories `work/input.md` and the staged install's digest are unchanged, and the only new file in the run directory is the evaluator's `response.md`; the wave's inventories show both checkouts unchanged.
- **criteria** —
  - `N1` — `pass` — both judges find three differences, all pattern repairs changing no element of a claim, and list thirteen limiting sentences each; two host sentences changed one noun outside their limiting clauses, which both judges record kept word for word and, read conservatively as recast, in class (a) on a pattern inside the sentence; *I am not against digital booking.* and *We make no claim to have funded or costed that trial.* kept.
  - `N2` — `pass` — both judges class all three differences as pattern repairs that change no element of a claim, and find all three reported accurately.
  - `O1` — `pass` — the response target was honoured and nothing was written beside the source.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — this ticket's scope answers no criterion from a Harness trace.
  - `R1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — Redline's and Write's criteria; they do not apply to Unslop.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — the correction subagent's round was accepted

## `post-column-sv-r1-a`

- **fixture** — `column-sv-r1`, post arm — not run
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the post-change arm is not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `post-column-sv-r1-b`

- **fixture** — `column-sv-r1`, post arm — not run
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the post-change arm is not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `post-column-sv-r2-a`

- **fixture** — `column-sv-r2`, post arm — not run
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the post-change arm is not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `post-column-sv-r2-b`

- **fixture** — `column-sv-r2`, post arm — not run
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the post-change arm is not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `post-opinion-en_GB-r1-a`

- **fixture** — `opinion-en_GB-r1`, post arm — not run
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the post-change arm is not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `post-opinion-en_GB-r1-b`

- **fixture** — `opinion-en_GB-r1`, post arm — not run
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the post-change arm is not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `post-opinion-en_GB-r2-a`

- **fixture** — `opinion-en_GB-r2`, post arm — not run
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the post-change arm is not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `post-opinion-en_GB-r2-b`

- **fixture** — `opinion-en_GB-r2`, post arm — not run
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the post-change arm is not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `control-slop-heavy-review`

- **fixture** — `slop-heavy`, control — not run
- **invocation** — `/unslop --max=0 --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the controls, which guard a candidate, are not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `control-slop-heavy`

- **fixture** — `slop-heavy`, control — not run
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the controls, which guard a candidate, are not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `control-slop-heavy-sv-review`

- **fixture** — `slop-heavy-sv`, control — not run
- **invocation** — `/unslop --max=0 --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the controls, which guard a candidate, are not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `control-slop-heavy-sv`

- **fixture** — `slop-heavy-sv`, control — not run
- **invocation** — `/unslop --language=sv --max=1 --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the controls, which guard a candidate, are not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `control-clean-en-GB`

- **fixture** — `clean-en-GB`, control — not run
- **invocation** — `/unslop --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the controls, which guard a candidate, are not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `control-flawed-en-US`

- **fixture** — `flawed-en-US`, control — not run
- **invocation** — `/unslop --max=0 --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the controls, which guard a candidate, are not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none

## `control-flawed-sv`

- **fixture** — `flawed-sv`, control — not run
- **invocation** — `/unslop --max=0 --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none: not run.
- **side effects** — none: not run.
- **criteria** —
  - all — `skipped` — the pre-change arm had no `N1` miss, so the plan's exit is not reproduced and the controls, which guard a candidate, are not run.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — none
