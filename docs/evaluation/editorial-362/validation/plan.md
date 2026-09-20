# Writer-validation diagnostic for #362

Frozen on 2026-09-20 after checker round 3 and before any run below. It tests one sentence proposed for the writer's validation paragraph in `source-check.md`: "Where the report names a difference and sets it aside, verify that the statement it quotes excludes the case."

Reason: every checker miss in the paired format (three of them, in `../checker/runs/`) has one shape. The report names the real difference, builds the separating case, and sets it aside on a supplied statement, or an inference, that does not exclude it. A report like that lists no finding, so the writer's validation is the only place left to catch it.

Each run is a fresh `claude-opus-5` subagent at high deliberation that gets a fixture, one report and the validation paragraph. This is an approximation: in a real run the validating writer also wrote the draft. It shows whether the paragraph's wording lets a reader catch the faulty set-aside, not how often a writer will.

| Case | Report | Expected last line |
| --- | --- | --- |
| `m1` | `candidate-3/p3-r3` (missed the consent clause) | accepted defect, the consent clause |
| `m2` | `candidate-2/p3-r1` (missed the consent clause) | accepted defect, the consent clause |
| `m3` | `candidate-2/p1-r3` (missed the variable swap) | accepted defect, "digital proficiency" |
| `c1` | `candidate-3/n2-r1` (no findings, eight set-asides) | no accepted defect |
| `c2` | `candidate-3/n3-r2` (no findings, six set-asides) | no accepted defect |
| `t1` | `candidate-3/p1-r1` (one true finding) | accepted defect, "digital proficiency" |

Arms: `with` the sentence and `without` it, the paragraph otherwise identical (`task-with.md`, `task-without.md`). `m1`–`m3` run twice in each arm. `c1`, `c2` and `t1` run once in each arm. Eighteen runs, none rerun, all kept. The sentence is kept in the product only if `with` catches more of `m1`–`m3` than `without` and neither control turns into an accepted defect.
