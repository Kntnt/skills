# Results for #387: the narrowed-denial finding under the shipped task

Run on 2026-09-24 in the Claude family, Claude Code 2.1.281. Every checker and every judge was a fresh `kntnt-opus-high` subagent — **`claude-opus-5-5` at high deliberation** — with no conversation history. The plan at [`plan.md`](plan.md) was committed before the first checker started and has not been edited since. Nothing else already under `docs/evaluation/` was edited.

**The false finding did not reproduce.** Under the shipped comparison task, **0 of 6** checkers filed a finding against the narrowed denial in `nd1`, both blinded judges agreeing on every report. That is the plan's "not reproduced" exit. No reworded arm was written, the comparison round and the runs on the seven fixtures of `../editorial-362/checker/fixtures/` were not made, and `skills/editorial/write/references/source-check.md` is **unchanged**. No file under `skills/` changed, so no catalog regeneration is owed. [ADR-0220](../../adr/0220-a-narrowed-denial-is-not-filed-against-under-the-shipped-comparison-task.md) records the decision.

On `bd1`, the broadened denial, the same arm filed a finding against the focus passage in **6 of 6** runs, both judges agreeing on every report.

## The arm

One arm was run: `shipped`, frozen at [`arms/shipped-task.md`](arms/shipped-task.md). Its task line is the blockquoted line beginning "Compare the complete draft" in `skills/editorial/write/references/source-check.md` at the commit this build started from, **`385976f7`**. That line, and the base contract's Claims section, are the ones #379 ran: `arms/shipped-task.md` is a byte copy of `../editorial-379/arms/shipped-task.md`, and the readiness addendum's `cmp` against `385976f7` printed nothing.

| Arm | Words in the task line | Median wall time per run, `bd1` and `nd1` | Median wall time per run, the seven |
| --- | --- | --- | --- |
| `shipped` | 580 | 126 s (12 runs) | not run — the defect did not reproduce |

Wall time runs from the moment the run was staged, immediately before its subagent was dispatched, to the last modification time of its report. Runs on one fixture were made one after another, never two at once; runs on `bd1` and on `nd1` overlapped.

## First round, `nd1-narrowed-denial`

Designed class: a finding against the focus passage is **false**. Focus passage: *The questionnaire does not ask about participants' mental health.*

| Run | Blinded name | Judge 1, Q1 | Judge 2, Q1 | Counted | Words | Wall time |
| --- | --- | --- | --- | --- | --- | --- |
| `nd1-r1` | C | no | no | passage cleared | 2 083 | 123 s |
| `nd1-r2` | F | no | no | passage cleared | 2 183 | 119 s |
| `nd1-r3` | A | no | no | passage cleared | 2 052 | 108 s |
| `nd1-r4` | B | no | no | passage cleared | 1 953 | 108 s |
| `nd1-r5` | D | no | no | passage cleared | 2 118 | 129 s |
| `nd1-r6` | E | no | no | passage cleared | 2 255 | 121 s |

**Findings counted against the focus passage: 0 of 6.** The judges split on no report, so the tie-break moved nothing; the opposite resolution of a split would also have given 0 of 6.

On Q2, both judges answered **no** for all six reports: a finding against the passage is not correct on either judge's own reading. That agrees with the designed class, so there is no contradiction to record. Both gave the entailment as the reason, and both added that the draft's own list of the questionnaire's three questions rules out the reading that some other health question was asked.

Every one of the six reports pairs the passage with *Enkäten frågar inte om deltagarnas hälsa*, names the narrowing, tests it, and clears it. None files it on either of the two grounds #379's four reports used — what an ordinary reader takes away, or withheld certainty. Their decisive sentences, as the judges quote them:

- `nd1-r3`: "Test, source holds and draft fails: impossible. Supported, no finding."
- `nd1-r4`: "The draft's statement follows from the source. No finding."
- `nd1-r1`: "Read in context, right after a quotation about mental ill health, it does not imply that other health questions were asked. Supported. No finding."
- `nd1-r5`: "The narrowing matches the claim under discussion." (result: "Supported")
- `nd1-r6`: "The draft is entailed by the source." (result: "Supported")
- `nd1-r2`: "No case compatible with the material makes the draft false. Supported, though weaker than the source."

Every report filed the same two other findings, on "decides on March 3" and on "does not know"; the judges class the first disputed and the second supported. One report (`nd1-r5`) also filed a translation finding on the quoted "mental ill health", which judge 1 classes false and judge 2 disputed.

