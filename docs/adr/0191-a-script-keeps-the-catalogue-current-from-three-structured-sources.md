# A script keeps the catalogue current from three structured sources

This record narrows [ADR-0185](0185-the-worlds-facts-are-fetched-by-the-agent-and-adopted-through-the-validator.md). That record concluded that a script learns nothing about the world, because a script cannot interpret the pages an agent reads. For models and their prices this is no longer so. What the rules now are is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own shipped files. This record argues the case. ADR-0185's restriction to person-invoked fetching, and its conclusion that nothing reaches the network unattended, still stand until the pass is scheduled, and the ticket that schedules it (#312) supersedes it.

## What changed

**The facts a pass needs are published as structured data.** An investigation on 2026-09-11 (`docs/research/model-lifecycle-2026-09.md`) found three sources that a script can read with no agent, no web page and no model call:

- **Claude Code** lists the models the account can use in its control protocol's answer to `initialize`, with the deliberation levels each supports. The exchange is `initialize` and nothing else, so no prompt is sent and no token is generated.
- **Codex** lists them through `codex app-server`'s `model/list`, with the vendor's hidden entries marked.
- **OpenRouter**'s public `GET /api/v1/models`, which needs no authentication, carries a per-category price for every model of all three makers, a price above a prompt-token threshold where one applies, a release instant, and the supported efforts.

So the catalogue can gain a model and a new price without anybody running `/model-selector update`. `update` reads web pages through an agent, and `adopt` checks the shape of what the agent wrote but not whether the numbers are true.

## The rule

**One pass, `catalogue.py refresh`, a subcommand of the existing script.** It is run by hand. Nothing schedules it yet. `update` is left as it is until #313 retires it. Both can write prices meanwhile, and the last writer wins.

**Each source governs what it is the authority on, and nothing else.**

- The harness lists govern which Claude and GPT models are offered, their aliases, and their levels where the list reports them. Hidden entries are skipped, because the vendor has already pruned that list. A harness list is read only where its maker is chosen, since nothing it offers for an unchosen maker may enter the catalogue.
- OpenRouter governs prices, release dates, the slug it routes each model by, and which Grok models are offered. Grok has no harness list, being reached only through OpenRouter. The Grok models offered are every `x-ai/` id except those with a `:` variant suffix such as `:batch`, those ending `-multi-agent`, and those whose entry lists no level on the ladder. A model with no deliberation control cannot be launched at a level. On 2026-09-11 that leaves `grok-4.3`, `grok-4.5` and `grok-4.6`.

A source that cannot be read changes nothing it governs. While the Claude list is unreadable, OpenRouter still reprices the Claude models the catalogue holds, but no Claude model is added. A list is incomplete where it may be missing entries: OpenRouter's pages that do not add up to its `total_count`, or a Codex list served from the fallback bundled with the binary. That is detected when the models cache is older than the pass start minus Codex's 300-second cache TTL. An incomplete OpenRouter list changes nothing. An incomplete Codex list may still add models and set levels. Neither is evidence that a model is gone.

**A new model's identity is derived, not read from prose.**

| Maker | `id` | `family` | `aliases` | `provider` |
|---|---|---|---|---|
| Claude | `resolvedModel` without a bracketed serving selector such as `[1m]`; the `default` entry skipped | the list's `value` without that selector | that same value | `anthropic` |
| GPT | the list's `model` | the id's last hyphen-separated segment where it is alphabetic, else the id | none | `openai` |
| Grok | the OpenRouter id without `x-ai/` | `grok` | none | `spacexai` |

`reasoning_billed_as` is `output` for all three makers. A new model gets no capability seed and no `provider_says`. Its `released` is the date of the matched OpenRouter entry's `created`. Where OpenRouter was read completely and matches nothing, it is the date the pass first saw the model, so the newest release still wins its family's agent definitions. Where OpenRouter was not read completely, it stays null until a later pass fills it in. The pass also fills in a null `released` on an existing entry, and never changes one that is set. That is what keeps `grok-4.6`, shipped undated, the newest Grok once `grok-4.3` and `grok-4.5` arrive dated. Aliases are merged as a union and never removed.

