---
name: compile
description: Compile ready executable child tickets into fresh, independently checked executor-plan bundles.
disable-model-invocation: true
argument-hint: '[--yes] [#<ticket> ...] [-- <instruction>]'
compatibility: Requires git, gh, and uv, plus a Harness that can spawn subagents
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "git gh uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: "subagents"
---

# compile

Turn ready executable children into self-contained executor plans against one stable current tree. Compilation moves current codebase facts, exact scope, verification, serial allocation, and finished seam tests into a clone-local bundle before execution begins; a fresh-context cold reader must prove each bundle stands alone before it is accepted.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

The payload's `capabilities` are the half of the check no script can do — you are the Harness, so answer whether each `confirm` sentence is true. Any Unsatisfied Capability: give its `how`, compile nothing, change nothing, and stop. Exit 0 is not a go-ahead until every Capability is answered.

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is `library/` under the Manager directory that contains the checker — absent, tell the user to run `/kntnt update`, then stop.

## Invocation

Read `$LIBRARY/references/invocation-envelope.md` and follow it before help routing or formal validation; only the Formal Invocation reaches Help, Arguments, scripts, and nested formal parsers. `--help`, `-h`, and `help` print `$HERE/help.md` verbatim and stop.

## Arguments

`/compile [--yes] [#<ticket> ...]`, and nothing else. Every ticket reference is a local `#`-prefixed issue number. Flags precede operands, and explicit references preserve the order written.

- `--yes` — answer yes without asking at the bare selection checkpoint. With explicit references there is no question to answer, so refuse `--yes` beside explicit references rather than ignoring it.
- `#<ticket> ...` — the complete explicit selection. Each reference must name an open executable child in the current repository; parent decision issues, qualified references, ranges, bare numbers, and free text are invalid operands.

An undeclared flag, a flag after an operand, or any invalid operand is refused as `$LIBRARY/references/invocation-envelope.md` says. Compile nothing, mutate no tracker state, write no bundle, and stop.

## Selection

Read `docs/rules/pipeline.md` from the repository being compiled when it exists, then resolve the repository's tracker convention from its always-loaded agent file and selected issue-tracker document. Resolve the configured executable-ready state, including every required scope label, rather than assuming plain `ready-for-agent`.

Explicit references are the complete selection and need no confirmation. Report an explicitly selected child with a fresh accepted bundle as already fresh and leave it unchanged; report an ineligible reference precisely rather than silently dropping it.

With no references, select every open executable child carrying the configured executable-ready state and lacking a fresh accepted bundle, ordered by ascending issue number. Render that complete selection and ask one yes-or-no question before work; `--yes` answers yes without asking. An empty selection is reported and changes nothing.

Blockers do not gate compilation. Read and record them as durable input, but leave execution eligibility and scheduling to `/dispatch`; a blocker landing changes `HEAD` and therefore expires the dependent plan naturally.

## Durable input

Read `$LIBRARY/references/slices.md`, then fetch each selected child through its contract: complete body and every comment oldest first, parent relation, parent decision issue with its complete body and thread, and native blocking relations or the documented fallbacks. A later comment outranks earlier contradictory text. Follow the parent only for outcome, scope, decisions, and constraints relevant to this child; do not compile sibling implementation detail into its requirement.

Applicable Contextual Instruction or Conversation Context may answer an owner-owned gap only when it comes from the owner and stays inside the durable decision. Write that answer to the child thread before compilation so the next compiler sees the same complete source. Refuse guidance that contradicts or widens the durable decision instead of publishing it.

A nonconforming child or an owner-owned gap cannot produce an honest plan. Gather every missing owner-owned point into one complete question, post it once, remove only its executable-ready state, add `needs-info`, preserve its scope labels and milestone, and continue with the remaining selected children. Technical choices inside the repository's frames are the compiler's to make and state in the plan; they never become parking questions.

## Stable batch

Capture the repository identity, integration branch, and full `HEAD`, and resolve the store with `git rev-parse --git-common-dir`. Create a temporary detached worktree at that commit and read all implementation state there, so unrelated local edits are neither hidden nor absorbed; report local changes that overlap a plan's eventual footprint without treating them as source.

Resolve the complete repository verification gate from the detached tree's always-loaded instructions and contribution guide. Run that untouched repository gate once for the batch before a seam-test overlay exists. A red baseline stops the batch, reports the exact command and failure, parks no child, and accepts no bundle.

If the integration branch moves from the captured `HEAD` while compiling, discard candidates and restart the whole batch from the new tip so footprints and allocations share one vantage. Remove every temporary worktree the run created when it is no longer needed, including on failure.

## Compilation

Read [`compiling.md`](references/compiling.md). Reconcile each durable vantage and compilation hint with the captured tree, then produce the complete bundle required by `$LIBRARY/references/compiled-plan.md`: binding contract, advisory appendix, exact footprint, serial allocations, manifest, verification commands, machine-checkable done criteria, STOP conditions, and finished compiler-owned seam tests.

Materialise each candidate's test overlay over a clean detached tree at the captured `HEAD` and run every focused command. Accept a red baseline only at the intended behavioural assertion for missing ticket behaviour; syntax, import, fixture, collection, environment, or unrelated assertion failure rejects the candidate. Seal every accepted test's destination, base blob, and compiled blob; an executor never owns those bytes.

After recon fixes every plan's serial needs, allocate once per registry across the deterministic selected-ticket order. Account for committed identifiers and allocations held by other fresh plans at the captured `HEAD`. A plan receives exact identifiers, and needing another identifier is a STOP condition rather than authority to rescan or extend the allocation.

## Cold read

Fill [`cold-read.md`](references/cold-read.md) for one completed candidate and launch a fresh-context subagent on the exact inherited main seat. Give it only the bundle and a clean detached tree at the captured commit: no tracker access, compiler notes, or explanation of intent.

Only a concrete PASS accepts the candidate. Correct a mechanical finding and give the complete corrected candidate to a new cold reader; never ask the same context to approve the correction it requested. A finding that exposes an owner-owned gap parks only that child through the Durable input rule, while siblings continue. A failure in the cold-read mechanism reports that child as failed and accepts nothing for it.

## Acceptance

Immediately before acceptance, verify that the integration branch still points at the captured `HEAD`; re-read the child and parent sources; recalculate the child source fingerprint, parent source fingerprint, and bundle fingerprint; and validate every manifest reference and bundle byte against `$LIBRARY/references/compiled-plan.md`. A changed branch restarts the batch. A changed tracker source recompiles that child and sends the new candidate to a new cold reader.

The plan root is `<git-common-dir>/kntnt-pipeline/plans/<ticket>/`, commonly `.git/kntnt-pipeline/plans/<ticket>/`. Publish the verified candidate as one immutable bundle directory at `.git/kntnt-pipeline/plans/<ticket>/bundles/<fingerprint>/`, using the fingerprint hexadecimal without its `sha256:` prefix, then replace the `accepted` pointer by atomic rename only after the directory is complete. Never edit an immutable bundle directory or expose a partial candidate. Follow the shared Interface for identical interrupted candidates, replacement, cleanup, and recovery.

Successful compilation changes no tracker state. The bundle remains clone-local and untracked; no plan, excerpt, allocation, or test is posted to the issue.

## Completion

Close in the register of `$LIBRARY/references/tldr-mode.md`. Partition every selected item exactly once as accepted, parked, already fresh, or failed; give the captured `HEAD`, all accepted bundle paths, each complete parking question, the red command or acceptance failure for failures, and any local overlap that will matter before execution. Name that accepted bundles are for `/dispatch`, but invent no `/dispatch` invocation before that Skill ships.
