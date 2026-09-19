# Write — supplementary baseline for source fidelity

- **record** — `write-gpt-2026-09-19-349-followup-baseline`
- **date** — `2026-09-19` (all native session timestamps are on this UTC date)
- **ticket** — #329, #349, #352
- **skill** — `write`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`, confirmed in all eight native sessions
- **harness** — Codex CLI 0.155.1
- **corpus commit** — `bf14dc2` supplementary matrix/packages; original opinion and customer-case source bytes remain identical to frozen `6e531f5`
- **instruction revision** — `7ff6ec048f136ad797117a71c7b148843ab2e15e`

These are the eight baseline Write invocations fixed in the [supplementary matrix](../editorial-329/followup/matrix.md), judged independently before opening candidate results. Each used a separate private native session, exact neutral invocation and complete source package. No source-aware checker or Redline was invoked. S1 is inapplicable to this baseline; no independent check was promised. T2 is inapplicable because all resolved techniques are `none`.

The [native audit](../editorial-329/followup/reviews/baseline-native-audit.json) checks full source and contract bytes in actual command outputs, identity, before/after preservation, actual side effects and root removal. Every evidence directory also retains the full response, extracted complete artifact, separate delivery account, invocation, native trace, immutable revision, inventories and cleanup receipt. Extracting artifact/account is evaluator work outside model-writable roots and changes no returned prose.

All eight completed with exit 0. F1 fails in three artifacts: both original Swedish opinion repetitions (#349), and the first original US customer case (#352 plus a previously observed #344 chronology defect). Five artifacts pass F1. These counts describe these eight observations, not reliability in general.

## `opinion-sv-r1`

- **fixture** — `opinion-sv-r1` in the supplementary matrix
- **invocation** — `/write --genre=opinion --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — One complete draft with Kntnt metadata and a separate delivery account; [artifact](../editorial-329/followup/runs/baseline/opinion-sv-r1/write/artifact.md), [account](../editorial-329/followup/runs/baseline/opinion-sv-r1/write/account.md), [full response](../editorial-329/followup/runs/baseline/opinion-sv-r1/write/response.txt).
- **side effects** — No enduring Skill-created files; command-private UV directories are removed. The inventories record 317 Harness-owned home paths (native sessions, databases/locks, caches, bundled skills/plugins and config registration). Source and all work/scratch paths are unchanged; authentication is unchanged. Complete [changes](../editorial-329/followup/runs/baseline/opinion-sv-r1/write/filesystem-changes.json), [trace](../editorial-329/followup/runs/baseline/opinion-sv-r1/write/trace.jsonl), and [cleanup](../editorial-329/followup/runs/baseline/opinion-sv-r1/write/cleanup.json).
- **criteria** —
  - **F1** — `fail` — Unsupported fact (#349): “Vi har varken kostnadsberäknat eller finansierat försöket” converts an absent claim into known absence. The unqualified statement that neither workload nor users’ reasons have been investigated also exceeds the source’s narrower limits on the documents and pilot measures.
  - **G1** — `pass` — An accountable case for keeping two booking routes leads to a named municipal decision.
  - **G2** — `pass` — The early postponement thesis, report figures, real administration objection and closing board action perform distinct jobs.
  - **P1** — `pass` — The booking denominator and absence of demographic measures are explained before the proposed wider trial; the source-strength failure is recorded under F1.
  - **W1** — `pass` — Three informative subheadings and connected paragraphs guide the argument without fragmenting it.
  - **L1** — `pass` — Natural Swedish argumentation retains the author’s precise non-opposition to digital booking.
  - **L2** — `pass` — Swedish dates, compounds and punctuation are consistent.
  - **T1** — `pass` — The exact genre and locale flags govern the artifact metadata; technique resolves to none and no technique resource is loaded.
  - **R2** — `pass` — The native trace contains the complete Write body, base, selected genre, web craft and delivery contract, plus the resolved composition scope; no review half, peer editorial pass or unselected genre is loaded.
  - **O1** — `pass` — Full inventories show unchanged source/work/scratch, no retained Skill files, unchanged authentication and only Harness-owned home effects; the private root is now absent.
- **unresolved findings** — none delivered as unresolved; any unsupported claims above are evaluation findings, not successfully reported limitations.
- **defects filed** — #349; existing defect references, no new issue created by this evaluator.
- **notes** — The completion account says the material’s gaps are reflected in the text, but that does not cure the stronger factual assertion.

## `opinion-sv-r2`

- **fixture** — `opinion-sv-r2` in the supplementary matrix
- **invocation** — `/write --genre=opinion --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — One complete draft with Kntnt metadata and a separate delivery account; [artifact](../editorial-329/followup/runs/baseline/opinion-sv-r2/write/artifact.md), [account](../editorial-329/followup/runs/baseline/opinion-sv-r2/write/account.md), [full response](../editorial-329/followup/runs/baseline/opinion-sv-r2/write/response.txt).
- **side effects** — No enduring Skill-created files; command-private UV directories are removed. The inventories record 321 Harness-owned home paths (native sessions, databases/locks, caches, bundled skills/plugins and config registration). Source and all work/scratch paths are unchanged; authentication is unchanged. Complete [changes](../editorial-329/followup/runs/baseline/opinion-sv-r2/write/filesystem-changes.json), [trace](../editorial-329/followup/runs/baseline/opinion-sv-r2/write/trace.jsonl), and [cleanup](../editorial-329/followup/runs/baseline/opinion-sv-r2/write/cleanup.json).
- **criteria** —
  - **F1** — `fail` — Unsupported fact (#349): “Försöket är varken kostnadsberäknat eller finansierat av föreningen” asserts absence of work where the source only withholds a claim.
  - **G1** — `pass` — The author argues for a defined trial while acknowledging the administration burden.
  - **G2** — `pass` — The thesis is early, evidence is attributed, the real objection is met and the board receives a concrete requested decision.
  - **P1** — `pass` — The argument distinguishes bookings from people and connects evidence gaps to the proposed measurement; F1 separately rejects the costing/funding assertion.
  - **W1** — `pass` — The evidence, objection and proposed action have useful headings and coherent paragraph lengths.
  - **L1** — `pass` — Native Swedish prose preserves the author’s non-opposition and avoids invented hostile motives.
  - **L2** — `pass` — Swedish date and number forms and ordinary punctuation are consistent.
  - **T1** — `pass` — The exact genre and locale flags govern the artifact metadata; technique resolves to none and no technique resource is loaded.
  - **R2** — `pass` — The native trace contains the complete Write body, base, selected genre, web craft and delivery contract, plus the resolved composition scope; no review half, peer editorial pass or unselected genre is loaded.
  - **O1** — `pass` — Full inventories show unchanged source/work/scratch, no retained Skill files, unchanged authentication and only Harness-owned home effects; the private root is now absent.
- **unresolved findings** — none delivered as unresolved; any unsupported claims above are evaluation findings, not successfully reported limitations.
- **defects filed** — #349; existing defect references, no new issue created by this evaluator.
- **notes** — A second fresh repetition reproduces the defect with different grammatical framing; no first-person explanation suffices.

## `case-study-en_US-r1`

- **fixture** — `case-study-en_US-r1` in the supplementary matrix
- **invocation** — `/write --genre=case-study --language=en_US --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — One complete draft with Kntnt metadata and a separate delivery account; [artifact](../editorial-329/followup/runs/baseline/case-study-en_US-r1/write/artifact.md), [account](../editorial-329/followup/runs/baseline/case-study-en_US-r1/write/account.md), [full response](../editorial-329/followup/runs/baseline/case-study-en_US-r1/write/response.txt).
- **side effects** — No enduring Skill-created files; command-private UV directories are removed. The inventories record 317 Harness-owned home paths (native sessions, databases/locks, caches, bundled skills/plugins and config registration). Source and all work/scratch paths are unchanged; authentication is unchanged. Complete [changes](../editorial-329/followup/runs/baseline/case-study-en_US-r1/write/filesystem-changes.json), [trace](../editorial-329/followup/runs/baseline/case-study-en_US-r1/write/trace.jsonl), and [cleanup](../editorial-329/followup/runs/baseline/case-study-en_US-r1/write/cleanup.json).
- **criteria** —
  - **F1** — `fail` — Unsupported facts: “Asked to assess the experience” invents an interview request (#352), and “began the trial in September 2025” turns the supplied decision date into a start date (previously recorded #344 class).
  - **G1** — `pass` — Operations managers learn the customer’s workflow choices, bounded trial result and qualified appraisal.
  - **G2** — `pass` — Headline, ingress, customer action, supplier role, measurements and actual customer appraisal are present; publisher stance is disclosed.
  - **P1** — `pass` — The narrative separates assignment from completion and correlation from causation; the unsupported chronology and interview circumstance are rejected under F1.
  - **W1** — `pass` — A concise ingress and connected short narrative paragraphs make the case readable without needing extra section headings.
  - **L1** — `pass` — Natural American narration and intact customer quotations retain a professional customer-case voice.
  - **L2** — `pass` — American apartments, date order and double quotation marks are consistent.
  - **T1** — `pass` — The exact genre and locale flags govern the artifact metadata; technique resolves to none and no technique resource is loaded.
  - **R2** — `pass` — The native trace contains the complete Write body, base, selected genre, web craft and delivery contract, plus the resolved composition scope; no review half, peer editorial pass or unselected genre is loaded.
  - **O1** — `pass` — Full inventories show unchanged source/work/scratch, no retained Skill files, unchanged authentication and only Harness-owned home effects; the private root is now absent.
- **unresolved findings** — none delivered as unresolved; any unsupported claims above are evaluation findings, not successfully reported limitations.
- **defects filed** — #352; related retained defect class #344; existing defect references, no new issue created by this evaluator.
- **notes** — This baseline recurrence of an old chronology defect is recorded without attributing it to the new candidate.

## `case-study-en_US-r2`

- **fixture** — `case-study-en_US-r2` in the supplementary matrix
- **invocation** — `/write --genre=case-study --language=en_US --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — One complete draft with Kntnt metadata and a separate delivery account; [artifact](../editorial-329/followup/runs/baseline/case-study-en_US-r2/write/artifact.md), [account](../editorial-329/followup/runs/baseline/case-study-en_US-r2/write/account.md), [full response](../editorial-329/followup/runs/baseline/case-study-en_US-r2/write/response.txt).
- **side effects** — No enduring Skill-created files; command-private UV directories are removed. The inventories record 317 Harness-owned home paths (native sessions, databases/locks, caches, bundled skills/plugins and config registration). Source and all work/scratch paths are unchanged; authentication is unchanged. Complete [changes](../editorial-329/followup/runs/baseline/case-study-en_US-r2/write/filesystem-changes.json), [trace](../editorial-329/followup/runs/baseline/case-study-en_US-r2/write/trace.jsonl), and [cleanup](../editorial-329/followup/runs/baseline/case-study-en_US-r2/write/cleanup.json).
- **criteria** —
  - **F1** — `pass` — September remains the decision date, interview attribution stays with the supplied email, all three quotations preserve their qualifications, and the figures retain workload and causal limits.
  - **G1** — `pass` — The case gives an operations reader concrete implementation choices and the customer’s own judgement.
  - **G2** — `pass` — The customer remains the actor; the supplier is third person, publication is disclosed, and appraisal is not inferred from the figures.
  - **P1** — `pass` — Purpose, setup, evidence, appraisal and the pending expansion decision follow intelligibly, with no unsupported question framing.
  - **W1** — `pass` — The independent ingress and continuous paragraph sequence orient the reader; the brief source-limit sentence does not obstruct the account.
  - **L1** — `pass` — Idiomatic American narration and the original speaker’s voice coexist without promotional inflation.
  - **L2** — `pass` — American spelling, December 4 date order and quotation punctuation are coherent.
  - **T1** — `pass` — The exact genre and locale flags govern the artifact metadata; technique resolves to none and no technique resource is loaded.
  - **R2** — `pass` — The native trace contains the complete Write body, base, selected genre, web craft and delivery contract, plus the resolved composition scope; no review half, peer editorial pass or unselected genre is loaded.
  - **O1** — `pass` — Full inventories show unchanged source/work/scratch, no retained Skill files, unchanged authentication and only Harness-owned home effects; the private root is now absent.
- **unresolved findings** — none delivered as unresolved; any unsupported claims above are evaluation findings, not successfully reported limitations.
- **defects filed** — none; existing defect references, no new issue created by this evaluator.
- **notes** — This independent repetition passes F1; it does not erase the first repetition’s failure.

## `opinion-unknown-sv-r1`

- **fixture** — `opinion-unknown-sv-r1` in the supplementary matrix
- **invocation** — `/write --genre=opinion --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — One complete draft with Kntnt metadata and a separate delivery account; [artifact](../editorial-329/followup/runs/baseline/opinion-unknown-sv-r1/write/artifact.md), [account](../editorial-329/followup/runs/baseline/opinion-unknown-sv-r1/write/account.md), [full response](../editorial-329/followup/runs/baseline/opinion-unknown-sv-r1/write/response.txt).
- **side effects** — No enduring Skill-created files; command-private UV directories are removed. The inventories record 317 Harness-owned home paths (native sessions, databases/locks, caches, bundled skills/plugins and config registration). Source and all work/scratch paths are unchanged; authentication is unchanged. Complete [changes](../editorial-329/followup/runs/baseline/opinion-unknown-sv-r1/write/filesystem-changes.json), [trace](../editorial-329/followup/runs/baseline/opinion-unknown-sv-r1/write/trace.jsonl), and [cleanup](../editorial-329/followup/runs/baseline/opinion-unknown-sv-r1/write/cleanup.json).
- **criteria** —
  - **F1** — `pass` — The draft does not claim that Kajliv lacks an estimate or permission; it confines factual gaps to the supplied material and makes no claim that the seasonal option is cheaper.
  - **G1** — `pass` — The harbour board is asked to compare two concrete alternatives before choosing an installation.
  - **G2** — `pass` — An early thesis, attributed company rationale, bounded booking count and explicit closing action support a recognisable opinion article.
  - **P1** — `pass` — The 18 booked days are kept distinct from visitor numbers and income; the requested comparison follows from the stated information gaps.
  - **W1** — `pass` — Six connected paragraphs with a specific headline provide a clear short web argument without requiring artificial subheadings.
  - **L1** — `pass` — Natural Swedish phrasing sustains firm advocacy while respecting the company’s stated rationale.
  - **L2** — `pass` — Swedish compounds, dates and number forms are consistent.
  - **T1** — `pass` — The exact genre and locale flags govern the artifact metadata; technique resolves to none and no technique resource is loaded.
  - **R2** — `pass` — The native trace contains the complete Write body, base, selected genre, web craft and delivery contract, plus the resolved composition scope; no review half, peer editorial pass or unselected genre is loaded.
  - **O1** — `pass` — Full inventories show unchanged source/work/scratch, no retained Skill files, unchanged authentication and only Harness-owned home effects; the private root is now absent.
- **unresolved findings** — none delivered as unresolved; any unsupported claims above are evaluation findings, not successfully reported limitations.
- **defects filed** — none; existing defect references, no new issue created by this evaluator.
- **notes** — The optional statement about the association’s own missing claim is omitted. This is a valid draft, but supplies no evidence that this run could explicitly restate that distinction correctly.

## `opinion-absence-en_GB-r1`

- **fixture** — `opinion-absence-en_GB-r1` in the supplementary matrix
- **invocation** — `/write --genre=opinion --language=en_GB --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — One complete draft with Kntnt metadata and a separate delivery account; [artifact](../editorial-329/followup/runs/baseline/opinion-absence-en_GB-r1/write/artifact.md), [account](../editorial-329/followup/runs/baseline/opinion-absence-en_GB-r1/write/account.md), [full response](../editorial-329/followup/runs/baseline/opinion-absence-en_GB-r1/write/response.txt).
- **side effects** — No enduring Skill-created files; command-private UV directories are removed. The inventories record 317 Harness-owned home paths (native sessions, databases/locks, caches, bundled skills/plugins and config registration). Source and all work/scratch paths are unchanged; authentication is unchanged. Complete [changes](../editorial-329/followup/runs/baseline/opinion-absence-en_GB-r1/write/filesystem-changes.json), [trace](../editorial-329/followup/runs/baseline/opinion-absence-en_GB-r1/write/trace.jsonl), and [cleanup](../editorial-329/followup/runs/baseline/opinion-absence-en_GB-r1/write/cleanup.json).
- **criteria** —
  - **F1** — `pass` — The signed treasurer note supports “we have not prepared a conversion cost estimate”; the distinct owner-consent status is explicitly left unestablished. Interest remains nonbinding and eight weeks remains a requested timetable.
  - **G1** — `pass` — Residents receive a clear case for a feasibility study that takes predictable rental income seriously.
  - **G2** — `pass` — Early position, 9-of-14 survey support, fair financial objection and named trustee action are all present.
  - **P1** — `pass` — The draft separates interest from bookings, estimate absence from unknown consent, and a desired timetable from established feasibility.
  - **W1** — `pass` — A specific headline and coherent topical paragraphs let readers follow a compact argument without arbitrary segmentation.
  - **L1** — `pass` — Natural British opinion prose preserves the author’s conditional acceptance of commercial letting.
  - **L2** — `pass` — British date order and spelling are maintained.
  - **T1** — `pass` — The exact genre and locale flags govern the artifact metadata; technique resolves to none and no technique resource is loaded.
  - **R2** — `pass` — The native trace contains the complete Write body, base, selected genre, web craft and delivery contract, plus the resolved composition scope; no review half, peer editorial pass or unselected genre is loaded.
  - **O1** — `pass` — Full inventories show unchanged source/work/scratch, no retained Skill files, unchanged authentication and only Harness-owned home effects; the private root is now absent.
- **unresolved findings** — none delivered as unresolved; any unsupported claims above are evaluation findings, not successfully reported limitations.
- **defects filed** — none; existing defect references, no new issue created by this evaluator.
- **notes** — Positive control is exercised rather than omitted: warranted categorical absence and unclaimed consent both appear with the correct asymmetry.

## `case-unprompted-en_US-r1`

- **fixture** — `case-unprompted-en_US-r1` in the supplementary matrix
- **invocation** — `/write --genre=case-study --language=en_US --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — One complete draft with Kntnt metadata and a separate delivery account; [artifact](../editorial-329/followup/runs/baseline/case-unprompted-en_US-r1/write/artifact.md), [account](../editorial-329/followup/runs/baseline/case-unprompted-en_US-r1/write/account.md), [full response](../editorial-329/followup/runs/baseline/case-unprompted-en_US-r1/write/response.txt).
- **side effects** — No enduring Skill-created files; command-private UV directories are removed. The inventories record 319 Harness-owned home paths (native sessions, databases/locks, caches, bundled skills/plugins and config registration). Source and all work/scratch paths are unchanged; authentication is unchanged. Complete [changes](../editorial-329/followup/runs/baseline/case-unprompted-en_US-r1/write/filesystem-changes.json), [trace](../editorial-329/followup/runs/baseline/case-unprompted-en_US-r1/write/trace.jsonl), and [cleanup](../editorial-329/followup/runs/baseline/case-unprompted-en_US-r1/write/cleanup.json).
- **criteria** —
  - **F1** — `pass` — Ortiz is attributed to the supplied publication email without an invented interview question, visit or emotional reaction; the 47 donations, 11 uncertain dates and limited outcomes remain supported.
  - **G1** — `pass` — Archive managers learn how the customer selected fields, retained uncertainty and judges the limited pilot.
  - **G2** — `pass` — The customer owns the descriptions and checks; supplier import/training and qualified appraisal are distinct, with supplier publication disclosed.
  - **P1** — `pass` — Concrete choices lead to source-bounded results and a conditional older-record decision, and quotations add the reasons and preparation experience.
  - **W1** — `pass` — A self-contained ingress and well-connected narrative paragraphs support scanning and sustained reading.
  - **L1** — `pass` — Native American catalog and theater usage and restrained narration preserve Ortiz’s practical voice.
  - **L2** — `pass` — American spellings, May 6 date order and punctuation are consistent.
  - **T1** — `pass` — The exact genre and locale flags govern the artifact metadata; technique resolves to none and no technique resource is loaded.
  - **R2** — `pass` — The native trace contains the complete Write body, base, selected genre, web craft and delivery contract, plus the resolved composition scope; no review half, peer editorial pass or unselected genre is loaded.
  - **O1** — `pass` — Full inventories show unchanged source/work/scratch, no retained Skill files, unchanged authentication and only Harness-owned home effects; the private root is now absent.
- **unresolved findings** — none delivered as unresolved; any unsupported claims above are evaluation findings, not successfully reported limitations.
- **defects filed** — none; existing defect references, no new issue created by this evaluator.
- **notes** — The new no-question package passes under unchanged Write; it is not evidence that every such package will pass.

## `case-question-en_GB-r1`

- **fixture** — `case-question-en_GB-r1` in the supplementary matrix
- **invocation** — `/write --genre=case-study --language=en_GB --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — One complete draft with Kntnt metadata and a separate delivery account; [artifact](../editorial-329/followup/runs/baseline/case-question-en_GB-r1/write/artifact.md), [account](../editorial-329/followup/runs/baseline/case-question-en_GB-r1/write/account.md), [full response](../editorial-329/followup/runs/baseline/case-question-en_GB-r1/write/response.txt).
- **side effects** — No enduring Skill-created files; command-private UV directories are removed. The inventories record 319 Harness-owned home paths (native sessions, databases/locks, caches, bundled skills/plugins and config registration). Source and all work/scratch paths are unchanged; authentication is unchanged. Complete [changes](../editorial-329/followup/runs/baseline/case-question-en_GB-r1/write/filesystem-changes.json), [trace](../editorial-329/followup/runs/baseline/case-question-en_GB-r1/write/trace.jsonl), and [cleanup](../editorial-329/followup/runs/baseline/case-question-en_GB-r1/write/cleanup.json).
- **criteria** —
  - **F1** — `pass` — The final question-based transition is supported by the actual email question, the January start is supplied, and the text preserves unmeasured repair duration/revenue/satisfaction and the backlog reservation.
  - **G1** — `pass` — Workshop managers learn the status-definition decision, reported visibility and qualified continued use.
  - **G2** — `pass` — Headline and ingress introduce the customer result; customer action, supplier setup, trial limits and manager appraisal each do useful work.
  - **P1** — `pass` — Status definitions precede the account of what the trial established, and reported experience is distinguished from measured speed.
  - **W1** — `pass` — The What the trial established section gives a useful second entry point after the setup narrative.
  - **L1** — `pass` — Natural British workshop prose and exact supplied quotations keep the manager’s practical reservation.
  - **L2** — `pass` — British spelling, day-month dates and consistently chosen double quotation marks are valid.
  - **T1** — `pass` — The exact genre and locale flags govern the artifact metadata; technique resolves to none and no technique resource is loaded.
  - **R2** — `pass` — The native trace contains the complete Write body, base, selected genre, web craft and delivery contract, plus the resolved composition scope; no review half, peer editorial pass or unselected genre is loaded.
  - **O1** — `pass` — Full inventories show unchanged source/work/scratch, no retained Skill files, unchanged authentication and only Harness-owned home effects; the private root is now absent.
- **unresolved findings** — none delivered as unresolved; any unsupported claims above are evaluation findings, not successfully reported limitations.
- **defects filed** — none; existing defect references, no new issue created by this evaluator.
- **notes** — Positive control is exercised: “Asked whether she would make the same choice again, and what she would change” accurately reflects the supplied question and is not removed merely for matching the earlier defect’s form.

