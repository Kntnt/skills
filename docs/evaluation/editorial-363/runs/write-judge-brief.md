# Write run judge brief

You judge one run of a writing Skill. The Skill takes a brief with source material, writes one first draft, has a fresh checker compare the draft with the material (at most twice), validates each report, repairs supported defects, and either delivers the draft or stops without delivering.

You are given a run directory. Read `work/source.md` (the brief and all supplied material), `response.md` (what the user received), `delivered.md` (the delivered draft, where the run delivered one), and every file under `evidence/` (drafts, checker reports and the writer's dispositions, where the run kept them). Read nothing else. You are not told how the Skill or the run was configured, what it was changed to test, or what model ran it, and you must not guess. A checker's or the writer's own approval is an argument to weigh, never evidence. Judge from the source yourself.

Where the run delivered nothing, judge the last draft in the evidence and mark it as not delivered.

## Criteria

| F1 | Does every assertion, quotation, attribution and implication stay within the supplied material, including uncertainty, chronology, causal limits and author perspective? Cite any unsupported addition or dropped caveat. Count-size judgements need a supplied comparison. |
| G2 | Do the required parts perform distinct useful jobs? The text carries a headline, a standfirst, a byline, a lead, one or more sections and an ending, in that order, each doing its own job. For a customer account: the customer's situation, action, results and appraisal, a truthful publisher stance, the customer left an acting party, and a call to action built from supplied offers, links or contact routes. |
| L1 | Does the prose sound professionally written in the resolved language, with native idiom and syntax, without importing one language's phrasing into the other? Separate this from locale mechanics — spelling, punctuation, number and date forms are not L1. |

## What to write

Write one Markdown file, `judgement.md`, in the run directory:

1. **Outcome**: delivered or stopped; how many comparisons ran; whether the delivered prose is identical to the last prose a checker saw.
2. **F1**, on the judged draft: pass or fail, citing every unsupported addition, changed term, changed subject, scope, date, modality or certainty, dropped caveat, invented event or personal attribute. Check translated terms in both directions: could something fall under the draft's term and not the source's, or the reverse, in this context? Keep unknown apart from absent.
3. **G2** and **L1** on the same draft: pass or fail, with passages and reader effect.
4. **Quoted speech.** The draft is in a language the material may not be in. Take every passage of quoted speech in the judged draft, in the order it appears, and give one line each:
   - the passage as the draft carries it, and the source sentence or sentences it renders;
   - whether a competent reader **of the draft's language**, reading only the draft, takes that passage on one pass, or stops at some point in it and has to supply something to carry on. Say where they stop and what they have to supply. Answer about the language the draft is in and not about the language the source is in, and remember that a figure a language uses itself — an ellipsis, a metonymy, a shorthand — reads on one pass however odd it looks parsed literally;
   - whether its meaning, stance, degree of certainty, any reservation in it, and the speaker's own voice are what the source carries, or moved;
   - whether any quotation the material offers and permits is missing from the draft altogether.

   Then say, in one sentence, whether every passage of quoted speech in this draft is speech a reader of its language takes on one pass with the source's meaning, stance, reservation and voice intact.
5. **Intermediate**: for every checker finding in the evidence, and for every finding the reply mentions where no report file exists, one line: the passage, the allegation, what the writer did, and your class — supported repair, disputed caution, wrong finding accepted, right finding rejected, wrong finding rejected (correct), or not judgeable from the evidence. Then say whether a real defect you found under F1 or under point 4 was seen by no checker.
6. **Stop or delivery**: a valid stop, a false stop, a valid delivery, or a delivery that should not have happened, with the reason.

Reply in at most 150 words with the outcome, the F1/G2/L1 verdicts, the one-sentence answer from point 4, and the path.
