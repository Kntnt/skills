# setup

Record the Harness list. Adding a Harness applies every skill Enabled in Global to it. Removing a Harness asks before deleting this collection's skills there. The first run may then hand off to Enable.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" plan setup`. Done when stdout is a JSON plan.
2. Show `detected` Harnesses. Pre-check those with `selected` true. Let the user change the set. Done when the Harness list is decided.
3. If the plan would drop a Harness that is in `current`, say that this collection's skills will be deleted there, and wait. Done when the user confirms or there is no removal.
4. Run `uv run "$HERE/scripts/kntnt.py" apply setup` with `--harness <id>` for each chosen Harness. Add `--yes` when a Harness is being removed. Done when stdout is JSON.
5. If `first` was true, offer Enable: follow `$HERE/enable.md` with no skill names. Otherwise stop.
