# Restore the documentation-only boundary — #362

Attempt `ms-20261002-c8f9a6`, amend 2, starts at `71987cb9c6d23ffe49ddbc01b3dcb49d526a9400`. The independent verdict rejected the shipped registry exclusion added in amend 1. The latest Agent Brief authorises evidence finalisation; the owner clarification changes closure authority, not the product boundary. This amendment removes that exclusion from the final tree and preserves the completed retest and all earlier receipts. The historical [amend 1 report](../amend-1/README.md) describes its own attempt and remains unchanged; its product repair is superseded here.

## Scope repair and test boundary

The complete shipped `skills/` tree, including Orchestrate's engine and the generated catalogue, is byte-identical to ticket base `5b0260283b1d1597ca1ed2dddc602888dac7119d`. There is no new manifest-based registry rule. The proposed product changelog block was removed from `.kntnt-orchestrate/362.md`; both evaluation record-index entries remain staged there for the run to apply sequentially. The run-owned index and changelog themselves are untouched.

The imported immutable captures add 22 directories of numbered files to the repository index. The original engine discovers these directories under its existing rule, irrespective of companion manifests. The repository-state test's old fixture described the index before this additive evidence existed. Its exact expected dictionary now includes all 22 directories and each maximum sequence number, independently taken from the frozen source inventory. It still verifies the exact directory set, the decision-record maximum and now every captured maximum; unexpected directories or incorrect maxima fail. No evidence file is renamed, hidden, deleted or edited.

The public `isolate` test introduced in amend 1 is retained with the same fixture and all three original reservation expectations. Two expectations are added for the manifested capture directories, restoring its assertion of the original public contract. No test is deleted, skipped or weakened; [the test-preservation receipt](test-preservation.json) also verifies that all 384 ticket-base test functions remain. This test and the expanded repository fixture both [failed before restoration](red-1.txt), then [passed](green-1.txt) with the unchanged evidence-preservation and native-audit tests. The seam is the existing public reservation operation and the repository's exact tracked fixture; it was already specified by the supplied verdict and baseline contract. No new public behavior is commissioned.

## Whole-surface audit

[Scope and preservation](scope-and-preservation.json), with its [read-only audit source](scope-audit-source.txt), checks every shipped file against the ticket base, every one of the 630 imported files against its independent pre-transfer size/hash, and all 29,552 pre-amend evaluation artifacts against their Git blobs. All earlier packet files, records, finalisation artifacts, failed gates, successful gates, handoffs and amendment receipts remain unchanged. No frozen plan, input, criterion, historical judgment, ADR, editorial resource or earlier editorial-329 evidence is rewritten. The retained source worktree and branch are not accessed or changed in this amendment; their previously established preservation is retained without claiming a fresh observation outside the assigned tree. The initial slow audit was [stopped](audit-stopped.json) and replaced by the successful single-process batched hash audit; no mismatch or semantic trial triggered that replacement.

The two verified defect classes share the same boundary: additive evaluator/evidence integration cannot introduce shipped runtime or catalogue behavior. The sweep covers the complete shipped tree, the proposed changelog, the public test's asserted operation and the exact repository fixture. The only authored changes beyond this additive receipt directory are restoring the two shipped files, updating those two test expectations, and correcting the run-owned note. The tests document the unchanged operation against the integrated evidence.

## Verification and cleanup

The [four gate commands](gate-commands.json) are exactly those supplied and still stated in the unchanged `CONTRIBUTING.md`. [Environment settings](environment.json) resolve TMPDIR and tool roots to this ticket's physical system-temporary scratch. HOME and CODEX_HOME are not overridden. CPython 3.12 is selected for the green/full gate; the red receipt transparently retains its default CPython 3.14 run. Lifecycle registration alone uses a ticket-owned KNTNT_HOME, so the required recording operation writes inside the assigned scratch rather than another session's machine state.

[Gate processes](gate-processes.json) retains each exact command, process-group registration, completion status and duration; [the supervision source](supervisor-source.txt) and `gate-1.txt` through `gate-4.txt` retain the execution method and full outputs. [Cleanup](cleanup.json) records all 16 registered PIDs absent, all command groups ended, and five literal owned paths removed. It retains both session-registration manifests; no service or wait remains running. The gate used CPython 3.12.14, compared with the preceding verifier's 3.12.13; no environment-sensitive test was changed. [All four supplied commands passed](gate-summary.json):

| Command | Result |
| --- | --- |
| Ruff check | [Pass](gate-1.txt), 1.25 seconds including provisioning. |
| Ruff format | [Pass](gate-2.txt), 7,943 files already formatted, 0.83 seconds. |
| Full mypy command | [Pass](gate-3.txt), 89 source files, 4.40 seconds including provisioning. |
| Full pytest command | [Pass](gate-4.txt), 2,733 tests in 144.46 seconds; 145.53 seconds including provisioning. |

This builder result does not replace independent verification. Cleanup restored the absence of the local `uv.lock` and pytest cache observed at amendment start; no pre-existing ignored file was guessed away.

## Bounded outcome

The [completed measurement](../../gpt-retest-2026-10-01/README.md), [original checklist disposition](../../gpt-retest-2026-10-01/acceptance-disposition.md), [published result text](../result-comment.md) and [residual mapping](../residuals.md) retain their outcomes. Six English Write deliveries, eleven nested comparisons and six scope diagnostics were already complete. Variable judgments remain 5/6, article F1 4/6, complete-response F1 2/6, G2 5/6, L1 6/6 and scope detection 4/6; skips, method limits and accepted false allegations remain explicit. Full editorial acceptance and certification of later main remain unavailable.

The false-allegation and standfirst briefs remain local and owner-held. Document scope remains a parked measurement, with no extra checker or causal benefit inferred. No fresh product trial, semantic judge, product repair beyond removal of the rejected expansion, new issue, closure, push, release or global installation is performed. All original omissions remain omissions. The fresh verifier and Orchestrate retain the final disposition authority.
