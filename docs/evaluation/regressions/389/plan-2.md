# Frozen plan — #389, second wave

Written before any run of this wave had returned, and not edited afterwards.
[The first wave's plan](plan.md) is left exactly as it was written; this one
adds to it and replaces nothing.

## What the first wave left unestablished

The ten runs under [`runs/`](runs/) reached the rejection boundary twice, and
both rejections turned on a part the round had written: a subheading repeating
what it stood over, twice, and a standfirst promising a reason the body never
gives, once. Two things the rule states were therefore not exercised by any run:

1. **Rejection turning on a newly introduced headline.** The ticket's own case
   is a headline claiming in the publication's voice an effect the body
   withholds. Four unprompted attempts at the two fixtures that produced such a
   headline in the #386 evaluation produced none this time, so no run rejected
   one.
2. **Any run at a Correction Budget above one.** All ten ran at the default
   `--max=1`, so no run was ever in the state the rule's later-discovery clause
   governs — a defect established after a round later than the one that
   introduced it, where the state immediately before the introducing round is
   restored and every state built on it is discarded.

This wave is aimed at those two, and at nothing else.

## Revisions

The implementation is staged from the commit `8ba3c0b5`, which is the commit the
first wave's runs were staged for and which now exists. The claim a verifier
checks is `git rev-parse 8ba3c0b5:skills` against the `instruction_revision` in
each packet's `run.json`. The fixtures are the #386 inputs as committed at
`8d8925bf`, as in the first wave.

## The controlled setup, and what it is

Each run in this wave is given a Contextual Instruction, which no run of the
first wave was. That is a controlled setup and is recorded as one: it is not an
unprompted reproduction, and the packet's `contextual-instruction.txt` and
`prompt.txt` carry it verbatim.

What the instruction does is raise the pressure on the part the round rewrites.
What it does not do is any of the following, and a reader should check it against
each: it names no defect, it asks for no claim the text does not carry, it says
nothing about correction rounds, budgets, candidates, re-review or rejection, and
it is satisfiable without creating a defect — the four unprompted runs of
`case-study-sv` each satisfied a headline finding without one, by attributing the
judgement to the supervisor instead of asserting it in the publication's voice.
The defect, where a round creates one, is the round's own, and the rejection is
the run's own.

No source material is supplied to Redline in any case, and no correction return
is scripted: the harness types the Formal Invocation and the instruction as a
user types them, and reads nothing back into the run.

## Cases

Every case runs [#388's trace harness](../../editorial-388/harness/staged_run.py)
exactly as the first wave did, `--model=opus --effort=high`.

| Case | Input | Formal Invocation | Contextual Instruction | What it is for |
|---|---|---|---|---|
| `case-study-sv-steered` | `editorial-386/runs/case-study-sv/redline/work/input.md` | `/redline --output=response source.md` | *Rubriken ska säga vad testet gav, inte bara att det gjordes. Låt den lyfta fram nyttan med den gemensamma loggen.* | A newly introduced **headline** claiming an effect the body withholds, at the default budget. |
| `case-study-sv-steered-2` | the same | the same | the same | The same case a second time, because a round has to create the defect before anything can reject it. |
| `case-study-sv-budget-3` | the same | `/redline --max=3 --output=response source.md` | the same | The same pressure with room for three rounds: the state the later-discovery clause governs. |
| `article-flawed-budget-3` | `editorial-386/runs/article-flawed/work/input.md` | `/redline --genre=article --language=sv --max=3 --output=response source.md` | *Mellanrubrikerna ska vara konkreta och säga vad avsnittet under dem visar.* | A text with no subheading anywhere, so a round must write them, with room for three rounds. |

`--max=<n>` is the Correction Budget as the shipped `SKILL.md` and `help.md`
define it, used here as a caller uses it. Nothing about the Skill's own budget
contract is changed by this wave.

## What each outcome means

A case reaches the boundary only when the run's own re-review establishes a
defect a round introduced. The six conditions [the first plan](plan.md) states
govern such a case here unchanged, and two more apply to a run of more than one
round:

7. Where the round rejected is not the first, the text delivered is the state
   immediately before that round — the text as the round before it left it, and
   not the text as it arrived.
8. Where the defect is established after a round later than the one that
   introduced it, the text delivered is the state immediately before the
   introducing round, and every state built on that round is discarded with it.

A run that does not reach the boundary establishes nothing about rejection and
is recorded as that. A run whose round refuses the instruction's pressure —
leaving the finding unrepaired and saying so — is recorded as what it is, and is
not counted as a rejection.
