# Compiled plan Interface

A compiled plan is the clone-local execution contract that `/compile` writes and `/dispatch` consumes. This document is the shared Interface between them: it fixes the bundle, the mechanically checkable identities, the exact footprint and allocations, the freshness test, compiler-owned seam tests, and the bundle lifecycle. Neither Skill owns the other's side of the contract.

The durable intent comes from the executable child and its parent under the [durable slice contract](slices.md). The contributor-facing promises that pipeline Skill authors must keep uniform are in the [pipeline rules](../../../../docs/rules/pipeline.md). This Interface carries current implementation state and runtime detail that belongs in neither durable tickets nor authoring rules.

## Bundle location and shape

An accepted-bundle slot lives below the repository's Git common directory at `kntnt-pipeline/plans/<ticket>/`, where `<ticket>` is the decimal issue number without `#`. Resolve the base with `git rev-parse --git-common-dir`; `.git/kntnt-pipeline/plans/<ticket>/` is the ordinary main-worktree spelling, not an assumption that `.git` is a directory in every worktree.

The slot holds immutable bundle directories below `bundles/<fingerprint-hex>/` and one regular file named `accepted`. That pointer's complete contents are `bundles/<fingerprint-hex>` plus one LF, where `<fingerprint-hex>` is the 64 lowercase hexadecimal characters after `sha256:` in the accepted manifest. The pointer is slot metadata rather than a fourth bundle part; reading it once selects one complete immutable directory.

Every immutable bundle directory contains exactly three parts:

- `plan.md` — the complete executor brief, with one binding contract and one advisory appendix.
- `manifest.json` — the mechanically checked subset of the contract, with no independent product intent.
- `tests/` — the compiler-owned test overlay, mirroring each file's repository-relative destination below this directory.

No tracker comment, repository document, compiler note, or dispatch journal is a fourth part of the bundle. An executor receives the complete plan and materialised tests without needing the tracker or a peer Skill's private files.

## `plan.md`

The plan uses these headings in this order:

```
# Compiled plan for #<ticket>

## Binding contract

### Identity and provenance
### Goal
### Scope and footprint
### Invariants
### Current implementation context
### Seam tests
### Verification
### Done criteria
### STOP conditions

## Advisory appendix
```

The binding contract is the execution boundary. The advisory appendix is a replaceable route inside it: an executor may ignore every proposed step while still owing every binding provision.

### Identity and provenance

State the repository identity, integration branch, full HEAD object ID, child and parent issue references, child source fingerprint, parent source fingerprint, and the location of the bundle fingerprint. The line for the last identity is `Bundle fingerprint: manifest.json#bundle.fingerprint`; `plan.md` names the manifest field instead of copying its value, because literal digest bytes inside a file covered by that digest would be self-referential. Name the compiler's captured time only as report context; time does not contribute to freshness.

The child source fingerprint covers a canonical snapshot of the child's number, title, complete body, every comment oldest first, parent relation, and native blocking relations or their documented fallbacks. The parent source fingerprint covers a canonical snapshot of the parent's number, title, complete body, and every comment oldest first. Comment identity, author, creation time, and body are retained in snapshot order, so editing, deleting, or adding a comment changes the relevant fingerprint.

Canonical JSON in this Interface means the JSON Canonicalization Scheme defined by [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785), including its UTF-8 encoding, deterministic property order, and exact string-escape spellings. The manifest schema further admits strings, integers, booleans, null, arrays, and objects but no floating-point values. A source fingerprint is `sha256:` followed by the lowercase SHA-256 digest of its RFC 8785 bytes.

#### Canonical source snapshots

The canonical child snapshot has exactly the keys and value shapes in this object:

```json
{
  "issue": {
    "number": 181,
    "title": "State the compiled-plan Interface and shared pipeline rules",
    "body": "## What to build\n\n..."
  },
  "comments": [
    {
      "id": "IC_example_child",
      "author": "thomas",
      "created_at": "2026-08-26T08:00:00Z",
      "body": "One later clarification."
    }
  ],
  "parent": "#180",
  "blocked_by": ["#179"]
}
```

The canonical parent snapshot has exactly the keys and value shapes in this object:

```json
{
  "issue": {
    "number": 180,
    "title": "Compile ready slices into accepted executor plans",
    "body": "## Outcome\n\n..."
  },
  "comments": [
    {
      "id": "IC_example_parent",
      "author": "thomas",
      "created_at": "2026-08-26T07:00:00Z",
      "body": "The approved decision remains unchanged."
    }
  ]
}
```

Issue and comment bodies are the exact strings returned by the tracker, including their line endings. Comments are ordered by `created_at` oldest first, then by `id` when creation times tie; an issue with no comments uses an empty array. No tracker response field outside the shown shape enters either snapshot.

