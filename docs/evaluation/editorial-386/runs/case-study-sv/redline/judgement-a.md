# Judgement A — case-study-sv, Redline

## Changes

Five differences between `redline/work/input.md` and `redline/delivered.md`.

1. **Headline.** Before: `# Elm Quay testade gemensam logg i två hus`. After: `# Gemensam logg hjälpte Elm Quay men kostade förberedelsetid`. **A change to what a claim says (strength and subject).** The new headline asserts in the text's own voice that the log helped Elm Quay; the text carries that only as Maya Lind's attributed assessment ("Att ha en samlad bild av anmälningarna hjälper oss"). The grammatical subject also moves from the customer to the log.
2. **Standfirst.** Before: "31 anmälningar registrerades, och arbetsledaren skulle göra om testet – men med mer tid för förberedelser." After: "31 anmälningar registrerades i loggen, akuta ärenden och arbeten beställda före testet undantagna. Arbetsledaren skulle göra om testet – men med mer tid för förberedelser." **A change to what a claim says (scope).** The figure is unchanged but narrowed by an exclusion the body already carried; it makes the standfirst stand alone more honestly.
3. **Subheading 1.** Before: `## Så kom systemet på plats i de två husen`. After: `## Svale satte upp loggen – laget stod för kategorierna`. **Repair of a visible defect** (a label replaced by a statement of the section's angle), but with a side effect on subject: the supplier becomes the acting party in the first half.
4. **Body verb.** Before: "Laget testade om loggen kunde visa status för varje reparation". After: "Laget undersökte om loggen kunde visa status för varje reparation". **Repair of a visible defect** — it removes "testade … i ett test" repetition against the standfirst. No claim changes.
5. **Closing section.** Before: "…för större reparationer, och Lind rekommenderade inte Svale till varje bostadsbolag." After: "…för större reparationer. Lind gav ingen generell rekommendation av Svale." **A change to what a claim says (modality/scope).** The original allowed two readings (she recommends Svale, but not to all; or she did not recommend it at all); the new sentence states only that she gave no blanket recommendation.

## Headings

### Input

- `# Elm Quay testade gemensam logg i två hus` — **statement**, **echo** (repeats the standfirst's "prövade bostadsbolaget Elm Quay Housing en gemensam felanmälningslogg" and the lead's "pröva en gemensam logg i två hus")
- `## Så kom systemet på plats i de två husen` — **label**, **echo** (repeats the headline's "i två hus"; the section's own first sentence is about choosing the supplier, not about "de två husen")
- `## Siffrorna säger inget om orsaken` — **statement**
- `## Beslutet om fler hus återstår` — **statement**

### Returned text

- `# Gemensam logg hjälpte Elm Quay men kostade förberedelsetid` — **statement**, **overclaim** ("hjälpte Elm Quay" is a conclusion the text carries only at the lower strength of Lind's attributed quotation, while the body declines to attribute the median-time difference to the software and records that costs, resident satisfaction and completion time were not measured)
- `## Svale satte upp loggen – laget stod för kategorierna` — **statement**
- `## Siffrorna säger inget om orsaken` — **statement**
- `## Beslutet om fler hus återstår` — **statement**

## G1 — pass

The case study still does its job for an operations reader at a small housing company. The reader sees the starting situation ("Telefonanmälningar på ett ställe, e-post på ett annat"), what the trial cost in effort ("Vi lade mer tid på att komma överens om kategorierna än på att registrera de första anmälningarna"), what was and was not measured ("Kostnader, de boendes nöjdhet och tiden fram till avslutad åtgärd mättes inte"), and what the customer would do differently ("jag skulle lägga in en extra vecka för förberedelser"). The angle promised by the standfirst — "vad testet krävde och vad siffrorna inte säger" — is recognisable throughout, and the journalistic craft of a supplier-published case (attribution, sourcing to a dated internal note, refusal of causal inference) is intact in the body.

## G2 — fail

Every required part is present and in order: headline, standfirst (51 words, 1 paragraph, `anatomy-delivered.json` `parts.standfirst`), byline "Av Thomas Barregren", lead (39 words, 1 paragraph) before the first H2, three sections of three paragraphs each, and an ending that meets the lead's expectation. The case parts are all there: situation, action ("Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen"), results ("31 felanmälningar", "Mediantiden … var två arbetsdagar"), the customer's appraisal in her own words, a truthful publisher stance ("Den här kundberättelsen är publicerad av Svale Systems och är alltså inte oberoende journalistik"), and a call to action built from the supplied link ("Svale Systems [checklista för införande]"), which is a document to read rather than a sales step.

The failure is the headline. "Gemensam logg hjälpte Elm Quay men kostade förberedelsetid" claims, in the publication's own voice, an effect the text carries only as Lind's attributed judgement, immediately after a section headed "Siffrorna säger inget om orsaken" and a paragraph stating that "anteckningen tillskriver uttryckligen inte skillnaden programvaran". A reader who finishes the text meets an article that refuses the conclusion its headline has already drawn, and in a supplier-published case that refusal is the piece's main credibility asset. The headline also displaces the customer as acting party. The reply does report this as an unresolved finding, but it does not report it as unrepairable for want of material the Skill lacked — the Skill's own account says the budget was spent — so the defect is scored here and the detection is scored under R1.

## P1 — pass

The body's reasoning is intact and its conclusions stay proportionate to visible support. The one place a causal reading beckons is explicitly closed: "Arbetsbelastningen skilde sig mellan perioderna, och anteckningen tillskriver uttryckligen inte skillnaden programvaran." Unfamiliar specifics are introduced before use — the log, then the supplier, then the categories, then the figures — and transitions are real rather than connective filler ("Testet pågick i åtta veckor. Enligt Elm Quays interna testanteckning från 4 december 2025 …"). Useful technical substance survives: the trial's scope, the exclusions, the two measures compared, and the four things not measured. The disproportionate conclusion in the headline is scored at G2, not here.

## W1 — pass

`anatomy-delivered.json` reports `conforms: true`, `failures: []` and `norms: []`. Counted requirements: headline 58 characters (`parts.headline.characters`), within 20–70; standfirst 51 words (`parts.standfirst.words`), at most 60, and 1 paragraph; lead 1 paragraph, before the first H2; the longest subheading 52 characters (`parts.sections[0].subheading.characters`), at most 70; every section has at least one paragraph (3, 3, 3). Norms are met too: the headline is 8 words and 58 characters (`parts.headline`), the longest paragraph 42 words (`parts.sections[1].paragraphs[1].words`), no section exceeds three paragraphs, and `norms: []` confirms no heading level below the second. Standfirst and lead open on different first words ("Hösten" / "Telefonanmälningar"). *Most* holds: 10 of 11 paragraphs run to two or three sentences and 3 of 3 sections to two or three paragraphs (`typical`); the standfirst's fourth sentence is a single paragraph and does not fail the *most* statement. The body is complete when the standfirst is covered — the promise "vad testet krävde och vad siffrorna inte säger" is paid by the preparation-time quotations and the "Siffrorna säger inget om orsaken" section. The reader can orient and enter without losing the continuous explanation.

## L1 — pass

The Swedish reads as written in Swedish, not translated into it: "Så förvarades felanmälningarna hos Elm Quay Housing", "bestämde sig laget för att pröva", "innan nästa hus drar i gång". Inversion, particle verbs and the quotation dash are native. Two of the Skill's own sentences are stiffer than the rest. The standfirst's absolute construction "akuta ärenden och arbeten beställda före testet undantagna" is formal-register Swedish in an otherwise journalistic standfirst, and "Lind gav ingen generell rekommendation av Svale" reintroduces an ambiguity of its own, since Swedish "rekommendation av Svale" can be read as a recommendation *by* Svale as well as *of* it — an unfortunate result for a change made to remove ambiguity. Neither breaks the prose, so this is a qualitative concern, not a failure.

## L2 — pass

Swedish locale mechanics govern throughout. Dates take the Swedish form with a lower-case month: "4 december 2025", "I september 2025", "Hösten 2025". Quotations use the Swedish quotation dash "–" rather than English quotation marks, and the dash in the standfirst is an en dash with spaces. Numerals follow Swedish usage ("640 lägenheter", "31 felanmälningar", "sex medarbetare"). No currency or converted figure appears, and no new factual date was introduced — "4 december 2025" is carried over unchanged from the input.

## R1 — fail

**Removals.** None. No sentence, quotation, figure or delimiting statement was deleted; the account's claim that "Inget påstående togs bort" is accurate, as is its list of the four quotations, the figures and the four limiting statements that survive intact.

**Changed claims, and whether the account reports them accurately.**

- *Headline* (change 1): reported, and reported accurately and at length. The account names the change, names its own repair as the cause, identifies the only support the text offers (Lind's quotation), names the countervailing body statements, and leaves the decision to the user. This is the run's strongest work.
- *Closing sentence* (change 5): reported accurately. The account states the scope has moved, explains which reading was closed, and flags honestly that the new sentence no longer implies she recommended Svale to anyone — with the instruction to check against what Lind actually wrote.
- *Standfirst* (change 2): **not reported.** The account's "Påståenden" section says no figure and none of the delimiting sentences changed, which is true of the body, but it is silent about the exclusion clause the round added to the standfirst's figure. A reader of the account would not know the standfirst's claim had been narrowed.
- *Subheading 1* (change 3): **not reported.** The account mentions no heading change other than the headline, so the replacement of "Så kom systemet på plats i de två husen" goes unrecorded — including its side effect of making the supplier the acting party in a supplier-published case.
- *"testade" → "undersökte"* (change 4): **not reported.**

**Visible defects not addressed.** The input's first subheading, "Så kom systemet på plats i de två husen", was addressed. No other visible defect was left standing — but note that on the script the input already had `conforms: true`, `failures: []`, `norms: []` (`anatomy-input.json`), so no counted requirement or norm was available to repair.

**Changes of taste to passages that already worked.** Change 4 is close to one, though the "testade … i ett test" repetition against the standfirst gives it a reason. The decisive problem is the headline. The input headline met every counted requirement (40 characters, 8 words, `anatomy-input.json` `parts.headline`) and had a defensible defect — it echoed the standfirst and the lead — so rewriting it was in scope. What is not in scope is the result: the round replaced a true, modest headline with one that asserts an effect the text declines to assert, then spent its budget and shipped the overclaim. This is a self-inflicted defect, not an irreparable finding; reverting to the input headline, or writing one that states the angle without claiming an effect, needed no material the Skill lacked. R1 asks that Redline address concrete defects while preserving claims outside findings; here the Skill's own repair created the returned text's single worst claim problem. The reporting is exemplary and the account is honest about authorship of the fault, but honest reporting does not make the delivered text sound, and two further claim-scope changes went unreported entirely.

## Source loss

*Separate from every criterion above; the Skill could not know this file.*

Yes — two source requirements were weakened, both by the headline rewrite, and one by the subheading.

1. `write/work/source.md`, "Forbidden inferences / judging": "No claim that software caused the shorter assignment time, saved money, delighted residents or rescued a helpless customer," together with "Lind did not recommend Svale to every housing company. Her final quotation is her actual, qualified assessment. It is not an inference from the figures." The change from "Elm Quay testade gemensam logg i två hus" to "Gemensam logg hjälpte Elm Quay men kostade förberedelsetid" lifts the one permitted "helps us" out of Lind's qualified, attributed assessment and states it as the publication's own effect claim, in the position the reader reads first.
2. `write/work/source.md`, Brief: "The customer, Elm Quay Housing, should remain the acting party." The new headline makes the log the subject and Elm Quay its object, and the new subheading "Svale satte upp loggen – laget stod för kategorierna" puts the supplier in the acting position in its first clause. The source's material supports the second half ("Svale configured the log and trained six staff"), so the subheading is truthful, but the agency has shifted toward the publisher.

Two changes did **not** cost the source anything. The standfirst's added clause matches "It excludes emergencies and work ordered before the trial" exactly. And "Lind gav ingen generell rekommendation av Svale" preserves the reservation the source requires to survive ("The customer's reservation must survive"), rendering "Lind did not recommend Svale to every housing company" with, if anything, less ambiguity than the input had — at the cost of the new Swedish ambiguity noted under L1.
