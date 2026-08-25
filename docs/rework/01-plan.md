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

Work with the existing tools (the current grilling/to-tickets chain), since the new pipeline does not exist yet. The order matters: recon before questions, so Thomas is never asked anything the pile itself can answer.

1. **Triage sweep (recon).** Read every file in `docs/adr/` (fan out read-only subagents if useful) and classify each provisionally per the brief's triage rule: rules-doc line, consolidation candidate, delete, or move-to-standard. Also inventory where else instructions live (the coding standards, the files AGENTS.md references). Produce a classification table with a one-line justification per ADR.
2. **One decision round with Thomas.** Present the table and a concrete proposal — where the rules doc lives given the existing conventions, which consolidation ADRs to write (named), what moves where — as numbered owner-perspective questions, each with a recommended answer (grilling style, tldr register). The brief's open decisions are settled here, informed by the recon, never before it.
3. **Tickets.** Break the approved reform into tickets on the milestone with the existing to-tickets skill, explicitly instructing it to label `rework` + `rework-ready-for-agent` (never plain `ready-for-agent`). Expected slices: the rules document, each consolidation ADR, the standard moves, the deletion sweep.
4. **Execute** the tickets on this branch. Thomas's checkpoints in this phase are exactly two: the decision round (step 2) and the ticket breakdown (step 3).

Ticket-writing note: ADRs 0067 and 0099 govern how tickets are written in this repo — check during triage whether they remain binding, since the rebuild's own tickets are subject to them.

## Phase 2 — the five skills

Build in pipeline order — frame, to-slices, compile, dispatch, land — because each is useful standalone the day it lands, with the old tools filling the rest of the chain: frame alone replaces the grill-with-docs pain immediately; frame + to-slices + manual implementation works before dispatch exists; compile precedes dispatch because the plan format is dispatch's input contract. Each skill goes through its own mini-cycle: (1) draft a design brief in this directory from the skill's section in `00-brief.md`, resolving what you can from the codebase and the existing skills it borrows from (tldr, delegation, model-selector, orchestrate's rescued ideas); (2) one grilling round with Thomas on owner-level residuals only — behaviour, interface, defaults he must live with — each question with a recommended answer; (3) his approval of the brief and the ticket breakdown; (4) tickets on the milestone, same label instruction as phase 1; (5) implementation on this branch. Follow `docs/coding-standard/skills.md` for what a skill ships. Shared assets (the selection grammar, references both /dispatch and others read) are specified in the first design brief that needs them, not planned upfront.

## Phase 3 — bootstrap, takeover, cleanup

Once compile + dispatch work, the remaining tickets (land, polish, orchestrate deletion, this directory's deletion) are executed by dispatch itself — the pipeline's first real batch is its own completion. That batch must include `--at-once=2`, at least one merge conflict, and one pause-and-resume; surviving it is the acceptance test that permits orchestrate's deletion. Then the takeover merge and the final cleanup ticket, both specified in the brief's endgame section. Both the first dispatch batch and the takeover merge run only on Thomas's explicit go.
