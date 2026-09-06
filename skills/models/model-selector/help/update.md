# model-selector update

## NAME

model-selector update - fetch what can be fetched into the catalogue

## SYNOPSIS

**/model-selector** **update** [**--force**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

One bounded pass over the public facts this Skill reasons from: which models exist, which deliberation levels each supports, what each costs per token category, what independent benchmarks measure them at, and how the provider itself describes what each is for.

Rate cards are part of that. A price this Skill fetched carries the address it came from and the date it arrived, which is auditable in a way a figure typed in eight months ago is not — and a fetched fact with no source it can attribute is discarded rather than stored.

The pass is conditional, one connection at a time, and bounded against the clock before it starts. It starts no model and evaluates nothing. Sources fall due on the shipped cadence, which the profile does not override, and a model whose capability nothing has ranked makes its own benchmark index due regardless, so a newly adopted seat is not unrankable for a month by construction.

The same pass runs unattended at the end of a session while the Skill is Enabled. Running it by hand is the same work, immediately, and with **--force** it is that work with the cadence ignored.

A model discovered that your profile does not enable is written to the catalogue and left disabled. Adopting it is your own act, and `status` names it as something you may want. A pass in which nothing changed is a successful pass.

## OPTIONS

**--force**

Check every mutable source once, regardless of when it was last retrieved. A model detail page already known to be immutable is still not fetched again.

**--data=**_PATH_

Use *PATH* as the profile, catalogue and measurement directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An unreachable source is reported and the pass continues; nothing here fails a session. An option with no work to do here is refused rather than ignored: the Skill names the error, prints this SYNOPSIS, changes nothing, and points at `/model-selector update --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the refresh pass. This is the one command that uses the network by request; the unattended pass behind it is installed with the Skill and removed when it is Disabled.

## SEE ALSO

**/model-selector status --help**, **/model-selector setup --help**

