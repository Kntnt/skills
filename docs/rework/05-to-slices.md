# Phase 2, step 1 — `/to-slices`, as designed

> Draft written 2026-08-26 against commit `c7393f1`, from the `/to-slices` section of `00-brief.md`, the three requirements inherited from `04-frame.md`, and what this codebase and the existing `/to-spec` and `/to-tickets` Skills answer. It was the input to the owner-level round (step 2), which ran on 2026-08-26 and settled both residuals; it is now the input to the ticket breakdown. Deleted with the rest of `docs/rework/` by the final cleanup ticket.

The dossier states what `/to-slices` is for; this file is the design that satisfies it, the boundaries judged along the way, and what the owner settled. Everything here is settled — resolved from `docs/rules/`, from the Frame Record contract, from the Skills this one replaces, and from the configured tracker, or answered by Thomas in the round recorded below. Nothing in it is still a question.

## What the Skill is

`/to-slices` turns one complete Frame Record into the durable decision layer: one decision document and the tracer-bullet tickets that deliver it. The decision document is a GitHub parent issue; each slice is a child issue, and the blocking relations between those children are the graph later Skills execute. The Frame Record is the input baton and is deleted only after the complete approved set is present and verified on the tracker.

The Skill makes the technical decisions that slicing requires — where the verification seam sits, which work is one demonstrable vertical slice, which edges genuinely block, and where a wide refactor needs expand–contract. It opens no new product interview. A missing owner decision sends the record back to `/frame`; the one question `/to-slices` itself owns is whether the proposed breakdown and its blocking graph are approved.

## The input, and when it is ready

The Interface takes one Frame Record. A path operand addresses it directly. Bare invocation uses the only record under `.kntnt/frames/`; no record is a stop with the `/frame` handoff, and several records produce a choice rather than a guess. The prefilled line `/frame` hands over makes the direct path the normal form.

The Skill reads `$LIBRARY/references/frame-record.md` and validates the contract before synthesising anything: the seven headings are present in order, every address-bearing entry has an address, every ledger decision still in force names a frame, and every open entry names its owner and what would answer it. A malformed or unfinished record is left untouched and returned to `/frame --resume=<path>` with the defect named.

The framing commit is the currency of the handoff. `/to-slices` compares the commit section 1 names with `HEAD`. Where they differ, it reads the intervening diff before deciding that the findings have gone stale. If every changed path is a file named by an entry in section 7, the diff is framing's own durable output rather than a changed world: `/to-slices` verifies that containment, stamps section 1 with the current `HEAD`, and continues. Any changed path outside that manifest hands back `/frame --resume=<path>`, whose existing resume contract re-reads the frames and re-checks findings touched by the intervening diff. Once the record names the current `HEAD`, that commit becomes every published ticket's vantage point.

Section 7 is checked entry by entry before publication. Every entry must resolve from `HEAD`, not merely from the working tree, because the decision document is about to become the manifest `/land` follows after the record is gone. Nothing requires the rest of the tree to be clean. An entry that exists only locally stops publication with the exact entry and file named and a precise instruction to commit that knowledge; `/to-slices` stages and commits nothing itself. The resulting knowledge-only move of `HEAD` is the exception above, so the next invocation can stamp the new vantage and continue without sending unchanged findings through `/frame` again.

## Synthesis, not transcription

The decision document carries what stays true while the tickets wait: the outcome, scope, active decisions, binding constraints, and the knowledge manifest. It does not copy the Frame Record wholesale. Recon findings are folded into a decision, a constraint, or a compilation hint only where they materially govern later work; raw findings, their exploration trail, superseded ledger alternatives, and the interview's machinery die with the record.

The same durability rule binds every surface. No code excerpt, line number, current-state file inventory, reserved serial number, or exhaustive enumeration of a growing collection enters the decision document or a ticket. A stable area, symbol, or exemplar pattern may be named, and the vantage commit says where that hint came from. Exact files, fresh excerpts, serial allocations, and commands belong to `/compile`, written against the tip the executor will actually receive.

## The decision document

The Skill always creates a new GitHub issue rather than turning an existing source issue into its own document. A source issue named by the framing is linked under provenance and otherwise left untouched; the existing `/to-tickets` rule not to rewrite or close a parent request survives here.

The document has these sections:

1. **Outcome** — the task in the owner's words and the observable result the set delivers.
2. **Scope** — what the decision covers and what it deliberately leaves out.
3. **Decisions** — the active owner decisions and unvetoed ledger decisions, synthesised without changing their meaning.
4. **Constraints** — the frames that bind implementation, each with its durable source address.
5. **Slices** — the approved snapshot, in an order that makes the frontier legible: each child's title or published reference, delivered behaviour, seam, blockers, and Solo Ticket status. It is the recovery source until publication completes and the durable account of what the owner approved afterwards; the live blocking graph stays in the tracker's dependency relations rather than this snapshot becoming a second scheduler input.
6. **Open experiments** — the spike issues that answer section 6 entries, and the downstream decisions or slices each result may change.
7. **Knowledge to reconcile** — every section 7 entry and its address, carried forward whole so `/land` can check it against the implementation.
8. **Provenance** — the Frame Record's relative path, its framing commit, the commit this set was published against, and any source issue.

