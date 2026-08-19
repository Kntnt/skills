# All deterministic reasoning lives behind one seam

An unattended run over a ticket graph has two kinds of work in it. One kind is deterministic: read the tracker, parse the blocking edges, compute which tickets are workable now, record what happened, decide when to stop, render the account. The other kind is what only an agent can do: brief a session, judge whether work is finished, choose how to repair a collision.

A sketch that preceded the spec split the skill along a different line. Where the Harness offered an orchestration primitive, a fast path would use it and let that primitive hold the bookkeeping; everywhere else a slow path would keep the same bookkeeping in the agent's own context. That split is abandoned, and this is the decision that replaces it: **every deterministic step lives in a Python engine, and the engine's command-line interface is the skill's only seam.**

Three reasons, in the order they bind.

**One skill, one behaviour.** ADR-0005 says the desired set is one set across Harnesses; a skill that is sharp where one vendor's primitive exists and vague everywhere else breaks that at the level that matters most — the frontier computation, where being vague means building a ticket before the work it depends on exists. Determinism in the engine is the same determinism in every Harness.

**Only the engine can be tested.** A skill body is prose, and no Collection skill's prose carries tests. Bookkeeping kept in an agent's context is therefore bookkeeping nothing constrains — and the frontier is exactly the reasoning a regression would be silent in. Behind a command line it is arguments in, JSON and an exit code out, which the suite can hold to.

**What the primitive actually adds is concurrency, and concurrency has a flag.** The ceiling on how many tickets run at once is a number the developer passes; it is not a reason to fork the architecture.

So the skill body calls the engine and does what only an agent can. The engine emits JSON and never prompts — a script has no terminal to ask a question in — which is also why `--yes` reaches every one of its verbs (ADR-0029) and why the agent, not the engine, is what renders the plan to the user (ADR-0045).

**What this costs.** A decision the engine gets wrong is wrong identically everywhere, with no agent judgement standing between it and the repository. That is the trade taken deliberately: a mistake in one testable place beats the same mistake distributed across prose nobody can diff.
