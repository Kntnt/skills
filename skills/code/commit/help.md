# commit

## NAME

commit - commit the current working tree without pushing

## SYNOPSIS

**/commit** [*MESSAGE*] [**--yes**]

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

An invalid argument or option is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, commits nothing, and points to `/commit --help`.

A working tree with nothing to commit is a successful no-op and is reported as such.

## DEPENDENCIES

**Binaries**

`git` and `uv` on `PATH`.

**Skills**

The Manager must be Enabled so the dependency check can run.

## SEE ALSO

**/push --help**, **/release --help**
