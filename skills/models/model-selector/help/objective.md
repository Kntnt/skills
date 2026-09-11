# model-selector objective

## NAME

model-selector objective - set whether work is ordered on time or on cost, or say which is in force

## SYNOPSIS

**/model-selector** **objective** [**--data=**_PATH_] [**time**|**cost**] [**--** *INSTRUCTION*]

## DESCRIPTION

Whether work should be ordered on time or on cost depends on something only you know: how much of your subscription quota is left this week. With room to spare you want results as fast as possible; when the quota runs short you want the cheapest way to finish. So Model Selector keeps one standing objective, and every Skill that routes work inherits it rather than each growing a flag of its own.

With **time**, every answer asked for with no `--objective` is ranked on how long a finished job takes. With **cost**, on what a finished job costs — one attempt's price divided by its chance of success, a failed attempt being paid for again. A caller's own `--objective` still wins, so `/orchestrate --fast` orders its run on time whatever is set here. With nothing set, answers rank on cost: running out of quota mid-week stops everything, while a slower job is only slower.

Bare, this reports the objective in force and whether it is your standing choice or the default. A standing choice that cannot be read is reported as such, and answers rank on cost until it is set again.

Every answer names the objective it ranked on and whether it came from the caller, your standing choice, or the default. A run already under way that holds one objective for its whole length, as Orchestrate does, keeps the one it started with: a choice changed here reaches the next run.

The choice is kept on its own, beside the profile, so `setup` and the catalogue pass leave it standing. `reset` discards it with the profile, being an answer you gave.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile, catalogue and measurement directory instead of `~/.kntnt/model-selector/`.

## FILES

**~/.kntnt/model-selector/objective.json**

The standing choice, as `{"objective": "time"}` or `{"objective": "cost"}`. Absent, nothing is set. **--data** relocates it.

## DIAGNOSTICS

A word other than **time** or **cost** is refused, the Skill naming the error, printing this SYNOPSIS, changing nothing, and pointing at `/model-selector objective --help`; so is an option with no work to do here. A standing choice that cannot be read is reported rather than treated as an error, and no answer is ever refused over it.

## EXAMPLES

**/model-selector objective time**

Order every answer asked for with no `--objective` on how long a finished job takes, until `objective cost` sets it back.

**/model-selector objective**

Say whether time or cost is in force, and whether that is your standing choice or the default.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the interview's writer, which writes the standing choice. Nothing here reaches the network.

## SEE ALSO

**/model-selector --help**, **/model-selector setup --help**, **/model-selector reset --help**, **/orchestrate --help**
