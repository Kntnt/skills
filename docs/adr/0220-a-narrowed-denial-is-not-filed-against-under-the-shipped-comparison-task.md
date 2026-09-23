# A narrowed denial is not filed against under the shipped comparison task — measured, and the wording left alone

This record decides **not** to change the comparison task in Write's `source-check.md` for a draft that claims less than its material, after freezing a plan against it and measuring the shipped wording on the model the Skills now run on. The defect did not reproduce, so no rewording was written. Issue #387, filed from #379.

## What the change would have been, and why it looked right

**#379 measured a false finding at 4 of 6.** On a fixture built for it, the source says *Enkäten frågar inte om deltagarnas hälsa* and the draft says *The questionnaire does not ask about participants' mental health.* The source's denial entails the draft's, so a finding against that sentence is false, and both of #379's blinded judges classed it so in every report. Four of six `claude-opus-5` checkers filed one anyway.

**They filed it on grounds the task itself offers.** None missed the entailment. Two argued that the narrowing changes what an ordinary reader takes away. Two argued that the draft withholds certainty the material warrants, which has a footing in the task line's "Preserve supported claims, warranted certainty, …" and in the base contract's "Keep uncertainty where it exists and certainty where it is warranted". Neither text says that a draft claiming *less* than its material is a defect, and the task's own rule — if you can name no case, it is not a finding — points the other way. So #387 read it as a collision inside the task, to be settled in one place a checker reads, and triage settled that it was worth trying: a false finding reaches the writer, and nothing in the evidence says the writer's validation rejects one.

**The candidate was to be one changed task line**, confined to scope a statement entails, licensing no hedging and leaving quoted speech under `quotations.md`'s rule that a quotation's meaning is not narrowed. It was to ship only where it lowered the narrowed-denial count without lowering detection on a broadened denial, on four real-fault fixtures or on three supported-prose fixtures, each read against the shipped arm in the same session.

## Why nothing is shipped

[`docs/evaluation/editorial-387/results.md`](../evaluation/editorial-387/results.md) holds the measurement, against the plan frozen in [`plan.md`](../evaluation/editorial-387/plan.md) before the first run: the shipped task line at `385976f7`, six checkers on each of #379's two fixtures, every checker and judge a fresh subagent on `claude-opus-5-5` at high deliberation, two blinded judges per fixture.

**The false finding does not reproduce.** The plan's test was fixed before the runs: reproduced at one or more of six. **0 of 6** checkers filed a finding against the narrowed denial, both judges agreeing on every report. Every report paired the sentence with its source, named the narrowing, tested both directions and cleared it — "Test, source holds and draft fails: impossible. Supported, no finding." — and none reached for either of #379's two grounds. The same arm filed against the **broadened** denial in **6 of 6** runs, so the task's detection in the direction a negation needs is intact.

**There is no cause to write a wording for.** The plan admits exactly one reworded arm, and only after a reproduced miss, because the only evidence that could justify added reading in a task line is a miss the shipped line demonstrably makes. With none, the shipped line stays, and the comparison round against the seven fixtures of `docs/evaluation/editorial-362/checker/fixtures/` was not run: those seven measure only what a rewording would cost.

**The model changed between the two measurements, and this record rests on that on purpose.** The readiness addendum chose to run `claude-opus-5-5`, which the Skills now run on, over reproducing #379 byte for byte on `claude-opus-5`, and to compare no figure across the two. So this record does not say #379 was wrong. It says the behaviour it measured is absent on the current model under the current wording. The reports are also much leaner — about 2 100 words a report on the narrowed-denial fixture against #379's 3 645 — which is consistent with a checker that no longer argues itself into a second ground, though nothing here measured why.

This is the third such result by the same method: [ADR-0212](0212-a-quotation-is-read-in-the-language-it-is-written-in.md) for #363 and [ADR-0214](0214-a-bridge-prepares-a-quotation-rather-than-pre-says-it.md) for #364 also measured a filed defect, found it absent, and left the shipped wording alone.

## What this record does not decide

**The collision is still in the text.** "Warranted certainty" in the task line and "certainty where it is warranted" in the Claims section are unchanged and still do not say whether a draft that claims less than its material is a defect. A checker on another model, or on a later one, could read them as #379's four did. When the checker's model changes, the narrowed-denial fixture at `docs/evaluation/editorial-379/fixtures/nd1-narrowed-denial.md` is the cheap test to run again, and `docs/evaluation/editorial-387/plan.md` is a frozen method to copy.

**Nothing here reaches the GPT family.** The protocol forbids a Claude session from starting a Codex Harness, so the task line was not measured there.
