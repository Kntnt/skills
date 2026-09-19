# Final quotation-boundary verification — redline

- **record** — `redline-gpt-2026-09-19-341-translation-part-article-case`
- **date** — 2026-09-19
- **ticket** — #341, #344, #338, #329
- **skill** — redline
- **provider family** — gpt
- **model** — gpt-6-astra/high, inherited and checked in native turn contexts
- **harness** — Codex CLI 0.155.1, unchanged real-session runner
- **corpus commit** — 6e531f5fe0b610e046ae58787f246cc6239acbcc
- **instruction commit** — 29ff2047ad2dac330dd705feccdb3f2d0778831b

Three fresh case-study locale pairs use the frozen source, unchanged prompts and same revision within each pair. This revision removes the conflicting lexical quotation prohibition and includes the source-check completion criterion. All previous failures remain. English pairs check the same-language quotation boundary; Swedish checks actual translation. The British pair also fulfils the previously planned #344 chronology rerun; this is not evidence of a targeted chronology fix or future reliability. Only complete extracted artifact/metadata reaches Redline, never the source, delivery account or rubric. All criteria are judged from full text and native traces before provider comparison; no other provider records are consulted.

## case-study-en_GB

- **fixture** — case-study-en_GB, quotation-boundary and chronology rerun
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status; complete byte-identical artifact retained in `editorial-329/runs/rerun-341-translation/case-study-en_GB/redline/`.
- **side effects** — No work/export/scratch change; native home effects inventoried, authentication unchanged, root removed.
- **criteria** —
  - G1 — pass — Customer agency and truthful supplier publication context retained.
  - G2 — pass — Distinct headline/ingress, background, choices, measures and customer's qualified appraisal preserved.
  - P1 — pass — Assignment/completion distinction and noncausality support the restrained conclusion.
  - W1 — pass — Connected paragraphs and useful quotation bridges retained without a headings quota.
  - L1 — pass — Natural British narration and source speaker's coherent English retained; no Swedish calque.
  - L2 — pass — Actual British mechanics pass preserves trialled, date and consistent permitted quotation convention.
  - T1 — pass — Metadata case-study/none/en_GB agrees with selected/shared review and language loads; no technique.
  - R1 — pass — Entire input remains byte-identical; no taste repair or unavailable-source caveat, claims and customer voice preserved.
  - R2 — pass — Full review; no substantive correction needed. One successful installed Proofread flags-only shim invocation and shared/en_GB mechanics loaded, no later edit.
  - O1 — pass — Complete inventories and transient cleanup establish preserved input/resources and no lasting Skill effect.
- **unresolved findings** — none
- **defects filed** — none; Write's #344 sample outcome is distinct from this source-blind review.
- **notes** — Native identity confirmed; earlier rejected shell wrapper made no effects, successful private-directory retry is visible.

## case-study-sv

- **fixture** — case-study-sv, final quotation-boundary verification
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Full repaired artifact alone in `editorial-329/runs/rerun-341-translation/case-study-sv/redline/`; “innan nästa byggnad börjar” becomes “innan försöket börjar i nästa byggnad”.
- **side effects** — No work/export/scratch changes; native home effects inventoried, authentication unchanged, root removed.
- **criteria** —
  - G1 — pass — Customer-led account and supplier publication disclosure preserved.
  - G2 — pass — All background, choices, qualified measures, appraisal and checklist action remain; no extra quote or sales requirement.
  - P1 — pass — The repaired reference names the trial already established by surrounding text and preserves its prospective status.
  - W1 — pass — Complete narrative/paragraphing retained; one local phrase changes, no template or quota imposed.
  - L1 — pass — “innan försöket börjar i nästa byggnad” is idiomatic and explicit without changing customer stance or qualification. The remaining Swedish prose is natural.
  - L2 — pass — Actual shared/sv mechanics loaded once; correct date, dash and compound conventions retained.
  - T1 — pass — Metadata case-study/none/sv honoured; parent and fresh correction load selected/shared review resources and three language scopes, no technique.
  - R1 — pass — Visible referent defect detected and minimally repaired. Full before/after comparison confirms every other claim, quote, qualification and metadata byte survives; only final newline presentation also differs. No claim was removed and no removal account is needed for this local clarification.
  - R2 — pass — One correction with fork_turns=none, full child contract and language reads, complete return and parent re-review, then exactly one installed flags-only Proofread invocation with shared/sv mechanics. No substantive edit after it.
  - O1 — pass — Complete inventories and both sessions' transient cleanup show no lasting Skill file or source/resource mutation.
- **unresolved findings** — none in final Redline text; the paired Write L1 failure remains recorded separately.
- **defects filed** — #341: source-blind pipeline repair observed, not verified reliable prevention in Write.
- **notes** — Both native sessions gpt-6-astra/high. Encrypted handoff message prevents direct plaintext brief comparison; fresh-session metadata, actual full resource reads, complete return and effects are visible. This one successful repair does not erase earlier misses or guarantee future repair.

## case-study-en_US

- **fixture** — case-study-en_US, final quotation-boundary verification
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Full corrected case plus separate account of two redundant claims removed, preserved in `editorial-329/runs/rerun-341-translation/case-study-en_US/redline/`.
- **side effects** — No work/export/scratch changes; native home effects inventoried, authentication unchanged, root removed.
- **criteria** —
  - G1 — pass — Customer agency, qualified appraisal and supplier disclosure maintained.
  - G2 — pass — Preparation quotation now follows minimal “Lind said:” attribution; concrete next step remains without its generic restatement. Complete case functions preserved.
  - P1 — pass — All counts, exclusions, assignment/completion boundary and noncausality remain. Unsupported source-only interview prompt is not an internal contradiction this review can discover.
  - W1 — pass — Removing the preparatory paraphrase and closing restatement avoids two redundant restarts; paragraphing and independent ingress retained.
  - L1 — pass — Natural American language and original quoted voice unchanged.
  - L2 — pass — Actual shared/en_US mechanics pass leaves valid date, quotation and dash usage intact.
  - T1 — pass — Case-study/none/en_US honoured; parent/corrector load only selected/shared review resources and resolved scopes, no technique.
  - R1 — pass — Full diff shows exactly the two findings repaired. The lesson and next-decision substance remain in quotation/concrete preceding sentence; parent explicitly reports both removed redundant claims. Other facts, qualifications, quotations and metadata preserved. No unavailable-source caveat.
  - R2 — pass — One fresh correction with fork_turns=none, complete child resource/language reads and return, parent re-review, one actual installed flags-only Proofread invocation and shared/en_US mechanics. No later substantive edit.
  - O1 — pass — All writable-root inventories and transient cleanup show no lasting Skill file or source/resource mutation.
- **unresolved findings** — None under Redline's text-only scope. Upstream Write #352 (“Asked to assess”) remains in the final artifact and is not thereby validated.
- **defects filed** — #352 is the source-aware Write defect, not a new Redline defect.
- **notes** — Both native identities gpt-6-astra/high. Raw spawn brief is encrypted; fresh-session metadata, full child reads, complete return and effects are visible. All three source quotations remain verbatim.

