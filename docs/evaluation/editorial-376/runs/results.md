# Real Skill runs for #376, results

Run on 2026-09-20 as [`../plan.md`](../plan.md) says: three `/write` runs of the corpus `opinion` source in `en_US`, each a fresh `claude-opus-5` subagent at high deliberation in Claude Code, against a staged byte copy of the working tree with `skills/editorial/write/` changed for #376. Nothing was rerun. Each run directory holds `write/` (source, reply, evidence, inventories), `draft.md` — the prose the last comparison read — and two independent judgements.

The three runs were started together and ran concurrently, as the nine runs of [`../../editorial-362/runs/results.md`](../../editorial-362/runs/results.md) were, and nothing else was running on this machine while they did. Wall times are read from the mtime of each run's `inventory-before.txt` and its `response.md`.

## One slip in the plan, left as it is

[`../plan.md`](../plan.md)'s opening sentence points at a `criteria.md` beside it. No such file was ever written: the criteria are in the plan itself, under **Criteria, fixed before the runs**. The plan is left exactly as it was frozen, dangling pointer included, because what that criterion protects is a plan nothing touched after the first run started, and a tidied link would cost more than it is worth.

## What ran, and what ships

Four differences between the text these three runs executed and the text that is committed. All four were written after the runs started, and none of them is in the delivery rule the runs were made to measure.

1. In the comparison task, "A finding is a defect that must be repaired before delivery" became "A finding is a defect in the draft rather than a preference about it". The runs therefore executed a task that still asserted the outcome this ticket replaced — the conservative direction, which makes a run **less** likely to deliver with a finding standing, not more.
2. In the placement paragraph, "To a path, that document carries the same accounting once more as one clearly editorial block" became "Where that document goes to a path, it also carries the same accounting once, as one clearly editorial block". Same rule, plainer sentence. It governs the in-document markings case, which this row does not reach; [`../../regressions/376/`](../../regressions/376/README.md) measures it against the committed text.
3. `SKILL.md` step 9 ended "Done when the draft has been delivered"; it now ends "Done when the draft has been delivered, or the run has stopped with its prose preserved and accounted for".
4. `help.md` gained a sentence on a standpoint the brief gives as its author's own. `help.md` is not loaded by a run.

## Write

| Row | Outcome | Comparisons | Remaining findings reported | Delivered prose = prose the last comparison read | F1 | G2 | L1 | Judges split | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `opinion-en_US-r1` | delivered | 2 | 3, each with passage, source and proposed repair | yes | fail (3 named residuals) | pass | pass | no | 803 s |
| `opinion-en_US-r2` | delivered | 2 | 1, with passage, source and proposed repair | yes | fail (1 named residual) | pass | pass | no | 905 s |
| `opinion-en_US-r3` | delivered | 2 | 2, each with passage, source and proposed repair | yes | fail (2 named residuals) | pass | pass | no | 905 s |

Median wall time 905 s, against 1 024 s and 963 s for the two `opinion-en_US` rows of #362 — both of which **stopped and delivered nothing** — and against that evaluation's median of 896 s over nine runs of three sources in three locales. The cost of the new outcome in comparisons is nil: two comparisons then, two comparisons now. Its cost in wall time is within the spread of the old contract's own runs, and it is paid for a draft rather than for a refusal. Each run used one subagent for the writer and one per comparison, so three writers and six checkers; the six judgements cost six more.

Side effects, from the `sha256` inventories: in all three runs `source.md` and the staged install are unchanged and nothing remains in the run directory but the two files the evaluator asked for.

## What the runs show

- **Every run reached the situation the ticket is about, and every one of them delivered.** All three second comparisons left at least one finding the run accepted and could not repair without changing prose no comparison had read. Under the old contract each of these was a stop; under the new one each is a delivered draft with the finding named. The two `opinion-en_US` runs of #362 met the same kind of defect on the same source and produced no draft at all.
- **No run changed prose after the final comparison.** The prose the last checker read appears byte-for-byte in every reply, verified by exact substring against the evidence, and both judges of each run confirmed it independently. This is the gate `opinion-en_GB-r2` broke in #362, and the reasoning it broke it with — that the checker's own proposed wording is safe — is answered in all three replies, two of which say so in almost the instruction's own words.
- **Every remaining finding was reported with what the editor needs.** Each reply names the draft passage, says what the material carries instead, and gives the smallest repair the checker proposed, unapplied. `r3` says in terms that the findings are the checker's allegations and not established facts about the text; `r1` and `r2` say the passages are the reader's to settle.
- **Every reply led with the defects.** All three open on the draft being delivered with known defects, before the draft itself and before any other account of it.
- **`F1` fails in all three runs, and that is this contract working.** The residual each run names is the unsupported passage. The protocol hard-fails an unsupported fact and this ticket's plan says the verdict is recorded as it falls; no `needs-triage` ticket is earned by a residual the delivery account names. The residuals: in `r1`, 18 June stated as the occasion of the decision, "for the first time" widening an absence the source locates in the case papers, and "per booking" for *per bokningsväg*; in `r2`, "we have not calculated" for the source's *gör inget anspråk på att ha … kostnadsberäknat*; in `r3`, "two of the seven premises" for a set membership the material never states, and "a labor cost with a number attached" where the trial records time.
- **One finding was introduced by the run's own first-round repair.** `r3`'s "two of the seven premises" came out of a repair made after the first comparison; the second comparison caught it and the run reported it rather than repairing it again. That is the cap doing what it is for.
- **The judges did not split anywhere.** Six judgements, three runs, and on outcome, comparison count, byte-identity, F1, G2 and L1 the two judges of each run agree, down to which passages the residuals are.
- **`r2` shows a checker weakness this ticket does not touch.** Its first comparison had already reached the *gör inget anspråk* passage and filed it as an editorial question with no repair; the second raised it as a finding. That is the checker, not the delivery rule.
- **No evidence was truncated.** The Harness refused no checker write in any of the three runs, so the re-run clause the plan declared for that case was not used.

## Criteria the plan fixed

- **No run delivered prose no comparison had seen.** Met, 3 of 3.
- **No run ended in a stop on an accepted finding alone.** Met, 3 of 3 — no run stopped at all.
- **Where the final comparison left an accepted finding, the delivered prose is byte-identical to the prose that comparison read and the account names each remaining finding with its proposed repair.** Met, 3 of 3. The situation was reached in all three runs, so the plan's clause about reporting these two as unverified does not apply.
- **`T1` and `R2`** — `skipped` in every run: a subagent's Harness trace is not readable from the session that started it.

No revise-and-remeasure round was needed, and none was run.
