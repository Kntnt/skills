# Judgement A — run `post-column-sv-r1-b`

Files read: `work/input.md` and `response.md` in this run directory, and nothing else. The returned text is the fenced `markdown` block in `response.md`; I compared it line by line and byte by byte against the input.

## 1. Differences

The frontmatter block (`kntnt: genre: column / technique: none / language: sv`), the H1, the byline string, and every body sentence but one come back character-for-character identical. Six differences:

**D1 — new paragraph inserted between the H1 and the byline.**
- Before: (nothing; `# Mallen har en ruta för allt utom poängen` was followed directly by `Av Nora Vik, bibliotekarie`)
- After: `Det retar bibliotekarien Nora Vik att en bokad timme så lätt räknas som ett resultat i sig. Hon vill att en mötesmall också ska be om skälet till att kolleger behöver varandras tid, och tvivlar samtidigt på att ännu ett fält hjälper. Kolumnen behåller båda hållningarna och lämnar läsaren något att se efter i sin egen mall.`
- Class: **change of taste** — an added structural element (a summarising lede), not the repair of anything visible in the input. Two sub-points inside it:
  - Sentences 1–2 and the first half of sentence 3 restate input claims accurately, but in the third person about the author, above her own byline, inside a signed first-person column. Nothing in the input is written in that voice.
  - The clause `lämnar läsaren något att se efter i sin egen mall` has no source in the input. It is true of the returned text only because of D6 — the Skill's own appended sentence. Treated on its own it is a **new claim about what the column does**, i.e. a difference in meaning between the input document and the returned one; it does not alter any pre-existing claim.

**D2 — ordering consequent on D1.** The byline is no longer the first thing under the title. Follows D1; nothing was moved or edited to achieve it.

**D3 — new heading.**
- Before: (nothing between `… inte ett bestämt möte.` and `Jag uppskattar möten …`)
- After: `## Min invändning gäller kalendern, inte samtalet`
- Class: **change of taste** (added structure). Its content is fairly drawn from the two paragraphs it covers (`Min tanke är alltså inte att varje samtal ska pressas fram till ett beslut` and `Det som retar mig är något annat: att tid i kalendern …`). It asserts nothing the input does not.

**D4 — new heading.**
- Before: (nothing between `… den räckvidd en reflektion har.` and `Ändå tycker jag …`)
- After: `## Skälet till mötet tål att skrivas ner`
- Class: **change of taste** (added structure). Drawn from `finns det ett skäl att skriva ner` / `båda delarna tål att motiveras`.

**D5 — new heading.**
- Before: (nothing between `… vad behöver vi förstå tillsammans?` and `Där börjar tvivlet.`)
- After: `## Jag prövar frågan, osäker på om den hjälper`
- Class: **change of taste** (added structure). Drawn from `Där börjar tvivlet` / `Jag vet inte om ytterligare en ruta gör våra möten bättre`.

**D6 — dash form.**
- Before: `… genom att utöka formuläret — bibliotekarien som svarar …` (U+2014 em dash, spaced)
- After: `… genom att utöka formuläret – bibliotekarien som svarar …` (U+2013 en dash, spaced)
- Class: **mechanical correction (locale form)** — the Swedish spaced tankstreck. Spacing and the rest of the sentence are untouched.

**D7 — sentence appended to the closing paragraph.**
- Before: `Jag vill prova den i alla fall, och behålla båda hållningarna så länge: hoppet om frågan och tvivlet på ännu en ruta.`
- After: the same sentence, unchanged, then `Nästa gång du fyller i en mötesmall, lägg märke till vad den inte frågar efter.`
- Class: **change of taste** (an added closing call to action). It introduces second-person address, absent everywhere in the input, and asks the reader to inspect a template other than the library's. It asserts nothing about other meetings or other templates — it only instructs an observation — so it does not overrun `jag påstår inget om möten i allmänhet`, but it is new material, and it displaces the author's suspended doubt from the text's last position.

Nothing was deleted. No sentence, argument, or quotation from the input is missing or reordered. The trailing newline is present in both. The returned text is delivered inside a fenced block in the reply; that is a property of the delivery, not of the text.

**Count: 6 differences (D2 is consequent on D1). Changes to what an existing claim says: 0.** Two differences (D1, D7) add assertions or address that the input does not contain, and one clause inside D1 (`lämnar läsaren något att se efter i sin egen mall`) states something no input sentence supports.

## 2. The account

The reply's own summary is: *"Texten skiljer sig från den som kom in på tre sätt. Anatomins saknade delar är på plats: en sammanfattande ingress ovanför bylinen, och underrubriker som delar brödtexten i sektioner — allt formulerat ur det texten redan säger. Avslutningen har fått en uppmaning som vänder sig till läsaren och håller sig inom textens egna avgränsningar om räckvidd. Och korrekturpasset rättade tankstrecket till svensk typografi."*

