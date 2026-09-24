I stopped before the review started. /redline needs to start subagents, and this session can't. I reviewed nothing, and `input.md` is unchanged.

**What's missing:** /redline hands each correction to a new helper agent that has its own context. This session has no tool for starting one.

**How to fix it:** run `/redline --output=response input.md` again from a Claude session that can start subagents, such as an ordinary top-level Claude Code session.
