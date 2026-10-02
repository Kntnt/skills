# Local followups for maintainer disposition

These are exact proposed tracker texts, not published issues. Each is proposed with `needs-triage`; no implementation or new evaluation is authorised by this packet. All evidence measures `fb169087` under native CLI `0.159.3`, inherited `gpt-6.1-sol/xhigh`. Later `main` is not measured. Existing ownership references identify the subject of a fault, not a request to reopen a closed ticket. A disputed or skipped observation does not become a defect ticket.

## 1. Redline leaves stipulated Swedish quotation defects unreported

**Proposed body:**

The bounded GPT retest for #393 reproduces three mandatory-finding misses from complete frozen inputs. `r01` delivers “Den tiden skulle jag avsätta innan nästa hus börjar”; `c03` and `c04` deliver “Jag skulle avsätta den tiden innan nästa byggnad kommer i gång”. These are repair-log introductions in existing buildings, not construction work. Thomas has judged both original expressions defective in full context. The replies report the unavailable author but neither repair nor explicitly report these quotation obstructions.

Expected behaviour: read the quoted passage in its target language and complete context; make an idiomatic, supported repair or report that exact obstruction unresolved. Preserve supported meaning, stance and qualification. The two successful repairs in this same matrix are evidence that no canonical replacement is necessary, not an answer key to prescribe.

Evidence: `docs/evaluation/editorial-393/gpt-retest-2026-10-01/runs/{r01,c03,c04}/`, `owner-decision.md`, both raw blind judgements and protocol records. The separate ellipsis `c05` unresolved-report diagnosis is disputed and not counted among these three reproduced misses. Refs #393.

## 2. Redline expands valid English quotation without a reading obstacle

**Proposed body:**

In #393's unchanged-product positive response control `c07`, Redline changes “before the next building starts” to “before the trial in the next building starts”. The full English repair-log account supports the original figure. The report says its referent was unclear but establishes no concrete reading loss. Both independent blind judges reject the change as a false finding/unsupported review expansion, while accepting that the added trial meaning is contextually plausible.

Expected behaviour: preserve valid target-language quotation wording unless a reported finding establishes a real obstacle in the complete text. An implied activity alone is not an error. This fault concerns review preservation, not an invented trial fact or Swedish translation.

Evidence: `docs/evaluation/editorial-393/gpt-retest-2026-10-01/runs/c07/`, neutral sample-04 in both judgements, `semantic-judgements.json`. Its file-target counterpart `c08` preserves the working quotation; outcomes are separate. Refs #393; related quotation/preservation history #363/#377/#383.

## 3. Write invents authorship when source supplies no author

**Proposed body:**

Fresh Swedish Write invocation `w03` in #393 receives the unchanged corpus source, which states that no author name is supplied. The delivered draft says “Av användaren”. Its reply confirms “Bylinen anger användaren eftersom författarnamn saknas”. Both independent source-aware judges fail F1: missing authorship does not establish that the user wrote the article.

Expected behaviour: leave an unavailable author unfilled and report the gap rather than asserting authorship. Judge the entire delivered draft against supplied material; source-check process completion does not establish every claim's truth.

Evidence: `docs/evaluation/editorial-393/gpt-retest-2026-10-01/runs/w03/`, exact source and delivered text, both comparisons/dispositions and blind sample-13. The source-blind paired Redline `p03` did not receive the English source and is not charged with this unavailable comparison. Refs #393; source-duty/gate ownership should be reconciled with #376/#392 during triage.

## 4. Proofread removes visible quotation boundaries in a plain Markdown paragraph

**Proposed body:**

In #393 control `c09`, the substantive review leaves the final customer assessment as a marked quotation. The nested closing Proofread output removes the opening/closing quotation marks after “Lind said:” without adding blockquote formatting. The result is an ordinary Markdown paragraph with inferable attribution but no visible direct-quotation boundary. Both blind judges fail L2 and whole-quotation preservation.

Expected behaviour: a mechanical pass preserves the established quotation form unless it corrects a demonstrated punctuation defect. A plain paragraph is not a set-off blockquote merely because a preceding line introduces it.

Evidence: `runs/c09/transport-facts.json` in `docs/evaluation/editorial-393/gpt-retest-2026-10-01/`: mechanical input SHA begins `7d809a09`, output `6b5acf27`; exact captured files and native mechanical child retained. The preparation quotation's target phrase remains unchanged and passes independently. Refs #393.

## 5. Redline accepts removal of specific agency or qualifying narration as repetition

**Proposed body:**

#393's unchanged-product controls reproduce review-preservation losses outside the target quotation idiom question. In `c11/c12`, “Arbetslagen utformade själva kategorierna” is removed as repetition although the retained body says only that the school developed the categories. Both judges fail F1/R1 for loss of specific customer agency. In `c07/c08/c09/c10`, explicit narration that the customer's appraisal is qualified or includes a preparation reservation is removed solely as a quotation pre-echo; both fail R1. The qualification surviving inside the quotation does not itself establish a defect in its limiting frame.

Expected behaviour: a finding and its proposed repair distinguish repeated words from unique agency/scope/qualification. Preserve valid claim-limiting narration unless a real reported defect licenses its change, and reject an immediate round that introduces a defect under the shipped rule.

Evidence: the six exact input/artifact/reply comparisons and both blind judgements under `docs/evaluation/editorial-393/gpt-retest-2026-10-01/`. This is related to existing ownership #377/#383 and immediate round acceptance in #389. No second correction round ran and the later-round restoration clause remains unmeasured. Triage should reconcile existing ownership before filing. Refs #393.

## 6. Redline cleanup removes pre-existing harness directories

**Proposed body:**

In #393 response control `c07`, the parent removes the empty `scratch/cache`, `scratch/data`, `scratch/tmp` and `scratch/uv-cache` directories that the harness created before the Skill started. Native ordinal 196 records the `rmdir` operations, and before/after inventories confirm their removal. No supplied source or installed product was changed, but these directories were not owned working material of the Skill.

Expected behaviour: cleanup removes only material this invocation created. A response target does not authorise removal of pre-existing harness directories merely because they are empty.

Evidence: `runs/c07/trace-index.json`, complete parent rollout and `transport-facts.json` in `docs/evaluation/editorial-393/gpt-retest-2026-10-01/`. This is an incorrect side effect, distinct from #476's permission-blocked deletion of owned working files. This packet does not measure `main` after #476. Refs #393.

## 7. Reply checker reads outside prescribed excerpt boundaries

**Proposed body:**

Four fresh reply checkers in #393 read the mandatory delivery/base excerpts but also receive prohibited neighbouring text. `c08`, `c09`, `c12` and `p01` return the 52 words before the required base.review needle. The latter three additionally return the next delivery heading “Refusals”. These are exact actual returned bytes, not merely `sed` commands or file paths. The reply-check contract says to read the two specified sections and nothing else.

Expected behaviour: extract precisely the required delivery section and the specified base paragraph portion. A line-based range must not include text before a mid-line needle or the next heading.

Evidence: each `reply-scope-facts.json` and native checker trace in `docs/evaluation/editorial-393/gpt-retest-2026-10-01/runs/`. The observation is a bounded loading-scope violation; no semantic failure is inferred from those extra words. Complete filled dispatch text remains encrypted and is separately skipped. Refs #393.
