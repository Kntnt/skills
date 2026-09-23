# Load-chain review — the bridge rule as a `case-study` run actually loads it

Read against the tree as it stands at `ea31c6fe`. Nothing was changed, nothing was run. The question: does the chain a `case-study` run loads give a writer and a reviewer what they need to keep a quotation from being pre-said, and where does it not reach?

## 1. The chain as I found it

### Write

`skills/editorial/write/SKILL.md` step 5 fixes the load for `case-study`, and fixes it closed — *"Load the contract, and nothing besides it"*, ending *"Done when this bounded contract is loaded, with no review half."*

| Loaded by Write | Where the instruction is |
| --- | --- |
| `references/editorial/base.md` | step 5 |
| `references/editorial/genres/case-study.md` | step 5 |
| composition scope of the resolved language | step 5 (step 3 resolved it) |
| `references/editorial/web-craft.md` | step 5, named for the five web genres |
| `references/editorial/article-anatomy.md` | step 5, named for the four article genres |
| `references/editorial/headlines.md` | step 5, same four |
| `write/references/quotations.md` | step 6, **conditionally**: *"Where the material is speech to be quoted, read `quotations.md` first"* |
| `write/references/source-check.md` | step 8 |

No technique: `case-study.md` line 23 says *None*, so the technique level is empty and resolution falls through to no technique.

Explicitly **not** loaded by Write: every `.review.md`, `anti-slop.md`, and every language scope but `composition`. Step 5 says so in as many words.

Write's only second reader is the source-check subagent of step 8. `source-check.md` line 5 fixes what that checker is given: the brief, the material, the complete prose, the resolved language, *"the Claims section from the loaded base contract and, where quotations occur, the loaded quotation guidance"*, plus composition guidance for translated quotations. **The genre resource is not among them.** The checker's task text (line 7) is a source-support and translation comparison and closes *"General editorial and mechanical review are outside this comparison."* So the bridge rule reaches exactly one agent in the whole Write path: the drafting agent itself.

### Redline

`skills/editorial/redline/SKILL.md` step 5 loads both halves throughout:

- `base.md` + `base.review.md`
- `genres/case-study.md` + `case-study.review.md`
- `anti-slop.md`
- the `composition`, `review` and `anti-slop` scopes of the resolved language
- `web-craft.md` + `web-craft.review.md`
- `article-anatomy.md` + `article-anatomy.review.md`
- `headlines.md` + `headlines.review.md`

