# model-selector reset

## NAME

model-selector reset - discard the profile and the standing objective, and the measurement on request

## SYNOPSIS

**/model-selector** **reset** [**--evidence**] [**--yes**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

Bare, this discards the profile — the answers you gave about Harnesses, makers and how you pay — and the standing choice between time and cost that `objective` set, `objective.json`, and leaves the interview to be held again. Until it is, every answer not locked to a model is your own seat, and with no standing choice, answers rank on cost until one is set again. The measurement is untouched, so a fresh profile inherits everything already learned about the models of the makers it chooses.

With **--evidence**, this machine's own measurement goes too: the measurement store, the units seen and not yet graded, and the `capture/` directory. That is the only way to discard it, and it has to be asked for by name. Whatever an earlier design of this Skill left in the directory goes with it — that directory among them, and the files no version writes or reads any more, named in the preview like everything else.

The catalogue is kept either way. It is public fact carrying its own sources and dates, and `update` fetches it again in any case.

The exact paths are named with their row or byte counts before anything is removed, and you confirm the list. A declined confirmation writes nothing. What went is reported per path, by the same counts the preview showed — nothing here is migrated, backfilled or reinterpreted.

Two things survive on purpose. The Harness hooks stay installed and go on measuring, because discarding a measurement is not switching measurement off; switching it off is unchecking this Skill in `/kntnt select`. And the generated subagent definitions are left where they are until the next `setup` rewrites the set.

## OPTIONS

**--evidence**

Discard this machine's measurement as well as the profile and the standing objective. Without it, only those two go.

**--yes**

Answer the confirmation yes rather than asking, for an unattended run.

**--data=**_PATH_

Use *PATH* as the profile, catalogue and measurement directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

A path the directory does not hold is reported absent rather than as a failure, and a preview that removes nothing is a success. An option with no work to do here is refused rather than ignored: the Skill names the error, prints this SYNOPSIS, changes nothing, and points at `/model-selector reset --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the capture store's own reporter, which supplies the counts for the working state this removes.

## SEE ALSO

**/model-selector setup --help**, **/model-selector evidence --help**, **/kntnt select**
