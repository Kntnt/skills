# Redline — GPT — source-fidelity follow-up, supplemental and general cases

- **record** — `redline-gpt-2026-09-19-349-followup-new`
- **date** — `2026-09-19`
- **ticket** — #329, #349, #352
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, inherited `high`, confirmed in every native parent and child
- **harness** — Codex CLI 0.155.1
- **instruction commit** — `8f92e1266493f40099b3274374b6c0223c2f76a8`
- **corpus commit** — supplementary matrix/fixtures `bf14dc23ea872694d095e3a386beb06793a4e556`; original source packages remain `6e531f5fe0b610e046ae58787f246cc6239acbcc`

Every declared pair ran in a fresh source-blind session. Each supplied `input.md` was byte-compared with the complete extracted Write artifact, including metadata. Source packages, Write accounts, checker reports and evaluator assessments were not passed to Redline. For no-change responses, the input is the extracted final artifact; that copy is evaluator evidence, not a Skill write.

The evaluator separately compared all twelve final artifacts with the source: all preserve source fidelity. That is pipeline evidence, not a claim that Redline verified an unseen source. One review has a definite false-positive finding about an expressly uncertain proposed timetable. Its repetition of an unchanged artifact follows Redline step 11's unresolved-finding exception but conflicts with the shared delivery contract; this is recorded as a contract collision rather than unambiguous model disobedience. See the [observation and correction of the provisional assessment](../editorial-329/followup/reviews/opinion-timetable-observation.md).

Full inventories for all twelve runs show only private native Harness state changes, no surviving Skill files and unchanged inputs/resources. All private roots were removed after capture and review. Native dispatch payloads are encrypted; actual correction-child identity, fresh-spawn settings, full resource reads and returns are inspectable, but the exact dispatch brief is not.

## `opinion-unknown-sv-r1`

- **fixture** — `opinion-unknown-sv-r1`, complete preceding Write artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status after editorial review and one final mechanical pass; the input is final. [Full response](../editorial-329/followup/runs/candidate/opinion-unknown-sv-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/candidate/opinion-unknown-sv-r1/redline/artifact.md), [supplied input](../editorial-329/followup/runs/candidate/opinion-unknown-sv-r1/redline/supplied-input.md).
- **side effects** — No surviving Skill changes; native Harness state only. [Full differences](../editorial-329/followup/runs/candidate/opinion-unknown-sv-r1/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/candidate/opinion-unknown-sv-r1/redline/cleanup.json).
- **criteria** —
  - G1 — pass — The opening demands a comparison before permanent investment, addressing the harbour board's decision directly.
  - G2 — pass — The thesis, actual administrative benefit, evidence limits and requested next-meeting decision perform distinct jobs.
  - P1 — pass — The argument moves from missing decision data and limited booking counts to comparing two options without claiming the seasonal option is cheaper.
  - W1 — pass — An informative title and six coherent short paragraphs support scanning and continuous argument without padding.
  - L1 — pass — Natural Swedish advocacy such as 'Sex fasta uttag behöver motiveras' keeps a firm but factual voice.
  - L2 — pass — Swedish date order, compounds and punctuation are consistent.
  - T1 — pass — Actual resource reads and final metadata honour `opinion/sv/none`; no technique is inferred from text shape.
  - R1 — pass — The review preserves the working text, voice, claims, quotations and metadata without preference-driven correction.
  - R2 — pass — Full scoped review resources were read, no correction was needed, and exactly one installed Proofread invocation closed the run with no subsequent substantive edit; [native audit](../editorial-329/followup/runs/candidate/opinion-unknown-sv-r1/redline/native-audit.json).
  - O1 — pass — The observed delivery honours the response target and inventories show unchanged inputs/resources with no surviving work or scratch artifacts.
  - S1 — skipped — Source-aware comparison belongs to Write; this invocation intentionally receives only the artifact.
- **unresolved findings** — none
- **defects filed** — none from this Redline artifact
- **notes** — The final artifact remains independently source-faithful. Optional supported material need not be added, and no unseen-source verification is attributed to this pass.

## `opinion-unknown-sv-r2`

