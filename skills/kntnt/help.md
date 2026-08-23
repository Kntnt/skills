# kntnt

## NAME

kntnt - manage which collection Skills are Enabled

## SYNOPSIS

**/kntnt**

**/kntnt** **help** [*COMMAND*]

**/kntnt** **select** [**--on** *SKILL*]... [**--off** *SKILL*]... [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**]

**/kntnt** **update** [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**]

**/kntnt** **uninstall** [**--yes**] [**--dry-run**]

## DESCRIPTION

`kntnt` is the Collection's Manager and only namespaced entry point. It lists, Enables, refreshes, and removes Collection Skills across every detected Harness in a Global or Project layer. Other Skills are invoked by their own names.

With no command, `kntnt` prints this page. Each command prints its own page through `/kntnt <command> --help` or `/kntnt help <command>`. The Manager documents only its own commands. Select lists every Catalog Skill, Enabled or not. An Enabled Skill prints its page through `/<skill> --help`; Select can display the page for a Skill that is not yet Enabled.

Select and Update target Global by default. With `--project`, they target the current Project. Harnesses are detected on each run rather than configured or remembered.

## COMMANDS

**help** [*COMMAND*]

Print this page or the page for one Manager command.

**select**

List every Catalog Skill and change which ones are Enabled, or apply explicit `--on` and `--off` deltas.

**update**

Refresh Enabled Skills that differ from the Collection, handle new and Withdrawn Catalog entries, and re-check Dependencies.

**uninstall**

Remove the Collection from the machine, with the Manager removed last. Project copies are left untouched.

## OPTIONS

**--on** *SKILL*

Enable a named Skill without opening the Select list. Valid only with `select` and repeatable.

**--off** *SKILL*

Disable a named Skill without opening the Select list. Valid only with `select`, repeatable, and gated by `--yes` because it deletes files.

**--project**, **--project=on**

Target the current Project instead of Global. `--project=off` has the same effect as omitting the option. Valid only with `select` and `update`.

**--yes**

Assume yes for every yes-or-no question. Valid with `select`, `update`, and `uninstall`.

**--dry-run**

Run the changing command in a temporary home seeded with this Collection's files, report the outcome from that Sandbox, and discard it. Nothing on the machine changes. Valid with `select`, `update`, and `uninstall`.

## DIAGNOSTICS

An unknown command or an option with no work to do is refused rather than ignored. The Manager names the error, prints the addressed command's SYNOPSIS, performs no work, and points to the full page. No command accepts `--force`.

A failed Catalog fetch falls back to the stored Catalog where the command can safely operate from it. The report identifies the Catalog source and any limitation caused by fallback.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`. Commands that fetch the Collection or move Skill files also require `npx`; files move through `npx skills`.

**Network**

Select and Update normally fetch the Catalog, and changing commands fetch Skill files. Offline fallback behaviour is documented on each command page.

## SEE ALSO

**/kntnt help --help**, **/kntnt select --help**, **/kntnt update --help**, **/kntnt uninstall --help**, **/<skill> --help**
