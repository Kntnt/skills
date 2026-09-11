# The setup interview

Read when running `/model-selector setup`. This is the script for a conversation and the shape of what it produces.

## What the interview is for

Only the user can say which Harnesses this covers, which makers they want models from, and how the tokens are actually paid for. Every model a chosen maker offers is then eligible, so the interview never asks about a model on its own. Everything else — which models exist, what each supports, what each costs, which subscriptions a provider sells and what each of those costs — is already in the catalogue: the models and their prices kept current by the catalogue pass, dated and attributed, and the plans shipped with this collection. Asking a person for any of it wastes their time and gets a worse answer. **Never ask for a fact the catalogue holds.** If a price, a model list, a plan or a release date is missing, that is a gap in the catalogue, not a question.

Ask one question at a time. Do not ask again for something the user has already made unambiguous — in the invocation, in the Contextual Instruction, or earlier in this conversation. Confirm such an answer inside the next question rather than re-posing it.

## Read the catalogue first

Before the first question:

    uv run "$HERE/scripts/catalogue.py" [--data=<directory>]

It prints what this machine knows about the world: every model with its rate card and where that came from, and every subscription each provider markets with what it lists at. Questions 2 and 3 are answered out of that one document. Read it rather than the files behind it — which of them wins is a rule the engine keeps so that nothing has to apply it by hand.

## The three questions, in this order

### 1. Which Harnesses

Offer the ones detected on this machine as the answer and ask only whether that is right. Detection is a filesystem probe: `~/.claude` is Claude Code, `~/.codex` is Codex, `~/.config/opencode` is OpenCode. A Harness the user names that was not detected is accepted — they may be about to install it — and one that was detected and is not wanted is dropped.

The answer decides which models can be reached at all. The generated subagent definitions follow the makers chosen in question 2.

### 2. Which makers

Name the makers the catalogue holds — every distinct `provider` its models carry — each with the models it currently offers, and ask which of them the user wants models from. Show a maker under the name its models are known by: `anthropic` is Claude, `openai` is GPT, and `spacexai` is Grok; any other provider id is shown as the id itself. Record the answer as those ids, never as the display names.

Every model a chosen maker offers is eligible, including one the catalogue gains after this interview, and a maker left out is never recommended however well its models score, unless a call asks for `--scope=all`, which admits the whole catalogue. The user cannot choose or leave out a single model within a maker: which of them does a given job is what the measurements decide, and a model wanted for one piece of work is named with `--model` on that call. Say so when the question is asked, so that nobody expects a model list to follow.

This is a question about willingness — an account, a policy, a preference — and not about capability, so do not argue for a maker or characterise one as better, rank the models, or add an opinion of your own: a recommendation from measurement is what this Skill is for, and a recommendation from prose here would contaminate it.

### 3. How each maker is paid for, per Harness

Ask per maker **and per channel**, because the same maker is commonly reached two ways at once — a subscription plan inside one Harness and API rates from another — and the two cost differently for the same tokens. For each maker the user chose, and each Harness that can reach it, ask which of the two applies. Both can apply, in different Harnesses, and one channel per provider and Harness is what gets recorded.

**A subscription means naming the plan, and the name is the provider's own, whole.** Offer the plans the catalogue holds for that provider — each under the name it is marketed and billed by, each with what it lists at per month. *Claude Max 20x* is one name and *ChatGPT Pro 20x* is another; neither is a product and a level in two fields, because a name somebody has to split is a name two profiles will split differently. What goes into `plan` is exactly the name that was offered.

**A provider whose plans the catalogue does not hold is asked openly.** Say that this Skill has no list for that provider, ask what the plan is called, and record the answer as given. Never assemble a list from memory: an offered list that is wrong is answered wrongly, and the user has no way to see that the options came from nowhere.

**A set longer than the asking tool can offer is never trimmed to fit.** Where there are more plans than one question can carry as options, put the complete list in the question itself, numbered, and take the answer as typed. Dropping an option to fit the tool is how the plan somebody actually pays for stops being offerable at all.

**Compare what came back against what was offered.** An answer matching nothing offered was typed rather than chosen, and that is worth saying out loud: it means the catalogue has fallen behind, not that the user is wrong. Record it as given, say in the review that it came from outside the list, and say that plans come with a release of this collection and that `/kntnt update` is what brings a newer one in. The writer says the same thing again in its own report.

