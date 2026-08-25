---
name: redline
description: Review one supplied text against this collection's editorial contract — its genre, its optional technique, its language, and the shared anti-slop catalogue — report what the review found, and finish with exactly one mechanical pass.
disable-model-invocation: true
argument-hint: '[--genre=<genre>] [--technique=<technique>] [--language=<language>] [--max=<n>] [--output=<response|path>] [<text>|<path>|<url>] | [--genre=<genre>] [--technique=<technique>] [--language=<language>] [--max=<n>] --in-place[=on|off] <path> [-- <instruction>]'
compatibility: Requires uv, proofread, and a harness that can run subagents
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: "proofread"
  kntnt.externals: ""
  kntnt.capabilities: "subagents"
---

# redline

Read one Text Artifact against the editorial contract, say what the review found, and close with one mechanical pass. The artifact may come from anywhere: this collection wrote it, a person wrote it, or something else produced it entirely.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md.

`$LIBRARY` is `library/` under the Manager directory that contains the checker. If it is absent, tell the user to run `/kntnt update`, then stop.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

Two forms, each carrying exactly one Text Artifact:

- `/redline [--genre=<genre>] [--technique=<technique>] [--language=<language>] [--max=<n>] [--output=<response|path>] [<text>|<path>|<url>]`
- `/redline [--genre=<genre>] [--technique=<technique>] [--language=<language>] [--max=<n>] --in-place[=on|off] <path>`

The operand is the Text Artifact: inline text, one local path, or one URL. Where the invocation carries no operand, it is the single text the current turn identifies.

`--genre=<genre>` names a resource under `$LIBRARY/references/editorial/genres/`, by its filename without the extension.

`--technique=<technique>` names a resource under `$LIBRARY/references/editorial/techniques/`, the same way.

`--language=<language>` names the language or locale whose editorial guidance applies. Any spelling the Collection's resolver reaches is accepted — a canonical code (`sv`, `en_GB`), a case or separator variant of one (`en-GB`, `EN_GB`), a curated alias (`BrE`, `brittisk engelska`), or an ordinary description of a language in any language.

`--max=<n>` is the Correction Budget: the number of substantive corrections the review may delegate. It takes a non-negative integer. **This release accepts `0` alone, and `0` is the default.** The budget is what bounds a correction loop this Skill does not yet carry, so a review runs, its findings are reported for the reader to act on, and the closing mechanical pass is still performed. A positive value is refused rather than silently treated as zero.

`--output=<response|path>` names the Output Target. `response` is the default and the value `response` states it explicitly; anything else is one filesystem path.

`--in-place[=<value>]` selects In-place Editing. It accepts `yes`, `on`, and `true` against `no`, `off`, and `false`; bare `--in-place` means `on`, `--in-place=off` has the same effect as omitting the option, and the default is `off`.

Invalid forms, each refused the same way:

- A `--`-prefixed token that is not one of the six options, or one of them written without `=` and a value, `--in-place` excepted.
- The same option given twice, or given an empty value.
- `--in-place` with a value outside the vocabulary above.
- `--genre` or `--technique` naming a resource that is not installed.
- `--language` reaching no installed Language Resource, or more than one.
- `--max` with a value that is not a non-negative integer, or with a value this release does not accept.
- `--output` and `--in-place=on` in one invocation, which name two destinations for one text.
- More than one Text Artifact — several paths, a glob reaching more than one file, or a directory of texts.
- An out-of-order form: the Text Artifact written before a flag rather than after every flag.

Name in one line what was wrong, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim, and point at `/redline --help` for the page in full. Then review nothing, write nothing, and stop. A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing.

## Resolution

Genre, technique, and language are each resolved on their own, in this order of precedence:

1. The Formal Invocation.
2. A recognized Kntnt map in the Text Artifact's leading YAML frontmatter — the reserved `kntnt` key and its `genre`, `technique`, and `language` values, and nothing else. A `language`, `lang`, `genre`, or `technique` key at the top level of the document's own frontmatter belongs to that document, whatever it is named and whatever it holds; frontmatter carrying no `kntnt` map carries no configuration of this collection's.
3. The current Contextual Instruction.
4. Applicable Conversation Context.
5. Inference from the Text Artifact itself.
6. The parameter's default: `general` for genre, no technique, and the language of the Text Artifact.

A value found at one level suppresses the levels below it for that parameter alone. An explicit genre beside a language read out of the map and a technique taken from an instruction is an ordinary invocation, not a conflict.

Two things are never inferred. A technique applies because it was selected — by the invocation, the map, or an instruction that names one — and never because the text happens to fall into its shape. A language is settled rather than guessed: where the artifact is materially ambiguous or mixed, with no dominant language or alternation inside paragraphs, name the candidates and ask before anything is reviewed.

Handoff Metadata is never required and never created. A Text Artifact carrying no `kntnt` map is reviewed exactly like one that carries a complete one, and no map is added to it. Where a recognized map exists, it is used as defaults here and synchronized to the resolved configuration in step 8.

