# Kntnt Skills — agent guide

## ⚠️ TEMPORARY: protected rework state

> This section is temporary. It is removed by the rework's final cleanup ticket, once `rework` has merged into `main`.

A ground-up rebuild of this collection is in progress on the branch `rework`, checked out in the worktree `../skills-rework`. Its design dossier lives in `docs/rework/` on that branch.

- The branch `rework` and the worktree `../skills-rework` are EXEMPT from every cleanup instruction. "Remove all worktrees", "delete all branches", "make sure everything is merged and tidy" and the like apply to everything EXCEPT these two. Never delete, merge, rebase, or prune them.
- Tickets labeled `rework` (milestone "Skills 2.0") belong to the rebuild. Their ready state is `rework-ready-for-agent` — never add the plain `ready-for-agent` label to them, never work them from an ordinary session, and never pass them to /orchestrate, not even by explicit ticket number. Rework sessions, conversely, leave `ready-for-agent` tickets alone.
- The only rebuild artifact permitted on `main` is this section.
- On this branch (`rework`) only: agents commit and push to `origin rework` at their own discretion — no approval from Thomas needed (standing authorization, 2026-08-25). `main` keeps its own convention (commit per ticket, never push). Before working here, read `docs/rework/00-brief.md` and `docs/rework/01-plan.md` in full.

## Ground rules (authoritative)

Precedence over any conflicting skill, README, or other doc unless the user overrides in the moment.

- Authoritative: this file, the files it references, and the actual code/state.

## References

- `CONTEXT.md` — read when using a Collection term
- `docs/adr/` — read when deciding collection architecture
- `docs/rules/collection.md` — read when changing what a Manager verb promises, how the collection reaches a machine, or how a Skill routes delegated work
- `docs/rules/general.md` — read when writing code
- `docs/rules/python.md` — read when writing Python
- `docs/rules/skills.md` — read when adding a Skill or changing the files one ships
- `docs/rules/tickets.md` — read when writing a ticket
- `docs/evaluation/protocol.md` — read when evaluating an editorial Skill against the fixture corpus
- `skills/kntnt/library/references/languages/README.md` — read when adding or changing a Language Resource
- `skills/kntnt/library/references/editorial/README.md` — read when adding or changing the editorial base contract, a genre, a technique, or the anti-slop catalogue
- `CONTRIBUTING.md` — read when running tests or opening a PR
