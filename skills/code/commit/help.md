# commit

## NAME

commit - commit the current working tree without pushing

## SYNOPSIS

**/commit** [**--yes**] [*MESSAGE*] [**--** *INSTRUCTION*]

## DESCRIPTION

`commit` records the complete working tree as one commit on the current branch and stops without pushing, tagging, or releasing.

Before committing, it reconciles `CHANGELOG.md` with the actual changes. It creates or extends `[Unreleased]`, avoids duplicating a change already recorded anywhere in the file, and edits no released section. When untracked files appear unsuitable for the repository, it includes a proposed `.gitignore` change in the same review.

Commits made with plain git are an ordinary path: the next `/commit` or `/push` that finds a dirty tree, or `/release`, reads every commit since the last `v*` tag and records in `[Unreleased]` what `CHANGELOG.md` does not already hold; a second run adds nothing. The cost follows commit-subject quality: an informative subject can carry a changelog entry, while a thin subject makes the run open the diff. Because reconciliation is deferred, `[Unreleased]` may lag between plain commits and that run, so a repository whose changelog is contractual per commit maintains it in the committing workflow; the dedupe instruction keeps the later run from adding a second entry.

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

`git` and `uv` on `PATH`.

**Skills**

The Manager must be Enabled so the dependency check can run.

## SEE ALSO

**/push --help**, **/release --help**
