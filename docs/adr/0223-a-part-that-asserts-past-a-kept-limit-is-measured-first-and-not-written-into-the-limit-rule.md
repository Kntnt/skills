# Redline's limit rule does not name a part that asserts past a kept limit — measured first, and not reproduced

This record decides **not** to extend Redline's rule on limiting sentences to a headline, subheading or standfirst that asserts past a limit the text keeps. The form was measured first, against the product as it stands, and did not reproduce, so no wording was written and nothing ships. Issue #415, filed from the residual #398 recorded out of #383's evaluation.

## The form, and why it is a defect

**Four judges of #383's evaluation named the same shape without conferring.** A run wrote a headline, a subheading or a standfirst above a limiting sentence it left word for word, and the part asserted what that sentence bounds: sharper, more general, or a conclusion the sentence withholds. The limit then reaches the reader as a qualification of something already stated flatly. One judge called it *superscription*. [`docs/evaluation/editorial-415/results.md`](../evaluation/editorial-415/results.md) states the four instances in one place. All four are in the two Swedish column drafts, and in all four the part was one the run wrote into a text that had none.

**The form is a defect, and the collection already forbids it.** #415's readiness addendum ruled on this, in Thomas's absence and open to his review. [`headlines.md`](../../skills/kntnt/library/references/editorial/headlines.md), *Every word supported*, says a headline, and by that file's own scope a subheading, claims only what its text claims, *never sharper, never more general, never a conclusion the text does not draw*. [`base.md`](../../skills/kntnt/library/references/editorial/base.md), *Claims*, requires proportionate strength and says the boundary holds *in the title, summary, headings and body alike*. A part that asserts past a kept limit breaks both. A part that asserts no more than the kept sentence allows, with the limit below it, is ordinary structure.

The ruling rejected two alternatives. One was to rule the form ordinary structure, which the two rules above contradict. The other was to write a rule of its own in the article anatomy or in Write, which would answer the form twice, and no Write run shows it.

**What does not see it is Redline's limit rule**, in `base.review.md`, step 7 of `redline/SKILL.md`, the correction brief and `help.md`. That rule tests edits to the limiting sentence itself: the sentence removed, weakened or recast. A sentence that survives byte for byte meets it, whatever is written above. The candidate fix the addendum set out was to name the form in that rule in one clause and point at the two rules above, in those four places and nowhere else, shipped only if a measurement supported it.

## Why nothing is shipped

[`docs/evaluation/editorial-415/plan.md`](../evaluation/editorial-415/plan.md) was frozen at `22ef6183`, before the first run and before any wording. It ran the pre-change arm first. The arm staged the product at `708bff52`, which holds #397's, #398's, #400's and #402's changes, and ran the four #362 drafts twice each and the ten *Redline controls* once each. Every run was a fresh top-level Claude Code session on `claude-opus-5-5` at high deliberation. Each run had two blind judges on a new brief that asks the one question above.

**No run counts.** A run counts when both of its judges answer yes, and all thirty-six judgements answer no. Eleven runs changed a headline, a subheading or a standfirst the text already had, and no judge found any of those parts asserting past a limit the text keeps.

**The route by which the form reached #383's drafts is closed.** Every instance was a part written into a finished text that lacked it, which is the behaviour #397 was filed for. Since #397's change, a review reports a missing standfirst or subheading instead of writing it. None of the eighteen runs wrote one. `column-sv-r2`'s run reported the missing standfirst and sections and left them unwritten.

**So there is no miss for a change to be measured against.** A clause in the limit rule adds reading to four surfaces Redline loads on every run. The only evidence that could justify it is a miss the shipped product makes, and on these inputs it makes none. As the plan settles, no candidate was written, the post-change arm was not run, and the four places are byte-identical to `708bff52`. This is the same method as [ADR-0212](0212-a-quotation-is-read-in-the-language-it-is-written-in.md), [ADR-0214](0214-a-bridge-prepares-a-quotation-rather-than-pre-says-it.md) and [ADR-0221](0221-unslop-keeps-its-whole-passage-permission-measured-and-left-alone.md).

## What this record does not decide

**The form is still a defect.** This record leaves the ruling standing: a headline, subheading or standfirst that asserts past a kept limit breaks `headlines.md` *Every word supported* and `base.md` *Claims*, and those two rules are where the collection answers it. The limit rule does not repeat them. A later author who wants the limit rule to name the form would be adding the reading this record declined, without the miss that would pay for it.

**It is measurable without re-deriving it.** [`paratext-judge-brief.md`](../evaluation/editorial-415/paratext-judge-brief.md) and the counting rule in the plan state the form as a criterion. What reopens this record is a run of the current product in which both judges answer yes under that brief. Such a run could come from a text that invites a rewritten headline over a hedge, or from a regression of #397's change. `docs/evaluation/editorial-415/plan.md` is then a frozen method to copy, candidate and all.

**Unslop and Write are untouched.** Unslop writes no headline, subheading or standfirst, and no instance was written by Write.

**Nothing here reaches the GPT family.** The protocol forbids a Claude session from starting a Codex Harness, so Redline was not measured there.
