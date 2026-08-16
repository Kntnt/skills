# `--force` lays the skeleton; it is not the default

`agents-md` writes no files when it finds no fact (ADR-0022). `--force` overrides only that terminal case: it lays `CLAUDE.md` as `@AGENTS.md`, a minimal `AGENTS.md`, and an empty `agents.d/`. It does not invent facts.
