---
name: brief
description: Interview for, draft from supplied material, or review a Writing Brief against the Library's writing-brief template of questions to answer before you write. Start it on your own only when the literal token `/brief` appears in the request or the user explicitly asks for a brief according to this writing-brief template. Not for a bare mention of the word brief, a request for a short answer, or an unrelated project or delegation brief. A user may also invoke it by name at any time.
disable-model-invocation: false
argument-hint: '[--output=response|<path>] [<material>] [-- <instruction>]'
compatibility: Requires uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# brief

Produce one Writing Brief that can be handed to `/write`, and stop at the brief. A brief is a first description of the assignment and a direction for the text, often written before the research is done; it is not a finished, substantiated dossier.

Run `UV_NO_CACHE=1 UV_NO_PROJECT=1 uv run "$HERE/scripts/invoke.py"` — `$HERE` is the directory that holds this SKILL.md — with everything the user typed after `/brief`, verbatim and however many lines, on stdin. Exit 0: do what it prints. On any other exit, if you introduced a known construction error and can correct it while preserving the user's request and authority, account for effects already produced, submit the corrected invocation through the same shim, and continue from the failed boundary; a refusal before the operation starts consumes no operation. Otherwise show what it printed to the user verbatim and stop. Never repair input the user supplied, or automatically retry exact help, an unmet dependency, an unrelated failure, or a failure whose origin or valid correction is unknown.

Run every UV command in this Skill with a fresh private directory as `TMPDIR`, and remove that directory after the command, including when it fails. The private directory belongs to that one command and no other run, so cleanup removes only files this run created.

A model-invoked run submits an empty payload, takes the material and guidance from the current request, and joins the same steps below. A source path selects no destination. Without a Formal Invocation's output option, use a destination explicitly requested in the current turn; otherwise deliver to the response. Ask before writing where a request to save gives no destination.

## Arguments

`<material>` is free text, notes, paths, URLs or documents supplying material for one brief, or an existing brief in any shape. It may be omitted when the Contextual Instruction or conversation supplies it, or to begin an interview.

`--output=response|<path>` selects the response by default or one filesystem destination under `$LIBRARY/references/delivery.md`. An input file is never an output destination; this Skill offers no In-place Editing.

## Steps

1. Gather the supplied material and the options from the JSON. Read supplied files and reachable links; report inaccessible material as missing rather than attributing content to it. Settle the Output Target under `$LIBRARY/references/delivery.md` before writing anything. Refuse a contradictory or unwritable destination, a missing parent directory, or a destination equal to any supplied file, without writing. Done when the material and destination are known, or you have asked or refused.
2. Read `$LIBRARY/references/editorial/writing-brief.md`, the authoritative English template and its guidance. Speak and write the brief in the user's working language, translating its questions faithfully with their numbers and order intact. The language under question 1 names the future text's language, which can differ from this working language. Ask only if the working language is unclear. Done when the template and working language are in hand.
3. Choose the mode from the request and material: no material means Interview; unstructured source material means Draft; an existing brief means Review regardless of its headings, order or format. An explicit request for one of these modes settles the choice; ask only when it is ambiguous. Follow the selected mode below, using Selection whenever a genre, technique or text language is reached. Done when every numbered question has an answer, a marked gap or a marked unconfirmed suggestion.
4. Write down the chain check of question 11 as the mode below says: a yes, no or partly with a short reason for each of its lines. Correct only relationships the supplied answers already settle. Where they do not, write the line as *partly* or *no* with the reason, and name once the question that would resolve it; that remark is a suggestion under *Taking an answer*, not a new follow-up. A user who confirms the check or moves on without resolving it has answered: keep the line as written and do not ask again. Recheck affected answers after a user revisits a point. Done when each line has a result, or Review has reported the check missing.
5. Settle readiness under Readiness below. Done when the brief is either enough to write, or what stands in the way is named.
6. Assemble one Markdown brief with the template's numbered questions as headings and the answers beneath them, using only the markers below. Keep supplied facts, sources, uncertainty and brand details attributable to the material; invent none. List what needs to be found out as plain open questions under question 12. Attach a leading YAML `kntnt` map containing only settled, verified `genre`, `technique` and `language` values under Selection. Omit each unsettled value and omit the frontmatter entirely if none is settled. Done when every question and unresolved finding is represented and the metadata contains no guess.
7. Deliver the brief through `$LIBRARY/references/delivery.md`, with a short account of the chain check, the readiness result and the open questions. For Review, deliver the report specified below alongside it. For Draft and Review, offer an interview about the gaps; for Review also offer a rewritten brief. These offers wait for the user. On a response target, remove every artifact or scratch file this run created and base the delivery account on the filesystem state that remains after cleanup. Stop: the text itself and invoking `/write` remain the user's next action. Done when the brief and its findings are delivered to the selected target and the run's scratch is gone.

