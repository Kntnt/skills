# model-selector status

## NAME

model-selector status - report what is known, how fresh it is, and what is wanted from you

## SYNOPSIS

**/model-selector** **status** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

Four accounts, none of which asks a question, changes anything, or reaches the network.

The profile: when it was answered, which Harnesses, providers, models and payment channels it holds. Where it is absent or unreadable, that is said plainly, along with the consequence — every catalogue model the detected Harnesses can reach is treated as available until you run `setup`. A profile older than ninety days, a provider in the catalogue you have never been asked about, and how many catalogue models the profile does not enable are named here too.

The catalogue: how fresh its facts are, read off the dates the entries themselves carry — the newest and the oldest of them. Past thirty days on the newest, `update` is named as what brings them current. Nothing waits on that and nothing is placed where a model would read it, deliberately: a reminder inside a session changes the thing being measured.

The measurement: how many units have been recorded, over what span of dates, how many are waiting to be graded, and when the grader last ran.

The integration, per Harness this collection has an adapter for: `healthy`, `gated` where the Harness is holding it behind a trust decision this collection will not make for you, `degraded`, `absent`, or `unsatisfied` where that Harness's lifecycle cannot carry the contract at all. Beside it, whether that Harness's finished session record can supply measurements, and how much the capture store holds.

Everything here is a report. Nothing on this page stops a run.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile, catalogue and measurement directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An absent or unreadable profile is reported rather than treated as an error. An option with no work to do here is refused rather than ignored: the Skill names the error, prints this SYNOPSIS, changes nothing, and points at `/model-selector status --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the two readers this page renders: the catalogue's own print, whose dates say how fresh its facts are, and the capture integration's account of its health. Neither reaches the network.

## SEE ALSO

**/model-selector setup --help**, **/model-selector update --help**, **/model-selector evidence --help**
