---
name: model-selector
description: Derive routing context, route delegated execution, and observe externally judged routed attempts when another Skill requires Model Selector's public Interfaces. Do not use implicitly for recommend, setup, config, compare, capture, update, record, or status.
disable-model-invocation: false
argument-hint: "[recommend] [--decision=route|renew] [--budget=<amount>|--quality=<score>] [--data=<path>] [<workload>] | chart|compare [--decision=route|renew] [--data=<path>] <workload> | context|record [--data=<path>] <path> | route <path> | observe --artifact=<path> [--import] [--data=<path>] <path> | config [show|history] [--data=<path>] | config reset [--evidence] [--yes] [--data=<path>] | config add|edit|remove [--data=<path>] model|channel [<id>] | config policy [show|reset] [--data=<path>] [<cohort>] | update [--force] [--data=<path>] | setup|status [--data=<path>] [-- <instruction>]"
compatibility: Requires uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
  kntnt.integrations: "scripts/capture.py"
---

# model-selector

Configure the exact model versions and subscription/API channels available to one user, then select a Pareto-efficient model, effort and agent configuration for a workload, budget or quality floor without re-researching known releases.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md. `$LIBRARY` is `library/` under the Manager directory that contains the checker. If it is absent, tell the user to run `/kntnt update`, then stop.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop. If `--help` or `-h` immediately follows a recognized command path, print that path's page from the table below verbatim and stop before setup, reads, research, or writes.

| Command path | Manpage |
| --- | --- |
| `recommend` | `$HERE/help/recommend.md` |
| `context` | `$HERE/help/context.md` |
| `route` | `$HERE/help/route.md` |
| `chart` | `$HERE/help/chart.md` |
| `compare` | `$HERE/help/compare.md` |
| `setup` | `$HERE/help/setup.md` |
| `config` | `$HERE/help/config.md` |
| `config show` | `$HERE/help/config/show.md` |
| `config add` | `$HERE/help/config/add.md` |
| `config edit` | `$HERE/help/config/edit.md` |
| `config remove` | `$HERE/help/config/remove.md` |
| `config policy` | `$HERE/help/config/policy.md` |
| `config policy show` | `$HERE/help/config/policy/show.md` |
| `config policy reset` | `$HERE/help/config/policy/reset.md` |
| `config history` | `$HERE/help/config/history.md` |
| `config reset` | `$HERE/help/config/reset.md` |
| `update` | `$HERE/help/update.md` |
| `observe` | `$HERE/help/observe.md` |
| `record` | `$HERE/help/record.md` |
| `status` | `$HERE/help/status.md` |

## Arguments

| Invocation | Effect |
| --- | --- |
| `/model-selector setup` | Create or fully review the persisted model and access-channel profile. |
| `/model-selector config [show]` | Inspect the persisted profile. |
| `/model-selector config add model\|channel` | Add one model selection or access channel. |
| `/model-selector config edit model\|channel <id>` | Edit one model selection or access channel. |
| `/model-selector config remove model\|channel <id>` | Remove one model selection or access channel after confirmation. |
| `/model-selector config history\|reset` | Show configuration history, or reset the active configuration after confirmation. |
| `/model-selector config reset --evidence [--yes]` | Discard this machine's own measurement — the evidence ledger, its derived frontiers, the quota store, the Standing Policy override and its history, capture and the Usage Record store — after confirmation or `--yes`, keeping the profile and researched public facts. |
| `/model-selector config policy [show] [<cohort>]` | Show the Standing Policy each workload Cohort routes under, and what moved it. |
| `/model-selector config policy reset [<cohort>]` | Restore the shipped Standing Policy for one Cohort, or for every overridden Cohort, after confirmation. |
| `/model-selector [recommend] [<workload>]` | Recommend from stored evidence. Infer the current task only when the workload is omitted and unambiguous. |
| `/model-selector context <path>` | Derive a complete route artifact from stored selections and exact runtime facts, or wrap a frozen snapshot unchanged. |
| `/model-selector route <path>` | Resolve a structured request artifact into ordered exact launch decisions. |
| `/model-selector chart\|compare <workload>` | Show comparable frontier tables and plotting data. |
| `/model-selector update [--force]` | Revalidate due discovery, pricing, and benchmark indexes once. |
| `/model-selector observe --artifact=<path> [--import] <path>` | Turn completed routed attempts into a sanitized importable artifact in caller-owned scratch, and with `--import` file the machine-judged ones. |
| `/model-selector record <path>` | Validate and append unseen local run observations. |
| `/model-selector status` | Report the profile, evidence vintage, due sources, gaps, and capture's own health. |

