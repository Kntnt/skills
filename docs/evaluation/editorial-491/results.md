# Results for #491

**Stopped before Redline's baseline or implementation.** The independent complete-text validation of the supported-appraisal contrast produced a disagreement about a retained quotation. The frozen plan requires stopping dependent work on a validation disagreement. No product wording, corpus text or expectation is changed to make the reading agree. This is neither target reproduction nor non-reproduction: the target has not been measured.

The starting product/corpus revision is `4cf05813`. The prospective plan, exact controls, three contrasts, expectations, copied #480 judge briefs, native harness and fourteen-row baseline matrix were committed as `82eea7d7` before the first validator. `freeze.json` records that revision and prospective-file digests. The provider-native seat is the parent's verified `gpt-6.1-sol` at `xhigh`, with Codex CLI 0.160.0. Every completed validator's actual native turn context is checked in its `identity-audit.json`.

## Decision required

Both readers of `supported-appraisal` classify its customer headline as **supported** and its opening as **working**. They disagree about the body's references:

- Reader a classifies the body as **unresolved**, citing *innan nästa hus börjar*: “omits the activity that starts.” It invokes the existing clear-reference rule and the case-study instruction that quotation marks do not protect a missing referent. It says the log context permits clarification without inventing a rollout decision.
- Reader b classifies the body as **resolved**, reads the same quotation as a contextual ellipsis for the next house starting the shared-log trial, and identifies no contract conflict.

The phrase is retained from the revised corpus control; the alternate customer/appraisal/opening does not introduce it. The frozen contrast expectation says the complete text conforms and working wording is preserved. The two independent readings have not established that full-text conformance together. The plan's R1/C1 split rule applies to later run judges, not to contrast validators, and cannot silently decide this dispute.

The required decision is whether the quotation's ellipsis is working orientation or a visible reference omission, or whether to commission a new prospective contrast/validation pass that avoids that disputed quotation. No answer is inferred in this unattended session. A new pass must preserve this freeze and both completed readings. The validation split alone does not establish a real corpus conflict with a rule written after the control's freeze, so no corpus revision or separate corpus-defect claim is made here.

## Validation evidence

The six independent validators receive complete texts and the starting editorial contract through different anonymous native working directories under the physical scratch root. They receive no expected classification, candidate wording, ticket/arm path or investigation hint. `validation/validators.tsv` maps each contrast and letter to its neutral token; each packet retains the exact invocation, input, report, both private-root inventories, transient file versions, complete compressed native sessions and seat audit. These are validators, not Redline runs or R1/C1 judges.

All six native validators completed successfully. Their independent classifications are:

| Contrast | Reader a | Reader b | Distinction established |
| --- | --- | --- | --- |
| `supported-appraisal` | Headline supported; opening working; body unresolved at *innan nästa hus börjar* | Headline supported; opening working; body resolved | Supported appraisal/opening agree; complete-text conformance does not |
| `unsupported-attribution` | Headline unsupported; opening working; body resolved | Headline unsupported; opening working; body resolved | Both identify Svale receiving Lind's appraisal without support |
| `unresolved-referent` | Headline supported; opening working; body unresolved | Headline supported; opening working; body unresolved | Both identify *Det andra alternativet* as absent from the complete text |

The final [validation audit](checks/validation-audit.json) checks all six actual native contexts, prompts, public tool/reply traces and reports for ticket/arm disclosure and seat drift. It passes. Inventories establish that each validator's only working-material effect is its designated `validation-a.md` or `validation-b.md`; no text or contract material changes and no private authentication changes. Private Harness state, caches and staged exports are retained in the inventories. Wave-level working-tree changes are this builder's freeze manifest, gate receipts, results, record and deferred index note, not validator effects. No dependent Redline session was dispatched.

## Unmeasured target and controls

All fourteen planned baseline rows and the fourteen conditional candidate rows are skipped, individually, in [the protocol record](../records/redline-gpt-2026-10-02-491.md). There is no delivered Redline artifact, initial finding, correction proposal, re-review disposition, final Proofread, reply-check or R1/C1 judgment to score. No semantic red/green result is claimed. The five-stage headline/lead/standfirst ledger is inapplicable because no run reached its first review.

No candidate, revised candidate or implementation commit exists. No evidence-supported diagnosis was reached and no product change is authorized by fresh reproduction. No non-reproduction ADR is appropriate: an unrun baseline supplies no non-reproduction measurement. The reserved ADR number `0242` remains unused. No defect from #489/#490 is absorbed, and #478's declined checker extension is not rebuilt. No remaining Skill miss is filed from an unrun Skill evaluation.

## Verification

All four exact commands from CONTRIBUTING passed; [the receipts](checks/gate-results.json) preserve their commands, exit statuses, process ownership and start/end times. Ruff check and format check pass, mypy passes, and pytest reports **2,735 passed**. Only temporary/cache locations were relocated to assigned physical scratch; the builder's HOME and CODEX_HOME were preserved. [The preservation check](checks/preservation.json) establishes unchanged prospective working bytes and unchanged product, corpus, rules, tests and aggregate files. `freeze.json` records both working-copy and committed digests: Git's LF normalization affects the original matrix's line endings alone, and no row or method was changed. No shipped file changes, so the Catalog is unchanged and regeneration is unnecessary.

The final evidence commit carries the deferred records-index entry in `.kntnt-orchestrate/491.md`. CHANGELOG and `docs/evaluation/records/README.md` remain untouched. The branch is neither pushed nor merged. This packet is a stopped build's evidence, not a claim that #491's acceptance criteria have been delivered.

## Cleanup

All native sessions, their runner/wait processes and the gate completed. The [cleanup receipt](checks/cleanup.json) establishes that every original owned process group is gone, all explicitly named runtime/cache paths were removed, the supplied scratch directory is empty and the preserved deliverables remain. One recorded PID was subsequently reused in another process group; it was recognized as stale and never signalled. Nothing is deliberately left running. The first forced-removal command was rejected before execution; explicit non-forced removal of the same already-owned literal paths completed successfully.
