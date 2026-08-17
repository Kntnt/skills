---
name: delegation
description: Turn delegation mode on or off — you orchestrate, subagents execute — for this session, this project, or your user account.
disable-model-invocation: true
argument-hint: "[session|project|user] [on|off|status] [--yes]"
metadata:
  internal: true
  kntnt:
    binaries:
      - uv
---

# delegation

While delegation mode is on, you orchestrate — think, plan, brief, verify — and subagents execute on the cheapest model able to do the job. This skill turns the mode on or off. Model and effort stay the user's own move: `/model` and `/effort` are theirs to run.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or another recorded Harness). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `help`, `--help`, or `-h`, emit the Arguments and Steps below and stop.

## Arguments

One scope and one state, bare or flagged, in any order: `/delegation project on`, `/delegation --project --on`, and `/delegation --on --project` all mean the same.

- scope — `session` (the default), `project`, `user`.
- state — `on`, `off`, `status`.
- `--yes` — write the persistent scope without waiting for a yes.

Parse rules:

- Session is the only togglable scope. `session` with no state flips the verdict. `project` or `user` with no state is incomplete: change nothing, name what is missing, ask for `on`, `off`, or `status`. Flipping a file in `~/.claude`, or a committed file in a shared repo, off an inferred state is the wrong default.
- `status` with no scope reports all three scopes.
- Two scopes, two states, or a state alongside `status`: name the ambiguity, ask which was meant, change nothing.
- Natural language reaches `status` alone, from "is it on?". Ask rather than guess — "turn it on everywhere" versus "for this project" is exactly the guess that writes the wrong file.

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

1. Parse the arguments. Incomplete or ambiguous: say what is missing, change nothing, stop. Done when scope and state are settled, or you have stopped.
2. Scope `project` or `user`, any state: read [`persist.md`](persist.md) and follow it, then go to the report. Done when the block is written, removed, or read.
3. Session `on`, `off`, or a toggle of the current verdict. Going on: read `$HERE/mode.md` and adopt it as a standing instruction for the rest of this session. Going off: treat that instruction as inert history — execute tasks yourself again, and spawn subagents only when the user asks. `status` changes nothing. Done when the session state matches the argument.
4. Write `{"active": true}` or `{"active": false}`, and nothing else, to `kntnt-delegation.json` in the session scratchpad directory named in the system prompt, so a compaction cannot lose the state. No scratchpad directory: the conversation alone carries it. `status` writes nothing. Done when that file matches the session state, or there is nowhere to write it.
5. Report one line per scope touched — its state, then the verdict — and name any disagreement between the two, and any staleness found. Done when that report is shown.
