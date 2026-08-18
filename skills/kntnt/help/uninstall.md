# kntnt uninstall

Remove this collection from this machine.

## Synopsis

`/kntnt uninstall [--yes]`

## Description

Deletes every Catalog skill Enabled in Global from every Harness present in your home directory, and then the manager itself, last and through the transport, so the harness's own uninstall has nothing left to do.

The manager goes only where everything else really went. A run that leaves a skill behind keeps `kntnt`, since it is the one verb that could still remove it — so `kntnt` among the confirmed removals is the whole report.

## Options

- `--yes` — assume yes: remove without waiting for a confirmation. Uninstall deletes, so the script itself refuses without it.

## Notes

There is no `--project` form, and that is the decision rather than an omission. A skill in a working directory is checked into that repository and travels with it, so whether it stays is that project's decision. Those copies are never touched, and the report says so rather than letting anyone believe the machine is clean while a repository still carries them.

What is removed is what the Catalog names, so the report says whether that list came from the collection or from the stored copy. The usual remedy of running it again is only available while the manager is still installed.

## See also

`/kntnt help disable`, `/kntnt help update`.
