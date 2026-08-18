---
name: kntnt
description: Manage this collection — which skills are Enabled, in Global and in each Project.
disable-model-invocation: true
argument-hint: "[select|update|uninstall|help] [name] [--project] [--yes] [--dry-run]"
---

# kntnt

The Manager. One namespaced entry point. Every other collection skill is invoked by its own name.

`$HERE` is the directory that contains this SKILL.md.

**Dependencies.** `uv` on PATH. If it is missing, stop and tell the user to install uv from https://docs.astral.sh/uv/.

## Help

If the arguments are `help`, `--help`, `-h`, or `help <name>`, follow `$HERE/steps/help.md` and stop. `$HERE/help.md` is this skill's own manpage, and `$HERE/help/<verb>.md` is the manpage of one verb; both are printed by that file rather than read by you.

## Arguments

- no args / `help` `[name]` — Help for the manager, one of its verbs, or one named collection skill. Bare `/kntnt` means Help.
- `select` `[--project]` `[--yes]` `[--dry-run]` — Select: print the Catalog as a list and take the answer.
- `update` `[--project]` `[--yes]` `[--dry-run]` — refresh this collection, then re-check Dependencies.
- `uninstall` `[--yes]` `[--dry-run]` — remove this collection from this machine, the Manager last.

Every verb reads `--project` the same way: absent or `--project=off` means Global, `--project` or `--project=on` means this Project. Select and Update change that layer, and Select lists it. Uninstall is the one verb that takes no `--project`: it clears this machine, and a working directory's own copies belong to that project.

Which Harnesses a verb reaches is never asked and never recorded: every Harness present in that layer is acted on, worked out on each run.

`--yes` means assume yes: ask nothing that can be answered yes or no. Every verb of `scripts/kntnt.py` accepts it, so passing the user's flag straight through is always safe.

`--dry-run` runs a changing verb for real against a temporary home seeded with this collection's own files, and throws that home away when the run ends. Nothing on the machine changes, and what comes back is the verb's own outcome rather than a description of what it would have done. It has an npm cache of its own, so the transport is downloaded afresh and the run takes noticeably longer than the one it previews — say so before starting it. Every verb of `scripts/kntnt.py` accepts the flag, as with `--yes`, and a verb that changes nothing ignores it. A payload carrying `dry_run` is such a run's outcome: report it as the outcome it is, say in the same breath that nothing on the machine changed, and read its `directories` as the Sandbox's copies of the real ones — they sit under the temporary home `dry_run.sandbox` names, and that home is gone by the time you read the payload.

## Steps

1. Take the first argument as the subcommand. No arguments → `help`. `help`, `--help`, or `-h` → `help`.
2. Read `$HERE/steps/<subcommand>.md`. Unknown subcommand → follow `$HERE/steps/help.md` and stop.
3. Follow that file. Done when it says to stop.
