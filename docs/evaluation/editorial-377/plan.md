# Redline and the sentences that limit a claim — evaluation plan for #377

Frozen on 2026-09-20, before the first run of this evaluation. Nothing in this file, in the two turn files beside it, or in the two judge briefs beside it is edited after the first run; `diagnosis.md`, `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first; this file says only what they leave open.

## What is under test

Redline, as [#362's Claude-family evaluation](../editorial-362/README.md) found it, changes or deletes sentences whose work in the text is to bound what the text asserts, and makes unreported changes to what a claim says. The change this evaluation measures is a diagnostic in `skills/kntnt/library/references/editorial/base.review.md`, a narrowing of the whole-passage removal permission in `skills/editorial/redline/SKILL.md` step 7 and `skills/editorial/redline/references/correction.md`, and a widening of the delivery and correction account from removed claims alone to every change to what a claim says.

Two arms:

- **Pre-change**, the product as it stands at `4a932dd6`. Four runs, which are the diagnosis.
- **Post-change**, the product after the change. Eight runs on the same four inputs, and ten control runs.

Redline is never given source material in any run of either arm. The only file in a run's working directory is `input.md`.

## The one rule for what a change to a claim is

The definition this evaluation uses, for the diagnosis, for the judge brief and for the shipped account duty, is the list the Collection already ships in both correction briefs:

> Every claim you received must still appear with its **scope, certainty, attribution, chronology, causality and meaning** intact unless the finding named the whole claim as the defect.

A difference is a **change to what a claim says** when it alters any of those six. `../editorial-362/runs/redline-judge-brief.md` uses a shorter four-word vocabulary; it is frozen evidence of a finished run and is not the vocabulary here.

A **limiting sentence** is a sentence or clause whose work in the text is to bound what the text asserts: that something is not measured, not claimed, not witnessed or not general, or that the text is an observation of a document rather than a scene from an occasion.

**Hardening** is any change that raises what the text asserts. Three forms are tested for, and a judge that finds a fourth records and names it:

1. A refusal to assert becomes an assertion — *We make no claim to have costed that trial* to *We have not costed that trial*.
2. A disclaimer covering two things comes back covering one — the dropped *funded or* in the same sentence.
3. A sentence whose only work is to limit is deleted outright.

Moving a claim's actor is a change to what a claim says by attribution, and is judged there rather than as hardening: it does not raise what the text asserts.

## The escape clause

A deletion or weakening of a limiting sentence is permitted only where the account reports a finding naming a defect in that sentence which a judge can verify from the input text alone, independently of the account's assertion, and only in these two classes:

- **(a)** the limit that sentence states is still stated by a sentence the text retains, so that after the deletion the text bounds what it claims exactly as far as it did before. Which words carry the limit afterwards does not matter; what matters is that no surviving claim gains scope, certainty, attribution, chronology, causality or meaning.
- **(b)** the sentence contradicts another passage of the same text.

A finding that names the whole sentence as the defect without naming a defect inside it is not one of these and licenses nothing.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from driving a Codex Harness, so no GPT harness and no GPT model is started here; a GPT-family retest is a separate run ordered on #362.

Each run is one fresh subagent with no history, of type `kntnt-opus-high` (`claude-opus-5`, high deliberation). The correction subagents and the nested Proofread invocation that run starts inherit that seat, as they did for the runs this ticket is filed from. The session's own seat is `claude-opus-5`; runs are delegated so that each one is fresh and carries nothing of this session's knowledge of the ticket.

The staged copy is not an installed Skill, so the Skill tool cannot start it. The turn names the staged `SKILL.md` as its instructions and `$HERE` as its directory, and carries the Formal Invocation verbatim. Two installs are staged, each a byte copy of `skills/editorial/redline`, `skills/editorial/proofread` and `skills/kntnt` side by side, so that the shim finds the Manager beside the Skill and no global install is ever read:

- `…/377.scratch/install-pre` — the tree at `4a932dd6`. Used by [`redline-turn-pre.md`](redline-turn-pre.md).
- `…/377.scratch/install-post` — the tree after the change. Used by [`redline-turn-post.md`](redline-turn-post.md).

`…` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/377.scratch`, this session's scratch directory. The two turn files differ in that path and in nothing else; both are written to the shape [`../editorial-362/runs/redline-turn.md`](../editorial-362/runs/redline-turn.md) froze, whose own paths belong to another session and are not reusable.

Each run has its own working directory holding only `input.md` and, once the run creates it, `scratch/`. One evaluator instruction is added to the turn and declared here because it is not the Skill's: save the user-facing reply verbatim to `response.md` in the run directory. A `sha256` inventory is taken before and after each run over every writable location staged for it — the whole working copy of this repository, the run directory, and the staged install — as the protocol requires.

No hint of the defect under investigation appears in any turn, in any invocation, or in any judge brief.

## The matrix

