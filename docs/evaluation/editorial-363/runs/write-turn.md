# Write turn

The text a run's subagent is given, with `$INSTALL` the staged install for that arm and `$RUN` the run directory. It follows [`../../editorial-362/runs/write-turn.md`](../../editorial-362/runs/write-turn.md), with the two extra evaluator instructions the plan declares.

````text
A user has typed a Skill invocation. You are the session that runs it. The Skill's instructions are the file `$INSTALL/write/SKILL.md`; read it from disk and follow it exactly, including every reference it tells you to load, the shim it tells you to run, and the fresh subagents it tells you to start. `$HERE` is `$INSTALL/write`.

Read nothing under `/Users/thomas/Projects/skills` except `$INSTALL` and `$RUN`, and nothing under `~/.claude/skills`. You have the material in `source.md` and nothing else about where it came from. Do not look for this task, this evaluation, or any ticket: there is none to find, and the run is void if you go looking.

Your working directory is `$RUN/work`, which holds `source.md` and nothing else. Run every shell command from there. Use only `$RUN/scratch/` for any scratch the Skill asks you to create.

The invocation the user typed is:

    /write --genre=case-study --language=$LANG --output=response source.md

Four additions from the person observing this run, which are not part of the Skill and change nothing it does:

1. Before you remove the source-check scratch directory, copy it whole to `$RUN/evidence/`.
2. Save your complete user-facing reply verbatim to `$RUN/response.md`.
3. Save the delivered draft to `$RUN/delivered.md`, exactly as your reply carries it and with nothing added. If the run delivers no draft, create no such file.
4. Write the UTC timestamp to `$RUN/finished.txt` when you end, as `date -u +%Y-%m-%dT%H:%M:%SZ`.

Then give your reply as your final message.
````
