---
name: plan
description: Turn tickets, or a design settled in conversation, into plans under plans/.
disable-model-invocation: true
argument-hint: '[#N...] | ["description"] [--yes]'
metadata:
  internal: true
  kntnt:
    binaries:
      - git
      - gh
      - uv
    externals:
      - improve
---

# plan

Turn Tickets, or a design settled in this conversation, into Plans under `plans/`, self-contained enough that `execute` can build them while you are away. This skill writes no code and closes no Ticket.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or another recorded Harness). Run `uv run "<checker>" check --here "$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md.

## Help

If the arguments are `help`, `--help`, or `-h`, emit the Arguments and Steps below and stop.

## Arguments

- `#N...` — plan these Tickets, whatever labels they carry.
- `"description"` — plan the work described, with no Ticket behind it.
- no arguments — pick from a list.
- `--yes` — plan every `ready-for-agent` Ticket without showing the list, and set aside anything the planner cannot specify honestly instead of asking about it.

An argument that starts with `#` and digits is a Ticket reference; anything else is a description.

## Steps

1. Selection. With `#N...`, read each Ticket (`gh issue view <n> --comments`) and note whether `ready-for-agent` was among its labels. With a description, that is the one item. With neither, show a checklist: first row, only when this conversation has settled a design worth building, the design itself; then every open `ready-for-agent` Ticket (`gh issue list --state open --label ready-for-agent --json number,title`), with the ones that already have a Plan shown as such and left unchecked. `--yes` takes every `ready-for-agent` Ticket that has no Plan and never the conversation row. A named Ticket that already has a Plan is asked about — skip it? — and `--yes` says yes, because planning the same Ticket twice unattended is the wrong default. Done when the selection is a list the user chose, or the `--yes` set.
2. One Plan per selected item, one item at a time, by running `/improve plan <the work>` with `plans/` as the target directory. For a Ticket, hand over its number, title, body, and comments. For the conversation row, hand over the settled design, and name `CONTEXT.md` and `docs/adr/` when the decisions are already written there. Done when every selected item has a Plan file or has been set aside.
3. Under `--yes`, add to that invocation: where the work cannot be specified honestly, say what is unanswered and stop rather than ask. Set that item aside with its reason and go on to the next — a Ticket labelled `ready-for-agent` that lands here had a label it did not live up to, and the report says so. Without `--yes`, let the questions be asked. Done when no item is waiting on an answer.
4. The set pass. Each Plan was written alone and has seen none of the others, so this is what turns them into a queue: give every new Plan the next free number in `plans/` without reusing one; write `**Ticket**:` with number and URL into the Status block of each Plan that came from one; work out `**Depends on**:` across the new Plans and the ones already there; then write `plans/README.md` with the execution order, the dependency graph, and a status table listing every Plan, the new ones as TODO. Read `**Issue**:` as a Ticket reference where an older Plan carries it, and write `**Ticket**:`. Done when the queue's order and dependencies are on disk.
5. Report one line per selected item: the Plan written and its number, or set aside and what was left unanswered. Name `/execute` as what builds them. Done when that report is shown.
