# Turn

A user has typed a Skill invocation. You are the session that runs it. The Skill's instructions are the file `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/380.scratch/eval-stage/skills/redline/SKILL.md`; read it from disk and follow it exactly, including every reference it tells you to load, the shim it tells you to run, any peer Skill it tells you to run from the same staged directory, and any fresh subagent it tells you to start. `$HERE` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/380.scratch/eval-stage/skills/redline`.

Read nothing under `/Users/thomas/Projects/skills` outside `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/380.scratch/eval-stage/`, and nothing under `~/.claude/skills`. The staged directory above is the whole of the installation you have. You have the text in `input.md` and nothing else about where it came from.

Your working directory, the invocation the user typed, and the run directory are given in the message that sent you here. Run every shell command from that working directory. Use only the `scratch/` directory inside that working directory for any scratch the Skill asks you to create.

Nobody is available to answer a question. Where the Skill tells you to ask the user something, state the question in your final reply and stop the run there.

One addition from the person observing this run, which is not part of the Skill: when you are done, save your complete user-facing reply verbatim to `response.md` in the run directory, then give that same reply as your final message.
