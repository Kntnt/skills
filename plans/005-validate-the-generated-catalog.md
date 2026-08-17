# Plan 005: Fail Catalog generation on an entry that cannot carry its own name or description

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Drift check (run first)**: `git diff --stat 5978324..HEAD -- skills/kntnt/scripts/kntnt.py tests/test_kntnt.py skills/kntnt/catalog.json`
> No other plan in this set touches these files, so expect no difference. If any
> of them changed, compare the "Current state" excerpts against the live code
> before proceeding; on a mismatch, treat it as a STOP condition.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none (independent of plans 001–004; can land in any order)
- **Category**: bug
- **Planned at**: commit `5978324`, 2026-08-17

## Why this matters

`skills/kntnt/catalog.json` is the Catalog — the collection's declared list of its skills, generated from the skills' own frontmatter and shipped with the Manager. `CONTEXT.md:66-68` defines it, and `docs/adr/0012-skill-owns-dependencies.md` explains why it is generated rather than hand-written: "The Catalog is generated from those files so Status and Update can see the graph."

Two fields in each entry are the only thing a user sees **before** a skill is on disk:

- `name` is what `add_skills` passes to the transport as `--skill <name>` (`skills/kntnt/scripts/kntnt.py:511-512`). The transport resolves a skill by its **directory** name. A frontmatter `name` that differs from its directory therefore produces a Catalog entry that Enable cannot install — the failure surfaces as an opaque transport error at the moment a user tries to enable it.
- `description` is what `/kntnt status` prints (`kntnt.py:582`), what the Enable and Disable pickers show (`kntnt.py:612`), and the *entire* help text for a skill that is not yet enabled (`kntnt.py:1026-1027`).

Generation already fails loudly on one class of bad input — a misspelt Capability — and `kntnt.py:1046-1049` says exactly why:

```python
        # Generation is where a misspelt Capability has to fail. Past this
        # point the name would ride into the Catalog and only surface when a
        # user ran the skill.
        capability_notes(deps["capabilities"])
```

That reasoning applies unchanged to the name and the description, and neither is checked. An empty description ships silently and every user's picker shows a blank line. A `description:` written as a YAML folded scalar ships the literal indicator character, because the frontmatter parser in this script supports no block scalars — also silently.

This plan extends the existing "fail at generation" boundary to cover the two fields the Catalog exists to carry. It changes no runtime behaviour for any correct skill.

## Current state

### Files

- `skills/kntnt/scripts/kntnt.py` — the Manager engine. `generate_catalog` is the only function you will change.
- `tests/test_kntnt.py` — the CLI-level pytest suite for that engine. You will add three tests.

### `generate_catalog`, `kntnt.py:1033-1061`

```python
def generate_catalog(source: Path) -> dict[str, Any]:
    """Build a Catalog from SKILL.md files under *source*/skills."""

    entries: list[dict[str, Any]] = []
    skills_root = source / "skills"
    for skill_md in sorted(skills_root.glob("*/*/SKILL.md")):
        category = skill_md.parent.parent.name
        frontmatter = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = str(frontmatter.get("name") or skill_md.parent.name)
        if name == MANAGER:
            continue
        deps = skill_deps(frontmatter)

        # Generation is where a misspelt Capability has to fail. Past this
        # point the name would ride into the Catalog and only surface when a
        # user ran the skill.
        capability_notes(deps["capabilities"])
        entries.append(
            {
                "name": name,
                "category": category,
                "description": str(frontmatter.get("description") or ""),
                "binaries": deps["binaries"],
                "skills": deps["skills"],
                "externals": deps["externals"],
                "capabilities": deps["capabilities"],
            }
        )
    return {"origin": ORIGIN, "skills": entries}
```

Note the glob is `*/*/SKILL.md` — two levels below `skills/`, i.e. `skills/<category>/<skill>/SKILL.md`. The Manager itself lives at `skills/kntnt/SKILL.md`, one level, so it is never matched; the `if name == MANAGER: continue` guards only against a skill inside a category directory claiming the name `kntnt`.

### Its caller, `kntnt.py:1064-1078`

```python
def cmd_catalog(*, write: bool) -> int:
    """Print a generated Catalog from a local collection source."""

    source = Path(collection_source())
    if not source.is_dir():
        raise ManagerError(
            "KNTNT_SOURCE must be a local collection to generate the Catalog"
        )
    catalog = generate_catalog(source)
    text = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    if write:
        path = here() / "catalog.json"
        path.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0
```

