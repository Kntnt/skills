# model-selector config policy show

## NAME

model-selector config policy show - display the Standing Policy and what moved it

## SYNOPSIS

**/model-selector** **config** **policy** **show** [**--data=**_PATH_] [*COHORT*] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config policy show` displays the effective Standing Policy: the Rung routing starts an unmeasured Cohort at, the inclusive floor and ceiling it stays between, the failure threshold that may move it, and the exploration budget. With no *COHORT* it shows the shipped default, every Cohort that has moved, and the whole movement history. With one it shows only that Cohort's effective policy and its own history. It also reports `store_damaged`: routing always has a complete policy because the shipped default is one, so a stored layer that will not parse never stops a run — but it does put every ratcheted Cohort back at its cold start, and this is what tells that apart from a Cohort that never moved.

Every movement in that history was appended by one of two things: the failure threshold, which the evidence import evaluates whenever it records judged attempts and which names the run keys that tripped it, or `config policy reset`, which names nobody. Nothing else writes the store, and nothing moves a Cohort down but a deliberate act of the user's: this command's `reset`, which restores the shipped default and keeps the history, or `config reset --evidence`, which discards the whole store and its history together rather than writing a row to either.

The shipped default prints its values symbolically — `cold_start`, `weakest_enabled`, `main_seat` — because each one resolves against the candidate ladder of the individual request, and each printed line says so. A moved Cohort prints the exact Rung stored for it.

The command reads local configuration only; it performs no network access, evaluation, or write. Bare `/model-selector config policy` has the same effect.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

An absent store is reported as the shipped default rather than as an error. An unsupported option is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector config policy show --help`.

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

**/model-selector config policy reset --help**, **/model-selector config show --help**, **/model-selector route --help**
