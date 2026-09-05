# Evidence ledger

Use this reference only for `update` or `record`.

## Bundled seed

`$HERE/data/seed-evidence.jsonl` is a profile-neutral bootstrap snapshot. Its first row is `seed_manifest`; the remaining rows are `model_version_seed`, `model_reference_seed`, `capability_prior_seed`, `price_schedule_seed`, `benchmark_definition_seed` or `evaluation_prior_seed`. Every row has a stable `seed_id`, source, retrieval time and dated or provisional status. The file contains no access profile, subscription entitlement, account quota or local evaluation.

Read only rows whose model identities match enabled selections. `recommend` may consume applicable rows in place as dated priors without writing, including a `capability_prior_seed` when no newer applicable row exists in `capability-priors.jsonl`. During `update`, import unseen immutable model, benchmark and capability-prior records, materialize price schedules only for matching direct or gateway API channels, and map evaluation priors to their exact model configuration and benchmark. A `model_reference_seed` for a mutable alias remains provisional until resolution creates an `AliasBinding` and validated `ModelVersion`; its dependent prices and observations do not become decisive merely because they shipped in the seed.

Use `seed_id` for import idempotency and retain the original retrieval timestamp, status and sources. Newer ledger evidence supersedes an older seed row without deleting it. Revalidate mutable prices and benchmark indexes according to cadence; treat a bundled immutable `model_version_seed` as an already retrieved detail record and fetch its detail page again only if validation detects a conflicting identity.

## Store

Default directory: `~/.kntnt/model-selector/`.

The active profile and its revision history are defined in `profile-management.md`; the files below are evidence, not current user settings.

| File | Record type |
| --- | --- |
| `source-states.jsonl` | `SourceState` — mutable source check state and provenance. |
| `access-channel-snapshots.jsonl` | `AccessChannelSnapshot` — immutable commercial-channel identity used by observations. |
| `model-versions.jsonl` | `ModelVersion` — immutable validated model releases. |
| `alias-bindings.jsonl` | `AliasBinding` — effective-dated alias-to-version bindings. |
| `capability-priors.jsonl` | `CapabilityPrior` — append-only dated first-party qualitative capability claims. |
| `price-schedules.jsonl` | `PriceSchedule` — effective-dated rates, thresholds, tool fees and serving premiums. |
| `subscription-schedules.jsonl` | `SubscriptionSchedule` — effective-dated monthly fees, included surfaces, quota rules and credit fallback. |
| `access-mode-availability.jsonl` | `AccessModeAvailability` — effective-dated effort/thinking and serving-mode support per model and access surface. |
| `quota-observations.jsonl` | `QuotaObservation` — timestamped before/after session and weekly allowance readings. |
| `benchmark-definitions.jsonl` | `BenchmarkDefinition` — dataset, manifest, harness, grader, weights and resource identity. |
| `evaluation-configurations.jsonl` | `EvaluationConfiguration` — independent published benchmark scores for a model at a published configuration. |
| `run-observations.jsonl` | `RunObservation` — raw per-task attempt outcomes, usage, bill and latency. |
| `derived-frontiers.json` | No record type of its own — reproducible disposable summaries; safe to replace after source records are unchanged. |

Every record in `## Required records` is written to the one file named beside it above and to no other; the twelve record types and the twelve JSONL files correspond one to one. `derived-frontiers.json` is a summary rebuilt from those rows, so nothing appends a record to it.

`standing-policy.json` and `standing-policy-history.jsonl` sit in the same directory but belong to neither this reference nor the profile: they hold the Standing Policy each workload Cohort routes under, are written only by the Collection Library's own policy store, and are documented in `profile-management.md`. A movement of that policy is caused by measured evidence and names the run keys behind it, but it is not evidence and enters no frontier.

