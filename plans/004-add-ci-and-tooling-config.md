# Plan 004: Enforce the verification baseline in CI and pin the linter and type checker

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Prerequisite**: plans 001, 002, and 003 must have landed, and the suite must
> be fully green. This plan makes a red suite block every future pull request,
> so it must not land while any test is expected to fail. Step 1 checks this.
>
> **Drift check (run first)**: `git diff --stat 5978324..HEAD`
> This plan creates new files and does not depend on the contents of any
> existing one except `.gitignore`. Confirm `.gitignore` still contains the
> lines quoted in "Current state"; on a mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: `plans/001-characterize-version-bump.md`, `plans/002-unify-version-detection-and-writing.md`, `plans/003-parse-porcelain-with-nul-separators.md`
- **Category**: dx
- **Planned at**: commit `5978324`, 2026-08-17

## Why this matters

Everything needed to verify this repository already works. At commit `5978324`: `uv run --with pytest pytest` → 77 passed, `ruff check` → clean, `ruff format --check` → clean, `mypy --strict` on both engines → clean. Nothing runs any of it automatically. There is no `.github/` directory at all.

Two consequences, both concrete:

1. The repository's own coding standard mandates the tooling that is missing. `docs/coding-standard/general.md:180` — "**GitHub Actions** for continuous integration." `docs/coding-standard/python.md:44-49` — ruff as the single linter and formatter, mypy or pyright with "Strict mode on new code". Neither the CI nor the configuration exists, so the standard is aspirational where it should be mechanical.
2. `tests/test_kntnt.py` contains `test_shipped_catalog_matches_the_generated_one` — the only guard against a `catalog.json` that lies about what the collection ships. Every user's `/kntnt status`, Enable picker, and `help <skill>` read that file. It runs when someone remembers to run it.

`CONTRIBUTING.md:26-30` tells a contributor to run one command, `uv run --with pytest pytest`, and says nothing about ruff or mypy — so a contributor who follows the documented process submits work the maintainer then has to lint by hand.

After this plan, a push or pull request runs the full gate, and ruff and mypy read their settings from a checked-in file instead of from each invoker's defaults.

## Current state

### What exists

- `tests/test_kntnt.py` (50 tests) and `tests/test_ship.py` (27 tests at `5978324`; 34 after plans 001–003) — pytest, driven through each script's CLI with `uv run`.
- `skills/kntnt/scripts/kntnt.py` and `skills/code/commit/scripts/ship.py` — the two engines, both PEP 723 single-file scripts with `dependencies = []`.
- `tests/support/fake_skills.py` — a PEP 723 test double for the `npx skills` transport.
- `docs/coding-standard/general.md` and `docs/coding-standard/python.md` — the mandates quoted above.
- `.gitignore` — already ignores the caches these tools create:
  ```
  .pytest_cache/
  .mypy_cache/
  .ruff_cache/
  .coverage
  ```

### What does not exist

- `.github/` — verified absent: `ls -la .github` → `No such file or directory`.
- Any `pyproject.toml`, `setup.cfg`, `ruff.toml`, `mypy.ini`, or `.mypy.ini` at any level. Confirm with `find . -name 'pyproject.toml' -o -name 'ruff.toml' -o -name 'mypy.ini' | grep -v '\.git/'` → no output.

### The commands that must be enforced, verified at `5978324`

| Command | Result |
|---|---|
| `uv run --with pytest pytest` | `77 passed` |
| `uvx ruff check .` | `All checks passed!` |
| `uvx ruff format --check .` | `61 files already formatted` |
| `uvx mypy --strict skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py` | `Success: no issues found in 2 source files` |

The ruff version in use when these were run was 0.16.3 (visible from the `.ruff_cache/0.16.3/` directory).

### A constraint specific to this repository

**The `pyproject.toml` you create must not contain a `[project]` table with a `version` key.** `ship.py`'s `detect_versions` treats a `pyproject.toml` version as a release-bump target (`skills/code/commit/scripts/ship.py:386-389`), so adding one would make this repository's own `/release` start rewriting it. This repository's version lives in git tags and `CHANGELOG.md` and nowhere else — `detect_versions` currently finds nothing here, and `plan release` derives the version from `last_tag` (`ship.py:339-341`). Keep it that way: a tool-configuration-only `pyproject.toml` has no `[project]` table at all.

### Conventions

