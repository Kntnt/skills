# Results for #473: the press release follows the maintainer's instruction

Measured on 2026-09-30, between 14:49 and 15:06 UTC, in Claude Code 2.1.285 on `claude-opus-5-5` at high deliberation, as every packet's `trace-index.json` records for the session and every nested agent; every judge a fresh `kntnt-opus-high` subagent. The method is [`plan.md`](plan.md), frozen in the candidate's commit before the first run.

## The two candidates

- **`1605c82c`**, the first candidate: the rewritten `genres/pressrelease.md` and `genres/pressrelease.review.md`, `article_anatomy.py --genre=pressrelease`, the loading and measuring steps of Write, Redline and the correction brief, and their tests. All eight planned runs were staged from it.
- **`21ab2472`**, the revised candidate, the evaluation's one revise round. It adds one sentence to the base half's closing paragraph — *"Nothing stands below the release as notes to the editor: detail a journalist may use is background, and a link or an attachment stands with the links and attachments."* — and to the review half's *The shape* a test naming a block of notes to the editor as a part outside the sequence, with its minimum safe correction: fold its detail into the background whole, move its links, drop its label. The two runs that missed were run again from it, as `revise-one` and `revise-two`.

**The revised candidate ships** (the plan's exit 2): over the re-run subset it has no miss, where the first candidate had two.

## Per run

A judged criterion is met only where both judges pass it. `L1`, `M1` and `O1` were read by this session: `L1` by running the shipped script with `--genre=pressrelease` on the delivered text, `M1` from the transcripts, `O1` from `filesystem-changes.json`.

| Run | Staged from | Delivered | `L1` headline / summary | `M1` | `P1` | `Q1` | `Q2` | `Q3` | `B1` | `K1` | `D1` | `U1` | `N1` | `F1` | `O1` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `write-two` | `1605c82c` | draft in the reply | 53 / 46, exit 0 | met, parent | met | met | met | met | met | met | — | — | — | met | met |
| `write-one` | `1605c82c` | draft in the reply | 67 / 47, exit 0 | met, parent | met | met | met | n/a | met | met | — | — | — | met | met |
| `write-none` | `1605c82c` | draft in the reply | 66 / 49, exit 0 | met, parent | met | met, gap reported | n/a | n/a | met | met | — | — | — | met | met |
| `redline-two` | `1605c82c` | corrected text in the reply | 58 / 48, exit 0 | met, parent and correction agent | **missed** (A fail, B pass) | met | met | met | met | met | **5 of 6** | — | — | met | met |
| `redline-one` | `1605c82c` | corrected text in the reply | 64 / 48, exit 0 | met, parent and correction agent | **missed** (A pass, B fail) | met | met | n/a | met | met | **2 of 3** | — | — | met | met |
| `redline-none` | `1605c82c` | corrected text in the reply | 64 / 51, exit 0 | met, parent and correction agent | met | met | n/a | n/a | met | met | 3 of 3 | — | — | met | met |
| `revise-two` | `21ab2472` | corrected text in the reply | 64 / 47, exit 0 | met, parent and correction agent | met | met | met | met | met | met | 6 of 6 | — | — | met | met |
| `revise-one` | `21ab2472` | corrected text in the reply | 58 / 48, exit 0 | met, parent and correction agent | met | met | met | n/a | met | met | 3 of 3 | — | — | met | met |
| `control-response` | `1605c82c` | no-change status only | — | met, parent | — | — | — | — | — | — | — | skipped: no text delivered, `control-file` answers it | met | — | met |
| `control-file` | `1605c82c` | `output.md`, byte-identical to the input | 67 / 36, exit 0 | met, parent | — | — | — | — | — | — | — | met | met | — | met, `work/output.md` created as asked |

The two first-candidate misses are one defect: the planted *detail kept below the release as notes to the editor* did not fire in `redline-one` or `redline-two` by either judge. `redline-one` moved the history paragraph *into* the notes block and its reply then called the block *bakgrunden*; `redline-two` moved only the image link out of it. The judge who failed `P1` in each run failed it on that block. `redline-none`, from the same candidate, fired it. Both revise runs fired all their planted defects, both judges agreeing, and met every criterion.

## What the runs show beyond the criteria

- **Every run measured.** Each Write run ran the script with `--genre=pressrelease` on its draft, each Redline run three times in its parent session, and every Redline correction agent on its own repair. No run counted a limit by hand, and every figure a reply states matches the script's measurement of the text it names.
- **Quotations.** No run wrote a quotation the material or the input did not have. `write-none` reports that the material gave no quotation and that none was written; `write-one` reports that the second place is empty for the same reason; `write-one`'s missing email address is reported, not filled, and so is `redline-one`'s and `revise-one`'s.
- **The headline and the summary.** Every old-shape Redline run found, unplanted, that the input's summary opened on the headline's own wording, and repaired it; neither control run reported the conforming summary, which restates the headline's news in its own words, as a defect.
- **Publication time.** `write-two` and `write-none` put the material's publication time on its own line above the headline.
- **A known defect delivered disclosed.** `write-two`'s last source comparison found that one body sentence had dropped the clock times of the inauguration, and the run delivered it disclosed rather than repaired. Both judges passed `F1`, the summary giving the times. That shape — a true finding at the final comparison reported rather than repaired — is the one `editorial-364` assigned to [#376](https://github.com/Kntnt/skills/issues/376); it is recorded under that number and not counted here.

## What is filed

Nothing. The one miss the first candidate had is repaired in the revised candidate, which ships, and the revise runs left no miss.

## Measurement, and the decision record

The two counted limits are measured by the Library's script, extended with `--genre=pressrelease` rather than copied into a sibling, as the ticket's comment on measurement settled. No decision record is written: widening ADR-0209's rule to one more genre is easy to reverse and unsurprising beside that record, so it fails two of `docs/rules/docs.md`'s three criteria, and `docs/rules/skills.md` carries the rule. ADR number `0233`, reserved for this ticket, is unused.
