# Placement

Audience decides the home. Unclear → `docs/`.

| Home | What lives there |
| --- | --- |
| Inline in `AGENTS.md` | Facts every session always needs. Tiny set. |
| `docs/` | Also for humans (coding standards, ADRs, anything a person reads). This skill never writes these files. |
| `agents.d/` | Agent-only content. One concern per file. This skill may create, shorten, and split. |

`AGENTS.md` points. It does not restate.

## Pointers

- Moderate `docs/` file, or a session that needs the whole file → `AGENTS.md` points at `docs/` directly.
- `docs/` file ≥ 10 000 characters (`wc -c`) *and* a typical session needs a slice *and* the file has stable headings → `AGENTS.md` points at a **reading brief** in `agents.d/`. The brief names when to read, which heading, and how (grep, then that span). It does not restate the `docs/` text.
- Agent-only content → `AGENTS.md` points at the `agents.d/` file.

A brief that says “read the whole file” is a wasted hop. No brief without headings to slice on.

## References line

Format, always:

```markdown
- `<path>` — read when <situation>
```

`<situation>` is the **work**, not a sample of the file.

- **Class, not examples.** A glossary with twenty terms listed as three will not fire on the fourth. Name the class that covers every reason to open the file.
- **Completeness test.** For each heading or term in the target: would this line fire? Any no → rewrite the situation.
- **One situation.** Two unrelated jobs → two lines, or one class that covers both.
- Fail: `CONTEXT.md` — Enable, Harness, Collection
- Pass: `CONTEXT.md` — read when using a Collection term

Each `agents.d/` file starts with the same `read when …` line.

## `AGENTS.md` shape

```markdown
# <project> — agent guide

## Ground rules (authoritative)
Precedence over any conflicting skill, README, or other doc unless the user overrides in the moment.
- Authoritative: this file, the files it references, and the actual code/state.

## Non-obvious
- <one compressed line each>

## References
- `<path>` — read when <situation>
```

Emit Ground rules only when narrative docs exist. Omit empty sections. `CLAUDE.md` is exactly `@AGENTS.md`. Leave a symlink `CLAUDE.md` → `AGENTS.md` as-is. Leave `CLAUDE.local.md` alone. Prefer an existing `.claude/CLAUDE.md` over creating a root one.

## Index

Every `agents.d/` file has one References line. A file with no line is invisible. Prefer several 5–15-line files over one long file.
