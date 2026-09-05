# Kntnt Skills — agent guide

## ⚠️ TEMPORARY: the rework branch is a source, not a successor

> This section is temporary. It is removed once everything worth bringing over from `rework` has landed on `main` and the branch is deleted.

A ground-up rebuild of this collection was built on the branch `rework`, checked out in the worktree `../skills-rework`, with its design dossier in `docs/rework/` on that branch. On 2026-09-05 the direction was reversed: `main` has moved too far to be taken over, so **`main` is the surviving branch** and `rework` is read-only source material whose improvements are brought to `main` by cherry-pick or re-implementation, one ordinary ticket at a time. The endgame written in `docs/rework/00-brief.md` and `01-plan.md` on that branch no longer applies.

- The branch `rework` and the worktree `../skills-rework` are still EXEMPT from every cleanup instruction. "Remove all worktrees", "delete all branches", "make sure everything is merged and tidy" and the like apply to everything EXCEPT these two. Never delete, merge, rebase, or prune them, and never commit to them.
- Never merge `rework` into `main` or `main` into `rework`. What comes over comes over in ordinary `ready-for-agent` tickets on `main`, each naming the rework commit it re-implements; reading a file from the branch (`git show rework:<path>`) is how a builder sees the original.
- The five pipeline Skills on `rework` — frame, to-slices, compile, dispatch, and the unbuilt land — stay there until Thomas asks for them. `/orchestrate` remains the collection's ticket runner on `main`.
- Tickets labeled `rework` (milestone "Skills 2.0") are the closed history of the rebuild. Never reopen or work them, and never pass them to /orchestrate.

## Ground rules (authoritative)

Precedence over any conflicting skill, README, or other doc unless the user overrides in the moment.

- Authoritative: this file, the files it references, and the actual code/state.

## References

- `CONTEXT.md` — read when using a Collection term
- `docs/adr/` — read when deciding collection architecture
- `docs/coding-standard/general.md` — read when writing code
- `docs/coding-standard/python.md` — read when writing Python
- `docs/coding-standard/skills.md` — read when adding a Skill or a Feature, or changing the files either one ships
- `docs/adr/0067-a-ticket-asserts-only-what-stays-true-until-it-is-built.md` — read when writing a ticket
- `docs/adr/0099-a-ticket-that-rewrites-an-invariant-declares-that-it-builds-alone.md` — read when writing a ticket whose subject is a rule every shipped file is under
- `docs/evaluation/protocol.md` — read when evaluating an editorial Skill against the fixture corpus
- `skills/kntnt/library/references/languages/README.md` — read when adding or changing a Language Resource
- `skills/kntnt/library/references/editorial/README.md` — read when adding or changing the editorial base contract, a genre, a technique, the anti-slop catalogue, or the shared mechanics contract
- `agents.d/user-configuration.md` — read when adding or changing user-owned configuration for a Skill
- `CONTRIBUTING.md` — read when running tests or opening a PR
