# kntnt update

Refresh the skills of this collection whose files differ from it, then check every Dependency again.

## Synopsis

`/kntnt update [--project[=on|off]] [--yes] [--dry-run]`

## Description

Re-copies every skill the targeted layer has Enabled whose files differ from the ones the collection ships, and leaves the rest where they are, so the report says what moved rather than how much was Enabled. Re-copying a skill discards any local edit to it. The manager itself is refreshed every time: it is no catalog entry, so no digest describes it, and the verb that repairs everything else has to be able to reach itself. A skill the collection has withdrawn is deleted from that layer without asking: it can no longer be updated or supported, and no other command can reach it. A new catalog entry — a skill the collection has added since this manager last stored the catalog — is reported and offered: say yes and it is enabled here, say no and it stays disabled, and `/kntnt select` is where to change your mind later. You are asked at the moment you are already thinking about the collection, which is the moment the answer costs you nothing to give.

Afterwards every Dependency and every Capability is checked again, so a refresh that broke a prerequisite says so.

## Options

- `--project`, `--project=on` — refresh this Project rather than Global. `--project=off` is the bare form.
- `--yes` — assume yes: refresh without waiting for a confirmation, and enable every new catalog entry the run reports. It is the one flag in this collection that can put a skill you have not read into every harness you have, and that is the price of its meaning one thing everywhere; every name it enabled is in the report.
- `--dry-run` — run it against a temporary home seeded with this collection's files, and throw that home away. Nothing in the layer changes, and the report is the run's own outcome read off the Sandbox's disk. It downloads the transport afresh, so it takes longer than the run it previews.

## Notes

Update is the only verb that replaces the Catalog copy stored beside the manager, because it is the difference between that copy and the collection that tells a new skill from a withdrawn one.

Where the collection cannot be reached, nothing is refreshed, nothing is deleted, and nothing is reported as new. The files move through the same origin the list could not be read from, so there is nothing to copy, and a stale list does not get to decide which files go either. Run it again when the collection is reachable.

A Harness installed since the last run is reached with nothing to configure in between, because the targets are worked out on every run.

A new entry is enabled on its own, without whatever it depends on: something it needs and does not find is reported as unsatisfied afterwards rather than fetched behind the offer, because a skill you already chose to leave disabled is not this question's to answer. `/kntnt select` is where a dependency is added.

`/kntnt select --yes` is the deliberate opposite: it opens no list and enables nothing that was not already enabled. The unattended run that can add a skill is the one you pointed at the collection's own new entries.

## Dependencies

`uv` on PATH, and `npx` plus network access for the whole of what update does: the catalog it compares against is fetched from the collection, and the files it re-copies travel through the transport, which is `npx skills`. Where the collection cannot be reached nothing is refreshed, nothing is deleted, and nothing is reported as new.

## See also

`/kntnt help select`, `/kntnt help uninstall`.
