# kntnt help

Print the manager's manpage, or the manpage of one of its subcommands.

## Synopsis

`/kntnt help [command]`

`/kntnt`

## Description

With no name, prints the manager's own manpage — the same text bare `/kntnt` prints. With the name of a subcommand, prints that subcommand's manpage.

Help changes nothing, in either layer.

## Arguments

- `command` — a subcommand of the manager. A name that is not one is an error rather than an empty page.

## Options

None. Help takes no flags, and passing one is an error rather than a page with a note above it: the flag is named, the synopsis above is printed, and you are told where to read this page in full. The verb changes nothing, asks nothing, and writes nothing, so every flag the manager carries would have to mean nothing here — and a flag accepted and ignored is what teaches a user that flags sometimes do nothing.

## Notes

The manager documents its own verbs and no skill. Asking it about a skill meant remembering which collection that skill had arrived from, which is exactly the fact a user should not have to hold, so there are two better routes instead. A skill you have answers `/<skill> --help` with the manpage it ships beside itself, whichever collection it came from. A skill you do not have yet is read about from `/kntnt select`, which fetches that manpage from the collection — the list is where you decide whether to enable it, and deciding never requires installing it first.

## Dependencies

`uv` on PATH, and nothing else. Help prints pages shipped beside the manager, so it runs no transport and reaches no network — it is the one verb that still answers on a machine that is offline.

## See also

`/kntnt help select`, `/kntnt help update`, `/kntnt help uninstall`.
