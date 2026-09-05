# kntnt select

## NAME

kntnt select - list Collection Skills and Features and change which are Enabled

## SYNOPSIS

**/kntnt** **select** [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**] [**--** *INSTRUCTION*]

**/kntnt** **select** [**--on=**_ENTRY_]... [**--off=**_ENTRY_]... [**--project**[=**on**|**off**]] [**--yes**] [**--dry-run**] [**--** *INSTRUCTION*]

## DESCRIPTION

`kntnt select` shows the Catalog in two groups: its Skills by Category, one Skill per row, and under them its Features. Each Skill row includes Enabled state, description, required Harness Capability, and incomplete or Deviating files. Each Feature row includes Enabled state, description, the Harnesses it serves, and what it writes and where. Global is the default layer.

A Feature is a Catalog entry that owns Harness Integrations and nothing else: no Harness loads it, no Skill depends on it, and enabling it writes only into Harness configuration and files the user maintains. Features are Global only — the Project layer installs and removes no integration — and `--project` reports that instead of offering them.

In list mode, reply with the desired checked set; both groups are answered together, and a Feature never shares a name with a Skill. The Manager resolves required Collection Skills, reports anything left Unsatisfied, asks for confirmation, and applies the answer to every detected Harness. Every Skill can be read in full before answering.

An unchanged answer writes nothing. Confirming repairs incomplete copies; refreshing Deviating files overwrites local changes.

**--on** and **--off** apply only named changes without opening the list.

## OPTIONS

**--on=**_ENTRY_

Enable *ENTRY* — a Skill or a Feature — without opening the list. Repeatable; required Collection Skills are confirmed together.

**--off=**_ENTRY_

Disable *ENTRY* without opening the list. Repeatable, combinable with **--on**, and requires **--yes**: unchecking a Skill deletes files, and unchecking a Feature takes what it wrote back out of Harness configuration.

**--project**, **--project=on**

Target the current Project instead of Global. `--project=off` has the same effect as omitting the option.

**--yes**

Answer yes to confirmations, including the one a Feature raises when a single-valued setting it wants is already held by another command. Without **--on** or **--off**, it opens no list, Enables nothing new, and repairs Deviating or incomplete Enabled Skills — so it never replaces a held setting on its own, only alongside the name that asked for it.

**--dry-run**

Run in a discarded temporary home and report the result without changing the selected layer. The isolated cache makes this slower.

## ENTRY STATES

**Enabled**

The Skill is present in the targeted layer. Project view identifies Global-only Skills separately.

**Incomplete**

The Skill is present, or the Feature installed, in only some detected Harnesses. Confirming repairs it.

**Deviating**

The files differ from the Catalog Digest. Re-copying overwrites the layer's current files.

**Locked**

The Skill depends on an unchecked Collection Skill. The row names it; leaving it unchecked is allowed but reported as Unsatisfied. A Feature is locked where no detected Harness is one it serves; the row says so rather than hiding it.

## FILES

**Harness Integrations**

A Skill may own a Harness Integration, and a Feature owns nothing else: what it writes into a Harness's own configuration so the Harness calls it at its own lifecycle moments. It is written outside the Skill's own directory, so deleting the Skill's files does not reach it. A Feature owns Harness Integrations and nothing else, so this is the whole of what enabling or disabling one does. Checking an entry in Global asks it to install what it owns, and unchecking one asks it to remove them; the Project layer installs and removes none. The report says what became of each.

A Feature may also write into a global instruction file a Harness reads — `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.config/opencode/AGENTS.md` — and into a single-valued setting such as Claude Code's status line. Prose is written inside a fenced ownership marker and removal takes exactly that fence away. A single-valued setting another command already holds is never overwritten unquestioned: the row names what holds it and the confirmation asks whether to replace it, which **--yes** answers along with everything else it asks. Nothing is kept of what is replaced. What each Feature writes is on its row before the checkbox, and repeated in the confirmation before anything is written.

## OFFLINE OPERATION

Offline, Select uses the stored Catalog. It cannot fetch help for absent Skills or identify current versus Deviating files, so it offers no refresh.

## DIAGNOSTICS

An unknown Skill or Feature, invalid combination, or flag with no work to do is refused rather than ignored. The Manager prints the SYNOPSIS, changes nothing, and points to this page.

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
