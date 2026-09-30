# redline — claude — 2026-09-30 — #472

- **record** — `redline-claude-2026-09-30-472`
- **date** — `2026-09-30`
- **ticket** — `#472`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run and every nested agent, as each packet's `trace-index.json` records; every judge a fresh `kntnt-opus-high` subagent, which launches `claude-opus-5-5` at high deliberation
- **harness** — Claude Code 2.1.285
- **corpus commit** — `dd3c331a`, and `5697ccc3` for the seven revise runs

## Run conditions

Eight `Redline` runs on the synthetic inputs in [`../editorial-472/inputs/`](../editorial-472/inputs/), four brief–text pairs run twice each, staged from the first candidate `dd3c331a` by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) with `--extra-input` placing the brief and its material beside the text, as [`../editorial-472/plan.md`](../editorial-472/plan.md) says. The seven runs that missed were run again from the revised candidate `5697ccc3`, the evaluation's one revise round. There is no pre-change arm: the behaviour is the maintainer's ruling and ships whatever the measurement shows. The criteria and the per-run tables are in [`../editorial-472/results.md`](../editorial-472/results.md); each packet, with its two judgements, is under [`../editorial-472/runs/`](../editorial-472/runs/).

**Judging.** Two blind judges per run under [`../editorial-472/judge-brief.md`](../editorial-472/judge-brief.md), each reading only the text, the brief, the material and the reply. A criterion is met only where both pass it. `O1` was read by this session from `filesystem-changes.json` and `cleanup.json`. The editorial-quality matrix's criteria are not this evaluation's and are not scored.

**Side effects.** In every run `filesystem-changes.json` shows nothing under `work/` created, changed or removed, and the private root removed (`cleanup.json`).

## `a-carries-1`

- **fixture** — `../editorial-472/inputs/text-a-carries.md` as `input.md`, `brief-a.md` as `brief.md`, `material-a.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 6m29s.
- **side effects** — `none`.
- **criteria** —
  - `K1`, `K2`, `M1`, `F1` — `pass` on both judges; `K3`, `K4` not applicable.
  - `K5` — `fail` on both judges — the headings of questions 3, 11 and 12 shortened or reworded; every question present.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — superseded by `revise-a-carries-1`.

## `a-carries-2`

- **fixture** — `../editorial-472/inputs/text-a-carries.md` as `input.md`, `brief-a.md` as `brief.md`, `material-a.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, unchanged, with findings, a claim account and the brief-fulfilment section, in 8m03s.
- **side effects** — `none`.
- **criteria** —
  - `K1`, `K2`, `M1`, `F1` — `pass` on both judges; `K3`, `K4` not applicable.
  - `K5` — `fail` on both judges — the headings of questions 3, 10, 11 and 12 paraphrased.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — the delivered text is the input unchanged. Superseded by `revise-a-carries-2`.

## `a-elsewhere-1`

- **fixture** — `../editorial-472/inputs/text-a-elsewhere.md` as `input.md`, `brief-a.md` as `brief.md`, `material-a.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 7m58s.
- **side effects** — `none`.
- **criteria** —
  - `K2`, `M1`, `F1` — `pass` on both judges; `K3`, `K4` not applicable.
  - `K1` — `fail` on judge A, `pass` on judge B — the review named the turn to an accountant as a question 3 finding and its one round repaired it, but the section reported question 3 only as *fulfilled indirectly* for the delivered text, so it never showed the shortfall the text arrived with.
  - `K5` — `fail` on both judges — the headings of questions 11 and 12 shortened.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — superseded by `revise-a-elsewhere-1`.

## `a-elsewhere-2`

- **fixture** — `../editorial-472/inputs/text-a-elsewhere.md` as `input.md`, `brief-a.md` as `brief.md`, `material-a.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 8m48s.
- **side effects** — `none`.
- **criteria** —
  - `M1`, `F1` — `pass` on both judges; `K3`, `K4` not applicable.
  - `K1` — `fail` on both judges — as in `a-elsewhere-1`, question 3 reported *fulfilled, indirectly* after the round's repair, with the arrived shortfall only in a finding.
  - `K2` — `fail` on both judges — the structure reported fulfilled on its And–But–Therefore mapping and the hook while question 9 beside it was partly fulfilled.
  - `K5` — `fail` on both judges — the headings of questions 11 and 12 shortened.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — superseded by `revise-a-elsewhere-2`.

## `b-1`

- **fixture** — `../editorial-472/inputs/text-b.md` as `input.md`, `brief-b.md` as `brief.md`, `material-b.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 5m23s.
- **side effects** — `none`.
- **criteria** —
  - `K2`, `K3`, `F1` — `pass` on both judges; `K1`, `K4`, `M1` not applicable. Both open research questions named as open; the sketch's money-saving claim not held against the text; the tonne claim reported as unsupported and left for the writer.
  - `K5` — `fail` on both judges — the headings of questions 3, 11 and 12 shortened or reworded.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — superseded by `revise-b-1`.

## `b-2`

- **fixture** — `../editorial-472/inputs/text-b.md` as `input.md`, `brief-b.md` as `brief.md`, `material-b.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 4m15s.
- **side effects** — `none`.
- **criteria** —
  - `K2`, `K3`, `F1` — `pass` on both judges; `K1`, `K4`, `M1` not applicable.
  - `K5` — `fail` on both judges — question 11's heading with RIV spelled out.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — superseded by `revise-b-2`.

