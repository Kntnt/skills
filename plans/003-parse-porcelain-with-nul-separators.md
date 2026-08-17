# Plan 003: Parse `git status` with NUL separators so non-ASCII paths reach the user intact

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Drift check (run first)**: `git diff --stat 5978324..HEAD -- skills/code/commit/scripts/ship.py tests/test_ship.py`
> If either file changed since this plan was written, compare the "Current
> state" excerpts against the live code before proceeding; on a mismatch, treat
> it as a STOP condition. Expect `ship.py` to differ if
> `plans/002-unify-version-detection-and-writing.md` already landed — that plan
> does not touch `status_paths`, so the excerpt below should still match
> exactly. If it does not, stop.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none (independent of plans 001 and 002; can land before, after, or in parallel)
- **Category**: bug
- **Planned at**: commit `5978324`, 2026-08-17

## Why this matters

The `commit` skill's whole safety model is that the user sees what is about to be committed and confirms it. `skills/code/commit/SKILL.md:38` — "Show the changelog diff, the message, and the proposed `.gitignore` if any. Wait unless `--yes`." The file lists in that confirmation come from the JSON plan's `staged`, `tracked`, and `untracked` arrays.

Those arrays are built by parsing `git status --porcelain` as plain text. Git, by default (`core.quotepath` is on), C-quotes any path containing a byte outside ASCII — so a file named `skäl.md` arrives as the seven-character-escaped literal `"sk\303\244me.md"`. Reproduced at commit `5978324`: an untracked `skäl.md` came back in the plan as `"\"sk\\303\\244l.md\""`. For an author working in Swedish, that is not an edge case, it is Tuesday. The user is asked to approve a list they cannot read, which is the one thing the confirmation step exists to prevent.

A rename compounds it: the current parser splits on the literal `" -> "` inside the quoted form, so a renamed path with non-ASCII bytes is split inside its own quoting.

The commit itself is unaffected — `apply_commit` runs `git add -A` (`ship.py:423`) and never uses these paths. This is a bug in what the user is shown, not in what is committed, which is why it is P2 rather than P1. It is still a bug in the only screen that stands between the user and a commit.

## Current state

### Files

- `skills/code/commit/scripts/ship.py` — the plan/apply engine. `status_paths` is the only function you will change.
- `tests/test_ship.py` — the CLI-level pytest suite. You will add two tests.

### The parser, `ship.py:147-166`

```python
def status_paths(cwd: Path) -> tuple[list[str], list[str], list[str]]:
    """Return (staged, tracked unstaged, untracked) paths from porcelain."""

    staged: list[str] = []
    tracked: list[str] = []
    untracked: list[str] = []
    for line in git(cwd, "status", "--porcelain", "-uall").splitlines():
        code = line[:2]
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if code == "??":
            untracked.append(path)
        elif code[0] != " " and code[0] != "?":
            staged.append(path)
            if code[1] != " ":
                tracked.append(path)
        else:
            tracked.append(path)
    return staged, tracked, untracked
```

`git()` is at `ship.py:64-77` — it runs git with `capture_output=True`, `text=True`, and raises `GitError` on a non-zero exit.

### Callers — the classification semantics must not change

- `build_plan` (`ship.py:299`) → the three lists become the plan's `staged`, `tracked`, `untracked`, and `dirty` is `bool(staged or tracked or untracked)`.
- `apply_commit` (`ship.py:424`) → uses only `staged`, to check that `git add -A` actually staged something.

Three existing tests pin the current classification and must keep passing unchanged:

- `test_plan_commit_reports_tracked_dirty_file` (`tests/test_ship.py:79`) — a modified tracked file lands in `tracked`.
- `test_plan_commit_is_ready_when_only_untracked` (`tests/test_ship.py:94`) — an untracked file lands in `untracked`.
- `test_apply_commit_stages_unstaged_tracked_files` (`tests/test_ship.py:179`) — a file that is both staged and further modified is committed in full.

So: preserve the mapping exactly. `??` → untracked. A non-blank, non-`?` first column → staged, and additionally tracked when the second column is also non-blank. Everything else → tracked.

### What `-z` changes, verified by hand at commit `5978324`

Default output, in a repo with a modified file, a rename, and an untracked file, all with non-ASCII names:

