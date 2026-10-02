# Verification of the additive delivery

The original retest's historical checks remain untouched in `gpt-retest-2026-10-01/validation/`. These receipts belong to the evidence-finalisation branch, based on `5b026028`, not to a new product evaluation.

## Observed red and green

The public evidence-file boundary is the independently captured pre-transfer inventory. `tests/test_editorial_362_evidence.py` first failed on the missing packet README before any evidence was copied ([red receipt](red.txt)). After the smallest delivery operation—copying the 630 attributable files without changing their bytes—that preservation check passed.

The public native-audit command then failed on the first two runs' differently named explicit preservation flag ([second red receipt](audit-red.txt)). Supporting both retained receipt spellings, rather than changing the historical receipts, made both tests pass ([green receipt](green.txt)). The native audit checks positive completion and seat evidence, the frozen six-plus-six matrix, seven judges, eleven children, every captured-file digest, and actual final-checker output containing exactly the delivered prose. Neither test rejudges semantic outcomes or requires a canonical sentence.

## Unchanged project gate

The exact four commands were read from this worktree's CONTRIBUTING.md. `gate-processes.json` records their complete argv, cwd, owned process groups, start/completion, exit statuses and durations; `gate-1.txt` through `gate-4.txt` retain full output. All four were run, with no dropped command, narrowed test selection or substitute gate. The initial attempt and its receipts remain separately as `first-gate-*`.

The first Ruff check found import formatting, an explicit `check=False` omission and the new audit command's missing executable bit. Only the two new Python files and the new audit file's mode were corrected. No imported evaluator source, frozen evidence, product, fixture or criterion was edited. The final Ruff check, format check and complete CONTRIBUTING mypy invocation pass. The full suite result is retained verbatim in `gate-4.txt`; acceptance remains blocked on the three scheduler failures described below.

The environment confined temporary writes to the two authorised roots: `UV_CACHE_DIR`, `UV_TOOL_DIR`, `UV_PYTHON_INSTALL_DIR`, `XDG_CACHE_HOME` and `TMPDIR` all point under `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/362.scratch`. `PYTHONDONTWRITEBYTECODE=1` prevents additional bytecode artifacts. No HOME or CODEX_HOME override, test exclusion, fixture patch or injected fake password database was used. The command remains `uv run --with pytest --with pytest-xdist --with pyyaml pytest -n auto`.

## Decision preventing acceptance

Both full-suite attempts passed 2,729 tests and failed these three existing tests in `tests/test_ms_scheduler.py`. The final attempt took 126.30 seconds; Ruff, format and mypy all passed after the new-file formatting corrections:

- `test_the_manager_s_two_words_answer_with_the_job`
- `test_under_a_redirected_home_install_writes_the_plist_and_loads_nothing`
- `test_an_install_status_and_disable_under_a_temporary_root_call_no_launchctl`

Their temporary-root expectations require the scheduler to classify the fixture root as outside the real user's home. `skills/kntnt/library/scripts/integrations.py`'s `_real_account` reads `pwd.getpwuid(os.getuid()).pw_dir`, resolves both paths and checks `is_relative_to`. The permitted scratch root is inside `/Users/thomas`, so its fixture roots are inside the real account. The recording stand-in launchctl consequently sees a loaded/healthy job instead of the expected not-loaded/degraded result. This is a direct environment/fixture incompatibility, not evidence of a retest product defect. The tests provide a stand-in; no actual launchd job was installed.

Writing pytest roots in the normal system temporary directory would cross the explicit write boundary. Changing the tests or masking the actual-account lookup would be an unrelated fixture/criteria change. No such choice was inferred in this unattended task. The run must authorise an outside-home temporary location or settle fixture isolation before the gate can pass. No new issue is published for this conflict, and no issue closure is authorised by an incomplete verification.

No fresh product trial or semantic judge ran. There is no catalogue regeneration because no file under `skills/` changed. The shared index entry is committed only as `.kntnt-orchestrate/362.md` for the run to append, retaining every sibling.
