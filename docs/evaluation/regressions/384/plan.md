# Focused behavioural regression for #384 — plan

Frozen on 2026-09-21, before the first run below. This packet is governed by [`../README.md`](../README.md) and not by the corpus protocol or its `records/` format.

Product under test: the working tree at `76ddacc1` with this ticket's change in it — the new *How a response carries the text* section of `skills/kntnt/library/references/delivery.md`, and the one sentence added to each of the four editorial Skills' `help.md`. It is staged as a byte copy of `skills/editorial/redline`, `skills/editorial/proofread`, `skills/editorial/unslop` and `skills/kntnt` side by side, the way [`../376/plan.md`](../376/plan.md) stages its own product.

Every run is one fresh `claude-opus-5` subagent at high deliberation, with no history. Provider family `claude`; no Codex Harness and no GPT model is started from this session. No judge is used and none is needed: the check below is mechanical.

Method is taken from [`../../editorial-362/runs/plan.md`](../../editorial-362/runs/plan.md) and from that file only — the turn that names the staged `SKILL.md` as its instructions and `$HERE` as its directory and carries the Formal Invocation verbatim, the one evaluator instruction that saves the reply verbatim to `response.md`, and the `sha256` inventories before and after. Its product and its paths are its own and are not reused here. The staged copy is not an installed Skill, so the Skill tool cannot start it.

One evaluator instruction is added to each turn and declared here because it is not the Skill's: save the user-facing reply verbatim to `response.md` in the run directory. A `sha256` inventory of the run directory and of the staged install is taken before and after each run, over everything but the inventory files themselves.

## Why this packet exists

The contract said where a result goes and was silent on how the response carries it. One saved Redline reply in sixteen returned the text with its frontmatter block broken — `---`, a blank line, then `kntnt:`, where the input had `---` and `kntnt:` with nothing between them — and the run's account never mentioned it ([#384](https://github.com/Kntnt/skills/issues/384), ADR-0211). This packet measures whether the rule the contract now states reaches a real run of the three Skills that deliver a reviewed text.

It is not a corpus evaluation. One Swedish column, three Skills, six runs, one mechanical check.

## Fixtures

- [`fixtures/input.md`](fixtures/input.md) — a byte copy of `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, the text the damaged run was given. `sha256` `74b966f1352c4f42e75dc58a7f247bd42571fced8760bcf12064067b8b81de42`, equal to that file's.
- [`fixtures/input-seeded.md`](fixtures/input-seeded.md) — the same file, its frontmatter block byte for byte as it is, with exactly two changes to the body: the paragraph `I dagens snabbrörliga arbetsliv är möten viktigare än någonsin.` inserted as a paragraph of its own between `Av Nora Vik` and the paragraph opening `Jag granskar`, and the first occurrence of `dagordning` spelled `dagordnig`. The first plants an anti-slop pattern for Unslop, the second a mechanical error for Proofread, so that a run of each Skill has something to change and therefore an artifact to carry.

## The runs

Each run has its own working directory holding the fixture copied to `input.md` and nothing else. Each line below is the Formal Invocation carried verbatim into the turn.

| Runs | Fixture | Invocation |
| --- | --- | --- |
| `redline-1` … `redline-4` | `fixtures/input.md` | `/redline --output=response input.md` |
| `unslop-1` | `fixtures/input-seeded.md` | `/unslop --output=response input.md` |
| `proofread-1` | `fixtures/input-seeded.md` | `/proofread --output=response input.md` |

Where fewer than two of the four Redline replies carry an artifact, Redline is run twice more on `fixtures/input-seeded.md` as `redline-5` and `redline-6`. Where the Unslop or the Proofread reply is nonetheless a no-change status, it is recorded not exercised and nothing further is run for that Skill. These extra runs are not the revise-and-remeasure round.

## The check

Mechanical, over each saved reply:

1. The artifact sits inside exactly one fenced code block.
2. Everything the run says about the text is outside that fence.
3. The leading frontmatter block of the fenced text is byte-identical to that of the fixture the run was given.

None of the three Skills has a reason to change that block on this input: the `kntnt` map already says what a run of it resolves.

A reply that correctly carries no artifact — a response-targeted run that changed nothing and left no unresolved finding returns the short no-change status in place of the text — is recorded **not exercised** for all three items. It is not a pass, it is not a miss, it does not spend the revise-and-remeasure round, and nothing is filed for it.

## What happens on a miss

One revise-and-remeasure round is allowed. Its runs are recorded beside the first six under their own names (`redline-1-r2` and so on) and both rounds stay in this packet. Where a run still misses after it, the result is recorded as measured, the better of the two wordings ships, and the residual is filed `needs-triage` naming #384.

## What is reported

Per run: the fixture, the invocation, the wall time, the verdict on each of the three items, and the two `sha256` inventories. Incomplete coverage is marked as such. No criterion is softened to fit a result.
