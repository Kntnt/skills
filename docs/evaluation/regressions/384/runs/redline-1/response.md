I checked the one capability this Skill declares before doing anything else, and I cannot confirm it.

**`subagents`** — "you can spawn subagents that work in their own context window": **not true of me here.** This session has no tool for starting an agent in its own context window. I searched the available and deferred tools and found only ones for messaging and stopping agents that already exist (`SendMessage`, `TaskStop`), not one for starting a new one.

That capability is not optional decoration for this Skill. The Correction Budget is spent by handing each round's repair to a subagent started fresh, with no history of the earlier rounds, precisely so that the previous round's framing cannot bias the next repair. I could not substitute my own editing for that without quietly changing what the Skill does: I have read the text, so a correction from me would be the one thing the design rules out.

**How to satisfy it:** run this Skill in a harness that can spawn subagents.

Nothing has been reviewed and nothing has been written. `input.md` is untouched, and no output was produced.
