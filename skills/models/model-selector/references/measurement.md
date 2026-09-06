# What is measured, and what it costs

Read when explaining what this Skill records, when answering a question about privacy, or when reporting the measurement store. The user-facing summary of the same contract is in `help.md`; this is the detail behind it.

## The contract in one paragraph

Enabling this Skill installs session lifecycle hooks into every supported Harness on this machine, at the Global layer. They observe finished work, keep only substantial units of it, grade each unit by the cheapest means that can establish anything, and write one row per unit. No prompt, response, diff, file content, terminal line or absolute path is ever copied. Disabling the Skill removes every hook and keeps what was measured; `/model-selector reset --evidence` is the separate act that discards it.

## A Unit of Work

A unit begins at an instruction somebody typed — a person at the keyboard, or a peer agent messaging this session — and ends when the agent hands control back. Nothing else in the record begins one. A background task's report continues the unit it arrives in, and so do the session continuing itself, a tool result, a command echo and the rest of the transcript's own bookkeeping: a unit whose instruction is a notification and whose result is whatever happened next measures nothing anybody asked for. A subagent's own work is one unit, carrying that subagent's own model and deliberation level.

A unit is written only where it was **substantial**: three or more changing tool calls, or sixty seconds, or four thousand output tokens. A changing tool call is one that wrote something — an edit, a file write, a shell command that was not a read. Anything below that threshold is discarded with no trace at all, which is what keeps a session of short questions and answers out of the measurement entirely. A session that alternates between quick exchanges and long jobs contributes only the long jobs.

Nothing is measured while a unit is running. The read happens once, at the session's own last lifecycle event, over that session's own finished record and its companion subagent directory — the file the Harness's own payload named, and nothing wider. A record that cannot be read is an absence, never an error.

## The row

One row per unit, appended to `measurements.jsonl` under the selected data directory:

    attempt_id, at, kind, label, model, deliberation, harness, channel,
    grade, graded_by, tokens (input, cache_read, cache_write, output, reasoning),
    cost_usd, seconds, routed

Kind, model and deliberation are the whole of a measurement's identity: comparability across runs is comparability on those three. `label` is a finer description a caller supplied; it is kept and reported and never splits the comparison, because fragmenting the evidence is the failure this design exists to fix.

`cost_usd` is priced at write time from the rate card, so it is never null where the tokens were exposed. Cost is the list value of the tokens consumed, whoever paid for them, so a subscription seat and an API seat produce one comparable number.

A category the environment did not expose stays an explicit null. An absence read as a zero is how an unmeasured configuration becomes the cheapest thing on a frontier, and it is the reason this row is built by copying named fields rather than by removing unwanted ones.

## What is never copied

Prompts, responses, reasoning traces, diffs, file contents, terminal output, ticket and source bodies, secrets, transcripts, workspace names and absolute paths. The session identity that appears in a row is opaque and is not a path.

## The grade

A grade is a number between nought and one, not a pass or a fail. An attempt that did the work and missed a criterion nobody could have met is not the same event as one that did nothing useful, and recording them identically is a measurement error no sample size corrects.

Work never grades itself. A builder's own report of how it went, and a subagent's confidence in its own output, establish nothing. Four sources establish something, in descending authority:

**checker** — a caller's explicit verdict on the finished work, taken as a number rather than as a pass or fail.

**judge** — one call to a cheap model, described below, where nothing above it decided anything.

**signal** — free heuristics with no model behind them. Tests that ran and passed with no re-attempt score high. An instruction repeated later in the same session — the work was redone — scores low. A unit that was interrupted or errored with no result establishes nothing about the model and is dropped rather than scored zero.

**user** — what a person said.

The workflow's own failures are excluded rather than recorded as a model's failure: a mechanical hinder, an open product decision, a newly discovered dependency, a tracker failure, a merge collision.

## The judge, and what it costs

Where no checker and no free signal decided anything, one call is bought deliberately. The model is asked of the engine for `kind=converse`, which is what this call is — two short excerpts in, a number and a line out, rather than the reading `analyze` is priced for — at high stakes, which is what grading is — nothing checks a grade, and a judge that cannot do the job returns a plausible wrong number. So it is the cheapest point the engine is confident in rather than the cheapest point there is, and never a model named here, so the judge follows the catalogue rather than this page.

It is shown the kind vocabulary, the unit's instruction excerpt and its result excerpt (at most 800 characters each), the tool-call counts, the duration and the token totals. It returns a strict JSON object: the kind, a score from 0 to 100, and one line of reason. **The two excerpts are used to build that call and are written nowhere.** What persists is the number and the one line.

The budget is hard: at most twenty gradings in a pass, at most thirty seconds per call, one call at a time, and no pass at all where the store already holds fifty judge-graded rows from the last twenty-four hours. On a Claude-class cheap model a graded unit costs a fraction of a cent, and the budget bounds a day's worth of it well below the cost of a single routed job.

A judge that cannot be reached — no reachable model, a timeout, output that will not parse — leaves the unit in `pending.jsonl` for the next pass, up to three attempts, after which it is written with its signal grade if it has one and dropped if it does not. **A pass that cannot run never loses a session and never invents a number.**

## Nothing waits for a person

There is no queue to work through, no review verb, and no reminder placed anywhere a model would read it — a measurement prompt inside a session changes the thing being measured. Grading is dispatched detached at the end of a session and holds a lock so two passes cannot both run. Every failure in the hook path is swallowed: capture that breaks somebody's session is worse than no capture.

## Retention, and how to end it

Rows are kept until they are discarded by hand. They survive Disabling the Skill, because what was measured stays true whether or not measuring continues.

`/model-selector reset --evidence` is the one way to discard them, and it has to be asked for by name. It removes the measurement store, the units seen and not yet graded, and the capture directory's in-flight drafts, and it leaves the hooks installed and measuring. Switching measurement off is unchecking this Skill in `/kntnt select`, which removes every entry these hooks own from every Harness.

`/model-selector evidence` is how to see what is held, and `/model-selector status` is how to see the health of the hooks that collect it.
