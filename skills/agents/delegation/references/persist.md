# Persistent scopes

`project` and `user` keep one managed context pointer and one companion mode file. `$HERE` is the directory that contains `SKILL.md`.

## Targets

The pointer must land in a context file this harness loads automatically in every session at that scope. Resolve the target from what you load, rather than detecting which harness you are. A pointer in a file nothing loads is a confirmed "on" and a mode that does not exist — Claude Code, for one, reads a Project `AGENTS.md` only when a `CLAUDE.md` imports it.

`user` — this harness's own global context file, created if absent; `~/.claude/CLAUDE.md` in Claude Code, and its counterpart elsewhere. There is no cross-agent global convention, so this scope covers the harness you are in. Run the Skill in another harness to give that one the mode too.

`project` — first match wins:

1. This harness already loads an agent-agnostic `AGENTS.md`, directly or through a bridge such as a `CLAUDE.md` containing `@AGENTS.md` → write the pointer to `AGENTS.md`.
2. `AGENTS.md` exists but this harness does not load it → propose the bridge as part of the same confirmed write, then write the pointer to `AGENTS.md`.
3. No `AGENTS.md`, but this harness has its own Project file (`CLAUDE.md`, `GEMINI.md`, …) → write the pointer there.
4. No context file at all → create `AGENTS.md` with the title line `# <project> — agent guide` and the pointer, plus this harness's bridge. Name every file in one confirmation. The user has asked for a standing instruction, so the `agents-md` Skill's write-nothing default does not apply.

The companion is `agents.d/kntnt-delegation.md` under the Project root or under the directory holding the user context file. The context pointer always addresses it as `@agents.d/kntnt-delegation.md`. An existing companion without one well-formed managed pointer is a conflict: change nothing, report it, and ask.

## Managed files

Write exactly this pointer block last in the context file, with one blank line after whatever precedes it. Never inline the mode text in the context file.

```markdown
<!-- kntnt:delegation -->
- Delegate per @agents.d/kntnt-delegation.md.
<!-- /kntnt:delegation -->
```

Write exactly this companion file:

```markdown
- `agents.d/kntnt-delegation.md` — read when delegation mode is on.

{the entire content of $HERE/references/mode.md, verbatim}
```

- `on` rewrites the pointer block and companion from the current Skill, so it is idempotent and refreshes stale state.
- `off` removes the pointer block and companion file, and nothing else.
- **Stale** — the pointer block or companion file differs from what the current Skill writes. `status` reports it and names `/delegation on --project` or `/delegation on --user` as the fix.
- Two blocks in one file, a marker without its pair, or a companion without its pointer: change nothing, report, and ask.

## Confirmation

Show the context file and exact pointer insertion or removal, the companion path and exact write or removal, and any bridge file to be created, then wait for a yes unless `--yes` was passed. These files are hand-curated, and the confirmation absorbs a wrong target before anything is written.

- `project` says that both managed files are normally committed — everyone who clones the repository gets the mode, and every agent that follows the pointer gets the same instruction.
- `project` whose context file or companion already has uncommitted changes says so, preventing the mode change from being mistaken for unrelated work in progress.
- No backup file, in git or out. `off` is the exact undo of `on`, and Project scope works outside git too.

## Taking effect

`on` also adopts `mode.md` for the current session, exactly as it does in session scope, so the mode does not wait for a restart; `off` likewise suspends it here and now. Neither writes the session state file — the pointer and companion are the persistent record.
