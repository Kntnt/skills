# Frozen plan — #389, seventh and last wave

Written before any run of this wave had returned, and not edited afterwards. The
earlier plans are left exactly as they were written. No wave follows this one,
whatever it finds.

## Where the sixth wave left it

The sixth wave closed the headline case. `case-study-sv-short-headline-2`
rejected its round because the **headline** the round wrote — *Samlade
felanmälningar hjälper underhållslaget* — asserts in the publication's own
voice, and in general terms, a benefit the body carries only as Maya Lind's
quoted judgement, beside the body's own statement that the test note does not
attribute the median-time difference to the software. The same round had also
made a valid repair, and it went with the round; the text delivered is the input
byte for byte.

What is still unreached is the clause about a defect established **after** the
round that introduced it. Six runs now reach a second round. In every one of
them the second round was accepted or the loop stopped for want of progress, and
in every run that had a repair-created defect at all, the re-review that
followed that round established it there and then — which is where the rule is
built to fire.

## Why a controlled correction return is not the route here

The ticket's criterion 7 allows a controlled correction return: a prepared
candidate handed back to the loop, so that the re-review meets the case whatever
a fresh round would have written. That is not reachable with this harness. The
runner starts one real Claude Code session and types a Formal Invocation into
it; the correction subagent is started by the Skill inside that session, and
nothing between the two is addressable from outside without machinery to
intercept a subagent's return, which neither this ticket nor
[`editorial-388/`](../../editorial-388/) provides. Building it would mean
changing what the runs are runs of.

What was reachable was the Contextual Instruction, and the fifth wave
established that this route is closed from the other end:
`case-study-sv-dictated` refused an instruction dictating an unsupported
headline, because a Contextual Instruction may narrow what the Skill leaves open
but cannot contradict an invariant, and the two `opinion-flawed-dictated` runs
show that a dictation weak enough to pass the envelope is one the re-review may
not establish either.

## What this wave does, and that it is steered

Four runs of `article-flawed` at `--max=3` with one Contextual Instruction:
**Rubriken ska vara högst fem ord lång och mellanrubrikerna högst fyra ord.**
That is a steer and this packet calls it one. It constrains form and not
content, and both limits are satisfiable inside the text's own strength.

Its purpose is to put as many freshly written, marginal parts as possible in
front of two successive reviews. `article-flawed` is the fixture whose first
round is regularly accepted with the missing byline still standing, so a second
round follows; a headline and three subheadings written to a tight word limit
are the parts most likely to sit near the line, and a part near the line is the
one two reviews can read differently. A defect the first re-review does not
establish and the second one does is exactly the later-discovery case.

## Revisions

As the waves before it: the implementation staged from the commit `8ba3c0b5`,
the fixtures the #386 inputs at `8d8925bf`.

## Cases

| Case | Input | Formal Invocation | Contextual Instruction | What it is for |
|---|---|---|---|---|
| `article-flawed-tight-headings-1` … `-4` | `editorial-386/runs/article-flawed/work/input.md` | `/redline --genre=article --language=sv --max=3 --output=response source.md` | *Rubriken ska vara högst fem ord lång och mellanrubrikerna högst fyra ord.* | **Steered.** Four runs of one case: a defect established after the round that introduced it. |

## What each outcome means

The six conditions of [the first plan](plan.md) and the two added by [the
second](plan-2.md) govern a case here unchanged. This wave establishes the
later-discovery case only where a run's re-review establishes a defect
attributable to an **earlier** round than the one it followed, and the run then
delivers the state immediately before that earlier round.

If none of the four does that, the clause is unmet by any preserved run, and the
packet says so in those words: it names the clause, says no run reached it, and
gives the waves as the record of what was attempted. It does not read a run as
having shown something it did not show.
