# Plan 002: Make version detection and version writing agree, and make a failed bump write nothing

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Prerequisite**: `plans/001-characterize-version-bump.md` must be applied
> first. This plan's success criterion is that the three tests it left failing
> now pass. Verify that with step 1 before writing any code.
>
> **Drift check (run first)**: `git diff --stat 5978324..HEAD -- skills/code/commit/scripts/ship.py`
> Plan 001 does not touch this file, so the only expected difference from
> `5978324` is nothing. If `ship.py` changed, compare the "Current state"
> excerpts against the live code before proceeding; on a mismatch, treat it as
> a STOP condition.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: `plans/001-characterize-version-bump.md`
- **Category**: bug
- **Planned at**: commit `5978324`, 2026-08-17

## Why this matters

`ship.py` is the engine behind the `commit`, `push`, and `release` skills. Its release path writes version numbers into a project's manifests, promotes the changelog, tags `HEAD`, pushes the tag, and opens a GitHub release. Today it reads a version with one rule and writes it with a different rule, and the two disagree in three ways — one of which **silently corrupts the wrong field and reports success**, so a release gets tagged and published for a version the package never declares.

After this plan there is exactly one rule per file format that both locates and rewrites the version, a bump either succeeds completely or writes nothing at all, and a case the tool cannot resolve unambiguously refuses loudly instead of guessing. That last property is the point: for a tool that publishes releases on the user's behalf, a loud refusal is always cheaper than a quiet wrong answer.

## Current state

### Files

- `skills/code/commit/scripts/ship.py` — the plan/apply engine. The only file you will modify.
- `tests/test_ship.py` — the suite. Plan 001 added the five tests that specify this fix; **do not modify it in this plan.**

### The three disagreements, each reproduced at commit `5978324`

Reading — `ship.py:398-417`:

```python
def json_version(path: Path) -> str | None:
    """Return the top-level version string from a JSON file."""

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    value = data.get("version")
    return value if isinstance(value, str) else None


def toml_version(path: Path) -> str | None:
    """Return a ``version = "…"`` assignment from a TOML file."""

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("version") and "=" in stripped:
            _, _, raw = stripped.partition("=")
            return raw.strip().strip('"').strip("'")
    return None
```

Writing — `ship.py:20-22` and `ship.py:448-467`:

```python
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
JSON_VERSION_RE = re.compile(r'("version"\s*:\s*")([^"]+)(")')
TOML_VERSION_RE = re.compile(r'^(version\s*=\s*")([^"]+)(")', re.MULTILINE)
```

```python
def bump_version_files(cwd: Path, version: str) -> list[Path]:
    """Write *version* into every detected conventional location. Return paths."""

    written: list[Path] = []
    for relative, _current in detect_versions(cwd):
        path = cwd / relative
        original = path.read_text(encoding="utf-8")
        if path.suffix == ".toml":
            updated, count = TOML_VERSION_RE.subn(
                rf"\g<1>{version}\g<3>", original, count=1
            )
        else:
            updated, count = JSON_VERSION_RE.subn(
                rf"\g<1>{version}\g<3>", original, count=1
            )
        if count != 1:
            raise GitError(f"could not bump version in {relative}")
        path.write_text(updated, encoding="utf-8")
        written.append(path)
    return written
```

1. **JSON**: the reader takes the *top-level* `"version"` key. The writer replaces the *first* `"version": "…"` in file text order, with `count=1`. A manifest whose earlier blocks contain a nested `"version"` gets that one rewritten; the real version is untouched; the call returns normally.
2. **TOML**: the reader accepts any line whose stripped text starts with `version` and contains `=`, so `version_scheme = "post-release"` is read as a version. The writer's `TOML_VERSION_RE` requires the line to begin with `version` followed by optional whitespace and `=`, so it never matches that line — the reader reports a version the writer cannot write.
3. **Atomicity**: files are written one at a time inside the loop, and the first failure raises. `apply_bump` calls `bump_version_files` before promoting the changelog (`ship.py:524-527`), so a failure mid-loop leaves earlier manifests bumped, the changelog un-promoted, and a non-zero exit.

