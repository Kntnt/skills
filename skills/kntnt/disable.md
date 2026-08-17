# disable

Make one or more skills Disabled. With no skill names, open an interactive list. Uses the same `--project` rule as Enable. Requires a Harness list. `--project` cannot Disable a skill that is Enabled only in Global.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" plan disable` with the same `--project` flag and skill names the user passed. Done when stdout is JSON, or the command exits 2.
2. Exit 2 and stderr mentions setup: tell the user to run `/kntnt setup`, and stop.
3. Exit 2 and `action` is `pick`: show the Enabled skills grouped by Category, let the user choose, then run this file again with those names. Done when names are chosen or the user aborts.
4. Show the plan. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
5. Run `uv run "$HERE/scripts/kntnt.py" apply disable` with the same `--project` flag, the named skills, and `--yes`. Disable deletes files, so the script refuses without `--yes`; reaching this step means step 4 settled it. If `noop` is non-empty, say those skills were not Enabled in this layer. Done when stdout is JSON.
