# redline — claude — 2026-09-30 — #473

- **record** — `redline-claude-2026-09-30-473`
- **date** — `2026-09-30` (the seven runs were made between 14:49 and 15:06 UTC)
- **ticket** — `#473`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run, every correction agent and every nested Proofread pass, as each packet's `trace-index.json` records; every judge a fresh `kntnt-opus-high` subagent, which launches `claude-opus-5-5` at high deliberation
- **harness** — Claude Code 2.1.285
- **corpus commit** — `1605c82c`

## Run conditions

Seven `Redline` runs of the press release genre on the synthetic releases in [`../editorial-473/inputs/`](../editorial-473/inputs/), made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) as [`../editorial-473/plan.md`](../editorial-473/plan.md) says: three old-shape releases, one per quotation case, and the conforming release as the protocol's clean-control pair, all staged from the first candidate `1605c82c`; then the evaluation's one revise round, the two old-shape runs that missed, staged from the revised candidate `21ab2472`, which ships. There is no pre-change arm. The per-run table is in [`../editorial-473/results.md`](../editorial-473/results.md); each packet, with its two judgements, is under [`../editorial-473/runs/`](../editorial-473/runs/).

**Judging.** Two blind judges per run: old-shape runs under [`../editorial-473/redline-judge-brief.md`](../editorial-473/redline-judge-brief.md), given the plan's list of planted defects; the control pair under [`../editorial-473/control-judge-brief-response.md`](../editorial-473/control-judge-brief-response.md) and [`../editorial-473/control-judge-brief-file.md`](../editorial-473/control-judge-brief-file.md). A criterion is met, and a planted defect fires, only where both judges say so. `L1`, `M1` and `O1` were read by this session as the Write record says.

**Side effects.** In every run `filesystem-changes.json` shows nothing created, changed or removed outside the Harness's own files under the run's `HOME`, except `work/output.md` in the file-target control, which is the effect asked for; each private root was removed. The build's working tree read the same before and after the runs.

## `redline-old-two-quotations` — first candidate

- **fixture** — `../editorial-473/inputs/redline-old-two-quotations.md`, run `redline-two`, staged from `1605c82c`
- **invocation** — `/redline --genre=pressrelease --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected release in the reply after one correction round, in 6m57s, with seven findings reported as repaired.
- **side effects** — `none`
- **criteria** —
  - `L1` — `pass` — 58 characters, 48 words, exit 0, as the reply states.
  - `M1` — `pass` — the parent and the correction agent ran the script with `--genre=pressrelease`.
  - `D1` — `fail` — five of six fired on both judges; the notes block to the editor did not fire on either: only its image link was moved. An unresolved mandatory finding.
  - `P1` — `fail` — judge A fails it on the notes block kept between the background and the links; judge B passes it. An unresolved mandatory finding.
  - `Q1`, `Q2`, `Q3`, `B1`, `K1`, `F1` — `pass` on both judges.
  - `O1` — `pass`.
- **unresolved findings** — `none` reported by the run.
- **defects filed** — `none`; repaired by the revised candidate, whose rerun is below.
- **notes** — read in place by `revise-two`, as the plan's exit 2 says.

## `redline-old-one-quotation` — first candidate

- **fixture** — `../editorial-473/inputs/redline-old-one-quotation.md`, run `redline-one`, staged from `1605c82c`
- **invocation** — `/redline --genre=pressrelease --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected release in the reply after one correction round, in 6m21s.
- **side effects** — `none`
- **criteria** —
  - `L1` — `pass` — 64 characters, 48 words, exit 0.
  - `M1` — `pass` — the parent and the correction agent ran the script with `--genre=pressrelease`.
  - `D1` — `fail` — the headline and the summary fired on both judges; the notes block did not fire on either, and the run moved the history paragraph into it. An unresolved mandatory finding.
  - `P1` — `fail` — judge B fails it on the notes block standing where the background and the links belong; judge A passes it. An unresolved mandatory finding.
  - `Q1`, `Q2`, `B1`, `K1`, `F1` — `pass` on both judges; `Q3` not applicable.
  - `O1` — `pass`.
