# disable

Make one or more skills Disabled. With no skill names, open an interactive list. Uses the same `--project` rule as Enable, and reaches the same Harnesses. `--project` cannot Disable a skill that is Enabled only in Global.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" plan disable` with the same `--project` flag and skill names the user passed. Done when stdout is JSON, or the command exits 2.
2. Exit 2 and `action` is `pick`: show the Enabled skills grouped by Category, let the user choose, then run this file again with those names. Done when names are chosen or the user aborts.
3. Show the plan, including the `directories` the files will be deleted from. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
4. Run `uv run "$HERE/scripts/kntnt.py" apply disable` with the same `--project` flag, the named skills, and `--yes`. Disable deletes files, so the script refuses without `--yes`; reaching this step means step 3 settled it. If `noop` is non-empty, say those skills were not Enabled in this layer. Done when stdout is JSON.
