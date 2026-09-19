# Observed filesystem effects

No Skill-created path remains. The complete working copy, source.md, installed instruction copies, export and separate scratch tree are unchanged. Both UV commands used Python TemporaryDirectory; their directories were removed. The first shell cleanup command was rejected before execution, then replaced with working Python cleanup.

All 316 created entries belong to the private Codex home: native system skills/plugin bootstrap, cache, sqlite/WAL files, session records, locks and shell snapshots. The sole changed file is the private config.toml, where the Harness recorded this private project's trusted status; harness-config-after.toml shows the complete non-secret result. Authentication is unchanged. filesystem-changes.json enumerates every entry, including directories, and both inventories retain hashes and modes.

The response/draft, logs, inventories and other files under this evaluator-owned run directory are evaluator captures, outside the model-writable roots. They are declared deliverables, not Skill files.
