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

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

The payload's `capabilities` are the half of the check no script can do — you are the harness, so you answer. For each one, say whether its `confirm` sentence is true of you. Any that is not: give its `how`, do no work, install nothing, stop. Exit 0 is not a go-ahead until every one is answered.

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is `library/` under the Manager directory that contains the checker — absent, tell the user to run `/kntnt update`, then stop.

## Invocation

Read `$LIBRARY/references/invocation-envelope.md` and follow it before help routing or formal validation; only the Formal Invocation reaches Help, Arguments, scripts, and nested formal parsers. `--help`, `-h`, and `help` print `$HERE/help.md` verbatim and stop.

## Arguments

`/ready-for-agent-check [#<ticket> ...]`, and nothing else. Every argument is a ticket reference; there are no flags, and none is missing.

Anything else is an invalid form. Refuse it as `$LIBRARY/references/invocation-envelope.md` says, then check nothing and stop.

## Steps

1. Settle which tickets are in scope. Named none: every open ticket the tracker labels `ready-for-agent`. Named some: exactly those, whatever label each carries — a ticket is worth checking before it is labelled, and refusing one for want of the label would put the check after the decision it exists to inform. A reference nothing resolves — a number the tracker does not know, something that is not a number, or one written as `owner/repo#number` — is named as such and nothing is checked. Where the scope is empty, say so and stop. Done when the set is settled, or you have stopped.
2. Read each ticket in the set whole: the body it was filed with, and every comment on it since, oldest first, each with its author and date. Take it from the tracker rather than from anything you remember. The requirement is the thread and not the body — in this collection the settled decisions and the acceptance criteria usually arrive as a comment, so a ticket read as its body alone is a ticket read as its untriaged self. Done when every ticket in scope is held whole.
3. Review each ticket in its own subagent, started together rather than one after another. Read [`review.md`](references/review.md), fill it in per ticket, and give each subagent the filled-in brief and nothing else. **Never review a ticket in this context, and never tell a reviewer anything about the ticket that is not in the ticket.** A session that helped write the ticket knows what it meant, and knowing what it meant is exactly the advantage the builder will not have — a reviewer given it agrees with the ticket for reasons the ticket does not carry, and the check reports a readiness nothing on the tracker supports. Done when every ticket in scope has a verdict.
4. Report the verdicts as they came back, ticket by ticket, and change nothing on the tracker. For each ticket: whether a builder could carry it start to finish, then every stop and every cost the reviewer named, each quoting the sentence it is about. Where a reviewer found a claim the repository no longer bears out, give what the ticket says and what is there now, so the fix is a matter of reading rather than of looking. Say plainly that this is advice and not a label: nothing was written, no state moved, and what to do about a stop is the maintainer's to decide. Where every ticket passed, say that too — an empty report and a clean one are not the same answer. Done when the user has that report.