```
 M keep.txt
R  "old n\303\244me.txt" -> "new n\303\244me.txt"
?? "untracked \303\266.txt"
```

The same state under `git status --porcelain -z -uall`, with NUL rendered as a newline for display:

```
 M keep.txt
R  new näme.txt
old näme.txt
?? untracked ö.txt
```

Two facts to build on:

1. **With `-z`, paths are never quoted or escaped** — the raw bytes are emitted and the NUL byte is the separator. This is why `-z` is the fix rather than `-c core.quotepath=false`: it also removes the ambiguity of a path that legitimately contains a `"` or a newline.
2. **A rename or copy emits two fields**: the entry `R  <new path>`, then a *separate* NUL-terminated field holding `<old path>`. There is no `" -> "` marker. A parser that treats every field as an entry will read `old näme.txt` as an entry whose code is `ol` and whose path is `d näme.txt` — so the second field must be consumed deliberately.

Which status codes carry that extra field, verified against git 2.55.0:

| Repository state | Fields emitted |
|---|---|
| `git mv a.txt b.txt` | `R  b.txt` · `a.txt` |
| staged rename, then the new file edited again | `RM b.txt` · `a.txt` |
| plain `mv` followed by `git add -A` (rename detected) | `R  c.txt` · `a.txt` |
| plain `mv`, nothing staged (no rename pairing) | ` D a.txt` · `?? d.txt` |

So the marker is `R` or `C` in the **first** column, and an unstaged-only rename is not reported as a rename at all. The target shape below tests both columns regardless — no documented two-column code combination contains `R` or `C` without the extra field, so checking both is free insurance against a git version that reports a worktree rename as ` R`.

### Conventions this file follows — match them exactly

From `docs/coding-standard/general.md` and `docs/coding-standard/python.md`, as practised in `ship.py`:

- **Docstring, then a blank line, then the body.** Every function in this file does it:
  ```python
  def git_ok(cwd: Path, *args: str) -> bool:
      """Return True when a git command exits 0."""

      result = subprocess.run(...)
      return result.returncode == 0
  ```
- Full type hints on every signature.
- Errors raise `GitError` (`ship.py:53-55`); helpers never print.
- `pathlib.Path`, f-strings, early returns, no bare `except`.
- Paragraph comments: a `#` topic sentence above a paragraph whose purpose is not evident. Used sparingly in this file — see `ship.py:624-630` for the density. The NUL/rename handling warrants one; the list appends do not.
- Standard library only. The PEP 723 header (`ship.py:1-4`) declares `dependencies = []` and must stay that way.
- `ruff format` is authoritative for layout.

Test conventions (`tests/test_ship.py`) — the helpers already exist, do not write new ones:

- `_init_repo(path)` (`tests/test_ship.py:34-42`) — creates the dir with a plain `path.mkdir()` (no `parents=True`, so always pass `tmp_path / "proj"`), runs `git init -b main`, sets user identity, commits a `README.md`.
- `_ship(cwd, *args, env=None)` (`tests/test_ship.py:45-58`) — runs `["uv", "run", str(SHIP), *args]` with `check=False`; assert on `.returncode`, `.stdout`, `.stderr`.
- `_git(cwd, *args)` (`tests/test_ship.py:23-31`) — runs git with `check=True`.
- Arrange-Act-Assert with a blank line between the three parts; no docstrings on test functions; names state the expected behaviour.

Use `test_plan_commit_is_ready_when_only_untracked` (`tests/test_ship.py:94-103`) as the structural pattern:

```python
def test_plan_commit_is_ready_when_only_untracked(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "notes.md").write_text("keep\n", encoding="utf-8")

    result = _ship(repo, "plan", "commit")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["ready"] is True
    assert "notes.md" in plan["untracked"]
```

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Full suite | `uv run --with pytest pytest -q` | `77 passed` before this plan (`82 passed` if plans 001+002 already landed); two more after |
| This engine only | `uv run --with pytest pytest tests/test_ship.py -q` | `27 passed` before; `29 passed` after (`32` → `34` if 001+002 landed) |
| Lint | `uvx ruff check .` | `All checks passed!` |
| Format | `uvx ruff format --check .` | exit 0 |
| Types | `uvx mypy --strict skills/code/commit/scripts/ship.py` | `Success: no issues found in 1 source file` |

