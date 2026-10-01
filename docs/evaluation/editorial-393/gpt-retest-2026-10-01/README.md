# GPT quotation retest, 2026-10-01

This packet measures the unchanged product at `fb16908712c4d47a36fc6ee9dfb3eb2714a19e65` under the new [maintainer decision](owner-decision.md). It does not edit that product, the inherited inputs, historical records or ADR-0212. Issue #393 owns the retest; publication and tracker decisions remain with the maintainer.

- [Frozen plan](plan.md), [input manifest](input-manifest.json), [judge criteria](judge-brief.md) and [native parent identity](parent-identity-evidence.json).
- [Current Write identifier construction](construction-repair-plan.md), [historical metadata construction](metadata-construction-plan.md), [actual refusal/skip disposition](construction-disposition.md) and [timeout boundary](timeout-note.md). The original plan remains unchanged; these annexes account for invocation construction and interrupted evidence.
- [Invocation index](run-index.json), [staging location](staging-location.json), [cleanup ledger](cleanup.json) and [source integrity](source-integrity.json).
- [Native runner](harness/run.py), [artifact/identity inspector](harness/inspect_run.py) and [native trace indexer](harness/audit_trace.py). These evaluator tools do not implement editorial decisions.
- [Validation](validation/results.json).

The native evidence of a completed run contains the exact supplied input, Formal Invocation, reply, delivered artifact when present, JSON event stream, parent and every retained child rollout, process/result metadata, before/after inventories and transient Markdown/text versions. `deterministic-facts.json` records transport and byte comparisons without a language verdict. `trace-index.json` points into actual calls and lifecycle events without crediting a glob, an encrypted message or a self-report as a complete resource read.

Native rollout filenames use local time, while event timestamps use UTC. The actual event timestamps and result durations establish chronology. All recorded model/effort contexts must match the parent's inherited `gpt-6.1-sol/xhigh` seat. A return code of zero alone cannot establish a completed operation: construction refusals, a service interruption inside a child, withholding and ordinary delivery have distinct dispositions.

Runs remain under neutral staging paths until blind semantic judging is complete. The judge receives only a neutral packet of exact source/input, actual delivered artifact and user-facing reply, together with the frozen criteria. Trace inspection is separate because native traces identify the model. The external file observer can miss a file that exists for less than its sampling interval, and native encrypted dispatch arguments do not expose the complete child brief. A dependent criterion states that gap.
