# Proposed title

Write: an opinion standfirst needs its headline to identify the decision

## What to build

Investigate and correct the opinion standfirst's standalone function. In the GPT retest for #362, `opinion-en_US-r3` delivers a standfirst that says “the value of each booking channel” and “a permanent change for all seven venues” without identifying either channel or the proposed change. Its complete text is:

> A report on an eight-week pilot in two association venues counts bookings rather than unique people. Lervik’s municipal executive board should weigh staff workload against the value of each booking channel before making a permanent change for all seven venues.

The independent blind judge finds the article source-faithful, but fails G2 because a reader shown this paragraph alone cannot identify the proposal to end telephone booking while digital booking remains. The headline and lead supply that information. All counted anatomy limits pass; those measurements do not establish the standfirst's semantic job. Write is a first-draft Skill and its source-only checker is not commissioned to perform a general editorial review, so this issue belongs to composition/genre adherence rather than a new checker review stage.

Evidence: `docs/evaluation/editorial-362/gpt-retest-2026-10-01/runs/opinion-en_US-r3/` and `judges/opinion-en_US-r3/captured-output.md`. The unchanged supplied brief, final draft, source-comparison reports, anatomy measurements, complete native traces and filesystem inventories are retained. Diagnose the loaded opinion, article-anatomy and web-craft guidance together. Keep the headline, standfirst and lead's respective jobs; do not prescribe the observed draft as a canonical sentence or solve the failure by repetition/padding.

## Acceptance criteria

- [ ] The observed standfirst's failure is assessed against the current standalone requirement, from the complete text and loaded resource chain.
- [ ] A plan committed before trials fixes independently judged standalone-comprehension criteria and includes controls where a valid standfirst is left alone.
- [ ] The resulting standfirst identifies the actor and decision a reader needs without depending on the headline or lead, while those parts add their own information and all applicable genre/anatomy criteria are recorded.
- [ ] Source fidelity, target locale, technique resolution, comparison budget, final compared prose and output lifecycle remain intact, and remaining misses are separately recorded.
- [ ] Full native evidence and independent blind judgments are retained; no present or historical evidence is rewritten.
- [ ] The four current checks in `CONTRIBUTING.md` pass.

---
Written against fb169087.

Publication status: local draft only; no issue number or readiness decision has been assigned. Proposed initial label: `needs-triage`, with `skill:write` and `bug`.

## Preparation audit — 2026-10-02

Prepared from the preserved local proposal and the complete US3 judgment/artifact. Current builder base `5b026028` carries the same opinion, anatomy, headlines, web-craft, base and Write contracts as measured `fb169087`. The anatomy explicitly requires a self-contained standfirst understood fully by a reader who sees only it. #414 already made base requirements operable, and #402 concerns an ending section, not this standalone introduction. No open duplicate was found. See [residual ownership](../residuals.md) and [contract hashes](../contracts-and-reads.json). This is a failure to meet an existing composition requirement, with no proof of a new missing instruction or a preferred repair design. Publication remains held by Thomas.
