---
name: unslop
description: Apply this collection's anti-slop pass to one supplied text and nothing else — false contrasts, empty openings, importance inflation, vague attribution, synonym cycling, robotic rhythm, and generic conclusions — repairing what it finds through a bounded budget of fresh correction subagents and reporting whatever is left. It selects no genre, no technique, and no editorial contract, and it runs no mechanical pass.
disable-model-invocation: true
argument-hint: '[--language=<language>] [--max=<n>] [--output=<response|path>] [<text>|<path>|<url>] | [--language=<language>] [--max=<n>] --in-place[=on|off] <path> [-- <instruction>]'
compatibility: Requires uv and a harness that can run subagents
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: "subagents"
---

# unslop

Read one Text Artifact against the shared anti-slop catalogue, repair what that pass found within the budget the invocation allows, say what is left, and stop there. This is one lens applied on its own, to a text that is otherwise finished: nothing here selects a genre, a technique, or an editorial contract, and nothing here proofreads afterwards.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md.

`$LIBRARY` is `library/` under the Manager directory that contains the checker. If it is absent, tell the user to run `/kntnt update`, then stop.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

Two forms, each carrying exactly one Text Artifact:

- `/unslop [--language=<language>] [--max=<n>] [--output=<response|path>] [<text>|<path>|<url>]`
- `/unslop [--language=<language>] [--max=<n>] --in-place[=on|off] <path>`

The operand is the Text Artifact: inline text, one local path, or one URL. Where the invocation carries no operand, it is the single text the current turn identifies.

`--language=<language>` names the language or locale whose anti-slop guidance applies. Any spelling the Collection's resolver reaches is accepted — a canonical code (`sv`, `en_GB`), a case or separator variant of one (`en-GB`, `EN_GB`), a curated alias (`BrE`, `brittisk engelska`), or an ordinary description of a language in any language.

`--max=<n>` is the Correction Budget: the greatest number of corrections this pass may delegate. It takes any non-negative integer and defaults to `1`, so an ordinary run includes one correction and one opportunity to verify it. `0` reviews without correcting — the findings come back for the reader to act on — and a higher value bounds a longer loop explicitly. It is a ceiling and never a quota: a run with nothing left to correct stops with the rest of it unspent.

`--output=<response|path>` names the Output Target. `response` is the default and the value `response` states it explicitly; anything else is one filesystem path.

`--in-place[=<value>]` selects In-place Editing. It accepts `yes`, `on`, and `true` against `no`, `off`, and `false`; bare `--in-place` means `on`, `--in-place=off` has the same effect as omitting the option, and the default is `off`.

Invalid forms, each refused the same way:

- A `--`-prefixed token that is not one of the four options, or one of them written without `=` and a value, `--in-place` excepted.
- The same option given twice, or given an empty value.
- `--in-place` with a value outside the vocabulary above.
- `--language` reaching no installed Language Resource, or more than one.
- `--max` with a value that is not a non-negative integer — a negative number, a fraction, or something that is not a number at all.
- `--output` and `--in-place=on` in one invocation, which name two destinations for one text.
- More than one Text Artifact — several paths, a glob reaching more than one file, or a directory of texts.
- An out-of-order form: the Text Artifact written before a flag rather than after every flag.

Name in one line what was wrong, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim, and point at `/unslop --help` for the page in full. Then read nothing, write nothing, and stop. A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing.

## Resolution

One editorial parameter is resolved here, the language, and it takes the first of these that answers:

1. The Formal Invocation.
2. A recognized Kntnt map in the Text Artifact's leading YAML frontmatter — the reserved `kntnt` key and its `language` value, and nothing else out of it. A `language`, `lang`, `genre`, or `technique` key at the top level of the document's own frontmatter belongs to that document, whatever it is named and whatever it holds; frontmatter carrying no `kntnt` map carries no configuration of this collection's.
3. The current Contextual Instruction.
4. Applicable Conversation Context.
5. Inference from the Text Artifact itself.
6. The language of the supplied text, which is what inference reads and what the default already is.

A value found at one level suppresses the levels below it. A language is settled rather than guessed: where the artifact is materially ambiguous or mixed, with no dominant language or alternation inside paragraphs, name the candidates and ask before anything is read against the catalogue.

No Kntnt map is created or synchronized. A map that exists supplies the language and is otherwise left exactly where it is, an artifact carrying none has none added to it, and the rest of the frontmatter comes through as it arrived — this Skill settles one of the three values such a map records, so writing one would claim a configuration it never resolved.

A recognized Kntnt map whose `language` no installed resource answers to, where `--language` supplied no value, is reported as unusable artifact metadata and stops the run. It is never quietly read as the nearest usable value, so a spelling such as `en_UK` never becomes `en_GB` on its own.

## Steps