JSONL source records are append-only, with one exception named in the table above: `source-states.jsonl` is mutable check state rather than evidence, holds exactly one row per `source_key`, and is updated in place — nothing appends to it and nothing supersedes a row in it. Every other store here is append-only. Correct a bad row by appending a superseding row that names its predecessor; never edit history. Write through a temporary sibling and atomic rename when the host supports it. Restrict permissions to the user because prompts, paths and usage may be sensitive. Do not store response bodies or secrets; store artifact hashes and sanitized excerpts.

Every external fact needs source URI, retrieval timestamp, parser version and source content hash. Account-specific facts may instead cite the originating config profile/revision, user confirmation timestamp and record hash. Unproven facts are `provisional` and cannot select a winner.

## Keys

Normalize ordered objects before hashing. Preserve exact protected identifiers. `canonical_json` is compact JSON with object keys sorted — `json.dumps(value, sort_keys=True, separators=(",", ":"))` in the shipped idiom.

```text
source_key = sha256(uri)
model_version_key = sha256(provider | canonical_model_id | provider_release_id)
model_reference_key = sha256(provider | canonical_model_id | version_kind | provider_release_id_or_alias)
capability_prior_key = sha256(provider | model_version_or_reference_key | source_uri | effective_at_or_retrieved_at | normalized_tags | claim_hash)
access_channel_key = sha256(config_profile_id | channel_id | canonical_channel_content_hash)
price_schedule_key = sha256(provider | model_version_key | channel | region | effective_from | rate_card_hash)
subscription_schedule_key = sha256(access_channel_key | effective_from | terms_hash)
benchmark_key = sha256(benchmark_name | version | dataset_hash | harness_commit | grader_version)
configuration_hash = sha256(canonical_json(configuration))
evaluation_key = sha256(model_key | benchmark_key | configuration_hash)
config_fingerprint = sha256(model_version_key | access_channel_key | effort | thinking_budget | mode | harness_commit | prompt_hashes | toolset_hash | cache_policy | retry_policy | fallback_policy | resource_profile)
run_key = sha256(config_fingerprint | benchmark_key | task_id | seed | attempt_index)
```

OpenAI release slugs without an exposed dated snapshot use version kind `provider_release_slug`; preserve a more specific resolved ID if the response supplies one. Treat SpaceXAI production names as `mutable_alias` and history every resolved target change. Anthropic 4.6-and-later dateless IDs are `pinned_release`, not evergreen aliases. Create `ModelVersion` only for a validated release identity; keep an unresolved alias under `model_reference_key` and `AliasBinding` until it resolves.

## Required records

`SourceState`: `record_type`, always `SourceState`; `source_key`; `uri`, the source's address and the only input to its key; `provider`, the slug of the party the source belongs to — the model provider, the gateway or the independent evaluator that publishes it; `kind`, one of the six values below; `status`, one of the five below; `etag`, `last_modified` and `content_hash`; `last_checked_at`, the time the source was last looked at, whatever came of the look; `last_retrieved_at`, the time it was last actually retrieved, null on a source no pass has retrieved; `last_changed_at`, the time the content was last seen to differ, null where no change is recorded; `parser_version`, the parser that read the source; and `finding`.

`kind` says what the source is. The vocabulary is closed, and a row carries exactly one of these six:

| `kind` | What the source is |
| --- | --- |
| `model_release_index` | A provider's model list or release index. |
| `model_detail` | One model's first-party detail page. |
| `capability_source` | A first-party page making a qualitative capability claim. |
| `benchmark_release_index` | An independent evaluator's release index. |
| `commercial_terms` | A provider's pricing or subscription terms. |
| `gateway_rate_card` | A gateway's rate card. |

`status` says how the pass left the source, and it takes one of five values. `unchanged`, `changed`, `unreachable` and `invalid` are the four outcomes of a source that was due and retrieved; `not_due` is the fifth, and it is what a source gets that the pass considered and left alone because its cadence had not elapsed. A row therefore exists for every source the pass considered, not only for every source it retrieved.

