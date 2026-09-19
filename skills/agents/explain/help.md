# explain

## NAME

explain - explain the reply just given, or whatever the instruction names, better than it was explained the first time

## SYNOPSIS

**/explain** [*INSTRUCTION*] [**--** *INSTRUCTION*]

## DESCRIPTION

`explain` gives an intelligent, busy colleague a brief, clear explanation. Without an instruction it explains the reply just given; with one it explains whatever the instruction names — a decision, a term, a part of that reply, a thing said earlier in the conversation.

The reply answers the point needing clarification directly, with only the background needed to understand it. It assumes ordinary subject knowledge but no familiarity with the project's glossary: project terms are used consistently, and project-specific or unusual terms are briefly explained where needed.

A focused question normally gets one to three short paragraphs; the reply expands when the question requires it or the reader asks. It keeps details that change the answer, its consequences, or the reader's decision. Implementation details and work history appear only when needed to answer the question or explicitly requested.

The prose uses short, familiar words and may use sentence fragments where the meaning is clear. Each point is stated once, with causal links, conditions, negation, and meaningful uncertainty preserved. Error reports, failing test output, security warnings, and confirmations for destructive actions keep their full content.

Where a decision is expected of the reader, the reply gives a brief basis for it and a recommendation. Where an action is expected, it says why. Where nothing is required, the reply says nothing about it and stops.

The Skill writes one reply and changes nothing. It adopts no standing mode, and how later replies are written is untouched.

## POSITIONAL ARGUMENTS

*INSTRUCTION*

An instruction on what to explain and how. It may name the subject, narrow it to a part of the earlier reply, name a language, or constrain the output. It is optional, and everything after the Skill name belongs to it, dash-prefixed words included — this grammar declares no flag, so a token such as `--foo` is part of the instruction rather than an undeclared option. The reserved separator carries the same instruction, and the two spellings are one invocation with one meaning.

## DIAGNOSTICS

The Skill takes one optional free-text instruction and no options. It declares no flag, so a dash-prefixed token is read as part of the instruction. A malformed Envelope — a separator with no instruction behind it — is refused rather than ignored: the Skill names the error, prints the SYNOPSIS, writes nothing, and points to `/explain --help`.

An instruction that would widen the Skill, such as one asking it to change a file or run a command instead of explaining something, takes the context refusal rather than the syntax refusal.

Where nothing precedes the invocation and no instruction names a subject, the Skill says so and explains nothing; that is reported and is not an error.

## EXAMPLES

Explain the reply above, with no further instruction.

```
/explain
```

Explain one part of it, in Swedish. The two spellings are one invocation.

```
/explain bara säkerhetsdelen
/explain -- bara säkerhetsdelen
```

Explain something said earlier rather than the reply just given.

```
/explain the trade-off behind the caching decision we settled earlier
```

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv`, which runs the Manager's invocation engine, and the Manager itself: its Collection Library carries the Invocation Envelope contract a Contextual Instruction is applied under. No peer Skill and no Harness Capability.

## SEE ALSO

**/kntnt select**
