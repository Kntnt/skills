# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

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

[Unreleased]: https://github.com/Kntnt/skills/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/Kntnt/skills/releases/tag/v0.4.0
