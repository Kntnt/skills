# Rules — routing and evidence

Read before changing how a Skill of this collection routes work it delegates, what it may file as evidence about it, or what an owned Harness integration installs and reports.

This module covers the routing chain: when Model Selector is reached at all, what its interface promises, how a point is chosen, how a chosen point is actually launched, what becomes a measurement and how a measurement is graded, how delegated execution is shaped, and what an owned Harness integration is allowed to do on the machine. It is not about how the collection reaches a machine, which is `collection.md`, nor about the form of a Skill's or a Feature's shipped files, which is `skills.md`. Model Selector's own references hold the detail; this module states what is true of them and where the boundaries are.

The capitalised terms — Seat, Main Seat, Work Kind, Unit of Work, Measurement, Grade, Deliberation, Bridge, and the rest — are defined in [`CONTEXT.md`](../../CONTEXT.md). That file says what a term means; this module says what is true of it.

The rules whose reasoning is settled in a decision record are named here in a phrase and cited to the record rather than argued again — the record is where the alternatives and their costs live, and a second telling of the argument is a second thing to keep true.

## When routing happens at all

**Model Selector is model-invoked only where another Skill requires its public interface** (ADR-0182). Its description is the complete trigger and excludes recommendation, setup, configuration, evidence inspection and status, each of which stays an explicit user invocation. A machine caller reaches the interface as a script rather than as a Skill invocation, so nothing of the body is loaded into the caller's context to get an answer out of it.

**A spawn the caller runs on its own Main Seat, with no model or deliberation override, is not routed** (ADR-0179). The boundary is the caller's own choice rather than a routing outcome, and there is no judgement call left for spawn time.

**The shortcut removes the ceremony for the default, and must not remove the question** (ADR-0179). Making Main-Seat spawns free while every cheaper seat still routes tilts each decision toward the expensive seat because it is the frictionless one, so cheap judgment-in-noise roles — distillation, summarisation, evidence collection — still weigh a routed cheaper seat rather than defaulting to it.

**A verdict inherits the complete Main Seat exactly and is never routed** (ADR-0085). Judging work is authority rather than a decision that happened to come back inheriting, so no override, route result, repair or failure can downgrade that seat, and verdict work is never price-optimised.

## What the interface promises

**Model Selector answers every call it can parse, and refuses nothing** (ADR-0182). There is no status a caller may read as *start nothing*. Where the profile is missing, where the catalogue is empty, where no candidate is reachable, the answer names the caller's own seat with a note saying why. A caller that must be stopped is stopped by something that knows what the work is worth, and an optimiser does not.

**One call, one answer, and no snapshot travels** (ADR-0182). The caller says what kind of work it has, which scope of models it will accept, what harness and seat it is calling from, and any lock the user typed. It receives the model, the deliberation, the channel that pays for it, one launch instruction, the basis the answer rests on, whether the call was one that explored and on which dimension, and the expected cost and success rate behind it. Nothing of the profile, the catalogue or the measurement store comes back with it.

**A lock is honoured by Model Selector and enforced by the caller** (ADR-0182). A `--model` or `--deliberation` the user typed is passed through and resolved: a family alias resolves through the catalogue, an alias naming several enabled releases takes the newest and says so, and a lock naming nothing known leaves the pool intact and says so. Where a caller has promised its user that an unhonourable lock stops the run, that caller compares what came back against what it asked for and refuses locally. The promise belongs to the layer that made it.

**A decision is reproducible because it was recorded** (ADR-0182). A caller that must route a long run once and hold to it writes the decisions it received into its own durable state and reads them back on re-invocation. It does not freeze the world they were made in, and a state file that cannot be read costs one further call rather than the run.

**No caller reproduces any of the selection policy** (ADR-0182). Candidate filtering, the cost arithmetic, the estimate hierarchy, the ladder an escalation climbs and the launch translation are the module's alone. A caller that wants the next point up after a failure asks for it by naming the point that failed.

## How a point is chosen

