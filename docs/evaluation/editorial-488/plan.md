# Frozen native delivery regression for #488

Frozen before the first native run and any product change. The ticket body and its 2026-10-01 Agent Brief are the requirement. Read [the protocol](../protocol.md). No frozen file is edited after runs begin; supplements are separate prospective freezes, never rewritten history.

## Revisions, seat and seam

Starting product and corpus revision: `5457c89405aece11b325937f9f07407f01974f7c`. Inputs below are committed with this plan. The candidate is committed before staging if the fresh baseline reproduces the terminal-delivery defect. Otherwise the candidate arm stages the same unchanged product revision, and the outcome is recorded as not reproduced with ADR-0239; no speculative wording change ships.

Provider family GPT; model `gpt-6.1-sol`, reasoning effort `xhigh`, Codex CLI `0.160.0`. All runs, nested correction agents, reply checkers and independent judges use this one seat. Native turn_context records verify what actually launched. A mismatch voids the affected run rather than being counted as that seat. No Claude Harness or model is invoked.

The public seam is the complete terminal reply captured by Codex `exec --output-last-message`, never an earlier streamed block or the unchanged input file. The separate native trace answers correction, final Proofread, reply-check completion, cleanup/refusal and final-message ordering. A wording-presence pytest cannot establish this behavior; the fresh baseline is the red step, and product work requires an observed native failure first. Where no red appears there is no green repair to claim.

## Frozen material and matrix

`inputs/article-unnamed.md` is byte-identical to #480's contrast input. The other three inputs are byte-identical to this starting commit's existing editorial-quality controls. No contextual instruction, brief, technique or budget flag is supplied. Every run starts with one input named `input.md`; Harness dispatch and the installed Skills are infrastructure rather than supplied editorial material.

- `article-clean.md` — `f183e6da31cf78081cc7c7eee69570940e24802997e92d96bb111966aa4170d5`.
- `article-unnamed.md` — `5e43d4f391ba9e07920564e998ac7d764373e3d098df692ceebd4f6d01c8e374`.
- `column-flawed.md` — `9b12ad3fb2cb74011c974feda1d7aafa8c0394ac6899417be2dbdd40ad0e96ab`.
- `opinion-flawed.md` — `ab033d9f4c817c9eaa0efa32db93819a99291a3b22e29fb39f0d640e830ed990`.

Both arms run these nine rows, each a fresh top-level session:

| Row | Invocation | Count per arm |
| --- | --- | --- |
| article-unnamed | `/redline --genre=article --language=sv --output=response input.md` | 3 |
| opinion-flawed | `/redline --genre=opinion --language=sv --output=response input.md` | 3 |
| article-clean-response | `/redline --genre=article --language=sv --output=response input.md` | 1 |
| article-clean-file | `/redline --genre=article --language=sv --output=output.md input.md` | 1 |
| column-flawed-file | `/redline --genre=column --language=sv --output=output.md input.md` | 1 |

The article-unnamed headline must be corrected to identify its subject or retained with that defect reported unresolved. Opinion-flawed normally requires correction or reports unresolved unsupported motives, a booking-denominator inference, contradictory costs and a vague exhortation. These facts distinguish a missing artifact from a genuine clean no-change review. Record for each targeted response whether correction happened, was rejected, or findings remained; do not reinterpret a missing delivery as a successful review.

Article-clean is the clean no-change control: its file delivery is compared byte for byte with the input, and the response may use the short Swedish status only when unchanged with no unresolved findings. Column-flawed-file is a distinct flawed file control: the output must exist and the reply names its destination and reports findings without duplicating the artifact.

## Staging and capture

`harness/run.py` copies #362's GPT retest trace runner, itself based on `../editorial-329/harness/run.py`. It changes the current parent identity, CLI version, repository depth and private-root location, confines cleanup registration to this ticket's scratch home and adds the ability to stage a blind judge's response file. It preserves immutable git-archive staging, inventories, source identity, final reply, JSON event stream, every parent/child native rollout and observed transient file versions. No production Harness or SDK semantics are changed.

Every install is exported with `git archive` from the recorded revision, flattened with Manager and editorial Skills side by side under `.agents/skills`. Each run has a private HOME, CODEX_HOME, TMPDIR, caches, work and separate scratch under `/private/tmp/kntnt-orchestrate-20261002.o7bmMK/ticket-488-scratch`. No actual user HOME is writable. The runner inventories the entire private root before and after, including Harness storage. Files are inventoried by hash; authentication contents are never published. Evaluator captures stay outside the native writable root. Owned processes are registered immediately, run in their own groups and awaited; roots are retained until evidence is preserved, then removed by literal-path cleanup.