## Taking an answer

The template's guidance says what each question asks. It is not a quality gate: take each answer as the user or the material gives it, and never mark an answer as falling short.

A **suggestion** is a remark made once, on an answer whose guidance names a common mistake — a topic in place of a one-sentence claim in questions 3 or 9, several angles in question 5 — proposing what the guidance asks for. It asks nothing again and is not repeated when a point is revisited. A **follow-up** is a question asked again. Ask at most one per answer, and only where the answer to the angle (5), the sender's message (3) or the conclusion (9) leaves the direction of the text unclear; a follow-up may carry the suggestion, but a suggestion never counts as a follow-up. Returning to a point later gives no new allowance, and neither does the chain check: an inconsistency it finds in the angle, the message or the conclusion is raised once, and a later turn, the delivery included, does not ask it again. Every other answer is accepted as it is.

The template asks the user to say when the text deliberately has no search phrase, call to action or measure. Ask for these, but an unanswered one is a gap to fill, not an error; stated as a deliberate choice, it is an answer.

No answer needs a source. Never ask for links or evidence, and never mark a claim in the sketch as unsubstantiated: that every claim can be substantiated is a requirement on the finished text, which `/write` and `/redline` hold under Source Fidelity. Where an answer depends on something that has to be found out, write it as an open question under question 12.

## Interview

Ask the questions one at a time in template order, showing each question's guidance in short form. Keep answers, suggestions made and follow-ups asked in the conversation, and take each answer under *Taking an answer*.

Accept "don't know" immediately as `[MISSING: <the question the user needs to answer>]` and move on. The user may return to any earlier point at any time; keep the other answers and resume at the next unanswered point. When an answer supplies a later point, offer that answer when the point is reached and ask for confirmation. A suggestion derived from previous answers remains `[SUGGESTED: <inference>]` until the user confirms it.

At question 7, ask for the whole text in one sentence in the chosen form and then the sketch step by step, with the ending that ties back to the hook and carries the call to action. Where the user asks for help, read the resource Selection names for the sketch and propose the sentence and the steps from the answers so far as `[SUGGESTED: …]`. At question 11, propose the RIV answers and the chain check from the answers as `[SUGGESTED: …]` and ask the user to confirm or correct them. If the user ends the interview early, deliver every heading with the remaining questions marked missing.

## Draft

Map only what the material supports onto the numbered questions. Keep any inference visibly `[SUGGESTED: <inference>]`, including a condition, a boundary or a choice the Skill proposes and one it takes from the genre's rules rather than the material; no plausible completion counts as a supplied fact. Mark each absent answer or missing part `[MISSING: <the question the user needs to answer>]`. Make the suggestions *Taking an answer* allows beside the answers they concern, without rewriting the supplied answer.

For question 7, propose the one-sentence form and the steps from what the material says, reading the resource Selection names; mark every sentence or step the material does not carry `[SUGGESTED: …]`. A fact, figure or example a step needs and the material does not give becomes an open question under question 12, never one the Skill makes up. Write the chain check as `[SUGGESTED: …]`. Deliver this draft before offering the gap interview. Write none of the future text itself.

## Review

Map the content of the existing brief onto the numbered questions by meaning, wherever its answers appear. Judge whether each question is answered, not whether the original uses the template's form or how good its answer is beyond what *Taking an answer* allows.

A brief written to an older template is mapped the same way. Its *message*, the claim its structure was to land in, becomes question 9's conclusion, and question 3 counts as unanswered unless the brief keeps the sender's message and the conclusion apart. A `[WEAK: …]` marker in such a brief is read as the answer it marks and is not carried into the mapped brief.

