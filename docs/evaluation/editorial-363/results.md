# Results for #363: idiomatic quoted speech, and leaving a working quotation alone

Measured against [the frozen plan](plan.md) and the frozen criteria in [`fixtures/README.md`](fixtures/README.md). Nothing in either was edited after the first run.

This file is written as the runs complete, so a section marked **pending** is work not yet done rather than work that found nothing.

## What was run, and in what

### Three arms, not two

The plan freezes two arms. A third, `r`, is the one revise-and-remeasure round the exit criterion allows, and the wording it carries is the wording this branch ships.

| Arm | Install | Product |
| --- | --- | --- |
| `b` | `install-baseline` | `main` at `8a37e57e`, unchanged |
| `c` | `install-candidate` | baseline plus the first candidate wording |
| `r` | `install-revised` | baseline plus the revised wording, byte-identical to the files this branch ships |

The candidate wording asks the reader-of-this-language question and stops there. The revised wording names what the reader has to supply — a verb whose subject cannot perform it, a time or place adverbial whose event is missing, a reference the sentence never introduces — and adds the instruction to read a repair back the same way before it stands.

### The harness, and a declared difference from the plan

The plan says each invocation runs in "one fresh subagent per invocation, of type `kntnt-opus-high`". The `b` and `c` arms were run that way. The `r` arm was not, and this is a declared difference.

Both Skills declare `kntnt.capabilities: "subagents"` and stop before writing where the harness cannot start one. The session that completed the `r` arm is itself a subagent of an orchestrating session, and a subagent of this harness has no agent-spawning tool at all: a Write run started that way stops on the unsatisfied capability before it resolves genre, technique or language. One such stop was produced and is kept at `logs/voided/` in the run scratch; it is a harness failure and not a run, and it is counted against nothing.

The `r` arm therefore runs each invocation as a **fresh top-level Claude Code session**, started from the shell as

```
claude -p --model claude-opus-5 --effort high --permission-mode bypassPermissions "<the turn>"
```

with the child-session environment variables unset so the session is not a child, and with the working directory set to that run's `work/`. The model and the deliberation level are the ones the plan names; what changes is that the seat is a session rather than a subagent, which is what lets the Skill start the checker and correction subagents its contract requires. The addendum's "the supported native harness for this family is Claude Code itself" is what this is. The turn text is unchanged between arms and is recorded in [`runs/write-turn.md`](runs/write-turn.md) and [`runs/redline-turn.md`](runs/redline-turn.md).

The difference is asymmetric between arms and is a reason to read an `r`-arm wall time beside a `b` or `c` one with care. It is not a reason to read the editorial outcomes with care: the Skill, its resources, its input and its blindness are the same in all three.

## Cost: what each wording adds to the mandatory reading

Words, by `wc -w`, in the surfaces a run actually loads. `help.md` is a man page and is not runtime reading; it is listed because `docs/rules/docs.md` requires it to restate the changed rule.

| Surface | Baseline | Candidate | Revised | Cand. Δ | Rev. Δ |
| --- | --- | --- | --- | --- | --- |
| `write/references/quotations.md` | 671 | 756 | 819 | +85 | +148 |
| `write/references/source-check.md` | 1 930 | 1 984 | 2 006 | +54 | +76 |
| `redline/SKILL.md` | 4 012 | 4 122 | 4 173 | +110 | +161 |
| `editorial/genres/case-study.review.md` | 167 | 182 | 179 | +15 | +12 |
| **Write, per run** | | | | **+139** | **+224** |
| **Redline, per run** | | | | **+125** | **+173** |
| `write/help.md` (not runtime) | 1 568 | 1 608 | 1 614 | +40 | +46 |
| `redline/help.md` (not runtime) | 1 393 | 1 424 | 1 430 | +31 | +37 |

`redline/references/correction.md` (1 624 words), the shared `base.md` (597) and `base.review.md` (549), and `genres/case-study.md` (282) are unchanged in every arm. For scale, `docs/evaluation/editorial-362/README.md` measures the whole mandatory reading for one `opinion` run at about 5 860 words.

The removed attempt at `git show 3f21d9b1:skills/editorial/redline/references/quotation-review.md` cost 418 reference words **and** a full artefact in a fresh seat at every review and re-review. Neither wording measured here adds a seat.

## Wall time

Pending.

## Row-by-row results

Pending.

## Criteria

Pending.

## Findings that belong to another ticket

Pending.
