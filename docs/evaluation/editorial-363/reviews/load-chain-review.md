# Load-chain review of the #363 wording

**What this review read, and where it now is.** This is an independent reading of the revised wording of #363 against the chain its six surfaces sit in. It was written while that wording was in the working tree, so every *now* and every present tense below is about that tree and not about the branch. The branch does not ship it: the six surfaces were returned to the baseline in `36e2b599`, so the diff this review read is empty here and is recovered as `git diff 8a37e57e 19862dc2 -- skills tests`. `19862dc2` is the commit that holds the wording, and its six surfaces hash to the staged `install-revised` file for file. The four tests §5 discusses were removed with the wording and are in that commit too.

The reading itself is unchanged, and deliberately so. It was made without the measurement in front of it, its verdict is one of the three independent grounds [`../results.md`](../results.md) gives for not shipping, and rewriting its findings after the fact would destroy the only thing that makes it worth keeping.

**Five word counts in §4 and §5 are understated, and are restated here rather than edited in place.** Recounted with `wc -w` against `19862dc2`: the addition to Redline's step 6 is 161 words net, not the 123 §4 gives, and it is the whole of that file's change; the addition to `source-check.md` is 76 words net, not 56, and it is the whole of the task blockquote's change; and the three pinned constants §5 measures are 161, 148 and 88 words rather than 121, 118 and 66. Every one of those findings argues that the addition or the pin is larger than the behaviour it buys, so the larger figures do not weaken them. They are corrected because a number in an evidence file has to be recomputable from the tree the file names.

---

## The reading

An independent reading of `git diff 8a37e57e 19862dc2 -- skills/`, against the chain those six surfaces sit in. I read both `SKILL.md` bodies whole, both `help.md` pages whole, `redline/references/correction.md`, `write/references/quotations.md` and `source-check.md` whole, `editorial/base.md`, `base.review.md`, `README.md`, `headlines.md`, `article-anatomy.md`, `anti-slop.md`, `mechanics.md` (heading level), all ten genre halves, `languages/sv.md`, `en_GB.md`, `en_US.md`, `languages/README.md`, `docs/adr/0212`, and `docs/rules/docs.md`, `skills.md` and `general.md`. I read nothing under any `docs/evaluation/editorial-*` directory, and I did not run the suite. Nothing below rests on the measurement; it rests on the text.

---

## 1. Technical

**A contradiction the chain now carries: a source-blind review can be driven to falsify a quotation.** Step 6 now tells the review to make a finding inside quoted speech and to name it by the word the reader has to supply. Step 7 hands that finding to a correction subagent, whose brief has no quotation rule beyond *altering a quotation's meaning, stance, certainty or distinctive wording*, so supplying a missing word inside quotation marks reads as permitted. But `languages/sv.md` line 112 says:

> Wording inside *”…”* is the speaker's own, and the text vouches for it word for word. … Repaired wording set inside quotation marks is therefore false about the source rather than a typographic slip.

That sentence is in sv.md's **Mechanics** scope. Redline's step 5 says *Load no mechanics guidance: the mechanical pass in step 9 resolves its own*, and step 4 resolves `--scope=composition --scope=review --scope=anti-slop`; `correction.md` resolves the same three. So neither the reviewer nor the repairer can see the rule they would be breaking. What they *do* see is sv.md's composition scope pointing at a promise they are not allowed to load — *What each of the two marks promises a reader, and what that makes each of them a claim about, is settled in Mechanics* — and sv.md's review scope telling them the opposite of a licence: *without the source, leave that provenance claim unjudged*. Before this change the review had no general instruction to find defects inside quoted matter, so the gap was theoretical. It is not any more. **Must-fix:** step 6 (and, if the round is to be spent well, `correction.md`) has to say that a finding inside quoted matter is reported rather than repaired wherever the text's own mark vouches for the wording, and that the mark itself is not changed to make a repair lawful.

**A surface left behind: `redline/references/correction.md`.** The repository's own precedent for a rule that has to survive a correction round is the code-sample rule, and `docs/rules/skills.md` states it this way:

> Every Skill that runs an editorial, anti-slop or mechanical pass over a finished text states the rule in its pass step in the same words as its peers, **every correction brief's preservation clause names code beside the quotations and formatting it already names**, and every one of those Skills' manpages tells the reader that a code sample is quoted material.

