# commit

## NAME

commit - commit the current working tree without pushing

## SYNOPSIS

**/commit** [*MESSAGE*] [**--yes**] [**--** *INSTRUCTION*]

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

`git` and `uv` on `PATH`.

**Skills**

The Manager must be Enabled so the dependency check can run.

## SEE ALSO

**/push --help**, **/release --help**