- Markdown prose in this repository keeps **each paragraph on a single physical line** — no hard wrapping at a column width. Every file in `docs/` and the repository root does this. Match it in any prose you write.
- YAML: two-space indentation, no document start marker (`---`). There is no existing workflow to copy, so follow GitHub's own documented style.
- The repository is `Kntnt/skills` on GitHub (`README.md:3-4`), Apache 2.0, default branch `main`.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Full suite | `uv run --with pytest pytest -q` | `84 passed` with plans 001–003 landed; `87 passed` if 005 landed too |
| Lint | `uvx ruff check .` | `All checks passed!` |
| Format | `uvx ruff format --check .` | exit 0 |
| Types | `uvx mypy --strict skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py` | `Success: no issues found in 2 source files` |
| Workflow syntax | `uvx --from check-jsonschema check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/ci.yml` | `ok -- validation done` |

If `check-jsonschema` cannot be fetched in your environment, skip that check and say so in your report — it is a convenience, not a gate.

## Scope

**In scope** (create these; none exist today):

- `.github/workflows/ci.yml`
- `pyproject.toml` (repository root, tool configuration only)

**Out of scope** (do NOT touch):

- `CONTRIBUTING.md` — `plans/006-fix-contributing-doc-errors.md` owns every edit to that file, including documenting these commands. Two plans editing one file is a merge conflict for no reason.
- Any file under `skills/` or `tests/` — this plan adds enforcement, not fixes. If CI surfaces a failure, that is a STOP condition, not a licence to edit the code.
- `.gitignore` — it already covers all three tool caches. Verify, do not extend.
- `docs/coding-standard/*.md` — these are the mandate this plan satisfies; they need no change.
- Release automation, publishing, or any workflow that writes: no `permissions: write`, no tag or release steps, no `gh` calls. This repository releases through its own `/release` skill, deliberately (`skills/code/release/SKILL.md`). CI here only verifies.
- Dependabot, CodeQL, coverage reporting, matrix builds across operating systems. All defensible, none asked for; adding them makes this plan unreviewable.
- `CHANGELOG.md` — do not add an entry by hand; this repository's `commit` skill reconciles it at commit time.

## Git workflow

- Branch: `advisor/004-ci-and-tooling-config`
- One commit — one concern (`CONTRIBUTING.md:24`).
- Commit messages: imperative, sentence case, no conventional-commit prefix (`git log`: `Add the kntnt manager skill.`). Suggested: `Run the tests, linter, and type checker in CI`.
- Do NOT push, open a PR, or run this repository's own `/commit`, `/push`, or `/release` skills unless the operator instructed it.

## Steps

### Step 1: Confirm the suite is green before you make it a gate

**Verify**, all four:

1. `uv run --with pytest pytest -q` → `0 failed`, and at least `84 passed`. Write the count down; step 3 and step 5 compare against it. Expect `84` with plans 001–003 landed, or `87` if plan 005 landed as well — 005 is independent and may go in any order.
2. `uvx ruff check .` → `All checks passed!`
3. `uvx ruff format --check .` → exit 0
4. `uvx mypy --strict skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py` → `Success: no issues found in 2 source files`

If the count is below `84`, plans 001–003 have not all landed and this plan is premature — STOP. If any command fails, STOP: landing CI over a red baseline blocks every subsequent pull request.

### Step 2: Confirm nothing already configures these tools

**Verify**: `find . -path ./.git -prune -o \( -name 'pyproject.toml' -o -name 'ruff.toml' -o -name '.ruff.toml' -o -name 'mypy.ini' -o -name '.mypy.ini' -o -name 'setup.cfg' \) -print` → no output.

Any hit means a configuration already exists and this plan's assumptions are wrong — STOP and report what you found.

### Step 3: Create the tool configuration

Create `pyproject.toml` at the repository root, with tool sections only and **no `[project]` table** — see the constraint in "Current state".