Judgements: [`judging/gate-round/nd1/judgement-j1.md`](judging/gate-round/nd1/judgement-j1.md), [`judging/gate-round/nd1/judgement-j2.md`](judging/gate-round/nd1/judgement-j2.md).

## First round, `bd1-broadened-denial`

Designed class: a finding against the focus passage is **correct**. Focus passage: *The evaluation does not measure participants' knowledge.*

| Run | Blinded name | Judge 1, Q1 | Judge 2, Q1 | Counted | Words | Wall time |
| --- | --- | --- | --- | --- | --- | --- |
| `bd1-r1` | F | yes | yes | **finding filed** | 2 297 | 135 s |
| `bd1-r2` | E | yes | yes | **finding filed** | 2 772 | 143 s |
| `bd1-r3` | A | yes | yes | **finding filed** | 2 976 | 145 s |
| `bd1-r4` | C | yes | yes | **finding filed** | 2 868 | 161 s |
| `bd1-r5` | B | yes | yes | **finding filed** | 2 171 | 117 s |
| `bd1-r6` | D | yes | yes | **finding filed** | 2 665 | 161 s |

**Findings counted against the focus passage: 6 of 6.** The judges split on no report; the opposite resolution would also have given 6 of 6. The plan reads nothing from this count: the first round answers the reproduction question alone.

On Q2, both judges answered **yes** for all six reports, which agrees with the designed class. Both gave the plan's reason: the material denies measurement only of *förkunskaper*, prior knowledge, and the draft denies it of knowledge as such.

Judgements: [`judging/gate-round/bd1/judgement-j1.md`](judging/gate-round/bd1/judgement-j1.md), [`judging/gate-round/bd1/judgement-j2.md`](judging/gate-round/bd1/judgement-j2.md).

## Runs, reports and judging

Twelve runs were made and **twelve reports reached disk**. No run was void, no run wrote no report, no replacement run was started, and no report was dropped, reworded, rerun or excluded from a count. The reports are at [`runs/shipped/`](runs/shipped/) under their run names. The blinded copies the judges read are at [`judging/gate-round/`](judging/gate-round/) under shuffled neutral names, with the mapping at [`judging/gate-round/key.json`](judging/gate-round/key.json), written there only after all four judges had finished. Each checker and each judge worked in its own scratch directory under a random name, holding byte copies of its inputs, so no path it saw named an arm, a designed class or this evaluation. Each judge was given its fixture, its six reports, the judge brief and its fixture's focus passage, with the message frozen in [`judging/judge-dispatch.md`](judging/judge-dispatch.md), and nothing else.

## What this settles, and what it does not

**Under the shipped task, on `claude-opus-5-5`, the narrowed-denial finding is not a repeatable behaviour of the checker.** Six of six checkers tested the narrowing in both directions, found that the source's denial entails the draft's, and cleared the passage. The same six-run arm kept full detection on the broadened denial, so the task still tests the direction a negation needs. With nothing to remove, no rewording was measured against it, and the plan's exit is to leave `source-check.md` as it stands.

**What it does not settle.** #379's 4 of 6 was measured on `claude-opus-5`, against the same task line and the same fixture. This evaluation ran a different model on purpose (the readiness addendum's item 1) and compares no figure with #379's, so it does not say the earlier result was wrong; it says the behaviour is not there on the model the Skills now run on. The reports are also markedly shorter: a median of about 2 100 words a report on `nd1` against 3 645 for #379's six on the same fixture, and a median of 126 s a run over both fixtures against #379's 226 s. Nor does this evaluation reach the GPT family, which a Claude session may not run.

**The collision #387 names is still in the text.** "Preserve supported claims, warranted certainty, …" in the task line and "certainty where it is warranted" in the Claims section are unchanged, and a checker on another model could read them the way #379's four did. That is a reason to measure again when the model changes, not a demonstrated cause for a wording, and none was written.

## No record is owed under `../records/`

None was added there and its README was not edited. That format is per Skill invocation: [`../protocol.md`](../protocol.md) requires an `invocation` field holding the Formal Invocation as typed and a `fixture` field naming a fixture from the corpus index. **No Skill was invoked here**, and neither fixture run is in the corpus index, so neither field has a value. `../editorial-379/results.md` makes the same point for #379; this file is the report for this evaluation.