- **fixture** — `opinion-unknown-sv-r2`, complete preceding Write artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status after editorial review and one final mechanical pass; the input is final. [Full response](../editorial-329/followup/runs/candidate/opinion-unknown-sv-r2/redline/response.txt), [final artifact](../editorial-329/followup/runs/candidate/opinion-unknown-sv-r2/redline/artifact.md), [supplied input](../editorial-329/followup/runs/candidate/opinion-unknown-sv-r2/redline/supplied-input.md).
- **side effects** — No surviving Skill changes; native Harness state only. [Full differences](../editorial-329/followup/runs/candidate/opinion-unknown-sv-r2/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/candidate/opinion-unknown-sv-r2/redline/cleanup.json).
- **criteria** —
  - G1 — pass — The writer keeps Kajliv's demand for a comparison and supports developing the harbour without endorsing the permanent option.
  - G2 — pass — Early thesis, real objection and a named board action at the end provide a complete opinion piece.
  - P1 — pass — The timing ambiguity found by the first checker is repaired without changing the requested decision; the argument then follows coherently.
  - W1 — pass — Compact paragraphs keep the booking evidence, alternative comparison and final request distinguishable.
  - L1 — pass — Idiomatic Swedish connects the practical alternatives without translated constructions or inflated rhetoric.
  - L2 — pass — Dates, numeral use and Swedish punctuation remain appropriate.
  - T1 — pass — Actual resource reads and final metadata honour `opinion/sv/none`; no technique is inferred from text shape.
  - R1 — pass — The review preserves the working text, voice, claims, quotations and metadata without preference-driven correction.
  - R2 — pass — Full scoped review resources were read, no correction was needed, and exactly one installed Proofread invocation closed the run with no subsequent substantive edit; [native audit](../editorial-329/followup/runs/candidate/opinion-unknown-sv-r2/redline/native-audit.json).
  - O1 — pass — The observed delivery honours the response target and inventories show unchanged inputs/resources with no surviving work or scratch artifacts.
  - S1 — skipped — Source-aware comparison belongs to Write; this invocation intentionally receives only the artifact.
- **unresolved findings** — none
- **defects filed** — none from this Redline artifact
- **notes** — The final artifact remains independently source-faithful. Optional supported material need not be added, and no unseen-source verification is attributed to this pass.

## `opinion-absence-en_GB-r1`

- **fixture** — `opinion-absence-en_GB-r1`, complete preceding Write artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status after editorial review and one final mechanical pass; the input is final. [Full response](../editorial-329/followup/runs/candidate/opinion-absence-en_GB-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/candidate/opinion-absence-en_GB-r1/redline/artifact.md), [supplied input](../editorial-329/followup/runs/candidate/opinion-absence-en_GB-r1/redline/supplied-input.md).
- **side effects** — No surviving Skill changes; native Harness state only. [Full differences](../editorial-329/followup/runs/candidate/opinion-absence-en_GB-r1/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/candidate/opinion-absence-en_GB-r1/redline/cleanup.json).
- **criteria** —
  - G1 — pass — Reed argues for investigation while conceding the trustees' maintenance-income concern and the possible merits of letting.
  - G2 — pass — The early position, nine-of-fourteen survey limits, real financial objection and final trustee decision form a complete opinion argument.
  - P1 — pass — Expressions of interest remain distinct from bookings or income promises, and a proposed timetable remains distinct from established feasibility.
  - W1 — pass — The informative title and six topic-focused paragraphs offer a clear route from choice to evidence and action.
  - L1 — pass — British English phrases such as 'commercial letting' and 'pay its way' sound natural in the policy context.
  - L2 — pass — British date order and punctuation are consistent, with no imported US date or currency convention.
  - T1 — pass — Actual resource reads and final metadata honour `opinion/en_GB/none`; no technique is inferred from text shape.
  - R1 — pass — The review preserves the working text, voice, claims, quotations and metadata without preference-driven correction.
  - R2 — pass — Full scoped review resources were read, no correction was needed, and exactly one installed Proofread invocation closed the run with no subsequent substantive edit; [native audit](../editorial-329/followup/runs/candidate/opinion-absence-en_GB-r1/redline/native-audit.json).
  - O1 — pass — The observed delivery honours the response target and inventories show unchanged inputs/resources with no surviving work or scratch artifacts.
  - S1 — skipped — Source-aware comparison belongs to Write; this invocation intentionally receives only the artifact.
