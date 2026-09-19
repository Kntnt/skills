Read when preparing or implementing the first Frame delivery on main.

# Frame implementation handoff

Implement the first delivery in [the engineering workflow plan](../docs/plans/engineering-workflow.md). Read that plan and the current `AGENTS.md` first. The plan owns direction, status, the source addresses, and open owner decisions; this handoff scopes the next implementation session.

## Start from the existing implementation

Work from the main checkout at `/Users/thomas/Projects/skills`, or an ordinary implementation branch/worktree based on main. Read rework source through `git show`; the protected rework checkout is not the implementation workspace.

Read `4dbe937:docs/rework/04-frame.md`, `4dbe937:skills/code/frame/` and its references, `4dbe937:skills/kntnt/library/references/frame-record.md`, and `4dbe937:tests/test_frame.py`. The import's source implementation commit is `c7393f1`; the roadmap names its related changes. Treat old invocation, routing, handoff, and resource assumptions as source material to adapt.

Inspect today's applicable rules through `AGENTS.md`, especially Skill form, routing, documentation, tickets, and `CONTRIBUTING.md`. Use the required authoring skills when writing shipped instructions. Inspect existing tickets to avoid duplicating work; create ordinary main-track implementation tickets that cite the rework source, and implement through that track. Closed rework tickets stay historical.

Done when the implementation scope and tickets identify the current contracts and source material without importing the old pipeline wholesale.

## Resolve the remaining owner choice

Early in the session, read the plan's glossary decision and ask Thomas for the preferred name and location if it is still unresolved. Clarify whether he wants only Frame's default changed or this collection's current glossary migrated too. Present consequences for finding and maintaining domain knowledge, not parser or file-handling details. Continue independent adaptation work while awaiting the answer.

If a convention is chosen, record it in the plan and implementation ticket before dependent edits. Trace active references and the temporary downstream consumers. Preserve target-project overrides, update readers with any agreed migration, and keep historical documents intact. User-global skill installations and configuration are outside this repository delivery.

Done when the agreed convention and migration scope are explicit and the transitional workflow can find the glossary.

## Deliver a usable first step

- Preserve Frame's parallel investigation and attended interview, with questions aimed at Thomas as requirements owner and expert on user roles. Let the agent choose ordinary reversible technical details within agreed constraints, including when several reasonable choices exist. Report material choices briefly.
- Preserve incremental saving, resume, recorded evidence, owner decisions, agent decisions, open experiments, and the record of glossary/decision documents written. Apply the chosen glossary convention without making Frame depend on external interviewing or domain-documentation Skills.
- Replace the retired Model Selector invocation and frozen routing snapshot with the current public interface and evidence rules. Main-seat work, routed work, and measurements follow today's contracts; copy no retired routing subsystem.
- Use today's invocation shim, help and argument conventions, dependency declarations, Codex sidecar, README entry, and generated Catalog. Bring over only shared resources the first delivery needs, adapting their lifecycle claims to consumers that actually exist.
- Make the result usable by the existing `to-spec` and `to-tickets` in the same session. Carry the decisions and record forward explicitly and define what happens to the saved record during this transitional period. Do not emit a next command for the unavailable `to-slices` or invoke user-only successors automatically.
- Keep Orchestrate as the executor. Compile, Dispatch, and Land are later evaluation work rather than dependencies of this delivery.

Done when Frame can be used immediately in the transitional workflow and its own execution needs no Matt Pocock Skill.

## Verify and hand back

Run the checks required by `CONTRIBUTING.md`, including Catalog regeneration and the new-Skill validator comparison. Adapt the relevant source tests to the new contract rather than preserving obsolete wording.

Exercise the important behaviours: a simple task with no unnecessary questions; an owner choice about different user roles; a fact discoverable in the repository; a reversible technical choice; interrupted framing and resume; a project-defined glossary path and the agreed fallback; and the handoff to the currently available planning tools. Distinguish behavioural evidence from static instruction checks, and report what was actually exercised.

Update the roadmap with the resulting tickets, commits, validation, remaining work, and the next step. Report a concise owner-facing outcome. Complete the repository delivery before proposing any global installation change; runtime installation is a separate action unless Thomas requests it.

Done when the implementation and required checks are complete, the roadmap states the actual result, and the next session can continue without this conversation.
