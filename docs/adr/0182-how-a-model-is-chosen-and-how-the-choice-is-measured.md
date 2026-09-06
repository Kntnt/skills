# How a model is chosen, and how the choice is measured

This record settles the question Model Selector exists to answer: given work to be done, which model at which deliberation completes it for the least money, and how does the answer get better without anybody being asked to make it better. It replaces the selection-and-evidence half of [ADR-0179](0179-how-work-is-routed-and-what-becomes-evidence.md) and the eight anchors that record left standing, and it does so on measurements taken from the machine the previous design had been running on for eight months. What the rules now are is stated in [`docs/rules/routing.md`](../rules/routing.md), which is the authority on them. This record argues; it does not legislate.

## The records folded into this one

- ADR-0083 — Model Selector owns exact frozen routing
- ADR-0089 — Routed work reports the evidence it never imports
- ADR-0110 — A changed-nothing fix round escalates once from a selected seat
- ADR-0137 — Orchestrate imports machine-judged observations at verdict
- ADR-0147 — The frozen objective orders a frontier nothing else can
- ADR-0149 — A Cohort starts where its Standing Policy says, and only a reset lowers it
- ADR-0151 — An Exploration Attempt buys contrast one Rung down, on a budget
- ADR-0166 — An unranked main seat suspends the ceiling it cannot state
- ADR-0172 — A frozen account that inherits for the run restates its own decision
- ADR-0179 — How work is routed and what becomes evidence, in its selection and evidence half

**What of ADR-0179 still stands, and is not folded here.** That execution takes one of three paths chosen by the shape of the work; that a delegation brief names a report file in the spawn's own scratch and caps the inline reply; that a Skill owns the Harness integrations it installs and the owner travels in what is written; that the per-turn hook path is fail-open, bounded and local; and that the session's own last invocation may read that session's own finished record. Those paragraphs describe how work is shaped and how a machine is measured, and this record changes neither. [ADR-0085](0085-orchestrate-routes-execution-and-inherits-verdicts.md), which holds that a verdict inherits the complete Main Seat and is never price-optimised, also stands: judging work is authority rather than an optimisation, and nothing here touches it.

## Six findings, and none of them is an argument

The previous design was not wrong in its reasoning. It was wrong about the world, in six places, and each of the six was measured rather than reasoned about. They are written out because the temptation, on reading a design this elaborate, is to assume its elaborations were earned.

**The thing being optimised was never measured.** Of the hundred rows in the maintainer's evidence ledger, none carried a cash figure, none carried a quota figure, and two carried a token count of any kind. Beside that ledger sat forty-nine Usage Records that did carry token counts — one Claude Code session on `claude-opus-5` had spent 27.8 million cache-read tokens against 32 791 output tokens — and the design forbade every one of them from touching a decision, on the ground that work never grades itself. That ground is sound and the conclusion drawn from it was not: a Usage Record is not a verdict, but it is the only honest statement anybody had about what a configuration costs. So the shipped `cost_first` objective ordered candidates on a dimension that was null for every one of them, fell through to its documented tie-break, and selected by the Rung ladder — the weakest model first. That is why an unlocked run on this repository started on Haiku 4.5, whose record in the cohort it was selected for was nought for two.

**A load-bearing premise about the Harness was false.** The whole chain from `carried_by: inheritance` through `carried_control_not_selectable` to the `unavailable_override` refusal rests on the claim that Claude Code cannot set a subagent's deliberation and that nothing in this collection can change that. A subagent definition takes `model:` and it takes `effort:`, with the same five levels this collection calls portable. The premise was never checked against the Harness, and two open defects — a `--deliberation` lock that cannot be honoured for any Claude model, and a run stopped because no combination of flags could reach the point the evidence supported — are both artefacts of it rather than of the contract they were filed against.

**Evidence was keyed finely enough that it could never become dense.** A point was model by effort by harness by tools by policy by channel by price schedule, and a frontier split again on benchmark key by stage by cohort by sorted tags. A hundred rows over eight months therefore populated no cell well enough to decide anything. Worse, the rule that excluded a point whose conservative lower bound sat under a quality floor applied only to a point that had one: a configuration nobody had measured carried no bound and could not fail the test. Measuring a good configuration could disqualify it while never measuring a worse one kept it eligible for ever. On the day this was found, `claude-opus-5` at `xhigh`, six for six, was excluded in favour of `claude-haiku-4-5` at `xhigh`, which had never been run at all.

