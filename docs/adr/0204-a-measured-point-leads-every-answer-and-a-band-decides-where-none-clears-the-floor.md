# A measured point leads every answer, and a band decides where none clears the floor

This record amends [ADR-0187](0187-a-point-measured-for-the-kind-is-chosen-before-one-only-estimated.md) on the scope of the measured-first preference, which that record held to the points clearing the floor, and [ADR-0184](0184-the-cheapest-point-that-will-finish-and-one-dimension-explored-at-a-time.md) on what happens where nothing clears the floor, which it answered with the likeliest point at any price. [ADR-0188](0188-the-price-of-a-finished-job-orders-what-clears-the-floor.md)'s ordering on price per finished job is untouched: it is still what orders the candidates price is allowed to order, and this record only narrows which candidates those are. All three stand as written and describe the design at their own dates. What the rule now is is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own shipped files. This record argues the case.

## What the store showed

**An estimate nobody had tested won a day of work by three thousandths of a seeded number.** On 2026-09-19, replayed against the maintainer's store as it stood at 597 rows, `selection.py --kind=implement` answered `gpt-6-astra` at `high` at 16.74 USD per finished job, basis `prior`, with no rows of its own, over `claude-opus-5` at `high` at 7.01 USD with 142. Astra cleared the floor and Opus did not, so the measured-first preference never engaged at all — ADR-0187 held it to the points clearing the floor, and there were none among the measured ones to prefer. Astra's 0.832 was arithmetic rather than evidence: `sigmoid(SHARPNESS × (capability + bonus − difficulty))`. Clearing 0.8 that way at `high` takes a seeded capability of at least 0.873, and `claude-opus-5` is seeded at 0.87. A number nobody measured, three thousandths from a threshold nobody calibrated, decided which model built a day of tickets.

**Where nothing clears the floor at all, price stops mattering.** ADR-0184 ranks such a pool on chance alone, which is all a pool that can promise nothing has to offer — but it means a dear untested point sits wherever its prior puts it. Replayed against the same store at 698 rows, where nothing cleared, `gpt-6-astra` at `xhigh` at 38.99 USD per finished job sat second, ahead of `claude-opus-5` at `high` at 8.21. The full replay and its alternatives table are in [`docs/research/model-selector-cross-family-cost-2026-09.md`](../research/model-selector-cross-family-cost-2026-09.md).

**Both cases are one defect.** ADR-0187 read the floor as the thing that made a point worth preferring, so it made the preference conditional on the floor. But the floor is a statement about a posterior mean, and a mean computed from a seeded capability is not the same claim as a mean computed from a hundred and forty-two attempts. The preference was for the kind of evidence, and it was written as a preference for a number.

## The rule

**Every point measured for the kind comes before every point that is not, whether or not anything clears the floor.** Measured means what `evidence.py` already says: basis `measured`, at least `ENOUGH` rows in the exact kind, model and deliberation cell. That is the whole of the first cut, and it does not consult the floor.

**Among the measured points, where any clears the floor nothing changes.** They are ordered on price per finished job, or on elapsed time per finished job under `--objective=time`, and the measured points below the floor follow on their chances. That is the behaviour in force before this record, and the floor keeps its whole meaning wherever the measurements reach it.

**Where none of them clears the floor, price orders only the band.** The band is the measured points whose posterior mean is at least the best measured point's `Estimate.low` — the tenth percentile the estimator already computes at `LOW_QUANTILE` — the best measured point being the one with the highest mean. The answer is the one of those with the lowest price per finished job, and the measured points outside the band follow on their chances. The band is never empty, the best point's own mean being at least its own bound.

**Where the pool holds no measured point at all, the rule before this one stands unchanged.** That is the pool rather than the store: the ranking is handed what the scope, a model lock, a deliberation lock and the deliberation ceiling have already left, so a store full of measured rows for models the pool does not hold still answers `prior`.

