# Judgement B — case-study-sv / write

## 1. Outcome

**Delivered**, with two remaining findings reported in the delivery account.

The delivered prose is **identical** to the last prose a checker saw. `evidence/source-check/draft-2.md` is the draft comparison 2 read, and a line-by-line diff against `delivered.md` shows one difference only: the seven-line `kntnt` frontmatter block (`genre: case-study`, `technique: none`, `language: sv`) prepended to the delivered copy. Not one word of the headline, standfirst, byline, lead, three sections or closing paragraph differs. The delivery account's claim — "Prosan levereras exakt som den sista kontrollen läste den" — holds.

No dispositions file is kept under `evidence/`; the directory holds `draft-1.md`, `comparison-1.md`, `draft-2.md`, `comparison-2.md` only. The repair trace is nevertheless legible from the two drafts, and every one of comparison 1's six findings is repaired in draft 2:

| Comparison 1 finding | Draft 1 | Draft 2 / delivered |
|---|---|---|
| F3 ownership vs management | "i två av bolagets hus" | standfirst rebuilt; no ownership asserted anywhere |
| F4 standfirst states the log's contents | "Efter åtta veckor låg 31 anmälningar i loggen" | "31 anmälningar registrerades" |
| F9 unsupported act of selecting buildings | "valde laget ut två hus för ett test" | "bestämde sig laget för att pröva en gemensam logg i två hus" |
| F11 what was tested | "visa hur långt varje anmälan hade kommit" | "visa status för varje reparation" |
| F20 workload attributed to the note | "Anteckningen konstaterar att arbetsbelastningen skilde sig…" | "Arbetsbelastningen skilde sig mellan perioderna, och anteckningen tillskriver…" |
| T2 translation, English syntax | "innan nästa hus börjar" | "innan nästa hus drar i gång" |

The T2 repair alters a translated quotation, which the material permits ("Translation of the quotations is permitted, preserving stance and qualification") and which preserves the conditional and the comparison.

## 2. Headings

- `# Elm Quay testade gemensam logg i två hus` — **statement**, **echo (partial)**. It is a clause saying what the text says, understood on its own, and it claims nothing the text does not carry. The echo mark is partial: the standfirst's first sentence restates the same proposition — Elm Quay tried a shared log in a test — in different words ("prövade"/"testade", "felanmälningslogg"/"logg"), adding the season and the duration. The two are not word-identical, and the standfirst adds the time frame the headline lacks, so this is overlap of substance rather than of phrasing.
- `## Så kom systemet på plats i de två husen` — **label** (a plain name for what the section holds: how the log was put in place). No echo of its first sentence ("Laget testade om loggen kunde visa status för varje reparation…"). No colon, question or overclaim; configuration, training and a running eight-week trial are all supplied.
- `## Siffrorna säger inget om orsaken` — **statement**. It states the section's angle and withholds causation rather than asserting it, which is exactly the direction the material requires. No echo of "Testet pågick i åtta veckor." No overclaim.
- `## Beslutet om fler hus återstår` — **statement**. No echo: the first sentence under it ("Testet har ännu inte utvidgats.") is semantically adjacent but shares no wording. Not marked **overclaim**: the material supplies both the unexpanded trial and a pending decision, and frames that decision by expansion ("The trial has not yet expanded; the team will decide after checking…"), with Lind speaking of "the next building". Naming the decision's subject is an inference, but a close one the material puts at issue itself.

No heading uses a colon, none is a question, and no heading level below the second appears (`anatomy-delivered.json` reports `"failures": []` and `"norms": []`).

## 3. F1 — **pass**

Every assertion, quotation, attribution and implication I can test stays within the supplied material. The hard constraints of this brief are all honoured:

