# Tracked native artifacts meet the numbered-registry detector

The restored environment clears the initial three scheduler-test failures. The unchanged full gate nevertheless returns one failure and 2,729 passes:

`tests/test_run.py::test_the_registries_the_engine_finds_are_the_ones_this_repository_keeps`

The test expects Orchestrate's `numbered_registries(REPO_ROOT)` to return only `docs/adr`. The shipped detector in `skills/code/orchestrate/scripts/run.py` matches every tracked basename with `RECORD_NAME = re.compile(r"^(\d{4})-")` and groups them by parent directory, wherever they sit in the repository. The retained native packet contains such names, including `runs/r01/file-versions/0000-8821f2ea42f7.md`. The detector therefore returns `docs/adr` plus 29 packet `file-versions` directories. [Machine-readable diagnosis](gate-boundary.json) retains all actual directories and matching Markdown artifacts; the full pytest failure is in [the gate log](gate/pytest.txt).

The continuation base already commits these artifacts. The initial gate predates that additive evidence commit, and its results cannot certify the current tracked-import state. This is a deterministic interaction between the retained packet and the tracked-file detector, rather than the repaired home-location condition. The detector and its test are unchanged; the packet still matches source head `4e88c6e0` byte for byte.

The latest Agent Brief requires both immutable historical/native evidence and an all-green project gate, while excluding product/test changes. Meeting both now needs a separately scoped decision about registry detection, its repository assertion and the treatment of native file-version evidence. This builder chooses none of those designs, does not rename evidence, and does not drop the failing test. No existing numbered blocker has been established. No new defect issue is filed or product trial run.

All four exact commands were run to completion; ruff, format and mypy passed, pytest exited 1, and every owned runner/gate process group is absent. Earlier failed receipts remain untouched. The archived measurement and residual handoff remain available, but #393's builder verification criterion is unmet and closure stays pending.
