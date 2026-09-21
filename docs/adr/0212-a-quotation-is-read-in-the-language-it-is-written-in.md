# A quotation is read in the language it is written in — measured, and not shipped

This record decides **not** to put that rule into the two editorial Skills, after building it, measuring it against a frozen matrix and having it read independently. It exists because the next author will have the same idea, and because what the measurement found is worth more than the wording it rejected. Issue #363, which took over the remainder of #329, #341 and #358.

## What the rule was, and why it looked right

**One sentence of synthetic interview speech was right in English and wrong in Swedish.** *I would set that time aside before the next building starts* sits in a source package about a repair log trialled in two buildings. English carries it: a building starts in the sense of the work on it starting. Swedish, on the reading this ticket was filed on, does not — *innan nästa hus börjar* says that a house begins, and the reader has to supply the activity out of the paragraphs around it.

**The product was recorded failing it in both directions at once.** In the GPT-family evidence under `docs/evaluation/editorial-329/`, Write delivered the Swedish calque and no comparison caught it, a source-blind review read the same calque in a frozen Swedish control and left it standing, and in English a review expanded the working sentence into a spelled-out clause.

**The rule proposed was one test for both.** What does a reader **of the language in front of you** do at this passage: take it on one pass, or stop at a word they have to supply. A figure the language uses itself — an ellipsis, a metonymy, a shorthand — reads on one pass however odd its literal parse, and is not a finding. That the meaning can be worked out is explicitly not the answer. It was stated separately in each Skill's own surfaces, because the writer renders, the checker compares and the review reads one text with nothing beside it.

The argument is still a good argument. It is not what the measurement was about.

## Why it is not shipped

[`docs/evaluation/editorial-363/results.md`](../evaluation/editorial-363/results.md) holds the measurement, against the matrix frozen in [`plan.md`](../evaluation/editorial-363/plan.md) before the first run: three arms over the same frozen inputs, one baseline and two candidate wordings, every run a fresh seat, every judgement two blind judges.

**Neither failure reproduced in the Claude family.** Every Redline run of every arm returned its quoted sentence word for word — the English positive controls, the two Swedish controls, and all three new contrast fixtures. Both blind judges, in every case, answered that a reader of that text's language takes the passage on one pass, and that answer covers the two sentences the frozen material treats as defects. So the baseline arm — the product with no change at all — passed every quotation criterion there was to pass.

**The candidate wording's one measured effect was a defect.** Of the six Swedish drafts across the two arms, the only one whose checker raised a translation finding and whose writer repaired it wrote *arbetet* — the work — into Maya Lind's sentence. Both judges named the cost: the material settles nothing about what starts in the next building, so the repair chose for her. The ticket names that failure mode in its own words. The wording written to protect a quotation was the only thing that changed one.

**An independent reading reached the same place from the other side.** [`reviews/load-chain-review.md`](../evaluation/editorial-363/reviews/load-chain-review.md), written without the numbers, ends *do not ship as it stands*, on three must-fixes. One of them is exactly the defect the runs produced: `quotations.md` said *a figure of the source* where it meant a figure of the source **language**, so the rule reached a figure the speaker coined and told the writer to replace it with plain target-language statement. The other two are worse in kind — that the chain can drive a source-blind review into repairing wording inside quotation marks that `languages/sv.md` says the marks vouch for, while neither reviewer nor repairer is allowed to load that rule; and that dropping *merely* from *not protected merely by its quotation marks* in `case-study.review.md` turns a narrow disclaimer into a general one, in the genre made of customer speech.

**The exit was spent.** One revise-and-remeasure round; the revised wording was it. Fixing three must-fixes would be a second, so the measured result stands as measured and the shorter wording ships.

## What this record does not decide

**Not that the Swedish reading is wrong.** Whether *innan nästa hus börjar* is professional Swedish is a judgement about prose, and a blind judge disagreeing with it settles nothing. What is established is narrower and it is about the instrument: **in this provider family, with these criteria, neither failure can be detected**, so no wording could have been shown to remove one. Three of the ticket's six criteria had nothing to measure.

**Not that the GPT-family failures are cleared.** They stay failed. The protocol forbids a Claude session from driving a Codex harness, so they were not retested.

## What is kept, for whoever tries again

**The three contrast fixtures**, frozen with independent criteria before any product change, under [`docs/evaluation/editorial-363/fixtures/`](../evaluation/editorial-363/fixtures/). One moves the referent and keeps the construction, one moves the language and the rhythm, one is a negative. They exist so that a change cannot pass by learning one sentence, and they are still the right instrument for that.

**`C-ellipsis` as a recorded disagreement.** The negative control was frozen on the premise that a Swedish reader stops at *gick lagret över*. Both judges, in all three arms, read it on one pass. A fixture's criterion is not evidence about a reader, and this is where the two part company. Before the next attempt writes another rule, that is the thing to settle: **find a way to tell whether the defect is present at all**, because an evaluation whose judges cannot see the defect cannot measure a fix for it. [#388](https://github.com/Kntnt/skills/issues/388) is the nearest existing piece of that.

**What was set aside, and stays set aside.** The separate quotation reviewer at `git show 3f21d9b1:skills/editorial/redline/references/quotation-review.md` — 418 words and a full artefact in a fresh seat at every review and re-review — repaired three of four frozen Swedish targets, broke working English, and introduced an unrelated spelling defect. It does not come back. Nor does a shared surface under `skills/kntnt/library/references/editorial/`: a formulation general enough to cover rendering, comparing and reviewing is how the old sentence came to under-fire and over-fire at once. Nor a rule against metonymy, nor a rule for spelling out an implied noun; either would pass the Swedish case and fail the English one.
