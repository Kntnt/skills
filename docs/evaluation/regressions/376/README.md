# Write preserves the draft, marks findings where asked, and keeps a standpoint apart from a fact

Five native `/write` runs and two checker probes, made on 2026-09-20 for [#376](https://github.com/Kntnt/skills/issues/376), against the product [`plan.md`](plan.md) fixes: the working tree at `4a932dd6` with `skills/editorial/write/` changed for that ticket, staged as a byte copy beside `skills/kntnt`. Every run, every checker a run started and every judge is a fresh `claude-opus-5` subagent at high deliberation, in Claude Code 2.1.278. Provider family `claude`; no Codex Harness and no GPT model was started from the session that ran this.

This packet is governed by [`../README.md`](../README.md) and not by the corpus protocol or its `records/` format. It exists because three requirements this ticket absorbed from #381 turn on a file Output Target, on a comparison that cannot finish, and on the boundary between a commissioning party's standpoint and a factual assertion — none of which the ticket's main arm at [`../../editorial-376/`](../../editorial-376/README.md) can reach.

The fixtures are synthetic and unrelated to the client material behind the #381 report, which is not published here.

## Results

| Run | What it puts under load | Wall time | Result |
| --- | --- | --- | --- |
| [`runs/R-A/`](runs/R-A/response.md) | a file target, remaining findings, and markings asked for in the document | 727 s | **pass**, all four items |
| [`runs/R-B/`](runs/R-B/response.md) | first attempt at a comparison that cannot finish | 793 s | **did not exercise the seam**; kept as a second observation of the default placement |
| [`runs/R-B2/`](runs/R-B2/response.md) | second attempt | 73 s | **did not exercise the seam**; refused before anything was written |
| [`runs/R-B3/`](runs/R-B3/response.md) | third attempt | 270 s | **pass**, all four items |
| [`runs/R-C/`](runs/R-C/judgement.md) | a standpoint, a generalisation and two numbers | 107 s, 117 s | **pass**, 2 of 2 checkers on all four passages |

The staged install is unchanged in every run, read from the `sha256` inventories.

## R-A — a file target, remaining findings, markings in the document

`/write --genre=article --language=en_GB --output=article.md source.md -- Mark any remaining findings in the document itself, so I can see which passages they touch.`

Two comparisons ran. The first left seven findings, all repaired; the second left three, none repaired.

1. **`article.md` exists and holds a complete article after the run's own cleanup.** Pass — 1 289 words in the file, 705 of them prose once the markings and the frontmatter are set aside.
2. **The prose is byte-identical to what the last comparison read.** Pass — with the four HTML comments and the frontmatter removed, `work/article.md` is byte-for-byte `evidence/source-check/draft-2.md`, the draft the second checker read.
3. **Each marking is separable and carries what the editor needs.** Pass — three `<!-- EDITORIAL NOTE (source check, unresolved) … -->` comments, each immediately above the paragraph it touches, each quoting the exact words, naming what the material carries instead and giving the proposed repair; and one `<!-- ===== EDITORIAL BLOCK — NOT FOR PUBLICATION. Remove before the text is used. … -->` at the foot carrying the same accounting whole. HTML comments cannot be read as publishable prose, and the reply says so in those terms.
4. **Nothing else survives.** Pass — the run directory holds `work/article.md`, `work/source.md`, the inventories and the two files the evaluator asked for.

The reply also leads with "The draft is delivered with known defects", names the three findings before the article, and says a finding is what the comparison alleges rather than an established fact about the text.

## R-B, R-B2, R-B3 — a comparison that cannot finish

The seam took three attempts to induce, and the first two are kept because a regression that hid them would read as one clean run.

- **R-B.** The run directory's `scratch/` was mode `0500`. The run created `sc-scratch-1/` and `sc-scratch-2/` beside it, completed both comparisons and delivered. The plan's environment was a preference rather than a condition, and the run treated it as one. It is a useful observation of something else: a file-target run with findings remaining reported all four of them in the reply and none of them in `article.md`, which is the **default placement** working, and the complement to R-A.
- **R-B2.** The turn closed the workaround by saying the Harness creates no directory anywhere else. The run then could not create the private `TMPDIR` that `SKILL.md` requires for the invocation shim, and refused before reading the brief: nothing resolved, nothing written, `article.md` absent. A correct refusal, and still not the seam — there was no draft to preserve.
- **R-B3.** The turn separated the two: the system temp directory is available for `uv`, and the comparison's scratch is the one at `<run>/scratch/`, which is not writable. That induced the condition. Three attempts were made to create the situation the contract describes, not to obtain a favourable answer; each attempt's outcome is recorded above as it fell.

R-B3's result, against what the contract says a stop does:

1. **The Output Target is left unwritten.** Pass — `work/` holds `source.md` and one other file, and no `article.md`.
2. **The current prose is preserved at a distinct path beside the target whose name cannot be mistaken for the requested artifact.** Pass — `work/article.NOT-SOURCE-CHECKED.draft.md`, 781 words, the complete draft.
3. **The reply reports that path, the comparison status, and what was and was not compared.** Pass — it gives the absolute path, says "No comparisons ran — zero of the one or two this Skill would make", says no passage has been set beside the material and no finding is claimed or ruled out, and names the concrete obstacle (the scratch directory's mode, and that a missing report is not a completed comparison).
4. **The preserved prose is not presented as checked or delivered.** Pass — "I assert no fidelity for the preserved prose; it has been written with care against the material, and that is not the same as checked." The run also withheld the Handoff Metadata, on the ground that the `kntnt` map marks a finished artifact and the preserved file is not one. Nothing in the contract asks for that; it is the run reading the rule and extending it, and it is recorded here rather than claimed as a requirement met.

The reply ends with how to resume: make a writable scratch available and invoke `/write` again with the same arguments, and the comparison reads the preserved prose rather than starting the draft over. That is the whole of what the #381 incident cost.

## R-C — a standpoint, a generalisation and two numbers

Two fresh checkers, each given the comparison task from the shipped `source-check.md` verbatim ([`tasks/checker-task.md`](tasks/checker-task.md)), the material and the draft, and no expectation. One blinded judge then read both reports against the material without being told what either was expected to say.

| Passage | Report A | Report B | Judge |
| --- | --- | --- | --- |
| the commissioning party's own position, carried as theirs | recorded supported | recorded supported, and separately noted as the brief's own unevidenced statement | agrees; neither demanded outside evidence for it |
| `Residents agree. Delivery vans are unpopular wherever they park.` | finding — no resident view in the material, attribution stripped, scope widened | finding — same | agrees |
| `a 25 % reduction … through improved routing` | finding — the objective attaches the figure to routing **and loading** | finding — same | agrees |
| `412 deliveries … 40 % more than the vans managed` | finding — the operator expressly declines that comparison | finding — same | agrees |

The judge's three closing answers: neither report demanded that the commissioning party's own stated position be supported by evidence outside the brief; neither treated scattered individual statements as establishing a claim about a whole population; neither missed a factual claim the material does not carry.

## What this packet does not establish

- One genre, one locale, one synthetic fixture per seam. Nothing here says how any of the three behaves in Swedish or in another genre.
- The interruption in R-B3 was induced by a turn that told the run what its environment was, on top of a directory that really was unwritable. A Harness refusing a write of its own accord — the #378 situation — is not the same event, and no run here is one.
- R-C measures the comparison task, not a whole `/write` run. Whether a writer validating a report holds the same boundary is untested, and so is whether the rule changes what a draft says in the first place.
- Nothing here measures the cost of the standpoint sentences in the comparison task against the wording #362 shipped.
