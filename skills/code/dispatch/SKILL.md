---
name: dispatch
description: Execute, review, land, and recover fresh compiled plans on the current branch.
disable-model-invocation: true
argument-hint: '[--dry-run] [--at-once=<n>] [--model=<name>] [--deliberation=<low|medium|high|xhigh|max>] | [--dry-run] [--at-once=<n>] [--model=<name>] [--deliberation=<low|medium|high|xhigh|max>] [#<ticket> ...] | [--at-once=<n>] [--model=<name>] [--deliberation=<low|medium|high|xhigh|max>] [--yes] | [--at-once=<n>] [--model=<name>] [--deliberation=<low|medium|high|xhigh|max>] [#<ticket> ...] [-- <instruction>]'
compatibility: Requires git, gh, and uv, model-selector, plus a Harness that can spawn subagents
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "git gh uv"
  kntnt.skills: "model-selector"
  kntnt.externals: ""
  kntnt.capabilities: "subagents"
---

# dispatch

Execute fresh accepted compiled plans in disposable worktrees, judge every result on the unchanged main seat, and land approved changes serially on the branch where the invocation began. The live frontier is recomputed after every landing; compilation owns intent and tests, executors own only their exact patch footprint, and dispatch owns scheduling, review, integration, tracker transitions, recovery, and cleanup.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

The payload's `capabilities` are the half of the check no script can do — you are the Harness, so answer whether each `confirm` sentence is true. Any Unsatisfied Capability: give its `how`, dispatch nothing, change nothing, and stop. Exit 0 is not a go-ahead until every Capability is answered.

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is `library/` under the Manager directory that contains the checker — absent, tell the user to run `/kntnt update`, then stop.

## Invocation

Read `$LIBRARY/references/invocation-envelope.md` and follow it before help routing or formal validation; only the Formal Invocation reaches Help, Arguments, scripts, and nested formal parsers. `--help`, `-h`, and `help` print `$HERE/help.md` verbatim and stop.

## Arguments

The live forms are `/dispatch [--at-once=<n>] [--model=<name>] [--deliberation=<low|medium|high|xhigh|max>] [--yes]` and the same flags with `#<ticket> ...` instead of `--yes`. The read-only forms add `--dry-run` and accept either bare or explicit selection, but no `--yes`. Every flag precedes every operand; explicit references preserve the order written.

- `--dry-run` — render the current scheduling and routing facts without mutation. Always refuse `--yes` beside `--dry-run` because a read-only form has no confirmation to answer.
- `--at-once=<n>` — set the positive integer execution ceiling; default `1`.
- `--model=<name>` — lock only the model field supplied to Route for every executor decision.
- `--deliberation=<low|medium|high|xhigh|max>` — lock only the deliberation field supplied to Route for every executor decision.
- `--yes` — answer yes without asking at the bare live selection checkpoint. With explicit references there is no question to answer, so refuse that combination too.
- `#<ticket> ...` — the complete explicit selection of local issue references, in written order.

An undeclared flag, a flag after an operand, an invalid value or operand, or a combination above that gives a flag no work is refused as `$LIBRARY/references/invocation-envelope.md` says. Dispatch nothing, mutate no tracker state, open no journal, and stop.

## Resolve or open the run

Require a clean integration tree, capture the current repository identity, full integration ref and `HEAD`, and resolve `<git-common-dir>` with `git rev-parse --git-common-dir`. Read `$LIBRARY/references/compiled-plan.md`, `$LIBRARY/references/landed-change.md`, `$LIBRARY/references/delegation-mode.md`, the repository's governing agent file, and the issue-tracker and triage conventions that file selects.

Resolve the active journal for the full integration ref through `$HERE/scripts/journal.py`. An active journal resumes only through its exact recorded invocation, including the effective Contextual Instruction; any different invocation reports the active run and its exact resume line, then stops without opening or mixing another run.

A ticket is dispatch-eligible only when it is an open executable child in the current repository, has a fresh accepted compiled plan for the current integration branch and tip, every declared blocker has exactly one selected landing commit reachable from the integration tip, and no active journal owns it. Issue closure is never the landing signal. A missing or ambiguous landed-change baton, stale source or bundle, or journal ownership makes the ticket ineligible with its exact reason; assignment is deliberately checked only after Route, immediately before execution.

Explicit references are the complete selection. If any reference is invalid or ineligible, refuse the complete invocation rather than narrowing it. Bare selection takes every dispatch-eligible ticket in ascending issue number, renders the complete list, and asks one yes-or-no question before live work; `--yes` answers yes without asking. An empty selection reports no work and changes nothing.

## Dry run

For a dry run, compute and render the current graph, footprint exclusions, first executable frontier, provisional later waves, and Route readiness. The later waves are explicitly provisional because every landing changes the facts. A dry run opens no journal, assigns no ticket, persists no Route decision, creates no worktree or branch, and mutates neither Git, tracker, plan store, nor model-selector state.

## Open and schedule live work

Record immutable opening metadata and selection through the journal helper before consuming work. The opening binds repository, integration ref, opening `HEAD`, normalized exact invocation, effective instruction bytes, selected tickets in order, `--at-once`, and both Route override fields. Read `$HERE/references/recovery.md` whenever the journal projection reports a continuation rather than new work.

