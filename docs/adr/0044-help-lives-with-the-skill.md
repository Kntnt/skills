# Help lives with the skill, and `--help` is its route

`/kntnt help commit` requires knowing that `commit` arrived through this collection. That is exactly the sort of fact a user should not have to hold: the skill is in front of them, it answered when they typed its name, and the one thing they could not ask it was what it does.

So every collection skill ships `help.md` beside its `SKILL.md`, and its `SKILL.md` instructs it to print that file and stop when it is invoked with `--help`. One rule holds everywhere in the collection: `help.md` is always the manpage. The Manager's own files separate by kind on the same rule — agent instructions per verb under `steps/`, a manpage per verb under `help/`, and `help.md` as the Manager's own manpage — so *where is the help* has a single answer whether the thing being asked is a skill or a subcommand. This binds the five skills shipped today and every one added later.

Help that the agent generates from a skill's own Steps section is help that drifts the first time the instructions change and nobody re-reads the output, and drifts silently, because there is nothing to diff. A file is a thing a reviewer can read, and a thing the skill can print without deciding anything.

**Reading about a skill one does not yet have moves into `select`.** That is where the decision is actually made, and where the old route was really being used from. The list reads an installed skill's `help.md` from disk and fetches `skills/<category>/<name>/help.md` from the origin for one that is not installed; `category` is already a Catalog field, so the path is derivable and nothing new has to be published to make it work. Where the origin cannot be reached and the skill is not installed, the user is told that, rather than shown an empty help or one the agent invented.

With that route in place `/kntnt help <skill>` is withdrawn rather than kept alongside it. A second way to the same text is a second thing to keep true, and this one asked the user to remember the wrong fact. `/kntnt help <command>` stays, because the Manager's own verbs are the Manager's to document, and bare `/kntnt` still prints Help (ADR-0027).

None of this makes the Manager the owner of a skill's documentation. It never was; it was only the address.
