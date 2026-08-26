# Phase 2, step 1 — `/compile`, as designed

> Draft written 2026-08-26 against commit `7dd014a`, from the `/compile` section of `00-brief.md`, the handoff inherited from `05-to-slices.md`, the executable-child contract in the Collection Library, and the compile-time duties rescued from `/orchestrate`. The owner-level round (step 2) settled both residuals on 2026-08-26; it is now the input to approval of the ticket breakdown. Deleted with the rest of `docs/rework/` by the final cleanup ticket.

The dossier states what `/compile` is for; this file is the design that satisfies it, the boundaries judged along the way, and what the owner settled. Everything here is settled — resolved from `docs/rules/`, from `$LIBRARY/references/slices.md`, from the current pipeline Skills, from the compile-time half of the workflow `/dispatch` will replace, or answered by Thomas in the round recorded below. Nothing in it is still a question.

## What the Skill is

`/compile` turns each ready executable child into one self-contained executor plan against the repository's current `HEAD`. It reads the ticket's complete thread and the relevant decisions and constraints from its parent, resolves every durable hint into current files and fresh excerpts, fixes the verification commands and machine-checkable done criteria, writes the finished seam tests, allocates every serial resource the work will need, and states the exact footprint later scheduling may trust.

The plan has one purpose and one consumer: `/dispatch` gives it to an executor whose working tree starts at the commit it names. It is neither another durable decision layer nor a speculative plan somebody maintains while the tree moves. A changed source or a changed `HEAD` makes it ineligible rather than something to reconcile.

## Selection and invocation

The full grammar is `/compile [--yes] [#<ticket> ...]`, following the selection grammar the dossier fixes for `/compile`, `/dispatch`, and `/land`.

Explicit references select those executable children in the order written. They are `#`-prefixed issue numbers in the current repository; a parent decision issue, a qualified cross-repository reference, a range, and free text are not ticket operands. An explicit selection starts without a confirmation because naming the work is the confirmation.

Bare invocation selects every open executable child carrying the repository's configured ready state and lacking a fresh accepted plan. It renders the complete selection and asks one yes-or-no question before compilation starts. `--yes` answers that question yes and is therefore valid only on the bare form; beside explicit references it has no work to do and is refused rather than ignored. Bare ordering is ascending issue number, giving serial allocation and reporting one deterministic order without pretending to schedule execution.

Eligibility does not depend on blockers having landed. The dossier assigns that gate to `/dispatch`, and compiling a blocked child can still be useful where a batch needs one shared allocation pass. A blocker landing moves `HEAD`, which expires the plan naturally; no stale plan becomes executable merely because its graph edge closed.

The repository's configured ready state comes from its always-loaded agent file and selected issue-tracker convention. In this rework worktree that means `rework` plus `rework-ready-for-agent`, never plain `ready-for-agent`. The selection rule belongs in a new `docs/rules/pipeline.md`, with the corresponding pointer in `AGENTS.md`, because three Skills must keep one grammar and one meaning; each installed Skill still states its own accepted forms in its shipped body and manpage.

## The durable input

Read `$LIBRARY/references/slices.md`, then read each selected child through that contract: the whole issue body, every comment oldest first, its parent relation, the parent decision issue, and native blocking relations or their documented fallbacks. A later comment outranks an earlier contradictory statement. The requirement is the whole thread, so a compilation that reads only the body is incomplete even where the body looks sufficient.

The child supplies the end-to-end behaviour, observable acceptance criteria, seam contract, compilation hints, and publication vantage. The parent supplies the outcome and scope shared by the set, the owner and ledger decisions, and every binding constraint relevant to this child. `/compile` inlines what the executor needs from both; it never sends the executor to the tracker or to a peer Skill's internals to recover omitted meaning.

The ticket's publication vantage is evidence for recon rather than the executor's base. Compare it with current `HEAD` to see what moved in the hinted areas, then compile from the current tree. The durable layer was written to survive that move; treating every changed path as a reason to send the ticket back would recreate the drift apparatus the pipeline exists to delete.

A selected issue that does not satisfy the executable-child contract is not silently upgraded into one. Name what prevents an honest plan, post one question or correction request containing every missing owner-owned point, replace its ready state with `needs-info`, preserve its scope labels and milestone, and continue with the rest of the batch. A technical choice inside the repository's existing frames is the compiler's to make and record, never a question used to park the ticket.

