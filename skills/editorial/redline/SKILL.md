---
name: redline
description: Review one supplied text against this collection's editorial contract — its genre, its optional technique, its language, and the shared anti-slop catalogue — repair what the review found through a bounded budget of fresh correction subagents, report whatever is left unresolved, and finish with exactly one mechanical pass.
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

Read one Text Artifact against the editorial contract, repair what the review found within the budget the invocation allows, say what is left, and close with one mechanical pass. The artifact may come from anywhere: this collection wrote it, a person wrote it, or something else produced it entirely.

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

`--max=<n>` is the Correction Budget: the greatest number of substantive corrections the review may delegate. It takes any non-negative integer and defaults to `1`, so an ordinary review includes one correction and one opportunity to verify it. `0` reviews without correcting — the findings come back for the reader to act on, and the closing mechanical pass is still performed — and a higher value bounds a longer loop explicitly. It is a ceiling and never a quota: a run with nothing left to correct stops with the rest of it unspent.

`--output=<response|path>` names the Output Target. `response` is the default and the value `response` states it explicitly; anything else is one filesystem path.

`--in-place[=<value>]` selects In-place Editing. It accepts `yes`, `on`, and `true` against `no`, `off`, and `false`; bare `--in-place` means `on`, `--in-place=off` has the same effect as omitting the option, and the default is `off`.

Invalid forms, each refused the same way:

- A `--`-prefixed token that is not one of the six options, or one of them written without `=` and a value, `--in-place` excepted.
- The same option given twice, or given an empty value.
- `--in-place` with a value outside the vocabulary above.
- `--genre` or `--technique` naming a resource that is not installed.
- `--language` reaching no installed Language Resource, or more than one.
- `--max` with a value that is not a non-negative integer — a negative number, a fraction, or something that is not a number at all.
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

A value found at one level suppresses the levels below it for that parameter alone. An explicit genre beside a language read out of the map and a technique taken from an instruction is an ordinary invocation, not a conflict. Suppression is that precedence working rather than an error: a Contextual Instruction every higher level has already settled leaves nothing for it to settle, and the run continues rather than refusing it as unaddressable guidance. Where saying so is useful, the delivery names the suppressed instruction beside the resolved configuration.

Two things are never inferred. A technique applies because it was selected — by the invocation, the map, or an instruction that names one — and never because the text happens to fall into its shape. A language is settled rather than guessed: where the artifact is materially ambiguous or mixed, with no dominant language or alternation inside paragraphs, name the candidates and ask before anything is reviewed.

A genre inferred rather than named is inferred against what is installed. The genre directory is the list of installed values, and a run inferring one may read a single thing besides that listing: the opening of each installed genre resource — its `# <Name>` heading and the paragraph under it, which every resource carries so that a reader choosing between them has something to read without loading the rest. Read that far and no further. What a genre asks for is not evidence about whether that genre applies, so a resource read past its opening has been loaded rather than considered — and the loading step below is unchanged by any of this: it loads the genre inference settled on, and no other. Where no installed genre fits what is in front of you better than the default does, the default at the foot of the precedence stands.

Handoff Metadata is never required and never created. A Text Artifact carrying no `kntnt` map is reviewed exactly like one that carries a complete one, and no map is added to it. Where a recognized map exists, it is used as defaults here and synchronized to the resolved configuration in step 8.

A recognized Kntnt map whose value cannot be used — a language nothing installs, a genre or technique that is not there — is reported as unusable artifact metadata and stops the run, unless the Formal Invocation already settled that parameter. It is never quietly read as the nearest usable value, so a spelling such as `en_UK` never becomes `en_GB` on its own.

## Steps

