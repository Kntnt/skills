## What to build

Part of #329. Reconcile the shared delivery contract with consumer instructions when a review changes no prose but leaves unresolved findings. At the vantage commit, `references/delivery.md` requires status-only for every unchanged response; Redline and Unslop explicitly require the complete artifact when findings remain. The repeated timetable probes follow the latter instruction, so this is an instruction collision, not evidence of disobeying an unambiguous rule.

Put the destination behavior in the shared contract and have every consumer defer to it: a clean unchanged response is status-only; unresolved findings accompany the full response-target artifact; unchanged in-place files are not rewritten and findings accompany status; an explicit separate destination receives the complete artifact and the response reports the destination and findings without repeating it.

## Acceptance criteria

- [ ] One shared rule defines unchanged delivery and every affected consumer agrees with it.
- [ ] Native response, in-place and separate-file runs exercise unchanged prose with unresolved findings, retaining complete evidence and checking filesystem effects.
- [ ] Clean no-change behavior and explicit-destination no-echo behavior remain intact.
- [ ] Run the four CONTRIBUTING checks for the integrated change.

---
Written against 8f92e12