Because the expected counts depend on whether plans 001 and 002 landed first, **record the baseline count from step 1** and check the final count against `baseline + 2`.

## Scope

**In scope**:

- `skills/code/commit/scripts/ship.py` — `status_paths` only
- `tests/test_ship.py` — two new tests appended

**Out of scope** (do NOT touch, even though they look related):

- `apply_commit` (`ship.py:420-428`) — it uses `git add -A` and only checks that `staged` is non-empty. It needs no change and its behaviour must not change.
- `commit_subjects` (`ship.py:214-227`) — also parses git output, on a tab-separated `--format`. Commit subjects are not paths and are not quoted; leave it alone.
- `unpushed_count`, `default_branch`, `current_branch`, `last_tag` — other git wrappers, unaffected.
- `gitignore_proposal` (`ship.py:230-245`) and `GITIGNORE_BASE` — unrelated.
- `skills/code/commit/SKILL.md` — the skill's prose is already correct about showing the plan; only the data was wrong.
- Any change to the *classification* of a path into staged / tracked / untracked. This plan changes how paths are **read**, not how they are **categorised**.
- `CHANGELOG.md` — do not add an entry by hand; this repository's `commit` skill reconciles it at commit time.

## Git workflow

- Branch: `advisor/003-porcelain-nul-separators`
- One commit for the plan — one concern (`CONTRIBUTING.md:24`).
- Commit messages: imperative, sentence case, no conventional-commit prefix (`git log` examples: `Add the kntnt manager skill.`). Suggested: `Read git status with NUL separators so paths are not escaped`.
- Do NOT push, open a PR, or run this repository's own `/commit`, `/push`, or `/release` skills unless the operator instructed it.

## Steps

### Step 1: Record the baseline

**Verify**: `uv run --with pytest pytest -q` → all pass. Write down the count (`77` on a clean `5978324`, `82` if plans 001 and 002 already landed).

Any failing test at this point is a STOP condition.

### Step 2: Add the failing test for a non-ASCII untracked path

Append to `tests/test_ship.py`. This test fails before the fix and passes after.

```python
def test_plan_commit_reports_a_non_ascii_path_unescaped(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "skäl.md").write_text("reason\n", encoding="utf-8")
    (repo / "README.md").write_text("hello world\n", encoding="utf-8")

    result = _ship(repo, "plan", "commit")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["untracked"] == ["skäl.md"]
    assert plan["tracked"] == ["README.md"]
```

**Verify**: `uv run --with pytest pytest tests/test_ship.py::test_plan_commit_reports_a_non_ascii_path_unescaped -q`
→ **1 failed**, on the `untracked` assertion, with the actual value `['"sk\\303\\244l.md"']`.

If the actual value is already `['skäl.md']`, the environment has `core.quotepath=false` configured globally, which masks the bug. That is a STOP condition — report it, because the fix is still needed for users who do not have that setting.

### Step 3: Add the failing test for a rename

A rename emits two NUL fields; the parser must report the new path once and not invent an entry from the old one.

```python
def test_plan_commit_reports_a_renamed_path_once(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "proj")
    (repo / "gammal fil.txt").write_text("content\n", encoding="utf-8")
    _git(repo, "add", "gammal fil.txt")
    _git(repo, "commit", "-m", "Add a file")
    _git(repo, "mv", "gammal fil.txt", "ny fil.txt")

    result = _ship(repo, "plan", "commit")

    assert result.returncode == 0, result.stderr
    plan = json.loads(result.stdout)
    assert plan["staged"] == ["ny fil.txt"]
    assert plan["tracked"] == []
    assert plan["untracked"] == []
```

**Verify**: `uv run --with pytest pytest tests/test_ship.py::test_plan_commit_reports_a_renamed_path_once -q` → **1 failed.**

Report the actual `plan` dict in your notes; the pre-fix value depends on how git chose to render the rename, and the reviewer will want it.

### Step 4: Rewrite `status_paths` to split on NUL

Replace the function at `ship.py:147-166`. Keep the name, the signature, the return-tuple order, and the classification logic exactly as they are — the only thing changing is how fields are obtained.

Target shape:

