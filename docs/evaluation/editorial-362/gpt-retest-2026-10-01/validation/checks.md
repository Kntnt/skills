# Repository validation

The product revision remained fb16908712c4d47a36fc6ee9dfb3eb2714a19e65. These are the four required checks from CONTRIBUTING.md, run in the isolated evaluation worktree; no shipped file changed.

| Check | Outcome | Observed output |
| --- | --- | --- |
| `uvx ruff check .` | pass | All checks passed. |
| `uvx ruff format --check .` | pass | 6 734 files already formatted. |
| CONTRIBUTING.md's full mypy command | pass | Success: no issues found in 88 source files. |
| `uv run --with pytest --with pytest-xdist --with pyyaml pytest -n auto` | pass | 2 725 passed in 122.74 seconds. |

The exact pytest command, owned process group and working directory are in pytest-process.json; complete pytest output is in pytest.txt. Evaluator helpers added or modified afterwards receive their own Ruff checks; no product or test behaviour changes after these checks.

Final whole-worktree Ruff check and format check after completing the evaluator helpers and native evidence also pass: “All checks passed!” and “6854 files already formatted”. Testing-created local environment/cache files are removed during final cleanup; they are not product changes or deliverables.