`harness/campaign.py` runs at most three independent sessions concurrently, with no shared root. Arms run sequentially. It writes random opaque packet names under ticket scratch and a separate mapping; native runs and judges never see arm names in their working directories. Only completed, judged packets are copied into this evaluation's `runs/` tree. The plan's scripts and judge brief are committed before the first run.

## Judging and criteria

Two independent fresh native judges read each run's staged input and terminal response alone (plus `output.md` for a file target), against `judge-brief.md`. No model, revision, arm, ticket, earlier streamed artifact or trace is exposed. The trace audit is made separately by the builder and is explicitly not blind. Judge messages carry the row expectation, never a prediction of its result. A no-change response carries no delivered artifact; artifact-only criteria are skipped with that reason, while missing mandatory findings remain a failure.

- D1: A changed response or unchanged response with unresolved findings delivers the complete artifact in exactly one format-named fence, frontmatter intact, and its applicable findings/claim account outside it. A cleanup-only terminal reply fails; the target is reproduced if any baseline response run loses required delivery, especially where the trace shows an earlier full delivery followed by cleanup and a replacement final note.
- D2: A file target creates the complete output, reports its destination and findings without repeating the artifact. A clean different file still receives the input byte for byte.
- C1: The reply's report accompanies the text when required, covers the detected/resolved or unresolved findings and accurately accounts for changed claims. Judge factual coverage without demanding a particular correction's wording. Unsupported facts, wrong locale, mandatory findings neither resolved nor reported, and forbidden side effects cannot pass.
- O1: Before/after inventory and source stat establish that supplied sources and installed Skills remain unchanged, and no run-owned scratch survives beyond any retained paths truthfully named by the reply. Harness cache/session writes are classified separately and listed, never treated as permission for editorial copies to remain.
- T1: The native trace establishes final mechanical pass, final measurement (when required), exactly one completed reply checker except genuine short clean status, and word-for-word delivery of unfaulted checked statements. Draft/return/delivery comparisons are preserved; missing trace details are disclosed and scored skipped where no preserved evidence reaches them.
- T2: Run-owned tools and permitted cleanup finish before terminal delivery; no later run-owned tool follows it. Refused removals are not worked around, and a cleanup failure is reported with actual retained paths while the complete text/report remains accessible.

The two judges' D1/D2/C1 readings are both preserved. The split rule copies #480: a split fails unless the passage deciding the failing verdict is a difference covered by the claim account or closing summary, in which case both readings are recorded and the criterion passes. This exception never excuses missing delivery or a mandatory finding disappearing. O1/T1/T2 are evidence audits, not semantic blind judgements. Unrelated editorial quality is outside this ticket; an observed actual miss is recorded and filed under its owning issue where one already exists.

## Bounded exit and voids

No baseline reproduction: complete and preserve both unchanged-product arms, report not reproduced, write ADR-0239 and ship evidence alone. Do not strengthen Redline or another Skill on inference.

Reproduction: diagnose the observed order and make the smallest local Redline change preserving the reply-check freeze. Commit implementation and regenerate the catalog before candidate staging. A candidate ships if all target criteria hold without a control regression. One prospective revise round at most, no larger than the failed subset, is allowed. Otherwise ship only if it beats baseline on D1 and no previously passing control regresses; if not, restore product wording in a new commit. Record every remaining actual miss and file it as a needs-triage issue naming #488, with both judges' readings. Do not repair unrelated editorial defects here.

A usage-limit, HTTP 5xx/overload, timeout, or externally deleted/changed file interruption is void. Keep its packet whole under `voided/`, record the reason and rerun the same frozen row in a fresh root. A completed session that omits required delivery is a finding. No arm is rerun for a better score and no criterion is softened.

## Commits and deliverables

Commit this plan, frozen inputs, runner, campaign and judge brief before runs. If reproduced, commit the minimal implementation before its candidate arm; do not rewrite the plan-freeze or any implementation history. Finally commit results, packets, separate trace audits, the protocol-format record `../records/redline-gpt-2026-10-02-488.md`, and any ADR-0239. Index/changelog additions go only in `.kntnt-orchestrate/488.md`. Evidence names each arm's exact instruction revision; if an implementation ships it names that implementation commit. No push, branch creation or merge occurs.

Run all four unmodified CONTRIBUTING.md checks before completion. No shipped-file changes means no catalog regeneration is necessary. A missing provider capability or a genuine requirement decision is reported as blocked without pretending the regression completed.
