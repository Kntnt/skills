# Plan 001: Pin the release version machinery with tests that expose the wrong-field bump

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **This plan adds tests only.** Three of the five tests you write are
> **expected to fail** when you finish. That is the deliverable: a
> demonstrated red step. Plan 002 makes them pass. Do not edit
> `skills/code/commit/scripts/ship.py` — see STOP conditions.
>
> **Drift check (run first)**: `git diff --stat 5978324..HEAD -- skills/code/commit/scripts/ship.py tests/test_ship.py`
> If either file changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: tests
- **Planned at**: commit `5978324`, 2026-08-17

## Why this matters

`ship.py` is the engine behind the `commit`, `push`, and `release` skills. Its release path writes version numbers into project files, promotes the changelog, tags `HEAD`, pushes, and opens a GitHub release — the most destructive thing this repository does to someone else's project. Today that path reads a version with one rule and writes it with a different, disagreeing rule, and the disagreement can rewrite the wrong field while reporting success. The existing suite never caught it because it exercises the bump through exactly one shape: a flat `package.json` with a single `"version"` key.

This plan writes the tests that make the bug visible and fail loudly, so that plan 002's fix is verified rather than asserted. It also adds two regression guards over behaviour that works today and must keep working. Nothing here changes production code.

The project's coding standard states the reason directly, in `docs/coding-standard/general.md:23`:

> The RED step is not ceremony: a test never observed to fail is of unknown value, so demonstrate the failing run as an artifact (seen failing before the satisfying code exists), never inferred after the fact.

## Current state

### Files

- `skills/code/commit/scripts/ship.py` — the plan/apply engine for commit, push, and release. **Read-only in this plan.**
- `tests/test_ship.py` — the CLI-level pytest suite for that engine. The only file you will modify.

### The two disagreeing rules (read these, do not change them)

Reading a version — `ship.py:371-417`:

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

Writing a version — `ship.py:20-22` and `ship.py:448-467`:

