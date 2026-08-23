# Pareto selection

Use this reference only for `recommend`.

## Comparable point

Configuration identity includes model version or resolved alias target, reasoning effort or thinking budget, serving mode, access channel, subscription or billing plan, agent harness and commit, prompts, tools, cache/context/retry/fallback policies, resource profile and effective commercial schedule. `ultra`, multi-agent orchestration, fast/priority serving and cheap-first escalation are separate configurations.

Compare performance only inside one workload stratum and benchmark definition. Benchmark name, version, task manifest, harness, grader, repeats and resource profile must match. Never splice provider-reported rows, independent runs or different benchmark versions onto one y-axis without an explicit versioned normalization. Missing evidence is unknown, not zero.

Apply hard filters first: model availability, context, modalities, data residency, safety, latency ceiling and surface support. A high general score cannot compensate for a failed constraint.

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
- No threshold: show the frontier and choose its knee only when a workload owner supplied marginal value. Otherwise recommend a small frontier experiment, not an arbitrary ratio winner.
- Traffic mix: minimize weighted expected policy cost subject to every protected stratum's quality floor; never let easy traffic hide a failing hard tail.

Show p90 latency as a third metric. Report hardest-decile quality and cost beside the overall result when available.

## Escalation

For objectively checkable work, compare always-strong against cheap-first-then-strong. Charge the failed first attempt, retry, checker and added latency. Use an observed policy run when available; do not synthesize success probability by combining unrelated benchmark rows. Escalate on an external checker or declared failure signal, never the model's unsupported self-confidence.

Sweep one model's effort curve before proposing multi-model orchestration. Higher effort is not assumed to dominate: sampling and harness effects can make a lower setting tie or win.

## Recommendation shape

Return:

1. Exact winning configuration and rule that selected it.
2. Conservative quality, cost per successful task and p90 latency with units.
3. Nearest cheaper and stronger frontier neighbors.
4. Dominated named candidates and the point that dominates each.
5. Evidence cohort, vintage, uncertainty and missing coverage.
6. Smallest next evaluation that could change the decision.

Call a public benchmark result a prior, not a deployment guarantee. A decisive production recommendation requires representative local evidence.
