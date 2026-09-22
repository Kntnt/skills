# The bridge rule, read down the chain a `case-study` run actually loads

An independent read of the loaded resources as they stand at `ea31c6fe`. Nothing here rests on a diff: the question is what a writer and a reviewer are told, and where what they are told stops reaching.

## 1. The chain as I found it

### What Write loads

`skills/editorial/write/SKILL.md` step 5 fixes the composing contract and closes it: *Load the contract, and nothing besides it.* For `--genre=case-study` that is

- `references/editorial/base.md`
- `references/editorial/genres/case-study.md`
- no technique — `case-study.md` ends *The technique this genre is ordinarily written with: None.*, so level 6 of the resolution supplies nothing and no technique resource opens
- the **composition** scope of the resolved Language Resource, and that scope alone
- `references/editorial/web-craft.md` — the shared craft brief
- `references/editorial/article-anatomy.md`
- `references/editorial/headlines.md`

and the same step says the review halves are out: *A resource's review half — the file named for it with `.review.md` — belongs to the Skills that review, and so do the language's other scopes; none of them is loaded here.*

Three more resources enter later, none of them from the library:

- step 6, conditionally: `skills/editorial/write/references/quotations.md` — *Where the material is speech to be quoted, read `quotations.md` first.*
- step 7: `library/scripts/article_anatomy.py`, run over the finished draft
- step 8: `skills/editorial/write/references/source-check.md`, which dispatches a fresh checker subagent

What that checker is handed is itemised in `source-check.md`, and the list is short: the brief, the material, the complete draft, the resolved language, *the Claims section from the loaded base contract and, where quotations occur, the loaded quotation guidance*, plus composition guidance for translated quotations. Not `case-study.md`. Not the anatomy. And its task closes the door explicitly — *General editorial and mechanical review are outside this comparison.*

### What Redline loads

`skills/editorial/redline/SKILL.md` step 5 loads both halves of everything Write loads one half of, and adds two resources Write never sees:

- `base.md` + `base.review.md`
- `genres/case-study.md` + `genres/case-study.review.md`
- no technique, for the same reason
- the **composition**, **review** and **anti-slop** scopes of the language
- `anti-slop.md`
- `web-craft.md` + `web-craft.review.md`
- `article-anatomy.md` + `article-anatomy.review.md`
- `headlines.md` + `headlines.review.md`

Step 6 reviews against that set and runs the same anatomy script. Step 7 delegates each repair to a fresh subagent briefed from `skills/editorial/redline/references/correction.md`. Step 9 hands the result to Proofread for mechanics, and step 10 forbids anything substantive afterwards.

### What the correction agent loads

`correction.md`'s **The contract** paragraph reproduces Redline's step-5 list item for item: base both halves, genre both halves, technique both halves, `anti-slop.md`, the three language scopes, web-craft both, anatomy both, headlines both. So the correction subagent does hold the bridge rule and the pre-echo instruction. It is also told, twice and forcefully, *Repair what the findings name and nothing else* — so in practice the rule reaches it only through a finding Redline already wrote.

### The asymmetries

