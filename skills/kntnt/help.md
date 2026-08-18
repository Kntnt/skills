# kntnt

Manage this collection — which skills are Enabled, in Global and in each Project.

## Synopsis

`/kntnt [subcommand] [skill...] [--project[=on|off]] [--yes] [--dry-run]`

## Description

The manager is the collection's one namespaced entry point. Every other skill of the collection is invoked by its own name, and answers `--help` with the manpage shipped beside it; the manager documents its own subcommands and nothing else.

Bare `/kntnt` prints this text. Someone who types the manager's name with nothing after it does not yet know what to type next, and this is the answer to that.

## Subcommands

- `help [name]` — this text, the manpage of one subcommand, or the help of one collection skill.
- `status [skill...]` — report Global, or what applies in this directory with `--project`.
- `enable [skill...]` — make skills Enabled. No names opens a list.
- `disable [skill...]` — make skills Disabled. No names opens a list.
- `update` — refresh this collection, then re-check every Dependency.
- `uninstall` — remove this collection from this machine, the manager last.

## Options

- `--project`, `--project=on` — act on this Project rather than Global. `--project=off` is the bare form. Uninstall takes no `--project`.
- `--yes` — assume yes: ask nothing that can be answered yes or no.
- `--dry-run` — run the verb against a temporary home seeded with this collection's files, and throw that home away. Nothing on this machine changes. Accepted everywhere; the verbs that change nothing ignore it.

## Notes

Status lists every Catalog skill, Enabled or not; with `--project` it lists what applies in this directory and where each skill comes from. Enable, Disable, and Update default to Global. They act on every Harness present in the layer they target, worked out on every run rather than recorded. Uninstall clears this machine and leaves a working directory's own copies to that project.

A dry run is the expensive way to see a change before it happens: the verb really runs, against files copied into a temporary home, and the report is its own outcome read off that home's disk rather than a second account of what it meant to do. It downloads the transport afresh into a cache of its own, so it takes noticeably longer than the run it previews. The confirmation a changing verb asks for before it writes is the cheap way, and it is not a dry run.

## See also

`/kntnt help <subcommand>` for one verb in full. `/<skill> --help` for a skill of this collection.
