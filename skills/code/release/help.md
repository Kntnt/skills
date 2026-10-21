# release

## NAME

release - publish a version from the default branch

## SYNOPSIS

**/release** [**--no-build**] [**--yes**] [**minor**|**major**|*X.Y.Z*] [**--** *INSTRUCTION*]

## DESCRIPTION

`release` turns `[Unreleased]` into a published version from the default branch. It reconciles regardless of the working tree and promotes the changelog under the current date, updates the file that carries the version (`package.json`, `composer.json`, `pyproject.toml`, `Cargo.toml`, `.claude-plugin/plugin.json`, a WordPress plugin header, or a `VERSION` file; a Project with none of these is versioned by its tag alone), commits and pushes through the `push` Skill, creates an annotated tag, builds any release assets, then pushes the tag and publishes a GitHub release from the promoted changelog section.

If the Project has an executable `bin/build-release-assets`, written in any language, the release empties `release-assets/`, runs it while HEAD carries the new tag, and creates the GitHub release with every file it leaves there, so the release never appears without its assets. A Project without it attaches nothing, and neither does a release made with `--no-build`, whatever `release-assets/` holds. The plan, changelog diff, selected version, and build command are shown before anything is written unless `--yes` is present.

The displayed plan includes the complete changelog commit inventory; a request to see every commit is answered by re-running the plan with its full-inventory option.

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

Build and attach no release assets, even when the Project has `bin/build-release-assets`.

**--yes**

Release without waiting for confirmation.

## DIAGNOSTICS

An invalid argument or option is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, publishes nothing, and points to `/release --help`. An operand written before an option is out of order and is refused the same way.

A branch other than the default branch, an empty `[Unreleased]`, or a version that cannot be rewritten unambiguously stops the release before a partial bump is left behind.

If `gh` is unavailable or the remote is not GitHub, no release assets are built, the tag is pushed, and the Skill reports that the GitHub release step was skipped. The rest of the release remains complete.

If git tracks a file in `release-assets/`, the release refuses to empty that directory, and it stops the same way when `bin/build-release-assets` fails, leaves nothing there, or leaves a directory there. Nothing is then published: the release commit is pushed, the tag exists only in the local repository, and no GitHub release is created. Once the build is fixed, running `ship.py apply publish` from the Collection Library with the same version finishes the release; a fix that needs a commit first moves the local tag to it.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`git` and `uv` on `PATH`. `gh` is required only to publish the GitHub release and attach its assets.

**Skills**

`push` and the Manager must be Enabled.

## SEE ALSO

**/commit --help**, **/push --help**
