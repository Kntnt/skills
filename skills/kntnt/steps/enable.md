# enable

Make one or more skills Enabled. With no skill names, open an interactive list. Targets Global unless `--project` or `--project=on` is given. Which Harnesses are reached is not a question: every Harness present in that layer is acted on.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" plan enable` with the same `--project` flag and skill names the user passed. Done when stdout is JSON, or the command exits 2.
2. Exit 2 and `action` is `pick`: show the list grouped by Category, naming any `capabilities` an item needs of the harness, let the user choose, then run this file again with those names. Done when names are chosen or the user aborts.
3. Show the plan, including the `directories` it will write to. Wait unless `--yes` or `--dry-run` — a dry run writes nothing outside its own Sandbox, so there is nothing here to confirm. Done when the user confirms, or `--yes` or `--dry-run` is set.
4. Run `uv run "$HERE/scripts/kntnt.py" apply enable` with the same `--project` flag and the named skills. Forward `--dry-run` if the user passed it, and say before starting that the run happens against a temporary home that is thrown away, and that it downloads the transport afresh and so takes longer than the real run would. Done when stdout is JSON.
5. Report the outcome the payload carries, not the plan. `intended` names the skills the run set out to place, `confirmed` those the script then found on disk, and `noop` those already Enabled here. If `failed` is non-empty the command exits non-zero: say those skills are **not** Enabled, whatever the transport reported, name each one's `directories` as where to look, and do not call the run clean. Done when the user has the outcome.
