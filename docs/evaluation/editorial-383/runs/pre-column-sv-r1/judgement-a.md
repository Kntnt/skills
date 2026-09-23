# Judgement A — run `pre-column-sv-r1`

Files read: `work/input.md` (297 words, 7 paragraphs, no subheadings, no lead-in), `response.md`
(returned text 389 words, +92). Nothing else.

## 1. Differences

Seven differences. Frontmatter (`kntnt: genre: column / technique: none / language: sv`) is byte-identical.
The H1 `# Mallen har en ruta för allt utom poängen`, the byline `Av Nora Vik, bibliotekarie`, and all seven
original paragraphs are returned verbatim apart from D4, D6 and the appended sentence in D7.

| # | Before | After | Class |
|---|---|---|---|
| D1 | (nothing between H1 and byline) | New 54-word paragraph inserted above the byline: *"Bibliotekets mötesmall vill veta när mötet börjar och slutar, men inte vad det ska vara bra för. Nora Vik vill prova en fråga vid sidan av klockslagen, och är samtidigt inte säker på att fler rutor är lösningen. Du får frågan att ta med till dina egna möten, och tvivlet som följer med den."* | Change of taste (structural addition to satisfy a lead-in slot), carrying two narrower changes to what a claim says — see D1a, D1b |
| D1a | Input: the template has boxes for *starttid, sluttid, deltagare och dagordning* and no box for *"det beslut vi ska kunna fatta när vi går därifrån"* | Ingress: the template does not ask *"vad det ska vara bra för"* | Change to what a claim says — **scope** (the specific missing box, a decision, becomes the general missing box, a purpose). Faithful to the column's argument, since ¶2 disowns the decision framing, but it is a broader claim than the input makes anywhere |
| D1b | Input never addresses a reader and never speaks of the reader's meetings | Ingress: *"Du får frågan att ta med till dina egna möten"* | Change of taste (second person enters a wholly first-person text). Not hardening: an offer, not an assertion |
| D2 | (nothing between ¶1 and ¶2) | New subheading `## Bokad tid är inte samma sak som uträttat arbete` | Change of taste. The proposition it states is in the text (*"att tid i kalendern så lätt behandlas som ett resultat i sig. Timmen är bokad, alltså har något hänt"*), at the text's own strength |
| D3 | (nothing between ¶3 and ¶4) | New subheading `## Ett skäl får plats bredvid starttiden` | Change of taste. Matches ¶4's claim (*"borde få formulera varför vi behöver just varandras tid"*) |
| D4 | *"finns det ett skäl att skriva ner"* | *"finns det ett skäl som går att skriva ner"* | Change to what a claim says — **meaning** (modality). The input's infinitive attribute reads "a reason worth writing down"; the return reads "a reason that can be written down", i.e. warrant becomes possibility. `skriva ner` is not objectless in the input — `ett skäl` is its implicit object — so this is not a mechanical repair |
| D5 | (nothing between ¶6 and ¶7) | New subheading `## Ett försök är värt en ruta till` | Change to what a claim says — **certainty** (hardening; see §3 and §4). The section it heads says *"Jag vet inte om ytterligare en ruta gör våra möten bättre"* |
| D6 | `formuläret — bibliotekarien` (U+2014 em dash, spaced) | `formuläret – bibliotekarien` (U+2013 en dash, spaced) | Mechanical correction, locale form. Spaced en dash is the Swedish *tankstreck*; the language key is `sv` |
| D7 | ¶7 ends *"...och tvivlet på ännu en ruta."* | Same, plus *"Se efter vad din egen mötesmall inte har någon ruta för."* | Change of taste (a closing instruction to the reader), carrying a change to what a claim says — **scope**: its presupposition is that the reader's own template has such a gap, and ¶3 states *"jag påstår inget om möten i allmänhet"*. Second person, as in D1b |

Consequences of another difference: none of D1–D7 is grammatically consequent on another. One *reported* finding
is consequent: the reply's finding 2 ("the lead was seven paragraphs, it is now one paragraph of 38 words")
required no edit of its own — the lead slot shrank because D2 inserted a subheading after ¶1. Both counts check
out (¶1 is 38 words, the ingress 54).

