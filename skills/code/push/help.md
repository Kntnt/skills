# push

## NAME

push - commit the working tree and push the current branch

## SYNOPSIS

**/push** [**--yes**] [*MESSAGE*] [**--** *INSTRUCTION*]

## DESCRIPTION

`push` runs the `commit` Skill with the supplied arguments and then pushes the current branch. A clean working tree does not stop the push; commits already made but not yet sent are still pushed.

A clean-tree push does not reconcile the changelog, so plain commits are recorded at the next `/commit` that finds changes or at `/release`.

The branch is pushed to its configured upstream. When it has none, the Skill sets one on `origin`. The plan is shown before pushing, and a confirmation already obtained by `commit` is reused instead of asking twice.

The displayed plan uses a bounded commit excerpt; ask to see every commit to have the Skill re-run its plan with the full inventory.

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

`commit` and the Manager must be Enabled.

## SEE ALSO

**/commit --help**, **/release --help**