## `c-1`

- **fixture** — `../editorial-472/inputs/text-c.md` as `input.md`, `brief-c.md` as `brief.md`, `material-c.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 6m40s.
- **side effects** — `none`.
- **criteria** —
  - `K4`, `K5`, `F1` — `pass` on both judges; `K1`, `K2`, `K3`, `M1` not applicable. The old *message* answer assessed as question 9, question 3 unanswered, the reader flagged weak.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — both judges noted that question 4's *partly fulfilled* rested partly on the old relevance answer's *why now*. Not re-run: it met every criterion.

## `c-2`

- **fixture** — `../editorial-472/inputs/text-c.md` as `input.md`, `brief-c.md` as `brief.md`, `material-c.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 5m17s.
- **side effects** — `none`.
- **criteria** —
  - `K4`, `F1` — `pass` on both judges; `K1`, `K2`, `K3`, `M1` not applicable.
  - `K5` — `fail` on both judges — question 11's heading with RIV spelled out and without *and does the brief hold together?*, question 12's shortened.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — superseded by `revise-c-2`.

## `revise-a-carries-1`

- **fixture** — `../editorial-472/inputs/text-a-carries.md` as `input.md`, `brief-a.md` as `brief.md`, `material-a.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 7m01s.
- **side effects** — `none`.
- **criteria** —
  - `K1`, `K2`, `K5`, `M1`, `F1` — `pass` on both judges; `K3`, `K4` not applicable.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — staged from `5697ccc3`; counted in place of the first candidate's run.

## `revise-a-carries-2`

- **fixture** — `../editorial-472/inputs/text-a-carries.md` as `input.md`, `brief-a.md` as `brief.md`, `material-a.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 7m16s.
- **side effects** — `none`.
- **criteria** —
  - `K1`, `K2`, `K5`, `M1`, `F1` — `pass` on both judges; `K3`, `K4` not applicable.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — staged from `5697ccc3`; counted in place of the first candidate's run.

## `revise-a-elsewhere-1`

- **fixture** — `../editorial-472/inputs/text-a-elsewhere.md` as `input.md`, `brief-a.md` as `brief.md`, `material-a.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 10m04s.
- **side effects** — `none`.
- **criteria** —
  - `K1`, `K2`, `K5`, `M1`, `F1` — `pass` on both judges; `K3`, `K4` not applicable. Question 3 reported not fulfilled as the text arrived and partly fulfilled as delivered.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — staged from `5697ccc3`; counted in place of the first candidate's run.

## `revise-a-elsewhere-2`

- **fixture** — `../editorial-472/inputs/text-a-elsewhere.md` as `input.md`, `brief-a.md` as `brief.md`, `material-a.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 9m07s.
- **side effects** — `none`.
- **criteria** —
  - `K1`, `K2`, `K5`, `M1`, `F1` — `pass` on both judges; `K3`, `K4` not applicable. Question 3 reported not met as the text arrived and met as delivered.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — staged from `5697ccc3`; counted in place of the first candidate's run.

## `revise-b-1`

- **fixture** — `../editorial-472/inputs/text-b.md` as `input.md`, `brief-b.md` as `brief.md`, `material-b.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 5m09s.
- **side effects** — `none`.
- **criteria** —
  - `K2`, `K3`, `K5`, `F1` — `pass` on both judges; `K1`, `K4`, `M1` not applicable.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — staged from `5697ccc3`; counted in place of the first candidate's run.

## `revise-b-2`

- **fixture** — `../editorial-472/inputs/text-b.md` as `input.md`, `brief-b.md` as `brief.md`, `material-b.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 4m59s.
- **side effects** — `none`.
- **criteria** —
  - `K2`, `K3`, `K5`, `F1` — `pass` on both judges; `K1`, `K4`, `M1` not applicable.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — staged from `5697ccc3`; counted in place of the first candidate's run.

## `revise-c-2`

- **fixture** — `../editorial-472/inputs/text-c.md` as `input.md`, `brief-c.md` as `brief.md`, `material-c.md` as `material.md`
- **invocation** — `/redline --brief=brief.md --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, changed, with findings, a claim account and the brief-fulfilment section, in 5m43s.
- **side effects** — `none`.
- **criteria** —
  - `K4`, `K5`, `F1` — `pass` on both judges; `K1`, `K2`, `K3`, `M1` not applicable.
  - `O1` — `pass`.
- **unresolved findings** — reported with the text and left for the writer, as the reply lists them.
- **defects filed** — `none`.
- **notes** — staged from `5697ccc3`; counted in place of the first candidate's run.
