# kntnt enable

Make one or more skills of this collection Enabled.

## Synopsis

`/kntnt enable [skill...] [--project[=on|off]] [--yes] [--dry-run]`

## Description

Places each named skill's files in the layer being targeted, and reports afterwards what the disk shows rather than what the transport was asked to do. A skill already Enabled there is left alone.

With no skill names, the Catalog is shown as a list grouped by Category, naming any Capability a skill requires of the harness, and the choice is made from that.

## Arguments

- `skill...` — the skills to Enable. No names opens the list.

## Options

- `--project`, `--project=on` — Enable in this Project rather than Global. `--project=off` is the bare form.
- `--yes` — assume yes: place the skills without waiting for a confirmation.
- `--dry-run` — run it against a temporary home seeded with this collection's files, and throw that home away. Nothing in the layer changes, and the report is the run's own outcome read off the Sandbox's disk. It downloads the transport afresh, so it takes longer than the run it previews.

## Notes

Which Harnesses are reached is never asked and never recorded: every Harness present in the targeted layer is written to, worked out on every run. With no Harness detected, the shared `.agents/skills` directory is written to alone.

A skill that fails to land is named with the directories to look in, and the run is not called clean.

## See also

`/kntnt help disable`, `/kntnt help status`, `/kntnt help update`.
