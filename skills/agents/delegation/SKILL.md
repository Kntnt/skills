---
name: delegation
description: Turn delegation mode on or off — you orchestrate, subagents execute — for this session, this project, or your user account.
disable-model-invocation: true
argument-hint: "[session|project|user] [on|off] [--yes] | [session|project|user] status"
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: "subagents"
---

# delegation

While delegation mode is on, you orchestrate — think, plan, brief, verify — and subagents execute on the cheapest model able to do the job. This skill turns the mode on or off. Your own model and reasoning effort stay the user's move — whatever your harness offers for changing them is theirs to run, never yours.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

The payload's `capabilities` are the half of the check no script can do — you are the harness, so you answer. For each one, say whether its `confirm` sentence is true of you. Any that is not: give its `how`, change nothing, stop. Exit 0 is not a go-ahead until every one is answered.

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

One scope and one state, bare or flagged, in any order: `/delegation project on`, `/delegation --project --on`, and `/delegation --on --project` all mean the same.

- scope — `session` (the default), `project`, `user`.
- state — `on`, `off`, `status`.
- `--yes` — write the persistent scope without waiting for a yes. Valid only alongside `on` or `off`; `status` asks nothing, so there is nothing for the flag to answer.

Parse rules:

- Session is the only togglable scope. `session` with no state flips the verdict.
- `status` with no scope reports all three scopes.
- Natural language reaches `status` alone, from "is it on?". Prose is not a form, so anything wider than that is asked about rather than refused: "turn it on everywhere" versus "for this project" is exactly the guess that writes the wrong file, and only the user can settle which they meant.

Invalid forms, each refused the same way:

- A `--`-prefixed token that is not `--session`, `--project`, `--user`, `--on`, `--off`, `--status`, or `--yes`.
- `--yes` without `on` or `off`.
- `project` or `user` with no state. Flipping a file in the user's home configuration, or a committed file in a shared repo, off an inferred state is the wrong default, and an error infers nothing either.
- Two scopes, two states, or a state alongside `status`.

A flag is refused rather than ignored where it has no work to do here, and an incomplete form is refused rather than asked about, because a flag accepted and ignored teaches that flags sometimes do nothing and a question asked in place of the grammar leaves the user guessing at what the grammar is (ADR-0059).

## The mode

`$HERE/mode.md` is the single source of truth for what the mode says. Read it, and copy it verbatim wherever it is needed; state it in no other words.

Two states, no third:

- **on** — delegation happens as `mode.md` says.
- **not on** — delegation is yours to judge, exactly as with this skill Disabled. Session `off` suspends this skill's own instruction for the current session; delegating in general stays open.

## Verdict

The verdict is the effective state here and now:

- A session instruction given in this conversation wins — or one recorded in `kntnt-delegation.json` when a compaction has dropped it from view.
- Otherwise: on if and only if a managed block sits in a context file this harness loads here. `user` and `project` write the identical block, so they cannot disagree; either one present means on.
- Session `off` suspends obedience; the standing block's text stays in the context window and its tokens are still paid. A compaction can drop the session instruction while that block survives, so re-run `/delegation off` if delegating resumes.

## Steps

1. Parse the arguments by the rules above. An invalid form: name in one line what was wrong, print the `## Synopsis` section of `$HERE/help.md` verbatim, and point at `/delegation --help` for the page in full. Change nothing and stop. Done when scope and state are settled, or you have stopped.
2. Scope `project` or `user`, any state: read [`persist.md`](persist.md) and follow it, then go to the report. Done when the block is written, removed, or read.
3. Session `on`, `off`, or a toggle of the current verdict. Going on: read `$HERE/mode.md` and adopt it as a standing instruction for the rest of this session. Going off: treat that instruction as inert history — execute tasks yourself again, and spawn subagents only when the user asks. `status` changes nothing. Done when the session state matches the argument.
4. Write `{"active": true}` or `{"active": false}`, and nothing else, to `kntnt-delegation.json` in whatever per-session scratchpad or temporary directory your harness gives you, so a compaction cannot lose the state. No such directory: the conversation alone carries it. `status` writes nothing. Done when that file matches the session state, or there is nowhere to write it.
5. Report one line per scope touched — its state, then the verdict — and name any disagreement between the two, and any staleness found. Done when that report is shown.
