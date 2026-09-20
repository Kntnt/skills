# Turn

A user has typed a Skill invocation. You are the session that runs it. The Skill's instructions are the file `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/376.scratch/install/write/SKILL.md`; read it from disk and follow it exactly, including every reference it tells you to load, the shim it tells you to run, and the fresh subagents it tells you to start. `$HERE` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/376.scratch/install/write`.

Read only the staged install under `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/376.scratch/install/` and your own run directory. Read nothing else on this filesystem, and in particular nothing under `~/.claude/skills`, nothing under `/Users/thomas/Projects/skills/skills/`, and nothing under `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/376/`.

Your working directory, the invocation the user typed, and the run directory are given in the message that sent you here. Run every shell command from that working directory. Use only the run directory's `scratch/` for any scratch the Skill asks you to create.

Two additions from the person observing this run, which are not part of the Skill: before you remove the source-check scratch directory, copy it whole to `evidence/` in the run directory; and when you are done, save your complete user-facing reply verbatim to `response.md` in the run directory, then give that same reply as your final message.
