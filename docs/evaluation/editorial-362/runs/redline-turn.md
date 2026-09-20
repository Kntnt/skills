# Turn

A user has typed a Skill invocation. You are the session that runs it. The Skill's instructions are the file `/private/tmp/claude-501/-Users-thomas-Projects-skills/a176b05b-0635-4d22-b0f4-f5c709efebe2/scratchpad/install/redline/SKILL.md`; read it from disk and follow it exactly, including every reference it tells you to load, the shim it tells you to run, any peer Skill it tells you to run from the same staged directory, and any fresh subagent it tells you to start. `$HERE` is `/private/tmp/claude-501/-Users-thomas-Projects-skills/a176b05b-0635-4d22-b0f4-f5c709efebe2/scratchpad/install/redline`. Read nothing under `/Users/thomas/Projects` and nothing under `~/.claude/skills`. You have the text in `input.md` and nothing else about where it came from.

Your working directory, the invocation the user typed, and the run directory are given in the message that sent you here. Run every shell command from that working directory. Use only the run directory's `scratch/` for any scratch the Skill asks you to create.

One addition from the person observing this run, which is not part of the Skill: when you are done, save your complete user-facing reply verbatim to `response.md` in the run directory, then give that same reply as your final message.
