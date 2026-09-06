# Model, price and benchmark facts — September 2026

> Gathered 2026-09-06 against provider documentation and public leaderboards, as the input to Model Selector's rewrite. It records what was found and where; it decides nothing, and the decisions it fed are in `docs/adr/0182-how-a-model-is-chosen-and-how-the-choice-is-measured.md`. What of it binds anything is in `skills/models/model-selector/data/catalogue-seed.json`, which carries a source URL and a retrieval date on every fact it took. The rest is here because the unattended refresh has not been built against these feeds yet, and because a figure with a source beats the same figure remembered.

> Every price is USD per million tokens on the standard serving tier unless the row says otherwise, and seventeen items are marked unverified rather than filled in.

**Compiled:** 2026-09-06. **All retrieval dates in this document are 2026-09-06** unless a row says otherwise.
**Currency:** USD throughout. Prices are per million tokens (MTok) unless stated.

## How to read this document

Every figure carries a source. Sources are graded:

| Grade | Meaning |
|---|---|
| **P** | Primary — the provider's own documentation or pricing page. |
| **A** | Aggregator — OpenRouter's public models API. Mirrors first-party list price for the models cross-checked below, but it is a third party and can lag or diverge. |
| **L** | Local machine artefact — a cache or config file on this machine. Authoritative about *this machine's* configuration, not about the public product. |
| **unverified** | Could not be confirmed from any of the above. Treat as missing, not as zero. |

Where a figure is marked **unverified**, it is genuinely absent. Do not substitute a plausible number: a wrong price silently corrupts a routing decision, and an empty field fails loudly.


### Where each question is answered

| Brief | Section |
|---|---|
| 1. Model id, family, release date, pinned vs alias | §1.1 (Anthropic), §2.2 (OpenAI), §3.1 (xAI); compact in §0 |
| 2. Token prices by category + is reasoning billed as output | §1.2/§1.3, §2.3/§2.4, §3.2/§3.3; long-context tiers in §6.6 |
| 3. Reasoning/effort control, exact parameter and values | §1.4, §2.5, §3.4 |
| 4. Provider's own one-line "best for" (quoted) | §1.5, §2.6, §3.5 |
| 5. Subscription tiers and overage | §1.6, §2.7, §3.6 |
| 6. Machine-readable sources / unattended refresh | §6, with the verdict in §6.5 |
| 7. Benchmarks reporting cost-to-complete | §7 |
| 8. Exact launch invocations | §8 |
| What this machine is actually configured to run | Appendix A |
| Everything that could not be verified | Appendix B |

---

## 0. Seed table — current coding models, all three vendors

USD per million tokens, standard tier, short context. Retrieved 2026-09-06. `LC` = the long-context threshold above which the **whole request** re-prices. Effort parameter names differ per vendor — see the per-vendor sections.

| API model id | Vendor | Pinned? | In | Cache read | Cache write | Out | LC threshold | LC in/out | Effort values | Default |
|---|---|---|---|---|---|---|---|---|---|---|
| `claude-fable-5-1` | Anthropic | **yes** | 10 | **0.25** | 12.50 | 50 | none | — | low/medium/high/xhigh/max | high |
| `claude-opus-5` | Anthropic | **yes** | 5 | 0.50 | 6.25 | 25 | none | — | low/medium/high/xhigh/max | high |
| `claude-sonnet-5` | Anthropic | **yes** | 2 | 0.20 | 2.50 | 10 | none | — | low/medium/high/xhigh/max | high |
| `claude-haiku-4-5-20251001` | Anthropic | **yes** (alias `claude-haiku-4-5`) | 1 | 0.10 | 1.25 | 5 | none | — | **not supported** | — |
| `gpt-6-astra` | OpenAI | **no** | 10 | 1.00 | 12.50 | 50 | **272K** | 20 / 75 | low/medium/high/xhigh/max (**no `none`** → 400) | not stated |
| `gpt-5.6-sol` | OpenAI | **no** | **4** ⚠️promo | 0.40 | 5.00 | **20** | 272K | 8 / 30 | none/low/medium/high/xhigh/max | medium |
| `gpt-5.6-terra` | OpenAI | **no** | 2 | 0.20 | 2.50 | 12 | 272K | 4 / 18 | none/low/medium/high/xhigh/max | medium |
| `gpt-5.6-luna` | OpenAI | **no** | 0.20 | 0.02 | 0.25 | 1.20 | 272K | 0.40 / 1.80 | none/low/medium/high/xhigh/max | medium |
| `grok-4.6` | xAI | **no** | 2 | 0.50 | n/a | 6 | **200K** | 4 / 12 | low/medium/high/xhigh | high |
| `grok-4.5` | xAI | **no** | 2 | 0.30 | n/a | 6 | 200K | 4 / 12 | low/medium/high (xhigh silently → high) | high |
| `grok-4.3` | xAI | **no** | 1.25 | 0.20 | n/a | 2.50 | 200K | 2.50 / 5 | none/low/medium/high [A only] | disputed |
| `grok-build-0.1` | xAI | **yes** | 1 | 0.20 | n/a | 2 | 200K | 2 / 4 | likely none | — |

**Reasoning tokens are billed as output tokens by all three vendors.** Each states it in its own words (§1.3, §2.4, §3.3) — xAI's is inferred rather than quoted. This is the single most important shared fact: at `max`/`xhigh` effort the dominant cost is invisible tokens billed at the output rate.

**Five things a naive seed file gets wrong:**

1. **The long-context cliff is not marginal.** OpenAI: "priced at 2x input and 1.5x output **for the full request**." xAI: "billed at the higher rate for **all tokens in the request**." A 273k-token call to `gpt-6-astra` costs 2x a 271k-token one. Anthropic has no cliff at all — which inverts the ranking for repo-scale work.
2. **Only Anthropic pins every model id.** `gpt-6-astra`, the whole GPT-5.6 family, and `grok-4.6` have **no dated snapshot to pin to**. Any measured $/task recorded against those ids has a silent expiry.
3. **`gpt-5.6-sol`'s $4.00 is promotional** "at least through November 21, 2026".
4. **Cache economics are not uniform.** Anthropic prices two cache-write TTLs (5m at 1.25x, 1h at 2x) and gives Fable 5.1 a 0.025x read instead of the usual 0.1x. OpenAI charges cache writes on GPT-5.6+ only. xAI does not price cache writes at all.
5. **Effort vocabularies are not interchangeable.** Anthropic uses `output_config.effort` (nested); OpenAI uses `reasoning.effort`; xAI uses `reasoning_effort` (flat) or `reasoning.effort` (nested) depending on endpoint. `none` is valid on GPT-5.6 but a 400 on `gpt-6-astra`. `max` is valid on the API but rejected by `model_reasoning_effort` in the Codex CLI. `ultra` is a Codex mode, not an API effort.

---
## 1. Anthropic — Claude

### 1.1 Identity, release, pinning

Anthropic's own statement on pinning (grade P, `https://platform.claude.com/docs/en/about-claude/models/overview`, retrieved 2026-09-06):

> **Claude API ID:** Every Claude model ID is a pinned snapshot, including the dateless IDs used from the 4.6 generation on.

> **Claude API alias:** For models before the 4.6 generation, the alias is a convenience pointer that resolves to the dated ID. Dateless IDs are their own pinned snapshot; the alias row repeats them.

So for every current Claude model **the dateless id IS the pinned snapshot** — there is no mutable-alias problem to route around, except on Haiku 4.5, where `claude-haiku-4-5` is an alias for the dated `claude-haiku-4-5-20251001`.

