# Judgement B — case-study-sv, redline

## Changes

1. Headline. Before: `# Elm Quay testade gemensam logg i två hus`. After: `# Gemensam logg hjälpte Elm Quay men kostade förberedelsetid`. **Change to what a claim says** — strength and modality: the input headline asserted only that a trial took place; the returned one asserts, in the text's own voice and unattributed, that the log helped Elm Quay.
2. Standfirst. Before: `31 anmälningar registrerades, och arbetsledaren skulle göra om testet – men med mer tid för förberedelser.` After: `31 anmälningar registrerades i loggen, akuta ärenden och arbeten beställda före testet undantagna. Arbetsledaren skulle göra om testet – men med mer tid för förberedelser.` **Change to what a claim says** — scope: the 31-figure is narrowed by an exclusion clause (faithful to the body's own qualification) and one sentence becomes two.
3. First subheading. Before: `## Så kom systemet på plats i de två husen`. After: `## Svale satte upp loggen – laget stod för kategorierna`. **Change of taste** — the input subheading was conforming and stated its section's angle; the replacement is sharper but was not repairing a defect, and it moves the supplier into the subject position.
4. Body verb. Before: `Laget testade om loggen kunde visa status`. After: `Laget undersökte om loggen kunde visa status`. **Change of taste** — near-synonym substitution that reduces repetition of *test*; the sentence already worked.
5. Closing section. Before: `Laget vill först se hur kategorierna fungerar för större reparationer, och Lind rekommenderade inte Svale till varje bostadsbolag.` After: `Laget vill först se hur kategorierna fungerar för större reparationer. Lind gav ingen generell rekommendation av Svale.` **Change to what a claim says** — scope: the input's `inte … till varje` carried two readings (not to all, or not at all); the replacement closes the second reading but also drops the implication that she recommended it to some. Sentence split is the repair of a visible ambiguity.

## Headings

Input:

- `# Elm Quay testade gemensam logg i två hus` — **statement**, **echo** (repeats the standfirst's actor, verb and object: `prövade bostadsbolaget Elm Quay Housing en gemensam felanmälningslogg i ett test`)
- `## Så kom systemet på plats i de två husen` — **statement**
- `## Siffrorna säger inget om orsaken` — **statement**
- `## Beslutet om fler hus återstår` — **statement**

Returned text:

- `# Gemensam logg hjälpte Elm Quay men kostade förberedelsetid` — **statement**, **overclaim** (the body attributes no effect to the software; the only support is Lind's own quoted judgement, `Att ha en samlad bild av anmälningarna hjälper oss`)
- `## Svale satte upp loggen – laget stod för kategorierna` — **statement**
- `## Siffrorna säger inget om orsaken` — **statement**
- `## Beslutet om fler hus återstår` — **statement**

## G1 — pass

The case does its job for an operations manager at a small housing company: the situation (`Telefonanmälningar på ett ställe, e-post på ett annat`), the action (`Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen`), the results with their limits (`Kostnader, de boendes nöjdhet och tiden fram till avslutad åtgärd mättes inte`), the customer's own appraisal (`Jag skulle välja att göra om testet … men jag skulle lägga in en extra vecka för förberedelser`) and the publisher stance (`publicerad av Svale Systems och är alltså inte oberoende journalistik`) all survive intact. The reader learns what the trial cost in preparation time and what the numbers do not establish. The headline's unsupported conclusion is a real defect of this text; it is scored at G2 rather than counted twice here.

## G2 — fail

The anatomy requires a headline understood on its own **without claiming more than the text claims**. The returned headline, `Gemensam logg hjälpte Elm Quay men kostade förberedelsetid`, claims an effect the body explicitly withholds two sections later: `anteckningen tillskriver uttryckligen inte skillnaden programvaran`. The reader meets a verdict at the top that the text then declines to reach — and in a supplier-published case that is exactly the stance the disclosure line is there to protect. The reply reports this finding openly and leaves it unresolved, but it is not a finding that needed material the Skill lacked: the Skill created it in this round, and reverting or neutralising the headline needed nothing but words already on the page. Every other part performs its job — standfirst stands alone (script: 51 words, 1 paragraph), byline `Av Thomas Barregren` present, lead before the first H2 (script: 1 paragraph, 39 words), three explanatory sections, and a call to action built from a supplied route (`Svale Systems [checklista för införande]`, a document to read).

## P1 — pass

The reasoning is followable and hedged where it must be. The one figure that could carry an inference is fenced on both sides: `Mediantiden … var två arbetsdagar under testet och tre under de åtta veckorna dessförinnan. Arbetsbelastningen skilde sig mellan perioderna, och anteckningen tillskriver uttryckligen inte skillnaden programvaran.` Transitions are real (`Testet har ännu inte utvidgats. Laget vill först se …`), and the technical substance — categories, shifts, six trained staff, two sessions — remains. The single conclusion out of proportion to visible support is the headline, scored at G2.

## W1 — pass

Counted, on the script's figures for the returned text: `conforms: true`, `failures: []`, `norms: []`. Headline 58 characters and 8 words (within the 20–70 requirement and the eight-word/60-character *should*); standfirst 51 words (at most 60) in 1 paragraph; each subheading 52, 32 and 29 characters (at most 70); every section carries 3 paragraphs; the longest paragraph is 42 words, so no paragraph passes 80; no heading below the second level. *Most* holds across the whole text: `paragraphs_of_two_or_three_sentences: 10` of `paragraphs: 11`, and `sections_of_two_or_three_paragraphs: 3` of `sections: 3` — the one four-sentence paragraph is the standfirst, and a *most* statement never fails a single paragraph. Standfirst and lead open on different first words (`Hösten` / `Telefonanmälningar`) and are complementary: the standfirst's promise, `vad testet krävde och vad siffrorna inte säger`, is met by the body. Nothing is lost to density or fragmentation.

## L1 — pass

The Swedish reads as written Swedish, not translated English: `Så förvarades felanmälningarna hos Elm Quay Housing`, `innan nästa hus drar i gång`, the talstreck quotations. One qualitative concern, introduced by this round: `Lind gav ingen generell rekommendation av Svale` — in Swedish `en rekommendation av X` reads most naturally as a recommendation *made by* X, so the repair of one ambiguity opens a smaller one. It is a wobble in a single prepositional phrase, not a failure of the text's idiom.

## L2 — pass

Swedish locale mechanics hold throughout, and the round touched none of them: lower-case month in `4 december 2025`, `Hösten 2025`, `I september 2025`, spaced talstreck for quotations (`– Vi ville att kvällsskiftet …`), en dash in `göra om testet – men med mer tid`. No date was invented and no currency appears or was converted.

## R1 — fail

**Changed claims, against the account.**

- Headline (change 1). Reported, and reported accurately and in detail: the account names it `Olöst`, states that the round created it, quotes the only support the text offers, and explains why the body contradicts it. This is exemplary detection and reporting — but the account also chose to deliver the overclaiming headline rather than the conforming one it replaced, on the ground that `budgeten var förbrukad`. Nothing unavailable was needed to undo it. The text ships an unsupported claim in its most prominent position.
- Standfirst (change 2). **Not reported.** The account's claims section asserts `Inget påstående togs bort` and that exactly one claim moved in scope. Adding `akuta ärenden och arbeten beställda före testet undantagna` narrows the 31-figure's scope in the standfirst; it is truthful and I do not fault the edit, but the inventory that says one claim moved is incomplete.
- Lind sentence (change 5). Reported, and reported accurately, including the residual: `den säger inte heller, som den ursprungliga antydde, att hon rekommenderade Svale till några. Stäm av mot vad Lind faktiskt skrev.`

**Preservation.** All four quotations, all figures (640, 31, eight weeks, two/three working days, six staff, two sessions, 4 December 2025) and every bounding sentence — no supplier comparison, no attribution of the difference to the software, what was not measured, the supplier-published disclosure — stand unaltered. That part of the account is accurate.

**Taste changes to passages that already worked.** The input was clean on every measured point (input script: `conforms: true`, `failures: []`, `norms: []`, 11 of 11 paragraphs and 3 of 3 sections in the typical bands). Change 3 replaced a conforming subheading that stated its section's angle, and change 4 swapped one working verb for a synonym. Neither appears anywhere in the reply.

**Visible defects not addressed.** The headline echo the round correctly identified was the input's one real anatomy defect, and it is the only one; the round did address it, then over-corrected. The defect it left behind is its own.

The round earns credit for honesty and for preserving every quotation and caveat, but it delivers a text carrying an unsupported claim that it could have withdrawn, and its account of what it changed is incomplete in two places. Fail.

## Source loss

*Separate from every criterion above; the Skill had no access to this file.*

One real loss, from change 1. The source's judging note states outright: `No claim that software caused the shorter assignment time, saved money, delighted residents or rescued a helpless customer.` The returned headline, `Gemensam logg hjälpte Elm Quay men kostade förberedelsetid`, asserts precisely such a benefit in the publisher's own voice. The input headline did not.

One mild drift, from change 3. The brief says `The customer, Elm Quay Housing, should remain the acting party.` The new subheading `Svale satte upp loggen – laget stod för kategorierna` gives the supplier the first subject position of the section; the second clause returns the team, so the drift is small.

Two changes that cost the source nothing. Change 5: the source says `Lind did not recommend Svale to every housing company` and that `The customer's reservation must survive` — `Lind gav ingen generell rekommendation av Svale` keeps the reservation, and arguably renders it less ambiguously than the input did. Change 2: the source's `It excludes emergencies and work ordered before the trial` is now carried in the standfirst as well as the body, which strengthens the caveat rather than removing it.
