# Pareto selection

Use this reference only for `recommend`.

## Comparable point

Configuration identity includes model version or resolved alias target, reasoning effort or thinking budget, serving mode, access channel, subscription or billing plan, agent harness and commit, prompts, tools, cache/context/retry/fallback policies, resource profile and effective commercial schedule. `ultra`, multi-agent orchestration, fast/priority serving and cheap-first escalation are separate configurations.

Compare performance only inside one workload stratum and benchmark definition. Benchmark name, version, task manifest, harness, grader, repeats and resource profile must match. Never splice provider-reported rows, independent runs or different benchmark versions onto one y-axis without an explicit versioned normalization. Missing evidence is unknown, not zero.

Apply hard filters first: model availability, context, modalities, data residency, safety, latency ceiling and surface support. A high general score cannot compensate for a failed constraint.

## Cold-start selection

When representative matched measurements do not determine the exact point, make the cold-start choice in two stages: choose the weakest plausibly capable enabled model, then choose the lowest plausibly sufficient supported reasoning control for that model. Judge plausibility categorically from task complexity, ambiguity, context demand, autonomy, tool use, reversibility, consequence of failure and objective checkability. This heuristic chooses an experiment; it does not manufacture a benchmark score, confidence interval, cost observation or Pareto point.

For objectively checkable, reversible work, begin at the lowest plausible complete configuration and escalate exactly one adjacent Rung only after failure is verified by an external checker or declared failure signal — the next supported reasoning control on the same model, or, where that scale is exhausted or the Harness carries the control, the next enabled model up by capability regardless of provider. Stop at the first rung whose conservative quality clears the declared floor. Compare the whole policy with always starting stronger by charging every failed attempt, checker run, retry, quota charge, cost and added latency.

For high-consequence or irreversible work without a trustworthy external checker, select the strongest plausible enabled configuration and refuse unsafe exploration. An *exploration start* here is a cold-start classification of a point nothing has measured, and is a different thing from the Exploration Attempt `route` places one Rung below a Cohort's production Rung on a budget. Keep that point classified as heuristic unless representative matched evidence supports the exact configuration.

## Evidence class and output

Start every recommendation with exactly one prominent, text-bearing status banner. Its words are the primary accessible signal; emoji color only reinforces it. State the classification reason, confidence, the evidence still missing, and whether the exact selected point is an exploration start or a production recommendation.

- `🔵 HEURISTISK STARTPUNKT`: Representative matched measurements are insufficient to choose the exact point; capability priors and workload traits determine it. Label the selected point as an exploration start.
- `🟠 BLANDAD EVIDENS`: Relevant measurements exist, but heuristic assumptions still determine a decision-relevant part of the exact choice or its neighboring frontier. Name those assumptions and label the point as an exploration start unless matched evidence separately supports it for production.
- `🟢 MÄTDATABASERAD REKOMMENDATION`: Representative matched measurements have enough confidence and decision-relevant coverage to determine the exact point, and its conservative quality bound clears the declared floor. Label it as a production recommendation. Capability prose never qualifies a point for this class.

Classification follows confidence, representativeness and decision-relevant coverage, never a fixed observation count. Relevant measured evidence overrides a capability prior, but only evidence matched to the exact configuration, harness, access channel and comparable workload cohort can take over its decision.

## Fastest path to measurements

Immediately after a blue or orange banner, emit a section titled `Snabbaste vägen till mätdata`. It is a frozen, agent-executable experiment brief, not a suggestion to be redesigned during the run. Include:

- the workload artifact, cohort, rubric, quality floor, and external checker or declared failure signal;
- the exact configuration fingerprints to measure — the launch point and, where the request reaches one, the comparable Rung above it, or, where no exact point was selected, the measured frontier and the launchable points beside it — changing only the intended model or reasoning control while every other identity field stays frozen;
- required quality, cost, quota, latency, failure, retry and provenance measurements, charging every failed attempt, checker run, retry and added latency;
- a bounded run budget and a confidence-based stopping rule rather than a fixed observation count;
- the observation artifact and import form accepted by `model-selector record`;
- a quota-efficient sequential plan that starts at the lowest listed point and, where the brief lists the Rung above it, escalates that one adjacent Rung — the next reasoning control on the same model, or the next enabled model up by capability where that scale is exhausted or the Harness carries the control — only after externally verified failure; and
- a time-efficient parallel plan in which isolated agents run the listed configurations against the same frozen task and checker.

