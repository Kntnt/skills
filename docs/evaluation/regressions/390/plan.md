# Heading pairs — frozen regression plan

Frozen on 2026-09-22 before native execution, for #390, attempt `ms-20260922-37af51`. This is a focused packet under [the focused-regression protocol](../README.md), not a corpus evaluation. The product is the working tree based on `0cb71523`, with this ticket's changes. Stage byte copies of Write, Redline, Proofread and the Manager; preserve their SHA-256 inventory, exact invocation, native trace, response and filesystem account. Use the installed Codex CLI's configured GPT-family model and effort, copied without changing the user's installation. No other provider is run.

## Fixed cases

The fixture hashes are fixed in [fixtures.sha256.json](fixtures.sha256.json). Task files under [tasks/](tasks/) carry exact invocation material without these expected outcomes.

| Case | Input | Semantic criterion |
| --- | --- | --- |
| Recorded column | `fixtures/recorded-column.md`, byte copy of #386's Write delivery | Recognize the third subheading's repetition of its first sentence. The uncertainty about another form field is spent twice. Repair the heading from the section while preserving the doubt and other claims, or report the defect unresolved. |
| Paraphrased column | The recorded column with only that subheading changed to *En extra fråga kanske saknar verkan* | Recognize the same repeated proposition despite low lexical overlap; apply the same claim-preservation criterion. |
| Legitimate reuse | `fixtures/clean-reuse.md`, synthetic English library article | Do not flag the necessary repeated name *Riverton*, topic *Saturday*, or *library* merely for word reuse. The standfirst adds dates, trial length and purpose; section openings add counting and access details. Other genuine defects may be reported and do not invalidate this control. |
| Paraphrased headline | The clean control with headline and standfirst replaced | Recognize that *Weekend access is a temporary experiment* and *The Saturday service will run as a limited trial* repeat the same proposition despite little lexical overlap. Preserve the body's bounded trial and review claims. |
| Write column | Unchanged corpus `sources/column.md` copied to `fixtures/column-source.md` | Measure and judge all pairs before source comparison; deliver complementary pairs or explicitly account for remaining defects. Preserve uncertainty. Final delivered prose must be exactly the prose the final source comparison read, apart from metadata and delivery wrapping. |

## Execution and criteria

Run the four Redline cases with `/redline --max=1 --output=response input.md` and the Write case with `/write --genre=column --language=sv --output=response source.md`. Each is a fresh native session with its own work and scratch directories under the builder's permitted working tree. The supplied input and staged instructions are read-only to the run. Keep native parent and child records; a missing segment is a limitation, never evidence of an absent operation. Keep every attempt rather than replacing an unsuccessful one.

For each completed run judge: (1) the case's semantic criterion above; (2) consumption of `heading_pairs` in review or drafting and in every correction candidate, using the trace; (3) no unsupported strengthening or loss of claims; (4) bounded resource loading, with no review guidance or other editorial Skill loaded by Write; (5) source-check ordering for Write; (6) side effects against before/after inventories. A scalar overlap count or exact generated heading cannot settle any semantic criterion. The frozen cases are not changed to fit the outcome.

Save paired measurements before and after each delivered artifact. A correction agent must consider every pair even if its structural measurement exits 0, and word reuse alone cannot justify a correction. The packet does not test #389's acceptance/rollback policy.

If the native Harness cannot start or reach its service, preserve the failed startup and report native criteria as unexercised. Do not substitute a hand-authored repair, a script score or an evaluator's reading for a native outcome. Run remaining mechanical checks and record their independent result. No process may outlive its run; the runner records each process group immediately and terminates it on timeout.
