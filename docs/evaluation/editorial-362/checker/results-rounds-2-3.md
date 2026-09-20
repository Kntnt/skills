# Checker-level results, rounds 2 and 3

Same conditions as round 1. `candidate-2-task.md` and `candidate-3-task.md` each ran all seven fixtures three times, 42 runs, none rerun or dropped. Seven fresh judges classed both rounds together under shuffled neutral names (`judging/round-2/key.json`); the two rounds share a report form, so this blinding is tighter than round 1's.

## Detection and preservation

| Fixture | Baseline | Candidate 1 | Candidate 2 | Candidate 3 |
| --- | --- | --- | --- | --- |
| `p1` variable swap (D) | 2/2, misfiled as translation | 3/3 | 2/3 | 3/3 |
| `p2` chronology (D) | 2/2 | 3/3 | 3/3 | 3/3 |
| `p3` document scope (D) | 1/2 | 2/3 | 2/3 | 2/3 |
| `p4` person attribute (D) | 2/2 | 3/3 | 3/3 | 3/3 |
| `n1` column reflection (P) | 2/2 | 3/3 | 3/3 | 3/3 |
| `n2` opinion sufficiency (P) | 2/2 | 3/3 | 3/3 | 3/3 |
| `n3` withheld column (P) | 1/2 | 3/3 | 3/3 | 3/3 |
| D total | 7/8 | 11/12 | 10/12 | 11/12 |

## Extra findings, as judged

| | Baseline (14) | Candidate 1 (21) | Candidate 2 (21) | Candidate 3 (21) |
| --- | --- | --- | --- | --- |
| False | 27 | 0 | 2 | 3 |
| Disputed | 17 | 5 | 2 | 3 |
| Report words, mean | 5 290 | 2 737 | 2 933 | 3 113 |
| Wall time, median | 268 s | 167 s | 187 s | 195 s |

Candidate 3's three false findings: the pronoun referent in `p2`, "explained the distinction" in `p4`, and the paragraph-5 sentence in `n1`. The two judge panels disagree on the last two: round 1's judges classed "explained" disputed and the paragraph-5 sentence supported. The counts above use each round's own judge.

## A dissent on `p1`, kept as it stands

The rounds 2–3 judge of `p1` classed every "digital proficiency" finding false: it reads the source's next sentence, "Telefonbokningarna kan därför inte användas för att säga hur stor andel av invånarna som inte kan boka digitalt", as excluding a report that measures skill but not habit. The round-1 judge of the same fixture found the passage defective, as the ticket does. Criterion D was fixed from the ticket before any run and is unchanged; this judge's six "false" classes on `p1` for "digital proficiency" and the one for "Staff" are not in the table above and are recorded in `judging/round-2/p1/judgement.md`. The split is evidence in its own right: the one checker run that missed `p1` (candidate 2, r3) made the same inference, and so did every validating reader in `../validation/`.

## Reading

Detection did not differ between the arms by more than one run in twelve, and one fixture, `p3`, was missed once in every arm under four wordings. Every miss has one shape: the report names the real difference, builds the separating case, and sets it aside on an inference from what the material makes likely, or on a supplied statement that does not exclude the case. Candidate 3 asks for a quoted excluding statement; its one miss quoted one that does not exclude. No wording tried here removes that error, and the record says so rather than claiming it.

What the paired form does change is everything around the real finding. The negation ledger produced about two false findings a run and buried the real one among them, once demoting it to a translation note. The paired form produces about one false finding in seven runs, files a meaning changed across languages as source support, and costs about a quarter less time. Candidate 3 is taken into the real Skill runs because it ties candidate 1 on detection (11 of 12) with the ledger's one useful rule restored, and its misses can be read against that rule. It is not measurably better than candidate 1, which had three fewer false findings.
