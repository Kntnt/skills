# release

## NAME

release - publish a version from the default branch

## SYNOPSIS

**/release** [**minor**|**major**|*X.Y.Z*] [**--no-build**] [**--yes**]

## DESCRIPTION

`release` turns `[Unreleased]` into a published version from the default branch. It reconciles and promotes the changelog under the current date, updates the files that carry the version, commits and pushes through the `push` Skill, creates and pushes an annotated tag, and publishes a GitHub release from the promoted changelog section.

If the Project provides a conventional archive build, the resulting archive is attached to the release. The plan, changelog diff, selected version, and build command are shown before anything is written unless `--yes` is present.

Without a version operand, the Skill derives the next version from `[Unreleased]`: a `Removed` section or breaking change selects a major bump, except below 1.0.0 where it selects a minor bump; `Added` selects minor; every other change selects patch.

## POSITIONAL ARGUMENTS

**minor**

Force a minor version bump.

**major**

Force a major version bump.

*X.Y.Z*

Publish this exact semantic version.

## OPTIONS

**--no-build**

Skip the archive even when the Project has a build command.

**--yes**

Release without waiting for confirmation.

## DIAGNOSTICS

An invalid argument or option is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, publishes nothing, and points to `/release --help`.

A branch other than the default branch, an empty `[Unreleased]`, or a version that cannot be rewritten unambiguously stops the release before a partial bump is left behind.

If `gh` is unavailable or the remote is not GitHub, the tag is pushed and the Skill reports that the GitHub release step was skipped. The rest of the release remains complete.

## DEPENDENCIES

**Binaries**

`git` and `uv` on `PATH`. `gh` is required only to publish the GitHub release and attach an archive.

**Skills**

`push` and the Manager must be Enabled.

## SEE ALSO

**/commit --help**, **/push --help**
