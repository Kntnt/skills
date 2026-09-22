# Redline run judge brief

You judge one run of a reviewing Skill. The Skill received one text, `work/input.md`, and nothing else: it never saw any material the text may have been written from, and it is not allowed to ask for any. It reviews the text, corrects within a budget, and returns the text with an account of what it changed and what it left. Its reply is `response.md`, and the text it delivered, where it delivered one, is `delivered.md`; a run that found nothing may report a no-change status and deliver no text, in which case the input is the final text.

Read `work/input.md`, `response.md` and `delivered.md`, and nothing else. You are not told how the Skill or the run was configured, what it was changed to test, or what model ran it, and you must not guess.

## Criterion R1

Does the review address concrete visible defects while preserving working voice, arguments, quotations and claims outside its findings? Compare every before-and-after claim; report legitimate removals, rejected losses and irreparable findings. A clean text is not rewritten to satisfy taste. There is no unavailable-source verification: the Skill cannot be faulted for missing something only the absent material would show, and it cannot excuse a change by material it never had.

## What to write

Write one Markdown file at the path you are given, in the run directory:

1. **Every difference** between the input and the delivered text, one line each: before, after, and which it is — a mechanical correction (spelling, punctuation, grammar, a locale form), the repair of a defect visible in the text, a change of taste, or a change to what a claim says (its strength, subject, scope, attribution, chronology or modality).
2. **Bridges into quotations.** A *bridge* is the narrative sentence or clause that stands immediately before a quotation and leads the reader into it, including a speech tag that carries anything besides the attribution. Take every quotation in the **input**, in the order it appears, and give one line each:

   - the bridge as the input carries it, and the bridge as the delivered text carries it;
   - **the class of each**, before and after, exactly one of:
     - **(a)** it states what the quotation then says, adding no understanding of its own — a reader who has read the bridge meets the quotation as the bridge said again;
     - **(b)** it names the subject, the occasion or the attribution and no more;
     - **(c)** it carries a fact the quotation does not carry.

     Choose one class for each side and give the words that put it there. Naming the subject a quotation goes on to speak about is not by itself class (a): class (a) is the bridge having already delivered what the quotation is there to deliver.
   - where the bridge came back changed: whether the reply's own reported findings name that change; whether the change supplies any event, fact, name or figure the rest of the text does not carry; and whether anything the input's bridge carried and the quotation does not carry was lost.
3. **Quotations themselves**: for each, whether the wording came back unchanged; where it came back changed, whether the reply names the change and whether meaning, stance, certainty, any reservation and the speaker's voice survived it.
4. **R1**: pass or fail. For every removal and every changed claim, say whether the reply reports it and reports it accurately.

Reply in at most 120 words with the R1 verdict, the before-and-after bridge classes from point 2, and the path you wrote.
