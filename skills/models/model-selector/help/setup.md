# model-selector setup

## NAME

model-selector setup - record whose models you want and how you pay for them

## SYNOPSIS

**/model-selector** **setup** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

A short interview, held once and revisited when something changes. It asks about Harnesses, Makers, model series and payment channels, in this order and one question at a time.

Which Harnesses this covers. The ones found on this machine are offered as the answer, and you say if that is wrong.

Which Makers you want models from: Claude, GPT and Grok, or another provider the catalogue holds, shown with one current representative per series.

Then, once per chosen Maker, all model series or an explicit non-empty selection of series names from the catalogue. A series is the catalogue's family, not a version: Sonnet without Haiku, or Luna and Sol without Terra and Astra, are examples rather than a fixed option list. All series includes future series. An explicit selection follows new releases of the selected series automatically and does not add new series. To omit a whole Maker, change the Maker choice.

Ordinary automatic answers and alternatives, exploration, Trials, escalation and generated Claude definitions respect that choice. Among admitted releases only the newest usable one is recommended after reachability, locks and the deliberation ceiling. An explicit `--model` lock remains a one-call override and `--scope=all` admits the whole catalogue with a valid profile. A release lock is honoured in the answer; Codex and OpenRouter commands carry the release named, while a Claude Code subagent uses its generated family-and-level definition.

How each maker is paid for, per Harness — because the same maker is often reached two ways at once, on a plan in one Harness and on API rates in another, and the two cost differently. A subscription answer names the plan under the whole name its provider markets it by, and the plans you are offered are the ones the catalogue holds, each with what it lists at. An API answer is a rate card: reached directly, the catalogue already holds one per model, the price OpenRouter publishes; reached through a gateway, that price is the charge itself through OpenRouter and a different arrangement's bill through any other, so you are asked what you pay per million tokens, and what you record replaces it.

Nothing the catalogue holds is asked of you. Prices, model lists and release dates are kept current by the catalogue pass, dated and attributed, and the subscriptions each provider sells come with a release of this collection. What a plan costs you per month is shown as the catalogue's own figure and is not recorded, nothing in this Skill having a use for it. An answer you have already made unambiguous is not asked for again. The complete profile, including all-series or explicit series choices, is shown before it is written, and nothing is written until you accept it.

Every figure here is USD per million tokens and nothing converts. A rate card in another currency is refused by name rather than added to a dollar bill in silence. An answer that matched none of the options offered is recorded as you typed it and said to be one, because that means the catalogue has fallen behind rather than that your answer is wrong — plans come with a release of this collection, and `/kntnt update` is what brings a newer one in.

Profiles without `families` retain all present and future series of their chosen Makers. Unknown series, empty lists and series for unchosen Makers are refused atomically. A later read keeps a selected series that temporarily disappears without dropping other choices or admitting other series; structural damage is reported as a damaged profile. The profile holds no credentials. Writing it also regenerates the subagent definitions that make a deliberation level launchable — one per selected Anthropic family and supported level, following its newest release — and removes the ones your new answers no longer justify. Where that directory had to be created, the definitions reach sessions started from then on rather than the one you are in.

Once the profile is written, or you decline the review, setup runs the catalogue pass once and reports what each of its sources said, so the catalogue is current straight away rather than after the next daily pass. It does not run where the profile was refused.

Setup neither asks about nor writes a status line. The quota guard's figure for the Claude channel is written by the `statusline` Feature as it draws, so Enabling that Feature in `/kntnt select` is what arms the guard there and removing it is what disarms it; if you have replaced the status line with one of your own, or have none, the Claude channel simply gets no guard, which stops nothing. The Codex figure is read from Codex's own session logs and needs nothing of you at all.

Until it is held, nothing is chosen for you. Without a profile — or with one from before makers were chosen, which is read as none rather than translated, or one that cannot be read — every answer not locked to a model is the seat you already have, with a note naming this command, and `status` says the same. The generated subagent definitions are left as they are until a profile says which makers to use.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile, catalogue and measurement directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An incomplete or unaccepted profile is not written. An option with no work to do here is refused rather than ignored: the Skill names the error, prints this SYNOPSIS, changes nothing, and points at `/model-selector setup --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the writer that validates the profile against the catalogue and syncs the generated subagent definitions, and the catalogue pass setup ends with, which reaches only Claude Code's and Codex's model lists and OpenRouter's public one. No web page is read.

## SEE ALSO

**/model-selector status --help**, **/model-selector reset --help**