- **unresolved findings** — none
- **defects filed** — none from this Redline artifact
- **notes** — The final artifact remains independently source-faithful. Optional supported material need not be added, and no unseen-source verification is attributed to this pass.

## `opinion-absence-en_GB-r2`

- **fixture** — `opinion-absence-en_GB-r2`, complete preceding Write artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Unchanged prose and metadata were repeated with one unresolved timetable finding; the extracted copy differs only by one trailing blank line. [Full response](../editorial-329/followup/runs/candidate/opinion-absence-en_GB-r2/redline/response.txt), [final artifact](../editorial-329/followup/runs/candidate/opinion-absence-en_GB-r2/redline/artifact.md), [supplied input](../editorial-329/followup/runs/candidate/opinion-absence-en_GB-r2/redline/supplied-input.md).
- **side effects** — No surviving Skill changes; native Harness state only. [Full differences](../editorial-329/followup/runs/candidate/opinion-absence-en_GB-r2/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/candidate/opinion-absence-en_GB-r2/redline/cleanup.json).
- **criteria** —
  - G1 — pass — The author's firm proposal and willingness to consider commercial letting both survive.
  - G2 — pass — Thesis, evidence, genuine financial objection and specific decision remain present without neutralising advocacy.
  - P1 — pass — The requested timetable is expressly uncertain, not a factual guarantee that the study will finish; that distinction is coherent in an opinion piece.
  - W1 — pass — Each paragraph has a clear role and the concluding request is easy to find.
  - L1 — pass — The prose reads as natural British policy advocacy, with measured concessions and a direct final request.
  - L2 — pass — British date order and spelling remain consistent.
  - T1 — pass — Actual resource reads and final metadata honour `opinion/en_GB/none`; no technique is inferred from text shape.
  - R1 — fail — Qualitative contract failure: a stated request for eight weeks, expressly qualified by uncertain completion, is treated as requiring proof of feasibility or a changed proposal. The correction properly preserves the author's position, but the finding is a false positive.
  - R2 — pass — Full scoped review resources were read, one fresh correction used the default budget and was re-reviewed, and exactly one installed Proofread invocation closed the run with no subsequent substantive edit; [native audit](../editorial-329/followup/runs/candidate/opinion-absence-en_GB-r2/redline/native-audit.json).
  - O1 — skipped — Filesystem preservation and cleanup pass, but the response/no-change branch has conflicting instructions: Redline step 11 requires an artifact when findings remain while shared delivery says status only. The repetition cannot fairly be scored as clear model disobedience.
  - S1 — skipped — Source-aware comparison belongs to Write; this invocation intentionally receives only the artifact.
