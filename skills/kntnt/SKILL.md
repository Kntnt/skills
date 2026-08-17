---
name: kntnt
description: Manage this collection — which skills are Enabled, in Global and in each Project.
disable-model-invocation: true
argument-hint: "[status|enable|disable|update|help] [skill...] [--project] [--yes]"
---

# kntnt

The Manager. One namespaced entry point. Every other collection skill is invoked by its own name.

`$HERE` is the directory that contains this SKILL.md.

**Dependencies.** `uv` on PATH. If it is missing, stop and tell the user to install uv from https://docs.astral.sh/uv/.

## Help

If the arguments are `help`, `--help`, `-h`, or `help <name>`, follow `$HERE/help.md` and stop.

## Arguments

- no args / `help` `[skill]` — Help for the manager, or one named collection skill. Bare `/kntnt` means Help.
- `status` `[skill...]` `[--project]` — Status. No names reports every skill the form covers.
- `enable` `[skill...]` `[--project]` `[--yes]` — Enable. No names opens a picker.
- `disable` `[skill...]` `[--project]` `[--yes]` — Disable. No names opens a picker.
- `update` `[--project]` `[--yes]` — refresh this collection, then re-check Dependencies.

Every verb reads `--project` the same way: absent or `--project=off` means Global, `--project` or `--project=on` means this Project. Enable, Disable, and Update change that layer. Status changes nothing, so the flag picks the question instead: Global alone without it, and with it the Effective set — what applies in this working directory.

Which Harnesses a verb reaches is never asked and never recorded: every Harness present in that layer is acted on, worked out on each run.

`--yes` means assume yes: ask nothing that can be answered yes or no. Every verb of `scripts/kntnt.py` accepts it, so passing the user's flag straight through is always safe.

## Steps

1. Take the first argument as the subcommand. No arguments → `help`. `help`, `--help`, or `-h` → `help`.
2. Read `$HERE/<subcommand>.md`. Unknown subcommand → follow `$HERE/help.md` and stop.
3. Follow that file. Done when it says to stop.
