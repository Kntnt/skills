# kntnt

Manage this collection — which skills are Enabled, in Global and in each Project.

## Synopsis

`/kntnt [subcommand] [skill...] [--project[=on|off]] [--yes]`

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

## Notes

Status lists every Catalog skill, Enabled or not; with `--project` it lists what applies in this directory and where each skill comes from. Enable, Disable, and Update default to Global. They act on every Harness present in the layer they target, worked out on every run rather than recorded. Uninstall clears this machine and leaves a working directory's own copies to that project.

## See also

`/kntnt help <subcommand>` for one verb in full. `/<skill> --help` for a skill of this collection.
