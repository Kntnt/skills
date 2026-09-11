# The user chooses makers, and every model a chosen maker offers is eligible

This record amends the profile semantics of [ADR-0182](0182-how-a-model-is-chosen-and-how-the-choice-is-measured.md). The profile no longer carries a list of the model ids the user enabled; it carries the makers the user chose. Its "one file per enabled Anthropic model and supported level" becomes one file per Anthropic model and supported level wherever Anthropic is a chosen maker. What the rules now are is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own shipped files. This record argues the case.

## What the model list did

**Nothing new ever came into use by itself.** On the maintainer's machine the profile listed seven model ids. A model the catalogue gained afterwards was disabled until somebody added it by hand, so the pool the selector ranked was frozen at the day of the interview. The selector exists to decide between models on what it has measured, and it could never measure a model nobody had remembered to add.

**Leaving one model of a maker out was a preference the measurements already express.** A model that finishes the work less often, or costs more to finish it, loses the ranking without being removed by hand. Removing it by hand also stops the exploration that would find out it was cheaper than it looked, since a model outside the pool is never tried.

## The rule

**The user chooses makers, and setup is where they choose.** On 2026-09-11 the maintainer decided that the unit the user chooses is the maker — Claude, GPT, Grok — and not the model. Setup asks which makers to use beside the channels it already asks about, since both are the same kind of answer about the user's own arrangements, and no other verb takes it. A maker is recorded as the catalogue's provider id (`anthropic`, `openai`, `spacexai`), so the catalogue gains no field. The word is *maker* because *family* already means Fable, Opus and Sonnet in the catalogue and in the generated agent definitions.

**Eligibility is computed, and reach is unchanged.** A catalogue model is a candidate where its maker is chosen and the call can reach it exactly as before: a channel pays for it, or it belongs to the caller's own provider, which needs none. `--scope=all` is still the whole catalogue for a valid profile. Which models a maker offers is decided when models are added to the catalogue. The user cannot enable or disable a single model within a maker, and a per-call `--model` lock stays as it was.

**The generated agent definitions follow the chosen makers.** Every Anthropic model the catalogue holds gets one file per supported level wherever the profile chooses Anthropic, with no channel needed, since Anthropic is the provider a Claude Code seat already pays for. A valid profile that does not choose Anthropic leaves none.

**A missing, old-shape or damaged profile inherits.** A profile that cannot be read, or carries a maker or a channel this Skill cannot route by, or carries the old lists beside makers, stands in as a profile choosing no maker. So does a profile with a model list and no makers, which is not translated. With no maker chosen nothing is eligible, the caller's own provider included, so every call not locked to a model is answered with the caller's own seat and a note naming `/model-selector setup`. A call locked to a model is still answered. ADR-0182 already said this of a missing profile: the caller runs the work on its own seat. The code had drifted from it to a fallback over the whole catalogue, a wider pool than anybody chose. Without a valid profile the generated agent definitions are left untouched, because the stand-in would remove every definition the last real answers justified.

## The alternatives

**Keep the model list and add new models to it automatically.** Rejected. A list that grows by itself as a maker ships is a maker choice written out model by model, and it goes on offering a way to remove one model that the rule above gives no reason for.

**Makers, with single models switched off within them.** Rejected. Two ways to say one thing, the second of which does by hand what the ranking and the measurements already do, and denies the measurement the rows that would correct it. A user who wants one model for one call has the `--model` lock.

**Translate an old profile into makers.** Rejected. The makers of the listed models would widen what the user chose without saying so, and this collection has one user, who runs setup again after the release.

**Keep the whole catalogue as the pool for a missing profile.** Rejected. It is a pool nobody chose, and with makers as the unit a stand-in choosing none is the honest reading of an unanswered interview.
