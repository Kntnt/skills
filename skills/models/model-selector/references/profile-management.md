# Profile management

Use this reference for first-run setup, `setup`, or `config`.

## Store

The selected data directory contains:

| File | Purpose |
| --- | --- |
| `config.json` | Current validated configuration and active revision. |
| `config-history.jsonl` | Append-only prior revisions and tombstones. |
| `standing-policy.json` | Script-owned Standing Policy overrides, one entry per moved workload Cohort. |
| `standing-policy-history.jsonl` | Append-only Standing Policy movements and their causes. |

`config.json` contains `schema_version`, `profile_id`, `revision`, `created_at`, `updated_at`, `currency`, `region`, refresh cadences, access channels, model selections and optional quota shadow prices. Give every channel and model selection a stable user-facing ID.

The persisted version-1 shape is formalized by `profile.schema.json`. Context migrates older valid shapes in memory before validation and never rewrites them; no earlier documented shape currently requires a transformation. A missing or invalid profile is represented as `profile: null` for routing and does not open setup.

An access channel records `channel_id`, provider, surface or gateway, billing type (`subscription`, `direct_api`, `gateway_api`, or `other`), exact plan/tier when applicable, actual or list recurring fee, billing currency and tax treatment, included/overage policy, reset windows, model-specific quota multipliers and sources. Claude Max 5x/20x and ChatGPT/Codex Pro 5x/20x are examples of plan tiers, not an exhaustive built-in catalog. Never store API keys, cookies, account IDs or other secrets.

A model selection records `selection_id`, provider, family, requested model ID, canonical provider model ID, provider release ID, resolved target when available, version kind (`pinned_release`, `provider_release_slug`, or `mutable_alias`), validation status, channel ID, effort/thinking policy and values, serving-mode policy and values, harness/surface, fallback policy, enabled state and `watch_for_newer_versions`. The default version kind is `pinned_release`; use `provider_release_slug` when the provider exposes a named release but no dated immutable snapshot, and require explicit acceptance for a mutable alias. Discovery may notify about a newer family version but never replaces the configured reference without a config edit. The same model through two channels is two selections.

Map configuration to evidence deterministically: `requested_model_id` is the ID sent through the selected channel or gateway; `canonical_provider_model_id` is the underlying provider ID; `provider_release_id` is the immutable release ID or documented release slug when one exists; `resolved_target` is the concrete target returned for a mutable alias. For example, an OpenRouter selection may request `x-ai/grok-4.6` while recording underlying `grok-4.6` as the canonical provider ID and the returned concrete target separately. An unresolved alias has a model-reference identity but no immutable model-version identity and remains provisional for recommendations.

Store `all_supported` as the policy value, not as a copied list. At recommendation time, intersect model-version capabilities with access-mode availability for the selected surface/channel; unknown surface support excludes that mode as unverified. `update` refreshes evidence and derived candidates without rewriting `config.json`. Apply the same policy/value shape separately to effort/thinking and serving modes.

Routing policy has shipped defaults rather than profile-owned setup fields: `cold_start: select`, `quality_floor: 0.7`, and `shadow_prices: null`. Context reads these defaults from `data/routing-defaults.json`; no setup answer is required before the first route.

Serialize writes with an atomically created `config.lock` directory containing owner and timestamp metadata. While holding the lock, re-read and verify the expected revision/content hash, abort on a concurrent change, recover any prior `config.previous.*.json` snapshot missing from history, and validate every reference. Write the new revision to a temporary sibling, preserve the current state as `config.previous.<revision>.json`, atomically replace `config.json`, append the preserved revision to `config-history.jsonl` idempotently by profile/revision, then remove the preserved snapshot and lock. Report and retain recoverable files if any step fails. A removal creates a new revision; it does not delete ledger evidence. A reset follows the same lock protocol, appends a tombstone and removes `config.json` only after the user confirms the exact path.

If `config.lock` already exists, inspect its owner and timestamp without modifying it. Stop for a live or unverifiable owner. When the owner can be proven dead and the lock is older than ten minutes, atomically rename it to `config.lock.abandoned.<UTC timestamp>` before retrying; retain and report that recovery artifact instead of deleting it silently.

## Standing policy

The Standing Policy is where one workload Cohort starts on the Rung ladder and how far up and down that ladder routing may go. It is not part of the profile and is never edited by hand: the shipped default is a complete working policy, the store holds only the overrides a measured failure threshold created, and the `config.lock` protocol above does not apply to it. Both files are owned by the Collection Library's `scripts/standing_policy.py`, which `config policy` invokes and which the context derivation reads.

The shipped default is `starting_rung: "cold_start"`, `floor: "weakest_enabled"`, `ceiling: "main_seat"`, a failure threshold of 2 failures in a window of 4, and an exploration budget of `epsilon` 0.1, one attempt per run, seed `kntnt-standing-policy-v1`. Those first three values are symbolic and resolve against each individual request's candidate ladder; they are never materialized into the user file merely because routing read them. A Cohort with no entry has revision 0; its first override starts at revision 1 and each later movement raises its own revision by one. In version 1 nobody sets a floor, a ceiling, a threshold, an epsilon, or a budget: only `starting_rung` is ever stored, and only by a threshold trip.