`detect_versions` — the caller both of the readers and, indirectly, of the writers — is at `ship.py:371-395`:

```python
def detect_versions(cwd: Path) -> list[tuple[str, str]]:
    """Find conventional version locations relative to *cwd*."""

    found: list[tuple[str, str]] = []
    package = cwd / "package.json"
    if package.is_file():
        version = json_version(package)
        if version:
            found.append(("package.json", version))
    composer = cwd / "composer.json"
    if composer.is_file():
        version = json_version(composer)
        if version:
            found.append(("composer.json", version))
    pyproject = cwd / "pyproject.toml"
    if pyproject.is_file():
        version = toml_version(pyproject)
        if version:
            found.append(("pyproject.toml", version))
    plugin = cwd / ".claude-plugin" / "plugin.json"
    if plugin.is_file():
        version = json_version(plugin)
        if version:
            found.append((".claude-plugin/plugin.json", version))
    return found
```

Its result is consumed in two places besides the bump — `build_plan` (`ship.py:336-341`) puts it in the plan as `version_files` and `current_version`, which the `release` skill shows the user and uses to compute the next version (`skills/code/release/SKILL.md:39`). So a bad read is not merely a bad write: it also puts a nonsense string in front of the user as the current version.

### Where the writes land

`ship.py:513-528`:

```python
def apply_bump(cwd: Path, version: str) -> str:
    """Bump version files and promote the changelog. Return the version."""

    tag = _require_version(version)
    _require_default_branch(cwd)
    if git(cwd, "tag", "-l", tag).strip():
        raise GitError(f"tag {tag} already exists")
    changelog = cwd / "CHANGELOG.md"
    if unreleased_is_empty(changelog) is not False:
        raise GitError("nothing to release")

    bump_version_files(cwd, version)
    date = datetime.datetime.now(tz=datetime.UTC).date().isoformat()
    new_text = promote_changelog(changelog.read_text(encoding="utf-8"), version, date)
    changelog.write_text(new_text, encoding="utf-8")
    return version
```

### Conventions this file follows — match them exactly

From `docs/coding-standard/general.md` and `docs/coding-standard/python.md`, as actually practised in `ship.py`:

- **Docstring, then a blank line, then the body.** Every function in this file does it. This is house style, not an accident:
  ```python
  def fail(message: str, code: int = 1) -> int:
      """Print an error to stderr and return an exit code."""

      print(f"error: {message}", file=sys.stderr)
      return code
  ```
- Full type hints on every signature and module-level constant.
- Errors raise `GitError` (`ship.py:53-55`); the CLI layer turns them into `fail()` plus an exit code (`ship.py:615-619`). Never `print` an error inside a helper.
- Module-level compiled regexes in `SCREAMING_SNAKE_CASE` at the top of the file (`ship.py:20-23`).
- Private helpers are prefixed with `_` (`_gh`, `_origin_url`, `_require_version`). Public-ish ones are not.
- `pathlib.Path` throughout; f-strings only; early returns to flatten nesting; no bare `except` — name the exception.
- Paragraph comments: a `#` topic sentence above a paragraph whose *purpose* is not evident from the code. This file uses them sparingly and only where the reasoning is non-obvious — see `ship.py:624-630` for the density to match. Do not narrate obvious code.
- PEP 723 header at the top (`ship.py:1-4`) declares `dependencies = []`. **This script must stay dependency-free — standard library only.** `tomllib` is standard library from Python 3.11 and `requires-python = ">=3.12"`, so it is allowed.
- `ruff format` is authoritative for layout. Run it rather than hand-aligning.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Full suite | `uv run --with pytest pytest -q` | after this plan: `0 failed`, same total as step 1 (`82 passed` if only plans 001+002 have landed) |
| This engine only | `uv run --with pytest pytest tests/test_ship.py -q` | after this plan: `0 failed`, same total as step 1 (`32 passed` if only plans 001+002 have landed) |
| Lint | `uvx ruff check .` | `All checks passed!` |
| Format | `uvx ruff format --check .` | exit 0 |
| Types | `uvx mypy --strict skills/code/commit/scripts/ship.py` | `Success: no issues found in 1 source file` |

