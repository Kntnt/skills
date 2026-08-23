---
name: model-selector
description: Configure, compare, and update price-performance evidence for chosen AI model versions, effort levels, and subscription or API access channels.
disable-model-invocation: true
argument-hint: "[setup|config|recommend|chart|compare|update|record|status] [args] [--decision=route|renew] [--budget=<amount>] [--quality=<score>] [--force] [--data=<path>]"
metadata:
  kntnt.internal: "true"
  kntnt.binaries: ""
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# model-selector

Configure the exact model versions and subscription/API channels available to one user, then select a Pareto-efficient model, effort and agent configuration for a workload, budget or quality floor without re-researching known releases.

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

| Invocation | Effect |
| --- | --- |
| `/model-selector setup` | Create or fully review the persisted model and access-channel profile. |
| `/model-selector config [show]` | Inspect the persisted profile. |
| `/model-selector config add model\|channel` | Add one model selection or access channel. |
| `/model-selector config edit model\|channel <id>` | Edit one model selection or access channel. |
| `/model-selector config remove model\|channel <id>` | Remove one model selection or access channel after confirmation. |
| `/model-selector config history\|reset` | Show configuration history, or reset the active configuration after confirmation. |
| `/model-selector [recommend] [<workload>]` | Recommend from stored evidence. Infer the current task only when the workload is omitted and unambiguous. |
| `/model-selector chart\|compare <workload>` | Show comparable frontier tables and plotting data. |
| `/model-selector update [--force]` | Revalidate due discovery, pricing, and benchmark indexes once. |
| `/model-selector record <path>` | Validate and append unseen local run observations. |
| `/model-selector status` | Report the profile, evidence vintage, due sources, and gaps. |

`--data=<path>` is valid on every form and overrides the default data directory. `--decision=route|renew` is valid for `recommend`, `chart`, and `compare`; `route` is the default. `--budget=<amount>` and `--quality=<score>` are valid only for `recommend` and are mutually exclusive. `--force` is valid only for `update`.

Anything outside these forms is invalid. Name in one line what was wrong, print the `## Synopsis` section of `$HERE/help.md` verbatim, and point at `/model-selector --help` for the page in full. Change nothing and stop. A flag is refused rather than ignored where it has no work to do here (ADR-0059).

## Evidence first

Default data directory: `~/.model-selector/`. A user-supplied `--data=<path>` wins. Read `config.json` and existing evidence before any research or recommendation.

When `config.json` is absent or invalid, read `$HERE/references/profile-management.md` and run first-use setup before any command that needs selections. Never install a bundled access combination as the user's configuration.

When no evidence ledger exists, use only the configured models covered by `$HERE/data/seed-evidence.jsonl` as dated seed priors. `recommend` reads applicable seed evidence without writing; `update` initializes applicable ledger records, preserving retrieval dates and sources. Never present the seed as current after its stated date.

One point means `model version × effort/thinking × harness × tools × policy × access channel × price or subscription schedule`. Never compare or recommend a bare model family.

`--decision=route` is the default and answers which already-owned channel to use now. `--decision=renew` evaluates whether a monthly subscription earns its fixed fee. `--budget=<amount>` selects best conservative quality within a budget only when all eligible points share that cost unit. `--quality=<score>` selects the lowest conservative cost clearing the floor. Keep USD, rolling-window quota, weekly quota and subscription credits separate unless the user supplies an explicit shadow price.

## Setup and config

Read `$HERE/references/profile-management.md`. Setup is mandatory on first use and persistent thereafter. `setup` performs a complete guided review; `config` applies the requested inspection or narrow revision. Ask one question at a time, preserve unambiguous input already given, show the resulting profile before writing and keep evidence history independent from configuration membership.

Complete when every enabled pinned release or explicitly accepted mutable alias points to a valid subscription, direct API, gateway API or other access channel, and the saved revision can be inspected without repeating the interview.

## Recommend

Read `$HERE/references/pareto-selection.md`, then:

1. Resolve workload stratum, surface/harness, quality metric, budget or quality floor, latency/safety/availability filters and evidence date. State any inferred value.
2. Select only enabled configured model versions, effort/serving modes and access channels. Prefer local production-shaped observations, then matched independent evaluations, then configuration-bearing first-party results; use prose tier claims only to choose experiments.
3. Compute conservative workload quality and channel-appropriate cost per successful completed task. For a routing decision, keep marginal cash, quota burn and latency visible; for a renewal decision, allocate the monthly plan fee across successful work and compare the counterfactual. Build the relevant Pareto frontiers; do not optimize a naive quality/cost ratio or pretend that included usage has a token price.
4. Recommend one point, its nearest cheaper and stronger frontier neighbors, and any checkable cheap-first escalation policy supported by evidence. A routing policy is its own configuration, never free capability.
5. Report evidence source/version, uncertainty, exclusions and staleness. When evidence cannot support the requested comparison, say what is missing and propose the smallest discriminating evaluation instead of inventing a rank.

Complete when the recommendation names an exact configuration and decision rule, every named alternative is comparable, and the user can see why dominated candidates lost.

## Chart

Follow `recommend` through frontier construction without selecting one winner. For each comparable cohort, emit a compact table containing exact configuration, conservative quality, marginal USD per success, five-hour quota burn per success, weekly quota burn per success, allocated subscription USD per success and p90 latency. Use `null`, not zero, for unavailable metrics. Then emit plotting-ready CSV in a fenced block. Produce a single mixed-channel x-axis only when the user supplied a shadow price; otherwise render separate cash, quota and renewal views and explain why they cannot honestly share one numeric x-axis.

## Update

Read `$HERE/references/evidence-ledger.md`. Run one bounded update pass:

1. Initialize a missing ledger with applicable evidence for configured selections. Merge applicable public seed records absent from an older ledger without replacing newer local evidence. The seed contains no user access profile, subscription entitlement or quota observation.
2. Revalidate only sources required by enabled selections and watched families that are due by configured cadence: provider model/release indexes and commercial terms weekly by default; benchmark release indexes monthly by default. `--force` checks each relevant mutable index once but still never refetches a known immutable model detail page.
3. Fetch detail pages only for newly discovered version keys. Append alias, price, subscription, quota, benchmark and deprecation changes as effective-dated records; preserve prior rows.
4. Generate fingerprints for missing configuration observations. Never rerun an existing run key; never trigger evaluation from a price-only change.
5. Reprice stored usage separately from historical billed cost, rebuild affected configured frontiers and report exactly what changed. A discovered newer family version is reported but remains excluded until the user adds it alongside the old selection or replaces the old version through `config edit`.

No source changed is a successful update. Complete when every due source has a recorded check outcome and every discovered change is appended or explicitly marked provisional.

## Record

Read `$HERE/references/evidence-ledger.md`. Validate provenance, configuration fingerprint, benchmark key, token categories, cost, outcome and timestamps for every supplied observation. Append only unseen run keys; reject conflicting duplicates rather than overwriting them. Rebuild only affected frontiers and report accepted, skipped and rejected records.

## Status

Read `config.json` and ledger metadata only. Report the active revision and source cadences against the current date, but perform no network requests, writes or evaluations. Distinguish stale mutable sources from immutable model detail records that intentionally have no refresh date.
