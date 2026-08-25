# push

## NAME

push - commit the working tree and push the current branch

## SYNOPSIS

**/push** [**--yes**] [*MESSAGE*] [**--** *INSTRUCTION*]

## DESCRIPTION

`push` runs the `commit` Skill with the supplied arguments and then pushes the current branch. A clean working tree does not stop the push; commits already made but not yet sent are still pushed.

The branch is pushed to its configured upstream. When it has none, the Skill sets one on `origin`. The plan is shown before pushing, and a confirmation already obtained by `commit` is reused instead of asking twice.

## POSITIONAL ARGUMENTS

*MESSAGE*

Pass this text to `commit` as the commit message.

## OPTIONS

**--yes**

Commit and push without waiting for confirmation.

## DIAGNOSTICS

An invalid argument or option is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, commits and pushes nothing, and points to `/push --help`. An operand written before an option is out of order and is refused the same way.

A clean tree on a branch already level with its upstream is a successful no-op and is reported as such.

If no `origin` exists, the remote rejects a non-fast-forward update, or the branch cannot be pushed, the error is reported and any new local commit remains available for another attempt.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`git` and `uv` on `PATH`.

**Skills**

`commit` and the Manager must be Enabled.

## SEE ALSO

**/commit --help**, **/release --help**