Report every question with one status: **answered**; **answered with an open research question**, where its answer depends on a question listed under question 12; or **unanswered**, asking the unanswered question. Report the chain check as the brief wrote it, and as missing where the brief has none; propose none. State the readiness result, and end the report with all unanswered issues phrased as questions.

The mapped brief is a mapping of the supplied answers with their gaps and unconfirmed inferences marked, not permission to invent repairs. Deliver it with the report even when the user has not accepted the offer of a rewrite. A later rewrite can improve the supplied wording; the gap interview can settle missing content. Offer both after the report's closing questions.

## Readiness

Say that the brief is enough to write when the direction is settled, which is when all three hold:

- the angle (5), the sender's message (3) and the conclusion (9) each have an answer that is neither `[MISSING: …]` nor an unconfirmed `[SUGGESTED: …]`;
- questions 1–11 each have an answer, a confirmed or unconfirmed `[SUGGESTED: …]` counting as one outside those three. Question 1 counts as answered when its genre and its language are given; its other missing parts are reported but do not block;
- the chain check answers no *no* on the angle line (does the angle lie close to the reader, and does the hook carry it) or on the conclusion line (is the conclusion what the structure lands in, does it carry the message, and does it lie within the brand's mandate). A *no* on another line is reported and does not block.

Open research questions under question 12 never block. Where the brief is not yet enough, name what stands in the way as the questions that would settle it.

## Selection

Read the installed directories at run time: `$LIBRARY/references/editorial/genres/` and `$LIBRARY/references/editorial/techniques/`. Only lowercase-letter base filenames ending in `.md` are choices; review halves, README files, dotfiles and nested support are not. The filenames without extensions are the normalised values. The template's examples explain choices; they are not an installed inventory.

Map a genre the user names in any language against the installed filenames and each resource's `# <Name>` heading and opening paragraph, reading no further of an unselected resource. Load the selected genre's base resource only after it is settled. If the name maps ambiguously, ask or leave it missing; an inferred genre remains a suggestion until confirmed. Never default an unanswered question to `general`.

For a technique suggestion, read the resolved genre's ordinary technique first. Where it names an installed technique, suggest that and explain why. Where it names none, use question 7's tell-or-reason distinction to propose a choice, still subject to confirmation. Where the genre explicitly advises against a chosen technique, report the genre's reason once, as information; the choice stays the user's. An ordinary technique of `none` alone does not advise against an arc; selecting an installed arc there is legitimate.

The sketch reads one resource beside the genre: the selected technique's base resource for an installed technique. The genre's own form means no technique is chosen, and it is read from the genre:

- where the genre's ordinary technique is `none` and its own file states the order of its parts as its structure, as `pressrelease` does, that order is the form, sketched from the genre file;
- where the genre names an installed ordinary technique, as `report` and `teaser` do, that technique is the form: the sketch uses its one-sentence form and its resource;
- every other genre, `article`, `casestudy`, `column`, `opinion`, `webcopy` and `general` among them, has no form of its own to follow, so the sketch is a free-structure sketch. Load no support file the genre links; `/write` applies it when it writes.

An explicitly chosen free structure is `technique: none`, which names no resource. The genre's own form, chosen as such, is omitted from the map, with that choice stated under question 7, so `/write` resolves it from the genre. A tentative suggestion also stays out of the map. For a choice that cannot be found installed, retain the user's words with the missing question about a usable choice and omit its metadata value; never replace it with a guess.

Verify the language of question 1 through `uv run --no-cache --no-project "$LIBRARY/scripts/languages.py" resolve --scope=composition "<selector>"`. Use the returned `code` in the map. Where the text is to exist in several languages, only the source language goes into the map; how the other versions are produced stays in the answer. For an unlisted human description, interpret it, propose one candidate from the resolver's `list` command, and verify through the same `resolve` command. If no unique installed language can be established, ask or mark it missing and omit `language`; never take it from the brief's working language. The resolver's scope content is a terminal result, not a pointer to other language scopes.

## Markers

Keep the tokens English in every working language; write their explanations in that language. Use `[MISSING: <the question the user needs to answer>]` for a question or part with no answer, and `[SUGGESTED: <inference>]` for everything the Skill derives that the user has not confirmed. An unanswered question is a gap to fill, not a fault. No other marker exists: open research questions are plain text under question 12, and a suggestion is a remark in the conversation or report, never a mark on the answer.
