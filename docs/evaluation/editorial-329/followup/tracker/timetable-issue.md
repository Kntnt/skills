## What to build

Part of #329. Preserve the distinction between an explicitly qualified policy proposal and an unsupported factual guarantee during source-blind review. The complete candidate `opinion-absence-en_GB-r2` text asks trustees for an eight-week deferral while explicitly acknowledging no evidence that a feasibility study can finish in that time. Redline calls the timetable an unresolved defect requiring new evidence or a changed position, although the text asserts no guaranteed completion.

The initial failure and three exact-input neutral replays are retained under `docs/evaluation/editorial-329/followup/`; two of three replays repeat the finding and one is clean. Diagnose the existing opinion and shared review contracts, then make the smallest general repair justified by that evidence. Do not prescribe a fixture-specific ending or weaken detection of actual contradictions and unsupported factual claims.

## Acceptance criteria

- [ ] Preserve failed runs and independent R1 assessments under the frozen rubric.
- [ ] Qualified advocacy is judged as advocacy; a proposed deadline alone is not a factual guarantee of feasibility.
- [ ] Repeated source-blind runs on the full failed artifact avoid the false positive, with a separate genuine unsupported-certainty control still detected.
- [ ] Run the four CONTRIBUTING checks for the integrated change.

---
Written against 8f92e12