```toml
# Tool configuration only. This repository ships PEP 723 single-file scripts,
# not a distributable package, so there is deliberately no [project] table: a
# version key here would make this project's own /release skill start bumping
# it (see skills/code/commit/scripts/ship.py, detect_versions).

[tool.ruff]
target-version = "py312"

[tool.mypy]
python_version = "3.12"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Rationale for each key, so a reviewer can check the intent rather than the taste:

- `target-version = "py312"` — matches the `requires-python = ">=3.12"` in every script's PEP 723 header (`skills/kntnt/scripts/kntnt.py:2`, `skills/code/commit/scripts/ship.py:2`). Without it, ruff infers a target and the inference can change between versions.
- `strict = true` under `[tool.mypy]` — `docs/coding-standard/python.md:48`: "**mypy** or **pyright** for static type checking — pick one per project. Strict mode on new code." Putting it in the file means `uvx mypy <paths>` is strict without anyone remembering the flag.
- `python_version = "3.12"` — same reason as ruff's target.
- `testpaths = ["tests"]` — makes a bare `pytest` collect the same set CI collects.

Do **not** add `[tool.ruff.lint]` rule selections in this plan. Ruff's default rule set is what produced today's clean run; selecting more rules would surface new findings and turn a tooling plan into a code-change plan.

This exact file was tried against a throwaway copy of the repository at commit `5978324` before this plan was written: `ruff check` → `All checks passed!`, `ruff format --check` → `61 files already formatted`, bare `uvx mypy <the two engines>` → `Success: no issues found in 2 source files`, and pytest collected all tests. So the expected results below are observed, not predicted. The only difference you should see is the test count, which is higher once plans 001 and 003 have added theirs.

**Verify**:

1. `uvx ruff check .` → `All checks passed!`
2. `uvx ruff format --check .` → exit 0
3. `uvx mypy skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py` → `Success: no issues found in 2 source files` — note **no `--strict` flag**; the config now supplies it. If this reports errors that `--strict` did not, STOP and report them; `strict = true` in config should be equivalent.
4. `uv run --with pytest pytest -q` → step 1's count, `0 failed`
5. `uv run --with pytest pytest -q --collect-only 2>&1 | tail -1` → reports step 1's count of tests collected

### Step 4: Create the CI workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Install uv
        uses: astral-sh/setup-uv@v7
        with:
          enable-cache: true

      - name: Lint
        run: uvx ruff check .

      - name: Check formatting
        run: uvx ruff format --check .

      - name: Type-check
        run: uvx mypy skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py

      - name: Test
        run: uv run --with pytest pytest -q
```

Points a reviewer should be able to confirm at a glance:

- `permissions: contents: read` — the workflow only reads. Nothing here needs write access, and the default token permissions are broader than needed.
- Steps are ordered cheapest-first: lint and format fail in seconds, tests take about ten. A contributor with a formatting slip learns it before waiting on the suite.
- One job, one runner, no matrix. Every script pins `requires-python = ">=3.12"` and `uv` provisions the interpreter itself, so there is nothing to matrix over until the project supports a range it actually tests.
- `mypy` runs without `--strict` because step 3 put `strict = true` in `pyproject.toml`. The two must not both carry the setting.
- The tests shell out to real `git` and create throwaway repositories; `ubuntu-latest` ships git, so no extra install step is needed. `tests/test_ship.py:14-20` scrubs inherited `GIT_*` variables and sets its own author identity, so CI needs no `git config` step either.

If the action versions above are not the current majors when you run this, use the current major and say which you used in your report. Do not pin to a commit SHA — this repository has no such convention.

**Verify**:

1. `test -f .github/workflows/ci.yml && echo present` → `present`
2. `uvx --from check-jsonschema check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/ci.yml` → `ok -- validation done`. If `check-jsonschema` cannot be fetched, run `uv run --with pyyaml python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/ci.yml'))" && echo "yaml ok"` → `yaml ok`, and note the substitution.
3. `grep -c "permissions:" .github/workflows/ci.yml` → `1`

### Step 5: Run the CI steps locally, in the workflow's order

Run exactly what the workflow runs, in the same sequence, and confirm each exits 0.

```sh
uvx ruff check .
uvx ruff format --check .
uvx mypy skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py
uv run --with pytest pytest -q
```

**Verify**: all four exit 0; the last reports step 1's count and `0 failed`.

### Step 6: Confirm the working tree holds only the two new files

**Verify**:

1. `git status --porcelain` → exactly two lines, both `??`: `.github/` (or `.github/workflows/ci.yml`) and `pyproject.toml`
2. `git diff --stat` → empty. This plan modifies no tracked file.
3. `git status --porcelain --ignored | grep -E '\.(ruff|mypy|pytest)_cache'` → the caches appear as ignored, not untracked. If any shows as `??`, `.gitignore` is not covering it — report that rather than editing `.gitignore` (it is out of scope, and at `5978324` it already covers all three).

## Test plan

**No new tests.** This plan adds no behaviour to test; it makes the existing suite run automatically. The suite is the test plan.

