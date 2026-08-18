# kntnt disable

Make one or more skills of this collection Disabled.

## Synopsis

`/kntnt disable [skill...] [--project[=on|off]] [--yes]`

## Description

Deletes each named skill's files from the layer being targeted, and reports afterwards what the disk shows rather than what the transport was asked to do. A skill that was not Enabled there is reported as such and nothing is deleted for it.

With no skill names, the Enabled skills are shown as a list grouped by Category, and the choice is made from that.

## Arguments

- `skill...` — the skills to Disable. No names opens the list.

## Options

- `--project`, `--project=on` — Disable in this Project rather than Global. `--project=off` is the bare form.
- `--yes` — assume yes: delete the files without waiting for a confirmation. Disable deletes, so the script itself refuses without it.

## Notes

`--project` cannot Disable a skill that is Enabled only in Global. A Project layer that could subtract from Global would make the result depend on the order the two were written in, and would surprise anyone who Enabled a skill once on the machine.

A skill whose files survive the removal is named with the directories they remain in, and the run is not called clean.

## See also

`/kntnt help enable`, `/kntnt help status`, `/kntnt help uninstall`.
