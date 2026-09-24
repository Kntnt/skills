Before `/redline` starts, it checks that it has what it needs to run. One requirement isn't met here.

- **Subagents.** The requirement is that I can start subagents that each work in their own context window. I can't in this session. None of my tools starts one, and `/redline` hands each correction to a new subagent that starts with no history.

To fix this, run this skill in a harness that can start subagents.

Nothing was reviewed, corrected or written, and `input.md` is unchanged.
