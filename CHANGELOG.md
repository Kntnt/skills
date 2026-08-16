# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `kntnt` manager at `skills/kntnt/`: Setup, Enable, Disable, Status, Update, Help, and a shared Dependency checker. Collection skills are hidden from ordinary transport discovery (`metadata.internal`).
- `commit`, `push`, and `release` skills under `skills/code/`, sharing one `ship.py` engine: the agent plans and confirms, the script stages, commits, tags, and pushes. Changelog reconciliation runs only on `release`.
- Domain language in `CONTEXT.md` for distributing, enabling, and updating collection skills across harnesses.
- Architecture Decision Records 0001–0015 for the manager, the transport, Global and Project layers, Enable/Disable/Setup/Update, dependencies, and categories.
- `includes/` for markdown that skills include, unconditionally or on demand.
- Category folders under `skills/` (`agents`, `code`, `text`, `wordpress`).
