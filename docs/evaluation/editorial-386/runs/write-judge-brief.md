# Write judge brief

You judge one run of a writing Skill. The Skill takes a brief with source material, writes one first draft, has a fresh checker compare the draft with the material, validates each report, repairs supported defects, and either delivers the draft or stops without delivering.

## What you read

The message that sent you here names a run directory and says whether you write `judgement-a.md` or `judgement-b.md`. Read exactly these files inside that directory:

- `work/source.md` — the brief and all the material the Skill was supplied.
- `response.md` — the complete reply the user received, the delivery account among it.
- `delivered.md` — the delivered draft, as the evaluator extracted it from that reply. Where it is absent, the run stopped without delivering and `last-draft.md` holds the last draft the run produced; judge that instead and mark it not delivered.
- `anatomy-delivered.json`, or `anatomy-last-draft.json` for a stopped run — a measuring script's output on that text.
- every file under `evidence/`, where the run kept any: drafts, checker reports and the writer's dispositions.

Read nothing else — no repository, no corpus, no other run, no file another judge wrote. You are not told how the Skill or the run was configured, which model ran it, or what anybody expected of it, and you must not guess. A checker's or the writer's own approval is an argument to weigh, never evidence. Judge from `work/source.md` yourself.

## The counts are the script's

The JSON file is a script's measurement of the text you judge. It carries `conforms`, `failures`, `norms`, `typical` and `parts`. Quote its figures as the evidence for every counted line below. Count no characters, words, sentences, paragraphs or sections yourself, and where a count you need is not in that file, say it is not measured rather than producing one.

## The anatomy and the headlines

Two of the criteria below — `G2` and `W1` — rest on a fixed skeleton the genres `article`, `case-study`, `column` and `opinion` carry. Its statements have three strengths, quoted from the reference the Skill writes under:

- A plain statement is a requirement: it holds in every conforming text.
- *Should* marks a norm: follow it as a requirement, and depart only when following it is impossible or the departure is clearly better for the reader.
- *Most* states what is typical across the whole text; each single paragraph or section follows its own content.

Respect them exactly as written:

- A requirement fails on a count, and the count is the script's.
- A departure from a *should* is a failure only where following the norm was possible and the text is no better for having left it.
- *Most* is read across the whole text and never fails a single paragraph or a single section.

Then quote every heading in the text you judge — the level-1 headline and each level-2 subheading — one to a line, and mark each with every label that fits, or `none`:

- **statement** or **label** — a clause that says what the text says, or a plain name for what the text holds. For a subheading, the text is its own section.
- **colon** — a colon standing in for a verb.
- **question** — a question headline.
- **echo** — it repeats the words or the phrasing of the standfirst, or, for a subheading, of the first sentence under it.
- **overclaim** — a figure, name, claim or conclusion in it that the text does not carry, or carries at a lower strength.

The marks are evidence for `G2` and `W1`. They are not verdicts on their own.

## Criteria, from the evaluation corpus

Score each applicable criterion `pass`, `fail` or `skipped` with an observable passage or trace event. In the four article genres, a counted requirement of the anatomy — a 20–70-character headline, a standfirst of at most 60 words, a subheading of at most 70 characters, at least one paragraph in a section, one paragraph each for standfirst and lead — is established by counting, and a count that falls outside it is the failure. Everywhere else the older reading holds: a quantitative measurement supports judgement and never makes a failure on its own. That is the whole of the scale for `web-copy`, and it is how every *should* and *most* statement is read. Distinguish **contract rejection** from **qualitative concern** and **method limit**. Several very different successful texts can pass. Never score exact wording, newspaper names in output, similarity to an example, or preference for one valid editorial solution.

