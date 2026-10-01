# Service interruptions

Cell 04's first Write judge A invocation ended with native `Selected model is at capacity. Please try a different model.` and `turn.failed`, return code 1, after 641.59 seconds. It had already written judgement.md, but the whole invocation is void; no judgement from it counts. Raw parent/session/capture/inventory evidence is preserved under voids/item-04-composition-reader-a-attempt-1. A fresh independent invocation uses the identical neutral packet, brief, criteria and inherited seat, without the void report or error being shown to it.

The evaluator coordinator PID 46069 was temporarily SIGSTOP'd to reserve a native slot for recovery while keeping at most two active invocations. Already-running native sessions continue unaffected. It must be SIGCONT'd after cell 04 recovery, and it remains registered for cleanup. No plan, corpus, source, product or seat changed.