- **unresolved findings** — the missing email address, reported.
- **defects filed** — `none`; repaired by the revised candidate.
- **notes** — the reply's claim account says the history now stands *i bakgrunden*, where it stands in the notes block; both judges record the misstatement and find no claim changed by it. Read in place by `revise-one`.

## `redline-old-no-quotation`

- **fixture** — `../editorial-473/inputs/redline-old-no-quotation.md`, run `redline-none`, staged from `1605c82c`
- **invocation** — `/redline --genre=pressrelease --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected release in the reply after one correction round, in 5m05s.
- **side effects** — `none`
- **criteria** —
  - `L1` — `pass` — 64 characters, 51 words, exit 0.
  - `M1` — `pass` — the parent and the correction agent ran the script with `--genre=pressrelease`.
  - `D1` — `pass` — all three planted defects fired on both judges.
  - `P1`, `Q1`, `B1`, `K1`, `F1` — `pass` on both judges; `Q2`, `Q3` not applicable; no quotation written, the gap reported.
  - `O1` — `pass`.
- **unresolved findings** — the missing quotation, reported as a gap and not filled.
- **defects filed** — `none`
- **notes** — none

## `redline-old-two-quotations` — revised candidate

- **fixture** — `../editorial-473/inputs/redline-old-two-quotations.md`, run `revise-two`, staged from `21ab2472`
- **invocation** — `/redline --genre=pressrelease --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected release in the reply after one correction round, in 6m15s, with seven findings reported as repaired.
- **side effects** — `none`
- **criteria** —
  - `L1` — `pass` — 64 characters, 47 words, exit 0.
  - `M1` — `pass` — parent and correction agent.
  - `D1` — `pass` — all six planted defects fired on both judges, the notes block among them.
  - `P1`, `Q1`, `Q2`, `Q3`, `B1`, `K1`, `F1` — `pass` on both judges.
  - `O1` — `pass`.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — the reply counts four body paragraphs where the plan planted three, taking the history paragraph as body; both judges record the finding as fired.

## `redline-old-one-quotation` — revised candidate

- **fixture** — `../editorial-473/inputs/redline-old-one-quotation.md`, run `revise-one`, staged from `21ab2472`
- **invocation** — `/redline --genre=pressrelease --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected release in the reply after one correction round, in 5m51s.
- **side effects** — `none`
- **criteria** —
  - `L1` — `pass` — 58 characters, 48 words, exit 0.
  - `M1` — `pass` — parent and correction agent.
  - `D1` — `pass` — all three fired on both judges.
  - `P1`, `Q1`, `Q2`, `B1`, `K1`, `F1` — `pass` on both judges; `Q3` not applicable.
  - `O1` — `pass`.
- **unresolved findings** — the missing email address, reported.
- **defects filed** — `none`
- **notes** — none

## `redline-conforming` — response target

- **fixture** — `../editorial-473/inputs/redline-conforming.md`, run `control-response`
- **invocation** — `/redline --genre=pressrelease --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status in Swedish, in 1m48s.
- **side effects** — `none`
- **criteria** —
  - `M1` — `pass` — the parent ran the script with `--genre=pressrelease`.
  - `U1` — `skipped` — no text was delivered; the file-target entry answers it.
  - `N1` — `pass` on both judges — no finding against a correct part.
  - `O1` — `pass`.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — none

## `redline-conforming` — file target

- **fixture** — `../editorial-473/inputs/redline-conforming.md`, run `control-file`
- **invocation** — `/redline --genre=pressrelease --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `work/output.md`, byte-identical to the input, and a reply reporting no findings, in 1m52s.
- **side effects** — `work/output.md` created, as the output target asks; nothing else.
- **criteria** —
  - `L1` — `pass` — 67 characters, 36 words, exit 0.
  - `M1` — `pass` — the parent ran the script with `--genre=pressrelease`.
  - `U1` — `pass` on both judges — no difference between `work/input.md` and `work/output.md`.
  - `N1` — `pass` on both judges.
  - `O1` — `pass`.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — none
