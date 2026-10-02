# GPT quotation retest, 2026-10-01

This packet measures the unchanged product at `fb16908712c4d47a36fc6ee9dfb3eb2714a19e65` under the new [maintainer decision](owner-decision.md). It does not edit that product, the inherited inputs, historical records or ADR-0212. Issue #393 owns the retest; publication and tracker decisions remain with the maintainer.

- [Frozen plan](plan.md), [input manifest](input-manifest.json), [judge criteria](judge-brief.md) and [native parent identity](parent-identity-evidence.json).
- [Current Write identifier construction](construction-repair-plan.md), [historical metadata construction](metadata-construction-plan.md), [actual refusal/skip disposition](construction-disposition.md) and [timeout boundary](timeout-note.md). The original plan remains unchanged; these annexes account for invocation construction and interrupted evidence.
- [Invocation index](run-index.json), [staging location](staging-location.json), [cleanup ledger](cleanup.json) and [source integrity](source-integrity.json).
- [Native runner](harness/run.py), [artifact/identity inspector](harness/inspect_run.py) and [native trace indexer](harness/audit_trace.py). These evaluator tools do not implement editorial decisions.
- [Validation](validation/results.json).
- [Results](results.md), [all semantic judgements and splits](semantic-judgements.json), [trace verdicts](trace-verdicts.json) and [cost/loading](cost-and-loading.json).
- [Exact local tracker comment](tracker-comment.md) and [proposed followup texts](proposed-followups.md); nothing is published.
- [Retained evidence locations and copy digests](evidence-locations.json), [neutral judge packet](judges/input.md), [Redline record](../../records/redline-gpt-2026-10-01-393.md) and [Write record](../../records/write-gpt-2026-10-01-393.md).

The native evidence of a completed run contains the exact supplied input, Formal Invocation, reply, delivered artifact when present, JSON event stream, parent and every retained child rollout, process/result metadata, before/after inventories and transient Markdown/text versions. `deterministic-facts.json` records transport and byte comparisons without a language verdict. `trace-index.json` points into actual calls and lifecycle events without crediting a glob, an encrypted message or a self-report as a complete resource read.

Native rollout filenames use local time, while event timestamps use UTC. The actual event timestamps and result durations establish chronology. All recorded model/effort contexts must match the parent's inherited `gpt-6.1-sol/xhigh` seat. A return code of zero alone cannot establish a completed operation: construction refusals, a service interruption inside a child, withholding and ordinary delivery have distinct dispositions.

Runs remained under neutral staging paths until both blind semantic judgements completed. Their byte-verified copies are now retained under `runs/`, `construction-refusals/`, `voided/` and `judges/`. Each judge received only a neutral packet of exact source/input, actual delivered artifact and user-facing reply, together with the frozen criteria. Trace inspection is separate because native traces identify the model. The external file observer can miss a file that exists for less than its sampling interval, and native encrypted dispatch arguments do not expose the complete child brief. A dependent criterion states that gap. The final results also name the omitted British mechanics passage that limits that standalone judgement.