The decision issue is not executable work and never receives the repository's ready-for-agent label. It receives any scope label and milestone the repository's tracker convention or the Contextual Instruction requires. Its child relation, not a ready label, is how later readers know what work belongs to it.

The decision issue stays open while any child is still live. Once every child has reached a terminal state — landed, or explicitly abandoned as `wontfix` — `/land` closes the parent as part of the same knowledge closure that reconciles its section 7 manifest. That closing duty belongs to `/land`'s mini-cycle and is recorded here rather than implemented early by `/to-slices`.

The shape belongs in `$LIBRARY/references/slices.md`, not inside `/to-slices`: `/to-slices` writes it, `/compile` reads the child contract, and `/land` reads the parent and its knowledge manifest. Starting it in one Skill would make the writer the owner of its consumers' input Interface, the same false ownership `frame-record.md` avoided.

That manifest preserves the third requirement inherited from `04-frame.md`: `/land` checks every knowledge entry the framing wrote against what the implementation actually did, and corrects or replaces it where the two diverge. `/to-slices` performs no reconciliation early; its duty is to carry the complete list across the point where it deletes the only other manifest.

## The slice contract

Each implementation ticket is narrow enough for one fresh context window, independently demonstrable or verifiable, and complete through every layer its behaviour crosses. A layer-only task is folded into the first behaviour that needs it unless it is an expand step, a contract step, or an experiment whose own result is the deliverable.

Every ticket carries:

- **What to build** — the end-to-end behaviour this slice makes real, in the project's own vocabulary.
- **Acceptance criteria** — observable, checkable outcomes, complete enough that `/compile` can turn them into machine-checkable done criteria without inventing product intent.
- **Seam contract** — what behaviour is verified and at which seam. Prefer the highest stable existing seam; introduce a seam only where no existing one can express the behaviour, and keep the new Interface smaller than the behaviour it hides.
- **Compilation hints** — areas to inspect, stable symbols, and exemplar patterns. They orient fresh recon and never pretend to be the exact file list or implementation plan.
- **Vantage point** — the commit the ticket was written against.
- **Parent and blockers** — native GitHub relations where available; textual `Parent` and `Blocked by` fallbacks where the tracker exposes no relation.
- **`Builds alone`**, opening its own line, exactly where the ticket's subject is a repository-wide invariant that rewrites or newly enforces a rule every shipped file is under.

The ticket is self-contained about its own behaviour and verification seam. The parent remains the authoritative account of decisions shared across slices; `/compile` follows the parent relation and inlines the relevant decisions into the plan rather than making every child duplicate the whole document.

All executable children receive the repository's ready-for-agent state on publication — `ready-for-agent` by the default convention, or the repository's explicit equivalent. On this rework track the Contextual Instruction supplies `rework` plus `rework-ready-for-agent` and the “Skills 2.0” milestone, never plain `ready-for-agent`. A non-executable gate receives the repository's honest waiting state instead of masquerading as work an agent can start.

## How the slices are cut

**Tracer bullets are the normal form.** Each one takes a thin complete path to an outcome a reviewer can demonstrate or verify on its own. Sizing is against one fresh context window, not against a file count or an estimate of human days. Prefactoring that only makes a later change easier is absorbed into the first slice that uses it; otherwise the graph fills with horizontal tickets whose completion proves no behaviour.

**Blocking edges state necessity, not preferred order.** A child blocks another only where the latter cannot be implemented or verified honestly before the former lands. Presentation order, likely execution order, shared files, and a desire to reduce conflicts do not create semantic edges. Scheduling and collision avoidance belong to `/dispatch`, which recomputes waves from the graph and the compiled footprints.

**Wide refactors use expand–contract.** Expand introduces the new form beside the old while keeping the repository green; migration batches move bounded parts of the blast radius while both forms coexist; contract removes the old form after every migration. Each batch is sized for one fresh context and is blocked by expand; contract is blocked by every batch. The compatibility interval is what keeps every ticket landable — no shared red integration branch is smuggled into the durable graph, because `/dispatch` only merges independently verified work.

**Repository-wide invariants build alone.** The Skill writes the exact declaration instead of trying to infer a conflict surface no ticket can enumerate. The declaration affects scheduling only; it does not turn a broad feature into an acceptable ticket or excuse one from the single-context bound.

