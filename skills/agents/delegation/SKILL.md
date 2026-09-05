---
name: delegation
description: Turn delegation mode on or off — you orchestrate, subagents execute — for this session, this project, or your user account.
disable-model-invocation: true
argument-hint: "[on|off] [--project|--user] [--yes] | status [--project|--user] [-- <instruction>]"
compatibility: Requires uv, model-selector, and a harness that can run subagents
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: "model-selector"
  kntnt.externals: ""
  kntnt.capabilities: "subagents"
---

# delegation

While delegation mode is on, you orchestrate — think, plan, brief, verify — and subagents execute, routed through model-selector unless you run them on the frozen main seat with no override. This skill turns the mode on or off. Your own model and reasoning effort stay the user's move — whatever your harness offers for changing them is theirs to run, never yours.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

The payload's `capabilities` are the half of the check no script can do — you are the harness, so you answer. For each one, say whether its `confirm` sentence is true of you. Any that is not: give its `how`, change nothing, stop. Exit 0 is not a go-ahead until every one is answered.

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is `library/` under the Manager directory that contains the checker — absent, tell the user to run `/kntnt update`, then stop.

## Invocation

Read `$LIBRARY/references/invocation-envelope.md` and follow it before help routing or formal validation; only the Formal Invocation reaches Help, Arguments, scripts, and nested formal parsers. `--help`, `-h`, and `help` print `$HERE/help.md` verbatim and stop, and `on`, `off`, or `status` followed by `--help` or `-h` prints `$HERE/help/on.md`, `$HERE/help/off.md`, or `$HERE/help/status.md` verbatim and stops.

## Arguments

`/delegation`, `/delegation on [--project|--user] [--yes]`, `/delegation off [--project|--user] [--yes]`, or `/delegation status [--project|--user]`, and nothing else. The grammar is closed and carries no operand: `on`, `off`, and `status` are command paths, and the Formal Invocation ends where they and their flags end.

- `--project` and `--user` name the two persistent scopes. Without either, the scope is this session, which has no name of its own.
- `--yes` — write the persistent scope without waiting for a yes. Valid only alongside `on` or `off`; `status` asks nothing, so there is nothing for the flag to answer.

Parse rules:

- The session is the only togglable scope, and the bare invocation is the whole of that form: it flips the current verdict and takes no flag.
- `status` with no scope flag reports all three scopes.

Invalid forms, each refused the same way:

- A token that is neither a recognized command path nor a declared flag, wherever it stands. There is no free-text operand, so `/delegation is it on everywhere?` is an invalid form rather than a question to answer.
- More than one of `on`, `off`, `status`, or a command path written after a flag.
- A flag-spelled command path. The mode has one spelling, the bare word, and a `--`-prefixed variant of it is an undeclared flag like any other.
- Both scope flags at once, or either of them on the bare form.
- `--project` or `--user` with no command path. Flipping a file in the user's home configuration, or a committed file in a shared repo, off an inferred state is the wrong default, and an error infers nothing either.
- `--yes` without `on` or `off`.

Each of those is refused as `$LIBRARY/references/invocation-envelope.md` says — a flag with no work to do here included, and an incomplete form rather than a question about it.

## The mode

`$HERE/references/mode.md` is the single source of truth for what the mode says. Read and adopt it verbatim. Persistent scopes follow [`persist.md`](references/persist.md): they copy the mode and fence to two companion files and keep only an `@` pointer block in the context file.

Two states, no third:

- **on** — delegation happens as `mode.md` says.
- **not on** — delegation is yours to judge, exactly as with this skill Disabled. `off` in the session scope suspends this skill's own instruction for the current session; delegating in general stays open.

## Verdict

The verdict is the effective state here and now:

- A session instruction given in this conversation wins — or one recorded in `kntnt-delegation.json` when a compaction has dropped it from view.
- Otherwise: on if and only if a managed pointer block in a context file this harness loads resolves to both readable companions. `--user` and `--project` write identical pointers and companions, so they cannot define different modes; either complete trio means on.
- `off` in the session scope suspends obedience; standing context already loaded for this session and its tokens are still paid. A compaction can drop the session instruction while the persistent trio survives, so re-run `/delegation off` if delegating resumes.

## Steps

1. Parse the arguments by the rules above. An invalid form is refused as `$LIBRARY/references/invocation-envelope.md` says, addressing the page of the most specific recognized command path — `$HERE/help/on.md`, `$HERE/help/off.md`, or `$HERE/help/status.md`, and `$HERE/help.md` where none was recognized. Change nothing and stop. Done when the form and the scope are settled, or you have stopped.
2. `--project` or `--user`, with any command path: read [`persist.md`](references/persist.md) and follow it, then go to the report. Done when the pointer and companions are written, removed, or read.
3. Session scope — `on`, `off`, or the bare invocation's toggle of the current verdict. Going on: read `$HERE/references/mode.md` and adopt it as a standing instruction for the rest of this session. Read `$HERE/references/fence.md` as its canonical fence preamble, fill in the spawn-specific paths, and paste it at the top of every subagent brief, adding only any task-specific tightening. Going off: treat that instruction as inert history — execute tasks yourself again, and spawn subagents only when the user asks. `status` changes nothing. Done when the session state matches the argument.
4. Write `{"active": true}` or `{"active": false}`, and nothing else, to `kntnt-delegation.json` in whatever per-session scratchpad or temporary directory your harness gives you, so a compaction cannot lose the state. No such directory: the conversation alone carries it. `status` writes nothing. Done when that file matches the session state, or there is nowhere to write it.
5. Report one line per scope touched — its state, then the verdict — and name any disagreement between the two, and any staleness found. Done when that report is shown.
