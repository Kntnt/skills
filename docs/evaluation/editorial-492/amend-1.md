# Amend 1: gate repairs and the unavailable initial allegation

This amend starts from `cf96ff8ae306dea10d2cf88e54fb39ec5c7b3f1e` for
#492, attempt `ms-20261002-bc04ba`. It repairs the two deterministic code/check
faults and leaves acceptance criterion 3 unmet. It makes no claim that the
whole ticket is ready to land.

## Supported repairs

The existing registry-inventory test was observed failing before any repair:
its engine result contained 38 additional tracked directories from this packet.
The expectation now names every directory and its exact maximum, independently
bound to the frozen `file-versions.json` capture manifests. The existing #362
expectations and the assertion of complete dictionary equality remain intact.
No engine behaviour, registry discovery boundary or numbered evidence changes.
The focused test then passed.

A new declaration-contract test was observed failing on all five unannotated
module constants in the maintained evaluator: `REPOSITORY`, `NATIVE_CODEX`,
`CLEANUP`, `AUTHENTICATION` and `SKILLS`. Explicit `Path` and `dict[str, str]`
annotations make it pass. This is the only newly authored executable module in
the original ticket diff. The audit also checks every function signature,
including the nested capture function; none lacks an annotation. Erasing the
five annotations makes the amended evaluator AST identical to the original.
The frozen plans, smoke runner snapshot, native records and staged instruction
bytes remain unchanged. No new editorial session uses the amended evaluator.

## Diagnostic evidence audit and stop

The [audit](amend-1-evidence-audit.json) enumerates all five correction runs,
with authentic parent spawn ordinals, matching child task records, exact
sealed-payload hashes, every captured path and the observable initial parent
messages. Every full initial task is sealed in both records. None of these
runs captured an initial diagnostic memo as a Markdown/text file. The captured
editorial material is the input and later mechanical/final delivery; those
states cannot establish the initial allegation.

For `pre-library-alternatives-clean-file-1`, parent ordinal 67 says that the
lead repeats the standfirst's proposal and reasons. Ordinal 68 sends the sealed
correction task; its identical sealed content reaches the child at ordinal 9.
The concrete reader loss required to license the added library question is
absent from the accessible record. This is the gap identified in criterion 3,
not evidence that no finding occurred. The exact addition, existing sources of
its information, claim status, proposal, acceptance/re-review, Proofread and
accurate final report remain in the original packet and results.

The other four parents explicitly identify the standfirst-only mapping
referent or the certain-closure contradiction. Those observable allegations
are retained in the audit, separately from the unavailable full tasks. They
are not silently downgraded because the same capture limitation occurs there.
The non-reproducing opinion target runs had no correction task to recover.

No later summary is substituted for the missing library allegation, no T1
skip is promoted to a pass, and no existing judgement or criterion outcome is
changed. A new run cannot reveal what the original reviewer alleged. The
frozen plan forbids rerunning a completed result to obtain a preferable
verdict and provides no procedure for replacing that original diagnostic
record. Choosing a new observation method or treating a new measurement as a
replacement for it is an evaluation decision not settled by this ticket.
Under the unattended amend's stop rule, native evaluation work stops here.
The outstanding decision is how to recover the original plaintext allegation
or authorise and define a replacement measurement with complete initial-task
capture. Criterion 3 remains unmet until that decision is made and fulfilled.

## Verification

The original four CONTRIBUTING commands are unchanged. Their amend outputs,
receipts and the two red/green pairs are retained under `checks/amend-1/`.
Only disposable caches and temporary environments use the physically resolved
assigned scratch; the real HOME and CODEX_HOME are preserved. No shipped file
changes, so catalog regeneration is not triggered. All four checks exited 0: Ruff lint passed, Ruff format checked 8,777 files,
mypy checked 91 source files, and the full xdist suite passed all 2,736 tests
in 123.93 seconds. The [summary](checks/amend-1/summary.json) binds these checks
to the exact amended code hashes and retains the observed red/green receipts.
There are no surviving owned check process groups. The disposable runtime and
check wrapper are removed after their logs are retained; lifecycle and cleanup
receipts remain deliverables in the assigned scratch. Passing the project gate
does not satisfy the outstanding diagnostic-evidence criterion.
