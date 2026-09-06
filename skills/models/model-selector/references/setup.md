# The setup interview

Read when running `/model-selector setup`. This is the script for a conversation and the shape of what it produces.

## What the interview is for

Only the user can say which Harnesses this covers, which providers they are willing to be sent to, which of those providers' models they want in the pool, and how the tokens are actually paid for. Everything else — which models exist, what each supports, what each costs, what each is good at — is fetched, dated and attributed, and asking a person for it wastes their time and gets a worse answer. **Never ask for a fact the catalogue holds or `update` can retrieve.** If a price, a model list, a release date or a provider's own description of a model is missing, that is a gap in the catalogue and `/model-selector update` is the fix, not a question.

Ask one question at a time. Do not ask again for something the user has already made unambiguous — in the invocation, in the Contextual Instruction, or earlier in this conversation. Confirm such an answer inside the next question rather than re-posing it.

## The four questions, in this order

### 1. Which Harnesses

Offer the ones detected on this machine as the answer and ask only whether that is right. Detection is a filesystem probe: `~/.claude` is Claude Code, `~/.codex` is Codex, `~/.config/opencode` is OpenCode. A Harness the user names that was not detected is accepted — they may be about to install it — and one that was detected and is not wanted is dropped.

The answer decides which models can be reached at all, and which generated subagent definitions are worth writing.

### 2. Which providers

Name the providers the catalogue holds, each with the models it currently offers, and ask which of them the user wants suggestions from. A provider left out is never recommended however well it scores.

This is a question about willingness — an account, a policy, a preference — and not about capability, so do not argue for a provider or characterise one as better. Show what each has and let the user choose.

### 3. Which models

For each chosen provider, list its current models with the provider's own one-line description of what each is for, and offer them all ticked. The user unticks what they do not want.

Show the provider's positioning as the provider's, attributed and dated. Do not summarise it, rank the models, or add an opinion of your own: a recommendation from measurement is what this Skill is for, and a recommendation from prose here would contaminate it.

### 4. How each provider is paid for, per Harness

Ask per provider **and per channel**, because the same provider is commonly reached two ways at once — a subscription plan inside one Harness and API rates from another — and the two cost differently for the same tokens. For each provider the user kept, and each Harness that can reach it, ask which of the two applies. Both can apply, in different Harnesses, and one channel per provider and Harness is what gets recorded.

**A subscription** means naming the plan and its tier:

| Provider | Tiers |
| --- | --- |
| Anthropic | free tier, Pro, Max 5x, Max 20x |
| OpenAI | Free, Plus, Pro, Business |
| xAI | free tier, SuperGrok, SuperGrok Heavy |

A provider the catalogue holds that is not in this table is asked the same way, with its own published tiers offered from the catalogue.

**An API channel** means a rate card, which the catalogue already holds per model and token category. Ask only whether the provider is reached directly or through a gateway, and which gateway where that is the answer — a gateway prices differently, and that is a fact about the user's arrangement rather than about the model.

Do not ask what a plan costs per month. The list price is a fetched fact; it is shown in the review below, where the user corrects it if their own price differs.

## Before writing

Show the complete profile — Harnesses, providers, models, and one line per payment channel naming provider, Harness, plan and tier or rate card and gateway, and what each subscription costs per month. Ask for acceptance. Nothing is written until it is accepted, and a declined review returns to the question the user wants changed rather than restarting the interview.

## What is written

Assemble one JSON object and hand its path to the writer; never edit the profile file directly.

    uv run "$HERE/scripts/setup_apply.py" [--data=<directory>] <path-to-profile-json>

    {
      "harnesses": ["claude-code", "codex"],
      "providers": ["anthropic", "openai"],
      "models": ["claude-opus-5", "claude-sonnet-5", "gpt-5.4"],
      "channels": [
        {"provider": "anthropic", "harness": "claude-code", "pay": "subscription",
         "plan": "Claude", "tier": "Max 20x", "monthly": 200.0, "currency": "USD",
         "gateway": null},
        {"provider": "openai", "harness": "codex", "pay": "api",
         "plan": null, "tier": null, "monthly": null, "currency": null,
         "gateway": null}
      ],
      "answered_at": "2026-09-06T09:12:00Z"
    }

`models` holds exact catalogue model ids, not family aliases: an alias is resolved when a lock is read, and the profile is a statement about releases. `pay` is `subscription` or `api` and nothing else. `plan` is the provider's subscription product and `tier` the level of it from the table above; both are null on an API channel. `gateway` names the gateway where one stands between the user and the provider, and is null on a direct channel.

The writer validates the object against the catalogue, writes it atomically at mode 0600, and regenerates the subagent definitions — one per enabled Anthropic model and supported deliberation level — removing the ones the new answers no longer justify. Render its report. Where it says the definitions directory had to be created, say that Claude Code reads that directory as a session starts, so the new definitions reach sessions started from now on rather than this one.

The profile holds no credential of any kind, and nothing here asks for one.

## When the interview is not held

Setup is not a precondition for anything. An absent or damaged profile degrades to every catalogue model the detected Harnesses can reach, which is a wider pool than anyone chose but is still an answer. `status` reports it, names this command, and stops nothing.