- **D1** — reported: `en sammanfattande ingress ovanför bylinen`. Accurate as to what and where. Inaccurate in one respect: the qualifier `allt formulerat ur det texten redan säger` does not hold for the clause `lämnar läsaren något att se efter i sin egen mall`, which is formulated out of the Skill's own D7 addition, not out of the input. The reply does not quote the lede or flag that it is written in the third person about the author.
- **D2** — reported implicitly by `ovanför bylinen`. Accurate.
- **D3, D4, D5** — reported collectively: `underrubriker som delar brödtexten i sektioner`. Accurate, though the reply neither counts them nor quotes them, so a reader of the reply alone cannot tell three headings were written.
- **D6** — reported: `korrekturpasset rättade tankstrecket till svensk typografi`. Accurate.
- **D7** — reported: `Avslutningen har fått en uppmaning som vänder sig till läsaren och håller sig inom textens egna avgränsningar om räckvidd`. Accurate as to the fact; the appraisal (`håller sig inom …`) is the Skill's own and is defensible, since the sentence asserts nothing about meetings in general.
- The reply counts the changes as `tre sätt`, grouping the lede and the three headings into one. Six differences (five of them authored additions) are presented as three.
- `Inga fynd kvarstår` and the closing sentence — `Inget påstående togs bort, och inget fick sin räckvidd, säkerhet, tillskrivning, kronologi, orsakslogik eller innebörd flyttad: brödtextens meningar kommer tillbaka ordagrant, de avgränsande meningarna inbegripna` — are true of the input's own sentences, and I verified them: no removal, no altered claim, every limit verbatim. What the reply never says is that the input had no defect other than the dash, and that everything else it did was conformance to a structure the input did not have. It reports no finding, legitimate removal, rejected loss, or irreparable finding.

## 3. Limiting sentences

Six in `work/input.md`. All six come back **as they were**, character-for-character:

1. `"Det är dokumentet jag tittar på, inte ett bestämt möte."` — kept as it was.
2. `"Min tanke är alltså inte att varje samtal ska pressas fram till ett beslut."` — kept as it was.
3. `"Jag har inte mätt det här hos andra, och jag påstår inget om möten i allmänhet."` — kept as it was. This is a disclaimer covering two things (no measurement elsewhere; no claim about meetings in general) and both halves return intact.
4. `"Det är min reflektion, med den räckvidd en reflektion har."` — kept as it was.
5. `"Jag vet inte om ytterligare en ruta gör våra möten bättre."` — kept as it was.
6. `"Kanske blir frågan bara en rad till att fylla i."` — kept as it was.

Borderline, and listed for completeness: `"Jag vill prova den i alla fall, och behålla båda hållningarna så länge: hoppet om frågan och tvivlet på ännu en ruta."` bounds the piece by refusing to resolve the doubt. The clause is untouched; D7 appends a sentence after it in the same paragraph, so it is no longer the text's last word, but the limit it states is stated exactly as before and no claim around it gains scope, certainty, attribution, chronology, causality or meaning.

**No limiting sentence is weakened or deleted**, so the sub-questions under this heading do not arise. No hardening of any of the three named forms, and no fourth form, is present: no refusal to assert became an assertion, no two-part disclaimer came back covering one, and no sentence whose only work is to limit was removed. The one place where a claim reappears without the limits attached is the added lede (D1), which restates what annoys the author while the limits sit further down the page — but the lede attributes the annoyance to her by name, claims nothing about meetings in general, and the limits are retained in the body, so the returned text bounds what it claims exactly as far as the input did.

## 4. R1

**Fail.**

Preservation is not the problem: every argument, every body sentence and every limiting sentence survives verbatim, and the one mechanical fix (D6) is a legitimate locale correction. The failure is the other half of the criterion — *"Clean texts may not be rewritten to satisfy taste or numerical guidelines."* The input is a clean column with no visible defect beyond the em dash, and the reply itself concedes it found nothing (`Inga fynd kvarstår`); yet it added five blocks of new text purely to fill out a structure it says was missing (`Anatomins saknade delar är på plats`).

The passage that decides it is the inserted lede:

> `Det retar bibliotekarien Nora Vik att en bokad timme så lätt räknas som ett resultat i sig. Hon vill att en mötesmall också ska be om skälet till att kolleger behöver varandras tid, och tvivlar samtidigt på att ännu ett fält hjälper. Kolumnen behåller båda hållningarna och lämnar läsaren något att se efter i sin egen mall.`

This is prose the author did not write, about the author, in the third person, placed above her byline in a signed first-person column — a change of the working voice at the head of the document, addressing no defect, and containing one clause (`lämnar läsaren något att se efter i sin egen mall`) that is true only because of a second unrequested addition. D7 compounds it by ending the column on an instruction to the reader in place of the author's suspended doubt. Under R1 a clean text should have come back with the dash fixed and nothing else.
