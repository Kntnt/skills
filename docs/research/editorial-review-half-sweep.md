# Editorial review halves against their base halves

Researched on **2026-09-28**, against `708bff52`, the run branch's tip, which carries #396's change to `headlines.md`, for issue #414. This is a findings document. What it led to is the test written into `skills/kntnt/library/references/editorial/README.md` under `## Review extensions` and into the pairing sentence in `docs/rules/skills.md`, and issue #438.

## The test

A review half is complete when the requirement it diagnoses is **stated operably where the writer reads it — in the files Write loads for the genre**. Operable means that a writer who has read only those files can tell, before writing, whether a sentence of theirs meets the requirement. The model is `article-anatomy.md`'s reader test: *A reader who has just read the standfirst meets the lead as new material, never as the standfirst said again.*

The files Write loads for a genre are those in its step 5 and the references it reads in step 6: `base.md`, the genre's base half, the resolved technique's base half, the language's composition scope, the support files `web-craft.md` (article, case-study, column, opinion, web-copy), `article-anatomy.md` and `headlines.md` (the first four only), and `skills/editorial/write/references/quotations.md` where the material is speech to be quoted. A report is ordinarily written with `pac.md` and a teaser with `abt.md`, so those techniques are read with those genres.

Each rule of a review half has one of these classes:

- **operable-in-base**: the requirement it diagnoses is already stated operably where the writer reads it, and the reason names the file.
- **review-only**: only the review half says how to avoid producing the defect in a draft.
- **sound**: the wording is about recognising, reporting or minimally correcting a defect in finished prose, which a writer does not need.
- **handled by #396**: the `case-study` bridge rule alone.
- **out of scope, filed as #N**: a rule that could be made operable only by adding a target or by choosing between two readings of the base half.

The unit is one line per numbered section where a review half has them (`press-release`, `report`, `teaser`), and otherwise one line per sentence that names a defect. The sentences that name no defect — the correction procedure, the limits on a finding, what is left alone — are given lines of their own too, grouped where they stand together, so that every sentence of a review half is accounted for.

## Verdict

One rule in the fourteen review halves is review-only: the `case-study` quotation bridge. It is reserved for #396, and #396 made the subheading over a quotation operable but not the bridge, so it is recorded as handled by #396, not made operable, and filed as #438. Every other rule is either operable-in-base or sound.

So no base half changed, no review-half sentence became a restatement, and none was deleted. The one change the sweep leads to is the test itself, in the format page and the standard, so that the next author of a review half holds a new pair to it.

The rules closest to the line are listed under *The closest calls* at the end, with the reason each was judged operable.

## `base.md` and `base.review.md`

| Rule | Class | Reason |
| --- | --- | --- |
| "A finding identifies the passage, the requirement and what the reader loses. Another successful choice, a house-style preference and a mechanical error are not editorial findings" | sound | Says what a finding is and what is not one; a writer does not report findings. |
| "Repetition of whole sentences or passages is an editorial matter, even when the duplication is verbatim" | sound | Says which pass owns a defect. The writer's requirement is `base.md`'s *merely saying the same thing again does none of these*. |
| "an unexplained term" | operable-in-base | `base.md`: *introduce unfamiliar concepts before the reasoning needs them*, *introduce an unfamiliar abbreviation before using it alone*. |
| "a transition asserting a relation the surrounding sentences do not establish" | operable-in-base | `base.md`: *A transition may explain a connection, but cannot invent one.* |
| "a section whose place obscures the argument" | operable-in-base | `base.md`: *order material by that reader's needs rather than the writer's discovery process*. |
| "Cover the paratext to find unresolved references in the body" | operable-in-base | `base.md`: *The body and its sections remain intelligible without treating a title, standfirst or subheading as their opening sentence.* The review half adds only the way to find it. |
| "Judge rhythm by its effect, not sentence counts; purposeful repetition, a personal rough edge and a useful digression may be doing essential work" | sound | Limits what a reviewer may call a defect. |
| "A number contradicting its stated denominator, a causal conclusion following only a sequence, or a certainty contradicted by a nearby qualification is diagnosable" | operable-in-base | `base.md`, *Claims*: every claim supported by the text or its material, *A sequence or correlation establishes no cause*, *Keep uncertainty where it exists*. |
| "A plausible quotation or experience is not disproved by the absence of its original source. Review no unseen material, request none, and add no source-verification caveat" | sound | Limits the review to the text in front of it. |
| "Use the anti-slop catalogue to recognise empty performance, not to prohibit a working figure, contrast or ending" | sound | Says what the catalogue is for in a review. The writer's requirement is `base.md`'s *decoration and manufactured drama cannot* and *Remove introductions and conclusions that add only an announcement or a generic flourish*. |
| "Test suspected filler by what its removal costs; preserve any fact, implication or voice it carries beside the defect" | sound | A way to recognise filler and a limit on removing it. The writer's requirement is `base.md`'s *Each passage earns its place*, with its criteria. |
| "Strong supported criticism needs no generic softening" | sound | Stops a reviewer from softening. `base.md` states the writer's side: *Criticism addresses the supported issue*. |
| The bounding-sentence paragraph ("A sentence can do its work by bounding what the text asserts …") | sound | Says how to recognise a sentence that carries a limit and where a finding may lie. The writer's requirement is the three `base.md` sentences it quotes, which are operable. |
| "Make the smallest correction that removes a finding" and the rest of that paragraph, the claim account included | sound | Correction and reporting. |
| "Compare each correction with its input …" to the end | sound | Checking a correction. |

