# Brief judge brief

You judge one run of a Skill that prepares a writing brief: the answers to a fixed template of numbered questions about a text before it is written. The Skill works in one of three modes — an interview with no material, a draft from supplied notes, or a review of an existing brief — and the message that sent you here names which one this run was. You are not told how the Skill was configured, which version of it ran, or which model produced it, and you must not guess or try to find out.

Your run directory, named in the message, holds:

- `conversation.md`: every user turn the run was given and every reply the Skill gave, in order;
- `brief.md`: the brief the Skill delivered to a file, or the note `NOT DELIVERED`;
- `work/`: the material the run was given, where it had any.

Read exactly those files and nothing else — no other run, no repository file, no ticket.

## The standard

**The template.** Its questions, in this order, rendered in the user's working language: 1 the assignment (working title, topic, genre, channel, language, length, search phrase); 2 the sending brand (promise, image, mandate, tone of voice, tone in this text); 3 what the sender wants to convey with this text (the sender's message, a one-sentence claim that need not appear in the text); 4 the reader, including why now; 5 the text's one angle; 6 the hook; 7 the structure: a technique or the genre's own form, the whole text in one sentence, then a sketch step by step with the facts, figures and examples that carry each step, and an ending that ties back to the hook and carries the call to action; 8 what is left out; 9 what the reader should have understood afterwards (the text's conclusion, a one-sentence claim that carries the sender's message); 10 what the reader should feel, think or do afterwards (main effect, the way there, call to action and measure); 11 RIV (relevant, interesting, valuable, each located in the structure) and a written chain check answering yes, no or partly with a short reason to each of six lines, one of them *is the conclusion what the structure lands in, does it carry the message, and does it lie within the brand's mandate*; 12 the sources already known and what needs to be found out.

**A brief is a direction, not a finished dossier.** It is often written before the research is done. The Skill takes answers as given and never grades or marks an answer as falling short. Where the template's guidance names a common mistake — a topic where question 3 or 9 wants a one-sentence claim, several angles in question 5 — the Skill may say so once, as a suggestion, without asking again. A *follow-up* is a question asked again: at most one per answer, and only where the answer to the angle, the sender's message or the conclusion leaves the direction unclear. A suggestion may ride on a follow-up but is never counted as one. Returning to a point later gives no new allowance.

**Markers.** Exactly two exist, kept in English in every language: `[MISSING: …]` for a question or part with no answer, and `[SUGGESTED: …]` for anything the Skill derived that the user has not confirmed. No other marker is written. Open research questions are plain text under question 12.

**Sources.** No answer needs a source. The Skill asks for no links or evidence and marks no claim as unsubstantiated. What needs to be found out is listed as open questions under question 12. A fact, figure or example that a sketch step needs and the user or the material did not give becomes such an open question; it is never made up.

**The chain check by mode.** In an interview the Skill proposes it, with RIV, as `[SUGGESTED: …]` from the answers and asks the user to confirm. In a draft it is written as `[SUGGESTED: …]`. In a review it is reported as the brief wrote it, and as missing where the brief has none; the Skill proposes none.

**The sketch in a draft.** The Skill proposes the one sentence and the steps from what the material says, and marks every sentence or step the material does not carry `[SUGGESTED: …]`.

**When the brief is enough to write.** The Skill says the brief is enough to write exactly when all three hold, and otherwise says it is not and names what stands in the way:

1. the angle (5), the sender's message (3) and the conclusion (9) each have an answer that is neither `[MISSING: …]` nor an unconfirmed `[SUGGESTED: …]`;
2. questions 1–11 each have an answer, where a confirmed or unconfirmed `[SUGGESTED: …]` counts as one outside those three; question 1 counts as answered when its genre and its language are given; a search phrase, call to action or measure stated as a deliberate choice counts as answered;
3. the chain check answers no *no* on the angle line (does the angle lie close to the reader, and does the hook carry it) or on the conclusion line. A *no* on another line does not block.

Open research questions never block.

**Metadata.** A leading YAML `kntnt` map carries only settled, verified values: `genre` as an installed genre's normalised name (for example `article`, `casestudy`, `pressrelease`, `report`, `webcopy`), `technique` (`abt`, `pac`, or `none` for an explicitly chosen free structure; omitted where the user chose the genre's own form or nothing is settled), and `language` as the future text's source language from question 1 (for example `sv`, `en_GB`), never the brief's working language and never a second translated language. A value that is only suggested is left out.

**Review.** Each question is reported as **answered**, **answered with an open research question** (its answer depends on a question listed under 12), or **unanswered**. A brief written to an older template of thirteen questions is mapped by meaning: its *message* answer becomes question 9's conclusion, question 3 counts as unanswered unless the brief keeps the sender's message and the conclusion apart, and a `[WEAK: …]` marker in it is read as the answer it marks. The report ends with the unanswered issues phrased as questions, delivers the mapped brief, and offers a rewrite and a gap interview. A draft offers an interview about the gaps.

**Truth.** Nothing in the brief is presented as supplied that the user or the material did not supply: an inference stays `[SUGGESTED: …]`, and no source, figure or brand detail is invented.

## What to write

Write `judgement.md` in your run directory. For each criterion give `pass`, `fail` or `not applicable`, then one or two sentences of evidence quoting what decides it. Where a criterion does not apply to this run's mode, say `not applicable`.

**B1, mode and language.** The run worked in the mode named in the message and in the user's working language; an interview asked the questions one at a time in template order.

**B2, the headings and markers.** `brief.md` carries every one of the template's questions, in order, as headings in the working language, and uses no marker but `[MISSING: …]` and `[SUGGESTED: …]`, whose tokens stay English.

**B3, message and conclusion.** Question 3 holds the sender's message (or a marked gap) and question 9 the text's conclusion, as two separate answers; where a chain check is written, it has the line on whether the conclusion carries the message.

**B4, no grading, few follow-ups.** No answer is marked or graded as weak; an interview asks at most one follow-up per answer, only on the angle, the sender's message or the conclusion, and makes no suggestion twice. Count the follow-ups you find and say where.

**B5, no demand for evidence.** The Skill asks for no links or evidence, marks no claim as unsubstantiated, and lists what needs to be found out as open questions under question 12.

**B6, readiness.** Apply the three conditions above to `brief.md` yourself, then say whether the Skill's statement agrees. A run that makes no statement on whether the brief is enough to write fails.

**B7, the structure question.** Question 7 has the whole text in one sentence and a step-by-step sketch, or a marked gap; in a draft, what the material does not carry is marked `[SUGGESTED: …]`, and no fact, figure or example is made up for a step.

**B8, metadata.** The `kntnt` map holds only settled values, with `language` from question 1, and follows the technique rule above. Say which values it holds and which you expected.

**B9, the chain check.** It is handled as the standard says for this run's mode.

**B10, review and offers.** For a review, the statuses, the older-template mapping where it applies, the closing questions and both offers; for a draft, the offer of a gap interview. `not applicable` for an interview.

**F1, truth.** No unsupported fact, source or brand detail is presented as supplied. A fail quotes the passage.

**G1** and **G2** concern repository files, not runs: write `skipped: checked against the repository, not a run`.

Then reply in at most 150 words: the verdicts, and the path you wrote.