| Model | API model id | Family | Alias or pinned | Release date | Context | Max output |
|---|---|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | Fable | Pinned snapshot (dateless) [P] | 2026-08-31 [A, inferred from OpenRouter `canonical_slug: anthropic/claude-fable-5.1-20260831`; Anthropic's own pages do not print a release date] | 1M | 128K |
| Claude Fable 5 | `claude-fable-5` | Fable | Pinned snapshot [P] | 2026-06-05 approx. [A, `anthropic/claude-fable-5` created 2026-06-05] | 1M | 128K |
| Claude Opus 5 | `claude-opus-5` | Opus | Pinned snapshot [P] | 2026-07-23/24 [A, `canonical_slug: anthropic/claude-opus-5-20260723`; corroborated by the Models API doc example showing `"created_at": "2026-07-24T00:00:00Z"` for `claude-opus-5`] | 1M | 128K |
| Claude Opus 4.8 | `claude-opus-4-8` | Opus | Pinned snapshot [P] | 2026-05-28 approx. [A] | 1M | 128K |
| Claude Sonnet 5 | `claude-sonnet-5` | Sonnet | Pinned snapshot [P] | 2026-06-30 [A, `canonical_slug: anthropic/claude-sonnet-5-20260630`] | 1M | 128K |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` (alias `claude-haiku-4-5`) | Haiku | **Dated snapshot + alias** [P] | 2025-10-01 (id date) | 200K | 64K |
| Claude Mythos 5.1 | `claude-mythos-5-1` | Mythos | Pinned snapshot [P] | unverified | 1M | 128K |

Mythos 5 / 5.1 are limited-availability (Project Glasswing, `https://anthropic.com/glasswing`) and are listed only for completeness — do not route to them by default.

Source for ids, context, max output, thinking mode, default effort: `https://platform.claude.com/docs/en/about-claude/models/overview` [P].
Source for lifecycle: `https://platform.claude.com/docs/en/about-claude/model-deprecations` [P]. That page publishes *retirement* dates ("not sooner than …"), not release dates — hence the release column leans on the aggregator's dated canonical slugs and is flagged as such.

Retirement commitments (Anthropic-operated platforms only) [P]: `claude-fable-5-1` not sooner than 2027-09-01; `claude-opus-5` 2027-07-24; `claude-sonnet-5` 2027-06-30; `claude-opus-4-8` 2027-05-28; `claude-haiku-4-5-20251001` **2026-10-15 — i.e. within six weeks of this compilation date.**

### 1.2 Token prices (per MTok, USD)

Source: `https://platform.claude.com/docs/en/about-claude/pricing` [P], retrieved 2026-09-06.

| Model | Input | Cache write 5m | Cache write 1h | Cache read (hit) | Output | Batch in/out |
|---|---|---|---|---|---|---|
| `claude-fable-5-1` | $10 | $12.50 | $20 | **$0.25** | $50 | $5 / $25 |
| `claude-mythos-5-1` | $10 | $12.50 | $20 | $0.25 | $50 | $5 / $25 |
| `claude-fable-5` | $10 | $12.50 | $20 | $1 | $50 | $5 / $25 |
| `claude-opus-5` | $5 | $6.25 | $10 | $0.50 | $25 | $2.50 / $12.50 |
| `claude-opus-4-8` | $5 | $6.25 | $10 | $0.50 | $25 | $2.50 / $12.50 |
| `claude-opus-4-7` | $5 | $6.25 | $10 | $0.50 | $25 | $2.50 / $12.50 |
| `claude-opus-4-6` | $5 | $6.25 | $10 | $0.50 | $25 | $2.50 / $12.50 |
| `claude-sonnet-5` | $2 | $2.50 | $4 | $0.20 | $10 | $1 / $5 |
| `claude-sonnet-4-6` | $3 | $3.75 | $6 | $0.30 | $15 | $1.50 / $7.50 |
| `claude-haiku-4-5-20251001` | $1 | $1.25 | $2 | $0.10 | $5 | $0.50 / $2.50 |

**Cache-read anomaly worth encoding.** Verbatim [P]:

> *Cache hits and refreshes on Claude Fable 5.1 and Claude Mythos 5.1 are priced at 0.025x the base input price. All other models use the standard 0.1x multiplier.*

So the multiplier is **not** uniform: 5m write = 1.25x input, 1h write = 2x input, read = 0.1x input **except** Fable 5.1 / Mythos 5.1 where read = 0.025x input. A tool that hardcodes 0.1x will overstate Fable 5.1 cache cost by 4x.

**Sonnet 5 price stability** — verbatim [P]:

> The $2/$10 per million input/output token pricing for Claude Sonnet 5, announced at launch as introductory pricing through August 31, 2026, is now the standard price. The previously scheduled increase to $3/$15 per million input/output tokens on September 1, 2026 will not occur.

This matters: a cached figure captured before 2026-09-01 may carry a stale scheduled increase.

**Tokenizer warning that breaks naive $/task comparison** — verbatim [P]:

> Claude 4.7 and later models and Claude Mythos Preview use a newer tokenizer that contributes to their improved performance on a wide range of tasks. This tokenizer produces approximately 30% more tokens for the same text. The exact increase depends on the content and workload shape. Claude Sonnet 4.6 and earlier models use the previous tokenizer.

Per-token price is therefore **not** comparable across the 4.6/4.7 tokenizer boundary, nor against other vendors, without a token-count correction.

**Multipliers that stack** [P]: `inference_geo: "us"` applies **1.1x** to every token category on Claude 4.6+. Batch API is **-50%** on input and output. Fast mode (research preview, Opus 5 / Opus 4.8, first-party API only) reprices to **$10 input / $50 output** and stacks with caching and residency multipliers.

**Long context:** no premium. Verbatim [P]: "Claude 4.6 and later models … include the full 1M token context window at standard pricing. (A 900k-token request is billed at the same per-token rate as a 9k-token request.)" — unlike xAI and some OpenAI tiers, there is no long-context surcharge to model.

### 1.3 Are reasoning tokens billed as output?

**Yes.** Verbatim [P], `https://platform.claude.com/docs/en/build-with-claude/thinking`, retrieved 2026-09-06:

> Thinking has a cost: the tokens Claude spends reasoning are billed as output tokens, even when the thinking text isn't returned to you, and they count toward `max_tokens` alongside the response text.

Note the second clause: on Fable 5.x / Opus 5 / Opus 4.8/4.7 / Sonnet 5 the default `thinking.display` is `"omitted"`, so the billed thinking tokens are **invisible in the response text**. Cost estimated from returned text alone will be systematically low.

### 1.4 Reasoning / effort control

**Exact parameter:** `output_config.effort` — a nested field on the request body, **not** top-level. GA, no beta header.
Source: `https://platform.claude.com/docs/en/build-with-claude/effort` [P].

**Exact allowed values:** `low`, `medium`, `high`, `xhigh`, `max`. Default is `high` on every model that supports it.

> Setting `effort` to `"high"` produces exactly the same behavior as omitting the `effort` parameter entirely.

Do **not** pass `adaptive` as an effort value — verbatim: "Don't pass `adaptive` as an `effort` value: `adaptive` is a thinking mode, not an effort level."

| Model id | `low` | `medium` | `high` | `xhigh` | `max` | Default |
|---|---|---|---|---|---|---|
| `claude-fable-5-1` | ✓ | ✓ | ✓ | ✓ | ✓ | `high` |
| `claude-fable-5` | ✓ | ✓ | ✓ | ✓ | ✓ | `high` |
| `claude-opus-5` | ✓ | ✓ | ✓ | ✓ | ✓ | `high` |
| `claude-opus-4-8` | ✓ | ✓ | ✓ | ✓ | ✓ | `high` |
| `claude-opus-4-7` | ✓ | ✓ | ✓ | ✓ | ✓ | `high` |
| `claude-opus-4-6` | ✓ | ✓ | ✓ | — | ✓ | `high` |
| `claude-sonnet-5` | ✓ | ✓ | ✓ | ✓ | ✓ | `high` |
| `claude-sonnet-4-6` | ✓ | ✓ | ✓ | — | ✓ | `high` |
| `claude-haiku-4-5` | **not supported** | | | | | n/a |

Verbatim caveat [P]: "Not every model that supports `max` supports `xhigh`." The `xhigh` row above is from the effort page's per-level availability lists; `claude-opus-4-5-20251101` also supports effort but only `low`/`medium`/`high`.

Full supported-model list, verbatim [P]: `claude-fable-5-1`, `claude-mythos-5-1`, `claude-fable-5`, `claude-mythos-5`, `claude-mythos-preview`, `claude-opus-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`, `claude-opus-4-5-20251101`, `claude-sonnet-5`, `claude-sonnet-4-6`.

Hard constraint to encode: on `claude-opus-5`, `thinking: {"type": "disabled"}` **returns 400 at `xhigh` or `max` effort** [P].

Effort is advisory, not a budget — verbatim [P]: "Effort is a behavioral signal, not a strict token budget."

Cache interaction that costs money if ignored [P]: changing top-level effort mid-conversation invalidates the prompt cache. On `claude-fable-5-1` / `claude-mythos-5-1` / `claude-opus-5` only, a per-message effort change (beta header `mid-conversation-output-config-2026-07-01`) preserves the cache.

### 1.5 Provider's own one-line "best for" (verbatim)

From the Description row of the comparison table at `https://platform.claude.com/docs/en/about-claude/models/overview` [P], retrieved 2026-09-06:

| Model | Anthropic's one-line description (verbatim) |
|---|---|
| Claude Fable 5.1 | "For demanding reasoning and long-horizon agentic work" |
| Claude Opus 5 | "For complex agentic coding and enterprise work" |
| Claude Sonnet 5 | "The best combination of speed and intelligence" |
| Claude Haiku 4.5 | "The fastest model with near-frontier intelligence" |

And the routing sentence Anthropic itself gives, verbatim [P]:

> If you're unsure which model to use, start with Claude Opus 5 for most workloads. Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5 at higher effort still fall short.

### 1.6 Anthropic subscription tiers

Sources: `https://claude.com/pricing` [P]; `https://support.claude.com/en/articles/8325606-what-is-the-pro-plan` [P]; `https://support.claude.com/en/articles/11049741-what-is-the-max-plan` [P]; `https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans` [P]; `https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan` [P]. All retrieved 2026-09-06.

**Headline finding: Anthropic publishes no absolute numeric allowance for any consumer tier.** Every published limit is a *relative multiplier* against the tier below, plus an undisclosed weekly cap. A recommender cannot compute "how many tasks fit in a Max 20x month" from public data — only relative headroom. This is a genuine gap, not a research failure.

| Tier | Price | Models | Stated allowance (verbatim where quoted) | Overage |
|---|---|---|---|---|
| Free | $0 | Sonnet, Haiku | No numeric limit published. | none — hard stop |
| Pro | $20/mo ($17/mo billed annually) — verbatim: "The Pro plan is available for $20 per month (US), with pricing in your local currency where supported." | Opus, Sonnet, Haiku; Fable **only via usage credits** | "At least five times the usage per session compared to our free service." Sessions reset every five hours; weekly limits "apply across all models". Includes Claude Code and Cowork. | Usage credits at standard API rates |
| Max 5x | $100/mo | + Fable up to 50% of weekly limit at no extra cost | "Max 5x provides five times more usage per session than the Pro plan." | Usage credits at standard API rates |
| Max 20x | $200/mo | as Max 5x | "Max 20x provides 20 times more usage per session than the Pro plan." | Usage credits at standard API rates |
| Team | $20/seat/mo standard; $100/seat/mo premium (annual) | premium seats get Fable at the 50% rule | standard: "more than Pro"; premium: "5x more usage than standard" | extra usage available |
| Enterprise | $20/seat/mo + usage at API rates (annual) | all models incl. Fable | "Admins set user and org spend limits" | usage-based, continuous |

**Overage mechanics** — verbatim [P]:
> Usage credits are billed at standard API rates.
> Usage credits apply to both Claude conversations and Claude Code terminal usage. Your combined usage across both interfaces counts toward your limits.

Purchased via Settings → Usage → Add funds (prepaid). Daily redemption limit $2000/day. Monthly spending cap configurable, or "Set to unlimited". Auto-reload available.

**Fable on a plan** — verbatim [P], `.../15424964-claude-fable-models-on-your-plan`:
> Claude Fable 5 and Claude Fable 5.1 are available on all paid plans (Pro, Max, Team, and Enterprise).
> You can use up to 50% of your weekly usage limits on Fable models at no extra cost — [Max plans, premium Team seats, premium Enterprise seats]
> your use of other models draws from the same usage limits and you can never use more than your weekly limit
> [Pro / standard Team:] Fable 5 and Fable 5.1 aren't included in your plan's usage limits. You can use them with usage credits, which let you pay for usage beyond what your plan includes.

The promotion giving 50% of the weekly limit on Fable 5 to *all* plans **ended 2026-07-19 23:59:59 PT** and applied to Fable 5 only [P, via search snippet of the same article]. A seed file carrying the promo terms is stale.

**Discretionary throttling** — verbatim [P], Max plan article:
> In addition, to manage capacity and ensure fair access to all users, we may limit your usage in other ways, such as weekly and monthly caps or model and feature usage, at our discretion.

Encode this as: subscription allowances are **not a contractual quantity** and must not be used as a hard budget in a router.

---
## 2. OpenAI — GPT

**Documentation has moved.** `platform.openai.com/docs/*` now **301-redirects** to `developers.openai.com/api/docs/*`, and `developers.openai.com/codex` **308-redirects** to `learn.chatgpt.com/docs`. Separately, `openai.com/*`, `chatgpt.com/*` and `help.openai.com/*` return **HTTP 403** to automated fetches — anything that would have come from those is marked unverified below rather than sourced from a blog.

### 2.1 The four config strings on this machine — verdict

| String | Verdict |
|---|---|
| `gpt-6-astra` | **Real, currently-served OpenAI API model id.** Flagship, released 2026-09-03. Also a valid Codex CLI value. |
| `gpt-5.6-sol` | **Real, currently-served API model id.** Also reachable via the mutable alias `gpt-5.6`. |
| `gpt-5.6-terra` | **Real, currently-served API model id.** |
| `gpt-5.6-luna` | **Real, currently-served API model id.** |

None is Codex-CLI-only; none is a dated snapshot. All four appear in `https://developers.openai.com/api/docs/models` [P], retrieved 2026-09-06.

### 2.2 Identity, release, pinning

| API model id | Family | Released | Pinned or alias | Context | Max output |
|---|---|---|---|---|---|
| `gpt-6-astra` | GPT-6 | **2026-09-03** [P, changelog] | Undated id. Page says "Default snapshot: `gpt-6-astra`" and the snapshot list contains only itself — **no dated snapshot exists**, so it is mutable in practice | 1,050,000 | 128,000 |
| `gpt-5.6-sol` | GPT-5.6 | **2026-07-09** [P] | Same shape; also the target of the `gpt-5.6` alias | 1,050,000 | 128,000 |
| `gpt-5.6-terra` | GPT-5.6 | 2026-07-09 [P] | Same shape | 1,050,000 | 128,000 |
| `gpt-5.6-luna` | GPT-5.6 | 2026-07-09 [P] | Same shape | 1,050,000 | 128,000 |
| `gpt-5.6` | alias | — | **Mutable alias.** Verbatim: "The `gpt-5.6` alias routes requests to GPT-5.6 Sol." | — | — |
| `gpt-5.5` | GPT-5.5 | unverified | **True alias** → default snapshot `gpt-5.5-2026-04-23` | 1,050,000 | — |
| `gpt-5.3-codex-spark` | Codex preview | unverified | Codex/ChatGPT-only; **not in the API docs or pricing page**. Verbatim: "Text-only research preview model optimized for near-instant, real-time coding iteration. Available to ChatGPT Pro users." | 128,000 [L] | — |

**Pinning finding, same shape as xAI's:** `gpt-6-astra` and the whole GPT-5.6 family have **no dated snapshot to pin to**. `gpt-5.5` does (`gpt-5.5-2026-04-23`). So of the three vendors, only Anthropic gives a pinned id for every current model. A recorded benchmark result keyed to `gpt-6-astra` has a silent expiry.

**OpenRouter's dated slugs are not OpenAI ids.** OpenRouter publishes `canonical_slug: openai/gpt-6-astra-20260903` and `openai/gpt-5.6-{sol,terra,luna}-20260709` [A]. Those strings do **not** exist as OpenAI API ids — OpenRouter appears to have synthesised them from real release dates. Never emit one as a model id.

**All `*-codex` models are retired.** From `https://developers.openai.com/api/docs/deprecations` [P], section "2026-04-22: Legacy GPT model snapshots (July 2026 shutdown)":

| Model | Shutdown | Replacement |
|---|---|---|
| `gpt-5.3-codex`, `gpt-5.2-codex`, `gpt-5.1-codex`, `gpt-5.1-codex-max`, `gpt-5-codex` | 2026-07-23 | `gpt-5.6-sol` |
| `gpt-5.1-codex-mini` | 2026-07-23 | `gpt-5.6-terra` |
| `codex-mini-latest` | 2026-02-12 | `gpt-5-codex-mini` |

⚠️ **Unresolved contradiction in OpenAI's own docs.** `gpt-5.3-codex` is listed as shut down 2026-07-23, yet it still has a live model page and a live pricing row ($1.75 in / $0.175 cached / $14.00 out, Responses API only). The same shape applies to `gpt-5.4` / `gpt-5.4-mini`, which Codex docs say "retire from Codex on August 31, 2026" (already past) but which remain on the API pricing page with no API deprecation entry. **Treat all of them as retired and do not route to them**; the only way to settle it is an authenticated `GET /v1/models`, which reports `shutdown_date`.

### 2.3 Token prices (per MTok, USD)

Source: `https://developers.openai.com/api/docs/pricing.md` [P], retrieved 2026-09-06. Page header: "Prices per 1M tokens." Currency USD.

**I re-fetched this URL directly with `curl` to confirm it first-hand:** HTTP 200, 21,424 bytes, `content-type: text/markdown; charset=utf-8`, no authentication. The file contains four cleanly labelled rate tables — `### Standard pricing data`, `### Batch pricing data`, `### Flex pricing data`, `### Fast pricing data` — each with the same nine-column header (`Model | Short context input | Short context cached input | Short context cache writes | Short context output | Long context input | ... | Long context output`). This is the single most parseable price source found across all three vendors.

**Standard tier:**

| Model | Input | Cached input | Cache write | Output | LC input | LC cached | LC write | LC output |
|---|---|---|---|---|---|---|---|---|
| `gpt-6-astra` | $10.00 | $1.00 | $12.50 | $50.00 | **$20.00** | $2.00 | $25.00 | **$75.00** |
| `gpt-5.6-sol` | **$4.00** | $0.40 | $5.00 | **$20.00** | $8.00 | $0.80 | $10.00 | $30.00 |
| `gpt-5.6-terra` | $2.00 | $0.20 | $2.50 | $12.00 | $4.00 | $0.40 | $5.00 | $18.00 |
| `gpt-5.6-luna` | $0.20 | $0.02 | $0.25 | $1.20 | $0.40 | $0.04 | $0.50 | $1.80 |
| `gpt-5.5` | $5.00 | $0.50 | — | $30.00 | $10.00 | $1.00 | — | $45.00 |
| `gpt-5.4` | $2.50 | $0.25 | — | $15.00 | $5.00 | $0.50 | — | $22.50 |

**LC = long context, i.e. prompts above 272,000 input tokens.** Verbatim [P], per-model pages:

> Prompts with >272K input tokens are priced at 2x input and 1.5x output for the full request.

and for astra specifically:

> Prompts with more than 272K input tokens are priced at 2x input and cache rates and 1.5x output for the full request.

Note **"for the full request"** — like xAI, this is not marginal. Crossing 272k re-prices every token in the call.

**Cache writes are real and OpenAI's own, not an aggregator construct.** Verbatim [P] `https://developers.openai.com/api/docs/guides/prompt-caching`:

> Cache writes are billed at 1.25x the uncached input token rate.
> For GPT-5.6 and later, cache writes cost 1.25× the standard, uncached input-token rate.
> A cached prefix remains eligible for reuse for 30 minutes after its most recent write or reuse, though OpenAI may retain it longer.

Cache-write billing applies to **GPT-5.6 and later only** — `gpt-5.5` and `gpt-5.4` show "—" in those columns. A cost model that applies a 1.25x write charge to `gpt-5.5` will overcharge.

**Service tiers change the rate table** [P]:

| Tier | Effect |
|---|---|
| Batch | ≈50% of standard — astra $5.00 / $0.50 / $6.25 / $25.00; sol $2.00 / $0.20 / $2.50 / $10.00 |
| Flex (`service_tier="flex"`) | "Tokens are priced at Batch API rates" — identical numbers to Batch |
| Fast (`service_tier="fast"`) | exactly 2x Standard. Read directly from the Fast table: astra $20.00 / $2.00 / $25.00 / $100.00; sol $8.00 / $0.80 / $10.00 / $40.00; terra $4.00 / $0.40 / $5.00 / $24.00; luna $0.40 / $0.04 / $0.50 / $2.40 |
| Data residency | "Regional processing (data residency) endpoints are charged a 10% uplift for models released on or after March 5, 2026…" |

Batch and Flex rows are byte-identical in the file (astra $5.00 / $0.50 / $6.25 / $25.00), consistent with the Flex guide's "Tokens are priced at Batch API rates".

**Incidental find worth flagging:** the same file documents a "Daybreak program" with two mutable aliases — verbatim, "`gpt-daybreak-blue-latest` and `gpt-daybreak-red-latest` are aliases that currently point to `gpt-5.6-sol` and `gpt-5.6-cyber`, respectively. As new models are released through the Daybreak program, these aliases will be updated to point to the latest…". A fifth current model id, `gpt-5.6-cyber`, therefore exists. I checked `models.md` directly [P]: it is **out of scope for general coding** — "GPT-5.6 Cyber: Our most advanced cybersecurity model for authorized vulnerability research and security testing." The two Daybreak aliases are described as "An alias for flagship general-purpose models with safeguards for defensive cybersecurity work" (Blue) and "An alias for advanced cybersecurity models for authorized vulnerability research and security testing" (Red). Both are **mutable aliases by design** and must never be pinned. Prices for `gpt-5.6-cyber`: **unverified** (not in the rows I read).

⚠️ **`gpt-5.6-sol`'s $4.00 is promotional.** Verbatim [P], pricing.md: "GPT-5.6 Sol's promotional pricing is available at least through November 21, 2026." Seed data must carry that expiry, or the tool will keep recommending sol on a price that has lapsed.

### 2.4 Are reasoning tokens billed as output?

**Yes, explicitly.** Verbatim [P] `https://developers.openai.com/api/docs/guides/reasoning`, retrieved 2026-09-06:

> While reasoning tokens are not visible via the API, they still occupy space in the model's context window and are billed as output tokens.

Consequence: `max` effort on `gpt-6-astra` bills invisible reasoning at **$50/MTok** standard, **$75/MTok** above 272k, **$100/MTok** in Fast mode. All three vendors bill reasoning at the output rate — that is the one thing they agree on.

### 2.5 Reasoning / effort control

**Exact API parameter:** `reasoning.effort` (nested object) on the Responses API.

| Model | Allowed values | Accepts `none`? | Default |
|---|---|---|---|
| `gpt-6-astra` | `low`, `medium`, `high`, `xhigh`, `max` | **No** — verbatim: "GPT-6 Astra does not support `none` reasoning effort. Setting `reasoning.effort`… to `none` returns HTTP 400." | not stated |
| `gpt-5.6-sol` / `-terra` / `-luna` | verbatim: "Reasoning.effort supports: none, low, medium (default), high, xhigh, and max." | Yes | `medium` |
| `gpt-5.5` | `none`, `low`, `medium` (default), `high`, `xhigh` — **no `max`** | Yes | `medium` |

Global statement [P] `https://developers.openai.com/api/docs/guides/reasoning`: "Supported values are model-dependent and can include `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`." **`minimal` is in the global set but listed by none of the four current models** — it looks legacy (GPT-5/5.1 era). Which models still accept it: **unverified**.

**Codex CLI vocabulary diverges from the API's.** From `https://learn.chatgpt.com/docs/config-file/config-reference` [P]:

| Key | Values |
|---|---|
| `model_reasoning_effort` | `minimal` \| `low` \| `medium` \| `high` \| `xhigh` — **no `max`, no `none`** |
| `plan_mode_reasoning_effort` | `none` \| `minimal` \| `low` \| `medium` \| `high` \| `xhigh` |
| `model_reasoning_summary` | `auto` \| `concise` \| `detailed` \| `none` |

So the API accepts `max` and the CLI does not; astra rejects `none` and the CLI never offers it. **A single "effort" value cannot be passed blindly to both surfaces.**

⚠️ **`ultra` is not an API effort value.** The local Codex model cache lists `ultra` as a supported reasoning level on `gpt-6-astra`, `gpt-5.6-sol` and `gpt-5.6-terra`, glossed "Maximum reasoning with automatic task delegation" [L]. In OpenAI's Codex documentation `ultra` is a **mode**, not an effort: "Ultra uses subagents to handle separate parts of a complex task in parallel." It does not appear in the API's effort enum, nor in `model_reasoning_effort`. **Do not send `effort=ultra` to the API.** Treat it as a Codex-client execution topology.

### 2.6 OpenAI's own one-line statement (verbatim)

Two official sets exist and they differ. Both retrieved 2026-09-06.

| Model | API docs (`developers.openai.com/api/docs/models`) | Codex docs (`learn.chatgpt.com/docs/models.md`) |
|---|---|---|
| `gpt-6-astra` | "Our most capable model, built for the hardest end-to-end work" | "Our most capable model for complex work across code, apps, and research, combining advanced reasoning, computer use, and stronger judgment." |
| `gpt-5.6-sol` | "Flagship model for complex professional work" | "The most capable GPT-5.6 model for complex coding, computer use, research, and cybersecurity." |
| `gpt-5.6-terra` | "GPT-5.6 model that balances intelligence and cost" | "Balanced GPT-5.6 model for everyday work, with performance competitive with GPT-5.5 at a lower cost." |
| `gpt-5.6-luna` | "GPT-5.6 model optimized for cost-sensitive workloads" | "Fast and affordable GPT-5.6 model that delivers strong capability at the lowest cost in the family." |
| `gpt-5.5` | "A new class of intelligence for coding and professional work." | — |

Coding-specific, verbatim [P] `https://developers.openai.com/api/docs/guides/latest-model`:
> GPT-6 Astra is our most intelligent model yet, with state-of-the-art performance in computer use, browsing, software engineering, science, and professional work.

The local Codex cache carries a third, shorter set [L] — "Our most capable model for complex, demanding work." (astra), "Reliable agentic workhorse for everyday tasks." (sol), "Balanced agentic coding model for everyday work." (terra), "Fast and affordable agentic coding model." (luna). Three official wordings for the same model; pick one source and stay with it.

### 2.7 OpenAI subscription tiers

Source: `https://learn.chatgpt.com/docs/pricing.md` [P], retrieved 2026-09-06. `help.openai.com` is 403 to automated fetches, so ChatGPT *chat* message limits (the "160 messages every 3 hours" style figures) are **unverified** and deliberately omitted.

| Plan | Price | Includes |
|---|---|---|
| Free | $0/mo | "Explore Codex capabilities on quick coding tasks" |
| Go | $8/mo | "Use Codex for lightweight coding tasks" |
| Plus | $20/mo | "Codex on the web, in the CLI, in the IDE extension, and on iOS"; GPT-5.6 family |
| Pro 5x | from $100/mo | "5x or 20x more Codex usage than Plus"; GPT-5.3-Codex-Spark preview |
| Pro 20x | $200/mo | as above + unlimited ChatGPT Voice |
| Business | $20/user/mo — verbatim: "*2+ users, billed annually. $25 per user per month when billed monthly.*" | ChatGPT + Codex, SAML SSO, MFA |
| Enterprise / Edu | "Contact sales" | priority processing, residency controls |
| API key | usage-based | "Pay for Codex usage based on API pricing" |

**There is no separate Codex subscription** — Codex is bundled into every ChatGPT plan.

**Codex usage estimates — note the disclaimer.** Verbatim header [P]: "The estimates below show local messages per five-hour period. Cloud chats on ChatGPT plans use GPT-5.6 Sol and may use more of your allowance than local messages. **These estimates are not fixed message limits.**"

| Model | Plus | Pro 5x | Pro 20x |
|---|---|---|---|
| GPT-6 Astra | 5–45 | 25–225 | 100–900 |
| GPT-5.6 Sol | 10–100 | 50–500 | 200–2,000 |
| GPT-5.6 Terra | 25–200 | 125–1,000 | 500–4,000 |
| GPT-5.6 Luna | 250–2,000 | 1,250–10,000 | 5,000–40,000 |

Footnotes verbatim: "Local messages and cloud chats share your plan's usage allowance. **Weekly limits may also apply.**" · "For Enterprise/Edu users with flexible pricing, there are no fixed rate limits—usage scales with credits."

This is still the most numerically informative consumer disclosure of the three vendors — Anthropic publishes only multipliers, xAI only "a weekly usage allowance" — but the ranges span roughly 9x, so they cannot carry a budget.

**Overage — verbatim** [P]:
> ChatGPT Plus and Pro users who reach their usage limit can purchase additional credits to continue working without needing to upgrade their existing plan.
> If you are approaching usage limits, you can also switch to a smaller model to make your usage limits last longer.
> All users may also run extra local chats using an API key, with usage charged at standard API rates.
> If you reach your usage limits during an active turn, the agent will be able to continue working on that turn, subject to fair use limits.

So: credit top-up, voluntary model downgrade, or BYO API key at standard rates — **not** a hard cutoff. Enterprise without credits: "Features pause until credits become available."

**Credit rate card (credits per 1M tokens)** [P]:

| Model | Input | Cached | Output |
|---|---|---|---|
| GPT-6 Astra | 250 | 25 | 1,250 |
| GPT-5.6 Sol | 100 | 10 | 500 |
| GPT-5.6 Terra | 50 | 5 | 300 |
| GPT-5.6 Luna | 5 | 0.5 | 30 |

Footnote: "GPT-5.6 usage averages 5-30 credits per message."

⚠️ **The USD price of a credit is unverified.** No reachable page states pack sizes or prices. Dividing the credit card by the USD price card yields a consistent 25 credits = $1.00 across all five models on both input and output — but that is arithmetic on two OpenAI tables, **not an OpenAI statement**. Do not route on it.

---
## 3. xAI — Grok

**Branding: the rename is real and first-party confirmed.** `https://x.ai/news/xai-joins-spacex` [P], retrieved 2026-09-06, states "SpaceX announced today that it has acquired xAI", dated **2026-02-02**, and the page is branded **"SpaceXAI LLC"**. So "SpaceXAI" in `docs.x.ai` and in OpenRouter display names is a genuine vendor rename, not a mislabel.

**But the authoritative domain is unchanged: `x.ai` / `docs.x.ai`.** Every API path, doc page and model card is still there; the base URL is still `https://api.x.ai`; the OpenRouter id prefix is still `x-ai/`. No `spacex.com` API surface was found. Branding change, not a domain migration — key on ids, never display names.

**Fetch caveat, and it is selective:** `x.ai/pricing`, `x.ai/grok`, `x.ai/api` and `grok.com/plans` return **HTTP 403** to non-browser clients (Cloudflare). `x.ai/news/*` and all of `docs.x.ai/*` fetch fine. The blocked pages are exactly the ones carrying consumer subscription prices, so **no xAI tier price is verified in this document** (§3.6).

### 3.1 Identity, release, pinning — the reproducibility problem

Aliasing convention, verbatim from `https://docs.x.ai/developers/models` [P], retrieved 2026-09-06:

> `<modelname>` is aliased to the latest stable version. `<modelname>-latest` is aliased to the latest version… `<modelname>-<date>` refers directly to a specific model release. This will not be updated.

| Model id | Family | Alias or pinned | Released | Context | Notes |
|---|---|---|---|---|---|
| `grok-4.6` | Grok 4.x | **MUTABLE — no dated pin published** | 2026-08-12 [A] | 500K | flagship; the bare name is a moving target |
| `grok-4.5` | Grok 4.x | Mutable; aliases `grok-4.5-latest`, `grok-build-latest` | 2026-07-08 [A] | 500K | |
| `grok-4.3` | Grok 4.x | Mutable; alias `grok-4.3-latest` | 2026-04-30 [A] | 1M | |
| `grok-build-0.1` | Grok Build | **Pinned** (version in id); aliases `grok-code-fast-1`, `grok-code-fast`, `grok-code-fast-1-0825` | 2026-05-20 [A] | 256K | agentic coding model |
| `grok-4.20-0309-reasoning` | Grok 4.20 | **Pinned** (dated) | 2026-03-31 [A] | 1M | |
| `grok-4.20-0309-non-reasoning` | Grok 4.20 | Pinned | 2026-03-31 [A] | 1M | |
| `grok-4.20-multi-agent-0309` | Grok 4.20 | Pinned | 2026-03-31 [A] | 1M | |

**The finding that matters most for a routing tool: `grok-4.6` has no published dated snapshot.** There is no reproducible pinned id for xAI's flagship. A run recorded as "grok-4.6" today is not guaranteed to be the same weights next month, so any measured $/task attached to that id has a silent expiry. Anthropic pins every id; OpenAI publishes a `Default snapshot` per model; xAI does not, for its flagship.

Release dates are **day-precise only via OpenRouter's `created` field [A]** — xAI's release notes give month granularity. Flagged as aggregator-derived.

**A caught aggregator error, worth recording as a calibration datum.** OpenRouter lists `x-ai/grok-4.20` and `x-ai/grok-4.20-multi-agent` at `context_length: 2000000`. xAI's own `https://docs.x.ai/developers/models` and the per-model cards both say **1,000,000**. xAI is right; OpenRouter is wrong by 2x. Same feed that matched xAI's prices to the cent gets a context window wrong — so the feed's *fields* have to be trusted individually, not wholesale.

**Retired 2026-05-15 12:00 PM PT** — `https://docs.x.ai/developers/migration/may-15-retirement` [P]. Do not route to these; they survive only as redirects: `grok-code-fast-1` → `grok-build-0.1`; `grok-4-1-fast-reasoning`, `grok-4-fast-reasoning`, `grok-4-0709` → `grok-4.3` at `low` effort; `grok-4-1-fast-non-reasoning`, `grok-4-fast-non-reasoning`, `grok-3` → `grok-4.3` at `none` effort. **"Grok Code Fast" and "Grok 4.x Fast" no longer exist as live models**, though OpenRouter still lists them (priceless) in its catalogue.

### 3.2 Token prices (per MTok, USD)

Source: `https://docs.x.ai/developers/pricing` and `https://docs.x.ai/developers/models` [P], retrieved 2026-09-06. Currency USD, confirmed on the page. Independently reconciled against OpenRouter's per-token figures [A] — **exact match on every row including the override tier.**

| Model | Ctx | Input <200K | Cached in <200K | Output <200K | Input ≥200K | Cached in ≥200K | Output ≥200K |
|---|---|---|---|---|---|---|---|
| `grok-4.6` | 500K | $2.00 | $0.50 | $6.00 | **$4.00** | **$1.00** | **$12.00** |
| `grok-4.5` | 500K | $2.00 | $0.30 | $6.00 | $4.00 | $0.60 | $12.00 |
| `grok-4.3` | 1M | $1.25 | $0.20 | $2.50 | $2.50 | $0.40 | $5.00 |
| `grok-4.20-0309-reasoning` | 1M | $1.25 | $0.20 | $2.50 | $2.50 | $0.40 | $5.00 |
| `grok-4.20-0309-non-reasoning` | 1M | $1.25 | $0.20 | $2.50 | $2.50 | $0.40 | $5.00 |
| `grok-4.20-multi-agent-0309` | 1M | $1.25 | $0.20 | $2.50 | $2.50 | $0.40 | $5.00 |
| `grok-build-0.1` | 256K | $1.00 | $0.20 | $2.00 | $2.00 | $0.40 | $4.00 |

This table was independently confirmed twice: once against `docs.x.ai` prose and once against OpenRouter's `pricing.overrides[]` array. They agree to the cent, including the override tier.

**The long-context trap, verbatim** [P] `https://docs.x.ai/developers/pricing`:

> Requests whose prompt reaches the listed token threshold are billed at the higher rate for **all tokens in the request**.

It is **not marginal pricing.** Crossing 200,000 prompt tokens doubles the bill for the entire request, output included. A 201k-token request costs exactly twice a 199k-token one.

**Cache write: not separately priced.** xAI publishes no cache-write line. OpenRouter shows no `input_cache_write` key on any xAI-hosted endpoint (the Bedrock endpoint carries `"input_cache_write": "0"`). Encode cache-write cost as **zero/absent** for xAI, not as unknown.

**Batch:** "Batch API requests are billed at a 20% discount to standard rates" [P] — on `grok-4.3` and `grok-4.20-*`. But **`grok-4.6` and `grok-build-0.1` both say "Batch API: Not supported"** [P]. No batch lever on the flagship.

**Web search:** $0.005 per search [A, OpenRouter endpoints]. **Per-response cost field:** `cost_in_usd_ticks`, where "10'000'000'000 ticks = 1 dollar"; `cost_in_nano_usd` on `/v1/responses` [P, REST chat reference] — xAI is the only one of the three that returns the dollar cost of a call in the response itself. That is directly useful for measuring $/task.

### 3.3 Are reasoning tokens billed as output?

**Almost certainly yes — but xAI never says the word "output", so this is graded as inference, not fact.**

What is actually on the page [P]:
> When you use a reasoning model, the reasoning tokens are billed as part of your total consumption. — `https://docs.x.ai/docs/guides/reasoning`

And `reasoning_tokens` is nested inside `completion_tokens_details` (and `output_tokens_details` on `/v1/responses`) in the REST reference [P].

The nesting under *completion*/*output* implies the completion rate, and there is no separate reasoning price on xAI or in OpenRouter's `internal_reasoning` field for xAI endpoints. **Inferred, not quoted.** For `grok-4.6` above 200k that means **$12.00/MTok for thinking you never see.**

### 3.4 Reasoning / effort control

| Endpoint | Exact parameter | Allowed values |
|---|---|---|
| `POST /v1/chat/completions` | `reasoning_effort` (flat string) | `"none"`, `"low"`, `"medium"`, `"high"`, `"xhigh"` |
| `POST /v1/responses` | `reasoning.effort` (nested object) | same five |

Source: `https://docs.x.ai/developers/rest-api-reference/inference/chat` and `https://docs.x.ai/docs/guides/reasoning` [P], retrieved 2026-09-06. Default: "If not specified, `reasoning_effort` defaults to `"high"`."

| Model | Accepted effort | What effort actually does |
|---|---|---|
| `grok-4.6` | `low`, `medium`, `high` (default), `xhigh` | reasoning depth; "`xhigh` is available on `grok-4.6` and later" |
| `grok-4.5` | `low`, `medium`, `high` (default) | verbatim: "On models that do not support it, such as `grok-4.5`, requests with `"xhigh"` are treated as `"high"`" — **silently downgraded, not rejected** |
| `grok-4.20-multi-agent` | `low`, `medium`, `high`, `xhigh` | **"Controls agent count"**, not reasoning depth — effort buys parallel agents here |
| `grok-4.3` | ⚠️ OpenRouter reports `none`/`low`/`medium`/`high` with default `low` [A] — **stated on no xAI page.** xAI's reasoning guide never mentions `grok-4.3` at all | — |
| `grok-build-0.1` | **likely none** — OpenRouter's `supported_parameters` omits `reasoning_effort` while 4.6/4.5/4.3 all include it | — |

Level semantics, verbatim [P]: Low — "Uses some reasoning tokens, but still fast"; Medium — "More thinking for less-latency sensitive applications"; High — "Uses more reasoning tokens for deeper thinking"; XHigh — "Maximum reasoning depth, with correspondingly higher latency".

**Two failure modes to encode:**
1. **Endpoint-dependent rejection vs downgrade.** `/v1/responses`: effort is "Supported by some models; models that do not support it reject the request". `/v1/chat/completions`: "(Not supported by reasoning models)". Same value, different failure.
2. **Unresolved contradiction.** The reasoning guide says "Reasoning cannot be disabled", yet the chat API enum includes `"none"` and the retirement page maps `grok-3` → "`grok-4.3` with `none` reasoning effort". Best reading: `none` is valid on `grok-4.3`, refused on `grok-4.6`. **Unverified per model — test before relying on it.**
3. **xAI's reasoning guide documents only `grok-4.6`, `grok-4.5` and `grok-4.20-multi-agent`.** Everything known about `grok-4.3`'s and `grok-build-0.1`'s effort handling comes from an aggregator or from inference. **Send `reasoning_effort` explicitly on every call rather than trusting any documented default** — the guide says the default is `high`, OpenRouter says `grok-4.3` defaults to `low`, and no xAI page settles it.

### 3.5 xAI's own one-line statement (verbatim)

| Model | Quote | URL |
|---|---|---|
| `grok-4.6` | "Grok 4.6 is SpaceXAI's frontier model built for coding, agentic tasks, and knowledge work." | `https://docs.x.ai/developers/grok-4-6` |
| `grok-4.6` (model card) | "SpaceXAI's frontier model for coding, agentic tasks, and knowledge work." | `https://docs.x.ai/developers/models/grok-4.6` |
| `grok-4.5` | "SpaceXAI's intelligent coding model for agentic software, engineering, and workflow tasks." | `https://docs.x.ai/developers/models/grok-4.5` |
| `grok-4.3` | "Fast, reliable model with strong tool calling and instruction following capabilities." | `https://docs.x.ai/developers/models/grok-4.3` |
| `grok-build-0.1` | "SpaceXAI's intelligent coding model for agentic software, engineering, and workflow tasks." | `https://docs.x.ai/developers/models/grok-build-0.1` |
| `grok-build-0.1` (release notes) | "xAI's coding model, trained specifically for agentic coding workflows." | `https://docs.x.ai/developers/release-notes` |
| `grok-4.20-multi-agent-0309` | "Multiple agents collaborate in parallel to perform deep research tasks." | `https://docs.x.ai/developers/models/grok-4.20-multi-agent-0309` |

⚠️ `grok-4.5` and `grok-build-0.1` return an **identical** sentence from two separate URLs. Consistent with the shared `grok-build-latest` alias, but verify by eye before quoting either publicly.

**Unresolved alias conflict:** the `grok-4.5` card lists `grok-build-latest` as one of its aliases, while `https://docs.x.ai/build/overview` says "The same model that powers Grok Build, `grok-4.6`, is also available directly on the xAI API." Do not rely on `grok-build-latest` resolving to either — resolve it at runtime from the `aliases[]` array in §6.

Knowledge cutoff, verbatim [P]: "The knowledge cut-off date of Grok 4.6 is February 1, 2026." Max output for `grok-4.6`: "No text output limit" [P]; OpenRouter reports `max_completion_tokens: 450000` [A].

### 3.6 xAI subscription tiers — could not be verified

**Every consumer price below is unverified.** `x.ai/pricing` and `grok.com/plans` both returned **HTTP 403**. Tier *names* appear in `https://docs.x.ai/grok/faq` [P]: Free, SuperGrok Lite, SuperGrok, SuperGrok Plus, SuperGrok Heavy, and X Premium / X Premium+ bundling. Third-party figures for SuperGrok Heavy disagree with each other ($300/mo vs $100/mo) and are **not** reproduced here.

What *is* verified, verbatim from `https://docs.x.ai/grok/faq` [P], retrieved 2026-09-06:

> Rolling out in June 2026, Grok will now use a simpler, more flexible system for paid users — One flexible weekly usage pool that works across all Grok products
> a weekly usage allowance included with your subscription
> Different products cost different amounts depending on how much compute that product requires
> You can purchase Extra Usage Credits to instantly continue usage · You can upgrade to a higher plan for a larger weekly allowance · You can turn on Auto Top Up

And from `https://docs.x.ai/grok/overview` [P]: "Paid SuperGrok plans raise your limits and unlock more across every product, drawing from a single weekly usage allowance you can spend however you like."

**Consumer plans are not metered per token and share no billing surface with the API.** A subscription tier cannot substitute for API spend in a routing cost model — the same is true of Anthropic's plans (§1.6). This is worth encoding explicitly: the tool must not net subscription capacity against API dollars.

### 3.7 xAI machine-readable endpoints — and they ship prices

Source: `https://docs.x.ai/developers/rest-api-reference/inference/models` [P], retrieved 2026-09-06. Base URL `https://api.x.ai`.

| Endpoint | Auth | Prices? | Fields |
|---|---|---|---|
| `GET /v1/models` | Bearer, **required** | **Yes** | `id`, `aliases`, `created`, `owned_by`, `context_length`, `prompt_text_token_price`, `completion_text_token_price`, `cached_prompt_text_token_price`, `prompt_image_token_price`, `*_long_context` variants, **`long_context_threshold`**, `image_price` |
| `GET /v1/models/{model_id}` | required | Yes | same, single object |
| `GET /v1/language-models` | required | **Yes** | the above **plus** `version`, `fingerprint`, `input_modalities`, `output_modalities`, `search_price`. Docs: "List all chat and image understanding models available to the authenticating API key" |
| `GET /v1/image-generation-models` | required | Yes | `image_price`, `pricing[]` by quality/resolution |
| `GET /v1/video-generation-models` | required | **No** | — |

**Price unit — read this before dividing anything.** Verbatim [P]: "Price of the prompt text token in USD cents per 100 million tokens." So **$/MTok = value ÷ 10,000**. Cross-checked against the documented sample response: `prompt_text_token_price: 12500` → $1.25/MTok, which matches `grok-4.3`. Confirmed, not inferred.

Two fields make xAI the best-structured of the three for this purpose: `long_context_threshold` makes the 200k cliff machine-readable instead of prose to be parsed, and `aliases[]` resolves the `grok-build-latest` ambiguity programmatically.

Probed unauthenticated on this machine 2026-09-06: `GET https://api.x.ai/v1/models` and `GET https://api.x.ai/v1/language-models` both return **HTTP 401** `{"code":"unauthenticated:no-credentials","error":"No credentials presented."}`. A key is genuinely required.

---
## 6. Machine-readable sources — can an unattended refresh work without scraping HTML?

All endpoint probes below were run directly from this machine with `curl` on 2026-09-06 and the HTTP status is quoted from the actual response.

### 6.1 Probe results

| Endpoint | Method | Auth | Result (probed 2026-09-06) | Returns prices? |
|---|---|---|---|---|
| `https://openrouter.ai/api/v1/models` | GET | **none** | **HTTP 200**, 714,425 bytes, 431 models | **Yes** — per-token USD |
| `https://api.anthropic.com/v1/models` | GET | `x-api-key` | HTTP 401 `{"type":"error","error":{"type":"authentication_error","message":"x-api-key header is required"}}` | **No** |
| `https://api.openai.com/v1/models` | GET | Bearer | HTTP 401 `{"error":{"message":"Missing bearer authentication in header",...}}` | **No** (id list only) |
| `https://api.x.ai/v1/models` | GET | Bearer | HTTP 401 `{"code":"unauthenticated:no-credentials","error":"No credentials presented."}` | **Yes**, once authenticated |
| `https://api.x.ai/v1/language-models` | GET | Bearer | HTTP 401, same body | **Yes**, plus `long_context_threshold` and `aliases[]` |
| `https://developers.openai.com/api/docs/pricing.md` | GET | **none** | Markdown price tables | **Yes** — the only first-party unauthenticated price source found |

### 6.2 Anthropic Models API — capability discovery, not pricing

`GET https://api.anthropic.com/v1/models` (docs: `https://platform.claude.com/docs/en/api/models-list` [P]). Requires `x-api-key` + `anthropic-version: 2023-06-01`. Query params `after_id`, `before_id`, `limit` (default 20, max 1000).

Per-model fields returned: `id`, `display_name`, `created_at` (RFC 3339 release datetime), `max_input_tokens`, `max_tokens`, `type`, and a `capabilities` object containing `batch`, `citations`, `code_execution`, `context_management`, `image_input`, `pdf_input`, `structured_outputs`, `thinking.types.{adaptive,enabled}`, and — directly useful here — **`effort` with per-level `{low, medium, high, xhigh, max}` support booleans**.

**It returns no pricing.** So Anthropic gives you a machine-readable *capability and effort-level* feed, and an HTML-only *price* feed. Those are two different refresh problems.

It does return `created_at`, "RFC 3339 datetime string representing the time at which the model was released" [P] — which is the authoritative fix for the release-date column in §1.1 that currently leans on OpenRouter's dated slugs. **This machine has no Anthropic credential** (`ANTHROPIC_API_KEY` unset, `ant` CLI not installed), so that call could not be made today. One authenticated `GET /v1/models` would upgrade those dates from grade A to grade P.

### 6.3 OpenRouter — the only unauthenticated all-vendor price feed

`GET https://openrouter.ai/api/v1/models` returns a JSON array under `data`. Per entry: `id`, `canonical_slug`, `name`, `created` (unix), `context_length`, `description`, `knowledge_cutoff`, `architecture`, `top_provider`, `per_request_limits`, `supported_parameters`, `default_parameters`, `benchmarks`, `expiration_date`, and:

- `pricing`: `{prompt, completion, input_cache_read, input_cache_write, web_search, overrides}` — **USD per single token** (multiply by 1e6 for per-MTok).
- `reasoning`: `{mandatory, default_enabled, supported_efforts[], default_effort}` — a machine-readable effort ladder per model.

**Fidelity check against Anthropic's own price page, all seven current Claude models, 2026-09-06:**

| Model | OpenRouter (in/out/cache-read/cache-write, $/MTok) | Anthropic official | Verdict |
|---|---|---|---|
| `anthropic/claude-fable-5.1` | 10 / 50 / 0.25 / 12.50 | 10 / 50 / 0.25 / 12.50 | **exact match** |
| `anthropic/claude-opus-5` | 5 / 25 / 0.50 / 6.25 | 5 / 25 / 0.50 / 6.25 | **exact match** |
| `anthropic/claude-sonnet-5` | 2 / 10 / 0.20 / 2.50 | 2 / 10 / 0.20 / 2.50 | **exact match** |
| `anthropic/claude-haiku-4.5` | 1 / 5 / 0.10 / 1.25 | 1 / 5 / 0.10 / 1.25 | **exact match** |
| `anthropic/claude-fable-5` | 10 / 50 / 1.00 / 12.50 | 10 / 50 / 1.00 / 12.50 | **exact match** |
| `anthropic/claude-opus-4.8` | 5 / 25 / 0.50 / 6.25 | 5 / 25 / 0.50 / 6.25 | **exact match** |
| `anthropic/claude-sonnet-4.6` | 3 / 15 / 0.30 / 3.75 | 3 / 15 / 0.30 / 3.75 | **exact match** |

7 of 7 exact, including the awkward 0.025x Fable 5.1 cache-read rate. That is meaningful evidence the feed mirrors first-party list price rather than reselling at a markup.

**But the feed is NOT rate-tier-consistent across vendors — verified counter-example.** For `openai/gpt-5.6-sol`, OpenRouter publishes $2 in / $10 out / $0.20 cache-read / $2.50 cache-write. OpenAI's own Standard tier for that model is **$4.00 in / $20.00 out / $0.40 cached / $5.00 cache write** (short context). OpenRouter's numbers are exactly OpenAI's **Batch/Flex** rate for `sol` — while, on the same feed, `gpt-6-astra` is quoted at OpenAI's **Standard** rate. So the feed silently mixes rate tiers between models of the same vendor, and a refresh that trusts it would under-price `gpt-5.6-sol` by **2x**. See §2 for the first-party figures.

**Known fidelity gaps in the OpenRouter feed** — encode these, do not paper over them:
1. **One cache-write price only.** Anthropic prices a 5-minute write (1.25x) and a 1-hour write (2x). OpenRouter's `input_cache_write` carries the **5-minute** figure. A 1h-TTL workload costed from OpenRouter is understated by 1.6x on the write leg.
2. **No batch discount on the base row** — batch appears as separate `:batch` model ids.
3. **No residency / fast-mode / long-context multipliers.**
4. **Vendor label drift**: xAI models are listed under the display name "SpaceXAI" (e.g. `SpaceXAI: Grok 4.6`) while the id prefix stays `x-ai/`. Key on the id, never the display name.
5. **Synthesised model ids.** OpenRouter's `canonical_slug` values `openai/gpt-6-astra-20260903` and `openai/gpt-5.6-{sol,terra,luna}-20260709` are **not OpenAI API ids** — OpenAI publishes no dated snapshot for those models (see §2). The dates embedded in them are real release dates, but the slugs are OpenRouter's own construction. Never emit a `canonical_slug` as an API model id.
6. It is an aggregator. It can lag a same-day price change, and it prices *its own gateway*, which need not equal a direct-to-provider contract.

### 6.4 Codex CLI model feed (local artefact)

`~/.codex/models_cache.json` on this machine — grade **L**. `fetched_at: 2026-09-06T08:32:44.532057Z`, `client_version: 0.153.4`, plus an `etag`, so the CLI is refreshing it over HTTP against an OpenAI backend (the `codex` binary contains the strings `https://chatgpt.com/backend-api`, `/models`, and `/v1/models`). The exact public URL is **unverified** and it is very likely an authenticated, undocumented CLI-internal endpoint — do not build an unattended refresh on it.

It carries no prices, but it does carry, per model: `slug`, `display_name`, `description`, `default_reasoning_level`, `supported_reasoning_levels` (each with an `effort` name and a human description), `context_window`, `max_context_window`, `supported_in_api`, `visibility`, `service_tiers`, `additional_speed_tiers`, `support_verbosity`. See §2 for what it says.

### 6.6 Long-context price tiers — the field most likely to be missed

The OpenRouter model objects carry a `pricing.overrides` array that base price rows hide. I read it directly on 2026-09-06 [A]; **both thresholds were then confirmed first-party** [P] (§2.3 for OpenAI, §3.2 for xAI), so this is two-source data, not aggregator-only:

| Model | Threshold | Above-threshold input | output | cache read | cache write | vs base |
|---|---|---|---|---|---|---|
| `openai/gpt-6-astra` | prompt > **272,000** tokens | **$20** | **$75** | $2 | $25 | base is $10 / $50 / $1 / $12.50 → **2.0x input, 1.5x output** |
| `x-ai/grok-4.6` | prompt > **200,000** tokens | **$4** | **$12** | $1 | — | base is $2 / $6 / $0.50 → **2.0x across the board** |
| every `anthropic/*` model | — | `overrides: null` | | | | **no long-context tier** |

Both thresholds re-price **the entire request**, not the overage. Verbatim, OpenAI [P]: "Prompts with >272K input tokens are priced at 2x input and 1.5x output **for the full request**." Verbatim, xAI [P]: "Requests whose prompt reaches the listed token threshold are billed at the higher rate for **all tokens in the request**." So a 273k call to `gpt-6-astra` costs twice a 271k call, and a 201k call to `grok-4.6` costs twice a 199k call. This is a step function, and a linear cost model will be wrong on both sides of it.

Anthropic states the same thing in its own words [P]: "Claude 4.6 and later models … include the full 1M token context window at standard pricing."

Consequence for a recommender: **for long-context coding work the ranking flips.** A 300k-token repo-wide task on `gpt-6-astra` costs $20/MTok input, not $10 — the same as Fable 5.1's flat $10 becoming the cheaper option on input at that length. Any cost model that reads only the headline price will get long-context routing exactly backwards. The threshold, not just the rate, has to be part of the seed data.

Note that `gpt-6-astra`'s threshold (272,000) is also exactly the `context_window` value the local Codex CLI cache reports for that model, against a `max_context_window` of 872,000 — i.e. the CLI's default context ceiling sits precisely at the price cliff.

**Also in the feed, for §7:** each model object carries a `benchmarks` key with `artificial_analysis` (`intelligence_index`, `coding_index`, `agentic_index`) and `design_arena` (per-category elo, win rate, rank). These are **accuracy/quality indices, not cost-to-complete** — useful as a quality axis to pair against price, but they do not answer §7.

### 6.5 Verdict on unattended refresh

**Yes for OpenAI (unauthenticated) and xAI (with a key); prices no for Anthropic. And NOT from OpenRouter alone.**

- **OpenAI: yes, cleanly.** OpenAI serves its documentation as Markdown at `https://developers.openai.com/api/docs/pricing.md`, plus per-model `.md` pages. That is machine-readable, unauthenticated, and first-party — no HTML scraping. This is the single best refresh source found. (`platform.openai.com/docs/*` now 301s to `developers.openai.com/api/docs/*`.)
- **Anthropic: capabilities yes, price no.** `GET /v1/models` (authenticated) gives `created_at`, context limits and a per-level `effort` capability map — everything except money. The price table is HTML only.
- **xAI: yes, and it is the best-structured of the three — but it needs a key.** `GET https://api.x.ai/v1/language-models` returns per-token prices *and* `long_context_threshold` *and* `aliases[]`, so the 200k price cliff and the `grok-build-latest` ambiguity are both resolvable programmatically. Unit is "USD cents per 100 million tokens" — **divide by 10,000** for $/MTok. xAI's HTML pricing page is *not* a fallback: `x.ai/pricing` returns 403 to non-browser clients.
- **OpenRouter is a usable cross-check, not a source of record.** It is the only unauthenticated all-vendor price feed, and it matched Anthropic 7/7 exactly — but it quoted `gpt-5.6-sol` at OpenAI's batch rate while quoting `gpt-6-astra` at standard, a silent 2x error on one row of the same vendor. A refresh built on it alone will be wrong in ways that do not announce themselves.

**Recommended refresh design:** pull OpenAI from `developers.openai.com/api/docs/pricing.md`; pull Anthropic capabilities from the authenticated `/v1/models` and hold its prices as human-maintained constants with a review date; pull OpenRouter as a *diff source only* — any disagreement between OpenRouter and the stored first-party figure raises a flag for a human rather than overwriting anything. Label every field in the seed file with its grade, so an aggregator-only number is visibly an aggregator-only number and cannot masquerade as verified.

---
## 7. Benchmarks that report cost-to-complete for coding

**Yes — several, and four of them are ingestible without scraping HTML.** My own first pass concluded otherwise; a parallel search found sources I had missed, and I then verified the three load-bearing ones myself with `curl`. Every HTTP status and field name below is quoted from a real response on 2026-09-06.

The single best answer to "what does a task cost on model X" is **LiveBench's cost CSV**, which publishes an explicit **cost per successful task** for the current frontier models.

### 7.1 Ranked by usefulness

| # | Source | Cost metric | Structured URL | 2026 frontier models? | License |
|---|---|---|---|---|---|
| 1 | **LiveBench cost table** | **`cost_per_successful_task`** and `cost_per_question` | `https://livebench.ai/cost_2026_06_25.csv` — **verified HTTP 200, 23,811 bytes, 54 rows** (mirror: `https://raw.githubusercontent.com/LiveBench/new-livebench/main/public/cost_2026_06_25.csv`) | **Yes, all of them** | NOASSERTION (Apache-2.0 + MIT bundled) |
| 2 | **Terminal-Bench 4.0** | **`total_cost_usd`** + full cached/uncached/output token split | one JSON per submission under `https://github.com/harbor-framework/terminal-bench/tree/main/leaderboard/submissions` — **verified HTTP 200, 15,958 bytes**. 24 more submissions on the same schema at `https://github.com/harbor-framework/terminal-bench-2-1/tree/main/leaderboard/submissions`, for a longer time series | **Yes** — Opus 5, Fable 5, Fable 5.1, Sonnet 5, Opus 4.8, GPT-5.6 Sol/Terra/Luna, Grok 4.5, Grok 4.6; submissions 2026-08-26 → 2026-09-02 | **Apache-2.0** |
| 3 | **OpenHands Index** | **per-instance `cost`** — the only per-task source. HF card documents it as "USD; null when unavailable", so **null-handling is required** | `https://datasets-server.huggingface.co/rows?dataset=OpenHands%2Fopenhands-index&config=instances&split=test` (40,643 rows), unauthenticated. The Space also ships a REST `api.py`: `https://huggingface.co/spaces/OpenHands/openhands-index` | Partial — has `claude-fable-5`, Opus 4.5–4.8, GPT-5.2/5.4/5.5. **No Opus 5, GPT-6 Astra or Grok 4.6** | ambiguous: README says MIT, HF card says apache-2.0, no LICENSE file |
| 4 | **SWE-bench official leaderboard** | **`cost`** and **`instance_cost`** | `https://raw.githubusercontent.com/SWE-bench/swe-bench.github.io/master/data/leaderboards.json` — **verified HTTP 200, 4,091,442 bytes** | **No** — 180 verified entries, newest are Claude 4.5/4.6 Opus, Gemini 3 Flash, MiniMax M2.5 | ⚠️ **CC BY-NC 4.0 — non-commercial** |
| 5 | Aider polyglot | `total_cost` per suite run | `https://raw.githubusercontent.com/Aider-AI/aider/main/aider/website/_data/polyglot_leaderboard.yml` — verified HTTP 200, 45,725 bytes | **No — zero.** Frozen: last commit 2025-10-04, newest entry 2025-10-03 | Apache-2.0 |
| 6 | OpenRouter benchmarks | `avg_cost_per_task`, `avg_latency_per_task_ms`, `primary_score`, `total_tasks` | `https://openrouter.ai/api/v1/benchmarks?task_type=coding` — needs a free key (401 verified) | unverified | CC BY 4.0; 30 req/min, 500 req/day |

### 7.2 LiveBench — verified values, read by me today

From `cost_2026_06_25.csv`, columns `cost_per_question` and `cost_per_successful_task` (USD):

| Model row | cost/question | **cost per successful task** |
|---|---|---|
| `claude-fable-5-1-max-effort` | 1.0108 | **1.2117** |
| `gpt-6-astra-max` | 0.6046 | **0.7359** |
| `claude-opus-5-max-effort` | 0.5599 | **0.7067** |
| `gpt-5.6-sol-max` | 0.4178 | **0.5070** |
| `grok-4.6` | 0.1614 | **0.2068** |

That ordering is the answer the tool actually wants, and it is not what the per-token table predicts: `grok-4.6` is 3.4x cheaper per solved task than `claude-opus-5` at max effort, while its input price is only 2.5x lower — because effort and solve rate move the total, not the sticker rate. **This is the concrete case for costing per completed task rather than per token.**

Caveat: LiveBench's cost columns are **suite-wide, not coding-only**. The file also carries per-task output-token columns (`code_completion`, `code_generation`, `python`, `javascript`, `typescript`), so a coding-weighted figure can be recomputed rather than taken as printed. The CSV name embeds a date, and a bogus date returns 404, so the filename is a real dated artefact — a refresh job must discover the current date rather than hardcode `2026_06_25`.

### 7.3 Terminal-Bench — the cleanest contract

One JSON per submission. Verified fields on `2026-08-26-anthropic-claude-opus-5-max-claude-code.json`: `metrics.total_cost_usd` (**5969.11**), `cached_input_tokens` (6,271,909,956), `output_tokens` (66,012,156), `accuracy` (51.82 ±3.39), `n_trials` (330), `avg_trial_duration_sec`, `pass_at_2`…`pass_at_5`, and — directly useful here — **`metadata.reasoning_effort: "max"`** and `metadata.date`.

Two properties make it the best unattended target: `total_cost_usd` is **required** by `leaderboard.yaml` and is recomputed by maintainers from hub job links rather than self-reported, and the record carries the *cached vs uncached* input split, so the cache economics in §1.2/§2.3/§3.2 can be applied rather than assumed. Its limit is that cost is per run, not per task.

Incidental corroboration: this file's `metadata.date` for Opus 5 is **2026-07-24**, matching the release date inferred in §1.1 from OpenRouter's dated slug and the Models API doc example.

### 7.4 SWE-bench — it does publish cost, but partially and under a non-commercial licence

I initially concluded SWE-bench had no cost data, because the one submission I sampled in `SWE-bench/experiments` carried only `api_calls`. That was wrong. The site repo's `leaderboards.json` **does** carry cost. Verified by me: 180 Verified-split entries, each with fields `cost`, `instance_cost`, `instance_calls`, `resolved`, `reasoning_effort`, `model_release_date`, `agent`, `date`, `per_instance_details`. Examples read today — Claude 4.5 Opus (high): `cost: 376.95`, `instance_cost: 0.7539`, `resolved: 76.8`. Claude 4.6 Opus: `cost: 275.76`, `instance_cost: 0.5515`, `resolved: 75.6`.

Two blockers, both confirmed:
- **Coverage is partial: only 45 of 180 Verified entries carry a cost.** `checklist.md` makes no cost field mandatory, so community submissions routinely omit it — the newest entry (2026-09-01, `gemini-3-5-flash`) ships `instance_calls` but no `cost`.
- **`https://raw.githubusercontent.com/SWE-bench/swe-bench.github.io/master/LICENSE` begins "Attribution-NonCommercial 4.0 International".** Non-commercial. Check before ingesting into anything shipped.

And no 2026 frontier model appears: no Opus 5, Fable, GPT-6, or Grok 4.6.

### 7.5 Publishes cost on the page, no structured export

Useful negatives — these have the best 2026 coverage of any cost board and are scrape-only:

| Source | Cost metric shown | Why it does not qualify |
|---|---|---|
| **SWE-rebench** `https://swe-rebench.com/leaderboard` | Cost per Problem ($), Tokens per Problem, % cached. 117 models; Fable 5 64.5%, Grok 4.5 63.8%, Opus 5 63.4% | `/api/leaderboard`, `/leaderboard.json`, `/api/results` all 404. The HF dataset `nebius/SWE-rebench-leaderboard` is the *task* set, not results |
| **DeepSWE** `https://deepswe.datacurve.ai/` | Pass@1 / Avg cost / Out tok / Steps; updated 2026-09-03. Opus 5 $11.84, Fable 5 $13.41, GPT-6 Astra $6.52, GPT-5.6 Sol $6.46, Grok 4.6 $3.45 | `github.com/datacurve-ai/deep-swe` (Apache-2.0) holds tasks and Dockerfiles only; `/api/leaderboard` 404 |
| **Artificial Analysis Coding Agent Index v1.4** `https://artificialanalysis.ai/agents/coding-agents` | Cache-aware cost per task; 68 model×harness entries; shows a **32x cost swing for the same model across harnesses** | API at `/api/v2` requires a key (401 verified) and the cost object is Pro+ at $417/mo/seat. The Coding Agent Index is not in the documented endpoint list — whether any tier exposes it is **unverified** |
| **Kilo** `https://kilo.ai/leaderboard` | $/attempt from real usage | no API or export found |
| **HAL** `https://hal.cs.princeton.edu/` | cost per task USD across 9 benchmarks | **Dead.** Updates paused; `github.com/princeton-pli/hal-harness` archived 2026-07-01; models only through Aug 2025 |

The Artificial Analysis 32x finding is the most important qualitative result here: **the harness costs more than the model does.** A recommender that ranks models without fixing the harness is measuring the wrong variable.

### 7.6 MirrorCode — the one open lead worth following

**MirrorCode** (METR × Epoch AI) is the closest thing to a released cost-per-attempt benchmark, and it arrived too recently to be settled here.

- `https://epoch.ai/MirrorCode` — leaderboard budget is **10B tokens + 7 days per attempt**; one run reportedly cost **$2,600 over 19 days**.
- `https://epoch.ai/blog/mirrorcode-preliminary-results` — a 1B-token budget works out to roughly **$550/task**; Opus 4.0/4.1/4.5/4.6 evaluated.
- Artifacts: `https://github.com/epoch-research/MirrorCode-data` (codebases, transcripts, scores); harness `https://github.com/METR/MirrorCode`. Epoch content is CC-BY.
- **Whether the data repo carries per-run dollars is unverified.** If it does, it becomes the best-licensed per-attempt cost source available.

Separately, Epoch's cost work does not live in its accuracy-only benchmark hub: `https://github.com/epoch-research/llm-benchmark-efficiency`, path `results/default/lowest_cost_models_above_previous_frontier/`, paired with arXiv 2511.23455. **CSV contents unverified.**

### 7.7 Checked, does not publish cost

**METR — firm negative, files checked individually.** `https://metr.org/assets/benchmark_results_1_1.yaml` carries `average_score`, `p50_horizon_length`, `is_sota`, `doubling_time_in_days` — no cost, no tokens. `https://metr.org/assets/task_results_1_1.yaml` (670 KB) carries `agents{coefficient, intercept, release_date, tasks[...]}` — no cost. `github.com/METR/eval-analysis-public`'s `runs.jsonl` is `task_id, alias, score_binarized, score_cont, human_minutes, invsqrt_task_weight` — no cost, DVC-tracked so not actually in git, GitHub API reports `license: null`, last push 2026-03-06. `metr.org/time-horizons` was last updated 2026-05-08 and contains no Opus 5, Fable 5.x, GPT-5.6 or Grok 4.x. Where METR does put dollars — "Expenditure Horizon", `https://metr.org/blog/2026-07-21-expenditure-horizon/` — it is prose and charts with **no data file**; Toby Ord had to eyeball those charts (`https://www.tobyord.com/writing/hourly-costs-for-ai-agents`) and reports METR declined to share the cost data. · SWE-bench Pro / Scale SEAL (accuracy ±CI only; a footnote mentions capped vs uncapped cost runs but publishes no figures) · SWE-Atlas · **SWE-Lancer** (the dollars are the *score* — agent earnings out of $1M in Upwork payouts — not cost to run; repo archived 2025-07-18, merged into `openai/preparedness`) · **Epoch AI** (excellent downloads — `https://epoch.ai/data/benchmark_data.zip` updated 2026-09-06, CC-BY — but **accuracy-only**; `eci_benchmarks.csv` has no cost, price or token column; their inference-price-trends page is stale at 2025-02-05) · **LMArena** (now 301-redirects to `https://arena.ai/leaderboard`; HF dataset `lmarena-ai/leaderboard-dataset` is CC-BY-4.0 and current to 2026-09-05 but carries only Elo/rank/votes) · **Vals AI** (has a Cost axis and good 2026 coverage — GPT-6 Astra, Fable 5.1, Opus 5 — but no public API: `www.vals.ai/api/benchmarks` 404) · LiveBench's *score* tables (`table_*.csv`, no cost columns — only the separate `cost_*.csv` has them) · BigCodeBench (archived 2026-01-03) · EvalPlus (stale 2025-10-02) · SWE-bench-Live · Harbor-Index · **llm-stats.com** (keyed REST API, 380+ models, current — but it publishes score × per-token price, a join table, **not a measured cost-to-complete**) · Claw-SWE-Bench (arXiv 2606.12344 — treats cost accounting as first-class but is a paper snapshot, no live leaderboard) · **GSO-bench** (`https://gso-bench.github.io/` — Opt@1, hack-adjusted score, wall-clock, turns per task; no dollars) · **TestEvo-Bench** (`https://www.testevo-bench.com/`, arXiv 2607.02469 — the *paper* imposes $3 / $1 / $0.5 per-task budgets, but the leaderboard columns are Success% / Pass% / ExecFail% / CovOnPass; the budget framing is worth knowing even though no cost column ships) · **HAL Reliability Dashboard** (`https://hal.cs.princeton.edu/reliability/` — the live successor to HAL, current to roughly Opus 4.7 / Gemini 3.5 Flash / GPT-5.5, and it reports **no cost at all**; so the HAL line has current data without cost and stale data with it) · SWE-bench Pro data repo (`https://github.com/scaleapi/SWE-bench_Pro-os` — tasks only) · third-party re-derivations (morphllm "price per point", benchlm.ai, codingfleet, pricepertoken, userightai, benchgen).

**No first-party cost-vs-accuracy coding leaderboard was found from Vercel, Cursor, Cognition, Google, or AWS Bedrock.** Their per-task dollar figures circulate only via Artificial Analysis and SEO aggregators.

HAL's stale figures, kept only for calibration: Opus 4.5 on CORE-Bench Hard 77.8% @ $87.16; SWE-bench Verified Mini — SWE-Agent+o4-mini Low 54.0% @ $259.20, Opus 4.1 High 54.0% @ **$1,599.90**, GPT-5 Medium 46.0% @ $162.93, Gemini 2.0 Flash 24.0% @ $4.72 (paper arXiv 2510.11977, 21,730 rollouts, ~$40,000 total). The Opus 4.1 vs o4-mini pair is the point: **identical 54.0% accuracy, 6.2x the cost.** That is the whole argument for costing per completed task.

### 7.8 Recommendation

For an unattended job: **LiveBench `cost_*.csv`** (only source with explicit cost-per-solve on current models) **+ Terminal-Bench submission JSONs** (Apache-2.0, current, cache-aware token split, records `reasoning_effort`) **+ OpenRouter `/api/v1/models`** as the price table. Add **OpenHands Index** via the unauthenticated HF rows endpoint if per-instance granularity is needed, accepting its ~2-month lag and ambiguous licence. Treat **SWE-bench's `leaderboards.json` as licence-blocked (CC BY-NC 4.0)** for anything commercial, and **SWE-rebench / DeepSWE as scrape-only sanity checks** — they have the best 2026 coverage but no export.

Two standing cautions: LiveBench's cost is suite-wide, so weight it by its coding-task columns; and per §7.5, harness choice can move cost 32x for the same model, so a benchmark figure is only transferable to a job that uses a comparable harness.

## 8. Exact launch invocations

Two source classes, kept apart:

- **[DOCS]** official documentation, URL given, retrieved 2026-09-06.
- **[LOCAL]** `--help` from the binary installed on this machine. Authoritative for *this* version, not for others. Versions: `codex` 0.153.4, `opencode` 1.18.29, `claude` 2.1.263.

Flags marked **does not exist** were probed and rejected by the installed binary. A launcher must never emit them.

### 8.1 OpenAI Codex CLI — `codex exec`

Documentation has moved twice: `github.com/openai/codex/docs/*.md` are now stubs pointing at `developers.openai.com/codex/*`, which 308-redirects to `learn.chatgpt.com/docs/*`. A launcher pinned to the old GitHub doc paths is reading three-line pointers.

| Flag | Meaning (verbatim) | Values | Source |
|---|---|---|---|
| `-m, --model <MODEL>` | "Model the agent should use" | free-form; docs example `gpt-5.6-terra` | [LOCAL] + [DOCS] |
| `-c, --config <key=value>` | "Override a configuration value that would otherwise be loaded from `~/.codex/config.toml`." Value parsed as TOML | dotted key paths | [LOCAL] |
| `model_reasoning_effort` (set via `-c`) | "Adjust reasoning effort for supported models (Responses API only; `xhigh` is model-dependent)" | `minimal` \| `low` \| `medium` \| `high` \| `xhigh` | [DOCS] config-reference |
| `-s, --sandbox <SANDBOX_MODE>` | "Select the sandbox policy to use when executing model-generated shell commands" | `read-only`, `workspace-write`, `danger-full-access` | [LOCAL] + [DOCS] |
| `--approve-for-me` | "Route approval requests through automatic review using the workspace-write sandbox" | boolean | [LOCAL] |
| `--dangerously-bypass-approvals-and-sandbox` | "Skip all confirmation prompts and execute commands without sandboxing. EXTREMELY DANGEROUS." | boolean | [LOCAL] |
| `-C, --cd <DIR>` | "Tell the agent to use the specified directory as its working root" | path | [LOCAL] |
| `--add-dir <DIR>` | "Additional directories that should be writable alongside the primary workspace" | path | [LOCAL] |
| `-o, --output-last-message <FILE>` | "Specifies file where the last message from the agent should be written" | path | [LOCAL] + [DOCS] |
| `--json` | "Print events to stdout as JSONL" | boolean | [LOCAL] + [DOCS] |
| `--output-schema <FILE>` | "Path to a JSON Schema file describing the model's final response shape" | path | [LOCAL] |
| `--skip-git-repo-check` | "Allow running Codex outside a Git repository" | boolean | [LOCAL] |
| `--ephemeral` | "Run without persisting session files to disk" | boolean | [LOCAL] |
| `-p, --profile <NAME>` | "Layer `$CODEX_HOME/<name>.config.toml` on top of the base user config" | profile name | [LOCAL] |
| `--full-auto` | **does not exist in 0.153.4** — probe returns `error: unexpected argument '--full-auto' found`, though the docs still describe it as a deprecated compatibility flag | — | [LOCAL] probe |
| `-a, --ask-for-approval` | **not accepted by `codex exec`** — top-level `codex` only. Probe: `error: unexpected argument` | — | [LOCAL] probe |
| `--experimental-json` | **does not exist** — the flag is `--json` | — | [LOCAL] probe |

`-c` value quoting, verbatim from `https://learn.chatgpt.com/docs/config-file/config-advanced`:

```bash
codex --config model='"gpt-5.6-terra"'
codex --config sandbox_workspace_write.network_access=true
codex --config 'shell_environment_policy.include_only=["PATH","HOME"]'
```

The value is TOML, not JSON — a bare `-c model_reasoning_effort=high` is a different thing from `-c model_reasoning_effort='"high"'`. Get this wrong and the effort silently does not apply.

`codex exec resume` exists: `codex exec resume [OPTIONS] [SESSION_ID] [PROMPT]`, with `--last` and `--all`. **It accepts a much smaller flag set** — no `-s/--sandbox`, `-C/--cd`, `-p/--profile`, `--add-dir`. A resume leg must carry sandbox as `-c sandbox_mode='"workspace-write"'`.

Default sandbox, verbatim [DOCS]: "By default, `codex exec` runs in a read-only sandbox." So approval policy for `exec` is set with `-c approval_policy='"never"'`, not a flag.

**Worked example:**
```bash
codex exec \
  --model gpt-5.6-terra \
  --config model_reasoning_effort='"xhigh"' \
  --sandbox workspace-write \
  --cd /path/to/repo \
  --skip-git-repo-check \
  --json \
  --output-last-message /tmp/codex-final.txt \
  "Implement ticket #123 and run the test suite"
```
Docs endorse the pairing, verbatim: "Pair `--json` with `--output-last-message` in CI to capture machine-readable progress and a final natural-language summary."

### 8.2 OpenCode — `opencode run`

The repo has moved: `github.com/sst/opencode` 301-redirects to `github.com/anomalyco/opencode`. Docs source is `packages/web/src/content/docs/*.mdx` on branch `dev`.

Reasoning effort **is** settable from the CLI, but the flag is `--variant`, not a reasoning-effort flag.

| Flag | Meaning (verbatim) | Values | Source |
|---|---|---|---|
| `-m, --model` | "Model to use in the form of provider/model" | `provider_id/model_id` | [DOCS] `https://opencode.ai/docs/cli/` |
| `--variant` | "Model variant (provider-specific reasoning effort)" | Anthropic: `high` (default), `max`. OpenAI: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`. Google: `low`, `high`. Plus custom names | [DOCS] cli + models; [LOCAL] |
| `--format` | "Format: default (formatted) or json (raw JSON events)" | `default`, `json` | [DOCS] + [LOCAL] |
| `--dir` | "Directory to run in, or path on the remote server when attaching" | path | [DOCS] + [LOCAL] |
| `--agent` | "Agent to use" | agent name | [DOCS] |
| `--auto` | "Auto-approve permissions that are not explicitly denied" ([LOCAL] adds "(dangerous!)") | boolean | [DOCS] + [LOCAL] |
| `-c, --continue` / `-s, --session` / `--fork` | continue or fork a session | — | [DOCS] |
| `--thinking` | "Show thinking blocks" | boolean | [DOCS] + [LOCAL] |
| output-to-file flag | **does not exist** — `run` prints to stdout; use shell redirection | — | [DOCS] + [LOCAL] |
| sandbox flag | **does not exist** — isolation is the `permission` config plus `--auto` | — | [DOCS] permissions |

Config key path for effort is `provider.<provider_id>.models.<model_id>.variants.<variant_name>.reasoningEffort`. Verbatim from `https://opencode.ai/docs/models/`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "opencode": {
      "models": {
        "gpt-5": {
          "variants": {
            "high": {
              "reasoningEffort": "high",
              "textVerbosity": "low",
              "reasoningSummary": "auto"
            }
          }
        }
      }
    }
  }
}
```

Permissions, verbatim from `https://opencode.ai/docs/permissions/` — each key resolves to `"allow"`, `"ask"` or `"deny"`; keys are `read`, `edit`, `glob`, `grep`, `bash`, `task`, `skill`, `lsp`, `question`, `webfetch`, `websearch`, `external_directory`, `doom_loop`:

```json
{ "permission": { "*": "ask", "bash": "allow", "edit": "deny" } }
```

**Worked example:**
```bash
opencode run \
  --model openrouter/x-ai/grok-4.6 \
  --variant high \
  --dir /path/to/repo \
  --format json \
  --auto \
  "Implement ticket #123 and run the test suite" \
  > /tmp/opencode-run.jsonl
```

### 8.3 Claude Code — `claude -p` (headless)

Effort is a first-class flag here.

| Flag | Meaning (verbatim) | Values | Source |
|---|---|---|---|
| `-p, --print` | "Print response without interactive mode" | boolean | [DOCS] `https://code.claude.com/docs/en/cli-reference` |
| `--model <model>` | "Sets the model for the current session with a model alias … or a model's full name" | aliases `fable`, `opus`, `sonnet`, `haiku`, `best`, `opus[1m]`, `sonnet[1m]`, `opusplan`; full ids `claude-opus-5`, `claude-sonnet-5`, `claude-fable-5-1`, … | [DOCS] cli-reference + model-config |
| `--effort <level>` | "Set the effort level for the current session … Overrides `modelSettings` and `effortLevel` … does not persist" | [DOCS]: `low`, `medium`, `high`, `xhigh`, `max`, `ultracode`. **[LOCAL] 2.1.263 help lists only `(low, medium, high, xhigh, max)`** | [DOCS] cli-reference |
| `--output-format <format>` | "Specify output format for print mode" | `text` (default), `json`, `stream-json` | [DOCS] cli-reference + headless |
| `--permission-mode <mode>` | "Begin in a specified permission mode" | `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`, `manual` | [DOCS] cli-reference |
| `--dangerously-skip-permissions` | "Skip permission prompts. Equivalent to `--permission-mode bypassPermissions`" | boolean | [DOCS] cli-reference |
| `--allowedTools` / `--allowed-tools` | "Tools that execute without prompting for permission" | permission-rule syntax, e.g. `"Bash(git log *)" "Read"` | [DOCS] cli-reference |
| `--add-dir <directories...>` | "Add additional working directories for Claude to read and edit files." **Grants file access; does not set cwd** | paths | [DOCS] cli-reference |
| `--permission-prompts <target>` | who answers permission prompts under `--print` | `host` (default), `none` — requires v2.1.259+ | [LOCAL] + [DOCS] headless |
| `--json-schema <schema>` | structured output validation; result lands in `structured_output` | JSON Schema string | [DOCS] headless |
| `--bare` | skips hooks/plugins/MCP/CLAUDE.md discovery; "the recommended mode for scripted and SDK calls" | boolean | [DOCS] headless |
| `--max-budget-usd <amount>` | "Maximum dollar amount to spend on API calls (only works with --print)" | number | [LOCAL] |
| `--fallback-model <model>` | comma-separated fallback list (only with `--print`) | model ids | [LOCAL] |
| `--cwd` | **does not exist** — probe: `error: unknown option '--cwd'`. `cd` first, or use `-w, --worktree` | — | [LOCAL] probe |

Effort can also be set by env or settings [DOCS] `https://code.claude.com/docs/en/model-config`:

| Mechanism | Values |
|---|---|
| `--effort` | `low`, `medium`, `high`, `xhigh`, `max`, `ultracode` |
| `CLAUDE_CODE_EFFORT_LEVEL` env | `low`, `medium`, `high`, `xhigh`, `max`, `auto` |
| `effortLevel` settings key | `low`, `medium`, `high`, `xhigh` — **not `max`** |
| `modelSettings.<model>.effortLevel` | per-model override |
| `MAX_THINKING_TOKENS` env | **not the effort control.** `0` turns thinking off on adaptive-reasoning models; other values apply only to fixed-budget Opus 4.6 / Sonnet 4.6 |

Per-model effort ceiling, verbatim from model-config:
```
| Fable 5.1 and Fable 5                    | low, medium, high, xhigh, max |
| Opus 5, Sonnet 5, Opus 4.8, and Opus 4.7 | low, medium, high, xhigh, max |
| Opus 4.6 and Sonnet 4.6                  | low, medium, high, max        |
```

Verbatim gotcha [DOCS] headless: "For `-p`, the built-in starting permission mode is Manual on every plan, so pass the permission mode you want." An unattended launcher that omits `--permission-mode` will stall.

**Worked example:**
```bash
cd /path/to/repo && \
claude -p "Implement ticket #123 and run the test suite" \
  --model claude-opus-5 \
  --effort high \
  --output-format json \
  --permission-mode bypassPermissions \
  --permission-prompts none \
  --allowedTools "Bash,Read,Edit" \
  > /tmp/claude-run.json
```

### 8.4 Cross-CLI summary

| | model flag | reasoning effort | working dir | final output to file |
|---|---|---|---|---|
| `codex exec` | `-m/--model` | `-c model_reasoning_effort='"high"'` (TOML-quoted) or `--profile` | `-C/--cd` | `-o/--output-last-message` (native) |
| `opencode run` | `-m/--model provider/model` | `--variant high` | `--dir` | shell redirect only |
| `claude -p` | `--model` | `--effort high` (native flag) | `cd` first | shell redirect only |

Only `codex exec` writes the final message to a file natively. The other two need shell redirection, and `opencode`'s `--format json` / `claude`'s `--output-format stream-json` change what lands in that file.

**Sources:** `https://learn.chatgpt.com/docs/codex/cli`, `https://learn.chatgpt.com/docs/non-interactive-mode`, `https://learn.chatgpt.com/docs/config-file/config-reference`, `https://learn.chatgpt.com/docs/config-file/config-advanced`, `https://opencode.ai/docs/cli/`, `https://opencode.ai/docs/models/`, `https://opencode.ai/docs/permissions/`, `https://github.com/anomalyco/opencode`, `https://code.claude.com/docs/en/cli-reference`, `https://code.claude.com/docs/en/headless`, `https://code.claude.com/docs/en/model-config`. All retrieved 2026-09-06.

---
## Appendix A — what this machine is actually configured to run (grade L)

Read directly from disk on 2026-09-06. This is evidence about *this machine*, not about the public products; it is included because it settles which model ids are real in practice and what the CLIs default to.

**`~/.codex/config.toml`** (mtime 2026-09-05 20:18):
```toml
model_reasoning_effort = "high"
approval_policy = "never"
sandbox_mode = "danger-full-access"
model = "gpt-6-astra"
service_tier = "default"
```
So the machine's Codex default is `gpt-6-astra` at effort `high`, with approvals off and no sandbox. Confirms `gpt-6-astra` is a live, currently-served model id, and confirms `model_reasoning_effort` is the config key name (matching §8.1).

**`~/.config/opencode/opencode.jsonc`**:
```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "openrouter/x-ai/grok-4.6",
  "permission": "allow"
}
```
So OpenCode on this machine reaches Grok 4.6 **through the OpenRouter gateway**, not direct to xAI — the `provider/model` string is `openrouter/x-ai/grok-4.6`, i.e. provider `openrouter` plus the OpenRouter model slug. Prices billed on that path are OpenRouter's, not xAI's direct rates.

**`~/.codex/models_cache.json`** — `fetched_at: 2026-09-06T08:32:44.532057Z`, `client_version: 0.153.4`. Nine entries. Reasoning ladders and defaults verbatim from the file:

| slug | display_name | description (verbatim) | default effort | supported efforts | ctx / max ctx | in API? | visibility |
|---|---|---|---|---|---|---|---|
| `gpt-6-astra` | GPT-6-Astra | "Our most capable model for complex, demanding work." | `medium` | low, medium, high, xhigh, max, **ultra** | 272,000 / 872,000 | yes | list |
| `gpt-reserve` | GPT-Reserve | "Fast and affordable agentic coding model." | `medium` | low, medium, high, xhigh, max | 272,000 / 872,000 | yes | **hide** |
| `gpt-5.6-sol` | GPT-5.6-Sol | "Reliable agentic workhorse for everyday tasks." | `low` | low, medium, high, xhigh, max, **ultra** | 272,000 / 872,000 | yes | list |
| `gpt-5.6-terra` | GPT-5.6-Terra | "Balanced agentic coding model for everyday work." | `medium` | low, medium, high, xhigh, max, **ultra** | 272,000 / 872,000 | yes | list |
| `gpt-5.6-luna` | GPT-5.6-Luna | "Fast and affordable agentic coding model." | `medium` | low, medium, high, xhigh, max | 272,000 / 872,000 | yes | list |
| `gpt-5.5` | GPT-5.5 | "Proven previous-generation model for coding and general work." | `medium` | low, medium, high, xhigh | 272,000 / 272,000 | yes | list |
| `gpt-5.4-mini` | GPT-5.4-Mini | "Small, fast, and cost-efficient model for simpler coding tasks." | `medium` | low, medium, high, xhigh | 272,000 / 272,000 | yes | list |
| `gpt-5.3-codex-spark` | GPT-5.3-Codex-Spark | "Ultra-fast coding model." | `high` | low, medium, high, xhigh | 128,000 / 128,000 | **no** | list |
| `codex-auto-review` | Codex Auto Review | "Automatic approval review model for Codex." | `medium` | low, medium, high, xhigh, max | 272,000 / 872,000 | yes | hide |

**Context-window caveat.** The `context_window` numbers above are what the *Codex CLI* will use, not necessarily the model's API maximum. For `gpt-5.4-mini` the cache says 272,000 while OpenRouter reports 400,000 for `openai/gpt-5.4-mini`; for `gpt-6-astra` the cache says 272,000 against a `max_context_window` of 872,000 while OpenRouter reports 1,050,000. Do not seed API context limits from this file.

The effort ladder here is richer than the one OpenRouter reports, which stops at `max`. The `ultra` level's own description in the file is **"Maximum reasoning with automatic task delegation"** — note that this is a *different kind of thing* from the other levels: it changes the execution topology, not just the depth. Whether `ultra` is a public API value or a Codex-CLI-only affordance is resolved in §2; until then treat it as CLI-only.

Two entries are marked `visibility: hide` (`gpt-reserve`, `codex-auto-review`) — they exist and are API-supported but are not offered in the picker. `gpt-5.3-codex-spark` is the inverse: shown in the picker but `supported_in_api: false`. A recommender should surface neither as an API target.

---
## Appendix B — everything that could not be verified

Listed so the gaps are visible rather than quietly filled. None of these should be guessed at; several are cheap to close with one authenticated call or one browser visit.

### Blocked by missing credentials on this machine

| Item | What would close it |
|---|---|
| Anthropic per-model release dates as `created_at` (currently aggregator-derived) | one `GET https://api.anthropic.com/v1/models` with any API key |
| Which OpenAI ids are actually *served* today, and their `shutdown_date` — the only way to settle the `gpt-5.3-codex` / `gpt-5.4` contradiction | one `GET https://api.openai.com/v1/models` with any key |
| xAI's own price feed, `long_context_threshold` and `aliases[]` | one `GET https://api.x.ai/v1/language-models` with any key |
| What `grok-build-latest` resolves to (the `grok-4.5` card and `docs.x.ai/build/overview` disagree) | the `aliases[]` array from the call above |

### Blocked by Cloudflare / 403 to automated fetches

| Item | Notes |
|---|---|
| **All xAI consumer tier prices** — Free, SuperGrok Lite, SuperGrok, SuperGrok Plus, SuperGrok Heavy, X Premium+ | `x.ai/pricing`, `x.ai/grok`, `x.ai/api`, `grok.com/plans` all 403. Third-party figures for SuperGrok Heavy disagree with each other ($300 vs $100/mo) and are deliberately not reproduced. Tier *names* are confirmed from `docs.x.ai/grok/faq` |
| ChatGPT *chat* message limits (the "160 messages / 3 hours" style numbers) | `help.openai.com`, `openai.com`, `chatgpt.com` all 403. Codex usage estimates in §2.7 came from `learn.chatgpt.com` and are quoted; the chat-side numbers are not |
| OpenAI Business Premium seat pricing, Enterprise per-seat price | same |

### Not published by the vendor at all

| Item | Notes |
|---|---|
| Anthropic's absolute numeric allowance for any consumer tier | Only relative multipliers are published, plus an explicitly discretionary weekly cap. This is a property of the product, not a research failure |
| xAI's numeric weekly allowance | "a weekly usage allowance" with no number |
| The USD price of an OpenAI credit | The credit rate card exists (§2.7) but no reachable page gives pack sizes or prices. A consistent 25 credits = $1.00 falls out of dividing two OpenAI tables, but that is my arithmetic, not OpenAI's statement — **do not route on it** |
| A dated pinned snapshot for `gpt-6-astra`, `gpt-5.6-*`, or `grok-4.6` | Confirmed absent, not merely unfound. Only Anthropic pins every current id |
| **Any public $/task feed for current models** | Confirmed absent (§7). Aider has the right schema but stopped in Oct 2025; SWE-bench is current but records `api_calls`, not money |
| Whether xAI bills reasoning tokens *at the output rate* | xAI says only "billed as part of your total consumption". The nesting of `reasoning_tokens` under `completion_tokens_details` implies it. Inferred, never stated |

### Contradictions left open

| Contradiction | Status |
|---|---|
| `gpt-5.3-codex` listed as shut down 2026-07-23 yet still has a live model page and price row; `gpt-5.4`/`gpt-5.4-mini` "retire from Codex Aug 31 2026" yet remain on the API pricing page with no deprecation entry | OpenAI's own docs disagree with each other. Treat all as retired |
| xAI's reasoning guide says "Reasoning cannot be disabled", but the chat API enum includes `"none"` and the retirement page maps `grok-3` → "`grok-4.3` with `none` reasoning effort" | Best reading: `none` valid on 4.3, refused on 4.6. Test before relying on it |
| `grok-4.5` and `grok-build-0.1` return an identical "best for" sentence from two different URLs | Consistent with the shared `grok-build-latest` alias, but verify by eye before quoting either |
| `claude --effort ultracode` is documented but absent from the installed binary's `--help` (2.1.263) | Docs say it needs v2.1.203+, so it should work. Documented-but-unlisted |
| OpenRouter lists `grok-4.20` at 2M context; xAI says 1M | xAI is right. Recorded as a calibration datum for how far to trust the aggregator field-by-field |

### Benchmark questions left open (§7)

| Question | Status |
|---|---|
| Whether `github.com/epoch-research/MirrorCode-data` carries per-run dollars | **Unverified.** If it does, MirrorCode becomes the best-licensed per-attempt cost source (CC-BY) |
| Contents of `epoch-research/llm-benchmark-efficiency` → `results/default/lowest_cost_models_above_previous_frontier/` | CSV **unverified** |
| Whether any Artificial Analysis tier exposes Coding Agent Index cost-per-task via API | **Unverified.** Not in the documented endpoint list; cost object is Pro+ at $417/mo/seat |
| Undocumented JSON routes behind `swe-rebench.com` or `deepswe.datacurve.ai` | All guessed paths 404. **Unverified**, not disproven |
| OpenHands Index licence — HF card says apache-2.0, README says MIT, no LICENSE file | **Unresolved.** Settle before ingesting |
| LiveBench licence (NOASSERTION), SWE-Marathon and Vals AI data licences | **Unresolved** |
| `hal_traces` size — measured at ~113 GB on one pass, ~161.6 GB on another | Conflicting, and moot: encrypted, viewer broken, no licence declared. Unusable either way |
| Never checked at all: CodeArena, RepoBench, SWE-Perf / SWE-fficiency (arXiv 2607.01211), Commit0 as a standalone leaderboard, Design Arena's cost metrics | **Genuinely open** |

### Deliberately excluded

`gpt-5.6-cyber` and the `gpt-daybreak-blue-latest` / `gpt-daybreak-red-latest` aliases are real and current, but they are cybersecurity models, out of scope for general coding routing. Their prices were not read. Anthropic's Mythos 5 / 5.1 are limited-availability (Project Glasswing) and should not be default routing targets.

