# Checker-level results, round 1

Run on 2026-09-20 in Claude Code, every checker and judge a fresh `claude-opus-5` subagent at high deliberation. Baseline: 14 runs. Candidate (`candidate-task.md`): 21 runs. Nothing was rerun or dropped. Seven judges, one per fixture, classed every finding from their own reading of the fixture, with both arms shuffled under neutral names (`judging/round-1/key.json`, kept outside the repository until judging ended). The two arms' reports differ in form, so the blinding hides which arm is which, not that there are two.

| Fixture | Criterion | Baseline | Candidate |
| --- | --- | --- | --- |
| `p1` variable swap | D | 2/2, both filed as translation findings; one first cleared the claim on support | 3/3, all filed as source support |
| `p2` chronology | D | 2/2 | 3/3 |
| `p3` document scope | D | 1/2; one run noticed the gap and accepted the clause | 2/3; one run named the counter-case and accepted the clause |
| `p4` person attribute | D | 2/2 | 3/3 |
| `n1` column reflection | P | 2/2 | 3/3 |
| `n2` opinion sufficiency | P | 2/2 | 3/3 |
| `n3` withheld column | P | 1/2; one run cleared the passage and still filed a finding on it | 3/3 |

| X, all fixtures | Baseline (14 runs) | Candidate (21 runs) |
| --- | --- | --- |
| Findings judged false | 27 | 0 |
| Findings judged disputed | 17 | 5 |
| Report words, mean | 5 290 | 2 737 |
| Wall time, median | 268 s | 167 s |

The judge of `n1` classed one passage the plan had not listed as a supported finding: the paragraph-5 sentence that replaces the notes' "varför vi behöver just varandras tid" with "varför vi behöver undersöka något tillsammans". Baseline raised it in 1 of 2 runs, among four weaker findings; the candidate raised it alone in 2 of 3. The judge of the same fixture in rounds 2–3 classed the same finding false, because the draft's next sentence restores the notes' object. Two judges disagreeing makes it disputed; see `results-rounds-2-3.md`.

## Reading

The Claude family does not reproduce defect B's false finding on the transition sentence, and its baseline checker does notice defect A. What it reproduces is the mechanism behind both. The negation ledger yields about two false findings a run beside each real one, and twice a checker saw a real difference and reasoned it away (`p3` baseline; `p1` baseline first cleared the claim "on support" and demoted it to a translation note, the class the writer is told to test against idiom). A writer validating such a report meets a real fault in the same list, at the same or lower severity, as several false ones. That is the situation in which the GPT-family writer accepted all five column findings and nobody pressed the variable swap.

The candidate's one miss shows a loophole in its own wording: the checker built the counter-case, then set it aside because the material does not describe such a case and because the draft "is weaker". `candidate-2-task.md` states that the case need only be compatible with the material and that cautious wording does not excuse it. The whole arm is rerun under it, three runs a fixture.