1. Parse the arguments by the rules above and settle the single Text Artifact. An invalid form takes the refusal those rules describe. Done when one Text Artifact and a valid set of options are in hand, or you have stopped.
2. Settle the destination before anything is read against the catalogue, following `$LIBRARY/references/delivery.md`. Make every refusal that contract names by reading alone — In-place Editing together with a separate Output Target, an output path equal to the input path, In-place Editing against inline text or a URL or a source that is not a writable local file, and a destination whose parent directory does not exist — so that a refusal has nothing written behind it. Done when the destination is settled, or you have stopped.
3. Read the Text Artifact's leading YAML frontmatter where it has any, and look in it for one top-level `kntnt` map. Read `language` out of that map and nothing else out of it, and read nothing outside it as configuration. Done when the artifact's recognized language value is known to be present, absent, or unusable.
4. Resolve the language by `## Resolution`, and verify the selector with `uv run "$LIBRARY/scripts/languages.py" resolve --scope=anti-slop "<selector>"`. Exit 0: take the reported `code` as the resolved language and the returned scope as this run's language-specific guidance. A non-zero exit says which of the ways the selector failed and takes the refusal in `## Arguments`; an unlisted description of a language is interpreted first, then proposed as one installed candidate from `uv run "$LIBRARY/scripts/languages.py" list` and verified through that same `resolve` command. Report unusable recognized metadata as `## Resolution` describes, and ask rather than guess at a mixed language. Nothing has been written yet, so asking costs nothing to undo. Done when the language is settled and its scope is in hand, or you have asked or refused.
5. Load `$LIBRARY/references/editorial/anti-slop.md`, and take it together with the scope step 4 already returned as the whole of what this pass is read against. Load nothing else: no base contract, no genre, no technique, and none of the other scopes a Language Resource carries. The wider editorial guidance belongs to the Skill that applies the whole contract, and rules held here are rules this pass would end up applying to a text nobody asked it to review. Done when those two are loaded and nothing else has been.
6. Read the Text Artifact against them and record what you find as findings: where in the text, which pattern, and what the reader loses. The findings are anti-slop findings and nothing else — false contrasts, empty openings, importance inflation, vague attribution, synonym cycling, robotic rhythm, and generic conclusions, each applied by what it does in the resolved language rather than by the English words the catalogue writes it with. A sentence that is merely unusual, a fact you would have put differently, a structure you would have chosen against: none of these is a finding here, and a text whose only fault is one of them is clean. Judge only what is in front of you. This Skill never compares the Text Artifact with source material, never asks for material it was not given, and never remarks that source verification was unavailable — Source Fidelity is the contract of the Skill that wrote the text, and a caveat about material nobody supplied is noise in every run that was not one. Done when the pass is complete.
7. Spend the Correction Budget, up to it and never towards it. While findings remain from the most recent pass and budget remains, take one round:
   - Delegate the correction to a subagent started fresh for this round, from [`correction.md`](references/correction.md) filled in as that brief says. Fresh means it carries no history: not what an earlier round found, not what an earlier correction attempted, and not your own reading of the text, so the framing of the round before cannot bias this repair. It receives the complete current Text Artifact and the complete findings of the most recent pass — the text as it now stands and every finding as it was recorded, never a summary and never a stale draft — the language resolved in step 4, and the requirement to leave alone everything the findings do not concern.
   - Decrement the budget once per correction, whatever that correction came back with. A round that repaired nothing has still spent what it spent.
   - Take the returned text as the current Text Artifact and read it again, from the top, exactly as step 6 reads and against the two things loaded in step 5. A correction is verified by being reviewed again and never accepted on the report of whoever made it: an agent reporting on its own work is the one reader who cannot check it. The findings of this pass, and not the subagent's account of what it fixed, are the findings from here on.

   The loop stops at the first of three conditions, and each ends step 7. It stops when no findings remain, leaving the rest of the budget unspent — a text the pass is already clean against is not corrected again to use up a number. It stops when a correction makes no relevant progress, which is a round whose re-reading leaves the findings it was given standing with nothing they named changed: the next round would be the same round, so stop and carry those findings forward, saying which of them are unresolved. And it stops when the budget is spent with findings left, which carries them forward the same way for a person to finish. Done when one of the three has stopped the loop, or the budget was `0` and there was nothing to spend.
8. Run no mechanical pass and correct nothing outside the lens. This run was asked for one pass and delivers one pass: spelling, punctuation, grammar, and the locale's own mechanics are somebody else's gesture, and so is everything the editorial contract holds that this Skill never loaded. Material the findings do not concern comes through as it arrived, the frontmatter among it. Done when the diff you are about to deliver is anti-slop repair throughout.
9. Deliver by `$LIBRARY/references/delivery.md`. Where findings remain — those step 7 carried forward, whichever of its three conditions stopped the loop — deliver the Text Artifact to its Output Target and report the findings separately, saying which are unresolved; that holds where nothing in the text changed too, since the findings are the point of that run, and a file-targeted or in-place run leaves the findings in the response beside the destination it wrote. Where no findings remain, deliver the Text Artifact alone, and where such a clean run was aimed at the response or at its own source and changed nothing, write nothing and return only the short no-change status. Keep the pass to its findings: the reasoning behind them, the passages you considered and dismissed, and any correspondence with a correction subagent stay out of the output. Done when the Text Artifact has been delivered, or the no-change status has been reported.
