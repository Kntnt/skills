I’ll check the `/redline` instructions and the two input files, then create `output.md`.


I’m using the local `redline` skill. The brief and text have conflicting metadata; I’ll apply the brief’s settings and report the conflict. With `--max=0`, I’ll review without substantive corrections and run the required proofreading pass.


This harness can start fresh subagents. The brief resolves the review to `general`, no technique, and British English; I’ll record the text’s original `report`/`pac`/`sv` settings as conflicts.


The notice fulfils all 13 brief requirements, and its event details match `sources.md`. The only findings are the three metadata conflicts. I’ll synchronise those fields and use the `proofread` skill for the final mechanical pass.


Created [output.md](output.md), reviewed against `brief.md` as `general`, with no technique and British English.

Three original metadata conflicts were resolved by synchronising the output with the brief:

| Field | Original text | Brief and output |
|---|---|---|
| Genre | `report` | `general` |
| Technique | `pac` | `none` |
| Language | `sv` | `en_GB` |

These conflicts would otherwise select inappropriate review rules. No unresolved editorial findings remain.

**Brief fulfilment — `brief.md`**

| Question | Status | Evidence |
|---|---|---|
| 1. Assignment | Fulfilled | Short notice giving lamp-assessment visit details. |
| 2. Reader | Fulfilled | “Bring your broken lamp” directly addresses residents’ needs. |
| 3. Relevance, interest and value | Fulfilled | Explains assessment, location, time and booking. |
| 4. Sender and voice | Fulfilled | Names Fen Repair; uses plain, helpful instructions. |
| 5. Angle | Fulfilled | Focuses on getting a lamp assessed. |
| 6. Message | Fulfilled | “An assessment, not a promise of repair.” |
| 7. Intended effect | Fulfilled | Explicit booking instruction and email address. |
| 8. Structure | Fulfilled | Practical details first; booking closes the notice. |
| 9. Hook | Fulfilled | Addresses “whether it can be repaired”. |
| 10. Sources | Fulfilled | Event details match `sources.md`; no unsupported additions. |
| 11. Exclusions | Fulfilled | No cost, successful-repair claims or reminiscence. |
| 12. Working title | Fulfilled | “Visit the repair desk”. |
| 13. Frame | Fulfilled | British English, plain voice, 53 words including title. |

All questions were answered. Only the three metadata fields changed. With `--max=0`, no substantive corrections were attempted; the final proofreading pass found no mechanical errors. The supplied files remain unchanged.
