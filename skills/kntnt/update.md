# update

Refresh this collection's skills, then check every Dependency again. Report each new Catalog entry; do not Enable it and do not ask. Do not refresh an External. Without `--project` apply the Global layer; with `--project` apply the Project layer. A Harness installed since the last run is reached without any configuration, because the targets are worked out on each run.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" plan update` with the same `--project` flag the user passed. Done when stdout is JSON.
2. Show the plan, including the `directories` it will refresh. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
3. Run `uv run "$HERE/scripts/kntnt.py" apply update` with the same `--project` flag. Done when stdout is JSON.
4. Say each name in `new` is in the Catalog and Disabled. Say each name in `removed` is no longer in the Catalog. For each item in `unsatisfied`, give its `how`. For each item in `capabilities`, answer its `confirm` about yourself — you are the harness, and no script can test that; where it is not true of you, say that `skill` does no work here and give its `how`. If `catalog_refreshed` is false, say the Catalog could not be fetched, so Status may still be reporting an old list. Done when the user has the report.
5. `intended` names the skills the run set out to refresh, and `confirmed` those the script then found on disk. If `failed` is non-empty the command exits non-zero: say those skills did not land, whatever the transport reported, name each one's `directories` as where to look, and do not call the run clean. Done when the user has the outcome.