**Do not ask what a plan costs per month, and do not record it.** The list price is a fact the catalogue ships, shown in the review as the catalogue's own. Nothing in this Skill reads a monthly price — there is no renewal to decide and no bill to reconcile — so a figure collected here would be a question asked for nothing. Where the user's own price differs, because they are billed in another currency or on an older rate, that is worth knowing and is not an answer this profile has anywhere to put.

**An API channel means a rate card.** Ask only whether the provider is reached directly or through a gateway, and which gateway where that is the answer.

- **Directly**, the catalogue already holds the rate card, per model and token category: the price OpenRouter publishes, the one measure it keeps for every channel. Ask nothing further.
- **Through a gateway**, what the catalogue holds is the price OpenRouter publishes: through OpenRouter that is the charge itself, and through any other gateway it is a different arrangement's bill. A rate the user records replaces it either way. So ask what the user pays per million tokens, for input, cached input, cache writes and output, and record it on the channel.

**Every figure is USD, and nothing anywhere converts.** Ask for a rate card in USD per million tokens, and say so as you ask. A card in any other currency is refused by the writer, by name, rather than added to a dollar bill in silence. Where the user's gateway quotes one averaged input rate with caching already accounted for, that single rate is what every input category carries, and say that is what you have done.

## Before writing

Show the complete profile — Harnesses, makers under their display names, and one line per payment channel naming maker, Harness, and either the plan or the gateway and its rate card. Beside a plan, show what the catalogue says it lists at, marked as the catalogue's own figure. Name any answer that did not come from what was offered. Ask for acceptance. Nothing is written until it is accepted, and a declined review returns to the question the user wants changed rather than restarting the interview.

## What is written

Assemble one JSON object and hand its path to the writer; never edit the profile file directly.

    uv run "$HERE/scripts/setup_apply.py" [--data=<directory>] <path-to-profile-json>

    {
      "harnesses": ["claude-code", "codex", "opencode"],
      "makers": ["anthropic", "openai", "spacexai"],
      "channels": [
        {"provider": "anthropic", "harness": "claude-code", "pay": "subscription",
         "plan": "Claude Max 20x", "gateway": null, "rates": null},
        {"provider": "spacexai", "harness": "opencode", "pay": "api",
         "plan": null, "gateway": "openrouter",
         "rates": {"input": 0.9915, "cache_read": 0.9915, "cache_write": 0.9915,
                   "output": 6.174, "currency": "USD", "unit": "per_mtok"}}
      ],
      "answered_at": "2026-09-06T09:12:00Z"
    }

`makers` holds catalogue provider ids, at least one, and no model id: every model a chosen maker offers is eligible, so a list of `providers` or `models` beside it is refused. A channel names its maker as `provider`, the catalogue field's own name. `pay` is `subscription` or `api` and nothing else. `plan` is the subscription under the whole name its provider markets it by, and is null on an API channel. `gateway` names the gateway where one stands between the user and the provider, and is null on a direct channel. `rates` is what the user pays per million tokens on that channel, and is null wherever the catalogue's own card is the right one — which is every subscription and every direct API channel.

The writer validates the object against the catalogue, writes it atomically at mode 0600, and regenerates the subagent definitions — one per Anthropic model and supported deliberation level wherever Anthropic is a chosen maker — removing the ones the new answers no longer justify, which is every one of them where Anthropic is not chosen. Render its report, its `notes` included: each one names an answer the catalogue could not account for, and each is a thing the user is entitled to know was recorded as typed. Where it says the definitions directory had to be created, say that Claude Code reads that directory as a session starts, so the new definitions reach sessions started from now on rather than this one.

Then run the catalogue pass once, as `SKILL.md`'s `## Setup` says: where the writer answered `ok`, and where the review was declined and nothing was written, but not where the writer refused the profile.

The profile holds no credential of any kind, and nothing here asks for one.

## When the interview is not held

Until it is held nothing is chosen, and nothing is stopped either. An absent profile, one an older release wrote — a `models` list and no `makers`, which is read as none rather than translated — and a damaged one all stand in as a profile choosing no maker. Damaged means unreadable, carrying an invalid channel or other entry, choosing a maker the catalogue does not know, or carrying `providers` or `models` beside `makers`. With no maker chosen nothing is eligible, the caller's own provider included, so every answer not locked to a model is the caller's own seat with a note naming this command; a `--model` lock is still answered. `status` reports the same. The generated subagent definitions are left untouched until a valid profile says which makers to use.
