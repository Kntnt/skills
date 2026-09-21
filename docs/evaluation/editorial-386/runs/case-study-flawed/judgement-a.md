# Judgement A — case-study-flawed

The run changed the text.

## 1. Changes

Every difference between `work/input.md` and `delivered.md`:

1. Headline `# Vår fantastiska lösning räddade Elm Quay` → `# I Elm Quays försök tog tilldelningen två arbetsdagar`. **Repair of a visible defect and a change to what a claim says** — strength and subject both: a supplier-voice rescue claim the text carries nowhere is replaced by the measured assignment time the body does carry.
2. Standfirst `**Elm Quay registrerade 31 ärenden. Elm Quay registrerade 31 ärenden.**` → `**Under åtta veckor förde Elm Quay anteckningar om ett försök med programvara: 31 registrerade ärenden, akuta undantagna, och en jämförelse med hur lång tid det tog tidigare. Arbetsledaren Maya Lind berättar vad hon skulle göra annorlunda nästa gång.**` **Repair of a visible defect** (the sentence was printed twice) **plus a change of scope**: the figure 31 now carries the exclusion `akuta undantagna` and the eight-week window, which the bare original did not.
3. Lead `Elm Quay registrerade 31 ärenden. Vi på Svale är världsledande på att skapa framgång, och kunden stod hjälplös innan vi kom.` → `Ett åtta veckor långt försök hos Elm Quay ligger bakom det här kundcaset. Företaget prövade programvara från leverantören Svale och förde egna anteckningar, som är noga med vad de inte kan avgöra.` **Repair of a visible defect and removal of two claims** — first-person supplier superiority and the customer's helplessness, neither supported anywhere in the text.
4. Subheading `## Kunden fick en gemensam bild` → `## Arbetsledaren efterlyser en längre upptakt`. **Repair of a visible defect and a change to what a claim says**: the original asserted as fact what only the quote's speaker says helps, and it pre-said the sentence beneath it.
5. Paragraph `Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.` deleted. **Repair of a visible defect** — it said the quote below it in advance. The claim survives in the quote with the same attribution.
6. Quote attribution `säger Maya Lind, arbetsledare hos kunden` → `säger Maya Lind, arbetsledare på Elm Quay`. **Change to a claim's subject naming**, inside a quotation's attribution tag; same person, same employer, named rather than referred to. The quoted words themselves are untouched.
7. Subheading `## Resultatet bevisar allt` → `## Siffrorna säger inte varför tilldelningen gick fortare`. **Repair of a visible defect and a reversal of what the claim says**: the original claimed the conclusion the section's own note declines to draw; the replacement states the note's limit.
8. `Enligt kundens försöksanteckning` → `Enligt Elm Quays försöksanteckning`. **Change to a claim's subject naming**; same source, named.
9. Sentence `Vår programvara orsakade därför hela förbättringen.` deleted. **Repair of a visible defect and removal of a claim** — it contradicted the sentence immediately before it, which says the difference cannot be attributed to the software.

Unchanged and preserved: both quotations' wording, including Lind's reservation `men jag skulle lägga till en vecka för förberedelser`; the measures `31 ärenden`, `åtta veckor`, `med akuta ärenden undantagna`, `två arbetsdagar jämfört med tre tidigare`; the note's own disclaimer `Anteckningen säger att arbetsbelastningen var olika och att skillnaden inte kan tillskrivas programvaran.`; the publisher line `Kundcaset publiceras av leverantören Svale.` No byline was added.

No mechanical correction was made, and the reply states the closing mechanical pass found none to make.

## 2. Headings

**Input**