`ManagerError` (`kntnt.py:64-69`) carries a message and an exit code defaulting to 1; `main` (`kntnt.py:1205-1208`) catches it and turns it into `fail()` plus that code. So raising `ManagerError` from `generate_catalog` produces `error: <message>` on stderr and exit 1 — which is exactly what `capability_notes` already does via `kntnt.py:290`.

### Why a folded description is silently wrong

The frontmatter parser is a restricted YAML subset, `kntnt.py:172-181` and `kntnt.py:195-249`:

```python
def parse_yaml_scalar(raw: str) -> Any:
    """Parse a YAML scalar used in skill frontmatter."""

    if raw in {"true", "True"}:
        return True
    if raw in {"false", "False"}:
        return False
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {"'", '"'}:
        return raw[1:-1]
    return raw
```

Its docstring at `kntnt.py:196` states the contract: "Parse a restricted YAML subset: maps, lists of scalars, scalars." Block and folded scalars are not in that subset. A frontmatter line `description: >` followed by an indented paragraph therefore yields the one-character string `">"` as the description, and the following indented lines are parsed as something else entirely. The value ships to every user.

An **empty** `description:` takes a different path and lands in the same place: with no value on the line, `parse_simple_yaml` opens a nested map (`kntnt.py:238-246`), so `frontmatter["description"]` becomes `{}`, and `str(frontmatter.get("description") or "")` renders it as `""`.

Both were run through the real parser at commit `5978324` before this plan was written, so the values below are observed rather than reasoned:

| frontmatter line | `frontmatter["description"]` | what reaches the Catalog |
|---|---|---|
| `description: ` | `{}` | `""` |
| `description: >` | `">"` | `">"` |
| `description: >-` | `">-"` | `">-"` |
| `description: A collection skill.` | `"A collection skill."` | `"A collection skill."` |

### The current Catalog passes all three proposed checks

Every entry in `skills/kntnt/catalog.json` has a non-empty single-line description, and every skill's frontmatter `name` matches its directory: `agents-md`, `delegation`, `commit`, `push`, `release`. So this plan must leave the shipped Catalog byte-identical — `test_shipped_catalog_matches_the_generated_one` (`tests/test_kntnt.py:842-857`) is the guard, and it must keep passing without regenerating anything.

### Conventions this file follows — match them exactly

From `docs/coding-standard/general.md` and `docs/coding-standard/python.md`, as practised in `kntnt.py`:

- **Docstring, then a blank line, then the body.** Every function does it:
  ```python
  def capability_notes(names: list[str]) -> list[dict[str, str]]:
      """Describe each required Capability so the agent can answer for itself."""

      notes: list[dict[str, str]] = []
      ...
  ```
- Full type hints on every signature and module-level constant.
- Errors raise `ManagerError` (`kntnt.py:64-69`), never print. `ManagerError(msg)` exits 1; `ManagerError(msg, 2)` exits 2. **Use the default 1 here** — exit 2 in this script means "the user must do something first" (`kntnt.py:426`, `kntnt.py:675`), while a malformed skill is a maintainer's bug.
- Module-level constants in `SCREAMING_SNAKE_CASE`, grouped at the top of the file (`kntnt.py:21-41`). `DEP_KINDS` at `kntnt.py:263` shows that a constant may also sit next to the code that uses it when that reads better.
- `pathlib.Path`, f-strings, early returns, no bare `except`.
- Paragraph comments: a `#` topic sentence above a paragraph whose *purpose* is not evident. `kntnt.py:1046-1048` and `kntnt.py:31-35` show the density and the register — they explain *why*, never *what*.
- Standard library only. The PEP 723 header (`kntnt.py:1-4`) declares `dependencies = []` and must stay that way. In particular: do not reach for PyYAML to fix the parser. That is a much larger decision than this plan, and the parser's limits are documented, not accidental.

Test conventions (`tests/test_kntnt.py`) — the helpers already exist, do not write new ones:

