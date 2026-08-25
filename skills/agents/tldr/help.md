# tldr

## NAME

tldr - reframe the previous response or keep later responses concise

## SYNOPSIS

**/tldr** [**--** *INSTRUCTION*]

**/tldr** (**on**|**off**) [**--user**] [**--yes**] [**--** *INSTRUCTION*]

**/tldr** **status** [**--** *INSTRUCTION*]

## DESCRIPTION

`tldr` has two modes of operation. Without a command path it treats the invocation as feedback that the preceding answer missed the useful level, focus, or density, then answers that substance again together with any earlier context needed to understand it. It reframes even an answer that was already short instead of merely compressing the same structure.

The replacement answer speaks to a technically capable person who owns the outcome without expecting them to hold every implementation detail. It leads with the conclusion, keeps practical implications and material decisions, omits internal mechanics by default, and uses whatever structure fits the content. Any action or decision genuinely requiring the user is explicit; no heading, list, or empty verdict is mandatory.

With `on` or `off`, the Skill controls the same perspective as a standing instruction for subsequent replies. Turning it on does not revisit or summarise the preceding answer. An explicit request for more detail overrides its default level for that reply.

The grammar is closed: the Skill takes no free-text operand, and nothing beyond a command path and its flags belongs before the reserved separator. A request that widens the range, names a language, narrows the subject, or constrains the output is a Contextual Instruction and is written after `--`, as `/tldr -- only the security part`.

TL;DR mode applies to replies in the conversation, not to source files, documentation, comments, commit messages, other artifacts, or general-purpose text and file compression.

## COMMANDS

**on**

Enable TL;DR mode for the selected scope.

**off**

Disable TL;DR mode for the selected scope.

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

An incomplete or invalid form is refused rather than ignored. The Skill names the error, prints the `SYNOPSIS` of the most specific recognized page, changes nothing, and points at that path's help route: `/tldr on --nonsense` is answered with the grammar of `on` rather than with the whole Skill's. A flag is refused rather than ignored where it has no work to do here, so `/tldr --user` and `/tldr --yes` are invalid without `on` or `off`, while `/tldr on --user --yes` is valid.

Unseparated text is not an instruction. A token after the Skill name or after a command path that is neither a recognized command path nor a declared flag is an invalid form, and so is a second command path; `/tldr only the security part` is refused rather than obeyed.

A replacement answer whose requested range is partly unavailable after context compaction states that limit instead of presenting an incomplete result as complete.

## EXAMPLES

**/tldr -- bara säkerhetsdelen**

Re-answer only the security-related part of the previous response, the narrowing arriving as a Contextual Instruction.

**/tldr on --user**

Show and confirm a user-level block that keeps later replies concise and decision-relevant in the current Harness without revisiting the preceding answer.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

None.

## SEE ALSO

**/tldr on --help**, **/tldr off --help**, **/tldr status --help**, **/delegation --help**, **/kntnt select**
