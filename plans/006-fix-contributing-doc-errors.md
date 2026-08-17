# Plan 006: Correct `CONTRIBUTING.md` — the project's own name, where its code lives, and how to verify it

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Prerequisite**: `plans/004-add-ci-and-tooling-config.md` should land first,
> because step 4 documents the commands that plan wires into CI, and the two
> must match character for character. If 004 has not landed, step 4 tells you
> what to do instead.
>
> **Drift check (run first)**: `git diff --stat 5978324..HEAD -- CONTRIBUTING.md`
> No other plan in this set touches this file, so expect no difference. If it
> changed, compare the "Current state" excerpts against the live file before
> proceeding; on a mismatch, treat it as a STOP condition.

## Status

- **Priority**: P3
- **Effort**: S
- **Risk**: LOW
- **Depends on**: `plans/004-add-ci-and-tooling-config.md` (soft — see step 4)
- **Category**: docs
- **Planned at**: commit `5978324`, 2026-08-17

## Why this matters

`CONTRIBUTING.md` is the first file a would-be contributor opens, and it currently gets three things wrong about the project it describes: it calls the project by another project's name, it points at a directory that does not exist, and it documents one verification command out of four. Each is small. Together they are the worst kind of documentation error — `docs/coding-standard/general.md` treats a stale doc as worse than a missing one, because a reader trusts it and acts on it.

The name error in particular reads as a copy-paste from a sibling repository, which is exactly what it is: the title says `kntnt-wp-skills` while this project is `Kntnt Skills` at `Kntnt/skills`. A contributor who greps for the project name finds nothing, or finds the wrong repository.

## Current state

### The file

`CONTRIBUTING.md`, 34 lines. Three defects, quoted verbatim.

**Defect 1 — `CONTRIBUTING.md:1`.** The title names a different project:

```markdown
# Contributing to kntnt-wp-skills
```

This project is `Kntnt Skills` — `README.md:1` is `# Kntnt Skills`, and the repository is `Kntnt/skills` (`README.md:3-4`, `CONTRIBUTING.md:23`). `kntnt-wp-skills` is a separate collection.

**Defect 2 — `CONTRIBUTING.md:26`.** The path is wrong:

```markdown
4. **Run the tests.** The Python helpers under `scripts/` are covered by a pytest suite under `tests/`. One command runs it, provisioning pytest through `uv`:
```

There is no top-level `scripts/` directory. Verified at commit `5978324` — the Python in this repository lives in three places:

- `skills/kntnt/scripts/kntnt.py` (1212 lines) — the Manager engine
- `skills/code/commit/scripts/ship.py` (683 lines) — the commit/push/release engine
- `tests/support/fake_skills.py` (188 lines) — a test double for the `npx skills` transport

The pattern is `skills/<category>/<skill>/scripts/`, not `scripts/`.

**Defect 3 — `CONTRIBUTING.md:26-30`.** One command of four is documented:

```markdown
   ```
   uv run --with pytest pytest
   ```
```

Four checks pass at commit `5978324` and all four are mandated by the project's own standard — `docs/coding-standard/python.md:44-49` requires ruff as "the single linter and formatter" and mypy or pyright with "Strict mode on new code":

| Command | Result at `5978324` |
|---|---|
| `uv run --with pytest pytest` | `77 passed` |
| `uvx ruff check .` | `All checks passed!` |
| `uvx ruff format --check .` | `61 files already formatted` |
| `uvx mypy --strict skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py` | `Success: no issues found in 2 source files` |

A contributor who runs only the documented command submits work the maintainer then has to lint by hand.

### What is correct and must not change

Do not "improve" these while you are in the file:

- `CONTRIBUTING.md:3` — the framing that this is *editorial guidance on what is likely to be merged, not a legal restriction*. Deliberate and load-bearing.
- `CONTRIBUTING.md:7-11` — the three-row contribution-scope table.
- `CONTRIBUTING.md:15` — the inbound-licensing paragraph citing Apache 2.0 §5. Legal text; leave it exactly as written.
- `CONTRIBUTING.md:25` — the pointer to `docs/coding-standard/`. Correct: that directory exists and holds `general.md` and `python.md`.
- `CONTRIBUTING.md:23` — the issue-tracker URL `https://github.com/Kntnt/skills/issues`. Correct.
- The four-item numbered structure of *How to contribute*, and the *Behaviour* and *Questions* sections.

