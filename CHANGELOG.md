# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Tests that pin the release version-bump: a nested JSON `"version"` must not be rewritten instead of the top-level one, a TOML `version_scheme` must not be read as the version, and a failed bump must write nothing.
- CI on push to `main` and on every pull request: ruff, mypy, and pytest. Tool settings live in `pyproject.toml`. `plans/` is excluded from ruff so Markdown Plans are not formatted as Python.

### Fixed

- Release version bump now reads and writes by one rule per format: the top-level JSON `"version"`, and `[project]` / `[tool.poetry]` in TOML. A file that cannot be rewritten unambiguously aborts the whole bump so nothing is left half-written.
- `git status` paths in the commit plan are no longer C-quoted: porcelain is read with NUL separators, so a file named `skäl.md` is shown as itself.
- Catalog generation refuses a skill whose frontmatter `name` is not its directory, or whose description is empty or a YAML block-scalar indicator the parser cannot read.
- `CONTRIBUTING.md` now names this Collection, points at `skills/<category>/<skill>/scripts/`, and lists the same four checks CI runs.

## [0.6.0] – 2026-08-17

### Added

- `plan` — turn Tickets, or a design settled in conversation, into Plans under `plans/`. `/plan #12 #17` plans those Tickets whatever labels they carry, `/plan "<description>"` plans work with no Ticket behind it, and bare `/plan` shows a picker of the open `ready-for-agent` Tickets with the conversation's settled design as its first row. The External `improve` writes each Plan; the skill then makes the batch a queue by numbering it, resolving `**Depends on**` across old and new Plans, recording each Plan's Ticket, and writing `plans/README.md`.
- `execute` — build the Plans under `plans/` unattended. One at a time, `improve` builds each in an isolated worktree and renders the verdict, and every approved Plan is Landed on the branch the run started on — squash-merged, then committed through `commit` so the changelog gets one entry per Plan — before the next is dispatched. Drift is checked once against the run's base, after which the invariant that `HEAD` stands where the run left it is what separates the run's own commits from a third party's. A blocked Plan is set aside with everything that depends on it. It commits and stops: no push, no tag, no release.
- Architecture Decision Records 0031 (Plans are written by one skill and built by another), 0032 (Land each approved Plan before the next one starts), 0033 (Drift is checked once, before the run), and 0034 (an unattended skill asks only yes or no), and the Collection terms *Land* and *Drift*.
- The Collection terms *Ticket* and *Plan*. A Ticket is a unit of work in the issue tracker, named so that no skill is bound to one tracker's own vocabulary; a Plan is a file under `plans/` describing one unit of work, self-contained enough that an agent with no other context can carry it out.
- `plans/` — six implementation plans and their index, from an audit of the two Python engines. Nothing is fixed yet; the plans describe the work. They cover a version bump that can rewrite a nested `"version"` field instead of the real one and still report success, `git status` output parsed so that any path with a non-ASCII byte reaches the user C-quoted, the absent continuous integration that would keep the passing tests, linter, and type checker passing, and Catalog generation accepting an entry whose name or description cannot do its job.

## [0.5.0] – 2026-08-17

### Added

- Capabilities: a fourth kind of Dependency, on what the running Harness can do rather than on what sits on disk. A skill declares `capabilities` in its frontmatter, `check` reports each one with a sentence to confirm and a fix, and the agent answers — no script can, since the Manager cannot know which Harness invoked it. Unknown Capability names fail when the Catalog is generated. Status, the Enable picker, and Update surface them.
- Architecture Decision Record 0030 (a harness requirement is a Dependency the agent answers, not an install-time gate) and the Collection term *Capability*.

### Changed

- `delegation` no longer assumes Claude Code. The mode text drops the hard-coded `haiku < sonnet < opus < fable` ladder and the Fable pricing note for a rule each harness resolves against its own models, and covers the case where subagents can be spawned but their model cannot be chosen. `~/.claude` and Claude Code's scratchpad directory become the general thing they were examples of.
- `delegation` declares the `subagents` Capability, so it refuses in a harness that cannot spawn them instead of writing a mode that harness cannot honour. It is still Enabled everywhere, keeping one desired set per layer (ADR-0005).

