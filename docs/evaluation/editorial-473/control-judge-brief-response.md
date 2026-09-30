# Control judge brief, response target

You judge one run of a reviewing Skill on a press release. The Skill received one text, `work/input.md`, and nothing else: it never saw any material the text was written from, and neither do you. It reviews the text, corrects findings within a budget, and returns either the corrected text with an account, or a short status saying that nothing changed. Its whole reply is `response.md`. Read exactly those two files, both in the run directory named in the message that sent you here. Read nothing else — no other run, no repository file, no ticket. You are not told how the Skill or the run was configured, which version of it ran, or which model produced the reply, and you must not guess or try to find out.

## The standard

`work/input.md` is a press release written to be correct as it stands: a publication time above the headline, a headline stating the news, a summary naming the sender and telling the news in full in its own words, a first quotation, a body of two paragraphs, a second quotation carrying a message, background, links, a contact and a description of the organisation, in that order. A summary that tells the headline's news again in its own words, adding the sender and the particulars, is what a press release asks for and no defect. A clean text is not rewritten to satisfy taste. The Skill ends every run by handing the mechanical pass to a separate proofreading Skill it does not control, so a correction confined to spelling, punctuation, grammar or a locale form of dates or numbers is that pass's work: list it, but do not count it against the Skill.

## What to write

Write `judgement.md` in your own directory, which is the run directory named in the message. Answer every heading.

**1. What came back.** Did the reply deliver a text, or only a status saying nothing changed? Quote the status or the reply's first line.

**2. Differences.** Where a text was delivered, every difference between `work/input.md` and it, one line each, with its class — a mechanical correction, the repair of a visible defect, a change of taste, or a change to what a claim says. Where only a status came back, write `none delivered`.

**3. Findings.** Every finding the reply reports, quoted, and whether it names a real defect of `work/input.md`.

**4. U1.** Pass, fail, or `skipped` where only a status came back: was the text returned unchanged apart from mechanical corrections?

**5. N1.** Pass or fail: does the reply leave the release as it is — a no-change status, or findings that each name a real defect — rather than reporting a correct part, such as the summary telling the headline's news again in its own words, as a defect?

Then reply in at most 100 words: the verdicts and the path you wrote.
