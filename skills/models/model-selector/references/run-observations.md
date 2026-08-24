# Run observations

Use this reference for `observe`, and beside `evidence-ledger.md` for `record`. It is the public contract a routed caller — Orchestrate, delegation, or any other Skill that launched work from a route decision — emits evidence under. `observe` is offline, non-interactive, and writes exactly one file: the artifact the caller named. It starts no setup, performs no network access, evaluation, or research, and writes no configuration, profile, evidence ledger, or derived frontier. `record` remains the only ledger mutation, and it happens because the user invoked it.

## The completed attempt

A caller supplies one canonical UTF-8 JSON envelope holding `schema_version` `1` and an ordered non-empty `attempts` array. Each attempt describes one routed execution that has reached an eligible completion boundary, and carries: `attempt_id`, the caller's own request name; `session_identity` and `task_identity`, both opaque; `workload_stratum`; `attempt_index`, counting from one within the work the task identifies; `harness`, naming the active Harness and its inventory revision; `benchmark`, whose `key` identifies the workload or benchmark the attempt is comparable within; `decision`, the public route decision the attempt launched from, kept whole; `outcome`; `completed_at`; and optionally `started_at`, `resolution`, `measurements`, `prior_attempt_id`, `checker_charge`, `seed`, and `artifact_hashes`.

The workload strata are `initial_build`, `amend`, `collision_repair`, `rebuild`, `mechanical_wave_fix`, and `delegated_execution`. An initial build and a mechanical wave fix are different work rather than the same work priced twice, and an amend is a distinct attempt at the first one's work, so each is its own stratum and its own attempt.

The attempt begins from its immutable route decision and the configuration fingerprint inside it. A `selected` decision names the exact point; an `inherit` decision ran on the frozen main seat and is fingerprinted from that seat; a `refused` decision launched nothing. Nothing is re-resolved here: the model, the native deliberation control, the channel, the adapter, the evidence class, and the provenance are read out of the decision the caller already holds, never chosen again.

## What establishes an outcome

An outcome is `pass`, `fail`, `abstain`, or `infra_error`, and only something external to the attempt may establish it. A decisive `pass` or `fail` requires an authority of `independent_verifier`, `objective_checker`, `frozen_rubric`, `declared_failure_signal`, or `user_confirmation`, together with a checker that names itself and is marked independent. A builder's or a subagent's self-report is never one: an authority of `self_report`, a checker that is not independent, and an unchecked subjective success are each refused rather than downgraded, so unchecked work cannot become measurement-based quality evidence.

`abstain` and `infra_error` carry a non-model condition instead: `mechanical_hinder`, `open_decision`, `discovered_dependency`, `tracker_failure`, or `merge_collision`. A mechanical hinder and a tracker failure are infrastructure; an open product decision, a newly discovered dependency, and a merge collision are abstentions. They may be established by the Harness or the tracker as well as by a checker, they are retained as what happened, and they never enter a configuration's quality: `record` computes a conservative success rate from judged model outcomes alone and counts the rest beside it. A decisive result offered together with a condition is refused, because the two are different claims about the same attempt.

## What an artifact carries

`observe` builds each observation field by field from an allow-list, so nothing reaches the artifact by sitting beside the facts in the input. An observation carries the run key and the identities it derives from — configuration fingerprint, benchmark key, opaque task identity, seed, attempt index — the opaque session identity, the workload stratum, the exact routed point and the point that actually served with the fallback it resolved from, the outcome with its authority, checker, condition, and permitted score dimensions, the available token categories and tool counts, retries, cash, provider bill, allocated subscription cost, and quota facts under exactly one accounting basis, wall and first-useful-output latency, both instants, sanitized artifact hashes, and the provenance of the decision: route status, snapshot identity, evidence class and vintage, profile and evidence identity, main-seat model, Harness, and Harness inventory revision.

Every measurement the environment did not expose stays an explicit `null`. A missing value is never inferred as zero, because a zero is a reading and an absence is not. Wall latency is derived only from the attempt's own two instants when the caller exposed no measured value.

An artifact never retains full prompts, responses, reasoning, ticket or source bodies, source files, diffs, terminal output, secrets, credentials, complete transcripts, or absolute paths where an opaque identity is sufficient. Score dimensions are normalized identifiers with numeric values, artifact hashes are an algorithm and a digest rather than a file name, and every emitted string is held to an identity: an absolute path, an embedded newline, or a value longer than an identity refuses the attempt as `unsanitized_value` and names only the field it was in.

## Cheap-first policy accounting

Where an attempt names a `prior_attempt_id` present in the same batch, its observation carries a `cheap-first` policy account: the run keys of both attempts, the retries, and what the whole sequence was charged in cash, rolling quota, weekly quota, allocated subscription cost, and wall seconds. The account adds the failed first attempt, the escalated attempt, and the `checker_charge` the caller supplied for the verdict between them, because a routing policy is a configuration of its own rather than free capability. A dimension no contributor exposed stays `null` rather than reading as a saving.

## Idempotency, conflict, and import

Emission is deterministic: the same attempt produces the same run key and the same content. Merging into an artifact skips an identical observation rather than repeating it, and an identity already present with different content is a conflicting identity — `conflicting_identity` — that surfaces both digests and overwrites neither. `record` applies the same rule against the ledger: an unseen run key is appended, an identical duplicate is skipped, and a conflicting duplicate is rejected while nothing changes. Only the derived frontiers whose eligible run set actually changed are rebuilt.

`observe` validates every observation with exactly the validation `record` applies before reporting it as importable, so a reported artifact is one an explicit import accepts and a hand-written one meets the same rules. The artifact stays in caller-owned scratch, is named in the caller's own report, and is imported only when the user invokes `/model-selector record` on it; it is never imported automatically, installs no lifecycle hook, and changes no tracker state. Its lifetime is that scratch directory's: nothing here rotates it, copies it elsewhere, or takes it away, and an imported artifact is left exactly where it was — retention, cleanup, and notification belong to #91.

## Stable refusals

Per-attempt refusals: `invalid_attempt`, `no_outcome`, `unlaunched_decision`, `incomplete_attempt`, `self_reported_outcome`, `unchecked_outcome`, `non_model_condition_outcome`, `missing_non_model_condition`, `invalid_scores`, `invalid_quota_accounting`, `unfingerprinted_inheritance`, `unfingerprinted_configuration`, `unsanitized_artifact_hash`, `unsanitized_value`, `incomplete_observation`, `invalid_run_key`, and `conflicting_identity`. A route decision that no external judgement completed is `no_outcome` and remains audit data rather than a `RunObservation`; an interrupted attempt is `incomplete_attempt` and can never be reported as a successful one.

Process-level refusals, emitted before any attempt is read: `invalid_arguments`, `unreadable_artifact`, `malformed_json`, and `invalid_artifact`. Every refusal is machine-readable on stdout, carries no traceback, and names no caller material.

## Boundary

This contract is the narrow routed-work artifact only. Issue #91 owns explicit-opt-in automatic capture across ordinary Harness work: lifecycle installation, automatic import, pending-review reconciliation, retention, cleanup, notification, and cross-Harness hook ownership are its, and it reuses this contract rather than building a second normalized representation of routed work.
