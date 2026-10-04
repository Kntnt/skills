# Gate boundary requiring a decision

All four exact CONTRIBUTING commands ran in the assigned tree. Ruff, formatting and mypy passed. The full `uv run --with pytest --with pytest-xdist --with pyyaml pytest -n auto` completed with **three failures and 2,727 passes**. Its complete log, exit 1 and process receipts remain under `gate/`. No gate command or scope was narrowed.

The failures are these existing tests:

- `tests/test_ms_scheduler.py::test_the_manager_s_two_words_answer_with_the_job`
- `tests/test_ms_scheduler.py::test_under_a_redirected_home_install_writes_the_plist_and_loads_nothing`
- `tests/test_ms_scheduler.py::test_an_install_status_and_disable_under_a_temporary_root_call_no_launchctl`

Each expects a scheduler under its redirected temporary home to remain unloaded. The unmodified `skills/kntnt/library/scripts/integrations.py` function `_real_account` resolves the password database's real account home and checks whether the job directory is under it. Here the real home is `/Users/thomas`. Both authorised writing roots, including the scratch `TMPDIR` used for pytest, are under that home. The fixtures therefore receive `loaded`/`healthy` from their recording stand-in where they expect `not loaded`/`degraded`. No real launchd job was started by those recording stand-ins.

The exact source predicate and failure assertions establish this boundary without a new product trial. [Machine-readable diagnosis](gate-boundary.json) confirms the resolved paths and that every gate process group is gone. This is independent of the additive evidence files; neither the scheduler code nor its tests changed.

Completing #393's all-green gate now requires a decision the brief does not authorise: allow test temporary files outside the two assigned writing roots, or separately scope a correction to the tests' native-account isolation. This builder makes neither choice, changes no product/test, publishes no new defect issue and does not close #393. No numbered dependency is established by this environmental boundary. The completed archived measurement and reviewed residual handoff remain available; the builder task is incomplete on its verification criterion.
