# A harness requirement is a Dependency the agent answers, not an install-time gate

Some skills need something of the Harness itself, not of the machine: `delegation` is meaningless where subagents cannot be spawned. The obvious fix — let the Catalog say which Harnesses a skill belongs on and have Enable install it only there — is the matrix ADR-0005 rejects: the desired set would differ per Harness, Status would have to report per Harness, and the drift the collection exists to prevent returns through the back door.

So a Capability is modelled as a fourth kind of Dependency, alongside binaries, skills, and externals. The skill is installed everywhere and refuses where it does not fit, exactly as an Unsatisfied binary makes it refuse — one desired set, one layer model, ADR-0005 and ADR-0013 untouched.

The check is split because it has to be. `kntnt.py` cannot know which Harness invoked it, still less what that Harness can do; an env-var sniff would be a guess, and a wrong guess would refuse a skill that works. The agent knows, because the agent *is* the Harness. So `check` reports each required Capability with a `confirm` sentence and a `how`, and the skill's own instructions make answering them part of the check. Exit 0 with a non-empty `capabilities` list means "nothing missing that a script can see", not "go ahead". Every legal name is defined in the script, so a misspelt Capability fails when the Catalog is generated rather than passing silently as a check that never runs.

The mode text itself still carries a degrade line for a harness with no subagents, because project scope writes it into a committed `AGENTS.md` that agents other than the one that ran the skill will read (ADR-0026).
