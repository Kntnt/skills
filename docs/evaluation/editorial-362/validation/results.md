# Writer-validation diagnostic, round 1 results

Eighteen runs on 2026-09-20, each a fresh `claude-opus-5` subagent at high deliberation in Claude Code. None rerun, all kept under `runs/`.

| Case | Expected | `with` the sentence | `without` it |
| --- | --- | --- | --- |
| `m1` report missed the consent clause | accepted defect | 0/2 | 0/2 |
| `m2` report missed the consent clause | accepted defect | 0/2 | 0/2 |
| `m3` report missed the variable swap | accepted defect | 0/2 | 0/2 |
| `c1` clean report, eight set-asides | no accepted defect | 1/1 | 1/1 |
| `c2` clean report, six set-asides | no accepted defect | 1/1 | 1/1 |
| `t1` report with the true variable-swap finding | accepted defect | 0/1 | 0/1 |

Every one of the eighteen runs ends `DRAFT: no accepted defect`.

## Reading

The sentence changes nothing and is not in the product. (The plan counts three checker misses in the paired form; there were four, and candidate 1's miss of `p3` was not among the cases.) A reader told to verify that a quoted statement excludes the set-aside case reports that it does; one run in the `with` arm noted that a set-aside "rests on context rather than a quoted exclusion but stands". The accounting mismatches the readers did find are bookkeeping: pronoun counts, an unpaired `technique: none`, two unpaired headings.

`t1` was planned as a control. Given a report that correctly raises "digital proficiency" for "digital vana", the validating reader rejected it in both arms. `with`: "the source's own 'därför' grounds the no-ability inference in that list". `without`: "the report's decisive case is conceded to rest on nothing supplied". Round 2 (`round-2/results.md`) shows this came from the staging: these readers had the validation paragraph alone. Given the whole of `source-check.md`, as a real writer has it, ten of ten accepted a true finding. The `m1`–`m3` result stands in both stagings: a validator does not catch a difference the report has wrongly set aside.
