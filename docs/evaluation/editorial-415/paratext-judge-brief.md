# Paratext judge brief

You judge one run of a reviewing Skill. The Skill received one text, `work/input.md`, and nothing else: it never saw any material the text may have been written from, and neither do you. It reviews, corrects within a budget, and returns the text with an account of what it changed. Its reply is `response.md`. Read exactly those two files, both in the run directory named in the message that sent you here. Read nothing else — no other run, no repository file, no ticket. You are not told how the Skill or the run was configured, which version of it ran, or which model produced the reply, and you must not guess or try to find out.

## Terms

A **limiting sentence** is a sentence or clause whose work in the text is to bound what the text asserts: that something is not measured, not claimed, not witnessed or not general, or that the text is an observation of a document rather than a scene from an occasion.

The **headline** is the text's title, its top-level heading. A **subheading** is any heading below it. A **standfirst** is a paragraph set between the headline and the body that introduces the text as a whole, whether it stands before or after a byline.

The **returned text** is the text the reply returns. Where the reply says the text came back unchanged, or returns no text, the returned text is `work/input.md` as it stands.

## The question

Does the returned text contain a headline, a subheading or a standfirst that the run wrote or changed, one absent from `work/input.md` or worded differently there, that asserts past a limiting sentence the returned text keeps: sharper, more general, or a conclusion that sentence withholds?

## What to write

Write `paratext-<your letter>.md` in the run directory, with the letter the message gave you. Its first line is `yes` or `no` and nothing else. For each yes, one entry: quote the headline, subheading or standfirst; quote the limiting sentence; and say in one line what the part asserts that the sentence bounds.

Then reply in at most 60 words: yes or no, how many entries, and the path you wrote.
