# kntnt update

## NAME

kntnt update - refresh the Collection and re-check Dependencies

## SYNOPSIS

**/kntnt** **update** [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**] [**--** *INSTRUCTION*]

## DESCRIPTION

`kntnt update` re-copies every Enabled Skill in the targeted layer whose files differ from the current Catalog Digest and leaves matching Skills unchanged. Global is the default layer. Re-copying overwrites local changes to a Skill.

The Manager is refreshed on every successful update because it is not a Catalog entry and has no Digest. A Withdrawn Skill is removed from the targeted layer without confirmation. A newly added Catalog Skill is reported and offered for Enablement; accepting the offer Enables only that Skill, and any Unsatisfied Dependency is reported afterwards.

After file changes, Update checks every Dependency and Capability again. It is the only command that replaces the stored Catalog, preserving the comparison needed to identify new and Withdrawn entries on a later run.

## OPTIONS

**--project**, **--project=on**

Target the current Project instead of Global. `--project=off` has the same effect as omitting the option.

**--yes**

Assume yes for confirmations, including the offer to Enable every new Catalog entry reported by the run. The report names every newly Enabled Skill.

**--dry-run**

Execute against a temporary home seeded with this Collection's files, report the Sandbox outcome, and discard it. Nothing in the selected layer changes. The isolated transport cache makes this slower than an ordinary run.

## OFFLINE OPERATION

If the Collection cannot be reached, Update refreshes nothing, removes nothing, reports no new entry, and leaves the stored Catalog unchanged. Run it again when the Collection is reachable.

## DIAGNOSTICS

An invalid argument or option with no work to do is refused rather than ignored. The Manager names the error, prints the SYNOPSIS, changes nothing, and points to the full page.

A Harness added since the previous run is detected automatically and needs no configuration.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Unaddressable is guidance with no addressable effect at all — guidance touching nothing this Skill's contract addresses — and never guidance a documented precedence has already settled against, which is suppressed instead: suppression is that precedence working, so the run continues and the delivery names the suppressed guidance beside the resolved configuration where saying so is useful. Only guidance that is part invalid — part conflicting, part scope-widening, or part unaddressable — goes unapplied as a whole; one parameter suppressed and another landing is an ordinary invocation. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

**Binaries**

`uv` and `npx` on `PATH`. Skill files move through `npx skills`.

**Network**

Required to fetch the current Catalog and Skill files. An unreachable Collection produces the bounded no-op described above.

## SEE ALSO

**/kntnt select --help**, **/kntnt uninstall --help**
