# kntnt update

## NAME

kntnt update - refresh the Collection and re-check Dependencies

## SYNOPSIS

**/kntnt** **update** [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**] [**--** *INSTRUCTION*]

## DESCRIPTION

`kntnt update` refreshes Enabled Skills whose files differ from the current Catalog and leaves matching files untouched. Global is the default layer. Refreshing overwrites local Skill changes.

The Manager is checked on every successful update. Withdrawn Skills are removed without confirmation; new Catalog Skills are reported and offered for Enablement.

A real Global update without formal **--yes** shows the complete refresh, Enablement, removal, and destination plan. A later answer authorizes only that exact plan; changed or incomplete approval is refused before writing.

Contextual Instruction, Conversation Context, earlier answers, broad repair requests, and agent handoffs do not authorize Global mutation. A dry run needs no confirmation.

After changes, Update checks Dependencies and Capabilities and replaces the stored Catalog.

## OPTIONS

**--project**, **--project=on**

Target the current Project instead of Global. `--project=off` has the same effect as omitting the option.

**--yes**

Answer yes to confirmations, including Enabling every new Catalog entry. For Global Update, the flag must be in the current Formal Invocation. The report names every newly Enabled Skill.

**--dry-run**

Run in a discarded temporary home and report the result without changing the selected layer. The isolated cache makes this slower.

## FILES

**Harness Integrations**

A Skill may own a Harness Integration: what it writes into a Harness's own configuration so the Harness calls that Skill at its own lifecycle moments. It is written outside the Skill's own directory, so deleting the Skill's files does not reach it. A Feature owns Harness Integrations and nothing else, so this is the whole of what enabling or disabling one does. Refreshing a Skill in Global asks that Skill to install what it owns again, and a Withdrawn Skill is asked to remove them before its files go; the Project layer installs and removes none. The report says what became of each.

## OFFLINE OPERATION

Offline, Update changes nothing and leaves the stored Catalog untouched.

## DIAGNOSTICS

An invalid argument or flag with no work to do is refused rather than ignored. The Manager prints the SYNOPSIS, changes nothing, and points to this page.

Global Apply without approval for the exact current plan is refused before writing. Run Update again to approve a changed plan.

New Harnesses are detected automatically.

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

**Binaries**

`uv` and `npx` on `PATH`. Skill files move through `npx skills`.

**Network**

Required to fetch the current Catalog and Skill files. An unreachable Collection produces the bounded no-op described above.

## SEE ALSO

**/kntnt select --help**, **/kntnt uninstall --help**
