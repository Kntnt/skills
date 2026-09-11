# Only a delegated Unit, or ten minutes of an agent's own work, is measured

This record amends [ADR-0182](0182-how-a-model-is-chosen-and-how-the-choice-is-measured.md) on one point: which Units of Work capture writes. ADR-0182 said that a Unit is written when it is substantial, whoever did the work. That no longer holds for a Unit of the session's own. ADR-0182 stands as written and describes the design at its own date. What the rule now is is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own `references/measurement.md`. This record argues the case.

## What the store showed

**Model Selector is only ever asked to choose a seat for delegated work, but its estimates were fitted on every substantial Unit capture saw.** Most of those were the user's own exchanges with their Main Seat, and those are a different size of job. On 2026-09-11 the live store held 242 captured rows that no router had placed, and half of them ran under five minutes. The routed rows had a median of 17.6 minutes.

**The size difference was read as a model difference.** The Main Seat is mostly Fable and routed builds are mostly Opus. Fable's `implement` rows were therefore mostly one-minute turns, with a median of $1.39 and 67 seconds. Opus's were mostly ticket builds, with a median of $3.86 and 17 minutes. `selection.py --kind=implement` answered `claude-fable-5-1` at `high` over `claude-opus-5` at `xhigh`, even though the measured grades were 0.82 and 0.93. A cheaper job looked like a cheaper model. Nothing in the grade or the price could correct this, because the two rows were not measuring the same kind of work.

## The rule

**What makes a Unit evidence is not whether it was delegated, but whether an agent worked on its own long enough for it to be a job.** So there are two tests, and which one applies depends on where the Unit came from.

- **A delegated Unit is held to the substantial test and nothing else**: three or more changing tool calls, sixty seconds, or four thousand output tokens, unchanged from ADR-0182. Short delegated jobs are exactly what the selector routes, and the median delegated Unit in the pending store ran for 2.5 minutes. A Unit counts as delegated when it is read from a subagent's own record, or when its instruction opens with the `attempt_id:` line a routed brief carries. That line identifies an attempt a dispatcher has already filed a verdict under, and a person at a keyboard does not type it. So a span carrying the line takes the attempt as its identity, the same way a subagent's record does, wherever the span was read.
- **A Unit of the session's own is also held to ten minutes of elapsed time**, measured from the instruction to handing control back. This keeps the two cases that are as informative as a delegation: a person who talks back and forth and then hands over a long task, and a prompt pasted into a fresh session that then runs for half an hour or two hours.
- **Anything else is written nowhere.** It never goes to the pending store and never to the measurement store, so the judge is never paid for it.

**The threshold applies after retries are marked, not before.** A retry is an instruction given twice in the same session, and it is marked among every substantial Unit before the short ones are dropped. A twelve-minute answer asked for again and redone in four minutes therefore keeps its retry signal, even though the redo itself is not written.

**The threshold is on elapsed time, and elapsed time depends in part on the model.** A fast model that finishes a job of its own in eight minutes is dropped, and a slow model that takes twelve is kept. This is accepted knowingly. Real jobs mostly run far longer than ten minutes, and delegated Units are not held to the threshold at all, so the bias applies only to the margin of the one population where speed is not what is being compared. The caveat is stated where the rule is written, so that nobody reading a ranking later has to rediscover it.

## The alternatives

**Measure delegated work only.** This is the simplest rule, and it matches the question the selector is asked. It was rejected because it loses the long own-session runs and the pasted-prompt runs. Those are real jobs on a known seat, as informative as any delegation, and they are a large share of the long work this machine does.

**Keep separate stores for manual and automatic work, each answering whoever asks.** This avoids comparing across populations entirely. It was rejected because it halves the data each answer rests on, and because a person asking Model Selector is almost always asking what to delegate. The manual store would answer a question almost nobody asks, and it would be paid for with evidence the automatic store needs.

## What this leaves out

**A routed attempt launched as a headless `claude -p` process is not measured, and this is a known gap.** A headless transcript carries no `origin` on its user lines, so capture opens no Unit in it, with or without an `attempt_id:` line. Treating a headless session's first line as an instruction would close the gap. It would also capture the judge's own `claude -p` calls, so this change does not do it.

**Units already in the stores are not held to the new rule by code.** The grading pass does not apply the threshold to what is already queued. On 2026-09-11 the maintainer purged the short own-session rows and the queued Units under ten minutes by hand. The figures above describe the store before that purge.
