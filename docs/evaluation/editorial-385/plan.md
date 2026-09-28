# Unslop and the sentences that limit a claim — evaluation plan for #385

Frozen on 2026-09-24, before the first run of this evaluation. Nothing in this file, in the two turn files beside it, or in the two judge briefs beside it is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) first, then [#377's plan](../editorial-377/plan.md), whose shape this one adapts to Unslop, and [#383's plan](../editorial-383/plan.md), whose turn files and judge briefs this one copies. This file says only what those leave open and what #385 settles differently.

**Frozen twice.** This plan was first committed at `e3723890`, and a first wave of the four pre-change runs was made and judged against it on 2026-09-24. One line was then changed at `0d7fd057`: the run command under *How a run is made*, respelled so that each flag carries its value after an `=`, as the repository's flag-grammar check requires. That is an edit after a run, so the first wave does not stand as this evaluation's pre-change arm. It is void, and it is kept under [`runs/voided/wave-1/`](runs/voided/wave-1/) with the reason. The plan is frozen again on 2026-09-28, by the commit that adds this paragraph, before the first run of the wave that replaces it, and "the first run" above means the first run of that wave. The two turn files and the two judge briefs are byte-identical to `e3723890`, and the rest of this plan is byte-identical to `0d7fd057`. [`runs/run_turn.sh`](runs/run_turn.sh) is respelled in the same commit, so that the script that starts every session and the command under *How a run is made* agree. The replacement wave is wave 2, and its inventories are `runs/wave-2-*.txt`. The record is named for the date the replacement wave is made, as [the protocol](../protocol.md)'s *date* field requires, so the name under *What is written down* reads `unslop-claude-<that date>-385.md`. The candidate was reverted after the void wave, at `18757082`. If the replacement wave has an `N1` miss, the candidate is applied again by a commit of its own before the post-change arm, and `install-post` stays the archive of `d84b20ae`.

## What is under test

#377 narrowed Redline's permission to remove a passage the finding named whole, so that it no longer reaches a sentence whose work is to bound what the text asserts, and left Unslop's counterparts as they were. #377's [diagnosis](../editorial-377/diagnosis.md) names the False contrasts pattern in `anti-slop.md` as what hardened `I am not against digital booking.` into `I support digital booking`, and Unslop loads that file whole. The candidate carries the narrowing to Unslop, in its *pattern* vocabulary, on the surfaces #385's thread names:

- `skills/editorial/unslop/SKILL.md` step 6, which now says itself what a limiting sentence is and that one is recognised by what it bounds and which claim would lose that bound, never by its form, with the false-contrast clause beside it;
- step 7, where the whole-passage permission stops at such a sentence, and its removal, weakening, hardening or recasting stands only on a finding naming a pattern inside it and only in class (a) or (b) below;
- `skills/editorial/unslop/references/correction.md`, the paragraph headed **What a repair may take with it, and what it may not** and the paragraph opening "Before you return the text, compare it before and after, claim by claim.";
- `skills/editorial/unslop/help.md`, the paragraph on corrections.

Unslop still loads nothing beyond `anti-slop.md` and the language's anti-slop scope.

**The English hedge-chain line.** #377's diagnosis names a third loaded sentence, the English hedge-chain line. One search on 2026-09-24 (`grep -n "^## \|hedge" skills/kntnt/library/references/languages/en_GB.md`) finds it at line 47, under `## Review` (lines 37–52) and not under `## Anti-slop` (line 53 on). Unslop resolves only the `anti-slop` scope, so the line is not in what Unslop loads. False contrasts remains the one loaded sentence the diagnosis names.

**The blocker.** #383 is closed and its work is on `main` since `a163bf65`: `anti-slop.md` carries the section *The test before a pattern is recorded*, and Unslop's step 7 carries the trace check and step 9 the closing summary. That section never names a limiting sentence or what one bounds, so step 6 states the recognition rather than pointing at it, as the readiness addendum of 2026-09-23 19:35 settles. #398, the native blocked-by edge, is closed and merged into the start commit.

Two installs, one per arm, and a third only if a revise round is spent:

- **Pre-change**, the product at `c211a1d5`, the commit this ticket was begun from. Four runs, one on each draft. This arm is run and judged first.
- **Post-change**, the product at `d84b20ae`, the committed candidate. Eight runs, two on each draft, and seven controls.

Unslop is never given source material in any run. The only file in a run's working directory is `input.md`.

## Definitions, from #377's plan with "defect" read as "pattern"

A difference is a **change to what a claim says** when it alters any of six things about a claim: its **scope, certainty, attribution, chronology, causality or meaning**.

A **limiting sentence** is a sentence or clause whose work in the text is to bound what the text asserts: that something is not measured, not claimed, not witnessed or not general, or that the text is an observation of a document rather than a scene from an occasion.

**Hardening** is any change that raises what the text asserts. Three forms are tested for, and a judge that finds a fourth records and names it:

1. A refusal to assert becomes an assertion — *We make no claim to have costed that trial* to *We have not costed that trial*.
2. A disclaimer covering two things comes back covering one.
3. A sentence whose only work is to limit is deleted outright.

Moving a claim's actor is a change to what a claim says by attribution, and is judged there rather than as hardening: it does not raise what the text asserts.

Form 2 drops #377's trailing reference to *funded or*, because no such sentence is in the brief; that is the one departure from word for word the clarifications of 2026-09-23 19:51 permit.

**The escape clause.** Removing, weakening, hardening or recasting a limiting sentence is permitted only where the reply reports a finding naming a pattern **inside** that sentence which a judge can verify from the input text alone, independently of the reply's assertion, and only in these two classes:

- **(a)** the limit that sentence states is still stated by a sentence the text retains, so that afterwards the text bounds what it claims exactly as far as it did before, and no surviving claim gains scope, certainty, attribution, chronology, causality or meaning;
- **(b)** the sentence contradicts another passage of the same text.

A finding that names the whole sentence as the pattern without naming a pattern inside it is not one of these and licenses nothing.

## How a run is made

Provider family `claude`, in Claude Code 2.1.281, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from driving a Codex Harness, so no GPT harness and no GPT model is started, controlled or invoked here, directly or through any tool, script or subagent.

**The seat.** Every run, every correction subagent and every judge runs on `claude-opus-5-5` at high deliberation. Where #377's plan and #385's Agent Brief say `claude-opus-5`, this evaluation launches `claude-opus-5-5`, as the readiness addendum of 2026-09-23 19:35 settles. Judges are fresh `kntnt-opus-high` subagents, which launch that model at that deliberation. A run is not a subagent: this build's session is itself a subagent, and a subagent of it is given no tool for starting a subagent of its own, so it could not start Unslop's correction subagent (#397's [plan amendment](../editorial-397/plan-amendment.md) records the same seam for Redline). Each run is therefore a fresh top-level Claude Code session, started by [`runs/run_turn.sh`](runs/run_turn.sh) as

```
claude --print --safe-mode --model=claude-opus-5-5 --effort=high \
  --dangerously-skip-permissions --strict-mcp-config \
  --output-format stream-json --verbose
```

with the turn on stdin, from the run's working directory. That is the same model at the same deliberation as a `kntnt-opus-high` subagent, started so that its correction subagents can run, and they take its seat. `--safe-mode` keeps every `CLAUDE.md`, every installed Skill, every hook and every custom agent away from the run, which matters because the run's working directory lies under `/Users/thomas/Projects/skills`, whose `CLAUDE.md` a session would otherwise load; the built-in tools, the subagent tool among them, work as usual. The session's stream is kept under the scratch root's `logs/`, outside the run directory, and its `init` event names the model the session ran on. `docs/evaluation/editorial-388/harness/staged_run.py` is not used, as the thread requires.

**The installs.** Each install is `skills/editorial/unslop` and `skills/kntnt` side by side and nothing else, written with `git archive` from the commit it names and never copied from a working tree:

```
git archive <commit> skills/editorial/unslop | tar -x -C <install> --strip-components=2
git archive <commit> skills/kntnt            | tar -x -C <install> --strip-components=1
```

The thread's example strips two components from both paths, which lays `kntnt`'s contents out flat beside `unslop/` rather than as a `kntnt/` directory, and the shim then fell back to the globally installed Manager; the two commands above give the layout the thread asks for, `unslop/` and `kntnt/` side by side. After staging, the shim was run from each install with `--output=response input.md` on stdin, and the `$LIBRARY` it printed was `…/install-pre/kntnt/library` and `…/install-post/kntnt/library` respectively. The two installs differ in four files: `unslop/SKILL.md`, `unslop/help.md`, `unslop/references/correction.md` and `kntnt/catalog.json`.

- `…/install-pre` — from `c211a1d5`. Used by [`unslop-turn-pre.md`](unslop-turn-pre.md).
- `…/install-post` — from `d84b20ae`. Used by [`unslop-turn-post.md`](unslop-turn-post.md).
- `…/install-revise` — only if a revise round is spent, from the committed revised candidate, with a turn file of its own, `unslop-turn-revise.md`, which is [`unslop-turn-post.md`](unslop-turn-post.md) with `install-post` read `install-revise` and nothing else changed.

`…` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/385.scratch/kntnt-eval-385`. The thread names `kntnt-eval-385/` directly inside the repository's common git directory; this build's brief confines what it writes to its working tree and to `…/.git/kntnt-orchestrate/385.scratch`, so the scratch root is `kntnt-eval-385/` inside that directory. It is inside the common git directory all the same: git does not track it, removing a worktree does not delete it, a temp-directory sweep does not reach it, and it is not recorded with `session_cleanup.py`.

**The turn files** are #383's [`redline-turn-pre.md`](../editorial-383/redline-turn-pre.md) and [`redline-turn-post.md`](../editorial-383/redline-turn-post.md) with the three substitutions the thread permits and no other change: the staged path, the Skill named `unslop` in place of `redline`, and the sentence naming what a run may not read naming only `/Users/thomas/Projects/skills`. The prompt a session receives is the turn file, then a rule, then the three things the turn says the dispatching message gives — the working directory, the run directory, and the invocation as the user typed it — and nothing else. The one evaluator instruction in the turn is #383's and is declared there: save the reply verbatim to `response.md` in the run directory.

**Where runs execute.** Each run directory is `…/runs/<run>/`, holding `work/input.md` and, once the run creates it, `work/scratch/`; the session's working directory is `work/`. The run directories are copied into this evaluation's `runs/` only after both judges have written.

**Locks and concurrency.** A sibling build (#400) runs its own evaluation on the same four drafts on this machine. Before a run on one of `column-sv-r1`, `column-sv-r2`, `opinion-en_GB-r1` or `opinion-en_GB-r2`, the runner takes `/Users/thomas/Projects/skills/.git/kntnt-eval-lock-<draft>` with `mkdir`, retrying every thirty seconds while it exists, and removes it as soon as the session returns. No two runs of this evaluation on the same draft run at the same time (#401); runs on different inputs run side by side.

**Interrupted runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void and is rerun; it is not a finding. A void run's directory is kept under `runs/voided/` with the reason.

No hint of the defect under investigation appears in any turn, in any invocation, or in any judge brief.

## The matrix

The four drafts are the `work/input.md` of the four Redline runs #362 recorded, copied byte for byte, the same four files #377 and #383 used. Each is source-blind and carries its own `kntnt` map, so the invocation names no language.

| Run | Arm | Input | Invocation |
| --- | --- | --- | --- |
| `pre-column-sv-r1` | pre | `../editorial-362/runs/column-sv-r1/redline/work/input.md` | `/unslop --output=response input.md` |
| `pre-column-sv-r2` | pre | `../editorial-362/runs/column-sv-r2/redline/work/input.md` | `/unslop --output=response input.md` |
| `pre-opinion-en_GB-r1` | pre | `../editorial-362/runs/opinion-en_GB-r1/redline/work/input.md` | `/unslop --output=response input.md` |
| `pre-opinion-en_GB-r2` | pre | `../editorial-362/runs/opinion-en_GB-r2/redline/work/input.md` | `/unslop --output=response input.md` |
| `post-column-sv-r1-a`, `-b` | post | as `pre-column-sv-r1` | `/unslop --output=response input.md` |
| `post-column-sv-r2-a`, `-b` | post | as `pre-column-sv-r2` | `/unslop --output=response input.md` |
| `post-opinion-en_GB-r1-a`, `-b` | post | as `pre-opinion-en_GB-r1` | `/unslop --output=response input.md` |
| `post-opinion-en_GB-r2-a`, `-b` | post | as `pre-opinion-en_GB-r2` | `/unslop --output=response input.md` |

The seven controls are exhaustive for this ticket; no other run of either `unslop-claude-*` record is repeated. Each is run once against `install-post`, with only the fixture copied to `input.md`, and each invocation is the Formal Invocation verbatim. The fixtures are read from this working tree at `c211a1d5`.

| Run | Fixture under `docs/evaluation/corpus/` | Invocation | Expectation |
| --- | --- | --- | --- |
| `control-slop-heavy-review` | `prose/slop-heavy.md` | `/unslop --max=0 --output=response input.md` | `catch`: findings are raised for the patterns the corpus README's *Material* line for `slop-heavy` plants, each named by its catalogue pattern and none phrased as a style preference. The text comes back unchanged. |
| `control-slop-heavy` | `prose/slop-heavy.md` | `/unslop --output=response input.md` | Claim floor: the returned text still carries the input's claims about meeting load, documentation, decisions, satisfaction, distributed work, adoption conditions and the synchronous/asynchronous trade-off — the list Unslop's own `references/correction.md` names — and every claim that did go or move is named in the reply's claim account. The corpus README's *Reject* line, "a correction that removes the patterns and the content with them", is the failure. |
| `control-slop-heavy-sv-review` | `prose/slop-heavy-sv.md` | `/unslop --max=0 --output=response input.md` | `catch`, as the first row, against the corpus README's *Material* line for `slop-heavy-sv`, the Swedish items among them; the reply is in Swedish. |
| `control-slop-heavy-sv` | `prose/slop-heavy-sv.md` | `/unslop --language=sv --max=1 --output=response input.md` | Claim floor: no claim of the input is gone or moved without being named in the reply's claim account, and none is removed except where the finding named the whole claim as the pattern. The reply and the text are in Swedish. |
| `control-clean-en-GB` | `prose/clean-en-GB.md` | `/unslop --output=response input.md` | `catch` and `status`: no finding, and the short no-change status rather than a text. |
| `control-flawed-en-US` | `prose/flawed-en-US.md` | `/unslop --max=0 --output=response input.md` | `lens`: no mechanical error is raised as a finding or corrected, and no genre, technique or structural expectation is imposed. |
| `control-flawed-sv` | `prose/flawed-sv.md` | `/unslop --max=0 --output=response input.md` | `lens`, as the row above, in Swedish. |

`catch`, `lens` and `status` are the criterion names [`../records/unslop-claude-2026-08-26.md`](../records/unslop-claude-2026-08-26.md) defines. These rows are not a comparison with that record, whose corpus commit is not today's: the standard is each row's expectation as frozen here.

Nineteen Unslop invocations in all: four pre-change, eight post-change, seven controls.

## Order of work, and the exit

1. The candidate is committed (`d84b20ae`), then `install-pre` and `install-post` are staged, then this plan, the turn files and the judge briefs are committed, and only then is the first run made.
2. The four pre-change runs are made and judged first.
3. **Not reproduced.** The defect this ticket was filed for is an `N1` miss on a pre-change run: a limiting sentence the run removes, weakens, hardens or recasts outside classes (a) and (b). Where no pre-change run has one, the defect is not reproduced: neither the post-change arm nor the controls is run, the candidate is reverted by a commit of its own, this directory is kept, `results.md` records the defect as not reproduced, and a decision record says so, numbered `0221`, the number reserved for this ticket.
4. Otherwise the eight post-change runs and the seven controls are made and judged.
5. **A control that misses** is re-run once against `install-pre`, with the pre-change turn file. A control "passed in the pre-change arm" where it passed when first run or where its re-run against `install-pre` passed. A miss against `install-post` that passes against `install-pre` is a regression; a miss in both is a failure that existed before this ticket, recorded as measured and filed `needs-triage` naming #385, and it does not block this ticket.
6. **The target figure** of an arm is its `N1` and `N2` misses over its runs on the four drafts, counted together, divided by its number of such runs. A miss is a single offending sentence or change, not a failed run. The pre-change arm has four runs and the post-change arm eight.
7. **One revise round** is available, no larger than the subset that failed: the revised candidate is committed, archived to `install-revise` with its own turn file, and the failed draft runs and all seven controls are rerun against it, adding at most eight draft runs and their judges.
8. **Exit.** Where the candidate, or the revised candidate, meets `N1` and `N2` on every post-change run and no control regresses, it ships. Where it does not, it ships only if its target figure is lower than the pre-change arm's and no control that passed in the pre-change arm fails against it; otherwise the product stays as it was at `c211a1d5`, and the candidate is reverted by a commit of its own. Either way, the result is written as measured, each remaining miss is filed as its own `needs-triage` ticket naming #385, and the ticket is done. No criterion is softened and no frozen plan, turn file, brief or fixture is edited.

## Judging

Two independent judges per artefact, each a fresh `kntnt-opus-high` subagent, each blind to the expected answer, to the arm the artefact came from, to the model that produced it and to this ticket. The two judges of one artefact are dispatched together and neither is told of the other. One judge suffices for a mechanical check — a diff, a count, the presence of a report, the before-and-after inventory — and those the dispatching session makes itself from the recorded files.

**Neutral paths.** Each judge gets a directory of its own made by `mktemp -d` under the system temporary directory, whose path names neither the arm, the input, the run nor this ticket, holding `work/input.md` and `response.md` copied from the run directory, `expectation.md` as well for a control, and the judge brief it is to follow, and nothing else. The dispatching message names that directory, the brief's path in it and the judge's letter, and tells the judge to keep any scratch of its own inside that directory. The judgement is copied into the run's directory as `judgement-a.md` or `judgement-b.md`, the mapping from directory to run is kept in `runs/judges.tsv`, and each directory is removed once its judgement is copied. The one departure from the build's confinement to its two directories is this: a `mktemp -d` path is unique, so no other session can have chosen it, and a path under the scratch root would name this ticket.

The twelve draft runs, pre and post alike, are judged by [`unslop-judge-brief.md`](unslop-judge-brief.md), so that no judge can tell which arm it is judging. It is #383's [`redline-judge-brief.md`](../editorial-383/redline-judge-brief.md) with the changes the thread lists and no other: "defect" reads "pattern"; the hardening forms are the three quoted above; heading 3 asks whether each limiting sentence is kept, removed, weakened, hardened or recast, and asks the (a)/(b) questions of every one removed, weakened, hardened or recast; the section *Criterion R1* and heading **4. R1** are gone, because the editorial-quality corpus marks `R1` "Redline only"; a new heading 4 asks whether every difference traces to a finding the reply reports and whether the reply's closing summary covers every kind of change and says nothing false; and the closing reply drops the R1 verdict.

The seven controls are judged by [`control-judge-brief.md`](control-judge-brief.md), one brief for all seven. It is #383's [`control-judge-brief.md`](../editorial-383/control-judge-brief.md) with the changes the thread lists and no other: its opening sentence has the judge read `work/input.md`, `response.md` and `expectation.md`; its section *The standard for this control* says the expectation is in `expectation.md` and comes from this plan, not from the corpus; the section *Criterion R1* is removed, and with it the sentence about a separate proofreading Skill, which is false of Unslop; heading 4 is **4. The expectation: pass or fail**; and the closing reply drops the R1 verdict.

**`expectation.md`.** For each control, the evaluator copies the row's *Expectation* cell verbatim from the table above into `expectation.md` in the run directory. Where the cell refers to another row or to a line of the corpus README, that text is written out in full beneath the cell and labelled as such: the *Material* line for `slop-heavy` under `control-slop-heavy-review`; the *Reject* line for `slop-heavy` under `control-slop-heavy`; the first row's cell and the *Material* line for `slop-heavy-sv` under `control-slop-heavy-sv-review`; and the `control-flawed-en-US` row's cell under `control-flawed-sv`. The corpus lines are taken from `docs/evaluation/corpus/README.md` at `c211a1d5`.

**Judge splits.** Where the two judges of an artefact split, both readings are recorded and neither is deleted or reconciled; for deciding whether a criterion is met, the stricter judgement governs, in both arms and on every criterion, as #377's plan says.

**Whose miss.** A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one: #397 (paratext authored into a finished text), #398 (the claim account's assurance), #400 (a paratext change accounted for as something else), #402 (anatomy conformance reported unexamined) and #415 (an unhedged assertion mounted above a kept limit). Both judges' readings are recorded.

## Criteria, fixed before the runs

- **`N1`**, on every draft run of both arms: no limiting sentence is removed, weakened, hardened or recast outside classes (a) and (b), as verified by a judge from the input alone under heading 3 of the judge brief. Each such sentence is one miss.
- **`N2`**, on the same runs: the reply names every change to what a claim says, by the six-element list, read from headings 1 and 2 of the judge brief. Each change a judge finds unnamed is one miss.
- **`C1`**, on each control: the run meets its row's expectation, read from heading 4 of the control brief.
- **`O1`**, on every run, from the before-and-after inventory: the Output Target contract, source preservation and cleanup hold. An evaluator capture is not a Skill file.
- **`S1`**, on every run, mechanically: no source material was supplied. The run's working directory held `input.md` and nothing else when the session started.

`N1` and `N2` on the post-change arm are this ticket's target criteria, and their combined figure is the target figure of the exit above. `N1` on the pre-change arm is what says whether Unslop reached a limiting sentence before the change.

**Recorded, not a criterion.** Heading 4 of the draft judge brief — whether every difference traces to a finding, and whether the closing summary covers every kind of change and says nothing false — is the check on #383's work. It is recorded in `results.md` and is not one of this ticket's criteria: a failure there spends no revise round and changes no wording here, and it is filed `needs-triage` naming #383 and #385.

**Skipped.** `T1` and `R2` are recorded `skipped` on every run: this ticket's scope runs Unslop through turn files and answers no criterion from a Harness trace. The reason is the ticket's scope, not a limit of the Harness. The editorial-quality corpus's other criteria — `R1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — are Redline's and Write's and are recorded `skipped` on every run, with the reason that they do not apply to Unslop.

## Inventory scope

`O1` and the `side effects` field are read from a `sha256` inventory taken before and after, never from a run's report of itself. [`runs/inventory.sh`](runs/inventory.sh) is a byte copy of #383's; [`runs/run_inventory.sh`](runs/run_inventory.sh) is #383's per-run script with one comment line added, and [`runs/wave_inventory.sh`](runs/wave_inventory.sh) is #383's wave script with this evaluation's paths and a status read that takes no optional lock. The scope is every writable location staged for a run:

1. **The run directory**, including `work/` and its `scratch/`.
2. **The staged install** the run reads.
3. **The rest of the scratch root**, other runs' directories, the other installs and `logs/` among them.
4. **The two checkouts of this repository a run is told not to read** — this ticket's working tree, `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/385`, and `/Users/thomas/Projects/skills` — by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all`, as #383's plan declares and for the same reason: both trees may carry work in progress while the runs are made.

Scopes 1 and 2 are inventoried by `run_turn.sh` immediately before each session starts and immediately after it returns, into `inventory-before.txt` and `inventory-after.txt`. Scopes 3 and 4 are inventoried once around each wave, into `wave-<n>-before-*.txt` and `wave-<n>-after-*.txt` beside `runs/`. A change under scope 2 or 3 during a wave cannot be attributed to one run of it, and is named in the `side effects` field of every entry in the wave.

## What each run directory holds

```text
runs/<run>/
  work/                        the run's working directory
    input.md                   the only input exposed to the run
    scratch/                   the only scratch the run may create
  response.md                  the user-facing reply, verbatim
  expectation.md               the row's expectation (controls only)
  inventory-before.txt
  inventory-after.txt
  judgement-a.md
  judgement-b.md
```

The session's stream and prompt stay under the scratch root's `logs/`; `results.md` names the model each session's `init` event reports.

## What is written down

[`results.md`](results.md) holds both arms and the controls, the check on #383's work, and whether the pre-change arm reached a limiting sentence. The record goes to `../records/unslop-claude-2026-09-24-385.md`, in the protocol's format, suffixed with this ticket's number as the clarifications require. Its line in `../records/README.md` is appended by the run from this ticket's note file, not by this build.
