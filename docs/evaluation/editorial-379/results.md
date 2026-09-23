# Results for #379: the shipped comparison task under a negated claim

Run on 2026-09-21 in the Claude family, Claude Code 2.1.278, every checker and every judge a fresh `claude-opus-5` subagent at high deliberation with no conversation history. The plan at [`plan.md`](plan.md) was frozen before the first checker started and has not been edited since; nothing under `../editorial-362/`, `../editorial-329/` or `../corpus/` was touched, and `../README.md` was not edited.

**The gate was met.** The shipped comparison task filed a finding against the broadened denial in **6 of 6** runs, above the frozen bar of five of six. `skills/editorial/write/references/source-check.md` is therefore **unchanged**, no file under `skills/` changed, no catalog regeneration is owed, no reworded arm was written, and the comparison round and the runs on the established seven were not made. Gate 2 was never reached.

**What the same runs also show, and what was done about it.** On the narrowed denial, where the source's denial entails the draft's and a finding is therefore false, the same task filed one in **4 of 6** runs. Both blinded judges, independently, classed a finding there as not correct in every one of the six reports. That is filed as its own `needs-triage` ticket, [#387](https://github.com/Kntnt/skills/issues/387), naming this ticket and carrying these figures. This evaluation does not change `source-check.md` for it: the frozen plan admits exactly one reworded arm and only where the gate is not met, and no criterion is softened to fit a result.

## No record is owed under `../records/`

None was added there and its README was not edited. That format is per Skill invocation: [`../protocol.md`](../protocol.md) requires an `invocation` field holding the Formal Invocation as typed and a `fixture` field naming a fixture from the corpus index. **No Skill was invoked here** and neither fixture is in the corpus index, so neither field has a value. The #362 checker diagnostic wrote no such record for the same reason and reported itself in `../editorial-362/checker/results-round-1.md` and `../editorial-362/checker/results-rounds-2-3.md`; this file is that report for this evaluation.

## The arm

One arm was run: `shipped`, frozen at [`arms/shipped-task.md`](arms/shipped-task.md). Its task line is the single blockquoted line beginning "Compare the complete draft" in `skills/editorial/write/references/source-check.md`, copied verbatim from `main` at commit **`76ddacc1`**, the tree this ticket found. No figure recorded under `../editorial-362/` appears anywhere below.

| Arm | Words in the blockquoted task line | Median wall time per run, two new fixtures | Median wall time per run, established seven |
| --- | --- | --- | --- |
| `shipped` | 580 | 226 s (12 runs) | not run — the gate was met |

Wall time is per run, from the subagent's start to its report write. All twelve checkers were started in one batch at 2026-09-21T15:06:31Z, and each run's time is that instant to its report file's mtime.

## Gate round, `bd1-broadened-denial`

Designed class: a finding against the focus passage is **correct**. Focus passage: *The evaluation does not measure participants' knowledge.*

| Run | Blinded name | Judge 1, Q1 | Judge 2, Q1 | Counted | Wall time |
| --- | --- | --- | --- | --- | --- |
| `bd1-r1` | F | yes | yes | **finding filed** | 217 s |
| `bd1-r2` | D | yes | yes | **finding filed** | 177 s |
| `bd1-r3` | E | yes | yes | **finding filed** | 221 s |
| `bd1-r4` | A | yes | yes | **finding filed** | 220 s |
| `bd1-r5` | C | yes | yes | **finding filed** | 168 s |
| `bd1-r6` | B | yes | yes | **finding filed** | 209 s |

**Detection: 6 of 6.** The judges split on **no** run, so the tie-break moved nothing and the opposite resolution of a split would also have given 6 of 6.

On Q2, both judges answered **yes** for all six reports — a finding against that passage is correct on each judge's own reading. That agrees with the frozen designed class, so there is nothing to record as a contradiction. Both gave the same reason the plan gives: the material denies measurement only of *förkunskaper*, the draft denies it of knowledge as such, and an end-of-course record inside the course leaders' written summaries is compatible with everything supplied and excluded by nothing in it.

Judgements: [`judging/gate-round/bd1/judgement-j1.md`](judging/gate-round/bd1/judgement-j1.md), [`judging/gate-round/bd1/judgement-j2.md`](judging/gate-round/bd1/judgement-j2.md).

## Gate round, `nd1-narrowed-denial`

Designed class: a finding against the focus passage is **false**. Focus passage: *The questionnaire does not ask about participants' mental health.*

| Run | Blinded name | Judge 1, Q1 | Judge 2, Q1 | Counted | Wall time |
| --- | --- | --- | --- | --- | --- |
| `nd1-r1` | A | no | no | passage cleared | 331 s |
| `nd1-r2` | F | yes | yes | **finding filed** | 279 s |
| `nd1-r3` | B | yes | yes | **finding filed** | 231 s |
| `nd1-r4` | D | yes | yes | **finding filed** | 234 s |
| `nd1-r5` | C | no | no | passage cleared | 284 s |
| `nd1-r6` | E | yes | yes | **finding filed** | 247 s |

**Findings counted against the focus passage: 4 of 6.** The judges split on **no** run, so the tie-break moved nothing and the opposite resolution of a split would also have given 4 of 6.

On Q2, both judges answered **no** for all six reports — a finding against that passage is not correct on either judge's own reading. That agrees with the frozen designed class, so there is nothing to record as a contradiction. Both gave the entailment as the reason, and both added that the draft's own later list of the questionnaire's three questions forecloses the contrary reading.

The four reports that filed a finding do not miss the entailment; each states it and files anyway, on one of two grounds the task offers. Two argue the narrowing changes what an ordinary reader takes away, so the sentence is "false to the material even though the words, taken in isolation, are entailed by it". Two argue the draft withholds warranted certainty: "The material warrants the flat denial; the draft withholds it at the one point where it does the most work." #387 carries that reading and what it collides with.

Judgements: [`judging/gate-round/nd1/judgement-j1.md`](judging/gate-round/nd1/judgement-j1.md), [`judging/gate-round/nd1/judgement-j2.md`](judging/gate-round/nd1/judgement-j2.md).

## Runs, reports and judging

Twelve runs were made and **twelve reports reached disk**. No run wrote no report, so the lost-report rule was never invoked, no replacement run was started, and no run was dropped, reworded, rerun or excluded from a count. The reports are at [`runs/shipped/`](runs/shipped/) under their run names, and the blinded copies the judges read are at [`judging/gate-round/`](judging/gate-round/) under shuffled neutral names, with the mapping at [`judging/gate-round/key.json`](judging/gate-round/key.json). No judge was given the key, the arm, the designed class, the ticket, the run counts, or either arm's task line; each was given its fixture, its six reports under neutral names, the judge brief at `../editorial-362/checker/judging/judge-brief.md` and its fixture's focus passage.

## What this settles, and what it does not

**The one-directional test is not a repeatable behaviour of the checker under the shipped task, in this family.** That was the first of the ticket's two questions and it gates the second. Six of six checkers tested the direction a negation needs — that something could fall under the broader term without falling under the narrower one — and every one of them named the separating case rather than clearing the passage on the subset direction alone. The second question, whether the one-directional test lets a real defect through, therefore does not arise from this evidence: nothing was let through.

**What it does not settle.** The evaluator's observation that opened this ticket, on the *funktionsförmåga*/"ability" passage in `../editorial-362/runs/opinion-en_US-r2/`, is neither confirmed nor refuted here. That passage is disputed, the ticket ruled it out as a fixture for exactly that reason, and this evaluation measured a different passage. What can be said is that the behaviour it was read as evidence of did not reproduce on a fixture built to elicit it, twelve runs, two judges, no split. Nothing here bears on the GPT family, which this session may not run: a Codex-side retest stays Thomas's own step on #362.
