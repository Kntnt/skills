# Frozen plan — #389

Written before any run of this packet was started, and not edited afterwards.

## What is being exercised

[#389](https://github.com/Kntnt/skills/issues/389). A correction round whose own
independent re-review establishes a defect the round introduced is rejected
entire: the pre-round Text Artifact is restored verbatim, the loop stops, the
round keeps the budget it spent, and the attempt is reported apart from the
findings the restored text still carries.

The shipped behaviour before the change stopped the loop on such a finding and
**delivered the defective correction anyway**, which is what `case-study-sv` of
the #386 evaluation recorded.

## Revisions

The implementation is staged from the detached commit object `8dd5f31b`, whose
`skills/` tree is `85d2690e`. That object is the working tree of this ticket's
single commit as it stood when the runs were started; the commit itself did not
exist yet, because the packet these runs produce is part of it. The claim a
verifier checks is `git rev-parse <commit>:skills` = `85d2690e1b5d8e101f42754ddb9906b77fc1c243`.

The fixtures are the #386 inputs as committed at `8d8925bf`.

## Cases

Every case runs [#388's trace harness](../../editorial-388/harness/staged_run.py),
which starts one real Claude Code session with its own configuration directory,
stages the Skills from the revision above with `git archive`, types the Formal
Invocation as a user types it, and keeps the parent transcript and every
subagent transcript. No source material is supplied to Redline in any case, and
no Contextual Instruction is given.

| Case | Input | Formal Invocation | What it is for |
|---|---|---|---|
| `case-study-sv` | `editorial-386/runs/case-study-sv/redline/work/input.md` | `/redline --output=response input.md` | The ticket's own reproduction. The headline says nothing of the angle; the round rewrote it into one claiming an effect the body withholds. A newly introduced unsupported claim. |
| `article-flawed` | `editorial-386/runs/article-flawed/work/input.md` | `/redline --genre=article --language=sv --output=response input.md` | The text has no subheading anywhere, so a round has to write them. #386 recorded one of them repeating the sentence under it. A newly introduced heading echo. |
| `case-study-flawed` | `editorial-386/runs/case-study-flawed/work/input.md` | `/redline --genre=case-study --language=sv --output=response input.md` | The acceptance control: a round with real findings to repair and no defect of its own, which must be accepted rather than rejected. |

## What each outcome means

A case **reaches the boundary** when the run's own re-review establishes a
defect that round introduced. The case then passes when, and only when, all of:

1. the delivered text is the pre-round state verbatim, not the candidate;
2. the reply says a round was attempted and rejected and what it had introduced;
3. the reply does not report the discarded defect as present in what it delivers;
4. the findings carried forward are the ones that commissioned the rejected round,
   reported unresolved rather than repaired;
5. no second attempt at that finding, and no compensating correction, follows;
6. exactly one closing Proofread pass runs, after the loop stopped.

A case that does **not** reach the boundary — the round introduced nothing, so
there was nothing to reject — establishes nothing about rejection and is
recorded as that, not as a pass. These runs are non-deterministic by nature: the
defect has to be created by a fresh correction subagent before anything can
reject it.

The acceptance control passes when its candidate is accepted and no rejection
occurs.
