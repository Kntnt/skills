---
name: delegation
description: Turn delegation mode on or off — you orchestrate, subagents execute — for this session, this project, or your user account.
disable-model-invocation: true
argument-hint: "[session|--session] | [--session|--project|--user] [--on|--off] [--yes] [session|project|user] [on|off] | [--session|--project|--user] [--status] [session|project|user] [status] [-- <instruction>]"
compatibility: Requires uv, model-selector, and a harness that can run subagents
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: "model-selector"
  kntnt.externals: ""
  kntnt.capabilities: "subagents"
---

# delegation

While delegation mode is on, you orchestrate — think, plan, brief, verify — and subagents execute only after model-selector has routed that execution. This skill turns the mode on or off. Your own model and reasoning effort stay the user's move — whatever your harness offers for changing them is theirs to run, never yours.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

The payload's `capabilities` are the half of the check no script can do — you are the harness, so you answer. For each one, say whether its `confirm` sentence is true of you. Any that is not: give its `how`, change nothing, stop. Exit 0 is not a go-ahead until every one is answered.

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is `library/` under the Manager directory that contains the checker — absent, tell the user to run `/kntnt update`, then stop.

## Invocation

Read `$LIBRARY/references/invocation-envelope.md` and follow it before help routing or formal validation; only the Formal Invocation reaches Help, Arguments, scripts, and nested formal parsers. `--help`, `-h`, and `help` print `$HERE/help.md` verbatim and stop.

## Arguments

One scope and one state, bare or flagged, in either order among themselves, and with every flag before every bare word: `/delegation project on`, `/delegation --project --on`, and `/delegation --on --project` all mean the same.

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
- An out-of-order form: a bare `session`, `project`, `user`, `on`, `off`, or `status` written before any flag, such as `/delegation project --on` or `/delegation status --yes`.

## The mode

`$LIBRARY/references/delegation-mode.md` is the single source of truth for what the mode says. Read it, and copy it verbatim wherever it is needed; state it in no other words.

Two states, no third:

- **on** — delegation happens as `delegation-mode.md` says.
- **not on** — delegation is yours to judge, exactly as with this skill Disabled. Session `off` suspends this skill's own instruction for the current session; delegating in general stays open.

## Verdict

The verdict is the effective state here and now:

- A session instruction given in this conversation wins — or one recorded in `kntnt-delegation.json` when a compaction has dropped it from view.
- Otherwise: on if and only if a managed block sits in a context file this harness loads here. `user` and `project` write the identical block, so they cannot disagree; either one present means on.
- Session `off` suspends obedience; the standing block's text stays in the context window and its tokens are still paid. A compaction can drop the session instruction while that block survives, so re-run `/delegation off` if delegating resumes.

## Steps

1. Parse the arguments by the rules above. An invalid form is refused as `$LIBRARY/references/invocation-envelope.md` says; change nothing and stop. Done when scope and state are settled, or you have stopped.
2. Scope `project` or `user`, any state: read [`persist.md`](references/persist.md) and follow it, then go to the report. Done when the block is written, removed, or read.
3. Session `on`, `off`, or a toggle of the current verdict. Going on: read `$LIBRARY/references/delegation-mode.md` and adopt it as a standing instruction for the rest of this session. Going off: treat that instruction as inert history — execute tasks yourself again, and spawn subagents only when the user asks. `status` changes nothing. Done when the session state matches the argument.
4. Write `{"active": true}` or `{"active": false}`, and nothing else, to `kntnt-delegation.json` in whatever per-session scratchpad or temporary directory your harness gives you, so a compaction cannot lose the state. No such directory: the conversation alone carries it. `status` writes nothing. Done when that file matches the session state, or there is nowhere to write it.
5. Report one line per scope touched — its state, then the verdict — and name any disagreement between the two, and any staleness found. Done when that report is shown.