The three timestamps are three different facts and only one of them schedules anything. **Cadence is measured from `last_retrieved_at` and from nothing else**, so a source whose `last_retrieved_at` is absent or null has never been retrieved and is due, whatever `last_checked_at` says. `last_checked_at` records that a pass considered the source — including one that found it not due and one that could not reach it — and moves no due date; measuring cadence from the look would push every source's next due date forward at every look and nothing would ever become due again.

`etag`, `last_modified` and `content_hash` are the validators conditional retrieval reads — the first two as the response offers them, the third a hash of the fetched content for a source that offers neither — and each may be null. `finding` is human-readable prose recording what the pass made of the source, and nothing parses it.

`AccessChannelSnapshot`: key, originating config profile/revision and channel ID, provider, surface or gateway, billing type, exact account plan/tier, region, currency, tax treatment, included-only or overage policy, actual recurring bill when supplied, source and valid interval. Snapshot a configured channel when evidence or observations first use it; later config changes create a new key and never rewrite prior observations.

`ModelVersion`: key, provider, canonical and provider release IDs, display family/name, release date, version semantics, modalities, context/output limits, supported controls, first-party source and discovery timestamp. Freeze after validation.

`AliasBinding`: `record_type`, `alias`, `provider`, `canonical_model_id`, `model_reference_key`, `target_model_version_key` — null until the alias resolves — `resolution_status` such as `documented_alias_unresolved`, `status` such as `provisional_until_resolved`, `resolver_evidence`, `sources`, `valid_from` and `valid_to`. `model_reference_key` is the member every join against an unresolved alias reads, the benchmark prior below included.

`CapabilityPrior`: stable prior key, exact model-version key or provisional model-reference key, first-party source URL, provider, retrieval time, source effective time when stated, normalized workload and capability tags, the qualitative claim with its verbatim-excerpt or faithful-paraphrase form and language, status, predecessor when superseding, and explicitly `low` confidence. A changed claim appends a new row that names its predecessor; it never rewrites history.

A `CapabilityPrior` is categorical evidence for choosing a cold-start experiment. Relevant matched measurements override it. It never enters numeric quality, uncertainty, success probability, cost or Pareto calculations; it cannot clear a quality floor, establish dominance, or make a recommendation measurement-based.

`PriceSchedule`: key, model-version key, channel, region, currency, input/cache-read/cache-write/output rates, threshold rules, tool fees, serving/batch premiums, effective interval and source. Price is mutable commercial data, never model metadata.

`SubscriptionSchedule`: key, access-channel key, list and actual recurring fee, included model/surface rules, rolling-window and weekly reset semantics, model-specific quota multipliers and caps, shared pools, purchasable-credit fallback, effective interval and source. Preserve user-supplied account rules with their provenance and vague provider limits as ranges or prose facts; do not manufacture a numeric quota.

`AccessModeAvailability`: access-channel key, model-version or model-reference key, harness/surface, supported effort/thinking values, supported serving modes, fallback capabilities, valid interval, source and confidence. Resolve `all_supported` only from the intersection of this record and `ModelVersion` capabilities; missing records make the affected modes unverified.

`QuotaObservation`: access-channel key, configuration fingerprint, task or session ID, accounting basis (`provider_charged_quota` or `reconstructed_raw_usage`), raw usage when reconstructed, applied multiplier, charged quota, before/after timestamps, before/after remaining session and weekly percentages when visible, reset timestamps, dashboard source and confidence. Select exactly one accounting basis. Provider-charged quota already includes its multiplier; reconstructed raw usage receives the multiplier once. Never infer a zero delta from a rounded unchanged display.

`BenchmarkDefinition`: key, name/version, task-manifest and dataset hashes, harness commit, grader/judge versions, score transform, category weights, resource limits, repeats and source.

