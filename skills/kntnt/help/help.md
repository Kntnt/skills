# kntnt help

## NAME

kntnt help - display a Manager or command manpage

## SYNOPSIS

**/kntnt** [**--** *INSTRUCTION*]

**/kntnt** **help** [*COMMAND*] [**--** *INSTRUCTION*]

## DESCRIPTION

`kntnt help` prints the Manager's page when *COMMAND* is omitted and prints one Manager command's page when it is supplied. Bare `/kntnt` is equivalent to `/kntnt help`.

Every Manager command also prints the same page when invoked with `--help` or `-h`, for example `/kntnt select --help`.

Help reads pages shipped beside the Manager, performs no normal work, changes no layer, and does not access the network or transport.

The Manager has no route for a Collection Skill's page. Use `/<skill> --help` for an Enabled Skill, or open the Select list and request the page for a Skill that is not Enabled.

## POSITIONAL ARGUMENTS

*COMMAND*

One of `help`, `select`, `update`, or `uninstall`.

## DIAGNOSTICS

An unknown command or any option is refused rather than ignored. The Manager names the error, prints the SYNOPSIS, changes nothing, and points to the full page.

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

`uv` on `PATH`.

## SEE ALSO

**/kntnt select --help**, **/kntnt update --help**, **/kntnt uninstall --help**, **/<skill> --help**