The four inputs are the `work/input.md` of the four Redline runs #362 recorded, copied byte for byte. Each is source-blind and carries its own `kntnt` map, so the invocation names no genre and no language.

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

The ten controls are the ten rows of the corpus's *Redline controls* table, exhaustive for this ticket. The seven rows of *Metadata, precedence and non-five-genre controls* — `metadata-none`, `instruction-none`, `legacy-abt`, `flag-pac`, `instruction-abt`, `report-pac` and `article-excerpt` — are not run here. Each control is run once, against the post-change install, staged and invoked as the corpus says: only the linked artifact copied to `input.md`, then `/redline --genre=<genre> --language=<locale> --output=response input.md`.

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

Twenty-two Redline invocations in all: four pre-change, eight post-change, ten controls.

## Judging

Two independent judges per artefact wherever a criterion turns on a judgement, each a fresh `kntnt-opus-high` subagent, each blind to the expected answer, to the arm the artefact came from, to the model that produced it and to this ticket. One judge suffices for a mechanical check — a diff, a count, the presence of a report, the before-and-after inventory — and those this session makes itself from the recorded files.

The twelve run artefacts, pre and post alike, are judged by one brief, [`redline-judge-brief.md`](redline-judge-brief.md), so that no judge can tell which arm it is judging. The ten controls are judged by [`control-judge-brief.md`](control-judge-brief.md), which carries that control's frozen expectation from the corpus table as its criterion and says nothing about what verdict is anticipated.

Where the two judges of an artefact split, both classes are recorded and neither judge is an oracle. For deciding whether a criterion is met — and so whether the one revise-and-remeasure round below is spent — the stricter of the two judgements governs; both are kept in the results and in the record, and neither is deleted or reconciled.

## Criteria, fixed before the runs

- **D1**, on each pre-change run, mechanically from the judgements: every difference between `input.md` and the returned text is classed, and for each that deletes or weakens a limiting sentence or that the account does not report, `diagnosis.md` quotes the sentence of a loaded resource that authorised it or states that no loaded resource does, naming the resources read.
- **R1**, on every run of both arms, from the corpus: does Redline address concrete visible defects while preserving working voice, arguments, quotations and claims outside findings? Compare every before/after claim; report legitimate removals, rejected losses and irreparable findings. Clean texts may not be rewritten to satisfy taste or numerical guidelines. No unavailable-source verification.
- **N1**, on each post-change run: no limiting sentence is deleted or hardened unless the account reports a finding of class (a) or (b) above, verified by a judge from the input text alone.
- **N2**, on each post-change run: the account names every change to what a claim says, by the six-element list.
- **C1**, on each control: the run meets that control's frozen expectation in the corpus's *Redline controls* table, on `R1`. Corrections made by the step 9 Proofread pass do not count against a clean control: `SKILL.md` step 5 forbids the review from loading mechanics guidance and step 9 hands the whole mechanical pass to Proofread, so a locale-mechanical correction in a returned text is that pass's and is outside `R1`.
- **O1**, on every run, from the before-and-after inventory: the Output Target contract, source preservation and cleanup hold. An evaluator capture is not a Skill file.

`T1` and `R2` are recorded `skipped` on every run, with the reason that both are answerable only from a Harness trace and a session cannot read the transcript of a subagent it started. Nothing here claims either passed and nothing fails for lacking them. Every other criterion the corpus applies to a run of this kind is recorded `skipped`, naming `R1`, `N1`, `N2` and `C1` as this ticket's criteria.

## What a control that misses means

"Still pass" is not a comparison: the only records covering these controls are `records/redline-gpt-2026-09-19-338-controls-genres.md` and `records/redline-gpt-2026-09-19-346-controls-genres.md`, both GPT-family, and the protocol forbids re-running them here. The standard is each control's own frozen expectation in the corpus table. Where a control misses it, that one control is re-run once against the pre-change install: a miss present in both arms is a pre-existing failure, recorded as measured and filed `needs-triage` naming #377, and it does not block this ticket.

## Scale, and the exit when a measurement is unfavourable

Twenty-two Redline invocations and about thirty-six judges. For each criterion that measures a model rather than a file, one revise-and-remeasure round is available, adding at most eight runs and sixteen judges. If the criterion is still unmet, the measured result is recorded as measured, the shipped wording is left as the better of the two arms, the remaining miss is filed as its own `needs-triage` issue naming #377, and the ticket is done. No criterion is softened and no frozen matrix, plan or fixture is edited to fit a result.

## What is written down

[`diagnosis.md`](diagnosis.md) holds the pre-change arm. [`results.md`](results.md) holds the post-change arm and the controls. `runs/<run>/` holds, for each run, `work/input.md`, `response.md`, `judgement-a.md` and `judgement-b.md` where the artefact was judged, and the two inventories. The record goes to `../records/redline-claude-2026-09-20-377.md`, in the protocol's format, and is listed in `../records/README.md`; it takes the issue after the date because a `redline`/`claude` record already exists for 2026-09-20.