### Conventions

- **Each paragraph is one physical line.** No hard wrapping at a column width — the wrapping newlines show up in some renderers and pollute diffs. Every Markdown file in this repository follows it; `CONTRIBUTING.md:9-11` has table rows several hundred characters long on single lines. Match this. Each list item is likewise its own single line.
- Fenced code blocks in this file carry **no language tag** — see `CONTRIBUTING.md:28-30`, and the same style in `README.md:38-40`. Keep that; do not add `sh` or `console`.
- Sentence case in headings; `##` for sections.
- British-leaning spelling is used in places (`behaviour`, `licence`) — `CONTRIBUTING.md:9`, `:17`, `:11`. Do not normalise it either way.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Full suite | `uv run --with pytest pytest -q` | all pass (`77` at `5978324`; more once plans 001–005 land) |
| Lint | `uvx ruff check .` | `All checks passed!` |
| Format | `uvx ruff format --check .` | exit 0 |
| Types | `uvx mypy --strict skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py` | `Success: no issues found in 2 source files` |

This plan changes only prose, so none of these can be broken by it. They are here because step 4 documents them and you must confirm each one actually works before writing it down.

## Scope

**In scope** (the only file you may modify):

- `CONTRIBUTING.md`

**Out of scope** (do NOT touch, even though they look related):

- `README.md` — its project name, install instructions, and skill descriptions are all correct.
- `docs/coding-standard/*.md` — these are the mandate; the doc that failed to reflect them is the one being fixed.
- `.github/workflows/ci.yml` and `pyproject.toml` — owned by `plans/004-add-ci-and-tooling-config.md`. If they do not exist yet, do not create them here.
- `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md` — correct, and `AGENTS.md` already points at `CONTRIBUTING.md` with `read when running tests or opening a PR`, which stays true.
- Any code or test. This plan writes prose only; `git diff --stat` must list exactly one file.
- The contribution-scope table, the licensing paragraph, and the Behaviour section — see "What is correct" above.
- `CHANGELOG.md` — do not add an entry by hand; this repository's `commit` skill reconciles it at commit time.

## Git workflow

- Branch: `advisor/006-fix-contributing-doc-errors`
- One commit — one concern (`CONTRIBUTING.md:24`, the rule this file states about itself).
- Commit messages: imperative, sentence case, no conventional-commit prefix (`git log`: `Add the kntnt manager skill.`). Suggested: `Name the right project and the real verification commands in CONTRIBUTING`.
- Do NOT push, open a PR, or run this repository's own `/commit`, `/push`, or `/release` skills unless the operator instructed it.

## Steps

### Step 1: Confirm the three defects are still present

**Verify**, all three:

1. `head -1 CONTRIBUTING.md` → `# Contributing to kntnt-wp-skills`
2. `grep -n 'under `scripts/`' CONTRIBUTING.md` → one match, on line 26
3. `test -d scripts && echo "EXISTS" || echo "absent"` → `absent`

If (1) or (2) does not match, the file has been edited since `5978324` — STOP. If (3) prints `EXISTS`, a top-level `scripts/` directory has been added and defect 2 is no longer a defect — STOP and report.

### Step 2: Fix the title

Change `CONTRIBUTING.md:1` from:

```markdown
# Contributing to kntnt-wp-skills
```

to:

```markdown
# Contributing to Kntnt Skills
```

`Kntnt Skills` matches `README.md:1` exactly. Do not use `Kntnt/skills` (that is the repository slug, used correctly at `CONTRIBUTING.md:3` and `:23`) and do not use `kntnt-skills`.

**Verify**: `head -1 CONTRIBUTING.md` → `# Contributing to Kntnt Skills`, and `grep -c 'kntnt-wp-skills' CONTRIBUTING.md` → `0`

### Step 3: Fix the path

