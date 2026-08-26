# The user scope

`--user` keeps the mode as a managed block in the context file this harness loads in every session. `$LIBRARY` is the Collection Library, resolved as `SKILL.md` resolves it.

## Target file

This harness's own global context file, created if it is absent: `~/.claude/CLAUDE.md` in Claude Code, and its counterpart elsewhere. You are the harness — resolve the target from what you actually load, rather than detecting which harness you are. A block in a file nothing loads is a confirmed *on* and a mode that does not exist.

No `AGENTS.md`, no `agents.d/`, no include: there is no cross-agent global convention, so this scope covers the harness you are in. Run the skill in another harness to give that one the mode too.

There is no project scope. Conversational perspective and density are personal reading preferences, and a committed block would impose them on everyone who clones the repository.

## The managed block

Write exactly this, last in the file, one blank line after whatever precedes it. One rule everywhere: no parsing, no heading to find, exact removal.

```markdown
<!-- kntnt:tldr -->
<!-- Managed block. Do not edit by hand — run /tldr to change or remove it. -->
{the entire content of $LIBRARY/references/tldr-mode.md, verbatim}
<!-- /kntnt:tldr -->
```

- `on` over an existing block rewrites it from the current `tldr-mode.md`, so `on` is idempotent and doubles as the refresh.
- `off` removes the whole block, both markers included, and nothing else.
- **Stale** — the lines between the second comment and the closing marker differ from `$LIBRARY/references/tldr-mode.md`. `status` reports it and names `/tldr on --user` as the fix.
- Two blocks in one file, or a marker without its pair: change nothing, report, ask.

## Confirmation

Show the exact target file and the exact insertion, then wait for a yes unless `--yes` was passed. The file is hand-curated, and the confirmation absorbs a wrong target: it is redirected in one word before anything is written.

- `off` where there is no block: say so and stop. Nothing to remove is not an error.
- No backup file, in git or out. `off` is an exact undo of `on`.

## Taking effect

`on --user` also adopts `tldr-mode.md` for the current session, exactly as a session `on` does, so the mode does not wait for a restart — the report of the write already obeys it. `off --user` likewise suspends it here and now.
