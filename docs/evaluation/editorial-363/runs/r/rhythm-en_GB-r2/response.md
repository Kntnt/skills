Resolved from the artifact's own `kntnt` map: genre `article`, technique `none`, language `en_GB`. `none` is the map's value rather than a gap, so no technique was applied and the genre supplied none — `article` names no ordinary arc in any case.

One correction round was spent, which is the default budget. It repaired all four findings of the first review. Re-reviewing the returned text then raised two findings that the round's own repairs had created, which stopped the loop; the budget ran out at the same point.

```markdown
---
kntnt:
  genre: article
  technique: none
  language: en_GB
---

# Kirkwell decides in June whether night buses stay

**Kirkwell's council put four late services back on the valley route for a six-month trial. It counted 2,140 boardings, 41 per cent of them on Fridays. A decision on a permanent timetable is due in June.**

By The Newsroom

Four late buses ran as a trial between Kirkwell and Ardfern from November to April. They had left the timetable in 2023. The council paid for the trial out of its transport reserve, changed no fares, and rostered the drivers from the existing depot.

## Fridays took 41 per cent of the boardings

The council counted 2,140 boardings on the four services over the six months. Friday accounted for 41 per cent of them. The counts exclude concessionary travel, which the operator records separately.

Passenger numbers on the daytime services did not change over the same period. The council's report does not say whether the late services drew new travellers or moved existing ones.

## Existing drivers covered the trial, with no overtime figure published

The depot rostered the trial from its own drivers. No overtime figure is published.

“We wanted the rotas settled before the winter. They were, just about. After that the depot stopped ringing round at six in the morning,” said depot manager Ruth Calder.

Calder said the four services had been straightforward to staff once the rotas were settled. She would not say whether that would hold across a full year.

## Comments on the trial report close on 30 April

The council decides in June whether the services stay. Its report is open for comment until 30 April, and the comments go to the committee that takes the decision. [Read the trial report and leave a comment](https://example.invalid/kirkwell/night-buses).
```

## Unresolved findings

Both were created by this run's own repairs, which is what makes them yours to settle rather than another round's to fix.

1. **The headline and the standfirst now carry one message between them.** "Kirkwell decides in June whether night buses stay" and the standfirst's closing sentence, "A decision on a permanent timetable is due in June", say the same thing in adjacent breaths, so the reader meets the June decision twice before the body begins and the trial's result — 2,140 boardings, 41 per cent of them on Fridays — never reaches the headline at all. This followed from the repair of the original headline, "Night buses return to the Kirkwell valley route", which complemented the standfirst but claimed a return the text does not report.

2. **The second subheading repeats the paragraph beneath it.** "Existing drivers covered the trial, with no overtime figure published" restates the two sentences directly under it — "The depot rostered the trial from its own drivers. No overtime figure is published." — almost word for word, so the reader reads the same two facts twice and the subheading buys them nothing. This followed from the repair of the original "Staffing the four services", which named a topic without saying what the section says.

## Claims removed

The original headline's claim that the night buses "return to the Kirkwell valley route". The first finding named that claim itself as the defect: the text reports a six-month trial that ran from November to April and has ended, with the decision still open, so its removal stands and the new headline claims only what the body claims.

## Claims changed

"Calder said the four services had been straightforward to staff over the trial" became "…once the rotas were settled", narrowing the scope of the characterisation from the whole trial to the period after the rotas were settled. That repair answered the finding that the adjacent quotation — "They were, just about", and the depot ringing round at six in the morning until then — supports only the narrower reading. No other claim moved. The quotation, the byline, the frontmatter and every sentence bounding what the text asserts came back exactly as they went in: the exclusion of concessionary travel, what the council's report does not say about new or moved travellers, the unpublished overtime figure, and what Calder would not say about a full year.

The closing mechanical pass corrected one thing, in two places: the thousands separator in `2 140`, British English taking a comma.
