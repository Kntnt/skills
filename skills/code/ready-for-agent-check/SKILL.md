---
name: ready-for-agent-check
description: Read the tracker's ready-for-agent tickets the way an unattended builder will — one subagent per ticket, in a context that did not write it — and report what would stop that builder, before a run spends a wave finding out.
disable-model-invocation: true
argument-hint: '[#<ticket> ...] [-- <instruction>]'
compatibility: Requires gh and uv, plus a harness that can run subagents
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "gh uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: "subagents"
---

# ready-for-agent-check

Find out whether a ticket can be built by somebody who has only the ticket. Each one is read by a subagent that did not write it, against the repository as it now stands, and what comes back is the sentence a builder would stop at.

`$HERE` is the directory that contains this SKILL.md, and `$MANAGER` is the Manager directory: `$HERE/../kntnt/` if it exists, else `kntnt/` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Neither found: tell the user to install the Manager (`npx skills add Kntnt/skills`) and stop. `$LIBRARY` is `$MANAGER/library/` — absent, tell the user to run `/kntnt update`, then stop.

Run `uv run "$MANAGER/scripts/kntnt.py" invoke --here="$HERE"` with the invocation payload — everything the user typed after `/ready-for-agent-check`, verbatim, however many lines — on stdin. On exit 0, answer the `capabilities` in its `dependencies` first: for each one, say whether its `confirm` sentence is true of you, and where it is not, give its `how`, change nothing, and stop. Then continue from the JSON. On any other exit print its stdout verbatim and stop: it has already printed what the user is to see, and none of that text is yours to write.

In the JSON, `path` is the command path as a list, `flags` holds each flag the user wrote — `true` where it stood bare, its value where it carried one, a list of values where it was repeated — `operands` is what followed the flags, in order, and `instruction` is the Contextual Instruction, or `null`, applied as `$LIBRARY/references/invocation-envelope.md` says.

## Arguments

Every operand is a ticket reference, and step 1 says what naming none means. This grammar declares no flag, so a dash-prefixed token is a reference like any other, and one nothing resolves.

## Steps

1. Settle which tickets are in scope. Named none: every open ticket the tracker labels `ready-for-agent`. Named some: exactly those, whatever label each carries — a ticket is worth checking before it is labelled, and refusing one for want of the label would put the check after the decision it exists to inform. A reference nothing resolves — a number the tracker does not know, something that is not a number, a dash-prefixed token among them, or one written as `owner/repo#number` — is refused as `$LIBRARY/references/invocation-envelope.md` says: name it, check nothing, and stop. Where the scope is empty, say so and stop. Done when the set is settled, or you have stopped.
2. Read each ticket in the set whole: the body it was filed with, and every comment on it since, oldest first, each with its author and date. Take it from the tracker rather than from anything you remember. The requirement is the thread and not the body — in this collection the settled decisions and the acceptance criteria usually arrive as a comment, so a ticket read as its body alone is a ticket read as its untriaged self. Done when every ticket in scope is held whole.
3. Review each ticket in its own subagent, started together rather than one after another. Read [`review.md`](references/review.md), fill it in per ticket, and give each subagent the filled-in brief and nothing else. **Never review a ticket in this context, and never tell a reviewer anything about the ticket that is not in the ticket.** A session that helped write the ticket knows what it meant, and knowing what it meant is exactly the advantage the builder will not have — a reviewer given it agrees with the ticket for reasons the ticket does not carry, and the check reports a readiness nothing on the tracker supports. Done when every ticket in scope has a verdict.
4. Report the verdicts as they came back, ticket by ticket, and change nothing on the tracker. For each ticket: whether a builder could carry it start to finish, then every stop and every cost the reviewer named, each quoting the sentence it is about. Among those are the inferences the reviewer had to make to get past a sentence — an intent it supplied, a reading it chose between, a fact it went and found — each carried under its own stop or cost and never as a class of its own, because what the maintainer has to read is the gap the ticket left and not the gap the reviewer happened not to have. Where a reviewer found a claim the repository no longer bears out, give what the ticket says and what is there now, so the fix is a matter of reading rather than of looking. Say plainly that this is advice and not a label: nothing was written, no state moved, and what to do about a stop is the maintainer's to decide. Where every ticket passed, say that too — an empty report and a clean one are not the same answer. Done when the user has that report.
