# Observed filesystem effects

No Skill-created path remains. The source, complete work tree, installed resources, export and all scratch locations are unchanged. Both UV calls used private TemporaryDirectory contexts; the final tool command also checked that none remained.

All 316 created paths are native Codex bootstrap/cache/session/database/lock files or directories in its private home. Its sole changed file is config.toml, where it added the private project's trusted status; the complete non-secret result is captured. Authentication is unchanged. Both inventories and filesystem-changes.json enumerate every path with hashes/modes where applicable.

Responses, extracted artifact, logs and inventories in this run's deliverable directory are evaluator captures outside model-writable roots.