## Scope

**In scope** (the only file you may modify):

- `skills/code/commit/scripts/ship.py`

**Out of scope** (do NOT touch, even though they look related):

- `tests/test_ship.py` — plan 001 wrote the specification. If a test looks wrong to you, that is a STOP condition, not an invitation to edit it. Changing the test to match your implementation defeats the entire exercise.
- `skills/code/release/SKILL.md` — the skill's prose describes the intended behaviour correctly already; only the engine was wrong.
- `skills/kntnt/scripts/kntnt.py` — a different engine, unaffected.
- `detect_build`, `make_targets`, `json_scripts`, `status_paths`, `promote_changelog`, `extract_release_notes`, `apply_tag`, `apply_publish` — leave them alone. `json_scripts` (`ship.py:259-269`) parses `package.json` too and looks adjacent, but it reads scripts, not versions.
- Do not add a dependency to the PEP 723 header. No `tomlkit`, no `packaging`.
- `CHANGELOG.md` — do not add an entry by hand; this repository's `commit` skill reconciles it at commit time.

## Git workflow

- Branch: continue on `advisor/001-characterize-version-bump`, or a branch that contains plan 001's commit. **Do not land this plan on a branch without 001** — the tests that prove it are there.
- Commit messages: imperative, sentence case, no conventional-commit prefix. Examples from `git log`: `Add the kntnt manager skill.` Suggested: `Read and write a version by one rule per format`.
- Do NOT push, open a PR, or run this repository's own `/commit`, `/push`, or `/release` skills unless the operator instructed it.

## Steps

### Step 1: Confirm you are standing on plan 001

**Verify**: `uv run --with pytest pytest -q` → exactly `3 failed`, and note the total collected; every later count in this plan is relative to it. (`3 failed, 79 passed` when plan 001 is the only other plan that has landed — a different total is fine, since plans 003 and 005 also add tests and may have gone first.)

The three failures must be exactly these, and no others:

- `test_apply_bump_ignores_a_nested_version_key`
- `test_plan_release_ignores_a_version_scheme_setting`
- `test_apply_bump_writes_nothing_when_one_file_cannot_be_bumped`

Any other number of failures, or any other test among them, is a STOP condition. The *total* may legitimately differ; the three named failures may not.

### Step 2: Read the TOML version with `tomllib`

Replace `toml_version` (`ship.py:409-417`) so it parses the document rather than scanning lines. `version_scheme` and every other key that merely starts with the letters `version` then becomes structurally impossible to mistake for a version.

Add `import tomllib` to the import block (`ship.py:9-18`), in alphabetical order among the standard-library imports — the block is currently `argparse, datetime, json, re, shutil, subprocess, sys`, so `tomllib` goes after `sys` and before the `from` imports.

Write it as a **text-level reader plus a thin `Path` wrapper** from the start. Step 4 needs to run the reader over rewritten text that is not yet on disk, so splitting it now avoids refactoring your own work later. Do the same split for `json_version` in this step, so both formats end up with the same shape.

Target shape — the four functions replace the existing `json_version` and `toml_version` (`ship.py:398-417`), in this order:

```python
def json_version(path: Path) -> str | None:
    """Return the top-level version string from a JSON file."""

    return json_reader(path.read_text(encoding="utf-8"))


def json_reader(text: str) -> str | None:
    """Return the top-level version string from JSON *text*."""

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    value = data.get("version")
    return value if isinstance(value, str) else None


def toml_version(path: Path) -> str | None:
    """Return the declared version from a TOML file."""

    return toml_reader(path.read_text(encoding="utf-8"))


def toml_reader(text: str) -> str | None:
    """Return the declared version from TOML *text*, or None.

    Reads `[project]` first, then `[tool.poetry]` — the two places a Python
    project's own version conventionally lives. A dynamic version is absent
    from both, which is the correct answer: there is nothing here to bump.
    """

    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None

    tool = data.get("tool")
    poetry = tool.get("poetry") if isinstance(tool, dict) else None
    for table in (data.get("project"), poetry):
        if isinstance(table, dict):
            value = table.get("version")
            if isinstance(value, str):
                return value
    return None
```

