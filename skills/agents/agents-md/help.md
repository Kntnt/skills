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

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Unaddressable is guidance with no addressable effect at all — guidance touching nothing this Skill's contract addresses — and never guidance a documented precedence has already settled against, which is suppressed instead: suppression is that precedence working, so the run continues and the delivery names the suppressed guidance beside the resolved configuration where saying so is useful. Only guidance that is part invalid — part conflicting, part scope-widening, or part unaddressable — goes unapplied as a whole; one parameter suppressed and another landing is an ordinary invocation. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

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

`git` and `uv` on `PATH`.

**Skills**

The Manager must be Enabled so the dependency check can run.

## SEE ALSO

**/kntnt select**