`--data=<path>` is valid on every form except `route`, which reads no profile or evidence at all, and on `observe` without `--import`, which writes none; it overrides the default data directory. `--artifact=<path>` and `--import` are valid only for `observe`, the first required and naming the caller-owned file the observations are written into, the second asked for by a routed caller that wants what it may file filed. `--decision=route|renew` is valid for `recommend`, `chart`, and `compare`; `route` is the default. `--budget=<amount>` and `--quality=<score>` are valid only for `recommend` and are mutually exclusive. `--force` is valid only for `update`. `--evidence` is valid only for `config reset`, discarding this machine's own measurement while keeping the profile and researched public facts. `--yes` is valid only combined with `--evidence` on `config reset`, and there answers that confirmation yes rather than asking; it is refused rather than ignored on every other form of this Skill, `config reset` bare included.

Anything outside these forms is invalid, an operand written before a flag among them. Where the invocation starts with a recognized command path, name in one line what was wrong, print the `## SYNOPSIS` from that path's manpage in the Help table verbatim, point at `/model-selector <command-path> --help`, change nothing, and stop. With no recognized command path, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim and point at `/model-selector --help` for the page in full instead. A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing.

## Evidence first

Default data directory: `~/.kntnt/model-selector/`. A user-supplied `--data=<path>` wins. Read `config.json` and existing evidence before any research or recommendation.

When `config.json` is absent or invalid, read `$HERE/references/profile-management.md` and run first-use setup before any command that needs selections except `context` and `route`. Context derives the missing-profile state and Route follows its own inheritance and refusal rules; neither starts setup. Never install a bundled access combination as the user's configuration.

When no evidence ledger exists, use only the configured models covered by `$HERE/data/seed-evidence.jsonl` as dated seed priors. `recommend` reads applicable seed evidence without writing and may read applicable `capability_prior_seed` rows in place when no newer ledger record exists. Relevant matched measurements override capability priors, which choose only cold-start experiments and never supply numeric evidence or clear a quality floor. `update` initializes applicable ledger records, preserving retrieval dates and sources. Never present the seed as current after its stated date.

One point means `model version × effort/thinking × harness × tools × policy × access channel × price or subscription schedule`. Never compare or recommend a bare model family.

`--decision=route` is the default and answers which already-owned channel to use now. `--decision=renew` evaluates whether a monthly subscription earns its fixed fee. `--budget=<amount>` selects best conservative quality within a budget only when all eligible points share that cost unit. `--quality=<score>` selects the lowest conservative cost clearing the floor. Keep USD, rolling-window quota, weekly quota and subscription credits separate unless the user supplies an explicit shadow price.

## Setup and config

Read `$HERE/references/profile-management.md`. Setup is mandatory on first use and persistent thereafter. `setup` performs a complete guided review; `config` applies the requested inspection or narrow revision. Ask one question at a time, preserve unambiguous input already given, show the resulting profile before writing and keep evidence history independent from configuration membership.

Complete when every enabled pinned release or explicitly accepted mutable alias points to a valid subscription, direct API, gateway API or other access channel, and the saved revision can be inspected without repeating the interview.

`config reset --evidence` discards what this machine measured and keeps what it researched and what the user configured. Under the selected data directory it removes exactly seven paths: `run-observations.jsonl`, `derived-frontiers.json` and `quota-observations.jsonl`, owned by the Collection Library's `routed_observations.py` and reached through `uv run "$HERE/scripts/observations.py" purge`; `standing-policy.json` and `standing-policy-history.jsonl`, owned by `$LIBRARY/scripts/standing_policy.py` and reached through `uv run "$LIBRARY/scripts/standing_policy.py" purge`; and the whole `capture/` subdirectory and `usage-records.jsonl`, owned by this Skill's own `scripts/capture.py` and reached through `uv run "$HERE/scripts/capture.py" purge`. Every other file `$HERE/references/evidence-ledger.md`'s `## Store` table names is untouched, and so are `config.json` and its history.

