# GPT retest of the delivered source comparison — #362

Frozen before the first counted invocation. Thomas commissioned this retest on 2026-10-01 in Codex, explicitly replacing the historical request to run the #376 closing revision with today's main. This is a post-delivery measurement, with no product change, baseline arm, or causal comparison against historical runs.

## Immutable product and seat

Product and supplied fixtures are exported/read from `fb16908712c4d47a36fc6ee9dfb3eb2714a19e65`, main HEAD at staging. The source `sources/opinion.md` and checker fixture `p3-document-scope.md` remain byte-identical to their committed versions. The current editorial-quality rubric is the version carried by this product (latest rubric change `e2e65c4028008bc60100c4e43e646f59ead7e918`).

Seat: `gpt-6.1-sol`, `xhigh`, inherited from the current parent native rollout identified in identity.json. Harness: Codex CLI `0.159.3`. Historical GPT trials used `gpt-6-astra/high`, Codex CLI `0.155.1`; historical counts and judgements are not a baseline for this evaluation. Every top-level run, checker, correction and judge uses this one current seat. Child turn contexts are verified afterwards. No Claude process/model/harness is started.

## Matrix and staging

Six fresh top-level native sessions run the installed Write from the immutable export: three `/write --genre=opinion --language=en_US --output=response source.md`, three `/write --genre=opinion --language=en_GB --output=response source.md`. Contextual instruction: none. Each work directory holds the unchanged corpus opinion source. Each private installation holds the revision's Manager, Write, Redline and Proofread, as the corpus requires; Redline is not invoked in this specifically commissioned retest.

Six further fresh native sessions execute the checker task verbatim from the delivered source-check.md, with its current Claims section, on the frozen p3-document-scope fixture, resolved locale en_GB, as checker/plan.md defines. They write only report.md. No expected finding or historical report is exposed to them. Repetition is fixed at six.

The adapted copy of editorial-329/harness/run.py is evaluator tooling only. It substitutes current binary/parent-session paths, current harness metadata and identity, and captures transient Markdown/text versions externally every 100 ms without instructing the Skill to retain scratch. It preserves native parent and all nested rollouts, exact response, complete private-root before/after inventories and file-change classification inputs. Authentication is copied into private HOME but never retained as published evidence; inventory excludes its content/digest. Every private root/process is registered immediately. Model writes are confined to inventoried work and scratch using the CLI workspace-write sandbox. Evaluator evidence is outside these writable roots. A capability smoke test (with no editorial source) may precede counted runs.

Runs execute under neutral scratch-root/directory names. Evidence is copied into this packet only after blind judging. Nothing under editorial-329, the historical editorial-362 plans/runs, main's product files, or the protected rework branch/worktree is changed.

## Frozen judging

Every Write draft is judged by a fresh native GPT session from prompts/write-judge.txt. Its packet gives complete source, response, extracted draft, captured intermediate files, and identity-redacted trace/technical evidence under neutral names. No model identity, product arm, ticket identity or historical family judgement is supplied. The evaluator can stage evidence after seeing old records but never serves as semantic judge. The current applicable corpus criteria F1 G1 G2 P1 W1 L1 L2 T1 R2 O1 are all recorded, plus V1–V4 and X as the commissioned criteria. Missing evidence is skipped and gaps named. Quantitative anatomy requirements are counted under the current rubric. T2/R1 are inapplicable because no technique/Redline was commissioned.

V1 asks whether digital vana is expressed without changing the measured variable (omission is unexercised/skipped). V2 requires delivery. V3 requires byte-identical final compared prose and complete residual reporting with proposed smallest repairs. V4 tests unknown versus absent. X records every report finding as supported/false/disputed and every writer disposition, including intermediate false edits. The frozen detailed rubric is in the committed judge brief.

The six checker reports receive one fresh blind judge under prompts/checker-judge.txt, following the historical checker judging method. D requires a finding on the established submission/source-package scope change for the right reason; noticing then clearing it fails. X counts every other finding as supported/false/disputed. C records report words and elapsed wall time. No preferred replacement sentence is a criterion.

No selective rerun or tuning occurs. Interrupted/service-limited runs and judges are void, kept apart, and rerun as the protocol requires. Ambiguity is recorded as disputed rather than silently decided for the product. Real newly exposed defects receive their own needs-triage issue; behaviour owned by another existing issue is recorded there. The parked document-scope limit is reported as measured for Thomas's decision, not silently turned into a repair request.

## Record and handoff

New append-only records are write-gpt-2026-10-01-362.md and source-check-gpt-2026-10-01-362.md under docs/evaluation/records. This packet retains the full run and judging evidence plus an acceptance-criterion disposition against all seven original checklist items, with the scope omitted by this commissioned retest explicit. Each is scored from observed evidence, never from historical failures becoming administratively closed. No push, release, installation or product change is authorised. Local commits use Refs #362 because Thomas decides closure. Report results on #362 and hand the parent the exact revision/seat, evidence path, unresolved misses, and recommended tracker action.