- `_world(tmp_path, entries=None)` (`tests/test_kntnt.py:83-128`) builds an isolated world: a fake home, a fake project, and a **fake collection source** at `world["source"]` containing `skills/<category>/<name>/SKILL.md` for each entry plus a Manager copy. With `entries=None` it creates `alpha` (category `code`), `beta` (`code`), and `gamma` (`text`).
- `_skill_md(name, *, description="A collection skill.", binaries=None, skills=None, externals=None, capabilities=None, help_body="")` (`tests/test_kntnt.py:23-55`) renders a SKILL.md. It writes `description: {description}` **unquoted**, which is what lets you produce both an empty and a folded description by passing `""` or `">"`.
- `_write(path, text)` (`tests/test_kntnt.py:18-20`) writes a file, creating parents.
- `_run(world, *args, cwd=None)` (`tests/test_kntnt.py:131-148`) runs the Manager with `KNTNT_HOME`, `KNTNT_SOURCE`, `KNTNT_PROJECT`, `KNTNT_HARNESS_PATHS`, and `KNTNT_TRANSPORT` pointed at the isolated world, `check=False`. **`KNTNT_SOURCE` is `world["source"]`, so `_run(world, "catalog")` generates from the fake collection** — that is how these tests stay off the real repository.
- Arrange-Act-Assert with a blank line between the parts. Test functions carry a docstring only when the *reason* is not obvious from the name — see `tests/test_kntnt.py:559-560` and `842-843`. Two of your three tests warrant one.

Use `test_check_rejects_an_unknown_capability` (`tests/test_kntnt.py:559-569`) as the structural pattern for a "generation must refuse" test:

```python
def test_check_rejects_an_unknown_capability(tmp_path: Path) -> None:
    """A misspelt Capability must refuse, not pass as a check that never runs."""

    world = _world(tmp_path)
    skill = world["project"] / "skill"
    _write(skill / "SKILL.md", _skill_md("alpha", capabilities=["telepathy"]))

    result = _run(world, "check", "--here", str(skill))

    assert result.returncode == 1
    assert "telepathy" in result.stderr
```

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Full suite | `uv run --with pytest pytest -q` | `77 passed` before this plan on a clean `5978324`; `+3` after |
| This engine only | `uv run --with pytest pytest tests/test_kntnt.py -q` | `50 passed` before; `53 passed` after |
| Lint | `uvx ruff check .` | `All checks passed!` |
| Format | `uvx ruff format --check .` | exit 0 |
| Types | `uvx mypy --strict skills/kntnt/scripts/kntnt.py` | `Success: no issues found in 1 source file` |
| Generate the real Catalog | `KNTNT_SOURCE="$PWD" uv run skills/kntnt/scripts/kntnt.py catalog` | prints JSON, exit 0 |

If plans 001–004 have already landed, the suite baseline is higher and `mypy` may be configured through `pyproject.toml` so that `--strict` is redundant. **Record the baseline from step 1** and check the final count against `baseline + 3`.

## Scope

**In scope**:

- `skills/kntnt/scripts/kntnt.py` — `generate_catalog` only, plus one module-level constant
- `tests/test_kntnt.py` — three new tests appended

**Out of scope** (do NOT touch, even though they look related):

- `parse_simple_yaml`, `parse_yaml_scalar`, `parse_frontmatter` (`kntnt.py:172-260`) — **do not extend the YAML parser.** This plan makes an unsupported construct fail loudly; teaching the parser to handle folded scalars is a different, larger change with its own risk, and `docs/coding-standard/general.md:20` (YAGNI) argues against it while no skill needs one.
- `skills/kntnt/catalog.json` — must stay byte-identical. If your change alters it, something is wrong.
- Any `SKILL.md` under `skills/` — all five pass the new checks already. If one does not, that is a STOP condition, not a file to edit here.
- `skill_deps`, `capability_notes`, `CAPABILITIES` — the capability check already works and is the precedent this plan follows, not something to modify.
- `status_payload`, `picker_payload`, `cmd_help` — the consumers of `description`. They are correct; the data reaching them was not. Do not add fallback text there: a blank description must fail at generation, not be papered over at display time.
- `CHANGELOG.md` — do not add an entry by hand; this repository's `commit` skill reconciles it at commit time.

## Git workflow

- Branch: `advisor/005-validate-generated-catalog`
- One commit — one concern (`CONTRIBUTING.md:24`).
- Commit messages: imperative, sentence case, no conventional-commit prefix (`git log`: `Add the kntnt manager skill.`). Suggested: `Refuse to generate a Catalog entry with no usable name or description`.
- Do NOT push, open a PR, or run this repository's own `/commit`, `/push`, or `/release` skills unless the operator instructed it.

