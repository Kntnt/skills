# Redline pair judge brief

You judge one run of a reviewing Skill. The Skill received one text and nothing else: it never saw the material the text was written from. It reviews, corrects within a budget, and returns the text with an account of what it changed, what it left and what it could not repair.

## What you read

The message that sent you here names a row directory and says whether you write `redline/judgement-a.md` or `redline/judgement-b.md`. Read exactly these files inside that row directory:

- `redline/work/input.md` — the text the Skill received.
- `redline/response.md` — the complete reply the user received: the returned text and the account.
- `redline/delivered.md` — the returned text, as the evaluator extracted it from that reply. Where the Skill changed nothing, this is a byte copy of the input.
- `redline/anatomy-input.json` and `redline/anatomy-delivered.json` — a measuring script's output on those two texts.
- `write/work/source.md` — the material the input was originally written from. **The Skill did not have this file, and you have it only for the *Source loss* section below.** Nothing in it bears on any criterion, because the Skill could not know it.

Read nothing else — no repository, no corpus, no other run, no file another judge wrote. You are not told how the Skill or the run was configured, which model ran it, or what anybody expected of it, and you must not guess.

## The counts are the script's

The two JSON files are a script's measurement of the input and of the returned text. Each carries `conforms`, `failures`, `norms`, `typical` and `parts`. Quote their figures as the evidence for every counted line below. Count no characters, words, sentences, paragraphs or sections yourself, and where a count you need is not in those files, say it is not measured rather than producing one.

## The anatomy and the headlines

Three of the criteria below — `G2`, `W1` and `R1` — rest on a fixed skeleton the genres `article`, `case-study`, `column` and `opinion` carry. The text's own metadata says which genre it is in.

**Where the genre is `web-copy`, that skeleton does not apply to it at all.** The script's figures are then description rather than requirement, no count makes a failure on its own, and `G2`, `W1` and `R1` are judged on their own words and on the `Web-copy` clause inside them. Say in each of those sections that the scale is advisory for this genre. A finding the Skill made against a counted limit on such a text is a finding against an advisory scale, and whether it is a wrong finding turns on whether the text was worse for the reader as it stood. Everything else in this brief holds unchanged.

Where the genre is one of the four, the skeleton's statements have three strengths, quoted from the reference the Skill reviews under:

- A plain statement is a requirement: it holds in every conforming text.
- *Should* marks a norm: follow it as a requirement, and depart only when following it is impossible or the departure is clearly better for the reader.
- *Most* states what is typical across the whole text; each single paragraph or section follows its own content.

Respect them exactly as written:

- A requirement fails on a count, and the count is the script's.
- A departure from a *should* is a failure only where following the norm was possible and the text is no better for having left it.
- *Most* is read across the whole text and never fails a single paragraph or a single section.

A finding the Skill made against a requirement the text meets on the script's figures is a wrong finding. A finding it made against a *should* the text had good reason to leave, or against a *most* read at one paragraph or one section, is a wrong finding too.

Then quote every heading in the input and every heading in the returned text — the level-1 headline and each level-2 subheading — one to a line, and mark each with every label that fits, or `none`:

- **statement** or **label** — a clause that says what the text says, or a plain name for what the text holds. For a subheading, the text is its own section.
- **colon** — a colon standing in for a verb.
- **question** — a question headline.
- **echo** — it repeats the words or the phrasing of the standfirst, or, for a subheading, of the first sentence under it.
- **overclaim** — a figure, name, claim or conclusion in it that the text does not carry, or carries at a lower strength.

The marks are evidence for `G2`, `W1` and `R1`. They are not verdicts on their own.

## Criteria, from the evaluation corpus

Score each applicable criterion `pass`, `fail` or `skipped` with an observable passage or trace event. In the four article genres, a counted requirement of the anatomy — a 20–70-character headline, a standfirst of at most 60 words, a subheading of at most 70 characters, at least one paragraph in a section, one paragraph each for standfirst and lead — is established by counting, and a count that falls outside it is the failure. Everywhere else the older reading holds: a quantitative measurement supports judgement and never makes a failure on its own. That is the whole of the scale for `web-copy`, and it is how every *should* and *most* statement is read. Distinguish **contract rejection** from **qualitative concern** and **method limit**. Several very different successful texts can pass. Never score exact wording, newspaper names in output, similarity to an example, or preference for one valid editorial solution.