Applicable Contextual Instruction may resolve a choice the ticket left open only when it comes from the owner and stays inside the parent decision. Before compiling, write that answer to the ticket thread so the requirement remains whole on a later recompile; an instruction that contradicts or widens the durable decision is refused under the Invocation Envelope rather than turned into a comment.

## The executor's vantage

Capture the full `HEAD` commit and current integration branch before recon. Read committed content from a temporary detached working tree at that commit, so unrelated local changes in the owner's working tree neither enter the plan nor have to be stashed. Name any local changes touching the eventual footprint in the report because `/dispatch` cannot honestly start from them, but do not read them as implementation state.

Resolve the repository's complete verification gate once for the batch from its always-loaded instructions and contributing guide, and run it on the untouched detached tree. A failing baseline stops the batch before plans or tracker mutations: an executor cannot be held to making an already-red command green without absorbing work no ticket names. The report names the command and failure; `/compile` neither repairs the branch nor parks tickets for a repository-level fault.

Immediately before accepting any plan, verify that the integration branch still points at the captured commit and read the child and parent back. The accepted source fingerprint covers both bodies, every comment, the parent relation, and the decisions and constraints the plan inlined. A changed `HEAD` restarts the batch against the new tip so allocations and footprints share one world; a changed tracker source recompiles the affected child from the newly complete thread. This final comparison is what makes the captured commit the executor's vantage rather than a commit the compiler happened to start from.

## The compiled plan

The plan is one bundle with a small Interface shared by its producer and consumer. The exact format belongs in `$LIBRARY/references/compiled-plan.md`, because `/compile` writes it and `/dispatch` reads and retires it; neither peer owns the other's input.

The human-readable `plan.md` has two registers.

**The binding contract** carries:

1. **Identity and provenance** — repository identity, integration branch, full `HEAD`, ticket and parent references, the source fingerprint, and the bundle fingerprint.
2. **Goal** — the child's delivered behaviour in the parent's outcome and decisions, with no implementation preference smuggled in as intent.
3. **Scope and footprint** — exact paths read, modified, created, and deleted; compiler-owned seam-test paths; dispatcher-owned shared writes where the repository declares any; and serial resources touched.
4. **Invariants** — the relevant repository rules and parent constraints, inlined closely enough that the executor needs no rules archaeology.
5. **Current implementation context** — exact files, symbols, line-qualified excerpts, and present behaviour as they stand at the captured commit.
6. **Seam tests** — every attached test file, its destination path, base and compiled blob identity, command, and expected red result against the captured commit.
7. **Verification** — focused commands for the seam and the complete repository gate, with working directory, environment assumptions, and expected success stated.
8. **Done criteria** — one machine-checkable criterion for every acceptance criterion, plus footprint and immutable-test checks; no judgement delegated under a checkbox that only repeats the ticket.
9. **STOP conditions** — every condition under which proceeding would require invention: a changed vantage or source, a missing dependency, an unallocated serial resource, a needed path outside the footprint, a seam test that must change, an owner decision, or a baseline the plan did not describe.

**The advisory appendix** carries the implementation route the compiler recommends: ordered steps, exemplars, likely edit points, and useful focused commands. An executor may replace that route completely while staying inside the binding contract. This is the depth the plan Interface is for: a weak executor receives enough implementation help to proceed, while a strong one is not forced to imitate the compiler's mechanics.

The bundle also carries a machine-readable `manifest.json` and a `tests/` tree containing the finished compiler-owned files at their repository-relative destinations. The manifest repeats only what `/dispatch` must check mechanically — provenance and fingerprints, footprint classes, serial allocations, test overlay metadata, commands, and done-criterion identifiers — while the Markdown remains the complete executor brief. The bundle fingerprint covers `plan.md`, the complete test tree, and the canonical manifest with its own fingerprint field omitted. A contradiction between the two registers rejects the bundle; the machine-readable subset never becomes a second statement of product intent.

## Footprints and serial resources

A footprint is exact because `/dispatch` will use it both to avoid collisions and to reject scope drift. `reads` names every committed path whose content the contract or advisory route depends on; `modifies`, `creates`, and `deletes` name every path the executor may change; compiler-owned test paths are a distinct write class the executor may not touch; dispatcher-owned paths name generated or shared append work the later coordinator, not the executor, applies. A glob, directory standing in for unknown descendants, or “files such as” is not a footprint and cannot be accepted.