1. **No review half reaches Write.** This is the structural one. The composing agent — the only party that can avoid the defect rather than repair it — gets the rule's one-sentence statement of intent. The reviewing and correcting agents get that sentence *plus* the pairing instruction that tells them how to look for it. The half that says how to find the fault is withheld from the half that would otherwise not commit it.
2. **`quotations.md` is Write-private.** It lives under `skills/editorial/write/references/`, and nothing outside Write references it. Redline never loads it; the correction subagent never loads it. Its only non-Write reader is the source-check checker, which `source-check.md` hands it directly. So the correction agent — the one party in the whole chain licensed to rewrite the prose standing beside a quotation — holds no quotation-repair boundary beyond one clause of `correction.md` (*without … altering a quotation's meaning, stance, certainty or distinctive wording*) and the corresponding sentence of `base.review.md`. Redline step 6 substitutes a one-line paraphrase: *Read each passage of reported speech as a review unit against the resolved language and genre guidance, preserving its meaning and distinctive voice.*
3. **`anti-slop.md` does not reach Write.** Its **Generic conclusions** entry — *A final paragraph that restates what the reader has just read* — is the nearest sibling in the collection to a pre-said quotation, the same defect with the sign flipped. The writer never reads it.
4. **Write's own verification step is constitutionally blind here.** The source-check comparison judges source support and translation fidelity. A bridge that pre-says a quotation is perfectly source-supported — the quotation is its source — so it passes. The script counts characters, words, sentences, paragraphs, sections and part order; it sees nothing. Write therefore has exactly one place where this rule can act: the writer's own reading of one sentence in `case-study.md` while composing.
5. **Both Skills load the standfirst/lead pairing; only Redline loads it twice.** More on that in §3.

## 2. Where the rule is stated, and what it asks of a writer

### The composing half

`genres/case-study.md`, the third paragraph of **What this genre asks for**, entire:

> Let attributed quotations carry the customer's experience and judgement, with narrative doing the connecting work. A bridge should prepare a quotation rather than pre-say it. Preserve the supplied speech within the quotation policy and the language's conventions.

That is the whole of what a writer is told. The middle sentence is the rule.

### The reviewing half

`genres/case-study.review.md`, the opening of its second paragraph:

> Read bridges beside quotations and the standfirst beside the body's opening. Remove a redundant pre-echo while keeping the attribution and any distinct fact.

### Is it a test?

No. It is a statement of intent expressed as a contrast between two coined verbs. *Pre-say* appears nowhere else in the collection; *pre-echo* appears nowhere else either; and *bridge*, in the editorial sense, appears in these two files and in no other resource an editorial run loads. `CONTEXT.md` does define **Bridge** — as *a command one Harness runs to put work on a model belonging to another*, the routing term, an unrelated sense — and `CONTEXT.md` is not loaded by a `case-study` run in any case. So an agent composing a case study meets *bridge* with no gloss and supplies its own, out of its general knowledge of journalism.

The question the rule puts in the writer's head is roughly *is this sentence a preparation or a pre-saying?* — a self-classification, asked about a sentence the writer has already decided to write, answered by the same judgement that wrote it. There is no reader in it, no moment, and no named failure. A writer who summarises the quotation's point and then quotes it can answer *preparation* in good faith: they did prepare the reader for it.

Compare what the same chain does with the identical shape of rule, one file away. `article-anatomy.md`, **Standfirst and lead**:

> Read in sequence, the lead advances. A reader who has just read the standfirst meets the lead as new material, never as the standfirst said again; what the body needs from the standfirst is named again in passing, and the lead moves on.

That names the reader, the moment of reading, the failure state in the reader's experience, and — in its second clause — what may legitimately be carried over anyway. It is a test a writer can run against a sentence. And `article-anatomy.review.md` gives the reviewer a procedure to go with it: *Read the standfirst separately, then with the lead. … Then read the body with the standfirst covered.*

The bridge rule has neither. There is no *read the section with the quotation covered*, no *read the quotation first and ask how much of it the reader already has*, and no statement of what a bridge may legitimately carry. The review half supplies a fragment of the last one — *while keeping the attribution and any distinct fact* — but it supplies it to the reviewer, not to the writer, and as a constraint on removal rather than as a description of the good form.

### The sentence standing in front of it

*with narrative doing the connecting work* is the instruction the rule then qualifies, and read on its own it supplies a way to fail. A writer asking what connecting work is may reasonably answer: state where the account has got to, state what the customer concluded, then let the customer say it. That is the defect. The rule is the corrective to its own neighbour, and it is the shorter and the vaguer of the two.

## 3. What the rule's words reach, and what they do not

### The scope of *bridge*

The chain never fixes it. Read ordinarily — and this is how the evaluation's own plan fixed it, and how both judges read it — a bridge is the clause or sentence standing immediately before the quotation. On that reading the rule's reach is one sentence, and the defect it names is not a property of one sentence. It is a property of everything the reader has already read when they arrive at the quotation.

Four things can pre-say a quotation. The rule reaches one of them.

- **A bridge.** Reached. Stated. Reviewed.
- **An earlier sentence in the same section.** Not a bridge, not reached. A paragraph that reports the customer's verdict and then, two sentences later, quotes the customer giving it, does the same damage as an adjacent pre-echo and escapes the word entirely.
- **The subheading over the section.** Not a bridge — a heading two steps up is not the clause before the quotation — and it does *more* damage, because the reader meets it before everything under it and carries it through the whole section. Nothing in the loaded set pairs a subheading with a quotation.
- **The standfirst, and the headline.** Furthest away, greatest reach, and the two the genre most actively encourages. `case-study.md`: *The headline names the customer's benefit or result, and the standfirst introduces the account behind it.* `headlines.md`: the headline *states the angle: the single most important message, the sentence that would remain if only one could*. In a case study, the customer's result is the angle — and a closing appraisal quotation is the customer saying that result in their own words. Some degree of pre-saying is therefore built into the form, and the chain gives nobody a way to tell the legitimate case (the headline asserts the result; the quotation supplies the customer's own words and their qualifications) from the defective one (the reader has already been given the sentence they are about to hear).

Where would the chain catch the cases the word misses?

- **`base.md`** reaches them in principle, and is loaded by everyone: *Each passage earns its place. Repetition may establish an independent entry point, explain a hard idea or give a deliberate rhetorical return; merely saying the same thing again does none of these.* But it is a general redundancy rule with no mention of quotations, and it is framed around the *second* saying. In a pre-said quotation the narrative sentence comes first and the quotation is the repetition — so a reviewer applying this rule literally is pointed at the wrong half, towards trimming the quotation, which is the one thing the genre exists to protect. The rule is available but mis-aimed.
- **`headlines.md` / `headlines.review.md`** come closest and still miss. The base says *subheading and the first sentence under it, say different things in different words*; the review lists as a finding *The same words and phrasing in the headline and the standfirst or opening paragraph, or in a subheading and the first sentence under it.* Two gaps. It is a words-and-phrasing test, not a content test — a heading that says the same thing in different words passes it. And where a bridge stands between the subheading and the quotation, the quotation is not *the first sentence under it*, so the pairing does not even engage the case. Worse, the composing instruction actively pushes the other way: *Word a subheading from its whole section, once the section is written, in words its first sentence does not use.* A section whose content-bearing centre is a quotation yields a subheading worded from that quotation, guarded only against reusing the bridge's vocabulary. That is an instruction to pre-say the quotation tidily.
- **`article-anatomy.md` / `.review.md`** pair standfirst with lead, and body with standfirst for unresolved referents. Never a quotation with anything.
- **`article_anatomy.py`** measures counted limits — characters, words, sentences, paragraphs per section, part order. It has no opinion here, and both Skills are told to take counts from it rather than from their own reading, so it consumes no attention either.

### The review half's pairings

Explicitly named across everything Redline loads:

| Pairing | Where |
| --- | --- |
| bridge × the quotation after it | `case-study.review.md` |
| standfirst × body's opening | `case-study.review.md` |
| standfirst × lead, and body read with standfirst covered | `article-anatomy.review.md` |
| headline × standfirst / opening paragraph | `headlines.review.md` |
| subheading × the first sentence under it | `headlines.review.md` |

Left out:

- subheading × the quotation in its section
- standfirst or headline × any quotation
- any earlier sentence of a section × the quotation that section is built around

So the genre's own review sentence spends its first half restating a pairing the loaded anatomy already states twice and states better, and spends none of itself on the pairings the defect can actually use. The one thing said three times is the thing already covered; the thing said nowhere is the heading.

## 4. What else in the chain pulls against the rule

1. **`case-study.md`'s own preceding clause** — *narrative doing the connecting work* — as in §2.
2. **`headlines.md`'s subheading recipe** — *Word a subheading from its whole section* plus *states the angle: the single most important message* — as in §3. For a section whose point is a quotation, the most important message is the quotation's message.
3. **`case-study.md`'s headline instruction** — *The headline names the customer's benefit or result* — which puts the appraisal quotation's substance at the top of the page by requirement.
4. **The paratext-independence rules, in two resources.** `article-anatomy.md`: *Self-contained: a reader who sees only the standfirst understands it fully. It says what the article is about and what the reader gains from reading it.* `base.md`: *The body and its sections remain intelligible without treating a title, standfirst or subheading as their opening sentence.* Both are right, and together they instruct the writer to put the payload in the paratext and then say the payload again in the body. That is the pre-say shape, sanctioned. The anatomy resolves the tension for exactly one pair — *what the body needs from the standfirst is named again in passing, and the lead moves on* — and for nothing else. No resource resolves it for a quotation.
5. **Redline's claim-preservation machinery works against the one repair the review prescribes.** `case-study.review.md` tells the reviewer to *Remove a redundant pre-echo* — that is, delete a narrative sentence. But `correction.md` tells the agent that would do it: *where the passage carries a claim beside the defect — a fact, an observation, the point the passage exists to make — the smallest change is the one that leaves that claim standing, and deleting the passage entire is not that change*; and *where you can see no way to remove the defect that does not take the claim with it, leave the passage alone and say so*. And Redline step 7 backs that with an acceptance check: *Where a claim sat beside the defect, reject the returned correction, keep the pre-round Text Artifact as current, carry the original finding forward as unresolved.* A pre-echo is by construction a sentence whose content is a claim, usually carrying an occasion or a date beside it. The review's own qualifier — *while keeping the attribution and any distinct fact* — shows the intended repair is a trim rather than a deletion, and the two instructions are reconcilable on that reading. But nothing in the loaded set says so, the word the reviewer is given is *Remove*, and the safe reading for both the correction agent and Redline's acceptance check is to leave the sentence and report the finding unresolved. The single place in the chain that is told to remove a pre-echo is also the place most heavily instructed not to remove sentences.
6. **The one instrument that would fix a heading pre-say is never pointed at it.** `headlines.review.md` ends *repair by rewriting the headline alone, from the text's angle and at the text's own strength. The text stays as it is.* That is precisely the right repair for a subheading that says what the quotation under it says — cheap, safe, touches no claim and no quotation. No rule in the chain produces a finding that would route there, because the **Avoid** list has no entry for a heading that pre-says a quotation in its section.
7. **A language-convention edge, worth one line.** `sv.md`'s composition scope: *Speech that the text reports is ordinarily set with a speech dash rather than in quotation marks*, with attribution trailing — *– Det gick fortare än vi trodde, säger hon.* In that form there may be no introducing clause at all, and the preparing work is done by the preceding paragraph. The word *bridge* presumes a shape Swedish reported speech does not always have, and the rule as worded has correspondingly less purchase in the language this collection's craft brief is built around.

## 5. The answer

**Partly — and only for one sentence's worth of the problem.**

A writer is given the intent and no test, in a single sentence, with a coined verb, standing immediately after a clause that supplies a way to fail it, and with nothing downstream in Write able to check it: the source comparison excludes editorial review by its own terms, and the script counts. A reviewer is given one pairing, which catches the adjacent case well, and is given no pairing for the two cases the paratext instructions elsewhere in the same chain actively encourage. So the chain is adequate against the narrow, adjacent form of the defect and not adequate against the form the rest of the chain tends to produce.

The shape of the gap is worth stating plainly: **the rule's window is one sentence wide; the defect is as wide as everything the reader has already read.**

### Must-fixes

Ordered by reach per word, which is the order I would insist on them.

1. **Add the missing pairing to `case-study.review.md`: read each quotation against the subheading standing over it, and against the standfirst, not only against the clause before it.** This is the largest hole and the cheapest patch — a clause added to a sentence that already exists, in a file the reviewer and the correction agent both load. Without it the chain has no route from a heading that pre-says a quotation to the one repair instrument (`headlines.review.md`) that could fix it safely.
2. **Say what a bridge is, in the resource, in one clause.** As it stands the scope of the rule is whatever the reading agent assumes, and the term's only definition in the repository is an unrelated routing sense in a file the run does not load. A rule whose central noun is undefined cannot be applied consistently by two readers, and consistency between the writer's reading and the reviewer's reading is the whole of what this pair of files is for.
3. **Give the composing half a reader test, in the shape the anatomy already uses, and say what a bridge may carry.** Something with the anatomy's anatomy: the reader meets the quotation as new material, never as something the section has already said for the speaker; the bridge gives the occasion, the speaker and what the quotation does not state. Until then the rule is an intent, and the sentence in front of it is more actionable than the rule is.

I would call (1) and (2) blocking. (3) I would call blocking on the merits of the reading alone.

### One note on the record

After forming the above I read `docs/adr/0214-a-bridge-prepares-a-quotation-rather-than-pre-says-it.md`, which decides not to reword the composing half, on the grounds that the fault did not reproduce in seven Claude-family runs and that the cost criterion admits added reading only against a reproduced miss. That is a sound decision on its own terms, and it does not touch must-fixes (1) or (2): the ADR's own measurement found the pre-echo had moved into the section heading, names `case-study.review.md`'s pairing of *a subheading with nothing* as the gap, and records that its judges split on where the bridge even was in the Swedish row — which is (2) arriving from the measurement side. Both are already carried by #396. My reading of the resources reaches the same two, independently, and would rank them ahead of the rewording the ADR declined. Where I differ from the record is only on (3): I would keep it as a must-fix on the reading, while accepting that the repository's evidence rule is a legitimate reason to hold it until a family that exhibits the fault is retested.

### Non-blocking observations

- `quotations.md` is loaded by Write and by the source-check checker, and by no reviewing or correcting agent. The correction subagent rewrites prose beside quotations holding a one-clause paraphrase of a six-section boundary document. Nothing in this ticket's question depends on it, but it is the asymmetry most likely to cost something elsewhere.
- `anti-slop.md` does not reach Write at all. Its **Generic conclusions** entry describes the same defect as this one with the sign flipped, and the writer never sees it.
- The standfirst × opening pairing is stated in three loaded files. That is not harmful, but it is the budget the genre's review file spends instead of covering the heading.
