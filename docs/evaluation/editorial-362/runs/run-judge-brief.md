# Run judge brief

You judge one run of a writing Skill. The Skill takes a brief with source material, writes one first draft, has a fresh checker compare the draft with the material (at most twice), validates each report, repairs supported defects, and either delivers the draft or stops without delivering. You are given a run directory. Read `write/work/source.md` (the brief and all supplied material), `write/response.md` (what the user received), `draft.md` beside `write/` if it exists (the delivered draft), and every file under `write/evidence/` (drafts, checker reports and the writer's dispositions, where the run kept them). Read nothing else. You are not told how the Skill or the run was configured and must not guess. A checker's or the writer's own approval is an argument to weigh, not evidence. Judge from the source yourself.

## Criteria, from the evaluation corpus

| F1 | Does every assertion, quotation, attribution and implication stay within the supplied material, including uncertainty, chronology, causal limits and author perspective? Cite any unsupported addition or dropped caveat. Count-size judgements need a supplied comparison. | Write, source-aware evaluator only |
| G2 | Do the required parts perform distinct useful jobs? Article: informative H1, separate informative ingress, lead before first H2, supplied-only byline, explanatory body, earned ending. Case: customer situation/action/results/appraisal, truthful publisher stance. Column: personal reflection, not compulsory anecdote or campaign. Opinion: early position, support, relevant real objection, identifiable action/actor. Web-copy: useful information/choice, conditions and accurate next-step consequence where applicable. | Both; excerpt control exempts full article form |
| L1 | Does the prose sound professionally written in the resolved language, with native idiom and syntax, without importing Swedish phrasing into English or generic translated English into Swedish? Separate this from locale mechanics. | Both |
| R1 | Does Redline address concrete visible defects while preserving working voice, arguments, quotations and claims outside findings? Compare every before/after claim; report legitimate removals, rejected losses and irreparable findings. Clean texts may not be rewritten to satisfy taste or numerical guidelines. No unavailable-source verification. | Redline only |

## What to write

Write one Markdown file, `judgement.md`, in the run directory:

1. **Outcome**: delivered or stopped; how many comparisons ran; whether the delivered prose is identical to the last prose a checker saw (compare the delivered draft with the last draft file in the evidence, and read the dispositions for repairs made after the last comparison).
2. **F1** on the delivered draft (or, for a stopped run, on the last draft in the evidence, marked as not delivered): pass or fail, citing every unsupported addition, changed term or thing measured, changed subject, scope, date, modality or certainty, dropped caveat, invented event or personal attribute. Check translated terms in both directions: could something fall under the draft's term and not the source's, or the reverse, in this context? Keep unknown apart from absent.
3. **G2** and **L1** on the same draft: pass or fail with passages and reader effect.
4. **Intermediate**: for every checker finding in the evidence, and for every finding the writer's reply mentions where no report file exists, one line: the passage, the allegation, what the writer did, and your class — supported repair, disputed caution, wrong finding accepted, right finding rejected, wrong finding rejected (correct), or not judgeable from the evidence. Then say whether a real defect you found under F1 was seen by no checker.
5. **Stop or delivery**: a valid stop, a false stop, a valid delivery, or a delivery that should not have happened, with the reason.

Reply in at most 120 words with the outcome, the F1/G2/L1 verdicts and the path.
