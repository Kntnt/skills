---
name: tldr
description: Summarise what was just said as a TL;DR, and turn TL;DR mode on or off so replies stay short and say what needs you.
disable-model-invocation: true
argument-hint: "[instruction] | [--on|--off|--status] [--user] [--yes]"
metadata:
  internal: true
  # Empty on purpose: this skill has no dependencies, so it runs no checker
  # (ADR-0012). Leave the key bare. `kntnt: {}` parses to the string "{}" and
  # catalog generation then reports a block that is visibly present as missing
  # (issue #48).
  kntnt:
---

# tldr

Summarise the reply above so the user can see what happened and whether anything needs them, and turn TL;DR mode on or off.

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

Two forms. `--on`, `--off`, or `--status` selects the mode form; anything else is the summarise form.

- `--user` targets the user scope. Without it the scope is this session.
- `--yes` is valid only alongside `--on` or `--off`.
- Text that is not `--`-prefixed belongs to the summarise form and is a free-form instruction in any language. It may widen the range (`all`), name a language (`sv`, `en_GB`, `engelska`, `AmE`, `svara på engelska`), or ask for anything else (`bara säkerhetsdelen`, `max 5 punkter`). Carry it out.

Invalid forms, each refused the same way:

- A `--`-prefixed token that is not `--on`, `--off`, `--status`, `--user`, or `--yes`.
- `--yes` without `--on` or `--off`.
- `--user` without `--on`, `--off`, or `--status`.
- More than one of `--on`, `--off`, `--status`.
- Free-form text alongside a mode form.

A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing (ADR-0029).

## Steps

1. Parse the arguments by the rules above. An invalid form: name in one line what was wrong, print the `## Synopsis` section of `$HERE/help.md` verbatim, and point at `/tldr --help` for the page in full. Change nothing and stop. Done when the form is settled, or you have stopped.
2. Summarise form: settle the range. Everything you have written since the user's last input, plus whatever earlier context that range refers to and would be unintelligible without. A free-form instruction moves it as it says. Done when the range is settled.
3. Summarise form, range empty or already short: say that in a sentence or two, say whether anything in it needs the user, and stop. A summary longer than what it summarises is theatre. Done when that is said.
4. Summarise form: read [`shape.md`](shape.md) and render the range by it. Stop; nothing below applies to this form. Done when the summary is shown.
5. `--status`: report the session state, the user state, the resulting verdict, and any staleness — the block's text differing from `$HERE/mode.md` — naming `/tldr --on --user` as the fix. Change nothing. Stop. Done when that report is shown.
6. `--user` with `--on` or `--off`: read [`persist.md`](persist.md) and follow it. Done when the block is written or removed, or you stopped at the confirmation.
7. `--on` or `--off`, every scope: going on, read `$HERE/mode.md` and adopt it as a standing instruction for the rest of this session. Going off, treat that instruction as inert history. It takes effect on this turn, so the report in step 8 already obeys it. Done when the session state matches the argument.
8. Report the scope touched, its state, and the verdict, in a line or two. Done when that report is shown.
