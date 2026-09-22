# Frozen plan — #389, third wave

Written after two runs of [the second wave](plan-2.md) had returned and before
any run of this wave was started, and not edited afterwards. The earlier plans
are left exactly as they were written.

## Why a third wave

The second wave's first two returns did not settle what it was aimed at:

- `case-study-sv-steered-2` accepted its candidate. The round's new headline
  attributed the benefit to the supervisor — *Gemensam logg hjälper
  underhållslaget, enligt arbetsledaren* — so nothing was there to reject.
- `case-study-sv-steered` **rejected its round**, and the defect its own
  re-review established was a strengthened claim in a **subheading** the round
  had written — *Elm Quay valde Svale utan att jämföra leverantörer*, where the
  text says only that no comparison is on record — beside a second subheading
  repeating the sentence under it. The round had rewritten the headline as
  well, and the headline went with the round; but the finding that rejected the
  round was not against the headline.

So a newly introduced **unsupported claim in the headline itself** is still not
what any preserved rejection turns on. This wave is aimed at that alone.

## Revisions

As the second wave: the implementation staged from the commit `8ba3c0b5`, the
fixtures the #386 inputs at `8d8925bf`.

## Why this fixture

`opinion-flawed` is the fixture on which a correction round has been observed
creating a headline defect: a staged run of `main` the same day as the #386
evaluation replaced its headline with one whose *ett halvår till* presupposes an
earlier half-year the text never states (issue #389's own account of it). Its
headline — *Kommunledningen hatar människor* — is one no round can leave
standing, so the headline is certain to be rewritten; what the round writes in
its place is the round's own.

The two unprompted runs of it in the first wave accepted their candidates, so
this wave gives the same disclosed kind of Contextual Instruction the second
wave used, pointed at the headline.

## Cases

| Case | Input | Formal Invocation | Contextual Instruction | What it is for |
|---|---|---|---|---|
| `opinion-flawed-steered` | `editorial-386/runs/opinion-flawed/work/input.md` | `/redline --genre=opinion --language=sv --output=response source.md` | *Rubriken ska säga vad skribenten vill att kommunstyrelsen gör.* | A newly introduced headline claiming what the text does not carry. |
| `opinion-flawed-steered-2` | the same | the same | the same | The same case a second time. |
| `case-study-sv-steered-3` | `editorial-386/runs/case-study-sv/redline/work/input.md` | `/redline --output=response source.md` | *Rubriken ska säga vad den gemensamma loggen gav underhållslaget.* | The ticket's own case, with the instruction pointed at what the headline asserts rather than at what it foregrounds. |

The instruction in each case names no defect, asks for no claim the text does
not carry, says nothing about rounds, budgets, candidates, re-review or
rejection, and is satisfiable without creating a defect: the text states the
writer's demand outright, and `case-study-sv-steered-2` satisfied a headline
finding by attributing the benefit to its source.

## What each outcome means

The six conditions of [the first plan](plan.md) and the two added by [the
second](plan-2.md) govern a case here unchanged. A case passes for the purpose
this wave was started for only where the finding that rejects the round is
against the **headline** the round wrote. A rejection turning on another part
is recorded as what it is, and a run that reaches no boundary establishes
nothing about rejection.
