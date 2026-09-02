# release

## NAME

release - publish a version from the default branch

## SYNOPSIS

**/release** [**--no-build**] [**--yes**] [**minor**|**major**|*X.Y.Z*] [**--** *INSTRUCTION*]

## DESCRIPTION

`release` turns `[Unreleased]` into a published version from the default branch. It reconciles regardless of the working tree and promotes the changelog under the current date, updates the files that carry the version, commits and pushes through the `push` Skill, creates and pushes an annotated tag, and publishes a GitHub release from the promoted changelog section.

If the Project provides a conventional archive build, the resulting archive is attached to the release. The plan, changelog diff, selected version, and build command are shown before anything is written unless `--yes` is present.

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

Skip the archive even when the Project has a build command.

**--yes**

Release without waiting for confirmation.

## DIAGNOSTICS

An invalid argument or option is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, publishes nothing, and points to `/release --help`. An operand written before an option is out of order and is refused the same way.

A branch other than the default branch, an empty `[Unreleased]`, or a version that cannot be rewritten unambiguously stops the release before a partial bump is left behind.

If `gh` is unavailable or the remote is not GitHub, the tag is pushed and the Skill reports that the GitHub release step was skipped. The rest of the release remains complete.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] adds an optional Contextual Instruction. The first standalone, unquoted `--` is the reserved separator. Everything before it is the Formal Invocation; everything after it, including later `--` tokens, is guidance. The guidance may start on the same line or after blank lines and must contain non-whitespace text.

`--force`, `foo--bar`, `` `--` ``, and `"--"` are not separators. Without the separator, the whole payload remains formal input, including later lines and paragraphs.

After validating the Formal Invocation, the Skill uses guidance to clarify or narrow open choices. Guidance cannot contradict formal input or an invariant, widen the Skill, bypass a gate, or request unrelated work. Redundant but applicable guidance is valid. Applicable Conversation Context follows the same limits.

Malformed formal input or an empty instruction takes the syntax refusal. The Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Context on an exact help route takes the context refusal without rendering the page.

Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal. The Skill names the guidance and its boundary, reports the mutation outcome, prints no synopsis, and stops without applying a valid remainder.

Unaddressable guidance can affect nothing inside the Skill's contract. Guidance settled by a documented precedence is suppressed instead: the run continues and reports the suppression where useful. Suppression for one parameter does not invalidate guidance that applies to another.

Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict appears only after a legitimate effect, it stops before the next effect and reports the exact partial outcome. It rolls nothing back unless atomic behaviour was promised.

A nested Skill receives only relevant guidance through an explicit Contextual Instruction. Successful execution requires no context acknowledgement; an existing report names a materially changed choice where useful.

The following schematic cases pin the split independently of any one Skill's Formal Invocation grammar; `\n\n` denotes two newline characters in one payload.

| Case | Envelope | Formal Invocation | Contextual Instruction | Outcome |
| --- | --- | --- | --- | --- |
| Same line | `/skill --force -- Preserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |
| Blank lines | `/skill --force --\n\nPreserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |
| Empty suffix | `/skill --force --   ` | `/skill --force` | — | Syntax refusal |
| Later separator | `/skill -- Preserve -- deployment facts` | `/skill` | `Preserve -- deployment facts` | Envelope valid; formal grammar next |
| No separator | `/skill Preserve deployment facts` | `/skill Preserve deployment facts` | — | No split; formal grammar decides |
| Attached and quoted | ``/skill --force foo--bar `--` "--"`` | ``/skill --force foo--bar `--` "--"`` | — | No split; formal grammar decides |
| Exact help | `/skill --help -- Explain this page` | `/skill --help` | `Explain this page` | Context refusal; render nothing |

## DEPENDENCIES

**Binaries**

`git` and `uv` on `PATH`. `gh` is required only to publish the GitHub release and attach an archive.

**Skills**

`push` and the Manager must be Enabled.

## SEE ALSO

**/commit --help**, **/push --help**
