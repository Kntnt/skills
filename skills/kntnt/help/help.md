# kntnt help

Print the manager's manpage, one subcommand's manpage, or one collection skill's help.

## Synopsis

`/kntnt help [name]`

`/kntnt`

## Description

With no name, prints the manager's own manpage — the same text bare `/kntnt` prints. With the name of a subcommand, prints that subcommand's manpage. With the name of a collection skill, prints that skill's help.

Help changes nothing, in either layer.

## Arguments

- `name` — a subcommand of the manager, or a skill of this collection. A name that is neither is an error rather than an empty page.

## Notes

Asking the manager about a skill means remembering which collection that skill arrived from, which is why this route is the one on its way out. A skill that is installed answers `--help` itself, and that is the shorter way to the same text: the manpage the manager prints for a skill is the file that skill ships.

A skill that is Disabled has no files on disk, so its help here is the Catalog description alone; `/kntnt enable <name>` gives the rest.

## See also

`/kntnt help status`, `/kntnt help enable`, `/kntnt help disable`, `/kntnt help update`, `/kntnt help uninstall`.
