# Proposed title

Write: a false source-comparison finding is accepted and declared as a known defect

## What to build

Investigate and correct the source-comparison validation that treats a stronger possible reading as something the supplied passage actually asserts. In the GPT retest for #362, `opinion-en_US-r2` delivers “The report measures neither age, functional ability, nor digital experience” for the supplied “Den mäter inte ålder, funktionsförmåga eller digital vana.” The second checker invents a distinction between historical experience and current familiarity; the source and draft supply neither operational restriction. The writer accepts that allegation and opens its delivery account with “Delivered with one known defect: ‘digital experience’ broadens the source's ‘digital vana.’”

The independent blind judge finds the article's variable faithful, but the accepted allegation and categorical delivery account false. This is not a post-comparison repair: the prose remains byte-identical to the final compared version, as #376 requires. The defect is in adjudication and the truth of the account accompanying a faithful text. Do not fix it by prescribing one synonym, banning criticism, treating every checker allegation as true or adding a comparison without evidence that it helps.

The independently judged GB third repetition shows the same operation: its second checker treats “familiarity with digital technology” as theoretical knowledge, the writer accepts that merely possible stronger reading, and the reply declares a known defect. That judge finds the phrase faithful in its booking-use context and fails the reply and report validation. The GB first repetition's separate judge rejects that phrase in its own draft; preserve this semantic sensitivity rather than asserting universal synonym equivalence. The concrete failure alleged here is an independently false categorical account and validation operation in the two named runs.

Evidence: `docs/evaluation/editorial-362/gpt-retest-2026-10-01/runs/opinion-en_US-r2/` and `judges/opinion-en_US-r2/captured-output.md`. The complete source, both report versions, writer disposition, exact output, parent/child traces and inventories are retained there. Read the full source-check contract and Claims guidance, and retain correct acceptance of actual variable changes and rejection of false stronger readings.

The second occurrence is in `runs/opinion-en_GB-r3/` and `judges/opinion-en_GB-r3/captured-output.md` under the same packet.

## Acceptance criteria

- [ ] The observed false acceptance is diagnosed from the complete source, draft, comparison reports and writer disposition; supported, false and disputed findings remain distinct.
- [ ] A plan committed before product trials fixes native same-seat runs, independent blinded criteria, positive preservation controls and real semantic-error controls, with no preferred replacement sentence supplied to the tested Skill.
- [ ] The changed operation preserves faithful contextual expression and the source's measured variable, and the delivery account does not assert an independently false alleged defect as fact.
- [ ] Correct supported findings, the two-comparison ceiling, exact final compared prose and disclosed genuine remaining findings remain intact; all applicable corpus criteria and side effects are recorded.
- [ ] Remaining measured misses become separate issues, and full native evidence is retained without changing the present record or historical failures.
- [ ] The four current checks in `CONTRIBUTING.md` pass.

---
Written against fb169087.

Publication status: local draft only; no issue number or readiness decision has been assigned. Proposed initial label: `needs-triage`, with `skill:write` and `bug`.
