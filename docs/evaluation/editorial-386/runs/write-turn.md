# Turn

A user has typed a Skill invocation. You are the session that runs it. The Skill's instructions are the file `/private/tmp/claude-501/-Users-thomas-Projects-skills/1152bc7f-820e-46e3-b676-a0818805225f/scratchpad/eval-stage/skills/write/SKILL.md`; read it from disk and follow it exactly, including every reference it tells you to load, the shim it tells you to run, and the fresh subagents it tells you to start. `$HERE` is `/private/tmp/claude-501/-Users-thomas-Projects-skills/1152bc7f-820e-46e3-b676-a0818805225f/scratchpad/eval-stage/skills/write`. Read nothing under `/Users/thomas/Projects` and nothing under `~/.claude/skills`.

Your working directory, the invocation the user typed, and the run directory are given in the message that sent you here. Run every shell command from that working directory. Use only the `scratch/` directory inside that working directory for any scratch the Skill asks you to create.

Nobody is available to answer a question. Where the Skill tells you to ask the user something, state the question in your final reply and stop the run there.

Two additions from the person observing this run, which are not part of the Skill: before you remove the source-check scratch directory, copy it whole to `evidence/` in the run directory; and when you are done, save your complete user-facing reply verbatim to `response.md` in the run directory, then give that same reply as your final message.
