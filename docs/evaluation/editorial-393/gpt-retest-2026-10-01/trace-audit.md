# Native trace audit

Semantic verdicts are kept separately. This audit credits actual tool calls, their returned material, externally captured file versions and filesystem inventories. A path mentioned in an encrypted dispatch is not credited as a full brief. Every file below refers to the retained evidence directory for that invocation.

## First four substantive Redline invocations

| Run | Duration (seconds) | Parent and children | Delivered artifact SHA-256 | Source/install changed | Final project writes |
| --- | ---: | --- | --- | --- | --- |
| r01 | 938.29 | parent, correction, mechanical, reply checker | `ab58b8989e2ef242d1cd3e9a1ad1d8e41677ba7f191b9652d7f2f42fb7fc217b` | neither | none |
| r02 | 1160.44 | parent, correction, mechanical, reply checker | `95271e0db4b4d690c502aaa775528f61daa0773da92b86f5faea6bb9511c5353` | neither | none |
| c03 | 1602.20 | parent, correction, mechanical, reply checker | `7749177b1bef16949d4b8e9272ad00da0e2a3c44d617adba4acdf2087fbc51f7` | neither | none |
| c04 | 1454.41 | parent, correction, mechanical, reply checker | `3472f9e7a77e1fc479bcb6c970247bc452ac6c05814b57c8c9fddb33f9047cc7` | neither | none |

All recorded contexts of these four parents and twelve children name `gpt-6.1-sol/xhigh`. Every one has native `task_started` and `task_complete` events. Their retained event streams and native rollouts contain no structured service error or failed-turn event. `deterministic-facts.json` gives the exact identities; `trace-index.json` supplies session paths, UTC timestamps and call ordinals.

In each run the external observer captured separate complete `mechanical-input.md` and `mechanical-output.md` files whose SHA-256 digests both match the actual response artifact. The mechanical child opened the input, executed the installed Proofread shim and mechanics resolver, and produced the distinct output. The parent read that complete output, checked the input digest and removed its private mechanical directory. These are observed no-mechanical-change closing passes, after one substantive correction round. The explicit parent spawn calls show `fork_turns: none`, without model/effort overrides.

Some initial shell tool submissions contained `rm -rf` in their temporary-directory traps and were rejected by the harness before execution. The retained follow-up uses Python cleanup or another permitted command and continues the same operation. Such a rejected command is not a second completed Proofread pass. The separate input/output bytes, successful shim response and child lifecycle are what establish the one completed pass, rather than counting submitted command strings.

Actual parent calls name the selected case-study resource, its review extension, base and base-review, anti-slop, web-craft and its review extension, article-anatomy and its review extension, and headlines and its review extension. The language resolver's successful JSON response includes the Swedish composition, review and anti-slop scopes themselves; merely finding no separate `cat sv.md` is therefore not evidence of a missing language load. Mechanical children separately receive the mechanics scope and read shared mechanics. Where a combined tool response was truncated, later individual/range reads are inspected against that gap rather than assuming the initial response was complete.

The full correction and reply-check dispatch messages are encrypted in native `spawn_agent` arguments. Fresh-child identity and subsequent actual resource/file reads are visible, but the complete filled-in dispatch brief cannot be recovered from those arguments. Any R2 line requiring that whole brief is `skipped` with this gap; it is not an inferred pass. The trace index retains both the encrypted call pointer and every later plaintext file-read call.

## Interrupted and refused evidence

The first corrected Write (`w01`) reached two source comparisons but the runner terminated it after 1800.24 seconds, returning `-15` with `timed_out: true`. It is an instrumentally interrupted attempt, not a completed Write or a fidelity-gate refusal. Its parent and two comparison children, partial draft, full retained comparison reports, first dispositions and transient versions are preserved. Its private root was removed only after that preservation and after checking its native process group was absent. The same intended repetition is commissioned again as `w01-rerun` under the frozen longer timeout.

The original invalid Write invocation (`r15`) and historical-artifact invocations (`r03`–`r06`) refused before editorial work because `case-study` is not installed in today's product. They are construction refusals, kept apart from the substantive matrix. [The disposition](construction-disposition.md) distinguishes actual refusals, unsent original rows and the corrected invocations on unchanged material.
