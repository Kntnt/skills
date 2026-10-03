# Independent audit of the retained #393 measurement

Attempt `ms-20261002-fa0735`. Audited from the assigned tree on 2026-10-02, without a product invocation, new semantic judge, candidate or historical rescore. [Machine-readable receipt](packet-audit.json) and [offline audit procedure](audit-packet.txt) expose the checks; [source-integration check](integration-check.txt), [observed red](red.txt) and [green](green.txt) establish the import's red/green boundary.

## Provenance and integrity

The source diff from frozen `fb169087` to retained `4e88c6e0` adds 1,125 packet files and the two #393 protocol records. It changes no product or test. All 1,127 integrated files match their source Git blobs. The owner-decision bytes also match `ed1d8587`; that commit's 2026-10-01 11:52:27 UTC freeze precedes the first native invocation at 11:53:48 UTC. The original branch still points at the retained head, and its worktree remains present. Existing tracked product, tests, evaluation history, ADRs, changelog, record index and contributing guide match the integration base.

The 1,062 entries in the retained copy ledger independently match their sizes and SHA-256 hashes. Every counted run's complete supplied input matches the frozen source file; the three paired inputs exactly match their respective Write deliveries, metadata included. Neither Write's English source nor its reply becomes a paired Redline input. All 83 exported product files match frozen Git archive bytes in every counted before/after inventory; source/install invariants remain unchanged. All 35 entries in both records match the disposition index, targets, delivery presence, artifact digests and target-criterion accounting.

The original plan and committed construction annexes remain separate. The final observed disposition, rather than the annex's anticipated launcher boundary, supplies the count: five pre-operation refusals (`r03`–`r06`, `r15`), eight unsent original turns (`r07`–`r12`, `r16`, `r17`), and two voids (`w01`, `r13`). None is a quotation failure or a delivered draft. The timeout/capacity replacements keep the intended repetitions; there is no product-quality retry.

## Actual delivery and target counts

| Set | Runs | Actual delivery | Target result |
| --- | ---: | --- | --- |
| Swedish negatives | 6 | Six response artifacts | Two agreed repairs, three mandatory misses, one dispute |
| Positive controls | 8 | Four response artifacts and four new files | Seven target passes, one unnecessary English expansion |
| Fresh Swedish Write | 3 | Three response artifacts | Three translation passes |
| Source-blind pairs | 3 | Two response artifacts; one short status | Two target passes; one skipped text judgement |
| Total | 20 | Nineteen artifacts and one status | No whole-product acceptance |

The receipt lists every run, output target, delivered digest and disposition. Response artifacts were independently extracted from complete fences and compared byte for byte. Every file target matches captured `work/output.md`. Counted replies match their completed native parent's final message. All three Write artifacts match the last checked prose after removal of only the leading handoff metadata. All seventeen Redline runs retain distinct closing mechanical input/output paths; an actually delivered artifact matches the closing output. `p02` runs the mechanical Skill in its parent, which the contract allows.

`p03` delivered only the Swedish no-change status. Its private output and supplied input cannot establish delivered preservation. Text-dependent criteria remain skipped, while its reply and inventories can answer output, language and mandatory-finding questions. The missing artifact is allowed by [delivery.md](../../../../skills/kntnt/library/references/delivery.md) and the [evaluation protocol](../../protocol.md); it is not a product failure inferred from a judge's delivery label.

The [frozen Q-negative criterion](../gpt-retest-2026-10-01/plan.md) determines the three misses (`r01`, `c03`, `c04`). Judge B's content-preservation `Q` labels do not override the owner decision or its own failing L1/R1 readings. `c05` remains disputed about the exact unresolved obstruction. The two agreed repairs are `r02` and `c06`. `c07` is the English target failure; `c09`'s different, final assessment loses quotation marks during Proofread but its preparation target passes. These faults have separate ownership.

## Native evidence and limits

The retained trees contain 29 native invocations and 86 native sessions: twenty counted parents and 54 children, plus the refusal/void sessions and two judges. Every retained context matches `gpt-6.1-sol/xhigh`; every counted session has native start/completion events. The 54 actual child starts specify `fork_turns=none`, distinct child identities and no model override. Both judges completed separately without children or work/scratch writes; each received the identical neutral packet. The offline audit finds all 79 fenced fields in each judge's actual returned tool material; the remaining artifact field explicitly records no delivered text for `p03`.

Native calls and inventories confirm the four excerpt overreads and `c07`'s removal of pre-existing scratch directories. The exact mechanical files establish `c09`'s boundary deletion inside Proofread. Those facts are independent of a run's self-report. Both semantic judgements and every protocol-record outcome remain unchanged.

The packet still has real limits: encrypted complete dispatch briefs, some truncated resource returns, and the external observer's 100-ms sampling window. Those dependent T1/R2 lines remain skipped. The neutral judging packet omitted the frozen British mechanics rule requiring thousands commas; its raw number-normalisation failures cannot establish a defect. Disputed Write source readings, `c05`'s unresolved report and `c06`'s extra heading reading remain disputed. They justify no unconditional pass or new failure ticket.

A further contract-review limit appears in the residual handoff: the raw byline and bridge allegations conflict with explicit loaded requirements. Their historical scores are preserved, but they are excluded from verified defect briefs. This is an additive ownership/contract audit, not rejudging history.

Every result measures product/corpus `fb169087`, native Codex CLI 0.159.3, GPT `gpt-6.1-sol/xhigh`. Later main, including the integration base after #476/#477/#479/#480, was not run. The older GPT results used another seat and CLI, so no cause of a historical difference is isolated. Passing repository checks verifies evidence integration and evaluator code, not editorial quality.
