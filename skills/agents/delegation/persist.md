# Persistent scopes

`project` and `user` keep the mode as a managed block in a context file this harness already loads. `$HERE` is the directory that contains `SKILL.md`.

## Target file

The block must land in a file this harness loads automatically in every session at that scope. You are the harness: resolve the target from what you load, rather than detecting which harness you are. A block in a file nothing loads is a confirmed "on" and a mode that does not exist — Claude Code, for one, reads a project `AGENTS.md` only when a `CLAUDE.md` imports it.

`user` — this harness's own global context file, created if absent; for Claude Code, `~/.claude/CLAUDE.md`. No `AGENTS.md`, no `agents.d/`, no include: there is no cross-agent global convention, so this scope covers the harness you are in. Run the skill in another harness to give that one the mode too.

`project` — first match wins:

1. This harness already loads an agent-agnostic `AGENTS.md`, directly or through a bridge such as a `CLAUDE.md` containing `@AGENTS.md` → write to `AGENTS.md`.
2. `AGENTS.md` exists but this harness does not load it → propose the bridge as part of the same confirmed write, then write to `AGENTS.md`.
3. No `AGENTS.md`, but this harness has its own project file (`CLAUDE.md`, `GEMINI.md`, …) → write there.
4. No context file at all → create the pair: `AGENTS.md` holding the title line `# <project> — agent guide` and the block, plus this harness's bridge. Name both files in one confirmation. The user has asked for a standing instruction in as many words, so the `agents-md` skill's write-nothing default does not apply.

## The managed block

Write exactly this, last in the file, one blank line after whatever precedes it — including after a `## References` index. One rule for every scope and harness: no parsing, no heading to find, exact removal.

```markdown
<!-- kntnt:delegation -->
<!-- Managed block. Do not edit by hand — run /delegation to change or remove it. -->
{the entire content of $HERE/mode.md, verbatim}
<!-- /kntnt:delegation -->
```

- `on` over an existing block rewrites it from the current `mode.md`, so `on` is idempotent and doubles as the refresh.
- `off` removes the whole block, both markers included, and nothing else.
- **Stale** — the lines between the second comment and the closing marker differ from `$HERE/mode.md`. `status` reports it and names `/delegation <scope> on` as the fix.
- Two blocks in one file, or a marker without its pair: change nothing, report, ask.

## Confirmation

Show the exact target file, the exact insertion, and any bridge file to be created, then wait for a yes unless `--yes` was passed. These files are hand-curated, and the confirmation absorbs a wrong target: it is redirected in one word before anything is written.

- `project` says in as many words that the file is normally committed — everyone who clones the repo gets the mode, and every other agent that reads `AGENTS.md` gets the block.
- `project` whose target already has uncommitted changes: say so, so the block is not mixed into work in progress.
- No backup file, in git or out. `off` is an exact undo of `on`, and project scope works outside git too.

## Taking effect

`on` also adopts `mode.md` for the current session, exactly as session `on` does, so the mode does not wait for a restart; `off` likewise suspends it here and now. Neither writes the session state file — the block in the context file is the record.
