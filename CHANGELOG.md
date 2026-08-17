# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
