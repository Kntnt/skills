---
name: tldr
description: Reframe what was just said for the person who owns the outcome, and turn TL;DR mode on or off so later replies stay concise and decision-relevant.
disable-model-invocation: true
argument-hint: "[instruction ...] | [--on|--off] [--user] [--yes] | --status [-- <instruction>]"
metadata:
  kntnt.internal: "true"
  kntnt.binaries: ""
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# tldr

Re-answer the reply above from the perspective of the person who owns the outcome, and turn the same TL;DR perspective on or off for later replies.

`$HERE` is the directory that contains this SKILL.md.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

Two forms. `--on`, `--off`, or `--status` selects the mode form; anything else is the re-answer form.

- `--user` targets the user scope. Without it the scope is this session.
- `--yes` is valid only alongside `--on` or `--off`.
- Text that is not `--`-prefixed belongs to the re-answer form and is a free-form instruction in any language. It may widen the range (`all`), name a language (`sv`, `en_GB`, `engelska`, `AmE`, `svara på engelska`), or ask for anything else (`bara säkerhetsdelen`, `max 5 punkter`). Carry it out.

Invalid forms, each refused the same way:

- A `--`-prefixed token that is not `--on`, `--off`, `--status`, `--user`, or `--yes`.
- `--yes` without `--on` or `--off`.
- `--user` without `--on` or `--off`.
- More than one of `--on`, `--off`, `--status`.
- Free-form text alongside a mode form.

A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing.

## Steps

1. Parse the arguments by the rules above. An invalid form: name in one line what was wrong, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim, and point at `/tldr --help` for the page in full. Change nothing and stop. Done when the form is settled, or you have stopped.
2. Re-answer form: settle the range. Everything you have written since the user's last input, plus whatever earlier context that range refers to and would be unintelligible without. A free-form instruction moves it as it says. Done when the range is settled.
3. Re-answer form, range empty: say there is no preceding answer to reframe and stop. If compaction has made the requested range incomplete, state that limit and use only the part still visible rather than implying complete coverage. Done when the available range is known, or you have stopped.
4. Re-answer form: read [`mode.md`](references/mode.md). Treat the invocation as feedback that the preceding answer missed the useful level, focus, or density, and answer its substance again under that perspective; merely shortening its existing structure does not satisfy the request. Stop; nothing below applies to this form. Done when the replacement answer is shown.
5. `--status`: report the session state, the user state, the resulting verdict, and any staleness — the block's text differing from `$HERE/references/mode.md` — naming `/tldr --on --user` as the fix. Change nothing. Stop. Done when that report is shown.
6. `--user` with `--on` or `--off`: read [`persist.md`](references/persist.md) and follow it. Done when the block is written or removed, or you stopped at the confirmation.
7. `--on` or `--off`, every scope: going on, read `$HERE/references/mode.md` and adopt it as a standing instruction for subsequent replies; do not revisit the preceding answer. Going off, treat that instruction as inert history. It takes effect on this turn, so the report in step 8 already obeys it. Done when the session state matches the argument.
8. Report the scope touched, its state, and the verdict, in a line or two. Done when that report is shown.
