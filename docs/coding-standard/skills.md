# Coding standard — Skills

Read before adding a Skill to this collection, or changing the files an existing one ships.

This module covers the form of a Skill's own shipped files — its `SKILL.md`, its `help.md`, and what lives beside them. It is not about what a Skill does; it is about what every Skill of this collection carries regardless of what it does. Read `general.md` first, and `python.md` too where the Skill ships an engine.

Much of what follows is enforced by the test suite, and where it is, the assertion that fails names the rule and points back here. Not all of it is, and where the suite holds less of a rule than the rule says — the README paragraph nothing compares against anything, a manpage section checked for its heading and not for the prose beneath it — this document says so where the rule is stated, rather than leaving a contributor to infer it from a green run. Read a green fourth check as *nothing the suite watches broke*, never as *the form is right*.

The rules whose reasoning is settled in a decision record are named here in a phrase and cited to the record rather than argued again — the record is where the alternatives and their costs live, and a second telling of the argument is a second thing to keep true.

## Why this is written down as well as asserted

A rule that lives in two places can disagree with itself, and this collection's own preference runs towards a single copy a reviewer can diff. The contract is written twice anyway, and deliberately, because the two copies are read at different moments by readers in different positions.

A contributor who has not yet written anything cannot be helped by an assertion message: nothing has failed, because nothing exists to fail. This document is for that moment. A contributor whose suite has just gone red cannot be helped by a document they did not know to read: they have a heading and a path, and what they need is the rule. The assertion message is for that moment, which is why every test enforcing a rule below fails with the rule and its reason in a phrase, and a pointer here or to the record.

The copies stay together because only one of them states the rule in full. The message names the rule and cites where it is stated; it does not restate the reasoning, and this document does not reproduce the tests. What can drift is the pointer, and a citation to a record number that resolves to nothing fails the suite.

## `SKILL.md`

### Frontmatter

The frontmatter is YAML and is read by a real YAML parser, so anything YAML accepts is what the field means (ADR-0060).

- **`name`** is the Skill's directory name, exactly. **`description`** is the only hook the harness has for deciding when a Skill applies (ADR-0019), and the Catalog carries both.
- **The fields a Skill may carry** are the six the Agent Skills specification defines, plus `argument-hint` and `disable-model-invocation`, which the collection ships knowingly (ADR-0066). A ninth field fails the suite until the record accepts it too.
- **Every `metadata` key carries the `kntnt.` prefix and every value is a string** (ADR-0061). The namespace is flat and shared with every other collection, so an unprefixed key is a key anybody may claim; a value in any other shape is coerced by a foreign reader rather than refused, and lost without a word. A list is one space-separated string, an empty list an empty string.
- **The four dependency lists** — `kntnt.binaries`, `kntnt.skills`, `kntnt.externals`, `kntnt.capabilities` — are written even when all four are empty, and `kntnt.internal: "true"` marks the Skill as this collection's. The lists are hard requirements only: the checker exits 2 on anything in them (ADR-0012), so nothing a Skill degrades gracefully without belongs there. All four are written even where they are empty because a key nobody wrote is read as an empty list, which is the answer a Skill requiring nothing gives — so an omission cannot be told from a declaration once the key is gone.
- **`compatibility` names exactly the binaries the dependency lists hold**, no more and no fewer, and the Capabilities likewise (ADR-0062). It is the one field a reader outside this collection knows to look at. A requirement the Skill degrades gracefully without is named there in prose and deliberately not in the lists — `/release` and `gh` is the only such case today. A Skill with nothing to state carries no `compatibility` field at all rather than an empty one.

### Body

The body carries only what the agent executes, which is why prose is the seam a Skill is held at (ADR-0046).