- `# Vår fantastiska lösning räddade Elm Quay` — **statement**, **overclaim** (the text's own note says the difference cannot be attributed to the software; *fantastiska* and *räddade* are carried nowhere)
- `## Kunden fick en gemensam bild` — **statement**, **echo** (repeats *en gemensam bild* from the first sentence under it), **overclaim** (asserts as fact what the section only has a speaker saying helps)
- `## Resultatet bevisar allt` — **statement**, **overclaim** (claims proof of everything where its own section declines the attribution)

**Returned text**

- `# I Elm Quays försök tog tilldelningen två arbetsdagar` — **statement** (carried by `Tiden till tilldelning var två arbetsdagar jämfört med tre tidigare`; no colon, no question, no echo of the standfirst, no overclaim)
- `## Arbetsledaren efterlyser en längre upptakt` — **statement** (a paraphrase of, not a repetition of, the quote beneath it, which says *jag skulle lägga till en vecka för förberedelser*; no echo, no overclaim)
- `## Siffrorna säger inte varför tilldelningen gick fortare` — **statement** (matches the note's own limit; no echo of the first sentence under it, no overclaim)

## 3. Against the expectation

- **Detect first-person supplier praise/rescue** — detected and repaired. `Vi på Svale är världsledande på att skapa framgång` and `kunden stod hjälplös innan vi kom` are gone from the lead, and the reply reports both removals with their reason. The same defect in the headline was repaired but is nowhere reported (see R1).
- **Detect pre-echoed quote** — detected and repaired. `Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.` is removed and the reply reports it as `borttaget som förhandseko av citatet under sig`.
- **Detect duplicate standfirst/lead** — detected and repaired. The doubled standfirst sentence and the lead's third repetition of it are gone; the script records the input norm `both open on "elm"` and records `"norms": []` for the returned text. The reply additionally reports a residual overlap it did not repair (its finding 4).
- **Detect causal contradiction** — detected and repaired. `Vår programvara orsakade därför hela förbättringen.` is removed and the reply reports it as contradicting the sentence before it.
- **No byline, reported as missing and left unfilled** — satisfied exactly. The script reports the same single failure for both texts, `"part": "byline", "measured": "absent"`, and the reply's finding 1 quotes `byline: absent` and states that no author is named anywhere, so the line is left unfilled rather than invented.
- **Two subheadings, neither describing its section, the second claiming a conclusion the note declines to draw** — repaired but not reported. Both were replaced with subheadings that do describe their sections, and the second now states the note's limit instead of overriding it; the reply's account of removals and changes never mentions either heading.
- **No ending section or call to action; the missing action reported rather than invented** — satisfied. The reply's finding 2 states that the genre's call to action must be built from offers, links or contact routes the material supplies, that the text supplies none, and that the line `Kundcaset publiceras av leverantören Svale.` is kept because it delimits what the text is. Nothing was invented.
- **Keep the customer's reservation and factual measures** — preserved. The reservation stands verbatim in the quote, and every measure and caveat listed under Changes is untouched.
- **Report unavailable support** — satisfied. Findings 1–3 are marked `kan inte repareras utan material som texten inte har`, and finding 3 names what the genre wants and the text lacks (background, the prompting situation, the roll-out) as obtainable only from Elm Quay or Svale.

No finding was made that the expectation rejects, and none was made against a counted requirement the returned text meets on the script's figures.

## 4. G1 — pass

The returned text does the case-study's job for a reader weighing the same software. It learns what was measured and over what window — `Enligt Elm Quays försöksanteckning registrerades 31 ärenden under åtta veckor, med akuta ärenden undantagna. Tiden till tilldelning var två arbetsdagar jämfört med tre tidigare.` — and, in the same breath, what the measurement will not support: `Anteckningen säger att arbetsbelastningen var olika och att skillnaden inte kan tillskrivas programvaran.` The angle is recognisable and holds from headline to last section: this trial produced a number, and the number does not explain itself. The craft is the appropriate one — every figure attributed to the note, the publisher's interest declared in `Kundcaset publiceras av leverantören Svale.`, and a customer voice allowed to keep its reservation. The reader considers a real trial rather than a testimonial. Thinness of the customer's situation is a missing part, judged under G2.

## 5. G2 — fail

Three of the genre's required parts are not doing a job in the returned text.

The **byline** is absent: the script reports one failure for `delivered.md`, `"part": "byline", "rule": "A text conforms when every part is present in the order shown.", "measured": "absent"`, and `"conforms": false`. The reply reports this as a finding it cannot repair without material the Skill does not have — no author is named in the text, and the Skill was given nothing else — so the omission is correctly left unfilled and its detection is credited under R1.

The **ending** does not exist. The last section closes on `Kundcaset publiceras av leverantören Svale.`, a provenance line, so nothing shows the standfirst's and lead's expectation met and nothing calls the reader to a next step. Case-study requires that call to be built from supplied offers, links or contact routes; the text carries no offer, no link and no contact route, so the reply reports it as irreparable without material the Skill does not have rather than inventing one — again credited under R1, but the returned text is still a case study that ends without an ending.

The **customer situation and action** are missing. The returned text carries results (`31 ärenden … två arbetsdagar jämfört med tre tidigare`) and the customer's appraisal (`– Jag skulle välja att göra försöket igen, säger Lind.`), and its publisher stance is truthful. It carries no account of who Elm Quay is, what prompted the trial, or how the software was put to work. The reply's finding 3 names exactly this gap and its source limit.

The parts that are present do perform distinct jobs: the headline states the angle, the standfirst stands alone, the lead precedes the first H2, and both subheadings now state the angle of what they head. But a returned text missing byline, ending and the customer's situation fails this criterion on its own terms.

## 6. P1 — pass

The reasoning is followable and every conclusion is now proportionate to visible support. The decisive passage is the second section: the figures are stated, then bounded, and no inference is drawn past the bound. Where the input closed that paragraph with `Vår programvara orsakade därför hela förbättringen.` — a conclusion its own preceding sentence forbids — the returned text stops at the note's limit, and the subheading `Siffrorna säger inte varför tilldelningen gick fortare` tells the reader in advance that no attribution is coming. Useful substance survives intact: the case count, the eight-week window, the exclusion of urgent cases, the two-versus-three-day comparison, and the unequal workload that makes the comparison weak.

The one soft spot is `en gemensam bild av ärendena`, which the reader first meets inside the quote with nothing introducing what the shared view is. It is plain language rather than an unexplained technical concept, and the input never introduced it either — the sentence that appeared to was a verbatim pre-echo of the quote. The reader is not misled, and the reply reports the missing bridge as its finding 5.

## 7. W1 — fail

The counted scale is met throughout. The script gives the headline as `"characters": 52, "words": 8` — inside 20–70 characters and not past eight words; the standfirst as `"words": 38, "paragraphs": 1`, inside the 60-word ceiling and one paragraph; the lead as `"paragraphs": 1`; the subheadings as 42 and 54 characters, both inside 70; every section carries at least one paragraph; the longest paragraph is `"words": 37`, far inside the 80-word norm; no heading sits below the second level. The norm the input broke is repaired: the script records `"measured": "both open on \"elm\""` for the input and `"norms": []` for the returned text, whose standfirst opens on *Under* and whose lead opens on *Ett*. The *most* figures, `"paragraphs": 6, "paragraphs_of_two_or_three_sentences": 3` and `"sections": 2, "sections_of_two_or_three_paragraphs": 1`, are read across the whole text and are not a failure here: the single-sentence paragraphs are two quotations and a one-line provenance note, each following its own content, and the figures improved from the input's 2 of 7 and 2 of 2.

The failure is qualitative and is actual reader loss at the point of entry. The standfirst opens `Under åtta veckor förde Elm Quay anteckningar om ett försök med programvara`; the lead's whole first sentence then says it again and adds only a pointer to the article itself — `Ett åtta veckor långt försök hos Elm Quay ligger bakom det här kundcaset.` A reader who has read the standfirst is restarted before the text moves, and the text only moves in the lead's second sentence. The two are not complementary, and the reply concedes exactly this in its finding 4, in the same words — `Läsaren som redan läst ingressen får en omstart innan texten kommer vidare` — without claiming any source limit for it. Both sentences are the Skill's own, so following the norm was possible and the text is not better for the repetition.

A second, smaller loss compounds it: the first section is a subheading and a bare quotation with no prose at all, so the reader is handed a speaker's reservation before anything has established what is being reserved. The reply names this too, as its finding 5.

## 8. L1 — pass

The Swedish is idiomatic and reads as written rather than translated. `som är noga med vad de inte kan avgöra` is a native construction with no English original behind it; `Arbetsledaren efterlyser en längre upptakt` uses *efterlyser* and *upptakt* the way a Swedish editor would; `Siffrorna säger inte varför tilldelningen gick fortare` is plain Swedish word order with an idiomatic comparative. The genitive `Elm Quays försöksanteckning` is formed correctly without an apostrophe, and `arbetsledare på Elm Quay` takes the preposition Swedish takes for an employer. Nothing in the new material carries generic translated English, and the reader hears one consistent, sober reporting voice across headline, standfirst, lead and both sections.

## 9. L2 — pass

The locale governs throughout. Speech is set with the Swedish speech dash and no quotation marks — `– Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Maya Lind, arbetsledare på Elm Quay.` — and the attribution follows the comma inside the same line, as Swedish practice has it. Numerals follow the Swedish convention: `31` as a figure, `åtta veckor`, `två arbetsdagar` and `tre` spelled out. The colon in the standfirst introduces a list in the Swedish manner. No date, currency or conversion appears anywhere in the returned text, and none was invented; no established variation in the preserved material was normalised away.

## 10. R1 — fail

**Defects addressed, and correctly.** Every defect the text made visible was caught and repaired within the text's own means: the supplier's first-person praise and the customer's supposed helplessness, the quote said in advance, the standfirst printed twice, the conclusion that contradicted the sentence before it, the headline that claimed a rescue, and the subheading that claimed proof its own section declines. Nothing was invented to fill a gap. No unavailable source was verified or pretended to. The two failures that a case study cannot repair from the text alone — the byline and the call to action — are reported as findings and left unfilled, which is precisely what the expectation asks.

**Preservation is clean.** The working voice, both quotations, the customer's reservation and every factual measure outside a finding stand untouched; the list under Changes confirms that nothing outside the findings was touched to satisfy taste. The text was not rewritten against a *most* count read at one paragraph or one section, and no finding was made against a requirement the script shows the text meeting. Finding 5, on the one-quote section, is grounded in the genre's demand that the narrative do the connecting work, not in the *most* statement about paragraphs per section, so it is not a wrong finding.

**Every removal and changed claim, against the account:**

- `Vi på Svale är världsledande på att skapa framgång` — removed; **reported accurately**, with the finding that produced it.
- `kunden stod hjälplös innan vi kom` — removed; **reported accurately**.
- `Vår programvara orsakade därför hela förbättringen.` — removed; **reported accurately**, including that the text now draws no conclusion about the cause.
- `Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.` — removed; **reported accurately**, including that the claim survives in the quote with the same attribution.
- `Elm Quay registrerade 31 ärenden` in the standfirst — rescoped; **reported accurately**, including that the scope is now narrower.
- `kundens försöksanteckning` → `Elm Quays försöksanteckning` — **reported accurately**.
- `Maya Lind, arbetsledare hos kunden` → `arbetsledare på Elm Quay` — **reported accurately**, with the correct note that the quoted wording is otherwise verbatim.
- Headline `Vår fantastiska lösning räddade Elm Quay` — replaced; **not reported anywhere**. This is the text's most prominent claim, and both its strength and its subject changed.
- Subheading `Kunden fick en gemensam bild` — replaced; **not reported anywhere**.
- Subheading `Resultatet bevisar allt` — replaced with a subheading of opposite polarity; **not reported anywhere**. The expectation names this heading as something the review must detect, and the account is where detection would show.

**Why this fails.** R1 requires the run to report its legitimate removals, and the account does not merely omit three of them — it states a count that excludes them: `Korrigeringsrundan tog bort fyra påståenden och flyttade tre`, followed by two lists presented as that enumeration. A user auditing the reply against the returned text finds their headline and both subheadings rewritten with nothing in the account to account for it, and no way to tell from the reply whether the change was a repair or a liberty. The account also contains a dangling cross-reference — finding 5 cites `(fynd 6 nedan)` for the pre-echo removal, and there is no finding 6; the removal appears in the following list instead.

The direction of all three unreported changes is safe — each lowered a claim's strength and none added anything the text does not carry — and the repairs themselves are right. That is why this is a close call rather than a plain one. But reporting is half of what R1 asks, and an account that presents an incomplete enumeration as complete does not meet it.

**Visible defects left unaddressed:** the standfirst/lead overlap (finding 4) and the first section's absent bridge (finding 5), both of which the Skill created in its own correction round and both of which it reports honestly as unresolved rather than claiming a source limit for them. They are reported, so they are not unresolved findings gone unreported; they remain quality problems of the returned text, scored under W1.

---

**Verdicts:** G1 pass · G2 fail · P1 pass · W1 fail · L1 pass · L2 pass · R1 fail
