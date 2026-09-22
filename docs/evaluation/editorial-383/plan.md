# Redline and the passage no finding named — evaluation plan for #383

Frozen on 2026-09-22, before the first run of this evaluation. Nothing in this file, in the two turn files beside it, or in the two judge briefs beside it is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first, then [#377's plan](../editorial-377/plan.md), which this one re-uses as it stands; this file says only what those leave open and what this ticket settles differently.

## What is under test

Redline, as [#377's post-change arm](../editorial-377/results.md) left it, rewrites a clean passage to taste outside any finding and mostly does not report it. Every one of the six `R1` failures in those eight runs turns on that, and four of the twenty control judgements name it as their one reservation. The change this evaluation measures is three things, settled by #383's triage comment and not open here:

- a trace check in `skills/editorial/redline/SKILL.md` step 7, beside the claim comparison, that traces every difference between the returned text and the pre-round Text Artifact to a finding of the review that commissioned the round, and restores an untraced passage byte for byte from the pre-round text;
- a closing summary in step 11, one paragraph saying by kind what the run changed beyond the claim account, built from the run's own comparison of the text as it arrived with the text it delivers;
- the "doing real work" guard in `skills/kntnt/library/references/editorial/anti-slop.md` stated as a test applied before a pattern becomes a finding, with *Synonym cycling* saying that the pattern needs names denoting one thing.

Unslop receives the same two procedural changes in its own *pattern* vocabulary. **Unslop is not measured here**: #385 measures it, and nothing in this evaluation says anything about it.

Two arms:

- **Pre-change**, the product as it stands at `3167fb68`, which is the tree this ticket was begun on. Four runs, one on each input.
- **Post-change**, the product after the change. Eight runs on the same four inputs, and ten control runs.

Redline is never given source material in any run of either arm. The only file in a run's working directory is `input.md`.

### Why the pre-change arm is replayed rather than re-used

#383 allows #377's post-change arm to serve as this ticket's pre-change arm **provided nothing Redline loads has changed since those runs**, and requires that to be verified by diffing Redline's shipped files and every library resource its step 5 loads against `0f490dd4`, the corpus commit [`../records/redline-claude-2026-09-20-377.md`](../records/redline-claude-2026-09-20-377.md) names.

That diff is not empty. Twenty-seven files differ, and the differences are substantial rather than editorial: `references/editorial/article-anatomy.md` and its review extension, `references/editorial/headlines.md` and its review extension, and `scripts/article_anatomy.py` did not exist at `0f490dd4` and are now loaded, measured with and reviewed against for the `article`, `case-study`, `column` and `opinion` genres; `base.review.md`, `delivery.md`, the seven genre resources, both techniques, the shared craft brief, Redline's own `SKILL.md`, its `help.md` and its correction brief all changed. So #377's runs are not runs of this product, and the four inputs are replayed once each as a fresh pre-change arm before any wording is changed.

The replay is recorded in this evaluation and not in #377's, whose records stay exactly as they stand.

## The one rule for what a difference traces to

The definition this evaluation uses is the one the triage comment settles, and it is the shipped wording's own:

> A difference traces where it repairs what a finding named, or where that repair necessitates it — agreement after a changed subject, a transition the repair would otherwise break.

A difference that traces to nothing is a **difference outside any finding**. The judge brief beside this file does not use that vocabulary and is not told it: it classes each difference as a mechanical correction, the repair of a visible defect, a change of taste, or a change to what a claim says. **A change of taste is how a difference outside any finding reaches this plan**, and the counting rule below is written in the judge's vocabulary for that reason.

The six-element list for a change to what a claim says — **scope, certainty, attribution, chronology, causality and meaning** — is unchanged from #377 and is what the judge brief carries.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from driving a Codex Harness, so no GPT harness and no GPT model is started, controlled or invoked here, directly or through any tool, script or subagent.

Each run is one fresh subagent with no history, of type `kntnt-opus-high` (`claude-opus-5`, high deliberation). The correction subagents and the nested Proofread invocation that a run starts inherit that seat, as they did for #377. Every judge is a fresh subagent of the same type. The dispatching session's own seat is `claude-opus-5`; runs are delegated so that each one is fresh and carries nothing of this session's knowledge of the ticket.

The staged copy is not an installed Skill, so the Skill tool cannot start it. The turn names the staged `SKILL.md` as its instructions and `$HERE` as its directory, and carries the Formal Invocation verbatim. Two installs are staged, each a byte copy of `skills/editorial/redline`, `skills/editorial/proofread` and `skills/kntnt` side by side, so that the shim finds the Manager beside the Skill and no global install is ever read:

- `…/383.scratch/install-pre` — the tree at `3167fb68`. Used by [`redline-turn-pre.md`](redline-turn-pre.md).
- `…/383.scratch/install-post` — the tree after the change. Used by [`redline-turn-post.md`](redline-turn-post.md).

`…` is `/Users/thomas/Projects/skills/.git/orchestrate-session-383-389-claude/383.scratch`, this session's scratch directory. Each install is written with `git archive` from the commit it names, never copied from a working tree, because two sessions are editing this repository while these runs are made.

The two turn files are [#377's](../editorial-377/redline-turn-post.md) with two substitutions and no other change: that scratch path in place of #377's, and the sentence naming the checkout a run may not read now naming both checkouts of this repository on this machine, since a second one exists.

Each run has its own working directory holding only `input.md` and, once the run creates it, `scratch/`. One evaluator instruction is added to the turn and declared here because it is not the Skill's: save the user-facing reply verbatim to `response.md` in the run directory. No other statement is added, and neither turn file paraphrases or replaces a step of the staged `SKILL.md`.

No hint of the defect under investigation appears in any turn, in any invocation, or in any judge brief.

## The matrix

The four inputs are the `work/input.md` of the four Redline runs #362 recorded, copied byte for byte, which are the same four files #377 used. Each is source-blind and carries its own `kntnt` map, so the invocation names no genre and no language.

| Run | Arm | Input | Invocation |
| --- | --- | --- | --- |
| `pre-column-sv-r1` | pre | `../editorial-362/runs/column-sv-r1/redline/work/input.md` | `/redline --output=response input.md` |
| `pre-column-sv-r2` | pre | `../editorial-362/runs/column-sv-r2/redline/work/input.md` | `/redline --output=response input.md` |
| `pre-opinion-en_GB-r1` | pre | `../editorial-362/runs/opinion-en_GB-r1/redline/work/input.md` | `/redline --output=response input.md` |
| `pre-opinion-en_GB-r2` | pre | `../editorial-362/runs/opinion-en_GB-r2/redline/work/input.md` | `/redline --output=response input.md` |
| `post-column-sv-r1-a`, `-b` | post | as `pre-column-sv-r1` | `/redline --output=response input.md` |
| `post-column-sv-r2-a`, `-b` | post | as `pre-column-sv-r2` | `/redline --output=response input.md` |
| `post-opinion-en_GB-r1-a`, `-b` | post | as `pre-opinion-en_GB-r1` | `/redline --output=response input.md` |
| `post-opinion-en_GB-r2-a`, `-b` | post | as `pre-opinion-en_GB-r2` | `/redline --output=response input.md` |

The ten controls are the ten rows of the corpus's *Redline controls* table, exhaustive for this ticket. The seven rows of *Metadata, precedence and non-five-genre controls* are not run here. Each control is run once, against the post-change install, staged and invoked as the corpus says: only the linked artifact copied to `input.md`, then `/redline --genre=<genre> --language=<locale> --output=response input.md`, with no contextual instruction and no technique.

| Run | Artifact | Invocation |
| --- | --- | --- |
| `control-article-clean` | `controls/article-clean.md` | `/redline --genre=article --language=sv --output=response input.md` |
| `control-article-flawed` | `controls/article-flawed.md` | `/redline --genre=article --language=sv --output=response input.md` |
| `control-case-study-clean` | `controls/case-study-clean.md` | `/redline --genre=case-study --language=sv --output=response input.md` |
| `control-case-study-flawed` | `controls/case-study-flawed.md` | `/redline --genre=case-study --language=sv --output=response input.md` |
| `control-column-clean` | `controls/column-clean.md` | `/redline --genre=column --language=sv --output=response input.md` |
| `control-column-flawed` | `controls/column-flawed.md` | `/redline --genre=column --language=sv --output=response input.md` |
| `control-opinion-clean` | `controls/opinion-clean.md` | `/redline --genre=opinion --language=sv --output=response input.md` |
| `control-opinion-flawed` | `controls/opinion-flawed.md` | `/redline --genre=opinion --language=sv --output=response input.md` |
| `control-web-copy-clean` | `controls/web-copy-clean.md` | `/redline --genre=web-copy --language=sv --output=response input.md` |
| `control-web-copy-flawed` | `controls/web-copy-flawed.md` | `/redline --genre=web-copy --language=en_US --output=response input.md` |

Twenty-two Redline invocations in all: four pre-change, eight post-change, ten controls. Eighteen of them are the post-change arm the acceptance criteria are read against.

## Judging

Two independent judges per artefact, each a fresh `kntnt-opus-high` subagent, each blind to the expected answer, to the arm the artefact came from, to the model that produced it and to this ticket. The two judges of one artefact are dispatched together and neither can read the other's file. One judge suffices for a mechanical check — a diff, a count, the presence of a report, the before-and-after inventory — and those the dispatching session makes itself from the recorded files.

The twelve run artefacts of the four inputs, pre and post alike, are judged by [`redline-judge-brief.md`](redline-judge-brief.md), so that no judge can tell which arm it is judging. The ten controls are judged by [`control-judge-brief.md`](control-judge-brief.md), which carries that control's frozen expectation from the corpus table as its criterion and says nothing about what verdict is anticipated. Both briefs are byte copies of #377's, as #383 requires; neither was rewritten for this ticket, and in particular neither mentions a trace, a closing summary or anything else this ticket changed.

A control's frozen expectation is the corpus README row's *Frozen expectation and rejection* cell, copied verbatim by the evaluator to `expectation.md` in the run directory and named to the judge by that path, so that the brief stays the same for all ten controls.

Every judge is told in its dispatching message to keep any scratch of its own inside its own run directory. [`../editorial-377/results.md`](../editorial-377/results.md) records why: one #377 judge found a shared `/tmp` path overwritten under it mid-task by a concurrent sibling.

Nothing a counted requirement of the article anatomy turns on is supplied to a judge. #377's briefs are re-used as they stand, and they hand the judge no measured figures, so a judge weighing a control clause about a character or word count counts it itself. That is a declared limit of re-using those briefs against a product that now measures those limits by script, and it is named in the record.

Where the two judges of an artefact split, both classes are recorded and neither judge is an oracle. For deciding whether a criterion is met, the counting rule below governs.

## How a difference is counted against a run

This is the rule #383 states, and it is fixed here before any run:

> A difference counts against a run when both judges class it as taste outside any finding, or when either does and the reply covers it neither in the claim account nor in the closing summary. Where the judges split on a difference the reply does cover, both classes are recorded and neither judge is an oracle.

A mechanical correction is the closing Proofread pass's and is outside `R1`, as #377's plan already settles: `SKILL.md` step 5 forbids the review from loading mechanics guidance and step 9 hands the whole mechanical pass to Proofread. A mechanical correction therefore never counts against a run under the rule above, and the closing summary covering it as a kind is enough.

## Criteria, fixed before the runs

- **`R1`**, on every run of both arms, from the corpus: does Redline address concrete visible defects while preserving working voice, arguments, quotations and claims outside findings? Compare every before/after claim; report legitimate removals, rejected losses and irreparable findings. Clean texts may not be rewritten to satisfy taste or numerical guidelines. No unavailable-source verification.
- **`A1`**, on each of the eighteen post-change runs: no difference counts against the run by the rule above.
- **`A2`**, on each of the eighteen post-change replies: a judge finds no statement false against the returned text, and no kind of difference the account leaves uncovered.
- **`N1`**, on each of the eight post-change runs on the four inputs, as [#377's plan](../editorial-377/plan.md) defines it: no limiting sentence is deleted or hardened unless the account reports a finding of class (a) or (b) that plan defines, verified by a judge from the input text alone.
- **`N2`**, on the same eight runs, as that plan defines it: the account names every change to what a claim says, by the six-element list.
- **`C1`**, on each control: the run meets that control's frozen expectation in the corpus's *Redline controls* table, on `R1`. Corrections made by the step 9 Proofread pass do not count against a clean control, for the reason above.
- **`C2`**, on the three controls #377 recorded a blemish on: the two rewritten section headings in `opinion-flawed`, the repaired paragraph split in `article-flawed`, and the pre-echoed quote and duplicate lead in `case-study-flawed` are each now either absent from the returned text or covered by the account.
- **`O1`**, on every run, from the before-and-after inventory: the Output Target contract, source preservation and cleanup hold. An evaluator capture is not a Skill file.
- **`S1`**, on every run, mechanically: no source material was supplied. The run's working directory held `input.md` and nothing else before the turn was dispatched.

`T1` and `R2` are recorded `skipped` on every run, with the reason #377's plan gives: both are answerable only from a Harness trace, and a session cannot read the transcript of a subagent it started. Nothing here claims either passed and nothing fails for lacking them. Every other criterion the corpus applies to a run of this kind — `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — is recorded `skipped`, naming `R1`, `A1`, `A2`, `N1`, `N2`, `C1`, `C2`, `O1` and `S1` as this evaluation's criteria.

## Inventory scope

`O1` and the `side effects` field are read from a `sha256` inventory taken before and after, never from a run's report of itself. [`runs/inventory.sh`](runs/inventory.sh) writes one sorted `sha256  path` line per regular file and skips nothing; it is a byte copy of the script [#386](../editorial-386/runs/inventory.sh) froze. The scope is every writable location staged for a run:

1. **The run directory**, including `work/` and its `scratch/`.
2. **The staged install** the run reads.
3. **The rest of the scratch staging root**, other runs' directories among them.
4. **Both checkouts of this repository on this machine** — `/Users/thomas/Projects/skills-388-391`, which carries this ticket's work, and `/Users/thomas/Projects/skills`, which carries another session's — each of which every turn tells the run not to read.

Scopes 1 and 2 are inventoried immediately before each run's turn is dispatched and immediately after its reply arrives, into that run's `inventory-before.txt` and `inventory-after.txt`. Scopes 3 and 4 are inventoried once around each parallel wave, into `wave-<n>-before.txt` and `wave-<n>-after.txt` beside `runs/`.

Scope 4 is covered by `git status --porcelain --untracked-files=all` and `git rev-parse HEAD` in each checkout rather than by hashing the tree, because both trees carry work in progress while the runs are made and a hash of either would report an editing session's changes as a run's. That substitution is a declared narrowing of the protocol's wider scope, it is stated in the record, and it is strictly sufficient for the question `O1` asks: a file a run created, replaced or removed anywhere in either tree appears in that output.

Because one staged install serves a whole wave, a change under scope 2 or 3 during a wave cannot be attributed to one run of that wave. Such a change is named in the `side effects` field of every entry in the wave and in `notes`, and the narrower per-run scope is not used to explain it away.

## What each run directory holds

```text
runs/<run>/
  work/                        the run's working directory
    input.md                   the only input exposed to the run
    scratch/                   the only scratch the run may create
  response.md                  the user-facing reply, verbatim
  expectation.md               the row's frozen expectation (controls only)
  inventory-before.txt
  inventory-after.txt
  judgement-a.md
  judgement-b.md
```

## Scale, and the exit when a measurement is unfavourable

Twenty-two Redline invocations and forty-four judges. One revise-and-remeasure round is available, adding at most eight runs and sixteen judges. If a criterion is still unmet, the measured result is recorded as measured, the shipped wording is left as the better of the two arms, the remaining miss is filed as its own `needs-triage` issue naming #383, and the ticket is done. No criterion is softened and no frozen plan, brief or fixture is edited to fit a result.

## What is written down

[`results.md`](results.md) holds both arms and the controls. `runs/<run>/` holds what the section above lists. The record goes to `../records/redline-claude-2026-09-22-383.md`, in the protocol's format, and is listed in `../records/README.md`; it takes the issue after the date because `redline`/`claude` records already exist for 2026-09-22.
