# Rework plan — phases and status

> Companion to `00-brief.md`; read that first. This file is the living status record — update the table as phases progress. Deleted with the rest of `docs/rework/` by the final cleanup ticket.

## Status

| Phase | Title | Status | Notes |
|-------|-------|--------|-------|
| 0 | Establish the track | DONE (2026-08-25) | Worktree `../skills-rework` + branch `rework`; AGENTS.md protection section on `main` and (extended) here; labels `rework`, `rework-ready-for-agent`; milestone "Skills 2.0"; this dossier |
| 1 | Doc reform | TODO | ADR triage → living rules doc + consolidation ADRs; must precede phase 2 |
| 2 | Build the five skills | TODO | Pipeline order: frame → to-slices → compile → dispatch → land |
| 3 | Bootstrap, takeover, cleanup | TODO | Dispatch executes its own remaining tickets; acceptance test; takeover merge; final cleanup ticket |

## Phase 1 — doc reform

Work with the existing tools (the current grilling/to-tickets chain), since the new pipeline does not exist yet. First settle the open decisions with Thomas (listed at the end of the brief's doc-reform section), then break the reform into tickets on the milestone: the triage sweep over `docs/adr/`, the living rules document, the consolidation ADRs, the moves into the coding standard, the deletions. Ticket-writing note: ADRs 0067 and 0099 govern how tickets are written in this repo — check during triage whether they remain binding, since the rebuild's own tickets are subject to them.

## Phase 2 — the five skills

Build in pipeline order — frame, to-slices, compile, dispatch, land — because each is useful standalone the day it lands, with the old tools filling the rest of the chain: frame alone replaces the grill-with-docs pain immediately; frame + to-slices + manual implementation works before dispatch exists; compile precedes dispatch because the plan format is dispatch's input contract. Each skill goes through its own mini-cycle: design brief in this directory, Thomas's approval, tickets on the milestone, implementation on this branch. Follow `docs/coding-standard/skills.md` for what a skill ships.

## Phase 3 — bootstrap, takeover, cleanup

Once compile + dispatch work, the remaining tickets (land, polish, orchestrate deletion, this directory's deletion) are executed by dispatch itself — the pipeline's first real batch is its own completion. That batch must include `--at-once=2`, at least one merge conflict, and one pause-and-resume; surviving it is the acceptance test that permits orchestrate's deletion. Then the takeover merge and the final cleanup ticket, both specified in the brief's endgame section.
