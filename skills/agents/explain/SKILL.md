---
name: explain
description: Provides a better explanation of what is specified in the argument, or of the reply that has just been given if there is no argument.
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

# Explain

## Arguments

If there is an argument, it is an instruction on what the user would like you to explain. The same instruction may arrive as a Contextual Instruction behind the reserved separator, so `operands` and `instruction` are read as one instruction between them. If no arguments are provided, the user wants you to explain your last response.

## Instructions

The user is a clever but busy person. They do not keep track of your work progress. They therefore ask you to explain things briefly and clearly.

### Step 1: Get the request

1. Run `uv run "$HERE/scripts/invoke.py"` — `$HERE` is the directory that holds this SKILL.md — with everything the user typed after `/explain`, verbatim and however many lines, on stdin. Exit 0: do what it prints. Any other exit: show what it printed to the user verbatim, and stop.

### Step 2: Reasoning

2. Put yourself in the user’s shoes and understand what they need in their current role.

3. Consider the relevant parts of what has been said earlier in the session in relation to the request.

4. Choose what matters from the user's perspective.

### Step 3. Formulate a response

5. Formulera ett svar without wasted words. Maximise relevant meaning per token, but lose nothing that could change their understanding, decision, or required action.

6. Keep what affects practical implications, behaviour, material trade-offs, risks, scope, cost, or future options. Leave out work logs, step-by-step narration, discarded approaches, file-level mechanics, and exhaustive alternatives unless they are material or asked for.

7. Make reasonable in-scope choices yourself. Ask only about choices that materially change the outcome, and recommend a default when you do.

8. Skip hedging and ritual pleasantries. Preserve facts, negations, quantities, exceptions, conditions, and limitations. State real uncertainty plainly. Reproduce a command, value, identifier, error, or quotation verbatim when it is material.

9. No heading, list, table, or verdict line is mandatory; use structure only where there is real structure. Make any action or decision required from the user unmistakable; where nothing is required, say nothing about it and stop once they have enough to understand the outcome.

10. Error reports, failing test output, security warnings, and confirmations for destructive actions keep their full content.

### Step 4: Deliver the response

11. Speak as a trusted colleague to the person who owns the outcome, not as an implementer handing over every internal detail.

12. Use terms and abbreviations that are established and widely recognised. Any other terms and abbreviations should be briefly explained before they are used.

13. Do not assume that the user has a full understanding of the subject matter; start with a very short paragraph that provides the context necessary to understand the answer.

14. Briefly explain what the user asked you to explain. Make serious effort to explain it better; don’t just summarise an answer you’ve already given.

15. State clearly what is expected of the user. If the user is expected to make a decision, provide a brief basis for the decision and a recommendation. If the user is expected to perform an action, explain why.
