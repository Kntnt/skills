# Writer-validation diagnostic, round 2 results

Twenty runs on 2026-09-20, each a fresh `claude-opus-5` subagent at high deliberation in Claude Code, given the whole of `source-check.md` for its arm. None rerun, all kept under `runs/`.

| Case | Expected | `current` | `burden` |
| --- | --- | --- | --- |
| `t1` true finding, variable swap | accepted | 3/3 | 3/3 |
| `t2` true finding, consent clause | accepted | 2/2 | 2/2 |
| `f1` four findings judged false | all rejected | 2/2 | 2/2 |
| `f2` the GPT-family column report, F4 | F4 rejected | 2/2 | 2/2 |
| `f3` the swap misfiled as translation | swap accepted | 1/1 | 1/1 |

Recorded, not scored: in `f2` all four runs also rejected F1–F3 and F5. In `f3` both arms rejected the five findings judged false; `current` also accepted the "Staff" for "förvaltningen" finding, which both judge panels classed disputed, and `burden` rejected it. Both arms named the misfiling of the swap as an accounting mismatch.

## Reading

`burden` does not beat `current`, so it is not in the product. The sentence "Reject a finding only with exact draft and source evidence …" stays as it was.

The difference from round 1 is what the validator was given. With only the validation paragraph, two readers of two rejected the true variable-swap finding on an inference. With the whole procedure, ten of ten accepted a true finding, and their stated reasons come from the comparison task: "no supplied statement excludes the checker's case", "F2–F5 target reasoning the comparison task excludes". The writer in a real run has the whole file. So the validators used the new task text as the standard they held a finding to. Both arms carried that text and no arm tested its absence, so this shows the rules in use, not that they are needed. Round 1's `t1` result is therefore an effect of how that diagnostic was staged and is not evidence that a real writer rejects the finding.

What this does not show: no validator in either round caught a report that had wrongly set a real difference aside (round 1, `m1`–`m3`, 0 of 12). A comparison that misses is still only caught by the second comparison, where one runs.
