# A model with no rows for a kind is owed a Trial of three jobs at any price

This record settles what [ADR-0204](0204-a-measured-point-leads-every-answer-and-a-band-decides-where-none-clears-the-floor.md) left out. That record put every point measured for a Work Kind before every point that is not, and closed by saying that the rule shuts an unmeasured model out of every plain answer, that the exploration [ADR-0184](0184-the-cheapest-point-that-will-finish-and-one-dimension-explored-at-a-time.md) bounded is not a door, and that the door is this. The two ship in one release and neither is released without the other. ADR-0184 and ADR-0204 stand as written and describe the design at their own dates. What the rule now is is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own shipped files. This record argues the case.

## What the store showed

**Exploration only goes downhill, and the downhill is narrow.** `_below` admits an exploration candidate only where it is cheaper than the plain answer, so no route exists by which a dearer untested model is ever tried once any measured point clears the floor. For a cheaper one the odds are thin by construction: about one call in ten explores, a second coin gives the model dimension half of those, and the draw is then shared among every cheaper rival. Simulated over 200 000 calls against the live pool, a never-measured model in the middle of the cheaper pack received 0.40 % of calls — about 750 build calls for the three rows that make a point measured, and fewer in practice, since a first failure collapses its posterior. The full simulation is finding 3 of [`docs/research/model-selector-cross-family-cost-2026-09.md`](../research/model-selector-cross-family-cost-2026-09.md).

**With ADR-0204 in force the two failures compound.** The ranking now shuts an untested point out of every plain answer the pool holds a measured point for, and the exploration cannot reach a dearer one at all. A model that is in fact better and dearer than the incumbent therefore has no route to a single row, whatever it would have done. The evidence store stops being a record of what this machine has tried and becomes a record of what it tried first.

## The rule

**A model holding fewer than `ENOUGH` rows of its own for a Work Kind is given three reversible jobs of that kind, at whatever they cost.** `ENOUGH` is the constant `evidence.py` already uses to decide when a cell stops being pooled and starts being measured, and no second threshold is introduced. After those rows exist the model is judged on them like everything else.

**Only a model that could plausibly win is owed one.** The estimate of the point it would be tried at must have a posterior mean of at least the bound the band draws over the pool this call ranks — the same bound, drawn by the same helper, that ADR-0204 gives the ranking where no measured point clears the floor. A Trial tries a model that might be the answer; it is not spent confirming that a weak model is weak. Where the pool holds no measured candidate there is no bound and no Trial, the ranking already letting an untested point be the plain answer in that case.

**The candidates are the points of the pool the call ranks, and nothing wider.** That is what makes every filter on the pool a filter on the Trial for free: the scope, either lock, the Quota Guard and the deliberation ceiling have all already run, and the rule reads none of them. The answer's own model is never given a Trial, a point tried instead of the answer never being the answer.

**The point tried is that model's at the answer's own level, or at the nearest level it supports.** Those are the semantics an exploration of the model dimension already has, asked again rather than restated. No price caps it: `_below` is not consulted, and a point nothing can price is a candidate like any other.

**One model at a time per kind, settled from the same rows.** A model already holding a row for the kind is a Trial in progress and is taken first; where several are, or where none has a row yet, the model whose Trial point the ranked list reaches first is taken. That is a total order, so the choice is deterministic and needs no key of its own.

**While a Trial is owed, every reversible call of that kind is one.** The exploration's coin is not tossed at all until the store holds that model's three rows, so a Trial is three consecutive jobs rather than three calls in thirty. Where no Trial is owed the exploration is exactly what it was, and whether one is owed is settled before the generator is touched, so a call owing none draws precisely what it drew before.

**The answer says which it was.** `explored` already means *this call was spent on the boundary rather than on the answer*, so it carries `trial` beside the two dimension names it carried before, and the note says the call was a Trial, names the point being tried and says what the evidence would have chosen. That is the duty ADR-0184 gives the exploration note, for the reason it gives it: a reader who finds a model nothing has measured chosen has to be able to tell a deliberate Trial from a routing fault at a glance.

