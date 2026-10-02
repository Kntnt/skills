# Frozen plan for the GPT quotation retest

Issue #393. Frozen and committed before the first counted invocation on 2026-10-01. Product and corpus checkout: `fb16908712c4d47a36fc6ee9dfb3eb2714a19e65`. This is one unchanged-product arm. It makes no causal claim against a historical arm and runs neither a candidate nor a revise round.

The new [maintainer decision](owner-decision.md) supplies the expected behaviour of the three Swedish negatives. [ADR-0212](../../../adr/0212-a-quotation-is-read-in-the-language-it-is-written-in.md), the #363 plan, fixtures and results, and every earlier GPT outcome stay historical evidence. None is edited. The inherited instructions of #393 are satisfied by settling the human reading first and measuring it here.

## Seat and staging

Native Codex CLI `0.159.3`, `/opt/homebrew/bin/codex`, with the actual evaluating session's `gpt-6.1-sol` model and `xhigh` effort. `parent-identity-evidence.json` retains the native metadata/context events that establish this identity. Every product parent, correction agent, checker and judge uses that seat. The runner copies the observed identity into private configuration rather than choosing a model. Every native rollout's metadata and turn contexts are checked after completion. History used Codex `0.155.1`, `gpt-6-astra/high`; changed product, harness and seat mean this retest does not isolate which change caused any difference.

The runner is the repository's native GPT runner adapted only for the current CLI, current parent identity and external preservation of transient text/report files. It exports exact committed bytes for the Manager and Write, Redline and Proofread into each private project, supplies only `source.md` or `input.md`, and sets isolated home, configuration, authentication copy, scratch and cache locations. No global Skill install is read or changed. Product instructions are byte copies of the frozen revision. Private model writes are confined to the work project and its separate scratch area by the native workspace sandbox. All locations are inventoried before and after, including staged installs and private harness home; authentication is represented by mode/size and an unpublished in-memory integrity check, never its contents.

Each invocation is a fresh top-level native session with no conversation history, so required fresh checkers and correction agents are available. Up to two invocations run concurrently, in separate roots. Runner and native process groups and scratch paths are registered immediately through session-cleanup. The runner captures the complete parent and child rollouts, JSONL event stream, stderr, reply, inventories, process/result metadata, and externally observed versions of transient Markdown/text files every 100 ms. Observation is outside the writable project and adds no instruction to the Skill. Sampling can miss a file whose entire existence falls between observations; any such gap is stated, never inferred away. Trace evidence takes precedence over a run's claim about itself.

Formal invocations are the complete contents of `turns/`; Contextual Instruction is `none`. No evaluator findings, replacement prose, fixture identity, old result or owner decision is given to a product session.

## Fixed matrix

`input-manifest.json` gives the full inherited input paths and their SHA-256 digests. Whole files are replayed without normalisation.

| Row | Target | Count | Invocation |
| --- | --- | ---: | --- |
| sv-control | response | 2 | `/redline --output=response input.md` |
| sv-artefact | response | 2 | same |
| ellipsis-sv | response | 2 | same |
| en-positive | response and new file | 1 each | `/redline --output=response input.md`; `/redline --output=output.md input.md` |
| en-us-r1 | response and new file | 1 each | same |
| metonymy-sv | response and new file | 1 each | same |
| rhythm-en_GB | response and new file | 1 each | same |
| case-study-sv | response | 3 | `/write --genre=case-study --language=sv --output=response source.md` |
| each delivered case-study-sv artifact | response | 1 fresh pair each | `/redline --output=response input.md` |

Thus 17 independent product sessions plus three dependent pairs: 20 at most. A Write that delivers no Text Artifact has its pair recorded `skipped`, with the reason. A withheld text is never treated as a delivered draft. There are no unplanned repetitions for a product miss, unrelated finding or clean-control change. A session or judge interrupted by service overload, HTTP failure or usage limit is void, preserved separately and rerun on the same input, as the protocol requires; those reruns are not counted as discretionary rounds.

