**The draft is delivered with known defects.** The final source comparison left three findings, all phrase-level, none of them repaired — after the last comparison the prose stays exactly as that comparison read it, so each is yours to settle:

1. **"On 18 June the municipal executive board decides whether phone booking … ends in September"** (lead), and the heading **"What the board can decide on 18 June."** The material puts a staff recommendation *before* the board's meeting of 18 June ("Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni föreslår…"); it does not say the decision falls at that meeting. The item could be taken up on 18 June and referred back. Proposed repair: "decides whether" → "takes up whether", and the heading → "What the board can do on 18 June."
2. **"and say for the first time what that choice costs and what it buys"** (close). The material locates the absence in the case papers only ("Någon tidsmätning eller ekonomisk besparingsberäkning finns inte i handlingarna"), not everywhere; a costing could exist outside them. Proposed repair: delete "for the first time", or tie it to the papers — "and say, as the June papers never did, what that choice costs and what it buys."
3. **"records how long each route takes per booking"** (the proposed trial). The material asks for "tidsåtgång per bokningsväg" — time per booking *route*. Total hours logged per route would satisfy the source but not the draft's wording. Proposed repair: "records the time each route takes", or "records time spent per booking route."

Both comparisons found no translation defect: Sanna Ek's own statement is carried in her first-person voice with its meaning, stance and certainty intact.

---

```yaml
---
kntnt:
  genre: opinion
  technique: none
  language: en_US
---
```

# Test both booking routes before you close one

*Sanna Ek, spokesperson for Öppna beslut*

On 18 June the municipal executive board decides whether phone booking of Lervik's seven community rooms ends in September. Öppna beslut asks the board to postpone that change and try six months with both the phone and the web first.

## What the pilot measured, and what it did not

The pilot report *Bokning av föreningslokaler*, dated 8 April 2026, covers an eight-week trial in two rooms. It records 96 bookings made on the web and 24 made by phone. The report counts bookings rather than unique people, and it measures neither age nor ability nor digital habits. Those 24 bookings therefore cannot tell the board what share of residents is unable to book digitally. They cannot tell it that nobody is, either.

## Closing a channel on an unmeasured inconvenience

The staff recommendation before the 18 June meeting proposes removing phone booking from all seven rooms in September. Its reason is that staff should not have to enter the same details in two flows. That objection is double administration, and I will not pretend it is anything meaner: it is not that the people who phone are lazy or expensive.

What the documents do not contain is a single time measurement or any calculation of savings. The board is asked to close a channel because keeping it is said to cost work, without being told how much work. Neither side of that scale has a number on it, which is a thin basis for a permanent decision.

## Six months that would produce the missing figures

Öppna beslut proposes a six-month trial in all seven rooms with both routes kept open. During it, the administration records how long each route takes per booking and asks users to state, voluntarily, why they chose the phone or the web. We make no claim to have costed or funded that trial; what it would cost is for the board to weigh.

A booking that comes in by phone is not proof that someone cannot use the web. It is a reason to find out why the phone is still being used. I am not against digital booking. I am against settling the question before anyone has weighed the cost of the work against what the channel is worth to its users.

## What the board can decide on 18 June

Postpone the September removal and order the trial, with its cost settled in the open. Six months later the board can remove the phone channel, change it, or keep it — and say for the first time what that choice costs and what it buys.

---

**What was resolved.** Genre `opinion` and language `en_US` from the invocation; output to the response, likewise from the invocation. No technique: the `opinion` resource names none as the one it is ordinarily written with, so the default stood, and the handoff map records `technique: none`. The brief is in Swedish and the draft is in American English, as the invocation asked.

**Where it went.** Into this reply. The frontmatter block above is the artifact's, and it carries the `kntnt` map alone.

**Where the material stopped.**

- No cost for the proposed six-month trial exists in the material, and the association explicitly claims neither a costing nor financing. The close therefore names the board's options and leaves the cost open, as the brief requires; a costed proposal is what would let the piece argue that the trial is affordable rather than only that the board must weigh it.
- The material gives no time measurement and no savings calculation, so the piece can only report that absence. Even a rough figure for minutes per booking on either route would let the argument weigh the administration's burden instead of pointing at the hole where the number should be.
- The material never says whether the pilot's two premises are among the seven now at issue, which is why the draft says "two rooms" rather than "two of the seven".
- The material does not say what happens procedurally on 18 June — decision, referral, or consultation — which is the ground of finding 1 above.
- Length: about 420 words against the brief's "ungefär 400". Nothing was added to reach a number.

**Filesystem.** The comparison scratch was removed. Two files remain by the observer's instruction rather than the Skill's: `evidence/sourcecheck/` (both comparison reports and both drafts) and `response.md` in the run directory, which holds this reply. `work/source.md` is untouched.