The compiler may discover that a ticket whose durable scope was honest cannot be expressed with an exact footprint against this `HEAD`. That is not permission to guess wide. Where fresh recon finds an owner-owned scope choice, park the ticket with the question; where the repository's frames select one correct path, take it and state why in the plan.

Serial allocation happens once per batch, after recon has established which registries each plan touches and how many identifiers it needs. For each numbered registry, read the highest committed identifier once, combine it with allocations held by other fresh plans at this same `HEAD`, and assign consecutive identifiers in the batch's deterministic order from one shared counter. A gap remains legitimate and is never reused. Every plan receives its exact identifiers; needing one more is a STOP condition rather than a second read of the directory from inside parallel execution.

The allocation table lives with the fresh plan set and is valid only at its captured `HEAD`. A changed tip expires the table with the plans. This is pre-allocation rather than a durable claim on the repository: unused identifiers may become gaps, and the landing commit records the identifiers actually taken.

## Seam tests, authored before execution

The compiler writes finished, runnable tests at the seam the child contract selected. It materialises the test overlay over the captured detached tree and observes the focused command fail for the missing behaviour, with the failure at the intended assertion rather than at syntax, import, fixture, or environment setup. The untouched repository gate must have passed before the overlay was applied. A test already green either proves the ticket is already satisfied or fails to distinguish its work; the compiler resolves which before accepting a plan.

The canonical test files stay in the plan bundle. `/dispatch` materialises them into the executor's isolated working tree, makes them non-writable as a guardrail, and gives the executor their commands but not permission to edit their paths. The bundle fingerprints remain outside the executor's working tree; review re-hashes every materialised file and rejects a changed, replaced, or deleted test even if its command is green. Read-only is therefore enforced at the review seam, not claimed as an operating-system security barrier against a process running as the same user.

The accepted test files become permanent repository tests. `/dispatch` materialises their exact accepted bytes beside the implementation, verifies them against the bundle after execution, and lands them itself; the executor implements against tests it cannot redefine and never owns their paths. The authorship separation therefore survives integration rather than ending at the verdict.

## The cold read

Every completed bundle goes to a fresh-context subagent before acceptance. This is verdict work, so it inherits the complete main seat exactly and is never routed through model-selector. The subagent receives only the bundle and a clean detached tree at the captured commit — no compiler notes, no tracker access, and no account of what the compiler meant — because the test is whether the plan stands alone.

The cold reader must be able to state the goal and scope from the plan, locate every excerpt, reproduce the expected red seam test, see one machine check per acceptance criterion, verify the footprint and allocations against the tree, and identify every point at which an executor would still have to invent a requirement. It returns PASS or FAIL with concrete findings. A mechanical omission is corrected and handed to a new cold reader; an owner-owned gap parks only that ticket under `needs-info`. A builder's confidence and the compiler rereading its own prose are neither acceptance.

The fresh-context read makes `subagents` a hard Capability. It adds no model-selector Skill Dependency: no execution is delegated here, and collection law keeps verdict authority on the exact main seat.

## Acceptance, storage, and recovery

A bundle is accepted only after its seam test has the recorded baseline result, its cold read passes, its manifest agrees with its files, and the final `HEAD` and tracker fingerprints still match. Plans that fail independently do not roll back accepted siblings, and a ticket parked for information does not stop the rest of the batch.

Accepted bundles live under the repository's Git common directory at `.git/kntnt-pipeline/plans/<ticket>/`, resolved through `git rev-parse --git-common-dir` rather than by assuming `.git` is a directory. That address is shared by linked worktrees, invisible to `git status`, durable across an interrupted session, and local to the clone whose exact objects and branch it names. A temporary sibling directory is renamed into place only after acceptance, so interruption leaves either the previous accepted bundle or no accepted bundle rather than half of one.

A plan is fresh only while repository identity, integration branch, `HEAD`, source fingerprint, and bundle fingerprint all match. A fresh plan makes the ticket ineligible for another bare compile; an explicit reference reports it already compiled and writes nothing. A stale bundle is never repaired in place: the next compilation replaces it atomically from current inputs. `/dispatch` consumes a fresh bundle, archives only the run journal it needs for its own recovery, and removes the bundle when the ticket lands or is parked.

No plan or excerpt is posted to the tracker. The tracker holds durable intent and questions that change it; a just-in-time artifact whose first rule is “expire when the source moves” would be noise and a tempting stale source if published beside them.