- **No causal claim.** "Mediantiden från anmälan till tilldelad åtgärd var två arbetsdagar under testet och tre under de åtta veckorna dessförinnan. Arbetsbelastningen skilde sig mellan perioderna, och anteckningen tillskriver uttryckligen inte skillnaden programvaran." The two figures stand side by side with no causal verb, and the non-attribution is the note's, exactly as the material splits the voices ("The periods had different workloads, and the note explicitly does not attribute the difference to the software"). The heading above it, "Siffrorna säger inget om orsaken", reinforces the withholding.
- **Assignment time is never turned into completion time.** "tilldelad åtgärd" and "tiden fram till avslutad åtgärd" stay distinct, and the latter is named as unmeasured: "Kostnader, de boendes nöjdhet och tiden fram till avslutad åtgärd mättes inte."
- **No money saved, no delighted residents, no rescued customer.** None of the three appears; all three are named as unmeasured.
- **The customer's reservation survives**, twice: in narration ("Lind rekommenderade inte Svale till varje bostadsbolag" — the partial negation preserved, neither narrowed to a blanket refusal nor widened to an endorsement) and inside Q3, where the concessive "men jag skulle lägga in en extra vecka för förberedelser" stays attached to the endorsement.
- **Management, not ownership.** "ett bostadsbolag med eget underhållslag som förvaltar 640 lägenheter" renders "manages 640 flats" without asserting ownership. Draft 1's "bolagets hus" is gone.
- **Attribution and exclusions carried where the count is stated in the body:** "Enligt Elm Quays interna testanteckning från 4 december 2025 registrerades 31 felanmälningar i loggen, och då är akuta ärenden och arbeten som beställts före testet inte inräknade."
- **Supplier narration in third person throughout** ("Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen"), and the publisher stance stated: "Den här kundberättelsen är publicerad av Svale Systems och är alltså inte oberoende journalistik."
- **Quotations whole, in order, unwelded**, each one of the three supplied, attributed with "skriver … i en mejlintervju" — which is what "All interviews occurred by email" supports, and which avoids the scene, emotion and remembered dialogue the material forbids. The single natural-gender assertion, "skriver hon", rests on the material's own "Her final quotation is her actual, qualified assessment".
- **The link is described as the brief describes it** — "Svale Systems [checklista för införande](https://example.invalid/svale/checklist) att läsa igenom" — a document to read, with no booking and no trial implied, the URL exact, and no claim about the checklist's contents.
- **Unknown kept apart from absent:** "Någon jämförelse med en annan leverantör finns inte" reports the absence rather than claiming a comparison was made and lost.
- **The figures are exact:** 640, two buildings, six staff, two sessions, eight weeks, 31, two and three working days, 4 December 2025. No count-size judgement is made — nothing is called few, many, fast or modest — so none needs a supplied comparison.
- **Byline.** "Av Thomas Barregren" is not in the material, and the material names no author. The delivery account states the rule and its application: "Uppdraget namnger ingen författare, så författaren är du." That is the required statement, and the absence of the name from the material is not an F1 defect.

Three passages I examined and do not count as failures, cited so the record is complete:

