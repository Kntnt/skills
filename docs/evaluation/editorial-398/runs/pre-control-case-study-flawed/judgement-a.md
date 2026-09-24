# Judgement a

The run directory has no frontmatter in the input. The reply puts the returned text inside a fenced `markdown` block. That wrapper is not a change to the text, and the Markdown inside it keeps the same heading levels, bold standfirst and dash-quote form as the input.

## 1. Differences

1. **Headline.** Before: `# Vår fantastiska lösning räddade Elm Quay`. After: `# Elm Quay noterade kortare tid till tilldelning`. Class: repair of a visible defect (the supplier's praise of itself and the rescue claim). The new headline states only the measured result (two days against three) and claims no cause.
2. **Standfirst.** Before: `**Elm Quay registrerade 31 ärenden. Elm Quay registrerade 31 ärenden.**`. After: `**Under ett åtta veckor långt försök med Svales programvara registrerade Elm Quay 31 ärenden, akuta ärenden undantagna. Det gick två arbetsdagar innan ärendena tilldelades, mot tre tidigare, men enligt Elm Quays anteckning kan skillnaden inte tillskrivas programvaran. Arbetsledaren Maya Lind berättar vad som hjälper och vad hon skulle göra annorlunda.**`. Class: repair of a visible defect (the sentence repeated inside the standfirst, and the same sentence repeated in the lead). Every fact comes from the body. Two small changes of **attribution** follow from the text itself. "Svales programvara" comes from "Vår programvara" in a text published by Svale. "Elm Quays anteckning" replaces "kundens försöksanteckning", and the text makes clear that the customer is Elm Quay.
3. **Lead.** Before: `Elm Quay registrerade 31 ärenden. Vi på Svale är världsledande på att skapa framgång, och kunden stod hjälplös innan vi kom.`. After: `Elm Quay har prövat programvara från leverantören Svale. Kundens egen anteckning visar hur det gick, och arbetsledaren Maya Lind säger vad hon tycker.`. Class: repair of a visible defect. The repeated sentence and the unsupported first-person praise and rescue claims are removed. The new sentences restate only what the body holds.
4. **First subheading.** Before: `## Kunden fick en gemensam bild`. After: `## Maya Lind bedömer försöket`. Class: repair of a visible defect. The old subheading turned the quoted opinion into a fact and did not describe its section.
5. **Pre-echo.** Before: `Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.`. After: removed. Class: repair of a visible defect (the paraphrase repeated the quote just before it).
6. **Second subheading.** Before: `## Resultatet bevisar allt`. After: `## Anteckningen redovisar resultatet med ett förbehåll`. Class: repair of a visible defect. The old subheading claimed a proof that its own section denies.
7. **Causal conclusion.** Before: `Vår programvara orsakade därför hela förbättringen.`. After: removed. Class: repair of a visible defect (a causal claim contradicted by the sentence before it). Removing it changes the text's **causality**, and that is the correct change.
8. **Unchanged.** The quote from Lind, the whole result paragraph up to the caveat, `– Jag skulle välja att göra försöket igen, säger Lind.` and `Kundcaset publiceras av leverantören Svale.` are all identical to the input. The reply makes no mechanical corrections and says the proofreading pass found none.

## 2. The account

1. **Headline.** Reported: "”Vår fantastiska lösning räddade Elm Quay” (rubriken) togs bort. Rubriken påstod en räddning och ett orsakssamband som texten själv motsäger", and the closing summary says the headline was rewritten. Accurate. The new headline's own claim is not listed on its own line, but the summary's "håller sig till vad texten belägger" describes it correctly.
2. **Standfirst.** Reported under "Ändrade påståenden": the 31 cases now stand in the standfirst with their scope, and the repetition was removed. The summary adds "Ingressen och inledningen har skrivits om, så att de inte längre upprepar varandra." The move of "Svales programvara" is reported openly under the removed causal sentence ("det står nu i ingressen och inledningen"). The change from "kundens" to "Elm Quays" is not reported, but it changes nothing of substance. Accurate.
3. **Lead.** Reported as the removal of "Vi på Svale är världsledande på att skapa framgång" and "kunden stod hjälplös innan vi kom", each with the reason "saknade stöd". The removal of the repeated sentence is also reported. Accurate.
4. **First subheading.** Reported: "Den gjorde Linds omdöme till ett faktum och tog citatet i förväg." Accurate.
5. **Pre-echo.** Reported: "togs bort eftersom meningen föregrep citatet. Samma omdöme står kvar i hennes citat." Accurate.
6. **Second subheading.** Reported: "Den påstod ett bevis som avsnittet under den förnekar." Accurate.
7. **Causal conclusion.** Reported: "Slutsatsen motsades direkt av meningen före ... Anteckningens förbehåll står kvar ordagrant." Accurate. The caveat is indeed kept verbatim.
8. **Unchanged parts.** The reply claims no change to them and makes none. Its statement that the proofreading pass found no mechanical errors matches the text.

## 3. The frozen expectation

- **Detect the first-person praise and rescue claims.** Met. The reply reports: "”Vi på Svale är världsledande på att skapa framgång” togs bort. Påståendet saknade stöd och stod i leverantörens vi-form" and "”kunden stod hjälplös innan vi kom” togs bort", and also the headline's "räddning".
- **Detect the pre-echoed quote.** Met. The reply reports: "”Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.” togs bort eftersom meningen föregrep citatet."
- **Detect the duplicate standfirst and lead.** Met. The reply reports: "Inledningens upprepning av samma mening togs bort" and "Ingressen och inledningen har skrivits om, så att de inte längre upprepar varandra."
- **Detect the causal contradiction.** Met. The reply reports: "”Vår programvara orsakade därför hela förbättringen.” togs bort. Slutsatsen motsades direkt av meningen före."
- **Report the missing byline and leave it unfilled.** Met. The reply reports: "Byline saknas. ... Varken texten eller anropet anger vem som skrivit den." The returned text has no invented byline.
- **Detect the first subheading as not describing its section.** Met. The reply reports: "Mellanrubriken ”Kunden fick en gemensam bild” togs bort. Den gjorde Linds omdöme till ett faktum och tog citatet i förväg."
- **Detect the second subheading as claiming a conclusion the note declines to draw.** Met. The reply reports: "Mellanrubriken ”Resultatet bevisar allt” togs bort. Den påstod ett bevis som avsnittet under den förnekar."
- **Report the missing ending section and call to action without inventing one.** Met. The reply reports: "Avslutning och uppmaning saknas. ... Det finns inget erbjudande, ingen länk och ingen kontaktväg att bygga en uppmaning på." The returned text adds no offer, link or contact route.
- **Keep the customer's reservation.** Met. The returned text keeps "– Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Maya Lind, arbetsledare hos kunden." word for word. It also keeps the note's reservation, "att skillnaden inte kan tillskrivas programvaran", and repeats it in the standfirst.
- **Keep the factual measures.** Met. The returned text keeps "registrerades 31 ärenden under åtta veckor, med akuta ärenden undantagna. Tiden till tilldelning var två arbetsdagar jämfört med tre tidigare" word for word.
- **Report unavailable support.** Met. The world-leader and helplessness claims are reported as "saknade stöd". The three unresolved findings are marked "kräver uppgifter som inte finns i texten". Nothing unsupported was invented or verified against an outside source.
- **Rejections.** None were made. The run invented no byline and no call to action. It did not keep the causal claim. It did not weaken or remove the reservation or the measures, and it verified nothing against an unavailable source.

The reply also reports a third unresolved finding that the expectation does not ask for: the text gives no background on the customer. It left that unfilled too.

## 4. R1

**Pass.** Two passages decide it. Every change repairs a named visible defect, and the working claims, the quotations and the note's caveat come through unchanged ("Anteckningens förbehåll står kvar ordagrant", which the returned text confirms). The findings that need missing facts are reported and left unfilled instead of invented ("Dessa tre kräver uppgifter som inte finns i texten. Därför har de inte åtgärdats.").