Run each of the three `purge --data=<directory>` commands once, without `--yes`, to render the exact paths this data directory holds and each one's row or byte count; a path the directory does not hold is reported as absent rather than as an error, and a purge preview is a success, unlike an unconfirmed `policy reset`. Show that combined preview and obtain confirmation the way every destructive configuration act does, or read it from a supplied `--yes` for an unattended run. A declined confirmation writes nothing. Confirmed, run the same three commands again with `--yes --data=<directory>` and report what went, per path, by count of rows or bytes, exactly as the preview named it — nothing here is migrated, backfilled or reinterpreted. Removing `capture/` clears its in-flight drafts; the Harness hooks stay installed and keep measuring, and the next session capture recreates whatever it needs. `config policy reset` is unchanged and stays the narrower act, restoring one Cohort's shipped default and keeping its own history; this is the wider one.

## Standing policy

Read `$HERE/references/profile-management.md`. The Standing Policy is where one workload Cohort starts on the Rung ladder and the inclusive floor and ceiling routing stays between. It ships working and has no `set`: a Cohort moves only upward, only when measured failures trip its threshold, and only a reset moves it back. It is script-owned state beside `config.json`, never hand-edited, and the profile's `config.lock` protocol does not apply to it.

Run `uv run "$LIBRARY/scripts/standing_policy.py" policy show --data=<directory> [<cohort>]` for `config policy [show]` and render its JSON: the effective starting Rung, floor, ceiling, failure threshold, and exploration budget, plus the rows that moved the Cohort with the run keys behind each. Where `store_damaged` is true, say so first: routing still has a complete policy, because the shipped default is one, but every Cohort that had moved is back at its cold start until the file is repaired or reset. Say for each shipped symbolic value — `cold_start`, `weakest_enabled`, `main_seat` — that it resolves per request against that request's own candidate ladder. `show` never writes.

For `config policy reset [<cohort>]`, show the exact store path and every Cohort about to be restored, obtain confirmation the way every destructive configuration act does, then run the same script as `policy reset --yes --data=<directory> [<cohort>]` and report the Cohorts restored. A declined confirmation writes nothing. Evidence, derived frontiers, and the profile are untouched, and the restored default reaches the next frozen routing context rather than a run already under way.

## Recommend

Read `$HERE/references/pareto-selection.md`. Normalize the resolved profile, evidence, active Harness, exact main seat, workload, categorical workload requirements, overrides, adapter mappings, route/renew economics, and policy into the artifact contract in `$HERE/references/route-request.schema.json`, then obtain the decision through the `recommend()` Interface in `$HERE/scripts/route.py`. This is the same selection core as Route; never repeat hard filters, evidence classification, cost selection, or escalation as prose-only judgement. Render the returned detailed recommendation as follows:

1. Resolve workload stratum, surface/harness, quality metric, budget or quality floor, latency/safety/availability filters and evidence date. State any inferred value.
2. Select only enabled configured model versions, effort/serving modes and access channels. Prefer local production-shaped observations, then matched independent evaluations, then configuration-bearing first-party results; use prose tier claims only to choose experiments.
3. When matched measurements cannot choose the exact point, choose the weakest plausibly capable enabled model, then the lowest plausibly sufficient supported reasoning control. For reversible, objectively checked work, start there and escalate exactly one adjacent Rung only after externally verified failure — the next supported reasoning control on the same model, or the next enabled model up by capability where that scale is exhausted or the Harness carries the control. For high-consequence or irreversible work without a trustworthy external checker, choose the strongest plausible enabled configuration and refuse unsafe exploration.
4. Compute conservative workload quality and channel-appropriate cost per successful completed task. For a routing decision, keep marginal cash, quota burn and latency visible; for a renewal decision, allocate the monthly plan fee across successful work and compare the counterfactual. Build the relevant Pareto frontiers; do not optimize a naive quality/cost ratio or pretend that included usage has a token price.
5. Recommend one point, its nearest cheaper and stronger frontier neighbors, and any checkable cheap-first escalation policy supported by evidence. A routing policy is its own configuration, never free capability.
6. Report evidence source/version, uncertainty, exclusions and staleness. When evidence cannot support the requested comparison, say what is missing and propose the smallest discriminating evaluation instead of inventing a rank.

Start every recommendation with exactly one prominent, text-bearing status banner from the evidence classes in `$HERE/references/pareto-selection.md`. The banner words are the primary accessible signal. It reports the classification reason, confidence, the evidence still missing, and whether the selected point is an exploration start or a production recommendation.

Immediately after a blue or orange banner, emit a section titled `Snabbaste vägen till mätdata` using the frozen experiment-brief contract in `$HERE/references/pareto-selection.md`. `recommend` remains offline and read-only: it plans the experiment but performs no network request, evaluation, or write. Normal work executes the brief, and `record` imports its observation artifact; do not add or imply an experiment command.

