# disable

Make one or more skills Disabled. With no skill names, open an interactive list. Uses the same `--project` rule as Enable, and reaches the same Harnesses. `--project` cannot Disable a skill that is Enabled only in Global.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" plan disable` with the same `--project` flag and skill names the user passed. Done when stdout is JSON, or the command exits 2.
2. Exit 2 and `action` is `pick`: show the Enabled skills grouped by Category, let the user choose, then run this file again with those names. Done when names are chosen or the user aborts.
3. Show the plan, including the `directories` the files will be deleted from. Wait unless `--yes` or `--dry-run` — a dry run deletes nothing outside its own Sandbox, so there is nothing here to confirm. Done when the user confirms, or `--yes` or `--dry-run` is set.
4. Run `uv run "$HERE/scripts/kntnt.py" apply disable` with the same `--project` flag, the named skills, and `--yes`. Forward `--dry-run` if the user passed it, and say before starting that the run happens against a temporary home that is thrown away, and that it downloads the transport afresh and so takes longer than the real run would. Disable deletes files, so the script refuses without `--yes`; reaching this step means step 3 settled it. If `noop` is non-empty, say those skills were not Enabled in this layer. Done when stdout is JSON.
5. Report the outcome the payload carries, not the plan. `intended` names the skills the run set out to remove, and `confirmed` those the script then found gone from the disk. If `failed` is non-empty the command exits non-zero: say those skills are **still** Enabled, whatever the transport reported, name each one's `directories` as where the files remain, and do not call the run clean. Done when the user has the outcome.
