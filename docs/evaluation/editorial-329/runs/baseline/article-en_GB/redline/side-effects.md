# Observed filesystem effects — O1 fails

The source artifact, complete working copy and installed resources are unchanged. However, the correction agent ran the language resolver with bare `uv run`, leaving **125 new scratch entries**: UV's cache/environment with PyYAML and `scratch/tmp/uv-81b8e87d6827e8eb.lock`. These are Skill-triggered dependency files, not Harness logs. They were still present after the final response. The parent's immediate `scratch.iterdir()` listing could not establish cleanliness inside pre-existing scratch subdirectories. This is the protocol's incorrect-side-effect rejection, filed as #340.

The other 315 new entries are native Codex private-home bootstrap/cache/session/database/lock files and directories. Its sole changed file is private config.toml, adding project trust; harness-config-after.toml preserves that non-secret configuration. Authentication did not change. Every new path is enumerated in filesystem-changes.json, with full before/after inventories. The additional native rollout belongs to the fresh correction agent and verifies gpt-6-astra/high inheritance.

The evaluator removed the private root only after capturing this failed state. Evaluator cleanup does not retroactively turn O1 into a pass. This run's preserved input, response, correction-agent-response, native sessions, logs and inventories are external evaluator captures.