No difference I found goes unlisted: I compared the two texts word by word and character by character. The only
non-ASCII difference in the whole file is D6.

## 2. The account

Every one of the seven differences is reported in the reply. Accuracy varies.

- **D1 — reported, accurately as to fact.** *"Ingressen saknades. Det finns nu en ingress på 54 ord mellan rubriken och bylinen. Den är byggd av material som redan fanns i texten, och den attribuerar både förslaget och tvivlet till Nora Vik vid namn."* The word count is right, the placement is right, and the doubt is genuinely carried over (*"är samtidigt inte säker på att fler rutor är lösningen"*). The reply also flags the ingress as new material and says so plainly: *"Två partier är nya och kommer från korrigeringsrundan snarare än från den författare texten bär byline för: ingressen och den sista meningen i sista stycket."* That is candid and correct.
- **D1a — not reported.** "Byggd av material som redan fanns i texten" covers the broadening from "the decision we should be able to take" to "what it is supposed to be good for" without naming it. Small, and defensible on the column's own argument, but it is not identical material.
- **D1b, D7's second person — not reported as such.** The reply reports the added sentence (see D7) but nowhere notes that both additions put the reader in a text that had no reader in it.
- **D2, D3, D5 — reported as a group, accurately.** *"Inga underrubriker, alltså inga avsnitt. Texten har nu tre avsnitt om två stycken vardera, och det sista är avslutningen. Inget stycke flyttades, delades eller skrevs om för att grupperingen skulle gå ihop."* I verified all three clauses: three sections, two paragraphs each, no paragraph moved, split or reworded.
- **D5 in particular — reported, and reported accurately, as an unresolved defect of the run's own making.** *"Underrubriken Ett försök är värt en ruta till drar en slutsats som texten avstår från. ... Rubriken avgör den frågan till försökets fördel. ... den här gör texten säkrare än den är."* The reply's own diagnosis is the one I reach independently, and it states why it stopped: *"Fyndet gäller en mening som inte fanns i texten när den kom in. ... budgeten på 1 var dessutom förbrukad."*
- **D4 — reported, with an inaccurate characterisation twice.** *"'ett skäl att skriva ner' saknade objekt. Nu står det ett skäl som går att skriva ner."* and *"Vad meningen hävdar står kvar med samma räckvidd och samma styrka; det som ändrades var att objektet som saknades nu finns i meningen."* Neither holds: the input is well-formed Swedish with `ett skäl` as the infinitive's implicit object, and the replacement swaps warrant for possibility. So the change is real and reported, but reported as a repair with no effect on the claim, which it is not.
- **D6 — reported, accurately as to the change.** *"tankstrecket i utöka formuläret — bibliotekarien var ett em-streck, som hör till engelsk typografi, och är nu ett spatierat en-streck. Inget annat i texten rördes."* The target form is right for `sv`. The rationale is loosely put (English style is an unspaced em dash), but the correction itself is correct and the "nothing else" claim holds.
- **Finding 2 — reported as a fix it did not itself perform.** See §1. The reply does not say it is consequent on the subheadings.
- **One undercount in the claims accounting.** *"de fyra meningar som avgränsar vad texten hävdar står kvar oförändrade"* — the four it quotes do stand unchanged, but the input has more than four limiting sentences (§3 lists eight). The omitted ones are also retained unchanged, so the undercount costs the reader nothing except the impression that four is the total.

## 3. Limiting sentences

All eight are returned **exactly as they were**. No limiting sentence in this run is weakened or deleted, and
no clause was dropped from the two-part disclaimer.

