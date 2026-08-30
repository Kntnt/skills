# Delegation mode

Orchestrate; subagents execute. Explicit user choices win.

Keep understanding, diagnosis, decisions, planning, briefs, verification, and the final answer on the main seat. Delegate when handoff costs less than direct work; when unsure, delegate. For predictably noisy reads, narrow first and delegate before raw output enters main context, requesting only a bounded, task-shaped report.

Before spawning, route the full execution brief, user overrides, and checker or failure signal through Model Selector: `$model-selector route` in Codex; `/model-selector route` in Claude. Follow its decision exactly without changing the main seat. Verify results independently.

If subagents are unavailable, execute normally. After an externally judged routed attempt, use `$model-selector observe` in Codex or `/model-selector observe` in Claude and leave its artifact in caller-owned scratch. Model Selector's `record` command remains user-only.
