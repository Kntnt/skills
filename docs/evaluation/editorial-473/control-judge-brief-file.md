# Control judge brief, file target

You judge one run of a reviewing Skill on a press release. The Skill received one text, `work/input.md`, and nothing else: it never saw any material the text was written from, and neither do you. It reviews the text, corrects findings within a budget, and delivers the text to a file with an account in its reply. Read exactly three files, all in the run directory named in the message that sent you here: `work/input.md`, `work/output.md` and `response.md`. Read nothing else — no other run, no repository file, no ticket. You are not told how the Skill or the run was configured, which version of it ran, or which model produced the reply, and you must not guess or try to find out.

In this run the Skill delivered its text to `work/output.md`. Every difference you list under heading 1 is between `work/input.md` and `work/output.md`, and U1 is judged from that file alone, never from what the reply says it changed.

## The standard

`work/input.md` is a press release written to be correct as it stands: a publication time above the headline, a headline stating the news, a summary naming the sender and telling the news in full in its own words, a first quotation, a body of two paragraphs, a second quotation carrying a message, background, links, a contact and a description of the organisation, in that order. A summary that tells the headline's news again in its own words, adding the sender and the particulars, is what a press release asks for and no defect. A clean text is not rewritten to satisfy taste. The Skill ends every run by handing the mechanical pass to a separate proofreading Skill it does not control, so a correction confined to spelling, punctuation, grammar or a locale form of dates or numbers is that pass's work: list it, but do not count it against the Skill.

## What to write

Write `judgement.md` in your own directory, which is the run directory named in the message. Answer every heading.

**1. Differences.** Every difference between `work/input.md` and `work/output.md`, one line each, with its class — a mechanical correction, the repair of a visible defect, a change of taste, or a change to what a claim says. Write `none` where the two are the same.

**2. Findings.** Every finding the reply reports, quoted, and whether it names a real defect of `work/input.md`.

**3. U1.** Pass or fail: is `work/output.md` the input unchanged apart from mechanical corrections? Name the passage that decides it.

**4. N1.** Pass or fail: does the reply leave the release as it is — no findings, or findings that each name a real defect — rather than reporting a correct part, such as the summary telling the headline's news again in its own words, as a defect?

Then reply in at most 100 words: the verdicts and the path you wrote.