A recognized Kntnt map whose value cannot be used — a language nothing installs, a genre or technique that is not there — is reported as unusable artifact metadata and stops the run, unless the Formal Invocation already settled that parameter. It is never quietly read as the nearest usable value, so a spelling such as `en_UK` never becomes `en_GB` on its own.

## Steps

1. Parse the arguments by the rules above and settle the single Text Artifact. An invalid form takes the refusal those rules describe. Done when one Text Artifact and a valid set of options are in hand, or you have stopped.
2. Settle the destination before anything is reviewed, following `$LIBRARY/references/delivery.md`. Make every refusal that contract names by reading alone — In-place Editing together with a separate Output Target, an output path equal to the input path, In-place Editing against inline text or a URL or a source that is not a writable local file, and a destination whose parent directory does not exist — so that a refusal has nothing written behind it. Done when the destination is settled, or you have stopped.
3. Read the Text Artifact's leading YAML frontmatter where it has any, and look in it for one top-level `kntnt` map. Read `genre`, `technique`, and `language` out of that map and nothing else out of it, and read nothing outside it as configuration. Done when the artifact's recognized values are known to be present, absent, or unusable.
4. Resolve genre, technique, and language by `## Resolution`. A genre or technique is verified against the resources actually installed in the two directories named in `## Arguments`. A language selector is verified by `uv run "$LIBRARY/scripts/languages.py" resolve --scope=composition --scope=review --scope=anti-slop "<selector>"`, whose non-zero exit says which of the ways it failed and takes the refusal in `## Arguments`; an unlisted description of a language is interpreted first, then proposed as one installed candidate and verified through that same command. Report unusable recognized metadata as `## Resolution` describes, and ask rather than guess at a mixed language. Nothing has been written yet, so asking costs nothing to undo. Done when all three are settled, or you have asked or refused.
5. Load what the review is read against, and nothing besides it: `$LIBRARY/references/editorial/base.md` and `$LIBRARY/references/editorial/base.review.md`; the selected genre from `$LIBRARY/references/editorial/genres/` and the `.review.md` file beside it where one exists; the resolved technique from `$LIBRARY/references/editorial/techniques/` and its `.review.md` the same way; `$LIBRARY/references/editorial/anti-slop.md`; and the three language scopes the resolver already returned in step 4. A review extension that is not there is not a defect — a base half on its own is a complete resource. Load no mechanics guidance: the mechanical pass in step 9 resolves its own. Done when those are loaded and nothing else has been.
6. Review the Text Artifact against everything loaded in step 5, and record what you find as findings: where in the text, which requirement, and what the reader loses. Judge only what is in front of you. This Skill never compares the Text Artifact with source material, never asks for material it was not given, and never remarks that source verification was unavailable — Source Fidelity is the contract of the Skill that wrote the text, and a caveat about material nobody supplied is noise in every run that was not one. A contradiction, an unsupported claim, or an editorial defect visible inside the artifact itself is an ordinary finding. Done when the review is complete.
7. Spend the Correction Budget. It is `0` in this release, so no substantive correction is delegated and every finding from step 6 is carried forward to delivery for the reader to act on. Done when the budget is spent or, as here, there was none to spend.
8. Where step 3 found a recognized `kntnt` map, synchronize its `genre`, `technique`, and `language` to the values resolved in step 4, writing `none` where no technique was resolved, and change nothing else in the frontmatter. Where the artifact carries no such map, add none. Done when the artifact's metadata, if it has any of ours, says what this run resolved.
9. Follow `$HERE/../proofread/SKILL.md` exactly once, with the Formal Invocation `--language=<resolved>` and the current complete Text Artifact as its operand. If the outer Contextual Instruction contains guidance relevant to mechanical correction, append only that guidance after an explicit `--`; otherwise pass no Contextual Instruction. Never forward the genre, the technique, the Correction Budget, or unrelated outer context. Take its result as the Text Artifact from here on; a no-change status means the text you already hold is final. Done when the mechanical pass has run once.
10. Change nothing substantive after step 9. The mechanical pass is last so that its corrections cannot be undone by later editing, and a sentence improved here would put mechanical errors back into a text that was just cleaned of them. Done when nothing has been touched since the pass.
11. Deliver by `$LIBRARY/references/delivery.md`. Where findings remain, deliver the Text Artifact to its Output Target and report the findings separately — including where nothing in the text changed, since the findings are the point of that run; a file-targeted or in-place run leaves the findings in the response beside the destination it wrote. Where no findings remain, deliver the Text Artifact alone, and where such a clean run was aimed at the response or at its own source and changed nothing, write nothing and return only the short no-change status. Keep the review to its findings: the reasoning behind them, the passages you considered and dismissed, and any correspondence with a nested Skill stay out of the output. Done when the Text Artifact has been delivered, or the no-change status has been reported.