## The handoff, and the order things land in

The `/compile` implementation ticket completes `/to-slices`' deferred handoff. After verified publication, `/to-slices`' closing report gains one exact next line listing every executable child in approved snapshot order: `/compile #<child> #<child> ...`. Its manpage adds **/compile --help** to `SEE ALSO`. Both changes land with the successor that makes them truthful.

`/dispatch` does not exist on the day `/compile` lands. The first version therefore closes in `$LIBRARY/references/tldr-mode.md` with the plans accepted, tickets parked and their exact questions, plans already fresh and skipped, the captured `HEAD`, and the plan-bundle paths. It names that `/dispatch` will consume them later but invents no invocation for a missing Skill. The `/dispatch` implementation ticket will add `/compile`'s prefilled next line and `SEE ALSO` entry under the same handoff rule.

The `/dispatch` brief inherits five requirements together, so the test-placement mechanism cannot be separated from the lifecycle that makes it trustworthy. It consumes only a fresh accepted plan bundle and retires that bundle when the ticket lands or is parked; materialises the compiler-owned test overlay into the isolated executor tree, preserves the accepted bytes as read-only to the executor, verifies them by re-hashing against the canonical bundle, and lands those exact files beside the implementation; adds `/compile`'s prefilled `/dispatch` line and **/dispatch --help** entry only when the successor ships; moves `delegation`'s `references/mode.md` into the Collection Library rather than reading peer internals; and cites the field evidence of the 21 `†`-marked records in `docs/rework/02-adr-triage.md` from git history rather than rediscovering it.

## What it ships

`skills/code/compile/`, with no engine. Compilation, codebase recon, test authorship, scope judgement, and cold-read correction are model work; `git` supplies committed-object reads, detached worktrees and blob identities, while `gh` supplies the tracker Interface. A private script would either be a shallow wrapper around those commands or the beginning of the runtime subsystem the pipeline is deleting. If `/dispatch` later proves one deterministic plan-store operation needs a helper, that helper must be small, live at the shared consumer boundary, and do that one thing.

- `SKILL.md` — frontmatter plus the executable body. `disable-model-invocation: true`; `argument-hint: '[--yes] [#<ticket> ...] [-- <instruction>]'`; `kntnt.binaries: "git gh uv"`, empty Skill and External lists, and `kntnt.capabilities: "subagents"`.
- `help.md` — the root manpage in the fixed profile.
- `agents/openai.yaml` — the Codex sidecar, mirroring the user-only invocation policy.
- `references/compiling.md` — the recon and synthesis review that turns one durable child and its parent into the two-register plan without inventing intent.
- `references/cold-read.md` — the fresh-context verdict brief, filled from one finished bundle.

And one Collection Library file plus one authoring rule module, because the consumers are already named:

- `library/references/compiled-plan.md` — the bundle, manifest, footprint, allocation, freshness, test-ownership, and lifecycle Interface written by `/compile` and read by `/dispatch`.
- `docs/rules/pipeline.md` with its `AGENTS.md` pointer — the shared ticket-selection grammar and the rules that make plan freshness and compiler-owned tests mean one thing across `/compile`, `/dispatch`, and `/land`.

The implementation also updates `/to-slices`' closing handoff and manpage, adds the README section, regenerates the Catalog, and covers source freshness, exact footprints, batch allocations, red seam tests, cold-read acceptance, and the cross-Skill handoff in the suite.

## Boundaries judged rather than followed

**The plan is a local runtime baton, not a tracker comment or repository document.** The durable ticket deliberately excludes exactly what the plan adds, and publishing those excerpts and allocations beside it would restore the stale second account the just-in-time split removed. The Git common directory is the one local address linked worktrees share without dirtying the repository; losing it costs a cheap recompile rather than a recovery protocol.

**The shared runtime contract and the authoring rule are different documents.** `$LIBRARY/references/compiled-plan.md` is installed implementation that `/compile` and `/dispatch` execute. `docs/rules/pipeline.md` tells contributors what the three Skill Interfaces must continue to promise and earns the `AGENTS.md` pointer forecast in `04-frame.md`. Each points at the other's subject instead of copying its detail.

**A dirty working tree does not change what “against `HEAD`” means.** Requiring the owner to stash unrelated work would add ceremony without improving the executor's vantage. Compiling in a detached tree keeps local content out by construction; overlap is reported because dispatching onto that working tree is a later practical conflict, not because it changes the plan.

