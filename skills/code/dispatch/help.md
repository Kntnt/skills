# dispatch

## NAME

dispatch - execute, review, land, and recover fresh compiled plans

## SYNOPSIS

**/dispatch** [**--at-once=**_N_] [**--model=**_NAME_] [**--deliberation=**_LEVEL_] [**--yes**] [**--** *INSTRUCTION*]

**/dispatch** [**--at-once=**_N_] [**--model=**_NAME_] [**--deliberation=**_LEVEL_] *#TICKET* ... [**--** *INSTRUCTION*]

**/dispatch** **--dry-run** [**--at-once=**_N_] [**--model=**_NAME_] [**--deliberation=**_LEVEL_] [**--** *INSTRUCTION*]

**/dispatch** **--dry-run** [**--at-once=**_N_] [**--model=**_NAME_] [**--deliberation=**_LEVEL_] *#TICKET* ... [**--** *INSTRUCTION*]

## DESCRIPTION

`dispatch` consumes fresh accepted compiled-plan bundles, routes executor attempts into disposable linked worktrees, independently reviews their complete results, and lands approved patches serially on the checked-out branch. Every attempt is isolated, including at the default concurrency of one, while every scheduling decision and verdict remains on the unchanged main seat.

A ticket is dispatch-eligible when it is an open executable child in the current repository, has a fresh accepted bundle for the current integration branch and tip, every declared blocker has exactly one matching landing commit reachable from that tip, and no active journal already owns it. Issue closure is not evidence that code landed.

Bare live selection lists every eligible ticket in ascending issue order and asks one confirmation; `--yes` answers it. Explicit references are already confirmed and preserve written order. Any ineligible explicit reference refuses the whole invocation rather than narrowing it.

Scheduling reads the current dependency graph, Git history, journal outcomes, and plan footprints on every turn. Blockers go first, a Solo Ticket runs alone, and otherwise the frontier fills in selection order to the concurrency ceiling. Two plans do not overlap when one writes a path the other reads or writes. The frontier is recomputed after each serial landing, so later waves are never frozen.

The dispatcher verifies every bundle, exact footprint, compiler-owned test blob, STOP condition, full diff, done criterion, seam command, and repository gate. It then returns one of four verdicts: APPROVE lands; REVISE sends one constructive finding to the same execution role for at most two rounds; REBUILD pauses for one fresh `/compile`; PARK records an owner question or human repair handoff.

An approved patch is rebuilt with canonical tests and dispatcher-owned writes on a fresh candidate from the current integration tip. One dispatcher-authored commit advances the invocation branch and carries the landed-change trailers. The child remains open for the future `/land` Skill; dispatch removes executable readiness only after verifying the commit.

The final account has exactly three states. Landed names commit and bundle evidence. Parked names the complete question or handoff and tracker transition. Stranded names the blocker or refusal that prevented execution without inventing an owner choice.

## POSITIONAL ARGUMENTS

*#TICKET* ...

The complete explicit selection of local issue numbers. References preserve their written order. Qualified references, parent decision issues, ranges, bare numbers, and free text are invalid operands.

## OPTIONS

**--dry-run**

Render the current graph, footprint exclusions, first executable frontier, provisional later waves, and Route readiness. It opens no journal, assigns no ticket, persists no Route decision, creates no worktree, and performs no mutation. It cannot be combined with `--yes`.

**--at-once=**_N_

Set the positive integer ceiling for concurrent executor attempts. The default is `1`; isolation still uses a linked worktree and temporary branch.

**--model=**_NAME_

Lock only the model field passed to model-selector's Route Interface. The main seat and every verdict remain unchanged.

**--deliberation=**_LEVEL_

Lock only the portable deliberation field passed to Route. *LEVEL* is `low`, `medium`, `high`, `xhigh`, or `max`; unavailable or unmappable values are refused rather than approximated.

**--yes**

Answer yes at the bare live selection confirmation. It is invalid with explicit references or `--dry-run`, where there is no question to answer.

