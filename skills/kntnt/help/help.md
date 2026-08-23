# kntnt help

## NAME

kntnt help - display a Manager or command manpage

## SYNOPSIS

**/kntnt**

**/kntnt** **help** [*COMMAND*]

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

## DEPENDENCIES

**Binaries**

`uv` on `PATH`.

## SEE ALSO

**/kntnt select --help**, **/kntnt update --help**, **/kntnt uninstall --help**, **/<skill> --help**