1. **Lead — "Telefonanmälningar på ett ställe, e-post på ett annat."** (comparison 2's S2). The material says only "Previously telephone reports and emails were stored separately"; a literal reading of the draft adds that each channel had exactly one store. Two independent checkers split on this — comparison 1 row 7 tested the same sentence and passed it, comparison 2 reported it. I side with the first: in Swedish, "på ett ställe … på ett annat" is the ordinary contrastive rendering of *apart from one another*, where the indefinite reads as *somewhere* rather than as a count, and the reader's takeaway — the two kinds of report lived apart, so no shift could see both — is precisely the material's. A **qualitative concern**, not an unsupported fact.
2. **Standfirst — "31 anmälningar registrerades"** (comparison 2's S1). The exclusions and the attribution are dropped here and supplied two paragraphs later. But the clause asserts no more than the note's own sentence, "31 repair reports were entered"; the draft adds nothing, strengthens nothing and totalises nothing ("samtliga", "totalt" are absent). The caveat's absence from a standfirst that the body immediately qualifies is a **qualitative concern** about where the qualification sits, not a fact outside the material. It is the thinner of the two findings, and the run's own proposed repair ("akuta ärenden och tidigare beställda arbeten oräknade") would be an improvement.
3. **"Någon jämförelse med en annan leverantör finns inte"** for "No comparison with another supplier is available." Availability is rendered as existence, a hair stronger. Since the material states availability where it means availability and flat non-existence elsewhere ("There are no cost, resident-satisfaction or completion-time measurements" → "mättes inte", correctly flat), this one clause slightly over-reads. It changes no claim about the trial, the product or the customer. Neither checker reported it as a defect; nor do I.

Translated terms checked in both directions: "manages" ↔ "förvaltar" (neither admits ownership), "flats" ↔ "lägenheter", "status of each repair" ↔ "status för varje reparation" (repair not silently turned into report — draft 1's error, repaired), "assignment" ↔ "tilldelad åtgärd" (not completion), "sessions" ↔ "tillfällen", "kept telephone reporting open" ↔ "kunde fortsätta anmäla fel per telefon" (entailed, and no agency asserted that the material denies).

## 4. G1 — **pass**

The genre does its job for the named reader — an operations manager at a small housing company. What that reader learns is concrete, peer-sized and actionable: a 640-flat manager ran an eight-week trial in two buildings; the supplier was chosen after testing one capability, with no comparison behind it; the real cost was not data entry but agreement — "Vi lade mer tid på att komma överens om kategorierna än på att registrera de första anmälningarna" — and the practical lesson is a named unit of time, "en extra vecka för förberedelser"; training was six staff in two sessions; the numbers prove nothing about the software; the expansion decision is still open.

The angle is recognisable and held from headline to close: *what the trial required, and what the figures do not say* — announced in the standfirst ("Här är vad testet krävde och vad siffrorna inte säger") and delivered by the second and third sections. The craft is journalistic rather than promotional: named source, dated document, attributions carried, the supplier confined to third-person configuring and training, the customer the acting party in every sentence where an actor appears, and the disclosure stated plainly at the end. A supplier-published case that tells its reader the numbers mean nothing causal, and that the customer would not recommend the product to everyone, is doing the honest version of this genre's job.

## 5. G2 — **pass**

The parts appear in the anatomy's order and each does its own work. `anatomy-delivered.json` reports `"conforms": true`, `"failures": []`, `"norms": []`, and resolves the parts as headline, standfirst, byline, lead, then three sections.

- **Headline** — "Elm Quay testade gemensam logg i två hus", 40 characters and 8 words per the script, inside the 20–70-character requirement and not past the eight-word norm. It states the angle of the whole and is understood on its own. It claims no more than the text carries.
- **Standfirst** — 42 words, 1 paragraph, `sentences_estimate` 3 (script), inside the 60-word requirement. It stands alone: who, what, how long, the key figure, the supervisor's verdict and the promise of the piece.
- **Byline** — "Av Thomas Barregren", 3 words (script). The brief names no author, so the invoking user's name is correct, and the delivery account states it: "Bylinen bär ditt namn. Uppdraget namnger ingen författare, så författaren är du. Ska texten gå osignerad eller under någon annans namn måste raden ändras före publicering."
- **Lead** — 39 words, 1 paragraph (script), and it sits before the first H2. It begins the work rather than restating the standfirst: the problem (two channels apart), the company's size and shape, and the September decision.
- **Sections** — three, each with a subheading and 3 paragraphs (script). Explanatory body throughout.
- **Ending** — "För den som överväger ett liknande test finns Svale Systems [checklista för införande](…) att läsa igenom." The call to action is built from the one supplied route, framed as optional ("För den som överväger"), and accurately described as a document to read. It is the next step the explanation supports: the piece has just shown that preparation is where the work sits, and a checklist for införande is what that reader now needs. It shows the lead's expectation met.

The case-genre parts are all present and distinct: **situation** (reports stored apart; shifts could not see the same information — carried by Q1, which the narrative does not restate), **action** (capability test, supplier choice, own categories, telephone reporting kept open, configuration and training, eight-week trial), **results** (31 entered with exclusions and attribution; both median figures with the non-attribution; the three unmeasured things), **appraisal** (Q3, the material's qualified assessment, plus "Lind rekommenderade inte Svale till varje bostadsbolag" and the pending expansion). The **publisher stance is truthful** and stated: "publicerad av Svale Systems och är alltså inte oberoende journalistik."

Each quotation contributes experience beyond the surrounding narrative, as the brief asks: Q1 supplies the shift-visibility motive and the ownership of the categories, stated nowhere else in the text; Q2 is the only account of what preparation actually cost; Q3 is the qualified verdict.

## 6. P1 — **pass**

The reader can follow the reasoning. Unfamiliar things are introduced before use: the shared log is named and its purpose given in the lead before any section discusses it; the categories appear first in Q1 as the team's own, so that Q2's "komma överens om kategorierna" lands on something already known; the measure is spelled out in full — "Mediantiden från anmälan till tilldelad åtgärd" — and its limits are stated in the same paragraph rather than left for the reader to infer.

Transitions are real rather than decorative: "Testet pågick i åtta veckor" opens the figures section by anchoring the period the numbers describe; "Testet har ännu inte utvidgats" opens the last section on the state the heading names.

Conclusions are proportionate to visible support, conspicuously so: the two median figures are placed side by side and *no* conclusion is drawn, with the reason given — differing workloads and the note's explicit non-attribution. The one judgement in the piece belongs to a named person and is quoted.

Useful technical substance remains: status visibility per repair, shift handover, the team designing its own categories, telephone reporting kept open for residents alongside the log, configuration and training effort in staff and sessions, and the open question of whether the categories hold for larger repairs.

One mild structural looseness, not a failure: the section headed "Så kom systemet på plats i de två husen" opens with the supplier choice and the no-comparison note before the placing itself, so its first paragraph sits slightly ahead of its heading. The reader loses nothing — the section does deliver the placing in its second and third paragraphs.

## 7. W1 — **pass**

A web reader can orient and enter without the explanation or the voice fragmenting. Every counted line below is the script's.

- **Requirements:** `"conforms": true` and `"failures": []`. Headline 40 characters (20–70). Standfirst 42 words (≤60), 1 paragraph. Lead 1 paragraph. Subheadings 39, 32 and 29 characters (each ≤70). Each of the 3 sections has 3 paragraphs (≥1).
- **Norms:** `"norms": []` — no departure to weigh. The headline is 8 words and 40 characters, inside both the eight-word and 60-character norms. No paragraph exceeds 80 words; the longest measured is 42 ("Mediantiden från anmälan…"). No section exceeds three paragraphs. No heading level below the second appears.
- ***Most*, read across the whole text:** `paragraphs: 11` of which `paragraphs_of_two_or_three_sentences: 11`, and `sections: 3` of which `sections_of_two_or_three_paragraphs: 3`. Both typical statements hold across the text.
- **Standfirst and lead complementary, on different first words:** the standfirst opens "Hösten", the lead "Telefonanmälningar". They do different work — summary versus the scene of the problem — rather than one restating the other.
- **Body complete when the standfirst is covered:** the standfirst promises what the trial required and what the figures do not say; section 1 gives the requirement in setup terms, section 2 gives the figures and their limit, section 3 closes the open decision. Nothing promised is left unpaid, and nothing large is delivered that the standfirst did not trail.
- **Rhythm and headings:** the lead's fragment opener ("Telefonanmälningar på ett ställe, e-post på ett annat.") gives the entry a beat, and the three subheadings are informative statements a scanner can read alone — particularly "Siffrorna säger inget om orsaken", which tells a skimming operations manager the single most important thing about this case.

No density or fragmentation loss identified.

## 8. L1 — **pass**

The prose reads as Swedish written by a Swede, not as translated English. Native constructions carry it: the V2 inversion after a fronted adverbial, "Så förvarades felanmälningarna hos Elm Quay Housing"; the natural negation "Någon jämförelse med en annan leverantör finns inte"; the fronted object in the quotation, "Den tiden skulle jag avsätta"; and ordinary spoken idiom in "komma överens om kategorierna", "drar i gång", "lägga in en extra vecka", "en samlad bild av anmälningarna". The quotation attributions use the Swedish pratminus with a trailing comma before "skriver Maya Lind", which is the convention. None of the three quotations carries English word order.

One blemish, cited and not counted as a failure: "anteckningen tillskriver uttryckligen inte skillnaden programvaran" is the one heavy, bureaucratic construction in the text, and the bare double-object order after *tillskriva* reads awkwardly — the canonical order puts the attributee first ("tillskriver programvaran skillnaden"), and a plain rephrasing such as "säger uttryckligen inte att skillnaden beror på programvaran" would read more easily for the operations manager this is written for. It is a wording stiffness in an otherwise native register, not imported English phrasing, and the sentence's meaning reaches the reader intact.

## 9. L2 — **pass**

The resolved locale governs throughout.

- **Date:** "4 december 2025" — Swedish day-month-year, month lowercase, no ordinal. The material's "4 December 2025" is carried without a new or converted date.
- **Season and common nouns lowercase:** "Hösten 2025", "arbetsdagar", "bostadsbolag".
- **Genitives:** "Elm Quays interna testanteckning" takes the bare *s* with no apostrophe; "Svale Systems checklista" adds no further marker to a name already ending in *s*. Both correct Swedish.
- **Dash:** the standfirst's "– men med mer tid för förberedelser" uses a spaced tankstreck, and the quotations use the pratminus. Correct Swedish typography in both roles.
- **Numbers:** digits for 640 and 31, words for the small counts ("sex medarbetare", "två arbetsdagar", "åtta veckor", "två tillfällen") — consistent Swedish practice, and no figure is reformatted or converted.
- **Spelling:** "e-post", "mejlintervju", "felanmälningslogg", "i gång" are all current Swedish forms.
- **No currency appears**, and none is invented — correctly, since the material has no cost measurements.

One stylistic nicety rather than an error: the standfirst's second sentence begins with the numeral "31", which Swedish style guides prefer to avoid at a sentence opening. Established variation, not a mechanical fault.

## 10. Remaining findings

The delivery account opens by stating that the draft is delivered with known defects, that the final source check left two remaining findings, and that no prose was changed after the last check. Both are reported with passage and repair, and both are the findings comparison 2 raised as S1 and S2.

**Finding 1 — the standfirst's count without its exclusions or its source.**
Reported passage: *"Ingressens '31 anmälningar registrerades' saknar undantagen och sin källa."*
Text: "31 anmälningar registrerades, och arbetsledaren skulle göra om testet – men med mer tid för förberedelser."
Proposed repair, quoted: *"31 anmälningar registrerades, akuta ärenden och tidigare beställda arbeten oräknade, och arbetsledaren skulle göra om testet …"*
Under F1 I do **not** count this as a defect of source support: the clause asserts no more than the material's own "31 repair reports were entered", and the body supplies both exclusions and the attribution two paragraphs later. It is a real editorial improvement left unmade — the standfirst is read on its own — so the text carries a minor remaining quality problem here, correctly reported.

**Finding 2 — the lead's one store per channel.**
Reported passage: *"Ledets 'Telefonanmälningar på ett ställe, e-post på ett annat' påstår ett ställe per kanal."*
Text: "Telefonanmälningar på ett ställe, e-post på ett annat."
Proposed repair, quoted: *"Telefonanmälningar för sig, e-post för sig."*
Under F1 I do **not** count this as a defect either, for the reason given in §3: the contrastive indefinite reads as *somewhere … somewhere else* in Swedish, the two checkers split on it (comparison 1 row 7 passed the identical sentence), and the reader's takeaway matches the material exactly. The proposed repair is nonetheless tighter and would cost the lead nothing.

Neither finding is an unconditional rejection. Nothing unsupported in substance is asserted, the locale is right, no mechanical editing was substituted for the work asked, both remaining findings are reported rather than buried, and the delivery account states the one side effect the run left behind — the evidence copies under `evidence/source-check/`, kept at the observer's request — with everything else removed and `source.md` untouched.

**Verdicts: F1 pass · G1 pass · G2 pass · P1 pass · W1 pass · L1 pass · L2 pass.**
