# kntnt

## NAME

kntnt - manage which collection Skills are Enabled

## SYNOPSIS

**/kntnt** [**--** *INSTRUCTION*]

**/kntnt** **help** [*COMMAND*] [**--** *INSTRUCTION*]

**/kntnt** **select** [**--on=**_SKILL_]... [**--off=**_SKILL_]... [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**] [**--** *INSTRUCTION*]

**/kntnt** **update** [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**] [**--** *INSTRUCTION*]

**/kntnt** **uninstall** [**--yes**] [**--dry-run**] [**--** *INSTRUCTION*]

## DESCRIPTION

`kntnt` lists, Enables, refreshes, and removes Collection Skills across detected Harnesses. Other Skills are invoked by their own names.

Bare `kntnt` prints this page. Use `/kntnt <command> --help` or `/kntnt help <command>` for command help. Select can show help for a Skill that is not yet Enabled.

Select lists every Catalog Skill, Enabled or not.

Select and Update target Global by default; **--project** targets the current Project. Harnesses are detected on every run.

A real Global Update without formal **--yes** shows its complete plan and applies only after approval of that exact plan.

## COMMANDS

**help** [*COMMAND*]

Print this page or the page for one Manager command.

**select**

List every Catalog Skill and change which ones are Enabled, or apply explicit `--on` and `--off` deltas.

**update**

Refresh Enabled Skills that differ from the Collection, handle new and Withdrawn Catalog entries, and re-check Dependencies.

**uninstall**

Remove the Collection from the machine, with the Manager removed last. Project copies are left untouched.

## OPTIONS

**--on=**_SKILL_

Enable a named Skill without opening the Select list. Valid only with `select` and repeatable.

**--off=**_SKILL_

Disable a named Skill without opening the Select list. Valid only with `select`, repeatable, and gated by `--yes` because it deletes files.

**--project**, **--project=on**

Target the current Project instead of Global. `--project=off` has the same effect as omitting the option. Valid only with `select` and `update`.

**--yes**

Answer yes to every yes-or-no question. Valid with `select`, `update`, and `uninstall`. Only a current Formal Invocation's **--yes** authorizes unattended Global Update.

**--dry-run**

Run `select`, `update`, or `uninstall` in a discarded temporary home and report the result without changing the machine.

## DIAGNOSTICS

An unknown command or a flag with no work to do is refused rather than ignored. The Manager prints the addressed SYNOPSIS, performs no work, and points to the full page. No command accepts **--force**.

Global Update requires formal **--yes** or approval of the exact displayed plan. A changed plan requires fresh approval.

When safe, a failed Catalog fetch uses the stored Catalog and reports the resulting limits.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`. Commands that fetch the Collection or move Skill files also require `npx`; files move through `npx skills`.

**Network**

Select and Update normally fetch the Catalog, and changing commands fetch Skill files. Offline fallback behaviour is documented on each command page.

## SEE ALSO

**/kntnt help --help**, **/kntnt select --help**, **/kntnt update --help**, **/kntnt uninstall --help**, **/<skill> --help**
