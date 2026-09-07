---
name: kntnt
description: Manage this collection — which skills are Enabled, in Global and in each Project.
disable-model-invocation: true
argument-hint: "[help [command]] | select [--on=<entry>] [--off=<entry>] [--project[=on|off]] [--yes] [--dry-run] | update [--project[=on|off]] [--yes] [--dry-run] | uninstall [--yes] [--dry-run] [-- <instruction>]"
compatibility: Requires uv, and npx plus network access for the transport and the Catalog fetch
---

# kntnt

The Manager. One namespaced entry point. Every other collection skill is invoked by its own name.

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is the Collection Library it ships, at `$HERE/library/`.

**Dependencies.** `uv` on PATH. If it is missing, stop and tell the user to install uv from https://docs.astral.sh/uv/.

## Invocation

Run `uv run "$HERE/scripts/kntnt.py" invoke --here="$HERE"` with the invocation payload — everything the user typed after `/kntnt`, verbatim, however many lines — on stdin. On exit 0 continue from the JSON it prints. On any other exit print its stdout verbatim and stop: it has already printed what the user is to see, and none of that text is yours to write.

In the JSON, `path` is the verb as a one-word list, and empty for bare `/kntnt`; `flags` holds each flag the user wrote — `true` where it stood bare, its value where it carried one, a list of values where it was repeated; `operands` is what followed the flags, in order; `instruction` is the Contextual Instruction, or `null`, and what it may settle is stated in `$LIBRARY/references/invocation-envelope.md`.

## Arguments

Every verb reads `--project` the same way: absent or `--project=off` means Global, `--project` or `--project=on` means this Project. Select and Update change that layer, and Select lists it. Uninstall takes no `--project`: it clears this machine, and a working directory's own copies belong to that project.

Which Harnesses a verb reaches is never asked and never recorded: every Harness present in that layer is acted on, worked out on each run.

`--yes` means assume yes: ask nothing that can be answered yes or no. On a real Global Update, only `--yes` in the current Formal Invocation skips the later confirmation; never infer it from Contextual Instruction, Conversation Context, earlier guidance, a repair request, or a handoff.

`--dry-run` runs a changing verb for real against a temporary home seeded with this collection's own files, and throws that home away when the run ends. Nothing on the machine changes, and what comes back is the verb's own outcome rather than a description of what it would have done. It has an npm cache of its own, so the transport is downloaded afresh and the run takes noticeably longer than the one it previews — say so before starting it. A payload carrying `dry_run` is such a run's outcome: report it as the outcome it is, say in the same breath that nothing on the machine changed, and read its `directories` as the Sandbox's copies of the real ones — they sit under the temporary home `dry_run.sandbox` names, and that home is gone by the time you read the payload.

## Steps

1. The verb is the one word in `path`; an empty `path` is bare `/kntnt`, which is `help`.
2. Read `$HERE/steps/<verb>.md` and follow it, passing the flags on as they stand — a flag read as `true` as its bare name, one read with a value as `--flag=value`, one read as a list once per value — and never dropping one to make a run succeed. Done when it says to stop.
