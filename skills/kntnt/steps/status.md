# status

Report the Global layer: every Catalog skill, Enabled or Disabled on this machine. With `--project` or `--project=on`, report the Effective set instead — what applies in this working directory, and where each skill comes from. `--project=off` is the bare form. Skill names narrow either form to those skills. Status reads; it changes nothing in either layer.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" status` with the same `--project` flag and skill names the user passed. Done when stdout is JSON.
2. Open by saying which question the payload answers, taking it from `reports`: `global` is *what does this machine have*, `effective` is *what applies in this directory*. Never leave the reader to work out which report they are looking at. Done when it is said.
3. Group `skills` by `category`. Name the `directories` the report covers — that is where Enable, Disable, and Update would act. The bare form covers Global alone, so it names only that layer. Done when the report is grouped.
4. Report **every** skill the payload carries, with its `state` and any `capabilities` it needs of the harness. In the `global` form a state is `enabled`, `disabled`, or `partial`. In the `effective` form it is `enabled` or `partial` only — never `disabled`, so give that form no Disabled bucket to fill — and each skill also carries a `source`: `global`, `project`, or `both`. Done when the user has the report.
5. Disabled skills belong in the `global` form and are absent from the `effective` one: the Catalog carries a skill this machine has not Enabled, but a skill Enabled in neither layer does not apply here. If the user named a skill and the `effective` form left it out, say it applies nowhere in this directory rather than showing an empty report. Done when that is said, or nothing was left out.
6. Read `catalog_refreshed`. `true` means the list came from the collection itself and needs no remark. `false` means the collection could not be reached and the list is the copy stored beside the manager: say so, and say the report may be missing skills published since — never present a stale list as the collection's current one. Done when that is said, or the list was fetched.