- **unresolved findings** — The review's timetable finding, judged false positive by the evaluator.
- **defects filed** — [#354](https://github.com/Kntnt/skills/issues/354), timetable false positive; [#353](https://github.com/Kntnt/skills/issues/353), delivery-rule collision.
- **notes** — The artifact remains source-faithful; the failure concerns the review judgement, not invented prose or changed advocacy. The original provisional delivery-violation claim is explicitly corrected in the linked observation.

## `case-unprompted-en_US-r1`

- **fixture** — `case-unprompted-en_US-r1`, complete preceding Write artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status after editorial review and one final mechanical pass; the input is final. [Full response](../editorial-329/followup/runs/candidate/case-unprompted-en_US-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/candidate/case-unprompted-en_US-r1/redline/artifact.md), [supplied input](../editorial-329/followup/runs/candidate/case-unprompted-en_US-r1/redline/supplied-input.md).
- **side effects** — No surviving Skill changes; native Harness state only. [Full differences](../editorial-329/followup/runs/candidate/case-unprompted-en_US-r1/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/candidate/case-unprompted-en_US-r1/redline/cleanup.json).
- **criteria** —
  - G1 — pass — The archive remains the actor choosing descriptions and checking records; Index Lantern's implementation role is specific.
  - G2 — pass — Title, ingress, background, choices, bounded results and qualified customer appraisal cover the case's distinct functions.
  - P1 — pass — The trial note's lack of time, cost and public-access measurements prevents unsupported success inferences.
  - W1 — pass — Short connected paragraphs and quote bridges make the compact case readable without requiring section headings.
  - L1 — pass — American archive vocabulary and natural quotation framing read fluently.
  - L2 — pass — American 'programs', 'catalog' and May 6 date order are appropriate.
  - T1 — pass — Actual resource reads and final metadata honour `case-study/en_US/none`; no technique is inferred from text shape.
  - R1 — pass — The review preserves the working text, voice, claims, quotations and metadata without preference-driven correction.
  - R2 — pass — Full scoped review resources were read, no correction was needed, and exactly one installed Proofread invocation closed the run with no subsequent substantive edit; [native audit](../editorial-329/followup/runs/candidate/case-unprompted-en_US-r1/redline/native-audit.json).
  - O1 — pass — The observed delivery honours the response target and inventories show unchanged inputs/resources with no surviving work or scratch artifacts.
  - S1 — skipped — Source-aware comparison belongs to Write; this invocation intentionally receives only the artifact.
- **unresolved findings** — none
- **defects filed** — none from this Redline artifact
- **notes** — The final artifact remains independently source-faithful. Optional supported material need not be added, and no unseen-source verification is attributed to this pass.

## `case-unprompted-en_US-r2`

- **fixture** — `case-unprompted-en_US-r2`, complete preceding Write artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status after editorial review and one final mechanical pass; the input is final. [Full response](../editorial-329/followup/runs/candidate/case-unprompted-en_US-r2/redline/response.txt), [final artifact](../editorial-329/followup/runs/candidate/case-unprompted-en_US-r2/redline/artifact.md), [supplied input](../editorial-329/followup/runs/candidate/case-unprompted-en_US-r2/redline/supplied-input.md).
- **side effects** — No surviving Skill changes; native Harness state only. [Full differences](../editorial-329/followup/runs/candidate/case-unprompted-en_US-r2/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/candidate/case-unprompted-en_US-r2/redline/cleanup.json).
- **criteria** —
  - G1 — pass — Customer decisions, supplier assistance and the qualified extension decision remain distinguishable.
  - G2 — pass — The result-bearing ingress, explanatory narrative, bounded evidence and actual customer appraisal perform useful separate jobs.
  - P1 — pass — Shared access is reported without turning it into measured time saving or an assured rollout to older records.
  - W1 — pass — The short case balances narrative and quotations, with the disclosure separated at the end.
  - L1 — pass — The English reads naturally, including 'bring in the older collection', without translated syntax.
  - L2 — pass — American 'programs', 'catalog' and date presentation stay consistent.
  - T1 — pass — Actual resource reads and final metadata honour `case-study/en_US/none`; no technique is inferred from text shape.
  - R1 — pass — The review preserves the working text, voice, claims, quotations and metadata without preference-driven correction.
  - R2 — pass — Full scoped review resources were read, no correction was needed, and exactly one installed Proofread invocation closed the run with no subsequent substantive edit; [native audit](../editorial-329/followup/runs/candidate/case-unprompted-en_US-r2/redline/native-audit.json).
  - O1 — pass — The observed delivery honours the response target and inventories show unchanged inputs/resources with no surviving work or scratch artifacts.
  - S1 — skipped — Source-aware comparison belongs to Write; this invocation intentionally receives only the artifact.
- **unresolved findings** — none
- **defects filed** — none from this Redline artifact
- **notes** — The final artifact remains independently source-faithful. Optional supported material need not be added, and no unseen-source verification is attributed to this pass.

## `case-question-en_GB-r1`

- **fixture** — `case-question-en_GB-r1`, complete preceding Write artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status after editorial review and one final mechanical pass; the input is final. [Full response](../editorial-329/followup/runs/candidate/case-question-en_GB-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/candidate/case-question-en_GB-r1/redline/artifact.md), [supplied input](../editorial-329/followup/runs/candidate/case-question-en_GB-r1/redline/supplied-input.md).
- **side effects** — No surviving Skill changes; native Harness state only. [Full differences](../editorial-329/followup/runs/candidate/case-question-en_GB-r1/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/candidate/case-question-en_GB-r1/redline/cleanup.json).
- **criteria** —
  - G1 — pass — The repair workshop's decisions and reported practical experience drive the case, with Benchline in third person.
  - G2 — pass — The approved-use headline, independent ingress, context, implementation and genuine customer appraisal form a complete case.
  - P1 — pass — The revised headline reports approved use instead of an unsupported causal visibility change, while the evidence remains explicitly non-measured.
  - W1 — pass — The ingress and lead do different work and quotations are prepared by short connective passages.
  - L1 — pass — Natural British workshop language preserves the customer's specific reservation.
  - L2 — pass — British date order and single quotation marks remain appropriate.
  - T1 — pass — Actual resource reads and final metadata honour `case-study/en_GB/none`; no technique is inferred from text shape.
  - R1 — pass — The review preserves the working text, voice, claims, quotations and metadata without preference-driven correction.
  - R2 — pass — Full scoped review resources were read, no correction was needed, and exactly one installed Proofread invocation closed the run with no subsequent substantive edit; [native audit](../editorial-329/followup/runs/candidate/case-question-en_GB-r1/redline/native-audit.json).
  - O1 — pass — The observed delivery honours the response target and inventories show unchanged inputs/resources with no surviving work or scratch artifacts.
  - S1 — skipped — Source-aware comparison belongs to Write; this invocation intentionally receives only the artifact.
- **unresolved findings** — none
- **defects filed** — none from this Redline artifact
- **notes** — The final artifact remains independently source-faithful. Optional supported material need not be added, and no unseen-source verification is attributed to this pass.

## `case-question-en_GB-r2`

- **fixture** — `case-question-en_GB-r2`, complete preceding Write artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status after editorial review and one final mechanical pass; the input is final. [Full response](../editorial-329/followup/runs/candidate/case-question-en_GB-r2/redline/response.txt), [final artifact](../editorial-329/followup/runs/candidate/case-question-en_GB-r2/redline/artifact.md), [supplied input](../editorial-329/followup/runs/candidate/case-question-en_GB-r2/redline/supplied-input.md).
- **side effects** — No surviving Skill changes; native Harness state only. [Full differences](../editorial-329/followup/runs/candidate/case-question-en_GB-r2/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/candidate/case-question-en_GB-r2/redline/cleanup.json).
- **criteria** —
  - G1 — pass — The workshop remains responsible for status definitions and adoption decisions; supplier assistance is bounded.
  - G2 — pass — Customer result, situation, implementation, evidence limits and actual appraisal provide the case's required functions.
  - P1 — pass — Reported usefulness stays separate from faster repairs, revenue and customer-satisfaction claims.
  - W1 — pass — The result-bearing ingress and chronological lead allow both independent entry and continuous reading.
  - L1 — pass — The British prose is fluent and the quoted workshop experience remains distinctive.
  - L2 — pass — Single quotation marks and British date order are consistent.
  - T1 — pass — Actual resource reads and final metadata honour `case-study/en_GB/none`; no technique is inferred from text shape.
  - R1 — pass — The review preserves the working text, voice, claims, quotations and metadata without preference-driven correction.
  - R2 — pass — Full scoped review resources were read, no correction was needed, and exactly one installed Proofread invocation closed the run with no subsequent substantive edit; [native audit](../editorial-329/followup/runs/candidate/case-question-en_GB-r2/redline/native-audit.json).
  - O1 — pass — The observed delivery honours the response target and inventories show unchanged inputs/resources with no surviving work or scratch artifacts.
  - S1 — skipped — Source-aware comparison belongs to Write; this invocation intentionally receives only the artifact.
- **unresolved findings** — none
- **defects filed** — none from this Redline artifact
- **notes** — The final artifact remains independently source-faithful. Optional supported material need not be added, and no unseen-source verification is attributed to this pass.

## `article-sv-r1`

- **fixture** — `article-sv-r1`, complete preceding Write artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status after editorial review and one final mechanical pass; the input is final. [Full response](../editorial-329/followup/runs/candidate/article-sv-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/candidate/article-sv-r1/redline/artifact.md), [supplied input](../editorial-329/followup/runs/candidate/article-sv-r1/redline/supplied-input.md).
- **side effects** — No surviving Skill changes; native Harness state only. [Full differences](../editorial-329/followup/runs/candidate/article-sv-r1/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/candidate/article-sv-r1/redline/cleanup.json).
- **criteria** —
  - G1 — pass — The article explains what the short measurement trial can tell property managers and how to use it cautiously.
  - G2 — pass — Informative headline, self-contained ingress, separate lead, explanatory H2 sections and an actionable ending are present without an invented byline.
  - P1 — pass — Sensor location and operative temperature are explained before their implications; no causal, health, legal or norm-comparison inference is added.
  - W1 — pass — The three informative sections separate duration, measurement meaning and follow-up while preserving substantive technical explanation.
  - L1 — pass — The Swedish is idiomatic and professionally explanatory, including the brief definition of temperature series.
  - L2 — pass — Swedish date and temperature forms and the speech dash are appropriate.
  - T1 — pass — Actual resource reads and final metadata honour `article/sv/none`; no technique is inferred from text shape.
  - R1 — pass — The review preserves the working text, voice, claims, quotations and metadata without preference-driven correction.
  - R2 — pass — Full scoped review resources were read, no correction was needed, and exactly one installed Proofread invocation closed the run with no subsequent substantive edit; [native audit](../editorial-329/followup/runs/candidate/article-sv-r1/redline/native-audit.json).
  - O1 — pass — The observed delivery honours the response target and inventories show unchanged inputs/resources with no surviving work or scratch artifacts.
  - S1 — skipped — Source-aware comparison belongs to Write; this invocation intentionally receives only the artifact.
- **unresolved findings** — none
- **defects filed** — none from this Redline artifact
- **notes** — The final artifact remains independently source-faithful. Optional supported material need not be added, and no unseen-source verification is attributed to this pass.

## `column-sv-r1`

- **fixture** — `column-sv-r1`, complete preceding Write artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status after editorial review and one final mechanical pass; the input is final. [Full response](../editorial-329/followup/runs/candidate/column-sv-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/candidate/column-sv-r1/redline/artifact.md), [supplied input](../editorial-329/followup/runs/candidate/column-sv-r1/redline/supplied-input.md).
- **side effects** — No surviving Skill changes; native Harness state only. [Full differences](../editorial-329/followup/runs/candidate/column-sv-r1/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/candidate/column-sv-r1/redline/cleanup.json).
- **criteria** —
  - G1 — pass — The author's self-irony about adding another form field carries a personal reflection instead of a campaign.
  - G2 — pass — Title, supplied byline, document-based opening, developing reflection and unresolved ending fit the column.
  - P1 — pass — The value of non-decision conversations and uncertainty about the extra field remain part of the argument.
  - W1 — pass — Seven coherent paragraphs vary the rhythm without unnecessary section headings.
  - L1 — pass — Natural Swedish self-irony and the recurring question maintain a recognisable personal voice.
  - L2 — pass — The integrated lower-case question after the colon is valid Swedish and should remain unchanged.
  - T1 — pass — Actual resource reads and final metadata honour `column/sv/none`; no technique is inferred from text shape.
  - R1 — pass — The review preserves the working text, voice, claims, quotations and metadata without preference-driven correction.
  - R2 — pass — Full scoped review resources were read, no correction was needed, and exactly one installed Proofread invocation closed the run with no subsequent substantive edit; [native audit](../editorial-329/followup/runs/candidate/column-sv-r1/redline/native-audit.json).
  - O1 — pass — The observed delivery honours the response target and inventories show unchanged inputs/resources with no surviving work or scratch artifacts.
  - S1 — skipped — Source-aware comparison belongs to Write; this invocation intentionally receives only the artifact.
- **unresolved findings** — none
- **defects filed** — none from this Redline artifact
- **notes** — The final artifact remains independently source-faithful. Optional supported material need not be added, and no unseen-source verification is attributed to this pass.

## `web-copy-en_US-r1`

- **fixture** — `web-copy-en_US-r1`, complete preceding Write artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — One redundant preparation sentence was removed; all substantive claims survive and two publication gaps are reported. [Full response](../editorial-329/followup/runs/candidate/web-copy-en_US-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/candidate/web-copy-en_US-r1/redline/artifact.md), [supplied input](../editorial-329/followup/runs/candidate/web-copy-en_US-r1/redline/supplied-input.md).
- **side effects** — No surviving Skill changes; native Harness state only. [Full differences](../editorial-329/followup/runs/candidate/web-copy-en_US-r1/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/candidate/web-copy-en_US-r1/redline/cleanup.json).
- **criteria** —
  - G1 — pass — The page helps a cooperative board assess fit and understand the consequence of expressing interest.
  - G2 — pass — Scope, deliverables, preparation, exclusions, price and next-step expectations are easy to locate.
  - P1 — pass — The benefit stays with a shared understanding and possible simplifications, with no promised savings or conflict reduction.
  - W1 — pass — Task-based headings, two useful deliverable bullets and explicit link microcopy support direct entry and action.
  - L1 — pass — The American English is fluent and practical without importing Swedish syntax.
  - L2 — pass — American 'email' and 'business days' are natural, while SEK and VAT remain the source's currency and tax terms.
  - T1 — pass — Actual resource reads and final metadata honour `web-copy/en_US/none`; no technique is inferred from text shape.
  - R1 — pass — The correction removes only the second sentence restating the required preparation materials; the preceding sentence preserves that requirement and the account names the removal. Unknown terms and placeholder destination remain explicit rather than invented.
  - R2 — pass — Full scoped review resources were read, one fresh correction used the default budget and was re-reviewed, and exactly one installed Proofread invocation closed the run with no subsequent substantive edit; [native audit](../editorial-329/followup/runs/candidate/web-copy-en_US-r1/redline/native-audit.json).
  - O1 — pass — The observed delivery honours the response target and inventories show unchanged inputs/resources with no surviving work or scratch artifacts.
  - S1 — skipped — Source-aware comparison belongs to Write; this invocation intentionally receives only the artifact.
- **unresolved findings** — Payment terms and summary delivery timing are unspecified; the form URL is a placeholder.
- **defects filed** — none from this Redline artifact
- **notes** — The .invalid URL is deliberately inert synthetic material. Its publication-readiness finding does not license replacing the supplied destination or claiming the form books/pays; neither happened. These reported gaps do not add unsupported facts.

## `general-en_GB-r1`

- **fixture** — `general-en_GB-r1`, complete preceding Write artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change status after editorial review and one final mechanical pass; the input is final. [Full response](../editorial-329/followup/runs/candidate/general-en_GB-r1/redline/response.txt), [final artifact](../editorial-329/followup/runs/candidate/general-en_GB-r1/redline/artifact.md), [supplied input](../editorial-329/followup/runs/candidate/general-en_GB-r1/redline/supplied-input.md).
- **side effects** — No surviving Skill changes; native Harness state only. [Full differences](../editorial-329/followup/runs/candidate/general-en_GB-r1/redline/filesystem-changes.json), [cleanup](../editorial-329/followup/runs/candidate/general-en_GB-r1/redline/cleanup.json).
- **criteria** —
  - G1 — pass — The article brief becomes a useful explanation for property managers under the explicitly selected general genre.
  - G2 — pass — A clear title, summary and explanatory headings serve the brief without inventing a byline or imposing unselected genre rules.
  - P1 — pass — Measurement limits are explained before the practical recommendation, and neither correlation nor timing becomes a causal conclusion.
  - W1 — pass — The question/measurement/follow-up sections support both scanning and sustained technical understanding.
  - L1 — pass — Natural British English includes 'draughts', 'school caretaker' and a fluent but faithful translated quotation.
  - L2 — pass — British date order, single quotation marks and Celsius are preserved without conversion.
  - T1 — pass — Actual resource reads and final metadata honour `general/en_GB/none`; no technique is inferred from text shape.
  - R1 — pass — The review preserves the working text, voice, claims, quotations and metadata without preference-driven correction.
  - R2 — pass — Full scoped review resources were read, no correction was needed, and exactly one installed Proofread invocation closed the run with no subsequent substantive edit; [native audit](../editorial-329/followup/runs/candidate/general-en_GB-r1/redline/native-audit.json).
  - O1 — pass — The observed delivery honours the response target and inventories show unchanged inputs/resources with no surviving work or scratch artifacts.
  - S1 — skipped — Source-aware comparison belongs to Write; this invocation intentionally receives only the artifact.
- **unresolved findings** — none
- **defects filed** — none from this Redline artifact
- **notes** — The final artifact remains independently source-faithful. Optional supported material need not be added, and no unseen-source verification is attributed to this pass.
