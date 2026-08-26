---
name: to-slices
description: Turn one complete Frame Record into an approved decision issue and executable tracer-bullet child tickets.
disable-model-invocation: true
argument-hint: '[--yes] [<frame-record>] [-- <instruction>]'
compatibility: Requires git, gh, and uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "git gh uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# to-slices

Turn one complete Frame Record into the durable decision issue and executable child tickets that later pipeline Skills consume. Slicing is synthesis: preserve the owner's outcome and settled decisions while choosing thin delivery paths, verification seams, and only the blocking edges that express necessity.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is `library/` under the Manager directory that contains the checker — absent, tell the user to run `/kntnt update`, then stop.

## Invocation

Read `$LIBRARY/references/invocation-envelope.md` and follow it before help routing or formal validation; only the Formal Invocation reaches Help, Arguments, scripts, and nested formal parsers. `--help`, `-h`, and `help` print `$HERE/help.md` verbatim and stop.

## Arguments

`/to-slices [--yes] [<frame-record>]`, and nothing else. The order is part of the form: an operand written before a flag is refused, not repaired.

- `--yes` — assume yes at the approval checkpoint. It pre-approves the first complete proposal; it never fills an incomplete record, selects among records, or answers a missing owner decision.
- `<frame-record>` — the path to one Frame Record. Omitted, use the only record under `.kntnt/frames/`; no record produces the `/frame` handoff, and several records require the user to select one.

An undeclared flag, more than one operand, or an operand before `--yes` is an invalid form. Refuse it as `$LIBRARY/references/invocation-envelope.md` says, then publish nothing and stop.

## Preflight

Read `$LIBRARY/references/frame-record.md` and validate the selected record before synthesis. The seven headings are present in order; sections 1 through 7 carry the content their contract requires; every entry requiring an address has one; every active ledger decision names a frame from section 2; and every open entry names its owner and what would answer it. A malformed or incomplete record stays unchanged: name every defect, hand it back as `/frame --resume=<path>`, and stop.

Read the framing commit from section 1 and resolve it with `git rev-parse --verify`. If it differs from `HEAD`, inspect `git diff --name-only <framing-commit>..HEAD`. A move is framing knowledge only when every changed path is named in section 7 and the diff contains no other path. Verify that containment, update section 1 to `HEAD`, and continue. Otherwise name the paths that make the findings meaningfully stale, hand the record back as `/frame --resume=<path>`, and stop.

Resolve every section 7 knowledge entry from committed history. For a repository path, use `git cat-file -e HEAD:<path>`, then verify that exact heading or line in the committed blob where the address qualifies the path; resolve a commit address as an object reachable from `HEAD`. A missing entry that exists in the working tree is local-only: name the entry and file, ask the owner to commit that knowledge, stage or commit nothing, preserve the record, and stop. A missing entry with no local counterpart is an incomplete record and takes the `/frame --resume=<path>` handoff.

Read the repository's configured tracker convention from its always-loaded agent file and the issue-tracker document that file selects. Resolve the applicable scope labels, executable ready state, and milestone from that convention and any Contextual Instruction. Use `git remote` to identify the GitHub repository, `gh auth status` to verify access, and read the current labels and milestone before synthesis. Ambiguous publication configuration is a preflight refusal, not an owner-design question: name what is missing, preserve the record, publish nothing, and stop.

## Synthesis

Read `$LIBRARY/references/slices.md` for the durable parent and child shapes, then read [`slicing.md`](references/slicing.md). Synthesize the complete decision issue from what remains true after the record is consumed: the outcome, scope, active owner and ledger decisions, binding constraints, approved slice snapshot, open experiments, complete knowledge manifest, and provenance. Raw recon trails, superseded alternatives, and interview machinery stay behind.

The decision issue is always a new or recovered publication of this Skill. Where the Frame Record names a source issue, link it under Provenance and otherwise leave its body, state, labels, and relations untouched.

Cut the child set as tracer bullets sized for one fresh context. Make every child independently demonstrable or verifiable through its seam, use expand–contract where a wide change cannot remain green in one slice, turn experiment-owned unknowns into spike children, and declare a Solo Ticket only where its subject rewrites or newly enforces a repository-wide invariant. Blocking edges express implementation or verification necessity; preferred order, shared files, and likely conflicts are not blockers.

Keep the durable layer free of code excerpts, line numbers, current-state inventories, reserved serial numbers, exact implementation commands, and exhaustive enumerations sibling work can falsify. Stable areas, symbols, exemplar patterns, and addresses may orient later compilation. Use the current `HEAD` as the publication commit and every child's vantage point.

## Approval

Render the complete decision issue and every proposed child before publication. For each child show its title, delivered behaviour, seam contract, blockers, and whether it builds alone. Ask one yes-or-no question: whether the granularity and blocking edges of this complete proposal are approved.

A requested merge, split, or edge correction produces a new complete preview before the question is asked again. A missing product or architecture decision is incomplete framing: name it, preserve the record, hand it back as `/frame --resume=<path>`, and stop. Technical choices inside the established frames remain visible in the preview and are this Skill's to make.

With `--yes`, render the same complete proposal, treat that first complete proposal as approved, and proceed without asking. The flag never approves a proposal that cannot be completed from the record.

## Publication

Read [`publishing.md`](references/publishing.md) only after one complete graph is approved. Publish or recover the decision issue and children in dependency order, apply the configured labels and milestone, establish native parent and blocking relations where the tracker exposes them, and use the shared contract's body fallbacks only where it does not.

Read the entire published set back. Success requires the decision issue, every child, their exact approved bodies, states, labels, milestone, parentage, and every blocking edge to agree with the approved graph. Only then delete the Frame Record. A partial or conflicting publication keeps it as the recovery baton and reports exactly what exists, what is missing, and what conflicts.

## Completion

Close in the register of `$LIBRARY/references/tldr-mode.md`: name the decision issue, the approved children, the current unblocked frontier, and any unresolved publication state. The decision issue remains open and carries no executable ready label; every child receives the configured ready state. After complete verified publication, hand over the exact next line with every executable child in approved snapshot order: `/compile #<child> #<child> ...`.
