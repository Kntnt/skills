# kntnt uninstall

## NAME

kntnt uninstall - remove the Collection from the machine

## SYNOPSIS

**/kntnt** **uninstall** [**--yes**] [**--dry-run**] [**--** *INSTRUCTION*]

## DESCRIPTION

`kntnt uninstall` removes every Catalog Skill Enabled in Global from every Harness detected in the user's home directory, then removes the Manager through the transport. The Manager is removed only after every other confirmed removal succeeds, so a partial run retains the command needed to finish.

Project copies are never removed. They are part of their repositories and travel with those Projects.

## OPTIONS

**--yes**

Remove the Collection without waiting for confirmation. The script requires this option because Uninstall deletes files.

**--dry-run**

Execute against a temporary home seeded with this Collection's files, report the Sandbox outcome, and discard it. Nothing on the machine changes. The isolated transport cache makes this slower than an ordinary run.

## OFFLINE OPERATION

Uninstall fetches the current Catalog when possible and otherwise uses the stored Catalog. The report identifies which source determined the removal set.

## DIAGNOSTICS

`--project` and every other unsupported option are refused rather than ignored. The Manager names the error, prints the SYNOPSIS, removes nothing, and points to the full page.

If any Skill cannot be removed, the Manager remains Enabled and the report names what is left.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Unaddressable is guidance with no addressable effect at all — guidance touching nothing this Skill's contract addresses — and never guidance a documented precedence has already settled against, which is suppressed instead: suppression is that precedence working, so the run continues and the delivery names the suppressed guidance beside the resolved configuration where saying so is useful. Only guidance that is part invalid — part conflicting, part scope-widening, or part unaddressable — goes unapplied as a whole; one parameter suppressed and another landing is an ordinary invocation. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

**Binaries**

`uv` and `npx` on `PATH`. Files are removed through `npx skills`.

**Network**

Used to fetch the current Catalog. The stored Catalog is the fallback when the Collection is unreachable.

## SEE ALSO

**/kntnt select --help**, **/kntnt update --help**