**Blocked tickets may compile and then expire.** The shared grammar assigns blocker completion to dispatch eligibility, not compile eligibility. Moving that gate earlier would make `/compile`'s bare form disagree with the dossier and prevent one batch from allocating shared serial resources across the selected set. The cost is bounded: a blocker landing changes `HEAD`, and the dependent plan is then plainly stale rather than subtly wrong.

**Source freshness includes the tracker, not only Git.** A comment can settle an acceptance criterion without moving `HEAD`; a plan that ignored that move would be stale while claiming the code had not drifted. Fingerprinting the whole child thread and relevant parent source keeps “current” honest on both halves of the input.

**The cold reader is an inherited verdict, not routed execution.** Moving `delegation`'s mode document belongs to `/dispatch`, as `05-to-slices.md` records for the later cycle. `/compile` neither moves it early nor recreates its doctrine; collection law already says the independent judgement stays on the exact main seat.

**No script runtime in this mini-cycle.** The complex work is judgement, and the deterministic operations already have public seams in `git` and `gh`. A plan-store engine now would either expose every judgement as input — a shallow Interface — or begin absorbing compilation itself. The compiled-plan contract is deliberately the seam a later small validator could deepen if real execution proves one necessary.

**`--yes` exists only where selection asks a yes-or-no question.** Bare invocation asks whether to compile the displayed set; explicit references do not. Accepting the flag beside references would violate the collection rule that a flag with no work is refused, and omitting it from the Skill entirely would leave the bare form without the unattended answer the dossier explicitly gives it.

## What this Skill deliberately does not do

It does not frame, reopen owner decisions, slice work, alter the blocking graph, compute a dispatch wave, route or launch an executor, claim a ticket, implement code, merge, close a child or parent, reconcile knowledge, or import routing evidence. It does not let a test become the compiler's hidden way of changing product intent. It produces the execution contract and its independent tests; `/dispatch` owns everything that happens after that baton is accepted.

## Settled by the owner

The two consequences the repository could not answer were put to Thomas on 2026-08-26 and answered in one round. They are recorded here as decisions, not as open questions; the frontier is empty.

**R1 — Compiled plans are clone-local and ephemeral under the Git common directory.** Portability would buy transport while leaving every freshness condition intact, plus add storage and authentication machinery for tests and excerpts. Compilation and dispatch therefore happen in the same clone; losing its Git directory loses accepted plans, and the recovery is a cheap recompile rather than a portable plan protocol.

**R2 — Accepted compiler-owned seam tests land as permanent regression tests.** The dispatcher, never the executor, owns their bytes: it materialises the overlay, verifies the files by re-hashing against the canonical bundle after execution, and lands the exact accepted files beside the implementation. That placement mechanism is an explicit inherited requirement on the `/dispatch` brief together with plan-bundle consumption and retirement, `/compile`'s handoff line and `SEE ALSO`, the delegation-mode move, and the field evidence behind the `†` records.

## The slices

Two tickets under the settled answers, awaiting the owner's separate approval of the breakdown. Both fit one fresh context, and neither is a Solo Ticket — the shared rules govern three pipeline Skills rather than rewriting an invariant every shipped file is under.

**S1 — The compiled-plan Interface and shared pipeline rules.** `$LIBRARY/references/compiled-plan.md` states the two-register bundle, manifest, exact footprint, serial allocation, source and `HEAD` freshness, compiler-owned test overlay, and lifecycle `/compile` and `/dispatch` share. `docs/rules/pipeline.md` plus its `AGENTS.md` pointer states the common ticket-selection grammar and cross-Skill ownership rules, with focused contract and pointer coverage. *Blocked by: nothing.* Delivers: one deep Interface for every plan producer and consumer, before either side depends on private prose.

**S2 — `/compile` accepts independently checked executor plans.** The Skill directory, its compiling and cold-read references, README section, Catalog entry, and tests; it selects ready executable children, reads each complete thread and parent contract, compiles from a stable current `HEAD`, runs the clean baseline and red seam tests, pre-allocates serial resources, cold-reads each bundle, and parks only tickets that cannot be specified honestly while the batch continues. The same ticket adds `/to-slices`' prefilled `/compile #<child> ...` line and `SEE ALSO` entry. *Blocked by: S1.* Delivers: current ready tickets converted into fresh, self-contained and independently accepted execution contracts, with immutable test authorship separated from implementation.
