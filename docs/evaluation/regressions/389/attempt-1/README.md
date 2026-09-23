# Attempt 1 — the rule as first written, and what it did not do

Kept because it is the run that found the gap. Nothing here is relabelled: this
attempt reached the boundary once, and there the run **did not reject** the
round.

## What was staged

The detached object `8dd5f31b`, whose `skills/` tree is `85d2690e`. It carried
the whole of the rule as first written — candidate status until re-review,
establishment against the retained states, whole-round rejection, verbatim
restoration, the budget account, the delivery account, both correction briefs
and both help pages. The staged `SKILL.md` is verifiable: `git archive
8dd5f31b skills/editorial/redline/SKILL.md` contains *reject the whole round
that introduced it*.

## The three cases

| Case | Reached the boundary? | What happened |
|---|---|---|
| [`article-flawed`](runs/article-flawed/) | **Yes** | The input has no subheading anywhere, so the round wrote three. Two of them drew findings from the run's own re-review: one that covers only half its section, and one saying the same as the last sentence under it. The run **accepted the round**, delivered both subheadings, and carried both findings forward as unresolved — the delivered reply's findings 3 and 4. 665 s, 2 agents, 29 calls, trace complete. |
| [`case-study-sv`](runs/case-study-sv/) | No | This time the round's new headline attributed the judgement to the supervisor — *Arbetsledaren skulle göra om loggtestet – men förbereda mer* — rather than claiming the effect in the publication's voice as the #386 round did. No finding remained and nothing was there to reject. 1031 s. |
| [`case-study-flawed`](runs/case-study-flawed/) | No, and correctly so | The acceptance control. The round repaired five findings, moved one subheading from an asserted fact to an attributed judgement, and introduced nothing; the candidate was accepted and the loop went on. Its finding 4 says in as many words that the defect *fanns redan i den inkomna texten*, so an old defect first noticed after a round was not attributed to the round. 864 s. |

## What the failure showed

The run's own narration reads *Round accepted (with one restoration)* — #383's
untraced-difference restoration ran, and then the re-review's two findings
against the round's own new subheadings were treated as ordinary unresolved
findings of the delivered text. The rule was in front of it and did not fire.
Three things were missing from the way it was written:

1. **The case was not named.** Every instance the #386 evaluation and the
   staged runs of `main` recorded was created in a part the round rewrote — a
   headline, a standfirst, a subheading. The rule described the test without
   naming where it applies.
2. **A commissioned part read as immune.** A finding had asked for the missing
   sections, so the subheadings traced to a finding and the round was accepted;
   nothing said that what the new part *says* is checked separately, or that
   the text having been worse without the part is no reason to keep a defective
   one.
3. **The spent budget answered for it.** The loop stops at the first of four
   conditions and the budget was spent, so the fourth condition could settle a
   round the third should have rejected.

`8619e45e` adds those three sentences and the prohibition they imply — a
finding the run's own round created is never carried forward for a person to
settle — and [`../runs/`](../runs/) holds the attempt made against it.
