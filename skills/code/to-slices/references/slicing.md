# Slicing judgement

Read this reference while turning a complete Frame Record into one approved graph. The durable shapes themselves live in `$LIBRARY/references/slices.md`; this file governs the judgement that decides what belongs in each shape.

## Tracer bullets

**Tracer bullets are the normal form.** Each child delivers a thin end-to-end behaviour that a reviewer can demonstrate or verify independently. Size it for one fresh context, not a file count or estimate in human days. A database-only, API-only, UI-only, or test-only task joins the first behaviour that needs it unless that layer is itself an observable contract or an expand step.

Choose the highest stable public seam that expresses the delivered behaviour. A seam contract states the behaviour and where it is observed; it does not prescribe the internal arrangement. Where a slice introduces a seam, keep the new Interface narrower than the complexity it hides.

## Blocking

An edge exists only when the downstream child cannot be implemented or verified honestly before the upstream child lands. Preferred order, presentation order, shared files, and anticipated merge conflicts create no semantic blocker. The approved snapshot preserves what the owner accepted; native tracker relations remain the live graph.

## Expand–contract

**Expand–contract keeps every intermediate tip green.** Expand introduces the new form beside the old. Migration children move bounded parts of the blast radius while both forms coexist, each sized for one fresh context. Contract removes the old form after every migration. Each migration is blocked by expand; contract is blocked by every migration.

Do not use expand–contract to excuse a horizontal preparation ticket. The expand child must itself deliver the compatible new contract that its migration children can consume and verify.

## Experiments

An experiment is a child whose delivered outcome is a decision. Carry the question, the bounded experiment, its observation seam, and the decision rule that turns the result into an answer. Every child whose honest contract depends on that answer is blocked by the experiment; unaffected work stays unblocked.

## Solo Tickets

A child whose subject rewrites or newly enforces a repository-wide invariant carries a line opening exactly `Builds alone`. Every other child omits it. Touching many files is not enough; the declaration belongs to a rule that governs files sibling work may not have written yet.

## Review

Before previewing the graph, inspect every child against these questions:

- Does it deliver or decide something independently observable?
- Does it fit one fresh context without deferring a hidden horizontal layer?
- Does its seam describe behaviour through a stable public boundary?
- Does every blocker express necessity rather than preference or collision avoidance?
- Does every open experiment carry an observation seam and decision rule?
- Does `Builds alone` appear exactly where the repository-wide-invariant rule requires it?