| ID | Question and evidence | Applies |
|---|---|---|
| G1 | Does the chosen genre do its job for the named reader, keep a recognisable angle and carry the appropriate journalistic or copy/UX craft? Cite what the reader learns, sees, considers or can do. | Both |
| G2 | Do the required parts perform distinct useful jobs? Each of the four article genres carries the anatomy's parts in its order — headline, standfirst, byline, lead, sections, an ending that calls the reader to action — and each part does its own job: a headline and subheadings that state the angle of what they head and are understood on their own without claiming more than the text claims or repeating the standfirst or the first sentence under them, a standfirst that stands alone, a lead that begins the work and comes before the first H2, an explanatory body, an ending that shows the lead's expectation met. The byline names the author the brief names, or the invoking user where the brief names none, which a Write run states in its delivery account; a Redline run on a text whose author nobody names reports the byline as missing and leaves it unfilled. Article: explanatory body, and a call to action that is the useful next step the explanation supports, commercial only where the assignment warrants. Case: customer situation/action/results/appraisal, truthful publisher stance, and a call to action built from supplied offers, links or contact routes. Column: personal reflection, not compulsory anecdote or campaign, and a call to action that grows out of the reflection and may stand beside honest uncertainty. Opinion: early position, support, relevant real objection, and the change or stance as the call to action, with an identifiable actor. Web-copy: useful information/choice, conditions and accurate next-step consequence where applicable. | Both; excerpt control exempts full article form |
| P1 | Can this reader follow the reasoning, with unfamiliar concepts introduced before use, real transitions and conclusions proportionate to visible support? Does useful technical substance remain? | Both; Redline uses text alone |
| W1 | Can a web reader orient and enter the text without losing its continuous explanation or voice? Are paragraphs coherent with useful rhythm, headings informative where the genre needs them, and standfirst and lead complementary — the body complete when the standfirst is covered, and the two opening on different first words? Identify actual reader loss for density or fragmentation. In the four article genres a requirement is judged by counting; a departure from a *should* — a paragraph over 80 words, a section over three paragraphs, a heading level below the second, a headline past eight words or 60 characters, a standfirst and a lead opening on the same first word — is a failure only where following the norm was possible and the text is no better for having left it; *most* — two or three sentences to a paragraph, two or three paragraphs to a section — is read across the whole text and never against one paragraph or one section. For `web-copy` the scale stays advisory. | Both |
| L1 | Does the prose sound professionally written in the resolved language, with native idiom and syntax, without importing Swedish phrasing into English or generic translated English into Swedish? Separate this from locale mechanics. | Both |
| L2 | Does the resolved locale govern spelling, punctuation and number/date/currency forms? Established variation is preserved; do not invent a new factual date or currency conversion. | Both, particularly final Proofread |
| T2 | When ABT is selected, do situation, genuine question/complication and supported response relate without invented crisis or triumph? When PAC is selected, does factual starting point/question lead through analysis to warranted conclusion? Early answer and section-level use can succeed. | Explicit technique cases and baseline |
| R1 | Does Redline address concrete visible defects while preserving working voice, arguments, quotations and claims outside findings? Compare every before/after claim; report legitimate removals, rejected losses and irreparable findings. A clean text is not rewritten to satisfy taste, a *most* count read against a single paragraph or section, or a *should* the text had good reason to leave; a failed anatomy requirement is a legitimate finding, and repairing it is not a rewrite. No unavailable-source verification. | Redline only |

The protocol's five unconditional rejections remain: unsupported facts, wrong locale, substantive mechanical editing, unresolved mandatory findings not reported, and incorrect side effects. A reported irreparable finding satisfies reporting, but its text is still labelled as having a remaining quality problem. Hidden invention in a source-blind control cannot fairly be required of Redline; visible contradictions can.

`G1`, `G2`, `P1`, `W1`, `L1` and `L2` are judged on the returned text in `redline/delivered.md`. A problem that remains there is a problem of that text even where the Skill reported it; where the reply reports it as a finding that could not be repaired without material the Skill does not have, say so in the evidence sentence, and score the detection and the reporting under `R1` instead.

`T2` is judged only where the returned text's own `kntnt` metadata or the reply names a technique that was selected. Where none was, write `T2 — skipped — no technique is named in the text's metadata or in the reply` and judge nothing under it. Do not infer a technique from the shape of the prose.

## What to write

Write your file in the row directory's `redline/`, with these sections:

1. **Changes** — every difference between `redline/work/input.md` and `redline/delivered.md`, one line each: before, after, and whether it is a mechanical correction, the repair of a visible defect, a change of taste, or a change to what a claim says — its strength, subject, scope or modality. Write `none` where the Skill returned the text unchanged.
2. **Headings** — the two marked lists above.
3. **G1**, **G2**, **P1**, **W1**, **L1**, **L2** — one section each on the returned text, `pass` or `fail`, with the passage quoted and the reader effect named. Every counted line quotes the script's figure.
4. **T2** — as the paragraph above says: a verdict where a technique was selected, `skipped` with that reason where none was.
5. **R1** — `pass` or `fail`. For every removal and every changed claim, say whether the Skill's own account reports it and reports it accurately. Name every visible defect the Skill did not address, and every change of taste it made to a passage that already worked.
6. **Source loss**, separately and no part of any criterion above, since the Skill could not know it: did any change remove or alter something `write/work/source.md` required — a stated caveat, a careful formulation of what is and is not claimed, a named limit? Quote the source passage and the change.

Reply in at most 150 words: the verdicts, the answer to question 6, and the path of the file you wrote.
