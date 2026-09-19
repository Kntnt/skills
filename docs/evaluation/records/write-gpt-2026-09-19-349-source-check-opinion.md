# Opinion source-support completion verification — write

- **date** — 2026-09-19
- **ticket** — #349, #343, #338, #329
- **skill** — write
- **provider family** — gpt
- **model** — gpt-6-astra/high, verified in native context; no override
- **harness** — Codex CLI 0.155.1, unchanged native runner
- **corpus commit** — 6e531f5fe0b610e046ae58787f246cc6239acbcc
- **instruction commit** — d0b2c99c12a8727503b1738f1cad92611d879e1e

The frozen source, invocations and candidate prompts are unchanged. Write step6 now makes source support checked as part of writing a condition of draft completion. This is a bounded operational hypothesis after semantic guidance alone failed in all three locales; it does not authorize a separate editorial review or Proofread pass. Prior failures remain in 338/343/349 records. New independent Write→Redline sessions retain complete YAML-bearing text; Redline gets no source or delivery account. Each criterion is assessed before comparison. One sample is observed coverage, not future reliability. All writable roots, actual contract loads, native children and final installed Proofread are inspected.

## `opinion-sv`

- **fixture** — `opinion-sv`
- **invocation** — `/write --genre=opinion --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Full YAML-bearing draft and distinct account in `../editorial-329/runs/rerun-349-source-check/opinion-sv/write/response.txt`.
- **side effects** — 320 native home additions plus config trust; root removed.
- **criteria** —
  - `F1` — `fail` — 'Vi har inte kostnadsberäknat försöket eller ordnat finansiering för det' again asserts absent work/funding arrangement where source only withholds a claim. The operational source-check completion condition did not prevent #349 in this sample.
  - `G1` — `pass` — Clear accountable local debate with sharp supported criticism.
  - `G2` — `pass` — Early position/byline, attribution, real administration objection, board action and cost decision.
  - `P1` — `pass` — Evidence gap supports trial and later choice; external unsupported absence scored F1.
  - `W1` — `pass` — Functional headings and coherent paragraphs.
  - `L1` — `pass` — Idiomatic Swedish.
  - `L2` — `pass` — Swedish date, compounds, punctuation and numerals.
  - `T1` — `pass` — opinion/none/sv; actual selected/base/web/composition resources.
  - `R2` — `pass` — New step6 actually loaded; one first draft, no review half or extra editorial/Proofread invocation. Internal checking cannot independently be certified by a load trace; F1 tests its outcome.
  - `O1` — `pass` — Complete inventory and cleanup verify response-only effects.
- **unresolved findings** — #349 persists on d0b2c99; process hypothesis not verified repaired.
- **defects filed** — #349 recurrence under source-support completion change.
- **notes** — Native rollout confirms gpt-6-astra/high. Instruction commit d0b2c99c12a8727503b1738f1cad92611d879e1e. Original criterion unchanged. Source-blind Redline receives only artifact.

## `opinion-en_GB`

- **fixture** — `opinion-en_GB`
- **invocation** — `/write --genre=opinion --language=en_GB --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Complete YAML-bearing draft and separate account in `../editorial-329/runs/rerun-349-source-check/opinion-en_GB/write/response.txt`.
- **side effects** — 314 native home additions plus config trust; root removed.
- **criteria** —
  - `F1` — `fail` — 'Öppna beslut has neither costed nor funded this proposal' again asserts absent work from unclaimed source status. New completion condition did not prevent #349; #343 non-opposition and other report facts retained.
  - `G1` — `pass` — Clear pointed accountable opinion.
  - `G2` — `pass` — Early thesis and author, attributed pilot, real objection, specific committee decision and cost responsibility.
  - `P1` — `pass` — Unmeasured benefit and unexplained user choices support trial; external absence failure scored F1.
  - `W1` — `pass` — Useful headings and coherent paragraphs.
  - `L1` — `pass` — Idiomatic British English.
  - `L2` — `pass` — British date/spelling/punctuation.
  - `T1` — `pass` — opinion/none/en_GB matches actual selected and shared composition loads.
  - `R2` — `pass` — New completion condition read, one draft and no review half or extra pass; load trace does not certify successful internal claim checking.
  - `O1` — `pass` — Complete native inventory and cleanup, response-only.
- **unresolved findings** — #349 remains on d0b2c99 in sv and en_GB; US pending.
- **defects filed** — #349 repeated after source-check completion change.
- **notes** — Native rollout confirms gpt-6-astra/high. Same frozen source and prompts, d0b2c99. Third-person faulty sentence again limits any pronoun-only causal explanation.

## `opinion-en_US`

- **fixture** — `opinion-en_US`
- **invocation** — `/write --genre=opinion --language=en_US --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Full YAML-bearing draft and distinct account in `../editorial-329/runs/rerun-349-source-check/opinion-en_US/write/response.txt`.
- **side effects** — 316 native home additions plus config trust; root removed.
- **criteria** —
  - `F1` — `fail` — 'Öppna beslut has neither costed nor funded this proposal' converts source non-claim into categorical absence again. #343 stance and all pilot facts otherwise preserved.
  - `G1` — `pass` — Clear accountable local opinion with supported criticism.
  - `G2` — `pass` — Early position and byline, attributed evidence, real administrative objection, board action and cost responsibility.
  - `P1` — `pass` — Evidence gaps justify trial and later choice; unsupported external absence scored F1.
  - `W1` — `pass` — Functional headings and coherent paragraphs.
  - `L1` — `pass` — Idiomatic US English.
  - `L2` — `pass` — US date, spelling, punctuation and numerals.
  - `T1` — `pass` — opinion/none/en_US and selected/shared composition resources match.
  - `R2` — `pass` — New completion condition actually loaded; one draft, no extra review or Proofread. Load trace cannot certify internal source checking; F1 tests its result.
  - `O1` — `pass` — Complete inventory and cleanup verify response-only effects.
- **unresolved findings** — #349 persists in all three locales on d0b2c99; repair not verified.
- **defects filed** — #349 repeated after source-support completion change.
- **notes** — Native rollout confirms gpt-6-astra/high. Same frozen source/prompts. Instruction commit d0b2c99c12a8727503b1738f1cad92611d879e1e. Third-person faulty sentence again rules out first-person conversion as a sufficient explanation.

## Completion

All three locale pairs are complete on d0b2c99. Every Write sample fails F1 for #349; all three source-blind Redline samples pass their applicable criteria and preserve the input. This supersedes earlier pending-language notes, without changing their historical assessments. All six native roots have been inventoried and removed. No successful repair claim follows from these runs.