**An advisory service could stop the work.** A refusal is read as *start nothing*, and the reasons a routing decision could refuse under included an override the environment could not express and a candidate pool the quality floor had emptied. The service that exists to make a run cheaper could therefore make it not happen, after the tickets were read, the waves computed and the frontier planned, and before any of the work began.

**Several constraints were invented rather than required.** A ceiling forbidding a routed seat to exceed the Main Seat; a quality floor at 0.70; a Standing Policy that ratcheted per Cohort with epochs and revisions; Exploration Attempts drawn against an epsilon and a per-run budget; a lexicographic objective over five incommensurable cost dimensions with optional shadow prices between them. Each is defensible alone. Together they are a machine whose most reliable output was a refusal.

**It was expensive to ask.** A 29 kB body, some 100 kB of references behind it, a runtime block of eleven facts the caller had to assemble, and two calls — the second of which echoed the entire frozen snapshot, profile and evidence ledger and every adapter translation included, back through the context window of a caller that was often already full.

## An advisory service answers, and it never refuses

**Model Selector returns an answer to every call it can parse.** There is no status a caller can read as *stop*, because a caller that must stop has to be stopped by something that knows what the work is worth, and an optimiser does not. Where the profile is missing, where the catalogue is empty, where nothing at all is reachable, the answer is that the caller should run the work on its own seat, with a note saying why. That is a floor rather than a failure: the caller was going to have a seat regardless, and the service's job is to improve on it or say it cannot.

**A lock the environment cannot honour still stops a run — and the caller stops it.** The promise that `/orchestrate --model=<name>` is honoured or the run refuses is a contract between Orchestrate and the developer who typed the flag, and it survives untouched. What changes is who keeps it: Orchestrate passes the lock through, compares what comes back against what it asked for, and refuses locally. One string comparison replaces a protocol, and the layer that owns the promise is the layer that enforces it. The case also nearly disappears, a family alias now being a first-class catalogue field rather than a vocabulary the lock could not reach.

**The ceiling goes, and nothing replaces it.** A routed seat was forbidden to exceed the Main Seat on the reasoning that the user chose their own session and routing decides only what runs beneath it. But the user chose their session for the conversation they are having, not as a budget for every job it delegates, and the objective already prices strength: a model that costs more is chosen only where it is expected to cost less per completed job. A ceiling on top of that objective is a second, blunter answer to a question the first one answers well, and its measured effect was to refuse the one configuration with a perfect record.

## One cost, and it is the money the tokens are worth

**Cost is the list value of the tokens a job consumed, whoever paid for them.** Five incommensurable dimensions — cash, rolling quota, weekly quota, allocated subscription cost, latency — are five orderings and therefore no ordering, which is why the shipped objective needed shadow prices the user was never going to supply. Every one of them is a way of asking what the tokens were worth, and the rate card answers that directly for a subscription seat and an API seat alike. What was actually paid is recorded, because the renewal question is real and needs it; what candidates are ranked on is one number.

**The number that is minimised is the cost of finishing, not the cost of trying.** Expected cost is the priced token appetite of a point divided by the probability that the point completes the work, because an attempt that fails is an attempt whose cost bought nothing and whose work is still to do. This is the whole of the two requirements the maintainer stated — the job must get done, and it must cost as little as possible — expressed as one quantity rather than as a constraint bolted onto a price. It is also what makes the intuition about strong models rigorous: a model that reasons better tends to spend fewer tokens reaching the same place, so its token appetite is measured per kind of work rather than assumed, and the arithmetic decides whether the cheaper token or the shorter path wins on this particular kind of job.

**Where a point cannot be priced it is ranked last and still eligible.** An unpriced candidate is not a free one, and the previous design's habit of reading an absent measurement as a zero is exactly how an unmeasured configuration became the cheapest thing on a frontier.

## Evidence is pooled up a hierarchy, so that no cell is empty

**A point's success rate is estimated at four levels, each the prior for the one below it.** Kind by model by deliberation, backing off to kind by model, backing off to model, backing off to a prior derived from the model's benchmarked capability against the kind's own difficulty. Each level is a Beta posterior whose prior mean is the level above and whose prior weight is a fixed pseudo-count, so a cell with three rows is mostly its own rows and a cell with none is entirely its parent's estimate.

