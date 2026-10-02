# Restored-environment verification — #362

This is an additive continuation of `4d46d138a2fd303f8b6bcd23f916017e9723e90d`. The earlier commits, failed gate receipts, historical evaluations and handoffs remain intact. The [environment repair](environment-repair.json) permits the assigned scratch symlink to resolve to system temporary storage outside the real account's HOME. No product experiment or semantic judgment was repeated.

The four unchanged CONTRIBUTING commands were run in the assigned worktree. `TMPDIR` and tool caches used the scratch directory's physical path; neither HOME nor CODEX_HOME was overridden. [Environment and exact commands](environment.json), [gate process registration/completion](gate-processes.json), [supervisor registration](supervisor.json) and full outputs retain the actual execution.

| Check | Restored-environment result |
| --- | --- |
| `uvx ruff check .` | Pass; [output](gate-1.txt), 1.17 seconds. |
| `uvx ruff format --check .` | Pass; [output](gate-2.txt), 0.52 seconds. |
| Complete CONTRIBUTING mypy command | Pass, 89 source files; [output](gate-3.txt), 5.06 seconds. |
| `uv run --with pytest --with pytest-xdist --with pyyaml pytest -n auto` | **Fail: 2,731 passed, one failed**; [complete output](gate-4.txt), 223.28 seconds including provisioning (pytest: 222.37 seconds). |

The new gate used Python 3.14.8, pytest 9.1.1 and 14 xdist workers. The three scheduler tests that failed in the earlier HOME-local environment now pass. The remaining failure is `tests/test_run.py::test_the_registries_the_engine_finds_are_the_ones_this_repository_keeps`.

That existing repository-state test expects only `docs/adr` to be a numbered registry. The actual detector's documented contract includes any tracked directory containing four-digit-prefixed Markdown filenames. The committed retest contains 90 immutable captured Markdown files with those names in 22 `file-versions` directories. [Registry evidence](registry-evidence.json) enumerates the exact tracked paths. The earlier gate ran before these captures were committed to the index; this continuation tests the committed delivery and exposes their compatibility with the existing registry assertion. No capture was renamed, removed or hidden from the index, and no detector, test, criterion or gate was changed.

**Verification remains blocked.** The latest Agent Brief confines this task to additive evaluator/evidence documentation and requires frozen evidence to remain intact. Choosing how the registry contract or its repository-state test should accommodate immutable captures is outside that brief. No numbered blocker for this compatibility question was supplied, and no new defect issue is authorised here. The run must assign or authorise that work before this ticket can meet its four-check acceptance criterion. This handoff does not infer a narrower gate or a passing verdict.

## Evidence preservation and bounded outcome

[Preservation checks](preservation.json) verify all 630 attributable integrated files against the independent pre-transfer inventory. The repeated read-only [native audit](native-audit.json) is byte-identical to the base receipt: six Write runs, six document-scope diagnostics, seven blind judges, eleven nested comparisons and 30 counted native sessions. Every delivered draft contains the exact prose read by its final comparison. No command targeted the retained source worktree/branch or protected rework source in this continuation.

The measured product remains `fb16908712c4d47a36fc6ee9dfb3eb2714a19e65`, native Codex CLI 0.159.3, `gpt-6.1-sol/xhigh`. Raw variable judgments remain 5/6 passes; article F1 4/6, complete-response F1 2/6, G2 5/6, L1 6/6, and document-scope detection 4/6. Delivery, final-compared prose/residual accounting and unknown-versus-absent each pass 6/6. False allegations, disputed readings, method errors, skips and void attempts retain their original dispositions. No later main or full editorial quality acceptance is certified.

| Latest Agent Brief item | Continuation disposition |
| --- | --- |
| 1. Preserve and integrate attributable evidence | Base delivery retained; all 630 selected bytes reverified. Shared index entries remain in the ticket's run-owned note. |
| 2. Audit artifacts, attempts, judgments and measurements | Base audit retained; read-only native audit returns exactly the same receipt. No historical rejudgment. |
| 3. Publish the narrowed result with omissions and failures | Prior result comment verified unchanged; [follow-on status](result-comment.md) reports the repaired environment and new gate blocker. Its publication receipt is retained beside this file. |
| 4. Durable residual mapping and local briefs; scope question parked | [Mapping](../residuals.md) and both reviewed briefs remain intact and unpublished. Document scope stays parked. |
| 5. No product/history changes or prohibited publication | No fresh trial, judge, product/test repair, issue publication/closure, push, release or installation. |
| 6. Four checks and cleanup receipts | Three checks pass; full pytest fails on the registry assertion. All gate groups ended; [cleanup receipt](cleanup.json) accounts for owned scratch/cache artifacts and retained pre-existing files. Acceptance is incomplete. |

The historical [original-checklist disposition](../../gpt-retest-2026-10-01/acceptance-disposition.md) still applies: omitted Swedish/column, Redline, stop/dependency, chronology/person, technique and baseline coverage is not supplied retrospectively. The retest is a completed measurement; this verification blocker and the residual editorial defects remain unresolved.
