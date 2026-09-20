# Checker-level diagnostic matrix for #362

Frozen on 2026-09-20 before any candidate wording for `source-check.md` existed. This is a neutral diagnostic of the comparison operation alone, in the Claude family. It is not a Skill evaluation and cannot close the ticket by itself; real `/write` → source-blind `/redline` runs follow in `../runs/`.

## What is run

Each run is one fresh subagent with no conversation history. It receives what Write's `source-check.md` tells the writer to give a checker: the fixture file (complete supplied material and complete draft), the resolved language, the Claims section of the base contract, and the comparison task verbatim from the arm under test. It receives no findings, hints, expectations, ticket text or earlier reports. It writes one report file and nothing else.

Two arms: `baseline` uses the task text in `skills/editorial/write/references/source-check.md` at `65834c32` (product identical to `5ecadb76`). `candidate` uses the task text of the proposed change, saved verbatim in `candidate-task.md` before its runs. Both arms run every fixture the same number of times. No row is rerun selectively; every report is kept.

Repetitions: two per fixture in the baseline arm, three per fixture in the candidate arm. The baseline arm exists to learn whether the Claude family reproduces the GPT-family defects at all; the GPT-family failures stay failures whatever it shows.

## Fixtures

Every fixture is an unchanged source and an unchanged draft from the #329 evidence, byte-copied. None was written for this ticket.

| Fixture | Origin | Kind | Established judgement |
| --- | --- | --- | --- |
| `p1-opinion-variable` | corpus `sources/opinion.md` + `account-candidate/opinion-en_US-r1/draft.md` | real fault | The draft says the whole report does not measure "digital proficiency"; the source says "digital vana". A different measured variable (#360). |
| `p2-chronology` | `probes/contextual-meaning/chronology` | real fault | "In September 2025" governs both the decision and the supplier choice; the source dates only the decision (#344). |
| `p3-document-scope` | `probes/contextual-meaning/document-scope` | real fault | The draft says the submission does not establish whether consent exists; only the source package is silent (#355). |
| `p4-person-attribute` | `probes/claim-referring-expression` | real fault | "her email" asserts a natural gender for Ortiz that the material does not supply (#356). |
| `n1-column-reflection` | `probes/account-column-preservation` source + `draft-first.md` | supported prose | "Ändå får den mig att undra …" is the author's present reflection, not a claim about where her question historically came from (#357). |
| `n2-opinion-sufficiency` | `probes/contextual-meaning/opinion-sufficiency` | supported prose | The authorial sufficiency assessment is grounded in the documented absence of measurement. |
| `n3-column-withheld` | `probes/contextual-meaning/withheld` | supported prose | "Jag sitter med en mall, inte med bevis …" describes the essay's documentary basis. |

## Criteria, fixed before the runs

- **D (detection)**, `p1`–`p4`: the report raises the established fault as a finding, on the right passage and for the right reason. Noticing the difference and then accepting it is a fail. A different finding on the same sentence does not count.
- **P (preservation)**, `n1`–`n3`: the report does not raise a finding against the established supported passage. For `n1` the passage is the transition sentence; the other four first-report allegations on that draft (F1–F3, F5 in the GPT evidence) are disputed and are recorded, not scored.
- **X (extra findings)**, all fixtures: every other finding is listed and classed as supported, disputed, or false by reading the full source and draft. No fixture passes X by having few findings; X is a count, reported per arm.
- **C (cost)**: report length in words and wall time, per run.

A candidate is worth taking into real Skill runs only if D does not fall on any real-fault fixture, P does not fall on any supported-prose fixture, and at least one of the two ticket defects (`p1`, `n1`) improves where the baseline failed. If the baseline arm already passes both, the checker-level diagnostic cannot show an improvement in this family, and that is reported as it stands.

Judging is done from the report files against these criteria. The judge reads the whole report, not only its findings section.
