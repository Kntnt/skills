# commit

## NAME

commit - commit the current working tree without pushing

## SYNOPSIS

**/commit** [**--yes**] [*MESSAGE*] [**--** *INSTRUCTION*]

## DESCRIPTION

`commit` records the complete working tree as one commit on the current branch and stops without pushing, tagging, or releasing.

Before committing, it reconciles `CHANGELOG.md` with the actual changes. It creates or extends `[Unreleased]`, avoids duplicating a change already recorded anywhere in the file, and edits no released section. When untracked files appear unsuitable for the repository, it includes a proposed `.gitignore` change in the same review.

The Skill uses *MESSAGE* when supplied. Otherwise it derives one concrete subject line from the new changelog entries or, for changes without a user-facing entry, from the diff. It shows the changelog diff, commit message, and any `.gitignore` proposal before writing unless `--yes` is present.

## POSITIONAL ARGUMENTS

*MESSAGE*

Use this text as the commit message instead of deriving one.

## OPTIONS

**--yes**

Commit without waiting for confirmation.

## DIAGNOSTICS

An invalid argument or option is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, commits nothing, and points to `/commit --help`. An operand written before an option is out of order and is refused the same way.

A working tree with nothing to commit is a successful no-op and is reported as such.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`git` and `uv` on `PATH`.

**Skills**

The Manager must be Enabled so the dependency check can run.

## SEE ALSO

**/push --help**, **/release --help**