**A point is a model and a deliberation, and nothing else** (ADR-0182). Harness, channel, serving mode, tools and policy are facts about how a point is reached and paid for, not dimensions it is compared on. The previous keying was fine enough that no cell in a hundred rows could decide anything.

**Scope is the caller's, and defaults to what it can actually call** (ADR-0182). `limited` admits the caller's own provider; `callable`, the default, adds every model the caller's Harness can reach through a Bridge and the profile has a channel for; `all` admits the whole catalogue. A scope is a statement about reachability and never about preference.

**Cost is what the tokens consumed are worth on the channel that pays for them** (ADR-0182, ADR-0183). One number orders the frontier, for a subscription seat and an API seat alike, because five incommensurable dimensions are five orderings and therefore none. It is the provider's own list value, except where the user has recorded what a channel actually charges — a gateway prices differently from the provider whose model it is, and that card replaces the catalogue's whole, the context cliff included, a threshold being a fact about the provider's own card. Every figure is USD and nothing anywhere converts, so a rate card in another currency is refused by name rather than added to a dollar bill in silence. What a subscription costs per month is not recorded, no verb of this Skill having a use for it.

**What is chosen is the cheapest point the evidence says will finish** (ADR-0184). Every call is ranked the same way: the candidates whose success probability clears the floor are ordered on price and the cheapest is taken, and where none clears it the likeliest is taken instead. Price is second and is never a reason to accept a lower chance of finishing. The stakes no longer change that ranking and decide only whether the call may be explored.

**A bounded share of reversible calls explores one dimension of the answer** (ADR-0184). A store that only ever runs its current favourite can never find out that a cheaper point would have sufficed, so about one call in ten that may be explored buys a row instead of taking the answer. It is a probability per call drawn from the caller's seed rather than a counter, so no particular call is the one and a seed reproduces which calls were. An exploration moves exactly one dimension — the model or the deliberation — chosen by a second coin, because a row that moved both says nothing about either: on `deliberation` it is the answer's own model at a lower level, on `model` it is another model at the answer's level or the nearest that model supports. The candidates are the points cheaper than the answer on that dimension, each drawn once from its own posterior in a fixed order, and the cheapest whose draw clears the floor is taken, else the best draw among them — so a point with few rows has a wide posterior and gets tried, and one that is confidently worse essentially never is, with nothing having to define which is which. Where the chosen dimension has nothing cheaper the answer stands and nothing is reported as explored; the other dimension is not tried in its place. Three requests are answered rather than explored — high stakes, which wants the best point the evidence knows of, nothing standing behind it to catch a wrong one; a request locking a model or a level, a user's instruction being no dimension to vary; and a request naming the point that just failed, which asks for the step up. What the answer reports is the posterior mean either way, the exploration being how the call was spent and never a claim about the world, and an explored answer names the dimension it moved and says what the evidence would have chosen.

**What finishing is counted in is the caller's to choose, and money is the default** (ADR-0182). A run nobody is waiting on is ordered on what it costs to finish; a run somebody is waiting on may be ordered on how long it takes to finish instead, read off the elapsed times actually measured rather than off a rate nobody has established. There is no exchange between the two and none is invented: converting a minute into a dollar is a statement about what the work is worth, and only a person can make it.

**An unpriced point is ranked last and stays eligible** (ADR-0182). A measurement that does not exist is never read as a zero; a null cost is a null cost, and an unmeasured configuration never becomes the cheapest thing on a frontier by having nothing behind it.

**Estimates are pooled up four levels, each the prior for the one below** (ADR-0182). Kind by model by deliberation, then kind by model, then model, then a prior from the model's benchmarked capability against the kind's own difficulty. Each level is a Beta posterior whose prior mean is the level above and whose prior weight is a fixed pseudo-count. A cell with no rows is entirely its parent's estimate, so a model that is mediocre where it has been measured is estimated as mediocre where it has not, and measuring a configuration can no longer disqualify it. A parent is fitted on the rows its child does not hold and only on those, so a row is counted once rather than once per level — the same handful of failures asserted at three levels in succession compounds into a confidence about the model that the handful never bought. A verdict carried between two kinds is damped only where it moves away from what the new kind's own difficulty already predicts; a move toward that prediction is the conservative direction, asserts nothing the difficulty had not said, and is taken whole. Damping both directions alike is what let a model flawless at trivial work read as near-certain at hard work, and what condemned a model on work it had never been asked to do.