Native relations are authoritative when available. The contract's `Parent` and `Blocked by` fallback lines are parsed only when the native surface is unavailable. Both surfaces normalize to local `#<ticket>` strings: one `parent` value and a `blocked_by` array in ascending issue number. Relation provenance is not included, so identical logical relations produce identical snapshot bytes on native and fallback tracker surfaces.

### Goal

State the child's delivered behaviour in the parent's outcome and decisions. Preserve product intent without turning an advisory implementation preference into a requirement.

### Scope and footprint

State the complete exact footprint under the classes defined below. Explain the boundary in executor terms, including why any fresh implementation finding that would cross it is a STOP condition rather than implied authority.

### Invariants

Inline every repository rule and parent constraint the executor must preserve closely enough that execution needs no rules archaeology. Give each source address, but do not make following the address necessary to understand the binding provision.

### Current implementation context

Give the exact repository-relative files, stable symbols, line-qualified excerpts, and present behaviour as they stand at the captured full HEAD. An excerpt identifies its source blob and line span so the consumer can prove it still describes that commit.

### Seam tests

For every file below `tests/`, state its repository-relative test destination, base blob, compiled blob, focused command, and expected red result on the captured HEAD. The red result identifies the intended failing assertion and distinguishes it from syntax, import, fixture, collection, or environment failure.

### Verification

State each focused command and the complete repository gate with its working directory, environment assumptions, and expected successful result after implementation. Commands are executable strings rather than paraphrases; destructive, interactive, or network-dependent behaviour is named explicitly.

### Done criteria

Give every acceptance criterion one stable identifier and one machine check, then add separate criteria for exact footprint compliance and compiler-owned test integrity. A criterion states the observed result and the command or built-in comparison that decides it; repeating ticket prose under a checkbox is not a check.

### STOP conditions

Stop when the repository identity, integration branch, full HEAD, child source, parent source, or bundle no longer matches; when a required dependency is absent; when execution needs an unallocated serial identifier or a path outside its write footprint; when a seam test would have to change; when the baseline differs from the one recorded; or when proceeding would invent an owner decision. A stopped executor reports the condition and changes nothing further.

### Advisory appendix

Give an ordered implementation route, current exemplars, likely edit points, and useful focused commands. Mark every part as advice. The appendix cannot add scope, weaken an invariant, redefine a seam test, or create a second done criterion.

## `manifest.json`

The manifest makes provenance, artifact integrity, scope, allocation, test ownership, commands, and done-criterion identities checkable without parsing prose. It does not repeat the goal, invariants, implementation context, or STOP conditions; those remain in the binding contract, and a manifest field that restates them would become a second source of product intent.

This is the complete field shape; arrays may be empty, but no key is optional:

```json
{
  "schema": "kntnt.compiled-plan/v1",
  "repository": {
    "identity": "github.com/Kntnt/skills",
    "integration_branch": "rework",
    "head": "0123456789abcdef0123456789abcdef01234567"
  },
  "source": {
    "ticket": "#181",
    "parent": "#180",
    "child_fingerprint": "sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    "parent_fingerprint": "sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
  },
  "bundle": {
    "fingerprint": "sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
  },
  "footprint": {
    "reads": ["skills/kntnt/library/references/slices.md"],
    "modifies": ["skills/code/example/SKILL.md"],
    "creates": [],
    "deletes": [],
    "compiler_owned_tests": ["tests/test_example.py"],
    "dispatcher_owned_writes": ["skills/kntnt/catalog.json"],
    "serial_resources": ["docs/adr"]
  },
  "allocations": [
    {
      "registry": "docs/adr",
      "identifiers": ["0113"]
    }
  ],
  "tests": [
    {
      "destination": "tests/test_example.py",
      "base_blob": null,
      "compiled_blob": "git:0123456789abcdef0123456789abcdef01234567",
      "command_id": "seam",
      "baseline_exit": 1,
      "baseline_assertion": "test_example_contract"
    }
  ],
  "commands": [
    {
      "id": "seam",
      "run": "uv run --with pytest pytest -q tests/test_example.py",
      "working_directory": ".",
      "environment": {},
      "expected_exit": 0
    }
  ],
  "done_criteria": [
    {
      "id": "AC-1",
      "checks": ["command:seam"]
    },
    {
      "id": "scope",
      "checks": ["footprint"]
    },
    {
      "id": "test-integrity",
      "checks": ["compiler-owned-tests"]
    }
  ]
}
```

