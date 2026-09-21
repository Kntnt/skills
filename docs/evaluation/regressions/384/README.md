# A reply carries the text in one fence, and the frontmatter comes through intact

Six native Skill runs — four `/redline`, one `/unslop`, one `/proofread` — made on 2026-09-21 for [#384](https://github.com/Kntnt/skills/issues/384), against the product [`plan.md`](plan.md) fixes: the working tree at `76ddacc1` with this ticket's change in it, staged as a byte copy of `skills/editorial/{redline,proofread,unslop}` and `skills/kntnt` side by side. Every run is a fresh `claude-opus-5` subagent at high deliberation, in Claude Code 2.1.278, with no history. Provider family `claude`; no Codex Harness and no GPT model was started from the session that ran this.

This packet is governed by [`../README.md`](../README.md) and not by the corpus protocol or its `records/` format.

It exists because the shared delivery contract settled where a result goes and was silent on how the response carries it. One saved Redline reply in sixteen came back with its frontmatter block broken — `---`, a blank line, then `kntnt:`, where its input had `---` and `kntnt:` with nothing between them — and said nothing about it (ADR-0211). The contract now states the rule; these runs are whether it reaches a real run.

The fixtures are the text that damaged run was given, and a seeded copy of it carrying one anti-slop pattern and one misspelling so that a run of each Skill has something to change.

## Results

| Run | Fixture | Wall time | Result |
| --- | --- | --- | --- |
| [`runs/redline-1/`](runs/redline-1/response.md) | `input.md` | 51 s | **not exercised** — stopped at the capability gate, no artifact carried |
| [`runs/redline-2/`](runs/redline-2/response.md) | `input.md` | 697 s | **pass**, all three items |
| [`runs/redline-3/`](runs/redline-3/response.md) | `input.md` | 661 s | **pass**, all three items |
| [`runs/redline-4/`](runs/redline-4/response.md) | `input.md` | 45 s | **not exercised** — stopped at the capability gate, no artifact carried |
| [`runs/unslop-1/`](runs/unslop-1/response.md) | `input-seeded.md` | 242 s | **pass**, all three items |
| [`runs/proofread-1/`](runs/proofread-1/response.md) | `input-seeded.md` | 72 s | **pass**, all three items |

Four replies carried an artifact and all four passed. Two Redline replies carried none and are recorded not exercised, as the plan says a reply that carries no artifact is recorded; neither is a miss, neither spent the revise-and-remeasure round, and no round was taken.

In every one of the six runs the only file that reached the run directory is the `response.md` the evaluator asked for: `work/input.md` is byte-identical before and after, and the staged install is unchanged. The response default wrote nothing, which the `sha256` inventories in each run directory show.

## The check

[`check.py`](check.py), run on each saved reply against the fixture that run was given; its output is at `runs/<run>/check.txt`. It reports how many fenced blocks the reply holds and which carry the artifact, whether any artifact content sits outside a fence, and whether the fenced text's leading frontmatter block is byte-identical to the fixture's. A reply carrying no artifact at all is reported not exercised rather than as a miss.

Run against the damaged reply this ticket came from, `docs/evaluation/editorial-362/runs/column-sv-r2/redline/response.md`, it reports zero fenced blocks, artifact content outside every fence, and a miss — so the check does detect the defect it was written for.

The three items, in each of the four replies that carried an artifact:

1. **One fence.** Each reply holds exactly one fenced block and it is the artifact's; the info string is `markdown` in all four. No run reached for a bare fence and none left the artifact unfenced.
2. **The run's own words outside it.** Read from each reply: the resolved configuration opens the reply above the fence, and the findings, the claim account and the mechanical-pass note follow below it. Nothing of the run's own is between the fence lines, and no part of the artifact is outside them — which `check.py` establishes mechanically by finding no `kntnt:` outside a fence.
3. **The frontmatter intact.** In all four the fenced text's leading frontmatter block is byte for byte the fixture's, `---\nkntnt:\n  genre: column\n  technique: none\n  language: sv\n---`. That is the block the original run turned into a horizontal rule and a paragraph.

## The two Redline runs that carried no artifact

`redline-1` and `redline-4` stopped before reading the text, each reporting the `subagents` Capability as unsatisfied: the session had no tool for starting an agent in its own context window, and Redline spends its Correction Budget by handing each round to a fresh subagent. That is the Skill's own rule for an Unsatisfied Capability — report it and stop before writing — so both replies are correct and neither is a miss. They carry no text, and a reply with no text has no fence to get right.

`redline-2`, `redline-3` and `unslop-1` ran in the same environment and corrected the text, so the capability gate answered differently on runs of one Skill under one condition. Nothing here establishes why, and it is not this ticket's question; it is recorded because four runs of one Skill on one input split two and two, and somebody reading these replies would otherwise have to discover it. It does not weaken what is measured: the delivery step is the same step whichever way the correction round was taken, and what these replies are read for is the shape of the reply.

## What this packet does not establish

- One Swedish column, one genre, one locale, one input. Nothing here says how any of the three Skills carries an English text, an HTML text, or a text holding fenced code of its own — the case the fence-length rule exists for is untested.
- Write is not measured here. It is bound by the same contract and its corpus is run by #380.
- Nothing here exercises a text whose Output Target is a file, In-place Editing, or the short no-change status, each of which the contract expressly excepts from the fence.
- The rule is a rule a body obeys and not a check anything enforces. Four replies obeying it is four observations, not a guarantee.
- A method probe was made before the four Redline replies were known: one further `/proofread` run on `fixtures/input-seeded.md`, started through the headless CLI rather than as a subagent, to establish a second way of staging a run in case the capability gate refused every Redline run. Its reply passed the same check. It is not recorded as a run here, no inventories having been taken around it, and the route was not needed.