One thing worth stating because it is easy to get wrong: do not add a test that asserts `.github/workflows/ci.yml` exists. `tests/test_ship.py:469-497` and several tests in `tests/test_kntnt.py` do assert on file contents, so there is precedent for prose assertions — but those pin *behavioural contracts* the skills depend on (that `commit` never pushes, that the manager is user-invoked). A CI file's existence is not such a contract, and a test asserting it would fail on any fork that uses different CI.

Verification that this plan worked is observational and happens after it lands: the first push shows a green check on GitHub. Note in your report that this cannot be confirmed locally.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `test -f pyproject.toml` and `test -f .github/workflows/ci.yml` both succeed
- [ ] `grep -c '^\[project\]' pyproject.toml` returns `0` — no `[project]` table, so `/release` will not start bumping this repository
- [ ] `uv run --with pytest pytest -q` reports step 1's count and `0 failed`
- [ ] `uvx ruff check .` exits 0 with `All checks passed!`
- [ ] `uvx ruff format --check .` exits 0
- [ ] `uvx mypy skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py` reports `Success: no issues found in 2 source files` **without** a `--strict` flag on the command line
- [ ] `grep -c 'strict' pyproject.toml` returns `1` and `grep -c 'strict' .github/workflows/ci.yml` returns `0` — the setting lives in one place
- [ ] `grep -n 'permissions' .github/workflows/ci.yml` shows `contents: read`
- [ ] `git diff --stat` is empty — no tracked file was modified
- [ ] `git status --porcelain` lists only the two new paths
- [ ] Report states that the green CI run itself is unverifiable locally
- [ ] `plans/README.md` status row for 004 updated

## STOP conditions

Stop and report back (do not improvise) if:

- Step 1's count is below `84` — plans 001–003 have not all landed, and this plan must not go before them. (`77` means none of them has; `80` means only plan 005 has.)
- Any of step 1's four commands fails. Do not "fix" the failure here; report it. A red baseline means one of plans 001–003 landed incompletely, and diagnosing that is not this plan's job.
- Step 2 finds an existing `pyproject.toml`, `ruff.toml`, or mypy configuration.
- Moving `strict` from the command line into `pyproject.toml` surfaces type errors that `uvx mypy --strict <paths>` did not. Report the errors verbatim; the two should be equivalent, and if they are not, someone needs to decide which is authoritative before this lands.
- Adding `target-version = "py312"` makes `ruff check` or `ruff format --check` report anything. Report the findings rather than reformatting code — a tooling plan that rewrites source is no longer reviewable as a tooling plan.
- You conclude the workflow needs write permissions, a secret, or a token. It does not: nothing here publishes, comments, or pushes.
- You are tempted to add a matrix, a coverage upload, Dependabot, or CodeQL. All are out of scope; note them as follow-ups in your report instead.

## Maintenance notes

- **`strict` lives in `pyproject.toml`, not on the command line.** If someone later adds `--strict` to the workflow step too, the two can drift apart and the local and CI checks stop being the same check. The done criterion above pins this deliberately.
- **The `[project]`-table prohibition is not stylistic.** `ship.py`'s `detect_versions` (`skills/code/commit/scripts/ship.py:386-389`) reads `pyproject.toml` looking for a version to bump, and `plans/002-unify-version-detection-and-writing.md` makes that read stricter but not narrower. The day someone adds `[project] version = "…"` here, `/release` starts rewriting this file — which may be the right call, but it should be a decision, not a side effect of adding a lint setting. Leave a note in the file if that changes.
- **Reviewer should scrutinize**: that the CI commands are character-for-character the ones in `CONTRIBUTING.md` after plan 006 lands (a contributor running the documented commands must get the same verdict as CI), and that no step writes anything.
- **Deliberately deferred**, each defensible and each its own concern: an OS/Python matrix (nothing to matrix over while every script pins `>=3.12` and `uv` provisions the interpreter); coverage measurement; Dependabot (there are no third-party dependencies to update — both engines declare `dependencies = []`); CodeQL; and a job that regenerates the catalog and diffs it, which `test_shipped_catalog_matches_the_generated_one` in `tests/test_kntnt.py` already covers from inside the suite.
- **When a third dependency-free script joins the repository**, add it to the mypy step's path list. There is no glob there on purpose: `uvx mypy skills/` would try to follow the Markdown-adjacent directory structure and pick up nothing useful, and an explicit list makes an omission visible in review.
