# Redline rejects a round its own re-review finds a defect in

Focused native regressions for [#389](https://github.com/Kntnt/skills/issues/389),
run on 2026-09-22 in the `claude` family. This packet follows [the
focused-regression convention](../README.md) and not the corpus protocol: it is
aimed at one behavioural seam, and it judges no fixture against the editorial
matrix.

Ten runs at the implementation this commit ships, and three before them at an
earlier draft of it. The earlier three are kept in
[`attempt-1/`](attempt-1/README.md), because one of them is the run that found
what the draft was missing. Nothing is relabelled and no run was discarded.

## How each run was made

Every run is one invocation of [#388's trace harness](../../editorial-388/harness/staged_run.py),
which starts a real Claude Code session with its own configuration directory,
installs the Skills there with `git archive` from a frozen revision, types the
Formal Invocation as a user types it, and keeps the parent transcript and every
subagent transcript. `--model=opus --effort=high`. No source material was
supplied to Redline, no Contextual Instruction was given, and no correction
return was controlled: every defect a round created, it created on its own.

The ten runs under [`runs/`](runs/) were staged from the detached object
`8619e45e`, whose `skills/` tree is
`7d347bfce7de7f4daf8884a298b50a47425130c8`. The object is detached because the
commit these runs belong to did not exist while they were being made.

Against the shipped tree of that commit, `git diff 8619e45e -- skills/` shows
exactly two differences and no third: one duplicated blank line removed between
two paragraphs of each correction brief, and the Catalog digests that follow
from it. No word of any instruction the runs read differs from the shipped one.

The fixtures are the #386 inputs at `8d8925bf`, copied verbatim; each packet's
`supplied-input.md` is what the run was given.

[The plan](plan.md) was frozen before the first run and names the revision
and the three cases that first wave ran. It is left exactly as it was
written. The seven further runs were added after `attempt-1` showed the rule
needed strengthening, and they are judged against the same six conditions the
plan states.

[`harness/outcomes.py`](harness/outcomes.py) reads the mechanical facts out of
each packet without reading the run's account of itself —
[`checks/outcomes.json`](checks/outcomes.json) and
[`attempt-1/outcomes.json`](attempt-1/outcomes.json) are its output. Every one
of the thirteen runs exited 0 with a complete trace, delegated exactly one
correction round, and invoked the Proofread shim exactly once.

## What the ten runs did

A run reaches the boundary only when its own re-review establishes a defect the
round introduced. Two of the ten did.

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

## What the two rejections establish

Read against [the frozen plan](plan.md)'s six conditions, both runs meet all
six, and between them they exercise both kinds of repair-created defect the
ticket names — a heading that repeats what it stands over, twice, and a
paratext part promising what the body does not carry, once.

1. **The pre-round text is delivered, verbatim.** `outcomes.json` records the
   SHA-256 of the supplied input and of the fenced text in the reply; they are
   equal for both runs and for neither of the other eight.
2. **The attempt is reported as an attempt.** Each reply carries a section of
   its own — *Avvisad korrigeringsrunda*, *Rättningsrunda som förkastades* —
   naming the round, what it had introduced, and that the state before it was
   restored.
3. **The discarded defect is not reported as present.** Both replies say so
   outright: *Inget av detta gäller den levererade texten*, and *Denna brist
   finns alltså **inte** i texten ovan*.
4. **The findings carried forward are the restored text's own.** All ten of
   `column-flawed`'s and all eight of `column-flawed-2`'s, every one marked
   unresolved, and each of them a finding of the review that commissioned the
   round that was rejected.
5. **The budget is spent and no second attempt follows.** *budgeten är förbrukad
   utan nytt försök*; the traces record one delegation each.
6. **One closing mechanical pass, after the loop stopped.** One Proofread shim
   invocation in each trace, after the round's delegation.

The other eight runs are what keeps this from being a rule that fires on
anything: eight candidates accepted, none rejected for a defect the round did
not introduce. `case-study-flawed` in `attempt-1` and `opinion-flawed` here each
show the discrimination working from the other side — an old defect noticed
only after a round is named as one the text arrived with, and reported rather
than blamed on the repair.

## Limits

- **The unsupported claim these runs rejected is a standfirst, not a headline.**
  The ticket's own case is a headline claiming an effect the body withholds.
  Four attempts at the two fixtures that produced such a headline before —
  `case-study-sv` twice, `opinion-flawed` twice — produced no such headline
  this time, so the run that could have rejected one never arose. What is
  established is that a newly introduced unsupported claim in a part the round
  wrote rejects the round; that the part in the observed case was the standfirst
  rather than the headline is a limit of the evidence and not of the rule, which
  names the headline, the standfirst and the subheading together.
- **Two rejections are two rejections.** They come from one fixture, in one
  genre, in Swedish. Nothing here establishes a rate, and nothing here
  establishes that every repair-created defect is caught — `attempt-1` is the
  demonstration that one can be missed.
- **These are non-deterministic runs.** The defect has to be created by a fresh
  correction subagent before anything can reject it, which is why eight of ten
  runs establish only that nothing was falsely rejected.
- **The trace does not decode the correction brief's delivery.** It records the
  delegation's prompt verbatim, which is how `column-flawed`'s brief is readable
  in [its trace index](runs/column-flawed/trace-index.json); nothing is inferred
  about a message the trace does not carry.
