# Heading-pair evidence — implementation, incomplete acceptance

For [#390](https://github.com/Kntnt/skills/issues/390). The working-tree
implementation exposes unjudged heading pairs and lexical overlap and makes
Write, Redline and fresh correction agents judge semantic repetition. **This
packet does not establish native behavioral acceptance or a passing full gate.**

The initial attempt, `ms-20260922-37af51`, is preserved in
[its original report](attempt-37af51.md), including four observed red/green
cycles, 48 passing mechanical tests and a native startup blocked by network
restrictions. Its [frozen plan](plan.md), [fixture hashes](fixtures.sha256.json),
[tasks](tasks/) and [input pair evidence](pairs/) remain unchanged. No #382
baseline was sought. The recorded echo is the preserved #386 column.

## Retry `ms-20260922-59e6c1`

The [retry plan](retry-plan.md) was written before execution. The inherited
implementation was inspected, without changing its product code or instructions.
The Catalog was regenerated. Native attempts used Codex CLI 0.155.1,
`gpt-5.6-sol`, `xhigh`, default service tier and separate staged installations.
Each directory below preserves exact argv, invocation, instruction inventory,
native parent trace, event stream, stderr and before/after workspace inventories:

| Frozen case | Retry evidence | Outcome |
| --- | --- | --- |
| Recorded Swedish echo | [recorded-column](retry-59e6c1/recorded-column/) | Interrupted during setup; no delivered artifact or correction agent |
| Paraphrased Swedish echo | [paraphrased-column](retry-59e6c1/paraphrased-column/) | Interrupted during setup; no delivered artifact or correction agent |
| Legitimate names/topic reuse | [clean-reuse](retry-59e6c1/clean-reuse/) | Interrupted during setup; no delivered artifact or correction agent |
| Paraphrased headline | Original frozen task only | Not started |
| Write column | Original frozen task only | Not started |

Service access succeeded. The builder then terminated and reaped all three
native process groups after the paraphrased-column agent created temporary
directories outside its assigned area. Its event stream records creation and
removal of `/tmp/redline-invoke.ctsIPR` and `/tmp/redline-language.BjYBuf`.
These effects violated the supplied workspace constraint; they are not hidden
by the inventories, which cover only each run's `work/` and `tmp/` directories.
The interruption records explain the stop. No completed editorial outcome is
claimed, and no post-delivery pair evidence exists.

The planned restart with an enforced writable-path boundary was not launched:
the full gate exposed the independent constraint below. None of the frozen
semantic criteria was changed or waived. Recognition of the recorded and
paraphrased echoes, restraint on legitimate reuse, correction-agent evidence
consumption, actual bounded resource loading and Write's final source-check
ordering remain unverified.

## Mechanical checks and the blocking constraint

The anatomy CLI/JSON [focused suite](retry-59e6c1/checks/mechanical.txt) again
passes **48 tests**. It covers full pairs, stable positional identity, Unicode
normalization, punctuation, repeated tokens, missing/unpairable members,
sentence-boundary ambiguity, equivalent Markdown/HTML evidence and unchanged
structural/verdict semantics. These are measurements, not semantic judgments.

The four published commands were run to completion; their commands, process
groups, exit statuses and durations are in
[processes.json](retry-59e6c1/checks/processes.json).

| Check | Result |
| --- | --- |
| `uvx ruff check .` | [Pass](retry-59e6c1/checks/ruff.txt) |
| `uvx ruff format --check .` | [Pass after formatting the new evidence runner](retry-59e6c1/checks/format-final.txt) |
| Published mypy command | [Pass, 71 source files](retry-59e6c1/checks/mypy.txt) |
| Published full pytest command | [2,139 passed, three failed](retry-59e6c1/checks/pytest.txt) |

The three failures are the scheduler tests
`test_the_manager_s_two_words_answer_with_the_job`,
`test_under_a_redirected_home_install_writes_the_plist_and_loads_nothing`, and
`test_an_install_status_and_disable_under_a_temporary_root_call_no_launchctl`.
A source export of unchanged `HEAD` (`0cb71523`, no new branch or worktree)
[reproduces all three](retry-59e6c1/checks/baseline.txt), using
[the recorded command](retry-59e6c1/checks/baseline-command.json).

The cause is the execution location. The scheduler's `_real_account()` in
`skills/kntnt/library/scripts/integrations.py` recognizes every descendant of
the password database's home, `/Users/thomas`, as a real-account path. These
three tests expect their temporary roots to be outside that home. Both write
roots authorized for this task are inside it, so the stand-in scheduler is
loaded where the assertions expect it not to be. `TMPDIR` was deliberately
inside the assigned scratch directory. Changing `HOME` cannot resolve this
gate, which reads the password database rather than that environment variable.

**Decision needed:** permit test temporary storage outside `/Users/thomas`, or
separately authorize making the scheduler tests independent of their temporary
directory's location. This ticket changes neither the scheduler nor its tests.
The builder stopped at this constraint rather than choosing a wider scope or
writing outside the permitted roots. Three passing gates and a baseline
reproduction do not satisfy the four-check acceptance criterion.

The check wrapper raised a bookkeeping `zip(strict=True)` exception after all
four commands had finished because its CONTRIBUTING extraction also found the
optional validator commands. Their actual completed results above are retained;
no gate was left running or omitted because of that wrapper error. The Catalog
[regeneration log](retry-59e6c1/checks/catalog.txt) is retained separately.

## Delivery and cleanup

The implementation, tests, instruction/documentation sweep and this packet are
committed together, with the reserved changelog and index entries in
`.kntnt-orchestrate/390.md`. The ticket remains incomplete for the reasons above.

All processes started by this retry were terminated and reaped or waited to
completion, including native processes, wrappers, the full suite and the
baseline reproduction. Nothing is deliberately left running. The retry's
staged installs, credential copies, private runtime state, caches, test temporary
files and source export are removed from its assigned scratch directory after
evidence capture. Its packet and the inherited orchestration logs are retained.
The saved workspace inventories show no supplied input or staged instruction
changed; each records one added uv lock file before the builder's final cleanup.