Not loaded: mechanics (step 9's nested Proofread owns it), and `quotations.md`, which is Write-local and is never named by Redline at all.

### The correction subagent

`redline/references/correction.md`, under **The contract**, restates Redline's step-5 list item for item, including `case-study.review.md` and both anatomy and headline halves. So the correction agent sees both halves of the bridge rule. It is nonetheless bounded by **What you change, and what you preserve**: *"Repair what the findings name and nothing else."* It can only act on a pre-say the reviewing agent already recorded as a finding.

### Proofread

Redline step 9 forwards only `--language` and the two paths, and step 10 forbids substantive change after it. Mechanics only. Out of scope for this rule.

### The asymmetries

1. **The writer loads no review half.** This is the load-bearing one. The two statements in this collection that make the anti-pre-say idea *operable* both live in review halves: `case-study.review.md` line 5 (*"Remove a redundant pre-echo while keeping the attribution and any distinct fact"*) and `article-anatomy.review.md` line 11 (*"read the body with the standfirst covered"*). The agent composing the sentence is forbidden to load either. The agent reading the finished text has both. The rule is stated most usefully to the party least able to prevent the defect.
2. **`anti-slop.md` reaches Redline and the correction agent, never Write.** Its **Generic conclusions** pattern — *"A final paragraph that restates what the reader has just read"* — is the nearest thing in the collection to a general rule against handing the reader something they already have. The writer never reads it. The writer's only equivalent is `base.md` line 19, *"merely saying the same thing again does none of these."*
3. **`quotations.md` reaches Write only, and conditionally.** Redline's reviewer and the correction agent never see it. `correction.md` inlines a partial paraphrase of its prohibitions — *"a quotation's meaning, stance, certainty or distinctive wording"* — which omits the self-correction rule, the *Anything additive* rule and the paraphrase route entirely. This does not bear on pre-saying (nothing in `quotations.md` concerns the narrative outside the quotation marks) but it is the same class of gap and worth recording.
4. **Write's second reader is given `base.md`'s Claims section, not the genre.** A bridge that asserts more than the material carries is catchable there. A bridge that is merely redundant is not a source finding, and the checker is told general editorial review is outside its comparison. So Write has no second reader for this rule at all.

## 2. Where the rule is stated, exactly

Base half, `skills/kntnt/library/references/editorial/genres/case-study.md` line 17, whole paragraph:

> Let attributed quotations carry the customer's experience and judgement, with narrative doing the connecting work. A bridge should prepare a quotation rather than pre-say it. Preserve the supplied speech within the quotation policy and the language's conventions.

Review half, `case-study.review.md` line 5, first two sentences:

> Read bridges beside quotations and the standfirst beside the body's opening. Remove a redundant pre-echo while keeping the attribution and any distinct fact.

Those are the only two places in the tree. `grep -rn "bridge"` over `skills/` returns nothing else editorial; `pre-say` and `pre-echo` occur once each, in these two sentences, and nowhere else in the collection.

### How a writer would apply it

It is a statement of intent, not a test.

*Prepare* and *pre-say* are both undefined, and *pre-say* is a coinage with no reader-facing question behind it. The instruction is a comparison between two abstractions, and a writer who believes they have prepared has satisfied it by believing so. There is no procedure — no "read these two things in sequence and ask X", no "cover this and check that" — of the kind the collection uses elsewhere.

Worse, the sentence immediately before it pushes the other way. *"narrative doing the connecting work"* is what a writer will reach for when composing the lead-in, and a summary of what the customer is about to say is superb connecting work and a perfect pre-say. The rule against it is the next sentence and it is weaker than the invitation.

The question it puts in the writer's head is therefore **"is my lead-in doing connecting work?"** — which is the wrong question, because a pre-say answers it *yes*. The question it does not put there is **"what does the reader already know by the time they reach the quotation marks?"**

That second question is exactly the form this collection uses one resource away, in a file Write does load. `article-anatomy.md` line 59:

> Read in sequence, the lead advances. A reader who has just read the standfirst meets the lead as new material, never as the standfirst said again; what the body needs from the standfirst is named again in passing, and the lead moves on.

That is a test. Read the pair in order; ask whether the second is new; and it even names what the second part *may* legitimately carry over (*"named again in passing"*). The bridge rule is the same shape of rule about a different pair of parts, and it has none of that machinery. A writer's best available procedure for the bridge is to borrow this one by analogy — which requires noticing the analogy unprompted.

The review half is materially better. *"Remove a redundant pre-echo while keeping the attribution and any distinct fact"* names the defect **and** the salvage, which is what `base.review.md` line 9's removal test (*"Test suspected filler by what its removal costs; preserve any fact, implication or voice it carries beside the defect"*) asks a reviewer to do. It is still not a reader test, but it is actionable, and by implication it is also the only place the collection says what a bridge may legitimately carry: the attribution and any distinct fact. The writer never loads it.

One smaller thing: the two halves use two different coined words for one defect — *pre-say* in the base half, *pre-echo* in the review half — and neither is defined. A writer and a reviewer discussing the same fault have no shared name for it.

## 3. What the words reach, and what they do not

### The scope of *bridge*

The product never defines it. The only written definition in the repository is evaluation apparatus — `docs/evaluation/editorial-364/plan.md` fixes a bridge as the clause standing immediately before the quotation — and no run loads that file.

The word does not class steadily even among careful readers holding that definition. ADR-0214 records that in `case-study-sv-r2` *"the judges disagreed about where the bridge is at all, one taking the heading and one not"*, and that in `case-study-en_US-r1` one bridge drew two (a) readings and one (b) across three readings. A rule whose subject two blind judges cannot locate the same way is not a rule a writer can run against a sentence.

### Yes, a sentence that is not immediately before the quotation does the same damage

The reader's loss is *meeting the quotation as something already delivered*. Nothing about that loss requires adjacency. Five places in a `case-study` can inflict it, and the chain's reach differs at each.

**The section subheading standing over the quotation.** This is not hypothetical: it is the measured result. ADR-0214, *What the measurement found instead*, records two of three `case-question-en_GB` drafts where the reader meets the closing quotation as something already said, in the heading — *Vale would use the schedule again for new jobs* over *I would use it again for new jobs.* Both judges of that row reported it unasked, one calling it the draft's clearest editorial defect, while both still classed the bridge itself (b), correctly.

*Would the chain catch it?* **No.** `case-study.review.md` line 5 pairs bridges with quotations and the standfirst with the body's opening; it pairs a subheading with nothing. `headlines.review.md` line 17 pairs *"a subheading and the first sentence under it"* — which touches the quotation only where the quotation is literally the section's first sentence, and even then the stated test is *"The same words and phrasing"*, a lexical one. A paraphrased pre-say passes it cleanly, and the measured heading above is a paraphrase. `headlines.review.md` line 3's four questions (support, core message, tone, misled) contain nothing about redundancy against what follows. This is #396, correctly scoped.

**The standfirst.** `article-anatomy.md` lines 38–43 require a summarising, self-contained paragraph that *"says what the article is about"*; `case-study.md` line 13 has it *"introduce the account behind it"* and makes *"the customer's own appraisal"* required content of the account. A standfirst that summarises an account whose point is the appraisal pre-says the closing appraisal quotation by construction.

*Would the chain catch it?* **No.** The standfirst is paired three times and never with a quotation: with the body's opening (`case-study.review.md` line 5), with the lead for restart-without-advancing, and with the body for dangling referents — and `article-anatomy.review.md` line 11 scopes that last one narrowly, to *"A pronoun, a definite form or a phrase such as the reason whose referent only the standfirst supplies"*, *"repaired by naming the referent"*. That is a comprehension check, not a redundancy check, and its repair adds words to the body rather than removing them from the paratext.

**The lead.** Same pressure one part down, same absence of a pairing.

**An earlier paragraph in the same section.** A reader who met the judgement two paragraphs above meets the quotation as repetition just as squarely as one who met it in the preceding clause.

*Would the chain catch it?* **Only through the general rule.** `base.md` line 19: *"Repetition may establish an independent entry point, explain a hard idea or give a deliberate rhetorical return; merely saying the same thing again does none of these."* And `base.review.md` line 3: *"Repetition of whole sentences or passages is an editorial matter, even when the duplication is verbatim."* Both are real but blunt: they are about repetition as such, with no quotation-specific instruction and no pairing to read side by side. They will fire on near-verbatim duplication and are unlikely to fire on a narrative paraphrase of a judgement that is then quoted.

**The ending.** `article-anatomy.md` line 80 makes restatement a requirement of the closing section: *"It shows that the expectation the lead set has been met."* Where the closing appraisal quotation sits in the ending — the ordinary place for it in this genre — the ending's own job pushes toward saying its content first.

*Would the chain catch it?* **Partly, for Redline only.** `anti-slop.md`'s **Generic conclusions** pattern is the nearest catch, and it is aimed at a final paragraph restating *the text*, not one restating a quotation it contains. Write does not load `anti-slop.md` at all.

### The review half's pairings, in full

What a `case-study` reviewer is told to read side by side:

- bridge ↔ quotation (`case-study.review.md` line 5)
- standfirst ↔ body's opening (`case-study.review.md` line 5)
- standfirst alone, then standfirst ↔ lead, then body with the standfirst covered (`article-anatomy.review.md` line 11)
- headline ↔ the text's angle; each subheading ↔ its own section; subheading ↔ its first sentence (`headlines.review.md` lines 3 and 17)
- quoted speech ↔ target-language idiom (`case-study.review.md` line 5); quotation form ↔ the text's own consistency (`sv.md` review scope line 54)

The pairing left out is **subheading ↔ the quotation it stands over**, and one step wider, **any paratext or earlier narrative ↔ a quotation further down**. Every pairing in the list above is between adjacent or structurally coupled parts. The pre-say defect is not confined to adjacency, and the pairing set is.

## 4. What else in this chain pulls against the rule

**`headlines.md` line 31 licenses the measured fault outright.** *"Word a subheading from its whole section, once the section is written, in words its first sentence does not use."* The section includes the quotation. The only stated bar is reusing the *first sentence's* words. So a subheading composed from the section's most quotable content, worded differently, is not merely permitted — it is the prescribed method. This is the strongest pull in the chain, it sits in a file **Write loads**, and it is the instruction that would most plausibly have produced the heading pre-echo ADR-0214 measured.

**`headlines.md` line 11 aims the subheading at the sharpest claim available.** *"It states the angle: the single most important message, the sentence that would remain if only one could. … Test: the headline could not head a different text on the same subject."* By line 3's own scope rule (*"Headline here covers a text's subheadings too; for a subheading, the text is its section"*), that test applies to every subheading. In a case study the single most important message of a section built around the customer's appraisal *is* the quoted judgement. The file's quality test and the genre's bridge rule point in opposite directions, and nothing reconciles them.

**`case-study.md` line 17's own first sentence.** *"narrative doing the connecting work"* — discussed above. The invitation precedes the restriction and is the more natural reading of the two.

**`base.md` line 9.** *"A transition may explain a connection, but cannot invent one."* A bridge is a transition. The permission to *explain* is stated; the caution against explaining the quotation's own content is not. The one restriction attached is truthfulness, not redundancy.

**`article-anatomy.md` lines 38–43 with `case-study.md` line 13.** A mandatory summarising standfirst over a genre whose mandatory content includes the customer's appraisal. Redundancy against the appraisal quotation is structurally invited, and no pairing checks for it.

**`article-anatomy.md` line 80.** Restatement as a requirement of the ending, where the appraisal quotation usually lives.

**Pulling the right way**, and worth naming: `base.md` line 19 is a genuine general brake, and `article-anatomy.md` line 59 gives the writer the exact reader test this rule wants — for a different pair of parts. The writer has the model in hand and is not pointed at it.

## 5. The answer

**Partly, and unevenly.**

For a **reviewer**, the chain is adequate for the narrow case and no wider. It names the defect, names the salvage, names the pairing, and hands the same resources to the correction agent that repairs it — and the measurement bears this out: `results.md` records three class (a) bridges repaired across the Redline pairs and none introduced. But its pairing set is adjacency-shaped, and the one place the fault was actually measured to live — the section heading — is paired with nothing. The reviewer is equipped for the case the rule names and blind to the case the evidence found.

For a **writer**, the chain does not reach. The composing agent loads one sentence: an intent with a coined undefined verb, an undefined subject, no reader test, and an invitation to summarise in the sentence immediately before it. It loads a headline instruction that actively prescribes wording a subheading from the whole section including the quotation. It loads none of the three things that would counterweight any of that — the review half's *pre-echo* wording, `anti-slop.md`'s **Generic conclusions**, or any pointer to `article-anatomy.md` line 59 as the model to apply here. The rule is stated in its usable form only to the agent that reads the text after it is written.

I would not reopen the bridge wording itself on this evidence. ADR-0214's reasoning stands: the fault does not reproduce in this family, the cost criterion has no miss to point at, and adding general wording to a shipped resource on non-reproducing evidence is the wrong trade. What follows are must-fixes about **reach and vocabulary**, not about sharpening an abstract rule.

### Must-fix 1 — `headlines.md` line 31 must stop licensing the fault

This is the cheapest repair in the chain and the only one that costs the writer no additional reading, because the sentence is already in Write's mandatory load. *"in words its first sentence does not use"* is the wrong bar when the section contains a quotation: it permits, and by its phrasing recommends, a heading that states the quotation's content in other words. Whatever wording replaces it, the bar has to be about what the reader already has rather than about which words were reused. Until it changes, the chain contains an instruction that produces the defect the genre resource forbids, and the instruction is more specific and more procedural than the prohibition.

### Must-fix 2 — any wording written for the heading case must land in a half the writer loads

#396 owns the heading gap. My insistence is on **where its repair goes**. If it lands only in `case-study.review.md`, it reproduces exactly the asymmetry this review found: the reviewer gets a rule the writer cannot read, for a defect only the writer can avoid. And it must not land in `headlines.review.md` alone either — that file's existing test is lexical and scoped to the section's first sentence, so widening it there would still miss a paraphrase two sentences down.

### Must-fix 3 — whatever survives must say what counts as a bridge

ADR-0214 reaches this conclusion from the other end (*"a wording written for the heading has to say what counts as a bridge, or it will be measured the same way"*), and it holds for the shipped wording too. Two blind judges holding a written definition disagreed about where a bridge was. A writer holding none is in a worse position. Either the word gets a scope in the resource that uses it, or it is replaced by naming the parts directly.

### Must-fix 4 — one word, not two

*pre-say* and *pre-echo* are two coinages for one defect, split across the two halves, each occurring exactly once in the tree and neither defined. Whichever survives, both halves should use it. This costs nothing and is a prerequisite for a reviewer's finding and a writer's rule being recognisably about the same thing.

### Not a must-fix, but recorded

`quotations.md` is Write-local and is never loaded by Redline's reviewer or by the correction agent; `correction.md` inlines a partial paraphrase of its prohibitions that drops the self-correction rule, the *Anything additive* rule and the paraphrase route. Nothing in `quotations.md` bears on pre-saying — it governs the inside of the quotation marks — so this is outside the question asked. It is the same shape of gap and belongs on somebody's list.
