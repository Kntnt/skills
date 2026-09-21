# A quotation is read in the language it is written in

This record decides how the two editorial Skills tell a quotation that has failed its target language from one that is doing that language's own work. Write's `references/quotations.md` and `references/source-check.md`, Redline's `SKILL.md` step 6, both `help.md` pages and the case-study review half carry one test between them: what does a reader **of the language in front of you** do at this passage. `docs/rules/docs.md` says where such a rule lives; this record says why the test has this shape and why three earlier shapes were set aside (issue #363, which took over the remainder of #329, #341 and #358).

## The two failures were the same failure

**One sentence of synthetic interview speech was right in English and wrong in Swedish.** *I would set that time aside before the next building starts* sits in a source package about a repair log trialled in two buildings. English carries it: a building starts in the sense of the work on it starting, and a reader takes the sentence on one pass. Swedish does not carry it. *Innan nästa hus börjar* and *innan nästa byggnad kommer i gång* say that a house begins, and a Swedish reader stops there and has to supply the activity out of the paragraphs around it.

**The product failed it in both directions at once.** Write delivered the Swedish calque and no comparison caught it; a source-blind review read the same calque in a frozen Swedish control and left it standing. In the same genre, in English, a review expanded *before the next building starts* into a spelled-out clause — a text that had nothing wrong with it, changed for a fault nobody could name.

**Those are not two defects but one missing test.** The only place the product told a review to look at quoted idiom was the case-study review half, and it named the miss and nothing else: *a missing referent that makes the reader reconstruct the meaning is a visible problem*. Read over the Swedish calque that sentence under-fires, because the meaning **can** be reconstructed. Read over the working English it over-fires, because a referent is implicit there too. One rule, stated by its failure mode, gives the same answer to two cases that need opposite ones.

## Why the test is a reader's one pass, in one language

**The question the rule now asks is what a reader of this language does at this passage.** A passage read on one pass is left alone. A passage that stops the reader to supply a word this language does not supply there is a finding, named by the word they have to supply. An ellipsis, a metonymy or a shorthand the language uses itself reads on one pass however odd it looks parsed literally, and is therefore not a finding.

**That the meaning can be worked out is explicitly not the answer.** It is the thing both earlier attempts came down to, and it is the thing that makes the Swedish miss look acceptable: the reader who reconstructs the activity has understood the sentence, and understanding is not the standard professional prose is held to. Saying so in the rule is what separates the two cases, because in the English text nothing has to be reconstructed at all.

**It is asked in one language, about one passage.** Not in the language the text may have come from, and never about a word somebody would rather see. A review that reaches for a synonym has found a preference; a review that can name the word the reader has to supply has found a defect. The clause the comparison task already carried — a concrete obstruction rather than a preferred synonym — had no test behind it until now, and this is that test.

## Why the writer and the checker are told the order to read in

**A rendering looks settled once the words it came from are in view.** The writer holds both languages at once and the checker is handed the source passage beside the draft passage, so both meet the calque with its source in sight; the shape that made it look reasonable is the shape on the page next to it. The source-blind review has no such problem and is given no such instruction.

**So both are told to read the finished rendering in the target language alone, first.** It costs nothing but an order of operations, and it is the only part of the change that answers the specific way this defect survives a comparison that is otherwise working. What it does not do is weaken the comparison: source support is judged exactly as before, and a translation finding stays a separate class from a source-support one.

## What was set aside

**A separate quotation reviewer.** The attempt preserved at `git show 3f21d9b1:skills/editorial/redline/references/quotation-review.md` gave each review and re-review a fresh seat with the whole artefact and 418 words of its own guidance. It repaired three of four frozen Swedish targets and broke working English, and one of its results introduced an unrelated spelling defect. It was removed before this ticket began and it does not come back: it cost a seat per review and did not separate the two directions, which is the only thing worth buying here.

**A shared surface.** The rule reaches both Skills, but not as one rule: the writer renders and the checker compares, while the review reads one text with nothing beside it. Written into `base.md` or `base.review.md` it would have had to be general enough to fit both acts, which is how it became the sentence that under-fires and over-fires at once. Each Skill states the test in the terms of the act it performs, which is what `docs/rules/docs.md` means by a rule governing one Skill's own behaviour living in that Skill's files.

**A rule against metonymy, and a rule for spelling out an implied noun.** Either would pass the Swedish case and fail the English one, and both would be a product that had learned one sentence. The contrast fixtures under `docs/evaluation/editorial-363/fixtures/` exist to catch exactly that: one moves the referent and keeps the construction, one moves the language and the rhythm, and neither names a replacement wording.

## What the evidence is

The measurement is in [`docs/evaluation/editorial-363/results.md`](../evaluation/editorial-363/results.md), with the frozen plan and the frozen fixture criteria beside it. Two arms over the same frozen inputs, the baseline arm being `main` unchanged, every run a fresh seat, every judgement two blind judges. The GPT-family failures this ticket inherits were not retested: the protocol forbids a Claude session from driving a Codex harness, so they stay failed and a GPT-family retest is a separate step.
