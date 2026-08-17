# `--yes` means assume yes, on every skill and every verb

Wherever a collection skill can ask something answerable yes or no, `--yes` answers it yes instead of asking. One flag, one meaning, across the collection — a user who learns it on `/commit` has learned it on `/kntnt` and `/agents-md`.

Every verb of every collection script accepts the flag, including the verbs that ask nothing. The confirmation itself lives in the skill, because a script run non-interactively cannot prompt; the script's job is only to not make a passed-through `--yes` an error. Before this, `argument-hint` advertised `--yes` on `/kntnt` while `apply enable --yes` died with `unrecognized arguments` — the skill was documented into a crash, and only luck decided whether the model forwarded the user's own flag.

Where a subcommand deletes files, the flag is also the gate: the script refuses without it. `apply disable` removes skills from disk, so requiring `--yes` there means the confirmation step cannot be skipped by accident, only on purpose. Verbs that add or refresh take the flag and ignore it.
