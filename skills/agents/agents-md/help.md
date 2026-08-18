# agents-md

Tend `AGENTS.md` and `agents.d/` — the files every session loads before it starts.

## Synopsis

`/agents-md [path] [--force] [--yes]`

## Description

Everything in `AGENTS.md` is paid for on every single session, whether or not it is needed, so the default is to write nothing. This skill decides what has earned that price and writes only that.

It inventories what the repository already tells an agent — `CLAUDE.md`, `AGENTS.md`, `agents.d/`, `docs/`, `README*`, and every tracked project skill — collects the candidate facts from those files and from the session that just ended, and puts each one through the same gates: is it true, is it non-discoverable, does the next session actually need it, is it already written down somewhere else. What survives is given a home; what does not is cut, with the source that settles it named in the report.

`AGENTS.md` itself stays a table of contents and a set of ground rules. A fact that belongs to one concern goes to its own file under `agents.d/`, and is reached from a References line saying *read when* the situation arises, so a session pays for the pointer rather than the page.

Where no fact earns a file, no file is written and the report says why.

The skill runs after a task, not during one — unless you invoked it yourself, which is always allowed.

## Arguments

- `path` — the directory to tend. Defaults to the current repository root.

## Options

- `--force` — lay the skeleton even where no fact has earned a file: `CLAUDE.md` as the one-line bridge to `AGENTS.md`, `AGENTS.md` as title and ground rules, and an empty `agents.d/`.
- `--yes` — assume yes: make each change the skill would have asked about instead of asking, and list it in the report. `docs/` stays a proposal even so — a human writes that text.

## Notes

The always-loaded pair is measured before and after, in characters, and so is the total including `agents.d/`. Growth is a cost, and the report shows it as one.

Prose under `docs/` is never written for you. What the skill may propose there is a place and a purpose; the words are yours.

## Dependencies

`git` and `uv` on PATH, and the manager installed — the skill checks for it and says how to install it if it is missing.

## See also

`/kntnt help enable` to Enable this skill elsewhere.
