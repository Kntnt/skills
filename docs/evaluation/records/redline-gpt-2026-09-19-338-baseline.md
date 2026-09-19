# Baseline Redline — editorial #338

- **record** — `redline-gpt-2026-09-19-338-baseline`
- **date** — `2026-09-19`
- **ticket** — `#338`, parent `#329`
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`, observed in native turn contexts
- **harness** — native Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `8ae4c21c203fa44f9782c3c0db2c85a5d805c3a6`

## Conditions

The [frozen matrix](../corpus/editorial-quality/README.md) supplied the criteria before any editorial run. Each invocation used a fresh native session, immutable local skill copies, one staged input and no previous conversation. The complete source package was given only to Write; Redline received only the complete extracted draft, including metadata. The baseline's ordinary ABT is retained rather than overridden. Exact neutral dispatch and scratch context are captured in each run's `harness-context.md`; they add no editorial instruction. No other provider's evaluation record was consulted. Judgements below precede any candidate comparison.

Raw responses, invocation/context, inventories, exact filesystem changes, native parent/correction rollouts and cleanup evidence are under [baseline runs](../editorial-329/runs/baseline/). Harness-created caches, native sessions and trusted-project config updates are explicitly distinguished from Skill effects in each `side-effects.md`. The evaluator's artifact extraction removes only the separately identified delivery account; it does not rewrite the text. Failed runs remain.

## `article-sv`

- **fixture** — `article-sv`, complete baseline draft only
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`; neutral Harness dispatch is preserved separately.
- **output target** — `response`
- **observed delivery** — The run reviewed the article and announced no editorial findings, then returned only the nested Proofread parser error, `'---' is not a flag of this collection's grammar`; no final Text Artifact or completed no-change status was delivered. [Input](../editorial-329/runs/baseline/article-sv/redline/supplied-input.md), [response](../editorial-329/runs/baseline/article-sv/redline/response.txt).
- **side effects** — No remaining Skill-created files; source artifact, installed resources and full work/scratch are unchanged. Private UV directories were cleaned. Codex created 318 private-home entries and recorded project trust; full hashes and paths are in the run inventories and filesystem change list.
- **criteria** —
  - `G1` — `skipped` — No final reviewed artifact was delivered after the technical failure; the input's genre quality is judged in the independent Write record.
  - `G2` — `skipped` — No final artifact was delivered; the unchanged source file is not silently treated as successful output.
  - `P1` — `skipped` — Final reasoning cannot be assessed without a completed delivered artifact.
  - `W1` — `skipped` — No final artifact was delivered for web-reading assessment.
  - `L1` — `skipped` — No final artifact was delivered for idiom assessment.
  - `L2` — `skipped` — The mandatory mechanical pass never reached its language/mechanics resolution.
  - `T1` — `pass` — The recognized input map resolves article/ABT/sv; trace loads common base, article plus review, ABT plus review, anti-slop and actual Swedish composition/review/anti-slop scopes, with no competing technique.
  - `T2` — `skipped` — No final artifact was delivered; the baseline input's low-key ABT is independently judged in Write.
  - `R1` — `skipped` — The review announced no substantive findings and spent no correction budget, but its completed preservation result was never delivered because Proofread failed.
  - `R2` — `fail` — Contract failure: item_12 serializes the full YAML-bearing artifact directly after `--language=sv --output=response\n`; the nested invocation engine treats the initial `---` as a flag and exits 2. One closing pass was attempted but none completed. This is a failed invocation/delivery, not an invented textual error or a hidden repair.
  - `O1` — `pass` — Complete inventories show no model artifact or scratch left behind and no source/resource mutation; Harness-only writes are preserved explicitly.