In `CONTRIBUTING.md:26`, replace `The Python helpers under `scripts/`` with a description that matches the tree. Keep the numbered-item structure and the sentence's shape:

```markdown
4. **Run the tests.** The Python engines under `skills/<category>/<skill>/scripts/` are covered by a pytest suite under `tests/`. Four commands verify a change, each provisioning its tool through `uv`:
```

Note this line also sets up step 4 by saying **four** commands rather than one. Write the whole line in one edit rather than editing it twice.

**Verify**:

1. `grep -c 'under `scripts/`' CONTRIBUTING.md` → `0`
2. `grep -c 'skills/<category>/<skill>/scripts/' CONTRIBUTING.md` → `1`

### Step 4: Document all four verification commands

Replace the single-command fenced block at `CONTRIBUTING.md:28-30` with all four, in the same order CI runs them — cheapest first, so a contributor with a formatting slip learns it before waiting on the suite:

````markdown
   ```
   uvx ruff check .
   uvx ruff format --check .
   uvx mypy skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py
   uv run --with pytest pytest
   ```

   These are the same four checks CI runs on every pull request, so a green run locally means a green run there.
````

**Two variants, pick by what is on disk:**

- **If `pyproject.toml` exists** (plan 004 landed): use the `mypy` line exactly as written above, with **no `--strict` flag** — the configuration supplies it. Confirm with `grep -c 'strict' pyproject.toml` → `1`.
- **If `pyproject.toml` does not exist** (plan 004 has not landed): write the mypy line as `uvx mypy --strict skills/kntnt/scripts/kntnt.py skills/code/commit/scripts/ship.py`, and **omit** the trailing sentence about CI, since there is no CI to be consistent with. Note the substitution in your report so whoever lands plan 004 knows to revisit this line.

Mind the indentation: the fence sits inside numbered item 4, so it is indented three spaces to stay part of that item, exactly as the existing block at `CONTRIBUTING.md:28-30` is. The trailing sentence is indented three spaces for the same reason.

**Verify**, in order:

1. Run each of the four commands you wrote down, copied from the file, and confirm each exits 0. This is the point of the step: a documented command that does not work is a worse defect than the one being fixed.
2. `grep -c 'uvx ruff check .' CONTRIBUTING.md` → `1`
3. `grep -c 'uv run --with pytest pytest' CONTRIBUTING.md` → `1`
4. `grep -c 'uvx mypy' CONTRIBUTING.md` → `1`

### Step 5: Confirm the file is still internally consistent and nothing else moved

**Verify**, all of these:

1. `wc -l CONTRIBUTING.md` → between `36` and `40`. The file was 34 lines; you added the three command lines plus a blank line and a sentence. A count far outside that range means more changed than intended.
2. `git diff --stat` → exactly one file, `CONTRIBUTING.md`
3. `git diff -- CONTRIBUTING.md | grep -c '^+' ` → at most `12` (including the `+++` header). A larger number means you rewrote prose that was correct.
4. `grep -n 'Apache License 2.0 by virtue of its §5' CONTRIBUTING.md` → still present, unchanged
5. `grep -n 'docs/coding-standard/' CONTRIBUTING.md` → still present, unchanged
6. `grep -c 'One concern per PR' CONTRIBUTING.md` → `1`
7. `awk 'length > 0 && /^[^|#`-]/ && length < 60 && !/^[0-9]\./ {print NR": "$0}' CONTRIBUTING.md` — read the output and confirm no paragraph got hard-wrapped into short lines. Prose paragraphs in this file are single long lines.

### Step 6: Read it as a new contributor would

Read the finished `How to contribute` section start to finish. Confirm three things by eye — this step has no command because it is the one judgment this plan asks for:

- The four numbered items still read as a sequence a newcomer can follow in order.
- Item 4 no longer promises a directory that does not exist.
- Nothing in the file still refers to another project.

State in your report that you did this, and quote the final item 4 in full.

## Test plan

**No tests.** This plan changes prose only.