1. Parse the arguments by the rules above and settle the single Text Artifact. An invalid form takes the refusal those rules describe. Done when one Text Artifact and a valid set of options are in hand, or you have stopped.
2. Settle the destination before anything is reviewed, following `$LIBRARY/references/delivery.md`. Make every refusal that contract names by reading alone — In-place Editing together with a separate Output Target, an output path equal to the input path, In-place Editing against inline text or a URL or a source that is not a writable local file, and a destination whose parent directory does not exist — so that a refusal has nothing written behind it. Done when the destination is settled, or you have stopped.
3. Read the Text Artifact's leading YAML frontmatter where it has any, and look in it for one top-level `kntnt` map. Read `genre`, `technique`, and `language` out of that map and nothing else out of it, and read nothing outside it as configuration. Done when the artifact's recognized values are known to be present, absent, or unusable.
4. Resolve genre, technique, and language by `## Resolution`. A genre or technique is verified against the resources actually installed in the two directories named in `## Arguments`. Where the genre has to be inferred rather than verified, `## Resolution` says what may be read to infer it. A language selector is verified by `uv run "$LIBRARY/scripts/languages.py" resolve --scope=composition --scope=review --scope=anti-slop "<selector>"`, whose non-zero exit says which of the ways it failed and takes the refusal in `## Arguments`; an unlisted description of a language is interpreted first, then proposed as one installed candidate and verified through that same command. Report unusable recognized metadata as `## Resolution` describes, and ask rather than guess at a mixed language. Nothing has been written yet, so asking costs nothing to undo. Done when all three are settled, or you have asked or refused.
5. Load what the review is read against, and nothing besides it: `$LIBRARY/references/editorial/base.md` and `$LIBRARY/references/editorial/base.review.md`; the selected genre from `$LIBRARY/references/editorial/genres/` and the `.review.md` file beside it where one exists; the resolved technique from `$LIBRARY/references/editorial/techniques/` and its `.review.md` the same way; `$LIBRARY/references/editorial/anti-slop.md`; and the three language scopes the resolver already returned in step 4. A review extension that is not there is not a defect — a base half on its own is a complete resource. Load no mechanics guidance: the mechanical pass in step 9 resolves its own. Done when those are loaded and nothing else has been.
6. Review the Text Artifact against everything loaded in step 5, and record what you find as findings: where in the text, which requirement, and what the reader loses. Judge only what is in front of you. This Skill never compares the Text Artifact with source material, never asks for material it was not given, and never remarks that source verification was unavailable — Source Fidelity is the contract of the Skill that wrote the text, and a caveat about material nobody supplied is noise in every run that was not one. A contradiction, an unsupported claim, or an editorial defect visible inside the artifact itself is an ordinary finding. Done when the review is complete.
7. Spend the Correction Budget, up to it and never towards it. While findings remain from the most recent review and budget remains, take one round:
   - Delegate the correction to a subagent started fresh for this round, from [`correction.md`](references/correction.md), filled in and delivered as that brief says. Fresh means it carries no history: not what an earlier round found, not what an earlier correction attempted, and not your own reading of the text, so the framing of the round before cannot bias this repair. It receives the complete current Text Artifact and the complete findings of the most recent review — the text as it now stands and every finding as it was recorded, never a summary and never a stale draft — the genre, technique, and language resolved in step 4, and the requirement to leave alone everything the findings do not concern.
   - Decrement the budget once per correction, whatever that correction came back with. A round that repaired nothing has still spent what it spent.
   - Take the returned text as the current Text Artifact and review it again, from the top, exactly as step 6 reviews and against everything loaded in step 5. A correction is verified by review and never accepted on the report of whoever made it: an agent reporting on its own work is the one reader who cannot check it. The findings of this review, and not the subagent's account of what it fixed, are the findings from here on.

   The loop stops at the first of four conditions, and each ends step 7. It stops when no findings remain, leaving the rest of the budget unspent — a text that is already clean is not corrected again to use up a number. It stops when a correction makes no relevant progress, which is a round whose re-review leaves the findings it was given standing with nothing they named changed: the next round would be the same round, so stop and carry those findings forward, saying which of them are unresolved. It stops when a re-review raises a finding an earlier round's own repair created — a defect the text did not have when it arrived and one of your rounds put there, the clearest case being a finding about material a round removed. You hold every state the text has passed through and are the only party that does: the subagent is fresh by design and each review reads the text in front of it, so a loop that has begun to answer for its own work is visible here and nowhere else. Another round would repair what the round before it did, so stop, carry the outstanding findings forward the same way, and name the repair the new finding followed from, which is the thing a person has to settle. And it stops when the budget is spent with findings left, which carries them forward the same way for a person to finish. Done when one of the four has stopped the loop, or the budget was `0` and there was nothing to spend.
8. Where step 3 found a recognized `kntnt` map, synchronize its `genre`, `technique`, and `language` to the values resolved in step 4, writing `none` where no technique was resolved, and change nothing else in the frontmatter. Where the artifact carries no such map, add none. Done when the artifact's metadata, if it has any of ours, says what this run resolved.
9. Follow `$HERE/../proofread/SKILL.md` exactly once, with the Formal Invocation `--language=<resolved>` and the current complete Text Artifact as its operand. If the outer Contextual Instruction contains guidance relevant to mechanical correction, append only that guidance after an explicit `--`; otherwise pass no Contextual Instruction. Never forward the genre, the technique, the Correction Budget, or unrelated outer context. Take its result as the Text Artifact from here on; a no-change status means the text you already hold is final. Done when the mechanical pass has run once.
10. Change nothing substantive after step 9. The mechanical pass is last so that its corrections cannot be undone by later editing, and a sentence improved here would put mechanical errors back into a text that was just cleaned of them. Done when nothing has been touched since the pass.
11. Deliver by `$LIBRARY/references/delivery.md`. Where findings remain — those step 7 carried forward, whichever of its conditions stopped the loop — deliver the Text Artifact to its Output Target and report the findings separately, saying which are unresolved; that holds where nothing in the text changed too, since the findings are the point of that run, and a file-targeted or in-place run leaves the findings in the response beside the destination it wrote. Where no findings remain, deliver the Text Artifact alone, and where such a clean run was aimed at the response or at its own source and changed nothing, write nothing and return only the short no-change status. Keep the review to its findings: the reasoning behind them, the passages you considered and dismissed, and any correspondence with a correction subagent or a nested Skill stay out of the output. Done when the Text Artifact has been delivered, or the no-change status has been reported.