After the banner and any experiment brief, emit a section titled `Observerad förbrukning` beside the recommendation and never merged into it: name the selected point and its frontier neighbors — the same points named above, and no wider pool — and, for each, resolve its own `model` and `portable_deliberation` and pass the ordered list through the `usage_by_seat()` Interface in `$HERE/scripts/usage_evidence.py` against the selected data directory. Only the `model` is matched on — no Seat resolves a portable deliberation — so report each returned figure exactly as it came back: the mean of each token category the Usage Record store actually holds for that model, the mean elapsed seconds, the Usage Record count and the earliest/latest instant behind them, and the deliberations those records carry, naming unresolved ones as unresolved. Two named points differing only in deliberation therefore report the same figures; say so rather than letting the repetition read as coincidence. State a figure no record supports as absent rather than as zero, and never let one feed the quality or cost figures above it — a Usage Record enters no frontier, clears no quality floor, breaks no tie, and chooses nothing; the recommendation above is made in full before this section is ever read.

Complete when the recommendation names an exact configuration and decision rule, every named alternative is comparable, the user can see why dominated candidates lost, and every named point's observed usage is reported or stated absent, per model and with the deliberations behind it named.

## Context

Read `$HERE/references/model-routing.md` and validate the input against `$HERE/references/context-request.schema.json`. Run `uv run "$HERE/scripts/context.py" [--data=<path>] <path>` and emit its JSON response without commentary. The runtime form reads the normalized profile, shipped seed, adapter templates, routing defaults, and the selected evidence ledger; specializes exact mappings from the caller-supplied Harness and main-seat facts; projects the ledger into `context.evidence.records`, so an attempt an external verdict judged reaches the next decision with nothing written by hand; and returns one complete route artifact. The snapshot form validates and returns the supplied frozen snapshot unchanged beside the current ordered requests. Context never enters setup and performs no network access, evaluation, research, or persistent write.

## Route

Read `$HERE/references/model-routing.md` and follow its public Model Routing Module exactly. Validate the complete artifact against `$HERE/references/route-request.schema.json`, run `uv run "$HERE/scripts/route.py" <path>`, and emit the helper's JSON response without commentary. A caller with runtime facts invokes Context first and passes its response directly to Route; Route never reconstructs derivation rules. Route never starts setup, performs no network access, evaluation, or research, and writes no configuration or evidence.

## Chart

Follow `recommend` through frontier construction without selecting one winner. For each comparable cohort, emit a compact table containing exact configuration, conservative quality, marginal USD per success, five-hour quota burn per success, weekly quota burn per success, allocated subscription USD per success and p90 latency. Add, for each row's own `model` and `portable_deliberation` resolved through the `usage_by_seat()` Interface in `$HERE/scripts/usage_evidence.py` — only the `model` is matched on, no Seat resolving a portable deliberation: the mean of each token category the Usage Record store holds for it, the mean elapsed seconds, the Usage Record count and vintage span behind them, and the deliberations those records carry, naming unresolved ones as unresolved. Two rows differing only in deliberation therefore carry the same figures. Use `null`, not zero, for unavailable metrics, the usage columns included — a Usage Record enters no frontier and chooses nothing, so it never feeds the quality or cost columns beside it. Then emit plotting-ready CSV in a fenced block, one column per figure the table carries. Produce a single mixed-channel x-axis only when the user supplied a shadow price; otherwise render separate cash, quota and renewal views and explain why they cannot honestly share one numeric x-axis.

## Update

Read `$HERE/references/evidence-ledger.md`. Run one bounded update pass:

1. Initialize a missing ledger with applicable evidence for configured selections. Merge applicable public seed records absent from an older ledger without replacing newer local evidence. The seed contains no user access profile, subscription entitlement or quota observation.
2. Revalidate only sources required by enabled selections and watched families that are due by configured cadence: provider model/release indexes, mutable first-party capability sources and commercial terms weekly by default; benchmark release indexes monthly by default. Refresh capability sources on the existing model/release-source cadence. `--force` checks each relevant mutable index once but still never refetches a known immutable model detail page.
3. Fetch detail pages only for newly discovered version keys. Append alias, price, subscription, quota, benchmark and deprecation changes as effective-dated records; preserve prior rows.
4. Generate fingerprints for missing configuration observations. Never rerun an existing run key; never trigger evaluation from a price-only change.
5. Reprice stored usage separately from historical billed cost, rebuild affected configured frontiers and report exactly what changed. A discovered newer family version is reported but remains excluded until the user adds it alongside the old selection or replaces the old version through `config edit`.

