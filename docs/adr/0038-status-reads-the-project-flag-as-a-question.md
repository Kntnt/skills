# Status reads the project flag as a question, not as a target

Every verb reads `--project` the same way: absent or `--project=off` is Global, `--project` or `--project=on` is the Project. Enable, Disable, and Update change the layer they are pointed at. Status changes nothing, so *targeting* a layer is a category error for it — and until now it opted out of the vocabulary altogether, reporting both layers in two columns and ignoring the flag. That was the collection's one inconsistent verb, and it was arbitrary rather than reasoned.

Status now obeys the flag like the rest. Bare, it reports Global: every Catalog skill with its state on this machine, Disabled ones included, because the Catalog still carries them and finding what there is to Enable is what that form is for. With the flag, it reports the **Effective** set — every skill Enabled in Global plus every skill Enabled in this Project (ADR-0013) — and each row says whether it comes from Global, the Project, or both.

**The flag form reports Effective, not the Project layer alone.** Standing in a working directory, the question is not *what did someone check into this repository*, it is *what can I use here*. A report of the Project layer by itself never answers that, and Effective is the term the collection already has for the answer. The layer alone is recoverable from the report — it is the rows sourced from the Project — while the answer to the real question is not recoverable from the layer.

A skill Disabled in both layers is present in the bare form and absent from the flag form. The two forms answer different questions, and *nothing* is the honest answer to *does this apply here*.

One payload serves both: one `state` per skill, a `source` where a source exists to name, and a `reports` field saying which question was answered. Two payloads would have made every reader — the skill body first among them — branch before it could read a row, and the report the user sees must never leave them guessing which of the two questions they are looking at.
