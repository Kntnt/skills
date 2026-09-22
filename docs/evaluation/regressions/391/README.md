# Write waits for checker completion and cleans up owned work

Focused native regressions for [#391](https://github.com/Kntnt/skills/issues/391), run on 2026-09-22 with Codex's native collaboration tools, inherited `gpt-6-astra` at high deliberation. This packet follows [the focused-regression convention](../README.md), not the corpus protocol. It does not use or change #388's trace harness.

The writer executed the staged Write Skill through its invocation shim with `general`, `en_GB`, no frontmatter and response output. The synthetic brief describes a library closure, opening hours, scheduled reopening and an unannounced contingency date. Each case used its own scratch and a fresh checker with no conversation history. One writer session executed the three cases sequentially because of the native concurrency limit. [The evaluator task](native-task.md), per-case invocation and checker prompts, [provenance](provenance.json), and [actual staged-file hashes](staged-files.json) preserve the setup.

## Observations

| Case | Report and delivery | Owned work after cleanup |
| --- | --- | --- |
| [File success](runs/file-success/result.md) | Checker wrote a complete report; writer consumed it after native completion and delivered unchanged prose. One bounded native wait returned without completion, then the native completion reply arrived. | Checker `check_file_success` was `completed` before and after cleanup; no shell waiter. |
| [Controlled denied write](runs/denied-write/result.md) | A policy injected into the checker denied report-file writes. Its complete 321-word reply exceeded the short-reply cap. No report file existed before the writer saved and read the reply; saved report and reply are byte-identical. Unchanged prose was delivered. | Checker `check_denied_write` was `completed` before and after cleanup; no shell waiter or additional native wait call. |
| [Controlled interruption](runs/interrupted/result.md) | Checker announced READY before report generation; native interruption returned its previous state as `running`. No report arrived. The writer stopped delivery and preserved the entire draft as not source-checked. | Checker `check_interrupted` was `interrupted` before and after cleanup; no shell waiter. |

All checker identities are under `/root/build_391_retry/native_391/`. Each case retains `lifecycle.json` with the exact identity and state observations, `events.json` with native calls and command completion, and filtered `process-*.json` snapshots. Snapshot matches that contain the inspection command itself are observers, not surviving waiters. Native checker state is established by native task observations; it is not inferred from the absence of an operating-system PID.

The before/after inventories show that every case work directory was removed. The writer's native state was subsequently observed as completed and the interrupted checker still as interrupted; the builder removed its staged Skill tree. [Final owned-state evidence](checks/final-owned-state.json) also records absent gate/finalizer PIDs and absent case/stage roots. No deliberately unbounded process was started, no completed checker was reactivated, and no interrupted checker was resumed. Evidence copies in this packet are intentional deliverables outside the run scratch.

[The builder's artifact checks](checks/artifact-verification.json) confirm that all three response prose blocks exactly match their initial drafts, the fallback report exactly matches the complete reply, and the interrupted case preserves the draft unchanged with its unchecked label. The report validation and final response for each case remain beside its invocation material.

## Contract and fixed checks

The [contract sweep](contract-sweep.md) accounts for the shipped procedure, delivery step and help surface. [Protected-paragraph checks](checks/preserved-contract.json) confirm that the checker task, findings validation, two-comparison ceiling, final-prose freeze, already-compared delivery branch and stopped-draft preservation remain unchanged.

The first builder reached the subscription limit after the synchronization red/green step and cleanup red step; the native retry continued its uncommitted changes. The original [synchronization failure](checks/red-sync.txt), [synchronization pass](checks/green-sync.txt), [cleanup failure](checks/red-cleanup.txt) and subsequent [cleanup pass](checks/green-cleanup.txt) are retained. These are executable-prose contract checks; native observations above supply the behavioral evidence. Captured check logs have trailing whitespace removed, with diagnostic text unchanged.

All four CONTRIBUTING checks passed: [Ruff check](checks/ruff-check.txt), [Ruff format](checks/ruff-format-green.txt), [mypy, 71 source files](checks/mypy.txt), and [pytest, 2,144 tests](checks/pytest-green.txt). The earlier formatting failure and full-suite failure are retained: the formatter wrapped one new assertion; the suite required preserving the shared filesystem-accounting sentence, which was restored alongside process/task accounting without weakening its test. [Focused final checks](checks/final-focused.txt) passed after the help paragraph was clarified and split. [Catalog generation output](checks/catalog.txt) and the Catalog equality check cover the final shipped bytes.

## Limits

- The denial is a controlled checker-policy constraint, with no attempted write. It is not an observed OS permission failure or a reproduction of Claude Code's historical refusal.
- The interruption is controlled, not a transport timeout. The checker announced entering a requested bounded native hold, but its internal wait call/result is not independently exported. The native interrupt and resulting task state are directly observed.
- Event logs are contemporaneous transcriptions where the Harness did not offer transcript export. File-success invocation-shim stdout was not retained; its [explicit limitation](runs/file-success/invocation-output-limitation.md) identifies what was observed without reconstructing the missing output.
- The staged source-check procedure is byte-identical to the final implementation. A wording-only delivery-account adjustment and help clarification after staging are disclosed in provenance; the final focused checks cover those edits.
- These cases exercise one short English fixture, one response target and first comparisons. They do not independently test cleanup failure, unavailable native completion, partial reports, a file output target, or a failed second comparison of unchanged prose. The instructions cover those branches; the existing preservation/final-comparison rules and their automated checks remain intact.
- The historical five-hour-fifty-five-minute waiter is not reconstructed or promoted into new measured evidence.
