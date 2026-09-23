# A newer release inherits the record of its family's older releases

This record settles what [ADR-0208](0208-only-the-newest-release-of-a-family-is-a-candidate.md) accepted as its cost and [ADR-0207](0207-a-model-with-no-rows-for-a-kind-is-owed-a-trial-of-three-jobs-at-any-price.md) was supposed to pay for: what a newer release of a model family is estimated from before it holds rows of its own. It also narrows [ADR-0192](0192-a-model-its-maker-stops-listing-is-removed-with-its-measurement.md), whose deletion of a removed model's rows rested on a premise the maintainer has now replaced. Those three records stand as written and describe the design at their own dates. What the rules now are is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own shipped files. This record argues the case (issues #418 and #419).

## What the store showed

**Four releases arrived in two days and the ranking lost a family.** The catalogue pass admitted `grok-4.7` on 2026-09-22 and `claude-opus-5-5`, `gpt-6-sol` and `gpt-6-luna` on 2026-09-23. Under ADR-0208 each of them retired the release before it — `grok-4.6`, `claude-opus-5`, `gpt-5.6-sol`, `gpt-5.6-luna` — from every pool. None of the four carried a capability, that being a seeded prior no pass fetches, so each was estimated at `UNKNOWN_CAPABILITY`, a coin flip: on `implement` all four stood at a 19.8 % chance of finishing, level with `gpt-5.5`, and on `prose` at 43 %. No Trial was owed to any of them, a Trial going only to a model whose point is at least as likely to finish as the bound around the best measured one, and the Trial that day went to `gpt-6-astra`, whose seeded prior is 0.90.

**The evidence the machine had was about the release it could no longer choose.** The store held 997 rows, 686 of them for `claude-opus-5`, 27 for `gpt-5.6-sol` and one for `grok-4.6`. ADR-0208 says those rows change nothing once the release is out of the pool, and that was the design: *the evidence about `grok-4.5` is evidence about `grok-4.5`*. So the machine that had measured Opus more than any other model answered as though it had never heard of Opus, and would have gone on doing so, because the door ADR-0207 built opens only for a model that already looks plausible.

**And the rows were three days from deletion.** Claude Code's list of 2026-09-23 no longer carried `claude-opus-5`, so ADR-0192's rule would have removed it on the third absent day and deleted the 686 rows with it — the whole of what this machine knew about the family, two days after the family's newest release had arrived with nothing.

## The premise

**A newer release of a family is at least as good as the release before it.** That is the maintainer's ruling of 2026-09-23, and it is what this record rests on: Opus 5.5 is not a stranger to Opus 5, and Fable 5.1 is not a stranger to Fable 5. A maker replaces a release with one it holds to be better, and the cases where that fails are what the newer release's own rows will show. So the older release's record is the right starting point for the newer one — a floor to grow from rather than a verdict — and the newer release's own measurements are what move it from there.

ADR-0192 rested on the opposite premise for the rows: *a model which has left its maker's list does not come back, so its rows are worth nothing to a selection that can no longer choose it*. That premise was true of the model and is no longer true of the rows. Where a newer release of the family stands, the rows are worth exactly what the newer release inherits from them.

## The rule

**Kin is the catalogue's own family, ordered as ADR-0208 orders it.** The older releases of a model are the releases of the same family — the `family` field, compared case-insensitively — that `catalogue.newest_first` places after it. Nothing infers a succession the catalogue does not state, for the reason ADR-0208 gives: `gpt-6-astra` inherits nothing from `gpt-5.6-sol`, and `gpt-5.5`, a family of one, inherits nothing at all. A release the lifecycle removed is kin still, its family and its release date kept in its lifecycle record from the day it went; rows are never given a family of their own and never rewritten.

**At every level of the estimate the kin's rows enter as a bounded prior, and the release's own rows enter whole.** The hierarchy of `evidence.py` is unchanged: sigmoid, then the model over its other kinds, then the kind over its other levels, then the exact cell, each a Beta posterior shrunk toward the level above by `PSEUDO`. What changes is what each level is fitted on. Beside the release's own rows, the same partition of its older kin's rows enters with a total weight of `INHERITED`, twice `ENOUGH`, spread evenly over them — six attempts' worth, however many rows there are — and their conditions are averaged into the level's translation at the same weight. A parent is still fitted only on what its child does not hold, for kin rows as for own. Where the release holds no rows, its answer is its kin's, shrunk as any pooled answer is; where it holds a Trial's three, they are a third of the cell; where it holds a dozen, they lead.

**A release with no seeded capability stands at its newest older kin's.** The bottom of the hierarchy is capability against difficulty, and a release the pass admitted before a release of the seed named it would otherwise start from the coin flip above. The value is read in the estimator, never written into the catalogue: a figure the pass wrote into `catalogue.json` would outrank the seed's own later word, since a refreshed entry carrying a capability keeps it.

