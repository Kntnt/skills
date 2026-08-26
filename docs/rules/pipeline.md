# Rules — shared pipeline Interfaces

Read before changing how `/compile`, `/dispatch`, or `/land` selects tickets, before changing what makes a compiled plan fresh, and before changing who owns seam tests between compilation and landing.

This module carries the promises that several pipeline Skills must state uniformly. It does not specify one Skill's private procedure, which belongs in that Skill's shipped documents, and it does not duplicate the runtime bundle contract in the Collection Library.

## Ticket selection

Pipeline Formal Invocations select tickets with positional references written exactly as `#<ticket>`. A reference names one issue number in the current repository. Qualified cross-repository references, parent decision issues, ranges, bare numbers, and free text are not ticket operands.

Where explicit references are present, they are the complete selection and explicit references preserve the order written. Naming the tickets is the confirmation, so the Skill starts without asking a second question.

Where no reference is present, each Skill computes every ticket eligible under its own Interface, renders the complete selection, and asks one yes-or-no question before doing work. Bare selection is ordered by ascending issue number; that order makes reporting and shared serial allocation deterministic without claiming to be an execution schedule.

`--yes` is the unattended answer to the bare selection's one question. It answers yes without asking and changes no eligibility, validation, freshness, blocker, or scope rule. With explicit references there is no question for `--yes` to answer, so the flag has no work and is refused rather than ignored.

Each Skill states its eligibility separately because their gates differ. `/compile` may accept a blocked executable child; `/dispatch` requires every blocker landed and a fresh accepted compiled plan; `/land` selects work that has landed but whose tracker and knowledge closure remain incomplete. None of those differences changes the shared operand grammar or confirmation rule.

## Compiled-plan freshness

The installed runtime Interface is [`skills/kntnt/library/references/compiled-plan.md`](../../skills/kntnt/library/references/compiled-plan.md). `/compile` writes that complete bundle and `/dispatch` consumes it; neither Skill restates a competing bundle format in its own references.

A fresh accepted compiled plan binds repository identity, integration branch, full HEAD, the complete child source, the relevant parent source, and the complete bundle contents. A mismatch makes the plan stale and ineligible for execution. Stale plans are replaced from current inputs, never repaired or reconciled in place.

Freshness is checked again at the handoff that relies on it. Compilation verifies the captured Git and tracker sources immediately before acceptance; dispatch verifies them and the local bundle immediately before execution. A changed blocker state does not make an otherwise stale plan fresh.

## Compiler-owned seam tests

`/compile` authors finished seam tests before execution and records their exact destination and blob identities in the accepted bundle. The tests express the approved seam contract and may not widen product intent that the durable child and parent established.

The executor never owns compiler-owned seam tests and may not change, replace, delete, or relocate them. `/dispatch` materialises their accepted bytes, verifies them again after execution, rejects an execution result whose tests differ, and lands those exact bytes as permanent regression tests beside an approved implementation.

Read-only filesystem permissions are a guardrail rather than the proof of ownership. Test integrity is decided by comparing the materialised files with the canonical bundle, and scope integrity is decided separately by comparing every changed path with the exact footprint.
