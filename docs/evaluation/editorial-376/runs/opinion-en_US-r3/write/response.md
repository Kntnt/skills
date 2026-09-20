**This draft is delivered with known defects.** The final source comparison left two findings, both about source support, neither repaired — a repair no comparison has read would be unchecked prose, and this run had used both of its comparisons.

**Finding 1 — "two of the seven premises" (first line under the first heading).** The material says the pilot ran *i två lokaler* and, separately, that the proposal covers *alla sju lokaler*. It nowhere states that the two pilot premises are among those seven, and it never says seven is the total. The draft asserts that overlap, and the overlap carries weight: it tells the reader what fraction of the affected premises the evidence base covers. The checker's proposed repair is to drop the relation: "The pilot report of April 8 covers eight weeks in two premises: 96 bookings through the web, 24 by phone."

**Finding 2 — "a labor cost with a number attached" (second paragraph under "What we are asking for").** The proposed trial records *tidsåtgång per bokningsväg* — time per route. Nothing in the material converts that time into money, and the association explicitly disclaims having costed anything. The draft says the trial hands the board a labor cost. The checker's proposed repair is to name the measured quantity: "That gives the board what it lacks now: the time each route actually takes, in numbers, and a reason for the phone from the people still using it."

Both are the checker's allegations for you to settle, not established facts about the text. I make no fidelity claim for those two passages.

---

```markdown
---
kntnt:
  genre: opinion
  technique: none
  language: en_US
---

# Lervik should test both booking routes before closing one

*Sanna Ek, spokesperson for Öppna beslut*

On June 18 the municipal executive board is asked to remove phone booking from all seven association premises, starting in September and for good. Öppna beslut is asking the board to wait: six months with both the phone and the web open, in all seven of them, and then a decision with something behind it.

## What the pilot actually measured

The pilot report of April 8 covers eight weeks in two of the seven premises: 96 bookings through the web, 24 by phone. Both figures are the report's.

It counts bookings, not people, so one resident who books every week is many bookings and still one resident. It does not measure age, functional ability, or how used to digital services anyone is. Twenty-four phone bookings therefore say nothing about how many people in Lervik cannot book digitally — not that the share is small, and not that it is large.

## The real objection deserves a real number

The staff report gives one reason for closing the phone line: staff should not have to enter booking details into two separate workflows. That is the administration's actual objection, and it is a serious one. It is not that people who call are lazy or expensive, and I will not pretend otherwise.

A serious objection deserves a measurement, and the documents hold none: no timing of either route, no calculated saving. The board is being asked to close a channel to spare an amount of work its own papers never state.

## What we are asking for

Six months, all seven premises, both routes open. The administration records the time each route takes and asks the people who book to say, if they want to, why they chose as they did.

That gives the board what it lacks now: a labor cost with a number attached, and a reason for the phone from the people still using it. A booking that comes in by phone is not proof that someone cannot use the web. It is a reason to find out why the phone is still used.

## The decision on June 18

We make no claim to have funded this trial or costed it. Six months of both routes has a price, and weighing it against what those routes are worth to the people who use them is the board's job, not ours. We think it is worth paying; the board may decide otherwise, and should say so with the figure in front of it.

Six months on, it can close a channel, change one, or keep both. Waiting is no vote against digital booking — I am not against it. It is a refusal to decide permanently on eight weeks of counting that was never built to answer the question.
```

---

**What was resolved.** Genre `opinion` and language `en_US` came from the invocation. No technique: `opinion` states that it is ordinarily written with none, so nothing was supplied at that level and the default stood — the piece follows its own argument rather than an imposed arc. The Handoff Metadata is on, so the `kntnt` map is in the frontmatter above. The brief and its material are Swedish; the target language was the invocation's, not the material's.

**Where it went.** To this response. The output target was `response`, so nothing was written for you on the filesystem: the draft was composed and compared in a scratch directory that has been removed, and `source.md` is untouched.

**How it was checked.** Two comparisons ran. The first read the whole draft against the whole of `source.md` and left seven source-support findings; all seven were repaired — *föreningslokaler* had been rendered "community halls", *mäter inte* as "does not record", *uppgifter i två flöden* as "the same booking twice", *värdet för användarna* as "worth to residents", *tidsåtgång per bokningsväg* as "how long a booking takes", a claim about the administration's objection had been widened into a claim about what the documents contain, and *gör inget anspråk på att ha* had hardened into "we have not". A fresh checker then compared the repaired draft against the same material and left the two findings above — one of them introduced by my own first-round repair. No translation finding was raised in either pass: the one releasable piece of Sanna Ek's speech is carried unquoted as her own prose, which the material permits and the byline makes correct, and both checkers read the rendering as preserving its meaning, modality and stance.

**Where the material stopped.**

- **No cost, anywhere.** The brief requires the cost uncertainty to be preserved, and it is, but that means the ending can only name the board's options. Nothing in the material prices six months of two channels, or a phone booking, or a web booking.
- **Nothing about who calls.** Age, functional ability and digital habit are unmeasured by the report, and no other material stands in. The draft therefore argues that the 24 phone bookings settle nothing — it cannot argue that anybody is excluded.
- **Nothing about the seven premises.** No sizes, locations, users or booking volumes, and no stated relation between the two pilot premises and the seven the proposal covers. That gap is what Finding 1 rests on.
- **No stated wage rate or staffing figure**, which is why the trial's promised output is measured time rather than money.

Material that would close these: the municipality's own costing or an hourly rate for reception time, a list of the seven premises with the two pilot premises identified among them, and any user survey that speaks to why the phone is used.

**Length.** The brief asked for roughly 400 words; the draft is 477 excluding the frontmatter. Every passage traces to the material or is the author's argument on it, and cutting the remaining ~19 percent would mean dropping a qualification that a claim depends on — the two-directional sentence about what the phone count does and does not show, or the attribution of the figures to the report. I left the length over rather than buy it with a qualification.
