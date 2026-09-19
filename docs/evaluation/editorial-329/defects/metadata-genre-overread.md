## What to build

Part of #329, observed in #338 explicit web-copy ABT evaluation. Record and assess an execution deviation in Redline's bounded resource discovery without adding a new selector rule: the existing Resolution contract already says a higher-level value suppresses lower levels and permits opening-definition discovery for inferred genres.

At `1a4f65b`, corpus `6e531f5`, native GPT `gpt-6-astra/high`, Codex CLI 0.155.1, `/redline --output=response input.md` receives complete valid YAML with `genre: web-copy`, `technique: abt`, `language: sv`. In `docs/evaluation/editorial-329/runs/rerun-345/web-copy-abt/redline/trace.jsonl`, item 5 reads that input, then item 6 reads the heading and definition of every installed genre through a Python glob. This is unnecessary lower-level inference discovery for a metadata-resolved genre. Item 7 subsequently loads only the correct full web-copy and ABT contracts. Final selection, substantive text, exactly one final Proofread pass and filesystem effects all pass; R2 records this limited overread independently.

No unseen genre contract was fully loaded, no alternative technique was selected, and the artifact is byte-identical after review. Preserve those limits instead of calling this a text defect or inventing a broader instruction ambiguity.

## Acceptance criteria

- [ ] Preserve the complete invocation, artifact, trace and separate successful text criteria/R2 overread assessment.
- [ ] Treat this as observed execution under an already-clear selector contract unless further evidence identifies genuine ambiguity; no new checklist is required.
- [ ] If replayed, use the exact original input and invocation on a recorded immutable revision, without prompting the expected selector behaviour; retain both outcomes.
- [ ] Report observed coverage without a reliability guarantee or erasure of the original deviation.
- [ ] Run the four CONTRIBUTING checks for the integrated change.

---
Written against 1a4f65b
