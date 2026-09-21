# Plan for #363: idiomatic quoted speech, and leaving a working quotation alone

Frozen on 2026-09-21, before the first run of either arm and before any product change. Base: `main` at `8a37e57e`. The three contrast fixtures and their criteria are frozen beside this file, in [`fixtures/README.md`](fixtures/README.md).

The ticket's readiness addendum of 2026-09-20 is the requirement wherever it touches the body, and this plan is written against it.

## The two failures

One sentence of synthetic interview speech carries both of them: *We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.*

- **Swedish.** Renderings such as *innan nästa hus börjar* and *innan nästa byggnad kommer i gång* leave a Swedish reader to supply the activity. A house does not begin in Swedish. It is an L1 defect in the target language, not a spelling error, not an invented fact, and not a demand for one particular replacement word.
- **English.** *before the next building starts* works in the full English account, and a review has nevertheless expanded it. The meaning survived; no concrete English obstacle motivated the change, so R1's preservation duty failed.

The same word shape is right in one language and wrong in the other. What a change here has to buy is detection in the first case **without** loss of preservation in the second, and the two are measured together.

## The hypothesis this arm tests

One rule, stated where each Skill needs it, that asks a question about the target language rather than about the reader's ingenuity:

> A figure the language itself uses — an ellipsis, a metonymy, a conventional shorthand — is read as that language reads it and is left alone. A construction that carries only because the source language says it that way is a defect, and what makes it one is that the reader of this language has to supply a word this language does not supply. That the meaning can be worked out is not the test.

The prediction is asymmetric and therefore falsifiable: the Swedish rows gain detections, the English rows lose none. A candidate arm that gains detections and also gains English expansions has failed, and the shorter wording ships.

Two things are deliberately not attempted. No replacement sentence is written into any surface, and no general prohibition on metonymy or on clarifying a quotation is introduced. The removed attempt at `git show 3f21d9b1:skills/editorial/redline/references/quotation-review.md` — 418 words and a full artefact in a fresh seat at every review and re-review — returns only on a showing it does not have.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from driving a Codex harness, so nothing here starts the GPT harness under `editorial-329/harness/`, and **the GPT-family failures this ticket inherits stay failed and are not retested**. A GPT-family retest is a separate step, ordered separately.

The staging is the method frozen in [`../editorial-362/runs/plan.md`](../editorial-362/runs/plan.md):

- A byte copy of `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` side by side in a private staging directory, so the shim finds the Manager beside the Skill and the global install is never read. One staged install per arm: the baseline install is `main` at `8a37e57e` unchanged; the candidate install is that tree plus this ticket's change and nothing else.
- One fresh subagent per invocation, of type `kntnt-opus-high` (`claude-opus-5`, high deliberation), with no history. The session's own seat is `claude-opus-5`; runs are delegated to a fresh subagent of that same model at high deliberation, which is a declared difference from "inherit the session's identity" and is recorded as one.
- The turn names the staged `SKILL.md` as its instructions and `$HERE` as its directory, and carries the Formal Invocation verbatim. The staged copy is not an installed Skill, so the Skill tool cannot start it.
- One working directory per run, holding only `source.md` (Write) or `input.md` (Redline) and nothing about where it came from.
- A `sha256` inventory of every writable location staged for the run — the whole working directory, the run directory and the staged install — before and after.

Four evaluator instructions are added to each turn and declared here because they are not the Skill's:

1. Copy Write's source-check scratch, and Redline's private mechanical input and result, to `evidence/` before the Skill removes them.
2. Save the complete user-facing reply verbatim to `response.md`.
3. Save the delivered text — the draft a Write run delivers, the artifact a Redline run delivers — to `delivered.md`, exactly as the reply carries it and with nothing added, and write nothing there where the run delivered nothing.
4. Write the UTC timestamp to `started.txt` before the run begins and to `finished.txt` when it ends, which is where the wall times in `results.md` come from.

None of them changes what the Skill does, and each is visible in the run directory as a file the Skill did not write.

## The frozen matrix

Two arms, because no Claude-family baseline exists for either failure: this family's only case-study run to date is `case-study-en_US-r1` in `editorial-362/runs/`, which delivered and passed F1, G2 and L1. The baseline arm exists to learn whether this family reproduces the defects at all, and the GPT-family failures stay failures whatever it shows.

These counts are the floor, per row. A row may be added; none is removed.

| Row | Input | Invocation | Baseline | Candidate |
| --- | --- | --- | --- | --- |
| `case-study-sv` | corpus `sources/case-study.md` as `source.md` | `/write --genre=case-study --language=sv --output=response source.md` | 2 | 3 |
| `case-study-en_US` | same source | same with `--language=en_US` | 1 | 2 |
| `case-study-en_GB` | same source | same with `--language=en_GB` | 1 | 2 |
| `sv-control` | `editorial-329/followup/runs/final-idiom-control/redline/supplied-input.md` | `/redline --output=response input.md` | 1 | 2 |
| `sv-artefact` | `editorial-329/followup/runs/final-delivery-original/case-study-sv-r1/draft.md` | same | 1 | 2 |
| `en-positive` | `editorial-329/followup/runs/third-candidate/case-study-en_US-r2/draft.md` | same | 1 | 2 |
| `en-us-r1` | `editorial-329/followup/runs/account-candidate/case-study-en_US-r1/redline/supplied-input.md` | same | 1 | 2 |
| `metonymy-sv` | `fixtures/metonymy-sv.md` | same | 1 | 2 |
| `rhythm-en_GB` | `fixtures/rhythm-en_GB.md` | same | 1 | 2 |
| `ellipsis-sv` | `fixtures/ellipsis-sv.md` | same | 1 | 2 |

