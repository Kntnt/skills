# An independently maintained engineering workflow

Living plan for Thomas and agents continuing this work. Read for direction, progress, or the next step; reading it is not an instruction to start implementation.

Last updated: 2026-09-19. Initial inspection: `main` at `2d5c944`, `rework` at `4dbe937`.

## Agreed direction

Own and evolve the engineering workflow in this collection without depending on Matt Pocock's skills. Preserve the principles Thomas values: narrow vertical slices, deep modules with small interfaces, behavioural tests, explicit dependencies, and independent verification. Independence means control over the shipped instructions and their dependencies, not discarding useful ideas or attribution.

Develop incrementally on `main`. The protected `rework` branch supplies designs and implementations to inspect. Its former takeover plan is withdrawn; the branch and worktree protections in `AGENTS.md` continue to apply.

Keep two user sessions: attended planning, followed by unattended execution. Thomas owns requirements and understands the needs of different user roles. Ask him about behaviour, priorities, consequential architecture choices, and material trade-offs. Agents investigate facts and choose ordinary technical details within agreed constraints.

Orchestrate may remain the executor permanently. Replacing it is not a condition of success. Required preparation and completion belong inside the execution workflow rather than becoming commands Thomas must remember.

## Delivery sequence and status

| Step | Deliverable | Status and next action |
| --- | --- | --- |
| 0 | Move project agent documents to `docs/agents/` and make `agents-md` maintain that placement. | Done: [#326](https://github.com/Kntnt/skills/issues/326) moved this repository's agent documents to `docs/agents/`, and `agents-md` now creates them there and moves them out of the retired project directory. `CONTEXT.md` is unchanged; the glossary migration belongs to step 1. |
| 1 | An owned `frame`, adapted from rework, replacing `grill-with-docs` in this workflow and taking responsibility for its interview and domain-documentation work. | Next: frame the first delivery and file its implementation tickets on main. Source implementation exists on rework; no Frame has been added to main. Use the [Frame handoff](../agents/frame-handoff.md), now under `docs/agents/`. Apply the agreed glossary convention below. |
| 2 | An owned `to-slices`, producing the decision issue and executable child tickets together. | Planned after Frame. Replaces `to-spec` and `to-tickets`; its tickets must work with the retained executor. |
| 3 | A workflow whose direct and indirect dependencies are maintained here. | Audit incrementally during steps 1 and 2, then verify the complete chain. Cover documentation, testing guidance, setup/configuration, and runtime references; do not recreate the entire external collection. |
| 4 | Measured improvements to execution cost and elapsed time, including automatic completion. | Deferred until the planning replacement works. Start from current Orchestrate; selectively adopt useful preparation and closure ideas from rework. |

After step 1, the transitional workflow is `frame` → existing `to-spec` → existing `to-tickets`, then Orchestrate in a fresh session. Frame's own operation must be independent; those temporary downstream tools remain external until step 2. After step 2, planning is `frame` → `to-slices`, followed by Orchestrate in a fresh session.

## What already exists

The rework checkpoint contains `frame`, `to-slices`, `compile`, and `dispatch`. `land` was designed but not built, and the planned first real Dispatch acceptance batch remained outstanding. Historical test results establish the old checkpoint, not compatibility with today's main or a performance improvement.

Frame's source addresses:

- `c7393f1:skills/code/frame/` — original implementation, including help, recon and knowledge references, and the Codex sidecar.
- `54b7748:skills/kntnt/library/references/frame-record.md` — shared Frame Record format.
- `ed8eac1:skills/kntnt/library/references/tldr-mode.md` — historical communication guidance; inspect current main before deciding whether any shared resource needs bringing over.
- `7dd014a` — later change giving Frame its `to-slices` handoff. That successor is not yet available on main.
- `4dbe937:docs/rework/04-frame.md` and `4dbe937:tests/test_frame.py` — design rationale and historical tests at the preserved checkpoint.

Read a source without switching branches, for example `git show 4dbe937:skills/code/frame/SKILL.md`. Historical issue numbers and rework tickets are provenance, not executable work for the new track.

## Frame's adaptation boundary

Reuse the existing design rather than restarting the interview-method design. Adapt its routing to today's public Model Selector interface and its packaging to today's Skill conventions. Give it a truthful handoff to the transitional workflow and an explicit lifecycle for its saved record while `to-slices` does not exist here.

The interview must distinguish facts to investigate, technical choices the agent can make, and consequential decisions Thomas owns. Several acceptable technical solutions do not by themselves require an owner question. Explain owner choices through consequences for users, with a recommendation. Keep decision reporting selective so it does not become another detailed approval burden.

The first delivery covers framing, relevant glossary and decision documentation, and a resumable handoff. It does not implement the later pipeline Skills or redesign Orchestrate.

## Agreed documentation and glossary conventions

On 2026-09-19 Thomas chose `docs/agents/` for compact instructions addressed specifically to agents. Other project documentation under `docs/` is written for humans and used by agents as the same source. `AGENTS.md` stays at the root as the entry point. Ticket #326 carried out the placement migration and the corresponding Skill changes; it preserved document contents except for necessary path/link changes and changed only paths in `AGENTS.md`.

Thomas also chose `docs/glossary.md` to replace root `CONTEXT.md`, as part of the Frame delivery. It is a human-readable shared vocabulary used by people and agents, and contains only term definitions, including preferred names and distinctions needed to identify their meaning. Requirements, behavioural rules, implementation instructions, architecture decisions, and general project background belong in their respective documents, not in the glossary.

Step 1 migrates this collection's glossary and its active readers/pointers, and gives Frame `docs/glossary.md` as its default for a target project without an explicit convention. Preserve explicit target-project conventions and keep the temporary `to-spec`/`to-tickets` consumers able to find the glossary through project-level instructions. Do not alter user-global configuration as a side effect or rewrite historical decision records. The filename, placement, purpose, and inclusion of this collection's migration are settled; do not ask Thomas to approve them again.

## Questions reserved for the later execution work

The September analysis identified design issues to resolve before adopting Compile or Dispatch. These are evaluation inputs, not a commitment to ship those Skills:

- Compile only when useful and close to execution. Normal branch progress must not repeatedly require Thomas or spend a failure-retry budget.
- Review translation against the original requirements as well as checking whether a plan is self-contained. Compiler-owned tests do not establish that no requirement was omitted.
- Match preparation and verification to the task, including behaviour-preserving refactors and documentation changes.
- Keep mechanical bookkeeping in suitable tested code; moving it into model instructions does not establish a saving.
- Close tickets and reconcile relevant knowledge automatically, with resumable completion when interrupted. A standalone `land` can remain a recovery entry point if useful.

Compare complete workflows on owner attention and interruptions, elapsed time, token cost, rework, and remaining defects. A faster Dispatch phase alone is not evidence of a cheaper complete workflow. No comparative performance measurement has been made for this plan.

## Keeping the plan usable

After a delivery or an owner decision, update this document in the same change: date, status, evidence such as issue and commit, remaining decisions, and the next bounded action. Keep proposals distinct from decisions and shipped behaviour. Inspect the actual tree and relevant ticket threads before answering a status request; report a mismatch instead of treating this table as proof of completion.

Keep one current plan here. `AGENTS.md` on main points here, and rework's documentation entry points direct its readers here. From the sibling rework worktree, read `../skills/docs/plans/engineering-workflow.md`; once committed, `git show main:docs/plans/engineering-workflow.md` also works without switching branches. Locate main through `git worktree list` if its working directory has moved.

Retire the Frame handoff after step 1 is delivered, preserving the outcome here and in the ordinary implementation tickets. Later steps get their own bounded handoffs when they become current.
