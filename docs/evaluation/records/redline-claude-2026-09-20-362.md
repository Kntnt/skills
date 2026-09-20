# redline — claude — 2026-09-20 — #362

- **record** — `redline-claude-2026-09-20-362`
- **date** — `2026-09-20`
- **ticket** — `#362`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5` at high deliberation, for every run, every subagent a run started, and every judge
- **harness** — Claude Code 2.1.278
- **corpus commit** — `65834c3`

## Run conditions

#362 changes nothing Redline loads. These are the source-blind pairs the ticket asks for: each run received, as `input.md`, exactly one draft delivered in [`write-claude-2026-09-20-362.md`](write-claude-2026-09-20-362.md), with its Kntnt map and nothing about its source. Staging, invocation seam, inventories and the delegation from a `claude-fable-5-1` session to `claude-opus-5` are as that record describes; the one evaluator addition was saving the reply to `response.md`. The matrix was frozen in [`../editorial-362/runs/plan.md`](../editorial-362/runs/plan.md). Each pair was judged by a fresh judge from `input.md` and the reply against `R1`. The judge was also given the source, which the Skill never had, to answer one separate question that is not part of `R1`: did a change remove or alter something the source required? No Codex Harness and no GPT model was started, controlled or invoked from this session.

## `opinion-en_GB-r1`

- **fixture** — the draft delivered by `opinion-en_GB-r1` in the Write record
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The reviewed text in the reply with its map; the account says one correction round was spent, the re-review found nothing, and no claim was removed.
- **side effects** — `none` from the Skill: `input.md` and the staged install unchanged, no file left in the working directory. `response.md` was created at the evaluator's request.
- **criteria** —
  - `R1` — `fail` — ten differences from the input, one the repair of a visible defect and nine of taste on a clean text (re-paragraphing, "channel" to "route", a recast closing line, "We" to "Öppna beslut", "the administration" to "the officers"), none of them reported (a substantive edit).
  - `effects` — `pass` — inventories before and after differ only by the evaluator's addition.
- **unresolved findings** — `none`
- **defects filed** — #377
- **notes** — outside `R1`, since the Skill could not know: Two subject changes moved the objection and the recording duty away from the source's *förvaltningen*, and "channel"/"route" merged the source's *kanal* and *bokningsväg*. Artefacts and judgement: [`../editorial-362/runs/opinion-en_GB-r1/redline/`](../editorial-362/runs/opinion-en_GB-r1/redline/judgement.md).

## `opinion-en_GB-r2`

- **fixture** — the draft delivered by `opinion-en_GB-r2` in the Write record
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The reviewed text in the reply with its map, then a "Claims removed" section naming two removals.
- **side effects** — `none` from the Skill: `input.md` and the staged install unchanged, no file left in the working directory. `response.md` was created at the evaluator's request.
- **criteria** —
  - `R1` — `pass` — three changes, both removals reported; the account calls "We make no claim to have funded or costed" → "We have not costed" "preserved in full", which misdescribes a changed modality.
  - `effects` — `pass` — inventories before and after differ only by the evaluator's addition.
- **unresolved findings** — `none`
- **defects filed** — #377
- **notes** — outside `R1`, since the Skill could not know: The source says "Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket"; the funding disclaimer and the no-claim modality were both required, and both went. Artefacts and judgement: [`../editorial-362/runs/opinion-en_GB-r2/redline/`](../editorial-362/runs/opinion-en_GB-r2/redline/judgement.md).

## `column-sv-r1`

- **fixture** — the draft delivered by `column-sv-r1` in the Write record
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The reviewed text in the reply with its map, then one removed sentence, quoted, with the reason.
- **side effects** — `none` from the Skill: `input.md` and the staged install unchanged, no file left in the working directory. `response.md` was created at the evaluator's request.
- **criteria** —
  - `R1` — `pass` — one tautological restatement removed and reported, one dash corrected; voice, arguments and claims otherwise untouched.
  - `effects` — `pass` — inventories before and after differ only by the evaluator's addition.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — outside `R1`, since the Skill could not know: No material loss: "Jag har inte mätt det här hos andra" remains. Artefacts and judgement: [`../editorial-362/runs/column-sv-r1/redline/`](../editorial-362/runs/column-sv-r1/redline/judgement.md).

## `column-sv-r2`

- **fixture** — the draft delivered by `column-sv-r2` in the Write record
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The reviewed text in the reply with its map, then "Borttagna påståenden" naming two deleted sentences and what went with each.
- **side effects** — `none` from the Skill: `input.md` and the staged install unchanged, no file left in the working directory. `response.md` was created at the evaluator's request.
- **criteria** —
  - `R1` — `fail` — two whole sentences deleted from a clean text, accurately reported; neither repaired a visible defect and each removed a hedge, changing a claim's scope and strength (a substantive edit).
  - `effects` — `pass` — inventories before and after differ only by the evaluator's addition.
- **unresolved findings** — `none`
- **defects filed** — #377
- **notes** — outside `R1`, since the Skill could not know: Both deleted sentences are the source's own caveats, near verbatim: "Det är en iakttagelse av dokumentet, inte en scen från ett visst möte" and "Det här är min reflektion, inte något jag har mätt hos andra". Artefacts and judgement: [`../editorial-362/runs/column-sv-r2/redline/`](../editorial-362/runs/column-sv-r2/redline/judgement.md).

## `opinion-en_US-r1`

- **fixture** — the draft of `opinion-en_US-r1` in the Write record
- **invocation** — not made
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none
- **side effects** — `none`
- **criteria** —
  - `R1` — `skipped` — Write stopped without delivering; there was no text to review.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `opinion-en_US-r2`

- **fixture** — the draft of `opinion-en_US-r2` in the Write record
- **invocation** — not made
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none
- **side effects** — `none`
- **criteria** —
  - `R1` — `skipped` — Write stopped without delivering; there was no text to review.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `opinion-sv-r1`

- **fixture** — the draft of `opinion-sv-r1` in the Write record
- **invocation** — not made
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none
- **side effects** — `none`
- **criteria** —
  - `R1` — `skipped` — not paired: Redline loads nothing the change touches, and the plan paired only the rows the ticket centres on.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `case-study-en_US-r1`

- **fixture** — the draft of `case-study-en_US-r1` in the Write record
- **invocation** — not made
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none
- **side effects** — `none`
- **criteria** —
  - `R1` — `skipped` — not paired, for the same reason.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `opinion-absence-en_GB-r1`

- **fixture** — the draft of `opinion-absence-en_GB-r1` in the Write record
- **invocation** — not made
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — none
- **side effects** — `none`
- **criteria** —
  - `R1` — `skipped` — not paired, for the same reason.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`