```python
def status_paths(cwd: Path) -> tuple[list[str], list[str], list[str]]:
    """Return (staged, tracked unstaged, untracked) paths from porcelain.

    Reads the NUL-separated form: git C-quotes any path with a byte outside
    ASCII in its default output, and these paths are shown to the user to
    confirm before a commit, so they have to arrive as themselves.
    """

    staged: list[str] = []
    tracked: list[str] = []
    untracked: list[str] = []

    # A rename or copy spends a second field on the original path. Walk the
    # fields by index so that one can be consumed rather than parsed as an
    # entry of its own.
    fields = git(cwd, "status", "--porcelain", "-z", "-uall").split("\0")
    index = 0
    while index < len(fields):
        entry = fields[index]
        index += 1
        if len(entry) < 4:
            continue
        code = entry[:2]
        path = entry[3:]
        if "R" in code or "C" in code:
            index += 1

        if code == "??":
            untracked.append(path)
        elif code[0] != " " and code[0] != "?":
            staged.append(path)
            if code[1] != " ":
                tracked.append(path)
        else:
            tracked.append(path)

    return staged, tracked, untracked
```

Three details that matter:

- `split("\0")` on git's output yields a trailing empty string, because every entry is NUL-*terminated* rather than NUL-separated. The `len(entry) < 4` guard skips it. It also skips the empty string that a clean tree produces. This guard is the reason the function needs no separate empty-output special case.
- `index += 1` inside the `R`/`C` branch consumes the original-path field. Do not read it — nothing downstream wants it, and the old code did not report it either. Note that this happens *before* classification, so an `RM` entry (staged rename plus a further worktree edit) still lands in both `staged` and `tracked` exactly as it does today.
- The classification block is copied verbatim from the current implementation, including `code[0] != " " and code[0] != "?"`. Resist tidying it into `code[0] not in " ?"` in this plan: a behaviour-preserving change is easier to review when the preserved part is textually identical.

**Verify**: `uv run --with pytest pytest tests/test_ship.py -q` → baseline-for-this-file `+ 2` passed, `0 failed`. Both new tests pass and all pre-existing ones still do.

### Step 5: Confirm the suite, types, and formatting

**Verify**, in order — every one must hold:

1. `uv run --with pytest pytest -q` → step 1's baseline `+ 2` passed, `0 failed`
2. `uvx mypy --strict skills/code/commit/scripts/ship.py skills/kntnt/scripts/kntnt.py` → `Success: no issues found in 2 source files`
3. `uvx ruff check .` → `All checks passed!`
4. `uvx ruff format --check .` → exit 0. If it reports either changed file would be reformatted, run `uvx ruff format` on that file and re-check.
5. `git status --porcelain` → only ` M skills/code/commit/scripts/ship.py` and ` M tests/test_ship.py`
6. `grep -n '" -> "' skills/code/commit/scripts/ship.py` → no matches. The text-marker rename split is gone.
7. `grep -c 'dependencies = \[\]' skills/code/commit/scripts/ship.py` → `1`

### Step 6: Confirm by hand that the user-facing plan is readable

Work in a temporary directory outside this repository.

```sh
cd "$(mktemp -d)"
git init -q -b main . && git config user.email t@e.com && git config user.name T
printf 'a\n' > "gammal näme.txt" && printf 'b\n' > keep.txt
git add -A && git commit -qm init
git mv "gammal näme.txt" "ny näme.txt"
printf 'c\n' > "otäckt ö.txt"
printf 'x\n' >> keep.txt
uv run <ABSOLUTE PATH TO>/skills/code/commit/scripts/ship.py plan commit
```

**Verify**: the plan's `staged` is `["ny näme.txt"]`, `tracked` is `["keep.txt"]`, and `untracked` is `["otäckt ö.txt"]` — every path spelled the way the filesystem spells it, no backslash escapes, no stray entry from the rename's original path. Paste those three arrays into your report.

Delete the temporary directory afterwards.

## Test plan