**Token appetite backs off the same way** (ADR-0182). It is the other half of the cost arithmetic and it is measured per kind and model rather than assumed, which is how the claim that a stronger model spends fewer tokens enters the decision as evidence rather than as an intuition.

**Capability is a published measurement and nothing else becomes one** (ADR-0182). It seeds the top of the hierarchy where no local row exists. A first-party capability claim, a price and a throughput figure are none of them a capability, and prose never becomes a number.

**One step up is the next point more likely to succeed, the cheapest among those** (ADR-0184). Cheapest by price, or by the clock where the caller asked for time. A caller whose attempt failed names the point that failed and receives that step. A caller that locked a dimension gets no step in it, the value being the user's own, and an escalation is never explored.

## How a chosen point is launched

**There are three launch forms and no fourth** (ADR-0182). A subagent definition this Skill generates, naming the model and the effort; a Bridge command the caller runs as a process; or inheritance, which passes no launch argument at all and runs on the caller's own seat.

**Deliberation is a launchable control on Claude Code, through a generated definition** (ADR-0182). One file per enabled Anthropic model and supported level, prefixed, regenerated on every update, and removed when the Skill is disabled. They are the only files this collection writes into that directory. The alternative — a recommendation the Harness could not honour — is what previously caused evidence to accrue to a level nothing had run at.

**A Bridge is a real argv, produced by the module and run by the caller** (ADR-0182). It names the model and the reasoning control in that tool's own spelling. The caller runs it and reads its output; it composes no invocation of its own.

**Inheritance is the floor and is always available** (ADR-0182). It is what an answer degrades to, and a caller can act on it without knowing why.

## What becomes a measurement

**A Unit of Work is an instruction and its answer** (ADR-0182). It begins when an agent is told to do something, by a person or by another agent, and ends when it hands control back. Only a substantial unit is written — three or more changing tool calls, or sixty seconds, or four thousand output tokens — so the ordinary back-and-forth of a working session leaves no trace at all.

**A Measurement is keyed by kind, model and deliberation, and those three are the whole of its identity** (ADR-0182). It carries the grade, who graded it, the token categories the environment exposed, the priced cost, the elapsed time and whether the work was routed. A finer label the caller supplies is kept and reported and never splits the comparison.

**The observation is built by allow-list, and every field is copied by name** (ADR-0182). Prompts, responses, reasoning, ticket and source bodies, diffs, terminal output, secrets, transcripts and absolute paths are absent because they are never copied. A measurement the environment did not expose stays an explicit null, an absence read as zero being how an unmeasured configuration becomes the cheapest on a frontier.

**Work never grades itself** (ADR-0182). A builder's own report and a subagent's confidence establish nothing. A grade comes from an external checker's verdict, from a free signal, from the judge, or from the user, in that order of authority, and the workflow's own failures — a mechanical hinder, an open product decision, a newly discovered dependency, a tracker failure, a merge collision — are excluded rather than recorded as a model's failure.

**A grade is a number between nought and one** (ADR-0182). An attempt that did the work and failed a criterion nobody could meet is not the event that an attempt which did nothing useful is, and recording them identically is a measurement error no sample size corrects.

**The judge is bought deliberately, and reads only the unit's own ends** (ADR-0182). Where no checker and no free signal has decided anything, one call to a reachable model reads the unit's instruction and its result and returns a number and one line of reason. The point is asked for as the work the call is — a short bounded exchange, two excerpts in and a number out — and never as the work the unit was, a judge priced as a repository read costing more than what it grades. Which model is the selection question asked at high stakes, grading being work nothing checks: the cheapest point the estimates are confident in rather than the cheapest point there is, and decided rather than drawn, because a store whose grades came from a lottery of graders would be measuring the graders. The excerpts are used to make the call and are never stored. It runs under a hard budget, one call at a time, and a pass that cannot reach a model leaves the unit for the next one rather than inventing a number.

