# explain

## NAME

explain - explain the reply just given, or whatever the instruction names, better than it was explained the first time

## SYNOPSIS

**/explain** [*INSTRUCTION*] [**--** *INSTRUCTION*]

## DESCRIPTION

`explain` answers for a clever but busy reader who does not keep track of the work in progress. Without an instruction it explains the reply just given; with one it explains whatever the instruction names — a decision, a term, a part of the answer, a thing said earlier in the conversation.

This is an explanation and not a summary. The Skill starts from what the reader needs in their current role, opens with the context they need to follow the answer, and then explains the matter better than the earlier reply did rather than restating it in fewer words. Terms and abbreviations that are not widely established are explained before they are used.

What comes back keeps facts, negations, quantities, exceptions, conditions, and limitations that could change what the reader understands, decides, or has to do, and leaves out work logs, step-by-step narration, discarded approaches, and file-level mechanics unless they are material or asked for. Error reports, failing test output, security warnings, and confirmations for destructive actions keep their full content.

Where a decision is expected of the reader, the reply gives a brief basis for it and a recommendation. Where an action is expected, it says why. Where nothing is required, the reply says nothing about it and stops.

The Skill writes one reply and changes nothing. It adopts no standing mode, and how later replies are written is untouched.

## POSITIONAL ARGUMENTS

*INSTRUCTION*

An instruction on what to explain and how. It may name the subject, narrow it to a part of the earlier reply, name a language, or constrain the output. It is optional, and everything after the Skill name belongs to it, dash-prefixed words included — this grammar declares no flag, so a token such as `--foo` is part of the instruction rather than an undeclared option.

This is the same instruction the reserved separator carries, offered without the separator because a grammar with no command path has no verb for prose to shadow.

## DIAGNOSTICS

The Skill takes one optional free-text instruction and no options. It declares no flag, so a dash-prefixed token is read as part of the instruction; where a flag would have no work to do it is refused rather than ignored, never accepted and quietly dropped. A malformed Envelope — a separator with no instruction behind it — names the error, prints the SYNOPSIS, writes nothing, and points to `/explain --help`.

An instruction that would widen the Skill's responsibility, such as one asking it to change a file or run a command instead of explaining something, takes the context refusal rather than the syntax refusal.

Where no reply precedes the invocation and no instruction names a subject, the Skill says so; that is reported and is not an error.

## EXAMPLES

Explain the reply above, with no further instruction.

```
/explain
```

Explain one part of it, in Swedish. The reserved separator is accepted here and changes nothing, this grammar having no command path for the text to be mistaken for.

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

**/delegation --help**, **/kntnt select**
