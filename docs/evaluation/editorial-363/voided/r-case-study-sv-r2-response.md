`/write --genre=case-study --language=sv --output=response source.md`

## Stopped: unsatisfied capability `subagents`

The Skill declares one capability, and I have to answer it before anything else. Its confirm sentence is:

> you can spawn subagents that work in their own context window

That sentence is **not true of this session**. There is no subagent tool here. The only agent-related tools available are `TaskStop` and `SendMessage`, both of which act on agents that already exist, and a direct attempt to start one returns:

```
No such tool available: Task. Task is disabled for this session, in subagents as well as here.
```

**How to satisfy it:** run this skill in a harness that can spawn subagents.

## Why this stops the run instead of being worked around

The capability is not incidental to `write`. The source and quotation comparison is what makes the draft deliverable, and it requires a fresh checker with its own context window and no conversation history — precisely so that the comparison is not made by the same reading that produced the draft. I cannot stand in for that checker: I have already read the brief and would be validating my own prose against my own memory of the source, which is the one thing the step exists to prevent. A Swedish case study would also carry translated quotations, whose target-language reading the same step is required to check.

Nor is there a legitimate substitute at hand. The skills that can reach a background agent are research tools that browse, which the comparison task explicitly forbids, and starting an external process would be neither the inherited main seat nor a checker under this Skill's task.

## State

Nothing was written, created, or modified. No draft exists, nothing was delivered, and no output was produced at the response target. `source.md` was read and the invocation was parsed without error — the flags `--genre=case-study`, `--language=sv` and `--output=response` are well-formed — but genre, technique and language were never resolved against the installed resources, because resolution comes after the capability check and the run stops here.

Re-run the same invocation unchanged in a harness that can spawn subagents.
