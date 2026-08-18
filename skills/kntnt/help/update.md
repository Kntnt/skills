# kntnt update

Refresh this collection's skills, then check every Dependency again.

## Synopsis

`/kntnt update [--project[=on|off]] [--yes] [--dry-run]`

## Description

Re-copies every skill the targeted layer has Enabled that the collection still carries, so what is on disk is what the collection ships. A skill the collection has withdrawn is deleted from that layer without asking: it can no longer be updated or supported, and no other command can reach it. A new Catalog entry is reported and left Disabled — Update never Enables anything on its own.

Afterwards every Dependency and every Capability is checked again, so a refresh that broke a prerequisite says so.

## Options

- `--project`, `--project=on` — refresh this Project rather than Global. `--project=off` is the bare form.
- `--yes` — assume yes: refresh without waiting for a confirmation.
- `--dry-run` — run it against a temporary home seeded with this collection's files, and throw that home away. Nothing in the layer changes, and the report is the run's own outcome read off the Sandbox's disk. It downloads the transport afresh, so it takes longer than the run it previews.

## Notes

Update is the only verb that replaces the Catalog copy stored beside the manager, because it is the difference between that copy and the collection that tells a new skill from a withdrawn one.

Where the collection cannot be reached, nothing is deleted and nothing is reported as new: a stale list does not get to decide which files go. Run it again when the collection is reachable.

A Harness installed since the last run is reached with nothing to configure in between, because the targets are worked out on every run.

## See also

`/kntnt help select`, `/kntnt help uninstall`.
