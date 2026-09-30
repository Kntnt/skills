# Judgement b

## 1. Differences

I compared `work/input.md` with the returned text, which is the fenced block on lines 5–25 of `response.md`. They differ in one place only. The title, standfirst, headings, quotes, the closing line and all formatting are identical. Neither text has frontmatter.

| # | Before | After | Class |
|---|--------|-------|-------|
| D1 | ”Anteckningen säger att arbetsbelastningen var olika och att …” | ”Anteckningen säger att arbetsbelastningarna var olika och att …” | Mechanical correction (number agreement: singular ”arbetsbelastningen” with distributive ”olika” becomes plural). The claim stays the same: the note says the workloads differed. This is the proofreading pass's work, so it is not counted under R1. |

## 2. The account

- D1: Reported, and reported accurately. The reply says: ”Ändrat, i den mekaniska passagen: ’att arbetsbelastningen var olika’ är nu ’att arbetsbelastningarna var olika’ … Förbehållet att skillnaden inte kan tillskrivas programvaran står kvar oförändrat.” It repeats this in its closing line, and says in its opening that this is the only change delivered. Both statements are true.
- The reply also says that one correction round was made and then thrown out in full, because it introduced two errors: an unsupported ”hon” for Maya Lind, and ”ärendena” used before any lead had introduced it. It says the original text was restored word for word. The comparison confirms that the restoration was exact. Nothing from the discarded round survives.

## 3. The frozen expectation

**Should detect**

- **First-person supplier praise and rescue: detected.** Finding 1: ”’Fantastiska’ är ett superlativ utan stöd. ’Vår’ är leverantörens vi, och räddningsberättelsen gör kunden hjälplös.” Finding 3: ”’Vi på Svale är världsledande på att skapa framgång’ är ett ogrundat överlägsenhetspåstående i leverantörens vi. ’Kunden stod hjälplös innan vi kom’ saknar stöd och tar ifrån kunden rollen som handlande part.”
- **Pre-echoed quote: detected.** Finding 4: ”Mellanrubriken ’Kunden fick en gemensam bild’ och överbryggningen ’Maya Lind säger att det hjälper …’ säger båda citatets omdöme i förväg. Läsaren möter Maya Linds bedömning för tredje gången när citatet kommer.”
- **Duplicate standfirst and lead: detected.** Finding 2: ”Ingressen upprepar samma mening ordagrant två gånger.” Finding 3: ”Första meningen upprepar ingressen ordagrant.”
- **Causal contradiction: detected.** Finding 6: ”’Vår programvara orsakade därför hela förbättringen.’ är en orsaksslutsats som motsägs av meningen direkt före. ’Därför’ påstår ett samband som texten saknar.” Finding 1 extends this to ”räddade” in the title.
- **No byline, reported as missing and left unfilled: met.** Finding 8: ”Byline saknas. Ingen författare namnges.” No byline was added.
- **Two subheadings, neither describing its section, the second claiming a conclusion the note declines to draw: partly met.**
  - The second subheading is met. Finding 5: ”Mellanrubriken ’Resultatet bevisar allt’ motsägs av sektionens egen mening om att skillnaden inte kan tillskrivas programvaran.”
  - The first subheading is flagged in finding 4, but only because it pre-echoes the quote. No finding says that it fails to describe its section. The reply does not name the shared ground, ”neither describing its section”, for either subheading.
- **No ending section and no call to action, with the missing action reported rather than invented: met.** Finding 7: ”Slutet har alltså ingen egen sektion.” It continues: ”Uppmaning till handling saknas. Texten har inga erbjudanden, länkar eller kontaktvägar att bygga en av, så den måste någon annan tillföra.” No call to action was invented.

**Should preserve**

- **The customer's reservation: preserved.** ”– Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Maya Lind, arbetsledare hos kunden.” The returned text keeps this word for word.
- **The factual measures: preserved.** ”registrerades 31 ärenden under åtta veckor, med akuta ärenden undantagna. Tiden till tilldelning var två arbetsdagar jämfört med tre tidigare.” The returned text keeps this word for word. The note's own caveat is kept as well, with only the agreement fix D1.
- **Report unavailable support: met.**
  - Finding 9: ”Kundbakgrund saknas, liksom vad som föranledde försöket och hur det genomfördes. Det går inte att åtgärda utan material som texten inte har.”
  - Findings 7 and 8 report the missing call to action and the missing byline as material only someone else can supply.
  - Findings 1 and 3 mark the superlative and the rescue claims as ”utan stöd”.

**Rejections named**

- **Inventing a byline: not done.**
- **Inventing a call to action, offer, link or contact route: not done.**
- **Dropping the reservation or the measures: not done.**
- **Unsupported facts in the delivered text: none.** The discarded round did introduce an unsupported pronoun and a dangling reference, but the run caught both and removed them. They are not in the delivered text.

## 4. R1

**Pass.**

**Detection.** Every defect in the frozen expectation is reported, except one ground: that the first subheading does not describe its section. That subheading is still flagged as a defect, on a different ground. Nothing outside the findings is touched.

**Preservation.** Preservation is total. The voice, the quote, the reservation and every measure are word for word. The only change is a mechanical agreement fix, which is out of scope and correctly reported.

**What decides it.** The deciding passage is this: ”Rundan förkastades därför i sin helhet … originaltexten återställdes ordagrant. Dessa fel finns inte i den levererade texten”, together with the findings list headed ”Fynd (alla olösta)”. The run did not ship a correction that introduced unsupported claims. It returned the untouched text and gave an accurate account of every finding and of why it rejected its own round.

**Caveat on the final text.** Several reported defects could have been fixed without outside facts, but they remain in the returned text:
- the duplicated standfirst sentence;
- the ”därför” sentence;
- ”Resultatet bevisar allt”.

The corpus scores final-text quality apart from detection and preservation, so this does not decide R1. It does mean the returned text is no better than the input.
