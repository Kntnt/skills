---
name: kntnt
description: Manage this collection — which skills are Enabled, on which Harnesses.
disable-model-invocation: true
argument-hint: "[status|setup|enable|disable|update|help] [skill...] [--project] [--yes]"
---

# kntnt

The Manager. One namespaced entry point. Every other collection skill is invoked by its own name.

`$HERE` is the directory that contains this SKILL.md.

**Dependencies.** `uv` on PATH. If it is missing, stop and tell the user to install uv from https://docs.astral.sh/uv/.

## Help

If the arguments are `help`, `--help`, `-h`, or `help <name>`, follow `$HERE/help.md` and stop.

## Arguments

- no args / `status` `[skill...]` — Status. Bare `/kntnt` means Status.
- `setup` — record the Harness list.
- `enable` `[skill...]` `[--project]` `[--yes]` — Enable. No names opens a picker.
- `disable` `[skill...]` `[--project]` `[--yes]` — Disable. No names opens a picker.
- `update` `[--project]` `[--yes]` — refresh this collection, then re-check Dependencies.
- `help` `[skill]` — help for the manager, or one named collection skill.

Enable, Disable, and Update target Global unless `--project` or `--project=on` is given. `--project=off` targets Global.

## Steps

1. Take the first argument as the subcommand. No arguments → `status`. `help`, `--help`, or `-h` → `help`.
2. Read `$HERE/<subcommand>.md`. Unknown subcommand → follow `$HERE/help.md` and stop.
3. Follow that file. Done when it says to stop.
