# Judgement B — case-study-flawed

## 1. Changes

The Skill returned a changed text. Every difference between `work/input.md` and `delivered.md`:

1. Headline — before: *Vår fantastiska lösning räddade Elm Quay*; after: *I Elm Quays försök tog tilldelningen två arbetsdagar*. **Change to what a claim says** (strength and subject: a rescue attributed to the supplier's solution becomes a measured duration scoped to the trial) and the repair of a visible defect.
2. Standfirst, first sentence — before: *Elm Quay registrerade 31 ärenden.*; after: *Under åtta veckor förde Elm Quay anteckningar om ett försök med programvara: 31 registrerade ärenden, akuta undantagna, och en jämförelse med hur lång tid det tog tidigare.* **Repair of a visible defect** (the standfirst carried the same sentence twice) and a **change of scope**: the figure is now bounded by *åtta veckor* and *akuta undantagna*, as the body always had it.
3. Standfirst, second sentence — before: *Elm Quay registrerade 31 ärenden.* (the duplicate); after: *Arbetsledaren Maya Lind berättar vad hon skulle göra annorlunda nästa gång.* **Repair of a visible defect**; the replacement claim is carried by the quotation in section 1.
4. Lead, first sentence — before: *Elm Quay registrerade 31 ärenden.*; after: *Ett åtta veckor långt försök hos Elm Quay ligger bakom det här kundcaset.* **Repair of a visible defect** (the lead opened by repeating the standfirst verbatim).
5. Lead, second sentence — before: *Vi på Svale är världsledande på att skapa framgång, och kunden stod hjälplös innan vi kom.*; after: *Företaget prövade programvara från leverantören Svale och förde egna anteckningar, som är noga med vad de inte kan avgöra.* **Change to what a claim says**: two unsupported claims (supplier supremacy; a helpless customer) are removed and replaced with claims the text carries.
6. Subheading 1 — before: *Kunden fick en gemensam bild*; after: *Arbetsledaren efterlyser en längre upptakt*. **Change to what a claim says** (strength: an achieved result becomes the speaker's reservation) and the repair of a visible defect.
7. Paragraph removed — before: *Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.*; after: nothing. **Repair of a visible defect** (it said the quotation below it in advance); the same claim with the same attribution survives inside the quotation.
8. Quotation attribution — before: *säger Maya Lind, arbetsledare hos kunden*; after: *säger Maya Lind, arbetsledare på Elm Quay*. **Change to what a claim says** in subject only — same person, same employer, named rather than referred to. The speaker's own words are untouched.
9. Subheading 2 — before: *Resultatet bevisar allt*; after: *Siffrorna säger inte varför tilldelningen gick fortare*. **Change to what a claim says** (a proof becomes the limit the note itself states) and the repair of a visible defect.
10. Body attribution — before: *Enligt kundens försöksanteckning*; after: *Enligt Elm Quays försöksanteckning*. **Change to what a claim says** in subject only; the attribution is the same.
11. Body, final sentence removed — before: *Vår programvara orsakade därför hela förbättringen.*; after: nothing. **Repair of a visible defect**: it contradicted the sentence immediately before it, which says the difference cannot be attributed to the software.

Unchanged: *– Jag skulle välja att göra försöket igen, säger Lind.* and *Kundcaset publiceras av leverantören Svale.* No mechanical corrections were made; none were needed.

## 2. Headings

### Input

- `# Vår fantastiska lösning räddade Elm Quay` — **statement**, **overclaim** (the body says *skillnaden inte kan tillskrivas programvaran*; nothing in the text supports a rescue or a *fantastisk* solution).
- `## Kunden fick en gemensam bild` — **statement**, **echo** (repeats *en gemensam bild av ärendena* from the first sentence under it), **overclaim** (the text has only Lind saying such a view helps, not that the customer obtained one).
- `## Resultatet bevisar allt` — **statement**, **overclaim** (the note in the section below expressly declines to attribute the difference).

### Delivered

- `# I Elm Quays försök tog tilldelningen två arbetsdagar` — **statement**. No echo: the standfirst names a comparison, not the figure. No overclaim: the body carries *Tiden till tilldelning var två arbetsdagar jämfört med tre tidigare*, and the headline scopes it to the trial.
- `## Arbetsledaren efterlyser en längre upptakt` — **statement**. No echo: it summarises rather than repeats *jag skulle lägga till en vecka för förberedelser*. No overclaim; the claim stands at the strength the quotation gives it.
- `## Siffrorna säger inte varför tilldelningen gick fortare` — **statement**. No echo of the first sentence under it. No overclaim: it states the limit the note states.

## 3. Against the expectation

- *Detect first-person supplier praise/rescue* — **detected and repaired**. *Vi på Svale är världsledande på att skapa framgång* and *kunden stod hjälplös innan vi kom* are gone from the lead, and the same voice is gone from the headline.
- *Detect pre-echoed quote* — **detected and repaired**. *Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.* is removed; the reply reports the removal and notes the claim survives in the quotation.
- *Detect duplicate standfirst/lead* — **detected and repaired in part**. The script measured the input's departure as `norms: [{"part": "lead", "measured": "both open on “elm”"}]`; `anatomy-delivered.json` reports `"norms": []`. The reply's finding 4 reports a residual overlap between the new standfirst and the new lead as unresolved.
- *Detect causal contradiction* — **detected and repaired**. *Vår programvara orsakade därför hela förbättringen.* is removed and the removal is reported with the contradiction named.
- *No byline, reported as missing and left unfilled* — **detected and correctly left unfilled**. `anatomy-delivered.json` still gives `"failures": [{"part": "byline", "measured": "absent"}]`, and the reply's finding 1 quotes `byline: absent`, states that nothing names an author, and declines to fill it.
- *Two subheadings, neither describing its section, the second claiming a conclusion the note declines* — **detected and repaired**; see the marked lists above. The repairs are **not reported** in the reply's account of what it changed.
- *No ending section or call to action; report rather than invent* — **detected and reported**, finding 2, which names the absence of any offer, link or contact route as the reason it cannot be written. It remains absent in `delivered.md`.
- *Keep the customer's reservation and factual measures* — **preserved**. *men jag skulle lägga till en vecka för förberedelser* is verbatim, as are *31 ärenden*, *åtta veckor*, *akuta ärenden undantagna*, *två arbetsdagar jämfört med tre tidigare* and *arbetsbelastningen var olika och att skillnaden inte kan tillskrivas programvaran*.
- *Report unavailable support* — **reported**. Findings 1–3 name the byline, the call to action and the missing customer background as unrepairable without material the Skill does not have.
- No finding was made that the expectation rejects: nothing was invented, no measure was dropped, and the reservation was not softened.

## 4. Criteria

### G1 — pass

The case-study does its job for a reader weighing a supplier's software. The reader learns what was measured and over how long (*Enligt Elm Quays försöksanteckning registrerades 31 ärenden under åtta veckor, med akuta ärenden undantagna*), what changed (*Tiden till tilldelning var två arbetsdagar jämfört med tre tidigare*), what the measurement cannot settle (*skillnaden inte kan tillskrivas programvaran*), what the customer would change (*jag skulle lägga till en vecka för förberedelser*), and who publishes the piece (*Kundcaset publiceras av leverantören Svale.*). The angle — what the trial showed and what it cannot say — is recognisable from headline to last section, and the craft of the genre is present: attribution to a named source, verbatim quotation, disclosed publisher stance. The input's angle was a supplier boast the material contradicted; the returned text's angle is one the material supports.

### G2 — pass

On the script's figures the returned text carries headline (`"characters": 52`), standfirst (`"words": 38`, `"paragraphs": 1`), lead (`"words": 32`, `"paragraphs": 1`) and two sections (`"paragraphs"` of 1 and 3), in the anatomy's order, with `"byline": null`. Each present part does its own job: the headline states the angle without claiming more than the body; the standfirst stands alone, covering scope, figures, caveat and the human element; the lead begins the work and precedes the first H2; both subheadings state the angle of the section they head and are understood on their own; the body explains. For the case genre, the results and the customer's own appraisal are present and the publisher stance is truthful.

Two parts are absent from `delivered.md`. The byline fails the anatomy on the script's count (`"failures": [{"part": "byline", "measured": "absent"}]`), but this criterion states that a Redline run on a text whose author nobody names reports the byline missing and leaves it unfilled, which is what the reply does. The ending's call to action, and the customer's situation and course of action, are likewise missing; the reply reports both (findings 2 and 3) as findings that cannot be repaired without material the Skill does not have — the text supplies no offer, link or contact route and no background. The detection and reporting of all three are scored under R1.

### P1 — pass

The reasoning is followable end to end and the conclusions are now proportionate to the visible support. The lead frames a trial with notes *som är noga med vad de inte kan avgöra*; the final section gives the figures and then the limit in the same paragraph, and stops there. The input's *Vår programvara orsakade därför hela förbättringen.* drew a conclusion the sentence before it denied; with it gone, the reader is not asked to accept anything the note does not carry. The technical substance survives intact: the sample (31 ärenden), the window (åtta veckor), the exclusion (akuta ärenden undantagna), the before-and-after (två arbetsdagar jämfört med tre) and the confound (arbetsbelastningen var olika). No concept is used before it is introduced.

### W1 — pass

A web reader can orient and enter. Counted requirements all hold on the script's figures: headline 52 characters and 8 words, standfirst 38 words in 1 paragraph, lead 32 words in 1 paragraph, subheadings of 42 and 54 characters, and every section with at least one paragraph (1 and 3). No *should* is departed from: `anatomy-delivered.json` reports `"norms": []`, where the input's measurement reported the standfirst and lead as *both open on "elm"* — the returned text opens them on *Under* and *Ett*. The longest measured paragraph is 37 words, far inside the 80-word norm, and no section exceeds three paragraphs. The standfirst is covered by the body, and the two are complementary rather than duplicate.

The *most* figures fall short read across the whole text — `"paragraphs": 6` with `"paragraphs_of_two_or_three_sentences": 3`, and `"sections": 2` with `"sections_of_two_or_three_paragraphs": 1` — but this is typicality, not a requirement, and it never fails a single paragraph or section: three of the six paragraphs are the two quotations and the one-sentence publisher stance, whose content dictates a single sentence. The one real reader bump is the first section, which is now a subheading and a bare quotation with no bridge into it; the reply's finding 5 reports this as a remaining problem it cannot repair, since any bridge would have to say what *en gemensam bild* refers to and the text does not say. It is a small loss of continuity in a text that otherwise reads straight through, and the detection is scored under R1.

### L1 — pass

The Swedish reads as Swedish written by a professional, not as translated English. *Ett åtta veckor långt försök hos Elm Quay ligger bakom det här kundcaset* uses native word order and the idiomatic *ligger bakom*; *Arbetsledaren efterlyser en längre upptakt* and *Siffrorna säger inte varför tilldelningen gick fortare* are compact native constructions rather than calques. *förde egna anteckningar, som är noga med vad de inte kan avgöra* gives the notes an agency that is ordinary in Swedish reporting. The genitive *Elm Quays* is formed correctly against a foreign proper noun, and *tilldelning*, *arbetsledare* and *försöksanteckning* are the right register for the domain. Nothing imports English syntax.

### L2 — pass

Swedish locale mechanics govern throughout. Quotations are set with the Swedish speech dash (*– Att ha en gemensam bild…*) and closed with the *säger*-clause in Swedish order. The headline is in sentence case, as Swedish practice requires. Numerals follow the convention that low counts are spelled out and larger ones are not: *två arbetsdagar*, *tre tidigare*, *åtta veckor*, *en vecka* against *31 ärenden*. No date, currency or conversion appears anywhere in the returned text, and none was invented: every figure in `delivered.md` is a figure the input carried. Spelling and punctuation are standard Swedish throughout.

## 5. R1 — fail

**What it got right.** Every defect the expectation names as visible was found and handled. The supplier's first person and its rescue framing are gone from both the lead and the headline; the pre-echoing paragraph is gone; the standfirst's duplicated sentence is gone and the script now reports `"norms": []` where it reported the standfirst and lead *both open on "elm"*; the contradicting causal sentence is gone. The three anatomy defects are handled as the criterion requires: the byline is reported missing (quoting `byline: absent`) and left unfilled, the two subheadings are replaced with subheadings that state their sections, and the missing call to action is reported rather than invented. Preservation is exact: both quotations keep their wording, including the customer's reservation, and every factual measure and every limiting clause stands. No unavailable source was verified, no fact was introduced, and the text was not rewritten to taste — the changes all sit on identified defects.

**Removals and changed claims, against the Skill's own account.**

- *Vi på Svale är världsledande på att skapa framgång* — removed; **reported accurately**, with the finding named.
- *kunden stod hjälplös innan vi kom* — removed; **reported accurately**.
- *Vår programvara orsakade därför hela förbättringen.* — removed; **reported accurately**, and the account correctly states that the text now draws no conclusion about the cause.
- *Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.* — removed; **reported accurately**, including that the claim survives in the quotation.
- *Elm Quay registrerade 31 ärenden* in the standfirst → *31 registrerade ärenden, akuta undantagna* — **reported accurately** as a narrowing of scope.
- *kundens försöksanteckning* → *Elm Quays försöksanteckning* — **reported accurately**.
- *arbetsledare hos kunden* → *arbetsledare på Elm Quay* — **reported accurately**.
- *Vår fantastiska lösning räddade Elm Quay* → *I Elm Quays försök tog tilldelningen två arbetsdagar* — **not reported**. The most prominent unsupported claim in the text was removed and replaced, and the account's list of removed and changed claims does not contain it. The nearest entries tie the supplier-voice finding to the lead alone (*fyndet att leadet talade i leverantörens vi*).
- *Kunden fick en gemensam bild* → *Arbetsledaren efterlyser en längre upptakt* — **not reported**.
- *Resultatet bevisar allt* → *Siffrorna säger inte varför tilldelningen gick fortare* — **not reported**, although the replaced heading asserted the very conclusion the note declines to draw.

**Why this fails.** The criterion requires that every before/after claim be compared and that legitimate removals be reported. Three claim changes, one of them the text's headline, are absent from the account, and the account's own tally — *Korrigeringsrundan tog bort fyra påståenden och flyttade tre* — excludes them, so a reader comparing the two texts is told a smaller and different story than the diff shows. The account also carries a dangling cross-reference: finding 5 sends the reader to *fynd 6 nedan*, and no finding 6 exists in the reply. The repairs themselves were right and the unresolved findings were reported honestly; the reporting of what was resolved is materially incomplete, and that is the criterion's own requirement.

**Visible defects not addressed.** None beyond those the reply reports as unresolved. The residual standfirst/lead overlap (finding 4), the quotation-only first section (finding 5), the missing byline (finding 1), the missing call to action (finding 2) and the missing customer background (finding 3) all remain in `delivered.md`; findings 1–3 could not be repaired without material the Skill does not have, and 4 and 5 remain because the correction budget was spent.

**Findings the expectation rejects.** None. Nothing was invented, the reservation and the factual measures were kept, and the unavailable support was reported rather than filled in.
