# tldr on

## NAME

tldr on - enable TL;DR mode for the selected scope

## SYNOPSIS

**/tldr on** [**--user**] [**--yes**] [**--** *INSTRUCTION*]

## DESCRIPTION

`tldr on` adopts the TL;DR perspective as a standing instruction for subsequent replies. It does not revisit, reframe, or summarise the preceding answer; that is what a bare `/tldr` is for.

The mode takes effect on the turn that switches it on, so the report of the write already obeys it. An explicit request for more detail overrides the default level for that reply, and the perspective governs conversation replies rather than code, documentation, comments, commit messages, or other artifacts.

Without `--user` the scope is this session alone, and context compaction may drop it. With `--user` the same text is written as a managed block into this Harness's global context file, last in the file, and the Skill shows the exact target and the exact insertion before writing. Repeating `on` over an existing block rewrites it from the current perspective text, so it is idempotent and doubles as the refresh for a block `status` reports as stale.

## OPTIONS

**--user**

Target this Harness's user context instead of the current session. There is no Project scope: conversational perspective and density are reader preferences rather than a shared Project convention.

**--yes**

Write the user block without waiting for confirmation. The session scope has nothing to confirm, so the flag is answered by the user scope's confirmation alone.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/tldr on --help`. A flag is refused rather than ignored where it has no work to do here, and any token after the command path that is neither `--user` nor `--yes` is refused the same way.

Two managed blocks in one file, or a marker without its pair, stop the write: the Skill changes nothing, reports what it found, and asks.

## EXAMPLES

**/tldr on**

Keep later replies in this conversation concise and decision-relevant, leaving the preceding answer untouched.

**/tldr on --user --yes**

Write the managed block into this Harness's global context file without asking for confirmation first.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

None.

## SEE ALSO

**/tldr --help**, **/tldr off --help**, **/tldr status --help**
