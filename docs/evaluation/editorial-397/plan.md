# Plan for #397: a review reports a part the text lacks, and repairs a part it has

Frozen on 2026-09-24, before the first run of either arm and before any product change. Nothing in this file, in the two turn files beside it or in the two judge briefs beside it is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first, then [#383's plan](../editorial-383/plan.md), whose method this one re-uses; this file says only what that plan leaves open and what #397 settles differently.

**`<start>` is `20133068`**, the head of the branch `kntnt-orchestrate/main/397` when the build began. The pre-change arm is staged from it. **The corpus commit is `a321690f`**, the commit before this plan's, which revises three clauses of two corpus rows and nothing else (see *The corpus rows*). Both arms read their inputs and their expectations from it.

The requirement is the ticket's thread as it stood on 2026-09-23: the body, the triage addendum of 2026-09-22, the addendum of 2026-09-23 19:21 UTC on the block, the readiness addendum of 19:45 UTC and the clarifications of 19:50 UTC. Where they conflict the later one stands.

## What is under test

The four #362 drafts carry no standfirst, no subheadings and, in three of them, no call to action. The article anatomy requires all three, and Redline as `<start>` ships it answers the absence by writing the missing parts into the finished text: a standfirst written about the bylined author in the third person, subheadings imposed on a body of three to seven paragraphs, a closing exhortation in the author's own voice after her deliberate ending, and a headline reworded to reach a word or character band. In [#383's](../editorial-383/results.md) twelve runs on those drafts, `R1` failed on all twenty-four judgements on the clause *clean texts may not be rewritten to satisfy taste or numerical guidelines*.

Thomas's ruling on the ticket is the specification and is not open here: **a review reports a part the text does not have, and repairs a part the text has.** The candidate states it in the review extension `article-anatomy.review.md` as points 1 to 8 of the readiness addendum's *The rule*, adds one sentence to `article-anatomy.md` after *"Limits are exact; verify each one by counting."*, and sweeps Redline's `SKILL.md` step 7, `genres/article.review.md` and the correction brief so that none of them still has a reviewer or a correction agent write a part the text lacks. Its exact wording is written after the pre-change arm has been judged and is recorded in `results.md` with its commit. The ruling ships whatever this measurement shows; the measurement decides which wording ships where a revise round is taken, and what is written down.

## The corpus rows

Before this plan was frozen, commit `a321690f` revised three clauses of the *Redline controls* table, as the readiness addendum and its clarifications require, and nothing else in the file:

- `article-flawed`: *"The missing navigation is reported, not written, and no measured fact, exclusion or funding uncertainty is deleted."*
- `column-flawed`: *"no standfirst, which is reported, not written;"* and *"no call to action, reported and not written."*

Every control's `expectation.md` in both arms is its row's *Frozen expectation and rejection* cell at `a321690f`, copied verbatim.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

**The seat.** Each run is one fresh subagent of type `kntnt-opus-high`, which launches **`claude-opus-5-5` at high deliberation**. The correction subagents and the nested Proofread pass a run starts inherit that seat. Every judge is a fresh subagent of the same type. Where #383's plan says `claude-opus-5`, this evaluation launches `claude-opus-5-5`, as the readiness addendum settles; the dispatching session is itself `claude-opus-5-5`.

**The installs.** Two installs, each written with `git archive` from the commit it names and never copied from a working tree, extracted flat so that each Skill's directory and `kntnt/` stand side by side and the shim finds `HERE.parent / "kntnt"`:

```
git archive <commit> skills/editorial/write skills/editorial/redline skills/editorial/proofread skills/editorial/unslop | tar -x -C <install> --strip-components=2
git archive <commit> skills/kntnt | tar -x -C <install> --strip-components=1
```

`skills/kntnt` takes one component where the editorial Skills take two, because stripping two from it would scatter the Manager's own files into the install root; the result is the layout the addendum describes.

- `…/397.scratch/install-pre` — `<start>`. Used by [`redline-turn-pre.md`](redline-turn-pre.md).
- `…/397.scratch/install-post` — the committed candidate. Used by [`redline-turn-post.md`](redline-turn-post.md).
- `…/397.scratch/install-revise` — the committed revised candidate, only if a revise round is taken. Its turn is `redline-turn-post.md` with `install-post` read as `install-revise`, which is a path substitution and nothing else.

`…` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate`, and `397.scratch` is this build's scratch directory.

**The turns.** The two turn files are #383's with paths substituted and nothing else changed: the staged install's path, and the second checkout the run may not read, which is now `/Users/thomas/Projects/skills-rework` since `/Users/thomas/Projects/skills-388-391` no longer exists. The message dispatching a run names the turn file, the run's working directory, the run directory and the invocation, and carries nothing else. No hint of the defect under investigation appears in any turn, in any invocation or in any judge brief.

**Where runs execute.** Each run's directory is `397.scratch/runs/<run>/`, with its working directory `work/` holding only `input.md` when the turn is dispatched. After both judges of a run have written, its directory is copied into this evaluation's `runs/<run>/`.

**No two runs on one input at a time** (#401). The two post-change runs on each draft are made one after the other. A sibling build, #399's, runs Redline beside this one in the same session scratchpad and also runs `case-study-clean`, so every run of `case-study-clean` is made only while this build holds the shared lock directory `/Users/thomas/Projects/skills/.git/kntnt-orchestrate-runB-locks/case-study-clean`, taken with `mkdir` before the run is dispatched and removed with `rmdir` as soon as it has returned. A file in the session scratchpad that the sibling's runs wrote is not this build's run's output; it is attributed by path and transcript in `results.md` and never scored.

## The matrix

The four drafts are `../editorial-362/runs/{column-sv-r1,column-sv-r2,opinion-en_GB-r1,opinion-en_GB-r2}/redline/work/input.md`, copied byte for byte. Each carries its own `kntnt` map, so the invocation names no genre and no language:

| Input | SHA-256 (first 16) | Invocation |
| --- | --- | --- |
| `column-sv-r1` | `4fe7a78864930951` | `/redline --output=response input.md` |
| `column-sv-r2` | `74b966f1352c4f42` | `/redline --output=response input.md` |
| `opinion-en_GB-r1` | `02171183566bb9a1` | `/redline --output=response input.md` |
| `opinion-en_GB-r2` | `cfefda44d50dcb42` | `/redline --output=response input.md` |

The ten controls are the ten rows of the corpus's *Redline controls* table, staged as the corpus says — only the linked artifact copied to `input.md` — and invoked as in #383's matrix: `/redline --genre=<genre> --language=<locale> --output=response input.md`, with `web-copy-flawed` in `en_US` and every other row in `sv`, with no contextual instruction and no technique.

| Arm | Runs |
| --- | --- |
| pre | `pre-<draft>` once on each of the four drafts; `pre-control-<row>` once on each of the ten controls |
| post | `post-<draft>-a` then `post-<draft>-b` on each draft; `post-control-<row>` once on each control |

Thirty-two Redline invocations and sixty-four judgements before any revise round. #383's pre-change arm had no controls; this one has them because the addendum requires the same inputs in both arms, and the criteria and the exit compare controls across arms.

**A clean control is run once, not twice.** The protocol's rule on a clean control asks for a response-target and a file-target run. The ticket fixes one run per control per arm with #383's invocations, so only the response-target run is made. A clean control that delivers text is judged from that text; one that returns only the no-change status is judged from the reply, which says nothing changed, and the judge's reading of it is what `C1` records. That is a declared narrowing, as it was in #383.

## Judging

Two independent judges per artefact, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket. The twenty-four draft runs, both arms, are judged by [`redline-judge-brief.md`](redline-judge-brief.md), the controls by [`control-judge-brief.md`](control-judge-brief.md). Both are byte copies of #383's, which are byte copies of #377's.

**Neutral paths.** Each judge gets a directory of its own, `397.scratch/j/<token>/`, named by a random token that names neither the arm, the row nor the run, holding `work/input.md` and `response.md` copied from the run and nothing else. The judge writes `judgement-<letter>.md` there and keeps any scratch there; the judgement is copied into the run directory as `judgement-a.md` or `judgement-b.md`. The two judges of one artefact are dispatched together and cannot read each other's directory by any path they are given. The scratch directory's own path carries this build's number, which is not the arm; the judge is told nothing of what it is. A control judge's message carries the row's frozen expectation as one paragraph headed **Frozen expectation**, as the brief says.

One judge suffices for a mechanical check — a diff, the presence of a report, the inventory — and those the dispatching session makes itself from the recorded files.

## Criteria, fixed before the runs

As #383's plan defines them, on these runs:

- **`R1`**, on every run of both arms.
- **`C1`**, on every control run of both arms: the run meets its row's frozen expectation, on `R1`, read against the row as `a321690f` leaves it.
- **`O1`**, on every run, from the before-and-after inventory.
- **`S1`**, on every run: the working directory held `input.md` and nothing else when the turn was dispatched.

`A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are recorded `skipped` on every run, naming `R1`, `C1`, `O1` and `S1` as this evaluation's criteria. No criterion here is answered from a Harness trace, so `staged_run.py` is not used.

### When `R1` is met

#383's plan settles a split in these words: *"Where the two judges of an artefact split, both classes are recorded and neither judge is an oracle. For deciding whether a criterion is met, the counting rule below governs."* Its counting rule reads: *"A difference counts against a run when both judges class it as taste outside any finding, or when either does and the reply covers it neither in the claim account nor in the closing summary."* Applied to `R1`:

- A run meets `R1` when both judges pass it, and misses it when both fail it.
- Where the judges split, the run misses `R1` unless the passage that decides the failing verdict is a difference that the reply covers in its claim account or its closing summary. In that case both readings are recorded and the run meets `R1`.
- `C1` is read by the same rule.

### What the ticket's criteria read

1. **Drafts.** `R1` is met on the four drafts when every post-change run on each of them meets it.
2. **Clean controls.** `article-clean`, `column-clean` and `opinion-clean` come back unchanged in the post-change arm. Proofread's mechanical changes are excluded, as #383's plan reads it. Checked mechanically from the reply against `input.md`, and read with both judges.
3. **Reported, not invented.** In the post-change arm, `article-flawed`'s missing byline and `case-study-flawed`'s missing call to action are reported and not written — checked mechanically from the reply — and both controls meet `C1`.
4. **The other controls.** Each control is compared across arms on `C1`: one that meets `C1` in the pre-change arm and misses it in the post-change arm has regressed.

**Target criterion.** `R1` on the four drafts. The candidate beats the pre-change arm when a larger share of its eight draft runs meets `R1` than of the pre-change arm's four.

**Reproduced.** The defect reproduces when at least one pre-change draft run writes a standfirst, a subheading, an ending or a call to action that its input did not have — established from the diff of the reply's text against `input.md` — and misses `R1` on it: the passage deciding a failing verdict is that part.

**Whose miss.** A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one: #398 (the claim account's assurance), #400 (a paratext change accounted for as something else), #402 (anatomy conformance reported unexamined) and #415 (an unhedged assertion mounted above a kept limit). A headline rewritten only to fit a band is #397's miss; the same rewrite left out of, or misnamed in, the account is #400's. Both judges' readings are recorded; where they split, the rule above decides.

## Inventory scope

As #383's plan, with its paths replaced. [`runs/inventory.sh`](runs/inventory.sh) and [`runs/run_inventory.sh`](runs/run_inventory.sh) are byte copies of #383's; [`runs/wave_inventory.sh`](runs/wave_inventory.sh) is #383's with this build's paths:

1. **The run directory**, including `work/` and any `scratch/` — per run, before dispatch and after the reply, into `inventory-before.txt` and `inventory-after.txt`.
2. **The staged install** the run reads — per run, as a digest of its full listing, in the same two files.
3. **The rest of this build's scratch root**, other runs' directories and the judges' directories among them — once around each wave.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock — once around each wave. Both carry other work in progress, so a hash of either would report an editing session's change as a run's; this is the narrowing #383 declared.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/40416275-c971-4568-a8ae-051cb6943e72/scratchpad/`, where a correction subagent may write (#401) and where the sibling build's runs also write — once around each wave. A change there is attributed by path and by the run's own reply before it is named in any run's `side effects`.

A *wave* is the set of runs in flight between two wave inventories. A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## Exit

1. **Not reproduced.** Where no pre-change draft run reproduces the defect, the result is recorded as not reproduced. Thomas's ruling ships all the same: the candidate is written, the post-change arm is run and scored, its result is written down as measured, and no decision record is written.
2. **The candidate** ships where the post-change arm meets criteria 1 to 3.
3. **One revise round**, at most, where it does not, no larger than the subset that failed: the runs of the inputs on which a criterion was missed, against a revised candidate committed first and staged as `install-revise`. The criteria are then read over the revised subset in place of the first candidate's runs on those inputs. Where the revised candidate meets them, it ships. Where it does not, the wording that ships is the one of the two candidates whose arm has the larger share of draft runs meeting `R1`, and where they are level, the first. The ruling ships either way, as the readiness addendum's *Items 3 and 4 do not undo Thomas's ruling* requires: no revert and no decision record follow from a miss.
4. Either way the result is written as measured, and each remaining miss — every criterion the shipped candidate misses and every control it regresses — is filed as its own `needs-triage` ticket naming #397.

No criterion is softened, no frozen plan, brief or fixture is edited to fit a result, and no arm is re-run to get a better reading.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun; so is a run that reports a file it wrote changed or deleted under it by another process. A void run is moved whole to `voided/` beside `runs/` before its row is run again. A run that completes and stops is a finding.

## What each run directory holds

```text
runs/<run>/
  work/                        the run's working directory
    input.md                   the only input exposed to the run
  response.md                  the user-facing reply, verbatim
  expectation.md               the row's frozen expectation (controls only)
  inventory-before.txt
  inventory-after.txt
  judgement-a.md
  judgement-b.md
```

## What is written

This file, the two turn files and the two judge briefs, committed before the first run; `results.md` beside them with the outcome whichever way it falls, including whether `docs/rules/docs.md`'s three criteria for a decision record hold; the judged run directories under `runs/`, with the wave inventories beside them; any void run under `voided/`; and one record, `../records/redline-claude-<date>-397.md`, in the protocol's format. Its line for `../records/README.md` is appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
