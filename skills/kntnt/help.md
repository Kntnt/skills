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

`kntnt` is the Collection's Manager and only namespaced entry point. It lists, Enables, refreshes, and removes Collection Skills across every detected Harness in a Global or Project layer. Other Skills are invoked by their own names.

With no command, `kntnt` prints this page. Each command prints its own page through `/kntnt <command> --help` or `/kntnt help <command>`. The Manager documents only its own commands. Select lists every Catalog Skill, Enabled or not. An Enabled Skill prints its page through `/<skill> --help`; Select can display the page for a Skill that is not yet Enabled.

Select and Update target Global by default. With `--project`, they target the current Project. Harnesses are detected on each run rather than configured or remembered.

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

Assume yes for every yes-or-no question. Valid with `select`, `update`, and `uninstall`.

**--dry-run**

Run the changing command in a temporary home seeded with this Collection's files, report the outcome from that Sandbox, and discard it. Nothing on the machine changes. Valid with `select`, `update`, and `uninstall`.

## DIAGNOSTICS

An unknown command or an option with no work to do is refused rather than ignored. The Manager names the error, prints the addressed command's SYNOPSIS, performs no work, and points to the full page. No command accepts `--force`.

A failed Catalog fetch falls back to the stored Catalog where the command can safely operate from it. The report identifies the Catalog source and any limitation caused by fallback.

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

`uv` on `PATH`. Commands that fetch the Collection or move Skill files also require `npx`; files move through `npx skills`.

**Network**

Select and Update normally fetch the Catalog, and changing commands fetch Skill files. Offline fallback behaviour is documented on each command page.

## SEE ALSO

**/kntnt help --help**, **/kntnt select --help**, **/kntnt update --help**, **/kntnt uninstall --help**, **/<skill> --help**
