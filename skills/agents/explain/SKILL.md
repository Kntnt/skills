---
name: explain
description: Explain the reply just given, or whatever the instruction names, better than it was explained the first time.
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

# explain

Run `uv run "$HERE/scripts/invoke.py"` — `$HERE` is the directory that holds this SKILL.md — with everything the user typed after `/explain`, verbatim and however many lines, on stdin. Exit 0: do what it prints. Any other exit: show what it printed to the user verbatim, and stop.

## Arguments

If there is an argument, it is an instruction on what the user would like you to explain. The same instruction may arrive as a Contextual Instruction behind the reserved separator, so `operands` and `instruction` are read as one instruction between them. If no arguments are provided, the user wants you to explain your last response.

## Steps

1. Settle the subject: the reply just given, or what the instruction names in it or earlier in the conversation. If there is nothing to explain, say so and stop. Done when the subject is settled, or you have stopped.
2. Write the explanation for the reader below, under the instruction given — the language it names, the part it narrows to, the shape it constrains. Done when it is short enough to be read and long enough that the reader could afterwards explain the matter to somebody else in their own words.

## The reader

The reader is clever but busy: they own the outcome and have not followed the work. Speak to them as a trusted colleague, not as an implementer handing over every internal detail.

- **Open with the context they need.** One very short paragraph that makes the rest intelligible. Established terms and abbreviations stay; any other is explained where it is introduced. Where the project defines its own terms, in a `CONTEXT.md` or the like, use them rather than a synonym, and explain each where it is introduced like any other term the reader may not hold.
- **Explain rather than summarise.** Start from what the matter means and say that, better than the earlier reply did; the same reply in fewer words is not it.
- **Select before you compress.** Keep what affects practical implications, behaviour, trade-offs, risks, scope, cost, or future options, and every fact, negation, quantity, exception, condition, and limitation that could change what the reader understands, decides, or has to do. Reproduce a command, value, identifier, error, or quotation verbatim where it is material. Leave out work logs, step-by-step narration, discarded approaches, file-level mechanics, and exhaustive alternatives unless they are material or asked for.
- **Write like a manual, whatever the subject.** Short sentences, one idea each, in the active voice. One word for one thing throughout; never a synonym for variety. Verbs over chains of nouns.
- **Plain and exact.** State real uncertainty plainly, without hedging or ritual pleasantries. Error reports, failing test output, security warnings, and confirmations for destructive actions keep their full content.
- **Shape follows content.** No heading, list, table, or verdict line is mandatory; use structure only where there is real structure.
- **Make what is expected of the reader unmistakable.** A decision gets a brief basis and a recommendation; an action gets its reason. Where nothing is required of them, say nothing about it, and stop once they have enough to understand the outcome.
