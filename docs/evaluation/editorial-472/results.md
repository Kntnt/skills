# Results for #472

Measured on 2026-09-30 under the frozen [`plan.md`](plan.md), with [`judge-brief.md`](judge-brief.md) and the inputs in [`inputs/`](inputs/). Every run was a top-level `claude --print` session in Claude Code 2.1.285, made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) and its new `--extra-input`, on `claude-opus-5-5` at high deliberation, as every packet's `trace-index.json` records for the parent and each nested agent. Every judge was a fresh `kntnt-opus-high` subagent. No run or judge was cut off, so nothing is void.

## The first candidate, `dd3c331a`

Eight runs, sixteen judgements. A criterion is met only where both judges pass it.

| Run | K1 | K2 | K3 | K4 | K5 | M1 | F1 | O1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `a-carries-1` | met | met | n/a | n/a | **missed** (A, B) | met | met | met |
| `a-carries-2` | met | met | n/a | n/a | **missed** (A, B) | met | met | met |
| `a-elsewhere-1` | **missed** (A) | met | n/a | n/a | **missed** (A, B) | met | met | met |
| `a-elsewhere-2` | **missed** (A, B) | **missed** (A, B) | n/a | n/a | **missed** (A, B) | met | met | met |
| `b-1` | n/a | met | met | n/a | **missed** (A, B) | n/a | met | met |
| `b-2` | n/a | met | met | n/a | **missed** (A, B) | n/a | met | met |
| `c-1` | n/a | n/a | n/a | met | met | n/a | met | met |
| `c-2` | n/a | n/a | n/a | met | **missed** (A, B) | n/a | met | met |

The misses, as the judges recorded them:

- **K5, seven runs.** The report shortened or reworded the template's headings: question 3 without *with this text*, question 10 paraphrased, question 11 as *RIV and the chain check* or with RIV spelled out as *relevant, interesting and valuable*, and question 12 without *and what do you need to find out?*. Every question was present; only the wording departed.
- **K1, both `a-elsewhere` runs.** The review found that the text led the reader to an accountant and named it as a question 3 finding, and its one correction round turned the text back towards the weekly habit. The Brief fulfilment section then assessed the delivered text alone and reported question 3 as *fulfilled indirectly*, so the section never showed the shortfall the text arrived with. Judge B passed `a-elsewhere-1` on the finding; one judge is enough to record a miss.
- **K2, `a-elsewhere-2`.** The structure was reported fulfilled on its And–But–Therefore mapping and the hook, while question 9 beside it was only partly fulfilled: the structure's status did not rest on the conclusion.

Every other criterion was met on both judges: a text that carried the message without saying it was judged fulfilled with no finding against its silence (`K1`, `a-carries`); no run faulted the text for departing from the sketch or for an indirect call to action (`K2`); no open research question or unsupported sketch claim became a shortfall, both open questions were named as open, and the tonne-of-landfill claim was reported as unsupported by the material and left for the writer (`K3`); and both older-template runs mapped the old *message* to question 9, reported question 3 unanswered and flagged the reader weak (`K4`).

## The revise round, `5697ccc3`

The protocol's one revise round, taken over the seven runs that missed, against a revised `brief-review.md` committed first: headings word for word, never shortened, paraphrased or spelled out; the arrived status beside the delivered one where a correction changed it; the structure fulfilled only where the one sentence, the hook and the conclusion all hold. `c-1` met every criterion and was not re-run.

| Run | K1 | K2 | K3 | K4 | K5 | M1 | F1 | O1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `revise-a-carries-1` | met | met | n/a | n/a | met | met | met | met |
| `revise-a-carries-2` | met | met | n/a | n/a | met | met | met | met |
| `revise-a-elsewhere-1` | met | met | n/a | n/a | met | met | met | met |
| `revise-a-elsewhere-2` | met | met | n/a | n/a | met | met | met | met |
| `revise-b-1` | n/a | met | met | n/a | met | n/a | met | met |
| `revise-b-2` | n/a | met | met | n/a | met | n/a | met | met |
| `revise-c-2` | n/a | n/a | n/a | met | met | n/a | met | met |

Both `a-elsewhere` runs now reported question 3 as not fulfilled as the text arrived, beside its delivered status (*partly fulfilled* in one, *met* in the other), and every judge passed `K1`. Every run carried the twelve headings word for word.

## Side effects

In all fifteen runs `filesystem-changes.json` shows nothing under `work/` created, changed or removed, the three supplied files included, and `cleanup.json` shows the private root removed. `git status --porcelain --untracked-files=all` of this working tree was the same before and after each wave apart from this build's own files. `O1` is met in every run.

## Observations that are not criteria

- Several replies headed the section *How well the text meets the brief* or *How the text meets the brief* rather than *Brief fulfilment*. `brief-review.md` names the section in bold but no criterion asks for the name, and every judge found the section.
- In `c-1`, both judges noted that question 4's *partly fulfilled* rested partly on the old relevance answer's *why now*, which the mapping moved under question 4.

## Exit

Exit 2 of the plan: the revised candidate `5697ccc3` has no miss over the re-run subset, against ten for the first, so it ships. No miss remains, so nothing is filed.
