# push

## NAME

push - commit the working tree and push the current branch

## SYNOPSIS

**/push** [*MESSAGE*] [**--yes**]

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

An invalid argument or option is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, commits and pushes nothing, and points to `/push --help`.

A clean tree on a branch already level with its upstream is a successful no-op and is reported as such.

If no `origin` exists, the remote rejects a non-fast-forward update, or the branch cannot be pushed, the error is reported and any new local commit remains available for another attempt.

## DEPENDENCIES

**Binaries**

`git` and `uv` on `PATH`.

**Skills**

`commit` and the Manager must be Enabled.

## SEE ALSO

**/commit --help**, **/release --help**
