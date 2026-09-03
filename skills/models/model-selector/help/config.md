# model-selector config

## NAME

model-selector config - inspect or revise the model and access profile

## SYNOPSIS

**/model-selector** **config** [**show**|**history**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **config** **reset** [**--evidence**] [**--yes**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **config** **add** [**--data=**_PATH_] (**model**|**channel**) [**--** *INSTRUCTION*]

**/model-selector** **config** (**edit**|**remove**) [**--data=**_PATH_] (**model**|**channel**) *ID* [**--** *INSTRUCTION*]

**/model-selector** **config** **policy** [**show**|**reset**] [**--data=**_PATH_] [*COHORT*] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config` manages the persisted profile without network access or evaluations. Bare `config` is equivalent to `config show`.

Configuration changes are validated, saved as revisions, and reported with any newly due evidence or invalidated frontiers. An ordinary configuration change never deletes the evidence ledger; `config reset --evidence` is the one exception, discarding it by name after confirmation and leaving the profile untouched.

## COMMANDS

**show**

Display the active profile. This is the default when no configuration subcommand is supplied.

**add** (**model**|**channel**)

Add one model selection or access channel through a guided interview.

**edit** (**model**|**channel**) *ID*

Edit one identified model selection or access channel.

**remove** (**model**|**channel**) *ID*

Remove one identified selection or channel after confirmation.

**policy**

Inspect or restore the Standing Policy each workload Cohort routes under.

**history**

Display profile revision timestamps and summaries.

**reset**

Remove the active profile after confirmation while retaining history and evidence; `--evidence` is the mirror move, discarding this machine's own measurement after confirmation while retaining the profile and its history.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

**--evidence**

For `reset`, discard this machine's own measurement rather than the profile. See `/model-selector config reset --help`.

**--yes**

For `reset --evidence`, answer its confirmation yes rather than asking. Valid only combined with `--evidence`.

## DIAGNOSTICS

An unknown or incomplete configuration subcommand is refused rather than ignored. The Skill prints the addressed page's SYNOPSIS, changes nothing, and points to the corresponding `--help` invocation. An operand written before an option is out of order and is refused the same way.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] adds an optional Contextual Instruction. The first standalone, unquoted `--` is the reserved separator. Everything before it is the Formal Invocation; everything after it, including later `--` tokens, is guidance. The guidance may start on the same line or after blank lines and must contain non-whitespace text.

`--force`, `foo--bar`, `` `--` ``, and `"--"` are not separators. Without the separator, the whole payload remains formal input, including later lines and paragraphs.

After validating the Formal Invocation, the Skill uses guidance to clarify or narrow open choices. Guidance cannot contradict formal input or an invariant, widen the Skill, bypass a gate, or request unrelated work. Redundant but applicable guidance is valid. Applicable Conversation Context follows the same limits.

Malformed formal input or an empty instruction takes the syntax refusal. The Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Context on an exact help route takes the context refusal without rendering the page.

Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal. The Skill names the guidance and its boundary, reports the mutation outcome, prints no synopsis, and stops without applying a valid remainder.

Unaddressable guidance can affect nothing inside the Skill's contract. Guidance settled by a documented precedence is suppressed instead: the run continues and reports the suppression where useful. Suppression for one parameter does not invalidate guidance that applies to another.

Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict appears only after a legitimate effect, it stops before the next effect and reports the exact partial outcome. It rolls nothing back unless atomic behaviour was promised.

A nested Skill receives only relevant guidance through an explicit Contextual Instruction. Successful execution requires no context acknowledgement; an existing report names a materially changed choice where useful.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector config show --help**, **/model-selector config add --help**, **/model-selector config edit --help**, **/model-selector config remove --help**, **/model-selector config policy --help**, **/model-selector config history --help**, **/model-selector config reset --help**
