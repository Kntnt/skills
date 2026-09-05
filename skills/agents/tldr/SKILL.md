---
name: tldr
description: Re-explain the answer just given for a senior developer who delegated the work and therefore does not hold its details, and say plainly what it now asks of them.
disable-model-invocation: true
argument-hint: '[<instruction>] [-- <instruction>]'
compatibility: Requires uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# tldr

Explain the reply above again for somebody who did not follow it. The answer is treated as correct and inaccessible, never as bloated, so what comes back carries the background the original assumed and ends by naming what is now required of the reader.

`$HERE` is the directory that contains this SKILL.md, and `$MANAGER` is the Manager directory: `$HERE/../kntnt/` if it exists, else `kntnt/` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Neither found: tell the user to install the Manager (`npx skills add Kntnt/skills`) and stop. `$LIBRARY` is `$MANAGER/library/` — absent, tell the user to run `/kntnt update`, then stop.

Run `uv run "$MANAGER/scripts/kntnt.py" invoke --here="$HERE"` with the invocation payload — everything the user typed after `/tldr`, verbatim, however many lines — on stdin. On exit 0, answer the `capabilities` in its `dependencies` first: for each one, say whether its `confirm` sentence is true of you, and where it is not, give its `how`, change nothing, and stop. Then continue from the JSON. On any other exit print its stdout verbatim and stop: it has already printed what the user is to see, and none of that text is yours to write.

In the JSON, `path` is the command path as a list, `flags` holds each flag the user wrote — `true` where it stood bare, its value where it carried one, a list of values where it was repeated — `operands` is what followed the flags, in order, and `instruction` is the Contextual Instruction, or `null`, applied as `$LIBRARY/references/invocation-envelope.md` says.

## Arguments

The operand is an instruction about how the re-explanation is written. It may narrow the subject, name a language, or constrain the output — each a choice this Skill's contract leaves open. The same instruction may arrive as a Contextual Instruction behind the reserved separator: `/tldr bara säkerhetsdelen` and `/tldr -- bara säkerhetsdelen` are one invocation with one meaning, so `operands` and `instruction` are read as one instruction between them.

## Steps

1. Settle the range. It is the preceding assistant output, plus whatever earlier context that output refers to and would be unintelligible without. It is never a pasted document, a file, or tool output the user points at — those are things to act on, and this Skill acts on what was said about them. An instruction may narrow the range; it cannot move it off the preceding answer. Done when the range is settled.
2. Range empty: say there is no preceding answer to explain and stop. Where compaction has left the range incomplete, state that limit and use only the part still visible rather than implying complete coverage. Done when the available range is known, or you have stopped.
3. Read [`mode.md`](references/mode.md) and re-explain the range under it. Treat the invocation as evidence that the answer was pitched at the wrong reader, not that it was too long for its own purpose: it may be an article, a research answer, a requested explanation, review output, or a long design discussion, each long with reason. Start from what the answer meant and say that instead; rewriting its sentences more tersely does not satisfy the request. Write under the instruction given — the language it names, the subject it narrows to, the shape it constrains. Done when the re-explanation is shown.
4. Close it by naming what the user must do, decide, or answer. Where nothing is required of them, say that explicitly rather than ending without the line. Done when the closing action line is present.
