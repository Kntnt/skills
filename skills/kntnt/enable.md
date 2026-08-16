# enable

Make one or more skills Enabled. With no skill names, open an interactive list. Targets Global unless `--project` or `--project=on` is given. Requires a Harness list.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" plan enable` with the same `--project` flag and skill names the user passed. Done when stdout is JSON, or the command exits 2.
2. Exit 2 and stderr mentions setup: tell the user to run `/kntnt setup`, and stop.
3. Exit 2 and `action` is `pick`: show the list grouped by Category, let the user choose, then run this file again with those names. Done when names are chosen or the user aborts.
4. Show the plan. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
5. Run `uv run "$HERE/scripts/kntnt.py" apply enable` with the same `--project` flag and the named skills. Done when stdout is JSON.