## Steps

### Step 1: Record the baseline

**Verify**:

1. `uv run --with pytest pytest -q` → all pass. Write down the count.
2. `KNTNT_SOURCE="$PWD" uv run skills/kntnt/scripts/kntnt.py catalog > /tmp/catalog-before.json; echo $?` → `0`
3. `python3 -c "import json,sys; a=json.load(open('/tmp/catalog-before.json')); b=json.load(open('skills/kntnt/catalog.json')); print('identical' if a==b else 'DRIFT')"` → `identical`

Keep `/tmp/catalog-before.json`; step 5 compares against it. Any failing test, or `DRIFT`, is a STOP condition.

### Step 2: Add the name-mismatch test

Append to `tests/test_kntnt.py`. Add a skill whose frontmatter name disagrees with its directory, then generate.

```python
def test_catalog_generation_rejects_a_name_that_is_not_the_directory(
    tmp_path: Path,
) -> None:
    """The transport installs by directory, so a Catalog name that differs cannot resolve."""

    world = _world(tmp_path)
    _write(
        world["source"] / "skills" / "code" / "delta" / "SKILL.md",
        _skill_md("epsilon"),
    )

    result = _run(world, "catalog")

    assert result.returncode == 1
    assert "epsilon" in result.stderr
    assert "delta" in result.stderr
```

**Verify**: `uv run --with pytest pytest tests/test_kntnt.py::test_catalog_generation_rejects_a_name_that_is_not_the_directory -q`
→ **1 failed**, on `assert result.returncode == 1`, with an actual return code of `0` — generation currently accepts the mismatch.

### Step 3: Add the empty-description and folded-description tests

```python
def test_catalog_generation_rejects_an_empty_description(tmp_path: Path) -> None:
    world = _world(tmp_path)
    _write(
        world["source"] / "skills" / "code" / "alpha" / "SKILL.md",
        _skill_md("alpha", description=""),
    )

    result = _run(world, "catalog")

    assert result.returncode == 1
    assert "description" in result.stderr
    assert "alpha" in result.stderr


def test_catalog_generation_rejects_a_folded_description(tmp_path: Path) -> None:
    """parse_simple_yaml has no block scalars, so a folded description ships as '>'."""

    world = _world(tmp_path)
    _write(
        world["source"] / "skills" / "code" / "alpha" / "SKILL.md",
        _skill_md("alpha", description=">"),
    )

    result = _run(world, "catalog")

    assert result.returncode == 1
    assert "alpha" in result.stderr
```

**Verify**: `uv run --with pytest pytest tests/test_kntnt.py -k "empty_description or folded_description" -q` → **2 failed**, both on the return-code assertion with an actual `0`.

At this point three of your tests fail and nothing else does. Record the three failure messages — `docs/coding-standard/general.md:23` asks for the red step as an artifact, not an inference.

### Step 4: Validate in `generate_catalog`

Add the constant next to the code that uses it, immediately above `generate_catalog` (`kntnt.py:1033`), following the placement of `DEP_KINDS` at `kntnt.py:263`:

```python
# The frontmatter parser reads a restricted YAML subset with no block scalars,
# so `description: >` yields this indicator as the value. Generation is where
# that has to fail: past it the character ships as the skill's whole help text.
BLOCK_SCALARS = frozenset({">", "|", ">-", "|-", ">+", "|+"})
```

Then hoist the description into a local and validate both fields. The three checks go **after** the `if name == MANAGER: continue` guard and alongside the existing `capability_notes` call, so all four of generation's refusals sit together:

```python
        deps = skill_deps(frontmatter)
        description = str(frontmatter.get("description") or "")

        # Generation is where a misspelt Capability has to fail. Past this
        # point the name would ride into the Catalog and only surface when a
        # user ran the skill. The same is true of the two fields the Catalog
        # exists to carry: the transport installs by directory name, and the
        # description is a skill's entire help until it is Enabled.
        capability_notes(deps["capabilities"])
        if name != skill_md.parent.name:
            raise ManagerError(
                f"{skill_md}: name '{name}' is not the directory "
                f"'{skill_md.parent.name}'; the transport installs by directory"
            )
        if not description:
            raise ManagerError(f"{skill_md}: description is empty")
        if description in BLOCK_SCALARS:
            raise ManagerError(
                f"{skill_md}: description '{description}' is a YAML block "
                "scalar, which the frontmatter parser does not support; "
                "write it on one line"
            )
```

