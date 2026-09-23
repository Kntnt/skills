# Checker diagnostic for #379: a negated claim tested in the direction the negation needs

Frozen on 2026-09-21 before any run of this evaluation was made, and before any wording for `skills/editorial/write/references/source-check.md` was drafted. Nothing below is edited after the first checker starts; what the runs produce goes in [`results.md`](results.md) and under [`runs/`](runs/) and [`judging/`](judging/).

This is a neutral diagnostic of the comparison operation alone, in the Claude family, as [`../editorial-362/checker/plan.md`](../editorial-362/checker/plan.md) is. It is not a Skill evaluation, it invokes no Skill, and it cannot close the ticket by itself.

## The question

Write's comparison task tells a checker that "A term carried into another language names the same thing only where nothing in this context could fall under one term and not the other", and then to "test both directions". Under a **negation** the direction that matters is reversed: a broader term makes a denial *stronger*, so "the report measures nothing about X" is supported by a source denying Y only where everything that counts as X also counts as Y. The #362 evidence records a checker clearing such a passage in one direction only ([`../editorial-362/runs/opinion-en_US-r2/write/evidence/check/report.md`](../editorial-362/runs/opinion-en_US-r2/write/evidence/check/report.md)), and the observation that this is a defect is the evaluator's alone.

Two questions, the first gating the second: is the one-directional test a repeatable behaviour of the checker, and does it let a real defect through? This plan measures before it changes anything.

## What is run, and what is not

**No Skill is invoked.** Every run is one checker: a fresh subagent given one fixture file, the resolved language, and one arm's prompt file — the fresh-checker framing, the Claims section of the base contract inlined, and the arm's task line verbatim under `## Task`, in the shape of [`../editorial-362/checker/candidate-3-task.md`](../editorial-362/checker/candidate-3-task.md). It receives no findings, hints, expectations, ticket text or earlier reports. It writes one report file and nothing else.

**Provider family `claude`**, per [`../protocol.md`](../protocol.md). No Codex Harness is started and no GPT model is run, by this evaluation or from it.

**Seat.** Every checker and every judge is a fresh `claude-opus-5` subagent at high deliberation with no conversation history, as [`../editorial-362/README.md`](../editorial-362/README.md) records for that evaluation. `source-check.md` tells a writer that a checker inherits the Main Seat; that is the product's rule and not this diagnostic's, and a diagnostic run on a weaker seat measures the seat instead of the task.

**No record is owed under [`../records/`](../records/README.md)**, and none is added there or to its README. That format is per Skill invocation: [`../protocol.md`](../protocol.md) requires an `invocation` field holding the Formal Invocation as typed and a `fixture` field naming a fixture from the corpus index, and this evaluation has neither. The #362 checker diagnostic wrote no such record for the same reason and reported itself in `checker/results-round-1.md` and `checker/results-rounds-2-3.md`.

**Nothing frozen elsewhere is edited.** Nothing under `../editorial-362/`, `../editorial-329/` or `../corpus/` is touched by this evaluation, and `../README.md` is not edited.

## The two arms

| Arm | Task line | Where it is frozen |
| --- | --- | --- |
| `shipped` | The single blockquoted line beginning "Compare the complete draft" in `skills/editorial/write/references/source-check.md`, verbatim from `main` as this ticket found it at `76ddacc1`. | [`arms/shipped-task.md`](arms/shipped-task.md) |
| `reworded` | The same file with that one line changed, and nothing else in the file different. Written only if the gate below is not met. | `arms/reworded-task.md` |

The two prompt files differ in that line alone. No figure recorded under `../editorial-362/` appears on either side of any comparison here: that evaluation's `candidate 3` arm is not the shipped text (its README records three words changed after its runs), and #378 moved the same line again before this ticket started. The shipped arm is measured here, in this session and under this seat, so that #378's edit is outside the comparison instead of scored as this ticket's effect.

## The fixtures

Two, newly written for this ticket. Each is one file in the form the established fixtures use: complete supplied material — synthetic-material line, brief, underlag, boundaries — then the complete draft with its frontmatter. Swedish source and `en_US` draft, the pair the motivating defect arose in and the pair every established fixture that bears on it uses. Neither reuses the *funktionsförmåga*/"ability" passage, which is disputed and can settle nothing.