## OUTPUT

A live run reports each selected ticket as Landed, Parked, or Stranded, with its exact evidence or reason. It names the active or archived journal, any deliberately retained human-conflict resource, any observation artifact, and exact `/compile` plus resume lines where REBUILD awaits its user checkpoint.

A dry run reports only the current graph, exclusions, frontier, provisional later waves, and routing readiness.

## FILES

`<Git common directory>/kntnt-pipeline/plans/<ticket>/`

The clone-local accepted bundle store authored by `/compile`. A consumed bundle is escrowed before execution and retired only after its terminal tracker transition is durable.

`<Git common directory>/kntnt-pipeline/dispatch/active/<branch-digest>/`

The current branch's one active journal. Its exact recorded invocation is the only resume command; a different invocation reports that command and starts nothing.

`<Git common directory>/kntnt-pipeline/dispatch/archive/<run>/`

The compact completed journal and any retained parked patch or sanitized model-selector observation artifact.

`<Git common directory>/kntnt-pipeline/dispatch/worktrees/<run>/<ticket>/<attempt>/`

Disposable attempt worktrees. A human conflict may deliberately retain one named path and branch until the same invocation resumes; completed runs retain none.

## RECOVERY

Re-invoke the exact original command. The journal projection distinguishes attempt without patch, patch without review, lost REVISE context, interrupted landing, REBUILD, human conflict, terminal tracker transition, bundle retirement, and cleanup. Durable artifacts are replayed; missing state is never inferred from a surviving worktree or tracker label.

Routine attempt resources are disposable after patch capture. A parked ticket's latest full patch remains inspectable until that ticket lands or is explicitly abandoned, but it never authorizes replay against a new plan.

## DIAGNOSTICS

An undeclared option, a flag after an operand, invalid ticket or value, `--yes` with explicit references or `--dry-run`, an ineligible explicit reference, a dirty integration tree, a stale or ambiguous plan, a missing or ambiguous landed-change baton, an assigned ticket owned by another actor, a Route refusal, or contradictory journal evidence is refused rather than ignored. The Skill names the reason, prints the SYNOPSIS, performs no unsafe partial mutation, and points to `/dispatch --help`. A flag with no work to do is refused rather than ignored.

A different invocation while this branch owns an active run prints the active run and exact resume line. A plan made stale by a landing prints `/compile #<ticket>` followed by the original resume command. A conflict needing a human names the one retained worktree and branch, immutable-test warning, and one exact decision.

## EXAMPLES

`/dispatch` — show every currently eligible ticket, ask once, then execute the confirmed run sequentially.

`/dispatch --yes` — execute every currently eligible ticket sequentially without asking the bare-selection question.

`/dispatch --at-once=2 #41 #44` — execute the explicit selection with up to two footprint-compatible attempts at once.

`/dispatch --dry-run --at-once=2 #41 #44` — inspect the current graph and provisional waves without mutation.

`/dispatch --model=gpt-5.6-luna --deliberation=medium #41` — lock both executor Route fields without changing the main seat.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator between the Formal Invocation and an optional Contextual Instruction.

The complete contract is stated once in the Collection Library at `library/references/invocation-envelope.md`: separator recognition, the boundaries on Contextual Instruction and Conversation Context, syntax and context refusals, and nested invocation handling.

## DEPENDENCIES

**Binaries**

`git`, `gh`, and `uv` on `PATH`. `gh` must be authenticated with write access to the current GitHub repository.

**Skills**

`model-selector`, whose public `route` form resolves every executor and whose `observe` form may emit judged attempt evidence, and the Manager, so the dependency check and Collection Library are available.

**Capabilities**

The current Harness must be able to spawn subagents. Every executor is isolated from the unchanged main-seat dispatcher, so there is no main-context degraded mode.

## SEE ALSO

**/compile --help**, **/model-selector route --help**, **/model-selector observe --help**, **/kntnt select**
