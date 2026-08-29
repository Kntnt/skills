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

[**--** *INSTRUCTION*] adds an optional Contextual Instruction. The first standalone, unquoted `--` is the reserved separator. Everything before it is the Formal Invocation; everything after it, including later `--` tokens, is guidance. The guidance may start on the same line or after blank lines and must contain non-whitespace text.

`--force`, `foo--bar`, `` `--` ``, and `"--"` are not separators. Without the separator, the whole payload remains formal input, including later lines and paragraphs.

After validating the Formal Invocation, the Skill uses guidance to clarify or narrow open choices. Guidance cannot contradict formal input or an invariant, widen the Skill, bypass a gate, or request unrelated work. Redundant but applicable guidance is valid. Applicable Conversation Context follows the same limits.

Malformed formal input or an empty instruction takes the syntax refusal. The Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Context on an exact help route takes the context refusal without rendering the page.

Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal. The Skill names the guidance and its boundary, reports the mutation outcome, prints no synopsis, and stops without applying a valid remainder.

Unaddressable guidance can affect nothing inside the Skill's contract. Guidance settled by a documented precedence is suppressed instead: the run continues and reports the suppression where useful. Suppression for one parameter does not invalidate guidance that applies to another.

Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict appears only after a legitimate effect, it stops before the next effect and reports the exact partial outcome. It rolls nothing back unless atomic behaviour was promised.

A nested Skill receives only relevant guidance through an explicit Contextual Instruction. Successful execution requires no context acknowledgement; an existing report names a materially changed choice where useful.

## DEPENDENCIES

**Binaries**

`uv` and `npx` on `PATH`. Files are removed through `npx skills`.

**Network**

Used to fetch the current Catalog. The stored Catalog is the fallback when the Collection is unreachable.

## SEE ALSO

**/kntnt select --help**, **/kntnt update --help**