**This is what makes an unmeasured point stop being attractive.** Under the previous rule an unmeasured cell had no bound to fail and so passed every filter; under this one it inherits its parent's estimate, and a model that is mediocre wherever it has been measured is estimated as mediocre where it has not. The perverse incentive — that measuring a configuration could only ever hurt it — is gone by construction rather than by a rule saying it should be.

**Token appetite backs off the same way, over the same four levels.** It is the second half of the cost arithmetic and it is a measurement, not a constant, for the same reason the success rate is.

**A finer label never splits the evidence.** A caller may say that this was an `orchestrate/initial_build`, and that is kept and reported; it does not create a cohort. A cohort per brief is a frontier of one row, and the previous design's cohorts were fine enough that its four largest held twenty-three, nine, eight and one row respectively. The classification that governs comparison is a closed vocabulary of eight kinds of work, chosen for the single property that it predicts how much intelligence a job needs.

## Work is graded on a scale, and the grade is bought

**A binary outcome was unjust to the configuration it was measuring.** An attempt that did the work correctly and failed a criterion that could not be met is not the same event as an attempt that did nothing useful, and recording them identically is a measurement error that no amount of sample size corrects. The outcome is a number between nought and one.

**The grade comes from the most authoritative source available, and a model is the last of them.** An external checker's verdict outranks everything; free signals — a task re-attempted, a declared test suite that ran and passed, an interrupted turn — come next; and where neither has decided anything, a cheap model reads the finished unit's own instruction and result and returns a number and one line of reason. That last is a real cost and a real disclosure, and it is taken deliberately: without it the scale collapses back to the binary it replaced, because the free signals are silent on most work. The excerpts it reads are used to make the call and are never stored; what persists is the number and the reason.

**The unit measured is an instruction, not a session.** Work begins when an agent is told to do something — by a person or by another agent — and ends when it hands control back. A session that alternates between quick questions and long jobs contributes the long jobs and nothing else, which is what a threshold on changing tool calls, elapsed time and output tokens enforces. Below it, nothing is written at all, so the ordinary back-and-forth of a working session leaves no trace to be averaged into anything.

**The wall between what is measured and what is judged comes down, and the rule it protected is restated where it belongs.** Ordinary work still never grades itself: a builder's own report establishes nothing, and it is a checker, a signal, a judge or the user that supplies a grade. What changes is that the usage a session actually spent is allowed to be the cost of the work it did, instead of being kept in a second store on the ground that it carried no verdict. The two facts were always about one attempt.

## Deliberation is a control this Harness has, once somebody writes the file

**A subagent definition carrying `model` and `effort` is the launch instruction.** Model Selector generates one file per enabled Anthropic model and supported level, and a decision launches by naming the definition rather than by passing arguments the Agent tool does not take. This is the mechanism the previous design was built around not having, and it turns a recommendation that could only be advice on this Harness into one that is actually launched — which matters because evidence accrues to what ran, and evidence about a level nothing ever ran at is worth nothing.

**The trade this makes is writing into the user's own global configuration.** The files are generated, prefixed, regenerated on every update and removed when the Skill is disabled, and they are the only thing this collection puts in that directory. The alternative was a recommendation the Harness could not honour, measured against a seat it did not name, which is how the previous design came to have six perfect runs at a level its own contract said could not be selected.

## What a caller pays to ask

**The machine interface is a script, and the body is for people.** A caller runs one command and reads one small object; it does not load a Skill body, does not assemble a runtime block of eleven facts, and is never handed a frozen snapshot back. The previous shape cost a caller a body, a set of references and an echoed snapshot, per call, in a context window that was frequently the scarcest thing in the run — and what it bought was reproducibility that the caller was already getting by writing the decision into its own state directory.

**A decision is reproducible because it was recorded, not because the world was frozen.** Orchestrate keeps the decisions it made and re-reads them on re-invocation, exactly as it did. What it stops keeping is the snapshot beside them, and a routing file that cannot be read stops being irreplaceable: the run routes again, says so in its report, and continues. Losing an unattended run costs the whole night; one local call costs nothing.
