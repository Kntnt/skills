# The final comparison and the delivery, for #376: what was changed, shown and not shown

Everything here was run on 2026-09-20 in the Claude family: Claude Code 2.1.278, every run, every checker a run started and every judge a fresh `claude-opus-5` subagent at high deliberation, started from a `claude-opus-5[1m]` session. The protocol forbids a Claude session from driving a Codex harness, so nothing here retests any GPT-family result, and the GPT-family retest that #362 is still open for stays Thomas's own step.

## The change

Three files of `skills/editorial/write/` ship differently: `references/source-check.md` (989 words before, 1 574 after), `SKILL.md` (steps 6, 7 and 9) and `help.md` (`--output`, `## SOURCE FIDELITY`).

- **The delivery outcome.** Where the final comparison — the last one the run made, whether that is the second or the first — leaves an accepted defect or a genuinely unresolved material claim, Write delivers the prose exactly as that comparison read it and reports every remaining finding beside the draft: the passage, the concrete problem, what the material carries instead, and the smallest repair the checker proposed. The account says the draft comes with known defects before it says anything else about it, and asserts no fidelity for the passages it names. A remaining finding is reported as what the comparison alleges and the editor settles.
- **The gate, made absolute.** After the final comparison no prose changes at all, "not even into a repair the checker itself proposed: a repair no comparison has read is unchecked prose however safe it looks". That sentence answers the reasoning `opinion-en_GB-r2` of [#362](../editorial-362/README.md) talked itself past.
- **What still stops, and what a stop may not do.** Stopping is for prose no comparison has read: a comparison that could not finish, material that could not be supplied in full, a missing or partial report. A stop no longer destroys the draft — the current prose is preserved where the user can still reach it, with the comparison status and what was and was not compared, so the work can be resumed rather than written again. Only genuine scratch is removed.
- **Where the findings go.** Beside the text by default, never inside the draft or the Output Target file. On an explicit request for markings in the document, that is followed instead, with the prose left exactly as the comparison read it and each marking plainly editorial and separable from it.
- **Whose a statement is.** The comparison task now preserves who stands behind a statement: a valuation, a rhetorical generalisation or a position the brief gives as the commissioning party's own is supported as that party's standpoint and needs no external evidence to be expressed as theirs, while a figure, an event or a claim about an actual population stays a factual claim whoever supplied it. Calling an unsupported factual claim an opinion supports nothing. The writer is told not to go looking for outside legitimation of a standpoint already identified as somebody's own.

The two-comparison cap is unchanged. The comparison task is otherwise unchanged from what #362 shipped.

## Why: what #362 measured

Three of nine runs met a real defect at the second comparison, and the contract had only two ways out. `opinion-en_US-r1` and `-r2` held the gate and stopped, at 1 024 s and 963 s, each after five supported repairs, over a defect one clause would have closed; both stops were judged valid and neither produced a draft. `opinion-en_GB-r2` applied the checker's own proposed wording after the last comparison and delivered prose no checker had read, and a residual in the same draft was caught by nothing. #362 says both that a stop is never an approved draft and that never delivering is not a solution, and the contract as written could not give both. [`../editorial-362/runs/results.md`](../editorial-362/runs/results.md).

The preservation half comes from a real article run reported in #381: a completed comparison left three bounded findings, the run followed the rule and removed the scratch that held the only copy of a finished 2 600-word draft, its source copies and its check reports, and the text had to be written again — without the comparison it had already passed.

## What was measured

| Step | Runs | Result |
| --- | --- | --- |
| [The arm](plan.md), three `/write` runs of the corpus `opinion` source in `en_US`, the same row whose two #362 runs both stopped | 3, plus 6 judges | All three reached the situation the ticket is about and all three delivered. The prose the last comparison read appears byte-for-byte in every reply; no run changed prose afterwards; every remaining finding is named with its passage, its source and its proposed repair; every reply leads with the defects. `F1` fails in all three on the named residual, which is this contract working and earns no ticket. `G2` and `L1` pass. The two judges of each run agreed on everything. Median 905 s, against 1 024 s and 963 s for two runs that delivered nothing. [`runs/results.md`](runs/results.md). |
| [The focused regressions](../regressions/376/README.md) for preservation, in-document markings and the standpoint boundary | 5 runs, 2 checker probes, 1 judge | All three seams pass. Markings: a file target with an explicit request for them delivered `article.md` whose prose, with the markings and the frontmatter set aside, is byte-identical to the draft the last comparison read, the three findings carried as separable editorial comments and an editorial block holding the same accounting. Preservation: a run whose comparison could not finish left `article.md` unwritten, preserved the complete draft at `article.NOT-SOURCE-CHECKED.draft.md` beside it, reported the path, the obstacle and that no comparison ran, asserted no fidelity, and said how to resume — after two earlier attempts that failed to induce the condition and are kept. Standpoint: 2 of 2 checkers on all four passages, confirmed by a blinded judge. |
| The four checks in `CONTRIBUTING.md` | | pass |

## The acceptance criteria, one by one

1. **`source-check.md` states one outcome for a supported finding at the final comparison, and `help.md` describes the same outcome.** Met.
2. **A frozen evaluation runs the corpus `opinion` source in `en_US` at least three times; no run delivers prose no comparison has seen; the record says for each run whether a draft was delivered.** Met, 3 of 3.
3. **The cost of the chosen outcome is reported beside the current one.** Met: two comparisons then and now, median 905 s against 896 s over #362's nine runs and against the two `opinion-en_US` rows at 1 024 s and 963 s. [`runs/results.md`](runs/results.md).
4. **The four checks pass and the catalog is regenerated.** Met.
5. **The delivered prose is byte-identical to the prose the last comparison read, and the account names each remaining finding with its proposed repair.** Met, 3 of 3, verified by exact substring and by two independent judges per run.
6. **No run ends in a stop on an accepted finding alone.** Met: no run stopped.
7. **Every surface inside `skills/editorial/write/` that asserted the old outcome states the new one, and the three named tests pass unamended.** Met; the sweep found nothing asserting it outside that directory.
8. **The shipped wording states the outcome for the final comparison the run made, whether the second or the first.** Met.

## What is not solved

- **No run of the arm ever stopped**, so nothing in the three `opinion` runs shows the preservation rule in use; it is measured only in [`../regressions/376/`](../regressions/376/README.md), on one synthetic fixture, and the condition there had to be induced over three attempts and was finally stated to the run as a fact about its environment. A Harness refusing a write of its own accord, which is the #378 situation, is not the same event and is still unobserved under this contract.
- **Four sentences were written after the arm started.** They are listed in [`runs/results.md`](runs/results.md). The one inside the comparison task still asserted the outcome this ticket replaced, which biases against the result rather than towards it; the other three are outside what a run loads or outside this row.
- **`r2`'s first comparison filed a real defect as an editorial question with no repair**, and only the second raised it as a finding. That is the checker, not the delivery rule, and it is the kind of thing #362's checker diagnostic is about.
- **One run's own first-round repair introduced the defect its second comparison found** (`r3`, "two of the seven premises"). The cap caught it; a repair made after a *first* comparison is still unchecked until the second reads it, and a run that makes no change has no second comparison to catch anything.
- **Nothing here says what Redline does to a draft delivered with named findings.** That is #377's.
- **One locale, one genre, one source.** The row was chosen because it is the row that failed; nothing here says how the new outcome behaves in Swedish, in another genre, or with a technique.

## Cost

`source-check.md` grows by 585 words and `SKILL.md` by 161. For an `opinion` run the mandatory reading (`SKILL.md`, `base.md`, the genre, `web-craft.md`, `delivery.md`, `source-check.md`, before the language scope and any source) goes from 5 861 to 6 607 words, 13 % more. The comparison count is unchanged. This evaluation used 3 arm runs with 6 checkers and 6 judges, 4 regression runs with 5 checkers, 2 checker probes and 1 regression judge: 27 subagent runs, of which the 3 arm runs took 803 s, 905 s and 905 s and the 4 regression runs 727 s, 793 s, 73 s and 270 s.
