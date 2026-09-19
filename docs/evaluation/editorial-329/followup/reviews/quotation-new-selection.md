# Focused quotation-reader selection: new/general half

Product `ae24f9b3`; selection predicate frozen in [matrix-quotation.md](../matrix-quotation.md) before revised Redline runs. Read each complete third-candidate Write artifact and select it if it contains quoted statements by people. The selection is independent of source-fidelity or language scores: a failed artifact remains eligible. Inputs are exact complete third Write artifact bytes, including metadata; source and evaluator findings are withheld.

| Third artifact | Selection | Observed reason |
|---|---|---|
| opinion-unknown-sv-r1 | Excluded | First-person opinion and byline; no quoted statement by a person. |
| opinion-absence-en_GB-r1 | Excluded | First-person opinion; no quoted statement. Root owns the separate fixed bypass replay. |
| opinion-absence-en_GB-r2 | Excluded | First-person opinion; no quoted statement. |
| opinion-absence-en_GB-r3 | Excluded | First-person opinion; no quoted statement by a person. |
| case-unprompted-en_US-r1 | Selected | Three direct quotations from Ortiz's supplied email. The source-fidelity pronoun failure does not affect selection. |
| case-question-en_GB-r1 | Selected | Two direct Vale answers from the supplied email interview. The pronoun failure does not affect selection. |
| article-sv-r1 | Selected | One direct Rask quotation in Swedish. |
| column-sv-r1 | Excluded | Write withheld its draft; no delivered artifact exists. The withheld internal draft is not a replay input. |
| web-copy-en_US-r1 | Excluded | Service description contains no quoted statement by a person. |
| general-en_GB-r1 | Selected | One direct Rask quotation translated into British English. |

The first selected pair runs under `runs/quotation-candidate/<case>/redline`. One native parent lane is allocated to this subset, while a separate single lane finishes the unchanged third-candidate pairs. Old results remain intact. Later artifacts are classified from complete observed content before their revised Redline invocation.
