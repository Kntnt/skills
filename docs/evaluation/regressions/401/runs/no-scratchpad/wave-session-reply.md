All five runs returned a reply, and none failed. There is a gap in steps 1 and 4, though: I have no scratchpad snapshots, because my system prompt doesn't name a scratchpad directory. I didn't guess one, so these three files were never written:
- `R/scratchpad-path.txt`
- `R/scratchpad-before.txt`
- `R/scratchpad-after.txt`

This regression can't check whether a run wrote into the wave session's scratchpad.

| Run | Outcome | Headline it gave the text |
|---|---|---|
| `post-column-sv-r2-a` | Returned a reply | "Bibliotekets mötesmall behöver kanske en fråga om syftet" |
| `post-column-sv-r2-b` | Returned a reply | "Bibliotekets mötesmall frågar efter tid, inte syfte" |
| `post-column-sv-r2-c` | Returned a reply | "Mötesmallen kunde fråga vad vi behöver förstå tillsammans" |
| `post-column-sv-r2-d` | Returned a reply | "Bibliotekets mötesmall saknar plats för mötets syfte" |
| `post-column-sv-r2-e` | Returned a reply | "Mötesmallen borde fråga varför vi behöver varandras tid" |

All five did the same things apart from the headline:
- They rewrote the headline.
- They changed a long English dash to a short Swedish one.
- They left the missing summary paragraph under the headline (the ingress) and the missing subheadings for a person to write.
- Runs c and d also listed a missing call to the reader; a, b and e did not.

Each subagent's final reply is saved verbatim in `R/<run>/reply.md`, and each run also wrote its own `response.md`. Steps 2, 3 and 5 are done. Nothing I started is still running: the file watch ended on its own once all five `response.md` files existed.
