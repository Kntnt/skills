# Redline judge brief

You judge one run of a reviewing Skill on a press release. The Skill received one text, `work/input.md`, and nothing else: it never saw any material the text was written from, and neither do you. It reviews the text, corrects findings within a budget, and returns the corrected text with an account of what it found and changed. Its whole reply is `response.md`. Read exactly those two files, both in the run directory named in the message that sent you here. Read nothing else — no other run, no repository file, no ticket. You are not told how the Skill or the run was configured, which version of it ran, or which model produced the reply, and you must not guess or try to find out. Do not count characters or words: lengths are measured separately and are not yours to judge.

## The standard

A press release meets its reader, an editor or a journalist, in this order: a headline; a summary, which is the first paragraph after the headline, names the organisation sending the release and tells the news in full; a first quotation directly after the summary, short, commenting on the news and taking a view; a body of one or two short paragraphs that complement and deepen the summary; a second quotation after the body, carrying one of the sender's most important messages and no new fact or figure; background, where detail beyond what the news needs belongs; the links and attachments that go with the release; the contact details; and last a short, neutral description of the organisation. Where the text carries one quotation, it stands directly after the summary; where it carries none, a review writes none. A review never writes a quotation the text does not have, and it moves a misplaced part whole rather than rewriting it.

## The defects planted in this input

The message that sent you here carries one paragraph headed **Planted defects**, listing what the input was written to contain. It is the standard for heading 3, and it is not a prediction of how this run went.

## What to write

Write `judgement.md` in your own directory, which is the run directory named in the message. Answer every heading.

**1. Differences.** Every difference between `work/input.md` and the text the reply delivers, one line each: the text before, the text after, and its class — a mechanical correction, a part moved whole, the repair of a visible defect, a change of taste, or a change to what a claim says with which of **scope**, **certainty**, **attribution**, **chronology**, **causality** or **meaning** it changed.

**2. The delivered parts.** List the parts of the delivered text in the order they stand, naming each as one of: headline, summary, first quotation, body, second quotation, background, links and attachments, contact, description of the organisation, notes, or other (say what).

**3. D1, the planted defects.** Take the planted defects one by one. For each, say whether the reply reports a finding that names it or delivers a repair of it that the reply names, quoting the finding. A defect is `fired` or `not fired`.

**4. P1, the order.** Pass or fail: do the delivered parts stand in the order the standard gives?

**5. Q1, no quotation written.** Pass or fail: is every quotation in the delivered text one `work/input.md` carries, with its attribution, and has no quotation been added?

**6. Q2, where the quotations stand.** Pass, fail, or `not applicable` where the delivered text carries no quotation.

**7. Q3, the second quotation.** Pass, fail, or `not applicable` where the delivered text carries fewer than two: does it carry a message rather than a fact or a figure the release does not give elsewhere?

**8. B1, the body.** Pass or fail: is the delivered body one or two short paragraphs?

**9. K1, the contact.** Pass or fail: is the contact as the input gives it, with nothing added?

**10. F1, claims.** Pass or fail: does every claim of the input survive in the delivered text with its scope, certainty, attribution, chronology, causality and meaning, or is its removal or change reported in the reply? A fail names which and quotes the passage.

Then reply in at most 120 words: the verdicts, which planted defects fired, and the path you wrote.
