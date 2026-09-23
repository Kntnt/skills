# Checker diagnostic for #387: a narrowed denial filed as a defect

Frozen before any run of this evaluation was made and before any reworded task line was drafted. Frozen means committed: the commit that adds this file precedes the first checker, and nothing below is edited after it. What the runs produce goes in [`results.md`](results.md) and under [`runs/`](runs/) and [`judging/`](judging/).

This is a neutral diagnostic of Write's comparison task alone, in the Claude family, in the method of [`../editorial-379/plan.md`](../editorial-379/plan.md), which it copies wherever this file does not say otherwise. It invokes no Skill.

## The question

#379 measured the shipped comparison task on a narrowed denial, [`../editorial-379/fixtures/nd1-narrowed-denial.md`](../editorial-379/fixtures/nd1-narrowed-denial.md), where the source says *Enkäten frågar inte om deltagarnas hälsa* and the draft says *The questionnaire does not ask about participants' mental health.* The source's denial entails the draft's, so a finding against that sentence is false. Four of six checkers filed one anyway, each stating the entailment and filing on a second ground the task offers: that the narrowing changes what an ordinary reader takes away, or that the draft withholds certainty the material warrants ("Preserve supported claims, warranted certainty, …" in the task line; "certainty where it is warranted" in the base contract's Claims section).

Two questions, the first gating the second. Does the false finding reproduce under the shipped task, on the model the Skills now run on? And where it does, does one reworded task line remove it without costing the detection the task has on a broadened denial, on the four real-fault fixtures, or the preservation it has on the three supported-prose fixtures?

## What is run, and what is not

**No Skill is invoked, and no install is staged.** Every run is one checker: a fresh subagent given one fixture file, the resolved language of its draft, and one arm's prompt file, started with the message frozen in [`arms/checker-dispatch.md`](arms/checker-dispatch.md). It receives no findings, hints, expectations, ticket text or earlier reports. It writes one report and nothing else. The fixture and the prompt file it reads are byte copies placed under a random directory name in the builder's scratch, so no path it sees names an arm, a designed class or this evaluation.

**Provider family `claude`**, per [`../protocol.md`](../protocol.md). No Codex Harness is started and no GPT model is run.

**Seat.** Every checker and every judge is a fresh subagent of type `kntnt-opus-high`, which launches **`claude-opus-5-5` at high deliberation**, with no conversation history, started from one Claude Code session (2.1.281). Where #379's plan says `claude-opus-5`, this evaluation runs `claude-opus-5-5`, and no figure from #379 is compared with any figure here.

**Baseline.** The shipped arm is run in this evaluation, in this session and under this seat, from the commit the build started from, **`385976f7`**. Every count a gate reads is compared against that in-session arm and never against #379's figures.

**No record is owed under [`../records/`](../records/README.md)**, and none is added there or to its README. That format is per Skill invocation: [`../protocol.md`](../protocol.md) requires an `invocation` field holding the Formal Invocation as typed and a `fixture` field naming a fixture from the corpus index, and this evaluation has neither.

**Nothing already under `docs/evaluation/` is edited.** Every fixture is read in place, from `../editorial-379/fixtures/` and `../editorial-362/checker/fixtures/`, and every file this evaluation writes is inside `docs/evaluation/editorial-387/`.

## The two arms

| Arm | Task line | Where it is frozen |
| --- | --- | --- |
| `shipped` | The single blockquoted line beginning "Compare the complete draft" in `skills/editorial/write/references/source-check.md` at `385976f7`, without the leading `> `. | [`arms/shipped-task.md`](arms/shipped-task.md) |
| `reworded` | The shipped arm's prompt file with that one line changed and nothing else different. Written only where the first round reproduces the false finding, and committed before the comparison round's first run. | `arms/reworded-task.md` |

