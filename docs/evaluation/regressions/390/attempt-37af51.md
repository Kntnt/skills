# Heading pairs: mechanical evidence and a blocked native run

Attempt `ms-20260922-37af51`, 2026-09-22, for [#390](https://github.com/Kntnt/skills/issues/390). **The native behavioral acceptance criteria are unverified.** Codex could not reach its service, and no editorial turn completed. This packet records that limitation rather than claiming that lexical measurements demonstrate semantic judgment.

The [plan](plan.md), [fixture hashes](fixtures.sha256.json) and [exact task material](tasks/) were fixed before the native attempt. The recorded Swedish input is a byte copy of [#386's Write delivery](../../editorial-386/runs/column-sv/write/delivered.md); its [judgment A](../../editorial-386/runs/column-sv/write/judgement-a.md), [judgment B](../../editorial-386/runs/column-sv/write/judgement-b.md) and [Redline repair](../../editorial-386/runs/column-sv/redline/delivered.md) remain historical evidence. No #382 baseline was sought or reconstructed.

## Native outcome

The first planned run used Codex CLI 0.155.1 with the installed configuration's `gpt-5.6-sol`, `xhigh`, default service tier, in a private staged workspace. [process.json](runs/recorded-column/process.json) records the exact argv, process group, timeout and exit status; [invocation.txt](runs/recorded-column/invocation.txt) and [harness-context.md](runs/recorded-column/harness-context.md) preserve the turn and workspace instructions. The [instruction inventory](runs/recorded-column/instruction-digests.json) identifies the staged working-tree product based on `0cb71523`.

[Native events](runs/recorded-column/events.jsonl), [stderr](runs/recorded-column/stderr.txt) and the [native session record](runs/recorded-column/native/) show DNS failure reaching `chatgpt.com`, retries, and fallback from WebSockets to HTTPS. The runner terminated and reaped process group 36719 after 45 seconds, exit `-15`. No response artifact or correction agent was produced. [Before](runs/recorded-column/before.json) and [after](runs/recorded-column/after.json) inventories of staged work and private temporary storage are identical. Private Codex runtime state was outside those two inventories; its retained native session is linked above. These inventories do not establish an unrestricted whole-machine filesystem claim.

| Planned run | Outcome |
| --- | --- |
| Recorded column / Redline | Startup blocked; all six native criteria unexercised |
| Paraphrased column / Redline | Not started after the shared network obstacle |
| Legitimate reuse / Redline | Not started after the shared network obstacle |
| Paraphrased headline / Redline | Not started after the shared network obstacle |
| Column source / Write | Not started after the shared network obstacle |

The four [input pair measurements](pairs/) are actual CLI output. They preserve the full text and overlap for the frozen semantic cases; they are not editorial findings. No post-run pair measurements exist because no native draft or correction was returned. The [startup runner](harness/attempt.py) preserves the bounded invocation used here; it expects the private staging described in the plan and process record, which is removed during cleanup.

## Mechanical verification

Tests use the anatomy script's public CLI/JSON boundary. The observed red/green sequence is preserved:

| Slice | Red | Green |
| --- | --- | --- |
| Full pairs and unjudged overlap | [Missing `heading_pairs`](checks/red-1.txt) | [1 passed](checks/green-1.txt) |
| First-sentence closing marks | [Two missing closers](checks/red-2.txt) | [7 passed](checks/green-2.txt) |
| No borrowed prose across headings | [Missing nested-heading pair](checks/red-3.txt) | [41 passed](checks/green-3.txt) |
| Unpairable first paragraph | [Empty/punctuation-only text treated as a sentence](checks/red-4.txt) | [2 passed](checks/green-4.txt) |

The final [focused suite](checks/mechanical.txt) passes **48 tests**, including Unicode NFC/casefold normalization, punctuation, deduplicated tokens, absent members, documented sentence-boundary ambiguity, stable positional identities, full standfirst text, equivalent Markdown/HTML/WordPress evidence, and the pre-existing structural/verdict checks. Added tests that already passed exercised existing parsing and the earlier slices; no production change was made to satisfy them.

Commands used for these focused runs were `uv run --offline --no-project --with pytest pytest -q -p no:cacheprovider tests/test_article_anatomy.py`, with the slice selected by `-k heading_pairs`, `-k first_sentence`, `-k each_subheading`, or `-k unpairable` where shown in the logs. `TMPDIR` and `UV_CACHE_DIR` pointed inside `.scratch-390/` in this working tree. Required cached packages were copied into that private cache because the sandbox denied network access and writes to global tool state.

The four CONTRIBUTING checks were run to completion. Their [commands and initial process outcomes](checks/verification.json) are retained, including initial tooling misses and a scratch-helper formatting failure, both resolved before the final checks:

| Check | Final outcome |
| --- | --- |
| `uvx ruff check .` | [Pass](checks/ruff-final.txt) |
| `uvx ruff format --check .` | [Pass](checks/format-final.txt) |
| Published mypy command | [Pass, 71 source files](checks/mypy-complete.txt) |
| `uv run --with pytest --with pytest-xdist --with pyyaml pytest -n auto` | [2,050 passed; 9 failed; 83 errors](checks/pytest.txt) |

The full-suite failure is not a green gate. All 83 errors are HTTP-fixture socket binds denied with `PermissionError: [Errno 1] Operation not permitted`. The nine failures are in session cleanup and scheduler tests, outside the changed paths. A source export of unchanged `HEAD` (`0cb71523`, no new branch or worktree) reproduces all nine failures and one representative socket error: [baseline command](checks/baseline-command.json), [outcome](checks/baseline.txt), [process record](checks/baseline-process.json). This establishes that those outcomes also occur without #390's changes; it does not claim that every underlying cause was diagnosed.

The Catalog was regenerated using `KNTNT_SOURCE=. uv run skills/kntnt/scripts/kntnt.py catalog --write`. No historical decision record, headline editorial standard, or #389 acceptance/rollback policy was changed. The reserved changelog and regression-index entries are supplied through `.kntnt-orchestrate/390.md`.

## Remaining work

Run the frozen native cases where Codex can reach its service and retain completed parent/correction/source-check traces, delivered artifacts, paired output, filesystem inventories and semantic judgments. The packet currently cannot establish recognition of echoes, restraint on legitimate reuse, actual resource-loading behavior or the order of a completed Write source check. Run the full gate in an environment that supports its local servers and process inspection. These remain acceptance work, not waived criteria.

The builder could not stage or commit: `git add` failed because the sandbox denied creation of `/Users/thomas/Projects/skills/.git/worktrees/skills-388-391/index.lock`. [The exact staging command and refusal](checks/commit.txt) are retained. The implementation and this packet therefore remain working-tree changes, not a completed ticket or a committed delivery.

## Process and scratch account

The native process group, four-check runner, baseline test runner, package-cache copy and later mypy invocation were all waited to completion or explicitly terminated and reaped. No process was deliberately left running. The private `.scratch-390/` tree, including the copied authentication, staged install, source export and tool caches, is removed after evidence capture; pre-existing repository caches are retained.

One early discovery command cannot be certified as finished: `ls /Users/thomas/.cache/uv && du -sh /Users/thomas/.cache/uv && command -v pytest || true && rg --files --hidden /Users/thomas/.cache/uv/environments-v2 /Users/thomas/.local/share/uv/tools 2>/dev/null | rg '/(pytest|ruff|mypy|pyvenv.cfg)$' | head -35 && git status --short`. Its tool call yielded after printing the initial directory names, and an output-only wrapper discarded the returned session identifier. Subsequent `ps` and `pgrep` process inspection was denied by the environment, so the builder could neither establish its PID nor certify termination. This is a process-accounting gap, not a process intentionally retained for the next session.
