# Model Selector's `update` is retired, and plans ship with the collection

This record supersedes what is left of [ADR-0185](0185-the-worlds-facts-are-fetched-by-the-agent-and-adopted-through-the-validator.md): the agent's reading of provider pages, and `catalogue.py adopt`, the validator it handed its reading to. [ADR-0191](0191-a-script-keeps-the-catalogue-current-from-three-structured-sources.md) and [ADR-0193](0193-the-catalogue-pass-runs-daily-by-itself-and-reaches-only-structured-sources.md) kept `update` as the one place a page was read. This record removes it. What the rules now are is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own shipped files. This record argues the case.

## What changed

**`update` has no job left.** The daily catalogue pass (#312) learns new models, prices, thresholds, deliberation levels, release dates and aliases from three structured sources. It removes a model its maker stops listing (#311) and resyncs the generated agent definitions whenever it changes the catalogue. So a verb the user is told to run would do nothing the machine does not already do. It would still cost attention, and it would keep a second path to the catalogue that nothing exercises and that goes stale unnoticed (#313).

**Every part of the old `update` has a place or is dropped.** The parts are the ones `docs/research/model-lifecycle-2026-09.md`, section 4, lists.

| What `update` did | Where it goes |
|---|---|
| New models, per-category prices, prompt-token threshold, deliberation levels | The catalogue pass (ADR-0191) |
| Release date and aliases | The catalogue pass (ADR-0191) |
| Removing a model that has gone | The catalogue pass (ADR-0192) |
| Agent-definition resync | The catalogue pass's own resync |
| Subscription plans (names, `monthly_usd`) | Shipped seed data only, current as of a release of the collection. No runtime refresh. |
| `provider_says` and other provider prose | Dropped |
| Capability seeds | Unchanged. They were never fetched. |
| Profile and payment channels | `setup`, as before |

## The rule

**The verb is removed, not refused.** `help/update.md` is gone, and the Skill's grammar has no `update` path. Under the Manager's `invoke` engine a word with no `help/` page is an operand, so `/model-selector update` is now ordinary work text like any other word. No retired-path mechanism is added and no stub page is kept, because the collection keeps no backward compatibility for a single user.

**`catalogue.py adopt` goes with it.** Its validation functions stay, because the pass writes every entry through them. Its field-by-field merge, its plan replacement and its report go, since only `adopt` used them. So does the `setup_apply.py` mode that synced the definitions with no profile, which only `update` ran. The catalogue pass is the one writer of `catalogue.json`.

**Plans are read from the shipped seed alone.** No structured source lists what a provider sells, and the pass reads no page. A plan therefore changes only when the collection is released with a new seed, and `/kntnt update` brings that release in. `catalogue.load` returns the seed's plans even where an older `catalogue.json` still holds plans of its own, since those were read by a mechanism that no longer exists and nothing will ever bring them current. `status` no longer reports the plans' `retrieved` dates. A date that moves only with a release says nothing about the provider, and the catalogue's freshness is now the pass's own per-source outcome.

**`provider_says` is removed everywhere.** It was a provider's one-line positioning of a model. The interview showed it, and nothing ranked on it. Prose never becomes a number (`docs/rules/routing.md`), and a recommendation from prose shown beside one from measurement contaminates it. So it leaves the seed, the loader and the printed catalogue.

**`setup` reads no page and ends with the pass.** Its opening step, which held `## Update` first when the catalogue was more than thirty days old, is gone. Setup runs `catalogue.py refresh` once at its end. It runs where the writer answered `ok` and where the review was declined, and never after the writer refused a profile. It is started by hand rather than with `--scheduled`, so it takes the pass's lock but ignores the daily marker and does not count as the day's attempt. Re-running setup on a day the pass already ran therefore still refreshes, for example after adding a maker, so a fresh machine has a current catalogue at once rather than the next morning.

## The alternatives

**Keep `update` for plans alone.** Rejected. It is the one part no structured source covers, and it is also the part least worth an agent's reading: a plan changes a few times a year, and nothing in the Skill ranks on its price. An agent reading pages to refresh it keeps alive the whole path this series set out to retire, with all its failure modes, for a fact a release carries well enough.

**Refuse `update` with a message naming `status` and `setup`.** Rejected. The Manager's invocation engine has no retired-path mechanism, and adding one for a single verb on a single machine is backward compatibility this collection does not keep. As an operand, the word reaches the selection engine as work text, which is what any other unknown word does.

**Keep plans refreshed through `catalogue.json` by some later source.** Not done now. Should a structured source of plans appear, the pass can govern them the way it governs prices, and the seed-only rule is where that change would begin.
