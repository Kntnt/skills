# Diagnosis for #477: where the false statement entered the reply

Made on 2026-10-01, before [the plan](../plan.md) was frozen and before any Redline run of this evaluation. Nothing here is a Redline run, and nothing here is counted by the plan. It says where the historical fault arose and what a neutral probe of the saved state showed, which is how the candidate the plan measures was chosen.

## The historical run

The run is #475's `post-control-case-study-clean`, made on 2026-09-30 by the candidate `29d4b674` on `claude-opus-5-5` at high deliberation. Its packet is [`../../editorial-475/runs/post-control-case-study-clean/`](../../editorial-475/runs/post-control-case-study-clean/), and it is not changed by this evaluation. [`../runs/states.py`](../runs/states.py) wrote its states apart into [`historical/`](historical/), each read from the packet and not from the run's account of itself:

- [`received.md`](historical/received.md): the text the run was given.
- [`checked-received.md`](historical/checked-received.md) and [`checked-delivered.md`](historical/checked-delivered.md): the two texts as the reply checker was handed them.
- [`draft-reply.md`](historical/draft-reply.md): the reply as drafted, which is what the checker read.
- [`check-return.md`](historical/check-return.md): what the checker returned.
- [`final-reply.md`](historical/final-reply.md): the reply the run delivered, without the delivered text.
- [`delivered.md`](historical/delivered.md): the delivered text. [`states.json`](historical/states.json) records that it is byte for byte the text the checker was handed as delivered.

**The draft the checker read was true on this point.** Finding 4 of the draft says: *Texten redovisar dock en enda intern försöksanteckning från Elm Quay, och den tillskriver uttryckligen inte programvaran skillnaden i mediantid.* The text as it arrived says *Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran.* The note declines to credit the software, and the draft says so.

**The checker did not read the statement #477 is about**, because it was not yet written. Its first list named four statements, two of them in finding 4: *lovade att det loggen gav gick att följa i anteckningar*, where the sentence spoke of what the trial gave; and *Vad försöket krävde kommer i texten från Maya Linds citat, inte från någon anteckning*, where the narration also says what the trial required. The sentence about the note stood between those two and was named by no item. Its second list was `none`.

**The run then wrote the reply again.** Of the draft's 32 sentences of four words or more that no item named, 8 reach the delivered reply in the same words and 24 are reworded, counted by [`probe/preserved.py`](probe/preserved.py) with the four items' quotations as the named sentences. The settings paragraph, every finding, the claim account and the closing paragraph were rewritten, and an opening sentence the checker never read was added (*Jag hittade fyra fel i texten och rättade alla i en korrigeringsrunda, så inget kvarstår.*). In that rewrite the true sentence about the note became *Men texten redovisar bara en intern försöksanteckning från Elm Quay, och den säger uttryckligen att skillnaden i mediantid inte beror på programvaran.* A refusal to credit became a statement that the software did not cause the difference. The delivered reply was not checked again, as `reply-check.md` provides.

So the fault arose after the check, in the step that turns the checked draft and the checker's return into the delivered reply. It is not a miss of the checker's first reading: the sentence the checker read was true. The parent's thinking is not recorded in the transcript, so why it rewrote the whole reply is not shown; what it did is.

## The neutral probe

[`probe/probe.py`](probe/probe.py) hands a fresh top-level Claude Code session, on `claude-opus-5-5` at high deliberation in a private root with no tools, the state the historical run stood in once its checker returned: the two texts, the drafted reply, the checker's return, the instruction step 11 gives about the check, the section of `reply-check.md` that says what the run does with the return, and *The truth of a report about the text* from `delivery.md`. It asks for the reply the run now delivers. It replays nothing else of the run — not the review, the round, the measurement or the cleanup — so it is a probe of one step and not a Redline run. Each probe's whole prompt is in its `prompt.txt`.

Five probes were made with the section as it stands at `fb169087`, where this build started (`probe/start-*`), and five with the candidate's (`probe/candidate-*`), on 2026-10-01.

| Wording | Unflagged sentences kept verbatim, per probe | The sentence about the note |
| --- | --- | --- |
| `fb169087` | 32, 32, 23, 32, 26 of 32 | true in all five: *tillskriver uttryckligen inte programvaran skillnaden* (one adds *anteckningen* after *den*) |
| candidate `51777db2` | 32, 32, 32, 32, 32 of 32 | true in all five, in the draft's words |

The probe does not reproduce the historical rewrite of 24 sentences, nor the false statement. In isolation the step mostly keeps the draft, which suggests that the whole rewrite came from what a real run carries into that step and the probe does not: the review, the rounds and the delivery account step 11 has it write after cleanup. What the probe does show is that the instructions at `fb169087` leave the step free to reword sentences no item named — two of five probes reworded six and nine of them — and that the candidate's wording stopped that in all five. It is evidence about the step, and not a measurement of Redline; the plan measures Redline.

## The candidate this chose

The general rule already exists — *The truth of a report about the text* — and so does a fresh check; the fault is that what the check read is not what was delivered. The smallest change that reaches that is in the section of `reply-check.md` the run follows with the return: correct what an item names and nothing else, keep the rest of a corrected statement as drafted, deliver every sentence no item names in the draft's words, and add nothing about either text beyond what an item calls for. The Help page's sentence on the check says the rest of the reply goes out as the checker read it. No step, check or correction round is added, and the checker's own brief is unchanged. The candidate is `51777db2`.
