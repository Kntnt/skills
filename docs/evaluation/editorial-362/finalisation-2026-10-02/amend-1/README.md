# Registry compatibility amend — #362

Attempt `ms-20261002-030a34`. Amend 1 starts at `ca72bb42caf4d135505163af13c5ab559f736040`, after the independent verdict rejected the evidence integration's deterministic numbered-registry failure. The frozen GPT retest is complete; its editorial failures, omissions, disputed readings and parked document-scope measurement remain exactly as recorded. This amend does not repeat or rejudge it.

## Cause and bounded repair

The repository index contains 117 numbered file-version captures added by this ticket: 90 Markdown files and 27 text files, across 22 directories. The detector interpreted their sequence numbers as numbers for future authored records. [The whole-surface audit](numbered-captures.json) lists every path and verifies its membership and hash against the original companion manifest, including smoke, voided, judge and counted-run captures.

The compatibility repair changes only Orchestrate's registry implementation: a `file-versions` directory with its companion `file-versions.json` tracked in the same index is an archived capture directory, so it receives no new-record reservation. Ordinary numbered registries remain discovered wherever they sit, including an unmanifested directory named `file-versions` and a registry beside archived captures. No evaluation directory is blanket-excluded. No editorial instruction, frozen criterion, historical record, ADR, existing test assertion or CONTRIBUTING command changes. The generated catalogue follows the changed engine bytes.

The original repository-state regression and a new public `isolate` reservation regression were both [observed failing](red-1.txt) before the implementation changed, then [passed](green-1.txt). The new case includes both Markdown and text captures and keeps ordinary numbered registries on the reservation list. No assertion was weakened or removed.

## Verification

The exact four CONTRIBUTING commands run with HOME and CODEX_HOME unchanged; [environment overrides](environment.json) resolve TMPDIR to this ticket's physical system-temporary scratch and put tool caches there. [Commands, groups, completion codes and elapsed times](gate-processes.json) and all four full outputs are retained. Every unchanged command passed:

| Check | Result |
| --- | --- |
| Ruff | [Pass](gate-1.txt), 0.22 seconds. |
| Formatting | [Pass](gate-2.txt), 7,943 files already formatted, 0.64 seconds. |
| Complete mypy command | [Pass](gate-3.txt), 89 source files, 15.68 seconds including provisioning. |
| Full pytest command | [Pass](gate-4.txt), **2,733 passed in 171.55 seconds**, 173.52 seconds including provisioning. |

The complete suite includes the unchanged source-preservation and native-audit tests. [The amendment boundary check](boundary-check.json) lists every changed pre-existing path. [Cleanup](cleanup.json) records removal of only this amend's working artifacts and completion of its process groups; earlier handoffs and verdict receipts remain deliverables.

The preserved-source inventory and native lifecycle audit remain in the complete suite. No measured Write, checker or judge session is started. The retained source worktree, branch and every existing handoff are untouched. No new defect issue, issue closure, push, release or global installation is performed.

## Existing task disposition

Items 1–5 of the latest Agent Brief retain the independently verified evidence-finalisation outcomes. The local [residual mapping](../residuals.md), false-allegation and standfirst briefs remain reviewable and unpublished; document scope stays parked. Amendment verification concerns item 6 and the imported evidence's interaction with the repository gate. A successful builder gate does not replace the fresh independent verdict or certify later main or full editorial quality.

Raw command outputs retain their emitted whitespace, including pytest failure formatting in the red receipt. They are evidence rather than reformatted prose.
