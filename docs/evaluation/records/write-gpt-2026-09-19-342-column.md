# Column verification — write — #342

- **record** — `write-gpt-2026-09-19-342-column`
- **date** — `2026-09-19`
- **ticket** — `#342`, evaluation `#338`, parent `#329`
- **skill** — `write`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`; checked against native turn_context per invocation
- **harness** — Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `eb4a26efd4f8ea54599972b0a74033b2c9811c23`

## Conditions

The [frozen matrix](../corpus/editorial-quality/README.md) is unchanged. After candidate column-sv and column-en_GB shifted the author's perspective, #342 clarified the existing ghostwriting boundary. Those failed runs and the evaluator's explicit reassessment remain in [the first column record](./write-gpt-2026-09-19-338-part-column-opinion-web.md). These are new fresh invocations; en_US is its first declared cell, the other two are affected reruns. All three use the same revised resource.

Only the original source package is supplied to Write. Redline receives the complete extracted artifact with metadata, without the source or delivery account. No expected result or reviewer finding is supplied. Same native runner/isolation as the first candidate; all writable roots inventoried and native correction sessions retained. Full outputs and evidence live under [rerun-column](../editorial-329/runs/rerun-column/). Judgements are made against the fixed rubric before comparison; no other provider's record is consulted.

## column-sv

- **fixture** — `column-sv`, affected rerun
- **invocation** — `/write --genre=column --language=sv --output=response source.md`
- **contextual instruction** — none; neutral native dispatch retained with run
- **output target** — response
- **observed delivery** — Complete Swedish column with metadata and separate account; [artifact](../editorial-329/runs/rerun-column/column-sv/write/artifact.md), [full response](../editorial-329/runs/rerun-column/column-sv/write/response.txt).
- **side effects** — No surviving Skill effect; work/source/resources/scratch unchanged.316 native home additions and one private config trust change are enumerated and classified in [side-effects](../editorial-329/runs/rerun-column/column-sv/write/side-effects.md). Root removed after capture.
- **criteria** —
  - F1 — pass — “Det är min invändning när jag läser mallen” locates the calendar observation in the supplied reflection without claiming Nora herself treats slots as results. Trust, differing understanding, possible value of non-deciding conversations and doubt about another box all remain. The rhetorical return to the document does not introduce a separate remembered meeting or physical scene.
  - G1 — pass — The template's missing purpose becomes a personal inquiry rather than an efficiency campaign; the ending preserves hope and doubt together.
  - G2 — pass — Relevant title/byline, concrete document opening, developing reflection and resonant uncertain ending; no manufactured anecdote.
  - P1 — pass — The initial missing decision field is reconsidered through the legitimate value of conversation, leading to a broader question about shared understanding.
  - W1 — pass — Coherent paragraphs alternate observation, reconsideration and proposal; short turns provide entry without unnecessary H2s or fragmenting the argument.
  - L1 — pass — “klä ut det till ett beslut” and “problemet med formuläret ... mer formulär” carry idiomatic, quiet Swedish humour. No translated syntax is observed.
  - L2 — pass — Swedish compounds, title case, punctuation and byline are correct; no factual conversion.
  - T1 — pass — YAML column/none/sv matches actual item_4 genre/base/web-craft read; no technique resource is read.
  - R2 — pass — Installed Write and invocation engine used; item_5 returns composition only, with no review half, peer Skill or mechanical pass.
  - O1 — pass — Complete inventories and trace confirm preserved input/resources and cleared temporary UV directories.
- **unresolved findings** — None; lack of demonstrated meeting effect is a retained source limit.
- **defects filed** — None in this rerun; addresses #342.
- **notes** — All native turn contexts expose gpt-6-astra/high. Source-aware judgement made before the paired Redline output; prior failed runs remain.

## column-en_GB

- **fixture** — `column-en_GB`, affected rerun
- **invocation** — `/write --genre=column --language=en_GB --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Complete draft and account; [artifact](../editorial-329/runs/rerun-column/column-en_GB/write/artifact.md), [response](../editorial-329/runs/rerun-column/column-en_GB/write/response.txt). The attempted instruction clarification did not repair #342 here.
- **side effects** — No Skill artifact or source/resource change;320 native home additions and a config trust change classified in [side-effects](../editorial-329/runs/rerun-column/column-en_GB/write/side-effects.md). Root removed.
- **criteria** —
  - F1 — fail — Unsupported attributed personal stance: “how easily I can regard time in the calendar as a result in itself” turns Nora's observation about meeting practice into her own propensity. The source grants the reflection and irritation, not that she thinks this way herself. Same defect #342, despite eb4a26e's reference to conduct.
  - G1 — pass — A reflective template inquiry with self-deprecating humour; the source-fidelity failure is separate from successful genre craft.
  - G2 — pass — Title, byline, document opening, developing reflection and uncertain closing question form a column, with no demand for invented meeting scenes.
  - P1 — pass — The missing decision box is reconsidered through trust and exploration before the broader shared-understanding question.
  - W1 — pass — Connected variable paragraphs and short turns orient the reader without numerical conformity or gratuitous subheads.
  - L1 — pass — “awkwardly trying to explain themselves” and “more form” sound like idiomatic English reflection; the changed personal stance is semantic fidelity, not poor English.
  - L2 — pass — British quotation/punctuation and idiom observed; no factual conversion.
  - T1 — pass — YAML column/none/en_GB agrees with actual item4 scoped base/genre/web-craft read and item5 composition resolution; no technique file.
  - R2 — pass — Installed Write/invocation executed, no review half, review scope or peer pass.
  - O1 — pass — Full-root inventory and context-managed temporary-directory cleanup show no surviving Skill effect.
- **unresolved findings** — The delivered account does not report its invented personal propensity; F1 remains a hard rejection.
- **defects filed** — #342, retained as a failed repair; subsequent correction/rerun required.
- **notes** — Observed model gpt-6-astra/high. Judged before reading paired Redline; no altered prompt or corpus. en_US was not run at this superseded revision and remains pending at the revised one.