Then use the local in the entry dict, replacing the inline `str(frontmatter.get("description") or "")`:

```python
                "description": description,
```

Two things to get right:

- Rewrite the existing comment as shown rather than adding a second one beside it. One paragraph, one topic sentence — `docs/coding-standard/general.md:48-52`.
- The error messages interpolate `skill_md`, the full path, so a maintainer running `catalog` over a large collection is told which file to open. Both `name` and the directory name appear, because "these two disagree" is unactionable without both.

**Verify**: `uv run --with pytest pytest tests/test_kntnt.py -q` → step 1's file baseline `+ 3` passed, `0 failed`.

### Step 5: Confirm the shipped Catalog did not move

This is the check that proves the plan changed nothing for correct skills.

**Verify**:

1. `KNTNT_SOURCE="$PWD" uv run skills/kntnt/scripts/kntnt.py catalog > /tmp/catalog-after.json; echo $?` → `0`
2. `diff /tmp/catalog-before.json /tmp/catalog-after.json` → no output
3. `diff <(KNTNT_SOURCE="$PWD" uv run skills/kntnt/scripts/kntnt.py catalog) skills/kntnt/catalog.json` → no output
4. `git diff --stat -- skills/kntnt/catalog.json` → empty

If any of these shows a difference, one of the five shipped skills fails a check you just added — STOP and report which.

### Step 6: Confirm the suite, types, and formatting

**Verify**, in order:

1. `uv run --with pytest pytest -q` → step 1's baseline `+ 3` passed, `0 failed`
2. `uvx mypy --strict skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py` → `Success: no issues found in 2 source files`
3. `uvx ruff check .` → `All checks passed!`
4. `uvx ruff format --check .` → exit 0. If it reports either changed file would be reformatted, run `uvx ruff format` on it and re-check.
5. `git status --porcelain` → only ` M skills/kntnt/scripts/kntnt.py` and ` M tests/test_kntnt.py`
6. `grep -c 'dependencies = \[\]' skills/kntnt/scripts/kntnt.py` → `1`

### Step 7: Confirm the failure message is useful to a human

Run generation over a deliberately broken copy, outside this repository, and read the message as a maintainer would.

```sh
cp -R . "$(mktemp -d)/broken" && cd "$_"
mkdir -p skills/code/typo
printf -- '---\nname: mistyped\ndescription: A skill.\n---\n\n# typo\n' > skills/code/typo/SKILL.md
KNTNT_SOURCE="$PWD" uv run skills/kntnt/scripts/kntnt.py catalog; echo "exit=$?"
```

**Verify**: exit `1`, and stderr names the path `skills/code/typo/SKILL.md`, the frontmatter name `mistyped`, and the directory `typo`. Paste the message into your report.

Delete the temporary directory afterwards. (`cp -R .` copies `.git` too; that is harmless here since nothing commits, but do not run any git command inside the copy.)

## Test plan

Three new tests in `tests/test_kntnt.py`, appended at the end of the file after `test_delegation_requires_subagents_and_says_so` (`tests/test_kntnt.py:860-871`). The last three tests in that file are already repository-fact assertions, so generation-validation tests sit naturally beside them.

| Test | Covers | Before | After |
|---|---|---|---|
| `test_catalog_generation_rejects_a_name_that_is_not_the_directory` | frontmatter name must equal the directory the transport installs by | FAIL | PASS |
| `test_catalog_generation_rejects_an_empty_description` | a blank description cannot ship to Status, the pickers, or help | FAIL | PASS |
| `test_catalog_generation_rejects_a_folded_description` | an unsupported YAML construct fails at generation instead of shipping `>` | FAIL | PASS |

Structural pattern: `test_check_rejects_an_unknown_capability` (`tests/test_kntnt.py:559`).

The positive case needs no new test: `test_shipped_catalog_matches_the_generated_one` (`tests/test_kntnt.py:842`) already generates the real Catalog and compares it byte for byte, so it fails if any of the five shipped skills trips a new check. Step 5 verifies the same thing by hand.