This change updates the pass step and the manpage and leaves the correction brief untouched. The brief's own instruction — *Where a finding names something you cannot repair without inventing a fact, changing what the text claims, or altering a quotation's meaning, stance, certainty or distinctive wording, leave that passage alone and say so* — is the sentence a repairer meeting a quotation finding will reach for, because it is the only one addressed to the case. The likely outcome is a round spent returning the text unchanged with a note, which step 7 then reads as *a correction makes no relevant progress* and stops the loop on. The finding is correctly carried forward, so nothing breaks; a budget is burned to learn what the brief already knew. **Should-fix.**

**A duplication: the same test is now stated in two places for one genre.** `genres/case-study.review.md` says *a referent the reader has to reconstruct is a visible problem, and a figure the language uses itself is not*; step 6 says the same thing for every genre, in different words. `docs/rules/docs.md`: *A rule states itself once*. `editorial/README.md`, on review extensions: *it restates no base rule in other words, because a requirement and its diagnostic drift apart the moment both claim to say what is required*. The two wordings also put the word *reconstruct* in opposite roles — case-study makes having to reconstruct the defect, while step 6 says *That the meaning can be worked out from the surrounding text does not answer it*. They are reconcilable on a careful reading; they are one rule with two vocabularies, loaded together, in the one genre where quotations are most of the text. **See §2 for where I think it belongs.**

**Term drift across the five surfaces.** The thing under test is called *reported speech* (redline `SKILL.md`), *a quotation* (redline `help.md`), *the finished rendering* (`quotations.md`), *quoted speech* (`case-study.review.md`) and *a concrete obstruction* (`source-check.md`). Four of those are defensible under ADR-0212's own reasoning — each Skill states the test in the terms of the act it performs — but the first two are one Skill's two surfaces, and they are not the same set: *reported speech* takes in indirect speech (*she said the change had taken about a year*), which no quotation marks enclose. The page therefore under-promises rather than over-promises, which is the harmless direction, but a reader comparing them cannot tell whether that was meant. **Optional**, fixed by writing *reported speech* on the page too.

**Nothing refers to anything the change removed.** The one candidate was the retired `redline/references/quotation-review.md`; the only mention left in the tree is inside ADR-0212's *What was set aside*, which is where it belongs. No test pinned the old case-study sentence, and `docs/adr/README.md` carries no index to update.

**No `help.md` promises behaviour its `SKILL.md` does not describe.** Redline's page (*A figure that language uses is taken on one pass and left alone; a construction the reader has to stop in and supply a word for is a finding*) is step 6 compressed correctly. Write's page carries both halves of the change — the checker's reading order and the writer's read-back — and both are in the files they claim. Write's page inherits one problem from `quotations.md`; see §3.

---

## 2. Where the rule lives

Four of the six placements are right, and I would move the fifth.

- Redline's step 6 and `help.md`: correct. The source-blind reading of one text is Redline's act alone, and ADR-0212's argument for not putting it in `base.review.md` is sound — a formulation general enough to cover rendering, comparing and reviewing is how the old sentence came to under-fire and over-fire at once.
- Write's `quotations.md` and `source-check.md` and `help.md`: correct. Translation and comparison are Write's act alone, and `source-check.md` is a file only Write opens, which is what `docs/rules/skills.md` puts under a Skill's `references/`.
- `genres/case-study.review.md`: **wrong file now**. Before this change it was the only place the product said anything about quoted idiom to a review, so it was the right place by default. Step 6 has taken that job for every genre, and what is left in case-study is a genre-specific restatement of a genre-independent rule, on a shared surface, in a second vocabulary. The library README's test for what may sit in a genre resource — *it states only what the base contract does not: a rule repeated here is one rule made into two things to keep true* — decides it. **Should-fix: delete the idiom clause from `case-study.review.md`** and let the sentence return to what is genuinely genre-specific (*Read bridges beside quotations … Remove a redundant pre-echo while keeping the attribution and any distinct fact. Clarify only what the surrounding text settles; otherwise report it.*). If it is kept instead, see the must-fix in §3, which is about the words it was given.