Every point the brief lists is one the request can actually launch — the candidate pool its own hard filters, explicit locks and Cohort Standing Policy left. Where an exact point was selected, the step to the second is the same Rung routing escalates along, resolved by the same ladder rather than by a second reading of it. Where no exact point was selected, the brief lists the measured frontier first and fills the rest from that same pool, so its points are comparable evidence rather than an escalation pair, and neither their order nor the distance between them is a Rung. Where the request reaches no comparable point at all, because it pinned the deliberation, exhausted the ladder, or is bounded to the one point it starts on, the section still appears with that single point and both plans state plainly that there is nothing to compare it against; measuring it is what turns a heuristic starting point into evidence, and `record` accepts the resulting observation as it does any other.

`recommend` emits the brief but executes no work. The ordinary work path runs it, and `record` validates and imports the resulting observations.

## Observed usage

Use this section for `recommend`, `chart` and `compare` alike. A Usage Record is what one finished ordinary session cost and how long it took on one Seat — no verdict, no Cohort, no configuration fingerprint. It never chooses: it enters no frontier, clears no quality floor, breaks no tie, and never makes a point eligible that quality evidence excluded. The whole of the frontier above is built and ordered without it.

For `recommend`, emit a section titled `Observerad förbrukning`, beside the frontier and never merged into it, for exactly the points already named: the selected point and its frontier neighbors, and no wider pool. `chart` and `compare` instead carry the same figures as columns on their own existing table, for every point that table renders. Either way, resolve each named point's own `model` and `portable_deliberation` and pass the ordered list through the `usage_by_model()` Interface in `$HERE/scripts/usage_evidence.py` against the selected data directory.

The join is on `model` alone: no Seat capture writes resolves a portable deliberation, so joining on the pair would match nothing at all. Report, per point: the mean of each token category the Usage Record store actually holds for it, per record; the mean elapsed seconds per record; the count of Usage Records behind those means; the earliest and latest instant any of them names; and the deliberations those records carry, with unresolved ones named as unresolved. Two named points differing only in deliberation share a model, so they report the same figures — say which deliberations stand behind a figure rather than letting it pass as one Seat's. A mean is reported only where every contributing Usage Record carried that measurement — the same rule a chain's own observed cost mean already applies. State everything else as absent rather than as zero, exactly as an unmeasured quality or cost figure already is.

The same profile and ledger, with and without Usage Records, select the same point: this section is read only after `recommend`, `chart` and `compare` have already derived and ordered their own answer in full, and nothing it reports changes that answer.

## Metrics

Prefer objective local outcomes: hidden tests, repository tests, exact data checks or frozen blinded rubrics. For binary tasks report pass rate with Wilson or bootstrap 95% interval. For graded work retain rubric dimensions; use a composite only when its versioned weights express the workload's value.

Use conservative quality: lower 95% bound when observations permit; otherwise reported score minus its published uncertainty. Treat differences inside the larger reported interval, or inside three points when matched infrastructure uncertainty is unknown, as ties.

Use observed total cost, not token list price:

```text
request_cost = (
    uncached_input_tokens * input_rate
    + cache_read_tokens * cache_read_rate
    + cache_write_tokens * cache_write_rate
    + billed_output_tokens * output_rate
) / 1_000_000
+ tool_invocation_cost
+ sandbox_or_session_cost
+ serving_premium
```

Sum every turn, failure, retry and fallback. Prefer provider-returned billed cost when available. For binary retryable tasks, empirical cost per success is `sum(all attempt costs) / number of successful tasks`; report mean and p90 attempt cost separately. Apply provider long-context thresholds to the whole request as documented. Never compare raw token counts across provider tokenizers as a common unit of work.

## Access economics

Do not assign API token rates to subscription usage. Track every successful task with these separate costs:

```text
marginal_cash_per_success = sum(metered_request_costs + purchased_credit_costs) / successful_tasks
session_quota_burn_per_success = sum(before_after_session_percentage_points) / successful_tasks
weekly_quota_burn_per_success = sum(before_after_weekly_percentage_points) / successful_tasks
allocated_plan_cost_per_success = monthly_plan_fee * task_allocation_weight / sum(all_plan_task_allocation_weights)
```

Use actual dashboard deltas when available. If a provider exposes only a remaining percentage, record a timestamped before/after pair around the task. A documented messages-per-window range is a planning prior, never a measured task cost. Do not convert quota percentages to tokens.

Use one quota accounting basis per observation:

- `provider_charged_quota`: use the dashboard or provider-returned weighted usage as recorded; the provider has already applied the model multiplier.
- `reconstructed_raw_usage`: use raw usage and apply the applicable model multiplier once.

Apply model multipliers from the selected access channel only. For example, when a configured Claude plan records Fable at 2× and its other models at 1×, `100` raw units become `200` Fable quota units, while an observed dashboard charge of `200` remains `200`; it never becomes `400`. A subscription multiplier and a corresponding API list-price difference are relative-cost representations on separate channels, not cumulative adjustments. A provider-returned USD bill already reflects its rate and receives no quota multiplier.