**An experiment is a slice with a decision as its outcome.** Every section 6 question that only an experiment can answer becomes its own spike ticket, carrying the question, the experiment, the observation seam, and the decision rule that turns the result into an answer. Every slice whose honest contract depends on that answer is blocked by the spike. This is the second requirement inherited from `04-frame.md`; `/land` later refreshes the affected downstream tickets from the landed result rather than expecting `/to-slices` to guess it in advance.

## The approval checkpoint

Before writing anything to GitHub, the ordinary form presents the proposed decision document in owner register and the complete slice set as a numbered list. Each slice shows its title, delivered behaviour, seam contract, blockers, and whether it builds alone. The question is confined to the two judgements the dossier assigns this checkpoint: whether the granularity is right and whether the blocking edges are true. A requested merge, split, or corrected edge is folded into a new complete preview; nothing is published until the owner approves one.

A proposed slice that exposes a missing product or architecture decision is evidence that framing is incomplete, not an invitation for `/to-slices` to grow a second interview. The Skill names the point, leaves the record in place, and hands it back to `/frame --resume=<path>`. Technical choices inside established frames are taken by the Skill and made visible in the preview.

`--yes` answers that approval yes before synthesis and therefore asks no question, exactly as the collection rule requires of every Skill that carries it. It accepts the Skill's first complete proposal and proceeds directly to publication; it cannot make an incomplete Frame Record complete, select among several records, or answer a product decision discovered missing. The live preview remains the default, and the full grammar is `/to-slices [--yes] [<frame-record>]`.

## Publication and recovery

After approval, publication is one recoverable transaction expressed through ordinary `gh` operations rather than through an engine:

1. Create or recover the decision issue, whose provenance contains the Frame Record path and framing commit.
2. Create each child in dependency order, apply the configured labels and milestone, and attach it to the decision issue.
3. Write every native blocking relation, or the body fallback where GitHub does not expose one.
4. Replace each provisional slice name in the decision document with its published issue reference, retaining the approved behaviour, seam, blockers, and Solo Ticket status beside it.
5. Read the parent and every child back, verifying bodies, state, labels, milestone, parentage, and every edge.
6. Delete the Frame Record only after that read proves the complete approved set is published.

The provenance pair makes re-invocation idempotent without a script or a second state file. The parent is written with the complete approved slice snapshot before the first child is created, so a network failure leaving a parent and three of five children leaves both the input record and the exact approval it was being published from. The same invocation finds that parent, reconciles what exists against its snapshot, creates only what is missing, repairs missing relations, verifies, and then deletes the record. A conflict between published content and the still-present record is reported rather than overwritten, because another actor may have edited the tracker after the partial run.

The deletion is the first inherited requirement from `04-frame.md`. “Published” means the verified parent, every child, and every relation — not that the first `gh issue create` returned a number. A failed publication reports exactly what exists and leaves the record as the recovery baton.

## The handoff, and the order things land in

The `/to-slices` implementation ticket also completes `/frame`'s deferred handoff. `/frame`'s closing report gains the exact next line, with the record path filled in: `/to-slices .kntnt/frames/<slug>.md`. `/frame`'s manpage adds **/to-slices --help** to `SEE ALSO`. Both changes land with the successor they name, so no shipped help points at a Skill the Catalog cannot supply.

`/compile` does not exist on the day `/to-slices` lands. The first version therefore closes in `$LIBRARY/references/tldr-mode.md` with the decision issue, the approved children, the current frontier, and anything publication left unresolved; it names what compilation will add later but invents no invocation for a missing Skill. The `/compile` implementation ticket will add `/to-slices`' prefilled next line and `SEE ALSO` entry, by the same handoff rule this mini-cycle inherits from `/frame`.

## What it ships

`skills/code/to-slices/`, with no engine. Synthesis, seam selection, and slice judgement are agent work; GitHub already supplies the deterministic persistence Interface, and a wrapper around a handful of `gh` calls would add a second tracker client without hiding meaningful complexity.

- `SKILL.md` — frontmatter plus the executable body. `disable-model-invocation: true`; `argument-hint: '[--yes] [<frame-record>] [-- <instruction>]'`; `kntnt.binaries: "git gh uv"`, with empty Skill, External, and Capability lists.
- `help.md` — the root manpage in the fixed profile.
- `agents/openai.yaml` — the Codex sidecar, mirroring the user-only invocation policy.
- `references/slicing.md` — the tracer-bullet, expand–contract, spike, seam, and Solo Ticket review used while cutting the set.
- `references/publishing.md` — the GitHub publication order, native relations and fallbacks, provenance recovery, and final read-back gate.

And one Collection Library file, because its consumers are already named:

- `library/references/slices.md` — the durable decision-document and ticket contract written by `/to-slices`, read by `/compile`, and closed over by `/land`.

