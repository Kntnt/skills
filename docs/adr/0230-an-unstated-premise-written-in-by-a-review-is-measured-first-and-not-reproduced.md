# A review writing an unstated premise into a clean opinion — measured first, and not reproduced

This record decides **not** to add to Redline's review guidance a rule that a repair writes in no premise, assumption or inference the argument leaves implicit. The ticket made that change conditional on a measurement. The measurement ran the product as it stood and found no run that wrote such a premise, so the rule does not ship. Issue #468, the premise half. The ticket's other half, that a loss is counted as the reader would suffer it in every passage, reproduced and ships; this record does not concern it.

## The behaviour, and why it was filed

**#429's evaluation saw it once in its shipped wording.** One file-target run of `opinion-clean` added a whole paragraph at the start of the last section, naming the assumption that abolishing telephone booking in September would rest on. Both judges failed `R1` on it. The run's own reply conceded that the text never made the claim. Other runs of the same fixture, in every arm, added words to the lead that named both booking routes or said that the switch removes telephone booking. #434 had been filed against the same shape, closed on 2 runs of 10, and its closing comment set a higher rate as the condition for filing it again. #468 was filed for that reason.

**The triage comment on #468 stated what should hold.** A review reports an assumption the argument leaves unstated where a reader cannot follow the argument without it. Where a reader can follow the argument, the assumption is no finding. The review never writes the assumption into the text. This is Thomas's #397 ruling, that a review reports a part the text does not have and repairs a part it has, applied to an argument's premises. `base.review.md` already says the same of a repair that *requires information absent from the text*, and `opinion.review.md` says *Clarify a broken argument without replacing its position*.

**The candidate** added one sentence beside *Introduce no new evidence, experience, attribution or outcome* in `base.review.md`, and seven words to the correction brief's sentence that lists what its agent leaves alone. The readiness addendum made it conditional: *a half recorded as not reproduced leaves its text unchanged*.

## Why nothing is shipped

[`docs/evaluation/editorial-468/plan.md`](../evaluation/editorial-468/plan.md) was frozen at `8532ee21`, before the first run. The plan set the test in advance, as the addendum required. An addition to `opinion-clean` counts where it asserts something no sentence of the input states: a premise, an assumption or an inference. An addition that only names what a sentence of the input already states is a clarification. A clarification is recorded and not counted. The pre-change arm staged the product at `41fd4c55`, the tree #429 left. It ran `opinion-clean` as three response-target and file-target pairs. Every run was a fresh top-level Claude Code session on `claude-opus-5-5` at high deliberation, and every run had two blind judges.

**No pre-change run wrote a premise.** Four of the six runs delivered the text unchanged. Each of the other two added one phrase to the lead, and each phrase names what the input already states:

- *ett byte som tar bort telefonbokningen och kan ske i september*. The standfirst states the same fact: *I september kan telefonbokningen av Lerviks föreningslokaler försvinna*.
- *båda bokningsvägarna, digital bokning och telefonbokning*. The lead's own first sentence names the digital route, and the headline and the standfirst name the telephone route. The addendum names this addition as the example of a clarification.

The judges split on both runs, one failing `R1` as taste and one passing. That is a finding about the lead, and a clarification, and it is recorded in the results.

**So there is no miss for the rule to be measured against.** The rule would add a sentence to a file that Redline and every correction agent read on every run. The only evidence that could justify it is a miss the product makes, and on this fixture the product makes none. The candidate arm wrote no premise either, and changed `opinion-clean`'s lead in none of its six runs. That arm had the rule in it, so its result says nothing about the rule. `base.review.md`'s smallest-correction paragraph and the correction brief are byte-identical to `41fd4c55`. This is the method [ADR-0212](0212-a-quotation-is-read-in-the-language-it-is-written-in.md), [ADR-0223](0223-a-part-that-asserts-past-a-kept-limit-is-measured-first-and-not-written-into-the-limit-rule.md) and [ADR-0225](0225-a-correction-rounds-repeating-heading-is-measured-first-and-not-reproduced.md) follow.

## What this record does not decide

**The requirement still stands.** A review that writes into a text a premise the argument leaves unstated breaks the rule already in `base.review.md`: a repair that *requires information absent from the text* is left, and the finding is reported unresolved. It also breaks `opinion.review.md`'s *Clarify a broken argument without replacing its position*. This record declines only a second, narrower statement of that rule, for which there is no miss to pay.

**Clarifications are not premises.** An addition that names what a sentence of the text already states adds no claim. The measurement still found those additions in the pre-change arm. Whether a clean text should gain them at all is the reader-loss rule's question, which #468's other half ships. This record does not decide it.

**It is measurable without re-deriving it.** The frozen plan states the test for a counted addition, and says who calls it and how. What reopens this record is a run of the current product whose delivered text asserts something no sentence of its input states. It could be the paragraph #429 recorded, or a warrant a review writes into a PAC text. #470's readiness addendum says such a warrant is reported and not written in. The plan is then a method to copy, candidate and all.

**Nothing here reaches the GPT family.** The protocol forbids a Claude session from starting a Codex Harness, so Redline was not measured there.
