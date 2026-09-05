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

`$HERE` is the directory that contains this SKILL.md.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop. If they are `on --help` or `on -h`, print `$HERE/help/on.md` verbatim and stop. If they are `off --help` or `off -h`, print `$HERE/help/off.md` verbatim and stop. If they are `status --help` or `status -h`, print `$HERE/help/status.md` verbatim and stop.

## Arguments

`/brief on`, `/brief off`, or `/brief status`, and nothing else. The grammar is closed and declares no flag: `on`, `off`, and `status` are command paths, there is no operand, and the Formal Invocation ends where the command path ends.

- The command path is required. Every form of this Skill is explicit about the state it produces, and a bare `/brief` names none.
- Anything the user wants of the run arrives as a Contextual Instruction after the reserved separator, as `/brief on -- svara på svenska`. It may name a language or constrain the report — each a choice this Skill's contract leaves open, which is what a Contextual Instruction may settle. Guidance that would widen the Skill's responsibility takes the context refusal of the Invocation Envelope rather than the syntax refusal below.

Invalid forms, each refused the same way:

- A token that does not open a recognized command path, wherever it stands. There is no free-text operand, so `/brief only the security part` is an invalid form rather than an instruction, and a bare `/brief` is an incomplete one rather than a shorthand for any of the three.
- More than one of `on`, `off`, or `status`.
- Any flag at all. This grammar declares none, so every `--`-prefixed token is undeclared here.
- A flag-spelled command path. The mode has one spelling, the bare word, and a `--`-prefixed variant of it is an undeclared flag like any other.

A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing; this grammar declares no flag at all, so every `--`-prefixed token is undeclared and refused as one.

## Steps

1. Parse the arguments by the rules above. An invalid form: name in one line what was wrong, then print the `## SYNOPSIS` section of the most specific recognized page verbatim and point at that path's help route — `$HERE/help/on.md`, `$HERE/help/off.md`, or `$HERE/help/status.md` with `/brief on --help`, `/brief off --help`, or `/brief status --help`. With no recognized command path, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim and point at `/brief --help` for the page in full. Change nothing and stop. Done when the form is settled, or you have stopped.
2. `status`: report whether the perspective is on or off in this conversation, in a line. Write nothing, change nothing, and stop. Done when that report is shown.
3. `on`: read [`mode.md`](references/mode.md) and adopt it as a standing instruction for the rest of this conversation; do not revisit the preceding answer. `off`: treat that standing instruction as inert history from here on, and where it was never on, say so and stop — nothing to turn off is not an error. Write nothing to any file, settings key, or scratch state, in any Harness — the state lives in this conversation and ends with it. It takes effect on this turn, so the report in step 4 already obeys it. Done when this conversation's state matches the argument.
4. Report the state this conversation is now in, in a line. Done when that report is shown.