| ID | Question and evidence | Applies |
|---|---|---|
| F1 | Does every assertion, quotation, attribution and implication stay within the supplied material, including uncertainty, chronology, causal limits and author perspective? Cite any unsupported addition or dropped caveat. Count-size judgements need a supplied comparison. | Write, source-aware evaluator only |
| G1 | Does the chosen genre do its job for the named reader, keep a recognisable angle and carry the appropriate journalistic or copy/UX craft? Cite what the reader learns, sees, considers or can do. | Both |
| G2 | Do the required parts perform distinct useful jobs? Each of the four article genres carries the anatomy's parts in its order — headline, standfirst, byline, lead, sections, an ending that calls the reader to action — and each part does its own job: a headline and subheadings that state the angle of what they head and are understood on their own without claiming more than the text claims or repeating the standfirst or the first sentence under them, a standfirst that stands alone, a lead that begins the work and comes before the first H2, an explanatory body, an ending that shows the lead's expectation met. The byline names the author the brief names, or the invoking user where the brief names none, which a Write run states in its delivery account; a Redline run on a text whose author nobody names reports the byline as missing and leaves it unfilled. Article: explanatory body, and a call to action that is the useful next step the explanation supports, commercial only where the assignment warrants. Case: customer situation/action/results/appraisal, truthful publisher stance, and a call to action built from supplied offers, links or contact routes. Column: personal reflection, not compulsory anecdote or campaign, and a call to action that grows out of the reflection and may stand beside honest uncertainty. Opinion: early position, support, relevant real objection, and the change or stance as the call to action, with an identifiable actor. Web-copy: useful information/choice, conditions and accurate next-step consequence where applicable. | Both; excerpt control exempts full article form |
| P1 | Can this reader follow the reasoning, with unfamiliar concepts introduced before use, real transitions and conclusions proportionate to visible support? Does useful technical substance remain? | Both; Redline uses text alone |
| W1 | Can a web reader orient and enter the text without losing its continuous explanation or voice? Are paragraphs coherent with useful rhythm, headings informative where the genre needs them, and standfirst and lead complementary — the body complete when the standfirst is covered, and the two opening on different first words? Identify actual reader loss for density or fragmentation. In the four article genres a requirement is judged by counting; a departure from a *should* — a paragraph over 80 words, a section over three paragraphs, a heading level below the second, a headline past eight words or 60 characters, a standfirst and a lead opening on the same first word — is a failure only where following the norm was possible and the text is no better for having left it; *most* — two or three sentences to a paragraph, two or three paragraphs to a section — is read across the whole text and never against one paragraph or one section. For `web-copy` the scale stays advisory. | Both |
| L1 | Does the prose sound professionally written in the resolved language, with native idiom and syntax, without importing Swedish phrasing into English or generic translated English into Swedish? Separate this from locale mechanics. | Both |
| L2 | Does the resolved locale govern spelling, punctuation and number/date/currency forms? Established variation is preserved; do not invent a new factual date or currency conversion. | Both, particularly final Proofread |

The protocol's five unconditional rejections remain: unsupported facts, wrong locale, substantive mechanical editing, unresolved mandatory findings not reported, and incorrect side effects. A reported irreparable finding satisfies reporting, but its text is still labelled as having a remaining quality problem. Hidden invention in a source-blind control cannot fairly be required of Redline; visible contradictions can.

## What to write

Write your file in the run directory, with these sections:

1. **Outcome** — delivered or stopped, and whether the delivered prose is identical to the last prose a checker saw. Compare the delivered text with the last draft under `evidence/` and read the dispositions for repairs made after the last comparison.
2. **Headings** — the marked list above.
3. **F1** — `pass` or `fail`, citing every unsupported addition, changed term, changed subject, scope, date, modality or certainty, dropped caveat, invented event or personal attribute. Check a translated term in both directions: could something fall under the draft's term and not the source's, or the reverse, in this context? Keep unknown apart from absent.
4. **G1**, **G2**, **P1**, **W1**, **L1**, **L2** — one section each, `pass` or `fail`, with the passage quoted and the reader effect named. Every counted line quotes the script's figure.
5. **Remaining findings** — quote each finding the reply's delivery account reports as remaining, with the passage and the proposed repair. A finding the account names is still a defect of the text; say under `F1` whether it is one.

Reply in at most 120 words: the outcome, the seven verdicts, and the path of the file you wrote.