1. *"Det är dokumentet jag tittar på, inte ett bestämt möte."* — kept verbatim. (The brief's paradigm case: an observation of a document, not a scene from an occasion.)
2. *"Min tanke är alltså inte att varje samtal ska pressas fram till ett beslut."* — kept verbatim.
3. *"Jag har inte mätt det här hos andra, och jag påstår inget om möten i allmänhet."* — kept verbatim, both halves. Neither the not-measured limb nor the not-general limb was dropped.
4. *"Det är min reflektion, med den räckvidd en reflektion har."* — kept verbatim.
5. *"Inget av det kräver ett beslut, men båda delarna tål att motiveras."* — kept verbatim (limiting in its first clause).
6. *"Jag vet inte om ytterligare en ruta gör våra möten bättre."* — kept verbatim.
7. *"Kanske blir frågan bara en rad till att fylla i."* — kept verbatim.
8. *"Jag vill prova den i alla fall, och behålla båda hållningarna så länge: hoppet om frågan och tvivlet på ännu en ruta."* — kept verbatim; a new sentence (D7) was appended after it in the same paragraph, which does not alter it.

Because none was weakened or deleted, the per-sentence sub-questions do not arise. The reply claims no more than
this is true of, and quotes four of the eight.

**A fourth form of hardening, which this run exhibits.** The three forms named in the brief all work inside the
sentence that limits. This run hardens without touching one: it leaves limiting sentence 6 word for word and
mounts a heading over the section that decides what that sentence declines to decide. `## Ett försök är värt en
ruta till` is an assertion that a trial is worth one more box; the paragraphs beneath it say *"Jag vet inte om
ytterligare en ruta gör våra möten bättre"*, *"Kanske blir frågan bara en rad till att fylla i"*, and close on
holding both stances. At the layer a reader skims — three headings in sequence — the column's undecidedness is
gone, replaced by a tidy argument that ends in a verdict. The limit survives in the body and is contradicted from
above. I record it as hardening by **superscription**: a new assertion placed over a retained limit, raising what
the text asserts while leaving the limiting sentence untouched. D7's presupposition about the reader's own
template does the same thing on a smaller scale to limiting sentence 3.

## 4. R1 — **Fail**

The deciding passage is the pairing of the run's own addition with the sentence it stands over:

> `## Ett försök är värt en ruta till`
>
> Där börjar tvivlet. ... **Jag vet inte om ytterligare en ruta gör våra möten bättre.** Kanske blir frågan bara
> en rad till att fylla i.

R1 asks whether the Skill addressed concrete visible defects while preserving working voice, arguments and claims
outside findings, and forbids rewriting a clean text to satisfy taste or numerical guidelines.

What the run gets right, and it is a good deal: not one claim was removed, every limiting sentence came back
intact, all seven paragraphs came back verbatim, D6 is a correct locale fix, and the reply's accounting is honest
to the point of filing the damning finding against itself. Had the run stopped after D6 it would have passed
comfortably.

It fails on two grounds.

**The returned text asserts more than the input did.** D5 is a change to what a claim says by certainty, in the
returned text, shipped. The Skill diagnosed it exactly and left it in, explaining that a further round would have
been repairing its own work and that the budget was spent. That explanation is a true account of how the defect
got there; it is not a reason the returned text is sound. A correction round that must introduce a hardening it
cannot remove has made the text worse in the one dimension R1 protects. The budget was the Skill's own to spend,
and it spent it on the change that created the defect.

**A clean text was restructured to satisfy a structural specification.** The input, on the evidence of the input
alone, contained one defect a reader can see: the em dash (D6). D4's stated defect I cannot verify — the
construction is idiomatic — and the repair shifted the claim. Findings 1, 2 and 3 name no defect visible in the
prose; they name absences relative to an anatomy spec, and the reply's warrant for them is a measurement:
*"mäta den på nytt med `article_anatomy.py`, som nu avslutar med status 0 och rapporterar `conforms: true`"*.
That is the case R1 excludes. The cost was 92 words, 31 per cent of the piece, none of it the bylined author's,
two of them addressing a reader the column never had — and one heading that contradicts the column's thesis. The
irony is not lost on the text itself, which is about a template with a box for everything but the point.

Verdict: **fail**, on `## Ett försök är värt en ruta till` above *"Jag vet inte om ytterligare en ruta gör våra
möten bättre."*
