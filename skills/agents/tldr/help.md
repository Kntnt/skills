# tldr

## NAME

tldr - explain the answer just given to whoever delegated the work and did not follow it

## SYNOPSIS

**/tldr** [*INSTRUCTION*] [**--** *INSTRUCTION*]

## DESCRIPTION

`tldr` answers the preceding reply again, for a senior developer who delegated the work and therefore does not hold its details. The reply is treated as correct but pitched at the wrong reader: what comes back carries the background the original assumed and unpacks the vocabulary that belongs to this work alone, while ordinary technical terms stay as they were.

This is a re-explanation and not a compression. Rewriting the previous answer's sentences more tersely does not satisfy it; the Skill starts from what the answer meant and says that instead. Its usual input is text that is long with reason — an article, a research answer, a requested explanation, review output, a long design discussion — so length is never on its own a reason to cut.

Every reply ends by naming what the user must do, decide, or answer. Where nothing is required of them, the closing line says so rather than being omitted: the Skill is invoked because the user is not reading closely, and an action buried mid-text is an action missed.

The range is the preceding assistant output, plus whatever earlier context that output refers to and would be unintelligible without. A pasted document, a file, or tool output the user points at is never the range. Where nothing precedes the invocation, the Skill says so and writes nothing. Where compaction has left the range incomplete, it states that limit and uses only what is still visible.

The Skill writes one reply and changes nothing. It adopts no standing mode, and how later replies are written is untouched.

## POSITIONAL ARGUMENTS

*INSTRUCTION*

An instruction about how the re-explanation should be written. It may narrow the subject, name a language, or constrain the output. It is optional, and everything after the Skill name belongs to it, dash-prefixed words included — this grammar declares no flag, so a token such as `--foo` is part of the instruction rather than an undeclared option.

This is the same instruction the reserved separator carries, offered without the separator because a grammar with no command path has no verb for prose to shadow.

## DIAGNOSTICS

The Skill takes one optional free-text instruction and no options. It declares no flag, so a dash-prefixed token is read as part of the instruction; where a flag would have no work to do it is refused rather than ignored, never accepted and quietly dropped. A malformed Envelope — a separator with no instruction behind it — names the error, prints the SYNOPSIS, writes nothing, and points to `/tldr --help`.

An instruction that would widen the Skill's responsibility, such as one asking it to explain a file or a pasted document instead of the preceding answer, takes the context refusal rather than the syntax refusal.

An empty range is reported and is not an error: nothing precedes the invocation, so nothing is written.

## EXAMPLES

Explain the reply above, with no further instruction.

```
/tldr
```

Explain it in Swedish, and only the part about security. The reserved separator is accepted here and changes nothing, this grammar having no command path for the text to be mistaken for.

```
/tldr bara säkerhetsdelen
/tldr -- bara säkerhetsdelen
```

Ask for a constraint on the output. A dash-prefixed word inside the instruction is part of it, so this asks for an explanation that does not stop at the `--yes` flag rather than passing one.

```
/tldr förklara vad --yes gör, inte bara att det finns
```

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

The Manager must be Enabled: its Collection Library carries the Invocation Envelope contract this Skill reads before anything else. Nothing beyond it — no `uv`, no peer Skill, and no Harness Capability.

## SEE ALSO

**/brief --help**, **/delegation --help**, **/kntnt select**
