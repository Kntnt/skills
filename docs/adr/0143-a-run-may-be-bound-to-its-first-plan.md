# A run may be bound to its first plan

Orchestrate already resolves its complete frontier before it claims anything, but a caller that independently inspected a dry plan could not bind the subsequent real invocation to that same plan. Repeating the invocation authorized whatever frontier existed when the real plan ran, so a caller either accepted that drift or paid for another interaction after every preflight.

**A caller may authorize the first plan of an Orchestrate invocation by supplying its canonical approval identity.** The identity covers the branch and default-branch names, resolved scope, concurrency ceiling and working-tree mode, model and deliberation locks, waves in order, and Solo Tickets. It deliberately excludes ticket bodies, comments, and the base commit: the question step may add comments before later plans, and a commit landing on the branch changes neither the named run nor its authorized frontier.

The engine computes SHA-256 over a versioned domain prefix and compact, key-sorted UTF-8 JSON. It emits that identity on every plan. A supplied identity is compared before routing or claiming; a mismatch makes the plan unready and records the expected identity, computed identity, and canonical payload beside empty claim and starting lists. That audit is the only state a real mismatch writes. A dry run writes nothing.

The expectation belongs to the first plan of an invocation rather than every plan in its workflow. The Skill passes it once. A matching plan records it durably, later unflagged plans preserve it, and an unflagged plan neither creates nor clears an expectation. A mismatch remains unmet until another flagged plan matches, and the claim verb refuses while it remains unmet. This preserves the question step's deliberate re-planning after thread answers without letting an unflagged plan erase a failed authorization.

The option is additive and absent by default. A caller that supplies no identity receives the existing plan and workflow, apart from the plan's new identity fields, while a caller that already knows the exact plan can collapse its external authorization handshake into the engine's comparison.

What this costs is a small durable projection of fields already present in the plan and a versioned serialization contract that future changes must preserve or explicitly replace. In return, the authorization remains exact while no second caller turn is required merely to compare two equal plans.