## Why the band, rather than every untested model

**Because without it the rule owes more Trials than a maintainer would ever sit through.** Measured against the maintainer's store on 2026-09-20, the unfiltered rule owed `implement` fifteen consecutive Trial builds on five models whose own priors put them between 17 % and 46 %, against a best measured bound of 65 %. With the band none of them is owed one, while `gpt-6-astra` on 2026-09-19, at a prior of 83 %, would have been — which is exactly the model ADR-0204 was written about. The band is the difference between a door and a hole in the wall.

**And because the band is already drawn.** It is the one helper ADR-0204's ranking asks, over the same pool, and asking it again here means there is one statement of *the evidence cannot tell these apart* rather than two that can drift.

## Why three jobs at any price, rather than a wider exploration or a lower floor

**Widening the exploration spends the same money on the wrong thing.** Raising `EXPLORATION`, or letting `_below` admit a dearer candidate, buys rows spread evenly over every untested point in the pool — which is how the 0.40 % figure arose in the first place. What makes a point judgeable is three rows in one cell, not thirty rows spread over ten cells, and a probability per call cannot concentrate. The Trial is not a bigger lottery; it is the decision to stop holding one for a model that has never been asked.

**Lowering the floor was rejected once already, for the reason it is rejected again.** ADR-0204 records it as a tuned constant moved until an answer came out right, and it fixes nothing here: at any floor there is a store in which an untested model is shut out of every plain answer and the exploration cannot reach it.

**Paying whatever it costs is the point rather than an oversight.** Three jobs is a bounded, one-off price — and it is only ever paid on reversible work, which has something standing behind it to catch a wrong answer. A price cap would reintroduce the exact defect: the models a cap excludes are the dear ones, and a dear model that is in fact better is precisely the case no other route reaches.

## Why the count comes from the store rather than from something that remembers

**Because a counter can disagree with the rows it counts.** How many Trial jobs a model has had is not a fact the selector needs to remember: the store's own rows answer it, through the `by_kind` group the estimator already computes for its forecast. A count exposed off that group is read from the same rows the estimate is read from, and no file can fall out of step with the ledger it describes.

**The count is honest rather than exact, and that is accepted.** A job whose row has not been filed yet — still being graded, or filed by one side only — does not count, and two calls in the same wave see the same rows, so a model can be given a fourth or a fifth job where calls overlap. The cost of overshooting is one extra reversible job. The cost of a counter file is a number that says three where the store says one, on the machine whose whole purpose is to be the record of what happened.

**`Estimate.n` is not that count and is not used for it.** It reports the size of the deepest non-empty group, so a model holding one row at the level being asked about and two elsewhere reports one, and a Trial counted off it would never end.

## The alternatives

**Leave ADR-0204's rule alone and let the exploration find untested models.** Rejected by the simulation above: 750 builds for three rows, and no route at all to a dearer model.

**Give every untested model a Trial.** Rejected by the replay above: fifteen consecutive builds on five models the prior itself put under half.

**Remember Trials in a state file of their own.** Rejected above. It adds a file that can disagree with the store, to avoid a cost measured in one extra reversible job.

**Make the Trial a flag, or a standing setting.** Rejected because it makes the collection's routing answer two different ways depending on something nobody reading the answer can see. There is one user-facing behaviour and one code path.

## What this leaves out

**Nothing here changes what a step up answers, what a lock does, or what high stakes gets.** `_explorable`'s three exclusions stand unchanged and a Trial asks them rather than restating them.

**Whether three is the right number is not settled by evidence.** It is `ENOUGH`, and it is reused rather than chosen, on the argument that the count at which this collection starts believing a cell is the count at which it should stop buying rows for one. If `ENOUGH` ever moves, this moves with it.
