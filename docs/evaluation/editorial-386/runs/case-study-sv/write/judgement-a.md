# Judgement A — case-study-sv / write

## 1. Outcome

**Delivered.** `response.md` carries the draft in full inside a fenced block, headed by a delivery account that labels it "levereras med kända brister" and names two remaining source-support findings.

**The delivered prose is identical to the last prose a checker saw.** `evidence/source-check/comparison-2.md` reads `draft-2.md`; the delivered body from the headline onward is byte-identical to `draft-2.md` (verified by diff). The only difference between `delivered.md` and `draft-2.md` is the YAML `kntnt` map (`genre: case-study`, `technique: none`, `language: sv`) prepended above the headline — metadata, not prose. The account states the same: "Prosan levereras exakt som den sista kontrollen läste den, så ingen av dem är åtgärdad." The dispositions in `comparison-1.md` account for six findings against `draft-1.md` (F3 ownership, F4 standfirst count, F9 an invented act of selecting the two buildings, F11 what was tested, F20 the workload attribution, T2 "innan nästa hus börjar"); all six are repaired in `draft-2.md`, which was then re-checked. No repair was made after the last comparison.

## 2. Headings

- `# Elm Quay testade gemensam logg i två hus` — **statement**, **echo**
- `## Så kom systemet på plats i de två husen` — **statement**
- `## Siffrorna säger inget om orsaken` — **statement**
- `## Beslutet om fler hus återstår` — **statement**

Notes on the two non-obvious marks. The headline is marked **echo** because the standfirst's first sentence restates its whole proposition with synonyms — "testade gemensam logg" against "prövade … en gemensam felanmälningslogg i ett test" — so the reader meets the same fact twice in successive lines; the headline keeps "i två hus" and the standfirst adds "hösten 2025" and "åtta veckor", so the overlap is partial, not total. No heading is marked **overclaim**: "Siffrorna säger inget om orsaken" withholds causation rather than asserting it, which is the direction the material requires ("the note explicitly does not attribute the difference to the software"); "Så kom systemet på plats" rests on "Svale configured the log and trained six staff during two sessions"; "Beslutet om fler hus återstår" rests on "The trial has not yet expanded; the team will decide after checking how the categories work for larger repairs", and the material frames the pending decision by expansion. No **colon** and no **question** form appears. No subheading repeats the first sentence under it.

## 3. F1 — pass

Judged against `work/source.md` directly. Every figure, date, name, statistic and attribution in the delivered text traces to a supplied passage with its scope, modality and holder intact:

