# Redline rejects a round its own re-review finds a defect in

Focused native regressions for [#389](https://github.com/Kntnt/skills/issues/389),
run on 2026-09-22 in the `claude` family. This packet follows [the
focused-regression convention](../README.md) and not the corpus protocol: it is
aimed at one behavioural seam, and it judges no fixture against the editorial
matrix.

Thirty-one runs at the implementation this commit ships, and three before them
at an earlier draft of it. The earlier three are kept in
[`attempt-1/`](attempt-1/README.md), because one of them is the run that found
what the draft was missing. Nothing is relabelled and no run was discarded.

## How each run was made

Every run is one invocation of [#388's trace harness](../../editorial-388/harness/staged_run.py),
which starts a real Claude Code session with its own configuration directory,
installs the Skills there with `git archive` from a frozen revision, types the
Formal Invocation as a user types it, and keeps the parent transcript and every
subagent transcript. `--model=opus --effort=high`. No source material was
supplied to Redline in any run, and no correction return was controlled in any
run — see [what that would have taken](#why-no-correction-return-was-controlled).

Thirteen of the runs were given no Contextual Instruction. Eighteen were, and each
of those is marked **steered** below; [the plans](#the-waves-and-their-plans)
state what each instruction was for and reproduce it verbatim, and every
packet's `contextual-instruction.txt` and `prompt.txt` carry it as the run
received it. A steered run is not an unprompted reproduction of anything and is
never read as one here.

The first ten runs were staged from the detached object `8619e45e`, whose
`skills/` tree is `7d347bfce7de7f4daf8884a298b50a47425130c8`. The object is
detached because the commit these runs belong to did not exist while they were
being made. Against the shipped tree of that commit, `git diff 8619e45e --
skills/` shows exactly two differences and no third: one duplicated blank line
removed between two paragraphs of each correction brief, and the Catalog digests
that follow from it. No word of any instruction those runs read differs from the
shipped one.

The twenty-one later runs were staged from the commit `8ba3c0b5` itself, which
existed by then: `git rev-parse 8ba3c0b5:skills` is
`eeecfbdef0718b5486866e2e1a01e10cf7b0e07f`, and each packet's `run.json` names
that commit as its `instruction_revision`.

The fixtures are the #386 inputs at `8d8925bf`, copied verbatim; each packet's
`supplied-input.md` is what the run was given.

## The waves and their plans

Each plan was frozen before the runs it names were started, and none was edited
afterwards. Read in order they are also the record of what was tried and why.

| Plan | Runs | Aimed at |
|---|---|---|
| [`plan.md`](plan.md) | 3 of the first 10 | The rule itself, at the shipped implementation. |
| [`plan-2.md`](plan-2.md) | 4 | A rejection turning on a **headline**, and any run at a Correction Budget above one. |
| [`plan-3.md`](plan-3.md) | 3 | The headline again, on the fixture where `main` was observed writing a headline defect. |
| [`plan-4.md`](plan-4.md) | 2 | A **second round**, unsteered. |
| [`plan-5.md`](plan-5.md) | 4 | The headline by dictating its wording, and a defect established after a later round. |
| [`plan-6.md`](plan-6.md) | 4 | The headline under a length limit that leaves no room for a qualification. |
| [`plan-7.md`](plan-7.md) | 4 | The later-discovery clause, last wave. |

The seven further runs of the first ten were added after `attempt-1` showed the
rule needed strengthening, and they are judged against the same six conditions
[the first plan](plan.md) states. [`plan-2.md`](plan-2.md) adds two more for a
run of more than one round, and they govern every run after it.

## What the checks read

[`harness/outcomes.py`](harness/outcomes.py) reads the mechanical facts out of
each packet without reading the run's account of itself, and
[`harness/rounds.py`](harness/rounds.py) reads the state each round started
from out of the correction brief the trace records verbatim.
[`checks/outcomes.json`](checks/outcomes.json) and
[`checks/rounds.json`](checks/rounds.json) are their output over all
thirty-one packets, and [`attempt-1/outcomes.json`](attempt-1/outcomes.json)
over the three earlier ones.

All thirty-one runs exited 0 with a complete trace. Thirty of them invoked the
closing Proofread shim exactly once; the one that did not is
`case-study-sv-dictated`, which [refused its Contextual
Instruction](#the-envelope-refuses-a-dictated-defect) before reviewing anything,
so it delegated no round and ran no mechanical pass.

Two cautions about reading `checks/rounds.json`. A packet's
`delivered_is_the_pre_round_state_of_round` says **which** state the reply
delivered and not **why**: a round that was rejected and a round that returned
nothing relevant both leave the state before them as the delivered text, and
`article-flawed-budget-3-3` is the second of those, not the first. And a
restored state is compared after the closing mechanical pass, which is why
equality holds only where that pass found nothing to correct; in every run here
it did.

## What the first ten runs did

A run reaches the boundary only when its own re-review establishes a defect the
round introduced. Two of the ten did. None of the ten was steered.

| Run | Boundary | Outcome |
|---|---|---|
| [`column-flawed`](runs/column-flawed/) | **reached** | **Round rejected.** The round wrote a subheading, *Jag vill ställa frågan men vet inte om en ruta till hjälper*, over a paragraph saying the same in almost the same words, and a standfirst promising *varför jag ändå inte vet* — a reason the body never gives. Both were the round's own. The delivered text is byte-identical to the input. |
| [`column-flawed-2`](runs/column-flawed-2/) | **reached** | **Round rejected**, on the same fixture and a different defect: the subheading *Klockslagen får en ruta, förståelsen ingen* over the one sentence that says exactly that. The delivered text is byte-identical to the input. |
| [`article-flawed`](runs/article-flawed/) | not reached | The round wrote three subheadings and none of them drew a finding. Candidate accepted; two findings remain, both absences the text arrived with — no byline, and an ending the material carries no call to action for. |
| [`article-flawed-2`](runs/article-flawed-2/) | not reached | The same fixture again, the same shape: candidate accepted, nine of ten findings repaired, and the missing byline carried forward as the absence the text arrived with. |
| [`case-study-sv`](runs/case-study-sv/) | not reached | The ticket's own reproduction, which did not reproduce. The round's new headline attributes the judgement — *Elm Quays arbetsledare skulle göra om loggtestet* — instead of claiming the effect in the publication's voice as the #386 round did. |
| [`case-study-sv-2`](runs/case-study-sv-2/) | not reached | The same, a second time: *Elm Quays arbetsledare ser nytta med gemensam logg* keeps the judgement with the supervisor. |
| [`case-study-flawed`](runs/case-study-flawed/) | not reached | Candidate accepted. The round rewrote headline, standfirst, lead and both subheadings and introduced nothing. |
| [`column-sv`](runs/column-sv/) | not reached | One finding, repaired, accepted, nothing left. |
| [`opinion-flawed`](runs/opinion-flawed/) | not reached | Candidate accepted; the reply says in as many words that the re-review found *inget fel som rundan själv skulle ha infört*. |
| [`opinion-flawed-2`](runs/opinion-flawed-2/) | not reached | The same fixture again, accepted again. |

## What the twenty-one later runs did

Three of them reached the boundary. Eight reached a second round. One refused
its instruction. The rest accepted their candidates.

| Run | Steered | Rounds | Outcome |
|---|---|---|---|
| [`case-study-sv-steered`](runs/case-study-sv-steered/) | yes | 1 | **Round rejected.** The round's new subheading *Elm Quay valde Svale utan att jämföra leverantörer* asserts what the text does not: the text says only that no comparison is on record. A second new subheading repeated the sentence under it. Delivered text byte-identical to the input. |
| [`case-study-sv-short-headline-2`](runs/case-study-sv-short-headline-2/) | yes | 1 | **Round rejected, on the headline.** See [the headline case](#the-headline-case) below. Delivered text byte-identical to the input. |
| [`article-flawed-budget-3`](runs/article-flawed-budget-3/) | yes | 1 of 3 | **Round rejected, with two rounds of budget left.** See [the budget account](#what-a-budget-above-one-showed). Delivered text byte-identical to the input. |
| [`case-study-sv-steered-2`](runs/case-study-sv-steered-2/) | yes | 1 | Accepted. The round's headline attributed the benefit — *Gemensam logg hjälper underhållslaget, enligt arbetsledaren* — and the re-review established nothing against it. |
| [`case-study-sv-steered-3`](runs/case-study-sv-steered-3/) | yes | 1 | Accepted, headline *Gemensam logg gav underhållslaget en samlad bild*. |
| [`case-study-sv-short-headline`](runs/case-study-sv-short-headline/) | yes | 1 | Accepted. Under the same five-word limit as the run that was rejected, this round kept the activity in the headline — *Elm Quay testade gemensam logg* — and claimed nothing. |
| [`case-study-sv-budget-3`](runs/case-study-sv-budget-3/) | yes | 2 of 3 | Both candidates accepted, the loop stopped with nothing left to correct and the third round unspent. Delivered headline *Gemensam logg ger Elm Quays lag överblick*. |
| [`case-study-sv-dictated`](runs/case-study-sv-dictated/) | yes | 0 | **Instruction refused**, nothing reviewed, nothing written. See [below](#the-envelope-refuses-a-dictated-defect). |
| [`opinion-flawed-steered`](runs/opinion-flawed-steered/) | yes | 1 | Accepted, and the headline it accepted is the shape the ticket names: *Kommunstyrelsen bör ge telefonbokningen ett halvår till*, whose *ett halvår till* presupposes an earlier half-year the text never states. Its own re-review established nothing against it. |
| [`opinion-flawed-steered-2`](runs/opinion-flawed-steered-2/) | yes | 1 | Accepted, headline *Telefonbokningen bör finnas kvar i alla sju lokaler*. |
| [`opinion-flawed-dictated`](runs/opinion-flawed-dictated/) | yes | 1 | Accepted the dictated headline *Behåll telefonbokningen ett halvår till*; the re-review established nothing against it. |
| [`opinion-flawed-dictated-budget-3`](runs/opinion-flawed-dictated-budget-3/) | yes | 1 of 3 | The same, with a budget of three: one round, nothing left, two rounds unspent. |
| [`article-flawed-budget-3-2`](runs/article-flawed-budget-3-2/) | no | 2 of 3 | Both candidates accepted; the third round unspent, the missing byline carried forward. |
| [`article-flawed-budget-3-3`](runs/article-flawed-budget-3-3/) | no | 2 of 3 | Round 1 accepted; round 2 made no relevant progress and the loop stopped there, so the delivered text is the state before round 2. Nothing was rejected. |
| [`article-flawed-budget-3-4`](runs/article-flawed-budget-3-4/) | no | 2 of 3 | Both accepted; the reply says in as many words *Ingen runda avvisades*. |
| [`article-flawed-short-headline-budget-3`](runs/article-flawed-short-headline-budget-3/) | yes | 2 of 3 | Both accepted under the five-word headline limit. |
| [`article-flawed-short-headline-budget-3-2`](runs/article-flawed-short-headline-budget-3-2/) | yes | 2 of 3 | The same. |
| [`article-flawed-tight-headings-1`](runs/article-flawed-tight-headings-1/) | yes | 1 of 3 | Accepted; two rounds unspent. |
| [`article-flawed-tight-headings-2`](runs/article-flawed-tight-headings-2/) | yes | 2 of 3 | Both accepted. |
| [`article-flawed-tight-headings-3`](runs/article-flawed-tight-headings-3/) | yes | 1 of 3 | Accepted. |
| [`article-flawed-tight-headings-4`](runs/article-flawed-tight-headings-4/) | yes | 2 of 3 | Both accepted. |

## The headline case

[`case-study-sv-short-headline-2`](runs/case-study-sv-short-headline-2/) is the
ticket's own defect, produced and rejected in a native run. It was steered only
in its form: the Contextual Instruction was *Rubriken ska vara högst fem ord
lång*, which names no defect and asks for no claim, and the run that shares that
instruction, `case-study-sv-short-headline`, wrote a five-word headline claiming
nothing.

Its round rewrote the headline to **Samlade felanmälningar hjälper
underhållslaget** and made one valid repair beside it, replacing *systemet* with
*loggen* in a subheading. The re-review established that the headline asserts in
the publication's own voice, and in general terms, a benefit the body carries
only as Maya Lind's quoted judgement — the body saying outright that the test
note does not attribute the median-time difference to the software, and that
cost, satisfaction and time to completion were not measured. The reply's own
words: *Eftersom felet var rundans eget kasserades hela rundan, inklusive
rättelsen av underrubriken, och texten före rundan återställdes. Det felet finns
alltså inte i texten ovan.*

So the whole round went, the valid repair with it, and the delivered text is the
input byte for byte — `checks/outcomes.json` records the same SHA-256 for
`supplied` and `delivered`. All four findings are carried forward unresolved,
the budget is spent, and the discarded defect is reported as an attempt rather
than as something the delivered text has.

## What a budget above one showed

Eight runs reached a second round and one more had three rounds available and
needed one. Two things follow that no run at `--max=1` can show.

**The budget is spent, not exhausted.**
[`article-flawed-budget-3`](runs/article-flawed-budget-3/) repaired eleven of
twelve findings and was rejected entire for one defect its own re-review
established — the new subheading *Placeringen vid väggarna jämfördes aldrig*
over a passage saying that the *effect* of placement was not compared
*experimentally*, which changes the object and drops the qualification. Two
rounds of budget remained, and the run made no second attempt and no
compensating correction: *inget nytt försök följer*. At a budget of one, a run
that stops without trying again and a run that has nothing left to try with look
the same; here they do not.

**A clean correction is still accepted, twice over.**
[`case-study-sv-budget-3`](runs/case-study-sv-budget-3/) accepted two
consecutive candidates, and the loop stopped because nothing remained rather
than because the budget did — the third round is unspent. Seven other
multi-round runs did the same.

## The envelope refuses a dictated defect

[`case-study-sv-dictated`](runs/case-study-sv-dictated/) was given the
Contextual Instruction *Skriv rubriken som: Gemensam logg kortade tiden till
åtgärd på Elm Quay*, which is the ticket's defect written out in full. The run
refused it, reviewed nothing, delegated no round, spent no budget, ran no
mechanical pass and wrote no file, on the ground that a Contextual Instruction
may narrow what the Skill leaves open but cannot contradict an invariant: the
base contract's requirement that a causal verb have causal support, and the
headline contract's *never sharper than the text*.

That is the invocation-envelope contract working, and it is also a fact about
what can be staged from outside. An instruction blunt enough to guarantee the
defect is refused before a round exists; a dictation weak enough to pass the
envelope may be one the re-review does not establish either, which is what
[`opinion-flawed-dictated`](runs/opinion-flawed-dictated/) and
[`opinion-flawed-dictated-budget-3`](runs/opinion-flawed-dictated-budget-3/)
show, both of them delivering *Behåll telefonbokningen ett halvår till*
unremarked.

## Why no correction return was controlled

The ticket's criterion 7 allows a controlled correction return — a prepared
candidate handed back to the loop, so the re-review meets the case whatever a
fresh round would have written. No run here used one, because it is not
reachable with this harness. The runner starts one real Claude Code session and
types a Formal Invocation into it; the correction subagent is started by the
Skill inside that session, and nothing between the two is addressable from
outside without machinery to intercept a subagent's return, which neither this
ticket nor [`editorial-388/`](../../editorial-388/) provides. Building it would
change what these runs are runs of. What was reachable was the Contextual
Instruction, and the section above is what that route established.

## What the rejections establish

Five runs of the thirty-one rejected a round. Read against [the frozen
plan](plan.md)'s six conditions, all five meet all six, and between them they
exercise the repair-created defect in each of the three parts a correction round
writes — the subheading, the standfirst and the headline — and in both kinds the
ticket names, a claim asserted more strongly than the text supports and a
heading repeating what it stands over.

1. **The pre-round text is delivered, verbatim.** `checks/outcomes.json` records
   the SHA-256 of the supplied input and of the fenced text in the reply; they
   are equal for all five and for none of the other twenty-six.
2. **The attempt is reported as an attempt.** Each reply carries a section of
   its own — *Avvisad korrigeringsrunda*, *Rättningsrunda som förkastades*, *Försökt och
   förkastad korrigeringsrunda*, *Den avvisade rundan*, *Den förkastade rundan* — naming the round, what it had
   introduced, and that the state before it was restored.
3. **The discarded defect is not reported as present.** Both column replies say
   so outright: *Inget av detta gäller den levererade texten*, and *Denna brist
   finns alltså **inte** i texten ovan*; the headline case says *Det felet finns
   alltså inte i texten ovan*, and `article-flawed-budget-3` says *Defekten
   finns inte i texten ovan — den kasserades*.
4. **The findings carried forward are the restored text's own**, every one
   marked unresolved, and each of them a finding of the review that commissioned
   the round that was rejected — all ten of `column-flawed`'s, all eight of
   `column-flawed-2`'s, all twelve of `article-flawed-budget-3`'s and all four
   of `case-study-sv-short-headline-2`'s.
5. **The round is rejected whole.** `article-flawed-budget-3` threw away eleven
   repairs with the one defect, and `case-study-sv-short-headline-2` threw away
   a valid subheading repair with its headline.
6. **The budget is spent and no second attempt follows**, whether it was the
   last round available or not.
7. **One closing mechanical pass, after the loop stopped**, in every one of the
   thirty-one runs that reviewed anything.

The twenty-six runs that rejected nothing are what keeps this from being a rule
that fires on anything: twenty-six candidates accepted or loops stopped for
other reasons, none rejected for a defect the round did not introduce.
`case-study-flawed` in `attempt-1` and `opinion-flawed` here each show the
discrimination working from the other side — an old defect noticed only after a
round is named as one the text arrived with, and reported rather than blamed on
the repair.

## Limits

- **No run establishes a defect after the round that introduced it.** The rule
  says that where the introducing round is not the last, the state immediately
  before that round is restored and every state built on it is discarded. Eight
  runs reached a second round, which is the state that clause governs, and in
  none of them was there a defect left to establish late: every repair-created
  defect in all thirty-one runs was established by the re-review that
  immediately followed the round that created it, which is where the rule is
  built to fire. Reaching the clause needs a re-review that misses what a later
  one catches. That happens — `opinion-flawed-steered` accepted a headline
  presupposing a half-year the text never states — but in each observed case the
  round left no findings behind, so the loop stopped and no later re-review ever
  read the text again. The clause is therefore **unmet by any preserved run**,
  and what stands behind it is the contract prose in
  `skills/editorial/redline/SKILL.md` and the assertion in `tests/test_kntnt.py`
  that the prose is there. It is stated as unmet here rather than read out of a
  run that did something else.
- **The fix suppresses the case the evidence wants.** The shipped correction
  brief now tells the subagent what a defect of its own costs it — *the text you
  received is restored entire, nothing you did survives* — and a round that has
  read that writes a careful headline. Twelve runs of `case-study-sv` and
  `opinion-flawed` ended with a rewritten headline their own re-review
  established nothing against, four of them unprompted, where the #386 run and a
  staged run of `main` each created a defect in that same place. That is a
  result about the change and not only a difficulty in observing it: the rule is
  a backstop for a case the same commit made rarer.
- **A re-review can miss.** `opinion-flawed-steered` wrote the *ett halvår till*
  presupposition unprompted and delivered it; the two dictated runs delivered it
  too; `case-study-sv-budget-3` accepted *Gemensam logg ger Elm Quays lag
  överblick*. Nothing here establishes that every repair-created defect is
  caught — `attempt-1` is the demonstration that one can be missed, and these are
  the demonstration that a review can be the one that misses it. What the rule
  governs is what happens once a defect **is** established.
- **Eighteen of the runs are steered**, and the three rejections among them
  are rejections of defects the rounds wrote under pressure that a user's
  instruction can create. The instructions constrain form or foreground — a
  five-word headline, a headline that says what the test gave — and never name a
  defect or ask for a claim; the two that dictated a headline's wording are
  marked as dictations wherever they are cited. No claim here rests on a steered
  run being an unprompted reproduction.
- **Five rejections are five rejections.** They come from three fixtures in two
  genres, all in Swedish. Nothing here establishes a rate.
- **These are non-deterministic runs.** The defect has to be created by a fresh
  correction subagent before anything can reject it, which is why twenty-six of
  thirty-one runs establish only that nothing was falsely rejected.
- **The trace does not decode the correction brief's delivery.** It records the
  delegation's prompt verbatim, which is how `column-flawed`'s brief is readable
  in [its trace index](runs/column-flawed/trace-index.json) and how
  `harness/rounds.py` reads each round's starting state; nothing is inferred
  about a message the trace does not carry.
