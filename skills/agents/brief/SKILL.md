---
name: brief
description: Turn Brief mode on or off for the conversation it is typed in, and report which of the two it is in, so replies stay concise and decision-relevant.
disable-model-invocation: true
argument-hint: "(on|off|status) [-- <instruction>]"
metadata:
  kntnt.internal: "true"
  kntnt.binaries: ""
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# brief

Adopt the Brief perspective for this conversation, drop it again, or report which of the two it is in. The mode reaches this conversation and nothing else: nothing is written anywhere, so another window, another project, and a later session are all untouched by it.

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is `library/` under the Manager directory beside it — `$HERE/../kntnt/library/` if it exists, else `kntnt/library/` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them); absent, tell the user to run `/kntnt update`, then stop.

## Invocation

Read `$LIBRARY/references/invocation-envelope.md` and follow it before help routing or formal validation; only the Formal Invocation reaches Help, Arguments, scripts, and nested formal parsers. `--help`, `-h`, and `help` print `$HERE/help.md` verbatim and stop, and `on`, `off`, or `status` followed by `--help` or `-h` prints `$HERE/help/on.md`, `$HERE/help/off.md`, or `$HERE/help/status.md` verbatim and stops.

## Arguments

`/brief on`, `/brief off`, or `/brief status`, and nothing else. The grammar is closed and declares no flag: `on`, `off`, and `status` are command paths, there is no operand, and the Formal Invocation ends where the command path ends.

- The command path is required. Every form of this Skill is explicit about the state it produces, and a bare `/brief` names none.
- Anything the user wants of the run arrives as a Contextual Instruction after the reserved separator, as `/brief on -- svara på svenska`. It may name a language or constrain the report — each a choice this Skill's contract leaves open, which is what a Contextual Instruction may settle. Guidance that would widen the Skill's responsibility takes the context refusal of the Invocation Envelope rather than the syntax refusal below.

Invalid forms, each refused the same way:

- A token that does not open a recognized command path, wherever it stands. There is no free-text operand, so `/brief only the security part` is an invalid form rather than an instruction, and a bare `/brief` is an incomplete one rather than a shorthand for any of the three.
- More than one of `on`, `off`, or `status`.
- Any flag at all. This grammar declares none, so every `--`-prefixed token is undeclared here.
- A flag-spelled command path. The mode has one spelling, the bare word, and a `--`-prefixed variant of it is an undeclared flag like any other.

Each of those is refused as `$LIBRARY/references/invocation-envelope.md` says. This grammar declares no flag at all, so every `--`-prefixed token is undeclared and refused as one.

## Steps

1. Parse the arguments by the rules above. An invalid form is refused as `$LIBRARY/references/invocation-envelope.md` says, addressing the page of the most specific recognized command path — `$HERE/help/on.md`, `$HERE/help/off.md`, or `$HERE/help/status.md`, and `$HERE/help.md` where none was recognized. Change nothing and stop. Done when the form is settled, or you have stopped.
2. `status`: report whether the perspective is on or off in this conversation, in a line. Write nothing, change nothing, and stop. Done when that report is shown.
3. `on`: read [`mode.md`](references/mode.md) and adopt it as a standing instruction for the rest of this conversation; do not revisit the preceding answer. `off`: treat that standing instruction as inert history from here on, and where it was never on, say so and stop — nothing to turn off is not an error. Write nothing to any file, settings key, or scratch state, in any Harness — the state lives in this conversation and ends with it. It takes effect on this turn, so the report in step 4 already obeys it. Done when this conversation's state matches the argument.
4. Report the state this conversation is now in, in a line. Done when that report is shown.
