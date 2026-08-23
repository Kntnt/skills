# tldr

## NAME

tldr - reframe the previous response or keep later responses concise

## SYNOPSIS

**/tldr** [*INSTRUCTION*...] [**--** *INSTRUCTION*]

**/tldr** (**--on**|**--off**) [**--user**] [**--yes**] [**--** *INSTRUCTION*]

**/tldr** **--status** [**--** *INSTRUCTION*]

## DESCRIPTION

`tldr` has two modes of operation. Without a mode option it treats the invocation as feedback that the preceding answer missed the useful level, focus, or density, then answers that substance again together with any earlier context needed to understand it. It reframes even an answer that was already short instead of merely compressing the same structure.

The replacement answer speaks to a technically capable person who owns the outcome without expecting them to hold every implementation detail. It leads with the conclusion, keeps practical implications and material decisions, omits internal mechanics by default, and uses whatever structure fits the content. Any action or decision genuinely requiring the user is explicit; no heading, list, or empty verdict is mandatory.

With `--on` or `--off`, the Skill controls the same perspective as a standing instruction for subsequent replies. Turning it on does not revisit or summarise the preceding answer. An explicit request for more detail overrides its default level for that reply.

TL;DR mode applies to replies in the conversation, not to source files, documentation, comments, commit messages, other artifacts, or general-purpose text and file compression.

## POSITIONAL ARGUMENTS

*INSTRUCTION*...

Free-form instructions for the replacement answer, in any language. They may widen the range, select a language, narrow the subject, or constrain the output.

## OPTIONS

**--on**

Enable TL;DR mode for the selected scope.

**--off**

Disable TL;DR mode for the selected scope.

**--status**

Report session and user state, the effective verdict, and any stale managed block. It changes nothing and cannot be combined with the other options.

**--user**

Target this Harness's user context instead of the current session. The Skill shows the file and exact managed block before writing.

**--yes**

Write or remove the user block without waiting for confirmation. It is valid only with `--on` or `--off`.

## SCOPES

**session**

The default. It applies only to subsequent replies in the current conversation and is stored nowhere else. Context compaction may drop it.

**user**

A managed block in this Harness's global context file. There is no Project scope because conversational perspective and density are reader preferences rather than a shared Project convention.

## DIAGNOSTICS

An incomplete or invalid form is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, changes nothing, and points to `/tldr --help`. In particular, `/tldr --user` and `/tldr --yes` are invalid, while `/tldr --on --user --yes` is valid.

A replacement answer whose requested range is partly unavailable after context compaction states that limit instead of presenting an incomplete result as complete.

## EXAMPLES

**/tldr bara säkerhetsdelen**

Re-answer only the security-related part of the previous response.

**/tldr --on --user**

Show and confirm a user-level block that keeps later replies concise and decision-relevant in the current Harness without revisiting the preceding answer.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

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

**/delegation --help**, **/kntnt select**
