# Column verification — redline — #342

- **record** — `redline-gpt-2026-09-19-342-column`
- **date** — `2026-09-19`
- **ticket** — `#342`, evaluation `#338`, parent `#329`
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`; checked against native turn_context per invocation
- **harness** — Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `eb4a26efd4f8ea54599972b0a74033b2c9811c23`

## Conditions

The [frozen matrix](../corpus/editorial-quality/README.md) is unchanged. After candidate column-sv and column-en_GB shifted the author's perspective, #342 clarified the existing ghostwriting boundary. Those failed runs and the evaluator's explicit reassessment remain in [the first column record](./redline-gpt-2026-09-19-338-part-column-opinion-web.md). These are new fresh invocations; en_US is its first declared cell, the other two are affected reruns. All three use the same revised resource.

Only the original source package is supplied to Write. Redline receives the complete extracted artifact with metadata, without the source or delivery account. No expected result or reviewer finding is supplied. Same native runner/isolation as the first candidate; all writable roots inventoried and native correction sessions retained. Full outputs and evidence live under [rerun-column](../editorial-329/runs/rerun-column/). Judgements are made against the fixed rubric before comparison; no other provider's record is consulted.

## column-sv

- **fixture** — `column-sv`, affected pipeline rerun
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none; neutral native dispatch retained with run
- **output target** — response
- **observed delivery** — No-change status; final artifact equals the entire input byte for byte, including metadata. [Final artifact](../editorial-329/runs/rerun-column/column-sv/redline/artifact.md), [response](../editorial-329/runs/rerun-column/column-sv/redline/response.txt).
- **side effects** — No surviving Skill effect.318 native private-home entries and config trust change classified in [side-effects](../editorial-329/runs/rerun-column/column-sv/redline/side-effects.md); complete source/resources/scratch preserved, root removed.
- **criteria** —
  - G1 — pass — Keeps the personal inquiry into a meeting template rather than changing it to a neutral guide or campaign.
  - G2 — pass — Title, supplied byline, documentary observation, developing reflection and uncertain ending remain intact.
  - P1 — pass — The reconsideration of a decision-only purpose is visible and proportionate; the closing question follows from it.
  - W1 — pass — Leaves working variable paragraph rhythm and the absence of subheadings alone; no numerical deviation finding.
  - L1 — pass — Preserves idiomatic Swedish and low-key humour, including “klä ut det till ett beslut”.
  - L2 — pass — The single mechanics pass identifies no objective correction; established spelling and punctuation remain.
  - T1 — pass — Metadata column/none/sv resolved; actual items6–8 load only column, shared base/web-craft pairs, anti-slop and returned sv scopes. Technique directory listing is selection inventory, not a technique load.
  - R1 — pass — Full artifact equality proves every sentence, claim, rhetorical turn and qualification survives; no unavailable-source investigation or taste repair.
  - R2 — pass — Complete review contract loaded, no correction needed; item9 opens installed Proofread, item11 invokes exactly once with `--language=sv --output=response`, items12–13 load shared mechanics and resolved sv scope. No subsequent substantive edit.
  - O1 — pass — Full-root inventories and temporary-directory commands establish response delivery and cleanup without source/resource mutation.
- **unresolved findings** — none
- **defects filed** — none; successful metadata-bearing closing pass also supports #339.
- **notes** — Native turn contexts confirm gpt-6-astra/high. Redline did not have the source and is assessed against visible text and preservation, not Write's source-fidelity responsibility.

## column-en_GB

- **fixture** — `column-en_GB`, paired with the failed Write rerun
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change; [final artifact](../editorial-329/runs/rerun-column/column-en_GB/redline/artifact.md) equals the input exactly, [response](../editorial-329/runs/rerun-column/column-en_GB/redline/response.txt).
- **side effects** — No Skill effect;316 native home entries and config trust update classified in [side-effects](../editorial-329/runs/rerun-column/column-en_GB/redline/side-effects.md). Root removed.
- **criteria** —
  - G1 — pass — Preserves the reflective personal inquiry.
  - G2 — pass — Working title/byline/opening/reflection/uncertain ending retained.
  - P1 — pass — Internal reasoning from decision box to shared understanding remains coherent.
  - W1 — pass — Retains purposeful variation and does not add subheadings by formula.
  - L1 — pass — Native British English expression preserved; no foreign-syntax repair needed.
  - L2 — pass — One actual mechanics pass reports no change; no established variation is treated as an error.
  - T1 — pass — Metadata column/none/en_GB honoured; item5 loads full selected/shared review contract, item6 only the three editorial language scopes; no technique.
  - R1 — pass — Byte-equal artifact preserves every claim and voice choice. The unsupported propensity is invisible without the source, so source-blind Redline cannot fairly be required to detect it.
  - R2 — pass — Installed Proofread opened at item7, invoked exactly once at item9 with flags alone, followed by shared and en_GB mechanics at items10–11. No correction needed or substantive edit afterwards.
  - O1 — pass — Whole-root inventories and cleanup establish permitted response effects only.
- **unresolved findings** — None reported by Redline. Source-aware evaluation separately retains Write defect #342; no claim that the final text is source-faithful.
- **defects filed** — None against this source-blind review.
- **notes** — Observed native gpt-6-astra/high; final artifact still contains Write's documented F1 defect.