The repository identity is the canonical tracker host and owner/name resolved from the current repository rather than the spelling of one remote URL. The integration branch is the branch on which accepted execution will land, and `head` is the full object ID that branch pointed to when compilation captured its vantage.

The source object carries the child source fingerprint and parent source fingerprint separately, so a consumer can name which durable input moved. `ticket` and `parent` are local `#` references in the identified repository. The footprint, serial allocations, tests, verification commands, and done-criterion identifiers use the definitions below.

`base_blob` is the Git blob object ID at the captured HEAD, prefixed `git:`, or null when the test destination does not yet exist. `compiled_blob` is the Git blob object ID of the compiler-owned bytes. Both use the repository's object format rather than assuming SHA-1.

Every `done_criteria` entry repeats only the stable identifier from `plan.md` and identities of mechanical checks. `command:<id>` points into `commands`; `footprint` and `compiler-owned-tests` are consumer comparisons defined by this Interface. Natural-language acceptance criteria do not belong in the manifest.

## Bundle fingerprint

The bundle fingerprint is `sha256:` plus the lowercase SHA-256 digest of one length-delimited stream. Reproduction first parses `manifest.json`, serialises it with the bundle fingerprint field omitted so the digest excludes itself, and uses that canonical JSON value. This produces the canonical manifest bytes while leaving the accepted file's field populated.

The stream contains `manifest.json` with those canonical bytes, `plan.md` with its exact bytes, and every regular file below `tests/` with its exact bytes, all in lexicographic bundle-relative path order. The root entries are exactly `manifest.json` and `plan.md`; an overlay entry is exactly `tests/<repository-relative destination>`, so the example test contributes `tests/tests/test_example.py`. For each entry, feed its UTF-8 bundle-relative path, one NUL byte, its ASCII decimal byte length, one NUL byte, and its bytes into SHA-256. In short, every entry contributes its path, byte length, and bytes; the framing prevents two different path/content sets from producing the same stream by concatenation ambiguity.

The manifest file itself may be pretty-printed for a human reader. Its insignificant formatting does not affect the bundle fingerprint because the canonical manifest value is what enters the stream. A changed value, `plan.md` byte, test destination, or test byte changes the digest.

## Exact footprint

Every path is a normalized, repository-relative POSIX path with no leading slash, `.` segment, `..` segment, or trailing slash. Paths are literal and case-sensitive. Globs are forbidden. A directory cannot stand for unknown descendants, and wording such as “files under” or “files such as” is not a footprint.

The seven footprint classes have distinct ownership:

- `reads` names every committed path whose content the binding contract or advisory appendix depends on. Reading a path does not grant authority to write it.
- `modifies` names every existing path whose bytes the executor may change.
- `creates` names every absent path the executor may add.
- `deletes` names every existing path the executor may remove.
- `compiler_owned_tests` records compiler-owned test writes by destination; these paths are materialised and landed by `/dispatch`, never owned by the executor.
- `dispatcher_owned_writes` records dispatcher-owned shared writes such as a generated Catalog or shared append file; the executor proposes any needed content in its report but never changes these paths.
- `serial_resources` names every exact registry from which execution consumes a pre-allocated identifier.

The four write classes `modifies`, `creates`, `deletes`, and `compiler_owned_tests` are pairwise disjoint, and none overlaps `dispatcher_owned_writes`. A path may appear in `reads` and one write class when the plan depends on its old content before changing it. Every executor-created, changed, or deleted path must appear in its corresponding executor-owned class; a changed path in `reads` alone is out of footprint.

The consumer compares the post-execution tree with the captured HEAD, excluding materialisation performed by the dispatcher itself, and rejects any changed path outside `modifies`, `creates`, and `deletes`. It separately verifies compiler-owned tests and applies dispatcher-owned writes. Scope compliance is all-or-nothing: one out-of-footprint path rejects the complete execution result rather than being silently dropped.

## Serial allocations

Allocation happens once per batch and once per registry after recon has fixed every selected plan's count. For each registry, start above the highest committed identifier and every identifier held by other fresh plans at the same HEAD, then assign consecutive identifiers in deterministic ticket order from one shared counter. The manifest records the registry and exact identifiers assigned to this plan.

Gaps are never reused. An allocation that is accepted but never landed may remain a gap, and that cost is preferable to two fresh plans claiming one serial identity. A changed HEAD expires the allocation with the plan.

An executor uses only its recorded identifiers. An extra identifier is a STOP condition: execution does not rescan the registry, fill a gap, borrow a sibling's allocation, or extend its own range.

## Compiler-owned test overlay

The `tests/` tree mirrors repository-relative destinations exactly. Each regular file has one manifest entry, and every manifest entry has one file; symlinks, directories in place of files, and unlisted files are invalid. The base blob proves what the destination held at the captured HEAD, and the compiled blob proves the exact accepted test bytes.

