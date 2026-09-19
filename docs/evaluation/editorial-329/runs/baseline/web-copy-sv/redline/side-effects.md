# Observed filesystem effects — O1 fails

The correction's bare `uv run` language resolution leaves 125 Skill-triggered scratch entries: UV environments/cache with PyYAML and a temporary lock. These are the same defect as #340. Input, installed resources and work tree are unchanged. The other 317 created entries are native Codex private-home bootstrap/plugin/session/database/lock artifacts. The sole changed file is its config.toml project-trust update; the non-secret resulting config is preserved. Authentication did not change.

Full inventories and filesystem-changes.json enumerate every path. Both parent and fresh correction turn contexts expose gpt-6-astra/high. The correction response is preserved separately; it is not falsely labelled a delivered final artifact. Evaluator cleanup follows observation of the failed O1 state and cannot retroactively make O1 pass.
