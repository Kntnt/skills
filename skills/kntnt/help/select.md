# kntnt select

## NAME

kntnt select - list Collection Skills and change which are Enabled

## SYNOPSIS

**/kntnt** **select** [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**] [**--** *INSTRUCTION*]

**/kntnt** **select** [**--on=**_SKILL_]... [**--off=**_SKILL_]... [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**] [**--** *INSTRUCTION*]

## DESCRIPTION

`kntnt select` shows the Catalog by Category, one Skill per row. Each row includes Enabled state, description, required Harness Capability, and incomplete or Deviating files. Global is the default layer.

In list mode, reply with the desired checked set. The Manager resolves required Collection Skills, reports anything left Unsatisfied, asks for confirmation, and applies the answer to every detected Harness. Every Skill can be read in full before answering.

An unchanged answer writes nothing. Confirming repairs incomplete copies; refreshing Deviating files overwrites local changes.

**--on** and **--off** apply only named changes without opening the list.

## OPTIONS

**--on=**_SKILL_

Enable *SKILL* without opening the list. Repeatable; required Collection Skills are confirmed together.

**--off=**_SKILL_

Disable *SKILL* without opening the list. Repeatable, combinable with **--on**, and requires **--yes** because files are deleted.

**--project**, **--project=on**

Target the current Project instead of Global. `--project=off` has the same effect as omitting the option.

**--yes**

Answer yes to confirmations. Without **--on** or **--off**, it opens no list, Enables nothing new, and repairs Deviating or incomplete Enabled Skills.

**--dry-run**

Run in a discarded temporary home and report the result without changing the selected layer. The isolated cache makes this slower.

## SKILL STATES

**Enabled**

The Skill is present in the targeted layer. Project view identifies Global-only Skills separately.

**Incomplete**

The Skill is present in only some detected Harnesses. Confirming repairs it.

**Deviating**

The files differ from the Catalog Digest. Re-copying overwrites the layer's current files.

**Locked**

The Skill depends on an unchecked Collection Skill. The row names it; leaving it unchecked is allowed but reported as Unsatisfied.

## OFFLINE OPERATION

Offline, Select uses the stored Catalog. It cannot fetch help for absent Skills or identify current versus Deviating files, so it offers no refresh.

## DIAGNOSTICS

An unknown Skill, invalid combination, or flag with no work to do is refused rather than ignored. The Manager prints the SYNOPSIS, changes nothing, and points to this page.

The end of the list counts Withdrawn Skills found on disk. Update removes them.

## EXAMPLES

**/kntnt select --on=release --yes**

Enable `release` and its required Collection Skills without opening the list.

**/kntnt select --yes**

Open no list and Enable nothing new; refresh Deviating Enabled Skills and repair incomplete copies.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` and `npx` on `PATH`. Skill files move through `npx skills`.

**Network**

Required to fetch the current Catalog, fetch pages for Skills absent from disk, and change Skill files. Read-only fallback uses the stored Catalog as described above.

## SEE ALSO

**/kntnt update --help**, **/kntnt uninstall --help**, **/<skill> --help**
