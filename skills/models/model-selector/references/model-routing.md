# Model Routing Module

This is the public routing Interface owned by model-selector. A caller invokes `/model-selector route <path>` with a UTF-8 JSON artifact containing one versioned request object or an ordered array. The response is one JSON object containing `schema_version`, `snapshot`, and `decisions`; `decisions` contains exactly one decision per input in the same order. Route is offline, non-interactive, and read-only: it never starts setup, performs no network access, research, evaluation, or evidence refresh, and writes no configuration or evidence.

## Request contract

The accepted `schema_version` is `model-selector-route-request-v1`. Every request supplies a unique `request_id`, `authority` (`execution` or `verdict`), `stage`, `workload` containing the verbatim workload material, `reversible`, and `verification`. `verification` identifies an independent checker, a declared failure signal, or explicitly says neither exists. Optional `overrides` has only `model` and `deliberation`; optional `prior` carries an earlier decision and independently verified failure relevant to the caller's existing retry bound. Optional top-level `snapshot` is a snapshot returned by an earlier response.

The public deliberation scale is exactly `low`, `medium`, `high`, `xhigh`, and `max`. Omission means automatic selection. Numeric values, provider control names, `auto`, `none`, `off`, and default aliases are invalid public values. A model override is an exact configured model version or an alias resolving unambiguously inside the snapshot; a family name is not exact.

Reject a malformed artifact as a whole before routing. Request-level failures instead produce ordered refused decisions so one bad request does not erase its peers' audit results.

## Frozen routing snapshot

When no snapshot is supplied, freeze the current profile revision; evidence vintage and identity; active Harness inventory and actual spawn capabilities; main-seat identity including its complete model, channel, native control, and serving mode; verified portable-to-native control mappings; separate commercial facts; and override policy. Give the canonical snapshot a deterministic `snapshot_id` and return the complete snapshot.

When a snapshot is supplied, validate it and use only its frozen profile, aliases, evidence, prices, quotas, Harness facts, main-seat identity, mappings, and policies. Never silently adopt a later profile revision, alias target, evidence record, price, quota, or Harness capability. An invalid or incomplete supplied snapshot refuses affected requests.

## Exact-point selection

Use the same complete-point, hard-filter, evidence-class, multidimensional-cost, uncertainty, and escalation rules as human `recommend`. Begin with enabled points in the snapshot. Intersect them with the active Harness's actual spawn capabilities and exclude every channel without a concrete current-Harness adapter. Exclude incomplete points, unavailable native mappings, unsafe workload points, and execution points above the complete main-seat ceiling.

An explicit model locks only that dimension and leaves deliberation selectable. An explicit deliberation locks only that dimension and restricts candidates to points with a verified mapping for that exact portable value. Refuse an unavailable or ambiguous override rather than substituting a neighbor, alias, or model. Refuse an explicit point above the main-seat ceiling. Automatic execution selection never exceeds the complete main-seat capability.

Portable levels define adjacency only; adjacency does not imply quality ordering, and matched evidence may prefer a lower portable level. For every model, channel, surface, and Harness point, resolve a usable portable value to its verified exact native effort, reasoning, thinking mode, or thinking budget. Route never interpolates, rounds, or guesses a missing mapping. Resolve `max` within the frozen snapshot to the highest verified native value for that exact point; include that resolved value in the configuration fingerprint.

Matched representative measurements are required for a `measurement_based` selection. Use `mixed` when measurements exist but a decision-relevant heuristic remains, and `heuristic` for a visibly cold-start choice. Stale evidence retains its recorded vintage and cannot silently support a fresher claim. Missing evidence remains unknown and never becomes zero, dominance, a cleared quality floor, or measurement-based support. Cash, rolling quota, weekly quota, allocated subscription cost, and latency remain separate dimensions unless the snapshot supplies explicit shadow prices.

Verdict authority always returns exact main-seat inheritance and is never price-optimized. If the Harness cannot represent exact inheritance of the frozen main seat, refuse it.

## Decision contract

Each decision has `request_id`, exactly one `status` value—`selected`, `inherit`, or `refused`—and `audit`. The three shapes are discriminated and must not be partially combined.

A `selected` decision alone carries `launch`. It names the exact configured model version or resolved alias, channel, native deliberation control, portable deliberation, serving mode, configuration fingerprint, and Harness-native launch arguments. It also carries evidence class, provenance, exclusions with stable codes and details, and any bounded next escalation. `launch.arguments` must be a complete instruction produced by the frozen Harness adapter, never generic provider syntax.

An `inherit` decision carries `inheritance`, never `launch`, and states the exact main-seat identity for verdict authority or the audited reason no safe execution override is applied. A missing profile may inherit. Insufficient discriminating evidence may inherit when selection would require invented facts.

A `refused` decision carries `reason` with one stable code and detail, never `launch` or launch arguments. Stable codes are `invalid_profile`, `invalid_snapshot`, `invalid_request`, `ambiguous_override`, `unavailable_override`, `unknown_main_seat_ceiling`, `above_main_seat_ceiling`, `unrepresentable_verdict_inheritance`, and `empty_safe_candidate_set`.

The `audit` object records the snapshot identity, evidence class when applicable, provenance identities, and exclusions considered. Provenance points to frozen profile and evidence identities rather than restating workload material.

## Bounded escalation

Emit a bounded next escalation only for reversible, objectively checked execution with an external checker or declared failure signal. Self-confidence is not verification. Without matched policy evidence supporting a different route, the next escalation is one adjacent portable level on the same model, only when that point has an exact verified native mapping and remains at or below the main-seat ceiling. Escalation consumes only a retry the caller already owns and creates no attempt. A prior failure influences selection only when externally verified and bound to the earlier configuration fingerprint.

Human `recommend` retains its evidence banner, frontier neighbors, uncertainty, exclusions, and experiment brief. Route is the compact machine-readable form; neither form owns separate selection semantics.
