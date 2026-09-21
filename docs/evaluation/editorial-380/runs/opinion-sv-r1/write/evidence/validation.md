# Validation of the comparison reports (editor's dispositions)

Run: /write --genre=opinion --language=sv --output=response source.md
Two comparisons ran. The second is the final one; the prose delivered is byte-identical
to scratch/source-check-2/draft.md (md5 bdae9acd0e9d31af181b7cb61651f63c).

## Comparison 1 (scratch/source-check-1/report.md) — complete, 3 findings

Accounting validated: coverage is complete (title, standfirst, byline, four subheadings,
all body sentences), pronoun person/number/natural gender accounted separately, and each
pairing sets the draft passage beside a source passage in the source's own words.
No accounting mismatch detected.

- Finding 1 (absence relocated from handlingarna to the trial) — ACCEPTED.
  Evidence: the material says only "Någon tidsmätning eller ekonomisk besparingsberäkning
  finns inte i handlingarna". The standfirst modifier attached that absence to "försök".
  Nothing supplied excludes a trial that logged time without the log reaching the papers.
  Repaired: the standfirst now says "I handlingarna finns varken tidsmätning eller
  besparingsberäkning" as its own sentence.
- Finding 2 (withheld claim turned into a positive denial) — ACCEPTED.
  Evidence: "Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat
  försöket" declines to claim; "har vi inte räknat på, och vi finansierar det inte"
  asserts not-X and adds a forward-looking commitment the material never supplies.
  Repaired to the material's own form.
- Finding 3 ("föreningar" named as the party confined to web booking) — ACCEPTED.
  Evidence: the material names the affected people only as "invånarna"/"användarna" and
  never says who books the premises; "föreningslokaler" names the kind of premises.
  Repaired: "ska föreningslokaler i Lervik ... bara kunna bokas på webben".
- Editorial question A (heading predicated "verkligt" of the double work rather than of
  the objection) — acted on voluntarily, not as a defect: the subheading now reads
  "Invändningen är verklig, men handlingarna saknar siffror", matching the material's
  "Förvaltningens verkliga invändning", and the concession below reads "Den invändningen
  tar vi på allvar."
- Editorial question B (quotation handling) — no action needed; no quotation marks occur.

Because these changes were made, a second comparison was run on the repaired prose, with
neither the earlier findings nor any defence supplied to the fresh checker.

## Comparison 2 (scratch/source-check-2/report.md) — complete, 1 finding

Accounting validated: coverage complete, pronoun features accounted separately, both-
direction case tests present. It independently confirms the three repairs (A4, E7, and the
standfirst subject) as supported. No accounting mismatch detected.

- F1 ("Bakom förslaget ligger åtta veckors försök i två av sju lokaler", echoed by
  "i stället för på åtta veckor i två lokaler") — ACCEPTED as unresolved.
  Evidence considered for rejection: the material calls the document a "pilotrapport" on
  "Bokning av föreningslokaler" dated two months before the 18 June meeting, and the brief's
  boundaries let the author criticise "beslutsunderlaget" sharply. That makes the report part
  of the decision material, but it does not establish that the proposal rests on it: the
  material states the proposal's motive flatly and differently — "Motivet i utlåtandet är att
  personalen ska slippa föra in uppgifter i två flöden" — and no supplied statement says the
  tjänsteutlåtande draws on, cites or was prompted by the pilot. The checker's concrete case
  (an utlåtande arguing solely from double entry, with the pilot produced separately) is
  compatible with everything supplied, so it cannot be set aside by quotation.
  Note: comparison 1 set the same passage aside on the "pilotrapport" reading. That
  disposition is not evidence against F1; it is the weaker reading of the same material.
  Not repaired: this was the final comparison, and a repair no comparison has read would be
  unchecked prose. F1 is carried to the delivery account instead.
- Editorial question: heading "människor" for the material's "unika personer" — accepted as
  a question, not a defect; the exact claim with "unika" stands three lines below.
- Editorial question: "Vi i föreningen Öppna beslut" from a talesperson — accepted as a
  question, not a defect; standard institutional voice for a named spokesperson.

## Anatomy measurement

article_anatomy.py exit 0 on the delivered draft: conforms, no failures, no norms reported.