Two new tests in `tests/test_ship.py`, appended after the last `apply publish` test (`tests/test_ship.py:432-466`, or after plan 001's additions if those landed) and **before** the three `SKILL.md` prose assertions at `tests/test_ship.py:469-497` — those read as a closing group and should stay last.

| Test | Covers | Before | After |
|---|---|---|---|
| `test_plan_commit_reports_a_non_ascii_path_unescaped` | a path with non-ASCII bytes arrives unescaped, and a plain ASCII sibling is still classified correctly | FAIL | PASS |
| `test_plan_commit_reports_a_renamed_path_once` | a rename yields exactly the new path, and its original-path field is consumed rather than parsed | FAIL | PASS |

Structural pattern: `test_plan_commit_is_ready_when_only_untracked` (`tests/test_ship.py:94`).

The three existing tests named under "Callers" are the regression guards for classification; they are already in the suite and must keep passing without modification.

Not covered, deliberately: a path containing a literal newline or a double quote. `-z` handles both correctly by construction, but a test would have to create such a file, which is awkward on some filesystems and adds nothing over the non-ASCII case. Noted as a follow-up instead.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `uv run --with pytest pytest -q` reports step 1's baseline `+ 2` passed and `0 failed`
- [ ] `grep -c "^def test_" tests/test_ship.py` returns the step-1 count for that file `+ 2`
- [ ] `uvx mypy --strict skills/code/commit/scripts/ship.py skills/kntnt/scripts/kntnt.py` reports `Success: no issues found in 2 source files`
- [ ] `uvx ruff check .` exits 0 with `All checks passed!`
- [ ] `uvx ruff format --check .` exits 0
- [ ] `grep -n '" -> "' skills/code/commit/scripts/ship.py` returns no matches
- [ ] `grep -n 'splitlines' skills/code/commit/scripts/ship.py` shows no match inside `status_paths` (other functions may still use it legitimately — `make_targets` and `toml_version` do)
- [ ] `git diff --stat` lists exactly two files: `skills/code/commit/scripts/ship.py` and `tests/test_ship.py`
- [ ] `git diff -- skills/code/commit/scripts/ship.py` shows changes confined to `status_paths` — no other function touched
- [ ] Step 6's three arrays pasted into the report
- [ ] `plans/README.md` status row for 003 updated

## STOP conditions

Stop and report back (do not improvise) if:

- The step 1 baseline has any failing test.
- The `status_paths` excerpt in "Current state" does not match the live code — the file drifted since `5978324`.
- Step 2's test passes before the fix. Your git has `core.quotepath=false` set globally, so the bug is masked in your environment and you cannot demonstrate the fix. Report it rather than working around it by changing git config, which would only hide it again.
- Making the new tests pass appears to require changing the staged/tracked/untracked classification, or changing `apply_commit`. It does not — only the field-reading changes.
- Any of the three regression tests named under "Callers" fails after your change. That means the classification moved; revert to the verbatim classification block from the target shape.
- `git status --porcelain -z` is unavailable or behaves differently in your git version. Report `git --version` and the raw output of `git status --porcelain -z -uall | tr '\\0' '\\n'` in the step 6 fixture.

## Maintenance notes

- **The `index += 1` in the `R`/`C` branch is load-bearing.** Drop it and every rename injects a phantom entry built from the original path's first two characters. There is no type error and no crash — just a wrong list in front of the user. `test_plan_commit_reports_a_renamed_path_once` is the guard; its `plan["tracked"] == []` assertion is the part that catches it.
- **Why the check reads both columns**: git 2.55 only ever puts the rename marker in the first column, so `code[0] in {"R", "C"}` would be correct today. Both columns are tested because it costs nothing and no other two-column code contains `R` or `C`. If a future git reports an unstaged rename as ` R` with a paired field, this already handles it.
- **`-z` and quoting are a pair.** If someone ever reverts to `--porcelain` without `-z` — for readability, say — the escaping comes straight back. The docstring says why; keep it.
- **Reviewer should scrutinize**: that the classification block is textually identical to the pre-change version, and that the `len(entry) < 4` guard handles both the trailing empty field and a clean tree. A clean tree yields `""` from `split`, which the guard skips, leaving three empty lists and `dirty` false — that path is covered by the existing `test_plan_commit_exits_when_tree_is_clean` (`tests/test_ship.py:106`).
- **Interaction to watch**: if `commit_subjects` (`ship.py:214`) is ever changed to include file names, it will need the same treatment — `--format` output is not quoted, but `--name-only` paths are.
- **Deliberately deferred**: a test for paths containing a literal `"` or newline; porcelain v2 (`--porcelain=v2`), which carries richer per-entry data and would be the move if the plan ever needs to show more than a path list.
