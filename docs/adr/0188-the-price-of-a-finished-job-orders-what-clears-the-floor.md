# The price of a finished job orders what clears the floor

This record amends [ADR-0184](0184-the-cheapest-point-that-will-finish-and-one-dimension-explored-at-a-time.md) on one point: what orders the candidates that clear the floor. ADR-0184 ordered them on the price of one attempt, or on one attempt's elapsed time under `--objective=time`. They are now ordered on that figure divided by the chance of success. The floor still decides which candidates are eligible, and [ADR-0187](0187-a-point-measured-for-the-kind-is-chosen-before-one-only-estimated.md)'s preference for points measured for the kind still stands. ADR-0184 stands as written and describes the design at its own date. What the rule now is is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own shipped files. This record argues the case.

## What the old order missed

**A point that fails is paid for again.** A point at 0.5 needs two attempts on average, and a point at 0.82 needs about 1.22. The per-attempt price leaves that out, so it prices a job as if every attempt finished it. What the user pays for is the finished job. A cheap run that stops, or has to be redone, is the expensive one. In the maintainer's experience a dearer model that is right the first time often costs less in total than a cheap one run again and again.

**Two points that both clear the floor show the gap.** In one shape the suite now holds, `claude-opus-5` at `low` finishes about 0.82 of the time and `medium` about 0.98. `medium` costs about 1.14 times as much per attempt and takes about 1.11 times as long. Both clear the floor, so neither is a lower chance bought with price. Per attempt, `low` is cheaper on both counts. Per finished job, `medium` is cheaper on both: 1.14 ÷ 0.98 × 0.82 ≈ 0.95 of the money, and about 0.93 of the time. The old order answered `low`, and the user paid for the retries.

## The rule

**Among the candidates that clear the floor, the order is on price divided by the chance of success.** Under `--objective=time`, it is one attempt's elapsed time divided by that chance. The chance is the posterior mean that already decides eligibility. The same figure orders the plain answer, the step up, and the entries of `alternatives` that clear the floor. For the step up, it orders every likelier candidate, including the fallback with no floor where nothing measured clears it.

**The floor still gates.** No point below the floor is taken for being cheap. Among those above it the order is on price divided by the chance of success. Candidates below the floor keep their order on chance alone, as before, and a tie is still broken on the per-attempt price.

**Exploration keeps its per-attempt comparisons.** Exploration exists to try points the evidence may be undervaluing. If its candidates were judged on the evidence's own mean, a point that once scored badly would never be retried, and ADR-0184 explores precisely to prevent that. So what counts as cheaper than the answer, and the order in which candidates are drawn, stay per attempt.

**The answer carries the figure it ranked on.** `expected` gains `per_success_cost_usd` and `per_success_seconds` beside the per-attempt `cost_usd` and `seconds`, and each entry in `alternatives` carries the same two. Each is null where the figure it divides is null, and an inheriting answer carries both as null. Without them a reader could not see why a dearer point won.

## ADR-0184's argument against a ratio

ADR-0184 rejected a ratio because it traded chance against money at an exchange rate nobody had agreed to. That rate was a tuned constant, `failure_overhead_usd`, added to the price of every failure. This rule differs on the three points that argument turned on.

**No lower chance is ever bought with price.** The floor decides eligibility first, and the division only orders what cleared it. A point at 0.6 that costs a tenth as much is still never the answer while anything clears the floor. The old ratio had no floor in front of it, and that is what let a low enough price buy a lower chance of finishing.

**1 ÷ p is the expected number of attempts, not an exchange rate.** Dividing by the chance of success does not say what a point of success rate is worth in dollars. It counts how many attempts one finished job takes on average, and multiplies the price of one attempt by that count. The result is still a price, in the same unit, of the thing the user actually buys.

**No tuned constant enters.** The figure is built only from the per-attempt price, or elapsed time, and the posterior mean, and both are already in the answer. `failure_overhead_usd`, the floor on the divisor and the quantities derived from them stay gone. The posterior mean never reaches nought, so the division needs no guard. Nothing is left that could be adjusted until an answer comes out right.

## The alternatives

**Keep the per-attempt order.** Rejected. It chooses the point that looks cheaper and is dearer in the total the user pays.

**Bring back the expected-cost arithmetic ADR-0184 removed.** Rejected for the reasons ADR-0184 gives. It had a per-failure constant nothing could measure or correct, and no floor in front of it.

**Favour a deliberation level by rule.** The maintainer's hunch is that most models do best somewhere around `medium` to `high`. That is for the measurements to show, through the deliberation dimension ADR-0184 already explores, and a rule would only be a second guess placed in front of them.
