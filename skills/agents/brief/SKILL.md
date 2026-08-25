---
name: brief
description: Reframe what was just said for the person who owns the outcome, and turn Brief mode on or off so later replies stay concise and decision-relevant.
disable-model-invocation: true
argument-hint: "[on|off] [--user] [--yes] | status [-- <instruction>]"
metadata:
  kntnt.internal: "true"
  kntnt.binaries: ""
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# brief

Re-answer the reply above from the perspective of the person who owns the outcome, and turn the same Brief perspective on or off for later replies.

`$HERE` is the directory that contains this SKILL.md.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop. If they are `on --help` or `on -h`, print `$HERE/help/on.md` verbatim and stop. If they are `off --help` or `off -h`, print `$HERE/help/off.md` verbatim and stop. If they are `status --help` or `status -h`, print `$HERE/help/status.md` verbatim and stop.

## Arguments

`/brief`, `/brief on [--user] [--yes]`, `/brief off [--user] [--yes]`, or `/brief status`, and nothing else. The grammar is closed and carries no operand: `on`, `off`, and `status` are command paths, and the Formal Invocation ends where they and their flags end.

- `--user` targets the user scope. Without it the scope is this session.
- `--yes` is valid only alongside `on` or `off`.
- Anything the user wants of the replacement answer arrives as a Contextual Instruction after the reserved separator, as `/brief -- bara säkerhetsdelen`. It may widen the range, name a language, narrow the subject, or constrain the output — each a choice this Skill's contract leaves open, which is what a Contextual Instruction may settle. Guidance that would widen the Skill's responsibility takes the context refusal of the Invocation Envelope rather than the syntax refusal below.

Invalid forms, each refused the same way:

- A token that is neither a recognized command path nor a declared flag, wherever it stands. There is no free-text operand, so `/brief only the security part` is an invalid form rather than an instruction.
- More than one of `on`, `off`, `status`, or a command path written after a flag.
- `--user` or `--yes` on the bare form or on `status`. Neither has work to do where nothing is written.
- A flag-spelled command path. The mode has one spelling, the bare word, and a `--`-prefixed variant of it is an undeclared flag like any other.

A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing.

## Steps

1. Parse the arguments by the rules above. An invalid form: name in one line what was wrong, then print the `## SYNOPSIS` section of the most specific recognized page verbatim and point at that path's help route — `$HERE/help/on.md`, `$HERE/help/off.md`, or `$HERE/help/status.md` with `/brief on --help`, `/brief off --help`, or `/brief status --help`. With no recognized command path, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim and point at `/brief --help` for the page in full. Change nothing and stop. Done when the form is settled, or you have stopped.
2. Bare form: settle the range, reading the Contextual Instruction where one was given. The default is everything you have written since the user's last input, plus whatever earlier context that range refers to and would be unintelligible without; an instruction that widens or narrows it moves it as it says. Done when the range is settled.
3. Bare form, range empty: say there is no preceding answer to reframe and stop. If compaction has made the requested range incomplete, state that limit and use only the part still visible rather than implying complete coverage. Done when the available range is known, or you have stopped.
4. Bare form: read [`mode.md`](references/mode.md). Treat the invocation as feedback that the preceding answer missed the useful level, focus, or density, and answer its substance again under that perspective; merely shortening its existing structure does not satisfy the request. Write the replacement answer under any Contextual Instruction given — the language it names, the subject it narrows to, the shape it constrains. Stop; nothing below applies to this form. Done when the replacement answer is shown.
5. `status`: report the session state, the user state, the resulting verdict, and any staleness — the block's text differing from `$HERE/references/mode.md` — naming `/brief on --user` as the fix. Change nothing. Stop. Done when that report is shown.
6. `--user` with `on` or `off`: read [`persist.md`](references/persist.md) and follow it. Done when the block is written or removed, or you stopped at the confirmation.
7. `on` or `off`, every scope: going on, read `$HERE/references/mode.md` and adopt it as a standing instruction for subsequent replies; do not revisit the preceding answer. Going off, treat that instruction as inert history. It takes effect on this turn, so the report in step 8 already obeys it. Done when the session state matches the argument.
8. Report the scope touched, its state, and the verdict, in a line or two. Done when that report is shown.
