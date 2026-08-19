# kntnt

Manage this collection — which skills are Enabled, in Global and in each Project.

## Synopsis

`/kntnt [subcommand] [command] [--project[=on|off]] [--yes] [--dry-run]`

## Description

The manager is the collection's one namespaced entry point. Every other skill of the collection is invoked by its own name, and answers `--help` with the manpage shipped beside it; the manager documents its own subcommands and nothing else. A skill you do not have yet is read about from the `select` list, which is where the decision to enable it is made anyway.

Bare `/kntnt` prints this text. Someone who types the manager's name with nothing after it does not yet know what to type next, and this is the answer to that.

## Subcommands

- `help [command]` — this text, or the manpage of one subcommand.
- `select` — print the catalog as a list, and change what is Enabled by answering it.
- `update` — refresh this collection, then re-check every Dependency.
- `uninstall` — remove this collection from this machine, the manager last.

## Options

- `--project`, `--project=on` — act on this project rather than global. `--project=off` is the bare form. Select and Update take it. Uninstall does not: it clears this machine, and a run that looked scoped to a project would be a lie about what happened.
- `--yes` — assume yes: ask nothing that can be answered yes or no. Select, Update, and Uninstall take it.
- `--dry-run` — run the verb against a temporary home seeded with this collection's files, and throw that home away. Nothing on this machine changes. Select, Update, and Uninstall take it.

Help takes none of the three. Where a flag is accepted it always means the same thing — which is not the rule that every verb accepts every flag, and is the better of the two: a flag accepted and ignored teaches that flags sometimes do nothing, so a verb with no meaning for one refuses it. A flag a verb does not take is an error naming the flag, followed by that verb's synopsis and where to read its page in full, and a subcommand the manager does not have is the same error against this page — nothing after the unknown word is read, so a typo never runs a different verb with the rest of the line as its arguments. No verb of the manager takes `--force`: the digest answers whether a thing needs doing and `--yes` answers whether to ask, so no third flag was left with anything to mean.

## Notes

Select lists every catalog skill, Enabled or not, and is where you change which of them are. Reading the list and acting on it are the same gesture, so there is no second verb to retype a name into, and any row on it can be read in full before you answer — including a skill you have never installed. Select and Update default to global; with `--project` they act on this working directory alone. They act on every harness present in the layer they target, worked out on every run rather than recorded. Uninstall clears this machine and leaves a working directory's own copies to that project.

A dry run is the expensive way to see a change before it happens: the verb really runs, against files copied into a temporary home, and the report is its own outcome read off that home's disk rather than a second account of what it meant to do. It downloads the transport afresh into a cache of its own, so it takes noticeably longer than the run it previews. The confirmation a changing verb asks for before it writes is the cheap way, and it is not a dry run.

## See also

`/kntnt help <subcommand>` for one verb in full. `/<skill> --help` for a skill of this collection you already have, and `/kntnt select` to read about one you do not.
