# compile

## NAME

compile - turn ready executable children into independently accepted executor plans

## SYNOPSIS

**/compile** [**--yes**] [**--** *INSTRUCTION*]

**/compile** *#TICKET* ... [**--** *INSTRUCTION*]

## DESCRIPTION

`compile` turns executable child tickets into fresh, self-contained executor-plan bundles against one captured current `HEAD`. It reads each child's complete body and thread, its parent decision, and its blocking relations; resolves durable hints into current committed files and excerpts; fixes an exact footprint and any serial allocations; writes finished seam tests; and accepts the result only after a fresh-context cold reader returns PASS.

Explicit ticket references are compiled in written order and start without another confirmation. Bare invocation selects every open child carrying the repository's configured executable-ready state and lacking a fresh accepted bundle, orders them by issue number, displays the complete selection, and asks one yes-or-no question. `--yes` answers that bare checkpoint without asking. The Skill records blockers but does not make a child ineligible for compilation; execution eligibility belongs to `/dispatch`.

Compilation reads committed content from a temporary detached worktree and runs the untouched repository gate once before compiling the batch. Unrelated local edits are not absorbed. A branch move restarts the batch, a tracker-source move recompiles the affected child, and a red untouched baseline stops without parking tickets.

A child whose durable source leaves an owner-owned requirement unresolved is parked independently: one complete question is posted, its executable-ready state is replaced with `needs-info`, and its scope labels and milestone remain. Successful compilation does not change tracker state.

Accepted bundles are clone-local under the Git common directory. Each accepted pointer selects one complete immutable fingerprinted bundle containing the human plan, machine manifest, and compiler-owned test overlay. No bundle content is posted to the tracker.

## POSITIONAL ARGUMENTS

*#TICKET* ...

One or more local `#`-prefixed issue numbers. They are the complete selection and preserve written order. Each must name an open executable child; a decision parent, qualified reference, range, bare number, or free-text operand is refused.

## OPTIONS

**--yes**

Answer yes without asking at the bare selection checkpoint. It is refused beside explicit ticket references because naming those tickets already confirms the selection and leaves the flag no work.

## OUTPUT

A concise batch report partitions every selected child as accepted, parked, already fresh, or failed. It gives the captured `HEAD`, accepted bundle paths, complete parking questions, failures, and any local edits overlapping a compiled footprint.

## FILES

`<git-common-dir>/kntnt-pipeline/plans/<ticket>/accepted`

The atomically replaced pointer to the accepted immutable bundle for one ticket.

`<git-common-dir>/kntnt-pipeline/plans/<ticket>/bundles/<fingerprint>/`

The immutable bundle selected by `accepted`, containing `plan.md`, `manifest.json`, and the compiler-owned `tests/` overlay. The Git common directory makes the bundle visible to linked worktrees without placing it in the repository tree.

## DIAGNOSTICS

An undeclared option, an option after an operand, an invalid ticket reference, or `--yes` beside explicit references is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, compiles nothing, changes no tracker state, writes no bundle, and points to `/compile --help`. A flag with no work to do is refused rather than ignored.

A red untouched repository gate stops the whole batch without parking children. A nonconforming or owner-incomplete child alone receives `needs-info` and does not stop eligible siblings. A failed red test, cold read, manifest check, fingerprint check, or source gate accepts no candidate for that child and is named in the report.

## EXAMPLES

`/compile #182 #185` — compile two executable children in that order without another confirmation.

`/compile` — display every eligible child and ask whether to compile the complete selection.

`/compile --yes` — compile that bare selection without asking its yes-or-no checkpoint.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator between the Formal Invocation and an optional Contextual Instruction.

The complete contract is stated once in the Collection Library at `library/references/invocation-envelope.md`: separator recognition, the boundaries on Contextual Instruction and Conversation Context, syntax and context refusals, and nested invocation handling.

## DEPENDENCIES

**Binaries**

`git`, `gh`, and `uv` on `PATH`. `gh` must be authenticated with read access and, when a child must be parked or an owner answer persisted, write access to the current GitHub repository.

**Skills**

The Manager must be Enabled so the dependency check and Collection Library are available.

**Capabilities**

The current Harness must be able to spawn subagents. Every accepted bundle requires a fresh-context cold reader on the exact inherited main seat, so compilation stops when that Capability is Unsatisfied.

## SEE ALSO

**/to-slices --help**, **/kntnt select**