- "640 lägenheter" ← "manages 640 flats"; "förvaltar" carries management, not ownership (the draft-1 defect "två av bolagets hus" is gone).
- "I september 2025 bestämde sig laget för att pröva en gemensam logg i två hus" ← the source sentence unchanged, including the decision staying in September and no act of selecting the buildings (draft-1's F9 repaired).
- "Laget testade om loggen kunde visa status för varje reparation och valde därefter Svale Systems" ← "It chose Svale Systems after testing whether the log could show the status of each repair" — chronology and the thing tested both exact (draft-1's F11 repaired).
- "Enligt Elm Quays interna testanteckning från 4 december 2025 registrerades 31 felanmälningar i loggen, och då är akuta ärenden och arbeten som beställts före testet inte inräknade" — attribution, date, figure and both exclusions all carried.
- "Mediantiden från anmälan till tilldelad åtgärd var två arbetsdagar … och tre under de åtta veckorna dessförinnan" — the median named as a median, the endpoints kept at assignment, and "tiden fram till avslutad åtgärd" named separately as unmeasured. The forbidden inference assignment → completion is not made anywhere.
- "Arbetsbelastningen skilde sig mellan perioderna, och anteckningen tillskriver uttryckligen inte skillnaden programvaran" — the workload difference is now in the material's own voice and only the non-attribution is the note's (draft-1's F20 repaired).
- The three quotations are each used whole, in the source's order, with stance and qualification intact: "Kategorierna var våra" keeps the ownership claim and Svale subordinate; "men jag skulle lägga in en extra vecka för förberedelser" keeps the reservation attached to the endorsement; "Lind rekommenderade inte Svale till varje bostadsbolag" keeps the partial negation without widening it into a refusal or narrowing it into an endorsement. **The customer's reservation survives.**
- No claim of cause, saving, resident satisfaction or a rescued customer. "Kostnader, de boendes nöjdhet och tiden fram till avslutad åtgärd mättes inte" blocks all three.
- Byline: "Av Thomas Barregren" is not in the material; the brief says "No author name supplied", and the delivery account states the substitution ("Uppdraget namnger ingen författare, så författaren är du"). G2 licenses this, so it is not an unsupported addition.
- The link is described exactly as the brief describes it — "checklista för införande … att läsa igenom", no booking and no trial — and its destination is not characterised beyond that. The account records that the URL was not fetched.

Four passages I tested and do not report as defects, two of which the run itself reports as remaining (see §9):

1. **Standfirst "31 anmälningar registrerades"** drops the note's attribution and the two exclusions. This is a real compression, and the checker's case stands in the abstract: the material says the *count* excludes emergencies, not that emergencies stayed out of the log. But 31 is the material's own figure, the direction of the looseness favours nobody (a bounded count is the smaller number), and the attribution and both exclusions are restored three paragraphs later in the same short text. No reader finishes the piece holding a belief the material does not support. Minor, not a dropped caveat that changes a claim.
2. **Lead "Telefonanmälningar på ett ställe, e-post på ett annat"** — tested in both directions. English "stored separately" ordinarily means the two channels were kept apart from each other, which is precisely what the Swedish idiom "på ett ställe … på ett annat" says; the count of physical stores is not what either sentence is about, and the source's next sentence ("The team wanted staff on different shifts to see the same information") is about information sitting apart. Supported on the ordinary reading.
3. **"Någon jämförelse med en annan leverantör finns inte"** against "No comparison with another supplier is available" — availability hardened to non-existence. The shift is real but anodyne: it withholds support rather than manufacturing it, and it cannot mislead in the publisher's favour.
4. **"ett bostadsbolag med eget underhållslag som förvaltar 640 lägenheter"** — the relative clause sits after "underhållslag", so a strict attachment would say the team manages the flats. Sense forces the company reading, which is the source's. A syntax concern (§8), not a factual one.

Nothing in the text is an invented event, personal attribute, emotion, scene or remembered dialogue; the email channel is stated ("skriver … i en mejlintervju"), as the material requires. Unknown is kept apart from absent: the text says the comparison does not exist and the three measurements were not made, and says the expansion decision is open, never that it was declined.

## 4. G1 — pass

The genre does its job for operations managers at small housing companies. The reader learns what the trial actually consisted of — two buildings, categories designed in-house, telephone reporting kept open, "Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen", eight weeks — and what it cost in effort, from the one person who ran it: "Vi lade mer tid på att komma överens om kategorierna än på att registrera de första anmälningarna." The angle is recognisable and held throughout: the standfirst promises "vad testet krävde och vad siffrorna inte säger", and the middle section delivers the second half by putting the two medians side by side and then refusing the inference. The craft is journalistic rather than promotional: named source, dated internal note, stated interview channel, the customer as the acting party in every clause where something was decided ("Laget testade … och valde", "Laget vill först se"), the supplier confined to third-person configuration and training, and an explicit disclosure. The reader can act: a linked implementation checklist, offered conditionally ("För den som överväger ett liknande test").

## 5. G2 — pass

**Parts and order.** `anatomy-delivered.json` reports `"conforms": true` with `"failures": []`, and `parts` carries headline, standfirst, byline, lead and three sections in order; the lead (`"words": 39`) precedes the first H2. Every counted requirement is met by the script's figures: headline `"characters": 40` (20–70), standfirst `"words": 42` (at most 60) and `"paragraphs": 1`, lead `"paragraphs": 1`, subheadings at `39`, `32` and `29` characters (at most 70), and each of the three sections carries three paragraphs (at least one).

**Case-study parts.** Situation: "Telefonanmälningar på ett ställe, e-post på ett annat," with the shift motive supplied by the customer herself — "Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort." Action: the capability test, the supplier choice, the in-house categories, the retained telephone channel, the configuration and training. Results: the bounded count, the two medians, and what was not measured. Appraisal: the third quotation, qualified, plus "Lind rekommenderade inte Svale till varje bostadsbolag" and "Testet har ännu inte utvidgats."

**Publisher stance.** Truthful and explicit: "Den här kundberättelsen är publicerad av Svale Systems och är alltså inte oberoende journalistik." Supplier narration is third person everywhere; the text never speaks as Svale.

**Call to action.** Built from a supplied route and described as the brief describes it — a document to read, not a consultation booking or a product trial.

**Byline.** "Av Thomas Barregren", with the account stating the brief named no author and the invoking user was used, and saying what must change before publication. This is what G2 asks of a Write run.

**Distinct jobs, with one concern.** Each subheading states the angle of what it heads, is understood alone, claims nothing the section does not carry, and does not repeat the sentence beneath it. The one weak seam is the headline/standfirst pair: the headline states the subject rather than the angle, and the standfirst's first sentence then restates that subject with synonyms before the standfirst gets to its own work. The standfirst nonetheless stands alone and adds the count, the verdict and the article's promise, and the headline's factual restraint is defensible in a supplier-published case where every stronger headline would overclaim. A qualitative concern, not a contract rejection.

## 6. P1 — pass

The reasoning is followable by the named reader and the terms arrive before they are used. "Felanmälningslogg" is defined by the lead's picture of the problem before the log is ever named as a product. "Mediantiden från anmälan till tilldelad åtgärd" states its own endpoints inside the sentence, and the following sentence contrasts it with "tiden fram till avslutad åtgärd", so the distinction that the material insists on is also the reader's aid to understanding. The transitions are real, not decorative: the first section moves from the problem to the choice and the setup, the second section's heading states the conclusion the figures will be held to, and the third moves from what happened to what has not been decided.

Conclusions are proportionate to visible support — conspicuously so. The strongest causal statement in the text is a refusal: "Arbetsbelastningen skilde sig mellan perioderna, och anteckningen tillskriver uttryckligen inte skillnaden programvaran." The technical substance a practitioner needs survives: 640 flats, two buildings, six staff, two sessions, eight weeks, 31 reports with their exclusions, 2 against 3 working days, and the explicit list of what was never measured. Minor: "systemet" enters in the first subheading having been called "logg" up to that point, which costs a beat but no comprehension.

## 7. W1 — pass

Orientation and entry are good and the explanation stays continuous. The script reports `"conforms": true` with `"norms": []`, so no *should* is departed from at all: the headline is `"words": 8` and `"characters": 40` (not past eight words or 60), no paragraph exceeds 80 words, no section exceeds three paragraphs, and no heading level below the second appears (`parts.other` is empty). The *most* statements are satisfied across the whole text, not merely on balance: `"paragraphs": 11` with `"paragraphs_of_two_or_three_sentences": 11`, and `"sections": 3` with `"sections_of_two_or_three_paragraphs": 3`.

Standfirst and lead are complementary and open on different first words — "Hösten" against "Telefonanmälningar". The standfirst is covered by the body: it promises the trial and its length (delivered in §2 of the text), the count (delivered with its exclusions), the supervisor's qualified verdict (delivered as the third quotation), and "vad testet krävde och vad siffrorna inte säger" (delivered by the first and second sections respectively). Rhythm is deliberate rather than uniform — the lead opens on a verbless pair, the sections alternate narration and quotation, and each section ends on the voice or the fact the next one builds from. No density or fragmentation loss: no paragraph is a lone sentence and none runs long enough to lose the thread.

## 8. L1 — pass

The Swedish reads as Swedish, not as translated English. Native constructions carry the prose: the fronted "Så förvarades felanmälningarna hos Elm Quay Housing" with V2 intact, "bestämde sig laget för att pröva", the existential inversion "Någon jämförelse med en annan leverantör finns inte", "och då är … inte inräknade", and "För den som överväger ett liknande test finns …". The quotations sound spoken rather than rendered: "Vi lade mer tid på att komma överens om kategorierna", "innan nästa hus drar i gång" (which also repairs draft-1's English-shaped "innan nästa hus börjar"), "Att ha en samlad bild av anmälningarna hjälper oss".

Two slips, neither enough to fail the criterion:

- "anteckningen tillskriver uttryckligen inte **skillnaden programvaran**" inverts the argument order of *tillskriva*, which takes the party credited first ("tillskriver inte programvaran skillnaden"). As written it reads literally as ascribing the software to the difference. Both nouns are definite and the semantics force the intended reading, so no reader is misled, but the clause is a beat harder than it should be.
- "rekommenderade inte Svale till **varje** bostadsbolag" is the English partial negation carried over; "inte … alla" is the ordinary Swedish shape. It is understood, and the scope of the negation is preserved.

One further syntax concern, noted under F1: the relative clause in "ett bostadsbolag med eget underhållslag som förvaltar 640 lägenheter" sits next to the wrong candidate antecedent.

## 9. L2 — pass

The resolved locale governs throughout, and no new factual date or conversion is invented. Dates: "4 december 2025" and "I september 2025" — lowercase month, day before month, Swedish order and no ordinal. Numbers follow the Swedish convention of spelling out the small ones and setting the rest in digits: "två arbetsdagar", "tre", "sex medarbetare", "åtta veckor" against "31 anmälningar" and "640 lägenheter". Punctuation is Swedish: quotations are set with the speech dash "–" rather than quotation marks, and the parenthetical dash in "göra om testet – men med mer tid" is a spaced tankstreck, not an em dash. Spelling and compounding are Swedish: "e-post", "mejlintervju", "felanmälningslogg", "i gång". The genitives are correct and specifically Swedish: "Elm Quays interna testanteckning" takes a bare *s* with no apostrophe, and "Svale Systems checklista" takes no further marker after the name's final *s*. Headline and subheadings are in sentence case. No currency appears, so none is converted. The one imported mark — the semicolon in "Kategorierna var våra; Svale hjälpte oss" — is the source quotation's own punctuation inside a permitted translation, and is left rather than editorialised.

## 10. Remaining findings

The delivery account reports two, both source support, both unrepaired, and both framed there as the checker's claims for the editor to settle rather than established errors.

1. **"Ingressens '31 anmälningar registrerades' saknar undantagen och sin källa."** Passage: the standfirst, "31 anmälningar registrerades, och arbetsledaren skulle göra om testet – men med mer tid för förberedelser." Proposed repair, quoted from the account: "31 anmälningar registrerades, akuta ärenden och tidigare beställda arbeten oräknade, och arbetsledaren skulle göra om testet …". Under F1 I judge this a real but minor compression, not a defect that fails the criterion: the figure is the material's, and the body restores both the attribution and the two exclusions in the same text. The repair would improve the standfirst and should be taken.
2. **"Ledets 'Telefonanmälningar på ett ställe, e-post på ett annat' påstår ett ställe per kanal."** Passage: the lead's opening sentence. Proposed repair, quoted from the account: "Telefonanmälningar för sig, e-post för sig." Under F1 I do not judge this a defect: "stored separately" and the Swedish idiom say the same thing on the ordinary reading, and the checker's counter-case turns on a literalism the sentence does not invite. The proposed repair is also the weaker sentence.

Both were reported to the user before the draft, with passage and repair, so nothing mandatory went unreported; the text is nonetheless delivered with a named remaining quality question in the standfirst.
