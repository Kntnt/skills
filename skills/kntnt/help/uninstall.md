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

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` and `npx` on `PATH`. Files are removed through `npx skills`.

**Network**

Used to fetch the current Catalog. The stored Catalog is the fallback when the Collection is unreachable.

## SEE ALSO

**/kntnt select --help**, **/kntnt update --help**
