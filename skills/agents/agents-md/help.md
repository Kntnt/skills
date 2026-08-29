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

`git` and `uv` on `PATH`.

**Skills**

The Manager must be Enabled so the dependency check can run.

## SEE ALSO

**/kntnt select**
