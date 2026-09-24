# Plan for #398: the claim account covers the claims a run wrote

Frozen on 2026-09-24, before the first run of either arm and before any product change. Nothing in this file, in the two judge briefs beside it or in the two inventory scripts under `runs/` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first, then [#383's plan](../editorial-383/plan.md), whose method this one re-uses as [#397's plan](../editorial-397/plan.md), [its amendment](../editorial-397/plan-amendment.md) and [#402's plan](../editorial-402/plan.md) last applied it; this file says only what those leave open and what #398 settles differently.

**`<start>` is `81f50bfd`**, the head of the branch `kntnt-orchestrate/main/398` when the build began, with #397's, #399's, #401's and #402's changes in it. The pre-change arm is staged from it. **The corpus commit is `81f50bfd` too.** Both arms read their inputs and their expectations from it. This ticket's diff does not touch the corpus.

The requirement is the ticket's thread as it stood on 2026-09-23: the body, the triage addendum of 2026-09-22, the addendum of 2026-09-23 19:21 UTC on the block, the readiness addendum of 19:37 UTC, its correction of 19:39 UTC and the clarifications of 19:49 UTC. Where they conflict the later one stands.

## What is under test

In [#383's post-change arm](../editorial-383/results.md) every reply on the four #362 drafts closed its itemised claim account with an assurance that no claim was removed and none was left standing with its scope, certainty, attribution, chronology, causality or meaning moved, and in every one a judge found that sentence false or misleading against the delivered text, which carried assertions the run had written. On `control-web-copy-flawed` the same sentence stood one paragraph after the reply's own finding disclosing that the rewritten headline had dropped the body's `including VAT`. The sentence is not shipped: the runs write it themselves, prompted by the clause `this account accompanies a clean artifact too, so what the run did to the claims is visible without a diff`, word for word the same in Redline's step 11 and Unslop's step 9.

Thomas's ruling on the ticket is the specification and is not open here: **a claim the run wrote joins the itemised account as a third class, beside the removed and the changed, and no assurance in a reply contradicts a finding the same reply states.** The clarifications of 19:49 UTC settle the rest: step 7 records an added claim in the same comparison that records removed and changed claims, and Redline's step 11 and Unslop's step 9 report it from there; a claim is *added* when the delivered text asserts it and the text as it arrived has no counterpart for it, an inference drawn from existing text among them where it asserts something the arrived text did not say, and *changed* when it has a counterpart whose scope, strength or subject differs; and that definition is written into the product where the three classes are named. The candidate sweeps Redline's and Unslop's `SKILL.md`, both `references/correction.md` briefs, both `help.md` pages and `base.review.md`. Its exact wording is written after the pre-change runs have started and is recorded in `results.md` with its commit. The ruling ships whatever this measurement shows; the measurement decides which wording ships where a revise round is taken, and what is written down.

Unslop receives the same change in its own vocabulary. **Unslop is not measured here**, as #383 did not measure it: the ticket's matrix is Redline's.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

This build's session is itself a subagent, and cannot give a run of its own a tool for starting Redline's correction subagent, as [#397's amendment](../editorial-397/plan-amendment.md) found. So every Redline run, of both arms and of any revise round, is a fresh top-level Claude Code session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py), run from this working tree:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=81f50bfd \
  --invocation='<invocation from the matrix>' \
  --input=<scratch>/inputs/<input>.md --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high
```

- **The seat.** `claude-opus-5-5` at high deliberation for the session, its correction subagents and its nested Proofread pass, which take the session's seat; `run.json` records the request and `trace-index.json` what ran. Where #383's plan says `claude-opus-5`, this evaluation launches `claude-opus-5-5`, as the readiness addendum settles. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation.
- **The installs.** `<commit>` is `<start>` for the pre-change arm, the committed candidate for the post-change arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own, laid out flat so that the shim finds `HERE.parent / "kntnt"`. The candidate is committed before its install is staged.
- **The inputs.** `<scratch>/inputs/<input>.md` is written once, before the first run, by `git show 81f50bfd:<path>` of the path the matrix names. The invocation is the whole prompt; no turn file is sent, because the Skill is installed rather than named by path, so #383's turn files are not copied here, as in #402.
- **Where runs execute.** The run's `HOME`, working directory, temporary directory and caches are a private root the runner makes with `mkdtemp` under the system temporary directory and removes on every exit. The packet is written under `<scratch>/packets/<run>/` and copied into this evaluation's `runs/<run>/` after both judges have written. `<scratch>` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/398.scratch`.
- **No two runs on one input at a time** (#401). #401's change landed at `a24e70a3`, before `<start>`, and every run's correction subagents write inside its own private root. The clarifications of 19:49 UTC ask for runs one at a time while #401 is open; it is merged into this branch, so runs on *different* inputs run side by side, at most five at once, as #402's build made them in the same unattended run. The runs of one input — both post-change runs on a draft, and a revise run — are made one after the other.
- **The staged runner's use.** The readiness addendum reserves `staged_run.py` for criteria answered from a Harness trace. It is used here, as in #397 and #402, because it is the one way from this seat to give Redline a session that can start its correction subagents; no criterion here is answered from the trace it keeps.

## The matrix

The four drafts are `docs/evaluation/editorial-362/runs/{column-sv-r1,column-sv-r2,opinion-en_GB-r1,opinion-en_GB-r2}/redline/work/input.md`, copied byte for byte. Each carries its own `kntnt` map, so the invocation names no genre and no language. The ten controls are the ten rows of the corpus's *Redline controls* table, staged as the corpus says — only the linked artifact as `input.md` — and invoked as in #383's matrix, with no contextual instruction and no technique.

| Input | SHA-256 (first 16) | Invocation |
| --- | --- | --- |
| `column-sv-r1` | `4fe7a78864930951` | `/redline --output=response input.md` |
| `column-sv-r2` | `74b966f1352c4f42` | `/redline --output=response input.md` |
| `opinion-en_GB-r1` | `02171183566bb9a1` | `/redline --output=response input.md` |
| `opinion-en_GB-r2` | `cfefda44d50dcb42` | `/redline --output=response input.md` |
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
| pre | `pre-<draft>` once on each of the four drafts; `pre-control-<row>` once on each of the ten controls; all from `<start>` |
| post | `post-<draft>-a` then `post-<draft>-b` on each draft; `post-control-<row>` once on each control; all from the committed candidate |
| revise | `revise-<input>` on each input of the failed subset, as many runs per input as that input has in the post-change arm, only if a revise round is taken |

Thirty-two Redline invocations and sixty-four judgements before any revise round. The controls run in both arms because the regression clause is read against the in-session pre-change arm, as the readiness addendum settles; #383's plan ran them in the post-change arm only, so running them pre-change is part of this ticket's method.

**A clean control is run once, not twice.** The protocol's rule on a clean control asks for a response-target and a file-target run. The ticket fixes #383's matrix, so only the response-target run is made, as in #383, #397 and #402. That is a declared narrowing.

## Judging

Two independent judges per run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket. The eight draft runs of the post-change arm and the four of the pre-change arm are judged by [`redline-judge-brief.md`](redline-judge-brief.md), the controls by [`control-judge-brief.md`](control-judge-brief.md). Both are byte copies of #383's, which are byte copies of #377's; neither mentions a claim account, an added claim or an assurance. A control judge's message carries the row's frozen expectation as one paragraph headed **Frozen expectation**, as the brief says: the row's *Frozen expectation and rejection* cell at `81f50bfd`, copied verbatim to the run's `expectation.md`.

**Neutral paths.** Each judge gets a directory of its own made by `mktemp -d` under the system temporary directory, whose path names neither the arm, the input, the run nor this ticket, holding `work/input.md`, copied from the packet's `supplied-input.md`, and `response.md`, copied from its `response.txt`, and nothing else; the packet's other files name the revision and the model. The judge writes `judgement-<letter>.md` there and keeps any scratch of its own there. The judgement is copied into the run's directory as `judgement-a.md` or `judgement-b.md`, the mapping from directory to run is kept in `runs/judges.tsv`, and each directory is removed once its judgement is copied. The two judges of one run are dispatched together and are not told of each other.

One judge suffices for a mechanical check — reading a reply for a finding or a sentence, a diff, the inventory — and those the dispatching session makes itself from the recorded files.

## Criteria, fixed before the runs

### `A2`, as the readiness addendum reads it

#383's plan defines `A2` on a reply: *a judge finds no statement false against the returned text, and no kind of difference the account leaves uncovered.* Neither brief names `A2`; a judge's reading of it is taken from its judgement as follows.

- **A judge records an `A2` miss** where its judgement, under any heading, calls a statement of the reply false, inaccurate or misleading against the returned text, or records under heading 2 a difference the reply does not report, or reports inaccurately.
- **The miss counts against #398** only where it turns on one of two things, as the readiness addendum settles:
  1. **The assurance** — a statement of the reply about what the run did, or did not do, to the claims: that none was removed, changed, moved or added, that nothing else happened to them, or the like. It counts where the judge finds it false or misleading against the returned text, or where it contradicts a finding, a claim-account entry or a summary sentence the same reply states.
  2. **An added claim** — a difference whose returned text asserts something `work/input.md` has no counterpart for, an inference drawn from existing text among them where it asserts something the input did not say, that the reply does not report as a claim the run added: naming the assertion and saying that the text did not make it before. Whether the difference is such a claim is read from the judge's own description of it; whether the reply reports it so is read from the reply, and quoted.
- **One judge is enough to fail a reply**, as in #383's practice and as the clarifications settle. A reply meets `A2` as read here when neither judge records a miss that counts against #398.
- **Every other `A2` miss is recorded and not counted here.** Where one of the tickets under *Whose miss* carries it, it is recorded under that ticket's number; where none does, it is filed as the exit says.

**Also recorded, not scored.** For every post-change reply, the dispatching session records whether the reply has an added-claim part of its claim account and what it lists, and, for every difference either judge describes as an assertion the input had no counterpart for, whether that part carries it.

### What the ticket's criteria read

1. **Target.** `A2`, read as above, is met on each of the eight post-change runs on the four drafts and on `post-control-web-copy-flawed`.
2. **Regression.** No control that meets `A2`, read as above, in the pre-change arm misses it in the post-change arm. `control-web-copy-flawed` is a target, not a regression control; it must not go from meeting `A2` to missing it all the same.

**Target criterion** is criterion 1. The candidate **beats the pre-change arm** when a larger share of the four drafts' replies meets `A2`, read as above, in the candidate arm (of eight) than in the pre-change arm (of four), and `control-web-copy-flawed` does not go from meeting it to missing it.

**Reproduced.** The pre-change arm reproduces the defect when at least one of `pre-<draft>` or `pre-control-web-copy-flawed` misses `A2`, read as above.

### Also on every run

- **`O1`**, from the runner's before-and-after inventories and the wave inventories.
- **`S1`**: the working directory held `input.md` and nothing else when the session started, read from `supplied-input.md` and the runner's before-inventory.
- **`R1`** on the drafts and **`C1`** on the controls, as the judges give them under heading 4, read by #397's split rule. Recorded, and compared across arms, but not a criterion of this ticket: the ticket's criteria are `A2` and the regression clause.

`A1`, `N1`, `N2`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are recorded `skipped` on every run, naming `A2`, `O1` and `S1` as this evaluation's criteria.

### Whose miss

A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one: #397 (paratext authored into a finished text), #399 (a length change left out of the account, as on `case-study-clean`), #400 (a paratext change — a headline, a standfirst, a subheading — accounted for as something else), #402 (anatomy conformance reported unexamined), #415 (an unhedged assertion mounted above a kept limit), and #429 to #432, which #397 filed from the same inputs. An unreported added claim counts against this ticket even inside paratext the run authored; the authoring itself is #397's. A headline or standfirst change reported as a change of wording that is in fact a change of what a claim says with a counterpart is #400's; the same change asserting something with no counterpart is an added claim and this ticket's. Both judges' readings are recorded.

## Inventory scope

Scopes 1 and 2 — the run's working directory, its staged install and its scratch — are the runner's before-and-after inventories of the run's private root. Scopes 3 to 5 are read around each arm by [`runs/wave_inventory.sh`](runs/wave_inventory.sh), which is #402's with this build's paths, calling [`runs/inventory.sh`](runs/inventory.sh), a byte copy of #383's:

3. **The rest of this build's scratch root**, the other runs' packets among them.
4. **This build's working tree and the main checkout** `/Users/thomas/Projects/skills`, by `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` read without taking the index lock. Both carry other work in progress, so a hash of either would report an editing session's change as a run's; this is the narrowing #383 declared.
5. **The session scratchpad** `/private/tmp/claude-501/-Users-thomas-Projects-skills/40416275-c971-4568-a8ae-051cb6943e72/scratchpad/`, which sibling builds also write to. A change there is attributed by path before it is named in any run's `side effects`.

A *wave* is the set of runs in flight between two wave inventories. A change under scope 3, 4 or 5 that cannot be attributed to one run is named in the `side effects` field of every run of that wave.

## Exit

1. **Not reproduced.** Where the pre-change arm does not reproduce the defect, the result is recorded as not reproduced. Thomas's ruling ships all the same: the candidate is written, the post-change arm is run and scored, its result is written down as measured, and no decision record is written.
2. **The candidate** ships where the post-change arm meets criteria 1 and 2.
3. **One revise round**, at most, where it does not, no larger than the subset that failed: the inputs on which criterion 1 or 2 was missed, run again against a revised candidate committed first, as many runs per input as that input has in the post-change arm. The criteria are then read over the revised subset in place of the first candidate's runs on those inputs. Where the revised candidate meets them, it ships. Where it does not, the wording with the larger share of `A2` passes, read as above, on the four drafts ships, and on a tie the first wording ships, as the clarifications settle. The ruling ships either way, as the correction of 19:39 UTC requires: no revert and no decision record follow from a miss.
4. Either way the result is written as measured, and each remaining miss — a criterion the shipped wording misses and a control it regresses — is filed as its own `needs-triage` ticket naming #398.

No criterion is softened, no frozen plan, brief or fixture is edited to fit a result, and no arm is re-run to get a better reading.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun. A void run's packet is moved whole to `voided/` beside `runs/` before its input is run again. A run that completes and stops is a finding.

## What is written

This file, the two judge briefs and the two inventory scripts, committed before the first run; `results.md` beside them with the outcome whichever way it falls; the judged packets under `runs/`, each with `expectation.md` for a control and `judgement-a.md` and `judgement-b.md`, with `runs/judges.tsv` and the wave inventories; any void run under `voided/`; and one record, `../records/redline-claude-2026-09-24-398.md`, in the protocol's format. Its line for `../records/README.md` is appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
