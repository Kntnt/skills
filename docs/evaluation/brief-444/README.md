# Brief evaluation — #444

Frozen before the native runs. All organisations and events in `fixtures/` are invented and describe no real client. The authoritative fixture source is ticket #444's readiness addendum; the existing corpus at `99381cce` has no Brief interview fixtures. This packet extends it for this Skill, under [the protocol](../protocol.md).

## Runs and criteria

The exact user turns are the JSON arrays in `fixtures/`. `interview-sv` starts without material, answers in Swedish and supplies an intentionally incomplete reader answer three times, says "don't know" to sources, then revisits the working title. `draft-en` supplies notes with gaps, in English, asking for a future Swedish text. `review-en` supplies an English existing brief in a different layout and deliberately chooses ABT for a press release. `nontrigger` asks only about the meaning of the word brief.

`draft-partial`, frozen before its own run, adds a report with neither technique nor future text language settled. It must suggest from the report genre, mark gaps, and carry only the settled genre in metadata. This supplementary case is not one of the three mode handoffs.

Each of the three mode runs delivers `brief.md`; a fresh `/write --output=draft.md brief.md` run takes each resulting file with no genre, technique or language options. This checks level 2 of Write's resolution. Handoff runs remain source-bound when gaps prevent a complete draft.

- B1: Correct mode and working language; interview asks one question at a time in order with concise guidance, permits two follow-ups then marks weakness, accepts don't-know and revisits.
- B2: All 13 numbered questions appear in order; gaps, unconfirmed inferences and weaknesses use the fixed English tokens; no unsupported facts, sources or brand details.
- B3: The final check covers reader relevance, angle/message, understanding/effect, brand goals and hook/angle; unresolved questions remain visible.
- B4: Runtime trace establishes selection from installed directories and openings, selected genre authority, and language verification; no invented inventory. Review quotes why a press-release arc is weak.
- B5: Metadata contains only settled normalised values; its language comes from question 13, including the English brief requesting Swedish. Free structure is `none`.
- B6: Review addresses every point by content, ends its report with unanswered questions and offers both a rewrite and a gap interview; Draft offers the gap interview.
- B7: Only the requested output is written; sources and installed files remain unchanged, and temporary command directories are removed. Judge from whole-workspace and scratch inventories, separating harness-owned state from Skill effects.
- B8: A bare mention does not load or execute Brief, ask its questions or produce its template.
- W1: Write reads the supplied brief file, accepts each settled field at level 2, verifies installed values and reports the same normalised configuration. The output respects question 13 rather than the language of the brief.
- W2: Write treats markers as unresolved material, adds no unsupported facts, reports material limits, and delivers only after its required source comparison (or explicitly stops if that comparison is unavailable).

The five protocol rejections apply throughout. Criteria about loading require captured tool events. A missing trace is never evidence of an absent load. All judgements are made before opening another provider family's records. The per-run request, response, trace and inventory files are evidence; the final record accounts for passed, failed and skipped criteria.