The four positives use both targets under the current [protocol](../../protocol.md#a-clean-control): response-target status/delivery and side effects are measured separately from the explicit file-target text. Every file-target result is captured exactly. A no-change response is no evidence for preservation of delivered text and gives `skipped` for a criterion needing that text. Paired Redline sees only the exact Text Artifact Write delivered, including its metadata, never the source or the Write account.

## Criteria and judging

Two independent fresh blind judges receive neutral run IDs under a separate scratch root and the fixed `judge-brief.md`. They see neither model, arm, ticket, historical outcome nor hypothesis. Their text/fidelity packet contains exact supplied input, delivered artifact where present, and user-facing reply. Write judging additionally receives the exact corpus source. Trace/transport judging is separated from semantic judging because native traces expose model identity. Mechanical byte comparisons need one evaluator only.

- **Q-negative:** Each Swedish negative is repaired idiomatically using only meaning supported by the complete input, or its exact obstruction is explicitly reported unresolved. Unchanged and unreported is a mandatory-finding failure under the maintainer decision, regardless of a judge's taste. A reported problem elsewhere in the quotation does not satisfy this criterion. Deleting the quotation is not a repair.
- **Q-translation:** Every delivered Swedish Write draft includes the substantive Maya Lind preparation quotation, rendered as idiomatic Swedish and preserving meaning, stance, qualification and customer voice. Omission fails this commissioned control. Both judges must agree for an unqualified pass. A correct withholding is a stop and not a passing draft; its fidelity gate is recorded separately. At least two of the three must deliver to establish a translation pass for the wave, and every delivered quotation must pass.
- **Q-preservation:** The two working English quotations and the two new positive quotations remain unchanged. Any expansion of the valid Swedish term/office figures fails. For other changes, a reported finding must establish a concrete target-language reading obstacle visible in the complete text; semantic judging decides whether it does. No fixed replacement is rewarded. A positive run flagged only because of its expected working quotation is a false finding, recorded separately even if preservation survives.
- **F1:** Source support and preservation of factual and attributed meaning, uncertainty, scope, chronology and causal limits. For Write compare the whole delivered draft with the exact source; for source-blind Redline compare input with output, never enlarge its source duty. Quotation meaning and idiom are scored separately.
- **G2:** Customer agency and experience, the qualified endorsement, supplier third person and disclosure, and an accurate optional destination where applicable; the article positive is judged against its genre instead. No invented scene or categorical benefit is excused by better wording.
- **G1/P1/W1/L2:** Also score the corpus's applicable genre job, reasoning/reader orientation, web form and locale-mechanics criteria from the complete artifact. Counted anatomy limits are measured rather than inferred; advisory norms require actual reader loss. These do not substitute for the target quotation criteria.
- **L1:** Idiomatic target-language prose throughout the delivered artifact, separately from mechanics. The frozen negative behaviour expectations cannot be rescored as valid by the judge.
- **R1:** Required review findings are resolved or delivered unresolved; working text is preserved, and each substantive difference has a supported finding rather than taste alone. Whole-artifact R1 is distinct from target-quotation success.
- **O1:** Output target honoured, sources/staged instructions unchanged, and no unauthorised artifact or process remains. Before/after inventories and traces classify each effect as harness or Skill. A no-change response is judged from its actual words, input and inventories only.
- **C-chain:** For each Redline, a complete private mechanical input is frozen; separate complete Proofread output exists, is read, and matches the delivered Text Artifact exactly where one was delivered. Default Correction Budget is preserved. Both no-change and artifact delivery branches are recorded if observed, never arranged.
- **T1/R2:** Record actual resource and fresh-agent loading from retained parent/child trace against the shipped load contract. A missing trace segment makes its dependent line `skipped` with the gap named. Neither a run's self-report nor a path glob proves an individual resource read.
- **Cost:** Report observed wall times and median by Skill and target, plus mandatory resource word counts from actual named reads where established. No cost-benefit or candidate-ship decision is made for an unchanged-product arm.

The corpus's five unconditional rejections apply. Both semantic judgements and any split remain in the packet. A split is `disputed`, not an unqualified pass. Deterministic missing-finding and byte-preservation facts remain measurable when a judge cannot decide idiom. A newly worded repair that both judges cannot assess remains an instrument limit. No third judge, answer shopping or further wording attempt is scheduled.

Other observed faults are recorded under their existing owning issue where established (#377/#383 review preservation, #389 round rejection, #390 headings, #392 source duty, #394 capability, #376 source gate). They remain whole-artifact failures where applicable but are not silently counted as quotation faults. An unowned observed fault gets a precise local proposed ticket; no issue is published by this evaluation.

## Deliverables and cleanup

Commit this plan, owner decision, turns, manifest, judge brief and runner before running. Preserve counted runs and voids, both blind judgements, deterministic checks, readable results, protocol-format issue-suffixed records, and exact local tracker comment/proposed actions. No GitHub comment, new issue, closing action, push, release, global installation, product edit or new ADR is authorised. No fixture search is made. Historical records stay unchanged.

Run the repository's applicable checks on the evidence branch before handoff. Preserve every deliverable, including this evidence worktree. Stop and verify all run-owned processes; delete scratch only with explicit literal full paths, after necessary evidence has been preserved. Keep cleanup evidence and name retained deliverable paths in the handoff.
