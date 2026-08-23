# release

## NAME

release - publish a version from the default branch

## SYNOPSIS

**/release** [**minor**|**major**|*X.Y.Z*] [**--no-build**] [**--yes**] [**--** *INSTRUCTION*]

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

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

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
