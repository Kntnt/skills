`/redline` cannot run here. Before anything is read or reviewed, the Skill requires me to answer its capability check, and one Capability is not true of me.

**`subagents` — "you can spawn subagents that work in their own context window": no.**

This session has no tool that starts a subagent. `SendMessage` can only message agents that already exist, `TaskStop` can only stop one, and the `Skill` tool runs a skill inside my own context rather than a separate one. `/redline` delegates each correction round to a subagent started fresh, with no history of the round before it, so there is no way for me to perform that part of the Skill honestly — doing the corrections myself would give exactly the biased repair the fresh-subagent rule exists to prevent.

**How to satisfy it:** run this skill in a harness that can spawn subagents.

Nothing was changed. `input.md` was not reviewed and not written to, and no output was produced.
