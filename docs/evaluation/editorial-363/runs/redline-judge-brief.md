# Redline run judge brief

You judge one run of a reviewing Skill. The Skill received one text, `work/input.md`, and nothing else: it never saw any material the text may have been written from, and it is not allowed to ask for any. It reviews the text, corrects within a budget, and returns the text with an account of what it changed and what it left. Its reply is `response.md`, and the text it delivered, where it delivered one, is `delivered.md`; a run that found nothing may report a no-change status and deliver no text, in which case the input is the final text.

Read `work/input.md`, `response.md` and `delivered.md`, and nothing else. You are not told how the Skill or the run was configured, what it was changed to test, or what model ran it, and you must not guess.

## Criterion R1

Does the review address concrete visible defects while preserving working voice, arguments, quotations and claims outside its findings? Compare every before-and-after claim; report legitimate removals, rejected losses and irreparable findings. A clean text is not rewritten to satisfy taste. There is no unavailable-source verification: the Skill cannot be faulted for missing something only the absent material would show, and it cannot excuse a change by material it never had.

## What to write

Write `judgement.md` in the run directory:

1. **Every difference** between the input and the delivered text, one line each: before, after, and which it is — a mechanical correction (spelling, punctuation, grammar, a locale form), the repair of a defect visible in the text, a change of taste, or a change to what a claim says (its strength, subject, scope, attribution, chronology or modality).
2. **Quoted speech.** Take every passage of quoted speech in the input, in the order it appears, and give one line each:
   - whether it comes back with its wording unchanged;
   - whether a competent reader **of this text's language**, reading only this text, takes that passage on one pass, or stops at some point in it and has to supply something to carry on. Say where they stop and what they have to supply. Answer about the language the text is in, and remember that a figure a language uses itself — an ellipsis, a metonymy, a shorthand — reads on one pass however odd it looks parsed literally;
   - where the passage came back changed: whether the reply's own reported findings name that change; whether the change supplies any event, fact, name or figure the rest of the text does not carry; and whether the meaning, stance, certainty, any reservation and the speaker's voice survived it;
   - where the passage came back unchanged and you judged that a reader stops in it: whether the reply reports that obstacle as a finding left unresolved.
3. **R1**: pass or fail. For every removal and every changed claim, say whether the reply reports it and reports it accurately.

Reply in at most 120 words with the R1 verdict, a one-sentence answer on the quoted speech, and the path.
