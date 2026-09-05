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

[**--** *INSTRUCTION*] adds an optional Contextual Instruction. The first standalone, unquoted `--` is the reserved separator. Everything before it is the Formal Invocation; everything after it, including later `--` tokens, is guidance. The guidance may start on the same line or after blank lines and must contain non-whitespace text.

`--force`, `foo--bar`, `` `--` ``, and `"--"` are not separators. Without the separator, the whole payload remains formal input, including later lines and paragraphs.

After validating the Formal Invocation, the Skill uses guidance to clarify or narrow open choices. Guidance cannot contradict formal input or an invariant, widen the Skill, bypass a gate, or request unrelated work. Redundant but applicable guidance is valid. Applicable Conversation Context follows the same limits.

Malformed formal input or an empty instruction takes the syntax refusal. The Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Context on an exact help route takes the context refusal without rendering the page.

Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal. The Skill names the guidance and its boundary, reports the mutation outcome, prints no synopsis, and stops without applying a valid remainder.

Unaddressable guidance can affect nothing inside the Skill's contract. Guidance settled by a documented precedence is suppressed instead: the run continues and reports the suppression where useful. Suppression for one parameter does not invalidate guidance that applies to another.

Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict appears only after a legitimate effect, it stops before the next effect and reports the exact partial outcome. It rolls nothing back unless atomic behaviour was promised.

A nested Skill receives only relevant guidance through an explicit Contextual Instruction. Successful execution requires no context acknowledgement; an existing report names a materially changed choice where useful.

The following schematic cases pin the split independently of any one Skill's Formal Invocation grammar; `\n\n` denotes two newline characters in one payload.

| Case | Envelope | Formal Invocation | Contextual Instruction | Outcome |
| --- | --- | --- | --- | --- |
| Same line | `/skill --force -- Preserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |
| Blank lines | `/skill --force --\n\nPreserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |
| Empty suffix | `/skill --force --   ` | `/skill --force` | — | Syntax refusal |
| Later separator | `/skill -- Preserve -- deployment facts` | `/skill` | `Preserve -- deployment facts` | Envelope valid; formal grammar next |
| No separator | `/skill Preserve deployment facts` | `/skill Preserve deployment facts` | — | No split; formal grammar decides |
| Attached and quoted | ``/skill --force foo--bar `--` "--"`` | ``/skill --force foo--bar `--` "--"`` | — | No split; formal grammar decides |
| Exact help | `/skill --help -- Explain this page` | `/skill --help` | `Explain this page` | Context refusal; render nothing |

## DEPENDENCIES

None.

## SEE ALSO

**/brief --help**, **/delegation --help**, **/kntnt select**
