Read when preparing or implementing the first Frame delivery on main.

# Frame implementation handoff

Implement the first delivery in [the engineering workflow plan](../docs/plans/engineering-workflow.md). Read that plan and the current `AGENTS.md` first. The plan owns direction, status, source addresses, and owner decisions; this handoff scopes the next implementation session.

[Ticket #326](https://github.com/Kntnt/skills/issues/326) is the placement prerequisite: it moves this handoff to `docs/agents/frame-handoff.md` and updates its references. Follow the current `AGENTS.md` pointer to find it. Source inspection and preparation can proceed while #326 is pending; make the affected Frame implementation tickets depend on its completed migration using the tracker's dependency convention.

## Start from the existing implementation

Work from the main checkout at `/Users/thomas/Projects/skills`, or an ordinary implementation branch/worktree based on main. Read rework source through `git show`; the protected rework checkout is not the implementation workspace.

Read `4dbe937:docs/rework/04-frame.md`, `4dbe937:skills/code/frame/` and its references, `4dbe937:skills/kntnt/library/references/frame-record.md`, and `4dbe937:tests/test_frame.py`. The import's source implementation commit is `c7393f1`; the roadmap names its related changes. Treat old invocation, routing, handoff, and resource assumptions as source material to adapt.

Inspect today's applicable rules through `AGENTS.md`, especially Skill form, routing, documentation, tickets, and `CONTRIBUTING.md`. Use the required authoring skills when writing shipped instructions. Inspect existing tickets to avoid duplicating work; create ordinary main-track implementation tickets that cite the rework source, and implement through that track. Closed rework tickets stay historical.

Done when the implementation scope and tickets identify the current contracts and source material without importing the old pipeline wholesale.

## Apply the agreed glossary convention

Thomas has chosen `docs/glossary.md` to replace root `CONTEXT.md`. Apply the plan's agreed convention without reopening the filename or placement decision. This collection's migration is part of the Frame delivery, separate from #326's agent-document placement migration.

The glossary is written for people and read by agents too. It contains only term definitions, including preferred names and distinctions that establish meaning. Keep requirements, behavioural rules, implementation instructions, architecture decisions, and general background in their own documents. Preserve the meaning of existing terms; if an entry contains a rule, place that rule in the appropriate authoritative document rather than dropping it or disguising it as a definition.

Move the existing glossary and update active rules, links, examples, and readers as needed. Make `docs/glossary.md` Frame's default in a target project without an explicit convention, while preserving target-project overrides. Keep `to-spec` and `to-tickets` able to find it through project-level instructions during the transition. Historical documents and user-global installations/configuration are outside this migration.

Done when the collection uses `docs/glossary.md` as its single current glossary, the glossary contains only term definitions, and Frame and the transitional workflow find the intended glossary.

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