Nothing in the change belongs in `base.md`, `base.review.md`, `web-craft.md`, `headlines.md` or a language resource, and nothing was put there. The one library file that arguably *should* move is not this change's doing: `genres/case-study.md` says *Preserve the supplied speech within the quotation policy* and the quotation policy is `write/references/quotations.md`, which Redline never loads and cannot. That dangling pointer predates the diff, but this change makes the review lean on it harder, so it is worth naming: **optional**, and the honest repair is to name the language's conventions alone there.

---

## 3. Editorial, read as the agent that receives it

**Redline's step 6, read with only what step 5 loaded.** The test is executable, and the gate that makes it so is the naming requirement: *a finding, named by the word the reader has to supply*. A reviewer that cannot name the word has found a preference, and the step says so twice. The three exemplars — a verb whose subject cannot perform it, a time or place adverbial whose event is missing, a reference the sentence never introduces — are diagnostic rather than a list to work through, which is the right shape. The over-fire guard is explicit and I do not read the step as a ban on ordinary figures: *An ellipsis, a metonymy or a shorthand this language uses itself is taken on one pass however odd its literal parse, and is left exactly as it stands* is about as flat a protection as prose can carry.

What the step does not say is what happens next. It makes quoted speech findable and says nothing about whether it is repairable, and the two things a reviewer holds when it gets there — step 7's ordinary delegation, and `correction.md`'s quotation clause — point in opposite directions. Added to the sv.md mark problem in §1, that is the one place in step 6 I would not ship as it stands.

**`case-study.review.md`, read by the same agent.** Here I think the change has introduced, narrowly, the thing it says it is not introducing. The old sentence read *a missing referent that makes the reader reconstruct the meaning is a visible problem, **not protected merely by quotation marks***. The new one reads:

> Quoted speech is read for idiom like the prose around it and is not protected by its quotation marks.

*Merely* was doing real work, and dropping it turns a narrow disclaimer into a general one. The reviewer holding that sentence has loaded no quotation policy at all — step 5 loads `base.md`, `base.review.md`, the genre pair, anti-slop, three language scopes, web-craft, article-anatomy and headlines, and not one of them says what may not be changed inside quoted speech. Read in that context, *not protected by its quotation marks*, beside *read for idiom like the prose around it*, is a licence to treat a customer's speech as ordinary prose to be brought up to the surrounding register — which `quotations.md` calls *the most tempting of these failures and the one a reader can least detect*, and which `report.review.md` guards against in its own corner (*A fragment inside quoted material is what somebody said and stays as it is*). Step 6's *preserving its meaning and distinctive voice* pulls the other way, but it is in a different file, and the genre half is the more specific instruction on the exact question. **Must-fix**, best fixed by §2's deletion, and otherwise by restoring the limiting word.

**`quotations.md`, read as the writer.** The new paragraph is the strongest writing in the change. The read-back requirement — *so has a repair of it they stop in again … because the shortest way out of one such figure is another* — is a real mechanism and it is the part nothing else in the chain supplies. One sentence in it is over-broad:

> A figure of the source — an ellipsis, a metonymy, a conventional shorthand — carries over only where the target language has one of its own to reach for; where it has none, say what the speaker said the way that language says it.

*A figure of the source* is not scoped to a figure of the source **language**. The examples are conventional and language-level, but the rule as written reaches a figure the speaker coined, and the remedy clause then tells the writer to replace it with plain target-language statement. Four hundred words below, the same file says *Where the speaker reached for an unusual word, an image, a piece of slang, or a phrasing that is theirs, it stays*. Which will a writer follow? The new sentence, because it is operational, it gives a test, and it is stated as a failure condition (*has failed however faithful its words are*), while the *distinctive wording* rule is stated as a preservation with no test behind it. `write/help.md` puts the collision two sentences apart on one page: *Meaning, stance, certainty, distinctive wording, and self-corrections are preserved* … *a figure of the source carries over only where that language has one of its own*. **Must-fix:** write *a figure the source language supplies* (or *a conventional figure of the source language*) on both surfaces, so the sentence cannot reach the speaker's own image. Redline's step 6 already has this right with *this language uses itself*; the fix is to make Write say what Redline says.

With that word fixed, I do not read either surface as a licence to rewrite quoted speech to taste: the boundary sections of `quotations.md` are intact, the additive ban is intact, and the new paragraph tests a rendering rather than licensing a rewrite.

