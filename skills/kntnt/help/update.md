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

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` and `npx` on `PATH`. Skill files move through `npx skills`.

**Network**

Required to fetch the current Catalog and Skill files. An unreachable Collection produces the bounded no-op described above.

## SEE ALSO

**/kntnt select --help**, **/kntnt uninstall --help**
