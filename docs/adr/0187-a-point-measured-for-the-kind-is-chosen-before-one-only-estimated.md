# A point measured for the kind is chosen before one only estimated

This record amends [ADR-0184](0184-the-cheapest-point-that-will-finish-and-one-dimension-explored-at-a-time.md) on one point: which candidates the answer is chosen among. ADR-0184 ranked every candidate whose posterior mean clears the floor on price, whatever that mean rested on. That no longer holds wherever a candidate measured for the kind clears the floor. ADR-0184 stands as written and describes the design at its own date. What the rule now is is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own shipped files. This record argues the case.

## What the store showed

**An untried model was the answer every time, high stakes included.** On 2026-09-11, before the maintainer purged the short own-session rows that ADR-0186 stops writing, `selection.py --kind=analyze` answered `gpt-6-astra` at `low` at both stakes, with basis `prior` and zero runs, over 53 measured `analyze` rows. Exploration exists to try a point like that in about one reversible call in ten, and never at high stakes. Ranked on the means alone, that point was the answer on every call instead. After the purge the same question answers `claude-sonnet-5` at `high`, measured, so this case stopped reproducing. What changed was what the store held, not the rule, and a store holding different rows would bring the case back.

**A verdict carried over from another kind beat the evidence about this one.** `gpt-5.6-luna` has seven rows in the store, all `implement`, two of them passed. Locked to `implement` at `low`, its estimate is 0.183. Carried over to `mechanical` at `medium`, it is 0.918 with basis `pooled`, and it was the answer to `--kind=mechanical` over `claude-opus-5` at `high`, which has 17 measured `mechanical` rows averaging 0.941. `--kind=converse` answered Luna pooled as well. These figures hold both before and after the purge. The seven rows were builds of wording tickets filed as `implement` before issue #292, but the carry-over is the defect whatever the rows were. Pooling is how an unmeasured cell gets an estimate at all, and an estimate is not evidence that the point does the work.

**The rule already said what high stakes wants.** `docs/rules/routing.md` says a high-stakes request wants the best point the evidence knows of. A point the evidence has never seen doing this kind of work is not that, however good its mean looks.

## The rule

**Where any candidate measured for the kind clears the floor, the answer is chosen among those candidates alone.** "Measured" means what `evidence.py` already says: basis `measured`, meaning at least `ENOUGH` rows in the exact kind × model × deliberation cell. A model's rows at other levels do not make a new level measured, and rows of another kind do not make a point measured for this one. Among the measured candidates that clear the floor, the ordering in force decides: price by default, the clock under `--objective=time`. Only where none clears is the whole pool ranked as before.

**Nothing is filtered out.** The ranked list puts the measured candidates that clear the floor first, then every other candidate exactly as the rule before this one ordered it. `alternatives` and `--after` read the same list. An unmeasured point is therefore still offered among the alternatives, and a caller that ran one can still name it as the point that failed.

**Exploration is left as it is, and does the rest.** Whether a cheaper, unmeasured point would do is the question exploration exists to answer. It draws from the points cheaper than the answer by their posteriors, so an unmeasured point is still tried in about one reversible call in ten, and never at high stakes. A point tried often enough becomes measured, and from then on it competes on the same terms as the rest.

**The step up prefers measured points on the same terms.** Where a point measured for the kind is more likely to succeed than the failed one and clears the floor, the step is the cheapest such point. Otherwise the step follows the rule ADR-0184 gave it: the cheapest point with a higher mean, with no floor. After the step, the other higher-mean points follow in price order.

**The judge inherits the rule without code of its own.** `grade.py` asks `selection.py` for `--kind=review --stakes=high --harness=process`. Where this machine has measured a reviewer that clears the floor, the judge is therefore chosen among the measured reviewers.

## The alternatives

**Keep the rule as it was: the cheapest mean that clears the floor.** Rejected by the evidence above. It answers with an untested estimate on every call where that estimate is cheaper, at high stakes as well, and it leaves the step up and the judge exposed to the same carry-over.

**Rank on a lower confidence bound instead of the mean.** A bound falls as the rows behind a point fall, so an estimate with little behind it would usually lose to a measured point. It was rejected because it is harder to predict and harder to explain, for the same effect. Whether a point wins would turn on a quantile whose width the pooling pseudo-counts set. A reader could not tell from the answer why a point with the higher mean lost. And the floor would stop meaning a chance of finishing.

**Measured first, chosen.** It says in words a reader can check against the `basis` the answer already reports, and it changes nothing where the store has measured nothing.

## What this leaves out

**Where nothing measured for the kind clears the floor, an estimate still answers.** On the live store after this change, `--kind=mechanical` answers `claude-sonnet-5` at `xhigh`, measured. `--kind=converse` still answers `gpt-5.6-luna`, pooled, because the store holds a single `converse` row. No point is measured for that kind, so the whole pool is ranked as before, which is what the rule says to do. A kind with no measured point is corrected by exploration and by rows accruing, not by this record.
