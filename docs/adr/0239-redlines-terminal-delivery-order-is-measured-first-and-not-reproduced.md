# Redline's terminal delivery order — measured first, and not reproduced

This record declines a wording change to Redline's delivery step without a fresh reproduction of the cleanup-only terminal reply. Issue #488 makes that change conditional on current-product measurement. The baseline's six targeted response runs all deliver the artifact and its report in the terminal reply. A rule added against those results would have no observed failure to repair and no measured improvement to establish.

## The failure that commissioned the measurement

The committed #480 results describe `pre-article-unnamed-2` delivering a corrected article and report in an earlier block, calling a cleanup tool afterwards, and ending with a cleanup-only note. The preserved `response.txt` contains that note alone. The full original transcript was not preserved, so this session reads the ordering from the results account, not from a transcript it inspected. The two original judges failed artifact delivery and findings.

The shared delivery contract requires the artifact and report after cleanup; Redline's step 11 follows that contract. Its reply checker freezes unfaulted statements about the text, rather than establishing a terminal-message boundary. The fenced-response decision, ADR-0211, settles carriage of the artifact, rather than tool ordering. Those obligations already require a complete caller-visible delivery. The proposed change would explicitly put every run-owned tool, cleanup, inventory check, final measurement and completed one-shot reply check before the final delivery.

## Why no product wording changes

The prospective plan at [`docs/evaluation/editorial-488/plan.md`](../evaluation/editorial-488/plan.md) was committed as `80ffe252` before native runs. It stages the product at `5457c89405aece11b325937f9f07407f01974f7c`, in fresh Codex CLI 0.160.0 sessions on `gpt-6.1-sol` at `xhigh` effort. The fresh baseline has three `article-unnamed` response runs, three `opinion-flawed` response runs, a clean response/file pair and a distinct flawed file control.

Every targeted response changed the text and delivered it in one `markdown` fence with the applicable findings and claim account. The opinion responses retained reported structural findings; none were mistaken for clean no-change reviews. Each terminal reply matches the native parent's final message. The separate traces establish completed correction and mechanical work, one completed reply checker, and cleanup before that delivery. They show no later run-owned call. The paired clean file is byte-identical to its input. The flawed file control reports refused cleanup and the actual retained directory and lock file without concealing its destination or findings.

The trace evidence has a limit: some delegated prompts are encrypted, and no complete externally captured drafted reply exists for every checker. Word-for-word preservation of every unfaulted checked statement cannot be inferred from the checker return and delivered account alone. That comparison is recorded as unavailable where the evidence does not reach it. No native run here contains frontmatter, so these runs do not independently exercise a frontmatter-bearing artifact.

The frozen exit requires an unchanged-product second arm when the baseline does not reproduce the fault. Its exact results, both judges' readings, inventory accounts, interruptions and remaining misses are preserved in [`results.md`](../evaluation/editorial-488/results.md) and the protocol-format record. Neither arm licenses an inferred change to another Skill or to Harness semantics.

## What would reopen the change

A fresh completed run of the current product whose terminal reply loses a required artifact or findings would reopen it. An earlier stream block containing the text would not rescue that reply. Preserving the native trace would then establish whether cleanup, an unfinished checker or another late tool replaced the required delivery.

This is a non-reproduction on one GPT seat, rather than a claim that the original Claude-family failure was invalid or that it cannot recur. No product wording change ships, and no speculative regression test claiming to prove terminal delivery is added.
