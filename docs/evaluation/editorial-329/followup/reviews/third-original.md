# Third-candidate original-source evaluation

All six predeclared original rows completed their available stages at immutable revision `7b86144d`, with unchanged source bytes `6e531f5`. Nine native invocations ran; three planned Redlines were correctly skipped because Write delivered no artifact. This is complete execution of the frozen selection, not six successful pairs.

| Original row | Write outcome | Fresh paired Redline |
|---|---|---|
| opinion-sv-r1 | False-positive refusal: contextual criticism of evidential sufficiency was reconstructed as exhaustive municipal knowledge absence. | Skipped, no artifact. |
| opinion-en_GB-r1 | Delivered; all original criteria and independent F1 pass after variable/scope repairs. | Pass, unchanged. |
| opinion-en_US-r1 | Correct refusal: changed measurement domain remains after two comparisons. | Skipped, no artifact. |
| case-study-en_US-r1 | Delivered; all original criteria and independent F1 pass after removing an overexplicit causal link. | Pass, unchanged. |
| case-study-en_US-r2 | Delivered; all original criteria and independent F1 pass after one clean comparison. | Pass, unchanged. |
| case-study-sv-r1 | Correct refusal: second comparison retains the nonidiomatic translated building/activity reference. | Skipped, no artifact. |

Three delivered drafts and three paired finals pass F1; the other three rows are **not delivered F1 passes**. The two valid refusals show the bounded gate preventing delivery with a remaining factual or translation finding. They also expose first-comparison misses: the US checker dismissed different measurement variables as stylistic alternatives, and the Swedish checker accepted the calque before the final checker caught it. No candidate reliability claim is made from a favourable report alone.

The Swedish opinion refusal is independently confirmed as false positive (#357). The complete paragraph ties “den avvägningen” to the author's criticism that the presented material is insufficient. Hidden municipal information would not contradict that contextual sufficiency judgement. The exact reports and final checked prose preserve both the checker’s broader counter-reading and the later adjudication. The valid first-round repairs remain distinct from this final error.

All 11 source-checker sessions are fresh, inherit gpt-6-astra/high, read the complete original source and actual scratch draft, and stay within the two-comparison bound. Every delivered artifact exactly matches its final checker’s plaintext read after removing only delivery metadata and outer blank lines. Withheld checked prose is retained separately and never substituted for an artifact. No source is supplied to Redline; all three paired inputs are byte-identical to the complete delivered draft.

## Evidence and cleanup

- [Write record](../../../records/write-gpt-2026-09-20-349-third-original.md): all six attempts, complete reports, precise refusal distinctions and skipped delivered-text criteria.
- [Redline record](../../../records/redline-gpt-2026-09-20-349-third-original.md): three complete passes and three explicit skips.
- [Observation history](third-original-observations.md): full-context judgements and visible adjudications.
- [Inventory](third-original-inventory.json): nine invocations, twenty native sessions, inherited identities, actual source access and all roots absent.

Every all-root inventory shows zero surviving Skill effects outside native home state, with input and authentication unchanged. Every private root was removed by a literal absolute path after capture. The original batch ended. No product changes or commits were made by this evaluator, and baseline/other-provider outcomes did not inform these judgements.

The measurement-domain substitution failures and valid refusal basis discussed above are now tracked in [#360](https://github.com/Kntnt/skills/issues/360); historical judgements remain unchanged.
