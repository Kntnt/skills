# kntnt select

Show what this collection has and change it in the same gesture.

## Synopsis

`/kntnt select [--project[=on|off]] [--yes] [--dry-run]`

## Description

Prints the catalog as a list grouped by category, one row per skill. A row carries a checkbox — checked when the skill is Enabled in the layer being targeted — the skill's one-line description, and any capability it requires of the harness, so nothing about a row has to be looked up somewhere else.

You answer the list in one sentence of plain text, and changing several skills is one reply rather than a walk through a menu. Checked means Enabled. You are asked to confirm once, and nothing reaches the disk before that.

The structure between skills is on the list rather than behind it. A skill that needs another one of this collection is shown locked while that other is unchecked, and the row names what to check instead. Check it anyway and what it needs comes with it: you are asked one yes/no question naming exactly what would be added, once for the whole chain — checking `release` where you have neither `push` nor `commit` is a single yes rather than one question per level — and nothing is written until you have answered it. `--yes` answers it.

Unchecking a skill that another checked skill depends on is reported, not blocked. You are told what it leaves unsatisfied, and the answer stands: it is your machine.

Reading is never a side-effecting act. An answer that changes nothing writes nothing — no refresh, no repair, no touching of files to make the disk agree with a list you only wanted to look at.

## Options

- `--project`, `--project=on` — list and change this project rather than global. `--project=off` is the bare form.
- `--yes` — assume yes: apply the answer without waiting for a confirmation. Unchecking deletes files, so the script itself refuses without it.
- `--dry-run` — run it against a temporary home seeded with this collection's files, and throw that home away. Nothing in the layer changes, and the report is the run's own outcome read off the sandbox's disk. It downloads the transport afresh, so it takes longer than the run it previews.

## Notes

A skill whose files reached only some of the directories the layer covers is shown checked and marked incomplete. That is a fact about the disk rather than a third state anyone chooses — a skill is Enabled or Disabled — and confirming the list repairs it.

A skill whose files differ from the ones the collection ships is marked **deviating**, never *out of date*. The comparison sees two states and no history, so it cannot say which way the difference runs, and outside a project copy that has fallen behind the commoner cause is an edit of your own. Re-copying it overwrites that edit, and the offer says so.

Where the collection cannot be reached, the list comes from the copy stored beside the manager and says so. Nothing is marked deviating or current on such a list, and no re-copy is offered from it: those digests describe the collection as of the last `/kntnt update`.

`--project` shows the project layer alone. A skill already Enabled globally is marked as such rather than shown unchecked: this layer holds no copy of it to uncheck, and checking the row would give you a second one.

Which harnesses are reached is never asked and never recorded: every harness present in the targeted layer is written to, worked out on every run. With no harness detected, the shared `.agents/skills` directory is written to alone.

The list closes by counting the skills on disk that carry this collection's marker and no longer appear in the catalog. `/kntnt update` is what takes those off.

## See also

`/kntnt help update`, `/kntnt help uninstall`.