Every delivered Write draft additionally gets one paired fresh source-blind Redline run on the delivered artifact, which is the body's *verkliga kandidat-Write→färsk-källblind-Redline-anrop*. In each Redline row the whole file is replayed as `input.md`; the corpus row's `--genre`/`--language` flags are not used, because the recorded replay of these inputs used neither.

`sv-control` is byte-identical to `corpus/editorial-quality/controls/case-study-clean.md`, and that corpus row's frozen expectation says nothing about this L1 miss. The fixture is not edited and the corpus row is not rewritten to mention it.

A run that stops for a finding **unrelated to the quotation** is recorded as a stop with its reason and its wall time, is not counted against the translation control, and **that row may be re-run once**. No other row is re-run, and every run is kept whatever it shows.

## Criteria, fixed before the runs

Judged from the delivered artifact, the run's own reply, the run directory and the inventories. Where a criterion turns on a judgement, two independent judges see the artifact and the criterion and are given neither the ticket, nor the hypothesis, nor any model identity; where they split, both classes are recorded and neither is an oracle. One judge suffices for a mechanical question: byte identity, a count, the presence of a file.

- **`K-translate`** (the addendum's translation control). Of the candidate `case-study-sv` runs not recorded as a stop for a finding unrelated to the quotation, at least two exist and every one delivers a draft; and in every delivered `sv` draft two independent judges both class the Maya Lind quotation as idiomatic Swedish speech whose meaning, stance, qualification and customer voice are unchanged. An omitted optional quotation is a fail. A delivered draft whose quotation leaves the reader to reconstruct the activity is a fail, whatever wording replaces it.
- **`K-repair-sv`** (Swedish source-blind repair). Both frozen Swedish inputs are replayed in both arms. In every candidate run, either the quotation is repaired using only what that text carries — two judges agreeing the repair invents no event and adds no fact — or the obstacle is reported with the delivered artifact and the uncertainty left standing. Inventing an event is a fail. A change the run's own reported findings do not name is a fail.
- **`K-preserve-en`** (English and contrast preservation). For each of `en-positive`, `en-us-r1`, `metonymy-sv` and `rhythm-en_GB`, every candidate run returns the working quotation unchanged, or reports a finding naming a concrete obstacle in that language visible in the text alone. An expansion no reported finding names is a fail, and a passing old replay does not excuse a failing new pair. The fixture criteria `C-metonymy`, `C-rhythm` and `C-ellipsis` are judged as `fixtures/README.md` states them.
- **`K-separate`** (the body's fifth criterion, still in force). Claims, attribution, the customer's reservations, chronology and metadata are judged separately from idiom. No fixed replacement sentence, no general metonymy ban and no widened source duty for Redline is introduced.
- **`K-chain`** (chain and transport). From the run directories and the inventories: Redline's private mechanical input is frozen complete, its separate complete Proofread result exists and is read, the delivered artifact is byte-identical to that result, the Correction Budget is the existing default, and both the no-change branch and a final delivery are exercised.
- **`K-cost`**. Mandatory reading in words and median wall time reported per arm. A wording that adds reading ships only where the candidate arm removes a miss the baseline arm reproduced in at least two runs; otherwise the shorter wording ships.
- **F1, G2, L1, R1** from [the corpus README](../corpus/editorial-quality/README.md), on every delivered draft and every Redline pair, so that a repair to idiom is not bought with a fidelity or a genre defect.

**T1 and R2 are recorded `skipped`**, with the reason that a subagent's transcript is not readable from the session that started it. Nothing here claims they passed and nothing is failed for lacking them; the loading question is carried instead by an independent documentary review of the whole load chain, in `reviews/`.

A finding of the shape [#377](https://github.com/Kntnt/skills/issues/377) owns — Redline deleting or hardening a sentence that limits what a text claims, or an unreported change of taste to a clean text — is recorded against #377 and is neither fixed nor counted here. So are findings of the shape [#389](https://github.com/Kntnt/skills/issues/389), [#390](https://github.com/Kntnt/skills/issues/390) and [#391](https://github.com/Kntnt/skills/issues/391). The two-comparison delivery gate belongs to [#376](https://github.com/Kntnt/skills/issues/376) and is not touched to make a criterion pass.

## Exit

One revise-and-remeasure round. If a criterion is still unmet after it, the measured result is recorded as measured, the shipped wording is the better of the two arms, the remaining miss is filed as its own ticket labelled `needs-triage` naming #363, and the ticket is done. No criterion is softened to fit a result.

## What is written

`results.md` beside this file; the run tree under `runs/`; the independent reviews under `reviews/`; and records under [`../records/`](../records/README.md) in the protocol's format. Nothing already frozen is edited — not the corpus, not anything under `editorial-329/`, not anything under `editorial-362/`.
