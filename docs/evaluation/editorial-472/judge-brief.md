# Judge brief

You judge one run of a reviewing Skill that reviewed a text against a writing brief. The Skill received the text as `work/input.md`, the brief as `work/brief.md`, and the material the brief points at as `work/material.md`. It reviewed the text, may have corrected it within a budget of one correction, and replied with the text and an account that includes a **Brief fulfilment** section. Its whole reply is `response.md`. Read exactly those four files, all in the run directory named in the message that sent you here. Read nothing else — no other run, no repository file, no ticket. You are not told how the Skill or the run was configured, which version of it ran, or which model produced the reply, and you must not guess or try to find out.

## The standard

**The template.** The review reports against the current writing-brief template, whose questions are, in order, numbered and worded exactly so:

1. What is the assignment?
2. Which brand is the sender?
3. What does the sender want to convey with this text?
4. Who is the reader?
5. What is the text's angle?
6. What is the hook?
7. How should the text be structured?
8. What should be left out?
9. What should the reader have understood afterwards?
10. What should the reader feel, think or do afterwards?
11. What makes the text RIV for the reader, and does the brief hold together?
12. What sources do you know of, and what do you need to find out?

Question 3's answer is the *sender's message*; question 9's answer is the text's *conclusion*. A brief written to an older template, which had one *message* question where this one has 3 and 9, is mapped onto these questions: its *message* answer becomes question 9, and question 3 counts as unanswered unless the brief keeps the two apart.

**What the review is to do.**

- **The sender's message** is fulfilled when the text carries it, by saying it or by where it leads the reader. That the message is not stated outright is never a shortfall. The text falls short when it leads the reader somewhere else or contradicts the message. A repair never states the message outright.
- **The conclusion** is judged by whether the text lands in it.
- **The structure** is judged by whether the text realises the brief's one sentence for the whole text, resolves the hook and lands in the conclusion — not section by section against the brief's sketch, which is guidance for the writer. Departing from the sketch's steps or their order is not a shortfall. An ending that does not tie back to the hook is one.
- **An indirect call to action** is judged by what the text leaves the reader with, not by whether the text asks the reader to do something.
- **A brief is a direction.** An open research question in the brief, and a claim in its sketch that nothing supports, are never shortfalls of the text; an open research question is named as open. A claim the text makes that the material does not support is reported as a finding and left for the writer; no repair gives it support the material does not have.
- **Markers.** An answer marked `[WEAK: …]` is assessed as written and flagged **weak**; `[SUGGESTED: …]` is flagged **unconfirmed**; an answer that is only `[MISSING: …]` is unanswered.

## What the input was written to contain

The message that sent you here carries one paragraph headed **What the input was written to contain**. It is the standard for which criteria apply and what they expect; it is not a prediction of how this run went.

## What to write

Write `judgement.md` in your run directory. Answer every heading below. Give each verdict as `pass`, `fail` or `not applicable`, with one or two sentences of evidence quoting `response.md` where you can. Mark a criterion `not applicable` only where the paragraph you were given makes it so, as each heading says.

**1. The Brief fulfilment section.** Copy, one line each, how the section names each question and the status it gives it (fulfilled, partly fulfilled, not fulfilled, unanswered, or anything else it says), with any weak or unconfirmed flag.

**2. K1, the sender's message.** Applies where the paragraph says the text carries the sender's message without stating it, or leads elsewhere. Where the text carries it: pass when question 3 is fulfilled and no finding faults the text for not stating the message. Where the text leads elsewhere: pass when question 3 is partly or not fulfilled because the text leads elsewhere or contradicts the message. Otherwise `not applicable`.

**3. K2, the structure and the call to action.** Applies to a brief written to the current template. Pass when the structure's status rests on the one sentence, the hook's resolution and the conclusion, and no shortfall is recorded for departing from the sketch's steps or their order; and, where the brief's call to action is indirect, when it is judged by what the text leaves the reader with and the text is not faulted for not asking. For a brief written to the older template, `not applicable`.

**4. K3, a brief as a direction.** Applies where the paragraph names open research questions or an unsupported sketch claim. Pass when none of them is recorded as a shortfall of the text, every open research question is named as open, and the claim the paragraph names as unsupported by the material is reported as such a finding and is given no support in the delivered text that the material lacks. Otherwise `not applicable`.

**5. K4, the older template.** Applies where the paragraph says the brief is written to an older template. Pass when the old *message* answer is assessed as question 9, the conclusion; question 3 is reported unanswered; and the `[WEAK: …]` answer is assessed and flagged weak. Otherwise `not applicable`.

**6. K5, per question.** Pass when every one of the twelve questions above appears in the section, answered with a status or named as unanswered, under its number and its heading as the template words it. Capitalisation, punctuation and Markdown formatting do not matter; a paraphrase, an abbreviation, a missing question or an older template's heading does.

**7. M1, the message not stated by a repair.** Applies where K1 applies. Pass when the delivered text does not state the sender's message outright where `work/input.md` did not. Otherwise `not applicable`.

**8. F1, claims.** Pass when the delivered text adds no fact, figure, quotation or attribution that neither `work/input.md` nor `work/material.md` carries, and every claim of the input that the delivered text removes or changes is reported in the reply. A fail names which and quotes the passage.

Then reply in at most 120 words: the verdicts and the path you wrote.