The two-line `tool` / `poetry` lookup is deliberately inline rather than extracted: one caller, four lines, and `docs/coding-standard/general.md:20` says no abstraction until more than one concrete implementation exists.

Keep this group positioned where `json_version` already is, immediately after `detect_versions` (`ship.py:371-395`).

`json_reader`'s body is the existing `json_version` body moved verbatim — do not otherwise change its behaviour in this plan. (It has a pre-existing rough edge: a JSON file whose top level is an array reaches `data.get` on a `list` and raises `AttributeError` rather than returning `None`. That is out of scope here and recorded as a follow-up in the maintenance notes.)

**Verify**: `uv run --with pytest pytest tests/test_ship.py -k "version_scheme or pyproject" -q` → `2 passed`

That is `test_plan_release_ignores_a_version_scheme_setting` (was failing, now passes) and `test_apply_bump_writes_the_pyproject_project_version` (was passing, still passes).

### Step 3: Add one helper that rewrites the assignment carrying a known value

The fix for the JSON disagreement is to stop asking "which text matches the pattern first?" and start asking "which match carries the version the reader reported?". Add this helper next to the existing regexes' consumers — put it immediately **above** `bump_version_files` (`ship.py:448`):

```python
def _rewrite_version(
    text: str, pattern: re.Pattern[str], current: str, version: str, relative: str
) -> str:
    """Return *text* with the assignment holding *current* set to *version*.

    Matching on the value rather than on the first occurrence is what keeps a
    nested `"version"` in some unrelated block from being rewritten instead of
    the real one. When no match carries *current*, or the result no longer
    reads back as *version*, this refuses: for a command that goes on to tag
    and publish, a wrong version written quietly is worse than a stopped run.
    """

    for match in pattern.finditer(text):
        if match[2] != current:
            continue
        return f"{text[: match.start(2)]}{version}{text[match.end(2) :]}"
    raise GitError(f"could not bump version in {relative}")
```

Group 2 of both `JSON_VERSION_RE` and `TOML_VERSION_RE` is the value, so slicing on `match.start(2)`/`match.end(2)` replaces exactly the version string and leaves quoting, spacing, and the rest of the line untouched.

**Verify**: `uvx ruff check . && uvx mypy --strict skills/code/commit/scripts/ship.py` → `All checks passed!` then `Success: no issues found in 1 source file`

The helper is unreachable at this point; that is expected. Step 4 wires it in.

### Step 4: Make `bump_version_files` resolve every file before writing any

Rewrite `bump_version_files` (`ship.py:448-467`) in two phases: resolve all new file contents in memory, verifying each; then write. Nothing reaches disk until every file has been resolved successfully, which is what makes a refusal leave the tree untouched.

Target shape:

```python
def bump_version_files(cwd: Path, version: str) -> list[Path]:
    """Write *version* into every detected conventional location. Return paths.

    Resolves every file before writing any of them, so a file this cannot
    rewrite unambiguously aborts the whole bump instead of leaving the project
    half-bumped for the caller to unpick by hand.
    """

    # Resolve first, write second — every failure mode has to land before the
    # first byte is written.
    resolved: list[tuple[Path, str]] = []
    for relative, current in detect_versions(cwd):
        path = cwd / relative
        pattern = TOML_VERSION_RE if path.suffix == ".toml" else JSON_VERSION_RE
        updated = _rewrite_version(
            path.read_text(encoding="utf-8"), pattern, current, version, relative
        )
        _confirm_version(path, updated, version, relative)
        resolved.append((path, updated))

    for path, updated in resolved:
        path.write_text(updated, encoding="utf-8")
    return [path for path, _updated in resolved]
```

And the confirmation, placed immediately above `_rewrite_version`:

```python
def _confirm_version(path: Path, updated: str, version: str, relative: str) -> None:
    """Raise unless *updated* reads back as *version* through the reader.

    The reader is the authority on where a version lives, so running it over
    the rewritten text is what proves the write hit that same place. It is the
    only check that also catches the ambiguous case, where a nested key holds
    the identical string and no value match can tell the two apart.
    """

    reader = toml_reader if path.suffix == ".toml" else json_reader
    if reader(updated) != version:
        raise GitError(f"could not bump version in {relative}")
```

