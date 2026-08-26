# frame

## NAME

frame - map a task before anything is built and write a Frame Record

## SYNOPSIS

**/frame** [*TASK*] [**--** *INSTRUCTION*]

**/frame** **--resume=**_PATH_ [**--** *INSTRUCTION*]

## DESCRIPTION

`frame` maps a task before any of it is built. It sorts every open point the task carries into one of three bins and only one of them becomes a question. What the codebase can answer is fetched by a read-only recon subagent. What the repository's own established rules already settle is decided by the Skill and written into a decision ledger. What is left — product behaviour, user experience, priority, architecture direction, and any trade-off carrying a cost, a risk, or a reversibility consequence — is put to the owner. A point that could fall either side of the last boundary goes to the owner when the decision is hard to reverse or would surprise them later.

Recon and interview run at the same time. Questions arrive in numbered rounds, each question phrased as the consequence being chosen between rather than the mechanism that delivers it, each carrying a recommended answer and what that answer costs, in the vocabulary the repository itself uses. Beside the questions, each round shows the decisions taken since the previous one — one line each, the choice and the constraint it was decided under. Rejecting one turns it back into a question in the next round, which is what keeps the ledger cheap to correct.

Before the first question the Skill establishes what binds: the repository's always-loaded agent file, the rule documents that file points at for the work in hand, the glossary it keeps, and how the repository verifies itself. Those constraints are what makes a decision in the owner's stead possible without asking.

The result is one Frame Record, written incrementally as the run proceeds, so an interrupted session loses at most the last round. Every framing is attended: a task with nothing to ask produces a complete record without a single round, and a question that reaches the owner is answered by the owner.

The Skill writes no code, builds nothing to find out, publishes nothing to any tracker, and does not slice, size, or sequence the work. A question only an experiment could answer is recorded as open, together with what would answer it.

Knowledge is written to the repository as it crystallises: a term that gets pinned down goes into the repository's glossary, and a decision that is hard to reverse, surprising without its context, and the result of a real trade-off earns a record in its decision archive — under that repository's own convention where it declares one, and under `CONTEXT.md` plus `docs/adr/` where it does not. Everything so written is listed in the record's final section, which is the only manifest it can later be withdrawn against.

## POSITIONAL ARGUMENTS

*TASK*

The task, in whatever words the owner has for it. Free text: everything from the first operand onwards is read as part of the task, so a word inside it that looks like an option is not one. Omitted, the task is the one the conversation has already reached, which is the ordinary way this Skill starts; where the conversation holds no task either, the Skill asks for one before doing anything else.

## OPTIONS

**--resume=**_PATH_

Continue the unfinished Frame Record at *PATH*. It is the direct address of a record rather than the only route to one: every run reports the records left in `.kntnt/frames/` and offers each of them for resuming or discarding. It may not be combined with *TASK*, a record already carrying the task it was opened with.

## OUTPUT

The record on disk, and a closing report naming what was mapped, what the owner decided, what the Skill decided in their stead, what is deliberately still open, and where the record is.

## FILES

`.kntnt/frames/<slug>.md`

The Frame Record, one file per framing, in the repository being framed. It is untracked and is a working artifact rather than a durable account of decisions; the format and lifecycle are stated in `library/references/frame-record.md` in the Collection Library. `/to-slices` consumes a complete record only after its approved issue set has been published and verified.

`.git/info/exclude`

Where the line ignoring `.kntnt/` is written, once per repository and only where that directory is not already ignored by some means. The ignore is local, matching a local artifact, and no tracked file is modified for it. A run that writes the line says so; a run that finds the directory already ignored says nothing about it.

## DIAGNOSTICS

The Skill accepts one option and one free-text operand. An undeclared option, an operand written before an option, and a *TASK* given alongside a resumed record are each refused rather than ignored; the Skill names the error, prints the SYNOPSIS, frames nothing, and points to `/frame --help`. A flag with no work to do is refused rather than ignored.

A path that resolves to no readable Frame Record is reported as such, and nothing is framed.

## EXAMPLES

`/frame` — frame the task the conversation has already reached.

`/frame Let people export a report as PDF` — frame that task, stated in the owner's words.

`/frame --resume=.kntnt/frames/pdf-export.md` — continue the framing that session was interrupted in.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`, for the dependency check.

**Skills**

`model-selector`, whose public `route` form resolves each recon wave into launch decisions, and the Manager, so the dependency check can run.

**Capabilities**

The current Harness must be able to spawn subagents. Recon in the main context is recon competing with the interview for the context the interview exists to protect, so this is not a degraded mode: the Skill stops when the Capability is Unsatisfied.

## SEE ALSO

**/to-slices --help**, **/model-selector route --help**, **/kntnt select**
