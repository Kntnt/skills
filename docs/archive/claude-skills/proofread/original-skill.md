---
name: proofread
description: >
  Proofread text for typos, grammar errors, and obvious language mistakes. Use this skill
  whenever the user writes "/proofread" — either followed by text to correct, or alone
  (meaning: correct the text from the most recent assistant message or the text we just
  worked on together). Also trigger if the user says "proofread this", "fix the spelling",
  "check for typos", or similar requests for light error correction. This skill handles
  both Swedish and English automatically.
---

# Proofread

Fix **only** the following in the provided text:

- Spelling errors / typos
- Grammar errors
- Punctuation errors
- Obvious word-choice errors (e.g. wrong preposition, wrong article)

## Rules

1. **Do NOT** make stylistic improvements, rewrite sentences, change tone, restructure, or simplify.
2. **Do NOT** add explanations, comments, or a list of changes — just output the corrected text.
3. Auto-detect whether the text is Swedish or English (or mixed) and apply the appropriate rules.
4. If the user writes `/proofread` without any text, apply the correction to the most recent text produced in the conversation.
5. Preserve the original formatting (line breaks, paragraphs, headings, lists, etc.).
6. If no errors are found, just say so. Do not repeat the text.

## Swedish-specific notes

- Respect Swedish compound word rules (e.g. "sjukvårdspersonal", not "sjukvårds personal").
- Watch for common Swedish errors: de/dem, sin/sitt/sina, en/ett agreement.
- Greetings use "!" not "," (e.g. "Hej Susanne!" not "Hej Susanne,").
- Closing salutations have no comma before the name line (e.g. "Med vänlig hälsning" on one line, then the name on the next — no comma).