```python
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

Three specific disagreements, each reproduced by hand at commit `5978324`:

1. **JSON**: `json_version` reads the *top-level* `"version"` key. `JSON_VERSION_RE` with `count=1` replaces the *first* `"version": "…"` anywhere in the file text. A `composer.json` whose `extra` block contains a nested `"version"` before the top-level one gets the nested value rewritten; the real version is left alone; `apply bump` exits 0 and prints the new version. The release then tags and publishes a version the package never declares.
2. **TOML**: `toml_version` accepts any line whose stripped text starts with `version` and contains `=`, so `version_scheme = "post-release"` under `[tool.setuptools_scm]` is read as the version. `TOML_VERSION_RE` requires the line to start with `version` followed by optional whitespace and `=`, so it does not match that line. The plan shows the user `pyproject.toml:post-release`, and `apply bump` raises `could not bump version in pyproject.toml`.
3. **Atomicity**: `bump_version_files` writes each file as it goes and raises on the first failure. With `package.json` and a `pyproject.toml` that hits case 2, `package.json` is written to the new version, then the call raises, so `apply_bump` never reaches the changelog promotion (`ship.py:526-527`). The user is left with a half-bumped tree and a non-zero exit.

### The write path these tests drive

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

Note the two preconditions your fixtures must satisfy for `apply bump` to get as far as the version files: the repo must be **on its default branch** (`main`), and `CHANGELOG.md` must have a **non-empty `[Unreleased]`** section. The existing `CHANGELOG` constant in the test file satisfies the second.

`extract_release_notes` — `ship.py:479-493` — is reached only through `apply publish`, and has no test today:

```python
def extract_release_notes(text: str, version: str) -> str:
    """Return the body of ``## [version]`` with headings shifted up one level."""

    pattern = re.compile(
        r"^## \[" + re.escape(version) + r"\][^\n]*\n(?P<body>.*?)"
        r"(?=^## \[|^\[[^\]]+\]:\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if match is None:
        return ""
    body = re.sub(
        r"^(#{3,6})(?= )", lambda m: m[1][1:], match["body"], flags=re.MULTILINE
    )
    return body.strip()
```

It is called from `apply_publish` (`ship.py:556-562`), which passes the result as `--notes` to `gh release create`.

### Test conventions to match

`tests/test_ship.py` drives the script through its CLI in a throwaway git repo. The helpers you will use already exist — **do not write new ones unless a step says to**:

- `tests/test_ship.py:11-12` — module constants:
  ```python
  REPO_ROOT = Path(__file__).resolve().parent.parent
  SHIP = REPO_ROOT / "skills" / "code" / "commit" / "scripts" / "ship.py"
  ```
- `tests/test_ship.py:34-42` — `_init_repo(path: Path) -> Path` creates the directory, `git init -b main`, sets `user.name`/`user.email`, writes `README.md`, and makes one commit. **Its `path.mkdir()` has no `parents=True`, so always pass `tmp_path / "proj"`, never a deeper path.**
- `tests/test_ship.py:45-58` — `_ship(cwd, *args, env=None)` runs `["uv", "run", str(SHIP), *args]` with `check=False` and returns the `CompletedProcess`. Assert on `result.returncode`, `result.stdout`, `result.stderr`.
- `tests/test_ship.py:23-31` — `_git(cwd, *args)` runs git with `check=True`.
- `tests/test_ship.py:67-76` — the shared changelog fixture:
  ```python
  CHANGELOG = """# Changelog

  ## [Unreleased]

  ### Added

  - A new greeting.

  ## [0.1.0] – 2026-01-01
  """
  ```
  (The date separator is an en dash `–`, U+2013, matching `promote_changelog` at `ship.py:476`. Keep it.)

The structural model for a bump test is `tests/test_ship.py:327-344`:

```python
def test_apply_bump_writes_version_and_promotes_changelog(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "package.json").write_text('{"version": "0.1.0"}\n', encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "package.json", "CHANGELOG.md")
    _git(repo, "commit", "-m", "Add package")
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")

    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert result.returncode == 0, result.stderr
    assert "0.2.0" in result.stdout
    package = json.loads((repo / "package.json").read_text(encoding="utf-8"))
    assert package["version"] == "0.2.0"
    changelog = (repo / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [0.2.0]" in changelog
    assert "## [Unreleased]" in changelog
    assert _git(repo, "tag", "-l", "v0.2.0").stdout.strip() == ""
```

The structural model for a `gh`-driven test is `tests/test_ship.py:401-429` — it writes a fake `gh` shell script into a temp `bin/`, `chmod`s it executable, and passes `PATH` and `GH_LOG` through `_ship(..., env={...})`. Copy that shape for the release-notes test.

Style rules that apply (`docs/coding-standard/general.md`, `docs/coding-standard/python.md`):

- Arrange-Act-Assert, with a blank line between the three parts — every existing test does this.
- Test names state the expected behaviour as a sentence: `test_apply_bump_ignores_a_nested_version_key`, not `test_bump_2`.
- Full type hints on every signature: `(tmp_path: Path) -> None`.
- `pathlib.Path`, f-strings, no bare `except`.
- No docstrings on individual test functions — the existing file has none; the name carries the meaning.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Full suite | `uv run --with pytest pytest -q` | before your change: `0 failed` (`77 passed` on a clean `5978324`) |
| This file only | `uv run --with pytest pytest tests/test_ship.py -q` | before your change: `0 failed` (`27 passed` on a clean `5978324`) |
| One test, verbose | `uv run --with pytest pytest tests/test_ship.py::<name> -q` | as stated per step |
| Lint | `uvx ruff check .` | `All checks passed!` |
| Format | `uvx ruff format --check .` | exit 0 |

`uv` is the only prerequisite. Tests shell out to real `git`, so `git` must be on `PATH`.

## Scope

**In scope** (the only file you may modify):

- `tests/test_ship.py` (append five tests)

**Out of scope** (do NOT touch, even though they look related):

- `skills/code/commit/scripts/ship.py` — plan 002 owns every change here. Making the tests pass in this plan destroys the artifact this plan exists to produce.
- `tests/test_kntnt.py` and `tests/support/fake_skills.py` — different engine, unaffected.
- `skills/code/release/SKILL.md` — the skill's prose is correct; only the engine misbehaves.
- `CHANGELOG.md` — do not add an entry. The repository's `commit` skill reconciles the changelog at commit time; writing one by hand here would duplicate it.

## Git workflow

- Branch: `advisor/001-characterize-version-bump`
- One commit for the whole plan is fine — it is a single concern (`CONTRIBUTING.md:24`: "One concern per PR").
- Commit messages in this repo are imperative, sentence case, no conventional-commit prefix. Examples from `git log`: `Add the kntnt manager skill.`, `Add CONTEXT, ADRs 0001–0015, includes/, and skill category folders`. Suggested: `Add failing tests for the release version bump`.
- Do NOT push, open a PR, or run this repository's own `/commit`, `/push`, or `/release` skills unless the operator instructed it.

## Steps

### Step 1: Confirm the baseline

Run the suite before touching anything, so you can tell your failures from pre-existing ones.

**Verify**: `uv run --with pytest pytest -q` → `0 failed`. Also run `uv run --with pytest pytest tests/test_ship.py -q` and note that count separately.

**Write both numbers down** — every later count in this plan is expressed relative to them, because plans 003 and 005 also add tests and may have landed before this one. On a clean `5978324` they are `77` and `27`; a different number is fine, a *failure* is a STOP condition.

### Step 2: Add the nested-JSON-key test

Append to `tests/test_ship.py`. A `composer.json` carries a nested `"version"` inside its free-form `extra` block, positioned **before** the top-level `"version"` in file order. After a bump, the top-level version must be the new one and the nested value must be untouched.

```python
def test_apply_bump_ignores_a_nested_version_key(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "composer.json").write_text(
        '{\n'
        '  "name": "acme/demo",\n'
        '  "extra": {\n'
        '    "pinned": { "version": "9.9.9" }\n'
        '  },\n'
        '  "version": "0.1.0"\n'
        '}\n',
        encoding="utf-8",
    )
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "composer.json", "CHANGELOG.md")
    _git(repo, "commit", "-m", "Add composer manifest")

    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert result.returncode == 0, result.stderr
    composer = json.loads((repo / "composer.json").read_text(encoding="utf-8"))
    assert composer["version"] == "0.2.0"
    assert composer["extra"]["pinned"]["version"] == "9.9.9"
```

**Verify**: `uv run --with pytest pytest tests/test_ship.py::test_apply_bump_ignores_a_nested_version_key -q`
→ **1 failed.** The failure must be on `assert composer["version"] == "0.2.0"`, showing `"0.1.0" == "0.2.0"` — the top-level key was not bumped. If instead it fails on the `extra` assertion, or passes, that is a STOP condition (the bug is not what this plan describes).

### Step 3: Add the TOML false-positive test

A `pyproject.toml` with a dynamic version and a `version_scheme` setting has **no** version for this tool to bump. `plan release` must therefore not list `pyproject.toml` in `version_files`, and must not report `post-release` as the current version.

```python
def test_plan_release_ignores_a_version_scheme_setting(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "pyproject.toml").write_text(
        '[project]\n'
        'name = "demo"\n'
        'dynamic = ["version"]\n'
        '\n'
        '[tool.setuptools_scm]\n'
        'version_scheme = "post-release"\n',
        encoding="utf-8",
    )
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")

    result = _ship(repo, "plan", "release")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["version_files"] == []
    assert plan["current_version"] != "post-release"
```

**Verify**: `uv run --with pytest pytest tests/test_ship.py::test_plan_release_ignores_a_version_scheme_setting -q`
→ **1 failed**, on `assert plan["version_files"] == []`, with the actual value `["pyproject.toml:post-release"]`.

### Step 4: Add the pyproject regression guard

This one **passes today** and must keep passing: a real `[project]` version round-trips correctly.

```python
def test_apply_bump_writes_the_pyproject_project_version(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "pyproject.toml").write_text(
        '[build-system]\n'
        'requires = ["hatchling"]\n'
        '\n'
        '[project]\n'
        'name = "demo"\n'
        'version = "0.1.0"\n',
        encoding="utf-8",
    )
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "pyproject.toml", "CHANGELOG.md")
    _git(repo, "commit", "-m", "Add pyproject")

    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert result.returncode == 0, result.stderr
    assert 'version = "0.2.0"' in (repo / "pyproject.toml").read_text(encoding="utf-8")
    assert 'requires = ["hatchling"]' in (repo / "pyproject.toml").read_text(
        encoding="utf-8"
    )
