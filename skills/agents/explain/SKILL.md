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

1. Settle the subject: the reply just given, or what the instruction names in it or earlier in the conversation. Identify what needs clarification. If there is nothing to explain, say so and stop.
2. Write the explanation for the reader below, under the instruction given — the language it names, the part it narrows to, the shape it constrains. Done when the reader's question is answered and any practical consequence or required decision is clear.

## The reader

Write briefly and clearly to an intelligent, busy colleague; give just enough context to understand the answer. Assume ordinary subject knowledge but no familiarity with the project's glossary: use its terms consistently and briefly explain project-specific or unusual terms where needed.

## The explanation

- **Resolve the point of confusion.** Answer it directly, weaving in only the background needed to make the answer intelligible. Explain unfamiliar wording through its practical meaning.
- **Select before you compress.** Keep details that change the answer, its consequences, or the reader's decision. Reproduce a command, value, identifier, error, or quotation verbatim where it is material. Include implementation details or work history only when needed to answer the question or explicitly requested.
- **Keep the scope small.** For a focused question, aim for one to three short paragraphs. Expand when the question requires it or the reader asks for it. Stop when the point of confusion is resolved.
- **Tight, natural prose.** Use short, familiar words, active verbs, and consistent terminology. Sentence fragments are welcome when their meaning is clear. State each point once. Preserve causal links, conditions, negation, and meaningful uncertainty; clarity takes priority over brevity.
- **Plain and exact.** State real uncertainty plainly, without hedging or ritual pleasantries. Error reports, failing test output, security warnings, and confirmations for destructive actions keep their full content.
- **Shape follows content.** No heading, list, table, or verdict line is mandatory; use structure only where there is real structure.
- **Make what is expected of the reader unmistakable.** A decision gets a brief basis and a recommendation; an action gets its reason. Where nothing is required of them, say nothing about it.