| Fixture | Origin | Term pair | Designed class |
| --- | --- | --- | --- |
| [`fixtures/bd1-broadened-denial.md`](fixtures/bd1-broadened-denial.md) | Written for this ticket (#379). Not taken from the #329 evidence or from any earlier evaluation. | Swedish *förkunskaper* (prior knowledge) → English "knowledge" | **Broadened denial.** The source denies something of the narrow term; the draft denies it of the broader one. No supplied statement excludes the case that separates them. A finding against the focus passage is **correct**. |
| [`fixtures/nd1-narrowed-denial.md`](fixtures/nd1-narrowed-denial.md) | Written for this ticket (#379). Not taken from the #329 evidence or from any earlier evaluation. | Swedish *hälsa* (health) → English "mental health" | **Narrowed denial.** The source denies something of the broad term; the draft denies it of the narrower one. A narrower denial is entailed by the broader one, so a finding against the focus passage is **false**. |

### `bd1-broadened-denial` — the designed fault

Source passage: `Den mäter inte deltagarnas förkunskaper.`

**Focus passage**, exactly as the draft carries it:

> The evaluation does not measure participants' knowledge.

The material denies only that the evaluation measures participants' *prior* knowledge. The draft denies that it measures participants' knowledge at all. The case that separates the two terms — an evaluation that records what participants knew at the end of the course, which is knowledge and is not prior knowledge — is compatible with the supplied material, and no supplied statement excludes it: the material says what the evaluation rests on and what it counts without claiming that list is everything it holds. The source's statement therefore holds where the draft's fails, and the draft's denial asserts more than the material carries.

### `nd1-narrowed-denial` — the designed non-fault

Source passage: `Enkäten frågar inte om deltagarnas hälsa.`

**Focus passage**, exactly as the draft carries it:

> The questionnaire does not ask about participants' mental health.

The material denies that the questionnaire asks about participants' health. The draft denies that it asks about their mental health, which the material's denial entails. The reverse case — a questionnaire that asks about physical health but not mental health, so that the draft's statement holds and the source's fails — is not compatible with the supplied material, which states that the questionnaire asks about health not at all. No case stands in either direction. The draft differs from its source at this passage only in denying the narrower term, and everything else it carries from the material is unchanged.

## Run counts, exact

Not floors. No row is rerun selectively and no report that reached disk is excluded.

- **Gate round.** `shipped` arm: exactly **six** runs on `bd1` and exactly **six** runs on `nd1`.
- **Comparison round**, made **only** where the gate below is not met: `reworded` arm exactly six runs on `bd1` and six on `nd1`; and **both** arms at exactly **three** runs on each of the seven established fixtures in `../editorial-362/checker/fixtures/` — `p1-opinion-variable`, `p2-chronology`, `p3-document-scope`, `p4-person-attribute`, `n1-column-reflection`, `n2-opinion-sufficiency`, `n3-column-withheld`. The shipped arm's runs on the seven are made then and not before: the seven bear only on whether a rewording makes something worse.

Reports are written under `runs/<arm>/<fixture>-r<n>.md`.

## A run whose report never reached disk

A report file that reached disk is judged as it stands, however short, hedged, incomplete or malformed, and is never dropped, reworded, rerun or excluded from a count.

A run that wrote **no** report file produced no evidence in either direction. It is recorded in `results.md` with its arm, its fixture and the harness error; it enters no count; and **one replacement run** is started in the same arm and fixture under the same conditions, so the exact counts above still hold. The replacement is recorded as one. Where a single arm and fixture needs more than three replacements, the builder stops and reports the obstacle on #379 rather than running on.

## Judging

**A judge is given** the fixture file, every report it is to judge under shuffled neutral names, the judge brief at [`../editorial-362/checker/judging/judge-brief.md`](../editorial-362/checker/judging/judge-brief.md), and that fixture's focus passage. It is given **neither arm's task line**, nor the designed class, nor the ticket, nor which arm any report came from, nor how many runs were made or how the reports divide between arms. A judge plainly sees how many files it holds; that was never what the blinding is for. The key mapping neutral names to runs is written to a `key.json` beside the reports and is never in a judge's reach.

**Both arms' reports for one fixture go to the same two judges, shuffled into one set.** Classing two arms by separate panels is the caveat `../editorial-362/README.md` records as having put two values on its own detection figure.

- **Gate round.** The shipped arm's six reports per new fixture, each fixture's set to two independent judges. Its counts answer the gate and nothing else.
- **Comparison round**, only where the gate is not met. For each of the nine fixtures, every report of both arms shuffled into one set, to two fresh independent judges. Every number in the comparison comes from this round, and no gate-round count is ever compared with a comparison-round count.

### The two questions

Each judge answers both, per report.

1. **Did this report file a finding against the focus passage named for this fixture?** A question of fact about the report's own text.
2. **On the judge's own reading of the fixture, is a finding against that passage correct?**

**The second question produces no count at all.** Both judges' answers are recorded, and where either contradicts the frozen designed class, `results.md` says so in a sentence. **The frozen designed class decides every count**, so the comparison holds whichever reading is right.

**Every count this evaluation turns on comes from the first question**, settled thus, before the first run:

- **What counts as a finding.** What the judge brief already counts: an item the report itself presents as a finding, whatever it calls it and at whatever severity, and not an item it clears, or records as a note, an observation or a watch-item without asking for a repair.
- **What counts as against the passage.** The focus passage is the exact quoted draft sentence given above for each fixture. A finding is against it only where the draft passage the report quotes is that sentence or a span inside it. A finding on a neighbouring sentence is not one, and is recorded among the report's other findings.
- **The tie-break.** Where the two judges disagree on the first question, the report is counted as the reading that **fails that fixture's criterion**. Where filing a finding is what the criterion wants — `bd1`, and the four real-fault fixtures under criterion D — the report counts as not having filed one. Where the absence of a finding is what the criterion wants — `nd1`, and the three supported-prose fixtures under criterion P — it counts as having filed one.

The miss shape the #362 evidence records is a report that names the real difference and then accepts the passage anyway, which is precisely the report two careful readers read two ways; a finding one careful reader cannot see is not a finding the writer downstream would act on. The criterion the established seven are already judged by says the same: "Noticing the difference and then accepting it is a fail". The rule is applied identically to every report of every arm, so it favours neither arm.

Because it moves numbers, it is reported. `results.md` gives, per arm and per fixture, the count the tie-break produces — which is the count every gate is read against — the number of reports the judges split on, and beside it the count the opposite resolution would have produced.

### The established seven

They carry no negated passage, so the scheme above is read against them through **criterion D** and **criterion P** as `../editorial-362/checker/plan.md` defines both under "Criteria, fixed before the runs", each fixture's focus passage and established judgement taken from that plan's fixture table. The first question there is whether the report filed a finding against that focus passage, and the same tie-break settles a split. "Criterion D over the four real-fault fixtures" and "criterion P over the three supported-prose fixtures" below mean D and P as that plan states them, and nothing wider.

## The two gates, frozen

**Gate 1 — whether anything is reworded at all.** One statement, one polarity:

> The gate is **met** where the `shipped` arm files a finding against `bd1`'s focus passage in **at least five of its six runs** on `bd1`, counted by the first question and the tie-break above.

Met: `source-check.md` is left unchanged, no file under `skills/` changes, no catalog regeneration is owed, `results.md` says so, and any finding counted against `nd1`'s focus passage is filed as its own `needs-triage` ticket naming #379. Not met: exactly one `reworded` arm, and no more.

**Gate 2 — whether a reworded line ships.** A conjunction of four conditions, all read against the `shipped` arm measured in the same comparison round and against no figure recorded under `../editorial-362/`:

1. Detection on `bd1` **rises**.
2. Findings counted against `nd1`'s focus passage **do not rise**.
3. Criterion D over the four real-fault fixtures **does not fall**.
4. Criterion P over the three supported-prose fixtures **does not fall**.

The reworded line ships only where it clears all four. Where it does not, `source-check.md` is **left unchanged**, whatever the reworded arm gained on one condition; the measurement is recorded as measured; the remaining miss is filed as its own `needs-triage` ticket naming #379 and carrying both arms' figures; and there is no second reworded arm. No criterion is softened to fit a result.

## The rewording, if one is made

It starts from the first half of the drafted replacement in [`../editorial-362/reviews/load-chain-review.md`](../editorial-362/reviews/load-chain-review.md) — *name a case in which the draft's statement holds and the source's fails, and a case in which the source's holds and the draft's fails* — written under `/writing-for-agents`. That review's closing disjunct, "or say that one suffices", is the opposite of what this evaluation tests and is not available to it. Another wording may be taken, and the commit says why it was taken instead.

## What `results.md` reports

- Per arm and per fixture and per run: both judges' answer to the first question and the outcome counted for it.
- Per arm and per fixture: the counted figure, the number of splits it rests on, and the figure the opposite resolution would have given.
- Both judges' answers to the second question, and a sentence wherever either contradicts the frozen designed class.
- Per arm: the word count of the blockquoted task line, and the median wall time per run — from the subagent's start to its report write — over the two new fixtures and, separately, over the established seven where those runs were made.
- The commit the shipped arm's task line was copied from.
- Every run that wrote no report, with its arm, its fixture and the harness error.
- Why no record is owed under `../records/`.