**A harness id is matched to its OpenRouter entry by a slug, else by normalising the id.** Where the entry already carries an OpenRouter slug, that slug is used. Otherwise the pass prefixes the maker's namespace (`anthropic/`, `openai/`, `x-ai/`), removes a trailing `-YYYYMMDD`, turns a hyphen between two digits into a dot, and matches exactly against ids with no `:` suffix. `claude-haiku-4-5-20251001` becomes `anthropic/claude-haiku-4.5`. A match is written back as the entry's slug. A model with no match keeps the price it has, or is added unpriced and attributed to the first-party documentation of the list that established it. On 2026-09-11 that is `gpt-5.3-codex-spark`, and it is journalled once as having no price source.

**The price is OpenRouter's, per category.** Its per-token strings are converted to USD per million tokens with `decimal.Decimal`, rounded to six places, so float noise never journals a change. A category OpenRouter omits keeps the figure it had. The first override carrying `min_prompt_tokens` becomes `long_context_threshold` and the long-context card, and a category the override omits takes the new base price. Categories the catalogue has no field for, such as `input_cache_write_1h`, are ignored.

**Every change is journalled, and status only reads.** Each pass appends one row per changed field to `catalogue-journal.jsonl`: a model added, an alias added, a price, level, threshold, release date or slug that moved, and the first pass on which a model has no price source. Each row carries its old and new value and the source that said so. The pass writes its per-source outcome, `complete`, `incomplete` or `unreadable` with a reason, to `refresh.json` beside the journal. The pass also records there which models had no match, so a model still without one journals nothing on the next pass. `catalogue.py journal --days=7` prints both files and writes nothing. `/model-selector status` renders what it prints. There is no seen-marker, since a report that moved one would change what the next report says. After any write to the catalogue the generated agent definitions are resynced.

**Adoption still goes through the validator, hardened.** A price member must be null or a finite, non-negative number. Rate cards merge category by category, in the pass and in `adopt` alike, so an update that omits a category, or states it as null, never loses it.

## Why OpenRouter's price, and never its average

**One consistent source is worth more than a mix.** On 2026-09-11 OpenRouter listed `gpt-5.6-sol` at 2 / 0.2 / 2.5 / 10 USD per million tokens for input, cache read, cache write and output. The seed, and OpenAI's own page as recorded in `docs/research/model-and-price-facts-2026-09.md`, give 4 / 0.4 / 5 / 20. The maintainer chose OpenRouter as the one central source. What the selector needs is a price that orders the candidates, so one source for every model is worth more than a better figure for some of them. The first pass journals Sol's change from the seed's figures, and it stands. For the OpenRouter channel this price is the actual charge. For a subscription channel it is the cost measure, as ADR-0183 says, since a subscription's price per token is not published. A rate the user records on a channel still replaces it.

**The blended average is never used.** OpenRouter also reports a measured average price per model. The selector already prices each token category separately, from the user's own measured token mix. For Claude Code that mix is dominated by cache reads. An average blended over other people's mix counts the expensive categories again, and would roughly double the cost of such a Unit of Work. The maintainer had already removed the blended Grok rate from his own profile by hand.

## The alternatives

**Schedule today's `update`.** Rejected here, and not needed for these facts. An unattended agent reading web pages still has to be trusted to read numbers correctly, and structured sources make that trust unnecessary for models and prices. Plans remain `update`'s, since no structured source lists them.

**Use the providers' own pages as the price source, and OpenRouter as a fallback.** Rejected. That makes a mix of sources, and the mix is what breaks a comparison between models.

**An SDK for each harness.** Rejected. The Skill's scripts declare no dependencies. Both protocols are one or two JSON lines over stdio, and a test replays the recorded exchange, so a CLI change to that shape is found when the fixtures are next recorded.
