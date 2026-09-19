## What to build

Part of #329, found by the final CONTRIBUTING checks for #338. Scope the test that rejects exact-prose assertions to the corpus and evaluation contracts it is intended to protect. Its current `EVALUATION.rglob("*.md")` also scans immutable observed outputs and mistakes their wording for an instruction to future models.

On resource revision `29ff204`, `test_nothing_in_the_corpus_or_the_protocol_asserts_exact_prose` fails on the phrase “guaranteed to” in the preserved opinion-en_US draft, final artifact and supplied-input capture under `runs/rerun-349/`. This is generated evidence, not a new criterion or normative claim. Full failure: `docs/evaluation/editorial-329/validation/integration-pytest.log`; 1872 other tests pass. Altering or deleting that output to satisfy the scan would corrupt the required evidence.

## Acceptance criteria

- [ ] Preserve the original output files, failure log and frozen corpus bytes.
- [ ] Keep the assertion over the actual corpus and protocol/template contracts; exclude observed-run artifacts and historical records from normative scanning.
- [ ] Independently review the scope change and run the focused test plus all four CONTRIBUTING checks.

---
Written against 29ff204
