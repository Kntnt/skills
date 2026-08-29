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

`uv` on `PATH`. Commands that fetch the Collection or move Skill files also require `npx`; files move through `npx skills`.

**Network**

Select and Update normally fetch the Catalog, and changing commands fetch Skill files. Offline fallback behaviour is documented on each command page.

## SEE ALSO

**/kntnt help --help**, **/kntnt select --help**, **/kntnt update --help**, **/kntnt uninstall --help**, **/<skill> --help**
