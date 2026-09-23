Three native /write cases ran sequentially with one writer task (/root/build_391_retry/native_391) and a fresh, history-free checker for each. Capacity prevented fresh writers. All used the exact immutable staged Skill; parent records the wording-only delta to final implementation.

- file-success: completed report-file comparison, no findings, unchanged response draft.
- denied-write: controlled Harness policy denial; complete 321-word reply saved/read by writer; no findings, unchanged response draft. This does not establish OS/provider refusal behaviour.
- interrupted: READY followed by native interrupt; state interrupted before and after cleanup; no report or completed comparison; draft preserved as not source-checked, delivery stopped.

Per-case paths in runs/ contain invocation, initial draft, checker task and spawn prompt, reports/replies or their observed absence, final response, validation/status, lifecycle, event transcription and filtered process snapshots. No report-path polling or shell waiter was launched. All writer-launched commands were synchronous and completed. Completed checkers were not reactivated; interrupted checker was not resumed.

Limitations: events are contemporaneous transcriptions when native outputs could not be exported directly; checker-internal tool traces are not available here. File-success shim stdout was not exported at execution time (see its explicit limitation file); language result was retained/exported. The interruption checker announced entering its requested bounded hold, while exact inner wait result is not available to this task. No claims are made beyond these observations.
