# Run judge brief

You judge one run of a writing Skill. The Skill takes a brief with source material, writes one first draft, has a fresh checker compare the draft with the material (at most twice), validates each report, repairs supported defects, and then either delivers the draft or stops. You are given a run directory. Read `write/work/source.md` (the brief and all supplied material), `write/response.md` (what the user received), and every file under `write/evidence/` (drafts, checker reports and the writer's dispositions, where the run kept them). Read nothing else. You are not told how the Skill or the run was configured, what it was expected to do, or what any other run did, and you must not guess. A checker's or the writer's own approval is an argument to weigh, not evidence. Judge from the source yourself.

## Criteria, from the evaluation corpus

| F1 | Does every assertion, quotation, attribution and implication stay within the supplied material, including uncertainty, chronology, causal limits and author perspective? Cite any unsupported addition or dropped caveat. Count-size judgements need a supplied comparison. Keep unknown apart from absent. Check a translated term in both directions: could something fall under the draft's term and not the source's, or the reverse, in this context? Where the draft says what the pilot report does not measure, the third item is habit, familiarity or experience, not skill or ability. |
| G2 | Do the required parts perform distinct useful jobs? Opinion: early position, support, relevant real objection, identifiable action and actor. |
| L1 | Does the prose sound professionally written in the resolved language, with native idiom and syntax, without importing Swedish phrasing into English? Separate this from locale mechanics. |

## What to write

Write one Markdown file, named as the message that sent you here says, in the run directory:

1. **Outcome**: was a draft delivered, or did the run stop without one? How many comparisons ran? Is the prose that reached the user byte-identical to the last prose a checker saw — compare the delivered text with the last draft file in the evidence, and read the dispositions for any change made after the last comparison. Quote the difference where there is one.
2. **Remaining findings**: list every finding the last comparison raised that the run did not repair. For each, say whether what the user received names that passage, says what the supplied material carries instead, and gives a proposed smallest repair. Quote what the reply says about it, or say that it says nothing.
3. **F1** on the text the user received (or, where the run stopped, on the last draft in the evidence, marked as not delivered): pass or fail, citing every unsupported addition, changed term or thing measured, changed subject, scope, date, modality or certainty, dropped caveat, invented event or personal attribute.
4. **G2** and **L1** on the same text: pass or fail with passages and reader effect.
5. **Intermediate**: for every checker finding in the evidence, and for every finding the reply mentions where no report file exists, one line: the passage, the allegation, what the writer did, and your class — supported repair, disputed caution, wrong finding accepted, right finding rejected, wrong finding rejected (correct), or not judgeable from the evidence. Then say whether a real defect you found under F1 was seen by no checker.
6. **Preservation**: say what the user is left holding. If no draft was delivered, does the reply carry the current prose or name a path to it, and does it say what was and was not compared?

Reply in at most 120 words with the outcome, the F1/G2/L1 verdicts and the path.
