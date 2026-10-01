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

## Two ellipsis invocations and resource-volume evidence

`c05` completed in 1699.20 seconds and delivered artifact `377fc879799b305c36eb98d4550a462ccfcd8d47f7997acbc0de09aec1dde6f0`. `c06` completed in 1463.20 seconds and delivered `68817c49ce27cd806a3b13b9b801fa27390ad8fb49b3d4b48ca593fad6aead98`. Each has the parent, one fresh correction child, one mechanical child and one reply checker, all with completed native lifecycles and the inherited seat. Neither has a structured service interruption. Both have separate captured mechanical input/output matching their delivered artifact, unchanged sources/install and no final work/scratch changes. Their semantic outcomes are left to the frozen criteria and blind judgements.

`resource-evidence.json` uses complete returned tool material, not command names, to identify exact committed resource content and successful resolver scope content. It unwraps complete JSON lines inside batched native outputs; a truncated later entry does not erase an earlier complete returned entry, while an incomplete entry is never credited. All six parents have complete returned content for the eleven mandatory selected editorial resources and all three Swedish review language scopes. Correction/mechanical coverage is listed separately by session; any uncredited child resource or dispatch portion requires its own trace inspection rather than a presumed absence. The returned-volume totals are lower bounds, exclude repeated copies in the same session, and are not token counts or a comprehension test.

| Run | Complete returned resource/scope words across native sessions |
| --- | ---: |
| r01 | 32,379 |
| r02 | 33,878 |
| c03 | 33,731 |
| c04 | 35,054 |
| c05 | 28,836 |
| c06 | 32,627 |

[The resource-size catalogue](resource-sizes.json) gives exact frozen hashes and complete-file word counts independently of any claim that a run loaded one. Mandatory-set cost is obtained by intersecting actual native read evidence with each role's load contract; it is kept distinct from these observed-volume totals.

## Later shared checkout

At 13:38 UTC the clean shared `main` checkout had advanced to `fe2587b7`, adding #476's Redline shell/cleanup guidance and corresponding catalogue/tests. [The environment observation](environment-drift.json) preserves that exact product diff. Every invocation in this packet still exports the committed `fb169087` product and corpus. Outcomes here therefore do not evaluate the later main revision, and no new arm is inferred or commissioned by that drift.

## Interrupted and refused evidence

The first corrected Write (`w01`) reached two source comparisons but the runner terminated it after 1800.24 seconds, returning `-15` with `timed_out: true`. It is an instrumentally interrupted attempt, not a completed Write or a fidelity-gate refusal. Its parent and two comparison children, partial draft, full retained comparison reports, first dispositions and transient versions are preserved. Its private root was removed only after that preservation and after checking its native process group was absent. The same intended repetition is commissioned again as `w01-rerun` under the frozen longer timeout.

The original invalid Write invocation (`r15`) and historical-artifact invocations (`r03`–`r06`) refused before editorial work because `case-study` is not installed in today's product. They are construction refusals, kept apart from the substantive matrix. [The disposition](construction-disposition.md) distinguishes actual refusals, unsent original rows and the corrected invocations on unchanged material.

## Closing-pass and writable-root comparison

`transport-facts.json` records exact captured mechanical input and output versions, actual native returned-byte matches and every before/after inventory difference for each completed run. File names vary: some runs use `input.md` and `output.md` inside their unique mechanical directory. Mechanical input and output are distinct files even when their bytes are identical. A complete output that differs from its frozen mechanical input is valid chain transport; whether the difference is mechanical is a separate judgement. Thus c09 and r14 have different input/output hashes, while their final output hashes match their delivered artifacts.

In c08 the parent reads and validates the complete output in a submitted Python command, parses its full JSON result inside the V8 tool call, and stores the final text without echoing it into the outer tool result. The trace retains the explicit `read_text`, unchanged-input and exact-output assertions, their successful result, and subsequent delivery from that stored value; the external output file capture matches delivery exactly. An absent outer returned-byte match here is not an absent file read.

The c07 parent removed the harness-created empty `scratch/cache`, `scratch/data`, `scratch/tmp` and `scratch/uv-cache` directories. Its ordinal-196 submitted command explicitly loops over these four names and calls `rmdir`; the after inventory confirms their removal. They pre-existed the Skill run and were not its private working directories. This is an O1 incorrect-side-effect failure, separate from quotation behaviour. No source, staged install or other user file changed. The later shared-main cleanup paragraph is not used to decide this failure; the frozen product already limits cleanup to its own private working area.
