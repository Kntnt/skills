# kntnt uninstall

Remove this collection from this machine.

## Synopsis

`/kntnt uninstall [--yes] [--dry-run]`

## Description

Deletes every Catalog skill Enabled in Global from every Harness present in your home directory, and then the manager itself, last and through the transport, so the harness's own uninstall has nothing left to do.

The manager goes only where everything else really went. A run that leaves a skill behind keeps `kntnt`, since it is the one verb that could still remove it — so `kntnt` among the confirmed removals is the whole report.

## Options

- `--yes` — assume yes: remove without waiting for a confirmation. Uninstall deletes, so the script itself refuses without it.
- `--dry-run` — run it against a temporary home seeded with this collection's files, and throw that home away. Nothing in the layer changes, and the report is the run's own outcome read off the Sandbox's disk. It downloads the transport afresh, so it takes longer than the run it previews.

## Notes

There is no `--project` form, and that is the decision rather than an omission. A skill in a working directory is checked into that repository and travels with it, so whether it stays is that project's decision. Those copies are never touched, and the report says so rather than letting anyone believe the machine is clean while a repository still carries them.

What is removed is what the Catalog names, so the report says whether that list came from the collection or from the stored copy. The usual remedy of running it again is only available while the manager is still installed.

## Dependencies

`uv` on PATH, and `npx` for the transport, which is the route the files leave by — the same one they arrived by, the manager's own removal included. The catalog is fetched from the collection over the network to settle what to remove, and falls back to the copy stored beside the manager. Which of the two the run worked from is in the report, and it matters more here than anywhere else: once the manager is gone there is no verb left to finish the job.

## See also

`/kntnt help select`, `/kntnt help update`.
