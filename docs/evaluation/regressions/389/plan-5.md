# Frozen plan — #389, fifth wave

Written before any run of this wave had returned, and not edited afterwards. The
earlier plans are left exactly as they were written.

## Why a fifth wave

Nine runs at the shipped rule have now been made beyond the first ten, and two
things the rule states are still not what any of them turns on.

**A newly introduced headline.** Five runs were given a Contextual Instruction
pointed at the headline. Two of them rejected their round — `case-study-sv-steered`
on a subheading asserting more than the text does, `article-flawed-budget-3` on
a subheading doing the same after repairing eleven of twelve findings — and in
both the round's new **headline** was discarded with the round without being the
finding that rejected it. The rest wrote headlines their own re-review found
nothing against. The shipped correction brief now tells the subagent what a
defect of its own costs it, which is one reason a round writes a careful
headline; it is also why an unprompted reproduction of the ticket's own case is
not something a plan can promise.

**A defect established after the round that introduced it.** Two runs reached a
second round — `case-study-sv-budget-3`, which accepted both and stopped clean
with a round unspent, and `article-flawed-budget-3-3`, whose second round made
no relevant progress and stopped the loop there. Neither had a defect to
establish late, because every rejection so far happened at the first re-review
after the round that created it, which is where the rule is meant to fire.

## What this wave does differently, and that it is steered

Two of its four runs **dictate the headline's wording in the Contextual
Instruction**. That is a controlled setup and this packet calls it one: the
instruction names the words the headline is to have, so the round's wording is
the setup's and not the round's own. It is the route [the ticket's criterion
7](https://github.com/Kntnt/skills/issues/389) allows for exercising the
boundary — *if controlled correction returns are needed to exercise the boundary,
disclose that setup rather than calling it an unprompted reproduction* — and
nothing in these two runs is offered as an unprompted reproduction of anything.

What remains the run's own in them is everything the rule is about: whether its
re-review establishes that the headline claims what the body does not carry,
whether it attributes that to the round, whether it rejects the whole round,
which state it restores, and what its delivery says about the attempt. The
instruction names no defect, says nothing about rounds, budgets, candidates,
re-review or rejection, and does not tell the run the headline is wrong.

The dictated wordings are the two the record already holds:

- *Gemensam logg kortade tiden till åtgärd på Elm Quay* — the effect
  `case-study-sv`'s body explicitly withholds, its test note attributing the
  shorter median time expressly not to the software. This is the ticket's own
  defect, written into the setup instead of waited for.
- *Behåll telefonbokningen ett halvår till* — the headline a staged run of
  `main` wrote on `opinion-flawed` the same day as the #386 evaluation, whose
  *ett halvår till* presupposes an earlier half-year the text never states. It
  is the subtler of the two, which is why it is also the one given a budget of
  three: a defect its first re-review does not establish is a defect a later one
  can, which is the only way the later-discovery clause is reached without
  scripting a review.

## Revisions

As the waves before it: the implementation staged from the commit `8ba3c0b5`,
the fixtures the #386 inputs at `8d8925bf`.

## Cases

| Case | Input | Formal Invocation | Contextual Instruction | What it is for |
|---|---|---|---|---|
| `case-study-sv-dictated` | `editorial-386/runs/case-study-sv/redline/work/input.md` | `/redline --output=response source.md` | *Skriv rubriken som: Gemensam logg kortade tiden till åtgärd på Elm Quay.* | **Steered.** A newly introduced headline claiming an effect the body withholds. |
| `opinion-flawed-dictated` | `editorial-386/runs/opinion-flawed/work/input.md` | `/redline --genre=opinion --language=sv --output=response source.md` | *Skriv rubriken som: Behåll telefonbokningen ett halvår till.* | **Steered.** The same, with the presupposition observed on `main`. |
| `opinion-flawed-dictated-budget-3` | the same | `/redline --genre=opinion --language=sv --max=3 --output=response source.md` | the same | **Steered.** The same defect with room for three rounds: a first re-review that does not establish it leaves a later one that can. |
| `article-flawed-budget-3-4` | `editorial-386/runs/article-flawed/work/input.md` | `/redline --genre=article --language=sv --max=3 --output=response source.md` | none | Unsteered. A third attempt at a second round that has a defect to establish. |

## What each outcome means

The six conditions of [the first plan](plan.md) and the two added by [the
second](plan-2.md) govern a case here unchanged. Beyond them:

- A steered run establishes the rejection path **at the headline** only where
  the finding that rejects the round is against the headline the round wrote.
  Where the run's re-review finds nothing against the dictated headline, the run
  establishes that and nothing more, and is recorded as that.
- A round that refuses the dictated wording — leaving the finding unrepaired and
  saying so — is recorded as what it is, and is not a rejection.
- Nothing in this wave is evidence that a run reproduces the ticket's defect on
  its own. Four unprompted runs of `case-study-sv` and four of `opinion-flawed`
  are the evidence about that, and they are in the packet unchanged.
