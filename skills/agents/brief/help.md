# brief

## NAME

brief - reframe the previous response or keep later responses concise

## SYNOPSIS

**/brief** [**--** *INSTRUCTION*]

**/brief** (**on**|**off**) [**--user**] [**--yes**] [**--** *INSTRUCTION*]

**/brief** **status** [**--** *INSTRUCTION*]

## DESCRIPTION

Bare `brief` re-answers the preceding response at a more useful level, focus, or density. It leads with the conclusion and keeps practical implications, decisions, and required user actions.

`on` and `off` control the same perspective for later replies. Turning it on does not revisit the preceding answer, and an explicit request for detail overrides the mode for that reply.

The Skill takes no free-text operand. Put any narrowing or output guidance after `--`, as `/brief -- only the security part`.

Brief mode affects conversation replies, not code, documentation, commit messages, or other artifacts.

## COMMANDS

**on**

Enable Brief mode for the selected scope.

**off**

Disable Brief mode for the selected scope.

**status**

Report session and user state, the effective verdict, and any stale managed block, without writing anything.

## OPTIONS

**--user**

Target this Harness's user context instead of the current session. The Skill shows the file and exact managed block before writing.

**--yes**

Write or remove the user block without waiting for confirmation. It is valid only with `on` or `off`.

## SCOPES

**session**

The default. It applies only to subsequent replies in the current conversation and is stored nowhere else. Context compaction may drop it.

**user**

A managed block in this Harness's global context file. There is no Project scope because conversational perspective and density are reader preferences rather than a shared Project convention.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints the most specific SYNOPSIS, changes nothing, and points to that page. A flag is refused rather than ignored where it has no work to do here.

**--user** and **--yes** require `on` or `off`. Unseparated text and a second command path are invalid.

If context compaction removed part of the requested range, the replacement answer states that limit.

## EXAMPLES

**/brief -- bara säkerhetsdelen**

Re-answer only the security-related part of the previous response, the narrowing arriving as a Contextual Instruction.

**/brief on --user**

Show and confirm a user-level block that keeps later replies concise and decision-relevant in the current Harness without revisiting the preceding answer.

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

**/brief on --help**, **/brief off --help**, **/brief status --help**, **/delegation --help**, **/kntnt select**