## [0.4.0] – 2026-08-17

### Added

- `--yes` is accepted by every verb of every collection script, and means the same thing everywhere: answer yes rather than ask. `agents-md` gained the flag; `kntnt` and `ship.py` previously advertised it and then died with `unrecognized arguments` when it was passed.
- Architecture Decision Records 0027 (bare `/kntnt` is Help), 0028 (Update re-adds), and 0029 (`--yes` means assume yes).

### Changed

- Bare `/kntnt` is now Help instead of Status. Status is reached as `/kntnt status`.
- `/kntnt disable` requires `--yes` on its apply step, because it deletes files and a script cannot prompt.
- Status spells out that it reports every Catalog skill, Disabled ones included, and points at `/kntnt update` when an expected skill is absent.
- `/kntnt update` says whether it managed to refresh the Catalog, so a failed fetch is visible rather than silent.

### Fixed

- `/kntnt update` refreshes the collection. It called the transport's `update`, which compares `SKILL.md` and skips a skill whose `SKILL.md` is unchanged — so any revision that touched only a sidecar was never delivered, and `delegation` could not reach the Catalog at all. Update now re-adds, and writes the Catalog to the running Manager's own directory, which the transport need not reach.
- The test double for the transport modelled `update` as an unconditional copy, making it more capable than the real thing and hiding the bug above.
- `apply setup` builds its removal list in a stable order rather than from an unordered set.

## [0.3.0] – 2026-08-17

### Added

- `delegation` skill under `skills/agents/`: turn delegation mode on or off — the agent orchestrates, subagents execute — for the session, the project, or the user account. Adapted from the `kntnt-skills` plugin skill of the same name.
- Architecture Decision Record 0026: `delegation`'s user scope is per-harness, its project scope is not.

## [0.2.0] – 2026-08-17

### Added

- README documents install, the manager, and the collection skills.
- `AGENTS.md` at the repo root with ground rules and pointers.

### Changed

- `commit` reconciles `[Unreleased]`, proposes a `.gitignore` when missing, and stages the whole working tree (`git add -A`).
- `push` follows `commit`, then pushes. It no longer commits on its own.
- `release` bumps, follows `push`, tags `HEAD`, publishes a GitHub release, and uploads a zip when a conventional build script exists.

### Fixed

- The manager finds OpenCode skills in `~/.agents/skills`, where the transport actually writes them.

## [0.1.0] – 2026-08-16

### Added

- `kntnt` manager at `skills/kntnt/`: Setup, Enable, Disable, Status, Update, Help, and a shared Dependency checker. Collection skills are hidden from ordinary transport discovery (`metadata.internal`).
- `commit`, `push`, and `release` skills under `skills/code/`, sharing one `ship.py` engine: the agent plans and confirms, the script stages, commits, tags, and pushes. Changelog reconciliation runs only on `release`.
- Domain language in `CONTEXT.md` for distributing, enabling, and updating collection skills across harnesses.
- Architecture Decision Records 0001–0015 for the manager, the transport, Global and Project layers, Enable/Disable/Setup/Update, dependencies, and categories.
- `includes/` for markdown that skills include, unconditionally or on demand.
- Category folders under `skills/` (`agents`, `code`, `text`, `wordpress`).
- `agents-md` skill under `skills/agents/`: create, shrink, or tend `AGENTS.md` and `agents.d/`.
- Architecture Decision Records 0016–0025 for `agents-md` placement, the `CLAUDE.md` bridge, invocation, when a line may be stripped, and `read when` pointers.

[Unreleased]: https://github.com/Kntnt/skills/compare/v0.6.0...HEAD
[0.6.0]: https://github.com/Kntnt/skills/releases/tag/v0.6.0
[0.5.0]: https://github.com/Kntnt/skills/releases/tag/v0.5.0
[0.4.0]: https://github.com/Kntnt/skills/releases/tag/v0.4.0
