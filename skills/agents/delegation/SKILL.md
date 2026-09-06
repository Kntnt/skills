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

While delegation mode is on, you orchestrate — think, plan, brief, verify — and subagents execute, on the seat model-selector chooses, unless you run them on the frozen main seat with no override. This skill turns the mode on or off. Your own model and reasoning effort stay the user's move — whatever your harness offers for changing them is theirs to run, never yours.

`$HERE` is the directory that contains this SKILL.md, and `$MANAGER` is the Manager directory: `$HERE/../kntnt/` if it exists, else `kntnt/` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Neither found: tell the user to install the Manager (`npx skills add Kntnt/skills`) and stop. `$LIBRARY` is `$MANAGER/library/` — absent, tell the user to run `/kntnt update`, then stop.

Run `uv run "$MANAGER/scripts/kntnt.py" invoke --here="$HERE"` with the invocation payload — everything the user typed after `/delegation`, verbatim, however many lines — on stdin. On exit 0, answer the `capabilities` in its `dependencies` first: for each one, say whether its `confirm` sentence is true of you, and where it is not, give its `how`, change nothing, and stop. Then continue from the JSON. On any other exit print its stdout verbatim and stop: it has already printed what the user is to see, and none of that text is yours to write.

In the JSON, `path` is the command path as a list, `flags` holds each flag the user wrote — `true` where it stood bare, its value where it carried one, a list of values where it was repeated — `operands` is what followed the flags, in order, and `instruction` is the Contextual Instruction, or `null`, applied as `$LIBRARY/references/invocation-envelope.md` says.

## Arguments

- `--project` and `--user` name the two persistent scopes. Without either, the scope is this session, which has no name of its own.
- `--yes` — write the persistent scope without waiting for a yes. `status` asks nothing.
- The session is the only togglable scope, and the bare invocation — an empty `path` — flips its current verdict.
- `status` with no scope flag reports all three scopes.

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

1. `--project` or `--user`, with any command path: read [`persist.md`](references/persist.md) and follow it, then go to the report. Done when the pointer and companions are written, removed, or read.
2. Session scope — `on`, `off`, or the bare invocation's toggle of the current verdict. Going on: read `$HERE/references/mode.md` and adopt it as a standing instruction for the rest of this session. Read `$HERE/references/fence.md` as its canonical fence preamble, fill in the spawn-specific paths, and paste it at the top of every subagent brief, adding only any task-specific tightening. Going off: treat that instruction as inert history — execute tasks yourself again, and spawn subagents only when the user asks. `status` changes nothing. Done when the session state matches the argument.
3. Write `{"active": true}` or `{"active": false}`, and nothing else, to `kntnt-delegation.json` in whatever per-session scratchpad or temporary directory your harness gives you, so a compaction cannot lose the state. No such directory: the conversation alone carries it. `status` writes nothing. Done when that file matches the session state, or there is nowhere to write it.
4. Report one line per scope touched — its state, then the verdict — and name any disagreement between the two, and any staleness found. Done when that report is shown.
