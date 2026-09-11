# model-selector setup

## NAME

model-selector setup - record whose models you want and how you pay for them

## SYNOPSIS

**/model-selector** **setup** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

A short interview, held once and revisited when something changes. It asks three things, in this order and one question at a time.

Which Harnesses this covers. The ones found on this machine are offered as the answer, and you say if that is wrong.

Which makers you want models from: Claude, GPT and Grok, each shown with the models it currently offers. Every model a maker you choose offers is a candidate, one it releases later included, and only a model of a maker you choose is ever recommended, however good another maker's models look, unless a call asks for `--scope=all`, which admits the whole catalogue. You do not pick models one by one: the measurements decide between them, and a model you want for one piece of work is named with `--model`.

How each maker is paid for, per Harness — because the same maker is often reached two ways at once, on a plan in one Harness and on API rates in another, and the two cost differently. A subscription answer names the plan under the whole name its provider markets it by, and the plans you are offered are the ones the catalogue holds, each with what it lists at and the date that was retrieved. An API answer is a rate card: reached directly, the catalogue already holds one per model; reached through a gateway it does not, a gateway pricing differently from the provider whose model it is, so you are asked what you pay per million tokens.

Nothing you can look up is asked of you. Prices, model lists, subscriptions, release dates and each provider's own description of what its models are for are fetched, dated and attributed, and refreshed by `update`. What a plan costs you per month is shown as the catalogue's own figure and is not recorded, nothing in this Skill having a use for it. An answer you have already made unambiguous is not asked for again. The complete profile is shown before it is written, and nothing is written until you accept it.

Every figure here is USD per million tokens and nothing converts. A rate card in another currency is refused by name rather than added to a dollar bill in silence. An answer that matched none of the options offered is recorded as you typed it and said to be one, because that means the catalogue has fallen behind rather than that your answer is wrong — `update` is what brings the plans back into line.

The profile holds no credentials. Writing it also regenerates the subagent definitions that make a deliberation level launchable — one per Anthropic model and supported level, where Anthropic is a maker you chose — and removes the ones your new answers no longer justify. Where that directory had to be created, the definitions reach sessions started from then on rather than the one you are in.

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

`uv` runs the writer that validates the profile against the catalogue and syncs the generated subagent definitions. Where the catalogue has gone stale the interview opens by reading the providers' pages, exactly as `update` does, which needs whatever web tool your Harness gives the agent; without one it offers what is already on disk.

## SEE ALSO

**/model-selector status --help**, **/model-selector update --help**, **/model-selector reset --help**