## `web-craft.md` and `web-craft.review.md`

| Rule | Class | Reason |
| --- | --- | --- |
| "Test the text as a reader who scans, then as one who follows its reasoning. Identify the actual cost of a dense or fragmented passage before proposing a change" | operable-in-base | `web-craft.md`: *paragraphs hold connected thoughts, and varied rhythm supports both scanning and sustained reading*. The review half adds the reading order and a limit on changes. |
| "A Swedish angle expressed in natural English succeeds; Swedish word order in English does not" | operable-in-base | `web-craft.md`: *Think and write wholly in the target language … A native professional should hear a colleague, not a translation.* |
| "flawless local spelling does not rescue generic promotional prose from a lost journalistic purpose" | operable-in-base | `web-craft.md`: *Language choice changes the language surface, not the chosen craft*, with the standards of craft it names. The genre's base half states what is commercial and when. |
| "Preserve successful genre-specific voice and structure instead of standardising them" | sound | Limits correction. |

## `article-anatomy.md` and `article-anatomy.review.md`

| Rule | Class | Reason |
| --- | --- | --- |
| "Read under the anatomy, and word each finding in the strength the statement it rests on has" | sound | How a finding is worded. |
| "A requirement that fails is a finding. Count characters and words before reporting a limit, and give the count" | operable-in-base | `article-anatomy.md`: *Limits are exact; verify each one by counting*, and Write step 7 measures them. |
| The paragraph on absent and present parts ("A part the text does not have is reported, and a part it has is repaired" …), the byline moved into place, the ending's repair and the parts the script reports absent | sound | Says what a review may write and what it reports. The anatomy's base half states the parts, their order and the ending's test, which a writer meets by writing them. |
| "a vague call to action among them" (in the ending's repair) | operable-in-base | `article-anatomy.md`: *the action follows from the article's content. The selected genre says what that action is*, and each of the four genres states its action. |
| "A departure from a *should* is a finding only when following the norm was possible and the text is no better for having left it" and the rest of that paragraph on bands | sound | Limits findings and changes. The strengths are defined in `article-anatomy.md`, and Write step 7 weighs norms by them. |
| "A paragraph holding two thoughts is one, and so is a text whose paragraphs are nearly all a single sentence or nearly all long" | operable-in-base | `article-anatomy.md`: *Each paragraph holds one thought*, *Most paragraphs come to two or three sentences*. |
| "an opening that restarts without advancing is the defect" | operable-in-base | `article-anatomy.md`'s reader test: *A reader who has just read the standfirst meets the lead as new material*. |
| "A pronoun, a definite form or a phrase such as *the reason* whose referent only the standfirst supplies is a finding" | operable-in-base | `article-anatomy.md`: *The lead introduces every person, thing and event it mentions, and nothing in the body points back to the standfirst.* |
| "A byline nobody can name is reported as missing and left unfilled" | sound | A reviewer's author question. The writer's rule is `article-anatomy.md`'s *when it names none, the author is the user*. |

## `headlines.md` and `headlines.review.md`

| Rule | Class | Reason |
| --- | --- | --- |
| "Read the text first and say its angle to yourself in one sentence" and the four questions | operable-in-base | `headlines.md`: *Settle the reader and the angle before wording anything*, and the rules the questions check. |
| "Would the reader feel misled afterwards?" | operable-in-base | `headlines.md`: *A reader who finishes the text finds that the headline told the truth about it.* |
| Claims, figures, names or conclusions not in the text, sharpened or generalised | operable-in-base | `headlines.md`, *Every word supported*: *never sharper, never more general, never a conclusion the text does not draw*. |
| Vague or mysterious wording that requires reading the text | operable-in-base | `headlines.md`: *it is understood on its own* and *It is plain before it is clever*. |
| A subject named with nothing said about it | operable-in-base | `headlines.md`: *A subject alone is a label. Test: the headline could not head a different text on the same subject.* |
| Words, names and abbreviations the audience will not know | operable-in-base | `headlines.md`: *Its words are ones this audience knows.* |
| Partial quotes, colons in place of a verb, headline-speak | operable-in-base | `headlines.md`: *A colon standing in for a verb, a clipped quotation and headline-speak all give way to the full clause.* |
| Puns and references that fail without the allusion | operable-in-base | `headlines.md`: *It works in full for a reader who misses every allusion.* |
| Question headlines, with their two exceptions | operable-in-base | `headlines.md`: *It gives the answer*, with the same two exceptions. |
| A tone more dramatic than the text's | operable-in-base | `headlines.md`: *Its tone is the text's tone, and never louder.* |
| The same words in headline and standfirst, or subheading and first sentence | operable-in-base | `headlines.md`: *say different things in different words*, and Write step 7 reads the heading pairs. |
| A subheading that pre-spends the quotation under it | operable-in-base | `headlines.md`, *A subheading over a quotation*, made operable by #396 with its reader test. |
| "Name what the reader loses, and repair by rewriting the headline alone …" and the report of a changed heading | sound | Correction and reporting. |
| *Leave alone* | sound | Limits findings. |

## `genres/article.md` and `genres/article.review.md`

| Rule | Class | Reason |
| --- | --- | --- |
| "does the lead begin explaining or reporting after the standfirst has introduced the piece, or does the text start twice?" | operable-in-base | `article.md`: *the standfirst introduces the offer, and the lead begins the explanation or reporting*, and `article-anatomy.md`'s reader test. |
| "Where a part of the opening is there but does not do its work, repair it from existing content …; where a part is missing, report it" | sound | Correction. |
| "Topic accumulation" | operable-in-base | `article.md`: *Make the angle clear early and let it govern the material*; `base.md`: *Keep a clear focus*, *unrelated background do not [belong]*. See *The closest calls*. |
| "a concept explained after the reasoning needs it" | operable-in-base | `article.md`: *Explain concepts and connections in the order this reader needs them*; `base.md` says the same. |
| "a sales close unrelated to the explanation" | operable-in-base | `article.md`: *The call to action is the useful next step the explanation supports, and it is commercial only where the assignment and material warrant it.* |
| "a different successful opening does not. Keep relevant technical substance when improving navigation" | sound | Limits findings and correction. |
| "Apply the full form to a complete article, not an explicitly requested excerpt" | operable-in-base | `article.md`: *An explicitly requested excerpt takes only the parts it needs.* |
| "Report a required part the text does not have rather than writing it" | sound | What a review writes. |

## `genres/case-study.md` and `genres/case-study.review.md`

| Rule | Class | Reason |
| --- | --- | --- |
| "Locate whose experience and judgement carry the account" | operable-in-base | `case-study.md`: *The customer's voice carries the experience*, *Let attributed quotations carry the customer's experience and judgement*. |
| "Supplier *we* in narrative … is diagnostic; a speaker using *we* in their own quotation is not" | operable-in-base | `case-study.md`: *Name the supplier in third person in the narrative, while quotations retain their speaker's perspective.* |
| "ungrounded superiority" | operable-in-base | `case-study.md`: *The publisher's interest is not a licence for unsupported praise or a claim of independent reporting.* |
| "a rescue story that makes the customer helpless" | operable-in-base | `case-study.md`: *Keep the customer an acting party*, and the opening's *how they acted*. |
| "Read bridges beside quotations" and "Remove a redundant pre-echo while keeping the attribution and any distinct fact" | handled by #396, not made operable; filed as #438 | #396 made the subheading over a quotation operable in `headlines.md` and defined the quotation bridge there, and left *A bridge should prepare a quotation rather than pre-say it* in `case-study.md` unchanged, so no file Write loads states operably what a bridge may carry. See `docs/evaluation/editorial-396/results.md`. |
| "Read … the standfirst beside the body's opening" | sound | Operable in `article-anatomy.md`'s reader test, which Write loads for this genre. |
| "Check quoted speech for target-language idiom too: a missing referent that makes the reader reconstruct the meaning is a visible problem, not protected merely by quotation marks" | operable-in-base | `quotations.md`: *in idiomatic target-language speech, not source-language syntax. … Make an implicit referent explicit only when the supplied context settles it*; `case-study.md`: *within the quotation policy and the language's conventions*. |
| "Clarify only what the surrounding text settles; otherwise report it" | sound | Limits a correction (the addendum's own example). |
| "A calm account with a qualified customer appraisal can be complete without more drama, quotations or selling" | sound | Limits findings. `case-study.md` states the writer's side: *a qualified judgement is sufficient*, *neither a heading each nor a quota of quotations*. |
| "Check whether stated results and reservations support the narrative's conclusions" | operable-in-base | `case-study.md`: *the supported results with their qualifications*, *A before-and-after result is not by itself evidence of the supplier's effect*; `base.md`, *Claims*. |
| "Preserve the customer's reservations and agency" | sound | Limits correction. The writer's side is in `case-study.md`, as the two lines above say. |
| "A visibly absent appraisal is a gap to report, not satisfaction to infer" | operable-in-base | `case-study.md`: *Where no appraisal or quotable speech is supplied, the gap remains visible and is reported, rather than filled with inferred satisfaction or invented words.* |
| "a plausible quotation is not a gap merely because its interview is unavailable. Resolve only what the text itself supplies" | sound | Limits the review to the text. |

## `genres/column.md` and `genres/column.review.md`

| Rule | Class | Reason |
| --- | --- | --- |
| "Where the connections disappear into generic exposition" | operable-in-base | `column.md`: a perspective opened *through a particular author's observation and thought*, *Begin with a concrete observation … develop the reflection through meaningful connections*. See *The closest calls*. |
| "or the humour becomes a detachable performance" | operable-in-base | `base.md`: *A useful analogy, question, image, fragment or humorous turn can clarify or carry a voice; decoration and manufactured drama cannot*; `column.md`: devices *when they earn their effect*. See *The closest calls*. |
| "An early point or a reasoned opinion is not itself a genre mismatch" | sound | Limits findings; `column.md`: *The point may be visible early*. |
| "Preserve purposeful fragments, rhetorical recurrence, pointed imagery and admitted doubt. A clear heading is not a reason to recast the piece. Change the actual obstruction, not its successful personality" | sound | Limits correction. |
| "Treat an internal contradiction in a personal account as a finding" | operable-in-base | A contradiction the writer introduces changes what the author thinks or has done, which `column.md` forbids (*Ghostwriting develops expression without changing what the author thinks, feels, has done or has experienced*); one the material carries is the review's to report. |
| "An anecdote's provenance cannot be established from prose alone: neither discredit it … nor replace it with an invented memory. Report what cannot be repaired from the text" | sound | Limits the review. `column.md` states the writer's side: *Invent no scene, memory or conversation*. |

## `genres/opinion.md` and `genres/opinion.review.md`

| Rule | Class | Reason |
| --- | --- | --- |
| "Identify the early position, the grounds supporting it and the action the ending leaves with somebody" | operable-in-base | `opinion.md`: *State the thesis early*, *Build a case the reader can follow*, *the ending makes clear who can act*. |
| "If *it is time to act* names no act, look for the existing proposal to make explicit; supply no new policy or decision" | operable-in-base | `opinion.md`: *a generic exhortation alone is not one*. The repair half is sound. |
| "Check factual premises and predictions against the support visible in the text, loaded figures for attribution, and objections for fair treatment" | operable-in-base | `opinion.md`: *Attribute load-bearing factual claims where they are used, and meet relevant real objections fairly*; `base.md`, *Claims*. |
| "Treat a clearly proposed target with its stated uncertainty as an authorial choice" and "A support finding identifies a premise or inferential dependency the argument actually asserts" | sound | Limits findings. |
| "An internal contradiction or broken inference is a finding; external reference checking is outside this review" | operable-in-base | `opinion.md`: *distinguishing evidence, judgement and inference*; `base.md`: *A transition may explain a connection, but cannot invent one*, *A sequence or correlation establishes no cause*. The second half is sound. |
| "Preserve a successful polemic … A pointed closing or rhetorical return is not a defect … Clarify a broken argument without replacing its position" | sound | Limits findings and correction. |

## `genres/press-release.md` and `genres/press-release.review.md`

| Section | Class | Reason |
| --- | --- | --- |
| The opening ("Diagnostics for the requirements … Nothing here is a requirement") | sound | Says what the file is. |
| *The shape* | operable-in-base | `press-release.md` states the order down to the notes and the standing description, that comment carries the judgement and the body the facts, and that a part the material gives nothing for is left out. The *Edge* and correction are review wording. |
| *The first sentence* | operable-in-base | `press-release.md`: *The summary opens with what has happened or will happen, who is doing it, and when*, with the failing openings named. The *Edge* on an undated event follows from `base.md`'s rule on invention. |
| *Printable facts* | operable-in-base | `press-release.md`, *Every fact is in a form that can be printed*, names each form the failures list. |
| *Exclusions* | operable-in-base | `press-release.md`: *Where a reader would reasonably assume something the material rules out … the release says so plainly and once.* |
| *Quotations* | operable-in-base | `press-release.md`: *A quotation is a person saying something only they could say*, *Where the material carries none, none is written*; `quotations.md` for a quotation made from a paraphrase. |
| *Information rather than selling* | operable-in-base | `press-release.md`: *What survives is what the material supports and the recipient can check*; `base.md` on evaluative characterisation. See *The closest calls*. |
| *The close* | operable-in-base | `press-release.md`, *What the release ends with is the material's*: contact with role and a way to reach them, publication time, a standing description that stops. |
| *Length* | operable-in-base | `press-release.md`: *A release is a page and not a document*, with surplus detail going to the notes. |

## `genres/report.md` and `genres/report.review.md`

| Section | Class | Reason |
| --- | --- | --- |
| The opening ("Diagnostics for the requirements … Nothing here is a requirement") | sound | Says what the file is. |
| *The shape* | operable-in-base | `report.md`: an opening fixing what the report covers, what it is for and the period, a summary above the body from about five thousand words or on request, and none below. |
| *The question* | operable-in-base | `report.md`: *it says what it was asked and what it is meant to settle, in the words its reader would use, before it says anything else.* |
| *The answer first* | operable-in-base | `report.md`: the finding stated plainly at the top, and *The rule fixes where the report's own answer to the question stands*. The *Edge* on a report that settles nothing follows from *What the report cannot settle is part of the report* and the recommendation rule's *usable answer*. |
| *Figures* | operable-in-base | `report.md`: *says what it counts, over what period, and where it came from*, estimates and projections labelled, no period quietly extended. |
| *Density, tables and charts* | operable-in-base | `report.md`, *The report is where the figures live*, names each failure: figures described instead of given, comparisons in sentences, a caption, an unintroduced table or chart. |
| *The objection* | operable-in-base | `report.md`: *it appears in the terms its holder would use, at its strongest, and the report then says what the material does and does not do to it.* |
| *Limits* | operable-in-base | `report.md`, *What the report cannot settle is part of the report*; `base.md`: *Preserve chronology, scope and qualifications wherever a claim appears.* |
| *The recommendation* | operable-in-base | `report.md`: *it names the action, who takes it, by when, and what it costs or risks, as far as the material supports each of those.* |
| *Sections* | operable-in-base | `report.md`, *Sections are named for what they hold, and better for what they found*, with the withholding heading, numbering and levels. The *Edge* on a short report without headings limits findings. |
| *Reading a section alone* | operable-in-base | `report.md`, *Every section is read by somebody who arrived at it directly*, names the pronoun, the definite form and *as shown above*. |
| *Register* | operable-in-base | `report.md`, *The sentences are whole ones*: no fragment, no one-word sentence, no sentence opening on a conjunction. The *Edge* on headings, captions and quoted fragments limits findings. |

## `genres/teaser.md` and `genres/teaser.review.md`

| Section | Class | Reason |
| --- | --- | --- |
| The opening ("Diagnostics for the requirements … Nothing here is a requirement") | sound | Says what the file is. |
| "This guidance is for the selected teaser genre, not the informative standfirst within an article or case study" | operable-in-base | `teaser.md`: *An informative article or case-study standfirst belongs to its own genre … and is not automatically a teaser*. |
| *The parts and their order* | operable-in-base | `teaser.md`: the naming line, the pull and the action in that order, written under a naming line the form supplies rather than saying it again, and no action where the form has nowhere for it. |
| *The content declaration* | operable-in-base | `teaser.md`: *from the teaser alone a reader can say what the text on the other side actually holds*, in the source's particulars rather than a field's general terms. The *Edge* that naming what a text settles is not settling it is carried by *the question it settles* and by the arc's *the source has it*. |
| *The promise* | operable-in-base | `teaser.md`: *settles it against what they were led to expect rather than against what was literally said*, and the click-forcing constructions named under *What this genre does not do*. |
| *The arc* | operable-in-base | `teaser.md`: *The arc is the whole of the teaser* and *It does not answer its own complication*; `abt.md` for a question as the turn and an open result as a valid outcome. |
| *The action* | operable-in-base | `teaser.md`: *The action names what the click delivers*, with *read more* and *learn more* named, and *it names something the source actually has*. |
| *Standing alone* | operable-in-base | `teaser.md`: *no pronoun whose antecedent is in the source, no definite form for something nobody has introduced … and no reliance on whatever happens to sit beside it*. |
| *The fixed forms* | operable-in-base | `teaser.md`: *a teaser whose declaration, promise, or action arrives after the cut was not read at all*, with the limit the placement or request names. |
| *The source's voice* | operable-in-base | `teaser.md`: *It does not take a voice the source does not have … it sounds like the source compressed*. |

## `genres/web-copy.md` and `genres/web-copy.review.md`

| Rule | Class | Reason |
| --- | --- | --- |
| "Scan for the reader's task, relevant information and any next-step consequence" | operable-in-base | `web-copy.md`: *Address the reader's actual task with supported benefits or useful information, the conditions that matter and … what happens next.* |
| "Abstract talk about a target audience does not help somebody act; locate the concrete information already present and bring it forward" | operable-in-base | `web-copy.md`: *Address the reader's actual task with supported benefits or useful information*, *Make the page's purpose and relevance apparent early* and *Every word serves that reader*. The repair is sound. |
| "Enter each section cold. Repair a stranded reference or opaque heading with the least context needed" | operable-in-base | `web-copy.md`: *Headings declare their contents; sections remain intelligible to someone entering there directly, with enough local context*. |
| "Useful regrouping of existing information needs no separately specified section in a missing brief. A dimension outside a scale guide is not itself a finding" | sound | Limits findings; `web-copy.md` states the scale guides as guides. |
| "*Book now* contradicts an expression-of-interest form that books nothing; a reference to a form here needs an included or explicitly specified form, not just its link" | operable-in-base | `web-copy.md`: *Name what each link or button actually does …; a linked form is not a form embedded in the page. … Distinguish expressing interest from ordering, paying or booking.* |
| "The stated destination and consequence guide the correction. Unknown conditions or behaviour remain unresolved rather than being invented" | sound | Correction; `web-copy.md`: *Use only supplied destinations, functions and terms*. |
| "Keep a complete information page free of an added sales template or unnecessary CTA" | sound | Limits correction. The writer's side is in `web-copy.md`: *an information page can stop once it answers the question*, buttons *earn their place by their function*. |
| "A service page's successful persuasive language can stay; diagnose an unsupported promise, not the fact that the text persuades" | operable-in-base | `web-copy.md`: *Persuasion rests on what is offered, without invented promises, urgency, guarantees or testimonials.* The first half is sound. |

## `techniques/abt.md` and `techniques/abt.review.md`

| Rule | Class | Reason |
| --- | --- | --- |
| "*we opened an office, but we also hired staff* supplies only an addition" | operable-in-base | `abt.md`: *Let a relevant obstacle, contrast or unanswered question make the next step worth following*, and the relations *must hold even without the words*. |
| "A calm unanswered question can provide the turn" | operable-in-base | `abt.md`: *A question need not be a crisis*. |
| "A fabricated crisis cannot repair a missing relation" | operable-in-base | `abt.md`: *Nothing in that arc requires an emergency*; `base.md`: *manufactured drama cannot*. |
| "Test the connections rather than the presence of three words, equal parts or one global arc. An early result followed by its explanation, or independent useful arcs in web-copy sections, can fully satisfy the selected technique" | sound | Limits findings; `abt.md` states each allowance. |
| "Clarify or move existing content … Keep qualifications in the consequence. If a necessary link or outcome is absent, report that gap … Leave another coherent application alone" | sound | Correction. |

## `techniques/pac.md` and `techniques/pac.review.md`

| Rule | Class | Reason |
| --- | --- | --- |
| "A descriptive premise is sufficient; do not demand a falsifiable thesis or manufacture a counterargument" | sound | Limits findings; `pac.md`: *without a controversial thesis or an invented opposing view*. |
| "For a hypothesis, examine whether the text actually tests it rather than merely restating it" | operable-in-base | `pac.md`: *Testing a hypothesis is one use*, *Analyse their meaning and limits, weighing alternative explanations*, *Draw the conclusion that analysis warrants*. |
| "*Repairs took a third of volunteer time, so doubling opening hours will clear every repair* claims an effect the figures do not establish" | operable-in-base | `pac.md`: *Draw the conclusion that analysis warrants*; `base.md`: *A causal verb … needs causal support*. |
| "Clarify the existing distinction between an observation and its implications; do not add evidence to rescue the conclusion" | sound | Correction; `pac.md` states the writer's side: *Add no new supporting evidence only at the conclusion*. |
| "An answer at the top is not a failure when the subsequent reasoning supports it" | sound | Limits findings; `pac.md`: *A report's opening answer … may precede the detailed analysis*. |
| "Diagnose missing analysis, an unsupported conclusion or a connection the reader cannot follow" | operable-in-base | `pac.md`: the three steps and *Make the reasoning traceable in the genre's own form*. |
| "rather than moving a successful summary or forcing a preferred section pattern. Use existing support; report what the text cannot settle" | sound | Limits correction. |

## The closest calls

These rules were judged operable-in-base, and each was the nearest to review-only in its pair. They are listed so that a later reading can test the judgement rather than repeat it.

- **`article.review.md`, topic accumulation.** `article.md`'s *let it govern the material* is abstract on its own, but `base.md`'s *Keep a clear focus* and *unrelated background do not [belong]* give the writer a question for each passage: does this serve the angle the opening set?
- **`column.review.md`, connections that disappear into generic exposition.** `column.md` says the reflection develops from *a concrete observation the material carries* and is *a particular author's observation and thought*. A writer can ask whether a paragraph still follows from that observation. The review half's own wording is a label for the failure, not a test the base lacks.
- **`column.review.md`, humour as a detachable performance.** *Earn their effect* is abstract, but `base.md` gives the test beside it: a humorous turn *can clarify or carry a voice; decoration and manufactured drama cannot*.
- **`press-release.review.md`, *Information rather than selling*.** The heading *It reads as information rather than as selling* is a contrast of the kind the bridge rule uses. But `press-release.md` follows it with a test a writer can apply to each modifier before writing it: *What survives is what the material supports and the recipient can check*.

## Outside this sweep

`anti-slop.md` has no review half and is not one of the fourteen pairs. It is loaded by the Skills that review and not by Write, and the editorial README says it states no target of its own. Whether every pattern it diagnoses is operable in `base.md` is a separate question, and this sweep did not answer it.