**The step up is asked the same way, over the points likelier than the one that failed.** The measured ones among those come first, ordered by the same two branches, and the band a step up draws is drawn over those points alone. Where none of the likelier points is measured, the step is what ADR-0184 gave it: the likelier point with the lowest price per finished job, with no floor.

**The answer says when the band decided it.** One line in `note`, naming the point the band was drawn around, written wherever that branch answered — a band of one included, and a step up included. It is the one case where a point below the floor is taken while something above it was on the table, and without the line a reader has no way to tell such an answer from an ordinary one. `basis` needs no new value: it already reports `measured`, and under this rule a plain answer reports it whenever the pool held a measured point.

**Nothing is tuned and no constant is added.** `FLOOR` keeps its value, the band is built from the uncertainty the estimator already carries, and the quantile it reads is the one `low` has always been reported at.

## Why not simply the cheapest measured point

**Because the cheapest junk in the pool wins.** Replayed measured-only with no band, the same question answers `gpt-5.6-luna` at `low`, posterior mean 0.18, at 1.16 USD per finished job. Dividing the price by the chance of success is a real correction — it counts the attempts a finished job takes — but it is a ratio, and a small enough price survives being divided by a small enough chance. The band is what puts a bar in front of that division: among the points the evidence cannot tell apart from the best one it holds, take the cheapest. It says nothing about points the evidence *can* tell apart, and it never lets one of those in on price.

## ADR-0187's rejected lower-bound alternative

ADR-0187 considered and rejected *"Rank on a lower confidence bound instead of the mean"*, on three counts: that whether a point won would turn on a quantile whose width the pooling pseudo-counts set, that a reader could not tell from the answer why a point with the higher mean lost, and that the floor would stop meaning a chance of finishing. That rejection does not stand against this rule, which differs on every one of those counts.

**The bound is read only where no measured point clears the floor.** On every other call it is not consulted at all, so the ordinary answer is decided by exactly what decided it before.

**The bound is drawn around the best measured point rather than becoming the ranking key.** Nothing is ranked on a lower bound here. The bound bounds a set; inside that set the order is the mean-driven price per finished job ADR-0188 settled, and outside it the order is on chance, as before.

**The floor keeps its whole meaning wherever a measured point clears it.** It goes on saying *is this good enough*, and it goes on deciding eligibility for every call the measurements can answer. What the band replaces is the fallback, where the floor had already stopped deciding anything.

**A reader can tell why a point with the higher mean lost, because the answer says so.** The note names the point the band was drawn around, and the two points' means and per-success figures are both in the answer. The 2026-09-19 defect was invisible for exactly the opposite reason: nothing in the answer said that a seeded capability had cleared a threshold and a hundred and forty-two rows had not.

## The alternatives

**Keep ADR-0187's rule as it stands.** Rejected by the replay above. It leaves the answer, the step up and the judge exposed to an untested estimate on every call the measurements fall short of the floor on, which on this store is most of them for the hardest kinds.

**Lower the floor.** Replayed at 0.7 it gives `claude-opus-5` at `high` on both snapshots, which is the answer wanted. It was rejected because it is a tuned constant moved until an answer came out right — the same fault ADR-0184 records `failure_overhead_usd` having — and because it fixes nothing about the preference: at any floor there is a store where nothing measured reaches it and an untested estimate does.

**Require an unmeasured point to clear the floor on its lower bound.** Replayed, `gpt-6-astra` at `xhigh` still wins on the first snapshot, through the fallback that ranks a pool clearing nothing on chance alone. It treats the symptom in one branch and leaves the other.

**Take the cheapest measured point outright.** Rejected above: mean 0.18 at 1.16 USD.

## What this leaves out

**An unmeasured model is now unreachable except through exploration, and that is not acceptable on its own.** This rule shuts a point with no rows for a kind out of every plain answer. The one-in-ten downhill exploration still reaches it, and was measured at about 750 build calls for the three rows that make a point measured — which is not a door. The door is the Trial, filed as issue #374: a model with no rows of its own for a kind gets three reversible jobs at whatever it costs. This record and that one ship in the same release, and neither is released without the other.
