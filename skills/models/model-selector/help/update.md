# model-selector update

## NAME

model-selector update - read the providers' pages and adopt what they say

## SYNOPSIS

**/model-selector** **update** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

One pass over the public facts this Skill reasons from: which models exist, which deliberation levels each supports, what each costs per token category, how the provider itself describes what each is for, and what each provider's subscriptions are called and list at.

The reading is done by the agent, with whatever web tool your Harness gives it, off the `source_url` the catalogue already carries for every model and every plan, and off the provider's own pricing page where that address does not carry the rate card. A script has no web tool and does not pretend to one, so where your Harness gives the agent none, this command says so and changes nothing — the catalogue stands as it shipped, and every other command goes on answering from it.

What was read is then handed to the catalogue's own validator, which is what decides whether a fact may enter the store at all. Every rule is per entry: an entry with no address and no date is discarded by name, because a price nothing can attribute is worse than no price; a rate card in a currency other than USD or a unit other than per million tokens is refused rather than converted; a deliberation level this Skill has no ladder for is refused with the level named. The rest of the document is adopted. Only a document that is not the catalogue's shape at all is refused whole, and then nothing at all is written.

A model merges field by field over what is in force, so a document saying only what was read leaves everything else standing. A provider's plans are replaced whole, because a plan somebody stopped selling has to be able to disappear. `capability` is never fetched and never written: it is a seeded prior refined by measurement, and how a published benchmark maps onto its scale is not settled. Nor is `gateways`, the slug a gateway such as OpenRouter routes a model by, which no provider's page carries. Where the refreshed catalogue holds neither for a model, the shipped seed's still applies.

The report names, per model, whether it was added, changed or unchanged and which fields moved; per provider, which plan list replaced which; and every entry discarded, by name and with the rule it failed. A pass in which nothing changed is a successful pass.

A model discovered is eligible the moment it is written to the catalogue, wherever its maker is one your profile chooses. Nothing has to be enabled by hand, and a model of a maker you did not choose is never recommended.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile, catalogue and measurement directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An unreachable page is reported and the pass continues with what was read. A document the validator refuses whole exits non-zero, having written nothing. An option with no work to do here is refused rather than ignored: the Skill names the error, prints this SYNOPSIS, changes nothing, and points at `/model-selector update --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the catalogue's own reader and validator. Reading a page needs whatever web tool your Harness gives the agent. This command and `setup` are the only two that reach the network at all.

## SEE ALSO

**/model-selector status --help**, **/model-selector setup --help**