**Nothing waits for a person** (ADR-0182). There is no pending queue a user must work through, no review verb, and no reminder placed where a model would read it — a measurement prompt inside the session changes the thing being measured.

## How delegated execution is shaped

**Execution takes one of three paths, chosen by the shape of the work** (ADR-0179). Pure execution with large output runs detached from the conversation, writing to disk, and the Main Seat reads only the report and searches the rest; judgment inside noisy data goes to a subagent for a bounded, task-shaped report; a small bounded command stays on the Main Seat, narrowed at the source. The rule is the shape of the work rather than an order of preference. *When unsure, delegate* survives and is scoped to the choice between subagent and Main Seat: uncertainty about whether something needs judgment is never settled by a detached process, which exercises none.

**The detached path is stated as a property and never as a tool** (ADR-0179). What is said is that the process is detached from the conversation, that its output is on disk, and that its report is the one thing read back; no command, flag, or waiting facility is named, one Harness's spelling of the property being another's.

**The Main Seat ends what it detached, or names it as left standing** (ADR-0179). Whatever a session starts it stops before it reports, and a deliberate exception is named in the report (ADR-0127).

**A delegation brief names a report file inside the spawn's own scratch, and caps the inline reply** (ADR-0179). The subagent writes complete findings to that file and replies with a stated, task-specific budget of conclusions only, no raw command output and no file dumps; the Main Seat reads the file only where its decision needs the detail, and still verifies results independently.

## Owned Harness integrations

**A Skill owns the Harness integrations it installs, and the owner travels in what is written** (ADR-0179). Every entry carries a stable ownership identity inside the command it runs rather than beside it in a key the Harness's own schema does not define, so removal is surgical without anything having to be remembered. Nothing keeps a private ledger of what was installed, so install, repair, update and remove are one operation applied to whatever is actually there. Which Harness is running stays the agent's to say and never a script's to sniff, and a Harness whose lifecycle cannot carry the contract reports an Unsatisfied Capability rather than being quietly skipped.

**Capture follows the Skill's own Enabled state and asks for nothing beyond it** (ADR-0179). Enabling the Skill through the Manager is the whole gesture and Disabling it the whole undo, at the seams `collection.md` describes. Only the Global layer is written, an owned entry being keyed by owner inside a Harness's own configuration, and only a Harness the Library has an adapter for is ever attempted. What Enabling installs, what is retained, and that Disabling removes every entry and keeps what was measured, are stated in the Skill's own `help.md`, readable before the list is answered.

**An adapter is verified against what its own Harness actually reads** (ADR-0179). Event names, entry shape and file location are established from the Harness as installed rather than assumed from a sibling's, and where a fact cannot be established that way the honest answer is Unsatisfied. A Harness that gates a new integration behind a user's trust is reported gated, never healthy: this collection forges no trust decision and writes no trust record on the user's behalf.

**The per-turn hook path is fail-open, bounded and local** (ADR-0179). It runs inside somebody's session, so it does local metadata I/O and nothing else — no model call, no test run, no repository-wide hashing, no transcript read, no long-lived work — and every failure in it is swallowed, capture that breaks a session being worse than no capture.

**The session's own last invocation may read that session's own finished record** (ADR-0179). That moment is not the per-turn path: it is a one-time, inline, bounded read of the transcript the caller's own payload named and that transcript's own companion subagent directory, and nothing wider. The read is field by field onto an allow-list, applied to a source carrying far more, and a record that cannot be read is an absence rather than an error.

**An unattended pass may learn what a model costs** (ADR-0182). The rule that it may learn what a model can do but never what it costs is reversed: a rate card is exactly what this Skill has to be current about, and a price carried with its source URL and retrieval date is auditable in a way a figure typed eight months ago is not. What the pass may never do is store a fact it cannot attribute — a price with no source is discarded rather than kept. The pass stays conditional, one connection at a time, and bounded against a monotonic clock; it starts no model, refuses no request and stops no run. Status is the only surface it reports on.