**What an attempt costs is borrowed from kin one step behind own rows at each tier.** The token and runtime forecasts back off through the kind's rows and then the model's; each of those tiers now answers from the release's own rows where it has any, else from its kin's, before falling to the tier above and then to the kind's shipped prior. The narrowing to routed rows applies to a kin group exactly as to an own one.

**`basis` says `family` where the answer rests on kin and on nothing of the release's own.** `measured` and `pooled` mean what they meant — enough rows of the release's own in the exact cell, or in the kind or the model — and `family` replaces `prior` alone: it is the word for a point whose numbers come from the record of an older release. Everything that reads `measured` reads it unchanged: the ranking of ADR-0204 puts no inherited point before a measured one, and the Trial of ADR-0207 is counted off the release's own rows, so a newcomer with a strong inheritance is owed one on its first call and is judged on its own record after three.

**A removed release's rows stay while a newer release of its family stands in the catalogue.** ADR-0192 removes the model as before: its entry goes, its mask is written, its definitions are resynced. Its rows and its waiting Units are deleted only where the removal leaves the family with no release in the catalogue; otherwise they stay as the newer release's inheritance, the removal is journalled with the release that inherits them and counts of nought, and a later pass that finds the family gone deletes them then. A record written before this rule, carrying no family, is deleted as before.

## Why a bounded weight rather than the rows whole

**Six hundred rows would never be outgrown.** Folded in whole, the predecessor's 686 rows would hold the successor's estimate wherever the predecessor stood for hundreds of calls, and a successor that turned out worse — the case the premise admits — would be found out only after its own record was as long. Six attempts' worth is the parent weight of the exact cell restated: enough that a release with nothing of its own answers from its kin rather than from a sigmoid, and few enough that a Trial's three rows are already a third of the cell and a dozen rows lead.

**A single constant, tied to one that exists.** `INHERITED` is twice `ENOUGH`, the count that makes a cell measured, and it is one number at every level rather than a table beside `PSEUDO`. That is a tuned constant of the same kind as `PSEUDO`, and it is argued for the same way: it decides how quickly own evidence outgrows a prior, not which point wins.

## Why the rows are inherited rather than relabelled

**A row is evidence of a version that does not change.** The quick fix was to rewrite the store, attributing the predecessor's rows to the successor. It was rejected because the ledger would then say that Opus 5.5 did work Opus 5 did, which no reader could later undo; because it would have to be done again by hand at every release, on every machine, which is the silent inertness this Skill exists not to have; and because the same premise applied at the estimate needs no lie in the ledger to hold. The rows keep their model, and the successor reads them as its inheritance.

**And the predecessor's posterior was not taken as the successor's prior either.** Handing each level of the successor's stack the predecessor's posterior at that level would cut the successor's own chain: what it measured on other kinds would no longer inform this one while it was young. Entering the kin rows into the successor's own fit keeps both — the inheritance and the chain — with one arithmetic.

## Why the rows survive the removal

**ADR-0192's own reason no longer holds for them.** It deleted the rows because nothing could be chosen on their strength. With this record something can, so keeping them is that decision's reasoning applied to a changed fact rather than a reversal of it. Where the family goes altogether, nothing inherits and the rows go as before.

**Keeping them costs a file that grows with use and nothing else.** A removed release is out of every pool under ADR-0208, so its rows shape no ranking except through the release that inherits them, which is the point.

## What it never does

**It never counts kin rows as the release's own.** No inherited point is `measured`, no Trial is satisfied by kin, and `Estimate.n` goes on counting the release's own rows.

**It never flows from a newer release to an older one.** A lock to `claude-opus-5` by its exact id is answered from Opus 5's rows and nothing later.

**It never rewrites a row, a catalogue entry or a lock.** The store is appended to as before, the catalogue's `capability` is written by the seed and by nothing here, and the locks of ADR-0182 run before any of this.

## The alternatives

**Do nothing and let the Trial find the newcomer.** Rejected by the store above: a newcomer at the coin flip is never plausible enough to be owed one on hard work, so the door ADR-0207 built stays shut for exactly the model it was built for.

**Hand-edit the seed's capability at every release.** Necessary for what the seed claims and done for these four, but rejected as the mechanism: it repairs only the sigmoid, the weakest level of the stack, and only on the day somebody edits a file.

**Relabel the rows.** Rejected above.

**Keep every removed model's rows, always.** Rejected, because the maintainer's premise of ADR-0192 still holds for a family that leaves altogether, and rows nothing can inherit are the rows that decision was about.

## What this leaves out

**Succession across families is still not inferred.** Whether Astra follows Sol is a fact no structured source states, and ADR-0208's reasons for not keeping such a table by hand stand.

**A removed kin's capability is not kept.** The lifecycle record carries its family and its date, which is what inheritance needs; a release with no seeded capability and no older kin left in the catalogue stands at the coin flip until a release of the seed names it, at the sigmoid level only, where its inherited rows outweigh that at once.
