# Writes

## Safe (write after the task)

- Add a `docs/agents/` file and its pointer, gates passed.
- Migrate a legacy `agents.d/` per [`migrate.md`](migrate.md).
- Add a pointer to an existing human `docs/` file, or a reading brief when placement allows.
- Shorten text this skill owns; keep the meaning.
- Rebuild the References index.
- Replace a `CLAUDE.md` that is exactly `@AGENTS.md` with the symbolic link placement prescribes.
- `CUT` a line with a cited discoverable source.
- `CUT` a line that a **tracked Project** skill already covers (Enabled in Project, `SKILL.md` in `git ls-files`, same meaning, that skill starts when the line would have mattered).

## Ask (one concrete question after the task, or the change itself under `--yes`)

- Drop a fact because this session did not use it.
- Drop a fact with no named source.
- Change `docs/` outside `docs/agents/` — propose the text; the human writes it.
- Unsure the fact is load-bearing.
- A Global-only skill appears to cover the line.

Do not ask the user to run `/agents-md`.

## Safety

In git: write, then tell the user to review. Warn when targets already have uncommitted changes. Out of git: show before/after, then write.
