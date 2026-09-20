# Writer-validation diagnostic, round 2

Frozen on 2026-09-20 after round 1 (`../plan.md`) and before any run below. Round 1 showed that a validating reader rejects a correct "digital proficiency" finding in both arms (`t1`, 2 of 2), on an inference from what the material makes likely, while holding the finding's counter-case to a stricter standard than the draft's claim. That is the ticket's defect A, reproduced in the Claude family at the writer's validation step.

One sentence of the validation paragraph is tested. `current`: "Reject a finding only with exact draft and source evidence showing support or a concrete mismatch in the report's reading." `burden`: "Reject a finding only by quoting the supplied statement that carries the draft's claim with its subject, scope and qualifications intact, or by showing a concrete mismatch between the report's reading and what the draft says in context. What the material makes likely is not support, and a finding's counter-case need only be compatible with the material."

The validator is a fresh `claude-opus-5` subagent at high deliberation. Unlike round 1 it receives the whole of `source-check.md` for its arm, as a real writer has it. It still did not write the draft; this remains an approximation.

| Case | Fixture | Report | Runs per arm | Expected |
| --- | --- | --- | --- | --- |
| `t1` | `p1` | `checker/runs/candidate-3/p1-r1` (true finding, variable swap) | 3 | finding accepted |
| `t2` | `p3` | `checker/runs/candidate-3/p3-r1` (true finding, consent clause) | 2 | finding accepted |
| `f1` | `n3` | `checker/runs/baseline/n3-r1` (four findings, all judged false) | 2 | all four rejected |
| `f2` | `n1` | `gpt-column-report-first.md`, the GPT-family report whose F4 the writer accepted in #357 | 2 | F4 rejected; F1–F3 and F5 are disputed and recorded, not scored |
| `f3` | `p1` | `checker/runs/baseline/p1-r2` (the swap filed as translation, five findings judged false) | 1 | the swap accepted; recorded per false finding |

Twenty runs, none rerun, all kept. `burden` goes into the product only if it accepts more of `t1`–`t2` than `current` and rejects F4 in `f2` and the four findings of `f1` at least as often as `current`.
