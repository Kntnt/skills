# brief

## NAME

brief - reframe the previous response or keep later responses concise

## SYNOPSIS

**/brief** [**--** *INSTRUCTION*]

**/brief** (**on**|**off**) [**--user**] [**--yes**] [**--** *INSTRUCTION*]

**/brief** **status** [**--** *INSTRUCTION*]

## DESCRIPTION

`brief` has two modes of operation. Without a command path it treats the invocation as feedback that the preceding answer missed the useful level, focus, or density, then answers that substance again together with any earlier context needed to understand it. It reframes even an answer that was already short instead of merely compressing the same structure.

The replacement answer speaks to a technically capable person who owns the outcome without expecting them to hold every implementation detail. It leads with the conclusion, keeps practical implications and material decisions, omits internal mechanics by default, and uses whatever structure fits the content. Any action or decision genuinely requiring the user is explicit; no heading, list, or empty verdict is mandatory.

With `on` or `off`, the Skill controls the same perspective as a standing instruction for subsequent replies. Turning it on does not revisit or summarise the preceding answer. An explicit request for more detail overrides its default level for that reply.

The grammar is closed: the Skill takes no free-text operand, and nothing beyond a command path and its flags belongs before the reserved separator. A request that widens the range, names a language, narrows the subject, or constrains the output is a Contextual Instruction and is written after `--`, as `/brief -- only the security part`.

Brief mode applies to replies in the conversation, not to source files, documentation, comments, commit messages, other artifacts, or general-purpose text and file compression.

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

An incomplete or invalid form is refused rather than ignored. The Skill names the error, prints the `SYNOPSIS` of the most specific recognized page, changes nothing, and points at that path's help route: `/brief on --nonsense` is answered with the grammar of `on` rather than with the whole Skill's. A flag is refused rather than ignored where it has no work to do here, so `/brief --user` and `/brief --yes` are invalid without `on` or `off`, while `/brief on --user --yes` is valid.

Unseparated text is not an instruction. A token after the Skill name or after a command path that is neither a recognized command path nor a declared flag is an invalid form, and so is a second command path; `/brief only the security part` is refused rather than obeyed.

A replacement answer whose requested range is partly unavailable after context compaction states that limit instead of presenting an incomplete result as complete.

## EXAMPLES

**/brief -- bara säkerhetsdelen**

Re-answer only the security-related part of the previous response, the narrowing arriving as a Contextual Instruction.

**/brief on --user**

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

**/brief on --help**, **/brief off --help**, **/brief status --help**, **/delegation --help**, **/kntnt select**
