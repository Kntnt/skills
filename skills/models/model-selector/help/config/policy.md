# model-selector config policy

## NAME

model-selector config policy - inspect or restore the Standing Policy routing starts from

## SYNOPSIS

**/model-selector** **config** **policy** [**show**|**reset**] [**--data=**_PATH_] [*COHORT*] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config policy` reads and restores the Standing Policy, which is where one workload Cohort starts on the Rung ladder and how far up and down that ladder routing may go. It ships working: nothing has to be set for routing to have a policy, and there is no `set`. A Cohort's policy moves only when measured failures trip its threshold, and it moves only upward; what brings it back down is a deliberate act of the user's — this command's `reset`, which restores the shipped default and keeps the history, or `config reset --evidence`, which discards the measurement the movement rests on and the history with it.

The policy lives beside `config.json` in the selected data directory, as `standing-policy.json` with an append-only `standing-policy-history.jsonl` next to it. Only Cohorts something moved are stored there; every other Cohort has the shipped default. The store is script-owned and is never hand-edited, so the profile's own `config.lock` protocol does not apply to it.

A policy change is frozen into the next routing context and covered by its snapshot identity, so it reaches the next run rather than one already under way.

## COMMANDS

**show** [*COHORT*]

Display the effective policy, its bounds, and the movements behind it. This is the default when no policy subcommand is supplied.

**reset** [*COHORT*]

Restore the shipped default for one Cohort, or for every overridden Cohort, after confirmation.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An unknown policy subcommand, a second Cohort operand, or an operand written after an option is refused rather than ignored. The Skill prints the addressed page's SYNOPSIS, changes nothing, and points to the corresponding `--help` invocation.

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

**/model-selector config policy show --help**, **/model-selector config policy reset --help**, **/model-selector config show --help**