`_confirm_version` calls `json_reader` / `toml_reader` — the text-level readers you already created in step 2. Nothing further to split here.

Note what makes this check the safety net rather than decoration: it is the **only** check that catches the ambiguous case, where a nested key holds a string identical to the real version. There `_rewrite_version` cannot tell the two apart and will rewrite the nested one; re-reading through the reader then shows the top level still holding the old version, and the bump refuses. That is what `test_apply_bump_writes_nothing_when_one_file_cannot_be_bumped` pins down.

**Verify**: `uv run --with pytest pytest tests/test_ship.py -q` → `0 failed`, with the same total step 1 collected for this file.

All five of plan 001's tests now pass, and every pre-existing test in the file still does. This plan adds no tests, so the total must not move.

### Step 5: Confirm the whole suite, the types, and the formatting

**Verify**, in order — every one must hold:

1. `uv run --with pytest pytest -q` → `0 failed`, with the same total step 1 collected
2. `uvx mypy --strict skills/code/commit/scripts/ship.py skills/kntnt/scripts/kntnt.py` → `Success: no issues found in 2 source files`
3. `uvx ruff check .` → `All checks passed!`
4. `uvx ruff format --check .` → exit 0. If it reports `ship.py` would be reformatted, run `uvx ruff format skills/code/commit/scripts/ship.py` and re-check.
5. `git status --porcelain` → exactly ` M skills/code/commit/scripts/ship.py` (plus plan 001's `tests/test_ship.py` if it is not yet committed)
6. `grep -n "dependencies = \[\]" skills/code/commit/scripts/ship.py` → matches at line 3. The script must still declare no third-party dependencies.

### Step 6: Confirm the original defect by hand

Automated tests pass; confirm the real-world shape once, so the report says the bug is gone rather than that the tests are green. Work in a temporary directory outside this repository.

```sh
cd "$(mktemp -d)"
git init -q -b main . && git config user.email t@e.com && git config user.name T
printf '{\n  "name": "acme/demo",\n  "extra": { "pinned": { "version": "9.9.9" } },\n  "version": "0.1.0"\n}\n' > composer.json
printf '# Changelog\n\n## [Unreleased]\n\n### Added\n\n- Thing.\n' > CHANGELOG.md
git add -A && git commit -qm init
uv run <ABSOLUTE PATH TO>/skills/code/commit/scripts/ship.py apply bump --version 0.2.0
cat composer.json
```

**Verify**: the command exits 0, and `composer.json` shows top-level `"version": "0.2.0"` with the nested `"pinned"` value still `"9.9.9"`. Paste the resulting `composer.json` into your report.

Delete the temporary directory afterwards.

## Test plan

**Write no new tests in this plan.** Plan 001 wrote the five that specify this fix; this plan's job is to satisfy them. The full expected state afterwards:

| Test (from plan 001) | Before this plan | After this plan |
|---|---|---|
| `test_apply_bump_ignores_a_nested_version_key` | FAIL | PASS |
| `test_plan_release_ignores_a_version_scheme_setting` | FAIL | PASS |
| `test_apply_bump_writes_the_pyproject_project_version` | PASS | PASS |
| `test_apply_bump_writes_nothing_when_one_file_cannot_be_bumped` | FAIL | PASS |
| `test_apply_publish_passes_changelog_notes_with_shifted_headings` | PASS | PASS |

Plus every pre-existing test in `tests/test_ship.py` and `tests/test_kntnt.py`, unchanged. The total collected must equal step 1's exactly — this plan writes no tests — and `0 failed`.

If you believe a sixth test is needed to cover something you wrote, note it in your report as a follow-up rather than adding it here — a plan whose test expectations shift mid-flight cannot be reviewed against its own criteria.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `uv run --with pytest pytest -q` reports `0 failed`, with the same total step 1 collected
- [ ] `uvx mypy --strict skills/code/commit/scripts/ship.py skills/kntnt/scripts/kntnt.py` reports `Success: no issues found in 2 source files`
- [ ] `uvx ruff check .` exits 0 with `All checks passed!`
- [ ] `uvx ruff format --check .` exits 0
- [ ] `git diff --stat -- tests/` is empty (plan 001's tests were not edited)
- [ ] `git diff --stat -- skills/` lists only `skills/code/commit/scripts/ship.py`
- [ ] `grep -n "dependencies = \[\]" skills/code/commit/scripts/ship.py` matches — no new third-party dependency
- [ ] `grep -c "subn" skills/code/commit/scripts/ship.py` returns `0` — the first-match-wins substitution is gone
- [ ] Step 6's manual check pasted into the report, showing the nested value preserved
- [ ] `plans/README.md` status row for 002 updated

## STOP conditions

Stop and report back (do not improvise) if:

- Step 1 does not report exactly three failures, or the three failing tests are not the three named ones — plan 001 has not been applied, or has been applied differently than specified. (A differing *total* is not a reason to stop: plans 003 and 005 add tests and may have landed first.)
- The "Current state" excerpts of `json_version`, `toml_version`, `bump_version_files`, or the three regexes do not match the live `ship.py` — the file drifted since `5978324`.
- You find you must edit `tests/test_ship.py` to make a test pass. Report which test and why; the test is the specification.
- `tomllib.loads` is unavailable (Python older than 3.11). The PEP 723 header pins `>=3.12`, so this should be impossible — report the interpreter version `uv` selected.
- Satisfying `test_apply_bump_writes_nothing_when_one_file_cannot_be_bumped` seems to require writing a temp file and renaming it into place, or any other filesystem-level transaction. It does not: resolving all contents in memory before the first `write_text` is sufficient for this test and for the real failure mode. If you think otherwise, report the case you have in mind rather than building it.
- Adding a third-party dependency looks necessary (e.g. `tomlkit` to round-trip TOML). It is not, because the write path edits the value span in place and never re-serializes the document. Report what pushed you there.
- After the fix, `plan release` on a real project in your environment reports a `current_version` you believe is wrong. Report the project's manifest shape.

## Maintenance notes

- **The two-phase write is load-bearing, not a style choice.** Anyone adding a fifth version location must resolve it in the first loop and write it in the second. A `write_text` inside the resolve loop silently reintroduces the half-bumped tree that `test_apply_bump_writes_nothing_when_one_file_cannot_be_bumped` exists to prevent.
- **The reader is the authority on where a version lives.** `_confirm_version` runs the reader over the rewritten text; that coupling is what makes the whole thing safe. If a future change makes the reader and writer disagree again, that test is the one that will catch it — do not weaken it into a `try`/`except`.
- **Known and accepted limit**: `TOML_VERSION_RE` is anchored to column 0, so in a TOML file with a version in both `[project]` and `[tool.poetry]`, the write targets whichever appears first in the file. `_confirm_version` catches the case where that is the wrong one and refuses. Handling it properly needs real TOML round-tripping and a dependency; the refusal is the honest answer until someone actually hits it.
- **Reviewer should scrutinize**: that `detect_versions` is still the single entry point for "where are the versions" (it must not grow a second, divergent copy in the bump path), and that `_rewrite_version` slices on group 2 rather than using `re.sub` with a replacement template — the template form is what allowed a `\g<1>`-based rewrite to hit the wrong match in the first place.
- **Interaction to watch**: plan 004 adds a `pyproject.toml` to this repository for ruff and mypy configuration. If that file ever gains a `[project] version` key, `detect_versions` will start finding it and `/release` will begin bumping this repository's own `pyproject.toml` — which is fine, but it changes what a release of this repo touches. Plan 004 is written to omit `[project]` for exactly this reason; if someone adds it later, that is the moment to decide deliberately.
- **Deliberately deferred**, all pre-existing and none implicated in this bug: `json_reader` raises `AttributeError` rather than returning `None` on a JSON file whose top level is an array; `promote_changelog` is untested against a changelog carrying link-reference definitions; and `_require_version` (`ship.py:496-501`) accepts pre-release strings like `1.0.0-rc.1` that nothing downstream is tested against.