Not covered, deliberately: a `description` that is a multi-line block whose *indicator* is followed by content (e.g. `description: >-` with an indented paragraph). The indicator itself is caught by `BLOCK_SCALARS`, which is the whole reachable failure; asserting on how `parse_simple_yaml` mangles the following lines would pin down parser behaviour this plan explicitly does not intend to keep stable.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `uv run --with pytest pytest -q` reports step 1's baseline `+ 3` passed, `0 failed`
- [ ] `grep -c "^def test_" tests/test_kntnt.py` returns `53`
- [ ] `diff <(KNTNT_SOURCE="$PWD" uv run skills/kntnt/scripts/kntnt.py catalog) skills/kntnt/catalog.json` produces no output
- [ ] `git diff --stat -- skills/kntnt/catalog.json` is empty
- [ ] `git diff --stat` lists exactly two files: `skills/kntnt/scripts/kntnt.py` and `tests/test_kntnt.py`
- [ ] `git diff -- skills/kntnt/scripts/kntnt.py` shows changes confined to `generate_catalog` and one new module-level constant — no other function touched
- [ ] `grep -c 'BLOCK_SCALARS' skills/kntnt/scripts/kntnt.py` returns `2` (the definition and its one use)
- [ ] `uvx mypy --strict skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py` reports `Success: no issues found in 2 source files`
- [ ] `uvx ruff check .` exits 0 with `All checks passed!`
- [ ] `uvx ruff format --check .` exits 0
- [ ] `grep -c 'dependencies = \[\]' skills/kntnt/scripts/kntnt.py` returns `1` — no new dependency
- [ ] The three red-step failure messages and step 7's message are quoted in the report
- [ ] `plans/README.md` status row for 005 updated

## STOP conditions

Stop and report back (do not improvise) if:

- Step 1's baseline has any failing test, or step 1.3 prints `DRIFT` — the shipped Catalog is already out of step with the skills, and that must be understood before this plan adds checks on top of it.
- The `generate_catalog` excerpt in "Current state" does not match the live code — the file drifted since `5978324`.
- Any test from steps 2 or 3 **passes** before you make the change in step 4. Generation is then already validating something; report what, and do not weaken the test.
- Step 5 shows the shipped `catalog.json` changing. One of the five real skills fails a check you added. Report which skill and which check — do **not** edit the skill's `SKILL.md` or regenerate the Catalog to make the diff go away, because that would ship a Catalog change inside a plan scoped to validation.
- You conclude the YAML parser must be extended, or PyYAML added, to satisfy a test. It must not: `BLOCK_SCALARS` catches the indicator as a plain string, no parsing change required.
- Adding `description` as a local variable causes a mypy error. It should be `str` by construction; report the error rather than adding a cast.

## Maintenance notes

- **These checks are a build-time boundary, not runtime validation.** They run in `generate_catalog`, reached only through `/kntnt catalog`, which is a maintainer verb — it is absent from `MANAGER_HELP` (`kntnt.py:42-61`) and from `skills/kntnt/SKILL.md`'s argument list on purpose. A user never hits them. The invariant they protect is "a shipped Catalog can always be acted on", and the thing that enforces it in practice is `test_shipped_catalog_matches_the_generated_one`, which regenerates on every test run.
- **`BLOCK_SCALARS` is a symptom check, not a fix.** It exists because `parse_simple_yaml` handles a documented subset of YAML (`kntnt.py:196`). If someone ever does teach the parser folded scalars, this constant and its check should be deleted in the same change — leaving a refusal for a construct the parser now supports would be worse than the original bug.
- **Reviewer should scrutinize**: that `skills/kntnt/catalog.json` is untouched in the diff (the plan's whole claim is that correct skills are unaffected), and that the name check compares against `skill_md.parent.name` rather than re-deriving the directory some other way — it must be the same value the `name` fallback uses at `kntnt.py:1041`, or the check can contradict itself.
- **Adding a new skill to the collection** now requires the frontmatter `name` to match the directory. That was always effectively true — the transport resolves by directory — but it was unstated and unenforced. Worth a line in `CONTRIBUTING.md` if anyone contributes a skill; `plans/006-fix-contributing-doc-errors.md` owns that file and does not currently add one, so this is a follow-up rather than part of either plan.
- **Deliberately deferred**: validating `category` (it is derived from the directory and cannot be wrong); rejecting a description over some length; and checking that a declared `skills` dependency names another Catalog entry, which would catch a typo in a dependency list the same way this catches one in a capability list. That last one is the most valuable follow-up here.
