# update

Refresh this collection's skills, then check every Dependency again. Report each new Catalog entry; do not Enable it and do not ask. Do not refresh an External. Without `--project` apply the Global layer; with `--project` apply the Project layer.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" plan update` with the same `--project` flag the user passed. Done when stdout is JSON, or the command exits 2.
2. Exit 2 and stderr mentions setup: tell the user to run `/kntnt setup`, and stop.
3. Show the plan. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
4. Run `uv run "$HERE/scripts/kntnt.py" apply update` with the same `--project` flag. Done when stdout is JSON.
5. Say each name in `new` is in the Catalog and Disabled. Say each name in `removed` is no longer in the Catalog. For each item in `unsatisfied`, give its `how`. For each item in `capabilities`, answer its `confirm` about yourself — you are the harness, and no script can test that; where it is not true of you, say that `skill` does no work here and give its `how`. If `catalog_refreshed` is false, say the Catalog could not be fetched, so Status may still be reporting an old list. Done when the user has the report.