At every live scheduling turn, re-read current blockers, integration reachability, journal outcomes, and remaining fresh footprints. Admit blockers first; give a declared Solo Ticket its own frontier; otherwise greedily fills the frontier in selection order up to `--at-once`. Recompute after each serial landing, tracker transition, rebuild request, park, or newly discovered dependency.

Two plans never execute together when either writes a path the other reads or writes. Executor-owned `modifies`, `creates`, and `deletes` paths and compiler-owned test destinations are writes. The dispatcher-owned shared writes do not exclude siblings because executors never touch them; pre-allocated serial resources do not exclude siblings because compilation assigned disjoint identifiers.

Freshness-check every admitted member against one same current integration tip, then copy its complete accepted bundle into a byte-for-byte verified bundle escrow. Atomically publish the escrow before recording `bundle-consumed`; later attempts and recovery read that escrow rather than the mutable accepted pointer. Once an admitted execution starts, a sibling landing does not retroactively stale that consumed plan: review integrates its patch against the newer combined tip. If an unstarted waiting plan becomes stale after another landing, record REBUILD, give the exact `/compile #<ticket>` and original resume invocation, complete all independent work, and stop at that user checkpoint.

## Route, claim, and execute

For every attempt, follow `$LIBRARY/references/delegation-mode.md` exactly and invoke model-selector's public `/model-selector route` Interface with the real execution brief and declared independent review. `--model` locks only the model field, `--deliberation` locks only the deliberation field, and omission leaves that field to Route. A selection launches exactly its native controls; inheritance delegates on the exact main seat with no override; refusal launches nothing.

Store the complete Route response as an artifact and make its decision durable before assignment or launch. On resume, replay that exact recorded decision without consulting current profiles, prices, evidence, aliases, or mappings. Routing precedes assignment: immediately before execution, assign the child to the authenticated user; a ticket already assigned to another actor is stranded rather than taken.

Read `$HERE/references/executor.md` and fill its brief. Every attempt runs on a temporary dispatch branch in a disposable linked worktree rooted at the plan's captured `HEAD`, even at `--at-once=1`. The dispatcher materialises tests from the escrow, verifies each Git blob identity before launch, and gives the executor only the complete plan, captured tree, exact write paths and allocations, ticket-specific scratch, and dispatcher-write proposal channel.

After the executor returns, inventory every created, modified, deleted, mode-changed, symlink, and binary result with a temporary index seeded from the attempt base. Capture a full-index binary patch, ordered changed paths, and patch digest; persist the patch artifact before recording `patch-captured`. A patch violating executor footprint or compiler-owned test ownership remains rejected evidence and is never trimmed or replayed into a revision. An accepted patch becomes the last accepted checkpoint from which a later attempt can be recreated after ordinary branch and worktree cleanup.

For every materialised test, compare the post-attempt Git blob identity with the escrow's `compiled_blob`. A changed, replaced, deleted, or relocated compiler-owned test rejects the complete execution result. Read `$HERE/references/review.md` and perform the full review yourself on the unchanged main seat; neither the executor report nor a green command supplies the verdict.

## Land and continue

For APPROVE, create a fresh landing candidate from the current integration tip, apply only the accepted executor patch, materialise canonical tests from the canonical escrow bytes, and apply dispatcher-owned writes serially. Read the combined diff and run every seam command plus the complete repository gate on that candidate.

If it passes, author one dispatcher-authored commit carrying exactly one `Kntnt-Ticket: #<ticket>` and one `Kntnt-Plan: sha256:<bundle-fingerprint>` trailer. Advance the invocation branch only when its ref still equals the candidate's expected tip. Then verify reachability, trailer identity, tree identity, and compiled test blobs before recording `landed`.

After `landed`, execute `T-LAND` from `$HERE/references/recovery.md`; for PARK execute the transition selected there. Persist the concrete transition plan before tracker mutation and its verified completion afterward. A tracker transition completes before bundle retirement, and retirement completes before routine cleanup. The next scheduling turn starts only after the current ticket reaches that durable boundary.

A newly discovered numbered dependency is written as a native blocking edge or the repository's documented fallback and reported Stranded. A needed owner answer without a ticket to point at is PARK. Never turn either into a guessed implementation.

## Recovery and completion

Use `$HERE/references/recovery.md` and the journal projection for every continuation, bundle lifecycle decision, tracker mutation, retained conflict, terminal account, and archive check. The helper owns transactional journal persistence only; the agent owns scheduling, Route, Git, tracker, review, and every verdict.

After an externally judged routed attempt, `/model-selector observe` may write a sanitized artifact beside the archived journal. The run never invokes `/model-selector record` and imports no evidence into the ledger.

Close in the register of `$LIBRARY/references/tldr-mode.md`. Partition every selected ticket exactly once as Landed, Parked, or Stranded. Name each landing commit and bundle fingerprint, each complete parking question or handoff and tracker transition, each stranded reason, the active or archived journal path, retained conflict resources, and observation artifact. Give exact `/compile` plus resume lines for pending REBUILD states. Name that `/land` will later close the durable loop, but invent no `/land` invocation before that Skill exists.

Dispatch does not frame, slice, compile or repair plans, author or modify compiler-owned tests, allocate serial identifiers, close tickets or parents, reconcile knowledge, push, tag, release, import model evidence, or reconcile outside completion. It executes no raw ticket, freezes no whole-run schedule, and creates no separate merge or coherence-review Skill.
