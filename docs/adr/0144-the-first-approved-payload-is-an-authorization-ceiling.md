# The first approved payload is an authorization ceiling

ADR-0143 made a matching caller-supplied approval durable across the later unflagged plans that Orchestrate deliberately runs after answering questions and advancing waves. That persistence correctly lets parking and ordinary progress remove work, but it also let a later frontier add a ticket, change an execution parameter, or drop a Solo constraint under an approval that never covered the change (issue #218).

**The first matched approval payload is an authorization ceiling for every later unflagged plan in the same invocation.** The fixed payload fields `branch`, `default_branch`, `scope`, `at_once`, `worktrees`, `model`, and `deliberation` remain equal. Every ticket in the later plan's waves appeared somewhere in the ceiling's waves. Every ceiling Solo Ticket that remains in the later waves remains Solo.

Wave order and membership among the remaining tickets are deliberately unconstrained. Orchestrate recomputes them from the tracker's current blocking graph on every plan, so completing or parking work may merge, split, or reorder waves without expanding the authorized frontier. Adding a Solo constraint likewise tightens rather than widens the first plan.

An unflagged plan outside the ceiling is unready and names the first changed fixed field, newly admitted ticket, or lost Solo constraint. It retains the original expected identity and payload as the audit ceiling, records the drifted plan identity, and marks approval unmet without replacing unrelated run state. The existing claim guard then refuses every ticket. A later flagged plan whose identity matches installs its payload as a new ceiling and makes approval met again.

Dry-run drift reports the same refusal without writing state, and a run that never supplied `--approval` retains its previous behavior. No new state field is needed: `approval_payload` already carries the first matched payload. The canonical payload and identity algorithm remain unchanged.

This decision narrows ADR-0143 only where it said every later unflagged plan preserves a met expectation. The first-plan approval, exact identity comparison, durable mismatch audit, and claim guard stand unchanged.

The cost is that a later plan must compare a small payload before it may start, and a branch change within one state directory must retain enough of the prior state to report drift rather than silently become an unrelated run. In return, removal and graph recomputation remain unattended while no new work or weakened constraint can inherit authority it was never given.