**`source-check.md`, read as the fresh checker.** The addition is executable and well aimed — the definition of *a concrete obstruction* is exactly the clause the task had been asserting without a test behind it, and the exclusion (*a figure that language uses itself is not one, and neither is a preferred synonym*) keeps the over-fire direction closed.

Its ordering instruction, though, arrives too late to be obeyed. It says *read the quotation in the target language alone before setting it beside the source*. It is the penultimate topic of a single ~640-word task whose **second** sentence is *For every factual and attributed claim, record the draft passage beside the source passage it rests on, quoted in the source's own words and language*. A quotation is an attributed claim. By the time the checker reads the new clause it has already built the accounting the report is made of, with every quotation sitting beside its source. Two sentences pull against each other and the earlier one wins, because it governs the artefact the checker is producing. **Should-fix:** state the quotation read at the head of the task — one sentence saying that where quotations are translated, each rendering is read in the target language alone before any pairing begins — and leave the definition of an obstruction where it is.

---

## 4. Cost

**Redline step 6 (+123 words on the body's longest step).**

- *Ask of each what a reader of this language does at it, and settle that before you go on to anything else* — the test. Earns its place. The clause *and settle that before you go on to anything else* is already carried by *Then cover the surrounding prose* three sentences later; **I would cut it.**
- *they take it on one pass, or they stop at a word you can name* — the discriminator and the naming gate. Earns its place.
- *An ellipsis, a metonymy or a shorthand this language uses itself …* — the over-fire guard, and the half the old genre sentence lacked. Earns its place. *however odd its literal parse* is decoration; it survives a cut, but it is cheap and it does pre-empt a literal-minded reading, so I would leave it.
- *They stop where the sentence leaves them to supply …* — the three exemplars. Earns its place; nothing else in the chain says what a stop looks like.
- *That the meaning can be worked out from the surrounding text does not answer it.* — the crux. Nothing else says it, and ADR-0212 is right that this is the sentence that separates the two directions.
- *Ask the question in the language in front of you, about the passage in front of you, and never about a word you would rather see.* — the first half is already carried by *what a reader of this language does at it*; the second half is the naming gate stated from the other side. **Restates; I would cut it**, or keep only *never about a word you would rather see*.

Note also that `base.review.md` already protects *a working figure, contrast or ending* against the anti-slop pass. Step 6's guard is scoped to language idiom rather than anti-slop and so is not a duplicate, but it is adjacent, and a reader holding both is being told twice not to over-fire.

**`quotations.md` (+four sentences).** Sentences 1, 2 and 4 all buy something the file did not have: the reading order, the operational test with its naming gate, and the carry-over rule. In sentence 3, *A rendering they stop in has failed however faithful its words are* restates the paragraph above it (*idiomatic target-language speech, not source-language syntax*; *they do not require word-for-word translation*); the rest of that sentence — the repair read-back — is the most valuable addition in the whole change. **I would cut the first clause and keep the colon onwards.**

**`source-check.md` (+56 words).** The obstruction definition earns its place. But the checker is already handed `quotations.md` — the task file says *Include the resolved language, the Claims section from the loaded base contract and, where quotations occur, the loaded quotation guidance* — so it now receives one test twice, in two wordings. Since the task text is the whole of what a fresh subagent executes and the attachment is reference, I would keep the task's version and accept the overlap; naming it here because `docs/rules/docs.md` would otherwise call it a second thing to keep true. **Optional.**

**Both `help.md` pages.** Each buys observable behaviour a reader deciding whether to run the Skill cannot otherwise predict, which is what `docs/rules/skills.md` wants under `DESCRIPTION`. One asymmetry: Redline's page states both halves (a working figure is left alone; a stop is a finding); Write's page states only the restrictive half. A reader of Write's page is not told that a figure the *target* language uses is left alone. **Optional**, one clause.

**`case-study.review.md`.** Net zero words for a rule already stated in step 6 — see §2.

---

## 5. The tests

All four pin something that ought to be pinned: the discriminating rule is prose, the prose is the whole of what an agent executes, and prose pins are this suite's established idiom. Three problems.

**Each pins far more than the behaviour.** `READER_OF_THIS_LANGUAGE` is 121 words, `RENDERING_READ_IN_THE_TARGET_LANGUAGE` 118, `COMPARISON_READS_THE_QUOTATION_FIRST` 66. The suite's own neighbours are fragments — `CODE_IS_PRESERVED = "every quotation, every code sample, every heading"`. Pinned whole, a paragraph breaks the suite when somebody changes *here* to *there*, drops *however odd its literal parse*, or takes my §4 cut, none of which touches the behaviour. Worse, a test that is a verbatim copy of a paragraph is the second copy `docs/rules/docs.md` warns about: an editor repairing the wording repairs it twice, in two files, or repairs neither. **Should-fix:** pin the clauses that carry the discrimination — *take it on one pass*, *a shorthand this language uses itself*, *does not answer it*, *named by the word the reader has to supply* — and let the connective tissue move.

**`test_the_comparison_reads_a_translated_quotation_before_the_source` claims more than it tests.** Its docstring rests the whole test on the task being *the whole of what reaches a fresh subagent*, and then asserts the string is somewhere in `source-check.md`. That file is mostly prose *around* the task; only the blockquote beginning `> Compare the complete draft` is sent. Move the sentence out of the blockquote into the surrounding prose — exactly the edit that would silently stop it reaching any checker — and the test still passes. **Should-fix:** assert against the blockquote, not the file.

**Two changed surfaces get no test while a third does.** Redline's `help.md` is pinned on the stated ground that what a review does to a working quotation is observable behaviour. Write's `help.md` gained two sentences making the same claim about the same behaviour and is pinned nowhere, and the changed `case-study.review.md` sentence — the one I read as the riskiest in the change — is pinned nowhere either. The rationale does not stop at Redline's page. **Optional to add, but the asymmetry should be deliberate.**

Nothing in the four tests is wrong about the repository (`REDLINE`, `REDLINE_HELP`, `REPO_ROOT` and `STANDARD` all exist and are used as their neighbours use them), and the failure messages say what broke and why, which is this suite's standard and is met.

---

## Verdict

**Must-fix**

1. Step 6 makes quoted matter findable with no rule about whether it is repairable, and `languages/sv.md`'s Mechanics scope — which neither the review nor its correction subagent is allowed to load — says that repaired wording inside `”…”` is false about the source. Say in step 6 that such a finding is reported rather than repaired where the mark vouches for the wording.
2. `case-study.review.md`: *is not protected by its quotation marks*, beside *read for idiom like the prose around it*, reaches a reviewer holding no quotation policy at all. Restore the limiting word, or (preferred) delete the clause as §2 says.
3. `quotations.md` and `write/help.md`: *a figure of the source* is not scoped to the source **language** and its remedy clause therefore licenses flattening a speaker's own image — against the same file's *distinctive wording … stays*, two sentences away on the page. Say *a figure the source language supplies*.

**Should-fix**

4. `redline/references/correction.md` is not brought into line, against the pattern `docs/rules/skills.md` states for the code-sample rule; a quotation finding will usually come back unrepaired and spend a round doing it.
5. The `source-check.md` reading order arrives after the task has already ordered every attributed claim to be paired with its source; state it at the head of the task.
6. Delete the idiom clause from `case-study.review.md` now that step 6 covers every genre (this is also the cheapest fix for must-fix 2).
7. The four tests pin whole paragraphs verbatim; pin the discriminating clauses instead.
8. The `source-check.md` test asserts against the file rather than the blockquote that actually reaches the checker.

**Optional**

9. Cut *and settle that before you go on to anything else* and *Ask the question in the language in front of you, about the passage in front of you* from step 6, and *A rendering they stop in has failed however faithful its words are* from `quotations.md`; each restates something a few words away.
10. Say *reported speech* on Redline's page, as the body does.
11. Give Write's page the protective half, as Redline's page has it.
12. Consider pinning Write's `help.md` and the changed `case-study.review.md` sentence, or say why not.
13. `genres/case-study.md` points at *the quotation policy*, a file Redline cannot load; pre-existing, and this change leans on it harder.

**Would I ship this wording as it stands? No.** The core of it is right, and the reader-of-this-language test is a better instrument than anything it replaces — items 4 onward are ordinary polish I would not hold a release for. But item 3 makes Write's own instruction contradict its distinctive-voice boundary on the page a user reads, and items 1 and 2 together let a source-blind review find a defect inside a Swedish quotation, hand it to a repairer with no quotation policy and no mechanics scope, and come back with wording inside quotation marks that the collection's own language resource calls false about the source. Those are three sentences and one clause of work. With them fixed, ship it.
