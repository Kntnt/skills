# Delegation mode

Orchestrate; subagents execute. Explicit user choices win.

Keep understanding, diagnosis, decisions, planning, briefs, verification, and the final answer on the main seat. Pure execution with large output runs detached from the conversation, writing to disk; read only the report, search the rest, and stop it or name it as left standing. Judgment inside noisy data goes to a subagent for a bounded, task-shaped report; a small bounded command stays on the main seat, narrowed at the source. Between subagent and main seat, delegate when handoff costs less than direct work; when unsure, delegate. For predictably noisy reads, narrow first and delegate before raw output enters main context.

A spawn you run on the frozen main seat with no model, deliberation, or surface override is not routed, and neither is verdict authority; a spawn onto any foreign surface, model, or deliberation override routes the full execution brief, user overrides, and checker or failure signal through Model Selector before spawning: `$model-selector route` in Codex; `/model-selector route` in Claude. Follow its decision exactly without changing the main seat. For cheap judgment-in-noise roles — distillation, summarization, evidence collection — still consider a routed cheaper seat rather than defaulting to the frictionless main seat. Verify results independently.

If subagents are unavailable, execute normally. After an externally judged routed attempt, use `$model-selector observe` in Codex or `/model-selector observe` in Claude and leave its artifact in caller-owned scratch. An unrouted spawn is never handed to `observe`; where capture is enabled, capture records it as the inheritance that actually happened. Model Selector's `record` command remains user-only.
