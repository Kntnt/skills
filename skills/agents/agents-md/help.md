# agents-md

## NAME

agents-md - tend a project's always-loaded agent instructions

## SYNOPSIS

**/agents-md** [**--force**] [**--yes**] [*PATH*] [**--** *INSTRUCTION*]

## DESCRIPTION

`agents-md` reviews the current Project's `AGENTS.md`, `CLAUDE.md`, `agents.d/`, documentation, and tracked Project Skills after a task. It writes only facts that are true, needed by a later session, not discoverable from the Project, and not already recorded elsewhere. With no *PATH*, it tends the repository root.

`AGENTS.md` remains a compact table of contents and set of ground rules. Concern-specific material belongs under `agents.d/` and is reached through a pointer that states when to read it. If no fact justifies always-loaded text or a referenced file, nothing is written.

The Skill may create or update the one-line `CLAUDE.md` bridge, `AGENTS.md`, and files under `agents.d/`. It never changes instructions outside the current repository and never writes proposed documentation prose under `docs/`; it may report a proposed location and purpose for a human to write.

## POSITIONAL ARGUMENTS

*PATH*

A directory inside the current repository. The repository root is the default. A path outside the repository is invalid.

## OPTIONS

**--force**

Create the minimum structure even when no fact qualifies: the `CLAUDE.md` bridge, an `AGENTS.md` title and ground-rules section, and an empty `agents.d/` directory.

**--yes**

Assume yes for every proposed change instead of waiting for confirmation. Documentation prose under `docs/` remains a proposal.

## OUTPUT

The report names every retained, moved, replaced, or rejected fact and the source that settles it. It also reports the character count of the always-loaded files and the total including `agents.d/`, before and after.

## DIAGNOSTICS

An invalid path, unknown option, or option combination is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, changes nothing, and points to `/agents-md --help`. An operand written before an option is out of order and is refused the same way.

A Project with no qualifying fact is a successful no-op and is reported as such.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`git` and `uv` on `PATH`.

**Skills**

The Manager must be Enabled so the dependency check can run.

## SEE ALSO

**/kntnt select**