For `--decision=route`, a subscription fee already paid for the current billing month is sunk. Included subscription work has zero marginal cash but may consume scarce quota; metered direct or gateway API work has positive marginal cash according to its effective schedule and consumes only the quota its configured channel actually declares. Compare quality, quota burn, marginal USD and latency as separate axes. If the user supplies a shadow price for one percentage point of each quota, compute `decision_cost = marginal_cash + session_burn * session_shadow_price + weekly_burn * weekly_shadow_price`; label it a scenario, not a bill.

For `--decision=renew`, report the actual monthly fee, successful tasks, allocated cost per success, quota exhaustion or unused capacity, and the counterfactual cost and quality if those tasks moved to the best remaining channel. A subscription earns renewal only from the tasks for which removing it would increase cash cost, reduce quality below the floor, increase latency beyond the ceiling, or exhaust another channel. Do not divide the monthly fee by a theoretical maximum message count.

Keep marginal USD, subscription credits, rolling-window quota, weekly quota and wall time separate unless the user supplies an explicit conversion. Taxes and credit-purchase fees belong to actual cash cost when known.

## Frontier

Configuration `A` dominates `B` only within a common cost basis: `A` costs no more and scores no lower, with at least one strict improvement. For mixed access channels, use multidimensional dominance across marginal cash, rolling quota, weekly quota and latency, or build one frontier per cost view. Remove dominated points after uncertainty and hard filters, then apply the requested rule:

- Budget: highest conservative quality with conservative cost `<= B`; ties go to lower cost, then lower p90 latency.
- Quality floor: lowest conservative cost with conservative quality `>= Q`; ties go to higher quality, then lower p90 latency.
- No threshold: apply the frozen objective. `cost_first` takes the lowest observed cash and breaks a tie on the lowest Time to Verified Pass; `time_first` reverses the two. Neither invents an exchange rate between the axes, so a frontier the applicable order cannot separate still recommends a small frontier experiment rather than an arbitrary ratio winner.
- Traffic mix: minimize weighted expected policy cost subject to every protected stratum's quality floor; never let easy traffic hide a failing hard tail.

Show p90 latency as a third metric. Report hardest-decile quality and cost beside the overall result when available.

## Objective

The standing objective is the cheapest configuration that holds quality, and the fastest one only where the run asked for it. It is frozen with the rest of the routing context, so every decision of one run is made under one objective and a resumed run cannot change it halfway.

Compare on observed means — what the configuration was measured to cost and to take — never on the price its mapping advertises. Cost is the whole policy: a chain's cash is every attempt it took to reach a pass, and its Time to Verified Pass is the run from the chain's first launch to the instant its first passing verdict landed, both charged to the configuration that finally passed. A chain no verdict passed contributes neither, because a censored attempt is not a fast free one.

A user's own declared shadow prices outrank the objective, being a tradeoff they stated and this reference has no better answer to. Where they cannot decide — a price missing, a dimension nothing measured, or two scenarios costing the same — the objective decides instead.

Where no surviving point exposes cash at all, which is what a subscription seat looks like from inside, `cost_first` orders by the Rung ladder, whose cheaper end is the cheaper configuration by construction. Where only some points expose it, nothing is ordered: a half-measured dimension is a gap in the ledger rather than a free point on the frontier.

## Escalation

For objectively checkable work, compare always-strong against cheap-first-then-strong. Charge the failed first attempt, retry, checker and added latency. Use an observed policy run when available; do not synthesize success probability by combining unrelated benchmark rows. Escalate on an external checker or declared failure signal, never the model's unsupported self-confidence.

Sweep one model's effort curve before proposing multi-model orchestration. Higher effort is not assumed to dominate: sampling and harness effects can make a lower setting tie or win.

## Downward probes

After a measured incumbent succeeds, propose an isolated probe of the adjacent lower point only when its matched evidence is missing or too uncertain, the result could change the relevant frontier or selected policy, and the task is representative, reversible and objectively checkable. The probe does not replace the production recommendation until its conservative quality bound clears the floor.

There is no fixed probe cadence; opportunity and expected decision value trigger the proposal. Otherwise keep routing production work to the measured incumbent.

## Recommendation shape

Return:

1. Exact winning configuration and rule that selected it.
2. Conservative quality, cost per successful task and p90 latency with units.
3. Nearest cheaper and stronger frontier neighbors.
4. Dominated named candidates and the point that dominates each.
5. Evidence cohort, vintage, uncertainty and missing coverage.
6. Smallest next evaluation that could change the decision.
7. Observed usage per named point, per model and never per Seat, beside this shape and never inside it: see `## Observed usage`.

Call a public benchmark result a prior, not a deployment guarantee. A decisive production recommendation requires representative local evidence.
