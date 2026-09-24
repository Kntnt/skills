# Plan for #402: the ending is a section of its own

Frozen on 2026-09-24, before the first run of either arm and before any product change. Nothing in this file or in the judge brief beside it is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first, then [#383's plan](../editorial-383/plan.md), whose method this one re-uses as [#397's plan](../editorial-397/plan.md) and [its amendment](../editorial-397/plan-amendment.md) last applied it to the same ten controls; this file says only what those leave open and what #402 settles differently.

**`<start>` is `1ef14cb5`**, the head of the branch `kntnt-orchestrate/main/402` when the build began, with #397's change in it. The pre-change arm is staged from it. **The corpus commit is `1ef14cb5` too.** Both arms read their inputs and their expectations from it, with the `article-flawed` and `column-flawed` rows as #397's `a321690f` revised them. This ticket's diff does not touch the corpus.

The requirement is the ticket's thread as it stood on 2026-09-23: the body, the triage addendum of 2026-09-22, the addendum of 2026-09-23 19:22 UTC on the block, the readiness addendum of 19:39 UTC and the clarifications of 19:50 UTC. Where they conflict the later one stands.

## What is under test

In [#383's run](../editorial-383/runs/control-opinion-flawed/) and in both arms of [#397's](../editorial-397/results.md), Redline repaired `opinion-flawed`'s closing exhortation from the body's own actor and act and left it standing inside the last section, `## Diskussion` in the input, which carries the argument. The frozen row counts *no ending section, the closing exhortation sitting inside the last one* as an anatomy defect, and #383's reply still said the delivered text met the anatomy without deviation.

Thomas's ruling on the ticket is the specification and is not open here: **the ending is a section of its own, opened by its own subheading, after at least one other section.** The candidate states it in `## Ending` of `article-anatomy.md` with the test for when a last section is an ending; lets `article-anatomy.review.md` find a closing passage inside a section that carries the argument to be a present ending that fails its rule, repaired by giving it a section of its own from the text's own content; has `article_anatomy.py` fail a text of exactly one level-2 section; and has Redline's step 6, step 11 and correction brief say that exit 0 settles the counted requirements only, and that a reply or return reports the text as conforming to the anatomy only where every requirement the script does not count was examined. Its exact wording is written after the pre-change runs have started and is recorded in `results.md` with its commit. The ruling ships whatever this measurement shows; the measurement decides which wording ships where a revise round is taken, and what is written down.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

This build's session is itself a subagent, and cannot give a run of its own a tool for starting Redline's correction subagent, as [#397's amendment](../editorial-397/plan-amendment.md) found. So every Redline run, of both arms and of any revise round, is a fresh top-level Claude Code session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from this working tree:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=1ef14cb5 \
  --invocation='<invocation from the matrix>' \
  --input=<scratch>/inputs/<row>.md --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high
```

- **The seat.** `claude-opus-5-5` at high deliberation for the session, its correction subagents and its nested Proofread pass, which take the session's seat; `run.json` records the request and `trace-index.json` what ran. Where #383's plan says `claude-opus-5`, this evaluation launches `claude-opus-5-5`, as the readiness addendum settles. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation.
- **The installs.** `<commit>` is `<start>` for the pre-change arm, the committed candidate for the post-change arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own, laid out so that the shim finds `HERE.parent / "kntnt"`. The candidate is committed before its install is staged.
- **The inputs.** `<scratch>/inputs/<row>.md` is `git show 1ef14cb5:docs/evaluation/corpus/editorial-quality/controls/<row>.md`, written once before the first run. The invocation is the whole prompt; no turn file is sent, because the Skill is installed rather than named by path, so #383's turn files are not copied here.
- **Where runs execute.** The run's `HOME`, working directory, temporary directory and caches are a private root the runner makes with `mkdtemp` under the system temporary directory and removes on every exit. The packet is written under `<scratch>/packets/<run>/` and copied into this evaluation's `runs/<run>/` after both judges have written. `<scratch>` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/402.scratch`.
- **No two runs on one input at a time** (#401). This build makes at most one run of a row at once. A run's correction subagents write inside its own private root, so a run of this build and a sibling build's run of the same row cannot collide in a shared scratchpad.
- **The staged runner's use.** The readiness addendum reserves `staged_run.py` for criteria answered from a Harness trace. It is used here, as in #397, because it is the one way from this seat to give Redline a session that can start its correction subagents; no criterion here is answered from the trace it keeps.

## The matrix

The ten controls are the ten rows of the corpus's *Redline controls* table, staged as the corpus says — only the linked artifact as `input.md` — and invoked as in #383's matrix, with no contextual instruction and no technique:

| Row | SHA-256 (first 16) | Invocation |
| --- | --- | --- |
| `article-clean` | `f183e6da31cf7808` | `/redline --genre=article --language=sv --output=response input.md` |
| `article-flawed` | `1c0e3b3ef98e06b2` | `/redline --genre=article --language=sv --output=response input.md` |
| `case-study-clean` | `32037623b16754f3` | `/redline --genre=case-study --language=sv --output=response input.md` |
| `case-study-flawed` | `ce574061bd09328e` | `/redline --genre=case-study --language=sv --output=response input.md` |
| `column-clean` | `98b65197fa9dd800` | `/redline --genre=column --language=sv --output=response input.md` |
| `column-flawed` | `9b12ad3fb2cb7401` | `/redline --genre=column --language=sv --output=response input.md` |
| `opinion-clean` | `179cc9615d2aa633` | `/redline --genre=opinion --language=sv --output=response input.md` |
| `opinion-flawed` | `ab033d9f4c817c9e` | `/redline --genre=opinion --language=sv --output=response input.md` |
| `web-copy-clean` | `8de234f1c80fe947` | `/redline --genre=web-copy --language=sv --output=response input.md` |
| `web-copy-flawed` | `a5470e4b3aea20a0` | `/redline --genre=web-copy --language=en_US --output=response input.md` |

| Arm | Runs |
| --- | --- |
| pre | `pre-control-<row>` once on each of the ten controls, from `<start>` |
| post | `post-control-<row>` once on each of the ten controls, from the committed candidate |
| revise | `revise-control-<row>` once on each control of the failed subset, only if a revise round is taken |

Twenty Redline invocations and forty judgements before any revise round. The four #362 drafts are not run: the clarifications of 19:50 UTC cut the measurement to the ten controls. Runs are dispatched in waves of at most five, each wave on five different rows.

**A clean control is run once, not twice.** The protocol's rule on a clean control asks for a response-target and a file-target run. The ticket fixes the ten controls as #383's plan stages them, so only the response-target run is made, as in #383 and #397. That is a declared narrowing.

## Judging

Two independent judges per run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket, judging by [`control-judge-brief.md`](control-judge-brief.md), a byte copy of [#383's](../editorial-383/control-judge-brief.md). A judge's message carries the row's frozen expectation as one paragraph headed **Frozen expectation**, as the brief says: the row's *Frozen expectation and rejection* cell at `1ef14cb5`, copied verbatim. For `opinion-flawed` that paragraph is the text of [`../editorial-383/runs/control-opinion-flawed/expectation.md`](../editorial-383/runs/control-opinion-flawed/expectation.md), which is the same cell.

**Neutral paths.** Each judge gets a directory of its own made by `mktemp -d` under the system temporary directory, whose path names neither the arm, the row, the run nor this ticket, holding `work/input.md`, copied from the packet's `supplied-input.md`, and `response.md`, copied from its `response.txt`, and nothing else; the packet's other files name the revision and the model. The judge writes `judgement-<letter>.md` there. The judgement is copied into the run's directory as `judgement-a.md` or `judgement-b.md`, the mapping from directory to run is kept in `runs/judges.tsv`, and each directory is removed once its judgement is copied. The two judges of one run are dispatched together and are not told of each other.

One judge suffices for a mechanical check — reading a reply for a finding, a diff, the inventory — and those the dispatching session makes itself from the recorded files.

## Criteria, fixed before the runs

As #383's plan defines them, on these runs:

- **`R1`** and **`C1`**, on every run: the run meets its row's frozen expectation, on `R1`, read against the row as `1ef14cb5` leaves it.
- **`O1`**, on every run, from the runner's before-and-after inventories.
- **`S1`**, on every run: the working directory held `input.md` and nothing else when the session started, read from `supplied-input.md` and the runner's before-inventory.

Every other criterion — `A1`, `A2`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` — is recorded `skipped` on every run.

### When `C1` is met

#383's plan settles a split: both classes are recorded and neither judge is an oracle, and *"a difference counts against a run when both judges class it as taste outside any finding, or when either does and the reply covers it neither in the claim account nor in the closing summary."* As #397 applied it: a run meets `C1` when both judges pass it and misses it when both fail it; where they split, it misses unless the passage that decides the failing verdict is a difference the reply covers in its claim account or its closing summary, in which case both readings are recorded and the run meets `C1`.

**The ending clause of `opinion-flawed`** — *no ending section, the closing exhortation sitting inside the last one and naming no act. Existing action/actor in body can repair the ending.* — is met only where both judges record it met under heading 3 of their judgement. The split rule above does not reach it.

### What the ticket's criteria read

1. **Target.** `post-control-opinion-flawed` meets every clause of its frozen expectation including the ending clause, and meets `C1`. A clause other than the ending clause is met where both judges record it met, or where they split and the reply reports a finding naming it, quoted by the judge who records it met.
2. **Conforming controls.** None of `article-clean`, `case-study-clean`, `column-clean` and `opinion-clean` acquires *a new finding* in the post-change arm: a finding about the ending — that the last section is not an ending, that an ending section is missing, or that closing content should stand in a section of its own — or about the number of sections, that the pre-change run of the same row lacks. The dispatching session reads each reply for such a finding, whether reported as repaired or as left, and quotes it. Any other finding the post-change run has and the pre-change run lacks is recorded in `results.md` and not counted here.
3. **The other controls.** Each control is compared across arms on `C1`: one that meets `C1` in the pre-change arm and misses it in the post-change arm has regressed. Recorded, and filed if it stands.

**Target criterion** is criterion 1. **Reproduced**: the pre-change arm reproduces the defect when `pre-control-opinion-flawed` leaves the ending clause unmet by the rule above.

**What each reply says about conformance.** For every anatomy genre run the dispatching session records whether the reply says the delivered text meets or conforms to the anatomy, and, where it does, whether the returned text has its ending in a section of its own. This is recorded, not scored.

**Whose miss.** A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one: #397 (paratext authored into a finished text), #398 (the claim account's assurance), #399 (`case-study-clean` missing `C1` on a rewritten subheading), #400 (a paratext change accounted for as something else), #415 (an unhedged assertion mounted above a kept limit), and #429 to #432, which #397 filed from the same ten controls: a working headline reworded under the headline contract (#429), `article-clean` and `column-clean` changed on a rewritten headline (#430), `opinion-clean`'s lead gaining the standfirst's *september* clause (#431), and `web-copy-clean` missing on a fact copied from a heading and a missing form link (#432). Both judges' readings are recorded; where they split, the rule above decides.

## Inventory scope

Scopes 1 and 2 — the run's working directory, its staged install and its scratch — are the runner's before-and-after inventories of the run's private root. Scopes 3 to 5 are read once around each wave by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), which is #397's with this build's paths, calling [`runs/inventory.sh`](runs/inventory.sh), a byte copy of #383's:

3. **The rest of this build's scratch root**, the other runs' packets among them.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock. Both carry other work in progress, so a hash of either would report an editing session's change as a run's; this is the narrowing #383 declared.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/40416275-c971-4568-a8ae-051cb6943e72/scratchpad/`, which sibling builds also write to. A change there is attributed by path before it is named in any run's `side effects`.

The worktree list at `<start>` holds the main checkout, `../skills-rework`, this build's working tree and `kntnt-orchestrate/401`; the last two are sibling builds' and the rework worktree is read-only source, so none of the three is in scope beyond what scope 4 names.

A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## Exit

1. **Not reproduced.** Where `pre-control-opinion-flawed` meets the ending clause, the result is recorded as not reproduced. Thomas's ruling ships all the same: the candidate is written, the post-change arm is run and scored, its result is written down as measured, and no decision record is written.
2. **The candidate** ships where the post-change arm meets criteria 1 and 2.
3. **One revise round**, at most, where it does not, no larger than the subset that failed: the controls on which criterion 1 or 2 was missed, run again against a revised candidate committed first. The criteria are then read over the revised subset in place of the first candidate's runs on those rows. Where the revised candidate meets them, it ships. Where it does not, the revised wording ships only if it meets criterion 1 where the first candidate missed it, or has fewer criterion-2 findings over the subset, and makes no control of the subset miss `C1` that the first candidate's run met; otherwise the first candidate's wording ships. The ruling ships either way, as the readiness addendum's *Items 3 and 4 do not undo Thomas's ruling* requires: no revert and no decision record follow from a miss.
4. Either way the result is written as measured, and each remaining miss — a criterion the shipped wording misses and a control it regresses — is filed as its own `needs-triage` ticket naming #402.

No criterion is softened, no frozen plan, brief or fixture is edited to fit a result, and no arm is re-run to get a better reading.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun. A void run's packet is moved whole to `voided/` beside `runs/` before its row is run again. A run that completes and stops is a finding.

## What is not measured

Write loads `article-anatomy.md`, so the two-section minimum changes what Write's draft must have and what its step 7 repairs. No Write run is made here, as the clarifications of 19:50 UTC say, and `results.md` says so.

## What is written

This file, the judge brief and the two inventory scripts, committed before the first run; `results.md` beside them with the outcome whichever way it falls; the judged packets under `runs/`, with `runs/judges.tsv` and the wave inventories; any void run under `voided/`; and one record, `../records/redline-claude-2026-09-24-402.md`, in the protocol's format. Its line for `../records/README.md` is appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
