# Final mechanical transport: two fixed controls

- **record** — `redline-gpt-2026-09-20-359-final-mechanical-controls`
- **date** — 2026-09-20 (native UTC)
- **tickets** — [#359](https://github.com/Kntnt/skills/issues/359), #329
- **skill** — redline
- **provider/model** — gpt / gpt-6-astra, high, verified in every native turn context
- **harness** — Codex CLI 0.155.1
- **corpus** — bf14dc2; exact preserved-output controls with hashes and native provenance in `../editorial-329/followup/fixtures/final-mechanical-provenance.json`
- **product** — 5ecadb76
- **matrix** — `../editorial-329/followup/matrix-final-delivery.md`
- **invocation for both rows** — `/redline --output=response input.md`
- **contextual instructions** — none; fresh isolated native runs, no retries
- **output target** — response

The record was opened when the two invocations started and completed after independent output and native-trace inspection. Both fixed controls pass. They demonstrate the declared no-change and mechanical-correction file boundaries, not a general guarantee or the cause of the earlier corruption.

Evidence: `../editorial-329/followup/runs/final-mechanical-controls/`, including exact inputs, prompts, executed helper, argv, complete native traces, extracted visible commands, actual mechanical results, audits and cleanup receipts.

## Shared applicable assessments

G1/G2, P1/W1, L1/L2 and R1 pass in both rows: the customer case, agency, quoted meaning/voice, measurement population, assignment/completion distinction and causal reservation survive. The corrected idiomatic Swedish quotation remains unchanged. T1 passes: genre/language inferred using the allowed resource openings and resolved guidance; no technique applies. T2 is skipped. Source-aware F1 and Write-only S1 are not scored for source-blind Redline.

R2 passes: each run reads the installed Redline and Proofread instructions and invokes Proofread's formal shim exactly once with resolved Swedish, a private complete input and distinct result file. No broad mechanics pass or extra quotation reader is delegated. The clean run follows Proofread in the parent; the erroneous run delegates the installed Skill to one fresh inherited seat with `fork_turns=none`, no model or effort override. In both, exact input transfer, full mechanical input reading, separate complete result writing, full final-result reading and unchanged-input verification are directly visible. The erroneous run's dispatch text is encrypted, but its exact formal invocation and complete input/output file reads independently establish the actual artifact boundary; no hidden passed prose is assumed.

O1 passes: both private input/result directories are removed before return, original input/authentication remain unchanged, and before/after inventories contain no surviving non-home Skill artifact. Harness private-home/cache effects are retained separately in the inventories. Both isolated roots were removed after evidence capture using literal full paths. Registered batch PID 39635 and its child runners ended.

## mechanical-clean

- **fixture** — final-mechanical-clean.md, exact accepted artifact extracted from the earlier visible correction/re-reader trace; SHA-256 `bc4b6530abc815b30efb4a14db7181ccfefffda70049acaf7a124ddfa3d21e6e`
- **observed delivery** — correct short Swedish no-change status; no repeated artifact and no claimed unresolved condition
- **side effects** — private mechanical input and result created and removed; source unchanged, no surviving Skill files
- **criteria** — all applicable shared criteria pass as above; exact result is byte-identical to the complete frozen input, including its terminal newline
- **unresolved findings** — none
- **defects filed** — existing #359; no new defect
- **notes** — 83.20 native seconds. The complete result is written even for no-change, printed in full, checked against the input and removed. Preserved as `mechanical-clean/redline/mechanical-result.md`. No purported final artifact has to be reconstructed from a child no-change message.

## mechanical-error

- **fixture** — final-mechanical-error.md, exact typo-bearing earlier delivered artifact; SHA-256 `4c35cf893a1f39d6bff978a355ac88db6ad4badaa0448c6cd7c46beac7e3c918`
- **observed delivery** — complete corrected artifact, no extra account or unresolved findings
- **side effects** — private input/result created and removed; source unchanged, no surviving Skill files
- **criteria** — all applicable shared criteria pass; only `arbetsbelastningning` becomes `arbetsbelastning`. Every other byte remains unchanged. The final response is byte-identical to the complete mechanical result, with no newline normalization required.
- **unresolved findings** — none
- **defects filed** — existing #359; no new defect
- **notes** — 135.77 native seconds. The actual fresh Proofread child reads the complete erroneous artifact, writes its complete correction to the separate destination, and the parent verifies unchanged input and reads that full result before cleanup. Preserved as `mechanical-error/redline/mechanical-result.md`, SHA-256 `5bc650b954ce101200b81627581a7aeb6c6c3e1748bf0e7427572ac5e90efac9`.

Aggregate native time: 218.97 seconds, not elapsed batch wall time. No runner failure or timeout; neither case was retried. Other paired/replay verification at 5ecadb76 remains separate evidence.
