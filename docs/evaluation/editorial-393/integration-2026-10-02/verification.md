# Integration verification

Attempt `ms-20261002-fa0735`; assigned branch `kntnt-orchestrate/main/393`, integration base `5b026028`. The gate is the four commands in the unchanged `CONTRIBUTING.md`, executed in this tree. Tool caches and temporary roots are confined to the assigned scratch directory; the commands themselves are neither narrowed nor replaced. Complete outputs, command strings, exit codes and process-group identities are retained in `gate/`. Ruff, formatting and mypy passed. Pytest failed three scheduler tests with 2,727 passes. The task has not met its required all-green gate; `gate-boundary.md` explains the path/account conflict.

The source-integration check was observed failing before import: all 1,127 required source files were absent. The protected-history check passed. After the byte-exact import, both checks passed. Its history comparison was made faster by using a tracked Git diff, and source blobs are now checked in one tree listing; the observable requirements stay the same. No product fixture or product test is added for this documentation-only change.

The offline packet audit independently verifies supplied bytes, artifact transport, native identities/lifecycles, excerpt overreads, retained copy digests and count accounting. It runs no product Harness and makes no semantic verdict. Its procedure and output are retained beside the machine-readable receipt. Original source validation and cleanup receipts are preserved byte for byte; they do not substitute for this integration's gate.

The records index and changelog remain untouched in this builder tree. The exact additive index block is in `.kntnt-orchestrate/393.md` for the run to append while preserving siblings. The run's later integrated-branch verification remains required.

Cleanup is recorded in `cleanup.json`: every gate process/group is waited to completion, owned temporary cache/scratch material is removed using the literal assigned path, and the original evidence worktree/branch and all deliverables remain. No process is deliberately left running.
