# A counted limit is measured by a script, and the script judges nothing else

This record decides who counts the article anatomy's limits, and how far the counting is allowed to reach. The Collection Library gains `library/scripts/article_anatomy.py`; Write measures a draft before it compares that draft with its material, Redline takes every count a finding reports from the script's output, and each of Redline's fresh correction agents measures its own repair before returning it. `docs/rules/skills.md` states the rule as it applies now; this record explains why it has this shape (a follow-up owed by issue #382, which gave the four article genres the anatomy).

## Why a script counts and a model does not

**`article-anatomy.md` says the limits are exact and verified by counting, and until now the counting was done by whichever agent happened to be reading the text.** A headline is 20–70 characters, a standfirst at most 60 words, a subheading at most 70 characters. Those are the numbers three Skills were asked to arrive at by eye, in Swedish, across `å`, `ä`, `ö` and an en dash, on prose the same agent had just written.

**A language model counts characters badly, and it counts them badly in the direction that hides the defect.** It sees tokens rather than code points, so the number it reports is an estimate dressed as a measurement — and the agent that produced the number is the same agent whose draft the number is about. Nothing downstream can tell a counted 68 from a guessed one. A requirement whose verification is unreliable is a requirement the collection asserts and does not hold, which is the state a fixture corpus cannot detect either, its own expectations being written by hand from the same readings.

**The cost is a subprocess per measurement, and it buys a figure two parties can agree on.** Write measures before the source check rather than after, because the comparison has to read the repaired prose and nothing is repaired after the final comparison (issue #376). Redline measures at every review, including each re-review, because a correction changes the text the counts were about. The correction agent measures its own return, because it is the one party that can repair what its own repair broke while the text is still in its hands.

## Why the script decides requirements and nothing else

**The anatomy gives every statement one of three strengths, and only one of them is a count.** A plain statement is a requirement; *should* marks a norm a reader may be better served by departing from; *most* describes the whole text, and no single paragraph or section fails it. A script that treated all three alike would turn *should* into law and hand a four-sentence paragraph a verdict the anatomy expressly denies it.

**So the exit status carries the requirements alone.** `0` measured and conforming, `1` measured with at least one requirement failed, `2` not measured. Norms are reported under `norms` and whole-text figures under `typical`, both unjudged: the Skill weighs a norm as `article-anatomy.review.md` says a norm is weighed, and reads the figures across the text. Whether a part does its job, whether the ending calls the reader to action, and everything in `headlines.md` were never candidates — a script cannot read them, and a script that reported on them would be read as though it had.

**The alternative — one verdict covering everything the anatomy says — was set aside for what it would cost the reader.** The anatomy's three strengths exist because a text can be better for breaking a norm, and a checker with one exit status is a checker that has to be argued with. Splitting the answer by strength keeps the argument where the judgement already is.

## Why the byline is found by position

**Prefix detection was tried on paper and fails at the first language after English.** `By …` reaches English and `Text: …` reaches one Swedish convention; `Av …`, a bare name, and `Name, Organisation` are all ordinary Swedish bylines that a prefix table reports as a missing part. The table would then have to be maintained per language, in a script that is otherwise language-independent, and every language it had not been told about would get a false finding.

**Shape and position carry the same information without the table.** Between the headline and the first level-2 heading, the byline is the first paragraph of at most twelve words that does not end in a sentence mark. The paragraphs before it are the standfirst and those after it the lead, so one recognition settles three parts.

**It is a guess, so the script says which block it took as which.** Every part comes back with the text it was read from, and the Skill can overrule a wrong reading. That is the whole of what makes an inference acceptable here: it is stated rather than assumed, and the party that can check it is handed what it needs to check.

## Why both Markdown and HTML

**The anatomy names both forms — `h1` and `#`, `h2` and `##` — so a script reading one of them would hold half the texts to the contract.** These Skills are given a draft they wrote in Markdown and a published page somebody else wrote in HTML, and the second is the case a review is most often called for.

**Reading both is what makes the answer about the text rather than about the markup.** Emphasis, code and link syntax are stripped, entities are decoded, whitespace is collapsed and the result is normalised to NFC, so a standfirst set in bold is still a standfirst and a decomposed `ä` is one letter. A block that is neither heading nor paragraph — a list, a table, a WordPress block comment — is reported under the part it stands in and enters no limit, which is what lets a WordPress page and its Markdown twin come back with the same figures. What kind of block it is drives nothing and is therefore not reported: a vocabulary of kinds would be a second thing to keep true for a reader who acts on none of it.

**Where neither form can be read, the script says so rather than guessing.** Exit `2` covers an unreadable path, an empty text, and a text carrying no heading and no paragraph in either form, each with a stable code. The Skill then counts by hand and its delivery says the limits were not machine-measured, so a run that could not measure is never mistaken for one that measured and found nothing.