- **The dependency preamble is present exactly when the dependency lists are not empty.** A Skill with nothing to declare calls no checker, because the call could only ever report an empty list and would itself declare `uv` (ADR-0012). Where the preamble is present it invokes the checker as `check --here "$HERE"` and names `npx skills add Kntnt/skills` as the fix for a missing Manager.
- **A `## Help` section** routes `--help`, `-h`, and `help` to `$HERE/help.md`, printed verbatim (ADR-0044). The heading is required and the route is required to sit under it: the suite reads the section out of every body the collection ships, the Manager's included, and asserts that it names `$HERE/help.md` and answers `--help` — one assertion for both. Looked for anywhere in the body those two tokens prove nothing, because the refusal clause every body carries names them already — a Skill whose `## Help` section was deleted outright would carry both and could no longer be asked what it does.
- **An invalid form is refused, never repaired or ignored.** The refusal names what was wrong, prints the `## Synopsis` section of `$HERE/help.md` verbatim, and points at `/<name> --help` for the page in full. The rule is stated in the body with the clause *A flag is refused rather than ignored where it has no work to do here*, closing on ADR-0059 — the record that carries it, and the one the suite pins that clause to.
- **A file the body opens only when the situation arises lives under `references/`** (ADR-0063). The published addresses — `help.md` beside `SKILL.md`, and the Manager's `catalog.json`, `steps/`, and `help/` — stay where they are. Every Markdown file a Skill ships that is neither its `SKILL.md` nor its `help.md` is one of these, which is how the suite finds them: it discovers them rather than being told which they are.
- **Every pointer resolves.** `$HERE/<path>` is resolved from the directory holding `SKILL.md` and a Markdown link from the file the link sits in; both are followed by the suite, in every Markdown file a Skill ships.

## `help.md`

The manpage ships beside its `SKILL.md` and is a file the Skill prints rather than prose it regenerates (ADR-0044). It is written for a reader deciding whether to enable the Skill, which is a reader who does not have it yet.

- **The sections.** `## Synopsis`, `## Description`, `## Options`, `## Notes`, `## Dependencies`, and `## See also` are required of every manpage in the collection — each Skill's own, the Manager's, and each of the Manager's per-verb pages under `help/`. Further sections are the Skill's own to add where it has something the standard set has no room for, so the set is a floor rather than a shape, and the suite holds all six present on every page it can find. It holds nothing else about them: a `## Description` of one word passes. What the check buys is presence, which is what a reader who does not have the Skill yet can count on meeting; whether a section was written for that reader is a review's judgement and no test's.
- **A manpage documents the arguments its Skill takes**, conventionally under `## Arguments`. That heading is a convention rather than a requirement, and nothing checks it: a heading naming the arguments more precisely makes the better page, which is why `/orchestrate` puts the arguments it takes under *Aiming the run* and `/ready-for-agent-check` puts its own under *Scope*.
- **`## Options` is present even where the Skill has no flags at all.** It says so in prose — *none, and none is missing* — because an absent section reads as a section nobody wrote, and a reader cannot tell an omission from a decision. It carries no record of its own, and neither do the two rules above it: all three are form rules with no rejected alternative worth preserving, and the one alternative here worth keeping — `## Arguments` required by its name — is the sentence above rather than a record.
- **The flags named in `argument-hint`, in `## Synopsis`, and in `## Options` are one identical set.** The Skill has no parser — the agent reading these files is the whole of the enforcement — so a flag advertised in one and missing from another is a grammar that disagrees with itself, which is the failure ADR-0059 was written against. `--help` is the route into the manpage rather than a flag on a form, and is named in none of the three.
- **The refusal is documented as well as performed.** The manpage says that a flag with no work to do is refused rather than ignored, so a reader who has not yet run the Skill knows the strictness is deliberate.

## The README

A Skill gets a `### <name>` section under the README's `## Usage` heading, describing it to somebody deciding whether they want it. The suite fails when the Catalog names a Skill the README has no section for, and when a section names a Skill the Catalog does not.

The paragraph closing that part — which Skills need which binaries and which Capabilities — is prose, and nothing compares it against the dependency lists. Update it by hand when a Skill's requirements change, and expect no check to catch you if you do not.

## Before opening the pull request

Regenerate the Catalog when any file under `skills/<category>/<skill>/` changed, and run the four checks. Both are in [`CONTRIBUTING.md`](../../CONTRIBUTING.md), together with how to compare a Skill against the specification's own reference validator.
