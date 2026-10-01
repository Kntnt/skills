# Service interruptions

Cell 04's first Write judge A invocation ended with native `Selected model is at capacity. Please try a different model.` and `turn.failed`, return code 1, after 641.59 seconds. It had already written judgement.md, but the whole invocation is void; no judgement from it counts. Raw parent/session/capture/inventory evidence is preserved under voids/item-04-composition-reader-a-attempt-1. A fresh independent invocation uses the identical neutral packet, brief, criteria and inherited seat, without the void report or error being shown to it.

The evaluator coordinator PID 46069 was temporarily SIGSTOP'd to reserve a native slot for recovery while keeping at most two active invocations. Already-running native sessions continue unaffected. It must be SIGCONT'd after cell 04 recovery, and it remains registered for cleanup. No plan, corpus, source, product or seat changed.

The fresh replacement A completed with return code 0, full native task completion and no service error. The remaining Write judge and both Redline judges also completed. The raw cell-04 error marker is retained beside the recovery completion marker; it does not describe the final cell as incomplete.

The recovery script's last line used numeric signal 18, which on this platform is SIGTSTP, so its printed claim that the coordinator resumed was false. The evaluator immediately checked the process state, verified PID 46069 still named the owned coordinator, and sent Python's symbolic `signal.SIGCONT` (19). The subsequent process state was running. This operational correction changed no invocation, input, judgement or product; the observed recovery source and its stdout are preserved rather than silently corrected.

Cell 06 composition attempt 1 reached the unchanged 1800-second deadline before delivery; returncode -15, timed_out true, partial parent and two source-checker traces retained as void. Fresh unchanged-input/seat attempts 2 and, only if infrastructure-interrupted, 3 remain within the frozen allowance. No timeout increase or product change. Operational recovery script preserved.

Cell 07 composition attempt 1 also reached the unchanged 1800-second deadline before delivery (returncode -15, timed_out true); complete partial parent/children and temporary versions preserved as void. First allowed fresh replacement retains input, product, seat and 1800 seconds.
