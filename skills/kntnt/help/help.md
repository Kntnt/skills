# kntnt help

## NAME

kntnt help - display a Manager, command, or Enabled Skill manpage

## SYNOPSIS

**/kntnt** [**--** *INSTRUCTION*]

**/kntnt** **help** [*NAME*] [**--** *INSTRUCTION*]

## DESCRIPTION

`kntnt help` prints the Manager's page when *NAME* is omitted. When *NAME* is a Manager command, it prints that command's page. Otherwise, when *NAME* is a Collection Skill that is Enabled in Global or in this Project, it prints that Skill's page as `/<skill> --help` prints it, installed choices included. Bare `/kntnt` is equivalent to `/kntnt help`.

Every Manager command also prints the same page when invoked with `--help` or `-h`, for example `/kntnt select --help`.

Help reads pages shipped beside the Manager or with an Enabled Skill. It performs no normal work, runs no Skill, changes no layer, and does not access the network or transport.

`/kntnt help <skill>` does not read the page of a Skill that is not Enabled. Open the Select list and request the page there instead.

## POSITIONAL ARGUMENTS

*NAME*

One of the Manager commands `help`, `select`, `update`, or `uninstall`, or the name of an Enabled Collection Skill. A Manager command takes precedence over a Skill with the same name.

## DIAGNOSTICS

An option is refused rather than ignored. The Manager names the error, prints the SYNOPSIS, changes nothing, and points to the full page.

A *NAME* that is neither a Manager command nor an Enabled Collection Skill is refused. The Manager installs nothing, fetches nothing, and points to Select for a Skill that is not Enabled. An Enabled Skill whose `help.md` is missing is reported by the missing file's path. The page is not fetched from the collection instead.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`.

## SEE ALSO

**/kntnt select --help**, **/kntnt update --help**, **/kntnt uninstall --help**, **/<skill> --help**
