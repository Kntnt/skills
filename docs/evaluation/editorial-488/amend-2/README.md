# Amend 2: the original checker-input blocker remains

Attempt `ms-20261002-689dc4`, starting at
`9e7817803178831149945ebd8dfb3c1069e0c3cb`.
This amend does not establish acceptance criterion 5 and does not claim a
successful repair. It adds a fresh diagnostic and project-gate handoff.

## The whole defect surface

[checked-input-probe.txt](checked-input-probe.txt) independently rereads the
original parent dispatch and child receipt for **all 18 counted runs**, verifies
their hashes against the earlier recovery audit, and checks for a complete
plaintext filled checker instruction at that actual boundary. The observed
[diagnostic failure](checked-input-probe.log) is exit 1:
zero original checker inputs are readable. The child's encrypted block matches
the parent's encrypted dispatch in every run. The per-run source addresses and
hashes are in [checked-input-receipt.json](checked-input-receipt.json).

The ten separate recovered drafts remain useful observations but cannot be
independently matched to the actual dispatched instruction. Eight runs still
lack even that separate complete draft. This is the same defect class across
every counted packet, not only the eight missing-draft packets. Completed
checker returns, their partial quotations and terminal replies establish no
complete original input. No draft is reconstructed from those outputs.

The previous [whole-surface recovery audit](../amend-1/recovery-audit.json) and
its limits remain intact. The assigned scratch contains the verifier's handoff
receipts and gate artifacts, not additional original native checker inputs.
[preserved-starting-tree.json](preserved-starting-tree.json) identifies every
ticket-owned file at the starting head; all remain byte-identical after this
amend. Original native packets, voids, judgements, frozen plan, scores, ADR-0239,
product and tests are unchanged.

## The decision this session cannot make

Criterion 5 requires complete original checked-input/return/delivery proof;
the plan's `skipped` outcome and honest disclosure cannot waive it. The
[frozen plan](../plan.md) says missing trace details are disclosed, forbids
repeating completed arms for a better score, and provides a prospective revise
round in its reproduction branch. Its non-reproduction branch completes both
unchanged-product arms, which have already completed. Its final sentence says
to report a missing provider capability or a genuine requirement decision as
blocked. The [protocol](../../protocol.md) also preserves completed evidence
and limits revise rounds.

The unresolved decision is whether a prospective campaign with a settled
method for preserving the **actual full checker input** may supply criterion
5's missing proof despite these completed frozen arms, and what method is
acceptable without changing the product, the checker instruction, its one-shot
execution or the checked reply. No such substitution or capture method is
settled by the ticket thread. An extra directive to a checker would conflict
with its shipped instruction to receive only the filled brief and return only
two lists. A draft snapshot alone would repeat the existing evidence gap.

This session stops at that decision under the unattended brief. It does not
start another campaign, resume an old run to recover a prompt from memory,
change a historical outcome, or speculate about a product repair when the
fresh baseline did not reproduce the terminal-delivery defect. The requirement
remains unmet; this diagnostic has no green repair result.

## Project gate and cleanup

All four commands from the unchanged CONTRIBUTING.md ran in this worktree,
with caches and temporary roots confined to the resolved assigned scratch.
HOME and CODEX_HOME are retained. Exact commands, exits and environment are in
[gate-receipt.json](gate-receipt.json); complete logs are `gate-1.log` through
`gate-4.log`. Ruff lint, Ruff formatting and mypy (89 source files) passed;
pytest passed all 2,733 tests in 166.52 seconds. These project checks do not
establish criterion 5.

The gate supervisor and command groups were registered immediately, awaited
and audited after completion. Only this amend's runtime directory was removed
by its full literal path; previous handoff deliverables are retained. The
[process audit](process-audit.json) found no surviving owned process.
The [cleanup receipt](cleanup-receipt.json) confirms runtime removal, byte
preservation of all 1,702 original ticket files and all 19 starting scratch
handoff files. Registration receipts remain beside this document.
No shipped file changes, so catalog regeneration is not due. The shared
changelog and record index are untouched; no new entry is needed.
