# Frozen plan — #389, fourth wave

Written before any run of this wave was started and before the third wave had
returned, and not edited afterwards. The earlier plans are left exactly as they
were written.

## Why a fourth wave

The second wave put the Skill in the state a Correction Budget above one
governs, and `article-flawed-budget-3` used it: the round repaired eleven of
twelve findings, its own re-review established one defect the round had
introduced, and the whole round was rejected with **two rounds of budget left
unspent and no second attempt**. That is the account of the budget that a run at
`--max=1` cannot give, where a spent budget and an exhausted one are the same
thing.

What it does not give is a run of more than one round. Every run so far has
rejected its round at the first one or accepted it and found nothing left to
correct, so no preserved run has a second round at all — and the rule's clause
about a defect established after a later round, which restores the state
immediately before the round that introduced it and discards every state built
on it, governs a state no run has been in.

This wave is aimed at reaching a second round. It gives the two conditions under
which one happens: a budget above one, and a first round that is accepted with
findings still standing. The first wave's two `article-flawed` runs are the
observed case of exactly that — each accepted its candidate with two findings
left, both of them absences the text arrived with — so this wave runs that
fixture at `--max=3` with **no Contextual Instruction at all**, since steering
the round is what made the second and third waves reject at the first round.

## Revisions

As the second and third waves: the implementation staged from the commit
`8ba3c0b5`, the fixtures the #386 inputs at `8d8925bf`.

## Cases

| Case | Input | Formal Invocation | Contextual Instruction | What it is for |
|---|---|---|---|---|
| `article-flawed-budget-3-2` | `editorial-386/runs/article-flawed/work/input.md` | `/redline --genre=article --language=sv --max=3 --output=response source.md` | none | A second round, and what the run does with a defect established in or after it. |
| `article-flawed-budget-3-3` | the same | the same | none | The same case a second time. |

## What each outcome means

The six conditions of [the first plan](plan.md) and the two added by [the
second](plan-2.md) govern a case here unchanged. What this wave can establish
beyond them:

- **A second round at all.** The trace records one delegation per round, and
  each delegation's brief carries the complete text as it stood when that round
  started, so the state before every round is readable from the packet.
- **A rejection at a round that is not the first**, where the text delivered is
  the state immediately before that round — the text as the round before it left
  it, and not the text as it arrived.
- **A defect established after the round that introduced it**, where the text
  delivered is the state immediately before the introducing round and the states
  built on it are discarded with it.

A run that accepts every round, or stops because a round made no relevant
progress, establishes none of those and is recorded as what it is. Whether the
loop reaches a second round is not in this plan's gift: a round that leaves
nothing to correct ends the loop with the budget unspent, which is the contract
working and not a failed case.