- **unresolved findings** — No editorial finding was reported; the unresolved technical error was returned verbatim. A completed mechanical review is unavailable.
- **defects filed** — [#339](https://github.com/Kntnt/skills/issues/339).
- **notes** — This is an actual run with a failed mandatory stage, not an unrun cell or a quality pass. No final.md is fabricated from the input. Baseline instructions and prompts remain unchanged for subsequent cells.

## `article-en_GB`

- **fixture** — `article-en_GB`, complete baseline draft only
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`; neutral Harness context is captured separately.
- **output target** — `response`
- **observed delivery** — A real fresh correction ran, but the final response contains only the nested Proofread parser error and an explicit incomplete-review notice; no final Text Artifact. [Response](../editorial-329/runs/baseline/article-en_GB/redline/response.txt), [intermediate correction](../editorial-329/runs/baseline/article-en_GB/redline/correction-agent-response.md).
- **side effects** — **125 new Skill-triggered scratch entries remained**, from the correction's bare `uv run`: an environment/PyYAML cache and temporary lock. The other 315 new paths and project-trust config update are Harness effects. Source, work and installed files are unchanged. [Classification](../editorial-329/runs/baseline/article-en_GB/redline/side-effects.md) and complete inventories distinguish these before evaluator cleanup.
- **criteria** —
  - `G1` — `skipped` — No completed final artifact was delivered; the Write draft's genre quality was judged independently.
  - `G2` — `skipped` — The intermediate correction preserves article parts, but the mandatory closing stage failed before final delivery.
  - `P1` — `skipped` — There is no completed final artifact; the intermediate edit preserves the explanation and causal limits.
  - `W1` — `skipped` — No final artifact was delivered for the pipeline's web-reading result.
  - `L1` — `skipped` — No completed final artifact; idiom of the intermediate correction is not substituted for final success.
  - `L2` — `skipped` — Proofread refused at parsing before its mechanical resolution/pass.
  - `T1` — `pass` — The metadata resolves article/ABT/en_GB; parent and correction read local selected ABT and article resources and resolve en_GB scopes, with no competing technique selected. Full resource-load completeness is separately constrained by R2 and trace truncation noted below.
  - `T2` — `skipped` — No final artifact; the bounded baseline ABT remains visible in the intermediate draft but cannot establish completed pipeline delivery.
  - `R1` — `skipped` — The intermediate correction changes only two identified places: it adds the already stated fictional qualification to the body and merges repeated final advice. Before/after comparison finds no lost claim, date, quotation, caveat or attribution. The mandatory final result was nevertheless not delivered.
  - `R2` — `fail` — Contract failure: a fresh same-model/high correction actually ran and was re-reviewed, but the subsequent one attempted installed Proofread invocation again sends raw YAML as invocation tokens and exits 2 on `---`; no closing pass completes.
  - `O1` — `fail` — **Incorrect side effect:** 125 scratch entries created by the correction's language-resolution command survived its parent response. Full inventories show this even though `input.md` itself is unchanged.
- **unresolved findings** — The final response openly says the review is incomplete due to the frontmatter handoff. The two editorial findings were repaired in the intermediate correction. The surviving cache was not reported by Redline.
- **defects filed** — [#339](https://github.com/Kntnt/skills/issues/339), [#340](https://github.com/Kntnt/skills/issues/340).
- **notes** — Both native turn contexts expose gpt-6-astra/high. The correction gets only the complete artifact, findings and local resources, not Write's source. Large combined resource reads were truncated in the functions tool; some files were re-read separately, so mere presence of the original shell `cat` is not claimed as proof of every byte reaching the model. No successful final.md is fabricated.

## `case-study-sv`

- **fixture** — `case-study-sv`, English source to Swedish; complete draft only
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`; neutral Harness context is captured separately.
- **output target** — `response`
- **observed delivery** — Completed no-change status after review and one Proofread pass; final artifact equals the input, with the observed translation flaw retained; [draft](../editorial-329/runs/baseline/case-study-sv/draft.md), [final](../editorial-329/runs/baseline/case-study-sv/final.md), [response](../editorial-329/runs/baseline/case-study-sv/redline/response.txt).
- **side effects** — No remaining Skill files; full work/input/resource/export/scratch inventories unchanged. Private UV directories were cleaned. Native Codex created 318 private-home entries and added project trust to its config; [classification](../editorial-329/runs/baseline/case-study-sv/redline/side-effects.md) lists the evidence boundaries.
- **criteria** —
  - `G1` — `pass` — The customer's own maintenance problem, category work and qualified appraisal organise the case; the supplier is a supporting third-person actor rather than a rescuer or first-person advertiser.
  - `G2` — `pass` — Situation, action, bounded results and actual quoted appraisal are all present; the checklist link describes a document, not a booking. The publisher is identified only in Write's delivery account, a reuse-context limitation, but the text does not claim independent publication.
  - `P1` — `pass` — The shift-work purpose precedes configuration, and the measured assignment time is explicitly distinguished from repair completion; workload differences explain why causation cannot be assigned.
  - `W1` — `pass` — The short coherent paragraphs move through decision, preparation, measured results and appraisal; no H2s are used, but this moderately sized case remains navigable through clear paragraph openings. No heading quota is imposed.
  - `L1` — `fail` — **Qualitative language interference:** “innan nästa byggnad börjar” carries over the source's “before the next building starts”; the Swedish reader has to reconstruct that the trial/implementation begins in that building. This is neither a fabricated fact nor a mechanical spelling error.
  - `L2` — `pass` — Swedish speech dashes, compounds, date and number forms are consistent; the awkward translated predicate is scored under L1 rather than misclassified as wrong locale mechanics.
  - `T1` — `pass` — The metadata carries case-study/abt/sv and the actual trace loads the selected case and only ABT, with Swedish scopes resolved explicitly; the default originates with the baseline genre for Write and the input metadata for Redline.
  - `T2` — `pass` — The need for shared information, category-preparation burden and qualified decision form a restrained arc; no miraculous rescue, satisfaction increase or software-caused improvement is invented.
  - `R1` — `fail` — **Qualitative repair miss:** the review delivers “Inga ändringar behövdes” and preserves every claim and voice, but it fails to address the visible awkward Swedish quotation predicate noted under L1. No unsupported source comparison is required to recognise the missing activity. This is an editorial miss, not a hidden mechanical rewrite.
  - `R2` — `pass` — Review resources and all required scoped content are actually visible; resource-visibility.json checks complete resource paragraphs across native tool outputs/re-reads. No correction is spawned because the run reports no finding. Item_14 quotes the full YAML-bearing operand with shlex.quote and invokes installed Proofread successfully; items_15–16 load mechanics and resolve sv exactly once, and no substantive edit follows.
  - `O1` — `pass` — Entire-root inventories and executed temporary-directory cleanup establish preserved source/resources and no surviving Skill scratch.
- **unresolved findings** — Redline reports none; the evaluator identifies the remaining L1 flaw despite the no-change status.
- **defects filed** — [#341](https://github.com/Kntnt/skills/issues/341).
- **notes** — Several idiomatic translations could satisfy L1, and the quotation need not be retained in every valid draft. This observation does not itself justify an additional blanket instruction. Candidate wording was not consulted for this judgement.

## `column-sv`

- **fixture** — `column-sv`, complete baseline draft only
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`; neutral Harness context is captured separately.
- **output target** — `response`
- **observed delivery** — Only the nested Proofread parser error (`'---' is not a flag of this collection's grammar`) was delivered; no final text or completed no-change status. [Response](../editorial-329/runs/baseline/column-sv/redline/response.txt).
- **side effects** — No remaining Skill files, and source/work/resources/scratch unchanged. All private UV contexts were cleaned. Native Codex's 316 created private-home entries and project-trust config update are enumerated separately.
- **criteria** —
  - `G1` — `skipped` — Closing-stage technical failure prevented final artifact delivery; the source draft is not relabelled as reviewed output.
  - `G2` — `skipped` — No completed final artifact was delivered.
  - `P1` — `skipped` — Final reasoning could not be judged after the failed mandatory handoff.
  - `W1` — `skipped` — No final artifact was delivered for web-reading judgement.
  - `L1` — `skipped` — No completed final artifact was delivered for idiom judgement.
  - `L2` — `skipped` — The mechanical pass failed at invocation parsing, before its own mechanics resolution.
  - `T1` — `pass` — The input metadata governs column/ABT/sv and the trace loads only the selected technique alongside genre/base/review/anti-slop and Swedish review scopes.
  - `T2` — `skipped` — A completed reviewed artifact is unavailable.
  - `R1` — `skipped` — No correction was needed according to the review, but its preservation result was not delivered after the parser refusal.
  - `R2` — `fail` — Contract failure: item_11 passes a raw YAML-bearing inline artifact to the installed Proofread engine, which rejects `---`; one closing pass was attempted, none completed.
  - `O1` — `pass` — Whole-root inventories preserve input/resources and show no surviving Skill-created files, even after the failed nested invocation.
- **unresolved findings** — The technical refusal is reported verbatim; the mandatory mechanical pass is incomplete.
- **defects filed** — [#339](https://github.com/Kntnt/skills/issues/339).
- **notes** — This real failed invocation is not counted as a quality pass and no final.md is fabricated.

## `opinion-sv`

- **fixture** — `opinion-sv`, complete baseline draft only
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`; neutral Harness context is captured separately.
- **output target** — `response`
- **observed delivery** — Only the nested Proofread parser error (`'---' is not a flag of this collection's grammar`) was delivered; no final text or completed no-change status. [Response](../editorial-329/runs/baseline/opinion-sv/redline/response.txt).
- **side effects** — No remaining Skill files, and source/work/resources/scratch unchanged. All private UV contexts were cleaned. Native Codex's 318 created private-home entries and project-trust config update are enumerated separately.
- **criteria** —
  - `G1` — `skipped` — Closing-stage technical failure prevented final artifact delivery; the source draft is not relabelled as reviewed output.
  - `G2` — `skipped` — No completed final artifact was delivered.
  - `P1` — `skipped` — Final reasoning could not be judged after the failed mandatory handoff.
  - `W1` — `skipped` — No final artifact was delivered for web-reading judgement.
  - `L1` — `skipped` — No completed final artifact was delivered for idiom judgement.
  - `L2` — `skipped` — The mechanical pass failed at invocation parsing, before its own mechanics resolution.
  - `T1` — `pass` — The input metadata governs opinion/ABT/sv and the trace loads only the selected technique alongside genre/base/review/anti-slop and Swedish review scopes.
  - `T2` — `skipped` — A completed reviewed artifact is unavailable.
  - `R1` — `skipped` — No correction was needed according to the review, but its preservation result was not delivered after the parser refusal.
  - `R2` — `fail` — Contract failure: item_12 passes a raw YAML-bearing inline artifact to the installed Proofread engine, which rejects `---`; one closing pass was attempted, none completed.
  - `O1` — `pass` — Whole-root inventories preserve input/resources and show no surviving Skill-created files, even after the failed nested invocation.
- **unresolved findings** — The technical refusal is reported verbatim; the mandatory mechanical pass is incomplete.
- **defects filed** — [#339](https://github.com/Kntnt/skills/issues/339).
- **notes** — This real failed invocation is not counted as a quality pass and no final.md is fabricated.

