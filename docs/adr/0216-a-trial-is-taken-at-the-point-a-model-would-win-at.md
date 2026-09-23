# A Trial is taken at the point a model would win at

This record narrows [ADR-0207](0207-a-model-with-no-rows-for-a-kind-is-owed-a-trial-of-three-jobs-at-any-price.md) on one question: which of a model's points its Trial is taken at. ADR-0207 said *the answer's own level, or the nearest level it supports*, and [ADR-0215](0215-a-newer-release-inherits-the-record-of-its-familys-older-releases.md) closed by recording that this left a newcomer untried on exactly the store the inheritance was written for. Both records stand as written and describe the design at their own dates, and ADR-0184's exploration is untouched. What the rule now is is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own shipped files. This record argues the case (issue #420).

## What the store showed

**The inheritance arrived and the door stayed shut.** On the maintainer's store of 2026-09-23, `claude-opus-5` held 235 `implement` rows at `high` and one at `medium`. Under ADR-0215 its successor `claude-opus-5-5`, with no row of its own, read 0.773 at `high` and 0.578 at `medium`, both on basis `family`. The call `--kind=implement --harness=claude-code --seat=claude-fable-5-1@high` was answered with `claude-fable-5-1` at `medium`, the band drawn around Fable at `high` put its bound at about 0.61, and the Trial looked at Opus 5.5 at `medium` alone. That point was under the bound, so no Trial was owed, and Opus 5.5's point at `high`, clear of the bound by sixteen points, was never asked about.

**The one point looked at was the family's thinnest.** A family's record is measured wherever its older releases were run, and this family had been run at `high`. The answer's level is a fact about a different model's record: Fable's measurements put the answer at `medium`, and nothing about Opus follows from that. So the rule read Opus at the level where Opus had the least behind it, and concluded from one row that the newcomer could not win.

## The ruling

**Among a model's points in the pool the call ranks, its Trial is taken at the one the ranked list reaches first among those whose posterior mean is at least the bound the band draws.** That is the maintainer's ruling of 2026-09-23. The point it names is the one the model would be the answer at if it were measured: the ranked list already orders a model's points as the ranking weighs them, so the first of them to clear the bound is where the model would actually compete.

## The rule

**A model is owed a Trial where any of its points clears the bound, and is tried at the first such point in ranked order.** A model none of whose points reaches the bound is owed nothing, which is ADR-0207's *a Trial tries a model that might be the answer* read along the whole ladder rather than at one rung of it.

**Everything else ADR-0207 settled stands.** The count is `ENOUGH` rows of the model's own for the kind, at every level, off the estimator's own `rows_for_kind`. The answer's own model is never a candidate. No band means no Trial. Among the models owed one, a model already holding a row for the kind is a Trial in progress and is taken first, and otherwise the model whose Trial point the ranked list reaches first — the same total order, now read off the point this rule names for each model. The note keeps its shape: the call was a Trial, the point tried is named, and what the evidence would have chosen is said.

**The candidates are still the points of the pool the call ranks, and nothing wider.** The scope, either lock, the Quota Guard and the deliberation ceiling narrow the pool before anything is ranked, so they narrow the Trial exactly as before and the rule reads none of them. A point above the ceiling is never tried, however plausible it would be: it is not in the list the rule looks along.

**No price caps the point tried.** It may cost more per job than the plain answer, and that is ADR-0207's *at whatever they cost* unchanged. What decides between one model's points is the order the ranking already gave them, and a point nothing can price is a candidate like any other.

## Why the answer's level was the wrong point

**It was borrowed from the exploration, where it is right.** ADR-0207 took the point tried as *the semantics an exploration of the model dimension already has, asked again rather than restated*. An exploration moves one dimension and must hold the other fixed, because a row that moved both says nothing about either; holding the level is the whole of that rule's purpose. A Trial holds nothing fixed. It is a point tried instead of the answer, and `TRIAL` was kept out of `DIMENSIONS` for that reason. Borrowing a constraint whose reason does not apply gave the Trial the exploration's level without the exploration's need for it.

**It became decisive once a family's record could be measured elsewhere.** ADR-0215 made a newer release inherit whatever its family measured, where it measured it, and a family measured almost wholly at one level gives its newest release one strong point and several thin ones. Nothing ties the answer's level to the strong one: the answer's level is read off another model's record, so where it falls on the newcomer's ladder is chance, and a Trial read there brings the newcomer in only when the chance falls right. On the store above it did not — which is the case ADR-0215 recorded as left to this question.

## The alternatives

**The answer's level, unless the family has no rows there.** It would not even have fixed the store above, Opus 5 holding one row at `medium`, which is not none; and with any threshold in place of *none* it is two rules where one does. A rule that asks where the answer runs, and then asks whether the family was measured there, and then asks where else to look, has to say what *else* means; the only answer that does not invent a preference is the ranked list, at which point the first two questions add nothing. It would also keep the borrowed constraint for models with no family at all, where it is just as unjustified and merely less often costly.

**The model's highest mean.** Rejected because it ignores what the point costs, and a Trial at a model's most expensive rung measures a point the ranking would not choose even if the Trial went well. The ranked list already weighs chance against price the way the answer does; taking its first plausible point means the three rows bought are rows about the point that would win.

**Leave it.** Rejected by the store above. The inheritance exists so that a newcomer is not a stranger, and a Trial that cannot reach the newcomer's strong point leaves it a stranger on every kind whose answer runs at a level its family did not use. The exploration beside it reaches the newcomer only at the answer's level and only where it is cheaper than the answer, which is the thin point again.

## What it never does

**It never changes the exploration's dimension rule.** `_alongside` stays exactly as it was, and an exploration of the model dimension still takes another model at the answer's level or the nearest it supports, because there the level is held for a reason.

**It never tries a point outside the pool.** The list it looks along is the one the call ranked, after every gate.

**It never satisfies a Trial with kin rows.** The count is the release's own rows for the kind, as ADR-0215 left it; a point that clears the bound on its family's record is owed its Trial, and the Trial ends on rows of its own.

## What this leaves out

**A Trial in progress may move level between calls.** Nothing is remembered between calls, so each call reads the model's first plausible point afresh, and the first row filed at one point moves every estimate of that model. A Trial can therefore take its three rows at more than one level. It already could: under ADR-0207 the point tried moved whenever the answer's level moved. The count ends the Trial either way, because it is kept over every level. Whether a Trial should instead stay at the level its first row was taken at is not settled here.

**What makes a cell measured, and the three-row count, are unchanged.** This record reads both and settles neither.
