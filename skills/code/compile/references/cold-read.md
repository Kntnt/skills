# Cold-read verdict

Fill this brief only after a candidate bundle is complete. Launch one fresh-context subagent on the exact inherited main seat and give it only the bundle and a clean detached tree at the captured `HEAD`, with this filled brief naming both. It receives no tracker access, compiler notes, prior verdict, or explanation of what the compiler meant.

## Inputs

- Bundle: `<absolute-candidate-bundle-path>`
- Clean detached tree: `<absolute-worktree-path>`
- Captured repository identity: `<host/owner/repository>`
- Captured integration branch and full HEAD: `<branch> <object-id>`

## Verdict task

Cold-read the bundle as the complete contract a fresh executor would receive. Read `$LIBRARY/references/compiled-plan.md` from the clean tree's installed Manager boundary only when the bundle directs you there for validation; do not seek missing intent from the tracker, conversation, compiler, or peer Skill internals.

Return `PASS` only when every check below succeeds. Return `FAIL` with concrete findings otherwise; each finding names the bundle path or tree evidence, the requirement that fails, and whether the defect is mechanical or exposes an owner-owned gap.

1. State the delivered goal, exact scope, invariants, and STOP conditions from the bundle alone. Fail if a requirement must be invented or recovered elsewhere.
2. Locate every current-context excerpt in the clean tree and verify its source blob and line span at the captured commit.
3. Materialise the exact compiler-owned overlay without changing it, run every focused command, and reproduce the expected red result at the intended behavioural assertion rather than at syntax, import, fixture, collection, environment, or unrelated behaviour.
4. Map every acceptance criterion named in the plan to one machine check, then verify that footprint compliance and compiler-owned-test integrity have their own criteria.
5. Verify the exact footprint and allocations against the clean tree: every path exists or is absent as its class says, write classes are disjoint, reads support actual plan content, serial registries exist, assigned identifiers are available, and another identifier would stop execution.
6. Verify `manifest.json`, plan prose, overlay entries, command references, done-criterion references, source identities, and bundle fingerprint agree internally.
7. Inspect the Advisory appendix for requirements smuggled outside the Binding contract. Fail if following or rejecting its advice could change scope, intent, invariants, tests, or done criteria.
8. Name every point at which the executor would still have to choose product behaviour, architecture direction, priority, risk, or scope. Any such point is an owner-owned finding and therefore FAIL.

## Return shape

On success, return exactly `PASS` followed by a compact evidence list covering the red assertion, acceptance-criterion count, footprint classes, allocations, and bundle fingerprint.

On failure, return `FAIL` followed by numbered findings. Mark each `mechanical` where the compiler can correct the bundle without changing intent, or `owner-owned` where the durable source cannot honestly settle it. Do not propose implementation code and do not repair the bundle.

A mechanical correction receives a new cold reader in another fresh context. An owner-owned finding parks only that ticket. This context never reviews a correction it requested.
