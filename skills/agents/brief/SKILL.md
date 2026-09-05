---
name: brief
description: Turn Brief mode on or off for the conversation it is typed in, and report which of the two it is in, so replies stay concise and decision-relevant.
disable-model-invocation: true
argument-hint: "(on|off|status) [-- <instruction>]"
compatibility: Requires uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# brief

Adopt the Brief perspective for this conversation, drop it again, or report which of the two it is in. The mode reaches this conversation and nothing else: nothing is written anywhere, so another window, another project, and a later session are all untouched by it.

`$HERE` is the directory that contains this SKILL.md, and `$MANAGER` is the Manager directory: `$HERE/../kntnt/` if it exists, else `kntnt/` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Neither found: tell the user to install the Manager (`npx skills add Kntnt/skills`) and stop. `$LIBRARY` is `$MANAGER/library/` — absent, tell the user to run `/kntnt update`, then stop.

Run `uv run "$MANAGER/scripts/kntnt.py" invoke --here="$HERE"` with the invocation payload — everything the user typed after `/brief`, verbatim, however many lines — on stdin. On exit 0, answer the `capabilities` in its `dependencies` first: for each one, say whether its `confirm` sentence is true of you, and where it is not, give its `how`, change nothing, and stop. Then continue from the JSON. On any other exit print its stdout verbatim and stop: it has already printed what the user is to see, and none of that text is yours to write.

In the JSON, `path` is the command path as a list, `flags` holds each flag the user wrote — `true` where it stood bare, its value where it carried one, a list of values where it was repeated — `operands` is what followed the flags, in order, and `instruction` is the Contextual Instruction, or `null`, applied as `$LIBRARY/references/invocation-envelope.md` says.

## Arguments

`on`, `off`, and `status` are the three things this conversation can be asked for, and `path` carries the one that was. A Contextual Instruction may name a language or constrain the report — each a choice this Skill's contract leaves open.

## Steps

1. `status`: report whether the perspective is on or off in this conversation, in a line. Write nothing, change nothing, and stop. Done when that report is shown.
2. `on`: read [`mode.md`](references/mode.md) and adopt it as a standing instruction for the rest of this conversation; do not revisit the preceding answer. `off`: treat that standing instruction as inert history from here on, and where it was never on, say so and stop — nothing to turn off is not an error. Write nothing to any file, settings key, or scratch state, in any Harness — the state lives in this conversation and ends with it. It takes effect on this turn, so the report in step 3 already obeys it. Done when this conversation's state matches the argument.
3. Report the state this conversation is now in, in a line. Done when that report is shown.
