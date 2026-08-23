# model-selector

Configure the exact AI model versions and access channels you use, then compare their price-performance evidence for a workload.

## Synopsis

```
/model-selector [recommend] [<workload>] [--decision=route|renew] [--budget=<amount>|--quality=<score>] [--data=<path>]
/model-selector chart|compare <workload> [--decision=route|renew] [--data=<path>]
/model-selector setup [--data=<path>]
/model-selector config [show|add model|add channel|edit model <id>|edit channel <id>|remove model <id>|remove channel <id>|history|reset] [--data=<path>]
/model-selector update [--force] [--data=<path>]
/model-selector record <path> [--data=<path>]
/model-selector status [--data=<path>]
```

## Description

`model-selector` treats a comparison point as a complete system: exact model release or resolved alias, effort or thinking budget, serving mode, harness, tools, policies, access channel, and effective commercial schedule. It recommends from Pareto frontiers instead of reducing quality and cost to one misleading ratio.

First use asks which exact model versions to include and how each is obtained. An access channel may be a subscription with its exact plan and tier, a direct metered API, a gateway API such as OpenRouter, or another arrangement. The confirmed profile is stored under `~/.model-selector/` by default and reused on later invocations. No credentials are stored.

The bundled seed contains dated public model identities, direct and gateway API prices, and independent benchmark priors. It contains no access profile, subscription entitlement, account quota, or local evaluation. Recommendations remain conditional on evidence vintage and become production-grade only when representative local observations support them.

## Commands

- `recommend` chooses one exact configuration and reports its nearest cheaper and stronger Pareto neighbours. Bare `/model-selector` is the same form when the current workload is unambiguous.
- `chart` and `compare` emit separate comparable frontier tables and plotting-ready CSV instead of choosing one winner.
- `setup` creates the first profile or reopens a complete guided review.
- `config` shows or revises model selections, access channels, history, and the active profile.
- `update` performs one bounded refresh of due mutable model indexes, commercial terms, and benchmark releases without refetching known immutable model details.
- `record` imports unseen local evaluation observations without overwriting conflicting history.
- `status` reports configuration, evidence age, gaps, and provisional facts without network access or writes.

## Options

- `--data=<path>` — use another configuration and evidence directory. Valid on every form.
- `--decision=route|renew` — compare marginal routing economics now or whether a fixed subscription fee earns renewal. Valid for `recommend`, `chart`, and `compare`; `route` is the default.
- `--budget=<amount>` — choose the highest conservative quality within a comparable budget. Valid only for `recommend` and mutually exclusive with `--quality`.
- `--quality=<score>` — choose the lowest conservative comparable cost that clears the quality floor. Valid only for `recommend` and mutually exclusive with `--budget`.
- `--force` — check every relevant mutable index once regardless of cadence. Valid only for `update`; it still does not refetch known immutable details or rerun existing observations.

## Notes

Cash, rolling-window quota, weekly quota, subscription credits, allocated plan cost, and latency stay separate unless you provide explicit shadow prices. Included subscription work may have zero marginal cash while still consuming scarce quota.

Configuration changes use revision history and do not delete evidence. Newly discovered model versions are reported but never replace an enabled version automatically. A supplied mutable alias remains provisional until its concrete target is resolved.

A flag with no work to do on the selected form is refused rather than ignored. An incomplete form changes nothing and prints the synopsis instead of guessing what you intended.

## Dependencies

None. Network access is useful only for `update`; the other forms operate on bundled or locally stored evidence and report when the evidence is insufficient.

## See also

`/kntnt select` to enable this skill in another layer or harness. Use `config history` to inspect prior profile revisions and `status` to see whether an update is due.