The implementation also updates `/frame`'s closing handoff and manpage, adds the README section, regenerates the Catalog, and covers the new contract and cross-Skill handoff in the suite.

## Boundaries judged rather than followed

**The decision document is a parent issue, not a tracked repository file and not the source request.** The existing chain already publishes specs and tickets to the configured tracker, GitHub supplies child and dependency relations, and the dossier explicitly puts the tickets there. One parent issue keeps decisions beside the work they govern without adding a second tracked documentation stream or rewriting the reporter's words.

**Native tracker relations are the live graph.** The configured issue-tracker document calls GitHub's issue dependencies canonical and supplies body lines only as fallback. The decision document keeps the approved graph as provenance and recovery state, while schedulers read the native relations; those are two different jobs rather than two competing live inputs. The approval preview is the snapshot before it receives issue numbers, not a third copy.

**`--yes` is present because approval has work for it.** The collection's flag grammar settles presence from function, and the collection's behaviour settles the meaning: no yes/no question is asked, and every such answer is yes. The flag pre-authorises the first complete graph; it does not fill a missing operand or owner decision, because neither is a yes/no question.

**No subagent or model-selector Dependency.** `/frame` has already paid for recon and protected the main context from its raw material. `/to-slices` is the high-ceiling synthesis itself, and its human checkpoint is the independent check on the decomposition. Delegating pieces of that synthesis would split one graph across contexts and then spend the main context joining it again.

**`git` and `gh` are hard Dependencies.** The Interface promises GitHub publication in the repository whose current commit becomes the vantage point. Without either binary there is no degraded form that still produces the promised durable layer. `uv` is the dependency checker's own requirement. No Capability is needed.

**No new rules module and no `AGENTS.md` pointer.** The durable shape is runtime implementation shared by three Skills and belongs in the Collection Library. It does not bind contributors authoring arbitrary tickets in this repository beyond `docs/rules/tickets.md`, and that module already states the durability and Solo Ticket rules that apply here.

## What this Skill deliberately does not do

It does not frame or reopen settled owner decisions. It does not write code, prototype, compile a plan, author a test file, allocate a serial resource, compute a dispatch wave, claim a ticket, or close a source request. It does not publish a horizontal implementation checklist and call it slicing. It leaves exact files and current code to `/compile`, scheduling to `/dispatch`, and landed-ticket closure plus knowledge reconciliation to `/land`.

## Settled by the owner

The two consequences the repository could not answer were put to Thomas on 2026-08-26 and answered in one round. They are recorded here as decisions, not as open questions; the frontier is empty.

**R1 — The decision issue stays open through delivery.** It is the progress umbrella until every child has landed or been explicitly abandoned as `wontfix`; `/land` then closes it as part of the knowledge-closure step that already reads it. GitHub shows the unfinished outcome without labeling the parent ready for execution, and `/land`'s mini-cycle inherits the closing duty.

**R2 — Framing knowledge must be in history before publication.** Every section 7 entry must be reachable from `HEAD`, without requiring the rest of the tree to be clean. A local-only entry stops with a precise commit handoff, and `/to-slices` never auto-commits: doing so would take separate authority and could sweep unrelated edits from the same files. The manifest the decision issue preserves therefore resolves in every clone `/compile`, `/dispatch`, and `/land` may run from. Committing the framing's own section 7 files does not stale its findings; the exception under *The input, and when it is ready* verifies that limited diff, stamps the current `HEAD` as the new vantage, and continues.

## The slices

Two tickets under the settled answers, pending the owner's approval of the breakdown. Both fit one fresh context, and neither is a Solo Ticket — nothing here rewrites a rule every shipped file is under.

**S1 — The durable slice contract in the Collection Library.** `library/references/slices.md` states the decision issue, child ticket, seam contract, compilation hint, graph, provenance, and knowledge-manifest shapes their writer and later readers share, with suite coverage for its resolved pointers. *Blocked by: nothing.* Delivers: the durable Interface `/to-slices` writes and `/compile` plus `/land` can rely on without reading a peer's internals.

**S2 — `/to-slices` publishes an approved slice set.** The Skill directory, its local slicing and publishing references, README section, Catalog entry, and tests; it validates and synthesises one Frame Record, previews the complete graph, publishes the verified parent and children recoverably, and deletes the record only on success. The same ticket adds `/frame`'s prefilled `/to-slices <path>` line and `SEE ALSO` entry. *Blocked by: S1.* Delivers: a framed task turned into durable decisions and ready tracer-bullet tickets, with the next pipeline handoff visible at the Skill that produces its input.

The parent-closing duty is recorded here for `/land`'s mini-cycle rather than implemented early. The committed-knowledge gate, its precise stop, and the knowledge-only vantage exception land inside S2's handoff wording and preflight.