For a changed first-party capability claim or normalized tag set, append changed capability-prior records without rewriting history. Keep every such row explicitly low-confidence and categorical.

No source changed is a successful update. Complete when every due source has a recorded check outcome and every discovered change is appended or explicitly marked provisional.

## Observe

Read `$HERE/references/run-observations.md` and follow it exactly. Run `uv run "$HERE/scripts/observations.py" observe --artifact=<path> [--import] [--data=<directory>] <path>` and emit the helper's JSON response without commentary. The attempts come from the caller that routed the work; this Skill re-resolves no model, no deliberation control and no evidence, and adds nothing the attempt did not establish. Observe is offline and starts no setup, research or evaluation, and writes no profile. Without `--import` it writes the artifact and nothing else, which is the form a user runs by hand. With `--import` it also files the machine-judged observations through the shared Collection Library's `record`, writing the evidence ledger and only the affected derived frontiers under the selected data directory, and evaluating the Standing Policy of every Cohort that import touched; a routed caller that wants its evidence filed asks for that by name, and Orchestrate reaches the same Library directly at its own verdict. Report the artifact path, what became importable, what was skipped as identical, what conflicted and every refused attempt with its stable code, then the import account where one was asked for: imported, identically skipped, conflicting and refused identities, and each touched Cohort's Standing Policy answer. A ledger refusal is reported and stops nothing. Never present an unjudged, self-graded or interrupted attempt as importable evidence.

## Capture

Read `$HERE/references/run-capture.md` and follow it exactly. Capture follows this Skill's own Enabled state and asks for nothing beyond it: the Manager installs this feature's owned lifecycle integration into every supported Detected Harness of the Global layer the moment the Skill is Enabled, placed, or refreshed, and removes every entry the moment it is Disabled — the same seams that already place and remove this Skill's own files, and no third step is ever asked for. A Project-layer Enable installs no integration, because an owned entry is keyed by owner inside a Harness's own configuration and a Global and a Project Enable of the same Skill would write and remove one another's single entry.

Capture is offline and performs no research or evaluation. It writes the capture store and, at a session's end, one Usage Record per Seat it ran on to its own store beside the evidence ledger; it never writes that ledger, never rebuilds a derived frontier, and changes no profile and no configuration. Ordinary work is measured and never judged: nothing here establishes an outcome, nothing waits for a human, and a Usage Record carries no checker, no condition, and no Cohort. Present a Usage Record as what one session cost on one Seat and nothing more.

Accepted Usage Records survive Disabling the Skill; a purge of captured data is a separate act the user has to ask for by name (`config reset --evidence`). `status` reports capture's own health.

## Record

Read `$HERE/references/evidence-ledger.md` and `$HERE/references/run-observations.md`. Run `uv run "$HERE/scripts/observations.py" record --data=<directory> <path>` and render its report. It validates provenance, configuration fingerprint, benchmark key, token categories, cost, outcome and timestamps for every supplied observation, appends only unseen run keys, skips identical duplicates, rejects conflicting duplicates rather than overwriting them, and rebuilds only the derived frontiers whose eligible run set changed, each named by its benchmark key, stage, workload cohort and workload tags. This command is the user-owned ledger mutation; Orchestrate calls the shared Library's same `record` implementation directly for eligible machine-judged attempts, never this command. The same call evaluates each touched Cohort's Standing Policy failure threshold and may ratchet its starting Rung one step up, never down. Report accepted, skipped and rejected records, then the `standing_policy` outcome of every touched Cohort: a `moved` Cohort by its from and to Rung, the failures out of the rows in its window against the threshold behind them, and `/model-selector config policy reset <cohort>` as the narrower way back — restoring the shipped default and keeping the history — with `config reset --evidence` as the wider one, discarding the measurement the movement rests on and the history with it; `standing_policy_ceiling_reached`, `stale_policy_context` and `below_threshold` are stated as they came.

## Status

Read `config.json` and ledger metadata only. Report the active revision and source cadences against the current date, but perform no network requests, writes or evaluations. Distinguish stale mutable sources from immutable model detail records that intentionally have no refresh date.

Also run `uv run "$HERE/scripts/capture.py" status --data=<directory>` and render its report as capture's own health section: adapter presence per Harness this collection has an adapter for (`healthy`, `gated`, `degraded`, `absent`, or `unsatisfied`), whether that Harness's own finished session record can supply measurements at all, and how many bytes the capture store holds. This performs no network request and writes nothing.