Do not add a test asserting `CONTRIBUTING.md` contains particular strings. There is precedent in this repository for asserting on Markdown — `tests/test_ship.py:469-497` and `tests/test_kntnt.py:807-871` do it — but each of those pins a *behavioural contract* the code depends on (that `commit` never pushes, that the Manager is user-invoked, that `delegation` declares its capability). A contributing guide's wording is not such a contract, and a test on it would ossify prose that should stay editable.

The real verification is step 4.1: every command written into the file is executed and must exit 0.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `grep -c 'kntnt-wp-skills' CONTRIBUTING.md` returns `0`
- [ ] `head -1 CONTRIBUTING.md` is exactly `# Contributing to Kntnt Skills`
- [ ] `grep -c 'under `scripts/`' CONTRIBUTING.md` returns `0`
- [ ] `grep -c 'skills/<category>/<skill>/scripts/' CONTRIBUTING.md` returns `1`
- [ ] All four of `uvx ruff check .`, `uvx ruff format --check .`, the mypy line as written in the file, and `uv run --with pytest pytest` exit 0 when copied out of the file and run
- [ ] `grep -c 'uvx mypy' CONTRIBUTING.md` returns `1`, and it carries `--strict` **only if** `pyproject.toml` is absent
- [ ] `grep -n 'Apache License 2.0 by virtue of its §5' CONTRIBUTING.md` still matches
- [ ] `git diff --stat` lists exactly one file, `CONTRIBUTING.md`
- [ ] `git diff --stat -- skills/ tests/ docs/` is empty
- [ ] `uv run --with pytest pytest -q` still reports the same pass count as before this plan, `0 failed`
- [ ] The report quotes the final numbered item 4 in full and states which mypy variant was used
- [ ] `plans/README.md` status row for 006 updated

## STOP conditions

Stop and report back (do not improvise) if:

- Step 1 finds the title or the `scripts/` reference already changed — the file drifted since `5978324` and someone else may be mid-edit.
- Step 1 finds a top-level `scripts/` directory now exists. Defect 2 would then be a real path, and the right fix is different.
- Any of the four commands in step 4.1 fails. Do **not** fix the code to make it pass and do not omit the command from the file: report the failure. A broken check is a separate problem from a doc that fails to mention it, and one of plans 001–005 landing incompletely is the likely cause.
- You cannot tell whether plan 004 landed. `test -f pyproject.toml && test -f .github/workflows/ci.yml` answers it; if the two disagree with each other, report that rather than guessing which variant of step 4 to write.
- The `--strict`-versus-config decision seems ambiguous. It is not: the flag and the config setting must never both be present, or local and CI checks can drift into being different checks. If `pyproject.toml` carries `strict = true`, the command line must not repeat it.
- You find yourself wanting to restructure the contribution-scope table, rewrite the licensing paragraph, or add sections (a code of conduct, a PR template, commit-message conventions). All are out of scope; list them as follow-ups in your report instead.

## Maintenance notes

- **The commands in this file and the steps in `.github/workflows/ci.yml` are one fact in two places.** That is a DRY violation the project accepts, because a contributor reading a guide should not have to open a YAML file to learn how to check their work. The cost is that they can drift. Anyone changing one must change the other; a reviewer seeing a CI step change should ask whether `CONTRIBUTING.md` moved with it.
- **The mypy line has no `--strict` once `pyproject.toml` exists.** If someone later adds the flag back "to be explicit", the setting then lives in two places and can disagree. `plans/004-add-ci-and-tooling-config.md` pins the same rule for the workflow.
- **The mypy path list is explicit, not a glob.** When a third dependency-free script joins the repository it must be added here and in the CI step. `plans/004-add-ci-and-tooling-config.md` explains why there is no glob: an omission should be visible in review.
- **Reviewer should scrutinize**: that the diff is small (three edits, not a rewrite), that the licensing paragraph and the scope table are untouched, and that no prose paragraph was hard-wrapped — the single-physical-line rule is a house convention that a formatter will not catch.
- **Deliberately deferred**: documenting that a new skill's frontmatter `name` must equal its directory name (an invariant `plans/005-validate-the-generated-catalog.md` starts enforcing at Catalog generation, and worth a line here once someone actually contributes a skill); a commit-message convention section; and a PR template. Each is its own concern.
