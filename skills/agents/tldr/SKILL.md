---
name: tldr
description: Re-explain the answer just given for a senior developer who delegated the work and therefore does not hold its details, and say plainly what it now asks of them.
disable-model-invocation: true
argument-hint: '[<instruction>] [-- <instruction>]'
metadata:
  kntnt.internal: "true"
  kntnt.binaries: ""
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# tldr

Explain the reply above again for somebody who did not follow it. The answer is treated as correct and inaccessible, never as bloated, so what comes back carries the background the original assumed and ends by naming what is now required of the reader.

`$HERE` is the directory that contains this SKILL.md.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

`/tldr [<instruction>]`, and nothing else. The grammar is the Skill name and one optional free-text operand: there is no subcommand, no flag, and nothing that can be missing.

- The operand is an instruction about how the re-explanation is written. It may narrow the subject, name a language, or constrain the output — each a choice this Skill's contract leaves open. Anything that would widen the Skill's responsibility takes the context refusal of the Invocation Envelope rather than the refusal below.
- The same instruction may arrive as a Contextual Instruction behind the reserved separator. `/tldr bara säkerhetsdelen` and `/tldr -- bara säkerhetsdelen` are both valid and mean the same thing: with no command path in the grammar there is no verb for prose to shadow, so the separator is offered here rather than required.
- A token that opens with a dash is part of that instruction like any other word. This grammar declares no flag, so `/tldr --foo bar` is guidance to obey as written or to refuse as guidance that widens the Skill, and never an undeclared flag.

The one invalid form is a malformed Envelope: a reserved separator with no instruction behind it. Nothing else here is a syntax refusal, there being no flag to be undeclared and no form to be incomplete. A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing; here the same rule is what makes a dash-token prose, this grammar having no flag for one to be mistaken for.

## Steps

1. Parse the arguments by the rules above. An invalid form: name in one line what was wrong, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim, and point at `/tldr --help` for the page in full. Change nothing and stop. Done when the form is settled, or you have stopped.
2. Settle the range. It is the preceding assistant output, plus whatever earlier context that output refers to and would be unintelligible without. It is never a pasted document, a file, or tool output the user points at — those are things to act on, and this Skill acts on what was said about them. An instruction may narrow the range; it cannot move it off the preceding answer. Done when the range is settled.
3. Range empty: say there is no preceding answer to explain and stop. Where compaction has left the range incomplete, state that limit and use only the part still visible rather than implying complete coverage. Done when the available range is known, or you have stopped.
4. Read [`mode.md`](references/mode.md) and re-explain the range under it. Treat the invocation as evidence that the answer was pitched at the wrong reader, not that it was too long for its own purpose: it may be an article, a research answer, a requested explanation, review output, or a long design discussion, each long with reason. Start from what the answer meant and say that instead; rewriting its sentences more tersely does not satisfy the request. Write under the instruction given — the language it names, the subject it narrows to, the shape it constrains. Done when the re-explanation is shown.
5. Close it by naming what the user must do, decide, or answer. Where nothing is required of them, say that explicitly rather than ending without the line. Done when the closing action line is present.
