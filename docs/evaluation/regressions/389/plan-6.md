# Frozen plan — #389, sixth wave

Written before any run of this wave had returned, and not edited afterwards. The
earlier plans are left exactly as they were written.

## What the fifth wave settled, and what it closed off

The fifth wave dictated the headline's wording in the Contextual Instruction,
which is the controlled route the ticket's criterion 7 allows. Two things came
back, and both of them are about the route rather than about the rule:

- **`case-study-sv-dictated` refused the instruction and reviewed nothing.** The
  dictated headline made the shared log the subject of *kortade*, and the run
  answered that a Contextual Instruction may narrow what the Skill leaves open
  but cannot contradict an invariant — the base contract's causal-support rule
  and the headline contract's *never sharper than the text* — so it stopped
  before any review, spent no budget and wrote nothing. That is the
  invocation-envelope contract working. It also means the harness cannot hand a
  round a defective headline by instruction: an instruction blunt enough to
  guarantee the defect is refused before a round exists.
- **`opinion-flawed-dictated` and `opinion-flawed-dictated-budget-3` applied the
  subtler dictated headline and their own re-reviews established nothing against
  it.** Both delivered *Behåll telefonbokningen ett halvår till*, whose *ett
  halvår till* presupposes an earlier half-year the text never states; neither
  re-review raised it. `opinion-flawed-steered` had already written almost the
  same headline unprompted and had it accepted the same way.

So the two ends of the controlled route are both closed: a dictation strong
enough to be caught is refused at the envelope, and one weak enough to pass the
envelope is not caught by the re-review. What is left is to put the round under
a pressure that is legitimate on its face and makes an overreaching headline the
likely thing to write.

## What this wave does, and that it is steered

All four runs are given the same Contextual Instruction: **Rubriken ska vara
högst fem ord lång.** That is a steer and this packet calls it one.

It constrains the headline's *form* and says nothing about its content: it names
no defect, asks for no claim, and a five-word Swedish headline that stays inside
the text's own strength is available in every fixture here. What it does is take
away the room in which the careful headlines of the earlier waves were written —
*Gemensam logg hjälper underhållslaget, enligt arbetsledaren* is seven words and
carries its attribution in the last two. A round that has to drop something
drops the qualification, which is the defect the ticket is about.

Whether it does, whether the re-review establishes it, and what the run then
does are the run's own.

## Why two of them have a budget of three

`article-flawed` is the fixture whose first round is regularly accepted with a
finding still standing — the missing byline, which no round can supply — so a
budget above one reaches a second round there, as `article-flawed-budget-3-3`
did. With the headline under pressure as well, such a run reaches one of the two
things still unexercised whichever way it falls:

- if its first re-review establishes the headline defect, the round is rejected
  at the round that wrote it, and the finding is against the **headline**;
- if the first re-review does not establish it and a second round follows, the
  second re-review reads that headline again — and a defect established then is
  established **after** the round that introduced it, which restores the state
  before that round and discards the state built on it.

## Revisions

As the waves before it: the implementation staged from the commit `8ba3c0b5`,
the fixtures the #386 inputs at `8d8925bf`.

## Cases

| Case | Input | Formal Invocation | Contextual Instruction | What it is for |
|---|---|---|---|---|
| `case-study-sv-short-headline` | `editorial-386/runs/case-study-sv/redline/work/input.md` | `/redline --output=response source.md` | *Rubriken ska vara högst fem ord lång.* | **Steered.** A headline with no room for the attribution the text's benefit carries. |
| `case-study-sv-short-headline-2` | the same | the same | the same | The same case a second time. |
| `article-flawed-short-headline-budget-3` | `editorial-386/runs/article-flawed/work/input.md` | `/redline --genre=article --language=sv --max=3 --output=response source.md` | the same | **Steered.** The same pressure where a second round is reached. |
| `article-flawed-short-headline-budget-3-2` | the same | the same | the same | The same case a second time. |

## What each outcome means

The six conditions of [the first plan](plan.md) and the two added by [the
second](plan-2.md) govern a case here unchanged. A run establishes the headline
case only where the finding that rejects the round is against the headline the
round wrote, and the later-discovery case only where the defect was established
after a round later than the one that introduced it. Anything else it does is
recorded as what it is.

This is the last wave. What it does not establish is written into the packet as
a limit, named as such, and not made to sound like something else.
