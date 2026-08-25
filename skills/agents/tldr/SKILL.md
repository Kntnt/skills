---
name: tldr
description: Reframe what was just said for the person who owns the outcome, and turn TL;DR mode on or off so later replies stay concise and decision-relevant.
disable-model-invocation: true
argument-hint: "[on|off] [--user] [--yes] | status [-- <instruction>]"
metadata:
  kntnt.internal: "true"
  kntnt.binaries: ""
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# tldr

Re-answer the reply above from the perspective of the person who owns the outcome, and turn the same TL;DR perspective on or off for later replies.

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is `library/` under the Manager directory beside it — `$HERE/../kntnt/library/` if it exists, else `kntnt/library/` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them); absent, tell the user to run `/kntnt update`, then stop.

## Invocation

Read `$LIBRARY/references/invocation-envelope.md` and follow it before help routing or formal validation; only the Formal Invocation reaches Help, Arguments, scripts, and nested formal parsers. `--help`, `-h`, and `help` print `$HERE/help.md` verbatim and stop, and `on`, `off`, or `status` followed by `--help` or `-h` prints `$HERE/help/on.md`, `$HERE/help/off.md`, or `$HERE/help/status.md` verbatim and stops.

## Arguments

`/tldr`, `/tldr on [--user] [--yes]`, `/tldr off [--user] [--yes]`, or `/tldr status`, and nothing else. The grammar is closed and carries no operand: `on`, `off`, and `status` are command paths, and the Formal Invocation ends where they and their flags end.

- `--user` targets the user scope. Without it the scope is this session.
- `--yes` is valid only alongside `on` or `off`.
- Anything the user wants of the replacement answer arrives as a Contextual Instruction after the reserved separator, as `/tldr -- bara säkerhetsdelen`. It may widen the range, name a language, narrow the subject, or constrain the output — each a choice this Skill's contract leaves open, which is what a Contextual Instruction may settle. Guidance that would widen the Skill's responsibility takes the context refusal of the Invocation Envelope rather than the syntax refusal below.

Invalid forms, each refused the same way:

- A token that is neither a recognized command path nor a declared flag, wherever it stands. There is no free-text operand, so `/tldr only the security part` is an invalid form rather than an instruction.
- More than one of `on`, `off`, `status`, or a command path written after a flag.
- `--user` or `--yes` on the bare form or on `status`. Neither has work to do where nothing is written.
- A flag-spelled command path. The mode has one spelling, the bare word, and a `--`-prefixed variant of it is an undeclared flag like any other.

## Steps

1. Parse the arguments by the rules above. An invalid form is refused as `$LIBRARY/references/invocation-envelope.md` says, addressing the page of the most specific recognized command path; change nothing and stop. Done when the form is settled, or you have stopped.
2. Bare form: settle the range, reading the Contextual Instruction where one was given. The default is everything you have written since the user's last input, plus whatever earlier context that range refers to and would be unintelligible without; an instruction that widens or narrows it moves it as it says. Done when the range is settled.
3. Bare form, range empty: say there is no preceding answer to reframe and stop. If compaction has made the requested range incomplete, state that limit and use only the part still visible rather than implying complete coverage. Done when the available range is known, or you have stopped.
4. Bare form: read [`mode.md`](references/mode.md). Treat the invocation as feedback that the preceding answer missed the useful level, focus, or density, and answer its substance again under that perspective; merely shortening its existing structure does not satisfy the request. Write the replacement answer under any Contextual Instruction given — the language it names, the subject it narrows to, the shape it constrains. Stop; nothing below applies to this form. Done when the replacement answer is shown.
5. `status`: report the session state, the user state, the resulting verdict, and any staleness — the block's text differing from `$HERE/references/mode.md` — naming `/tldr on --user` as the fix. Change nothing. Stop. Done when that report is shown.
6. `--user` with `on` or `off`: read [`persist.md`](references/persist.md) and follow it. Done when the block is written or removed, or you stopped at the confirmation.
7. `on` or `off`, every scope: going on, read `$HERE/references/mode.md` and adopt it as a standing instruction for subsequent replies; do not revisit the preceding answer. Going off, treat that instruction as inert history. It takes effect on this turn, so the report in step 8 already obeys it. Done when the session state matches the argument.
8. Report the scope touched, its state, and the verdict, in a line or two. Done when that report is shown.
