# kntnt select

## NAME

kntnt select - list Collection Skills and change which are Enabled

## SYNOPSIS

**/kntnt** **select** [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**] [**--** *INSTRUCTION*]

**/kntnt** **select** [**--on=**_SKILL_]... [**--off=**_SKILL_]... [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**] [**--** *INSTRUCTION*]

## DESCRIPTION

`kntnt select` displays the Catalog grouped by Category, with one row per Skill. Each row shows whether the Skill is Enabled in the targeted layer, its one-line description, any required Harness Capability, and incomplete or Deviating disk state. Global is the default layer.

In list mode, reply in plain text with the desired checked set. The Manager resolves required Collection Skills, reports anything the answer would leave Unsatisfied, asks for confirmation, and then applies the complete answer to every Harness detected in the layer. Every row can be read in full before the list is answered; requesting its help displays that Skill's own page without closing or answering the list.

An answer that changes nothing writes nothing. A Skill whose files are present in only some target Harnesses is shown checked and incomplete; confirming repairs it. A Skill whose files differ from the Collection is shown Deviating, and re-copying it overwrites local changes.

The explicit `--on` and `--off` form applies only the named deltas and opens no list. Existing unmentioned Skills retain their state and files.

## OPTIONS

**--on=**_SKILL_

Enable *SKILL* in the targeted layer without opening the list. Repeatable. Required Collection Skills are added after one confirmation for the complete dependency closure.

**--off=**_SKILL_

Disable *SKILL* in the targeted layer without opening the list. Repeatable and combinable with `--on`. Because it deletes files, the script requires `--yes`.

**--project**, **--project=on**

Target the current Project instead of Global. `--project=off` has the same effect as omitting the option.

**--yes**

Assume yes for confirmations. With neither `--on` nor `--off`, it opens no list, Enables no new Skill, refreshes Enabled Skills that Deviate, and repairs incomplete copies.

**--dry-run**

Execute against a temporary home seeded with this Collection's files, report the Sandbox outcome, and discard it. Nothing in the selected layer changes. The isolated transport cache makes this slower than an ordinary run.

## SKILL STATES

**Enabled**

The Skill is present in the targeted layer. In the Project view, a Skill Enabled only in Global is identified separately because the Project has no copy to disable.

**Incomplete**

The Skill is present in only some detected Harnesses. This is a disk condition, not a third selectable state.

**Deviating**

The Skill's files differ from the Digest in the fetched Catalog. The comparison establishes difference, not which state is newer. Re-copying overwrites the layer's current files.

**Locked**

The Skill depends on an unchecked Collection Skill. The row names what must also be checked. Unchecking a Skill still needed by another checked Skill is allowed but reported as leaving the dependent Unsatisfied.

## OFFLINE OPERATION

If the Collection cannot be reached, Select uses the stored Catalog and identifies it as the source. A page for a Skill absent from disk cannot be fetched. No Skill is marked current or Deviating, and no refresh is offered, because stored Digests describe the Collection as of the last Update.

## DIAGNOSTICS

An unknown Skill, invalid combination, or option with no work to do is refused rather than ignored. The Manager names the error, prints the SYNOPSIS, changes nothing, and points to the full page.

The end of the list counts Withdrawn Skills found on disk. Update removes them.

## EXAMPLES

**/kntnt select --on=release --yes**

Enable `release` and its required Collection Skills without opening the list.

**/kntnt select --yes**

Open no list and Enable nothing new; refresh Deviating Enabled Skills and repair incomplete copies.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` and `npx` on `PATH`. Skill files move through `npx skills`.

**Network**

Required to fetch the current Catalog, fetch pages for Skills absent from disk, and change Skill files. Read-only fallback uses the stored Catalog as described above.

## SEE ALSO

**/kntnt update --help**, **/kntnt uninstall --help**, **/<skill> --help**
