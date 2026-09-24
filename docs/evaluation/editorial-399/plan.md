# `case-study-clean` five times per arm — evaluation plan for #399

Frozen on 2026-09-24, before the first run of this evaluation. Nothing in this file, in the two turn files beside it, in the judge brief beside it, or in the three scripts under `runs/` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first, then [#383's plan](../editorial-383/plan.md), whose per-run staging, judging and counting this plan re-uses as they stand. This file says only what that plan leaves open and what this ticket settles differently.

## What is under test

[#383](../editorial-383/results.md) ran the control `case-study-clean` once against its post-change install and once against its pre-change install. The post-change run rewrote the conforming subheading `## Två perioder med olika arbetsbelastning` and both judges failed `R1`; the pre-change replay passed on both judges. One run per arm cannot separate variance from a caused regression. [#399](https://github.com/Kntnt/skills/issues/399) asks which it was.

This is a measurement, not a repair. No shipped file changes on any outcome, and there is no candidate.

## The two installs

- **Pre-change install:** `git archive 3167fb68`, the tree #383 began on.
- **Post-change install:** `git archive 5af1390d`, the tree object #383's record names for its post-change arm. For every staged path it matches `c26fd8c5`.

Current `main` is never staged: it has moved since #383 in files Redline loads, and an install from it would differ from the pre-change install in more than #383's six files.

Each install is extracted flat under this ticket's scratch root, `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/399.scratch`, so that it holds `write/`, `redline/`, `proofread/`, `unslop/` and `kntnt/` side by side and the shim finds `HERE.parent / "kntnt"`:

```sh
git archive <rev> skills/editorial/write skills/editorial/redline skills/editorial/proofread skills/editorial/unslop | tar -x -C <install> --strip-components=2
git archive <rev> skills/kntnt | tar -x -C <install> --strip-components=1
```

`<install>` is `…/399.scratch/install-pre` for `3167fb68` and `…/399.scratch/install-post` for `5af1390d`. Both hold 84 files. They differ in nine: Redline's `SKILL.md`, `help.md` and `references/correction.md`, the Library's `anti-slop.md` and `base.review.md`, `kntnt/catalog.json`, and Unslop's `SKILL.md`, `help.md` and `references/correction.md`. Redline does not load Unslop's three, so the six files the ticket names are the whole difference Redline sees. Neither install is ever copied from a working tree, and neither `.git/orchestrate-session-383-389-claude/383.scratch/install-{pre,post}` nor any other earlier staging is used.

## The seat

Every run, every correction subagent and nested Proofread pass a run starts, and every judge is a fresh `kntnt-opus-high` subagent, which launches **`claude-opus-5-5` at high deliberation**, in Claude Code 2.1.281. Where #383's plan says `claude-opus-5`, read `claude-opus-5-5`; that substitution is the only change of seat and not a change of method. The dispatching session is itself on `claude-opus-5-5`; runs and judges are delegated so that each is fresh and carries nothing of this session's knowledge of the ticket.

So both arms here compare with each other, and neither compares with #383's single miss, which ran on `claude-opus-5`. Every outcome statement this evaluation writes says it was measured on `claude-opus-5-5`, and adds: "#383's miss on `claude-opus-5` is not re-tested."

## How a run is made

The two turn files beside this plan, [`redline-turn-pre.md`](redline-turn-pre.md) and [`redline-turn-post.md`](redline-turn-post.md), are #383's with two substitutions and no other change: the install path, and the sentence naming the checkouts a run may not read, which now names `/Users/thomas/Projects/skills` and this ticket's worktree `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/399`. [`control-judge-brief.md`](control-judge-brief.md) is a byte copy of #383's. `redline-judge-brief.md` is not used, because no run here is on a #362 draft.

- **Input:** [`../corpus/editorial-quality/controls/case-study-clean.md`](../corpus/editorial-quality/controls/case-study-clean.md), copied byte for byte to the run's `work/input.md`.
- **Invocation:** `/redline --genre=case-study --language=sv --output=response input.md`.
- **Expectation:** [`../editorial-383/runs/control-case-study-clean/expectation.md`](../editorial-383/runs/control-case-study-clean/expectation.md), copied byte for byte to the run's `expectation.md`.

Each run executes under the scratch root at `…/399.scratch/runs/<run>`, holding `work/input.md` and nothing else when its turn is dispatched, and `expectation.md` beside `work/`. The run subagent's dispatching message is the turn file's text, followed by exactly three lines:

```text
Working directory: …/399.scratch/runs/<run>/work
Run directory: …/399.scratch/runs/<run>
The user typed: /redline --genre=case-study --language=sv --output=response input.md
```

No other statement is added, and no hint of the defect under investigation appears in any turn, invocation or judge message.

The run directory is copied into `runs/` beside this plan only after both judges have written.

## The matrix, the names and the order

| Run | Install |
| --- | --- |
| `case-study-clean-01` | pre-change, `3167fb68` |
| `case-study-clean-02` | post-change, `5af1390d` |
| `case-study-clean-03` | pre-change, `3167fb68` |
| `case-study-clean-04` | post-change, `5af1390d` |
| `case-study-clean-05` | pre-change, `3167fb68` |
| `case-study-clean-06` | post-change, `5af1390d` |
| `case-study-clean-07` | pre-change, `3167fb68` |
| `case-study-clean-08` | post-change, `5af1390d` |
| `case-study-clean-09` | pre-change, `3167fb68` |
| `case-study-clean-10` | post-change, `5af1390d` |

Odd numbers are the pre-change arm and even numbers the post-change arm. The runs go in numeric order, **one at a time, never two at once**: #401 is open, and several copies of one input running together are its conditions.

**The shared lock.** Ticket #397's builder runs `case-study-clean` through Redline in the same session scratchpad at the same time. Before each run this evaluation takes the lock `mkdir /Users/thomas/Projects/skills/.git/kntnt-orchestrate-runB-locks/case-study-clean`, waiting and retrying every 30 seconds while it exists, and removes it with `rmdir` as soon as that run's reply has arrived. The lock is never held across more than one run. A file in the session scratchpad that the sibling's runs wrote is not this evaluation's output: any such entry is attributed by its path and its run's own report, and never scored against a run here.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload, or a run that reports a file it wrote changed or deleted under it by another process, is void, not a finding. A void run is moved to `runs/void/`, is not judged, and is redone under the same number. A void judge is dispatched again.

`staged_run.py` is not used: no criterion here is answered from a Harness trace.

## Judging

Two independent judges per run, `a` and `b`, each a fresh `kntnt-opus-high` subagent, dispatched together once all ten runs are made, blind to the arm, to the model, to the expected verdict and to this ticket. Each judge's dispatching message carries the text of [`control-judge-brief.md`](control-judge-brief.md), its letter, the run directory's scratch path (`…/399.scratch/runs/case-study-clean-NN`, which names neither arm), the **Frozen expectation** paragraph copied from `expectation.md`, the path of that `expectation.md`, and the instruction to keep any scratch of its own inside that run directory and to remove it before finishing. The number `399` in the scratch path is this ticket's orchestration directory, as `383.scratch` was #383's, and says nothing about the arm.

Where the two judges of a run split, both verdicts are recorded and neither is an oracle; the rules below decide what a split means for each criterion.

## What each run records

- **`R1`** — each judge's verdict under heading 4 of the control brief, recorded per judge for every run.
- **`C1`** — **a run misses `C1` when either judge, or both, fails `R1`** against the frozen expectation. This rule decides a split on `C1`, and it departs from #383's plan, whose split rule governs `A1` only.
- **`A1`**, the five post-change runs — derived by the evaluator from both judges' *Differences* and *The account* sections by #383's counting rule: *a difference counts against a run when both judges class it as taste outside any finding, or when either does and the reply covers it neither in the claim account nor in the closing summary.* A judge's "change of taste" is how a difference outside any finding reaches this rule, as in #383. A mechanical correction never counts. `A1` holds when no difference counts against the run.
- **`A2`**, the five post-change runs — derived per judge by #383's definition: the judge finds no statement false against the returned text, and no kind of difference the account leaves uncovered. Both judges holding it is `pass`, neither is `fail`, and one of two is recorded as a **split**, which affects no outcome.
- **`A1` and `A2`**, the five pre-change runs — `skipped`: #383's plan defines them on post-change runs only, and `A1` tests a closing summary the pre-change product does not have.
- **`O1`** and **`S1`** — from the inventories, as #383's plan defines them.
- **`T1`** and **`R2`** — `skipped` on every run, for the reason #383's plan gives: both are answerable only from a Harness trace, and a session cannot read the transcript of a subagent it started.
- **Every other criterion** the corpus applies to a run of this kind — `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `N1`, `N2`, `C2` — `skipped`, not this evaluation's.

Every miss counts in this evaluation's tallies, whichever other ticket's behaviour it shows. A miss that shows a behaviour #397, #398, #400, #402 or #415 was filed against is also named under that ticket's number in the run's entry, with both judges' readings; that does not remove it from the counts.

## Reading the result

Count `C1` misses per arm, out of five. An arm falls in one of three bands:

- **majority** — 4 or 5 misses;
- **middle** — 2 or 3 misses;
- **minority** — 0 or 1 miss.

Exactly one of these is named as what the measurement shows:

- **First outcome, the cause is in #383's six files** — post-change 4 or 5, and pre-change 0 or 1. One `needs-triage` ticket is filed naming #399 and listing all six files as candidates — Redline's `SKILL.md`, `help.md` and `references/correction.md`, and the Library's `anti-slop.md`, `base.review.md` and `catalog.json` — without attributing the miss to any one of them. There is no bisection.
- **Second outcome, the headline contract's authority over a subheading that already conforms** — both arms miss at least once, both counts fall in the same band, and the post-change count is at least the pre-change count. As post / pre, that is exactly 1 / 1, 2 / 2, 3 / 2, 3 / 3, 4 / 4, 5 / 4 and 5 / 5. `results.md` and the record say that the miss belongs to the headline contract's authority over a subheading that already conforms, and name #397 and #400. No ticket is filed.
- **Third outcome, the single miss was variance** — 0 and 0. Recorded as measured; no ticket is filed.
- **Inconclusive** — every other pair, including any pair where the pre-change arm misses more often than the post-change arm (post 2 against pre 3, post 4 against pre 5 among them). Recorded as inconclusive with both counts, never as a pass or as one of the three outcomes; no ticket is filed.

No revise round and no extra runs follow on any outcome, and no decision record is written: this ticket never had a product change to withhold.

## Inventory scope

`O1` and the `side effects` field are read from `sha256` inventories, never from a run's report of itself. [`runs/inventory.sh`](runs/inventory.sh) and [`runs/run_inventory.sh`](runs/run_inventory.sh) are byte copies of #383's. [`runs/wave_inventory.sh`](runs/wave_inventory.sh) is #383's with two substitutions: the scratch root is this ticket's, and the repository list names this ticket's worktree in place of `/Users/thomas/Projects/skills-388-391`, which no longer exists. `inventory.sh` is copied to `…/399.scratch/evaluator/` before the first inventory, where `wave_inventory.sh` calls it.

1. **The run directory**, including `work/` and any `scratch/`.
2. **The staged install** the run reads.
3. **The whole scratch root**, both installs and every other run directory among them.
4. **Both checkouts**, `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/399` and `/Users/thomas/Projects/skills`, by `git status --porcelain --untracked-files=all` and `git rev-parse HEAD`, as #383's plan declares. The script is run with `GIT_OPTIONAL_LOCKS=0` in its environment so that a status call never refreshes another session's index; that is how it is invoked, not a change to it.

Scopes 1 and 2 are taken immediately before each run's turn is dispatched and immediately after its reply arrives, into the run's `inventory-before.txt` and `inventory-after.txt`. Runs are sequential, so each run is its own wave: scopes 3 and 4 are taken around every run into `runs/wave-NN-{before,after}-{scratch,repo}.txt`, `NN` being the run's number.

The session scratchpad a correction subagent may write to is outside every scope, as it was in #383, and is shared with the sibling's runs. What a run reports writing there is recorded in its notes.

## What each run directory holds

```text
runs/case-study-clean-NN/
  work/
    input.md
  response.md                  the user-facing reply, verbatim
  expectation.md               the frozen expectation, byte for byte
  inventory-before.txt
  inventory-after.txt
  judgement-a.md
  judgement-b.md
```

## What is written down

[`results.md`](results.md) holds the mapping above, every run's per-judge `R1`, its `C1`, and on post-change runs its `A1` and `A2`, the two counts, the outcome and the reasoning. The record goes to `../records/redline-claude-2026-09-24-399.md`, in the protocol's format. Its line for `../records/README.md` is appended by the run that integrates this work, from this ticket's note file, not by this evaluation. Nothing else already under `docs/evaluation/` changes, `../corpus/editorial-quality/README.md` and `../editorial-383/runs/control-case-study-clean/expectation.md` among it.
