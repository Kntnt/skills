# delegation

Turn delegation mode on or off — you orchestrate, subagents execute.

## Synopsis

```
/delegation [session|project|user] on|off [--yes]
/delegation [session|project|user] status
/delegation [session]
```

## Description

While delegation mode is on, the agent you are talking to thinks, plans, briefs, and verifies, and hands the execution to subagents on the cheapest model able to do the job. This skill is how that mode is turned on, turned off, and read.

Three scopes, in widening order of reach:

- `session` — this conversation only. Nothing is written to a context file, so nothing outlives the session but a note in whatever scratch directory the harness provides, kept so a compaction cannot lose the state.
- `project` — a managed block in the context file this repository already loads, normally a committed one. Everyone who clones the repository gets the mode.
- `user` — the same managed block in this harness's own global context file. It covers the harness you are in; run the skill in another harness to give that one the mode too.

The verdict is the effective state here and now: a session instruction wins, and otherwise the mode is on exactly when a managed block sits in a context file this harness loads here. `project` and `user` write an identical block, so they cannot disagree.

Your own model and reasoning effort stay yours. Whatever your harness offers for changing them is yours to run, never the skill's.

## Arguments

One scope and one state, bare or flagged, in any order: `/delegation project on`, `/delegation --project --on`, and `/delegation --on --project` all mean the same.

- scope — `session` (the default), `project`, or `user`.
- state — `on`, `off`, or `status`. `status` with no scope reports all three.

## Options

- `--yes` — assume yes: write the persistent scope without waiting for a confirmation. Valid only alongside `on` or `off`.

## Notes

Session is the only scope that can be toggled without saying which way. Flipping a file in your home configuration, or a committed file in a shared repository, off an inferred state is the wrong default, so `/delegation user` with no state changes nothing and prints the synopsis rather than asking which of `on`, `off`, or `status` you meant.

A flag with no work to do on the invocation you typed is refused rather than ignored, because a flag accepted and ignored teaches that flags sometimes do nothing. So `/delegation status --yes` is an error, while `/delegation user on --yes` is not. An invalid form is refused the same way as a disallowed flag, and there is one refusal rather than one per kind of mistake: the synopsis above, a line saying what was wrong, and nothing changed.

Session `off` suspends this skill's own instruction. It does not remove a standing block: that text stays in the context window and its tokens are still paid. A compaction can drop the session instruction while the block survives, so run `/delegation off` again if delegating resumes.

A block whose text no longer matches the skill's is reported as stale, and `/delegation <scope> on` is the fix — it rewrites the block rather than adding a second one.

## Dependencies

`uv` on PATH, the manager installed, and a harness that can spawn subagents. The last one is a Capability no script can test: the skill asks you to confirm it, and does no work where it is not true.

## See also

`/kntnt select` to Enable this skill elsewhere.
