# Durable slice contract

A sliced body of work has one durable decision issue and one executable child issue per approved slice. This document is their shared Interface: `/to-slices` writes both shapes, `/compile` reads the executable child and its parent, and `/land` reads the parent and its knowledge manifest. None of those Skills owns the contract carried between them.

The decision issue preserves what remains true after `/to-slices` consumes the [Frame Record](frame-record.md). The children preserve enough product intent and verification intent for just-in-time compilation. Together they carry durable decisions; exact implementation state belongs to the compiled plan written immediately before execution.

## Contract roles

`/to-slices` writes a complete decision issue and every executable child to this contract, then verifies the published content and relations before consuming the Frame Record.

`/compile` reads a child through this contract, follows its parent relation, and combines the child's own behaviour and seam with the relevant decisions and constraints from the parent.

`/land` reads the decision issue through this contract after child work lands, follows the complete knowledge manifest, and closes the parent only at the lifecycle boundary stated below.

## Durable boundary

Durable content may name stable areas, symbols, patterns, and addresses that orient a later reader. It carries the vantage point from which those hints were written so drift can be distinguished from error.

A decision issue or child carries no code excerpts, line numbers, current-state inventories, reserved serial numbers, or exhaustive enumeration that sibling work could falsify while the issue waits. Exact paths, fresh excerpts, current inventories, serial allocations, verification commands, and machine-checkable done criteria belong to the just-in-time plan.

## Decision issue

The decision issue is the non-executable parent of the approved children. It always carries these headings in this order, including headings whose sections have no entries:

```
## Outcome
## Scope
## Decisions
## Constraints
## Slices
## Open experiments
## Knowledge to reconcile
## Provenance
```

### Outcome

Carry the task in the owner's words and state the observable result delivered by the complete slice set. Preserve the owner's meaning rather than turning the outcome into an implementation description.

### Scope

State what the decision covers and what it deliberately leaves outside the work. The boundary applies to the whole slice set; a child narrows it for its own behaviour without widening it.

### Decisions

Carry every active owner decision and every unvetoed decision from the Frame Record's ledger. Synthesis may remove interview machinery and superseded alternatives, but it preserves the meaning and authority of each decision.

### Constraints

Carry every frame that binds implementation, with its durable source address. The section contains constraints that remain applicable to the children rather than a transcript of the recon that found them.

### Slices

This section is the approved slice snapshot. For every child it records the title or published issue reference and its delivered behaviour, seam, blockers, and Solo Ticket status. The order makes the approved frontier legible.

The native tracker relations are the live graph: parent-child relations define membership and dependency relations define blocking. Schedulers read those relations. The approved slice snapshot is durable provenance and recovery state; it preserves the graph the owner approved, lets an interrupted publication repair missing children or relations, and never becomes a second live scheduling input.

### Open experiments

Carry every approved experiment as a child issue, the question it answers, and the downstream decisions or slices its result may change. An empty section states that the set has no experiment still open at publication.

### Knowledge to reconcile

Carry every knowledge entry from the Frame Record's sole manifest, with its address, without dropping or summarising away an entry. This section becomes the complete knowledge manifest after the Frame Record is consumed.

### Provenance

Carry the relative Frame Record path, the framing commit named by that record, the publication commit against which the slice set was written, and any source issue the original task named. The relative Frame Record path and framing commit form the identity used to recover an interrupted publication; the publication commit is every child's shared starting vantage point.

The decision issue receives the repository's applicable scope labels and milestone, but no executable ready state. Its parent relation to the children is what identifies the body of work.

## Executable child issue

Each child is a narrow, end-to-end slice that one fresh context can implement and that a reviewer can demonstrate or verify independently. It always carries these headings in this order:

```
## What to build
## Acceptance criteria
## Seam contract
## Compilation hints
## Vantage point
```

### What to build

State the end-to-end behaviour the child makes real in the project's own vocabulary. Include the child's boundaries where they are needed to keep the behaviour inside the parent's scope.

### Acceptance criteria

State observable acceptance criteria complete enough for `/compile` to derive machine-checkable done criteria without inventing product intent. Each criterion describes an outcome visible at the contract's seam rather than a preferred implementation step.

### Seam contract

State the behaviour to verify and the public seam where it is observed. Prefer the highest stable existing seam that expresses the behaviour. Where the slice must introduce a seam, state the new Interface narrowly enough that it remains smaller than the behaviour it hides.

### Compilation hints

Name durable areas, stable symbols, and exemplar patterns that orient fresh codebase recon. A hint directs inspection; it does not claim an exact file list or prescribe a compiled implementation plan.

### Vantage point

Name the publication commit against which the child was written. A later compiler uses it to identify drift before it turns the durable hints into current paths, excerpts, and commands.

## Parentage and blockers

The child's native parent relation points to the decision issue, and its native dependency relations state every blocker. Where the tracker does not expose one of those relations, a line opening `Parent` or `Blocked by` carries the same information in the body. `None` is an explicit blocker value and means the child can enter the first frontier.

Native relations remain authoritative wherever the tracker provides them. The textual forms are fallbacks for a tracker without those relations, not duplicate scheduling state beside relations that already exist.

## Solo Ticket declaration

A child whose subject rewrites or newly enforces a repository-wide invariant carries a line opening exactly `Builds alone`. Every other child omits the declaration. The line records a scheduling constraint and does not relax the child's scope, acceptance, seam, or single-context bound.

## Lifecycle

The decision issue remains open while any child is live. A child reaches a final disposition when it is landed or explicitly abandoned as `wontfix`; a parked, blocked, or merely closed child without that disposition remains unresolved for this contract.

`/land` may close the decision issue only after every child is landed or explicitly abandoned and every knowledge entry has been reconciled against the implementation. Reconciliation checks the durable knowledge at each carried address, corrects or replaces anything the implementation disproved, and records the resulting disposition before the manifest is retired with the parent.

The parent, its approved snapshot, and its knowledge manifest therefore survive partial publication, execution, and interruption. Closure is the one boundary at which all executable work has a final disposition and every durable claim written during framing agrees with what landed.