`EvaluationConfiguration`: `record_type`, always `EvaluationConfiguration`; `evaluation_key`; `model_key`; `benchmark_key`, matching a `BenchmarkDefinition`; `configuration`, the published evaluated configuration such as `{"effort": "max", "serving_mode": "standard", "thinking": "adaptive"}`, whose members vary by publisher and whose `effort` may be `null`; `score`, the published numeric score on that benchmark; `published_cost_usd_per_task`; `output_tokens_per_second`; `status`; `source`, the publisher URL; `provenance`, `{"origin": "seed"}` on a row imported from the bundled seed; `retrieved_at`; and `seed_id`, the originating `evaluation_prior_seed` id, absent on a row that came from elsewhere.

This record is an independent published measurement of a model at a published configuration — a benchmark prior, and never a local attempt. `model_key` holds either a validated `ModelVersion`'s `model_version_key` or, for a model still behind a mutable alias, an `AliasBinding`'s `model_reference_key`; the alias-backed case is exactly what `status: independent_dated_prior_for_mutable_alias` marks, against `independent_dated_prior` for a resolved identity. `score` is the only quality member: `published_cost_usd_per_task` and `output_tokens_per_second` are commercial and throughput facts and no capability rank derives from them. An imported seed row keeps the seed's original retrieval timestamp, status and sources.

The evaluated system identity a local attempt ran under is no record here and no row of its own anywhere: the configuration fingerprint is computed as `config_fingerprint` in `## Keys` and carried inline on every `RunObservation` as `configuration_fingerprint`, which is where `run-observations.md` describes it and where a reader looking for the setup behind an attempt finds it.

`RunObservation`: run key, the attempt's own identity and the identity of the attempt it followed, configuration fingerprint and benchmark key, the routed request's `stage`, `workload_cohort` and `workload_tags` or their three nulls, task/seed/attempt, pass/fail/abstain/infra-error and raw dimension scores, all token categories, tool counts, provider bill, price schedule used, resolved model/fallback, wall/first-useful-output latency, timestamps and sanitized artifact hashes. The three identity fields are defined in `run-observations.md`, which also defines the frontier they place the row in.

## Conditional update

Default cadence: model/release indexes and commercial terms weekly; benchmark release indexes monthly; an immutable model detail page never, a known detail being one nothing refetches. Those are shipped data rather than sentences — `$HERE/data/refresh-cadences.json` holds one cadence per `kind`, and it is the file both this pass and the unattended one read. The configuration does not override them: the profile carries no cadence member and never had one. Check only sources required by enabled selections and families marked `watch_for_newer_versions`.

One case overrides the cadence rather than being scheduled by it: an enabled selection whose model has no capability rank — no `EvaluationConfiguration` for it in this ledger and no `evaluation_prior_seed` for it in the bundled seed — makes its own ranking sources due on this pass whatever their cadence says. Those sources are the `benchmark_release_index` rows for the benchmarks the seed ranks against, and nothing else: the model and release indexes are not made due by an unranked selection. Discovery running weekly while the only index that can score what it discovers runs monthly is what leaves a newly adopted seat unrankable for up to a month, and routing answers that gap by suspending the ceiling it cannot enforce (`references/model-routing.md`), so closing it early is the other half of the same design. Record a `SourceState` status for every source the pass considers — one of the four fetched outcomes for a due source, and `not_due` for one whose cadence has not elapsed. Stamp `last_checked_at` on every source considered and `last_retrieved_at` on every source actually retrieved, this one included: a retrieval that leaves the field alone leaves the source permanently due, since that field is the only thing any cadence is measured from.

