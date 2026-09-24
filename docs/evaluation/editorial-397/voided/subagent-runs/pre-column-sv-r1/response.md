I couldn't run /redline in this session, so I reviewed nothing and wrote nothing.

/redline needs to start a fresh subagent, with its own context window, for each correction round. This session has no tool that can start one. It can only send messages to agents that are already running.

To fix it, run this skill in a harness that can spawn subagents. Then run `/redline --output=response input.md` again.

`input.md` is unchanged.
