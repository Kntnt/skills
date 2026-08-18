# update

Refresh this collection's skills, then check every Dependency again. Report each new Catalog entry; do not Enable it and do not ask. A skill the collection has withdrawn is deleted from this layer, and that is not asked either — it can no longer be updated or supported, and no other command can reach it. Do not refresh an External. Without `--project` apply the Global layer; with `--project` apply the Project layer. A Harness installed since the last run is reached without any configuration, because the targets are worked out on each run.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" plan update` with the same `--project` flag the user passed. Done when stdout is JSON.
2. Show the plan, including the `directories` it will refresh. Its `refresh` list is what this layer has Enabled that the collection still carries, so say that a skill withdrawn upstream since the last run will be deleted rather than refreshed and that step 4 reports which. Wait unless `--yes`. Done when the user confirms or `--yes` is set.
3. Run `uv run "$HERE/scripts/kntnt.py" apply update` with the same `--project` flag. Done when stdout is JSON.
4. Say each name in `new` is in the Catalog and Disabled. For each item in `removed`, say the skill is no longer in the collection and what became of its files: `disk` is `removed` where they were deleted, `absent` where it was not Enabled here, and `failed` where they are still there — name that item's `directories`, and do not call the run clean. For each item in `unsatisfied`, give its `how`. For each item in `capabilities`, answer its `confirm` about yourself — you are the harness, and no script can test that; where it is not true of you, say that `skill` does no work here and give its `how`. If `catalog_refreshed` is false, say the collection could not be reached: the stored copy is unchanged, and `new` and `removed` are empty for want of anything to compare against rather than because nothing changed upstream. Done when the user has the report.
5. `intended` names the skills the run set out to refresh, and `confirmed` those the script then found on disk. If `failed` is non-empty the command exits non-zero: say those skills did not land, whatever the transport reported, name each one's `directories` as where to look, and do not call the run clean. Done when the user has the outcome.