```

**Verify**: `uv run --with pytest pytest tests/test_ship.py::test_apply_bump_writes_the_pyproject_project_version -q` → **1 passed.**

If this one fails, the pyproject read/write path is more broken than this plan assumes — STOP and report.

### Step 5: Add the all-or-nothing test

Two version files, where the second cannot be bumped unambiguously: its nested `"version"` holds the **same** string as the top-level one, so no value-matching rule can tell them apart. The required behaviour is a refusal that leaves **both** files exactly as they were — a failed bump must never leave a half-bumped tree.

```python
def test_apply_bump_writes_nothing_when_one_file_cannot_be_bumped(
    tmp_path: Path,
) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "package.json").write_text('{"version": "0.1.0"}\n', encoding="utf-8")
    ambiguous = (
        '{\n'
        '  "name": "acme/demo",\n'
        '  "extra": {\n'
        '    "pinned": { "version": "0.1.0" }\n'
        '  },\n'
        '  "version": "0.1.0"\n'
        '}\n'
    )
    (repo / "composer.json").write_text(ambiguous, encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    _git(repo, "add", "package.json", "composer.json", "CHANGELOG.md")
    _git(repo, "commit", "-m", "Add manifests")

    result = _ship(repo, "apply", "bump", "--version", "0.2.0")

    assert result.returncode != 0
    assert "composer.json" in result.stderr
    assert (repo / "package.json").read_text(encoding="utf-8") == (
        '{"version": "0.1.0"}\n'
    )
    assert (repo / "composer.json").read_text(encoding="utf-8") == ambiguous
    assert "## [0.2.0]" not in (repo / "CHANGELOG.md").read_text(encoding="utf-8")
```

**Verify**: `uv run --with pytest pytest tests/test_ship.py::test_apply_bump_writes_nothing_when_one_file_cannot_be_bumped -q`
→ **1 failed.** Today the command exits 0 (it silently bumps composer's nested key), so the failure will be on `assert result.returncode != 0`.

### Step 6: Add the release-notes test

`extract_release_notes` has no coverage. Reach it through `apply publish` with a fake `gh`, and assert that the notes handed to `gh` carry the section body with its `###` headings shifted to `##`. Model this on `tests/test_ship.py:401-429`.

```python
def test_apply_publish_passes_changelog_notes_with_shifted_headings(
    tmp_path: Path,
) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "CHANGELOG.md").write_text(
        "# Changelog\n"
        "\n"
        "## [Unreleased]\n"
        "\n"
        "## [0.2.0] – 2026-02-02\n"
        "\n"
        "### Added\n"
        "\n"
        "- A shipped thing.\n"
        "\n"
        "## [0.1.0] – 2026-01-01\n"
        "\n"
        "### Added\n"
        "\n"
        "- An older thing.\n",
        encoding="utf-8",
    )
    _git(repo, "add", "CHANGELOG.md")
    _git(repo, "commit", "-m", "changelog")
    _git(repo, "remote", "add", "origin", "git@github.com:example/proj.git")
    log = tmp_path / "gh.log"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    gh = bin_dir / "gh"
    gh.write_text('#!/bin/sh\necho "$@" >> "$GH_LOG"\n', encoding="utf-8")
    gh.chmod(gh.stat().st_mode | stat.S_IEXEC)

    result = _ship(
        repo,
        "apply",
        "publish",
        "--version",
        "0.2.0",
        env={
            "PATH": f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}",
            "GH_LOG": str(log),
        },
    )

    assert result.returncode == 0, result.stderr
    recorded = log.read_text(encoding="utf-8")
    assert "- A shipped thing." in recorded
    assert "## Added" in recorded
    assert "An older thing" not in recorded
```

`stat` and `os` are already imported at `tests/test_ship.py:6-7`; do not add imports.

**Verify**: `uv run --with pytest pytest tests/test_ship.py::test_apply_publish_passes_changelog_notes_with_shifted_headings -q` → **1 passed.**

If it fails, report the actual contents of the `gh.log` in your report — the notes-extraction behaviour is then also broken and plan 002 needs to know.

### Step 7: Confirm the red step and the shape of the suite

**Verify**:

1. `uv run --with pytest pytest -q` → exactly `3 failed`, and step 1's full-suite count `+ 5` collected in total. The three failures are exactly the tests from steps 2, 3, and 5 — no others.
2. `uvx ruff check .` → `All checks passed!`
3. `uvx ruff format --check .` → exit 0. If it reports `tests/test_ship.py` would be reformatted, run `uvx ruff format tests/test_ship.py` and re-check.
4. `git status --porcelain` → exactly one line: ` M tests/test_ship.py`

Record the three failure messages verbatim in your report. That transcript is the artifact `docs/coding-standard/general.md:23` asks for, and plan 002's reviewer will compare against it.

## Test plan

All five tests go in `tests/test_ship.py`, appended after the existing `test_apply_publish_uploads_asset_when_release_exists` (`tests/test_ship.py:432-466`) and before the three `SKILL.md` prose assertions at `tests/test_ship.py:469-497` — those read as a closing group and should stay last.

| Test | Covers | Expected at end of this plan |
|---|---|---|
| `test_apply_bump_ignores_a_nested_version_key` | JSON write hits the top-level key, not the first textual match | FAIL (the bug) |
| `test_plan_release_ignores_a_version_scheme_setting` | TOML read does not mistake `version_scheme` for a version | FAIL (the bug) |
| `test_apply_bump_writes_the_pyproject_project_version` | `[project] version` round-trips, other TOML lines untouched | PASS (regression guard) |
| `test_apply_bump_writes_nothing_when_one_file_cannot_be_bumped` | A failed bump writes no file and does not promote the changelog | FAIL (the bug) |
| `test_apply_publish_passes_changelog_notes_with_shifted_headings` | `extract_release_notes` picks the right section and shifts headings | PASS (new coverage) |

Structural pattern: `test_apply_bump_writes_version_and_promotes_changelog` (`tests/test_ship.py:327`) for the bump tests, `test_apply_publish_creates_github_release` (`tests/test_ship.py:401`) for the publish test.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `uv run --with pytest pytest -q` reports exactly `3 failed`, and passed `+` failed equals step 1's full-suite count `+ 5`
- [ ] `uv run --with pytest pytest tests/test_ship.py -q` reports exactly `3 failed`, and passed `+` failed equals step 1's file count `+ 5`
- [ ] `grep -c "^def test_" tests/test_ship.py` returns step 1's file count `+ 5` (`32` on a clean `5978324`)
- [ ] `uvx ruff check .` exits 0 with `All checks passed!`
- [ ] `uvx ruff format --check .` exits 0
- [ ] `git status --porcelain` lists only ` M tests/test_ship.py`
- [ ] `git diff --stat -- skills/` is empty (no production code touched)
- [ ] The report quotes the three failure messages verbatim
- [ ] `plans/README.md` status row for 001 updated

## STOP conditions

Stop and report back (do not improvise) if:

- Any test fails in step 1 — the suite is already red, and this plan's whole point is a *known* set of three failures. A different baseline **count** is fine and expected if plan 003 or 005 landed first; a baseline *failure* is not.
- The excerpts of `detect_versions`, `json_version`, `toml_version`, or `bump_version_files` in "Current state" do not match `skills/code/commit/scripts/ship.py` — the file has drifted since commit `5978324`.
- A test from step 2, 3, or 5 **passes**. The bug this plan characterizes is then already fixed or differently shaped; do not weaken the test to make it fail. Report which one passed and what the file actually contains.
- A test from step 4 or 6 **fails**. Report the full failure output; something beyond this plan's diagnosis is wrong.
- You conclude a test cannot be written without changing `ship.py`. It can — every test here drives the existing CLI. Report what blocked you rather than editing production code.
- `uv run --with pytest pytest` cannot run at all (no `uv`, no `git`). Report the missing prerequisite.

## Maintenance notes

- **This plan's output is deliberately red.** Do not merge it to the default branch on its own if CI is ever wired up before plan 002 lands — plan 004 adds that CI and is sequenced after 002 for exactly this reason. Keep 001 and 002 on the same branch, or land them back to back.
- The reviewer should check that the three failing tests fail *for the stated reason*, not incidentally. A test that fails because the fixture is malformed proves nothing.
- `test_apply_bump_writes_nothing_when_one_file_cannot_be_bumped` encodes a policy decision, not just a behaviour: an ambiguous file makes the whole bump refuse rather than guess. If a future maintainer wants best-effort bumping instead, this test is the one to argue with — and `plans/002-*.md` explains why refusal was chosen.
- Deliberately not covered here: `promote_changelog` against a changelog with link-reference definitions at the bottom (`[Unreleased]: https://…`), and `_require_version` against pre-release strings like `1.0.0-rc.1`. Both are plausible follow-ups; neither is implicated in the bug plan 002 fixes, so they stayed out to keep this plan one concern.
