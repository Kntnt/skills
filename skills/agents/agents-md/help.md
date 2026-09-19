# agents-md

## NAME

agents-md - tend a project's always-loaded agent instructions

## SYNOPSIS

**/agents-md** [**--force**] [**--yes**] [*PATH*] [**--** *INSTRUCTION*]

## DESCRIPTION

`agents-md` reviews the current Project's `AGENTS.md`, `CLAUDE.md`, `docs/agents/`, documentation, and tracked Project Skills after a task. It writes only facts that are true, needed by a later session, not discoverable from the Project, and not already recorded elsewhere. With no *PATH*, it tends the repository root.

`AGENTS.md` remains a compact table of contents and set of ground rules. Concern-specific material belongs under `docs/agents/` and is reached through a pointer that states when to read it. If no fact justifies always-loaded text or a referenced file, nothing is written.

A Project that still keeps these files in a legacy `agents.d/` has them moved to the same paths under `docs/agents/`, with every pointer and link to them rewritten and their other content unchanged. A file already present under `docs/agents/` is kept; an identical copy in the legacy directory is removed. Where the two directories hold different files at the same path, the Skill moves nothing, changes neither directory nor any pointer to them, and reports both paths so a person can choose.

The Skill may create or update `AGENTS.md`, files under `docs/agents/`, and the `CLAUDE.md` bridge: a symbolic link to `AGENTS.md`, so Claude Code reads the same file without importing it, and a session started in a subdirectory is not asked to approve an external import. It never changes instructions outside the current repository and never writes proposed documentation prose under `docs/` outside `docs/agents/`; it may report a proposed location and purpose for a human to write.

## POSITIONAL ARGUMENTS

*PATH*

A directory inside the current repository. The repository root is the default. A path outside the repository is invalid.

## OPTIONS

**--force**

Create the minimum structure even when no fact qualifies: the `CLAUDE.md` bridge, an `AGENTS.md` title and ground-rules section, and an empty `docs/agents/` directory.

**--yes**

Assume yes for every proposed change instead of waiting for confirmation. Documentation prose under `docs/` outside `docs/agents/` remains a proposal, and a collision between a legacy `agents.d/` file and a different `docs/agents/` file is still only reported.

## OUTPUT

The report names every retained, moved, replaced, or rejected fact and the source that settles it. It also reports the character count of the always-loaded files and the total including `docs/agents/`, before and after.

## DIAGNOSTICS

An invalid path, unknown option, or option combination is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, changes nothing, and points to `/agents-md --help`. An operand written before an option is out of order and is refused the same way.

A Project with no qualifying fact is a successful no-op and is reported as such.

A legacy `agents.d/` file whose `docs/agents/` counterpart holds different content is a collision: the Skill names both paths, says that they differ, and leaves both directories and their pointers as they were.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`git` and `uv` on `PATH`.

**Skills**

The Manager must be Enabled so the dependency check can run.

## SEE ALSO

**/kntnt select**