`arms/shipped-task.md` is a byte copy of [`../editorial-379/arms/shipped-task.md`](../editorial-379/arms/shipped-task.md). At `385976f7` its `## Task` line is byte-identical to the blockquoted task line of `source-check.md` (the readiness addendum's `cmp` prints nothing), and its `## Claims` section is, apart from blank lines at its edges, the `## Claims` section of `skills/kntnt/library/references/editorial/base.md`. The only text of `source-check.md` a checker receives is that one task line.

## The fixtures

Nine, read in place. The focus passage is quoted exactly as the draft carries it. For the seven fixtures of `../editorial-362/checker/`, it is the passage each judgement in `../editorial-362/checker/judging/round-2/<id>/judgement.md` names: the line it heads "Focus passage:" where it has one (`p3`, `p4`, `n1`, `n3`), and otherwise the draft sentence its reading of the focus passage quotes (`p1`, `p2`, `n2`) — not the paraphrase in that plan's fixture table.

| Id | Fixture | Language | Focus passage | Designed class, or established judgement |
| --- | --- | --- | --- | --- |
| `bd1` | [`../editorial-379/fixtures/bd1-broadened-denial.md`](../editorial-379/fixtures/bd1-broadened-denial.md) | `en_US` | The evaluation does not measure participants' knowledge. | Broadened denial. A finding against the focus passage is **correct**. |
| `nd1` | [`../editorial-379/fixtures/nd1-narrowed-denial.md`](../editorial-379/fixtures/nd1-narrowed-denial.md) | `en_US` | The questionnaire does not ask about participants' mental health. | Narrowed denial. A finding against the focus passage is **false**. |
| `p1` | [`../editorial-362/checker/fixtures/p1-opinion-variable.md`](../editorial-362/checker/fixtures/p1-opinion-variable.md) | `en_US` | The report does not measure age, functional ability, or digital proficiency. | Real fault: "digital proficiency" names a different variable from the source's *digital vana*. |
| `p2` | [`../editorial-362/checker/fixtures/p2-chronology.md`](../editorial-362/checker/fixtures/p2-chronology.md) | `en_US` | In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair. | Real fault: "In September 2025" governs the supplier choice too, which the source leaves undated. |
| `p3` | [`../editorial-362/checker/fixtures/p3-document-scope.md`](../editorial-362/checker/fixtures/p3-document-scope.md) | `en_GB` | it does not establish whether that consent exists. | Real fault: the draft says the submission does not establish whether consent exists; only the supplied package is silent on it. |
| `p4` | [`../editorial-362/checker/fixtures/p4-person-attribute.md`](../editorial-362/checker/fixtures/p4-person-attribute.md) | `en_US` | Ortiz explained the distinction in her email | Real fault: "her" asserts a natural gender for Ortiz that the material does not supply. |
| `n1` | [`../editorial-362/checker/fixtures/n1-column-reflection.md`](../editorial-362/checker/fixtures/n1-column-reflection.md) | `sv` | Ändå får den mig att undra vad vi ber om när vi ber om varandras tid. | Supported prose: the author's present reflection. |
| `n2` | [`../editorial-362/checker/fixtures/n2-opinion-sufficiency.md`](../editorial-362/checker/fixtures/n2-opinion-sufficiency.md) | `sv` | Min invändning gäller att kommunen föreslås ta bort telefonen innan den har underlag för den avvägningen. | Supported prose: the authorial sufficiency assessment, grounded in the documented absence of measurement. |
| `n3` | [`../editorial-362/checker/fixtures/n3-column-withheld.md`](../editorial-362/checker/fixtures/n3-column-withheld.md) | `sv` | Jag sitter med en mall, inte med bevis för kollegernas tillkortakommanden. | Supported prose: describes the essay's documentary basis. |

The language is each draft's `kntnt.language`; `n1`–`n3` carry no frontmatter and are Swedish (`sv`).

## Rounds and run counts, exact

Not floors. No row is rerun selectively, and no report that reached disk is excluded.

1. **First round: does the false finding reproduce?** The `shipped` arm alone, exactly **six** runs on `bd1` and exactly **six** on `nd1`. Each fixture's six reports go, shuffled, to two independent judges. The round answers one question: how many of the six `nd1` reports filed a finding against `nd1`'s focus passage, counted by the first question and the tie-break below?
   - At **0 of 6** the defect is **not reproduced**. No reworded arm is written, no comparison round is run, nothing under `skills/` changes, and the result is recorded as not reproduced in `results.md` and in a decision record, `docs/adr/0220-*.md`, as ADR-0212 did for #363 and ADR-0214 for #364.
   - At **1 or more**, the comparison round follows.
2. **Comparison round.** `arms/reworded-task.md` is written only now and committed before the round's first run. Then:
   - the `reworded` arm, exactly **six** runs on `bd1` and exactly **six** on `nd1`;
   - **both** arms, exactly **three** runs each on each of `p1`, `p2`, `p3`, `p4`, `n1`, `n2`, `n3`.

   The shipped arm's `bd1` and `nd1` runs are the six from the first round and are not run again.

Reports are written to `runs/<arm>/<fixture id>-r<n>.md`. The reworded arm's runs are numbered from `r1` in their own directory.

**Scheduling.** Two runs on the same fixture never run at the same time (#401). Runs on different fixtures may overlap, at most eight subagents at once. On each of the seven fixtures the six comparison-round runs alternate arms, `shipped` first, so neither arm gets the earlier or the later slots.

## A run that is void, and a run whose report never reached disk

A run or judge cut off by a usage limit, an HTTP 5xx or an overload is **void**, not evidence. It is recorded in `results.md` with its arm, its fixture and the error, enters no count, and is rerun in the same arm and fixture under the same conditions.

A report file that reached disk is judged as it stands, however short, hedged, incomplete or malformed, and is never dropped, reworded, rerun or excluded from a count. Where a checker could not write the file and gave the complete report in its reply, as the arm's task allows, that reply is saved as the report, unchanged, and says so in `results.md`. A run that produced neither, for any other reason, is recorded with its harness error, enters no count, and gets **one replacement run** under the same conditions, recorded as one. Where one arm and fixture needs more than three replacements, the builder stops and reports the obstacle on #387.

## Judging

The "Judging" section of [`../editorial-379/plan.md`](../editorial-379/plan.md) carries over whole, including "The two questions" and "The established seven". What follows restates it with this evaluation's paths, and adds only how criterion D's reason is read.

**A judge is given** a copy of the fixture file, every report it is to judge under shuffled neutral names, a copy of the judge brief at [`judging/judge-brief.md`](judging/judge-brief.md) (a byte copy of `../editorial-362/checker/judging/judge-brief.md`), and the fixture's focus passage, with the message frozen in [`judging/judge-dispatch.md`](judging/judge-dispatch.md). It is given nothing else: neither arm's task line, nor the designed class or established judgement, nor the ticket, nor which arm a report came from, nor how many runs were made or how the reports divide between arms. Each judge works in its own scratch directory under a random name. The key mapping neutral names to runs is written to `judging/<round>/key.json` only after both judges of every set have finished, and is never in a judge's reach.

- **First round.** Two sets, `bd1` and `nd1`, six shipped reports each, each set to two fresh independent judges. Its counts answer the reproduction question and nothing else.
- **Comparison round.** Nine sets, one per fixture. Every report of both arms for one fixture goes to the same two fresh judges, shuffled into one set: twelve reports for `bd1` and for `nd1` (the six first-round shipped reports and the six reworded ones), six for each of the seven. **Every gate is read from this round**, and no first-round count is ever compared with a comparison-round count.

### The two questions

Each judge answers both, per report.

1. **Did this report file a finding against the focus passage named for this fixture?** A question of fact about the report's own text.
2. **On the judge's own reading of the fixture, is a finding against that passage correct?**

**The second question produces no count.** Both judges' answers are recorded, and where either contradicts the designed class or established judgement, `results.md` says so in a sentence. The designed class and the established judgement decide every count.

**What counts as a finding.** What the judge brief counts: an item the report itself presents as a finding, whatever it calls it and at whatever severity, and not an item it clears, or records as a note, an observation or a watch-item without asking for a repair.

**What counts as against the passage.** For `bd1` and `nd1`, #379's rule: the draft passage the finding quotes is that sentence or a span inside it. For the seven, the draft passage the finding quotes is the focus passage, a span inside it, or a longer quotation of the draft sentence that contains it, since two of the seven focus passages are clauses. A finding on a neighbouring sentence is not against the passage.

**The tie-break.** Where the two judges disagree on the first question, the report counts as the reading that **fails that fixture's criterion**: for `bd1` and for D, as no finding; for `nd1` and for P, as a finding filed.

### The established seven

They are read through **criterion D** and **criterion P** as [`../editorial-362/checker/plan.md`](../editorial-362/checker/plan.md) defines both under "Criteria, fixed before the runs", and nothing wider.

- **D**, `p1`–`p4`: the report raises the established fault as a finding, on the right passage **and for the right reason**. Noticing the difference and then accepting it is a fail. A different finding on the same sentence does not count. A finding that states the established fault counts whether the report files it as source support or as translation.
- **P**, `n1`–`n3`: the report does not raise a finding against the focus passage.

**How the reason is read.** A judge is not told the established fault. Each judge's `## Focus-passage answers` table gives, for every finding it counts under the first question, the finding's allegation in one sentence, and the judge brief's per-report table gives the same finding with its quoted passage. The builder reads a judge's record as a D pass where that judge answers yes to the first question and at least one allegation it records states the fault in the right-hand column of the fixture table above:

| Id | The right reason |
| --- | --- |
| `p1` | "digital proficiency" does not name what *digital vana* names (skill or proficiency against habit, familiarity or experience), so the draft denies measuring a different variable. |
| `p2` | the fronted "In September 2025" dates the choice of Svale Systems, or the test before it, which the material leaves undated. |
| `p3` | the draft asserts of the submission that it does not establish whether the consent exists, where the material says only that the supplied material does not state its status: a change of subject or scope. |
| `p4` | "her" asserts a natural gender, or a gendered pronoun, for Ortiz that the material does not supply. |

Where the two judges' records give different D outcomes for one report, on the first question or on the reason, the report counts as a D fail, by the tie-break. `results.md` quotes, for every D report, the allegation each judge recorded, so the reading can be checked.

Because the tie-break moves numbers, it is reported: per arm and per fixture, the counted figure, the number of reports it rests on a split for, and the figure the opposite resolution would have given.

## The gates, frozen

### After the first round

Reproduced where the shipped arm's `nd1` count is **1 or more** of 6; not reproduced at **0 of 6**, with the consequences under "Rounds and run counts". Nothing else is read from the first round.

### After the comparison round

Four counts per arm, each read from the comparison round:

- **`nd1`**: `nd1` reports counted as filing a finding against its focus passage, of six. The **target**.
- **`bd1`**: `bd1` reports counted as filing a finding against its focus passage, of six.
- **D**: reports on `p1`–`p4` that pass criterion D, of twelve.
- **P**: reports on `n1`–`n3` that pass criterion P, of nine.

The reworded task line **ships** only where all of these hold:

1. `nd1` is **lower** in the reworded arm than in the shipped arm;
2. `bd1` is **not lower** in the reworded arm than in the shipped arm;
3. D is **not lower** in the reworded arm than in the shipped arm;
4. P is **not lower** in the reworded arm than in the shipped arm.

A control (`bd1`, D, P) fails where its reworded count is lower than its shipped count. Where the comparison round counts the shipped arm at 0 of 6 on `nd1`, no reworded line can meet condition 1, and nothing ships. No criterion is softened to fit a result.

**Exactly one reworded arm is written and measured.** There is no revise round and no second wording.

## The rewording

It starts from the four `nd1` reports #379 recorded as filing on its focus passage (`../editorial-379/runs/shipped/nd1-r2.md`, `nd1-r3.md`, `nd1-r4.md`, `nd1-r6.md`) and from whatever the first round's reports here add, and is written under `/writing-for-agents`. It changes the one task line and nothing else in the prompt file. The line it produces must pass this test:

- it confines itself to scope a statement entails: a draft statement that the source's statement entails, because it claims less of the same thing, is no finding on that account alone;
- it never licenses hedging, a weaker modality or less certainty than the material warrants;
- it names quoted speech as outside it, so that it does not touch the **Meaning** paragraph under "What may not" in `skills/editorial/write/references/quotations.md` ("Not narrowed, not widened, not sharpened."), under which narrowing a quotation's meaning is still a defect;
- it contradicts nothing in the Claims section of `skills/kntnt/library/references/editorial/base.md`.

## Where a result goes

- **A reworded line ships.** The reworded arm's task line is copied verbatim into `skills/editorial/write/references/source-check.md` as its blockquoted task line, and nothing else in that file changes. The Claims section of `base.md` is not changed. The catalog is regenerated. Where the reworded arm's `nd1` count is still above 0, that remaining miss is filed as its own `needs-triage` ticket naming #387.
- **The reworded arm is measured and does not ship.** `source-check.md` is left exactly as it stands, and the remaining miss is filed as its own `needs-triage` ticket naming #387 and carrying both arms' figures.
- **Not reproduced.** As under "Rounds and run counts".

## What `results.md` reports

For every round that ran:

- Per arm, per fixture and per run: both judges' answer to the first question and the outcome counted for it; for `p1`–`p4`, the allegation each judge recorded and the D outcome read from it.
- Per arm and per fixture: the counted figure, the number of splits it rests on, and the figure the opposite resolution would have given.
- Both judges' answers to the second question, and a sentence wherever either contradicts the designed class or established judgement.
- Per arm: the word count of the task line, and the median wall time per run — from the dispatch of the subagent to its report's modification time — over `bd1` and `nd1` and, separately, over the seven where those runs were made.
- The commit the shipped arm's task line was copied from.
- Every run that was void or wrote no report, with its arm, its fixture and the error.
- Why no record is owed under `../records/`.