`standing-policy.json` carries `schema_version` and a `cohorts` object keyed by the canonical `workload_cohort`. Each history row carries `effective_at`, the Cohort, `from`, `to`, `revision_before`, `revision_after`, and a `cause`: a `failure_threshold` cause names the run keys that tripped it and the `source_run_identity` of the run that closed the window, and a `reset` cause names none, having no evidence behind it beyond the user asking. The threshold cause is written by the ledger import itself, which evaluates it inside `record` under the eligibility and window rules in `evidence-ledger.md`; the movement reaches routing at the next frozen context and never a run already under way. `config policy show` reads both and writes nothing; `config policy reset` removes one Cohort's override, or every one of them where no Cohort is named, and appends one row per Cohort restored.

When `config.json` is invalid, preserve its exact bytes as `config.invalid.<UTC timestamp>.json` with user-only permissions before setup writes a replacement. Report the archive path.

## First run

Any invocation that needs selections first checks `config.json`. When it is absent or invalid, pause that invocation and conduct setup one question at a time. Reuse every unambiguous value already supplied in the request.

1. Ask which exact model versions to include. Accept a compact list, but resolve provider, family, requested/canonical provider IDs and release/version separately from local evidence. If the user gives only a family or mutable alias, ask for a pinned release; when local evidence cannot resolve it, save the supplied reference as `unverified` and propose `/model-selector update`. Retain an alias only after explicitly confirming its mutable behavior and record its resolved target when available.
2. For each distinct way the models are obtained, ask whether it is a subscription, direct metered API, gateway such as OpenRouter, or another arrangement. For a subscription collect the exact plan and tier, including multipliers such as 5x or 20x, recurring amount/currency/tax treatment, included versus credit-overage behavior and known reset windows. For metered access collect provider/gateway and region; obtain prices from evidence rather than asking for secrets.
3. Attach every model selection to one access channel. Ask independently whether effort/thinking and serving modes should use the default, `all_supported`, or an explicit list. Capture fallback policy and whether to watch the family for newer releases. Explain that only modes verified for both model and selected surface become candidates.
4. Show the complete profile, accounting units and unknown fields. Write only after confirmation. Continue the original invocation when it can run from stored evidence; otherwise name the missing evidence and propose `/model-selector update`.

An access channel is valid for persistence when it has a stable ID, provider, surface/gateway, billing type, `region` or explicit unknown, and `sources`. A subscription additionally requires `plan`, `tier`, `billing_period`, `currency`, `recurring_amount`, `tax_treatment`, `included_overage_policy`, `reset_windows`, and `quota_multipliers`; confirmed-unknown recurring amount, tax treatment, tier, and reset windows are `null`. Metered access requires `currency` and `rate_source`, where a confirmed-unknown source is `null`. Confirmed unknown values make only the dependent cost view provisional; they do not reopen setup.

Setup is complete when at least one selection is enabled, every enabled pinned release, provider release slug or explicitly accepted mutable alias points to one valid access channel, and every commercial cost has a declared unit or confirmed-unknown value. Persist once so later invocations never repeat the interview unless the configuration is missing, invalid, or explicitly reopened.

When an old ledger has access records but no `config.json`, offer to import the relevant records into a draft profile. Never infer a profile from bundled seed evidence; it contains public model and benchmark facts, not user entitlements.

## Commands

| Invocation | Behavior |
| --- | --- |
| `/model-selector setup` | Create the first profile, or review every field of the current profile and save a new revision. |
| `/model-selector config [show]` | Display the current profile, path, revision, models, channels, costs, modes, version-watch policy and unresolved fields; no writes or network. |
| `/model-selector config add model` | Interview one model selection and attach it to an existing or newly created channel. |
| `/model-selector config add channel` | Interview one access channel; leave it unused only when the user confirms that intent. |
| `/model-selector config edit [model|channel] <id>` | Show the exact current record, collect changed fields and save a validated revision. |
| `/model-selector config remove [model|channel] <id>` | Show the exact target and consequences, then save a revision after confirmation. A referenced channel must be reassigned or its dependent model selections removed in the same revision. |
| `/model-selector config policy [show] [<cohort>]` | Show the effective Standing Policy and the movements behind it; no network or writes. |
| `/model-selector config policy reset [<cohort>]` | Restore the shipped Standing Policy for one Cohort or for all of them after confirmation; retain the history. |
| `/model-selector config history` | Show revision timestamps and summaries from local history; no network or writes. |
| `/model-selector config reset` | Confirm the exact configuration path, append a tombstone and remove only `config.json`; retain evidence and history. |

After any add, edit or remove, report sources newly due, selections now lacking evidence and derived frontiers invalidated. Configuration commands consult local evidence only and never trigger network access or evaluations. A supplied release absent from local evidence may be saved with `validation_status: unverified`; it remains excluded from decisive recommendations until `/model-selector update` validates it.

Keep a selection ID stable when editing the version, channel, modes or policies of that conceptual selection. Adding a newer release alongside the existing release creates a new selection ID; replacing the old release uses `config edit model <id>`. A discovered release is never “adopted” implicitly.