1. Conditionally retrieve model indexes, release notes, deprecation feeds and mutable first-party capability sources using ETag or Last-Modified; otherwise hash the index content. Refresh capability sources on the existing model/release-source cadence, and append a new low-confidence `CapabilityPrior` only when the sourced claim or its normalized tags change.
2. Compute discovered version keys for configured selections and watched families. Fetch first-party detail pages only for relevant keys absent from `model-versions.jsonl`; a known immutable detail is never fetched again. Report a watched newer version without enabling or substituting it.
3. Resolve mutable aliases. Close a prior binding and append the new target when it changes.
4. Revalidate direct and gateway API rate cards and subscription/usage-limit pages independently of model discovery. Append scheduled future rates or terms immediately; close prior intervals only from the documented effective time.
5. Revalidate benchmark releases and harness repositories. Any dataset, manifest, grader, weighting or harness change creates a new benchmark key; never relabel old observations.
6. Generate missing configuration fingerprints and run keys only for enabled selections and modes. Execute nothing unless the user explicitly requested evaluation; `update` discovers gaps and reports them.
7. Reprice metered token/tool usage under the requested current schedule in derived output. Preserve original provider bill and published historical cost. Recompute subscription allocation from the selected billing-period observations without translating quota into API tokens.

A source without usable validators still receives one bounded fetch per due pass. `--force` ignores cadence once; it does not bypass fingerprints or fetch known detail pages.

## Import validation

For `record`, reject observations missing configuration identity, benchmark identity, outcome, provenance or timestamps. Reject quota observations that combine provider-charged usage with a second model multiplier, or raw usage without the applicable multiplier. Missing token categories may be explicit `null`; never silently convert them to zero. Separate infrastructure errors from model failures. A duplicate run key with identical content is skipped; a duplicate with different content is a conflict and changes nothing.

Recompute only derived frontiers whose eligible run set changed. A frontier is identified by benchmark key, stage, workload cohort and sorted workload tags together; rows differing on any of them are never compared as one frontier, and a row naming no cohort enters none. Derived files may be replaced because they are reproducible from append-only source records.

## Standing policy movement

Every observation carries the Standing Policy its own frozen decision ran under in `provenance.standing_policy`: the Cohort, its `policy_revision`, and the resolved `starting_rung`, `current_rung`, `floor`, `ceiling` and `next_rung_up`. A verdict inherits by authority rather than by policy and carries none. An old row is therefore always read against the ladder its own run froze; the current store is never used to reinterpret it. It also carries `provenance.exploration`, true where its decision was an Exploration Attempt — a routed attempt the policy deliberately placed one Rung below the Cohort's own, whose outcome is evidence about the point it ran on and never about the Rung it stepped down from.

`record` evaluates the failure threshold once per cohort the import touched, after the append, for the automatic import at a verdict and the user's own invocation alike. A row is eligible when it names that cohort, is decisive, was judged by an independent verifier, an objective checker or a declared failure signal, carries no exploration tag, carries the cohort's current `policy_revision`, ran on exactly its own carried `starting_rung`, and completed after the cohort's current policy epoch — which every threshold movement and every reset begins anew. The window is the last M eligible rows by `completed_at` ascending and then `run_key`, passes included and not necessarily full; at N or more failures in it the cohort moves to the last triggering failure's own carried `next_rung_up`, naming every failing run key and the run identity behind it. A carried `next_rung_up` of `null` is the ceiling and appends nothing.

Movement is upward only, and what moves it back is a deliberate act of the user's: `config policy reset`, which restores the shipped default and keeps the history, or `config reset --evidence`, which discards the measurement the movement rests on and the history with it. Evidence whose carried revision no longer matches the cohort's is kept in the ledger and moves nothing. `record` reports, per touched cohort, `moved` with the appended history row, `standing_policy_ceiling_reached`, `stale_policy_context`, or `below_threshold`, each with the failure count, the rows in the window and the threshold behind it.

## Change report

Report relevant new model versions, alias changes, capability-prior changes, price or subscription schedules, quota-rule changes, deprecations, benchmark versions, imported or missing configured points, frontier membership changes, stale/provisional sources and failures. Name zero changes explicitly; never manufacture work by refreshing immutable details.
