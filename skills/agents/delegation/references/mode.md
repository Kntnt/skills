# Delegation mode

Orchestrate; subagents execute. Explicit user choices about delegation, execution, model, or effort win.

Keep understanding, diagnosis, decisions, planning, briefs, verification, and the final answer on the main seat. Delegate when handoff costs less than direct work; when unsure, delegate. For predictably noisy reads, narrow first and delegate before raw output enters main context, requesting only a bounded, task-shaped report.

Before spawning, send the full execution brief, user overrides, and checker or failure signal through `/model-selector route`. Follow its decision exactly without changing the main seat. Verify results independently.

If subagents are unavailable, execute normally. After an externally judged routed attempt, use `/model-selector observe` and leave its artifact in caller-owned scratch. `/model-selector record` remains user-only.
