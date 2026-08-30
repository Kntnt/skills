# Model Selector is model-invoked at dependent Interfaces

Delegation and Orchestrate must route execution before they spawn it and may observe an externally judged attempt afterward. Both declare Model Selector as a Skill Dependency, but Model Selector was user-invoked only. A dependent instruction could therefore name its public `route` Interface while Codex omitted the Skill from model context and reported that no slash command or tool endpoint existed. The dependency was on disk and still unreachable by its callers.

**Model Selector is model-invoked only when another Skill requires its public `route` or `observe` Interface.** Its description is the complete trigger and excludes recommendations, setup, configuration, comparison, capture, evidence updates, recording, and status; those remain explicit user invocations. `record` remains user-only, so routed work still cannot import its own observation artifact (ADR-0089).

**A persisted cross-Harness instruction names each Harness's invocation syntax.** Codex uses `$model-selector`; Claude uses `/model-selector`. Neither spelling denotes a tool endpoint, and endpoint discovery is not an availability check for a Skill Dependency. Making the dependency model-invoked is what puts its description in model context so the caller can follow its `SKILL.md`.

This spends the standing context of one narrow description. In return the public Interfaces ADR-0083 assigned to Model Selector are reachable by the Skills that depend on them, without copying routing or observation mechanics into every project's always-loaded delegation instruction.