Before acceptance, `/compile` overlays these bytes on the captured clean tree and records a focused red result at the intended assertion. `/dispatch` materialises the same bytes into the isolated executor tree and may make them non-writable as a read-only guardrail. That permission bit is not an operating-system security boundary: an executor running as the same user could replace it, so the verdict never trusts permissions.

After execution, `/dispatch` re-hashes every materialised test using the repository's Git blob algorithm and compares it with `compiled_blob`. A test that is changed, replaced, or deleted rejects the execution result even when its command is green. A file whose destination had a non-null base blob must also still be the accepted compiled blob rather than a merge of executor edits.

On approval, `/dispatch` lands the exact accepted bytes itself beside the implementation. Accepted compiler-owned seam tests therefore become permanent regression tests, and their authorship remains outside executor ownership from compilation through landing.

## Freshness

A bundle is fresh only while repository identity, integration branch, full HEAD, child source fingerprint, parent source fingerprint, and bundle fingerprint all match. The integration branch must still point to the named HEAD; merely having the commit object locally is insufficient. The source fingerprints are recalculated from current tracker snapshots, the bundle fingerprint is recalculated from the local artifact before consumption, and the selected directory's hexadecimal name must agree with that fingerprint.

Internal agreement is also required: the ticket directory matches `source.ticket`; every footprint path has a valid class; allocations name declared serial resources; every test file and entry correspond; every command and done-criterion reference resolves; and the prose and manifest do not contradict one another. Internal disagreement makes the candidate invalid rather than stale, because no earlier world can make a self-contradictory bundle executable.

A changed source or changed HEAD never triggers reconciliation. A stale bundle is never reconciled in place; `/compile` rebuilds the complete candidate against current inputs, reruns its acceptance gates, and replaces the stale bundle only after the candidate passes. `/dispatch` consumes only a fresh accepted bundle.

## Acceptance, replacement, recovery, and retirement

Compilation writes a complete candidate in a temporary sibling below `<ticket>/bundles/` on the same filesystem. Nothing writes into an immutable bundle directory or the `accepted` pointer. Only after the candidate's baseline, red seam test, cold read, manifest agreement, source fingerprints, HEAD, and bundle fingerprint pass does a rename publish it as `bundles/<fingerprint-hex>/`; the destination is absent, or an identical directory left by an interrupted acceptance is verified and reused.

After the immutable directory is present and verified, write its relative path to a temporary pointer file beside `accepted`, flush the complete file, and use one atomic rename to replace or create `accepted`. In a replacement, a consumer that reads the pointer observes the old complete bundle or the new complete bundle, never an absent canonical selection or a partial directory. Only after the new pointer is visible and resolves correctly may unreferenced immutable bundles be removed.

An interruption before the pointer rename leaves the previous accepted selection unchanged and may leave a complete unselected directory or temporary file; an interruption after it leaves the new selection complete. Recovery reads `accepted` once, validates the selected directory, and discards or reuses complete unselected candidates by fingerprint rather than merging contents.

Accepted siblings are independent. One ticket failing compilation or being parked does not roll back another ticket whose bundle was accepted. A batch-level changed HEAD restarts the batch because footprints and serial allocations must describe one shared vantage.

The bundle is clone-local and has no portable recovery promise. Losing the Git common directory loses the plan, and recompilation is the recovery. No plan or excerpt is posted to the tracker.

`/dispatch` removes the accepted bundle when the ticket lands or is parked after retaining only the run-journal evidence its own recovery contract requires. In other words, the bundle is retired when the ticket lands or is parked; an abandoned candidate or backup is not a durable archive.

## Worked bundle fixtures

These concrete states pin the distinctions a producer and consumer must preserve. Each row changes only what it says; every fact not named remains as in the valid row.

| Fixture | State | Required result |
| --- | --- | --- |
| Valid | Every Git, tracker-source, and bundle identity matches; execution changes only `modifies` and `creates`; every materialised test matches its compiled blob | Consume the bundle |
| Stale source | A new child comment changes the child source fingerprint; every Git and bundle identity still matches | Recompile and atomically replace the stale bundle |
| Changed HEAD | The integration branch now points to a different commit; every tracker-source and bundle identity still matches | Restart compilation for the batch at the new HEAD |
| Changed test | The canonical bundle is fresh, but a materialised test no longer matches its compiled blob after execution | Reject the execution result; do not land the test or implementation |
| Out of footprint | The canonical bundle is fresh, but execution changes `README.md`, which appears in no executor-owned write class | Reject the execution result; do not land any changed path |
